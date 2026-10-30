"""EHF-RW-002: exact boundary response on all small Hamiltonian-triad unions.

Python standard library only. Implements standard Schur/Kron reduction;
does not implement celestial amplitudes or infer a holographic duality.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, permutations, combinations_with_replacement
from pathlib import Path
import hashlib
import json
import platform

ROOT = Path(__file__).resolve().parent


def tours(n):
    return [(0,) + p for p in permutations(range(1, n)) if p[0] < p[-1]]


def edge_mask(t, ix):
    return sum(1 << ix[tuple(sorted((t[j], t[(j + 1) % len(t)])))] for j in range(len(t)))


def ensemble(n):
    es = list(combinations(range(n), 2))
    ix = {e: j for j, e in enumerate(es)}
    cs = tours(n)
    masks = [edge_mask(c, ix) for c in cs]
    unions = defaultdict(list)
    labelled = 0
    for a, b, c in combinations_with_replacement(range(len(cs)), 3):
        if masks[a] & masks[b] & masks[c]:
            continue
        unions[masks[a] | masks[b] | masks[c]].append((a, b, c))
        labelled += 3 if len({a, b, c}) == 2 else 6
    return cs, es, dict(unions), labelled


def laplacian(mask, n, es):
    L = [[0] * n for _ in range(n)]
    for k, (i, j) in enumerate(es):
        if mask & (1 << k):
            L[i][i] += 1
            L[j][j] += 1
            L[i][j] = L[j][i] = -1
    assert all(sum(row) == 0 for row in L)
    return L


def inverse(a):
    n = len(a)
    w = [[F(x) for x in row] + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if w[i][k])
        w[k], w[pivot] = w[pivot], w[k]
        d = w[k][k]
        w[k] = [x / d for x in w[k]]
        for i in range(n):
            if i != k:
                c = w[i][k]
                w[i] = [x - c * y for x, y in zip(w[i], w[k])]
    return [row[n:] for row in w]


def response(L, b, z):
    n = len(L)
    H = [[L[i][j] + (z if i == j else 0) for j in range(b, n)] for i in range(b, n)]
    Hi = inverse(H) if H else []
    out = [[F(L[i][j] + (z if i == j else 0)) -
            sum(L[i][k] * Hi[k - b][l - b] * L[l][j]
                for k in range(b, n) for l in range(b, n))
            for j in range(b)] for i in range(b)]
    assert out == [list(row) for row in zip(*out)]
    if z == 0:
        assert all(sum(row) == 0 for row in out)
    else:
        full = inverse([[F(L[i][j] + (z if i == j else 0)) for j in range(n)] for i in range(n)])
        assert inverse(out) == [row[:b] for row in full[:b]]
    return tuple(x for row in out for x in row)


def transfer_signature(L, b):
    """L_BB and 2m exact moments certify identical full rational response.

    For two interiors of size m the difference realization has size 2m;
    Cayley-Hamilton makes equality of its first 2m moments sufficient.
    """
    n = len(L)
    m = n - b
    sig = [L[i][j] for i in range(b) for j in range(b)]
    # X = H^k C^T, H=L_II and C=L_BI.
    X = [[L[i][j] for j in range(b)] for i in range(b, n)]
    for _ in range(2 * m):
        sig.extend(sum(L[i][k] * X[k - b][j] for k in range(b, n))
                   for i in range(b) for j in range(b))
        X = [[sum(L[i][k] * X[k - b][j] for k in range(b, n))
              for j in range(b)] for i in range(b, n)]
    return tuple(sig)


def canonical_graph(mask, n, b, es):
    """Only unobserved interior labels may be permuted; B fixed pointwise."""
    ix = {e: i for i, e in enumerate(es)}
    original = [e for k, e in enumerate(es) if mask & (1 << k)]
    variants = []
    for p in permutations(range(b, n)):
        q = tuple(range(b)) + p
        variants.append(sum(1 << ix[tuple(sorted((q[i], q[j])))] for i, j in original))
    return min(variants)


def describe(mask, n, es, cs, unions):
    return {'edge_mask': mask, 'edges': [e for k, e in enumerate(es) if mask & (1 << k)],
            'one_generating_triad': [cs[i] for i in unions[mask][0]],
            'unordered_triad_decompositions': len(unions[mask])}


def audit(n):
    cs, es, unions, labelled = ensemble(n)
    Ls = {g: laplacian(g, n, es) for g in unions}
    output = {'n': n, 'labelled_triads': labelled,
              'unordered_triads': sum(map(len, unions.values())),
              'distinct_labelled_union_graphs': len(unions), 'rows': [], 'witnesses': []}
    lost = next((g for g in sorted(unions) if len(unions[g]) > 1), None)
    if lost is not None:
        output['lost_cycle_decomposition_witness'] = {
            **describe(lost, n, es, cs, unions),
            'two_distinct_unordered_triads': [[cs[i] for i in t] for t in unions[lost][:2]]}
    for b in range(1, min(4, n - 1) + 1):
        classes = {g: canonical_graph(g, n, b, es) for g in unions}
        obs = {kind: defaultdict(list) for kind in ('boundary_edges', 'static_response',
               'static_plus_z1', 'full_transfer')}
        for g in sorted(unions):
            L = Ls[g]
            raw = tuple(-L[i][j] for i in range(b) for j in range(i + 1, b))
            static = response(L, b, 0)
            shifted = response(L, b, 1)
            sig = transfer_signature(L, b)
            for kind, key in [('boundary_edges', raw), ('static_response', static),
                              ('static_plus_z1', static + shifted), ('full_transfer', sig)]:
                obs[kind][key].append(g)
        for kind, groups in obs.items():
            ambiguous = [gs for gs in groups.values() if len({classes[g] for g in gs}) > 1]
            row = {'n': n, 'boundary_size': b, 'observer': kind,
                   'graph_classes_mod_interior_relabelling': len(set(classes.values())),
                   'distinct_observations': len(groups),
                   'ambiguous_observations': len(ambiguous),
                   'largest_number_of_graph_classes_per_observation':
                       max(len({classes[g] for g in gs}) for gs in groups.values()),
                   'injective_mod_interior_relabelling': not ambiguous}
            output['rows'].append(row)
            # Retain a concrete non-isomorphic collision for every failing observer.
            if ambiguous:
                gs = ambiguous[0]
                a = gs[0]
                d = next(g for g in gs if classes[g] != classes[a])
                output['witnesses'].append({'boundary_size': b, 'observer': kind,
                    'graph_a': describe(a, n, es, cs, unions),
                    'graph_b': describe(d, n, es, cs, unions)})
            print(n, b, kind, row['distinct_observations'],
                  row['graph_classes_mod_interior_relabelling'],
                  'ambiguous', len(ambiguous), flush=True)
        # Verify all-response equivalence implies agreement at independent z=2,3.
        for gs in obs['full_transfer'].values():
            for z in (2, 3):
                target = response(Ls[gs[0]], b, z)
                assert all(response(Ls[g], b, z) == target for g in gs)
        # Graph isomorphism fixing B must preserve all measurements.
        seen = {}
        for g in unions:
            v = transfer_signature(Ls[g], b)
            assert classes[g] not in seen or seen[classes[g]] == v
            seen[classes[g]] = v
    # Full access is a positive reconstruction control: S(z)=zI+L.
    for L in Ls.values():
        assert response(L, n, 1) == tuple(F(L[i][j] + (i == j))
                                              for i in range(n) for j in range(n))
    return output


def main():
    result = {'probe': 'EHF-RW-002', 'date': '2026-10-30',
              'python': platform.python_version(),
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'arithmetic': 'integer and Fraction; no floating point or random sampling',
              'scope': 'all triad unions N=4..6; fixed boundary B=0..b-1; b=1..min(4,N-1)',
              'ensembles': [audit(n) for n in (4, 5, 6)]}
    (ROOT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
