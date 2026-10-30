"""EHF-RW-004: operational detectability of RW-003's matched N=5 pair.

Finite-matrix probabilities (floating point), independently checked against
matrix exponentiation and exact rational resolvents. Sample counts are
prospective binomial calculations, not simulated experiments or new data.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import platform

import numpy as np
import scipy
from scipy.linalg import expm
from scipy.stats import binom

HERE = Path(__file__).resolve().parent
DEP = HERE.parent / '2026-10-30-cycle-aware-boundary' / 'probe.py'
spec = importlib.util.spec_from_file_location('cycle_probe', DEP)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
TIMES = np.geomspace(0.001, 1000., 601)
RATES = ['0', '1/100', '3/100', '1/10', '3/10', '1', '3', '10', '30', '100']
ALPHA = 0.05
N_GRID = [int(m * 10**j) for j in range(0, 10) for m in (1, 2, 5)]


def vector(v, labels, value=1.):
    x = np.zeros(15)
    for k in labels:
        x[3*v+k] = value
    return x


E0, E1 = vector(0, [0]), vector(0, [1])
E2 = vector(0, [2])
U0 = vector(0, range(3), 1/3)
POS0 = vector(0, range(3))
PROTOCOLS = {
    'prepare0_read1': (E0, E1),
    'prepare0_read_position': (E0, POS0),
    'uniform_prepare_read1': (U0, E1),
    'uniform_prepare_read_position': (U0, POS0),
    'prepare0_read_same_label': (E0, E0),
    'prepare0_read_other_labels': (E0, vector(0, [1, 2])),
    'prepare2_read_position': (E2, POS0),
    'prepare2_read_position1': (E2, vector(1, range(3))),
    'prepare2_read_position2': (E2, vector(2, range(3))),
    'uniform_prepare_read2': (U0, vector(0, [2])),
    'uniform_prepare_position1_read2': (U0, vector(1, [2])),
    'uniform_prepare_position2_read2': (U0, vector(2, [2])),
    'uniform_prepare_read_position1': (U0, vector(1, range(3))),
    'uniform_prepare_read_position2': (U0, vector(2, range(3))),
}


def eig(L):
    a = np.array(L, dtype=float)
    vals, vecs = np.linalg.eigh(a)
    assert vals.min() > -1e-12
    vals[np.abs(vals) < 1e-12] = 0
    return vals, vecs


def probability_curve(spectrum, initial, detector):
    vals, vecs = spectrum
    weights = (detector @ vecs) * (initial @ vecs)
    p = weights @ np.exp(-vals[:, None] * TIMES)
    assert p.min() >= -1e-12 and p.max() <= 1+1e-12
    return np.clip(p, 0., 1.)


def sample_plan(pa, pc):
    """First feasible N on a declared 1-2-5 grid, never a minimum-N claim.

    Equal numbers of independent Bernoulli trials under either simple known
    hypothesis. Return a count threshold with both errors <= 0.05.
    """
    lo, hi = sorted((float(pa), float(pc)))
    gap = hi-lo
    if gap < 1e-12:
        return {'detectable_at_numeric_resolution': False}
    for n in N_GRID:
        threshold = int(binom.ppf(1-ALPHA, n, lo)) + 1
        error_lo = float(binom.sf(threshold-1, n, lo))
        error_hi = float(binom.cdf(threshold-1, n, hi))
        if error_lo <= ALPHA+1e-12 and error_hi <= ALPHA+1e-12:
            return {'detectable_at_numeric_resolution': True,
                    'independent_trials': n, 'declare_high_if_count_at_least': threshold,
                    'high_probability_hypothesis': 'A' if pa > pc else 'C',
                    'error_under_low': error_lo, 'error_under_high': error_hi,
                    'midpoint_hoeffding_sufficient_trials': math.ceil(2*math.log(1/ALPHA)/gap**2)}
    return {'detectable_at_numeric_resolution': True, 'feasible_trial_count_not_found_on_grid': True}


def main():
    inputs = json.loads((DEP.parent/'moment_checks.json').read_text())
    triads = [inputs['triad_a'], inputs['triad_b']]
    result = {'probe': 'EHF-RW-004', 'date': '2026-10-30',
        'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__,
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'dependency_sha256': hashlib.sha256(DEP.read_bytes()).hexdigest(),
        'matched_input_sha256': hashlib.sha256((DEP.parent/'moment_checks.json').read_bytes()).hexdigest(),
        'triad_a': triads[0], 'triad_c': triads[1],
        'rate_grid': RATES, 'time_grid': {'kind':'geometric', 'min':0.001, 'max':1000, 'count':601},
        'max_error_target_per_hypothesis': ALPHA,
        'trial_count_grid': N_GRID, 'access_rows': [], 'noise_rows': []}
    cache = {}
    discrepancies = []
    for rate in RATES:
        ls = [old.lift(t, F(rate)) for t in triads]
        spectra = [eig(L) for L in ls]
        cache[rate] = spectra
        for name, (initial, detector) in PROTOCOLS.items():
            a, c = [probability_curve(s, initial, detector) for s in spectra]
            delta = np.abs(a-c)
            j = int(np.argmax(delta))
            row = {'kappa': rate, 'protocol': name, 'time_at_max_gap_on_grid': float(TIMES[j]),
                   'max_probability_gap_on_grid': float(delta[j]),
                   'p_a': float(a[j]), 'p_c': float(c[j]),
                   'sampling': sample_plan(a[j], c[j])}
            result['access_rows'].append(row)
            if name == 'prepare0_read1': print(rate, 'best gap', delta[j], 'at', TIMES[j], flush=True)
        # Independent expm checks at predefined times, including the two
        # main simplified protocols; no eigenbasis code used in expm path.
        for L, spectrum in zip(ls, spectra):
            Lf = np.array(L, dtype=float)
            vals, vecs = spectrum
            for t in (0.01, 1., 10.):
                P1 = (vecs * np.exp(-t*vals)) @ vecs.T
                P2 = expm(-t*Lf)
                discrepancies.append(float(np.max(np.abs(P1-P2))))
                assert np.max(np.abs(P1-P2)) < 2e-12
                assert np.max(np.abs(P2.sum(axis=1)-1)) < 2e-12
                assert P2.min() >= -2e-12
            R_exact = np.array(old.resolvent(L), dtype=float)
            R_spectral = (vecs * (1/(1+vals))) @ vecs.T
            assert np.max(np.abs(R_exact-R_spectral)) < 2e-12
    # Exact resolvent check of all access protocols at z=1 and four rates.
    result['exact_resolvent_access_checks'] = []
    for rate in ('0', '1/10', '1', '10'):
        Rs = [old.resolvent(old.lift(t, F(rate))) for t in triads]
        for name, (initial, detector) in PROTOCOLS.items():
            def rational(v):
                return [F(1,3) if abs(x-1/3)<1e-12 else F(int(round(x))) for x in v]
            iv, dv = rational(initial), rational(detector)
            p = [sum(dv[i]*R[i][j]*iv[j] for i in range(15) for j in range(15)) for R in Rs]
            result['exact_resolvent_access_checks'].append({'kappa':rate, 'protocol':name,
                'a':str(p[0]), 'c':str(p[1]), 'difference':str(p[0]-p[1])})
    # Choose one operating protocol using the theoretical grid; no sampled
    # data are used for tuning. Freeze this before future validation trials.
    candidates = [r for r in result['access_rows'] if r['protocol']=='prepare0_read1']
    selected = max(candidates, key=lambda r:r['max_probability_gap_on_grid'])
    result['selected_operating_point'] = selected
    simple = max((r for r in result['access_rows'] if r['protocol'].startswith('prepare2_read_position')),
                 key=lambda r:r['max_probability_gap_on_grid'])
    result['selected_simplified_operating_point'] = simple
    result['simplified_preparation_noise'] = []
    si, sd = PROTOCOLS[simple['protocol']]
    sj = int(np.argmin(np.abs(TIMES-simple['time_at_max_gap_on_grid'])))
    for epsilon in (0., 0.1, 0.3, 0.5, 1.):
        initial = (1-epsilon)*si + epsilon*U0
        ps = [float(probability_curve(s, initial, sd)[sj]) for s in cache[simple['kappa']]]
        result['simplified_preparation_noise'].append({'preparation_replacement_probability':epsilon,
            'p_a':ps[0], 'p_c':ps[1], 'gap':abs(ps[0]-ps[1]), 'sampling':sample_plan(*ps)})
    kappa, t = selected['kappa'], selected['time_at_max_gap_on_grid']
    Ps = []
    for s in cache[kappa]:
        vals, vecs = s
        Ps.append((vecs*np.exp(-vals*t)) @ vecs.T)
    # Imperfect preparation: replace the intended cycle by a uniform draw
    # with probability epsilon. Readout: replace label by a uniform label
    # with probability eta; position detection remains perfect.
    for epsilon in (0., 0.1, 0.3, 0.5, 1.):
        for eta in (0., 0.1, 0.3, 0.5, 1.):
            initial = (1-epsilon)*E0 + epsilon*U0
            detector = (1-eta)*E1 + eta*POS0/3
            pa, pc = [float(detector @ P @ initial) for P in Ps]
            result['noise_rows'].append({'preparation_replacement_probability':epsilon,
                'readout_replacement_probability':eta, 'kappa':kappa, 'time':t,
                'p_a':pa, 'p_c':pc, 'gap':abs(pa-pc), 'sampling':sample_plan(pa,pc)})
    result['validation'] = {'max_expm_spectral_difference':max(discrepancies),
        'matrix_exponential_checks':len(discrepancies),
        'exact_resolvent_check_all_rates':True,
        'no_monte_carlo_used':True}
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('SELECTED', selected, flush=True)
    print('SIMPLIFIED', simple, flush=True)


if __name__ == '__main__':
    main()
