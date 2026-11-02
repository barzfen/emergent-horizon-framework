#!/usr/bin/env python3
"""
EHF-AMP-FOUND-03E: Exact Signed-Orbit Normal Form
=================================================

03D gave a minimal seven-seed filtration-adapted presentation of the exact
9 -> 8 target relation lattice under

    G = <(2 3),(5 6),(7 8)> ~= C2^3.

The seven seeds are constructive but expand into long Parke--Taylor sums.
03E separates symmetry from coefficient data.

For a joint sign character chi of G and a target ordering w, define the
primitive signed-orbit atom

    Omega_chi(w)
      = prim( sum_{g in G} chi(g) e_{can(g.w)} ).

Each atom has support on one G-orbit of target orderings. The script proves
an exact normal form for every successive quotient-character direction in

    L2  = V2/V0,
    L3  = V3/V2,
    L8  = V8/V3,
    L9  = V9/V3,
    L15 = V15/V14.

The target coefficient space has exactly ten G-orbits: eight of size 8 and
two of size 4. Every quotient direction is represented by a minimum-support
integer combination of signed-orbit atoms. Minimum support is certified by
exhaustive subset search in the relevant character-orbit coordinate space.

Expected minimum atom-support profile
-------------------------------------

    L2:
      +-+ : 5
      --- : 6

    L3:
      +-- : 6

    L8:
      -++ : 3
      -+- : 5
      --+ : 4,5
      --- : 4

    L9:
      ++- : 5
      +-- : 4,5
      -+- : 8
      --+ : 8
      --- : 6

    L15:
      -+- : 5

The 15 quotient-character directions therefore admit an exact normal form
using 79 signed-orbit atoms in total.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --seed-coefficients runs/ehf_amp_found_03d/sparse_seed_coefficients.csv \
  --out-dir runs/ehf_amp_found_03e \
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
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import sympy as sp

Cycle = Tuple[int, ...]
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


def cycle_text(cycle: Sequence[int]) -> str:
    return ",".join(map(str, cycle))


def sign_text(signs: SignTriple) -> str:
    return "".join("+" if sign == 1 else "-" for sign in signs)


def parse_signs(text: str) -> SignTriple:
    if len(text) != 3 or any(character not in "+-" for character in text):
        raise ValueError(text)
    return tuple(1 if character == "+" else -1 for character in text)  # type: ignore[return-value]


def canonical_rowspace(matrix: sp.MatrixBase) -> sp.Matrix:
    matrix = sp.Matrix(matrix)
    if matrix.rows == 0:
        return sp.zeros(0, matrix.cols)
    rref, _ = matrix.rref()
    rows = [
        list(rref.row(index))
        for index in range(rref.rows)
        if any(rref[index, column] != 0 for column in range(rref.cols))
    ]
    return sp.Matrix(rows) if rows else sp.zeros(0, matrix.cols)


def rowspace_sum(*spaces: sp.Matrix) -> sp.Matrix:
    nonempty = [space for space in spaces if space.rows]
    if not nonempty:
        columns = spaces[0].cols if spaces else 0
        return sp.zeros(0, columns)
    return canonical_rowspace(sp.Matrix.vstack(*nonempty))


def is_subspace(left: sp.Matrix, right: sp.Matrix) -> bool:
    return rowspace_sum(left, right).rows == right.rows


def primitive_integer_row(row: sp.MatrixBase) -> sp.Matrix:
    values = [sp.Rational(value) for value in list(row)]
    if not any(values):
        return sp.zeros(1, len(values))
    denominator_lcm = 1
    for value in values:
        denominator_lcm = sp.ilcm(denominator_lcm, int(value.q))
    integers = [int(value * denominator_lcm) for value in values]
    gcd_value = 0
    for value in integers:
        gcd_value = math.gcd(gcd_value, abs(value))
    if gcd_value:
        integers = [value // gcd_value for value in integers]
    first_nonzero = next(value for value in integers if value)
    if first_nonzero < 0:
        integers = [-value for value in integers]
    return sp.Matrix(1, len(integers), integers)


def row_key(row: sp.MatrixBase) -> Tuple[int, ...]:
    return tuple(int(value) for value in primitive_integer_row(row))


def coordinate_map(basis: sp.Matrix):
    _, pivots = basis.rref()
    pivot_columns = list(pivots)
    pivot_matrix = basis[:, pivot_columns]
    inverse = pivot_matrix.inv()

    def coordinates(rows: sp.MatrixBase) -> sp.Matrix:
        matrix = sp.Matrix(rows)
        result = matrix[:, pivot_columns] * inverse
        if result * basis != matrix:
            raise RuntimeError("Vector is not contained in the requested basis span")
        return result

    return coordinates


def target_action_destination(
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


def permutation_matrix(destination: Sequence[int]) -> sp.Matrix:
    size = len(destination)
    matrix = sp.zeros(size)
    for source, target in enumerate(destination):
        matrix[target, source] = 1
    return matrix


def orbit_span(
    vectors: Sequence[sp.Matrix],
    group_matrices: Sequence[sp.Matrix],
) -> sp.Matrix:
    rows: List[List[sp.Expr]] = []
    for vector in vectors:
        for group_matrix in group_matrices:
            rows.append(list(vector * group_matrix.T))
    return canonical_rowspace(sp.Matrix(rows))


def character_projector(
    generators: Sequence[sp.Matrix],
    signs: SignTriple,
) -> sp.Matrix:
    identity = sp.eye(generators[0].rows)
    projector = identity
    for sign, generator in zip(signs, generators):
        projector = projector * (identity + sign * generator) / 2
    return projector


def character_part(
    subspace: sp.Matrix,
    generators: Sequence[sp.Matrix],
    signs: SignTriple,
) -> sp.Matrix:
    if subspace.rows == 0:
        return sp.zeros(0, generators[0].rows)
    projector = character_projector(generators, signs)
    return canonical_rowspace(subspace * projector.T)


def state_orbits(
    state_count: int,
    destinations: Sequence[Sequence[int]],
) -> List[List[int]]:
    unseen = set(range(state_count))
    output: List[List[int]] = []
    while unseen:
        representative = min(unseen)
        orbit = sorted({destination[representative] for destination in destinations})
        output.append(orbit)
        unseen -= set(orbit)
    return output


def signed_orbit_atom(
    representative: int,
    signs: SignTriple,
    group_powers: Sequence[Tuple[int, int, int]],
    destinations: Sequence[Sequence[int]],
    state_count: int,
) -> sp.Matrix:
    vector = sp.zeros(1, state_count)
    for powers, destination in zip(group_powers, destinations):
        character = 1
        for sign, power in zip(signs, powers):
            if power:
                character *= sign
        vector[0, destination[representative]] += character
    if not any(value != 0 for value in vector):
        return sp.zeros(1, state_count)
    return primitive_integer_row(vector)


def read_seed_vectors(
    path: Path,
    states: Sequence[Cycle],
) -> Dict[str, sp.Matrix]:
    state_index = {cycle: index for index, cycle in enumerate(states)}
    vectors: Dict[str, sp.Matrix] = {}
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            seed_id = row["seed_id"]
            cycle = tuple(map(int, row["target_cycle"].split(",")))
            supplied_index = int(row["target_state_index"])
            if cycle not in state_index:
                raise RuntimeError(f"Seed cycle is not in reference fibre: {cycle}")
            actual_index = state_index[cycle]
            if supplied_index != actual_index:
                raise RuntimeError(
                    f"Target index mismatch for {cycle}: "
                    f"{supplied_index} != {actual_index}"
                )
            if seed_id not in vectors:
                vectors[seed_id] = sp.zeros(1, len(states))
            vectors[seed_id][0, actual_index] = int(row["coefficient"])
    return vectors


def supported_subspace(subspace: sp.Matrix, support: Sequence[int]) -> sp.Matrix:
    support_set = set(support)
    outside = [
        column
        for column in range(subspace.cols)
        if column not in support_set
    ]
    if not outside:
        return subspace
    constraints = subspace[:, outside].T
    nullspace = constraints.nullspace()
    if not nullspace:
        return sp.zeros(0, subspace.cols)
    rows = [
        list(vector.T * subspace)
        for vector in nullspace
    ]
    return canonical_rowspace(sp.Matrix(rows))


def quotient_dimension(candidate: sp.Matrix, lower: sp.Matrix) -> int:
    if candidate.rows == 0:
        return 0
    return rowspace_sum(lower, candidate).rows - lower.rows


def candidate_vectors_from_subspace(
    subspace: sp.Matrix,
    lower: sp.Matrix,
) -> List[sp.Matrix]:
    if subspace.rows == 0:
        return []
    primitive_rows = [
        primitive_integer_row(subspace.row(index))
        for index in range(subspace.rows)
    ]
    candidates: Dict[Tuple[int, ...], sp.Matrix] = {}

    coefficient_values = (-2, -1, 0, 1, 2)
    for coefficients in itertools.product(
        coefficient_values,
        repeat=len(primitive_rows),
    ):
        if not any(coefficients):
            continue
        row = sp.zeros(1, subspace.cols)
        for coefficient, basis_row in zip(coefficients, primitive_rows):
            if coefficient:
                row += coefficient * basis_row
        row = primitive_integer_row(row)
        if rowspace_sum(lower, row).rows == lower.rows:
            continue
        candidates[row_key(row)] = row

    return sorted(
        candidates.values(),
        key=lambda row: (
            sum(value != 0 for value in row),
            sum(abs(int(value)) for value in row),
            max(abs(int(value)) for value in row),
            row_key(row),
        ),
    )


def exhaustive_minimum_quotient_basis(
    upper: sp.Matrix,
    lower: sp.Matrix,
) -> Tuple[List[sp.Matrix], Tuple[int, ...]]:
    """
    Find a quotient basis with lexicographically minimum sorted support profile.

    The coordinate ambient dimension is at most ten, so every support subset
    can be audited exactly.
    """
    quotient_dim = upper.rows - lower.rows
    if quotient_dim <= 0:
        return [], ()

    candidates: Dict[Tuple[int, ...], sp.Matrix] = {}
    minimum_nonzero_support = None

    for support_size in range(1, upper.cols + 1):
        for support in itertools.combinations(range(upper.cols), support_size):
            constrained = supported_subspace(upper, support)
            if quotient_dimension(constrained, lower) == 0:
                continue
            for candidate in candidate_vectors_from_subspace(constrained, lower):
                candidates[row_key(candidate)] = candidate
        if candidates and minimum_nonzero_support is None:
            minimum_nonzero_support = support_size

    ordered = sorted(
        candidates.values(),
        key=lambda row: (
            sum(value != 0 for value in row),
            sum(abs(int(value)) for value in row),
            max(abs(int(value)) for value in row),
            row_key(row),
        ),
    )

    if quotient_dim == 1:
        selected = [ordered[0]]
        return selected, (
            sum(value != 0 for value in selected[0]),
        )

    if quotient_dim != 2:
        raise RuntimeError(
            f"03E expects quotient character multiplicity at most two, got {quotient_dim}"
        )

    best = None
    best_key = None
    for left_index, left in enumerate(ordered):
        left_space = rowspace_sum(lower, left)
        if left_space.rows != lower.rows + 1:
            continue
        for right in ordered[left_index + 1 :]:
            if rowspace_sum(lower, left, right).rows != lower.rows + 2:
                continue
            supports = sorted(
                (
                    sum(value != 0 for value in left),
                    sum(value != 0 for value in right),
                )
            )
            key = (
                tuple(supports),
                sum(abs(int(value)) for value in left)
                + sum(abs(int(value)) for value in right),
                row_key(left),
                row_key(right),
            )
            if best_key is None or key < best_key:
                best_key = key
                best = [left, right]

    if best is None or best_key is None:
        raise RuntimeError("Unable to find an exact two-direction quotient basis")
    return best, best_key[0]


def atom_expression(
    coefficients: sp.Matrix,
    atom_ids: Sequence[str],
) -> str:
    terms: List[str] = []
    for coefficient, atom_id in zip(list(coefficients), atom_ids):
        value = int(coefficient)
        if not value:
            continue
        if value == 1:
            terms.append(f"+ {atom_id}")
        elif value == -1:
            terms.append(f"- {atom_id}")
        elif value > 0:
            terms.append(f"+ {value} {atom_id}")
        else:
            terms.append(f"- {abs(value)} {atom_id}")
    if not terms:
        return "0"
    text = " ".join(terms)
    return text[2:] if text.startswith("+ ") else text


def expanded_relation_text(
    vector: sp.Matrix,
    states: Sequence[Cycle],
) -> str:
    terms: List[str] = []
    for index, coefficient in enumerate(list(vector)):
        value = int(coefficient)
        if not value:
            continue
        terms.append(
            f"{value:+d} * PT({cycle_text(states[index])})"
        )
    return " ".join(terms)


def write_markdown(
    path: Path,
    orbit_distribution: Mapping[int, int],
    normal_rows: Sequence[Mapping[str, object]],
    total_atom_count: int,
) -> None:
    lines = [
        "# EHF-AMP-FOUND-03E",
        "## Exact signed-orbit normal form",
        "",
        "Let",
        "",
        r"\[G=\langle(2\,3),(5\,6),(7\,8)\rangle\cong C_2^3.\]",
        "",
        r"For a joint sign character \(\chi\) and reference ordering \(w\), define",
        "",
        r"\[\Omega_\chi(w)=\operatorname{prim}\!\left("
        r"\sum_{g\in G}\chi(g)e_{\operatorname{can}(g\cdot w)}\right).\]",
        "",
        f"The 72 target orderings split into `{dict(sorted(orbit_distribution.items()))}` "
        "state orbits by orbit size.",
        "",
        "Each row below is an exact Parke--Taylor relation and represents one "
        "successive quotient-character direction.",
        "",
        "| Layer | Character | Direction | Minimum atoms | Signed-orbit normal form |",
        "|---|---|---:|---:|---|",
    ]
    for row in normal_rows:
        lines.append(
            f"| {row['layer_id']} | `{row['character']}` | "
            f"{row['direction_index']} | {row['atom_support_count']} | "
            f"`{row['atom_expression']}` |"
        )
    lines.extend([
        "",
        "## Exact compression result",
        "",
        f"The fifteen quotient-character directions use **{total_atom_count}** "
        "signed-orbit atoms in total. Every support number in the table is "
        "minimum within the corresponding quotient character sector; the two "
        "multiplicity-two sectors have lexicographically minimum support "
        "profiles `(4,5)`.",
        "",
        "This is a symmetry-separated normal form. It is not yet a derivation "
        "from a closed family of KK shuffle identities.",
        "",
    ])
    path.write_text("\n".join(lines))


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    seed_path = Path(args.seed_coefficients).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_03e_base")
    reference_key = ((1, 2, 3, 4), (5, 6, 7, 8))
    states: List[Cycle] = base.fibres(8)[reference_key]
    if len(states) != 72:
        raise RuntimeError("Expected 72 states in the reference target fibre")

    print("=" * 124)
    print("EHF-AMP-FOUND-03E: EXACT SIGNED-ORBIT NORMAL FORM")
    print("=" * 124)
    print(f"base script:                 {base_script}")
    print(f"03D seed coefficients:       {seed_path}")
    print(f"output directory:            {out_dir}")
    print("reference target fibre:      A={2,3,4}")
    print("symmetry group:              C2^3")
    print("coefficient domain:          QQ")

    generator_specs = [
        ("g1=(2 3)", {2: 3, 3: 2}),
        ("g2=(5 6)", {5: 6, 6: 5}),
        ("g3=(7 8)", {7: 8, 8: 7}),
    ]
    generators: List[sp.Matrix] = []
    generator_destinations: List[List[int]] = []
    for _, mapping in generator_specs:
        destination = target_action_destination(base, states, mapping)
        generator_destinations.append(destination)
        generators.append(permutation_matrix(destination))

    group_powers = list(itertools.product((0, 1), repeat=3))
    group_matrices: List[sp.Matrix] = []
    group_destinations: List[List[int]] = []
    identity = sp.eye(len(states))
    for powers in group_powers:
        matrix = identity
        for power, generator in zip(powers, generators):
            if power:
                matrix = matrix * generator
        group_matrices.append(matrix)
        destination = [
            next(
                row
                for row in range(len(states))
                if matrix[row, column] == 1
            )
            for column in range(len(states))
        ]
        group_destinations.append(destination)

    commuting_involutions = all(
        generator * generator == identity
        for generator in generators
    ) and all(
        generators[left] * generators[right]
        == generators[right] * generators[left]
        for left in range(3)
        for right in range(left + 1, 3)
    )

    orbits = state_orbits(len(states), group_destinations)
    orbit_distribution = Counter(len(orbit) for orbit in orbits)

    seed_vectors = read_seed_vectors(seed_path, states)
    required_seeds = {
        "L2_seed_1",
        "L3_seed_1",
        "L8_seed_1",
        "L8_seed_2",
        "L9_seed_1",
        "L9_seed_2",
        "L15_seed_1",
    }
    if set(seed_vectors) != required_seeds:
        raise RuntimeError(
            f"Unexpected 03D seed set: {sorted(seed_vectors)}"
        )

    seed_orbits = {
        seed_id: orbit_span([vector], group_matrices)
        for seed_id, vector in seed_vectors.items()
    }

    spaces: Dict[str, sp.Matrix] = {}
    spaces["V0"] = sp.zeros(0, len(states))
    spaces["V2"] = seed_orbits["L2_seed_1"]
    spaces["V3"] = rowspace_sum(
        spaces["V2"],
        seed_orbits["L3_seed_1"],
    )
    spaces["V8"] = rowspace_sum(
        spaces["V3"],
        seed_orbits["L8_seed_1"],
        seed_orbits["L8_seed_2"],
    )
    spaces["V9"] = rowspace_sum(
        spaces["V3"],
        seed_orbits["L9_seed_1"],
        seed_orbits["L9_seed_2"],
    )
    spaces["V14"] = rowspace_sum(spaces["V8"], spaces["V9"])
    spaces["V15"] = rowspace_sum(
        spaces["V14"],
        seed_orbits["L15_seed_1"],
    )

    expected_space_dimensions = {
        "V0": 0,
        "V2": 2,
        "V3": 3,
        "V8": 8,
        "V9": 9,
        "V14": 14,
        "V15": 15,
    }
    space_dimensions_match = all(
        spaces[name].rows == dimension
        for name, dimension in expected_space_dimensions.items()
    )
    lattice_checks = {
        "V2_subset_V3": is_subspace(spaces["V2"], spaces["V3"]),
        "V3_subset_V8": is_subspace(spaces["V3"], spaces["V8"]),
        "V3_subset_V9": is_subspace(spaces["V3"], spaces["V9"]),
        "V14_equals_V8_plus_V9": (
            spaces["V14"] == rowspace_sum(spaces["V8"], spaces["V9"])
        ),
        "V15_dimension_15": spaces["V15"].rows == 15,
    }

    atom_catalog_rows: List[Dict[str, object]] = []
    atom_vectors: Dict[SignTriple, List[sp.Matrix]] = {}
    atom_ids: Dict[SignTriple, List[str]] = {}

    for signs in itertools.product((1, -1), repeat=3):
        vectors: List[sp.Matrix] = []
        identifiers: List[str] = []
        for orbit_index, orbit in enumerate(orbits, start=1):
            representative = min(orbit)
            atom = signed_orbit_atom(
                representative,
                signs,
                group_powers,
                group_destinations,
                len(states),
            )
            if not any(value != 0 for value in atom):
                continue
            atom_id = f"Omega_{sign_text(signs)}_O{orbit_index:02d}"
            vectors.append(atom)
            identifiers.append(atom_id)
            support = [
                index
                for index, value in enumerate(list(atom))
                if value != 0
            ]
            atom_catalog_rows.append({
                "atom_id": atom_id,
                "character": sign_text(signs),
                "orbit_id": f"O{orbit_index:02d}",
                "orbit_size": len(orbit),
                "representative_state_index": representative,
                "representative_cycle": cycle_text(states[representative]),
                "atom_support_size": len(support),
                "atom_coefficient_values": ";".join(
                    map(
                        str,
                        sorted(
                            {
                                int(atom[0, index])
                                for index in support
                            }
                        ),
                    )
                ),
                "expanded_state_indices": ";".join(map(str, support)),
            })
        basis = sp.Matrix.vstack(*vectors)
        if canonical_rowspace(basis).rows != len(vectors):
            raise RuntimeError(
                f"Signed-orbit atoms are not independent for {sign_text(signs)}"
            )
        atom_vectors[signs] = vectors
        atom_ids[signs] = identifiers

    write_csv(out_dir / "signed_orbit_atom_catalog.csv", atom_catalog_rows)

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

    normal_rows: List[Dict[str, object]] = []
    normal_atom_rows: List[Dict[str, object]] = []
    expanded_rows: List[Dict[str, object]] = []
    character_summary_rows: List[Dict[str, object]] = []

    all_profiles_match = True
    all_quotients_reconstructed = True
    total_atom_count = 0
    total_direction_count = 0

    for layer_id, quotient_name, lower_name, upper_name in layers:
        lower_space = spaces[lower_name]
        upper_space = spaces[upper_name]

        for signs in itertools.product((1, -1), repeat=3):
            lower_character = character_part(lower_space, generators, signs)
            upper_character = character_part(upper_space, generators, signs)
            quotient_multiplicity = (
                upper_character.rows - lower_character.rows
            )
            if quotient_multiplicity == 0:
                continue

            atom_basis = sp.Matrix.vstack(*atom_vectors[signs])
            to_atom_coordinates = coordinate_map(atom_basis)
            lower_coordinates = canonical_rowspace(
                to_atom_coordinates(lower_character)
            )
            upper_coordinates = canonical_rowspace(
                to_atom_coordinates(upper_character)
            )

            selected, support_profile = exhaustive_minimum_quotient_basis(
                upper_coordinates,
                lower_coordinates,
            )
            expected_profile = expected_profiles[
                (layer_id, sign_text(signs))
            ]
            profile_match = tuple(support_profile) == tuple(expected_profile)
            all_profiles_match &= profile_match

            reconstructed = rowspace_sum(
                lower_coordinates,
                *selected,
            )
            reconstruction_ok = (
                reconstructed.rows == upper_coordinates.rows
            )
            all_quotients_reconstructed &= reconstruction_ok

            character_summary_rows.append({
                "layer_id": layer_id,
                "quotient": quotient_name,
                "character": sign_text(signs),
                "lower_character_dimension": lower_coordinates.rows,
                "upper_character_dimension": upper_coordinates.rows,
                "quotient_character_multiplicity": quotient_multiplicity,
                "minimum_atom_support_profile": ";".join(
                    map(str, support_profile)
                ),
                "expected_profile": ";".join(map(str, expected_profile)),
                "profile_match": profile_match,
                "exact_quotient_reconstruction": reconstruction_ok,
            })

            for direction_index, coordinate_row in enumerate(selected, start=1):
                ambient_relation = coordinate_row * atom_basis
                ambient_relation = primitive_integer_row(ambient_relation)
                support_count = sum(
                    value != 0
                    for value in coordinate_row
                )
                total_atom_count += support_count
                total_direction_count += 1

                direction_id = (
                    f"{layer_id}_{sign_text(signs)}_d{direction_index}"
                )
                expression = atom_expression(
                    coordinate_row,
                    atom_ids[signs],
                )
                expanded_support = sum(
                    value != 0
                    for value in ambient_relation
                )
                expanded_l1 = sum(
                    abs(int(value))
                    for value in ambient_relation
                )

                normal_rows.append({
                    "direction_id": direction_id,
                    "layer_id": layer_id,
                    "quotient": quotient_name,
                    "character": sign_text(signs),
                    "direction_index": direction_index,
                    "quotient_character_multiplicity": quotient_multiplicity,
                    "atom_support_count": support_count,
                    "minimum_support_proved": True,
                    "expected_atom_support": expected_profile[
                        direction_index - 1
                    ],
                    "support_match": (
                        support_count
                        == expected_profile[direction_index - 1]
                    ),
                    "atom_coefficient_l1_norm": sum(
                        abs(int(value))
                        for value in coordinate_row
                    ),
                    "expanded_PT_support": expanded_support,
                    "expanded_coefficient_l1_norm": expanded_l1,
                    "atom_expression": expression,
                    "expanded_relation_text": expanded_relation_text(
                        ambient_relation,
                        states,
                    ),
                })

                for atom_position, coefficient in enumerate(
                    list(coordinate_row)
                ):
                    value = int(coefficient)
                    if not value:
                        continue
                    normal_atom_rows.append({
                        "direction_id": direction_id,
                        "layer_id": layer_id,
                        "character": sign_text(signs),
                        "direction_index": direction_index,
                        "atom_id": atom_ids[signs][atom_position],
                        "atom_coefficient": value,
                    })

                for state_index, coefficient in enumerate(
                    list(ambient_relation)
                ):
                    value = int(coefficient)
                    if not value:
                        continue
                    expanded_rows.append({
                        "direction_id": direction_id,
                        "layer_id": layer_id,
                        "character": sign_text(signs),
                        "direction_index": direction_index,
                        "target_state_index": state_index,
                        "target_cycle": cycle_text(states[state_index]),
                        "coefficient": value,
                    })

            print(
                f"  {layer_id:3s} chi={sign_text(signs)} "
                f"mult={quotient_multiplicity} "
                f"minimum atoms={support_profile} "
                f"reconstruct={reconstruction_ok}"
            )

    write_csv(
        out_dir / "quotient_character_normal_form_summary.csv",
        character_summary_rows,
    )
    write_csv(
        out_dir / "signed_orbit_normal_form.csv",
        normal_rows,
    )
    write_csv(
        out_dir / "signed_orbit_normal_form_atom_coefficients.csv",
        normal_atom_rows,
    )
    write_csv(
        out_dir / "signed_orbit_normal_form_expanded_coefficients.csv",
        expanded_rows,
    )
    write_markdown(
        out_dir / "signed_orbit_normal_form.md",
        orbit_distribution,
        normal_rows,
        total_atom_count,
    )

    expected_orbit_distribution = {4: 2, 8: 8}
    orbit_distribution_match = (
        dict(sorted(orbit_distribution.items()))
        == expected_orbit_distribution
    )
    expected_total_atom_count = 79
    expected_direction_count = 15

    exact_certificate = (
        commuting_involutions
        and orbit_distribution_match
        and space_dimensions_match
        and all(lattice_checks.values())
        and all_profiles_match
        and all_quotients_reconstructed
        and total_atom_count == expected_total_atom_count
        and total_direction_count == expected_direction_count
    )

    verdict = (
        "EHF_AMP_FOUND_03E_EXACT_MINIMUM_SIGNED_ORBIT_NORMAL_FORM_PROVED"
        if exact_certificate
        else "EHF_AMP_FOUND_03E_SIGNED_ORBIT_NORMAL_FORM_FAILED"
    )

    certificate = {
        "theorem": (
            "Every successive quotient-character direction in the exact "
            "9->8 target tail-filtration lattice has a minimum-support normal "
            "form as an integer combination of primitive C2^3 signed-orbit "
            "atoms."
        ),
        "signed_orbit_atom": (
            "Omega_chi(w)=prim(sum_{g in C2^3} chi(g) "
            "e_{can(g.w)})"
        ),
        "state_orbit_distribution": dict(
            sorted(orbit_distribution.items())
        ),
        "quotient_direction_count": total_direction_count,
        "minimum_atom_support_profiles": {
            f"{layer}:{character}": list(profile)
            for (layer, character), profile in expected_profiles.items()
        },
        "total_signed_orbit_atom_occurrences": total_atom_count,
        "minimum_support_method": (
            "Exhaustive audit of every coordinate-support subset in each "
            "character-orbit space, followed by exact quotient-rank tests."
        ),
        "checks": {
            "commuting_C2cubed_involutions": commuting_involutions,
            "state_orbit_distribution_match": orbit_distribution_match,
            "tail_lattice_reconstructed_from_03D_seeds": (
                space_dimensions_match
                and all(lattice_checks.values())
            ),
            "all_minimum_profiles_match": all_profiles_match,
            "all_character_quotients_reconstructed": (
                all_quotients_reconstructed
            ),
            "total_atom_count_79": (
                total_atom_count == expected_total_atom_count
            ),
            "direction_count_15": (
                total_direction_count == expected_direction_count
            ),
        },
        "interpretation": (
            "The long 03D Parke--Taylor seed identities split into a finite "
            "catalogue of signed C2^3 orbit atoms. The coefficients in the "
            "normal form describe only relations among symmetry orbits; the "
            "group action itself is factored out."
        ),
        "claim_boundary": (
            "This is an exact symmetry-separated normal form and exact "
            "minimum atom-support certificate. It is not yet a derivation "
            "from a closed family of KK shuffle identities, an anchor-"
            "independent theorem, or a general-n result."
        ),
    }
    with (
        out_dir / "exact_signed_orbit_normal_form_certificate.json"
    ).open("w") as handle:
        json.dump(json_safe(certificate), handle, indent=2)

    elapsed = time.time() - started
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "state_orbit_distribution": dict(
            sorted(orbit_distribution.items())
        ),
        "tail_lattice_reconstructed": (
            space_dimensions_match and all(lattice_checks.values())
        ),
        "quotient_character_direction_count": total_direction_count,
        "total_minimum_signed_orbit_atom_count": total_atom_count,
        "all_minimum_support_profiles_match": all_profiles_match,
        "all_quotient_characters_reconstructed": (
            all_quotients_reconstructed
        ),
        "exact_minimum_signed_orbit_normal_form": exact_certificate,
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "exact_signed_orbit_normal_form_certificate.json",
            "signed_orbit_atom_catalog.csv",
            "quotient_character_normal_form_summary.csv",
            "signed_orbit_normal_form.csv",
            "signed_orbit_normal_form_atom_coefficients.csv",
            "signed_orbit_normal_form_expanded_coefficients.csv",
            "signed_orbit_normal_form.md",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)
    with (out_dir / "verdict.json").open("w") as handle:
        json.dump(
            {
                "verdict": verdict,
                "exact_minimum_signed_orbit_normal_form": exact_certificate,
                "direction_count": total_direction_count,
                "total_atom_count": total_atom_count,
            },
            handle,
            indent=2,
        )

    strict_failures: List[str] = []
    if args.strict:
        checks = {
            "commuting_C2cubed": commuting_involutions,
            "state_orbits": orbit_distribution_match,
            "tail_lattice": (
                space_dimensions_match
                and all(lattice_checks.values())
            ),
            "minimum_support_profiles": all_profiles_match,
            "quotient_reconstruction": all_quotients_reconstructed,
            "fifteen_directions": (
                total_direction_count == expected_direction_count
            ),
            "seventy_nine_atoms": (
                total_atom_count == expected_total_atom_count
            ),
        }
        strict_failures = [
            name
            for name, passed in checks.items()
            if not passed
        ]

    print("\n" + "=" * 124)
    print("FINAL SUMMARY")
    print("=" * 124)
    print(f"Target state-orbit distribution:      {dict(sorted(orbit_distribution.items()))}")
    print(f"Tail lattice reconstructed:           {summary['tail_lattice_reconstructed']}")
    print(f"Quotient-character directions:        {total_direction_count}")
    print(f"All minimum support profiles:         {all_profiles_match}")
    print(f"All character quotients reconstructed:{all_quotients_reconstructed}")
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
            "Construct and certify a minimum-support signed C2^3-orbit "
            "normal form for every exact 9->8 tail-filtration quotient "
            "character direction."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--seed-coefficients", required=True)
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
