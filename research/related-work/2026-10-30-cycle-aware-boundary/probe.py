"""EHF-RW-003: exact lifted-cycle boundary tests on the N=5 witness family.

Python standard library. Reuses the checked Fraction inversion and ensemble
enumeration from EHF-RW-002; records the dependency hash in results.json.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import hashlib
import importlib.util
import json
import platform

HERE = Path(__file__).resolve().parent
DEPENDENCY = HERE.parent / '2026-10-30-boundary-reconstruction' / 'probe.py'
spec = importlib.util.spec_from_file_location('boundary_probe', DEPENDENCY)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
N, B = 5, 3


def cycle_lap(t):
    L = [[F(0) for _ in range(N)] for _ in range(N)]
    for i, u in enumerate(t):
        v = t[(i + 1) % N]
        L[u][u] += F(1, 2)
        L[v][v] += F(1, 2)
        L[u][v] -= F(1, 2)
        L[v][u] -= F(1, 2)
    return L


def lift(triad, kappa):
    # Vertex-major ordering: (0,0),(0,1),(0,2),(1,0),...
    L = [[F(0) for _ in range(3 * N)] for _ in range(3 * N)]
    layers = [cycle_lap(t) for t in triad]
    for v in range(N):
        for k in range(3):
            for w in range(N):
                L[3 * v + k][3 * w + k] = layers[k][v][w]
            L[3 * v + k][3 * v + k] += kappa
            for j in range(3):
                if k != j:
                    L[3 * v + k][3 * v + j] = -kappa / 2
    assert all(sum(row) == 0 for row in L)
    assert all(L[i][j] == L[j][i] for i in range(3 * N) for j in range(3 * N))
    assert all(L[i][j] <= 0 for i in range(3 * N) for j in range(3 * N) if i != j)
    return L


def resolvent(L, z=F(1)):
    return old.inverse([[L[i][j] + (z if i == j else 0) for j in range(len(L))]
                        for i in range(len(L))])


def pos_response(R):
    # Equal mixture on input label; sum final labels. This is a resolvent
    # of an observed lifted process, not an asserted Markov semigroup on V.
    return tuple(sum(R[3 * v + k][3 * w + j] for k in range(3) for j in range(3)) / 3
                 for v in range(B) for w in range(B))


def resolved_response(R):
    # Allow a single global permutation of cycle names, not separate
    # permutations at different vertices. Exact tuple comparison, no hashes.
    return min(tuple(R[3 * v + p[k]][3 * w + p[j]]
                     for v in range(B) for k in range(3)
                     for w in range(B) for j in range(3)) for p in permutations(range(3)))


def canonical_triad(triad):
    """Forget cycle names and the names of the two unobserved vertices."""
    def tour(p):
        i = p.index(0)
        q = p[i:] + p[:i]
        return min(tuple(q), tuple(q[:1] + q[:0:-1]))
    return min(tuple(sorted(tour([p[v] for v in t]) for t in triad))
               for p in ((0, 1, 2, 3, 4), (0, 1, 2, 4, 3)))


def within_weight_controls(ts, positions, resolved):
    weights = [tuple(x for row in averaged_lap(t) for x in row) for t in ts]
    local = [resolved_response(lift(t, F(0))) for t in ts]
    canonical = [canonical_triad(t) for t in ts]
    out = {'same_weight_inequivalent_pairs': 0, 'position_distinguished': 0,
           'cycle_resolved_distinguished': 0, 'same_weight_and_local_boundary_pairs': 0,
           'same_weight_and_local_boundary_resolved_distinguished': 0}
    for i in range(len(ts)):
        for j in range(i + 1, len(ts)):
            if weights[i] != weights[j] or canonical[i] == canonical[j]:
                continue
            out['same_weight_inequivalent_pairs'] += 1
            out['position_distinguished'] += positions[i] != positions[j]
            out['cycle_resolved_distinguished'] += resolved[i] != resolved[j]
            if local[i] == local[j]:
                out['same_weight_and_local_boundary_pairs'] += 1
                out['same_weight_and_local_boundary_resolved_distinguished'] += resolved[i] != resolved[j]
            if resolved[i] != resolved[j] and 'first_distinguished_pair' not in out:
                out['first_distinguished_pair'] = {'triad_a': ts[i], 'triad_b': ts[j],
                    'same_local_boundary_generator_mod_cycle_names': local[i] == local[j]}
    return out


def averaged_lap(triad):
    layers = [cycle_lap(t) for t in triad]
    return [[sum(L[i][j] for L in layers) / 3 for j in range(N)] for i in range(N)]


def summarize(A, C):
    # Each entry is an exact finite observable on one unordered triad.
    a, c = Counter(A), Counter(C)
    equal = sum(a[s] * c[s] for s in a.keys() & c.keys())
    return {'decompositions_a': len(A), 'decompositions_b': len(C),
            'cross_pairs': len(A) * len(C), 'indistinguishable_cross_pairs_at_z1': equal,
            'distinguishable_cross_pairs_at_z1': len(A) * len(C) - equal,
            'distinct_responses_a': len(a), 'distinct_responses_b': len(c),
            'shared_response_classes': len(a.keys() & c.keys())}


def encode(seq):
    return [str(x) for x in seq]


def main():
    cs, es, unions, labelled = old.ensemble(N)
    full = (1 << len(es)) - 1
    missing = full ^ (1 << es.index((3, 4)))
    triads = {g: [[cs[i] for i in inds] for inds in unions[g]] for g in (full, missing)}
    assert [len(triads[g]) for g in (full, missing)] == [72, 2]
    result = {'probe': 'EHF-RW-003', 'date': '2026-10-30',
        'python': platform.python_version(), 'n': N, 'boundary_vertices': list(range(B)),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'dependency': str(DEPENDENCY.relative_to(HERE.parent.parent.parent)),
        'dependency_sha256': hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest(),
        'method': 'exact Fraction resolvent at z=1; all 72 versus 2 unordered decompositions',
        'spatial_rates': 'each of two neighbors in current cycle at rate 1/2; total spatial hop rate 1',
        'switching_rates': 'each other cycle at kappa/2; total switching rate kappa',
        'families': {str(g): {'union_edges': [e for i, e in enumerate(es) if g & (1 << i)],
                             'triads': triads[g]} for g in (full, missing)},
        'rows': [], 'selected_pair': {'triad_a': triads[full][0], 'triad_b': triads[missing][0]},
        'selected_responses': [], 'same_weight_controls': []}
    # Reproduce the old blind spot at the same z using a common time rescaling.
    plain = [old.laplacian(g, N, es) for g in (full, missing)]
    for rate in (F(1), F(1, 4)):
        obs = [tuple(x for row in resolvent([[rate * v for v in row] for row in L])[:B]
                     for x in row[:B]) for L in plain]
        assert obs[0] == obs[1]
    result['union_blind_spot_reproduced_at_common_rates'] = ['1', '1/4']
    # Fast switching retains edge multiplicity but no persistent cycle label.
    fast = {}
    for g in (full, missing):
        fast[g] = [tuple(x for row in resolvent(averaged_lap(t))[:B] for x in row[:B])
                   for t in triads[g]]
    result['fast_switching_weighted_control'] = summarize(fast[full], fast[missing])
    result['selected_pair_fast_responses'] = [encode(fast[g][0]) for g in (full, missing)]
    for kappa in (F(0), F(1, 10), F(1), F(10)):
        positions, resolved = {}, {}
        for g in (full, missing):
            positions[g], resolved[g] = [], []
            for j, t in enumerate(triads[g]):
                L = lift(t, kappa)
                R = resolvent(L)
                assert all(x >= 0 for row in R for x in row)
                assert all(sum(row) == 1 for row in R)  # z=1
                positions[g].append(pos_response(R))
                resolved[g].append(resolved_response(R))
                if j == 0:
                    # Independent boundary elimination and label-permutation control.
                    S = old.response(L, 3 * B, F(1))
                    Smat = [list(S[i * 3 * B:(i + 1) * 3 * B]) for i in range(3 * B)]
                    assert old.inverse(Smat) == [row[:3 * B] for row in R[:3 * B]]
                    Rp = resolvent(lift(t[::-1], kappa))
                    assert pos_response(Rp) == positions[g][-1]
                    assert resolved_response(Rp) == resolved[g][-1]
        for name, data in [('position_only', positions), ('cycle_resolved_mod_global_permutation', resolved)]:
            row = {'kappa': str(kappa), 'observer': name, **summarize(data[full], data[missing])}
            result['rows'].append(row)
            print(row, flush=True)
        for g in (full, missing):
            result['same_weight_controls'].append({'kappa': str(kappa), 'union_mask': g,
                **within_weight_controls(triads[g], positions[g], resolved[g])})
        result['selected_responses'].append({'kappa': str(kappa),
            'position_a': encode(positions[full][0]), 'position_b': encode(positions[missing][0]),
            'max_position_difference': str(max(abs(a - b) for a, b in zip(positions[full][0], positions[missing][0]))),
            'resolved_a': encode(resolved[full][0]), 'resolved_b': encode(resolved[missing][0])})
    # Finite high-rate check of the fast-switching limit on the selected pair.
    result['fast_limit_checks'] = []
    for g in (full, missing):
        errors = []
        for k in (F(10), F(100), F(1000)):
            r = pos_response(resolvent(lift(triads[g][0], k)))
            errors.append(max(abs(a - b) for a, b in zip(r, fast[g][0])))
        assert errors[2] < errors[1] < errors[0]
        result['fast_limit_checks'].append({'union_mask': g, 'kappas': [10, 100, 1000],
                                           'max_errors': encode(errors)})
    # Decisive: every finite tested rate/observer distinguishes every cross pair.
    # Do not assert in advance; report the actual outcome, including equality.
    (HERE / 'results.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
