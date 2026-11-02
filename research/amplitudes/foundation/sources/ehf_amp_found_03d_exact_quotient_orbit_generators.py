#!/usr/bin/env python3
"""
EHF-AMP-FOUND-03D: Exact Quotient Generators and Orbit Compression
==================================================================

03C proved that the fixed-anchor 9 -> 8 transmitted images form the exact
lattice

    V0 < V2 < V3 = V8 intersect V9 < V8,V9 < V14 = V8+V9 < V15,

inside one 15-dimensional target relation space, with common symmetry

    G = <(2 3),(5 6),(7 8)> ~= C2^3.

03D compresses that lattice into explicit exact seed relations.

For each successive quotient layer

    L2  = V2/V0,
    L3  = V3/V2,
    L8  = V8/V3,
    L9  = V9/V3,
    L15 = V15/V14,

the script:

1. loads the exact RREF bases produced by 03C;
2. constructs the exact quotient action of C2^3 over QQ;
3. computes all joint-character multiplicities;
4. proves that the minimum number of orbit seeds equals the maximum character
   multiplicity;
5. searches for sparse primitive integer seed relations whose C2^3 orbits
   generate the complete quotient;
6. verifies exact reconstruction of every layer.

Because C2^3 is abelian and all its rational irreducibles are one-dimensional,
a quotient with character multiplicities m_chi requires at least

    max_chi m_chi

cyclic orbit generators, and that number is sufficient.

The expected minimum seed counts are

    L2:1, L3:1, L8:2, L9:2, L15:1,

for a total of seven seed relations generating all 15 target directions
layer-by-layer.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_03d_exact_quotient_orbit_generators.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --subspace-bases-json runs/ehf_amp_found_03c/exact_subspace_rref_bases.json \
  --out-dir runs/ehf_amp_found_03d \
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
from functools import reduce
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

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


def rowspace_sum(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    if left.rows == 0:
        return canonical_rowspace(right)
    if right.rows == 0:
        return canonical_rowspace(left)
    return canonical_rowspace(sp.Matrix.vstack(left, right))


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
    first_nonzero = next(value for value in integers if value != 0)
    if first_nonzero < 0:
        integers = [-value for value in integers]
    return sp.Matrix(1, len(integers), integers)


def row_key(row: sp.MatrixBase) -> Tuple[int, ...]:
    primitive = primitive_integer_row(row)
    return tuple(int(value) for value in primitive)


def extend_basis(subspace: sp.Matrix, fullspace: sp.Matrix) -> Tuple[sp.Matrix, sp.Matrix]:
    """
    Return B=[W;C], where C is an exact complement of W in V.
    """
    if not is_subspace(subspace, fullspace):
        raise RuntimeError("Requested quotient has W not contained in V")
    current = canonical_rowspace(subspace)
    complement_rows: List[List[sp.Expr]] = []
    for index in range(fullspace.rows):
        candidate = sp.Matrix([list(fullspace.row(index))])
        enlarged = rowspace_sum(current, candidate)
        if enlarged.rows > current.rows:
            complement_rows.append(list(fullspace.row(index)))
            current = enlarged
    complement = (
        sp.Matrix(complement_rows)
        if complement_rows
        else sp.zeros(0, fullspace.cols)
    )
    basis = (
        sp.Matrix.vstack(subspace, complement)
        if subspace.rows
        else complement
    )
    if canonical_rowspace(basis) != canonical_rowspace(fullspace):
        raise RuntimeError("Failed to extend quotient basis exactly")
    return basis, complement


def coordinate_map(basis: sp.Matrix):
    """
    Return a function mapping an ambient row in span(B) to its coefficient row.
    """
    _, pivots = basis.rref()
    pivot_columns = list(pivots)
    pivot_matrix = basis[:, pivot_columns]
    inverse = pivot_matrix.inv()

    def coordinates(row: sp.MatrixBase) -> sp.Matrix:
        row_matrix = sp.Matrix(row)
        if row_matrix.rows != 1:
            raise ValueError("Coordinate conversion expects one row")
        coefficient = row_matrix[:, pivot_columns] * inverse
        if coefficient * basis != row_matrix:
            raise RuntimeError("Ambient row is not in the expected span")
        return coefficient

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


def action_permutation_matrix(destination: Sequence[int]) -> sp.Matrix:
    size = len(destination)
    matrix = sp.zeros(size)
    for source, target in enumerate(destination):
        matrix[target, source] = 1
    return matrix


def transport_row(row: sp.MatrixBase, permutation: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(row) * permutation.T


def quotient_action_matrix(
    full_basis: sp.Matrix,
    complement: sp.Matrix,
    subspace_dimension: int,
    permutation: sp.Matrix,
) -> sp.Matrix:
    coordinates = coordinate_map(full_basis)
    rows: List[List[sp.Expr]] = []
    for index in range(complement.rows):
        transformed = transport_row(complement.row(index), permutation)
        coefficient = coordinates(transformed)
        rows.append(list(coefficient[:, subspace_dimension:]))
    return sp.Matrix(rows)


def group_matrices(generators: Sequence[sp.Matrix]) -> Dict[SignTriple, sp.Matrix]:
    dimension = generators[0].rows
    identity = sp.eye(dimension)
    output: Dict[SignTriple, sp.Matrix] = {}
    for powers in itertools.product((0, 1), repeat=3):
        matrix = identity
        for power, generator in zip(powers, generators):
            if power:
                matrix = matrix * generator
        output[powers] = matrix
    return output


def character_multiplicities(
    generators: Sequence[sp.Matrix],
) -> Dict[SignTriple, int]:
    dimension = generators[0].rows
    identity = sp.eye(dimension)
    multiplicities: Dict[SignTriple, int] = {}
    for signs in itertools.product((1, -1), repeat=3):
        projector = identity
        for sign, generator in zip(signs, generators):
            projector = projector * (identity + sign * generator) / 2
        multiplicities[signs] = canonical_rowspace(projector).rows
    return multiplicities


def lll_complement_basis(complement: sp.Matrix) -> sp.Matrix:
    if complement.rows == 0:
        return complement
    integer_rows = sp.Matrix.vstack(
        *[primitive_integer_row(complement.row(index)) for index in range(complement.rows)]
    )
    try:
        reduced = integer_rows.lll()
    except Exception:
        reduced = integer_rows
    return sp.Matrix.vstack(
        *[primitive_integer_row(reduced.row(index)) for index in range(reduced.rows)]
    )


def candidate_seed_rows(
    reduced_basis: sp.Matrix,
    max_pool: int,
) -> List[sp.Matrix]:
    """
    Deterministic primitive candidates from ternary combinations of LLL rows.
    """
    dimension = reduced_basis.rows
    candidates: Dict[Tuple[int, ...], sp.Matrix] = {}
    for coefficients in itertools.product((-1, 0, 1), repeat=dimension):
        if not any(coefficients):
            continue
        row = sp.zeros(1, reduced_basis.cols)
        for coefficient, basis_row in zip(coefficients, range(dimension)):
            if coefficient:
                row += coefficient * reduced_basis.row(basis_row)
        primitive = primitive_integer_row(row)
        candidates[row_key(primitive)] = primitive

    ordered = sorted(
        candidates.values(),
        key=lambda row: (
            sum(value != 0 for value in row),
            sum(abs(int(value)) for value in row),
            max(abs(int(value)) for value in row),
            row_key(row),
        ),
    )
    return ordered[:max_pool]


def quotient_coordinates_for_ambient(
    row: sp.Matrix,
    full_basis: sp.Matrix,
    subspace_dimension: int,
) -> sp.Matrix:
    coordinates = coordinate_map(full_basis)(row)
    return coordinates[:, subspace_dimension:]


def orbit_span(
    seed_rows: Sequence[sp.Matrix],
    permutations: Sequence[sp.Matrix],
    full_basis: sp.Matrix,
    subspace_dimension: int,
) -> sp.Matrix:
    quotient_rows: List[List[sp.Expr]] = []
    for seed in seed_rows:
        for permutation in permutations:
            transformed = transport_row(seed, permutation)
            quotient = quotient_coordinates_for_ambient(
                transformed,
                full_basis,
                subspace_dimension,
            )
            quotient_rows.append(list(quotient))
    return canonical_rowspace(sp.Matrix(quotient_rows))


def select_minimal_seeds(
    candidates: Sequence[sp.Matrix],
    permutations: Sequence[sp.Matrix],
    full_basis: sp.Matrix,
    subspace_dimension: int,
    quotient_dimension: int,
    lower_bound: int,
    shortlist: int,
) -> Tuple[List[sp.Matrix], sp.Matrix]:
    """
    Search at the character-theoretic lower bound.
    """
    scored = []
    for row in candidates:
        span = orbit_span(
            [row],
            permutations,
            full_basis,
            subspace_dimension,
        )
        scored.append((span.rows, row, span))
    scored.sort(
        key=lambda item: (
            -item[0],
            sum(value != 0 for value in item[1]),
            sum(abs(int(value)) for value in item[1]),
        )
    )
    shortlist_rows = [item[1] for item in scored[:shortlist]]

    if lower_bound == 1:
        for row in shortlist_rows:
            span = orbit_span(
                [row],
                permutations,
                full_basis,
                subspace_dimension,
            )
            if span.rows == quotient_dimension:
                return [row], span
    else:
        for combination in itertools.combinations(shortlist_rows, lower_bound):
            span = orbit_span(
                list(combination),
                permutations,
                full_basis,
                subspace_dimension,
            )
            if span.rows == quotient_dimension:
                return list(combination), span

    raise RuntimeError(
        f"Unable to find {lower_bound} orbit seeds for a "
        f"{quotient_dimension}-dimensional quotient"
    )


def load_subspace_bases(path: Path) -> Dict[str, sp.Matrix]:
    with path.open() as handle:
        payload = json.load(handle)
    result: Dict[str, sp.Matrix] = {}
    for name, record in payload.items():
        rows = [
            [sp.Rational(value) for value in row]
            for row in record["rref_rows"]
        ]
        dimension = int(record["dimension"])
        if rows:
            matrix = canonical_rowspace(sp.Matrix(rows))
        else:
            # The ambient dimension is fixed by the n=8 target fibre.
            matrix = sp.zeros(0, 72)
        if matrix.rows != dimension:
            raise RuntimeError(
                f"Dimension mismatch for {name}: {matrix.rows} != {dimension}"
            )
        result[name] = matrix
    return result


def write_seed_markdown(
    path: Path,
    layer_records: Sequence[Mapping[str, object]],
    seed_records: Sequence[Mapping[str, object]],
) -> None:
    lines = [
        "# EHF-AMP-FOUND-03D",
        "## Exact quotient generators and orbit compression",
        "",
        "The common symmetry group is",
        "",
        r"\[G=\langle(2\,3),(5\,6),(7\,8)\rangle\cong C_2^3.\]",
        "",
        "For an abelian \(C_2^3\)-module, the minimum number of cyclic orbit "
        "generators equals the largest joint-character multiplicity.",
        "",
        "| Layer | Quotient | Dimension | Character multiplicities | Minimum seeds | Found |",
        "|---|---|---:|---|---:|---:|",
    ]
    for record in layer_records:
        lines.append(
            f"| {record['layer_id']} | {record['quotient']} | "
            f"{record['quotient_dimension']} | "
            f"`{record['nonzero_character_multiplicities']}` | "
            f"{record['minimum_seed_count']} | {record['seed_count_found']} |"
        )

    lines.extend(["", "## Sparse primitive seed relations", ""])
    for seed in seed_records:
        lines.extend([
            f"### {seed['seed_id']}",
            "",
            f"- Layer: `{seed['layer_id']}`",
            f"- Support size: {seed['support_size']}",
            f"- Coefficient \(L_1\) norm: {seed['coefficient_l1_norm']}",
            f"- Single-seed orbit rank in quotient: {seed['individual_orbit_rank']}",
            "",
            "```text",
            str(seed["relation_text"]),
            "```",
            "",
        ])

    lines.extend([
        "## Exact conclusion",
        "",
        "The five successive quotient layers require",
        "",
        r"\[1+1+2+2+1=7\]",
        "",
        "orbit seeds in total. Their exact \(C_2^3\)-orbits reconstruct all "
        "fifteen target-relation directions layer by layer.",
        "",
    ])
    path.write_text("\n".join(lines))


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    bases_path = Path(args.subspace_bases_json).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_03d_base")
    subspaces = load_subspace_bases(bases_path)

    required = {
        "V0", "V2", "V3_intersection", "V8", "V9", "V14", "V15"
    }
    missing = required - set(subspaces)
    if missing:
        raise RuntimeError(f"Missing 03C subspace bases: {sorted(missing)}")

    reference_key = ((1, 2, 3, 4), (5, 6, 7, 8))
    reference_states = base.fibres(8)[reference_key]
    if len(reference_states) != 72:
        raise RuntimeError("Expected 72 states in the reference target fibre")

    print("=" * 122)
    print("EHF-AMP-FOUND-03D: EXACT QUOTIENT GENERATORS AND ORBIT COMPRESSION")
    print("=" * 122)
    print(f"base script:                 {base_script}")
    print(f"03C subspace bases:          {bases_path}")
    print(f"output directory:            {out_dir}")
    print("reference fibre:             A={2,3,4}")
    print("symmetry group:              C2^3")
    print("coefficient domain:          QQ")

    generator_specs = [
        ("g1=(2 3)", {2: 3, 3: 2}),
        ("g2=(5 6)", {5: 6, 6: 5}),
        ("g3=(7 8)", {7: 8, 8: 7}),
    ]
    ambient_generators: List[sp.Matrix] = []
    for _, mapping in generator_specs:
        destination = target_action_destination(base, reference_states, mapping)
        ambient_generators.append(action_permutation_matrix(destination))

    ambient_group: List[sp.Matrix] = []
    identity_ambient = sp.eye(72)
    for powers in itertools.product((0, 1), repeat=3):
        matrix = identity_ambient
        for power, generator in zip(powers, ambient_generators):
            if power:
                matrix = matrix * generator
        ambient_group.append(matrix)

    layers = [
        ("L2", "V2/V0", "V0", "V2"),
        ("L3", "V3/V2", "V2", "V3_intersection"),
        ("L8", "V8/V3", "V3_intersection", "V8"),
        ("L9", "V9/V3", "V3_intersection", "V9"),
        ("L15", "V15/V14", "V14", "V15"),
    ]
    expected_dimensions = {"L2": 2, "L3": 1, "L8": 5, "L9": 6, "L15": 1}
    expected_seed_counts = {"L2": 1, "L3": 1, "L8": 2, "L9": 2, "L15": 1}

    layer_rows: List[Dict[str, object]] = []
    character_rows: List[Dict[str, object]] = []
    seed_rows: List[Dict[str, object]] = []
    coefficient_rows: List[Dict[str, object]] = []

    all_layer_dimensions = True
    all_minimal_counts = True
    all_reconstruction = True
    all_character_checks = True
    total_seeds = 0

    for layer_id, quotient_name, lower_name, upper_name in layers:
        lower = canonical_rowspace(subspaces[lower_name])
        upper = canonical_rowspace(subspaces[upper_name])
        full_basis, complement = extend_basis(lower, upper)
        quotient_dimension = complement.rows
        all_layer_dimensions &= quotient_dimension == expected_dimensions[layer_id]

        quotient_generators = [
            quotient_action_matrix(
                full_basis,
                complement,
                lower.rows,
                permutation,
            )
            for permutation in ambient_generators
        ]
        commuting_involutions = all(
            matrix * matrix == sp.eye(quotient_dimension)
            for matrix in quotient_generators
        ) and all(
            quotient_generators[left] * quotient_generators[right]
            == quotient_generators[right] * quotient_generators[left]
            for left in range(3)
            for right in range(left + 1, 3)
        )
        all_character_checks &= commuting_involutions

        multiplicities = character_multiplicities(quotient_generators)
        nonzero_multiplicities = {
            sign_text(signs): multiplicity
            for signs, multiplicity in multiplicities.items()
            if multiplicity
        }
        minimum_seed_count = max(multiplicities.values())
        all_minimal_counts &= minimum_seed_count == expected_seed_counts[layer_id]

        for signs, multiplicity in multiplicities.items():
            character_rows.append({
                "layer_id": layer_id,
                "quotient": quotient_name,
                "character": sign_text(signs),
                "g1_23": signs[0],
                "g2_56": signs[1],
                "g3_78": signs[2],
                "multiplicity": multiplicity,
            })

        reduced = lll_complement_basis(complement)
        candidates = candidate_seed_rows(reduced, args.max_candidate_pool)
        selected, reconstructed_span = select_minimal_seeds(
            candidates=candidates,
            permutations=ambient_group,
            full_basis=full_basis,
            subspace_dimension=lower.rows,
            quotient_dimension=quotient_dimension,
            lower_bound=minimum_seed_count,
            shortlist=args.seed_shortlist,
        )
        reconstruction_ok = reconstructed_span.rows == quotient_dimension
        all_reconstruction &= reconstruction_ok
        total_seeds += len(selected)

        layer_rows.append({
            "layer_id": layer_id,
            "quotient": quotient_name,
            "lower_space": lower_name,
            "upper_space": upper_name,
            "lower_dimension": lower.rows,
            "upper_dimension": upper.rows,
            "quotient_dimension": quotient_dimension,
            "expected_quotient_dimension": expected_dimensions[layer_id],
            "dimension_match": quotient_dimension == expected_dimensions[layer_id],
            "nonzero_character_multiplicities": ";".join(
                f"{character}:{multiplicity}"
                for character, multiplicity in sorted(nonzero_multiplicities.items())
            ),
            "maximum_character_multiplicity": minimum_seed_count,
            "minimum_seed_count": minimum_seed_count,
            "expected_minimum_seed_count": expected_seed_counts[layer_id],
            "seed_count_found": len(selected),
            "minimum_count_match": len(selected) == minimum_seed_count,
            "orbit_reconstruction_rank": reconstructed_span.rows,
            "exact_reconstruction": reconstruction_ok,
            "candidate_pool_size": len(candidates),
            "commuting_involutions_exact": commuting_involutions,
        })

        for seed_index, seed in enumerate(selected, start=1):
            seed_id = f"{layer_id}_seed_{seed_index}"
            individual_span = orbit_span(
                [seed],
                ambient_group,
                full_basis,
                lower.rows,
            )
            primitive = primitive_integer_row(seed)
            support = [
                (position, int(primitive[0, position]))
                for position in range(primitive.cols)
                if primitive[0, position] != 0
            ]
            relation_terms = [
                f"{coefficient:+d} * PT({cycle_text(reference_states[position])})"
                for position, coefficient in support
            ]
            relation_text = " ".join(relation_terms)
            seed_record = {
                "seed_id": seed_id,
                "layer_id": layer_id,
                "quotient": quotient_name,
                "seed_number": seed_index,
                "support_size": len(support),
                "coefficient_l1_norm": sum(abs(value) for _, value in support),
                "coefficient_max_abs": max(abs(value) for _, value in support),
                "individual_orbit_rank": individual_span.rows,
                "joint_seed_count_for_layer": len(selected),
                "joint_orbit_reconstruction_rank": reconstructed_span.rows,
                "relation_text": relation_text,
            }
            seed_rows.append(seed_record)
            for position, coefficient in support:
                coefficient_rows.append({
                    "seed_id": seed_id,
                    "layer_id": layer_id,
                    "target_state_index": position,
                    "target_cycle": cycle_text(reference_states[position]),
                    "coefficient": coefficient,
                })

        print(
            f"  {layer_id:3s}: dim={quotient_dimension}, "
            f"chars={nonzero_multiplicities}, "
            f"minimum seeds={minimum_seed_count}, "
            f"found={len(selected)}, reconstruct={reconstruction_ok}"
        )

    write_csv(out_dir / "quotient_layer_summary.csv", layer_rows)
    write_csv(out_dir / "quotient_character_multiplicities.csv", character_rows)
    write_csv(out_dir / "orbit_seed_summary.csv", seed_rows)
    write_csv(out_dir / "sparse_seed_coefficients.csv", coefficient_rows)
    write_seed_markdown(
        out_dir / "sparse_orbit_seed_relations.md",
        layer_rows,
        seed_rows,
    )

    expected_total_seeds = sum(expected_seed_counts.values())
    exact_certificate = (
        all_layer_dimensions
        and all_minimal_counts
        and all_reconstruction
        and all_character_checks
        and total_seeds == expected_total_seeds
    )
    verdict = (
        "EHF_AMP_FOUND_03D_EXACT_SEVEN_SEED_ORBIT_COMPRESSION_PROVED"
        if exact_certificate
        else "EHF_AMP_FOUND_03D_ORBIT_COMPRESSION_FAILED"
    )

    certificate = {
        "theorem": (
            "The 15-dimensional 9->8 target tail-filtration lattice is "
            "generated layer-by-layer by seven primitive relation seeds under "
            "the exact C2^3 action."
        ),
        "group": {
            "name": "C2^3",
            "generators": [name for name, _ in generator_specs],
            "all_irreducibles_over_Q": "one-dimensional sign characters",
        },
        "minimal_generator_principle": (
            "For a rational C2^3-module with character multiplicities m_chi, "
            "the minimum number of cyclic orbit generators is max_chi m_chi."
        ),
        "layers": {
            row["layer_id"]: {
                "quotient": row["quotient"],
                "dimension": row["quotient_dimension"],
                "character_multiplicities": row[
                    "nonzero_character_multiplicities"
                ],
                "minimum_seed_count": row["minimum_seed_count"],
                "exact_orbit_reconstruction": row["exact_reconstruction"],
            }
            for row in layer_rows
        },
        "total_seed_count": total_seeds,
        "expected_total_seed_count": expected_total_seeds,
        "exact_certificate": exact_certificate,
        "interpretation": (
            "The dimensions 2,1,5,6,1 of the successive lattice increments "
            "are organised by C2^3 character multiplicities. Repeated "
            "characters force two independent seeds in L8 and L9; all other "
            "layers are cyclic."
        ),
        "claim_boundary": (
            "This gives explicit exact finite seed identities and a minimal "
            "orbit-generator count. It does not yet derive the seeds from a "
            "closed symbolic family of shuffle identities, prove anchor "
            "independence, or establish the same module pattern at general n."
        ),
    }
    with (out_dir / "exact_orbit_generator_certificate.json").open("w") as handle:
        json.dump(json_safe(certificate), handle, indent=2)

    elapsed = time.time() - started
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "layer_dimensions_exact": all_layer_dimensions,
        "character_theoretic_minima_exact": all_minimal_counts,
        "all_layers_reconstructed_by_seed_orbits": all_reconstruction,
        "total_seed_count": total_seeds,
        "expected_total_seed_count": expected_total_seeds,
        "exact_seven_seed_orbit_compression": exact_certificate,
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "exact_orbit_generator_certificate.json",
            "quotient_layer_summary.csv",
            "quotient_character_multiplicities.csv",
            "orbit_seed_summary.csv",
            "sparse_seed_coefficients.csv",
            "sparse_orbit_seed_relations.md",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)
    with (out_dir / "verdict.json").open("w") as handle:
        json.dump(
            {
                "verdict": verdict,
                "exact_seven_seed_orbit_compression": exact_certificate,
                "total_seed_count": total_seeds,
            },
            handle,
            indent=2,
        )

    strict_failures: List[str] = []
    if args.strict:
        checks = {
            "layer_dimensions": all_layer_dimensions,
            "character_minimum_counts": all_minimal_counts,
            "exact_orbit_reconstruction": all_reconstruction,
            "commuting_C2cubed_actions": all_character_checks,
            "seven_total_seeds": total_seeds == expected_total_seeds,
        }
        strict_failures = [
            name for name, passed in checks.items() if not passed
        ]

    print("\n" + "=" * 122)
    print("FINAL SUMMARY")
    print("=" * 122)
    print(f"Exact quotient dimensions:            {all_layer_dimensions}")
    print(f"Character-theoretic seed minima:      {all_minimal_counts}")
    print(f"All quotient layers reconstructed:    {all_reconstruction}")
    print(f"Total primitive orbit seeds:          {total_seeds}")
    print(f"Expected total:                       {expected_total_seeds}")
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
            "Extract explicit minimal C2^3 orbit generators for the exact "
            "9->8 target tail-filtration quotient layers."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--subspace-bases-json", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--max-candidate-pool", type=int, default=728)
    parser.add_argument("--seed-shortlist", type=int, default=80)
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
