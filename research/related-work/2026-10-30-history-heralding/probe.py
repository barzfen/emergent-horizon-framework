"""EHF-RW-005: infer an initial cycle from a visible boundary crossing.

Exact event-entry and mean-waiting-time calculations; finite-time transition
probabilities computed numerically. No active cycle setter or resets assumed
for the non-overlapping event protocol. The observer and clock are specified.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import platform

import numpy as np
import scipy
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
DEP = HERE.parent / '2026-10-30-detection-access' / 'probe.py'
spec = importlib.util.spec_from_file_location('detection_probe', DEP)
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
model = previous.old
RATES = ['1/10', '1', '10']
LAGS = [0.001,0.01,0.1,0.3,1.,3.,10.,30.]


def trans(L, time):
    P = expm(-float(time)*np.array(L,dtype=float))
    assert P.min() >= -2e-12
    assert np.max(np.abs(P.sum(axis=1)-1)) < 2e-12
    return P


def jump_flux(L):
    # Uniform stationary law on 15 states: symmetry and irreducibility.
    # Observe the actual spatial jump 2->0, not merely two snapshots.
    fluxes = [F(0) for _ in range(15)]
    for k in range(3):
        for j in range(3):
            fluxes[j] += F(1,15)*(-L[6+k][j])
    total = sum(fluxes)
    posterior = [x/total for x in fluxes]
    assert total == F(1,30)
    assert posterior == [F(int(i==2)) for i in range(15)]
    return total, posterior


def mean_waits(L):
    # Kill the process at the target transition a=(2,2)->b=(0,2).
    # Remove just that off-diagonal rate; leave holding rates unchanged.
    a, b = 8, 2
    M = [row.copy() for row in L]
    M[a][b] = F(0)
    inv = model.old.inverse(M)
    h = [sum(row) for row in inv]
    assert all(x>0 for x in h)
    assert all(sum(M[i][j]*h[j] for j in range(15)) == 1 for i in range(15))
    assert h[b] == 30  # Mean interval between repeated event entries.
    assert np.max(np.abs(np.linalg.solve(np.array(M,dtype=float),np.ones(15))-
                         np.array(h,dtype=float))) < 1e-9
    return h


def snapshot_posterior(P):
    # At stationarity, condition on X(-lag)=2, X(0)=0, ignoring labels.
    weights = np.sum(P[0:3,6:9],axis=1)/15
    mass = float(weights.sum())
    return mass, weights/mass


def main():
    oldresults = json.loads((DEP.parent/'results.json').read_text())
    triads = [oldresults['triad_a'],oldresults['triad_c']]
    selected = oldresults['selected_simplified_operating_point']
    t, N = selected['time_at_max_gap_on_grid'],selected['sampling']['independent_trials']
    # Both triads have the same visible cycle membership for this edge.
    edge_memberships = [[k for k,c in enumerate(triad)
                         if any({c[i],c[(i+1)%5]}=={0,2} for i in range(5))]
                        for triad in triads]
    assert edge_memberships == [[2],[2]]
    result = {'probe':'EHF-RW-005','date':'2026-10-30',
        'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'dependency_sha256':hashlib.sha256(DEP.read_bytes()).hexdigest(),
        'input_results_sha256':hashlib.sha256((DEP.parent/'results.json').read_bytes()).hexdigest(),
        'triad_a':triads[0],'triad_c':triads[1],
        'observed_edge':[2,0],'edge_cycle_memberships':edge_memberships,
        'measurement_delay':t,'prospective_trial_count':N,
        'stationary_herald_flux':'1/30','event_posterior':'point mass at (position 0, cycle 2)',
        'event_rows':[],'snapshot_rows':[]}
    target = np.zeros(15);target[6:9]=1  # position 2, any label
    seed = np.zeros(15);seed[2]=1
    for rate in RATES:
        Ls = [model.lift(c,F(rate)) for c in triads]
        Ps = [trans(L,t) for L in Ls]
        heralded = []
        for name,L,P in zip(('A','C'),Ls,Ps):
            flux,posterior = jump_flux(L)
            p = float(target@P@np.array(posterior,dtype=float))
            h = mean_waits(L)
            end = P@seed
            # Dead-time protocol: wait t after each accepted herald, measure,
            # then wait for the first subsequent observed herald.
            wait_after_measurement = float(end@np.array(h,dtype=float))
            row = {'kappa':rate,'hypothesis':name,'event_flux':str(flux),
                   'post_event_state_probabilities':[str(x) for x in posterior],
                   'p_position2_at_delay':p,'mean_raw_herald_interval':str(h[2]),
                   'mean_wait_after_measurement':wait_after_measurement,
                   'mean_accepted_trial_interval':t+wait_after_measurement,
                   'mean_initial_wait_from_stationarity':float(sum(h)/15),
                   'mean_duration_N_trials_from_first_herald':t+(N-1)*(t+wait_after_measurement),
                   'mean_duration_N_trials_from_stationary_start':float(sum(h)/15)+t+(N-1)*(t+wait_after_measurement)}
            result['event_rows'].append(row)
            heralded.append(p)
            if rate == '1':
                expected = selected['p_a'] if name=='A' else selected['p_c']
                assert abs(p-expected)<2e-12
        for lag in LAGS:
            records = []
            for name,L,P in zip(('A','C'),Ls,Ps):
                Ppast = trans(L,lag)
                mass,post = snapshot_posterior(Ppast)
                start = np.zeros(15);start[:3]=post
                future = float(target@P@start)
                # Independent three-time joint probability via projection.
                prior = np.zeros(15);prior[6:9]=1/15
                mid = Ppast@prior;mid[3:]=0
                joint = float(target@P@mid)
                assert abs(joint-mass*future)<2e-14
                records.append({'hypothesis':name,'two_snapshot_record_probability':mass,
                    'posterior_cycles_at_position0':post.tolist(),
                    'future_position2_probability':future,
                    'three_time_joint_probability':joint})
            # Two-time position records alone are identical for this pair.
            assert abs(records[0]['two_snapshot_record_probability']-
                       records[1]['two_snapshot_record_probability'])<2e-13
            result['snapshot_rows'].append({'kappa':rate,'past_lag':lag,'future_lag':t,
                'records':records,
                'conditional_future_gap':abs(records[0]['future_position2_probability']-
                                             records[1]['future_position2_probability']),
                'unconditional_three_time_joint_gap':abs(records[0]['three_time_joint_probability']-
                                                        records[1]['three_time_joint_probability'])})
        print('kappa',rate,'event probabilities',heralded,'gap',abs(heralded[0]-heralded[1]),flush=True)
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Exact posterior, wait equations and three-time identities passed.')


if __name__ == '__main__':
    main()
