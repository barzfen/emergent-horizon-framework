#!/usr/bin/env python3
"""
EHF-HC-RAW-01
Definition Lock, Dihedral Quotient, Incidence Neutrality, and Raw Overlap Census

Pure standard-library audit of the undirected Hamilton-cycle state space HC_n,
before any LR3, LR2, 2-opt, sector, growth, probability, or physical rule is added.

States are undirected cyclic orderings of labels {0,...,n-1} modulo rotation
and reflection.  The canonical implementation anchors 0 at position 0 and
keeps the orientation with first neighbour < last neighbour.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from itertools import permutations
from pathlib import Path


def canonical_cycles(n: int):
    """Yield one representative of each undirected n-cycle."""
    if n < 3:
        raise ValueError("n must be >= 3")
    for p in permutations(range(1, n)):
        if p[0] < p[-1]:
            yield (0,) + p


def edge(a: int, b: int):
    return (a, b) if a < b else (b, a)


def edges_of(cycle):
    n = len(cycle)
    return frozenset(edge(cycle[i], cycle[(i + 1) % n]) for i in range(n))


def direct_dihedral_canonical(presentation):
    """Canonicalise by taking the lexicographic minimum over all 2n presentations."""
    c = tuple(presentation)
    n = len(c)
    candidates = []
    for orient in (c, tuple(reversed(c))):
        for shift in range(n):
            candidates.append(orient[shift:] + orient[:shift])
    return min(candidates)


def anchored_canonical(presentation):
    """Canonicalise by anchor-0 then reflection choice."""
    c = tuple(presentation)
    n = len(c)
    i = c.index(0)
    r = c[i:] + c[:i]
    rr = (r[0],) + tuple(reversed(r[1:]))
    return min(r, rr)


def linear_forest_components(forced_edges):
    """Return (is_linear_forest, k_edges, nontrivial_path_components)."""
    forced = {edge(*e) for e in forced_edges}
    if not forced:
        return True, 0, 0
    adj = {}
    for a, b in forced:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    if any(len(v) > 2 for v in adj.values()):
        return False, len(forced), 0

    seen = set()
    comps = 0
    for start in adj:
        if start in seen:
            continue
        comps += 1
        stack = [start]
        verts = 0
        degsum = 0
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            verts += 1
            degsum += len(adj[x])
            stack.extend(adj[x] - seen)
        ecount = degsum // 2
        # A connected component with ecount == verts is a cycle, not a path.
        if ecount != verts - 1:
            return False, len(forced), 0
    return True, len(forced), comps


def predicted_linear_forest_count(n: int, forced_edges):
    ok, k, c = linear_forest_components(forced_edges)
    if not ok:
        return 0
    if k == 0:
        return math.factorial(n - 1) // 2
    if k > n - 1:
        return 0
    return (2 ** (c - 1)) * math.factorial(n - k - 1)


def count_containing(cycle_edge_sets, forced_edges):
    f = frozenset(edge(*e) for e in forced_edges)
    return sum(1 for es in cycle_edge_sets if f <= es)


def overlap_moments(overlap_counts, total):
    mean = sum(k * v for k, v in overlap_counts.items()) / total
    second = sum((k * k) * v for k, v in overlap_counts.items()) / total
    return mean, second - mean * mean


def audit_n(n: int, strict: bool):
    cycles = list(canonical_cycles(n))
    edge_sets = [edges_of(c) for c in cycles]
    expected_states = math.factorial(n - 1) // 2

    checks = []
    checks.append(("state_count", len(cycles) == expected_states,
                   {"found": len(cycles), "expected": expected_states}))

    # Canonicalisation equivalence on the enumerated representatives and a
    # rotated/reversed presentation of each representative.
    canon_ok = True
    for c in cycles:
        variants = [c, c[1:] + c[:1], tuple(reversed(c))]
        for v in variants:
            if anchored_canonical(v) != direct_dihedral_canonical(v):
                canon_ok = False
                break
        if not canon_ok:
            break
    checks.append(("dihedral_canonical_equivalence", canon_ok, {}))

    structure_ok = True
    for es in edge_sets:
        if len(es) != n:
            structure_ok = False
            break
        degrees = Counter()
        for a, b in es:
            degrees[a] += 1
            degrees[b] += 1
        if set(degrees) != set(range(n)) or any(degrees[v] != 2 for v in range(n)):
            structure_ok = False
            break
    checks.append(("cycle_structure", structure_ok, {}))

    edge_counts = Counter()
    for es in edge_sets:
        edge_counts.update(es)
    expected_incidence = math.factorial(n - 2)
    incidence_values = sorted(set(edge_counts.values()))
    edge_neutral = incidence_values == [expected_incidence] and len(edge_counts) == math.comb(n, 2)
    checks.append(("edge_incidence_neutrality", edge_neutral,
                   {"values": incidence_values, "expected": expected_incidence}))

    # Pair-incidence laws.
    adjacent_pair = [(0, 1), (1, 2)]
    disjoint_pair = [(0, 1), (2, 3)]
    adjacent_found = count_containing(edge_sets, adjacent_pair)
    disjoint_found = count_containing(edge_sets, disjoint_pair)
    adjacent_expected = math.factorial(n - 3)
    disjoint_expected = 2 * math.factorial(n - 3)
    checks.append(("adjacent_pair_incidence", adjacent_found == adjacent_expected,
                   {"found": adjacent_found, "expected": adjacent_expected}))
    checks.append(("disjoint_pair_incidence", disjoint_found == disjoint_expected,
                   {"found": disjoint_found, "expected": disjoint_expected}))

    # General forced-linear-forest tests.
    patterns = {
        "single_edge": [(0, 1)],
        "adjacent_pair": [(0, 1), (1, 2)],
        "disjoint_pair": [(0, 1), (2, 3)],
        "path3": [(0, 1), (1, 2), (2, 3)],
        "triangle_control": [(0, 1), (1, 2), (2, 0)],
    }
    if n >= 5:
        patterns["path2_plus_edge"] = [(0, 1), (1, 2), (3, 4)]
    if n >= 6:
        patterns["matching3"] = [(0, 1), (2, 3), (4, 5)]

    forced_rows = []
    forest_ok = True
    for name, forced in patterns.items():
        found = count_containing(edge_sets, forced)
        expected = predicted_linear_forest_count(n, forced)
        ok = found == expected
        forest_ok &= ok
        lf, k, c = linear_forest_components(forced)
        forced_rows.append({
            "n": n,
            "pattern": name,
            "forced_edges": ";".join(f"{a}-{b}" for a, b in forced),
            "linear_forest": lf,
            "k_edges": k,
            "path_components": c,
            "found": found,
            "predicted": expected,
            "pass": ok,
        })
    checks.append(("forced_linear_forest_formula_examples", forest_ok, {}))

    # Raw edge-overlap with a reference cycle. Relabelling transitivity makes
    # this distribution source-independent; we also verify against several
    # alternate source cycles below.
    ref_edges = edges_of(tuple(range(n)))
    overlap_counts = Counter(len(es & ref_edges) for es in edge_sets)
    mean, var = overlap_moments(overlap_counts, len(cycles))
    mean_formula = 2 * n / (n - 1)
    var_formula = 2 * n * (n - 3) / ((n - 1) ** 2)
    moment_ok = abs(mean - mean_formula) < 1e-12 and abs(var - var_formula) < 1e-12
    checks.append(("overlap_moments", moment_ok,
                   {"mean": mean, "mean_formula": mean_formula,
                    "variance": var, "variance_formula": var_formula}))

    forbidden_ok = overlap_counts.get(n - 1, 0) == 0
    checks.append(("no_distinct_n_minus_1_overlap", forbidden_ok,
                   {"count": overlap_counts.get(n - 1, 0)}))

    # Check source-independence for up to five deterministic source cycles.
    source_indices = sorted(set([0, len(cycles)//4, len(cycles)//2, (3*len(cycles))//4, len(cycles)-1]))
    overlap_source_ok = True
    for idx in source_indices:
        src = edge_sets[idx]
        dist = Counter(len(es & src) for es in edge_sets)
        if dist != overlap_counts:
            overlap_source_ok = False
            break
    checks.append(("overlap_distribution_source_independence", overlap_source_ok,
                   {"sources_checked": len(source_indices)}))

    if strict and not all(ok for _, ok, _ in checks):
        failed = [(name, info) for name, ok, info in checks if not ok]
        raise AssertionError(f"n={n} strict checks failed: {failed}")

    summary = {
        "n": n,
        "states": len(cycles),
        "expected_states": expected_states,
        "edge_incidence": incidence_values[0] if len(incidence_values) == 1 else None,
        "expected_edge_incidence": expected_incidence,
        "adjacent_pair_incidence": adjacent_found,
        "disjoint_pair_incidence": disjoint_found,
        "mean_overlap": mean,
        "mean_overlap_formula": mean_formula,
        "variance_overlap": var,
        "variance_overlap_formula": var_formula,
        "overlap_support": sorted(overlap_counts),
        "all_checks_pass": all(ok for _, ok, _ in checks),
    }
    overlap_rows = [
        {"n": n, "overlap": k, "count": v, "fraction": v / len(cycles)}
        for k, v in sorted(overlap_counts.items())
    ]
    check_rows = [
        {"n": n, "check": name, "pass": ok, "details": json.dumps(info, sort_keys=True)}
        for name, ok, info in checks
    ]
    return summary, overlap_rows, forced_rows, check_rows


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
    ap.add_argument("--n-max", type=int, default=10)
    ap.add_argument("--out-dir", default="runs/ehf_hc_raw_01")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    if args.n_min < 4:
        raise SystemExit("This audit starts at n=4; use --n-min >= 4")
    if args.n_max < args.n_min:
        raise SystemExit("--n-max must be >= --n-min")

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    summaries = []
    overlaps = []
    forced = []
    checks = []

    print("=" * 100)
    print("EHF-HC-RAW-01: DEFINITION LOCK, DIHEDRAL QUOTIENT, INCIDENCE NEUTRALITY, RAW OVERLAP CENSUS")
    print("=" * 100)
    print(f"n range: {args.n_min}..{args.n_max}")
    print("No LR3 / LR2 / 2-opt / sector / growth rule is used.\n")

    for n in range(args.n_min, args.n_max + 1):
        summary, o, f, c = audit_n(n, strict=args.strict)
        summaries.append(summary)
        overlaps.extend(o)
        forced.extend(f)
        checks.extend(c)
        support = ",".join(map(str, summary["overlap_support"]))
        print(
            f"n={n:2d}  states={summary['states']:8d}  "
            f"edge-incidence={summary['edge_incidence']:8d}  "
            f"adj/disjoint pair={summary['adjacent_pair_incidence']}/{summary['disjoint_pair_incidence']}  "
            f"overlap mean={summary['mean_overlap']:.9f}  var={summary['variance_overlap']:.9f}  "
            f"support=[{support}]  PASS={summary['all_checks_pass']}"
        )

    write_csv(out / "summary.csv", summaries)
    write_csv(out / "overlap_distribution.csv", overlaps)
    write_csv(out / "forced_pattern_counts.csv", forced)
    write_csv(out / "checks.csv", checks)
    with (out / "summary.json").open("w") as f:
        json.dump({"summaries": summaries, "checks": checks}, f, indent=2)

    all_pass = all(r["all_checks_pass"] for r in summaries)
    print("\nExact identities audited:")
    print("  |HC_n| = (n-1)!/2")
    print("  cycles containing a fixed edge = (n-2)!")
    print("  cycles containing two adjacent fixed edges = (n-3)!")
    print("  cycles containing two disjoint fixed edges = 2(n-3)!")
    print("  linear-forest examples: N(F)=2^(c-1)(n-k-1)!")
    print("  E[edge overlap] = 2n/(n-1)")
    print("  Var(edge overlap) = 2n(n-3)/(n-1)^2")
    print("  overlap n-1 is absent for distinct cycles")
    print(f"\noutput: {out}")
    if all_pass:
        print("EHF_HC_RAW_01_DEFINITION_INCIDENCE_OVERLAP_PASS")
    else:
        print("EHF_HC_RAW_01_CHECK_FAILURE")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
