"""Exhaustive finite reachability audit; Python standard library only.

Run from any directory: python3 probe.py. No Monte Carlo or random seeds.
Graphs are simple and undirected. Cycle labels remain distinct unless stated.
"""
from collections import Counter, deque
from itertools import permutations, product, combinations
from pathlib import Path
import hashlib
import json
import math
import platform

HERE = Path(__file__).resolve().parent


def canon_cycle(p):
    p = tuple(p)
    i = p.index(0)
    q = p[i:] + p[:i]
    return min(q, q[:1] + q[:0:-1])


def cycles(n):
    return [(0,) + p for p in permutations(range(1, n)) if p[0] < p[-1]]


def edges(p, closed=False):
    pairs = list(zip(p, p[1:]))
    if closed:
        pairs.append((p[-1], p[0]))
    return frozenset(tuple(sorted(e)) for e in pairs)


def cycle_neighbors(p, rule):
    n = len(p)
    lengths = {'LR2': (2,), 'LR3': (3,), 'LR23': (2, 3),
               '2opt': tuple(range(2, n - 1))}[rule]
    out = set()
    for length in lengths:
        for start in range(n):
            ix = [(start + j) % n for j in range(length)]
            q = list(p)
            for j, k in enumerate(ix):
                q[k] = p[ix[length - 1 - j]]
            q = canon_cycle(q)
            if q != p:
                out.add(q)
    return out


def components(states, neighbors):
    unseen = set(states)
    sizes = []
    witnesses = []
    while unseen:
        s = min(unseen)
        witnesses.append(s)
        unseen.remove(s)
        queue = deque([s])
        count = 0
        while queue:
            s = queue.popleft()
            count += 1
            for t in neighbors(s):
                if t in unseen:
                    unseen.remove(t)
                    queue.append(t)
        sizes.append(count)
    return {'states': len(states), 'components': len(sizes),
            'component_size_histogram': dict(sorted(Counter(sizes).items())),
            'representatives_first_two': witnesses[:2]}


def audit_paths(n, kind):
    if kind == 'complete':
        graph = set(combinations(range(n), 2))
    elif kind == 'squared_path':
        graph = {(i, j) for i in range(n) for j in range(i + 1, n) if j - i <= 2}
    elif kind == 'clique_two_leaves':
        # Clique on 0..n-3 with leaves n-2 and n-1 at 0 and 1.
        graph = set(combinations(range(n - 2), 2)) | {(0, n - 2), (1, n - 1)}
    else:
        # Paper section 7: A_m(H_2), with m=1 or 2.
        m = (n - 6) // 2
        assert kind == 'paper_lift_H2' and n in (8, 10)
        graph = (set(combinations(range(4), 2)) - {(0, 1)}) | {(0, 4), (1, 5)}
        graph |= {tuple(sorted((s, v))) for s in range(6, 6 + m)
                  for v in list(range(6)) + list(range(6 + m, n))}
    def canon(p):
        p = tuple(p)
        return min(p, p[::-1])
    adjacency = {i: {j for j in range(n) if tuple(sorted((i, j))) in graph} for i in range(n)}
    def extend(p):
        if len(p) == n:
            if p < p[::-1]:
                yield p
            return
        for v in sorted(adjacency[p[-1]] - set(p)):
            yield from extend(p + (v,))
    states = {p for i in range(n) for p in extend((i,))}
    def neighbors(p):
        out = set()
        for q in (p, p[::-1]):
            for j in range(2, n):
                if tuple(sorted((q[0], q[j]))) in graph:
                    # Add endpoint--q[j], remove q[j-1]--q[j].
                    out.add(canon(q[:j][::-1] + q[j:]))
        out.discard(p)
        return out
    for p in states:
        for q in neighbors(p):
            assert q in states and p in neighbors(q)
            assert len(edges(p) ^ edges(q)) == 2
    result = components(states, neighbors)
    result.update(n=n, graph=kind, host_edges=len(graph))
    if kind in ('complete', 'squared_path'):
        assert result['components'] == 1
    elif kind == 'clique_two_leaves':
        assert result['states'] == result['components'] == math.factorial(n - 4)
    else:
        assert result['components'] >= 2
        for p in states:
            internal = edges(p) & set(combinations(range(6), 2))
            assert all((edges(q) & set(combinations(range(6), 2))) == internal for q in neighbors(p))
        result['paper_internal_path_invariant_checked'] = True
    return result


def audit_cycles(n, rule):
    states = cycles(n)
    assert len(states) == math.factorial(n - 1) // 2
    adj = {p: cycle_neighbors(p, rule) for p in states}
    for p, ns in adj.items():
        for q in ns:
            assert q in adj and p in adj[q]
            assert len(edges(p, True) ^ edges(q, True)) == 4
    result = components(states, adj.__getitem__)
    result.update(n=n, rule=rule)
    if rule in ('LR2', 'LR23', '2opt'):
        assert result['components'] == 1
    return result


def audit_triads(n):
    tours = cycles(n)
    index = {p: i for i, p in enumerate(tours)}
    edge_index = {e: i for i, e in enumerate(combinations(range(n), 2))}
    masks = [sum(1 << edge_index[e] for e in edges(p, True)) for p in tours]
    states = {s for s in product(range(len(tours)), repeat=3)
              if not (masks[s[0]] & masks[s[1]] & masks[s[2]])}
    rows = []
    for rule in ('LR2', 'LR3', 'LR23', '2opt'):
        adj = [[index[q] for q in cycle_neighbors(p, rule)] for p in tours]
        def neighbors(s):
            for k in range(3):
                others = masks[s[(k + 1) % 3]] & masks[s[(k + 2) % 3]]
                for j in adj[s[k]]:
                    if not (masks[j] & others):
                        yield s[:k] + (j,) + s[k + 1:]
        # All accepted moves checked for validity and reverse accessibility.
        frozen = 0
        for s in states:
            ns = list(neighbors(s))
            frozen += not ns
            for t in ns:
                assert t in states and s in set(neighbors(t))
        result = components(states, neighbors)
        result.update(n=n, rule=rule, frozen_states=frozen,
                      representation='ordered cycle triple; each tour modulo rotation/reflection')
        if n % 2 == 0 and rule == 'LR3':
            def partition(p):
                return tuple(sorted((tuple(sorted(p[::2])), tuple(sorted(p[1::2])))))
            signatures = {tuple(partition(tours[i]) for i in s) for s in states}
            result['alternating_partition_signatures'] = len(signatures)
            result['components_beyond_signature_count'] = result['components'] - len(signatures)
        # Quotient by cycle-label permutation; moves descend by symmetry.
        quotient = {tuple(sorted(s)) for s in states}
        quotient_result = components(quotient, lambda s: {tuple(sorted(t)) for t in neighbors(s)})
        result['cycle_label_quotient'] = quotient_result
        result['representative_tours_first_two'] = [[tours[i] for i in s]
                                                   for s in result['representatives_first_two']]
        rows.append(result)
        print('triad', n, rule, result['states'], result['components'],
              'unlabelled', quotient_result['components'], flush=True)
    return rows


def main():
    result = {'probe': 'EHF-RW-001', 'date': '2026-10-30',
              'python': platform.python_version(),
              'method': 'exhaustive enumeration and breadth-first components; simple unweighted move graph',
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'path_controls': [], 'single_cycles': [], 'triads': []}
    for n in range(4, 9):
        for kind in ('complete', 'squared_path'):
            result['path_controls'].append(audit_paths(n, kind))
    for n in range(6, 9):
        result['path_controls'].append(audit_paths(n, 'clique_two_leaves'))
    for n in (8, 10):
        result['path_controls'].append(audit_paths(n, 'paper_lift_H2'))
    for n in range(4, 9):
        for rule in ('LR2', 'LR3', 'LR23', '2opt'):
            result['single_cycles'].append(audit_cycles(n, rule))
    for n in (4, 5, 6):
        result['triads'].extend(audit_triads(n))
    (HERE / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Saved', HERE / 'results.json')


if __name__ == '__main__':
    main()
