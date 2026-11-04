"""Exhaustive MICRO reversal graphs; Python 3, NumPy, SciPy. No rates or energies."""
from pathlib import Path
from itertools import permutations
from collections import Counter
import hashlib
import json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

MODELS = ('OPW3', 'OPW23', 'all_Pi', 'all_MICRO')


def canonical(c):
    c = tuple(c)
    k = c.index(0)
    c = c[k:] + c[:k]
    return min(c, c[:1] + c[:0:-1])


def reverse(c, start, length):
    a = list(c)
    slots = [(start + j) % len(c) for j in range(length)]
    for slot, value in zip(slots, reversed([c[j] for j in slots])):
        a[slot] = value
    return canonical(a)


def partition(c):
    return sum(1 << v for v in c[::2])


def components(count, edges):
    if len(edges):
        a, b = edges.T
        graph = coo_matrix((np.ones(2 * len(a), dtype=np.int8),
                            (np.r_[a, b], np.r_[b, a])), shape=(count, count)).tocsr()
    else:
        graph = coo_matrix((count, count)).tocsr()
    nc, labels = connected_components(graph, directed=False)
    sizes = np.bincount(labels)
    return {'edges': len(edges), 'components': int(nc),
            'largest': int(max(sizes)) if count else 0,
            'isolated': int(np.sum(np.diff(graph.indptr) == 0)),
            'component_sizes': dict(sorted(Counter(map(int, sizes)).items()))}, labels


def run(n):
    states = [(0,) + p for p in permutations(range(1, n)) if p[0] < p[-1]]
    index = {c: i for i, c in enumerate(states)}
    pi = np.array([partition(c) for c in states])
    by_length = {length: set() for length in range(2, n - 1)}
    for i, c in enumerate(states):
        for length in by_length:
            for start in range(n):
                d = reverse(c, start, length)
                j = index[d]
                if i != j:
                    by_length[length].add((min(i, j), max(i, j)))
                # Complementary segments describe the same undirected target cycle.
                assert d == reverse(c, (start + length) % n, n - length)
        assert all(reverse(c, start, n - 1) == c for start in range(n))
    for length in by_length:
        assert by_length[length] == by_length[n - length]
    all_edges = set().union(*by_length.values())
    edges = {'OPW3': by_length[3], 'OPW23': by_length[2] | by_length[3],
             'all_Pi': all_edges, 'all_MICRO': all_edges}
    arrays = {}
    for name, pairs in edges.items():
        if name != 'all_MICRO':
            pairs = {e for e in pairs if pi[e[0]] == pi[e[1]]}
        arrays[name] = np.array(sorted(pairs), dtype=int).reshape(-1, 2)
    length_arrays = {length: np.array(sorted(pairs), dtype=int).reshape(-1, 2)
                     for length, pairs in by_length.items()}
    tours = np.array(states)
    rows = []
    witnesses = {}
    for half in range(1 << (n - 1)):
        mask = half << 1  # exactly one representative of every global-complement pair
        bits = ((mask >> tours) & 1).astype(np.int8)
        walls = np.sum(bits != np.roll(bits, 1, axis=1), axis=1)
        keep = ~np.any((bits != np.roll(bits, 1, axis=1)) &
                       (bits != np.roll(bits, -1, axis=1)), axis=1)
        ids = np.flatnonzero(keep)
        remap = np.full(len(states), -1, dtype=int)
        remap[ids] = np.arange(len(ids))
        row = {'mask': mask, 'ones': [v for v in range(n) if mask >> v & 1],
               'states': len(ids), 'lengths': {}, 'models': {}}
        row['minority'] = min(len(row['ones']), n - len(row['ones']))
        for length, es in length_arrays.items():
            accepted = es[keep[es[:, 0]] & keep[es[:, 1]]]
            preserves = accepted[pi[accepted[:, 0]] == pi[accepted[:, 1]]]
            row['lengths'][length] = {'MICRO_edges': len(accepted), 'MICRO_Pi_edges': len(preserves)}
        labels = {}
        selected = {}
        for name, es in arrays.items():
            es = es[keep[es[:, 0]] & keep[es[:, 1]]]
            selected[name] = es
            stats, labels[name] = components(len(ids), remap[es])
            stats['Pi_changing_edges'] = int(np.sum(pi[es[:, 0]] != pi[es[:, 1]]))
            stats['wall_changing_edges'] = int(np.sum(walls[es[:, 0]] != walls[es[:, 1]]))
            row['models'][name] = stats
            if name in ('OPW3', 'OPW23'):
                assert stats['wall_changing_edges'] == 0
            if name != 'all_MICRO':
                assert stats['Pi_changing_edges'] == 0
            for kind, condition in (
                ('domain_wall_change', walls[es[:, 0]] != walls[es[:, 1]]),
                ('Pi_change', pi[es[:, 0]] != pi[es[:, 1]])):
                key = name + ':' + kind
                hits = np.flatnonzero(condition)
                if len(hits) and key not in witnesses:
                    i, j = map(int, es[hits[0]])
                    events = [(s, length) for length in by_length for s in range(n)
                              if reverse(states[i], s, length) == states[j]]
                    witnesses[key] = {'mask': mask, 'ones': row['ones'],
                        'source': states[i], 'target': states[j], 'events': events,
                        'source_walls': int(walls[i]), 'target_walls': int(walls[j]),
                        'source_Pi': int(pi[i]), 'target_Pi': int(pi[j])}
        if len(ids):
            for lower, upper in zip(MODELS, MODELS[1:]):
                # Edge inclusion implies partition refinement; verify on every lower edge.
                es = selected[lower]
                assert np.all(labels[upper][remap[es[:, 0]]] == labels[upper][remap[es[:, 1]]])
                assert row['models'][upper]['components'] <= row['models'][lower]['components']
        rows.append(row)
    summary = []
    for minority in range(n // 2 + 1):
        subset = [r for r in rows if r['minority'] == minority]
        summary.append({'minority': minority, 'assignments': len(subset),
            'states': sorted({r['states'] for r in subset}),
            'components': {name: sorted({r['models'][name]['components'] for r in subset}) for name in MODELS},
            'wall_changing_edges': {name: sorted({r['models'][name]['wall_changing_edges'] for r in subset}) for name in MODELS}})
    return {'n': n, 'raw_states': len(states), 'raw_edges': {k: len(v) for k, v in arrays.items()},
            'summary': summary, 'witnesses': witnesses, 'colourings': rows}


if __name__ == '__main__':
    result = {'definition': 'fixed vertex bits; hard cyclic no-isolation; undirected labelled cycles; odd n; all colourings modulo complement, including constant assignment; nontrivial lengths 2..n-2; simple unweighted graphs',
              'runs': []}
    for n in (5, 7, 9):
        r = run(n)
        result['runs'].append(r)
        print(json.dumps({k: v for k, v in r.items() if k != 'colourings'}), flush=True)
    result['probe_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_name('results.json').write_text(json.dumps(result, indent=2) + '\n')
    print('ALL CHECKS PASSED')
