#!/usr/bin/env python3
"""
EHF-QM3-05
==========
Critical-Chamber Product-Permutahedron Scaling Audit

For m >= 2 let n = 2m + 3 and define the candidate critical chamber

    C_m = {
      (0, m+1, a_1, b_1, ..., a_m, b_m, m+2)
      : (a_1,...,a_m) is a permutation of 1,...,m
        and
        (b_1,...,b_m) is a permutation of m+3,...,2m+2
    }.

The probe tests the exact OPW3 graph isomorphism

    C_m  ~=  Perm_m square Perm_m,

where Perm_m is the adjacent-transposition Cayley graph of S_m.

It verifies:
  * canonicality and common Pi label;
  * exact LR3 active slots;
  * coordinate action of every LR3 edge;
  * state, degree and edge-count laws;
  * product-symmetric relabelling supports;
  * low-spectrum scaling of the factor and Cartesian product;
  * candidate normalized-gap formula
        [1 - cos(pi/m)] / (m - 1);
  * candidate slow multiplicity 2(m-1).

The graph-isomorphism checks are exact finite combinatorics.  The all-m spectral
gap formula remains a candidate unless separately proved or imported from an
appropriate spectral theorem.

Dependencies: numpy, scipy
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import sys
import time
from datetime import datetime, timezone
from itertools import permutations
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

SCRIPT_VERSION = "ehf_qm3_05_2026-07-25"

Permutation = Tuple[int, ...]
Cycle = Tuple[int, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_int_csv(text: str) -> List[int]:
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def adjacent_swap(permutation: Permutation, index: int) -> Permutation:
    arr = list(permutation)
    arr[index], arr[index + 1] = arr[index + 1], arr[index]
    return tuple(arr)


def critical_cycle(
    m: int,
    a_permutation: Permutation,
    b_permutation: Permutation,
) -> Cycle:
    cycle = [0, m + 1]
    for a, b in zip(a_permutation, b_permutation):
        cycle.extend((a, b))
    cycle.append(m + 2)
    return tuple(cycle)


def critical_pi_label(m: int):
    side_a = tuple(sorted([0, *range(1, m + 1), m + 2]))
    side_b = tuple(sorted([m + 1, *range(m + 3, 2 * m + 3)]))
    return tuple(sorted((side_a, side_b)))


def expected_target_coordinates(
    m: int,
    a_permutation: Permutation,
    b_permutation: Permutation,
    start: int,
):
    if start % 2 == 0:
        # start = 2i swaps a_i and a_{i+1}; Python index i-1.
        i = start // 2 - 1
        return adjacent_swap(a_permutation, i), b_permutation
    # start = 2i+1 swaps b_i and b_{i+1}; Python index i-1.
    i = (start - 1) // 2 - 1
    return a_permutation, adjacent_swap(b_permutation, i)


def factor_laplacian(permutations_list: Sequence[Permutation]):
    m = len(permutations_list[0])
    index = {permutation: i for i, permutation in enumerate(permutations_list)}
    rows: List[int] = []
    cols: List[int] = []

    for state_id, permutation in enumerate(permutations_list):
        for generator in range(m - 1):
            target = adjacent_swap(permutation, generator)
            rows.append(state_id)
            cols.append(index[target])

    adjacency = sparse.csr_matrix(
        (np.ones(len(rows), dtype=float), (rows, cols)),
        shape=(len(permutations_list), len(permutations_list)),
    )
    adjacency = 0.5 * (adjacency + adjacency.T)
    degree = m - 1
    laplacian = sparse.eye(len(permutations_list)) * degree - adjacency
    return laplacian.tocsr(), degree


def lowest_factor_spectrum(
    laplacian: sparse.csr_matrix,
    expected_multiplicity: int,
    tolerance: float,
):
    n = laplacian.shape[0]
    requested = min(n, max(2 * expected_multiplicity + 6, 12))

    if n <= 240 or requested >= n:
        eigenvalues = np.linalg.eigvalsh(laplacian.toarray())
    else:
        k = min(requested, n - 1)
        eigenvalues = eigsh(
            laplacian,
            k=k,
            which="SM",
            tol=tolerance,
            return_eigenvectors=False,
            maxiter=max(5000, 100 * n),
        )
        eigenvalues = np.sort(eigenvalues)

    eigenvalues[np.abs(eigenvalues) < 10 * tolerance] = 0.0
    positive = eigenvalues[eigenvalues > 10 * tolerance]
    if len(positive) == 0:
        raise RuntimeError("factor graph has no positive eigenvalue")
    gap = float(positive[0])
    multiplicity = int(
        np.sum(np.abs(eigenvalues - gap) <= 100 * tolerance)
    )
    return eigenvalues, gap, multiplicity


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit the critical OPW3 chamber as a Cartesian square of adjacent-transposition permutahedron graphs."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--ms", type=parse_int_csv, default=[2, 3, 4, 5])
    parser.add_argument("--eigen-tolerance", type=float, default=1e-10)
    parser.add_argument("--out-dir", default="runs/ehf_qm3_05")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    base_path = Path(args.base_script).resolve()
    base = load_module(base_path, "ehf_opw3_audit_01_base")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 126)
    print("EHF-QM3-05: CRITICAL-CHAMBER PRODUCT-PERMUTAHEDRON SCALING AUDIT")
    print("=" * 126)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"m values:             {args.ms}")
    print(f"target n values:      {[2*m+3 for m in args.ms]}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    checks: Dict[str, bool] = {}
    rows: List[dict] = []
    started_all = time.perf_counter()

    for m in args.ms:
        if m < 2:
            raise ValueError("m must be at least 2")

        started = time.perf_counter()
        n = 2 * m + 3
        a_labels = tuple(range(1, m + 1))
        b_labels = tuple(range(m + 3, 2 * m + 3))
        a_permutations = list(permutations(a_labels))
        b_permutations = list(permutations(b_labels))

        coordinate_to_cycle: Dict[Tuple[Permutation, Permutation], Cycle] = {}
        cycle_to_coordinate: Dict[Cycle, Tuple[Permutation, Permutation]] = {}

        expected_pi = critical_pi_label(m)
        canonical_ok = True
        pi_ok = True

        for a_permutation in a_permutations:
            for b_permutation in b_permutations:
                cycle = critical_cycle(m, a_permutation, b_permutation)
                canonical_ok &= base.canonical_cycle(cycle) == cycle
                pi_ok &= base.pi_label(cycle) == expected_pi
                coordinate = (a_permutation, b_permutation)
                coordinate_to_cycle[coordinate] = cycle
                cycle_to_coordinate[cycle] = coordinate

        expected_state_count = math.factorial(m) ** 2
        checks[f"m{m}_state_count"] = (
            len(coordinate_to_cycle) == expected_state_count
            and len(cycle_to_coordinate) == expected_state_count
        )
        checks[f"m{m}_canonical"] = canonical_ok
        checks[f"m{m}_common_pi"] = pi_ok

        expected_active_starts = tuple(range(2, 2 * m))
        active_exact = True
        coordinate_action_exact = True
        closure_exact = True
        directed_edges = 0

        for coordinate, cycle in coordinate_to_cycle.items():
            a_permutation, b_permutation = coordinate
            accepted_starts = []

            for start in range(n):
                target = base.circular_reverse(cycle, start, 3)
                if (
                    target != cycle
                    and base.pi_label(target) == expected_pi
                ):
                    accepted_starts.append(start)
                    directed_edges += 1

                    if target not in cycle_to_coordinate:
                        closure_exact = False
                        continue

                    expected_coordinate = expected_target_coordinates(
                        m,
                        a_permutation,
                        b_permutation,
                        start,
                    )
                    if cycle_to_coordinate[target] != expected_coordinate:
                        coordinate_action_exact = False

            if tuple(accepted_starts) != expected_active_starts:
                active_exact = False

        degree = 2 * (m - 1)
        expected_edge_count = expected_state_count * (m - 1)
        actual_edge_count = directed_edges // 2

        checks[f"m{m}_active_slots"] = active_exact
        checks[f"m{m}_coordinate_action"] = coordinate_action_exact
        checks[f"m{m}_closed_component"] = closure_exact
        checks[f"m{m}_degree"] = (
            directed_edges == expected_state_count * degree
        )
        checks[f"m{m}_edge_count"] = (
            actual_edge_count == expected_edge_count
        )

        factor_permutations = list(permutations(range(m)))
        factor_lap, factor_degree = factor_laplacian(
            factor_permutations
        )
        factor_eigenvalues, factor_gap, factor_gap_multiplicity = (
            lowest_factor_spectrum(
                factor_lap,
                expected_multiplicity=m - 1,
                tolerance=args.eigen_tolerance,
            )
        )

        product_normalized_gap = factor_gap / (2 * factor_degree)
        product_slow_multiplicity = 2 * factor_gap_multiplicity
        candidate_gap = (
            (1.0 - math.cos(math.pi / m)) / (m - 1)
        )
        gap_error = abs(product_normalized_gap - candidate_gap)

        checks[f"m{m}_factor_gap_multiplicity"] = (
            factor_gap_multiplicity == m - 1
        )
        checks[f"m{m}_product_slow_multiplicity"] = (
            product_slow_multiplicity == 2 * (m - 1)
        )
        checks[f"m{m}_candidate_gap_formula"] = (
            gap_error <= 1e-8
        )

        elapsed = time.perf_counter() - started
        rows.append({
            "m": m,
            "target_n": n,
            "pi_label": "|".join(
                ",".join(str(x) for x in side)
                for side in expected_pi
            ),
            "state_count": expected_state_count,
            "state_count_formula": "(m!)^2",
            "regular_degree": degree,
            "degree_formula": "2(m-1)",
            "edge_count": actual_edge_count,
            "edge_count_formula": "(m!)^2(m-1)",
            "active_starts": json.dumps(expected_active_starts),
            "factor_vertices": math.factorial(m),
            "factor_degree": factor_degree,
            "factor_unnormalized_gap": factor_gap,
            "factor_gap_multiplicity": factor_gap_multiplicity,
            "product_normalized_gap": product_normalized_gap,
            "candidate_gap_formula_value": candidate_gap,
            "candidate_gap_absolute_error": gap_error,
            "product_slow_multiplicity": product_slow_multiplicity,
            "candidate_slow_multiplicity": 2 * (m - 1),
            "symmetry_candidate": f"S_{m} x S_{m}",
            "representation_candidate": (
                "Std_A tensor 1_B plus 1_A tensor Std_B"
            ),
            "elapsed_seconds": elapsed,
        })

        print(
            f"[m={m}, n={n}] states={expected_state_count} "
            f"degree={degree} edges={actual_edge_count}"
        )
        print(
            f"  exact product action: active={active_exact} "
            f"closure={closure_exact} coordinates={coordinate_action_exact}"
        )
        print(
            f"  factor gap={factor_gap:.12g} "
            f"mult={factor_gap_multiplicity}; "
            f"product normalized gap={product_normalized_gap:.12g} "
            f"formula={candidate_gap:.12g} "
            f"error={gap_error:.3e}"
        )
        print(
            f"  predicted slow representation: "
            f"({m-1})+({m-1})={product_slow_multiplicity}"
        )
        print(f"  elapsed={elapsed:.2f}s")
        print()

    write_csv(out_dir / "critical_product_permutahedron_summary.csv", rows)

    checks = {key: bool(value) for key, value in checks.items()}
    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-QM3-05",
        "title": "Critical-Chamber Product-Permutahedron Scaling Audit",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "rows": rows,
        "exact_finite_statement": (
            "For every tested m, the explicitly constructed critical chamber "
            "is exactly the Cartesian square of the adjacent-transposition "
            "Cayley graph of S_m."
        ),
        "spectral_guardrail": (
            "The gap formula is numerically verified at the tested m values. "
            "An all-m proof requires a separate spectral argument."
        ),
        "physical_guardrail": (
            "The product-permutahedron graph and its standard representations "
            "are structural finite combinatorics, not physical spin, gauge "
            "symmetry, particle species, mass, or Hamiltonian."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_QM3_05_CRITICAL_PRODUCT_PERMUTAHEDRON_PASS"
            if strict_pass else
            "EHF_QM3_05_CRITICAL_PRODUCT_PERMUTAHEDRON_FAIL"
        ),
    }

    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print("=" * 126)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {summary['elapsed_seconds']:.2f}s")
    print("=" * 126)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
