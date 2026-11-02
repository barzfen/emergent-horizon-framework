#!/usr/bin/env python3
"""
EHF-AMP-FOUND-03C: Exact Tail-Filtration Subspace Lattice at 9 -> 8
===================================================================

03B proved that the exact fixed-anchor 9 -> 8 transmitted rank for
A={a<b<c} depends only on b,c. 03C explains that law at the level of the
transmitted subspaces themselves.

For each A, construct exactly

    I_A = D_A(ker Q_A) subset R_A^(8),

using the integer KK matrix Q_A and signed delete-9 map D_A. Transport the
target fibre F_A^(8) to the reference fibre F_{234}^(8) by the canonical
order-preserving block relabelling

    sorted(A)       -> (2,3,4),
    sorted(A^c)     -> (5,6,7,8).

All calculations are over QQ.

The probe establishes:

1. At fixed (b,c), changing a leaves the transported image exactly unchanged.
2. Across all 35 channels there are exactly six transported image subspaces,
   with dimensions 0,2,8,9,14,15.
3. They form the exact lattice

       V2 subset V8, V9,
       dim(V8 intersect V9)=3,
       V14 = V8 + V9,
       V14 subset V15=R_ref^(8), codim 1.

4. The common subgroup

       G=< (2 3), (5 6), (7 8) > ~= C2^3

   preserves the entire lattice. Exact joint-character multiplicities explain
   how the six rank levels occupy the 15-dimensional target relation space.

This converts the two-rightmost-label rank formula into a fixed target-space
tail-filtration law.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --out-dir runs/ehf_amp_found_03c \
  --strict
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
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

Cycle = Tuple[int, ...]
FibreKey = Tuple[Tuple[int, ...], Tuple[int, ...]]
Subset = Tuple[int, int, int]
SignTriple = Tuple[int, int, int]


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data: str) -> int:
        for stream in self.streams:
            stream.write(data)
            stream.flush()
        return len(data)

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()


def load_module(path: Path, name: str):
    if not path.exists():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    fields: List[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def json_safe(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


def subset_text(subset: Sequence[int]) -> str:
    return ",".join(map(str, subset))


def sign_text(signs: SignTriple) -> str:
    return "".join("+" if sign == 1 else "-" for sign in signs)


def canonical_rowspace(matrix: sp.MatrixBase) -> sp.Matrix:
    if matrix.rows == 0:
        return sp.zeros(0, matrix.cols)
    rref, _ = sp.Matrix(matrix).rref()
    rows = [
        list(rref.row(index))
        for index in range(rref.rows)
        if any(rref[index, column] != 0 for column in range(rref.cols))
    ]
    return sp.Matrix(rows) if rows else sp.zeros(0, rref.cols)


def rowspace_sum(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    if left.rows == 0:
        return right
    if right.rows == 0:
        return left
    return canonical_rowspace(sp.Matrix.vstack(left, right))


def intersection_dimension(left: sp.Matrix, right: sp.Matrix) -> int:
    return left.rows + right.rows - rowspace_sum(left, right).rows


def intersection_basis(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    if left.rows == 0 or right.rows == 0:
        return sp.zeros(0, left.cols)
    joined = left.T.row_join(-right.T)
    vectors = joined.nullspace()
    rows: List[List[sp.Expr]] = []
    for vector in vectors:
        coefficients = sp.Matrix(
            1,
            left.rows,
            [vector[index, 0] for index in range(left.rows)],
        )
        rows.append(list(coefficients * left))
    return canonical_rowspace(sp.Matrix(rows)) if rows else sp.zeros(0, left.cols)


def is_subspace(left: sp.Matrix, right: sp.Matrix) -> bool:
    return rowspace_sum(left, right).rows == right.rows


def target_action_dest(
    base,
    states: Sequence[Cycle],
    mapping: Mapping[int, int],
) -> List[int]:
    index = {cycle: position for position, cycle in enumerate(states)}
    destination: List[int] = []
    for cycle in states:
        relabelled = (1,) + tuple(mapping.get(label, label) for label in cycle[1:])
        canonical = base.canon(relabelled)
        destination.append(index[canonical])
    return destination


def transport_rows(rows: sp.Matrix, destination: Sequence[int]) -> sp.Matrix:
    if rows.rows == 0:
        return sp.zeros(0, len(destination))
    permutation = sp.zeros(len(destination))
    for source, target in enumerate(destination):
        permutation[target, source] = 1
    return canonical_rowspace(rows * permutation.T)


def canonical_target_transport(
    base,
    rank_module,
    subset: Subset,
    target_fibres: Mapping[FibreKey, Sequence[Cycle]],
    reference_subset: Subset,
    reference_states: Sequence[Cycle],
) -> Tuple[List[int], Dict[int, int]]:
    selected = tuple(subset)
    complement = tuple(label for label in range(2, 9) if label not in selected)
    reference_complement = tuple(
        label for label in range(2, 9) if label not in reference_subset
    )
    mapping: Dict[int, int] = {1: 1}
    mapping.update(dict(zip(selected, reference_subset)))
    mapping.update(dict(zip(complement, reference_complement)))

    source_states = target_fibres[rank_module.key_from_subset_8(subset)]
    reference_index = {
        cycle: position for position, cycle in enumerate(reference_states)
    }
    destination: List[int] = []
    for cycle in source_states:
        relabelled = (1,) + tuple(mapping[label] for label in cycle[1:])
        canonical = base.canon(relabelled)
        destination.append(reference_index[canonical])
    return destination, mapping


def exact_channel_image(
    base,
    helper,
    rank_module,
    subset: Subset,
    source_fibres: Mapping[FibreKey, Sequence[Cycle]],
    target_fibres: Mapping[FibreKey, Sequence[Cycle]],
    kk_index: Mapping[Tuple[int, ...], int],
) -> Tuple[sp.Matrix, Dict[str, object]]:
    q_matrix, stacked_matrix, metadata = (
        rank_module.exact_kk_and_stacked_matrices(
            base,
            helper,
            subset,
            source_fibres,
            target_fibres,
            kk_index,
        )
    )
    domain_q = DomainMatrix.from_Matrix(q_matrix).convert_to(QQ)
    nullspace_rows = domain_q.nullspace().to_Matrix()
    delete_matrix = stacked_matrix[math.factorial(7) :, :]
    image = delete_matrix * nullspace_rows.T
    image_rows = canonical_rowspace(image.T)

    q_rank = int(domain_q.rank())
    source_relation_dim = q_matrix.cols - q_rank
    metadata = {
        **metadata,
        "q_rank": q_rank,
        "source_relation_dim": source_relation_dim,
        "source_residue_kernel_dim": source_relation_dim - image_rows.rows,
        "image_rank": image_rows.rows,
    }
    return image_rows, metadata


def action_matrix_on_relation_basis(
    relation_basis: sp.Matrix,
    destination: Sequence[int],
) -> sp.Matrix:
    transformed = transport_rows_without_rref(relation_basis, destination)
    _, pivots = relation_basis.rref()
    pivot_columns = list(pivots)
    pivot_matrix = relation_basis[:, pivot_columns]
    representation = transformed[:, pivot_columns] * pivot_matrix.inv()
    if representation * relation_basis != transformed:
        raise RuntimeError("Failed to recover exact relation-space action")
    return representation


def transport_rows_without_rref(
    rows: sp.Matrix,
    destination: Sequence[int],
) -> sp.Matrix:
    permutation = sp.zeros(len(destination))
    for source, target in enumerate(destination):
        permutation[target, source] = 1
    return rows * permutation.T


def relation_coordinates(
    subspace: sp.Matrix,
    relation_basis: sp.Matrix,
) -> sp.Matrix:
    if subspace.rows == 0:
        return sp.zeros(0, relation_basis.rows)
    _, pivots = relation_basis.rref()
    pivot_columns = list(pivots)
    pivot_matrix = relation_basis[:, pivot_columns]
    coordinates = subspace[:, pivot_columns] * pivot_matrix.inv()
    if coordinates * relation_basis != subspace:
        raise RuntimeError("Subspace is not contained in the reference relation space")
    return canonical_rowspace(coordinates)


def stabilizer_order(
    base,
    reference_states: Sequence[Cycle],
    subspace: sp.Matrix,
    selected_labels: Sequence[int],
    complement_labels: Sequence[int],
) -> int:
    count = 0
    for selected_perm in itertools.permutations(selected_labels):
        for complement_perm in itertools.permutations(complement_labels):
            mapping = {1: 1}
            mapping.update(dict(zip(selected_labels, selected_perm)))
            mapping.update(dict(zip(complement_labels, complement_perm)))
            destination = target_action_dest(base, reference_states, mapping)
            if transport_rows(subspace, destination) == subspace:
                count += 1
    return count


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    helper_script = Path(args.helper_script).resolve()
    rank_script = Path(args.rank_script).resolve()
    direct_script = Path(args.direct_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_03c_base")
    helper = load_module(helper_script, "ehf_amp_found_03c_helper")
    rank_module = load_module(rank_script, "ehf_amp_found_03c_rank")
    direct = load_module(direct_script, "ehf_amp_found_03c_direct")

    source_fibres: Dict[FibreKey, List[Cycle]] = base.fibres(9)
    target_fibres: Dict[FibreKey, List[Cycle]] = base.fibres(8)
    subsets: List[Subset] = list(itertools.combinations(range(2, 9), 3))
    kk9_permutations = list(itertools.permutations(range(2, 9)))
    kk9_index = {
        permutation: index
        for index, permutation in enumerate(kk9_permutations)
    }

    reference_subset: Subset = (2, 3, 4)
    reference_key = rank_module.key_from_subset_8(reference_subset)
    reference_states = target_fibres[reference_key]

    print("=" * 122)
    print("EHF-AMP-FOUND-03C: EXACT TAIL-FILTRATION SUBSPACE LATTICE AT 9 -> 8")
    print("=" * 122)
    print(f"base script:                 {base_script}")
    print(f"reflection-aware helper:     {helper_script}")
    print(f"exact rank helper:           {rank_script}")
    print(f"exact n=8 helper:            {direct_script}")
    print(f"output directory:            {out_dir}")
    print(f"reference target fibre:      A={subset_text(reference_subset)}")
    print("coefficient domain:          QQ")
    print("numerical relation bases:    not used")

    # ------------------------------------------------------------------
    # Exact transmitted images, transported to a common target fibre.
    # ------------------------------------------------------------------
    channel_rows: List[Dict[str, object]] = []
    class_bases: MutableMapping[str, List[Tuple[Subset, sp.Matrix]]] = defaultdict(list)
    transported_bases_by_subset: Dict[Subset, sp.Matrix] = {}

    for index, subset in enumerate(subsets, start=1):
        t0 = time.time()
        image_rows, metadata = exact_channel_image(
            base,
            helper,
            rank_module,
            subset,
            source_fibres,
            target_fibres,
            kk9_index,
        )
        destination, mapping = canonical_target_transport(
            base,
            rank_module,
            subset,
            target_fibres,
            reference_subset,
            reference_states,
        )
        transported = transport_rows(image_rows, destination)
        transported_bases_by_subset[subset] = transported
        class_name = rank_module.rank_class_name(subset)
        class_bases[class_name].append((subset, transported))

        predicted_rank = rank_module.predicted_rank_from_two_rightmost(subset)
        channel_rows.append({
            "channel_index": index - 1,
            "A": subset_text(subset),
            "a": subset[0],
            "b": subset[1],
            "c": subset[2],
            "rank_class": class_name,
            "predicted_rank": predicted_rank,
            "exact_image_rank": transported.rows,
            "rank_matches_03B_law": transported.rows == predicted_rank,
            "exact_source_relation_dim": metadata["source_relation_dim"],
            "exact_source_residue_kernel_dim": metadata[
                "source_residue_kernel_dim"
            ],
            "source_fibre_size": metadata["source_fibre_size"],
            "canonical_transport_mapping": ";".join(
                f"{source}->{target}"
                for source, target in sorted(mapping.items())
                if source != 1
            ),
            "transported_subspace_rref_hash": hash(str(transported.tolist())),
            "elapsed_seconds": f"{time.time() - t0:.4f}",
        })

        if index % 5 == 0 or index == len(subsets):
            print(
                f"  [{index:02d}/35] A={subset_text(subset):5s} "
                f"rank={transported.rows:2d} class={class_name}"
            )

    write_csv(out_dir / "exact_transported_channel_images.csv", channel_rows)

    class_order = [
        "B_LE_4_C_LE_5",
        "B_LE_4_C_EQ_6",
        "B_EQ_5_C_EQ_6",
        "B_LE_4_C_GE_7",
        "B_EQ_5_C_GE_7",
        "B_GE_6",
    ]
    class_to_id = {
        "B_LE_4_C_LE_5": "V0",
        "B_LE_4_C_EQ_6": "V2",
        "B_EQ_5_C_EQ_6": "V8",
        "B_LE_4_C_GE_7": "V9",
        "B_EQ_5_C_GE_7": "V14",
        "B_GE_6": "V15",
    }

    representative_bases: Dict[str, sp.Matrix] = {}
    all_equal_within_class = True
    class_rows: List[Dict[str, object]] = []
    for class_name in class_order:
        items = class_bases[class_name]
        reference_basis = items[0][1]
        equal = all(basis == reference_basis for _, basis in items[1:])
        all_equal_within_class &= equal
        subspace_id = class_to_id[class_name]
        representative_bases[subspace_id] = reference_basis
        class_rows.append({
            "subspace_id": subspace_id,
            "rank_class": class_name,
            "dimension": reference_basis.rows,
            "channel_count": len(items),
            "subsets": ";".join(subset_text(subset) for subset, _ in items),
            "all_transported_images_equal_exactly": equal,
            "representative_A": subset_text(items[0][0]),
        })

    distinct_bases = {
        str(basis.tolist())
        for basis in representative_bases.values()
    }
    exactly_six_subspaces = len(distinct_bases) == 6

    # ------------------------------------------------------------------
    # Exact reference n=8 relation space.
    # ------------------------------------------------------------------
    kk8_permutations = list(itertools.permutations(range(2, 8)))
    kk8_index = {
        permutation: index
        for index, permutation in enumerate(kk8_permutations)
    }
    q8 = direct.exact_kk_coordinate_matrix(
        reference_states,
        8,
        kk8_index,
    )
    relation_basis = DomainMatrix.from_Matrix(q8).convert_to(QQ).nullspace().to_Matrix()
    relation_basis = canonical_rowspace(relation_basis)
    full_relation_dim = relation_basis.rows

    v0 = representative_bases["V0"]
    v2 = representative_bases["V2"]
    v8 = representative_bases["V8"]
    v9 = representative_bases["V9"]
    v14 = representative_bases["V14"]
    v15 = representative_bases["V15"]
    v3 = intersection_basis(v8, v9)

    lattice_checks = {
        "V0_is_zero": v0.rows == 0,
        "V2_subset_V8": is_subspace(v2, v8),
        "V2_subset_V9": is_subspace(v2, v9),
        "V8_intersection_V9_dimension_3": v3.rows == 3,
        "V14_equals_V8_plus_V9": v14 == rowspace_sum(v8, v9),
        "V14_subset_V15": is_subspace(v14, v15),
        "V15_equals_full_target_relation_space": v15 == relation_basis,
        "V15_over_V14_dimension_1": v15.rows - v14.rows == 1,
    }
    exact_lattice = all(lattice_checks.values())

    subspace_bases = {
        "V0": v0,
        "V2": v2,
        "V3_intersection": v3,
        "V8": v8,
        "V9": v9,
        "V14": v14,
        "V15": v15,
    }

    pair_rows: List[Dict[str, object]] = []
    observed_ids = ["V0", "V2", "V8", "V9", "V14", "V15"]
    for left_id in observed_ids:
        for right_id in observed_ids:
            left = representative_bases[left_id]
            right = representative_bases[right_id]
            sum_basis = rowspace_sum(left, right)
            pair_rows.append({
                "left": left_id,
                "right": right_id,
                "left_dimension": left.rows,
                "right_dimension": right.rows,
                "intersection_dimension": intersection_dimension(left, right),
                "sum_dimension": sum_basis.rows,
                "left_subset_right": is_subspace(left, right),
                "right_subset_left": is_subspace(right, left),
            })
    write_csv(out_dir / "pairwise_subspace_lattice.csv", pair_rows)

    # ------------------------------------------------------------------
    # Stabilizers inside S3 x S4 of the reference target fibre.
    # ------------------------------------------------------------------
    selected_labels = reference_subset
    complement_labels = tuple(
        label for label in range(2, 9) if label not in selected_labels
    )
    expected_stabilizers = {
        "V0": 144,
        "V2": 8,
        "V8": 24,
        "V9": 48,
        "V14": 8,
        "V15": 144,
    }
    stabilizer_rows: List[Dict[str, object]] = []
    stabilizer_orders: Dict[str, int] = {}
    for subspace_id in observed_ids:
        order = stabilizer_order(
            base,
            reference_states,
            representative_bases[subspace_id],
            selected_labels,
            complement_labels,
        )
        stabilizer_orders[subspace_id] = order
        stabilizer_rows.append({
            "subspace_id": subspace_id,
            "dimension": representative_bases[subspace_id].rows,
            "stabilizer_order_inside_S3xS4": order,
            "expected_order": expected_stabilizers[subspace_id],
            "expected_order_match": order == expected_stabilizers[subspace_id],
            "structural_description": {
                "V0": "full S3 x S4",
                "V2": "<(2 3),(5 6),(7 8)> ~= C2^3",
                "V8": "S3 on {2,3,4} times C2 on {5,6} times C2 on {7,8}",
                "V9": "C2 on {2,3} times S4 on {5,6,7,8}",
                "V14": "<(2 3),(5 6),(7 8)> ~= C2^3",
                "V15": "full S3 x S4",
            }[subspace_id],
        })
    write_csv(out_dir / "target_subspace_stabilizers.csv", stabilizer_rows)
    stabilizer_orders_match = stabilizer_orders == expected_stabilizers

    # ------------------------------------------------------------------
    # C2^3 joint-character decomposition.
    # ------------------------------------------------------------------
    generators = [
        ("g1=(2 3)", {2: 3, 3: 2}),
        ("g2=(5 6)", {5: 6, 6: 5}),
        ("g3=(7 8)", {7: 8, 8: 7}),
    ]
    generator_matrices: List[sp.Matrix] = []
    for _, mapping in generators:
        destination = target_action_dest(base, reference_states, mapping)
        matrix = action_matrix_on_relation_basis(relation_basis, destination)
        generator_matrices.append(matrix)

    generators_are_commuting_involutions = all(
        matrix * matrix == sp.eye(full_relation_dim)
        for matrix in generator_matrices
    ) and all(
        generator_matrices[left] * generator_matrices[right]
        == generator_matrices[right] * generator_matrices[left]
        for left in range(3)
        for right in range(left + 1, 3)
    )

    identity = sp.eye(full_relation_dim)
    eigenspaces: Dict[SignTriple, sp.Matrix] = {}
    for signs in itertools.product((1, -1), repeat=3):
        projector = identity
        for sign, generator in zip(signs, generator_matrices):
            projector = projector * (identity + sign * generator) / 2
        eigenspaces[signs] = canonical_rowspace(projector)

    subspace_coordinates = {
        subspace_id: relation_coordinates(
            representative_bases[subspace_id],
            relation_basis,
        )
        for subspace_id in observed_ids
    }
    v3_coordinates = relation_coordinates(v3, relation_basis)

    character_rows: List[Dict[str, object]] = []
    for signs in itertools.product((1, -1), repeat=3):
        eigenspace = eigenspaces[signs]
        row: Dict[str, object] = {
            "character": sign_text(signs),
            "g1_23": signs[0],
            "g2_56": signs[1],
            "g3_78": signs[2],
            "full_R15_multiplicity": eigenspace.rows,
        }
        for subspace_id in observed_ids:
            row[f"{subspace_id}_multiplicity"] = intersection_dimension(
                subspace_coordinates[subspace_id],
                eigenspace,
            )
        row["V3_intersection_multiplicity"] = intersection_dimension(
            v3_coordinates,
            eigenspace,
        )
        character_rows.append(row)
    write_csv(out_dir / "c2cubed_character_decomposition.csv", character_rows)

    expected_full_char_dims = {
        "+++": 0,
        "++-": 1,
        "+-+": 1,
        "+--": 3,
        "-++": 1,
        "-+-": 3,
        "--+": 3,
        "---": 3,
    }
    full_char_dims = {
        row["character"]: int(row["full_R15_multiplicity"])
        for row in character_rows
    }
    full_character_match = full_char_dims == expected_full_char_dims

    expected_subspace_chars = {
        "V2": {
            "+++": 0, "++-": 0, "+-+": 1, "+--": 0,
            "-++": 0, "-+-": 0, "--+": 0, "---": 1,
        },
        "V8": {
            "+++": 0, "++-": 0, "+-+": 1, "+--": 1,
            "-++": 1, "-+-": 1, "--+": 2, "---": 2,
        },
        "V9": {
            "+++": 0, "++-": 1, "+-+": 1, "+--": 3,
            "-++": 0, "-+-": 1, "--+": 1, "---": 2,
        },
        "V14": {
            "+++": 0, "++-": 1, "+-+": 1, "+--": 3,
            "-++": 1, "-+-": 2, "--+": 3, "---": 3,
        },
        "V15": expected_full_char_dims,
        "V3_intersection": {
            "+++": 0, "++-": 0, "+-+": 1, "+--": 1,
            "-++": 0, "-+-": 0, "--+": 0, "---": 1,
        },
    }
    computed_subspace_chars: Dict[str, Dict[str, int]] = {}
    for subspace_id in ["V2", "V8", "V9", "V14", "V15"]:
        computed_subspace_chars[subspace_id] = {
            row["character"]: int(row[f"{subspace_id}_multiplicity"])
            for row in character_rows
        }
    computed_subspace_chars["V3_intersection"] = {
        row["character"]: int(row["V3_intersection_multiplicity"])
        for row in character_rows
    }
    subspace_character_match = (
        computed_subspace_chars == expected_subspace_chars
    )

    # ------------------------------------------------------------------
    # Compact exact certificates.
    # ------------------------------------------------------------------
    for row in class_rows:
        subspace_id = str(row["subspace_id"])
        row["stabilizer_order"] = stabilizer_orders[subspace_id]
        row["tail_activation_description"] = {
            "V0": "no selected label at or above 6",
            "V2": "single selected tail label 6, with 5 absent",
            "V8": "selected pair {5,6}",
            "V9": "single selected tail label 7 or 8, with 5 absent",
            "V14": "selected 5 and one of {7,8}",
            "V15": "at least two selected labels from {6,7,8}",
        }[subspace_id]
    write_csv(out_dir / "six_tail_filtration_subspaces.csv", class_rows)

    basis_payload = {
        subspace_id: {
            "dimension": basis.rows,
            "rref_rows": [
                [str(value) for value in basis.row(row)]
                for row in range(basis.rows)
            ],
        }
        for subspace_id, basis in subspace_bases.items()
    }
    with (out_dir / "exact_subspace_rref_bases.json").open("w") as handle:
        json.dump(basis_payload, handle, indent=2)

    exact_explanation = (
        all(row["rank_matches_03B_law"] for row in channel_rows)
        and all_equal_within_class
        and exactly_six_subspaces
        and exact_lattice
        and stabilizer_orders_match
        and generators_are_commuting_involutions
        and full_character_match
        and subspace_character_match
    )

    verdict = (
        "EHF_AMP_FOUND_03C_EXACT_TAIL_FILTRATION_SUBSPACE_LAW_PROVED"
        if exact_explanation
        else "EHF_AMP_FOUND_03C_TAIL_FILTRATION_EXPLANATION_FAILED"
    )

    certificate = {
        "theorem": (
            "After canonical ordered-block transport to the A={2,3,4} target "
            "fibre, the 35 exact 9->8 residue images collapse to six fixed "
            "subspaces V0,V2,V8,V9,V14,V15 selected by the two-rightmost-label "
            "tail class."
        ),
        "canonical_transport": {
            "selected_labels": "sorted(A) -> (2,3,4)",
            "complement_labels": "sorted(A^c) -> (5,6,7,8)",
            "reflection_character_at_n8": "+1",
        },
        "six_subspaces": {
            row["subspace_id"]: {
                "dimension": row["dimension"],
                "channel_count": row["channel_count"],
                "rank_class": row["rank_class"],
                "tail_activation_description": row[
                    "tail_activation_description"
                ],
            }
            for row in class_rows
        },
        "lattice": {
            **lattice_checks,
            "V8_intersection_V9": "V3 of dimension 3",
            "V14": "V8 + V9",
            "V15": "full 15-dimensional reference target relation space",
        },
        "common_symmetry": {
            "group": "C2^3",
            "generators": [name for name, _ in generators],
            "commuting_involutions_exact": generators_are_commuting_involutions,
            "full_relation_character_multiplicities": full_char_dims,
            "subspace_character_multiplicities": computed_subspace_chars,
        },
        "stabilizer_orders_inside_S3xS4": stabilizer_orders,
        "interpretation": (
            "The smallest label a changes the size and kernel of the source "
            "relation space but, after canonical target transport, contributes "
            "no new transmitted target direction. The ordered tail occupancy "
            "activates a fixed lattice of target relation subspaces."
        ),
        "claim_boundary": (
            "This is an exact finite-dimensional explanation of the 03B rank "
            "law. It does not yet derive the lattice from a short closed-form "
            "KK identity, establish anchor independence, or prove a general "
            "odd-to-even theorem for arbitrary multiplicity."
        ),
    }
    with (out_dir / "exact_tail_filtration_certificate.json").open("w") as handle:
        json.dump(json_safe(certificate), handle, indent=2)

    elapsed = time.time() - started
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "channel_count": 35,
        "all_exact_ranks_match_03B": all(
            row["rank_matches_03B_law"] for row in channel_rows
        ),
        "all_images_equal_within_tail_class": all_equal_within_class,
        "distinct_transported_image_subspaces": len(distinct_bases),
        "subspace_dimensions": {
            subspace_id: representative_bases[subspace_id].rows
            for subspace_id in observed_ids
        },
        "V8_intersection_V9_dimension": v3.rows,
        "V14_equals_V8_plus_V9": lattice_checks["V14_equals_V8_plus_V9"],
        "V15_equals_full_target_relation_space": lattice_checks[
            "V15_equals_full_target_relation_space"
        ],
        "stabilizer_orders": stabilizer_orders,
        "C2cubed_character_decomposition_exact": (
            generators_are_commuting_involutions
            and full_character_match
            and subspace_character_match
        ),
        "exact_tail_filtration_explanation": exact_explanation,
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "exact_tail_filtration_certificate.json",
            "exact_transported_channel_images.csv",
            "six_tail_filtration_subspaces.csv",
            "pairwise_subspace_lattice.csv",
            "target_subspace_stabilizers.csv",
            "c2cubed_character_decomposition.csv",
            "exact_subspace_rref_bases.json",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)
    with (out_dir / "verdict.json").open("w") as handle:
        json.dump(
            {
                "verdict": verdict,
                "exact_tail_filtration_explanation": exact_explanation,
                "six_distinct_subspaces": exactly_six_subspaces,
                "exact_lattice": exact_lattice,
            },
            handle,
            indent=2,
        )

    strict_failures: List[str] = []
    if args.strict:
        checks = {
            "all_35_ranks_match": all(
                row["rank_matches_03B_law"] for row in channel_rows
            ),
            "equal_within_tail_class": all_equal_within_class,
            "exactly_six_subspaces": exactly_six_subspaces,
            "exact_lattice": exact_lattice,
            "stabilizer_orders": stabilizer_orders_match,
            "C2cubed_generators": generators_are_commuting_involutions,
            "full_character_dimensions": full_character_match,
            "subspace_character_dimensions": subspace_character_match,
        }
        strict_failures = [
            name for name, passed in checks.items() if not passed
        ]

    print("\nExact transported-image collapse")
    print(f"  equal within each tail class:       {all_equal_within_class}")
    print(f"  distinct transported subspaces:     {len(distinct_bases)}")
    print(
        "  dimensions:                        "
        f"{ {sid: representative_bases[sid].rows for sid in observed_ids} }"
    )

    print("\nExact subspace lattice")
    print(f"  dim(V8 intersect V9):               {v3.rows}")
    print(f"  V14 = V8 + V9:                      {lattice_checks['V14_equals_V8_plus_V9']}")
    print(f"  V15 = full target relation space:   {lattice_checks['V15_equals_full_target_relation_space']}")
    print(f"  codim(V14 in V15):                  {v15.rows - v14.rows}")

    print("\nCommon C2^3 character decomposition")
    print(f"  commuting involutions:              {generators_are_commuting_involutions}")
    print(f"  full R15 multiplicities:            {full_char_dims}")
    print(f"  exact subspace multiplicities:      {subspace_character_match}")

    print("\n" + "=" * 122)
    print("FINAL SUMMARY")
    print("=" * 122)
    print(f"All 35 exact ranks recovered:         {summary['all_exact_ranks_match_03B']}")
    print(f"Six fixed tail subspaces:             {all_equal_within_class and exactly_six_subspaces}")
    print(f"Exact lattice certificate:            {exact_lattice}")
    print(f"Exact stabilizer orders:              {stabilizer_orders_match}")
    print(f"Exact C2^3 character certificate:     {summary['C2cubed_character_decomposition_exact']}")
    print(f"Verdict:                              {verdict}")
    print(f"elapsed:                              {elapsed:.2f} seconds")
    print(f"summary:                              {out_dir / 'summary.json'}")
    if args.strict:
        print(f"strict checks:                        {'PASS' if not strict_failures else 'FAIL'}")
        if strict_failures:
            print(f"failed checks:                        {', '.join(strict_failures)}")
    print("=" * 122)

    if strict_failures:
        raise SystemExit(2)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Exact explanation of the 9->8 two-rightmost-label rank law as "
            "a six-subspace tail filtration in a common 15-dimensional target."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--helper-script", required=True)
    parser.add_argument("--rank-script", required=True)
    parser.add_argument("--direct-script", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "run.log").open("w") as log:
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = Tee(original_stdout, log)
        sys.stderr = Tee(original_stderr, log)
        try:
            print(f"===== RUN START {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            run(args)
            print(f"===== RUN END {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            return 0
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr


if __name__ == "__main__":
    raise SystemExit(main())
