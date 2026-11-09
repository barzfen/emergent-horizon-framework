"""Exact Terras minimax cutoffs and odd-count thresholds for the sieve."""

import argparse
from itertools import product
from pathlib import Path


def minimax(depth):
    multiplier, offset, modulus = 1, 0, 1
    odds = 0
    cutoffs = {}
    required_odds = [0]
    for step in range(1, depth + 1):
        next_modulus = 2 * modulus
        if multiplier < next_modulus:
            # Try an even step first. This gives the worst first contraction.
            cutoffs[step] = offset // (next_modulus - multiplier)
            # Use an odd step to keep the boundary word alive.
            multiplier, offset = 3 * multiplier, 3 * offset + modulus
            odds += 1
        required_odds.append(odds)
        modulus = next_modulus
    return cutoffs, required_odds


def brute_cutoffs(depth):
    """Independent enumeration of all words at small depths."""
    cutoffs = {}
    for d in range(1, depth + 1):
        for bits in product((0, 1), repeat=d):
            multiplier, offset, modulus = 1, 0, 1
            for step, bit in enumerate(bits, 1):
                if bit:
                    multiplier, offset = 3 * multiplier, 3 * offset + modulus
                modulus *= 2
                if multiplier < modulus:
                    if step == d:
                        cutoff = offset // (modulus - multiplier)
                        cutoffs[d] = max(cutoffs.get(d, 0), cutoff)
                    break
    return cutoffs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", type=int, default=200_000)
    parser.add_argument("--sieve-depth", type=int, default=20)
    parser.add_argument("--verify-depth", type=int, default=512)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    if not 1 <= args.sieve_depth <= min(24, args.verify_depth) or args.verify_depth > args.depth:
        parser.error("require sieve depth from 1 to 24 and sieve depth <= verify depth <= depth")

    cutoffs, required_odds = minimax(args.depth)
    brute_depth = min(16, args.depth)
    if brute_cutoffs(brute_depth) != {d: c for d, c in cutoffs.items() if d <= brute_depth}:
        raise RuntimeError("exhaustive small-depth check disagrees with minimax")
    record_depth = max(cutoffs, key=cutoffs.get)
    candidate_bound = cutoffs[record_depth]
    early_bound = max(c for d, c in cutoffs.items() if d <= args.sieve_depth)
    thresholds = " ".join(map(str, required_odds[:args.verify_depth + 1]))
    args.certificate.write_text(
        f"{args.depth} {args.sieve_depth} {args.verify_depth} {early_bound} "
        f"{candidate_bound} {record_depth}\n{thresholds}\n",
        encoding="ascii",
    )


if __name__ == "__main__":
    main()
