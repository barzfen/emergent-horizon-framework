#!/usr/bin/env python3
"""
EHF-OPW3-AUDIT-03
=================
Normalized-Laplacian Slow-Sector Survival

Compares the low normalized-Laplacian spectra of OPW3, LR2 and OPW23 on the
same canonical Hamilton-cycle state space.  For OPW3 and OPW23, whose chamber
partitions are already known to coincide at n=5,7,9, it also computes paired
slow-subspace principal-angle alignments.

The probe additionally measures how strongly the low modes are represented by:
  * the four LR3 active signatures;
  * the four LR2 active signatures;
  * the joint 16-signature crosswalk.

This is a spectral survival audit.  It does not yet define quantum dynamics,
physical energies, masses, phases, or particles.

Dependencies
------------
numpy
scipy

Example
-------
python3 scripts/ehf_opw3_audit_03_normalized_laplacian_slow_sector_survival.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --ns 5,7,9 \
  --graphs OPW3,LR2,OPW23 \
  --eigs-per-component 13 \
  --slow-dim 8 \
  --out-dir runs/ehf_opw3_audit_03 \
  --strict
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import statistics
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

SCRIPT_VERSION = "ehf_opw3_audit_03_2026-07-22"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_int_csv(text: str) -> List[int]:
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def parse_graph_csv(text: str) -> List[str]:
    allowed = {"OPW3", "LR2", "OPW23"}
    values = [x.strip().upper() for x in text.split(",") if x.strip()]
    bad = [x for x in values if x not in allowed]
    if bad:
        raise argparse.ArgumentTypeError(
            f"unknown graph(s) {bad}; choose from {sorted(allowed)}"
        )
    if not values:
        raise argparse.ArgumentTypeError("expected at least one graph")
    return values


def load_base(path: Path):
    spec = importlib.util.spec_from_file_location("ehf_opw3_audit_01_base", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load base script: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, rows: Sequence[dict], fieldnames: Sequence[str] | None = None) -> None:
    if fieldnames is None:
        if not rows:
            return
        fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def quantiles(values: Sequence[float]) -> dict:
    if not values:
        return {
            "min": None, "median": None, "mean": None, "max": None
        }
    return {
        "min": float(min(values)),
        "median": float(statistics.median(values)),
        "mean": float(statistics.fmean(values)),
        "max": float(max(values)),
    }


def component_partition(adjacency: Sequence[Set[int]]) -> List[List[int]]:
    seen: Set[int] = set()
    out: List[List[int]] = []
    for start in range(len(adjacency)):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        comp: List[int] = []
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        out.append(sorted(comp))
    out.sort(key=lambda c: (-len(c), c[0]))
    return out


def partition_key(components: Sequence[Sequence[int]]) -> Set[frozenset[int]]:
    return {frozenset(comp) for comp in components}


def local_adjacency(
    global_adjacency: Sequence[Set[int]],
    vertices: Sequence[int],
) -> sparse.csr_matrix:
    index = {state: i for i, state in enumerate(vertices)}
    rows: List[int] = []
    cols: List[int] = []
    for state in vertices:
        i = index[state]
        for target in global_adjacency[state]:
            j = index.get(target)
            if j is not None:
                rows.append(i)
                cols.append(j)
    data = np.ones(len(rows), dtype=float)
    return sparse.csr_matrix(
        (data, (rows, cols)),
        shape=(len(vertices), len(vertices)),
        dtype=float,
    )


def low_normalized_laplacian_modes(
    adjacency: sparse.csr_matrix,
    eigs_per_component: int,
    dense_cutoff: int,
    tolerance: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, str]:
    n = adjacency.shape[0]
    degrees = np.asarray(adjacency.sum(axis=1)).reshape(-1)

    if n == 1:
        return (
            np.array([0.0]),
            np.array([[1.0]]),
            degrees,
            "singleton",
        )

    if np.any(degrees <= 0):
        raise RuntimeError("non-singleton component contains an isolated state")

    inv_sqrt = 1.0 / np.sqrt(degrees)
    dmat = sparse.diags(inv_sqrt)
    normalized_adjacency = (dmat @ adjacency @ dmat).tocsr()

    requested = min(max(2, eigs_per_component), n)

    if n <= dense_cutoff or requested >= n:
        s_dense = normalized_adjacency.toarray()
        mu, vectors = np.linalg.eigh(s_dense)
        order = np.argsort(mu)[::-1]
        mu = mu[order][:requested]
        vectors = vectors[:, order][:, :requested]
        method = "dense"
    else:
        k = min(requested, n - 1)
        mu, vectors = eigsh(
            normalized_adjacency,
            k=k,
            which="LA",
            tol=tolerance,
            maxiter=max(5000, 100 * n),
        )
        order = np.argsort(mu)[::-1]
        mu = mu[order]
        vectors = vectors[:, order]
        method = "eigsh_LA"

    eigenvalues = 1.0 - mu
    eigenvalues[np.abs(eigenvalues) < 10 * tolerance] = 0.0
    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    vectors = vectors[:, order]

    # Deterministic column signs for reproducible ledgers.
    for j in range(vectors.shape[1]):
        pivot = int(np.argmax(np.abs(vectors[:, j])))
        if vectors[pivot, j] < 0:
            vectors[:, j] *= -1.0

    return eigenvalues, vectors, degrees, method


def observable_basis(
    codes: Sequence[object],
    degrees: np.ndarray,
    tolerance: float = 1e-11,
) -> Tuple[np.ndarray, int]:
    n = len(codes)
    unique_codes = sorted(set(codes), key=repr)
    if n == 0 or len(unique_codes) <= 1:
        return np.zeros((n, 0), dtype=float), len(unique_codes)

    code_to_col = {code: j for j, code in enumerate(unique_codes)}
    indicator = np.zeros((n, len(unique_codes)), dtype=float)
    for i, code in enumerate(codes):
        indicator[i, code_to_col[code]] = 1.0

    if float(degrees.sum()) > 0:
        stationary = degrees / degrees.sum()
    else:
        stationary = np.full(n, 1.0 / n)

    means = stationary @ indicator
    weighted = np.sqrt(stationary)[:, None] * (indicator - means[None, :])

    if weighted.size == 0:
        return np.zeros((n, 0), dtype=float), len(unique_codes)

    u, singular_values, _ = np.linalg.svd(weighted, full_matrices=False)
    rank = int(np.sum(singular_values > tolerance))
    return u[:, :rank], len(unique_codes)


def projection_mass(basis: np.ndarray, vector: np.ndarray) -> float:
    if basis.shape[1] == 0:
        return 0.0
    return float(np.linalg.norm(basis.T @ vector) ** 2)


def principal_alignment(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    if u.shape[1] == 0 or v.shape[1] == 0:
        return np.zeros(0, dtype=float)
    singular_values = np.linalg.svd(u.T @ v, compute_uv=False)
    return np.clip(singular_values, 0.0, 1.0)


def pi_text(label) -> str:
    return "|".join(",".join(str(x) for x in side) for side in label)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit OPW3 normalized-Laplacian slow sectors against OPW23."
    )
    parser.add_argument(
        "--base-script",
        required=True,
        help="path to Audit-01 foundation engine",
    )
    parser.add_argument("--ns", type=parse_int_csv, default=[5, 7, 9])
    parser.add_argument(
        "--graphs",
        type=parse_graph_csv,
        default=["OPW3", "LR2", "OPW23"],
    )
    parser.add_argument(
        "--eigs-per-component",
        type=int,
        default=13,
        help="number of lowest normalized-Laplacian eigenpairs retained, including zero mode",
    )
    parser.add_argument(
        "--slow-dim",
        type=int,
        default=8,
        help="number of nontrivial low modes used in paired-subspace comparisons",
    )
    parser.add_argument(
        "--dense-cutoff",
        type=int,
        default=160,
        help="components at or below this size use dense diagonalization",
    )
    parser.add_argument(
        "--eigen-tolerance",
        type=float,
        default=1e-10,
    )
    parser.add_argument(
        "--out-dir",
        default="runs/ehf_opw3_audit_03",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_path = Path(args.base_script).resolve()
    base = load_base(base_path)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 120)
    print("EHF-OPW3-AUDIT-03: NORMALIZED-LAPLACIAN SLOW-SECTOR SURVIVAL")
    print("=" * 120)
    print(f"script version:          {SCRIPT_VERSION}")
    print(f"base engine:             {base_path}")
    print(f"n values:                {args.ns}")
    print(f"graphs:                  {args.graphs}")
    print(f"eigenpairs/component:    {args.eigs_per_component}")
    print(f"paired slow dimension:   {args.slow_dim}")
    print(f"dense cutoff:            {args.dense_cutoff}")
    print(f"output directory:        {out_dir.resolve()}")
    print(f"strict:                  {args.strict}")
    print()

    checks: Dict[str, bool] = {}
    component_rows: List[dict] = []
    eigenmode_rows: List[dict] = []
    overlap_rows: List[dict] = []
    alignment_rows: List[dict] = []
    aggregate_rows: List[dict] = []
    summaries: Dict[str, dict] = {}
    started_all = time.perf_counter()

    for n in args.ns:
        if n % 2 == 0:
            raise ValueError(f"OPW requires odd n; received {n}")

        started_n = time.perf_counter()
        cycles = base.generate_cycles(n)
        cycle_index = {cycle: i for i, cycle in enumerate(cycles)}
        labels = [base.pi_label(cycle) for cycle in cycles]

        # Build all three because the signature crosswalk needs LR2 and LR3
        # even when the user asks to diagonalize only a subset.
        builds = {
            name: base.build_preserve_graph(
                cycles=cycles,
                cycle_index=cycle_index,
                labels=labels,
                name=name,
                lengths=base.GRAPH_LENGTHS[name],
            )
            for name in ("OPW3", "LR2", "OPW23")
        }
        components = {
            name: component_partition(builds[name].adjacency)
            for name in ("OPW3", "LR2", "OPW23")
        }

        same_foundational_partition = (
            partition_key(components["OPW3"])
            == partition_key(components["OPW23"])
        )
        checks[f"n{n}_OPW3_OPW23_partition_equal"] = same_foundational_partition

        lr3_codes_global = builds["OPW3"].accepted_slots
        lr2_codes_global = builds["LR2"].accepted_slots
        joint_codes_global = [
            (lr3_codes_global[i], lr2_codes_global[i])
            for i in range(len(cycles))
        ]

        spectral_cache: Dict[Tuple[str, frozenset[int]], dict] = {}
        graph_gaps: Dict[str, List[float]] = defaultdict(list)
        graph_component_sizes: Dict[str, List[int]] = defaultdict(list)
        graph_signature_capture: Dict[Tuple[str, str], List[Tuple[int, float]]] = defaultdict(list)

        print(f"[n={n}] states={len(cycles)} OPW3-components={len(components['OPW3'])}")

        for graph_name in args.graphs:
            for component_id, vertices in enumerate(components[graph_name]):
                adjacency = local_adjacency(builds[graph_name].adjacency, vertices)
                eigenvalues, eigenvectors, degrees, method = low_normalized_laplacian_modes(
                    adjacency=adjacency,
                    eigs_per_component=args.eigs_per_component,
                    dense_cutoff=args.dense_cutoff,
                    tolerance=args.eigen_tolerance,
                )

                size = len(vertices)
                edges = int(adjacency.nnz // 2)
                gap = float(eigenvalues[1]) if len(eigenvalues) > 1 else 0.0
                nontrivial_available = max(0, len(eigenvalues) - 1)
                slow_r = min(args.slow_dim, nontrivial_available)

                checks[f"n{n}_{graph_name}_c{component_id}_lambda0"] = (
                    abs(float(eigenvalues[0])) <= 1e-7
                )
                checks[f"n{n}_{graph_name}_c{component_id}_range"] = bool(
                    np.all(eigenvalues >= -1e-7)
                    and np.all(eigenvalues <= 2.0 + 1e-7)
                )
                checks[f"n{n}_{graph_name}_c{component_id}_gap_positive"] = (
                    True if size == 1 else gap > 1e-9
                )

                degree_mean = float(degrees.mean()) if len(degrees) else 0.0
                degree_std = float(degrees.std()) if len(degrees) else 0.0
                degree_cv = degree_std / degree_mean if degree_mean else 0.0

                component_rows.append({
                    "n": n,
                    "graph": graph_name,
                    "component_id": component_id,
                    "pi_label": pi_text(labels[vertices[0]]),
                    "states": size,
                    "edges": edges,
                    "degree_min": int(degrees.min()) if len(degrees) else 0,
                    "degree_max": int(degrees.max()) if len(degrees) else 0,
                    "degree_mean": degree_mean,
                    "degree_cv": degree_cv,
                    "eigensolver": method,
                    "eigenpairs_retained": len(eigenvalues),
                    "normalized_laplacian_gap": gap,
                    "relaxation_time_inverse_gap": (
                        1.0 / gap if gap > 0 else None
                    ),
                    "lambda_last_retained": float(eigenvalues[-1]),
                    "slow_modes_retained": slow_r,
                })

                graph_gaps[graph_name].append(gap)
                graph_component_sizes[graph_name].append(size)

                for mode_index, value in enumerate(eigenvalues):
                    vector = eigenvectors[:, mode_index]
                    ipr = float(np.sum(vector ** 4))
                    eigenmode_rows.append({
                        "n": n,
                        "graph": graph_name,
                        "component_id": component_id,
                        "component_states": size,
                        "mode_index": mode_index,
                        "eigenvalue": float(value),
                        "is_zero_mode": mode_index == 0,
                        "inverse_participation_ratio": ipr,
                        "participation_ratio": (1.0 / ipr if ipr > 0 else None),
                    })

                partition_codes = {
                    "LR3_SIGNATURE": [lr3_codes_global[v] for v in vertices],
                    "LR2_SIGNATURE": [lr2_codes_global[v] for v in vertices],
                    "LR3xLR2_SIGNATURE": [joint_codes_global[v] for v in vertices],
                }

                partition_bases: Dict[str, np.ndarray] = {}
                for partition_name, codes in partition_codes.items():
                    basis, cell_count = observable_basis(codes, degrees)
                    partition_bases[partition_name] = basis

                    masses: List[float] = []
                    for local_mode in range(1, 1 + slow_r):
                        mass = projection_mass(basis, eigenvectors[:, local_mode])
                        masses.append(mass)
                        overlap_rows.append({
                            "n": n,
                            "graph": graph_name,
                            "component_id": component_id,
                            "component_states": size,
                            "partition": partition_name,
                            "partition_cells_realized": cell_count,
                            "observable_subspace_dimension": basis.shape[1],
                            "mode_index": local_mode,
                            "eigenvalue": float(eigenvalues[local_mode]),
                            "projection_mass": mass,
                        })

                    mean_mass = float(np.mean(masses)) if masses else 0.0
                    graph_signature_capture[(graph_name, partition_name)].append(
                        (size, mean_mass)
                    )

                spectral_cache[(graph_name, frozenset(vertices))] = {
                    "vertices": vertices,
                    "eigenvalues": eigenvalues,
                    "eigenvectors": eigenvectors,
                    "degrees": degrees,
                    "gap": gap,
                    "slow_r": slow_r,
                }

        # Paired OPW3/OPW23 slow-subspace comparison.
        if {"OPW3", "OPW23"}.issubset(set(args.graphs)):
            for pair_id, vertices in enumerate(components["OPW3"]):
                key = frozenset(vertices)
                data3 = spectral_cache[("OPW3", key)]
                data23 = spectral_cache[("OPW23", key)]

                r = min(
                    args.slow_dim,
                    data3["slow_r"],
                    data23["slow_r"],
                )
                u3 = data3["eigenvectors"][:, 1:1 + r]
                u23 = data23["eigenvectors"][:, 1:1 + r]
                cosines = principal_alignment(u3, u23)
                squared = cosines ** 2

                checks[f"n{n}_pair{pair_id}_alignment_range"] = bool(
                    np.all(cosines >= -1e-10)
                    and np.all(cosines <= 1.0 + 1e-10)
                )

                lam3 = data3["eigenvalues"][1:1 + r]
                lam23 = data23["eigenvalues"][1:1 + r]
                rms_difference = (
                    float(np.sqrt(np.mean((lam3 - lam23) ** 2)))
                    if r else 0.0
                )

                alignment_rows.append({
                    "n": n,
                    "pair_id": pair_id,
                    "pi_label": pi_text(labels[vertices[0]]),
                    "states": len(vertices),
                    "slow_dimension": r,
                    "gap_OPW3": data3["gap"],
                    "gap_OPW23": data23["gap"],
                    "gap_ratio_OPW23_over_OPW3": (
                        data23["gap"] / data3["gap"]
                        if data3["gap"] > 0 else None
                    ),
                    "slow_eigenvalue_rms_difference": rms_difference,
                    "principal_cosine_min": (
                        float(cosines.min()) if len(cosines) else None
                    ),
                    "principal_cosine_mean": (
                        float(cosines.mean()) if len(cosines) else None
                    ),
                    "principal_cosine_squared_mean": (
                        float(squared.mean()) if len(squared) else None
                    ),
                    "principal_cosines": json.dumps(
                        [float(x) for x in cosines]
                    ),
                })

        # Aggregate graph and observable summaries.
        for graph_name in args.graphs:
            gaps = graph_gaps[graph_name]
            gap_stats = quantiles(gaps)
            row = {
                "n": n,
                "graph": graph_name,
                "states": len(cycles),
                "components": len(components[graph_name]),
                "largest_component": max(graph_component_sizes[graph_name]),
                "gap_min": gap_stats["min"],
                "gap_median": gap_stats["median"],
                "gap_mean": gap_stats["mean"],
                "gap_max": gap_stats["max"],
            }
            for partition_name in (
                "LR3_SIGNATURE",
                "LR2_SIGNATURE",
                "LR3xLR2_SIGNATURE",
            ):
                weighted = graph_signature_capture[(graph_name, partition_name)]
                total_weight = sum(size for size, _ in weighted)
                capture = (
                    sum(size * value for size, value in weighted) / total_weight
                    if total_weight else 0.0
                )
                row[f"{partition_name}_slow_capture_weighted_mean"] = capture
            aggregate_rows.append(row)

        if alignment_rows:
            n_alignment = [
                r for r in alignment_rows
                if r["n"] == n
                and r["principal_cosine_squared_mean"] is not None
            ]
            weighted_den = sum(r["states"] for r in n_alignment)
            weighted_alignment = (
                sum(
                    r["states"] * r["principal_cosine_squared_mean"]
                    for r in n_alignment
                ) / weighted_den
                if weighted_den else None
            )
        else:
            weighted_alignment = None

        summaries[f"n{n}"] = {
            "states": len(cycles),
            "OPW3_components": len(components["OPW3"]),
            "OPW23_components": len(components["OPW23"]),
            "OPW3_OPW23_partition_equal": same_foundational_partition,
            "weighted_mean_squared_slow_subspace_alignment": weighted_alignment,
            "elapsed_seconds": time.perf_counter() - started_n,
        }

        opw3_agg = next(
            (r for r in aggregate_rows if r["n"] == n and r["graph"] == "OPW3"),
            None,
        )
        opw23_agg = next(
            (r for r in aggregate_rows if r["n"] == n and r["graph"] == "OPW23"),
            None,
        )
        print(
            f"  OPW3 gap median={opw3_agg['gap_median']:.8f} "
            f"mean={opw3_agg['gap_mean']:.8f}"
            if opw3_agg else ""
        )
        print(
            f"  OPW23 gap median={opw23_agg['gap_median']:.8f} "
            f"mean={opw23_agg['gap_mean']:.8f}"
            if opw23_agg else ""
        )
        if weighted_alignment is not None:
            print(
                f"  paired slow-subspace mean squared alignment="
                f"{weighted_alignment:.8f}"
            )
        print(f"  elapsed={summaries[f'n{n}']['elapsed_seconds']:.2f}s")
        print()

    write_csv(out_dir / "spectral_component_summary.csv", component_rows)
    write_csv(out_dir / "low_eigenmode_summary.csv", eigenmode_rows)
    write_csv(out_dir / "signature_spectral_overlap.csv", overlap_rows)
    write_csv(out_dir / "paired_slow_subspace_alignment.csv", alignment_rows)
    write_csv(out_dir / "graph_aggregate_summary.csv", aggregate_rows)

    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-OPW3-AUDIT-03",
        "title": "Normalized-Laplacian Slow-Sector Survival",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "caveat": (
            "Low normalized-Laplacian modes are structural diffusion modes. "
            "This probe does not identify them with physical Hamiltonian energy "
            "eigenstates, particles, masses, or quantum phases."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_OPW3_AUDIT_03_NORMALIZED_LAPLACIAN_SLOW_SECTOR_PASS"
            if strict_pass
            else "EHF_OPW3_AUDIT_03_NORMALIZED_LAPLACIAN_SLOW_SECTOR_FAIL"
        ),
    }

    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print("=" * 120)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {summary['elapsed_seconds']:.2f}s")
    print("=" * 120)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
