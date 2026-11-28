#!/usr/bin/env python3
"""
EHF-QM3-02
==========
Degenerate Slow-Multiplet Chart-Orbit Resolution

QM3-01 found one chart-critical OPW3 chamber at n=7 and one at n=9.  In those
chambers, not every chart-completed quotient contains the complete degenerate
lowest eigenspace.

This probe studies the chart-selected subspaces inside that eigenspace.

For each chart chi, let Q_chi be the completed quotient projector and P_slow the
complete lowest nontrivial spectral projector.  In an orthonormal basis B_slow
of the slow eigenspace, define

    R_chi = B_slow^T Q_chi B_slow.

When Q_chi commutes with the normalized Laplacian, R_chi is an orthogonal
projector onto the slow directions visible in chart chi.

The chart family is treated as a finite fusion frame.  The probe computes:

  * chart-visible slow rank;
  * number of distinct chart-selected slow subspaces;
  * union and intersection ranks inside the slow multiplet;
  * pairwise principal-angle/overlap classes;
  * fusion-frame operator F = sum_chi R_chi;
  * frame bounds, condition number, and tightness;
  * whether the chart average is proportional to identity on the multiplet.

This is finite spectral linear algebra.  It does not assign spin, internal
quantum number, particle species, or physical gauge meaning.
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
from typing import Dict, Hashable, List, Sequence, Set, Tuple

import numpy as np
from scipy import sparse

SCRIPT_VERSION = "ehf_qm3_02_v2_2026-07-25"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_int_csv(text: str) -> List[int]:
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def parse_component_map(text: str) -> Dict[int, List[int]]:
    result: Dict[int, List[int]] = {}
    if not text.strip():
        return result
    for block in text.split(";"):
        block = block.strip()
        if not block:
            continue
        n_text, components_text = block.split(":", 1)
        result[int(n_text)] = [
            int(value.strip())
            for value in components_text.split(",")
            if value.strip()
        ]
    return result


def critical_components_from_summary(path: Path) -> Dict[int, List[int]]:
    data = json.loads(path.read_text())
    result: Dict[int, List[int]] = {}
    for key, value in data.get("summaries", {}).items():
        if not key.startswith("n"):
            continue
        n = int(key[1:])
        components = value.get("chart_critical_components")
        if components is None:
            components = value.get("critical_components", [])
        result[n] = [int(component) for component in components]
    return result


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module




def json_default(value):
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")

def write_csv(path: Path, rows: Sequence[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def normalized_laplacian(
    adjacency: Sequence[Sequence[int]],
) -> Tuple[np.ndarray, np.ndarray]:
    n = len(adjacency)
    degrees = np.array([len(row) for row in adjacency], dtype=float)
    if n == 1 and degrees[0] == 0:
        return np.zeros((1, 1), dtype=float), degrees

    rows: List[int] = []
    cols: List[int] = []
    for u, neighbours in enumerate(adjacency):
        for v in neighbours:
            rows.append(u)
            cols.append(v)

    adjacency_matrix = sparse.csr_matrix(
        (np.ones(len(rows), dtype=float), (rows, cols)),
        shape=(n, n),
        dtype=float,
    ).toarray()

    inverse_root_degree = np.divide(
        1.0,
        np.sqrt(degrees),
        out=np.zeros_like(degrees),
        where=degrees > 0,
    )
    symmetric_walk = (
        inverse_root_degree[:, None]
        * adjacency_matrix
        * inverse_root_degree[None, :]
    )
    return np.eye(n) - symmetric_walk, degrees


def partition_basis(
    colors: Sequence[int],
    degrees: np.ndarray,
) -> np.ndarray:
    columns: List[np.ndarray] = []
    for cell in sorted(set(colors)):
        members = [i for i, color in enumerate(colors) if color == cell]
        vector = np.zeros(len(colors), dtype=float)
        if np.all(degrees[members] == 0):
            vector[members] = 1.0
        else:
            vector[members] = np.sqrt(degrees[members])
        vector /= np.linalg.norm(vector)
        columns.append(vector)
    return np.column_stack(columns)


def projector_basis_from_matrix(
    matrix: np.ndarray,
    eigenvalue_threshold: float,
) -> Tuple[np.ndarray, np.ndarray]:
    eigenvalues, eigenvectors = np.linalg.eigh(
        0.5 * (matrix + matrix.T)
    )
    keep = eigenvalues > eigenvalue_threshold
    return eigenvectors[:, keep], eigenvalues


def subspace_rank(
    columns: np.ndarray,
    tolerance: float,
) -> int:
    if columns.size == 0:
        return 0
    singular_values = np.linalg.svd(
        columns,
        compute_uv=False,
    )
    return int(np.sum(singular_values > tolerance))


def restricted_projector_key(
    matrix: np.ndarray,
    decimals: int,
) -> Tuple[float, ...]:
    return tuple(np.round(matrix, decimals=decimals).ravel())


def principal_angle_cosines(
    basis_a: np.ndarray,
    basis_b: np.ndarray,
) -> np.ndarray:
    if basis_a.shape[1] == 0 or basis_b.shape[1] == 0:
        return np.array([], dtype=float)
    singular_values = np.linalg.svd(
        basis_a.T @ basis_b,
        compute_uv=False,
    )
    return np.clip(singular_values, 0.0, 1.0)


def pi_text(label) -> str:
    return "|".join(",".join(str(x) for x in side) for side in label)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve chart-selected directions inside degenerate OPW3 slow eigenspaces."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--chart-script", required=True)
    parser.add_argument("--target-ns", type=parse_int_csv, default=[7, 9])
    parser.add_argument(
        "--qm3-01-summary",
        default=None,
        help="QM3-01 run_summary.json used to select chart-critical chambers",
    )
    parser.add_argument(
        "--critical-components",
        type=parse_component_map,
        default=None,
        help="explicit map such as '7:18;9:68'; overrides --qm3-01-summary",
    )
    parser.add_argument("--eigenvalue-tolerance", type=float, default=1e-8)
    parser.add_argument("--projector-tolerance", type=float, default=1e-7)
    parser.add_argument("--rank-tolerance", type=float, default=1e-8)
    parser.add_argument("--key-decimals", type=int, default=9)
    parser.add_argument("--out-dir", default="runs/ehf_qm3_02")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    base_path = Path(args.base_script).resolve()
    chart_path = Path(args.chart_script).resolve()
    if args.critical_components is not None:
        selected_critical = args.critical_components
    elif args.qm3_01_summary is not None:
        selected_critical = critical_components_from_summary(
            Path(args.qm3_01_summary).resolve()
        )
    else:
        raise ValueError(
            "provide --qm3-01-summary or --critical-components so the probe "
            "targets only the chart-critical chambers found by QM3-01"
        )

    base = load_module(base_path, "ehf_opw3_audit_01_base")
    chartmod = load_module(chart_path, "ehf_opw3_audit_09_chart")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 124)
    print("EHF-QM3-02: DEGENERATE SLOW-MULTIPLET CHART-ORBIT RESOLUTION")
    print("=" * 124)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"chart engine:         {chart_path}")
    print(f"target n values:      {args.target_ns}")
    print(f"critical components: {selected_critical}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    checks: Dict[str, bool] = {}
    critical_rows: List[dict] = []
    chart_rows: List[dict] = []
    orbit_rows: List[dict] = []
    pair_rows: List[dict] = []
    summaries: Dict[str, dict] = {}
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

        source_build = base.build_preserve_graph(
            source_cycles,
            source_index,
            source_pi,
            "OPW3",
            base.GRAPH_LENGTHS["OPW3"],
        )
        target_build = base.build_preserve_graph(
            target_cycles,
            target_index,
            target_pi,
            "OPW3",
            base.GRAPH_LENGTHS["OPW3"],
        )
        components, _ = chartmod.connected_components(
            target_build.adjacency
        )

        charts = chartmod.chart_set(source_n)
        orientation_charts = chartmod.orientation_charts(charts)

        growth_by_chart = {}
        source_signature_by_orientation = {}
        target_signature_by_orientation = {}

        for chart in charts:
            parent, descriptors, _, _ = chartmod.build_chart_growth_map(
                base,
                chart,
                source_cycles,
                target_index,
            )
            growth_by_chart[chart.chart_id] = {
                "parent": parent,
                "descriptors": descriptors,
            }

        for chart in orientation_charts:
            source_signature_by_orientation[chart.orientation_id] = (
                chartmod.chart_active_signatures(
                    base,
                    source_cycles,
                    source_index,
                    source_pi,
                    chart.anchor,
                    chart.policy,
                )
            )
            target_signature_by_orientation[chart.orientation_id] = (
                chartmod.chart_active_signatures(
                    base,
                    target_cycles,
                    target_index,
                    target_pi,
                    chart.anchor,
                    chart.policy,
                )
            )

        critical_components = selected_critical.get(target_n, [])
        missing = [
            component_id for component_id in critical_components
            if component_id < 0 or component_id >= len(components)
        ]
        if missing:
            raise ValueError(
                f"critical component IDs outside n={target_n} census: {missing}"
            )

        for component_id in critical_components:
            vertices = components[component_id]
            local = chartmod.local_graph(
                target_build.adjacency,
                vertices,
            )
            lnorm, degrees = normalized_laplacian(local)
            eigenvalues, eigenvectors = np.linalg.eigh(lnorm)
            order = np.argsort(eigenvalues)
            eigenvalues = eigenvalues[order]
            eigenvectors = eigenvectors[:, order]
            eigenvalues[
                np.abs(eigenvalues) < args.eigenvalue_tolerance
            ] = 0.0

            if len(vertices) <= 1:
                continue

            lowest_gap = float(eigenvalues[1])
            slow_indices = [
                i for i in range(1, len(eigenvalues))
                if abs(float(eigenvalues[i]) - lowest_gap)
                <= args.eigenvalue_tolerance
            ]
            slow_basis = eigenvectors[:, slow_indices]
            slow_dimension = slow_basis.shape[1]

            restricted_projectors: List[np.ndarray] = []
            restricted_bases: List[np.ndarray] = []
            chart_capture_ranks: List[int] = []
            chart_capture_traces: List[float] = []
            chart_complete: List[bool] = []

            for chart in charts:
                growth = growth_by_chart[chart.chart_id]
                source_signature = source_signature_by_orientation[
                    chart.orientation_id
                ]
                target_signature = target_signature_by_orientation[
                    chart.orientation_id
                ]

                values = [
                    (
                        target_signature[state],
                        source_signature[growth["parent"][state]],
                        growth["descriptors"][state],
                    )
                    for state in vertices
                ]
                colors = chartmod.equitable_refinement(local, values)
                quotient_basis = partition_basis(colors, degrees)

                overlap = quotient_basis.T @ slow_basis
                restricted = overlap.T @ overlap
                restricted = 0.5 * (restricted + restricted.T)

                visible_basis, restricted_eigenvalues = (
                    projector_basis_from_matrix(
                        restricted,
                        eigenvalue_threshold=0.5,
                    )
                )
                capture_rank = visible_basis.shape[1]
                capture_trace = float(np.trace(restricted))
                complete = (
                    np.linalg.norm(
                        restricted - np.eye(slow_dimension),
                        ord="fro",
                    )
                    <= args.projector_tolerance
                )

                checks[
                    f"n{target_n}_c{component_id}_{chart.chart_id}_restricted_projector"
                ] = (
                    np.linalg.norm(
                        restricted @ restricted - restricted,
                        ord="fro",
                    )
                    <= 10 * args.projector_tolerance
                )

                restricted_projectors.append(restricted)
                restricted_bases.append(visible_basis)
                chart_capture_ranks.append(capture_rank)
                chart_capture_traces.append(capture_trace)
                chart_complete.append(complete)

                chart_rows.append({
                    "target_n": target_n,
                    "component_id": component_id,
                    "pi_label": pi_text(target_pi[vertices[0]]),
                    "component_states": len(vertices),
                    "lowest_gap": lowest_gap,
                    "slow_dimension": slow_dimension,
                    "chart_id": chart.chart_id,
                    "orientation_id": chart.orientation_id,
                    "anchor": chart.anchor,
                    "orientation_policy": chart.policy,
                    "insertion_order": chart.order_name,
                    "visible_slow_rank": capture_rank,
                    "slow_capture_trace": capture_trace,
                    "complete_slow_capture": complete,
                    "restricted_eigenvalues": json.dumps(
                        [
                            float(value)
                            for value in restricted_eigenvalues
                        ]
                    ),
                })

            checks[
                f"n{target_n}_c{component_id}_is_chart_critical"
            ] = not all(chart_complete)

            distinct: Dict[Tuple[float, ...], List[int]] = defaultdict(list)
            for chart_index, restricted in enumerate(restricted_projectors):
                distinct[
                    restricted_projector_key(
                        restricted,
                        args.key_decimals,
                    )
                ].append(chart_index)

            all_visible_columns = [
                basis
                for basis in restricted_bases
                if basis.shape[1] > 0
            ]
            if all_visible_columns:
                joined = np.column_stack(all_visible_columns)
                union_rank = subspace_rank(
                    joined,
                    args.rank_tolerance,
                )
            else:
                union_rank = 0

            projector_sum = np.sum(restricted_projectors, axis=0)
            sum_eigenvalues = np.linalg.eigvalsh(
                0.5 * (projector_sum + projector_sum.T)
            )
            intersection_rank = int(
                np.sum(
                    sum_eigenvalues
                    >= len(charts) - args.projector_tolerance
                )
            )

            frame_eigenvalues = np.sort(sum_eigenvalues)
            positive_frame = frame_eigenvalues[
                frame_eigenvalues > args.rank_tolerance
            ]
            frame_lower = (
                float(positive_frame.min())
                if len(positive_frame) else 0.0
            )
            frame_upper = (
                float(positive_frame.max())
                if len(positive_frame) else 0.0
            )
            frame_condition = (
                frame_upper / frame_lower
                if frame_lower > 0 else math.inf
            )
            frame_mean = float(np.trace(projector_sum) / slow_dimension)
            tightness_error = float(
                np.linalg.norm(
                    projector_sum
                    - frame_mean * np.eye(slow_dimension),
                    ord="fro",
                )
            )
            relative_tightness_error = (
                tightness_error
                / max(
                    np.linalg.norm(
                        frame_mean * np.eye(slow_dimension),
                        ord="fro",
                    ),
                    args.rank_tolerance,
                )
            )
            tight_frame = (
                relative_tightness_error
                <= args.projector_tolerance
            )

            checks[
                f"n{target_n}_c{component_id}_chart_union_spans_slow"
            ] = union_rank == slow_dimension
            checks[
                f"n{target_n}_c{component_id}_fusion_frame_positive"
            ] = frame_lower > args.rank_tolerance

            rank_histogram = Counter(chart_capture_ranks)
            complete_count = sum(chart_complete)

            critical_rows.append({
                "target_n": target_n,
                "source_n": source_n,
                "component_id": component_id,
                "pi_label": pi_text(target_pi[vertices[0]]),
                "component_states": len(vertices),
                "lowest_gap": lowest_gap,
                "slow_dimension": slow_dimension,
                "charts": len(charts),
                "complete_chart_count": complete_count,
                "incomplete_chart_count": len(charts) - complete_count,
                "visible_rank_histogram": json.dumps(
                    dict(sorted(rank_histogram.items()))
                ),
                "distinct_chart_selected_subspaces": len(distinct),
                "chart_union_rank": union_rank,
                "chart_intersection_rank": intersection_rank,
                "fusion_frame_lower_bound": frame_lower,
                "fusion_frame_upper_bound": frame_upper,
                "fusion_frame_condition_number": frame_condition,
                "fusion_frame_mean_eigenvalue": frame_mean,
                "fusion_frame_eigenvalues": json.dumps(
                    [float(value) for value in frame_eigenvalues]
                ),
                "tightness_error_frobenius": tightness_error,
                "relative_tightness_error": relative_tightness_error,
                "tight_fusion_frame": tight_frame,
                "mean_chart_capture_fraction": statistics.fmean(
                    trace / slow_dimension
                    for trace in chart_capture_traces
                ),
            })

            distinct_items = list(distinct.items())
            for orbit_id, (key, chart_indices) in enumerate(distinct_items):
                representative_index = chart_indices[0]
                representative_chart = charts[representative_index]
                representative_projector = restricted_projectors[
                    representative_index
                ]
                representative_basis = restricted_bases[
                    representative_index
                ]
                orbit_rows.append({
                    "target_n": target_n,
                    "component_id": component_id,
                    "orbit_id": orbit_id,
                    "charts_in_orbit": len(chart_indices),
                    "chart_ids": json.dumps(
                        [charts[index].chart_id for index in chart_indices]
                    ),
                    "representative_chart": (
                        representative_chart.chart_id
                    ),
                    "visible_rank": representative_basis.shape[1],
                    "restricted_projector": json.dumps(
                        representative_projector.tolist()
                    ),
                })

            for left_id in range(len(distinct_items)):
                for right_id in range(left_id, len(distinct_items)):
                    left_indices = distinct_items[left_id][1]
                    right_indices = distinct_items[right_id][1]
                    left_basis = restricted_bases[left_indices[0]]
                    right_basis = restricted_bases[right_indices[0]]
                    cosines = principal_angle_cosines(
                        left_basis,
                        right_basis,
                    )
                    overlap_trace = float(
                        np.trace(
                            restricted_projectors[left_indices[0]]
                            @ restricted_projectors[right_indices[0]]
                        )
                    )
                    pair_rows.append({
                        "target_n": target_n,
                        "component_id": component_id,
                        "left_orbit_id": left_id,
                        "right_orbit_id": right_id,
                        "left_rank": left_basis.shape[1],
                        "right_rank": right_basis.shape[1],
                        "projector_overlap_trace": overlap_trace,
                        "principal_angle_cosines": json.dumps(
                            [float(value) for value in cosines]
                        ),
                        "principal_angles_degrees": json.dumps(
                            [
                                float(
                                    np.degrees(
                                        np.arccos(
                                            np.clip(value, 0.0, 1.0)
                                        )
                                    )
                                )
                                for value in cosines
                            ]
                        ),
                    })

        critical_here = [
            row for row in critical_rows
            if row["target_n"] == target_n
        ]
        summaries[f"n{target_n}"] = {
            "source_n": source_n,
            "target_states": len(target_cycles),
            "chambers": len(components),
            "charts": len(charts),
            "critical_components": critical_components,
            "critical_count": len(critical_components),
            "all_critical_chart_unions_span_full_slow": all(
                row["chart_union_rank"] == row["slow_dimension"]
                for row in critical_here
            ),
            "tight_fusion_frame_components": [
                row["component_id"]
                for row in critical_here
                if row["tight_fusion_frame"]
            ],
            "elapsed_seconds": time.perf_counter() - started,
        }

        print(
            f"[{source_n}->{target_n}] critical chambers="
            f"{critical_components}"
        )
        for row in critical_here:
            print(
                f"  component={row['component_id']} "
                f"size={row['component_states']} "
                f"slow-dim={row['slow_dimension']} "
                f"complete-charts={row['complete_chart_count']}/"
                f"{row['charts']} "
                f"rank-hist={row['visible_rank_histogram']} "
                f"distinct-subspaces="
                f"{row['distinct_chart_selected_subspaces']} "
                f"union/intersection="
                f"{row['chart_union_rank']}/"
                f"{row['chart_intersection_rank']} "
                f"frame-eigs={row['fusion_frame_eigenvalues']} "
                f"tight={row['tight_fusion_frame']}"
            )
        print(f"  elapsed={summaries[f'n{target_n}']['elapsed_seconds']:.2f}s")
        print()

    write_csv(out_dir / "critical_multiplet_summary.csv", critical_rows)
    write_csv(out_dir / "chart_slow_capture_ledger.csv", chart_rows)
    write_csv(out_dir / "chart_subspace_orbits.csv", orbit_rows)
    write_csv(out_dir / "chart_subspace_pair_geometry.csv", pair_rows)

    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-QM3-02",
        "title": "Degenerate Slow-Multiplet Chart-Orbit Resolution",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "chart_script": str(chart_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "interpretation_guardrail": (
            "The chart-selected subspaces form finite spectral fusion frames. "
            "No physical spin, gauge representation, internal charge, or "
            "particle multiplet is inferred from degeneracy or chart orbits."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_QM3_02_DEGENERATE_SLOW_MULTIPLET_CHART_ORBIT_PASS"
            if strict_pass else
            "EHF_QM3_02_DEGENERATE_SLOW_MULTIPLET_CHART_ORBIT_FAIL"
        ),
    }
    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True, default=json_default)

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
