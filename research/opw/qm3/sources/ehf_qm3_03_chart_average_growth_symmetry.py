#!/usr/bin/env python3
"""
EHF-QM3-03
==========
Chart-Average Multiplet Split and Growth-Symmetry Audit

QM3-02 found that each chart-critical slow multiplet has exactly two
chart-selected subspaces: a common subspace visible in every chart and the
complete slow eigenspace visible only for some anchors.

This probe constructs the chart fusion operator

    F = sum_chi R_chi

inside the complete slow eigenspace and extracts

    P_common  = spectral projector of F at eigenvalue |charts|,
    P_sensitive = I - P_common.

It then tests whether this split is preserved by three empirically exact
transposition stabilizers of the critical chamber:

  OLD_LABEL_STABILIZER:
      chamber-preserving transpositions of two old labels.

  GROWTH_SET_STABILIZER:
      chamber-preserving transpositions that preserve the old/new label sets
      (old-old or newest-newest).

  CHAMBER_TRANSPOSITION_STABILIZER:
      every single label transposition that preserves the critical chamber,
      including old/new mixing when it exists.

The stabilizers are discovered from the actual OPW3 chamber rather than
inferred from the Pi-label sets, because the anchored Pi convention is not
equivariant under arbitrary label permutations.

The probe also determines whether orientation policy and insertion order affect
chart capture after the anchor is fixed.

This is structural finite-dimensional symmetry analysis.  It does not identify
the two sectors with spin, charge, chirality, gauge representation, particle
species, or any physical internal quantum number.
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
from typing import Dict, Hashable, Iterable, List, Mapping, Sequence, Set, Tuple

import numpy as np
from scipy import sparse

SCRIPT_VERSION = "ehf_qm3_03_2026-07-25"


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


def normalized_laplacian(
    adjacency: Sequence[Sequence[int]],
) -> Tuple[np.ndarray, np.ndarray]:
    n = len(adjacency)
    degrees = np.array([len(row) for row in adjacency], dtype=float)

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


def projector_basis(
    matrix: np.ndarray,
    threshold: float,
) -> Tuple[np.ndarray, np.ndarray]:
    eigenvalues, eigenvectors = np.linalg.eigh(
        0.5 * (matrix + matrix.T)
    )
    keep = eigenvalues > threshold
    return eigenvectors[:, keep], eigenvalues


def adjacent_swap_generators(labels: Sequence[int]) -> List[Tuple[int, int]]:
    ordered = sorted(labels)
    return [
        (ordered[i], ordered[i + 1])
        for i in range(len(ordered) - 1)
    ]


def unique_generators(
    generators: Sequence[Tuple[int, int]],
) -> List[Tuple[int, int]]:
    seen = set()
    result = []
    for a, b in generators:
        key = tuple(sorted((a, b)))
        if a == b or key in seen:
            continue
        seen.add(key)
        result.append(key)
    return result


def label_swap_permutation(
    label_count: int,
    swap: Tuple[int, int],
) -> Tuple[int, ...]:
    a, b = swap
    permutation = list(range(label_count))
    permutation[a], permutation[b] = permutation[b], permutation[a]
    return tuple(permutation)


def relabel_cycle(
    base,
    cycle: Sequence[int],
    permutation: Sequence[int],
):
    return base.canonical_cycle(
        tuple(permutation[label] for label in cycle)
    )


def local_permutation_matrix(
    base,
    cycles: Sequence[Tuple[int, ...]],
    global_index: Mapping[Tuple[int, ...], int],
    vertices: Sequence[int],
    permutation: Sequence[int],
) -> np.ndarray:
    local_index = {state: i for i, state in enumerate(vertices)}
    matrix = np.zeros((len(vertices), len(vertices)), dtype=float)

    for source_local, source_global in enumerate(vertices):
        target_cycle = relabel_cycle(
            base,
            cycles[source_global],
            permutation,
        )
        target_global = global_index[target_cycle]
        if target_global not in local_index:
            raise RuntimeError(
                "relabeling generator does not preserve critical chamber"
            )
        target_local = local_index[target_global]
        matrix[target_local, source_local] = 1.0

    if not np.allclose(matrix.T @ matrix, np.eye(len(vertices))):
        raise RuntimeError("state relabeling is not a permutation matrix")
    return matrix



def permutation_preserves_chamber(
    base,
    cycles: Sequence[Tuple[int, ...]],
    global_index: Mapping[Tuple[int, ...], int],
    vertices: Sequence[int],
    permutation: Sequence[int],
) -> bool:
    vertex_set = set(vertices)
    for state in vertices:
        target_cycle = relabel_cycle(
            base,
            cycles[state],
            permutation,
        )
        if global_index[target_cycle] not in vertex_set:
            return False
    return True


def commutant_dimension(
    generators: Sequence[np.ndarray],
    tolerance: float,
) -> int:
    if not generators:
        return 0

    dimension = generators[0].shape[0]
    equations = []
    identity = np.eye(dimension)

    for generator in generators:
        equations.append(
            np.kron(generator.T, identity)
            - np.kron(identity, generator)
        )

    stacked = np.vstack(equations)
    singular_values = np.linalg.svd(
        stacked,
        compute_uv=False,
    )
    rank = int(np.sum(singular_values > tolerance))
    return dimension * dimension - rank


def fixed_subspace_dimension(
    generators: Sequence[np.ndarray],
    tolerance: float,
) -> int:
    if not generators:
        return 0
    dimension = generators[0].shape[0]
    stacked = np.vstack(
        [generator - np.eye(dimension) for generator in generators]
    )
    singular_values = np.linalg.svd(
        stacked,
        compute_uv=False,
    )
    rank = int(np.sum(singular_values > tolerance))
    return dimension - rank


def pi_text(label) -> str:
    return "|".join(",".join(str(x) for x in side) for side in label)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit the chart-average common/sensitive slow-multiplet split under growth symmetries."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--chart-script", required=True)
    parser.add_argument("--qm3-02-summary", required=True)
    parser.add_argument("--target-ns", type=parse_int_csv, default=[7, 9])
    parser.add_argument("--eigenvalue-tolerance", type=float, default=1e-8)
    parser.add_argument("--projector-tolerance", type=float, default=1e-7)
    parser.add_argument("--rank-tolerance", type=float, default=1e-8)
    parser.add_argument("--out-dir", default="runs/ehf_qm3_03")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    base_path = Path(args.base_script).resolve()
    chart_path = Path(args.chart_script).resolve()
    summary_path = Path(args.qm3_02_summary).resolve()

    base = load_module(base_path, "ehf_opw3_audit_01_base")
    chartmod = load_module(chart_path, "ehf_opw3_audit_09_chart")

    with summary_path.open() as handle:
        qm3_02_summary = json.load(handle)

    critical_by_n = {
        int(key[1:]): value["critical_components"]
        for key, value in qm3_02_summary["summaries"].items()
    }

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 126)
    print("EHF-QM3-03: CHART-AVERAGE MULTIPLET SPLIT AND GROWTH-SYMMETRY AUDIT")
    print("=" * 126)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"chart engine:         {chart_path}")
    print(f"QM3-02 summary:       {summary_path}")
    print(f"target n values:      {args.target_ns}")
    print(f"critical components:  {critical_by_n}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    checks: Dict[str, bool] = {}
    critical_rows: List[dict] = []
    anchor_rows: List[dict] = []
    generator_rows: List[dict] = []
    group_rows: List[dict] = []
    summaries: Dict[str, dict] = {}
    started_all = time.perf_counter()

    for target_n in args.target_ns:
        source_n = target_n - 2
        started = time.perf_counter()

        source_cycles = base.generate_cycles(source_n)
        source_index = {
            cycle: i for i, cycle in enumerate(source_cycles)
        }
        source_pi = [base.pi_label(cycle) for cycle in source_cycles]

        target_cycles = base.generate_cycles(target_n)
        target_index = {
            cycle: i for i, cycle in enumerate(target_cycles)
        }
        target_pi = [base.pi_label(cycle) for cycle in target_cycles]

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

        print(
            f"[{source_n}->{target_n}] critical chambers="
            f"{critical_by_n.get(target_n, [])}"
        )

        n_group_results = []

        for component_id in critical_by_n.get(target_n, []):
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

            lowest_gap = float(eigenvalues[1])
            slow_indices = [
                i for i in range(1, len(eigenvalues))
                if abs(float(eigenvalues[i]) - lowest_gap)
                <= args.eigenvalue_tolerance
            ]
            slow_basis = eigenvectors[:, slow_indices]
            slow_dimension = slow_basis.shape[1]

            restricted_projectors = []
            chart_rank_by_anchor: Dict[int, List[int]] = defaultdict(list)
            chart_complete_by_anchor: Dict[int, List[bool]] = defaultdict(list)

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
                restricted_projectors.append(restricted)

                rank = int(
                    np.sum(
                        np.linalg.eigvalsh(restricted)
                        > 0.5
                    )
                )
                complete = bool(
                    np.linalg.norm(
                        restricted - np.eye(slow_dimension),
                        ord="fro",
                    )
                    <= args.projector_tolerance
                )
                chart_rank_by_anchor[chart.anchor].append(rank)
                chart_complete_by_anchor[chart.anchor].append(complete)

            fusion = np.sum(restricted_projectors, axis=0)
            fusion_eigenvalues, fusion_eigenvectors = np.linalg.eigh(
                0.5 * (fusion + fusion.T)
            )
            common_keep = (
                fusion_eigenvalues
                >= len(charts) - args.projector_tolerance
            )
            common_basis = fusion_eigenvectors[:, common_keep]
            common_projector = common_basis @ common_basis.T
            sensitive_projector = (
                np.eye(slow_dimension) - common_projector
            )
            common_dimension = common_basis.shape[1]
            sensitive_dimension = (
                slow_dimension - common_dimension
            )

            checks[
                f"n{target_n}_c{component_id}_fusion_common_nontrivial"
            ] = (
                0 < common_dimension < slow_dimension
            )
            checks[
                f"n{target_n}_c{component_id}_split_projectors"
            ] = (
                np.linalg.norm(
                    common_projector @ common_projector
                    - common_projector,
                    ord="fro",
                )
                <= args.projector_tolerance
                and np.linalg.norm(
                    sensitive_projector @ sensitive_projector
                    - sensitive_projector,
                    ord="fro",
                )
                <= args.projector_tolerance
                and np.linalg.norm(
                    common_projector @ sensitive_projector,
                    ord="fro",
                )
                <= args.projector_tolerance
            )

            incomplete_anchors = []
            complete_anchors = []
            anchor_consistent = True

            for anchor in sorted(chart_rank_by_anchor):
                ranks = chart_rank_by_anchor[anchor]
                completes = chart_complete_by_anchor[anchor]
                rank_set = sorted(set(ranks))
                complete_set = sorted({bool(value) for value in completes})
                consistent = bool(
                    len(rank_set) == 1
                    and len(complete_set) == 1
                )
                anchor_consistent &= consistent

                if all(completes):
                    complete_anchors.append(anchor)
                elif not any(completes):
                    incomplete_anchors.append(anchor)

                anchor_rows.append({
                    "target_n": target_n,
                    "component_id": component_id,
                    "anchor": anchor,
                    "charts_for_anchor": len(ranks),
                    "visible_rank_values": json.dumps(rank_set),
                    "complete_values": json.dumps(complete_set),
                    "orientation_order_independent": consistent,
                })

            checks[
                f"n{target_n}_c{component_id}_anchor_determines_capture"
            ] = anchor_consistent

            pi_sides = target_pi[vertices[0]]
            old_labels = set(range(source_n))
            new_labels = {source_n, source_n + 1}

            preserving_swaps: List[Tuple[int, int]] = []
            for a in range(target_n):
                for b in range(a + 1, target_n):
                    permutation = label_swap_permutation(
                        target_n,
                        (a, b),
                    )
                    if permutation_preserves_chamber(
                        base,
                        target_cycles,
                        target_index,
                        vertices,
                        permutation,
                    ):
                        preserving_swaps.append((a, b))

            old_label_generators = [
                swap for swap in preserving_swaps
                if swap[0] in old_labels
                and swap[1] in old_labels
            ]
            growth_set_generators = [
                swap for swap in preserving_swaps
                if (
                    swap[0] in old_labels
                    and swap[1] in old_labels
                )
                or (
                    swap[0] in new_labels
                    and swap[1] in new_labels
                )
            ]

            groups = {
                "OLD_LABEL_STABILIZER": old_label_generators,
                "GROWTH_SET_STABILIZER": growth_set_generators,
                "CHAMBER_TRANSPOSITION_STABILIZER": preserving_swaps,
            }

            for group_name, swaps in groups.items():
                slow_actions = []
                split_commutators = []
                cross_mixings = []
                graph_errors = []
                slow_invariance_errors = []

                for swap in swaps:
                    label_permutation = label_swap_permutation(
                        target_n,
                        swap,
                    )
                    state_permutation = local_permutation_matrix(
                        base,
                        target_cycles,
                        target_index,
                        vertices,
                        label_permutation,
                    )
                    graph_error = float(
                        np.linalg.norm(
                            state_permutation.T
                            @ lnorm
                            @ state_permutation
                            - lnorm,
                            ord="fro",
                        )
                    )
                    slow_action = (
                        slow_basis.T
                        @ state_permutation
                        @ slow_basis
                    )
                    slow_invariance_error = float(
                        np.linalg.norm(
                            slow_action.T @ slow_action
                            - np.eye(slow_dimension),
                            ord="fro",
                        )
                    )
                    split_commutator = float(
                        np.linalg.norm(
                            slow_action @ common_projector
                            - common_projector @ slow_action,
                            ord="fro",
                        )
                    )
                    cross_mixing = float(
                        np.linalg.norm(
                            common_projector
                            @ slow_action
                            @ sensitive_projector,
                            ord="fro",
                        )
                    )

                    checks[
                        f"n{target_n}_c{component_id}_{group_name}_{swap}_automorphism"
                    ] = (
                        graph_error <= args.projector_tolerance
                        and slow_invariance_error
                        <= 10 * args.projector_tolerance
                    )

                    slow_actions.append(slow_action)
                    split_commutators.append(split_commutator)
                    cross_mixings.append(cross_mixing)
                    graph_errors.append(graph_error)
                    slow_invariance_errors.append(
                        slow_invariance_error
                    )

                    generator_rows.append({
                        "target_n": target_n,
                        "component_id": component_id,
                        "group": group_name,
                        "swap_a": swap[0],
                        "swap_b": swap[1],
                        "graph_automorphism_error": graph_error,
                        "slow_action_orthogonality_error": (
                            slow_invariance_error
                        ),
                        "common_split_commutator": (
                            split_commutator
                        ),
                        "common_sensitive_cross_mixing": (
                            cross_mixing
                        ),
                        "slow_action_trace": float(
                            np.trace(slow_action)
                        ),
                    })

                split_invariant = bool(
                    max(split_commutators, default=0.0)
                    <= args.projector_tolerance
                )
                fixed_dimension = fixed_subspace_dimension(
                    slow_actions,
                    args.rank_tolerance,
                )
                commutant_dim = commutant_dimension(
                    slow_actions,
                    args.rank_tolerance,
                )

                group_row = {
                    "target_n": target_n,
                    "component_id": component_id,
                    "pi_label": pi_text(pi_sides),
                    "component_states": len(vertices),
                    "group": group_name,
                    "generator_count": len(swaps),
                    "generators": json.dumps(swaps),
                    "slow_dimension": slow_dimension,
                    "common_dimension": common_dimension,
                    "sensitive_dimension": sensitive_dimension,
                    "split_invariant": split_invariant,
                    "max_split_commutator": max(
                        split_commutators,
                        default=0.0,
                    ),
                    "max_cross_mixing": max(
                        cross_mixings,
                        default=0.0,
                    ),
                    "slow_fixed_subspace_dimension": fixed_dimension,
                    "slow_commutant_dimension": commutant_dim,
                    "max_graph_automorphism_error": max(
                        graph_errors,
                        default=0.0,
                    ),
                    "max_slow_action_orthogonality_error": max(
                        slow_invariance_errors,
                        default=0.0,
                    ),
                }
                group_rows.append(group_row)
                n_group_results.append(group_row)

            critical_rows.append({
                "target_n": target_n,
                "source_n": source_n,
                "component_id": component_id,
                "pi_label": pi_text(pi_sides),
                "component_states": len(vertices),
                "lowest_gap": lowest_gap,
                "slow_dimension": slow_dimension,
                "charts": len(charts),
                "fusion_eigenvalues": json.dumps(
                    [float(value) for value in fusion_eigenvalues]
                ),
                "common_dimension": common_dimension,
                "sensitive_dimension": sensitive_dimension,
                "complete_anchors": json.dumps(complete_anchors),
                "incomplete_anchors": json.dumps(
                    incomplete_anchors
                ),
                "anchor_determines_capture": anchor_consistent,
                "old_labels": json.dumps(sorted(old_labels)),
                "new_labels": json.dumps(sorted(new_labels)),
                "chamber_preserving_transpositions": json.dumps(
                    preserving_swaps
                ),
            })

            print(
                f"  component={component_id} "
                f"slow={slow_dimension}="
                f"{common_dimension}+{sensitive_dimension} "
                f"complete-anchors={complete_anchors} "
                f"incomplete-anchors={incomplete_anchors} "
                f"frame-eigs="
                f"{[round(float(x), 9) for x in fusion_eigenvalues]}"
            )
            for row in n_group_results:
                if (
                    row["target_n"] == target_n
                    and row["component_id"] == component_id
                ):
                    print(
                        f"    {row['group']:<20} "
                        f"split-invariant={row['split_invariant']} "
                        f"commutant-dim="
                        f"{row['slow_commutant_dimension']} "
                        f"fixed-dim="
                        f"{row['slow_fixed_subspace_dimension']} "
                        f"max-mixing={row['max_cross_mixing']:.3e}"
                    )

        summaries[f"n{target_n}"] = {
            "source_n": source_n,
            "critical_components": critical_by_n.get(
                target_n,
                [],
            ),
            "group_split_invariance": {
                group_name: all(
                    row["split_invariant"]
                    for row in n_group_results
                    if row["group"] == group_name
                )
                for group_name in (
                    "OLD_LABEL_STABILIZER",
                    "GROWTH_SET_STABILIZER",
                    "CHAMBER_TRANSPOSITION_STABILIZER",
                )
            },
            "elapsed_seconds": time.perf_counter() - started,
        }
        print(
            f"  elapsed={summaries[f'n{target_n}']['elapsed_seconds']:.2f}s"
        )
        print()

    write_csv(
        out_dir / "critical_chart_average_split.csv",
        critical_rows,
    )
    write_csv(
        out_dir / "anchor_capture_summary.csv",
        anchor_rows,
    )
    write_csv(
        out_dir / "symmetry_generator_actions.csv",
        generator_rows,
    )
    write_csv(
        out_dir / "symmetry_group_summary.csv",
        group_rows,
    )

    checks = {key: bool(value) for key, value in checks.items()}
    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-QM3-03",
        "title": "Chart-Average Multiplet Split and Growth-Symmetry Audit",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "chart_script": str(chart_path),
        "qm3_02_summary": str(summary_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "interpretation_guardrail": (
            "The common/sensitive decomposition is a structural spectral "
            "decomposition induced by the chart family. Even if preserved by "
            "a relabelling group, it is not thereby spin, charge, chirality, "
            "gauge representation, or a particle multiplet."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_QM3_03_CHART_AVERAGE_GROWTH_SYMMETRY_PASS"
            if strict_pass else
            "EHF_QM3_03_CHART_AVERAGE_GROWTH_SYMMETRY_FAIL"
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
