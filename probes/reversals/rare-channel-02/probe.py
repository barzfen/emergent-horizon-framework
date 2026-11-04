"""Symmetric-rate sensitivity on a fixed MICRO/Pi component. Python 3, numpy, scipy."""
from collections import Counter
from itertools import permutations
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq


def canon(c):
    c = tuple(c)
    k = c.index(0)
    c = c[k:] + c[:k]
    return min(c, c[:1] + c[:0:-1])


def reversal(c, start, length):
    a = list(c)
    ix = [(start + j) % len(c) for j in range(length)]
    for i, v in zip(ix, reversed([c[j] for j in ix])):
        a[i] = v
    return canon(a)


def pi(c):
    return frozenset(c[::2])


def walls(c, ones):
    return sum((a in ones) != (b in ones) for a, b in zip(c, c[1:] + c[:1]))


def valid(c, ones):
    return all((c[i] in ones) in ((c[i-1] in ones), (c[(i+1) % len(c)] in ones)) for i in range(len(c)))


def cycle_edges(c):
    return {frozenset((a, b)) for a, b in zip(c, c[1:] + c[:1])}


def component(start, neighbours):
    seen = {start}
    stack = [start]
    while stack:
        c = stack.pop()
        for d in neighbours[c]:
            if d not in seen:
                seen.add(d)
                stack.append(d)
    return seen


def laplacian(size, pairs):
    out = np.zeros((size, size))
    for i, j in pairs:
        out[i, i] += 1
        out[j, j] += 1
        out[i, j] -= 1
        out[j, i] -= 1
    return out


def run():
    n, ones = 9, {1, 2, 3, 4}
    seed = tuple(range(n))
    candidates = {(0,) + p for p in permutations(range(1, n)) if p[0] < p[-1]
                  and pi((0,) + p) == pi(seed) and valid((0,) + p, ones)}
    neighbours = {c: set() for c in candidates}
    support = {}
    for c in candidates:
        for length in (2, 3, 4):  # complementary lengths cover 2..7
            for start in range(n):
                d = reversal(c, start, length)
                if d in candidates and d != c:
                    neighbours[c].add(d)
                    pair = tuple(sorted((c, d)))
                    support[pair] = min(support.get(pair, n), length)
    states = sorted(component(seed, neighbours))
    index = {c: i for i, c in enumerate(states)}
    pairs = {tuple(sorted((index[c], index[d]))): support[tuple(sorted((c, d)))]
             for c in states for d in neighbours[c]}
    fast = sorted(pair for pair, length in pairs.items() if length <= 3)
    slow = sorted(pair for pair, length in pairs.items() if length == 4)
    for i, j in pairs:
        # Every nontrivial segment reversal has the same two-edge reconnection cost.
        assert len(cycle_edges(states[i]) - cycle_edges(states[j])) == 2
        assert len(cycle_edges(states[j]) - cycle_edges(states[i])) == 2
    L0, L1 = laplacian(len(states), fast), laplacian(len(states), slow)
    fast_neighbours = {i: set() for i in range(len(states))}
    for i, j in fast:
        fast_neighbours[i].add(j)
        fast_neighbours[j].add(i)
    groups = []
    assigned = set()
    for i in range(len(states)):
        if i not in assigned:
            g = sorted(component(i, fast_neighbours))
            groups.append(g)
            assigned.update(g)
    blocks = np.zeros((len(states), len(groups)))
    for j, group in enumerate(groups):
        blocks[group, j] = 1 / np.sqrt(len(group))
    reduced_L = blocks.T @ L1 @ blocks
    reduced_eigenvalues = eigh(reduced_L, eigvals_only=True)
    assert reduced_eigenvalues[1] > 0
    A = np.array([walls(c, ones) == 2 for c in states])
    assert set(walls(c, ones) for c in states) == {2, 4}
    equilibrium = float(np.mean(A))
    f = A.astype(float) - equilibrium
    norm = float(f @ f)
    positive_fast = eigh(L0, eigvals_only=True)
    fast_gap = float(min(x for x in positive_fast if x > 1e-9))
    rows = []
    for epsilon in (1., .1, .01, .001, .0001):
        L = L0 + epsilon * L1
        values, vectors = eigh(L)
        assert abs(values[0]) < 1e-10 and values[1] > 0
        assert np.max(np.abs(L.sum(axis=1))) < 1e-10
        weights = (vectors[:, 1:].T @ f) ** 2 / norm
        assert abs(sum(weights) - 1) < 1e-9
        def correlation(t):
            return float(weights @ np.exp(-values[1:] * t))
        integrated = float(weights @ (1 / values[1:]))
        hi = 1.
        while correlation(hi) > .5:
            hi *= 2
        half = float(brentq(lambda t: correlation(t) - .5, 0, hi))
        h = np.linalg.solve(L[np.ix_(A, A)], np.ones(int(np.sum(A))))
        assert np.max(np.abs(L[np.ix_(A, A)] @ h - 1)) < 1e-8
        cross_rates = -np.sum(L[np.ix_(A, ~A)], axis=1)
        cross_back = -np.sum(L[np.ix_(~A, A)], axis=1)
        rows.append({'epsilon': epsilon, 'gap': float(values[1]),
            'gap_over_epsilon': float(values[1] / epsilon),
            'integrated_wall_correlation_time': integrated,
            'epsilon_times_integrated_time': epsilon * integrated,
            'wall_correlation_half_time': half,
            'mean_first_exit_from_two_wall_set': float(np.mean(h)),
            'first_exit_range': [float(min(h)), float(max(h))],
            'two_wall_cross_rate_range': [float(min(cross_rates)), float(max(cross_rates))],
            'four_wall_cross_rate_range': [float(min(cross_back)), float(max(cross_back))],
            'correlation_at_times': {str(t): correlation(t) for t in (0, 1, 10, 100, 1000)},
            'correlation_at_slow_times': {str(t): correlation(t / epsilon) for t in (.1, 1, 10)}})
    zero_group_means = np.array([np.mean(f[g]) for g in groups])
    variance_of_group_mean = sum(len(g) * zero_group_means[j]**2 for j, g in enumerate(groups)) / len(states)
    assert abs(variance_of_group_mean - norm / len(states)) < 1e-12
    out = {'n': n, 'ones': sorted(ones), 'seed': seed, 'Pi': sorted(pi(seed)),
           'states': len(states), 'fast_edges': len(fast), 'slow_edges': len(slow),
           'fast_components': len(groups), 'fast_component_sizes': dict(sorted(Counter(map(len, groups)).items())),
           'wall_histogram': dict(sorted(Counter(walls(c, ones) for c in states).items())),
           'equilibrium_two_wall_probability': equilibrium,
           'projected_slow_gap': float(reduced_eigenvalues[1]),
           'smallest_positive_fast_gap': fast_gap,
           'fast_groups_wall_counts': [sorted({walls(states[i], ones) for i in g}) for g in groups],
           'zero_epsilon': {'components': len(groups), 'wall_correlation': 1, 'first_exit': 'infinite'},
           'rates': 'continuous-time symmetric per-distinct-edge rates: 1 for minimal support 2 or 3, epsilon for minimal support 4',
           'initial_condition': 'uniform on all two-wall states in the selected component',
           'rows': rows, 'carrier': {'states': states, 'fast_edges': fast, 'slow_edges': slow,
                                    'fast_groups': groups},
           'probe_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    return out


if __name__ == '__main__':
    out = run()
    Path(__file__).with_name('results.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'carrier'}, indent=2))
