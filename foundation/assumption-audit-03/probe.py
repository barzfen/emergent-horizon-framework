"""Boundary-event writer included in a finite classical Markov state.

Copyright (c) 2026 Barry Fensom. SPDX-License-Identifier: MIT
Requires NumPy and SciPy. Exact rate checks plus numerical matrix exponentials.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform

import numpy as np
import scipy
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
TRIADS = {
    'A': [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 2, 4, 1, 3]],
    'C': [[0, 1, 2, 3, 4], [0, 1, 2, 4, 3], [0, 2, 3, 1, 4]],
}
TIMES = [0, 1, 3, 10, 30, 100]


def base_rates(triad, kappa):
    rates = [[F(0) for _ in range(15)] for _ in range(15)]
    for k, cycle in enumerate(triad):
        for i, v in enumerate(cycle):
            for neighbor in (cycle[(i-1) % 5], cycle[(i+1) % 5]):
                rates[3*v+k][3*neighbor+k] += F(1, 2)
            for j in range(3):
                if j != k:
                    rates[3*v+k][3*v+j] += kappa/2
    assert all(sum(row) == 1+kappa for row in rates)
    assert all(rates[x][y] == rates[y][x] for x in range(15) for y in range(15))
    return rates


def herald(x, y):
    return x//3 == 2 and y//3 == 0


def generator(rates, writer=True, down=F(0), up=F(0), flag=False):
    # Probe x, register m, and optional ground-truth event-history flag h.
    # h is for validation, not information supplied to the tested reader.
    hs = 2 if flag else 1
    states = [(x, m, h) for x in range(15) for m in range(2) for h in range(hs)]
    index = {s: i for i, s in enumerate(states)}
    q = [[F(0) for _ in states] for _ in states]
    for i, (x, m, h) in enumerate(states):
        for y, rate in enumerate(rates[x]):
            if not rate:
                continue
            event = herald(x, y)
            mm = 1 if writer and event else m
            hh = int(bool(h or event)) if flag else 0
            q[i][index[(y, mm, hh)]] += rate
        noise = down if m else up
        if noise:
            q[i][index[(x, 1-m, h)]] += noise
        q[i][i] -= sum(q[i])
    for i, (x, m, h) in enumerate(states):
        assert sum(q[i]) == 0
        assert all(q[i][j] >= 0 for j in range(len(states)) if j != i)
        # Writer and noise leave every marginal probe jump rate unchanged.
        for y in range(15):
            if y != x:
                assert sum(q[i][j] for j, s in enumerate(states) if s[0] == y) == rates[x][y]
    return q, states, index


def transition(q, time):
    p = expm(float(time)*np.array(q, dtype=float))
    assert p.min() > -3e-12
    assert np.max(np.abs(p.sum(axis=1)-1)) < 3e-11
    return p


def tv(a, b):
    return float(np.abs(a-b).sum()/2)


def killed_generator(rates):
    q = np.array(rates, dtype=float)
    q -= np.diag(q.sum(axis=1))
    for x in range(15):
        for y in range(15):
            if herald(x, y):
                q[x, y] = 0  # Keep diagonal: lost probability counts a herald.
    return q


def run():
    source = HERE.parents[1]/'research/related-work/2026-10-30-history-heralding/results.json'
    source_hash = None
    if source.exists():
        old = json.loads(source.read_text())
        assert TRIADS['A'] == old['triad_a'] and TRIADS['C'] == old['triad_c']
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    output = {'audit': 'EHF assumption audit 03', 'date': '2026-11-01',
              'python': platform.python_version(), 'numpy': np.__version__,
              'scipy': scipy.__version__, 'triads': TRIADS,
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'rw005_input_sha256_if_present': source_hash,
              'rows': [], 'retention': [], 'controls': {}}
    for name, triad in TRIADS.items():
        assert all(sorted(cycle) == list(range(5)) for cycle in triad)
        edge_sets = [{tuple(sorted((c[i], c[(i+1) % 5]))) for i in range(5)}
                     for c in triad]
        assert not set.intersection(*edge_sets)
        membership = [k for k, c in enumerate(triad)
                      if any({c[i], c[(i+1) % 5]} == {0, 2} for i in range(5))]
        assert membership == [2]
        for kappa in (F(1, 10), F(1), F(10)):
            rates = base_rates(triad, kappa)
            assert rates[8][2] == F(1, 2)
            assert sum(rates[x][y]/15 for x in range(15) for y in range(15)
                       if herald(x, y)) == F(1, 30)
            killed = killed_generator(rates)
            # Post-herald reset-free waiting cost (numerical linear solve).
            waits = np.linalg.solve(-killed, np.ones(15))
            assert abs(waits[2]-30) < 2e-10
            q0, s0, ix0 = generator(rates)
            if kappa != 1:
                continue  # Other rates validate structure; scans use kappa=1.
            # An actual event from a blank register writes 1; sham has same
            # current probe state but no preceding event, and remains blank.
            assert q0[ix0[(8, 0, 0)]][ix0[(2, 1, 0)]] == F(1, 2)
            assert q0[ix0[(8, 0, 0)]][ix0[(2, 0, 0)]] == 0
            for epsilon in (F(0), F(1, 100)):
                q, states, index = generator(rates, down=epsilon, up=epsilon, flag=True)
                init = np.zeros(len(states))
                for x in range(15):
                    init[index[(x, 0, 0)]] = 1/15
                for time in TIMES:
                    end = init @ transition(q, time)
                    cells = {(m, h): float(sum(end[i] for i, s in enumerate(states)
                                              if s[1:] == (m, h)))
                             for m in (0, 1) for h in (0, 1)}
                    event_probability = cells[0, 1]+cells[1, 1]
                    expected_event = 1-float(np.ones(15)/15 @ expm(time*killed) @ np.ones(15))
                    assert abs(event_probability-expected_event) < 4e-12
                    if epsilon == 0:
                        assert abs(cells[0, 1])+abs(cells[1, 0]) < 3e-12
                    no_event = cells[0, 0]+cells[1, 0]
                    false_positive = cells[1, 0]/no_event if no_event > 1e-14 else None
                    expected_fp = (1-np.exp(-2*float(epsilon)*time))/2
                    assert false_positive is not None and abs(false_positive-expected_fp) < 4e-12
                    output['rows'].append({'triad': name, 'kappa': '1', 'epsilon': str(epsilon),
                        'time': time, 'probability_event_has_occurred': event_probability,
                        'probability_register_is_1': cells[1, 0]+cells[1, 1],
                        'false_positive_given_no_event': false_positive,
                        'false_negative_given_event': cells[0, 1]/event_probability if event_probability > 1e-14 else None})
                # Memory of ONE earlier event vs a matched blank history.
                qr, sr, ir = generator(rates, down=epsilon, up=epsilon)
                memory_mask = np.array([int(s[1] == 1) for s in sr])
                for time in TIMES:
                    p = transition(qr, time)
                    written, blank = p[ir[(2, 1, 0)]], p[ir[(2, 0, 0)]]
                    full_tv = tv(written, blank)
                    memory_tv = abs(float((written-blank) @ memory_mask))
                    survival = float(expm(time*killed)[2].sum())
                    expected = survival*np.exp(-2*float(epsilon)*time)
                    assert abs(full_tv-expected) < 4e-12
                    assert abs(memory_tv-expected) < 4e-12
                    output['retention'].append({'triad': name, 'epsilon': str(epsilon),
                        'time_after_written_event': time, 'full_tv': full_tv,
                        'memory_only_tv': memory_tv, 'no_new_herald_probability': survival,
                        'balanced_success': (1+memory_tv)/2})
            # No coupling: blank remains blank even if the probe crosses.
            uncoupled, su, iu = generator(rates, writer=False)
            assert uncoupled[iu[(8, 0, 0)]][iu[(2, 0, 0)]] == F(1, 2)
            end = transition(uncoupled, 30)[iu[(8, 0, 0)]]
            assert sum(end[i] for i, s in enumerate(su) if s[1]) == 0
            # A bidirectional toggle is reversible on the joint graph but
            # two crossings restore blank: it records parity, not 'ever'.
            toggle = np.zeros((30, 30))
            for x in range(15):
                for m in (0, 1):
                    for y, rate in enumerate(rates[x]):
                        if rate:
                            edge_crossing = {x//3, y//3} == {0, 2}
                            toggle[2*x+m, 2*y+(m ^ int(edge_crossing))] += float(rate)
            toggle -= np.diag(toggle.sum(axis=1))
            assert np.max(np.abs(toggle-toggle.T)) == 0
            assert toggle[2*8, 2*2+1] == .5 and toggle[2*2+1, 2*8] == .5
            output['controls'][name] = {'uncoupled_writer_never_writes': True,
                'toggle_joint_generator_symmetric': True,
                'toggle_two_crossing_record': [0, 1, 0],
                'latch_two_crossing_record': [0, 1, 1],
                'mean_next_directed_herald_after_herald': float(waits[2]),
                'stationary_herald_flux': '1/30'}
    output['all_assertions_passed'] = True
    (HERE/'results.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({'controls': output['controls'],
                      'selected_acquisition': [r for r in output['rows'] if r['triad']=='A' and r['time'] in (10, 30, 100)],
                      'selected_retention': [r for r in output['retention'] if r['triad']=='A' and r['time_after_written_event'] in (10, 30, 100)],
                      'all_assertions_passed': True}, indent=2))


if __name__ == '__main__':
    run()
