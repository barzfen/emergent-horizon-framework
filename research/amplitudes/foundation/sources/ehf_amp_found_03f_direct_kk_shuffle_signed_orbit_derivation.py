#!/usr/bin/env python3
"""
EHF-AMP-FOUND-03F: Direct KK-Shuffle Signed-Orbit Derivation
============================================================

03E expressed the exact 9 -> 8 tail-filtration quotient directions in a
minimum-support signed C2^3-orbit normal form. 03F reconstructs the same
structure directly from exact Kleiss--Kuijf shuffle matrices.

No output file from 03C, 03D, or 03E is used.

The script constructs:

1. the exact n=8 KK matrix Q8 on the reference fibre A={2,3,4};
2. the exact signed-orbit atom basis A_chi for every C2^3 character chi;
3. the character-reduced KK shuffle matrix

       M_chi = Q8 A_chi^T;

4. the exact target relation kernel ker_Q(M_chi);
5. six representative n=9 source images using exact Q9 and delete-9 maps;
6. the five tail-filtration quotient layers inside the direct KK kernels;
7. every minimum-support signed-orbit normal form by exact support search.

For each derived direction c, the identity

       M_chi c^T = 0

is certified coordinate by coordinate in the 720-dimensional n=8 KK basis.
This is a direct exact KK-shuffle certificate for the normal forms, not merely
an agreement with the 03D seed construction.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_03f_direct_kk_shuffle_signed_orbit_derivation.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --out-dir runs/ehf_amp_found_03f \
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
from collections import Counter
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

Cycle = Tuple[int, ...]
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


def sign_text(signs: SignTriple) -> str:
    return "".join("+" if sign == 1 else "-" for sign in signs)


def cycle_text(cycle: Sequence[int]) -> str:
    return ",".join(map(str, cycle))


def intersection_basis(normal, left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
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
    if not rows:
        return sp.zeros(0, left.cols)
    return normal.canonical_rowspace(sp.Matrix(rows))


def exact_source_image(
    rank_module,
    base,
    helper,
    subset: Subset,
    source_fibres,
    target_fibres,
    kk9_index,
) -> sp.Matrix:
    q_matrix, stacked_matrix, _ = rank_module.exact_kk_and_stacked_matrices(
        base,
        helper,
        subset,
        source_fibres,
        target_fibres,
        kk9_index,
    )
    nullspace_rows = (
        DomainMatrix.from_Matrix(q_matrix)
        .convert_to(QQ)
        .nullspace()
        .to_Matrix()
    )
    delete_matrix = stacked_matrix[math.factorial(7) :, :]
    return sp.Matrix(delete_matrix * nullspace_rows.T).T


def canonical_transport_destination(
    base,
    rank_module,
    subset: Subset,
    target_fibres,
    reference_subset: Subset,
    reference_states: Sequence[Cycle],
) -> List[int]:
    selected = tuple(subset)
    complement = tuple(label for label in range(2, 9) if label not in selected)
    reference_complement = tuple(
        label for label in range(2, 9) if label not in reference_subset
    )
    mapping = {1: 1}
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
    return destination


def transport_rows(normal, rows: sp.Matrix, destination: Sequence[int]) -> sp.Matrix:
    if rows.rows == 0:
        return sp.zeros(0, len(destination))
    permutation = sp.zeros(len(destination))
    for source, target in enumerate(destination):
        permutation[target, source] = 1
    return normal.canonical_rowspace(rows * permutation.T)


def build_direct_tail_spaces(
    normal,
    rank_module,
    base,
    helper,
    source_fibres,
    target_fibres,
    kk9_index,
    reference_subset: Subset,
    reference_states: Sequence[Cycle],
) -> Dict[str, sp.Matrix]:
    representatives: Dict[str, Subset] = {
        "V0": (2, 3, 4),
        "V2": (2, 3, 6),
        "V8": (2, 5, 6),
        "V9": (2, 3, 7),
        "V14": (2, 5, 7),
        "V15": (2, 6, 7),
    }
    spaces: Dict[str, sp.Matrix] = {}
    for name, subset in representatives.items():
        image = exact_source_image(
            rank_module,
            base,
            helper,
            subset,
            source_fibres,
            target_fibres,
            kk9_index,
        )
        destination = canonical_transport_destination(
            base,
            rank_module,
            subset,
            target_fibres,
            reference_subset,
            reference_states,
        )
        spaces[name] = transport_rows(normal, image, destination)
    spaces["V3"] = intersection_basis(normal, spaces["V8"], spaces["V9"])
    return spaces


def matrix_sparse_rows(
    matrix: sp.Matrix,
    character: str,
    kk_permutations: Sequence[Tuple[int, ...]],
    atom_ids: Sequence[str],
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for row in range(matrix.rows):
        for column in range(matrix.cols):
            value = matrix[row, column]
            if value == 0:
                continue
            rows.append({
                "character": character,
                "kk_row_index": row,
                "kk_basis_ordering": "1," + cycle_text(kk_permutations[row]) + ",8",
                "atom_id": atom_ids[column],
                "coefficient": int(value),
            })
    return rows


def write_derivation_markdown(
    path: Path,
    character_rows: Sequence[Mapping[str, object]],
    direction_rows: Sequence[Mapping[str, object]],
) -> None:
    lines = [
        "# EHF-AMP-FOUND-03F",
        "## Direct KK-shuffle derivation of the signed-orbit normal forms",
        "",
        "For each character `chi`, the exact reduced shuffle matrix is",
        "",
        r"\[M_\chi=Q_8A_\chi^{\mathsf T}.\]",
        "",
        "A signed-orbit coefficient row `c` is a Parke-Taylor relation exactly when",
        "",
        r"\[M_\chi c^{\mathsf T}=0.\]",
        "",
        "No output from 03C, 03D, or 03E is used in the construction.",
        "",
        "## Character-reduced KK kernels",
        "",
        "| Character | Atom dimension | KK rank | Relation nullity | Expected |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in character_rows:
        lines.append(
            f"| `{row['character']}` | {row['atom_dimension']} | "
            f"{row['reduced_KK_rank']} | {row['relation_nullity']} | "
            f"{row['expected_relation_nullity']} |"
        )
    lines.extend([
        "",
        "## Direct quotient-character kernel vectors",
        "",
        "| Layer | Character | Direction | Minimum atoms | KK cancellation | Normal form |",
        "|---|---|---:|---:|---|---|",
    ])
    for row in direction_rows:
        lines.append(
            f"| {row['layer_id']} | `{row['character']}` | "
            f"{row['direction_index']} | {row['atom_support_count']} | "
            f"{'exact' if row['direct_KK_zero'] else 'failed'} | "
            f"`{row['atom_expression']}` |"
        )
    lines.extend([
        "",
        "The coordinate-level cancellation ledger records every nonzero atom contribution to every active KK basis coordinate and verifies zero net coefficient.",
        "",
    ])
    path.write_text("\n".join(lines))


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    helper_script = Path(args.helper_script).resolve()
    rank_script = Path(args.rank_script).resolve()
    direct_script = Path(args.direct_script).resolve()
    normal_script = Path(args.normal_form_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_03f_base")
    helper = load_module(helper_script, "ehf_amp_found_03f_helper")
    rank_module = load_module(rank_script, "ehf_amp_found_03f_rank")
    direct = load_module(direct_script, "ehf_amp_found_03f_direct")
    normal = load_module(normal_script, "ehf_amp_found_03f_normal")

    source_fibres = base.fibres(9)
    target_fibres = base.fibres(8)
    reference_subset: Subset = (2, 3, 4)
    reference_key = rank_module.key_from_subset_8(reference_subset)
    reference_states: List[Cycle] = target_fibres[reference_key]

    kk8_permutations = list(itertools.permutations(range(2, 8)))
    kk8_index = {permutation: index for index, permutation in enumerate(kk8_permutations)}
    q8 = direct.exact_kk_coordinate_matrix(reference_states, 8, kk8_index)
    q8_domain = DomainMatrix.from_Matrix(q8).convert_to(QQ)
    q8_relation_basis = normal.canonical_rowspace(q8_domain.nullspace().to_Matrix())

    kk9_permutations = list(itertools.permutations(range(2, 9)))
    kk9_index = {permutation: index for index, permutation in enumerate(kk9_permutations)}

    print("=" * 124)
    print("EHF-AMP-FOUND-03F: DIRECT KK-SHUFFLE SIGNED-ORBIT DERIVATION")
    print("=" * 124)
    print(f"base script:                 {base_script}")
    print(f"reflection-aware helper:     {helper_script}")
    print(f"exact 9->8 rank helper:      {rank_script}")
    print(f"exact KK helper:             {direct_script}")
    print(f"normal-form utilities:       {normal_script}")
    print(f"output directory:            {out_dir}")
    print("03C/03D/03E output files:    not used")
    print("coefficient domain:          QQ")

    generator_specs = [
        ("g1=(2 3)", {2: 3, 3: 2}),
        ("g2=(5 6)", {5: 6, 6: 5}),
        ("g3=(7 8)", {7: 8, 8: 7}),
    ]
    generators: List[sp.Matrix] = []
    for _, mapping in generator_specs:
        destination = normal.target_action_destination(base, reference_states, mapping)
        generators.append(normal.permutation_matrix(destination))

    identity = sp.eye(len(reference_states))
    group_powers = list(itertools.product((0, 1), repeat=3))
    group_matrices: List[sp.Matrix] = []
    group_destinations: List[List[int]] = []
    for powers in group_powers:
        matrix = identity
        for power, generator in zip(powers, generators):
            if power:
                matrix = matrix * generator
        group_matrices.append(matrix)
        group_destinations.append([
            next(row for row in range(len(reference_states)) if matrix[row, column] == 1)
            for column in range(len(reference_states))
        ])

    state_orbits = normal.state_orbits(len(reference_states), group_destinations)
    orbit_distribution = Counter(len(orbit) for orbit in state_orbits)

    atom_vectors: Dict[SignTriple, List[sp.Matrix]] = {}
    atom_ids: Dict[SignTriple, List[str]] = {}
    reduced_matrices: Dict[SignTriple, sp.Matrix] = {}
    direct_kernels: Dict[SignTriple, sp.Matrix] = {}
    reduced_sparse_rows: List[Dict[str, object]] = []
    character_rows: List[Dict[str, object]] = []

    expected_relation_nullities = {
        "+++": 0,
        "++-": 1,
        "+-+": 1,
        "+--": 3,
        "-++": 1,
        "-+-": 3,
        "--+": 3,
        "---": 3,
    }

    for signs in itertools.product((1, -1), repeat=3):
        vectors: List[sp.Matrix] = []
        identifiers: List[str] = []
        for orbit_index, orbit in enumerate(state_orbits, start=1):
            representative = min(orbit)
            atom = normal.signed_orbit_atom(
                representative,
                signs,
                group_powers,
                group_destinations,
                len(reference_states),
            )
            if not any(value != 0 for value in atom):
                continue
            vectors.append(atom)
            identifiers.append(f"Omega_{sign_text(signs)}_O{orbit_index:02d}")
        atom_basis = sp.Matrix.vstack(*vectors)
        reduced = sp.Matrix(q8 * atom_basis.T)
        kernel = normal.canonical_rowspace(
            DomainMatrix.from_Matrix(reduced).convert_to(QQ).nullspace().to_Matrix()
        )
        character = sign_text(signs)
        atom_vectors[signs] = vectors
        atom_ids[signs] = identifiers
        reduced_matrices[signs] = reduced
        direct_kernels[signs] = kernel
        reduced_rank = int(DomainMatrix.from_Matrix(reduced).convert_to(QQ).rank())
        nullity = kernel.rows
        expected = expected_relation_nullities[character]
        character_rows.append({
            "character": character,
            "atom_dimension": atom_basis.rows,
            "reduced_KK_rows": reduced.rows,
            "reduced_KK_rank": reduced_rank,
            "relation_nullity": nullity,
            "expected_relation_nullity": expected,
            "nullity_match": nullity == expected,
            "nonzero_reduced_KK_entries": sum(
                reduced[row, column] != 0
                for row in range(reduced.rows)
                for column in range(reduced.cols)
            ),
        })
        reduced_sparse_rows.extend(
            matrix_sparse_rows(reduced, character, kk8_permutations, identifiers)
        )

    write_csv(out_dir / "character_reduced_kk_summary.csv", character_rows)
    write_csv(out_dir / "character_reduced_kk_sparse_entries.csv", reduced_sparse_rows)

    spaces = build_direct_tail_spaces(
        normal,
        rank_module,
        base,
        helper,
        source_fibres,
        target_fibres,
        kk9_index,
        reference_subset,
        reference_states,
    )
    expected_dimensions = {"V0": 0, "V2": 2, "V3": 3, "V8": 8, "V9": 9, "V14": 14, "V15": 15}
    dimensions_match = all(spaces[name].rows == dimension for name, dimension in expected_dimensions.items())
    lattice_checks = {
        "V2_subset_V3": normal.is_subspace(spaces["V2"], spaces["V3"]),
        "V3_subset_V8": normal.is_subspace(spaces["V3"], spaces["V8"]),
        "V3_subset_V9": normal.is_subspace(spaces["V3"], spaces["V9"]),
        "V14_equals_V8_plus_V9": spaces["V14"] == normal.rowspace_sum(spaces["V8"], spaces["V9"]),
        "V15_equals_direct_Q8_kernel": spaces["V15"] == q8_relation_basis,
    }

    layers = [
        ("L2", "V2/V0", "V0", "V2"),
        ("L3", "V3/V2", "V2", "V3"),
        ("L8", "V8/V3", "V3", "V8"),
        ("L9", "V9/V3", "V3", "V9"),
        ("L15", "V15/V14", "V14", "V15"),
    ]
    expected_profiles = {
        ("L2", "+-+"): (5,),
        ("L2", "---"): (6,),
        ("L3", "+--"): (6,),
        ("L8", "-++"): (3,),
        ("L8", "-+-"): (5,),
        ("L8", "--+"): (4, 5),
        ("L8", "---"): (4,),
        ("L9", "++-"): (5,),
        ("L9", "+--"): (4, 5),
        ("L9", "-+-"): (8,),
        ("L9", "--+"): (8,),
        ("L9", "---"): (6,),
        ("L15", "-+-"): (5,),
    }

    quotient_rows: List[Dict[str, object]] = []
    direction_rows: List[Dict[str, object]] = []
    atom_coefficient_rows: List[Dict[str, object]] = []
    expanded_rows: List[Dict[str, object]] = []
    cancellation_rows: List[Dict[str, object]] = []

    all_direct_kernel_containment = True
    all_profiles_match = True
    all_quotients_reconstructed = True
    all_coordinate_cancellations = True
    total_atom_count = 0
    direction_count = 0

    for layer_id, quotient_name, lower_name, upper_name in layers:
        lower_space = spaces[lower_name]
        upper_space = spaces[upper_name]
        for signs in itertools.product((1, -1), repeat=3):
            character = sign_text(signs)
            lower_character = normal.character_part(lower_space, generators, signs)
            upper_character = normal.character_part(upper_space, generators, signs)
            multiplicity = upper_character.rows - lower_character.rows
            if multiplicity == 0:
                continue

            atom_basis = sp.Matrix.vstack(*atom_vectors[signs])
            to_atom_coordinates = normal.coordinate_map(atom_basis)
            lower_coordinates = normal.canonical_rowspace(to_atom_coordinates(lower_character))
            upper_coordinates = normal.canonical_rowspace(to_atom_coordinates(upper_character))
            reduced = reduced_matrices[signs]

            direct_kernel_ok = reduced * upper_coordinates.T == sp.zeros(reduced.rows, upper_coordinates.rows)
            all_direct_kernel_containment &= direct_kernel_ok

            selected, support_profile = normal.exhaustive_minimum_quotient_basis(
                upper_coordinates,
                lower_coordinates,
            )
            expected_profile = expected_profiles[(layer_id, character)]
            profile_match = tuple(support_profile) == tuple(expected_profile)
            all_profiles_match &= profile_match

            reconstructed = normal.rowspace_sum(lower_coordinates, *selected)
            reconstruction_ok = reconstructed.rows == upper_coordinates.rows
            all_quotients_reconstructed &= reconstruction_ok

            quotient_rows.append({
                "layer_id": layer_id,
                "quotient": quotient_name,
                "character": character,
                "lower_character_dimension": lower_coordinates.rows,
                "upper_character_dimension": upper_coordinates.rows,
                "quotient_character_multiplicity": multiplicity,
                "direct_reduced_KK_kernel_containment": direct_kernel_ok,
                "minimum_atom_support_profile": ";".join(map(str, support_profile)),
                "expected_profile": ";".join(map(str, expected_profile)),
                "profile_match": profile_match,
                "exact_quotient_reconstruction": reconstruction_ok,
            })

            for direction_index, coefficient_row in enumerate(selected, start=1):
                direction_id = f"{layer_id}_{character}_d{direction_index}"
                ambient_relation = normal.primitive_integer_row(coefficient_row * atom_basis)
                direct_residual = reduced * coefficient_row.T
                direct_zero = direct_residual == sp.zeros(reduced.rows, 1)
                all_coordinate_cancellations &= direct_zero

                support_count = sum(value != 0 for value in coefficient_row)
                total_atom_count += support_count
                direction_count += 1

                direction_rows.append({
                    "direction_id": direction_id,
                    "layer_id": layer_id,
                    "quotient": quotient_name,
                    "character": character,
                    "direction_index": direction_index,
                    "atom_support_count": support_count,
                    "expected_atom_support": expected_profile[direction_index - 1],
                    "support_match": support_count == expected_profile[direction_index - 1],
                    "direct_KK_zero": direct_zero,
                    "active_KK_coordinates_before_cancellation": sum(
                        any(coefficient_row[0, column] * reduced[row, column] != 0 for column in range(reduced.cols))
                        for row in range(reduced.rows)
                    ),
                    "atom_expression": normal.atom_expression(coefficient_row, atom_ids[signs]),
                    "expanded_PT_support": sum(value != 0 for value in ambient_relation),
                    "expanded_relation_text": normal.expanded_relation_text(ambient_relation, reference_states),
                })

                for atom_position, coefficient in enumerate(list(coefficient_row)):
                    value = int(coefficient)
                    if value == 0:
                        continue
                    atom_coefficient_rows.append({
                        "direction_id": direction_id,
                        "layer_id": layer_id,
                        "character": character,
                        "direction_index": direction_index,
                        "atom_id": atom_ids[signs][atom_position],
                        "atom_coefficient": value,
                    })

                for state_index, coefficient in enumerate(list(ambient_relation)):
                    value = int(coefficient)
                    if value == 0:
                        continue
                    expanded_rows.append({
                        "direction_id": direction_id,
                        "target_state_index": state_index,
                        "target_cycle": cycle_text(reference_states[state_index]),
                        "coefficient": value,
                    })

                for kk_row in range(reduced.rows):
                    contributions = []
                    total = 0
                    for atom_position in range(reduced.cols):
                        atom_coefficient = int(coefficient_row[0, atom_position])
                        matrix_value = int(reduced[kk_row, atom_position])
                        product = atom_coefficient * matrix_value
                        if product == 0:
                            continue
                        contributions.append(
                            f"{atom_ids[signs][atom_position]}:{atom_coefficient}*{matrix_value}={product}"
                        )
                        total += product
                    if not contributions:
                        continue
                    cancellation_rows.append({
                        "direction_id": direction_id,
                        "layer_id": layer_id,
                        "character": character,
                        "kk_row_index": kk_row,
                        "kk_basis_ordering": "1," + cycle_text(kk8_permutations[kk_row]) + ",8",
                        "contributions": ";".join(contributions),
                        "net_coefficient": total,
                        "exact_zero": total == 0,
                    })
                    all_coordinate_cancellations &= total == 0

            print(
                f"  {layer_id:3s} chi={character} mult={multiplicity} "
                f"profile={support_profile} direct_KK={direct_kernel_ok}"
            )

    write_csv(out_dir / "direct_quotient_character_derivation.csv", quotient_rows)
    write_csv(out_dir / "direct_signed_orbit_normal_form.csv", direction_rows)
    write_csv(out_dir / "direct_signed_orbit_atom_coefficients.csv", atom_coefficient_rows)
    write_csv(out_dir / "direct_signed_orbit_expanded_coefficients.csv", expanded_rows)
    write_csv(out_dir / "kk_coordinate_cancellation_certificate.csv", cancellation_rows)
    write_derivation_markdown(
        out_dir / "direct_kk_shuffle_derivation.md",
        character_rows,
        direction_rows,
    )

    expected_orbit_distribution = {4: 2, 8: 8}
    expected_atom_count = 79
    expected_direction_count = 15
    all_character_nullities = all(bool(row["nullity_match"]) for row in character_rows)
    exact_certificate = (
        dict(sorted(orbit_distribution.items())) == expected_orbit_distribution
        and q8_relation_basis.rows == 15
        and dimensions_match
        and all(lattice_checks.values())
        and all_character_nullities
        and all_direct_kernel_containment
        and all_profiles_match
        and all_quotients_reconstructed
        and all_coordinate_cancellations
        and total_atom_count == expected_atom_count
        and direction_count == expected_direction_count
    )

    verdict = (
        "EHF_AMP_FOUND_03F_DIRECT_KK_SHUFFLE_SIGNED_ORBIT_DERIVATION_PROVED"
        if exact_certificate
        else "EHF_AMP_FOUND_03F_DIRECT_KK_SHUFFLE_DERIVATION_FAILED"
    )

    certificate = {
        "theorem": (
            "The fifteen minimum-support signed-orbit quotient directions are "
            "reconstructed directly from the exact character-reduced KK "
            "shuffle matrices M_chi=Q8 A_chi^T, independently of all 03C-03E "
            "output files."
        ),
        "direct_kernel_identity": "M_chi c^T = 0",
        "inputs_used": {
            "03C_output_files": False,
            "03D_output_files": False,
            "03E_output_files": False,
            "exact_n8_KK_shuffle_matrix": True,
            "exact_n9_source_KK_and_delete_maps": True,
        },
        "state_orbit_distribution": dict(sorted(orbit_distribution.items())),
        "character_kernel_nullities": {
            row["character"]: row["relation_nullity"] for row in character_rows
        },
        "tail_lattice_dimensions": {name: spaces[name].rows for name in expected_dimensions},
        "quotient_character_direction_count": direction_count,
        "total_minimum_atom_count": total_atom_count,
        "checks": {
            "direct_Q8_relation_dimension_15": q8_relation_basis.rows == 15,
            "tail_lattice_reconstructed_directly": dimensions_match and all(lattice_checks.values()),
            "character_kernel_nullities_match": all_character_nullities,
            "all_tail_spaces_contained_in_direct_KK_kernels": all_direct_kernel_containment,
            "minimum_support_profiles_match": all_profiles_match,
            "all_quotient_characters_reconstructed": all_quotients_reconstructed,
            "all_720_coordinate_cancellations_exact": all_coordinate_cancellations,
            "direction_count_15": direction_count == expected_direction_count,
            "atom_count_79": total_atom_count == expected_atom_count,
        },
        "interpretation": (
            "The 03E normal forms are not artefacts of the seven 03D seeds. "
            "They are exact kernel vectors of finite character-reduced KK "
            "shuffle matrices. Each vanishing relation has a coordinate-level "
            "cancellation certificate in the standard 720-dimensional n=8 KK basis."
        ),
        "claim_boundary": (
            "This is a direct exact matrix derivation from KK shuffles. It does "
            "not yet replace the kernel computation by a short parameterised "
            "human proof, establish anchor independence, or generalise to higher n."
        ),
    }
    with (out_dir / "direct_kk_shuffle_certificate.json").open("w") as handle:
        json.dump(json_safe(certificate), handle, indent=2)

    elapsed = time.time() - started
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "03C_03D_03E_output_files_used": False,
        "direct_Q8_relation_dimension": q8_relation_basis.rows,
        "state_orbit_distribution": dict(sorted(orbit_distribution.items())),
        "character_kernel_nullities_exact": all_character_nullities,
        "tail_lattice_reconstructed_directly": dimensions_match and all(lattice_checks.values()),
        "quotient_character_direction_count": direction_count,
        "total_minimum_signed_orbit_atom_count": total_atom_count,
        "all_minimum_support_profiles_match": all_profiles_match,
        "all_coordinate_level_KK_cancellations_exact": all_coordinate_cancellations,
        "direct_KK_shuffle_derivation_certificate": exact_certificate,
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "direct_kk_shuffle_certificate.json",
            "character_reduced_kk_summary.csv",
            "character_reduced_kk_sparse_entries.csv",
            "direct_quotient_character_derivation.csv",
            "direct_signed_orbit_normal_form.csv",
            "direct_signed_orbit_atom_coefficients.csv",
            "direct_signed_orbit_expanded_coefficients.csv",
            "kk_coordinate_cancellation_certificate.csv",
            "direct_kk_shuffle_derivation.md",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)
    with (out_dir / "verdict.json").open("w") as handle:
        json.dump({
            "verdict": verdict,
            "direct_KK_shuffle_derivation_certificate": exact_certificate,
            "direction_count": direction_count,
            "total_atom_count": total_atom_count,
        }, handle, indent=2)

    strict_failures: List[str] = []
    if args.strict:
        checks = {
            "no_prior_output_files": True,
            "state_orbits": dict(sorted(orbit_distribution.items())) == expected_orbit_distribution,
            "Q8_relation_dimension": q8_relation_basis.rows == 15,
            "direct_tail_lattice": dimensions_match and all(lattice_checks.values()),
            "character_kernel_nullities": all_character_nullities,
            "direct_kernel_containment": all_direct_kernel_containment,
            "minimum_support_profiles": all_profiles_match,
            "quotient_reconstruction": all_quotients_reconstructed,
            "coordinate_cancellations": all_coordinate_cancellations,
            "fifteen_directions": direction_count == expected_direction_count,
            "seventy_nine_atoms": total_atom_count == expected_atom_count,
        }
        strict_failures = [name for name, passed in checks.items() if not passed]

    print("\n" + "=" * 124)
    print("FINAL SUMMARY")
    print("=" * 124)
    print(f"Prior 03C/03D/03E outputs used:       False")
    print(f"Direct Q8 relation dimension:         {q8_relation_basis.rows}")
    print(f"Character KK nullities exact:         {all_character_nullities}")
    print(f"Tail lattice reconstructed directly:  {dimensions_match and all(lattice_checks.values())}")
    print(f"Quotient-character directions:        {direction_count}")
    print(f"All minimum support profiles:         {all_profiles_match}")
    print(f"All KK coordinate cancellations:      {all_coordinate_cancellations}")
    print(f"Total minimum signed-orbit atoms:      {total_atom_count}")
    print(f"Verdict:                              {verdict}")
    print(f"elapsed:                              {elapsed:.2f} seconds")
    print(f"summary:                              {out_dir / 'summary.json'}")
    if args.strict:
        print(f"strict checks:                        {'PASS' if not strict_failures else 'FAIL'}")
        if strict_failures:
            print(f"failed checks:                        {', '.join(strict_failures)}")
    print("=" * 124)

    if strict_failures:
        raise SystemExit(2)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Derive the exact 9->8 signed-orbit normal forms directly from "
            "character-reduced Kleiss--Kuijf shuffle matrices."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--helper-script", required=True)
    parser.add_argument("--rank-script", required=True)
    parser.add_argument("--direct-script", required=True)
    parser.add_argument("--normal-form-script", required=True)
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
