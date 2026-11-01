"""Reversible probe-gated structural writing, with no writer shutoff.

Copyright (c) 2026 Barry Fensom. SPDX-License-Identifier: MIT
AI-assisted finite classical model. Requires NumPy and SciPy.
"""
from collections import deque
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform

import numpy as np
import scipy
from scipy.linalg import eigh, expm

HERE = Path(__file__).resolve().parent
A = ((0, 1, 2, 3, 4), (0, 1, 2, 3, 4), (0, 2, 4, 1, 3))
B = ((0, 1, 3, 2, 4), A[1], A[2])
TRIADS = (A, B)
STATES = [(s, v, k) for s in range(2) for v in range(5) for k in range(3)]
IX = {s: i for i, s in enumerate(STATES)}
TIMES = (0, .1, 1, 3, 10, 30, 100)


def edges(c):
    return {tuple(sorted((c[i], c[(i+1) % 5]))) for i in range(5)}


def solve_exact(matrix, rhs):
    n = len(rhs)
    aug = [list(row)+[rhs[i]] for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[pivot] = aug[pivot], aug[j]
        scale = aug[j][j]
        aug[j] = [x/scale for x in aug[j]]
        for i in range(n):
            if i != j and aug[i][j]:
                scale = aug[i][j]
                aug[i] = [a-scale*b for a, b in zip(aug[i], aug[j])]
    solution = [row[-1] for row in aug]
    assert all(sum(row[j]*solution[j] for j in range(n)) == rhs[i]
               for i, row in enumerate(matrix))
    return solution


def generator(kappa, leakage):
    q = [[F(0) for _ in STATES] for _ in STATES]
    for i, (s, v, k) in enumerate(STATES):
        cycle = TRIADS[s][k]
        pos = cycle.index(v)
        for w in (cycle[(pos-1) % 5], cycle[(pos+1) % 5]):
            # Both directions of the boundary edge cause the same allowed
            # structural involution; reverse joint transitions have equal rates.
            ss = 1-s if {v, w} == {0, 2} else s
            assert tuple(sorted((v, w))) in edges(TRIADS[ss][k])
            q[i][IX[(ss, w, k)]] += F(1, 2)
        for kk in range(3):
            if kk != k:
                q[i][IX[(s, v, kk)]] += kappa/2
        if leakage:
            q[i][IX[(1-s, v, k)]] += leakage
        q[i][i] = -sum(q[i])
    assert all(sum(row) == 0 for row in q)
    assert all(q[i][j] == q[j][i] for i in range(30) for j in range(30))
    assert all(q[i][j] >= 0 for i in range(30) for j in range(30) if i != j)
    reached = {0}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in range(30):
            if j != i and q[i][j] and j not in reached:
                reached.add(j)
                queue.append(j)
    assert len(reached) == 30
    return q


def run():
    for triad in TRIADS:
        assert all(sorted(c) == list(range(5)) for c in triad)
        assert not set.intersection(*(edges(c) for c in triad))
        assert [k for k, c in enumerate(triad) if (0, 2) in edges(c)] == [2]
    result = {'audit': 'EHF assumption audit 05', 'date': '2026-11-01',
              'python': platform.python_version(), 'numpy': np.__version__,
              'scipy': scipy.__version__, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'triad_A': A, 'triad_B': B, 'joint_states': len(STATES),
              'rates_and_costs': [], 'retention': [], 'idle_false_writes': []}
    post_event = IX[(1, 0, 2)]
    matched_blank = IX[(0, 0, 2)]
    memory = np.array([int(s[0] == 1) for s in STATES])
    for kappa in (F(1, 10), F(1), F(10)):
        for leakage in (F(0), F(1, 100)):
            q = generator(kappa, leakage)
            assert q[IX[(0, 2, 2)]][post_event] == F(1, 2)
            assert q[post_event][IX[(0, 2, 2)]] == F(1, 2)
            # With no leakage, the gate is closed away from edge endpoints
            # in cycle 2. This is an instantaneous rate statement, not a
            # permanent isolation statement about future probe motion.
            for i, (s, v, k) in enumerate(STATES):
                hazard = sum(q[i][j] for j, t in enumerate(STATES) if t[0] != s)
                assert hazard == leakage + (F(1, 2) if k == 2 and v in (0, 2) else 0)
            # First reset is the first exit from structural sector B.
            sub = [[-q[i][j] for j in range(15, 30)] for i in range(15, 30)]
            waits = solve_exact(sub, [F(1)]*15)
            h = waits[post_event-15]
            stationary_start_wait = sum(waits)/15
            # Both structural sectors have equal mass; flip flux counts all
            # four directed coupled transitions (and leakage if enabled).
            flip_flux = sum(q[i][j]/30 for i, s in enumerate(STATES)
                            for j, t in enumerate(STATES) if s[0] != t[0])
            assert flip_flux == F(1, 15)+leakage
            result['rates_and_costs'].append({'kappa': str(kappa), 'leakage': str(leakage),
                'joint_generator_symmetric_and_connected': True,
                'initial_reverse_event_rate': '1/2',
                'probability_next_jump_is_reverse_crossing': str(F(1, 2)/(1+kappa+leakage)),
                'mean_first_reset_from_post_event': str(h),
                'mean_first_flip_from_uniform_probe': str(stationary_start_wait),
                'stationary_all_flip_flux': str(flip_flux),
                'mean_interval_between_all_stationary_flips': str(1/flip_flux)})
            qn = np.array(q, dtype=float)
            ev, u = eigh(qn)
            assert np.count_nonzero(np.abs(ev) < 1e-12) == 1
            for time in TIMES:
                p = np.eye(30) if time == 0 else (u*np.exp(time*ev)) @ u.T
                assert p.min() > -2e-13
                assert np.max(np.abs(p.sum(axis=1)-1)) < 3e-12
                written, blank = p[post_event], p[matched_blank]
                carrier_tv = abs(float((written-blank) @ memory))
                full_tv = float(np.abs(written-blank).sum()/2)
                assert carrier_tv <= full_tv+2e-12
                survival = float(expm(-float(time)*np.array(sub, dtype=float))[post_event-15].sum())
                current_b = float(written @ memory)
                assert survival <= current_b+3e-12
                result['retention'].append({'kappa': str(kappa), 'leakage': str(leakage),
                    'time': time, 'probability_carrier_currently_B': current_b,
                    'probability_no_reset_has_yet_occurred': survival,
                    'carrier_only_tv_between_written_and_blank': carrier_tv,
                    'carrier_only_balanced_success': (1+carrier_tv)/2,
                    'full_state_tv': full_tv, 'full_state_balanced_success': (1+full_tv)/2})
                idle = np.zeros(30); idle[:15] = 1/15
                result['idle_false_writes'].append({'kappa': str(kappa), 'leakage': str(leakage),
                    'time': time, 'probability_carrier_is_B': float(idle @ p @ memory)})
                if time == 3:
                    assert np.max(np.abs(p-expm(time*qn))) < 4e-13
            if kappa == 1 and leakage == 0:
                # Before any motion leaves the immediate post-write state,
                # an elementary race gives 1/4 immediate reverse probability.
                assert F(1, 2)/(1+kappa) == F(1, 4)
    result['all_assertions_passed'] = True
    (HERE/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'costs': result['rates_and_costs'],
        'retention_kappa_1_no_leakage': [r for r in result['retention'] if r['kappa']=='1' and r['leakage']=='0'],
        'idle_kappa_1_no_leakage': [r for r in result['idle_false_writes'] if r['kappa']=='1' and r['leakage']=='0'],
        'all_assertions_passed': True}, indent=2))


if __name__ == '__main__':
    run()
