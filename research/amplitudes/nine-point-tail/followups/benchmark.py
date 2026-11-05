"""Compare two-lift, KK, BCJ, and direct MHV reconstructions."""
from fractions import Fraction as F
import json
from pathlib import Path
from math import prod

from branches import kernel
from reconstruct import kk, can


def bracket(a, b):
    return a[0] * b[1] - a[1] * b[0]


def kinematics(sample):
    lam = {i: (1, i + sample * i**2) for i in range(1, 9)}
    tilde = {i: (i**2 + sample, (-1)**i * i + sample**2) for i in range(1, 7)}
    remaining = {}
    a, b = lam[7], lam[8]
    for component in (0, 1):
        rhs = tuple(-sum(lam[i][j] * tilde[i][component] for i in tilde) for j in (0, 1))
        remaining[component] = (F(bracket(rhs, b), bracket(a, b)),
                                F(bracket(a, rhs), bracket(a, b)))
    tilde[7], tilde[8] = zip(remaining[0], remaining[1])
    assert all(sum(lam[i][a] * tilde[i][b] for i in lam) == 0
               for a in (0, 1) for b in (0, 1))
    return lam, tilde


def denominator(word, lam):
    return prod(bracket(lam[i], lam[j]) for i, j in zip(word, word[1:] + word[:1]))


def mhv(word, lam):
    return F(bracket(lam[2], lam[3])**4, denominator(word, lam))


def reconstruction(relation, target, values):
    return -sum(c * values[w] for w, c in relation.items() if w != target) / relation[target]


def main():
    data = json.loads(Path(__file__).with_name("shared-lifts-results.json").read_text())
    witness = {tuple(w): F(c) for w, c in data["target_witness"]}
    target = tuple(data["common_cut_obstruction_word"])
    mobile = 8
    fixed = tuple(i for i in target if i != mobile)
    insertions = [can(fixed[:i] + (mobile,) + fixed[i:]) for i in range(1, len(fixed))]
    assert len(set(insertions)) == 6 and target in insertions
    pool = sorted(set(witness) | set(insertions))
    relations = [{pool[j]: c for j, c in row.items()} for row in kernel(kk(w) for w in pool)]
    eligible = [r for r in relations if target in r]
    direct_kk = min(eligible, key=len)

    points = []
    for sample in (1, 2, 3):
        lam, tilde = kinematics(sample)
        values = {w: mhv(w, lam) for w in pool}
        bcj = {w: sum(bracket(lam[mobile], lam[j]) * bracket(tilde[j], tilde[mobile])
                      for j in fixed[:i])
               for i, w in enumerate(insertions, start=1)}
        assert all(bcj.values())
        expected = values[target]
        for relation in (witness, direct_kk, bcj):
            assert reconstruction(relation, target, values) == expected

        # At the holomorphic pole choose lambda_9 = lambda_1. For momentum
        # conservation along lambda_9(e) = lambda_1 + e*lambda_2, one may
        # shift tilde_1 by -tilde_9 and tilde_2 by -e*tilde_9.
        on_pole = {**lam, 9: lam[1]}
        fold_value = [F(0), F(0)]
        for raw, *coeffs in data["side_by_side_lifts"]:
            w = tuple(raw)
            if w[-1] != 9:
                assert denominator(w, on_pole) != 0
                continue
            edges = list(zip(w, w[1:] + w[:1]))
            edges.remove((9, 1))
            normalized = F(bracket(lam[2], lam[3])**4,
                           prod(bracket(on_pole[a], on_pole[b]) for a, b in edges))
            assert normalized == values.get(can(w[:-1]), mhv(can(w[:-1]), lam))
            for j, c in enumerate(coeffs):
                fold_value[j] += F(c) * normalized
        assert fold_value == [0, 0]
        points.append(str(expected))

    print(json.dumps({
        "target": target,
        "available_amplitudes_excluding_target": len(pool) - 1,
        "two_lift_inputs": len(witness) - 1,
        "direct_kk_inputs": len(direct_kk) - 1,
        "kk_relation_space_dimension_in_pool": len(relations),
        "fundamental_bcj_inputs": len(insertions) - 1,
        "direct_mhv_formula_inputs": 0,
        "target_values_at_three_rational_kinematic_points": points,
    }, indent=2))


if __name__ == "__main__":
    main()
