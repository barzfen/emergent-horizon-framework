"""Exact residue census for Collatz first descent under the shortcut map."""

import argparse
from collections import Counter
import json


def step(n):
    return (3 * n + 1) // 2 if n % 2 else n // 2


def residue_census(depth, direct_depth):
    first_contraction = [0] * (depth + 1)
    least_uncovered = [None] * (depth + 1)
    largest_cutoff = 0
    cutoff_witness = None
    exceptions = {}
    check_prefixes = set()

    def visit(d, residue, multiplier, offset):
        nonlocal largest_cutoff, cutoff_witness
        modulus = 1 << d
        least = residue + modulus if d > 0 and residue < 2 else residue
        if multiplier < modulus:
            first_contraction[d] += 1
            if d <= direct_depth:
                check_prefixes.add((d, residue))
            cutoff = offset // (modulus - multiplier)
            if cutoff > largest_cutoff:
                largest_cutoff = cutoff
                cutoff_witness = {
                    "depth": d, "residue": residue, "least_start": least,
                    "multiplier": multiplier, "offset": offset,
                }
            for n in range(least, cutoff + 1, modulus):
                exceptions[n] = d
            return

        if d and (least_uncovered[d] is None or least < least_uncovered[d]):
            least_uncovered[d] = least
        if d == depth:
            return

        endpoint = (multiplier * residue + offset) // modulus
        # The two lifts differ by modulus at the start and by an odd number at the endpoint.
        odd_residue = residue if endpoint % 2 else residue + modulus
        even_residue = residue + modulus if endpoint % 2 else residue
        visit(d + 1, even_residue, multiplier, offset)
        visit(d + 1, odd_residue, 3 * multiplier, 3 * offset + modulus)

    visit(0, 0, 1, 0)
    rows = []
    survivors = 1
    for d in range(1, depth + 1):
        survivors = 2 * survivors - first_contraction[d]
        rows.append({
            "depth": d,
            "first_contracting_prefixes": first_contraction[d],
            "uncontracted_residues": survivors,
            "least_start_in_uncontracted_residues": least_uncovered[d],
        })
    return rows, largest_cutoff, cutoff_witness, exceptions, check_prefixes


def coefficient_counts(depth):
    """Count paths by length and odd-step count, with no residue or offset data."""
    active = {0: 1}
    survivors = []
    for d in range(1, depth + 1):
        next_active = Counter()
        for odds, count in active.items():
            for next_odds in (odds, odds + 1):
                if 3**next_odds >= 1 << d:
                    next_active[next_odds] += count
        active = next_active
        survivors.append(sum(active.values()))
    return survivors


def direct_check(prefixes, exceptions, depth):
    """Check the predicted first drop for each start in one full residue window."""
    for n in range(2, (1 << depth) + 2):
        predicted = None
        observed = None
        value = n
        for d in range(1, depth + 1):
            if (d, n % (1 << d)) in prefixes:
                predicted = d
            value = step(value)
            if value < n:
                observed = d
                break
        if n in exceptions and exceptions[n] <= depth:
            if predicted != exceptions[n] or (observed is not None and observed <= predicted):
                raise RuntimeError(f"Direct iteration disagrees on exception {n}")
        elif predicted != observed:
            raise RuntimeError(f"Direct iteration disagrees on start {n}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", type=int, default=30)
    parser.add_argument("--direct-depth", type=int, default=18)
    parser.add_argument("--count-depth", type=int, default=100)
    args = parser.parse_args()
    if not 1 <= args.direct_depth <= args.depth <= args.count_depth:
        parser.error("require 1 <= direct-depth <= depth <= count-depth")

    rows, cutoff, witness, exceptions, prefixes = residue_census(args.depth, args.direct_depth)
    counts = coefficient_counts(args.count_depth)
    if [row["uncontracted_residues"] for row in rows] != counts[:args.depth]:
        raise RuntimeError("Independent coefficient count disagrees with the residue traversal")
    direct_check(prefixes, exceptions, args.direct_depth)
    result = {
        "residue_rows": rows,
        "largest_integer_cutoff_at_first_contraction": cutoff,
        "cutoff_witness": witness,
        "exceptions_to_descent_at_first_contraction": exceptions,
        "direct_check_depth": args.direct_depth,
        "coefficient_only_counts_beyond_census": {
            d: counts[d - 1]
            for d in sorted({50, 100, args.count_depth})
            if args.depth < d <= args.count_depth
        },
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
