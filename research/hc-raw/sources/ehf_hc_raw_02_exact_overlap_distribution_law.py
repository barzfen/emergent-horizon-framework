#!/usr/bin/env python3
"""
EHF-HC-RAW-02
Exact Raw Overlap Distribution Law

Derives the exact overlap distribution for undirected Hamilton cycles on n
labelled sites modulo rotation/reflection, before any dynamical move rule.

Fix a reference cycle C and let X(D)=|E(C) ∩ E(D)| for D uniform on HC_n.
For k reference edges, sum the number of cycles containing each k-edge subset.
A proper k-edge subset of a cycle is a linear forest whose c circular runs are
path components.  Such a forced pattern is contained in

    2^(c-1) (n-k-1)!

undirected Hamilton cycles.  The number of k-edge subsets of an n-cycle with
exactly c runs is

    R(n,k,c) = n/c * C(k-1,c-1) * C(n-k-1,c-1).

Hence the binomial-overlap sums S[n,k] are exact, and binomial inversion gives

    M_n(r) = sum_{k=r}^n (-1)^(k-r) C(k,r) S[n,k],

where M_n(r) counts cycles D with exactly r common edges with C.

Standard library only.  Fresh enumeration is optional and is used only to
certify the formula at manageable n.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from itertools import permutations
from pathlib import Path


def hc_count(n: int) -> int:
    return math.factorial(n - 1) // 2


def canonical_cycles(n: int):
    """One representative of each undirected Hamilton cycle."""
    for p in permutations(range(1, n)):
        if p[0] < p[-1]:
            yield (0,) + p


def edge(a: int, b: int):
    return (a, b) if a < b else (b, a)


def edges_of(cycle):
    n = len(cycle)
    return frozenset(edge(cycle[i], cycle[(i + 1) % n]) for i in range(n))


def run_subset_count(n: int, k: int, c: int) -> int:
    """Number of labelled k-edge subsets of C_n with c circular runs.

    Valid for 1 <= k <= n-1 and 1 <= c <= min(k,n-k).
    """
    if not (1 <= k <= n - 1):
        return 0
    if not (1 <= c <= min(k, n - k)):
        return 0
    # n/c * binom(k-1,c-1) * binom(n-k-1,c-1) is integral.
    num = n * math.comb(k - 1, c - 1) * math.comb(n - k - 1, c - 1)
    if num % c:
        raise AssertionError((n, k, c, num))
    return num // c


def forced_count(n: int, k: int, c: int) -> int:
    """Cycles containing a proper k-edge reference subset with c runs."""
    return (2 ** (c - 1)) * math.factorial(n - k - 1)


def binomial_overlap_sum(n: int, k: int) -> int:
    """S[n,k] = sum_D C(X(D),k) = sum_{|F|=k,F⊂E(C)} #cycles containing F."""
    if k == 0:
        return hc_count(n)
    if k == n:
        return 1
    total = 0
    for c in range(1, min(k, n - k) + 1):
        total += run_subset_count(n, k, c) * forced_count(n, k, c)
    return total


def exact_overlap_distribution(n: int) -> dict[int, int]:
    S = [binomial_overlap_sum(n, k) for k in range(n + 1)]
    M = {}
    for r in range(n + 1):
        val = 0
        for k in range(r, n + 1):
            val += ((-1) ** (k - r)) * math.comb(k, r) * S[k]
        if val:
            M[r] = val
        elif val < 0:
            raise AssertionError(f"negative overlap count n={n}, r={r}: {val}")
    return M


def enumerate_overlap_distribution(n: int) -> Counter:
    ref = edges_of(tuple(range(n)))
    return Counter(len(edges_of(c) & ref) for c in canonical_cycles(n))


def exact_moments(M: dict[int, int]):
    total = sum(M.values())
    s1 = sum(r * v for r, v in M.items())
    s2 = sum(r * r * v for r, v in M.items())
    return total, s1, s2


def audit_n(n: int, enumerate_check: bool):
    S = [binomial_overlap_sum(n, k) for k in range(n + 1)]
    M = exact_overlap_distribution(n)
    checks = []

    # Circular-run partition counts must sum to C(n,k).
    runs_ok = True
    run_rows = []
    for k in range(1, n):
        subtotal = 0
        for c in range(1, min(k, n-k) + 1):
            rc = run_subset_count(n, k, c)
            subtotal += rc
            run_rows.append({
                "n": n,
                "k": k,
                "runs": c,
                "subset_count": rc,
                "forced_cycle_count": forced_count(n, k, c),
                "contribution_to_Snk": rc * forced_count(n, k, c),
            })
        runs_ok &= subtotal == math.comb(n, k)
    checks.append(("circular_run_partition", runs_ok, {}))

    total, s1, s2 = exact_moments(M)
    H = hc_count(n)
    checks.append(("distribution_normalization", total == H, {"found": total, "expected": H}))
    checks.append(("identity_overlap", M.get(n, 0) == 1, {"count": M.get(n, 0)}))
    checks.append(("n_minus_1_forbidden", M.get(n-1, 0) == 0, {"count": M.get(n-1, 0)}))
    expected_top_shell = n * (n - 3) // 2
    checks.append(("n_minus_2_shell", M.get(n-2, 0) == expected_top_shell,
                   {"found": M.get(n-2, 0), "expected": expected_top_shell}))

    # Exact moment identities without floating point.
    # E[X] = 2n/(n-1), E[X^2] = 6n/(n-1).
    checks.append(("first_moment_exact", s1 * (n - 1) == H * 2 * n,
                   {"numerator": s1, "denominator": H}))
    checks.append(("second_moment_exact", s2 * (n - 1) == H * 6 * n,
                   {"numerator": s2, "denominator": H}))

    enum = None
    if enumerate_check:
        enum = enumerate_overlap_distribution(n)
        checks.append(("fresh_enumeration_match", dict(sorted(enum.items())) == M,
                       {"enumerated_states": sum(enum.values())}))

    binomial_rows = []
    for k, sval in enumerate(S):
        binomial_rows.append({
            "n": n,
            "k": k,
            "S_nk": sval,
            "interpretation": "sum_D binom(overlap(D),k)",
        })

    distribution_rows = []
    for r in range(n + 1):
        count = M.get(r, 0)
        distribution_rows.append({
            "n": n,
            "overlap": r,
            "count": count,
            "nonzero": count > 0,
            "fraction_float": count / H,
        })

    summary = {
        "n": n,
        "states": H,
        "support": [r for r in range(n + 1) if M.get(r, 0) > 0],
        "derangements_M0": M.get(0, 0),
        "M_n_minus_2": M.get(n-2, 0),
        "M_n_minus_1": M.get(n-1, 0),
        "M_n": M.get(n, 0),
        "enumerated": enumerate_check,
        "all_checks_pass": all(ok for _, ok, _ in checks),
    }
    check_rows = [
        {"n": n, "check": name, "pass": ok, "details": json.dumps(info, sort_keys=True)}
        for name, ok, info in checks
    ]
    return summary, distribution_rows, binomial_rows, run_rows, check_rows


def write_csv(path: Path, rows):
    rows = list(rows)
    if not rows:
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-min", type=int, default=4)
    ap.add_argument("--n-max", type=int, default=30,
                    help="maximum n for exact formula generation")
    ap.add_argument("--enumerate-through", type=int, default=10,
                    help="fresh exhaustive enumeration through this n; set < n-min to disable")
    ap.add_argument("--out-dir", default="runs/ehf_hc_raw_02")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    if args.n_min < 4:
        raise SystemExit("use --n-min >= 4")
    if args.n_max < args.n_min:
        raise SystemExit("--n-max must be >= --n-min")

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    summaries = []
    distributions = []
    binomial_rows = []
    run_rows = []
    checks = []

    print("=" * 106)
    print("EHF-HC-RAW-02: EXACT RAW OVERLAP DISTRIBUTION LAW")
    print("=" * 106)
    print(f"formula range: n={args.n_min}..{args.n_max}")
    print(f"fresh exhaustive enumeration through n={args.enumerate_through}")
    print("No LR3 / LR2 / 2-opt / sector / growth rule is used.\n")

    for n in range(args.n_min, args.n_max + 1):
        enum_check = n <= args.enumerate_through
        summary, drows, brows, rrows, crows = audit_n(n, enum_check)
        if args.strict and not summary["all_checks_pass"]:
            failed = [r for r in crows if not r["pass"]]
            raise AssertionError(f"n={n} failed: {failed}")
        summaries.append(summary)
        distributions.extend(drows)
        binomial_rows.extend(brows)
        run_rows.extend(rrows)
        checks.extend(crows)
        support = ",".join(map(str, summary["support"]))
        print(
            f"n={n:2d} states={summary['states']:>25d}  "
            f"M0={summary['derangements_M0']:>20d}  "
            f"M[n-2]={summary['M_n_minus_2']:>6d}  "
            f"support=[{support}]  enum={'yes' if enum_check else 'no ':3s}  "
            f"PASS={summary['all_checks_pass']}"
        )

    write_csv(out / "summary.csv", summaries)
    write_csv(out / "exact_overlap_distribution.csv", distributions)
    write_csv(out / "binomial_overlap_sums.csv", binomial_rows)
    write_csv(out / "circular_run_contributions.csv", run_rows)
    write_csv(out / "checks.csv", checks)
    with (out / "summary.json").open("w") as f:
        json.dump({"summaries": summaries, "checks": checks}, f, indent=2)

    all_pass = all(r["all_checks_pass"] for r in summaries)
    print("\nExact theorem-shaped law used:")
    print("  R(n,k,c) = n/c * C(k-1,c-1) * C(n-k-1,c-1)")
    print("  N(forced k-edge subset with c runs) = 2^(c-1) (n-k-1)!")
    print("  S[n,k] = sum_c R(n,k,c) N(n,k,c), with S[n,0]=|HC_n| and S[n,n]=1")
    print("  M_n(r) = sum_{k=r}^n (-1)^(k-r) C(k,r) S[n,k]")
    print("  generating polynomial: P_n(z)=sum_k S[n,k](z-1)^k = sum_r M_n(r) z^r")
    print("\nCorollaries checked exactly:")
    print("  M_n(n)=1")
    print("  M_n(n-1)=0")
    print("  M_n(n-2)=n(n-3)/2")
    print("  E[X]=2n/(n-1)")
    print("  E[X^2]=6n/(n-1)")
    print(f"\noutput: {out}")
    if all_pass:
        print("EHF_HC_RAW_02_EXACT_OVERLAP_DISTRIBUTION_LAW_PASS")
    else:
        print("EHF_HC_RAW_02_CHECK_FAILURE")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
