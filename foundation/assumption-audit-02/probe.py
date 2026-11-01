"""Exact finite memory audit. Python 3.10+, standard library only.

Copyright (c) 2026 Barry Fensom. SPDX-License-Identifier: MIT
AI-assisted implementation of standard finite dynamics and probability.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import json
from pathlib import Path


def components(f):
    parent = list(range(len(f)))
    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for x, y in enumerate(f):
        parent[root(x)] = root(y)
    return tuple(root(x) for x in range(len(f)))


def tv(a, b):
    return sum((abs(x-y) for x, y in zip(a, b)), Q(0)) / 2


def evolve(p, kernel):
    return tuple(sum((p[x] * kernel[x][y] for x in range(len(p))), Q(0))
                 for y in range(len(kernel[0])))


def project(p, labels):
    return tuple(sum((v for v, label in zip(p, labels) if label == y), Q(0))
                 for y in range(2))


def point(n, x):
    return tuple(Q(i == x) for i in range(n))


def deterministic_audit():
    rows = []
    for n in range(1, 5):
        maps = pair_checks = invariant_readouts = reversible = 0
        for f in product(range(n), repeat=n):
            maps += 1
            comp = components(f)
            readouts = [r for r in product(range(2), repeat=n)
                        if all(r[f[x]] == r[x] for x in range(n))]
            assert len(readouts) == 2 ** len(set(comp))
            invariant_readouts += len(readouts)
            is_reversible = len(set(f)) == n
            reversible += int(is_reversible)
            for a, b in combinations(range(n), 2):
                pair_checks += 1
                assert any(r[a] != r[b] for r in readouts) == (comp[a] != comp[b])
                x, y = a, b
                merged = False
                for _ in range(n*n + 1):
                    merged = merged or x == y
                    if merged:
                        assert x == y
                    if is_reversible:
                        assert x != y
                    x, y = f[x], f[y]
        rows.append({"states": n, "maps": maps, "encoded_pair_checks": pair_checks,
                     "reversible_maps": reversible,
                     "invariant_binary_readouts_including_constants": invariant_readouts})
    return rows


def stochastic_audit():
    kernels = pairs = projections = 0
    for n in (2, 3):
        distributions = [tuple(Q(x, 2) for x in counts)
                         for counts in product(range(3), repeat=n) if sum(counts) == 2]
        for kernel in product(distributions, repeat=n):
            kernels += 1
            for a, b in combinations(distributions, 2):
                pairs += 1
                aa, bb = evolve(a, kernel), evolve(b, kernel)
                assert tv(aa, bb) <= tv(a, b)
                for labels in product(range(2), repeat=n):
                    projections += 1
                    assert tv(project(aa, labels), project(bb, labels)) <= tv(aa, bb)
    return {"kernels": kernels, "distribution_pair_checks": pairs,
            "binary_observation_checks": projections,
            "scope": "all stochastic rows with denominator 2 on 2 and 3 states"}


def noise_kernel(bits, p, correct=False):
    n = 1 << bits
    kernel = []
    for x in range(n):
        row = [Q(0)] * n
        for y in range(n):
            flips = (x ^ y).bit_count()
            probability = p**flips * (1-p)**(bits-flips)
            target = (n-1 if y.bit_count() > bits//2 else 0) if correct else y
            row[target] += probability
        assert sum(row) == 1
        kernel.append(tuple(row))
    return tuple(kernel)


def noise_audit():
    p = Q(1, 10)
    logical_error = 3*p*p - 2*p*p*p
    kernels = {"one_bit": noise_kernel(1, p),
               "three_bits_final_majority": noise_kernel(3, p),
               "three_bits_correct_every_step": noise_kernel(3, p, True)}
    states = {name: (point(len(k), 0), point(len(k), len(k)-1))
              for name, k in kernels.items()}
    table = []
    last_success_at_least_75 = {name: None for name in kernels}
    for t in range(31):
        scores = {}
        alpha = (1-2*p)**t
        expected = {"one_bit": alpha,
                    "three_bits_final_majority": (3*alpha-alpha**3)/2,
                    "three_bits_correct_every_step": (1-2*logical_error)**t}
        for name, (a, b) in states.items():
            distance = tv(a, b)
            assert distance == expected[name]
            if len(a) == 8:
                labels = tuple(int(i.bit_count() >= 2) for i in range(8))
                assert tv(project(a, labels), project(b, labels)) == distance
            success = (1+distance)/2
            if success >= Q(3, 4):
                last_success_at_least_75[name] = t
            scores[name] = {"tv_exact": str(distance), "success": float(success)}
        if t in (0, 1, 3, 5, 10, 12, 13, 20, 30):
            table.append({"step": t, **scores})
        states = {name: (evolve(a, kernels[name]), evolve(b, kernels[name]))
                  for name, (a, b) in states.items()}
    assert all(value is not None and value < 30
               for value in last_success_at_least_75.values())
    # Bounded-error protection: ideal majority restores either codeword
    # after any zero- or one-bit error. This differs from iid noise.
    for codeword in (0, 7):
        for error in (0, 1, 2, 4):
            corrupted = codeword ^ error
            restored = 7 if corrupted.bit_count() >= 2 else 0
            assert restored == codeword
    return {"physical_flip_probability": str(p),
            "logical_flip_probability_with_perfect_correction": str(logical_error),
            "last_step_success_at_least_75_percent": last_success_at_least_75,
            "table": table, "exact_evolution_steps_checked": 31}


def controls():
    # State index is 2*a+b; observe the first bit only.
    swap = (0, 2, 1, 3)
    reset_first = (0, 1, 0, 1)
    delayed_erase = (0, 0, 1, 1)  # (a,b) -> (0,a)
    output = {}
    for name, f in (("swap", swap), ("reset_first", reset_first),
                    ("transfer_then_erase", delayed_erase)):
        a, b = 0, 2
        history = []
        for t in range(4):
            history.append({"step": t, "full_tv": int(a != b),
                            "first_bit_tv": int(a//2 != b//2),
                            "states": [a, b]})
            a, b = f[a], f[b]
        output[name] = history
    assert [r["first_bit_tv"] for r in output["swap"]] == [1, 0, 1, 0]
    assert [r["full_tv"] for r in output["transfer_then_erase"]] == [1, 1, 0, 0]
    # A cyclic permutation keeps known-time information but has no
    # nonconstant invariant binary readout.
    cycle = (1, 2, 3, 0)
    assert len(set(components(cycle))) == 1
    output["four_cycle"] = {"reversible": True, "invariant_binary_readouts": 2,
                            "nonconstant_invariant_binary_readouts": 0}
    # Noninjective map retaining the bit for this encoding forever.
    f = (0, 0, 2, 2)
    a, b = 0, 2
    for _ in range(20):
        assert a != b
        a, b = f[a], f[b]
    output["irreversible_but_retains_encoded_bit"] = list(f)
    return output


def run():
    result = {"scope": "classical finite states; imposed dynamics and readouts",
              "deterministic_audit": deterministic_audit(),
              "data_processing_audit": stochastic_audit(),
              "controls": controls(), "noise_audit": noise_audit(),
              "all_assertions_passed": True}
    Path(__file__).with_name("results.json").write_text(json.dumps(result, indent=2) + "\n")
    concise = {**result, "noise_audit": {k: v for k, v in result["noise_audit"].items()
                                        if k != "table"}}
    print(json.dumps(concise, indent=2))


if __name__ == "__main__":
    run()
