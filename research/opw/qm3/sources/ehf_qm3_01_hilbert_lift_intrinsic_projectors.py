#!/usr/bin/env python3
"""
EHF-QM3-01
==========
OPW3 Hilbert Lift and Intrinsic Slow-Sector Projectors

Constructs finite chamber Hilbert spaces, the stationary and complete lowest
normalized-Laplacian eigenspaces, reference-chart packet/ancestry/growth
subspaces, and targeted all-chart intersections when a chart misses part of a
degenerate lowest eigenspace.

The normalized Laplacian is used as a canonical structural self-adjoint
operator, not yet as a physical Hamiltonian.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

SCRIPT_VERSION = "ehf_qm3_01_v2_2026-07-25"


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


def normalized_laplacian(adjacency: Sequence[Sequence[int]]):
    n = len(adjacency)
    degree = np.array([len(row) for row in adjacency], dtype=float)
    if n == 1 and degree[0] == 0:
        return np.zeros((1, 1), dtype=float), degree

    rows, cols = [], []
    for u, neighbours in enumerate(adjacency):
        for v in neighbours:
            rows.append(u)
            cols.append(v)
    a = sparse.csr_matrix(
        (np.ones(len(rows)), (rows, cols)), shape=(n, n), dtype=float
    ).toarray()
    inv = 1.0 / np.sqrt(degree)
    s = inv[:, None] * a * inv[None, :]
    return np.eye(n) - s, degree


def low_modes(lnorm, count, dense_cutoff, tolerance):
    n = lnorm.shape[0]
    if n == 1:
        return np.array([0.0]), np.array([[1.0]])
    if n <= dense_cutoff:
        values, vectors = np.linalg.eigh(lnorm)
    else:
        k = min(count, n - 1)
        s = np.eye(n) - lnorm
        mu, vectors = eigsh(
            sparse.csr_matrix(s),
            k=k,
            which="LA",
            tol=tolerance,
            maxiter=max(5000, 100 * n),
        )
        values = 1.0 - mu
    order = np.argsort(values)
    values = values[order]
    vectors = vectors[:, order]
    values[np.abs(values) < tolerance] = 0.0
    return values, vectors


def partition_basis(colors: Sequence[int], degree: np.ndarray) -> np.ndarray:
    """Degree-weighted orthonormal cell indicators in O(n) assembly time."""
    color_array = np.asarray(colors)
    _, inverse = np.unique(color_array, return_inverse=True)
    q = int(inverse.max()) + 1
    n = len(colors)

    weights = np.sqrt(degree)
    if np.all(weights == 0):
        weights = np.ones(n, dtype=float)

    norm_sq = np.bincount(inverse, weights=weights ** 2, minlength=q)
    norms = np.sqrt(norm_sq)
    basis = np.zeros((n, q), dtype=float)
    basis[np.arange(n), inverse] = weights / norms[inverse]
    return basis


def orthogonality_error(basis: np.ndarray) -> float:
    if basis.shape[1] == 0:
        return 0.0
    return float(np.linalg.norm(basis.T @ basis - np.eye(basis.shape[1]), ord="fro"))


def invariance_error(operator: np.ndarray, basis: np.ndarray) -> float:
    if basis.shape[1] == 0:
        return 0.0
    compressed = basis.T @ operator @ basis
    return float(np.linalg.norm(operator @ basis - basis @ compressed, ord="fro"))


def subspace_capture(container: np.ndarray, target: np.ndarray) -> float:
    if target.shape[1] == 0:
        return 1.0
    return float(np.linalg.norm(container.T @ target, ord="fro") ** 2 / target.shape[1])


def intersection_and_union(bases, intersection_tolerance, union_tolerance):
    n = bases[0].shape[0]
    summed = np.zeros((n, n), dtype=float)
    for basis in bases:
        summed += basis @ basis.T
    values, vectors = np.linalg.eigh(summed)
    count = len(bases)
    intersection = vectors[:, values >= count - intersection_tolerance]
    union = vectors[:, values > union_tolerance]
    return intersection, union, values


def pi_text(label) -> str:
    return "|".join(",".join(str(x) for x in side) for side in label)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--chart-script", required=True)
    parser.add_argument("--target-ns", type=parse_int_csv, default=[7, 9])
    parser.add_argument("--low-mode-count", type=int, default=16)
    parser.add_argument("--dense-eigen-cutoff", type=int, default=160)
    parser.add_argument("--eigenvalue-tolerance", type=float, default=1e-8)
    parser.add_argument("--subspace-tolerance", type=float, default=1e-7)
    parser.add_argument("--intersection-tolerance", type=float, default=1e-7)
    parser.add_argument("--union-tolerance", type=float, default=1e-9)
    parser.add_argument("--out-dir", default="runs/ehf_qm3_01")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    base_path = Path(args.base_script).resolve()
    chart_path = Path(args.chart_script).resolve()
    base = load_module(base_path, "ehf_opw3_audit_01_base")
    chartmod = load_module(chart_path, "ehf_opw3_audit_09_chart")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 124)
    print("EHF-QM3-01: OPW3 HILBERT LIFT AND INTRINSIC SLOW-SECTOR PROJECTORS")
    print("=" * 124)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"chart engine:         {chart_path}")
    print(f"target n values:      {args.target_ns}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    checks: Dict[str, bool] = {}
    chamber_rows = []
    layer_rows = []
    common_rows = []
    summaries = {}
    started_all = time.perf_counter()

    for target_n in args.target_ns:
        source_n = target_n - 2
        started = time.perf_counter()

        source_cycles = base.generate_cycles(source_n)
        source_index = {cycle: i for i, cycle in enumerate(source_cycles)}
        source_pi = [base.pi_label(cycle) for cycle in source_cycles]
        target_cycles = base.generate_cycles(target_n)
        target_index = {cycle: i for i, cycle in enumerate(target_cycles)}
        target_pi = [base.pi_label(cycle) for cycle in target_cycles]

        target_build = base.build_preserve_graph(
            target_cycles, target_index, target_pi, "OPW3", base.GRAPH_LENGTHS["OPW3"]
        )
        target_components, _ = chartmod.connected_components(target_build.adjacency)

        charts = chartmod.chart_set(source_n)
        orientation_charts = chartmod.orientation_charts(charts)
        reference_chart = next(
            chart for chart in charts
            if chart.anchor == 0
            and chart.policy == "LEX_MIN"
            and chart.order_name == "LOW_THEN_HIGH"
        )

        growth_by_chart = {}
        for chart in charts:
            parent, descriptors, _, _ = chartmod.build_chart_growth_map(
                base, chart, source_cycles, target_index
            )
            growth_by_chart[chart.chart_id] = {
                "parent": parent,
                "descriptors": descriptors,
            }

        source_signatures = {}
        target_signatures = {}
        for chart in orientation_charts:
            source_signatures[chart.orientation_id] = chartmod.chart_active_signatures(
                base, source_cycles, source_index, source_pi, chart.anchor, chart.policy
            )
            target_signatures[chart.orientation_id] = chartmod.chart_active_signatures(
                base, target_cycles, target_index, target_pi, chart.anchor, chart.policy
            )

        ref_growth = growth_by_chart[reference_chart.chart_id]
        ref_source_sig = source_signatures[reference_chart.orientation_id]
        ref_target_sig = target_signatures[reference_chart.orientation_id]

        all_chart_complete_count = 0
        critical_components = []
        critical_common_complete = 0
        critical_dimensions = []

        print(
            f"[{source_n}->{target_n}] states={len(target_cycles)} "
            f"chambers={len(target_components)} charts={len(charts)}"
        )

        for component_id, vertices in enumerate(target_components):
            local = chartmod.local_graph(target_build.adjacency, vertices)
            lnorm, degree = normalized_laplacian(local)
            eigenvalues, eigenvectors = low_modes(
                lnorm,
                count=args.low_mode_count,
                dense_cutoff=args.dense_eigen_cutoff,
                tolerance=args.eigenvalue_tolerance,
            )

            stationary = np.sqrt(degree)
            if np.linalg.norm(stationary) == 0:
                stationary = np.ones(len(vertices))
            stationary /= np.linalg.norm(stationary)
            b0 = stationary[:, None]

            if len(vertices) == 1:
                lowest_gap = 0.0
                bslow = np.zeros((1, 0))
            else:
                lowest_gap = float(eigenvalues[1])
                indices = [
                    i for i in range(1, len(eigenvalues))
                    if abs(float(eigenvalues[i]) - lowest_gap)
                    <= args.eigenvalue_tolerance
                ]
                bslow = eigenvectors[:, indices]

            checks[f"n{target_n}_c{component_id}_L_symmetric"] = (
                np.linalg.norm(lnorm - lnorm.T, ord="fro") <= args.subspace_tolerance
            )
            checks[f"n{target_n}_c{component_id}_stationary_orthonormal"] = (
                orthogonality_error(b0) <= args.subspace_tolerance
            )
            checks[f"n{target_n}_c{component_id}_slow_orthonormal"] = (
                orthogonality_error(bslow) <= args.subspace_tolerance
            )
            checks[f"n{target_n}_c{component_id}_stationary_slow_orthogonal"] = (
                np.linalg.norm(b0.T @ bslow, ord="fro") <= args.subspace_tolerance
            )
            checks[f"n{target_n}_c{component_id}_slow_invariant"] = (
                invariance_error(lnorm, bslow) <= args.subspace_tolerance
            )

            packet_values = [ref_target_sig[state] for state in vertices]
            parent_values = [
                (ref_target_sig[state], ref_source_sig[ref_growth["parent"][state]])
                for state in vertices
            ]
            full_values = [
                (
                    ref_target_sig[state],
                    ref_source_sig[ref_growth["parent"][state]],
                    ref_growth["descriptors"][state],
                )
                for state in vertices
            ]
            packet_colors = chartmod.equitable_refinement(local, packet_values)
            parent_colors = chartmod.equitable_refinement(local, parent_values)
            full_colors = chartmod.equitable_refinement(local, full_values)
            b_packet = partition_basis(packet_colors, degree)
            b_parent = partition_basis(parent_colors, degree)
            b_full_ref = partition_basis(full_colors, degree)

            for name, basis in (
                ("PACKET", b_packet),
                ("PARENT", b_parent),
                ("FULL", b_full_ref),
            ):
                checks[f"n{target_n}_c{component_id}_{name}_orthonormal"] = (
                    orthogonality_error(basis) <= args.subspace_tolerance
                )
                checks[f"n{target_n}_c{component_id}_{name}_invariant"] = (
                    invariance_error(lnorm, basis) <= args.subspace_tolerance
                )

            packet_in_parent = subspace_capture(b_parent, b_packet)
            parent_in_full = subspace_capture(b_full_ref, b_parent)
            checks[f"n{target_n}_c{component_id}_packet_nested"] = (
                abs(packet_in_parent - 1.0) <= args.subspace_tolerance
            )
            checks[f"n{target_n}_c{component_id}_parent_nested"] = (
                abs(parent_in_full - 1.0) <= args.subspace_tolerance
            )

            captures = {
                "STATIONARY": subspace_capture(b0, bslow),
                "PACKET_NONTRIVIAL": (
                    subspace_capture(b_packet, bslow) - subspace_capture(b0, bslow)
                ),
                "ANCESTRY_INCREMENT": (
                    subspace_capture(b_parent, bslow) - subspace_capture(b_packet, bslow)
                ),
                "GROWTH_INCREMENT": (
                    subspace_capture(b_full_ref, bslow) - subspace_capture(b_parent, bslow)
                ),
                "MICROSCOPIC_COMPLEMENT": 1.0 - subspace_capture(b_full_ref, bslow),
            }
            ranks = {
                "STATIONARY": 1,
                "PACKET_NONTRIVIAL": b_packet.shape[1] - 1,
                "ANCESTRY_INCREMENT": b_parent.shape[1] - b_packet.shape[1],
                "GROWTH_INCREMENT": b_full_ref.shape[1] - b_parent.shape[1],
                "MICROSCOPIC_COMPLEMENT": len(vertices) - b_full_ref.shape[1],
            }
            checks[f"n{target_n}_c{component_id}_layer_capture_sum"] = (
                abs(sum(captures.values()) - 1.0) <= 5 * args.subspace_tolerance
            )
            for layer in captures:
                layer_rows.append({
                    "target_n": target_n,
                    "component_id": component_id,
                    "pi_label": pi_text(target_pi[vertices[0]]),
                    "component_states": len(vertices),
                    "layer": layer,
                    "layer_rank": ranks[layer],
                    "slow_eigenspace_capture": captures[layer],
                })

            chart_bases = []
            chart_captures = []
            chart_dimensions = []
            for chart in charts:
                growth = growth_by_chart[chart.chart_id]
                source_sig = source_signatures[chart.orientation_id]
                target_sig = target_signatures[chart.orientation_id]
                values = [
                    (
                        target_sig[state],
                        source_sig[growth["parent"][state]],
                        growth["descriptors"][state],
                    )
                    for state in vertices
                ]
                colors = chartmod.equitable_refinement(local, values)
                basis = partition_basis(colors, degree)
                chart_bases.append(basis)
                chart_captures.append(subspace_capture(basis, bslow))
                chart_dimensions.append(basis.shape[1])

            all_chart_complete = all(
                abs(value - 1.0) <= args.subspace_tolerance
                for value in chart_captures
            )
            if all_chart_complete:
                all_chart_complete_count += 1
                common_capture = 1.0
                common_dimension = None
                union_dimension = None
            else:
                critical_components.append(component_id)
                b_common, b_union, sum_values = intersection_and_union(
                    chart_bases,
                    args.intersection_tolerance,
                    args.union_tolerance,
                )
                common_capture = subspace_capture(b_common, bslow)
                common_dimension = b_common.shape[1]
                union_dimension = b_union.shape[1]
                critical_dimensions.append(common_dimension)
                if abs(common_capture - 1.0) <= args.subspace_tolerance:
                    critical_common_complete += 1
                checks[f"n{target_n}_c{component_id}_common_orthonormal"] = (
                    orthogonality_error(b_common) <= args.subspace_tolerance
                )
                checks[f"n{target_n}_c{component_id}_common_invariant"] = (
                    invariance_error(lnorm, b_common) <= 5 * args.subspace_tolerance
                )
                checks[f"n{target_n}_c{component_id}_union_orthonormal"] = (
                    orthogonality_error(b_union) <= args.subspace_tolerance
                )
                checks[f"n{target_n}_c{component_id}_union_invariant"] = (
                    invariance_error(lnorm, b_union) <= 5 * args.subspace_tolerance
                )

            chamber_rows.append({
                "target_n": target_n,
                "component_id": component_id,
                "pi_label": pi_text(target_pi[vertices[0]]),
                "hilbert_dimension": len(vertices),
                "lowest_nontrivial_gap": lowest_gap,
                "lowest_eigenspace_dimension": bslow.shape[1],
                "packet_dimension": b_packet.shape[1],
                "parent_dimension": b_parent.shape[1],
                "reference_completion_dimension": b_full_ref.shape[1],
                "packet_slow_capture": subspace_capture(b_packet, bslow),
                "parent_slow_capture": subspace_capture(b_parent, bslow),
                "reference_completion_slow_capture": subspace_capture(b_full_ref, bslow),
                "all_chart_completion_slow_complete": all_chart_complete,
                "chart_slow_capture_min": min(chart_captures),
                "chart_slow_capture_mean": statistics.fmean(chart_captures),
            })
            common_rows.append({
                "target_n": target_n,
                "component_id": component_id,
                "pi_label": pi_text(target_pi[vertices[0]]),
                "component_states": len(vertices),
                "lowest_eigenspace_dimension": bslow.shape[1],
                "charts": len(charts),
                "chart_completion_dimension_min": min(chart_dimensions),
                "chart_completion_dimension_median": statistics.median(chart_dimensions),
                "chart_completion_dimension_max": max(chart_dimensions),
                "all_chart_slow_complete": all_chart_complete,
                "common_intersection_explicitly_computed": not all_chart_complete,
                "common_intersection_dimension": common_dimension,
                "common_intersection_slow_capture": common_capture,
                "union_dimension": union_dimension,
            })

        summaries[f"n{target_n}"] = {
            "source_n": source_n,
            "target_states": len(target_cycles),
            "chambers": len(target_components),
            "charts": len(charts),
            "all_chart_slow_complete_chambers": all_chart_complete_count,
            "chart_critical_components": critical_components,
            "chart_critical_count": len(critical_components),
            "critical_common_slow_complete_count": critical_common_complete,
            "critical_common_dimension_min": min(critical_dimensions) if critical_dimensions else None,
            "critical_common_dimension_max": max(critical_dimensions) if critical_dimensions else None,
            "elapsed_seconds": time.perf_counter() - started,
        }

        print(
            f"  all-chart complete lowest eigenspace: "
            f"{all_chart_complete_count}/{len(target_components)}"
        )
        print(f"  chart-critical chambers={critical_components}")
        if critical_dimensions:
            print(
                f"  critical common intersection contains full slow space: "
                f"{critical_common_complete}/{len(critical_components)}"
            )
            print(
                f"  critical common dimensions min/max="
                f"{min(critical_dimensions)}/{max(critical_dimensions)}"
            )
        print(f"  elapsed={summaries[f'n{target_n}']['elapsed_seconds']:.2f}s")
        print()

    write_csv(out_dir / "hilbert_chamber_summary.csv", chamber_rows)
    write_csv(out_dir / "reference_projector_layers.csv", layer_rows)
    write_csv(out_dir / "chart_common_subspace_summary.csv", common_rows)

    checks = {key: bool(value) for key, value in checks.items()}
    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-QM3-01",
        "title": "OPW3 Hilbert Lift and Intrinsic Slow-Sector Projectors",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "chart_script": str(chart_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "interpretation_guardrail": (
            "The normalized Laplacian is a canonical structural self-adjoint operator here, "
            "not yet a selected physical Hamiltonian. Hilbert spaces and projectors are exact "
            "finite linear algebra, not a derivation of physical quantum mechanics."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_QM3_01_HILBERT_LIFT_INTRINSIC_PROJECTORS_PASS"
            if strict_pass else
            "EHF_QM3_01_HILBERT_LIFT_INTRINSIC_PROJECTORS_FAIL"
        ),
    }
    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print("=" * 124)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {summary['elapsed_seconds']:.2f}s")
    print("=" * 124)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
