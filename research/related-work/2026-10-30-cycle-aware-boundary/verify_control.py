"""Exact moment certificate for a pair with identical weighted graph/local data.

Independent of resolvent inversion: computes boundary moments of the generator.
For equal 15-state realizations, 30 matching moments certify the complete
rational transfer function via Cayley-Hamilton on the difference realization.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import hashlib
import json
import probe as p

HERE = Path(__file__).resolve().parent


def moments(L):
    # Full power matrices permit both resolved and label-averaged observations.
    d = len(L)
    X = [[F(i == j) for j in range(d)] for i in range(d)]
    out = []
    for _ in range(2 * d):
        out.append(X)
        X = [[sum(L[i][k] * X[k][j] for k in range(d)) for j in range(d)]
             for i in range(d)]
    return out


def main():
    results = json.loads((HERE / 'results.json').read_text())
    sample = next(r['first_distinguished_pair'] for r in results['same_weight_controls']
                  if r['kappa'] == '1' and 'first_distinguished_pair' in r)
    a, b = sample['triad_a'], sample['triad_b']
    assert p.averaged_lap(a) == p.averaged_lap(b)
    assert p.canonical_triad(a) != p.canonical_triad(b)
    out = {'probe': 'EHF-RW-003 independent moment check', 'triad_a': a, 'triad_b': b,
           'boundary_vertices': [0, 1, 2], 'same_weighted_graph': True,
           'inequivalent_mod_hidden_and_cycle_relabellings': True, 'rows': []}
    for rate in (F(0), F(1, 10), F(1), F(10)):
        A, C = moments(p.lift(a, rate)), moments(p.lift(b, rate))
        pos_equal = all(p.pos_response(x) == p.pos_response(y) for x, y in zip(A, C))
        # Search a single permutation aligning all boundary moments, not an
        # independently chosen permutation for each moment.
        candidates = []
        for perm in permutations(range(3)):
            first = None
            for r, (x, y) in enumerate(zip(A, C)):
                for v in range(p.B):
                    for k in range(3):
                        for w in range(p.B):
                            for j in range(3):
                                lhs, rhs = x[3*v+k][3*w+j], y[3*v+perm[k]][3*w+perm[j]]
                                if lhs != rhs:
                                    first = {'order': r, 'entry': [[v,k],[w,j]],
                                             'a': str(lhs), 'b_aligned': str(rhs)}
                                    break
                            if first: break
                        if first: break
                    if first: break
                if first: break
            candidates.append({'cycle_permutation': perm, 'first_difference': first})
        same_local = any(c['first_difference'] is None or c['first_difference']['order'] > 1
                         for c in candidates)
        equal_all = any(c['first_difference'] is None for c in candidates)
        row = {'kappa': str(rate), 'moments_compared': 30,
               'same_local_boundary_generator_mod_cycle_names': same_local,
               'position_transfer_equal_for_all_z_positive': pos_equal,
               'resolved_transfer_equal_for_all_z_positive_mod_cycle_names': equal_all,
               'alignment_checks': candidates}
        assert same_local and pos_equal
        assert equal_all == (rate == 0)
        out['rows'].append(row)
        print('rate', rate, 'position all-z equal', pos_equal, 'resolved all-z equal', equal_all,
              'first differences', [c['first_difference']['order'] if c['first_difference'] else None
                                    for c in candidates], flush=True)
    out['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    # The generator is affine in kappa, so every L^3 entry is a polynomial
    # of degree at most three. Four exact evaluations certify its identity.
    local_alignments = [c['cycle_permutation'] for c in out['rows'][0]['alignment_checks']
                        if c['first_difference'] is None or c['first_difference']['order'] > 1]
    certificate = []
    for perm in local_alignments:
        values = []
        for k in (F(0), F(1), F(2), F(3)):
            left = moments(p.lift(a, k))[3][0][1]
            right = moments(p.lift(b, k))[3][perm[0]][perm[1]]
            assert left - right == -k / 8
            values.append(str(left - right))
        certificate.append({'cycle_permutation': perm, 'kappas': [0,1,2,3],
                            'entry': [[0,0],[0,1]], 'differences': values,
                            'polynomial': '-kappa/8'})
    out['third_moment_polynomial_certificate'] = certificate
    out['resolved_distinction_for_every_kappa_positive'] = True
    out['probe_sha256'] = hashlib.sha256((HERE / 'probe.py').read_bytes()).hexdigest()
    (HERE / 'moment_checks.json').write_text(json.dumps(out, indent=2) + '\n')


if __name__ == '__main__':
    main()
