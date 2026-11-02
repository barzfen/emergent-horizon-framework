#!/usr/bin/env python3
"""
EHF-XBR-03
==========
Canonical Middle-Block Bridge Operator and Intertwining Obstruction

XBR-02 established OPW dynamics and AMP relation transport as two exact lifts
over one common 72-chart relabelling groupoid.  It did not construct a
non-arbitrary map between the two lifts.

XBR-03 tests the most direct canonical candidate in the reference chart.

For each AMP channel A:

    M_A : R^(HC_7) -> R^(C_A)

is the OPW/AMP middle-block growth incidence restricted to the n=9 source
chamber C_A;

    D_A : R^(C_A) -> R^(T_A)

is the signed AMP deletion map to the n=8 target fibre;

    V_A <= R^(T_A)

is the exact transmitted AMP relation image;

    A_A : R^(C_A) -> R^(C_A)

is the OPW3 chamber adjacency operator.

The depth-k bridge is

    B_A^(k) = V_A D_A A_A^k M_A.

The probe asks:

  * Does the direct bridge B_A^(0) exist?
  * Does one OPW step activate it?
  * What is the first exact activation depth?
  * How much of V_A is reached at depths 2 and 3?
  * Is the deletion-adjoint lift W_A = row(V_A D_A) invariant under A_A,
    as required for a direct adjacency intertwiner?

All matrix ranks and containments are computed exactly over QQ.  The OPW
adjacency is a canonical structural operator, not a physical Hamiltonian.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import itertools
import json
import math
import sys
import time
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Set, Tuple

import numpy as np
import sympy as sp
from scipy import sparse
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

SCRIPT_VERSION = "ehf_xbr_03_2026-07-26"

Cycle = Tuple[int, ...]
Subset = Tuple[int, int, int]
Edge = Tuple[int, int]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_module(path: Path, name: str):
    if not path.exists():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        path.write_text("")
        return
    fields: List[str] = []
    seen: Set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def exact_rank(matrix: sp.MatrixBase) -> int:
    if matrix.rows == 0 or matrix.cols == 0:
        return 0
    return int(
        DomainMatrix.from_Matrix(matrix)
        .convert_to(QQ)
        .rank()
    )


def sympy_to_csr_integer(matrix: sp.MatrixBase) -> sparse.csr_matrix:
    rows: List[int] = []
    cols: List[int] = []
    data: List[int] = []
    for (i, j), value in matrix.todok().items():
        rows.append(int(i))
        cols.append(int(j))
        data.append(int(value))
    return sparse.csr_matrix(
        (np.asarray(data, dtype=np.int64), (rows, cols)),
        shape=matrix.shape,
        dtype=np.int64,
    )


def csr_to_sympy_integer(matrix: sparse.spmatrix) -> sp.MutableSparseMatrix:
    coo = matrix.tocoo()
    entries = {
        (int(i), int(j)): int(value)
        for i, j, value in zip(coo.row, coo.col, coo.data)
        if int(value) != 0
    }
    return sp.MutableSparseMatrix(
        matrix.shape[0],
        matrix.shape[1],
        entries,
    )


def connected_components(adjacency: Sequence[Set[int]]) -> List[List[int]]:
    seen: Set[int] = set()
    output: List[List[int]] = []
    for start in range(len(adjacency)):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        component: List[int] = []
        while stack:
            state = stack.pop()
            component.append(state)
            for target in adjacency[state]:
                if target not in seen:
                    seen.add(target)
                    stack.append(target)
        component.sort()
        output.append(component)
    output.sort(key=lambda component: (-len(component), component[0]))
    return output


def insert_after_gap(
    cycle: Sequence[int],
    gap: int,
    new_label: int,
) -> Cycle:
    values = list(cycle)
    values.insert(gap + 1, new_label)
    return tuple(values)


def grow_by_descriptor(
    opw,
    source: Cycle,
    descriptor: Tuple[int, int],
) -> Cycle:
    first, second = descriptor
    intermediate = insert_after_gap(source, first, 7)
    child = insert_after_gap(intermediate, second, 8)
    return opw.canonical_cycle(child)


def local_adjacency(
    global_adjacency: Sequence[Set[int]],
    global_states: Sequence[int],
) -> Tuple[sparse.csr_matrix, Dict[int, int]]:
    local_index = {
        global_state: local_state
        for local_state, global_state in enumerate(global_states)
    }
    rows: List[int] = []
    cols: List[int] = []
    for global_state in global_states:
        i = local_index[global_state]
        for target in global_adjacency[global_state]:
            j = local_index.get(target)
            if j is not None:
                rows.append(i)
                cols.append(j)
    adjacency = sparse.csr_matrix(
        (
            np.ones(len(rows), dtype=np.int64),
            (rows, cols),
        ),
        shape=(len(global_states), len(global_states)),
        dtype=np.int64,
    )
    return adjacency, local_index


def minimum_support_distance(
    adjacency: sparse.csr_matrix,
    source_support: Sequence[int],
    target_support: Set[int],
) -> int | None:
    if not source_support or not target_support:
        return None

    if any(state in target_support for state in source_support):
        return 0

    distances = np.full(adjacency.shape[0], -1, dtype=np.int32)
    queue: deque[int] = deque()
    for state in source_support:
        if distances[state] == -1:
            distances[state] = 0
            queue.append(state)

    indptr = adjacency.indptr
    indices = adjacency.indices

    while queue:
        state = queue.popleft()
        next_distance = int(distances[state]) + 1
        for target in indices[indptr[state]:indptr[state + 1]]:
            target = int(target)
            if distances[target] != -1:
                continue
            distances[target] = next_distance
            if target in target_support:
                return next_distance
            queue.append(target)

    return None


def first_positive(values: Sequence[int]) -> int | None:
    for index, value in enumerate(values):
        if value > 0:
            return index
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the canonical middle-block/deletion bridge and exact "
            "OPW-adjacency intertwining obstruction."
        )
    )
    parser.add_argument("--opw-base-script", required=True)
    parser.add_argument("--amp-base-script", required=True)
    parser.add_argument("--amp-helper-script", required=True)
    parser.add_argument("--amp-rank-script", required=True)
    parser.add_argument("--amp-lattice-script", required=True)
    parser.add_argument("--xbr02-run-dir", required=True)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--out-dir", default="runs/ehf_xbr_03")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    if args.max_depth < 3:
        raise ValueError("--max-depth must be at least 3")

    opw_path = Path(args.opw_base_script).resolve()
    amp_base_path = Path(args.amp_base_script).resolve()
    amp_helper_path = Path(args.amp_helper_script).resolve()
    amp_rank_path = Path(args.amp_rank_script).resolve()
    amp_lattice_path = Path(args.amp_lattice_script).resolve()
    xbr02_run_dir = Path(args.xbr02_run_dir).resolve()
    xbr02_summary_path = xbr02_run_dir / "run_summary.json"
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for path in (
        opw_path,
        amp_base_path,
        amp_helper_path,
        amp_rank_path,
        amp_lattice_path,
        xbr02_summary_path,
    ):
        if not path.exists():
            raise FileNotFoundError(path)

    opw = load_module(opw_path, "ehf_xbr_03_opw")
    amp_base = load_module(amp_base_path, "ehf_xbr_03_amp_base")
    amp_helper = load_module(amp_helper_path, "ehf_xbr_03_amp_helper")
    amp_rank = load_module(amp_rank_path, "ehf_xbr_03_amp_rank")
    amp_lattice = load_module(
        amp_lattice_path,
        "ehf_xbr_03_amp_lattice",
    )

    with xbr02_summary_path.open() as handle:
        xbr02_summary = json.load(handle)

    print("=" * 128)
    print("EHF-XBR-03: CANONICAL MIDDLE-BLOCK BRIDGE AND INTERTWINING OBSTRUCTION")
    print("=" * 128)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"OPW engine:           {opw_path}")
    print(f"AMP base:             {amp_base_path}")
    print(f"AMP exact rank:       {amp_rank_path}")
    print(f"AMP lattice:          {amp_lattice_path}")
    print(f"XBR-02 certificate:   {xbr02_summary_path}")
    print(f"maximum depth:        {args.max_depth}")
    print(f"output directory:     {out_dir}")
    print(f"strict:               {args.strict}")
    print()

    started = time.perf_counter()
    checks: Dict[str, bool] = {}
    channel_rows: List[dict] = []

    xbr02_exact = (
        bool(xbr02_summary.get("strict_pass"))
        and xbr02_summary.get("verdict")
        == "EHF_XBR_02_COMMON_GROUPOID_DUAL_FUNCTOR_COMPATIBILITY_PASS"
    )
    checks["xbr02_common_groupoid_certificate"] = xbr02_exact

    # ------------------------------------------------------------------
    # OPW reference graph and middle-block incidence.
    # ------------------------------------------------------------------
    cycles9 = opw.generate_cycles(9)
    index9 = {cycle: state for state, cycle in enumerate(cycles9)}
    pi9 = [opw.pi_label(cycle) for cycle in cycles9]
    graph9 = opw.build_preserve_graph(
        cycles9,
        index9,
        pi9,
        "OPW3",
        opw.GRAPH_LENGTHS["OPW3"],
    )
    components9 = connected_components(graph9.adjacency)
    component_sets = {
        frozenset(component): component_id
        for component_id, component in enumerate(components9)
    }

    cycles7 = opw.generate_cycles(7)
    middle_parent_by_child: Dict[int, int] = {}
    for parent_id, parent in enumerate(cycles7):
        for descriptor in ((3, 3), (3, 4)):
            child = grow_by_descriptor(opw, parent, descriptor)
            child_id = index9[child]
            if child_id in middle_parent_by_child:
                raise RuntimeError("middle-block child has multiple parents")
            middle_parent_by_child[child_id] = parent_id

    checks["middle_block_global_incidences_720"] = (
        len(middle_parent_by_child) == 720
    )

    # ------------------------------------------------------------------
    # AMP reference fibres and exact channel helpers.
    # ------------------------------------------------------------------
    source_fibres = amp_base.fibres(9)
    target_fibres = amp_base.fibres(8)
    kk_permutations = list(itertools.permutations(range(2, 9)))
    kk_index = {
        permutation: index
        for index, permutation in enumerate(kk_permutations)
    }

    all_source_chambers_exact = True
    all_relation_ranks_exact = True
    all_delete_isometries = True
    all_direct_support_disjoint = True
    all_direct_bridges_zero = True
    all_one_step_bridges_zero = True
    all_growth_distances_two = True
    all_raw_depth_two = True
    all_joint_amp_depth_two = True
    all_nonzero_lifts_noninvariant = True

    selected_middle_incidence_total = 0
    growth_hit_channels = 0
    nonzero_amp_channels = 0
    joint_channels = 0
    full_at_depth2 = 0
    full_at_depth3 = 0
    partial_after_depth3: List[str] = []

    for subset_values in itertools.combinations(range(2, 9), 3):
        subset: Subset = tuple(subset_values)  # type: ignore[assignment]

        source_key = amp_rank.key_from_subset_9(subset)
        source_cycles_one = source_fibres[source_key]
        source_global_ids = [
            index9[tuple(label - 1 for label in cycle)]
            for cycle in source_cycles_one
        ]

        source_component_id = component_sets.get(
            frozenset(source_global_ids)
        )
        source_chamber_exact = source_component_id is not None
        all_source_chambers_exact &= source_chamber_exact

        adjacency, local_index = local_adjacency(
            graph9.adjacency,
            source_global_ids,
        )
        adjacency_sympy = csr_to_sympy_integer(adjacency)

        # M_A: local chamber states x 360 old n=7 states.
        middle_rows: List[int] = []
        middle_cols: List[int] = []
        for local_state, global_state in enumerate(source_global_ids):
            parent = middle_parent_by_child.get(global_state)
            if parent is not None:
                middle_rows.append(local_state)
                middle_cols.append(parent)

        middle_matrix = sparse.csr_matrix(
            (
                np.ones(len(middle_rows), dtype=np.int64),
                (middle_rows, middle_cols),
            ),
            shape=(len(source_global_ids), len(cycles7)),
            dtype=np.int64,
        )
        middle_count = len(middle_rows)
        selected_middle_incidence_total += middle_count
        if middle_count > 0:
            growth_hit_channels += 1

        # Exact AMP Q, D, and transmitted relation image V_A.
        q_matrix, stacked_matrix, metadata = (
            amp_rank.exact_kk_and_stacked_matrices(
                amp_base,
                amp_helper,
                subset,
                source_fibres,
                target_fibres,
                kk_index,
            )
        )
        delete_sympy = stacked_matrix[math.factorial(7):, :]
        delete_matrix = sympy_to_csr_integer(delete_sympy)

        relation_image, relation_metadata = (
            amp_lattice.exact_channel_image(
                amp_base,
                amp_helper,
                amp_rank,
                subset,
                source_fibres,
                target_fibres,
                kk_index,
            )
        )

        predicted_rank = int(
            amp_rank.predicted_rank_from_two_rightmost(subset)
        )
        relation_rank = int(relation_image.rows)
        relation_rank_exact = relation_rank == predicted_rank
        all_relation_ranks_exact &= relation_rank_exact

        if relation_rank > 0:
            nonzero_amp_channels += 1

        # D_A D_A^T = 2I: the signed deletion adjoint is an isometry
        # after normalization by 1/sqrt(2).
        delete_gram = delete_matrix @ delete_matrix.T
        expected_gram = 2 * sparse.identity(
            delete_matrix.shape[0],
            dtype=np.int64,
            format="csr",
        )
        delete_isometry = (
            (delete_gram - expected_gram).nnz == 0
        )
        all_delete_isometries &= delete_isometry

        active_delete_support = set(
            int(column)
            for column in np.unique(delete_matrix.nonzero()[1])
        )
        middle_support = set(middle_rows)
        direct_support_overlap = len(
            active_delete_support & middle_support
        )
        direct_support_disjoint = direct_support_overlap == 0
        all_direct_support_disjoint &= direct_support_disjoint

        support_distance = minimum_support_distance(
            adjacency,
            middle_rows,
            active_delete_support,
        )
        if middle_count > 0:
            all_growth_distances_two &= support_distance == 2

        # Bridge sequence B_A^(k) = V_A D_A A_A^k M_A.
        walk_matrix = middle_matrix
        raw_ranks: List[int] = []
        amp_ranks: List[int] = []
        raw_nonzeros: List[int] = []
        amp_nonzeros: List[int] = []

        for depth in range(args.max_depth + 1):
            raw_bridge_sparse = delete_matrix @ walk_matrix
            raw_nonzeros.append(int(raw_bridge_sparse.nnz))
            raw_bridge_sympy = csr_to_sympy_integer(
                raw_bridge_sparse
            )
            raw_rank = exact_rank(raw_bridge_sympy)
            raw_ranks.append(raw_rank)

            if relation_rank > 0:
                amp_bridge = relation_image * raw_bridge_sympy
                amp_rank_depth = exact_rank(amp_bridge)
                amp_nonzero_depth = sum(
                    1
                    for value in amp_bridge
                    if value != 0
                )
            else:
                amp_rank_depth = 0
                amp_nonzero_depth = 0

            amp_ranks.append(amp_rank_depth)
            amp_nonzeros.append(amp_nonzero_depth)
            walk_matrix = adjacency @ walk_matrix

        direct_bridge_zero = (
            raw_ranks[0] == 0 and amp_ranks[0] == 0
        )
        one_step_bridge_zero = (
            raw_ranks[1] == 0 and amp_ranks[1] == 0
        )
        all_direct_bridges_zero &= direct_bridge_zero
        all_one_step_bridges_zero &= one_step_bridge_zero

        raw_activation_depth = first_positive(raw_ranks)
        amp_activation_depth = first_positive(amp_ranks)

        if middle_count > 0:
            all_raw_depth_two &= raw_activation_depth == 2

        joint = middle_count > 0 and relation_rank > 0
        if joint:
            joint_channels += 1
            all_joint_amp_depth_two &= amp_activation_depth == 2
            if amp_ranks[2] == relation_rank:
                full_at_depth2 += 1
            if amp_ranks[3] == relation_rank:
                full_at_depth3 += 1
            else:
                partial_after_depth3.append(
                    ",".join(map(str, subset))
                )

        # W_A = row(V_A D_A) must be adjacency-invariant for a direct
        # intertwiner A_A J_A = J_A K_A to exist on the full AMP image.
        if relation_rank > 0:
            lifted_rows = relation_image * delete_sympy
            lifted_rank = exact_rank(lifted_rows)
            transported_rows = lifted_rows * adjacency_sympy
            generated_rank = exact_rank(
                lifted_rows.col_join(transported_rows)
            )
            adjacency_invariant = generated_rank == lifted_rank
            all_nonzero_lifts_noninvariant &= not adjacency_invariant
        else:
            lifted_rank = 0
            generated_rank = 0
            adjacency_invariant = True

        channel_rows.append({
            "subset": ",".join(map(str, subset)),
            "rank_class": amp_rank.rank_class_name(subset),
            "source_component_id": source_component_id,
            "source_chamber_size": len(source_global_ids),
            "source_chamber_exact": source_chamber_exact,
            "target_fibre_size": delete_matrix.shape[0],
            "active_deletion_states": len(active_delete_support),
            "middle_block_incidences": middle_count,
            "middle_delete_support_overlap": direct_support_overlap,
            "minimum_support_distance": (
                "" if support_distance is None else support_distance
            ),
            "predicted_amp_rank": predicted_rank,
            "exact_amp_rank": relation_rank,
            "amp_rank_exact": relation_rank_exact,
            "delete_gram_equals_2I": delete_isometry,
            "raw_rank_k0": raw_ranks[0],
            "raw_rank_k1": raw_ranks[1],
            "raw_rank_k2": raw_ranks[2],
            "raw_rank_k3": raw_ranks[3],
            "amp_rank_k0": amp_ranks[0],
            "amp_rank_k1": amp_ranks[1],
            "amp_rank_k2": amp_ranks[2],
            "amp_rank_k3": amp_ranks[3],
            "raw_activation_depth": (
                "" if raw_activation_depth is None
                else raw_activation_depth
            ),
            "amp_activation_depth": (
                "" if amp_activation_depth is None
                else amp_activation_depth
            ),
            "amp_full_at_k2": (
                joint and amp_ranks[2] == relation_rank
            ),
            "amp_full_at_k3": (
                joint and amp_ranks[3] == relation_rank
            ),
            "lifted_amp_rank": lifted_rank,
            "rank_span_W_plus_WA": generated_rank,
            "lift_adjacency_invariant": adjacency_invariant,
        })

    checks["all_35_source_fibres_are_opw_chambers"] = (
        all_source_chambers_exact
    )
    checks["all_35_amp_ranks_exact"] = all_relation_ranks_exact
    checks["all_35_delete_gram_equals_2I"] = all_delete_isometries
    checks["selected_half_middle_incidences_360"] = (
        selected_middle_incidence_total == 360
    )
    checks["growth_hit_channel_count_19"] = (
        growth_hit_channels == 19
    )
    checks["nonzero_amp_channel_count_31"] = (
        nonzero_amp_channels == 31
    )
    checks["joint_growth_amp_channel_count_16"] = (
        joint_channels == 16
    )
    checks["all_direct_supports_disjoint"] = (
        all_direct_support_disjoint
    )
    checks["all_direct_bridges_zero"] = all_direct_bridges_zero
    checks["all_one_step_bridges_zero"] = (
        all_one_step_bridges_zero
    )
    checks["all_growth_support_distances_two"] = (
        all_growth_distances_two
    )
    checks["all_raw_bridges_activate_at_depth_two"] = (
        all_raw_depth_two
    )
    checks["all_joint_amp_bridges_activate_at_depth_two"] = (
        all_joint_amp_depth_two
    )
    checks["full_amp_rank_at_depth2_count_9"] = (
        full_at_depth2 == 9
    )
    checks["full_amp_rank_at_depth3_count_14"] = (
        full_at_depth3 == 14
    )
    checks["partial_depth3_channels_exact"] = (
        sorted(partial_after_depth3)
        == ["2,3,7", "2,6,7"]
    )
    checks["all_31_nonzero_lifts_fail_adjacency_invariance"] = (
        all_nonzero_lifts_noninvariant
    )

    # Class-level summary.
    class_groups: MutableMapping[str, List[dict]] = defaultdict(list)
    for row in channel_rows:
        class_groups[str(row["rank_class"])].append(row)

    class_rows: List[dict] = []
    for class_name, rows in sorted(class_groups.items()):
        joint_rows = [
            row for row in rows
            if int(row["middle_block_incidences"]) > 0
            and int(row["exact_amp_rank"]) > 0
        ]
        class_rows.append({
            "rank_class": class_name,
            "channel_count": len(rows),
            "amp_rank_values": ",".join(
                map(
                    str,
                    sorted({
                        int(row["exact_amp_rank"])
                        for row in rows
                    }),
                )
            ),
            "growth_hit_channels": sum(
                int(row["middle_block_incidences"]) > 0
                for row in rows
            ),
            "joint_channels": len(joint_rows),
            "joint_full_at_k2": sum(
                bool(row["amp_full_at_k2"])
                for row in joint_rows
            ),
            "joint_full_at_k3": sum(
                bool(row["amp_full_at_k3"])
                for row in joint_rows
            ),
            "nonzero_lifts_invariant": sum(
                int(row["exact_amp_rank"]) > 0
                and bool(row["lift_adjacency_invariant"])
                for row in rows
            ),
        })

    write_csv(out_dir / "channel_bridge_ledger.csv", channel_rows)
    write_csv(out_dir / "bridge_class_summary.csv", class_rows)

    checks = {key: bool(value) for key, value in checks.items()}
    strict_pass = all(checks.values())
    elapsed = time.perf_counter() - started

    scientific_classification = (
        "DIRECT_AND_ONE_STEP_OBSTRUCTED_TWO_STEP_MEDIATED_BRIDGE"
        if (
            all_direct_bridges_zero
            and all_one_step_bridges_zero
            and all_joint_amp_depth_two
        )
        else "MIXED_BRIDGE_STRUCTURE"
    )

    verdict = (
        "EHF_XBR_03_TWO_STEP_MEDIATED_BRIDGE_INTERTWINING_OBSTRUCTION_PASS"
        if strict_pass
        else "EHF_XBR_03_CANONICAL_BRIDGE_AUDIT_FAIL"
    )

    summary = {
        "probe": "EHF-XBR-03",
        "title": (
            "Canonical Middle-Block Bridge Operator and "
            "Intertwining Obstruction"
        ),
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "checks": checks,
        "strict_pass": strict_pass,
        "counts": {
            "channels": len(channel_rows),
            "middle_block_incidences_global": 720,
            "middle_block_incidences_in_35_amp_source_chambers": (
                selected_middle_incidence_total
            ),
            "growth_hit_channels": growth_hit_channels,
            "nonzero_amp_channels": nonzero_amp_channels,
            "joint_growth_amp_channels": joint_channels,
            "joint_full_amp_rank_at_depth2": full_at_depth2,
            "joint_full_amp_rank_at_depth3": full_at_depth3,
            "partial_after_depth3": partial_after_depth3,
        },
        "exact_results": {
            "direct_bridge": "zero in all 35 channels",
            "one_step_bridge": "zero in all 35 channels",
            "support_distance": (
                "exactly two in every growth-hit AMP source chamber"
            ),
            "two_step_activation": (
                "all 19 raw growth-hit channels and all 16 joint "
                "growth/nonzero-relation channels"
            ),
            "adjacency_intertwiner": (
                "obstructed on all 31 nonzero AMP images because "
                "row(V_A D_A) is not OPW-adjacency invariant"
            ),
        },
        "scientific_classification": scientific_classification,
        "scientific_statement": (
            "The canonical direct middle-block/deletion pairing vanishes "
            "because middle-block descendants and deletion-active states have "
            "disjoint support. One OPW3 step is still insufficient. Exactly "
            "two OPW3 adjacency steps activate every channel in which both "
            "growth and a nonzero AMP image are present. The deletion-adjoint "
            "AMP lift is not adjacency-invariant in any nonzero channel, so "
            "there is no direct full-image adjacency intertwiner."
        ),
        "claim_boundary": (
            "This is a finite structural bridge/obstruction theorem for the "
            "OPW3 adjacency and exact AMP deletion images. It is not a "
            "physical time evolution, Hamiltonian, scattering derivation, "
            "or natural isomorphism between the two functors."
        ),
        "elapsed_seconds": elapsed,
        "verdict": verdict,
    }

    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print("[channel census]")
    print(
        f"  channels=35 growth-hit={growth_hit_channels} "
        f"nonzero-AMP={nonzero_amp_channels} joint={joint_channels}"
    )
    print(
        f"  middle-block incidences in AMP source half="
        f"{selected_middle_incidence_total}/720"
    )
    print()
    print("[canonical bridge]")
    print(
        f"  direct bridges zero={all_direct_bridges_zero} "
        f"one-step zero={all_one_step_bridges_zero}"
    )
    print(
        f"  growth support distance exactly two="
        f"{all_growth_distances_two}"
    )
    print(
        f"  all joint AMP bridges activate at k=2="
        f"{all_joint_amp_depth_two}"
    )
    print(
        f"  full AMP rank: k=2 {full_at_depth2}/{joint_channels}, "
        f"k=3 {full_at_depth3}/{joint_channels}"
    )
    print(
        f"  partial after k=3={partial_after_depth3}"
    )
    print()
    print("[intertwining obstruction]")
    print(
        f"  all 31 nonzero deletion-adjoint lifts non-invariant="
        f"{all_nonzero_lifts_noninvariant}"
    )
    print()
    print("=" * 128)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {verdict}")
    print(f"elapsed:              {elapsed:.2f}s")
    print("=" * 128)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
