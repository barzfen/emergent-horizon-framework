#!/usr/bin/env python3
"""
EHF-QM3-04
==========
Exact Product-Symmetric Slow-Representation Classification

QM3-03 found that the common/sensitive split in each chart-critical OPW3 slow
multiplet is preserved by every chamber-preserving label transposition.

This probe generates the full finite group induced by those transpositions and
classifies its representation on the complete lowest eigenspace.

For each critical chamber it:

  * generates the exact label-permutation group;
  * discovers the disjoint transposition supports;
  * verifies a direct-product symmetric-group structure;
  * computes full, common-sector, and sensitive-sector characters;
  * tests the candidate decomposition

        Std(S_A) tensor 1(S_B)
        plus
        1(S_A) tensor Std(S_B);

  * computes block commutants and cross-intertwiner dimensions;
  * reconstructs the common and sensitive projectors from character sums.

This is finite representation theory of a structural graph symmetry.  It does
not establish physical spin, gauge group, charge, particle species, or a
physical Hamiltonian.
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
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Hashable, Iterable, List, Mapping, Sequence, Set, Tuple

import numpy as np
from scipy import sparse

SCRIPT_VERSION = "ehf_qm3_04_2026-07-25"

Permutation = Tuple[int, ...]
Swap = Tuple[int, int]


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

    inv = np.divide(
        1.0,
        np.sqrt(degrees),
        out=np.zeros_like(degrees),
        where=degrees > 0,
    )
    symmetric_walk = inv[:, None] * adjacency_matrix * inv[None, :]
    return np.eye(n) - symmetric_walk, degrees


def partition_basis(colors: Sequence[int], degrees: np.ndarray) -> np.ndarray:
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


def identity_permutation(n: int) -> Permutation:
    return tuple(range(n))


def transposition_permutation(n: int, swap: Swap) -> Permutation:
    a, b = swap
    permutation = list(range(n))
    permutation[a], permutation[b] = permutation[b], permutation[a]
    return tuple(permutation)


def compose_permutations(left: Permutation, right: Permutation) -> Permutation:
    """Return left after right."""
    return tuple(left[right[i]] for i in range(len(right)))


def inverse_permutation(permutation: Permutation) -> Permutation:
    inverse = [0] * len(permutation)
    for i, image in enumerate(permutation):
        inverse[image] = i
    return tuple(inverse)


def generate_group(
    degree: int,
    generator_permutations: Sequence[Permutation],
) -> List[Permutation]:
    identity = identity_permutation(degree)
    seen = {identity}
    queue = deque([identity])

    while queue:
        current = queue.popleft()
        for generator in generator_permutations:
            candidate = compose_permutations(generator, current)
            if candidate not in seen:
                seen.add(candidate)
                queue.append(candidate)

    return sorted(seen)


def relabel_cycle(base, cycle, permutation: Permutation):
    return base.canonical_cycle(
        tuple(permutation[label] for label in cycle)
    )


def permutation_preserves_chamber(
    base,
    cycles,
    global_index,
    vertices,
    permutation: Permutation,
) -> bool:
    vertex_set = set(vertices)
    return all(
        global_index[relabel_cycle(base, cycles[state], permutation)]
        in vertex_set
        for state in vertices
    )


def local_state_permutation_matrix(
    base,
    cycles,
    global_index,
    vertices,
    permutation: Permutation,
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
            raise RuntimeError("group element leaves the critical chamber")
        target_local = local_index[target_global]
        matrix[target_local, source_local] = 1.0

    return matrix


def support_components(
    degree: int,
    transpositions: Sequence[Swap],
) -> List[List[int]]:
    adjacency = {i: set() for i in range(degree)}
    involved = set()
    for a, b in transpositions:
        adjacency[a].add(b)
        adjacency[b].add(a)
        involved.update((a, b))

    components = []
    seen = set()
    for start in sorted(involved):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        component = []
        while stack:
            u = stack.pop()
            component.append(u)
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        components.append(sorted(component))

    components.sort()
    return components


def fixed_points_on_support(
    permutation: Permutation,
    support: Sequence[int],
) -> int:
    return sum(permutation[label] == label for label in support)


def standard_character(
    permutation: Permutation,
    support: Sequence[int],
) -> int:
    # Character of the zero-sum standard representation of S_m.
    return fixed_points_on_support(permutation, support) - 1


def cycle_type_on_support(
    permutation: Permutation,
    support: Sequence[int],
) -> Tuple[int, ...]:
    support_set = set(support)
    seen = set()
    lengths = []

    for start in support:
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            current = permutation[current]
            if current not in support_set:
                raise RuntimeError("group element does not preserve support")
            length += 1
        lengths.append(length)

    return tuple(sorted(lengths, reverse=True))


def commutant_dimension(
    actions: Sequence[np.ndarray],
    tolerance: float,
) -> int:
    if not actions:
        return 0
    dimension = actions[0].shape[0]
    identity = np.eye(dimension)
    equations = [
        np.kron(action.T, identity) - np.kron(identity, action)
        for action in actions
    ]
    stacked = np.vstack(equations)
    singular_values = np.linalg.svd(stacked, compute_uv=False)
    rank = int(np.sum(singular_values > tolerance))
    return dimension * dimension - rank


def intertwiner_dimension(
    actions_left: Sequence[np.ndarray],
    actions_right: Sequence[np.ndarray],
    tolerance: float,
) -> int:
    """
    Dimension of matrices X satisfying A_left X = X A_right for every element.
    """
    if not actions_left or not actions_right:
        return 0

    left_dim = actions_left[0].shape[0]
    right_dim = actions_right[0].shape[0]
    equations = []

    for left, right in zip(actions_left, actions_right):
        equations.append(
            np.kron(np.eye(right_dim), left)
            - np.kron(right.T, np.eye(left_dim))
        )

    stacked = np.vstack(equations)
    singular_values = np.linalg.svd(stacked, compute_uv=False)
    rank = int(np.sum(singular_values > tolerance))
    return left_dim * right_dim - rank


def character_projector(
    state_actions: Sequence[np.ndarray],
    characters: Sequence[float],
    irrep_dimension: int,
) -> np.ndarray:
    group_order = len(state_actions)
    total = np.zeros_like(state_actions[0])
    for character, action in zip(characters, state_actions):
        total += character * action
    return (irrep_dimension / group_order) * total


def projector_error(projector: np.ndarray) -> float:
    return max(
        float(np.linalg.norm(projector - projector.T, ord="fro")),
        float(np.linalg.norm(projector @ projector - projector, ord="fro")),
    )


def pi_text(label) -> str:
    return "|".join(",".join(str(x) for x in side) for side in label)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify the exact finite symmetry representation of chart-critical OPW3 slow multiplets."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--chart-script", required=True)
    parser.add_argument("--qm3-02-summary", required=True)
    parser.add_argument("--target-ns", type=parse_int_csv, default=[7, 9])
    parser.add_argument("--eigenvalue-tolerance", type=float, default=1e-8)
    parser.add_argument("--projector-tolerance", type=float, default=1e-7)
    parser.add_argument("--rank-tolerance", type=float, default=1e-8)
    parser.add_argument("--out-dir", default="runs/ehf_qm3_04")
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

    print("=" * 128)
    print("EHF-QM3-04: EXACT PRODUCT-SYMMETRIC SLOW-REPRESENTATION CLASSIFICATION")
    print("=" * 128)
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
    group_rows: List[dict] = []
    character_rows: List[dict] = []
    block_rows: List[dict] = []
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

        n_assignments = {}

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

            restricted_chart_projectors = []
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
                restricted_chart_projectors.append(
                    0.5 * (restricted + restricted.T)
                )

            fusion = np.sum(restricted_chart_projectors, axis=0)
            fusion_values, fusion_vectors = np.linalg.eigh(
                0.5 * (fusion + fusion.T)
            )
            common_keep = (
                fusion_values
                >= len(charts) - args.projector_tolerance
            )
            common_basis = fusion_vectors[:, common_keep]
            sensitive_basis = fusion_vectors[:, ~common_keep]
            common_projector_slow = common_basis @ common_basis.T
            sensitive_projector_slow = sensitive_basis @ sensitive_basis.T

            # Discover every chamber-preserving transposition.
            preserving_swaps: List[Swap] = []
            for a in range(target_n):
                for b in range(a + 1, target_n):
                    permutation = transposition_permutation(
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

            supports = support_components(
                target_n,
                preserving_swaps,
            )
            generator_permutations = [
                transposition_permutation(target_n, swap)
                for swap in preserving_swaps
            ]
            group = generate_group(
                target_n,
                generator_permutations,
            )

            expected_order = math.prod(
                math.factorial(len(support))
                for support in supports
            )
            checks[
                f"n{target_n}_c{component_id}_product_symmetric_order"
            ] = len(group) == expected_order
            checks[
                f"n{target_n}_c{component_id}_two_supports"
            ] = len(supports) == 2

            state_actions = []
            slow_actions = []
            common_actions = []
            sensitive_actions = []

            for permutation in group:
                state_action = local_state_permutation_matrix(
                    base,
                    target_cycles,
                    target_index,
                    vertices,
                    permutation,
                )
                slow_action = slow_basis.T @ state_action @ slow_basis
                common_action = common_basis.T @ slow_action @ common_basis
                sensitive_action = (
                    sensitive_basis.T
                    @ slow_action
                    @ sensitive_basis
                )
                cross_error = max(
                    float(
                        np.linalg.norm(
                            common_basis.T
                            @ slow_action
                            @ sensitive_basis,
                            ord="fro",
                        )
                    ),
                    float(
                        np.linalg.norm(
                            sensitive_basis.T
                            @ slow_action
                            @ common_basis,
                            ord="fro",
                        )
                    ),
                )
                checks[
                    f"n{target_n}_c{component_id}_g{len(state_actions)}_block_invariant"
                ] = cross_error <= args.projector_tolerance

                state_actions.append(state_action)
                slow_actions.append(slow_action)
                common_actions.append(common_action)
                sensitive_actions.append(sensitive_action)

            support_a, support_b = supports
            candidate_a_chars = [
                standard_character(permutation, support_a)
                for permutation in group
            ]
            candidate_b_chars = [
                standard_character(permutation, support_b)
                for permutation in group
            ]
            common_chars = [
                float(np.trace(action))
                for action in common_actions
            ]
            sensitive_chars = [
                float(np.trace(action))
                for action in sensitive_actions
            ]
            full_chars = [
                float(np.trace(action))
                for action in slow_actions
            ]

            def char_error(observed, expected):
                return max(
                    abs(float(a) - float(b))
                    for a, b in zip(observed, expected)
                )

            common_a_error = char_error(
                common_chars,
                candidate_a_chars,
            )
            common_b_error = char_error(
                common_chars,
                candidate_b_chars,
            )
            sensitive_a_error = char_error(
                sensitive_chars,
                candidate_a_chars,
            )
            sensitive_b_error = char_error(
                sensitive_chars,
                candidate_b_chars,
            )

            if (
                common_a_error <= args.projector_tolerance
                and sensitive_b_error <= args.projector_tolerance
            ):
                common_assignment = "STD_A_TENSOR_TRIV_B"
                sensitive_assignment = "TRIV_A_TENSOR_STD_B"
                common_expected = candidate_a_chars
                sensitive_expected = candidate_b_chars
            elif (
                common_b_error <= args.projector_tolerance
                and sensitive_a_error <= args.projector_tolerance
            ):
                common_assignment = "TRIV_A_TENSOR_STD_B"
                sensitive_assignment = "STD_A_TENSOR_TRIV_B"
                common_expected = candidate_b_chars
                sensitive_expected = candidate_a_chars
            else:
                common_assignment = "UNRESOLVED"
                sensitive_assignment = "UNRESOLVED"
                common_expected = candidate_a_chars
                sensitive_expected = candidate_b_chars

            checks[
                f"n{target_n}_c{component_id}_candidate_character_match"
            ] = common_assignment != "UNRESOLVED"
            checks[
                f"n{target_n}_c{component_id}_full_character_sum"
            ] = (
                char_error(
                    full_chars,
                    [
                        a + b
                        for a, b in zip(
                            candidate_a_chars,
                            candidate_b_chars,
                        )
                    ],
                )
                <= args.projector_tolerance
            )

            common_commutant = commutant_dimension(
                common_actions,
                args.rank_tolerance,
            )
            sensitive_commutant = commutant_dimension(
                sensitive_actions,
                args.rank_tolerance,
            )
            cross_intertwiners = intertwiner_dimension(
                common_actions,
                sensitive_actions,
                args.rank_tolerance,
            )

            checks[
                f"n{target_n}_c{component_id}_common_absolute_irreducible"
            ] = common_commutant == 1
            checks[
                f"n{target_n}_c{component_id}_sensitive_absolute_irreducible"
            ] = sensitive_commutant == 1
            checks[
                f"n{target_n}_c{component_id}_blocks_inequivalent"
            ] = cross_intertwiners == 0

            # Character projectors in the full chamber state space.
            p_slow_state = slow_basis @ slow_basis.T
            p_common_central_full = character_projector(
                state_actions,
                common_expected,
                common_basis.shape[1],
            )
            p_sensitive_central_full = character_projector(
                state_actions,
                sensitive_expected,
                sensitive_basis.shape[1],
            )
            # The full chamber representation can contain additional copies of
            # the same irreducible representation at other eigenvalues.
            # Sandwich the central idempotent by the intrinsic slow projector
            # to isolate the copy inside the lowest eigenspace.
            p_common_char = (
                p_slow_state
                @ p_common_central_full
                @ p_slow_state
            )
            p_sensitive_char = (
                p_slow_state
                @ p_sensitive_central_full
                @ p_slow_state
            )
            p_common_target = (
                slow_basis
                @ common_projector_slow
                @ slow_basis.T
            )
            p_sensitive_target = (
                slow_basis
                @ sensitive_projector_slow
                @ slow_basis.T
            )

            common_projector_error = float(
                np.linalg.norm(
                    p_common_char - p_common_target,
                    ord="fro",
                )
            )
            sensitive_projector_error = float(
                np.linalg.norm(
                    p_sensitive_char - p_sensitive_target,
                    ord="fro",
                )
            )
            checks[
                f"n{target_n}_c{component_id}_common_character_projector"
            ] = (
                common_projector_error
                <= 10 * args.projector_tolerance
                and projector_error(p_common_char)
                <= 10 * args.projector_tolerance
            )
            checks[
                f"n{target_n}_c{component_id}_sensitive_character_projector"
            ] = (
                sensitive_projector_error
                <= 10 * args.projector_tolerance
                and projector_error(p_sensitive_char)
                <= 10 * args.projector_tolerance
            )

            # Character ledger aggregated by cycle type on the two supports.
            class_rows: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], List[int]] = defaultdict(list)
            for group_index, permutation in enumerate(group):
                class_key = (
                    cycle_type_on_support(permutation, support_a),
                    cycle_type_on_support(permutation, support_b),
                )
                class_rows[class_key].append(group_index)

            for class_key, indices in sorted(class_rows.items()):
                character_rows.append({
                    "target_n": target_n,
                    "component_id": component_id,
                    "support_a_cycle_type": json.dumps(class_key[0]),
                    "support_b_cycle_type": json.dumps(class_key[1]),
                    "class_size_in_generated_group": len(indices),
                    "full_slow_character": statistics.fmean(
                        full_chars[i] for i in indices
                    ),
                    "common_character": statistics.fmean(
                        common_chars[i] for i in indices
                    ),
                    "sensitive_character": statistics.fmean(
                        sensitive_chars[i] for i in indices
                    ),
                    "candidate_std_a_character": statistics.fmean(
                        candidate_a_chars[i] for i in indices
                    ),
                    "candidate_std_b_character": statistics.fmean(
                        candidate_b_chars[i] for i in indices
                    ),
                })

            group_rows.append({
                "target_n": target_n,
                "source_n": source_n,
                "component_id": component_id,
                "pi_label": pi_text(target_pi[vertices[0]]),
                "component_states": len(vertices),
                "lowest_gap": lowest_gap,
                "slow_dimension": slow_dimension,
                "common_dimension": common_basis.shape[1],
                "sensitive_dimension": sensitive_basis.shape[1],
                "preserving_transpositions": json.dumps(
                    preserving_swaps
                ),
                "support_a": json.dumps(support_a),
                "support_b": json.dumps(support_b),
                "support_sizes": json.dumps(
                    [len(support_a), len(support_b)]
                ),
                "generated_group_order": len(group),
                "expected_product_symmetric_order": expected_order,
                "abstract_candidate": (
                    f"S_{len(support_a)} x S_{len(support_b)}"
                ),
                "common_assignment": common_assignment,
                "sensitive_assignment": sensitive_assignment,
                "common_character_error_std_a": common_a_error,
                "common_character_error_std_b": common_b_error,
                "sensitive_character_error_std_a": sensitive_a_error,
                "sensitive_character_error_std_b": sensitive_b_error,
                "common_character_projector_error": (
                    common_projector_error
                ),
                "sensitive_character_projector_error": (
                    sensitive_projector_error
                ),
            })

            block_rows.extend([
                {
                    "target_n": target_n,
                    "component_id": component_id,
                    "block": "COMMON",
                    "dimension": common_basis.shape[1],
                    "assignment": common_assignment,
                    "commutant_dimension": common_commutant,
                    "cross_intertwiner_dimension": cross_intertwiners,
                    "absolutely_irreducible_over_R": (
                        common_commutant == 1
                    ),
                },
                {
                    "target_n": target_n,
                    "component_id": component_id,
                    "block": "SENSITIVE",
                    "dimension": sensitive_basis.shape[1],
                    "assignment": sensitive_assignment,
                    "commutant_dimension": sensitive_commutant,
                    "cross_intertwiner_dimension": cross_intertwiners,
                    "absolutely_irreducible_over_R": (
                        sensitive_commutant == 1
                    ),
                },
            ])

            n_assignments[component_id] = {
                "group": f"S_{len(support_a)} x S_{len(support_b)}",
                "order": len(group),
                "common": common_assignment,
                "sensitive": sensitive_assignment,
                "common_dimension": common_basis.shape[1],
                "sensitive_dimension": sensitive_basis.shape[1],
            }

            print(
                f"  component={component_id} "
                f"group=S_{len(support_a)}xS_{len(support_b)} "
                f"order={len(group)} "
                f"slow={slow_dimension}="
                f"{common_basis.shape[1]}+"
                f"{sensitive_basis.shape[1]}"
            )
            print(
                f"    common={common_assignment} "
                f"sensitive={sensitive_assignment}"
            )
            print(
                f"    commutants="
                f"{common_commutant},"
                f"{sensitive_commutant} "
                f"cross-intertwiners={cross_intertwiners} "
                f"character-projector-errors="
                f"{common_projector_error:.3e},"
                f"{sensitive_projector_error:.3e}"
            )

        summaries[f"n{target_n}"] = {
            "source_n": source_n,
            "critical_components": critical_by_n.get(
                target_n,
                [],
            ),
            "assignments": n_assignments,
            "elapsed_seconds": time.perf_counter() - started,
        }
        print(
            f"  elapsed={summaries[f'n{target_n}']['elapsed_seconds']:.2f}s"
        )
        print()

    write_csv(
        out_dir / "product_group_classification.csv",
        group_rows,
    )
    write_csv(
        out_dir / "representation_character_table.csv",
        character_rows,
    )
    write_csv(
        out_dir / "representation_block_summary.csv",
        block_rows,
    )

    checks = {key: bool(value) for key, value in checks.items()}
    strict_pass = all(checks.values())

    summary = {
        "probe": "EHF-QM3-04",
        "title": "Exact Product-Symmetric Slow-Representation Classification",
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
            "The product-symmetric representation is a finite structural "
            "symmetry representation of OPW3 slow modes. It is not thereby a "
            "physical gauge group, spin representation, charge assignment, "
            "particle species, or Standard Model sector."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_QM3_04_PRODUCT_SYMMETRIC_REPRESENTATION_PASS"
            if strict_pass else
            "EHF_QM3_04_PRODUCT_SYMMETRIC_REPRESENTATION_FAIL"
        ),
    }

    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print("=" * 128)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {summary['elapsed_seconds']:.2f}s")
    print("=" * 128)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
