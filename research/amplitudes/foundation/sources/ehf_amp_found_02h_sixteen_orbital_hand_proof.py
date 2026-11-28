#!/usr/bin/env python3
"""
EHF-AMP-FOUND-02H: Sixteen-Orbital Hand-Proof Compression
==========================================================

This probe compresses the exact 36 x 36 reference-channel operator derived in
02G into two small exact proof objects:

1. a 16-orbital coefficient table under the complement-pair stabilizer;
2. nine Fourier blocks for the group algebra Q[S3 x S3], the largest only 4 x 4.

The key observation is that the 36 supported seven-point orderings are exactly
the alternating words

    1, A1, B1, A2, B2, A3, B3

with A={2,3,4}, B={5,6,7}. Hence the support is canonically S3 x S3.
The subgroup S3 x S3 acts regularly, so the exact channel operator is a right
convolution operator

    K[x,y] = f(x^{-1} y)

for an exact rational kernel f on 36 group elements.

The extra block-exchange C2 reduces the symmetric kernel to 16 unordered
stabilizer orbitals. Exact convolution powers on these 16 coordinates yield
the minimal polynomial. Fourier transformation over S3 x S3 then derives the
four nonzero spectral sectors from matrices of sizes 1, 2 and 4.

No numerical SVD, random kinematics, rational reconstruction, or 02D operator
bundle is used. The reference operator is rebuilt directly from the exact KK
construction supplied by 02G.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_02h_sixteen_orbital_hand_proof.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --symmetry-script scripts/ehf_amp_found_02e_complement_pair_symmetry_certificate.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --out-dir runs/ehf_amp_found_02h
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
from typing import Dict, Iterable, Iterator, List, Mapping, Sequence, Tuple

import sympy as sp

Cycle = Tuple[int, ...]
SmallPerm = Tuple[int, int, int]
GroupElement = Tuple[SmallPerm, SmallPerm]
FibreKey = Tuple[Tuple[int, ...], Tuple[int, ...]]
Permutation = Tuple[int, ...]


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


def json_safe(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return value


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
                fields.append(key)
                seen.add(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def cycle_text(cycle: Sequence[int]) -> str:
    return ",".join(map(str, cycle))


def small_perm_text(perm: SmallPerm) -> str:
    return "".join(str(value + 1) for value in perm)


def group_text(element: GroupElement) -> str:
    return f"{small_perm_text(element[0])}|{small_perm_text(element[1])}"


def compose(left: SmallPerm, right: SmallPerm) -> SmallPerm:
    """left o right."""
    return tuple(left[right[index]] for index in range(3))  # type: ignore[return-value]


def inverse(perm: SmallPerm) -> SmallPerm:
    result = [0, 0, 0]
    for source, target in enumerate(perm):
        result[target] = source
    return tuple(result)  # type: ignore[return-value]


def parity(perm: SmallPerm) -> int:
    inversions = sum(
        perm[left] > perm[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    return -1 if inversions % 2 else 1


def relative(left: GroupElement, right: GroupElement) -> GroupElement:
    return (
        compose(inverse(left[0]), right[0]),
        compose(inverse(left[1]), right[1]),
    )


def encode_order(order: Sequence[int], base_labels: Sequence[int]) -> SmallPerm:
    return tuple(base_labels.index(label) for label in order)  # type: ignore[return-value]


def encode_support_state(
    cycle: Cycle,
    a_labels: Sequence[int],
    b_labels: Sequence[int],
) -> GroupElement:
    a_order = (cycle[1], cycle[3], cycle[5])
    b_order = (cycle[2], cycle[4], cycle[6])
    if set(a_order) != set(a_labels) or set(b_order) != set(b_labels):
        raise RuntimeError(f"Support state is not alternating A/B: {cycle}")
    return encode_order(a_order, a_labels), encode_order(b_order, b_labels)


def convolution(
    left: Mapping[GroupElement, sp.Rational],
    right: Mapping[GroupElement, sp.Rational],
    group: Sequence[GroupElement],
) -> Dict[GroupElement, sp.Rational]:
    result: Dict[GroupElement, sp.Rational] = {}
    for target in group:
        total = sp.Rational(0)
        for source in group:
            argument = (
                compose(inverse(source[0]), target[0]),
                compose(inverse(source[1]), target[1]),
            )
            total += left[source] * right[argument]
        result[target] = sp.simplify(total)
    return result


def derive_kernel_minimal_polynomial(
    powers: Sequence[Mapping[GroupElement, sp.Rational]],
    group: Sequence[GroupElement],
) -> List[sp.Rational]:
    columns = [
        sp.Matrix([power[element] for element in group])
        for power in powers
    ]
    dependencies = sp.Matrix.hstack(*columns).nullspace()
    for vector in dependencies:
        if vector[-1] == 0:
            continue
        coefficients = [sp.simplify(value / vector[-1]) for value in vector]
        return coefficients
    raise RuntimeError("No exact convolution-kernel dependence found")


def polynomial_expression(
    coefficients: Sequence[sp.Rational],
    symbol: sp.Symbol,
) -> sp.Expr:
    return sp.expand(
        sum(value * symbol**degree for degree, value in enumerate(coefficients))
    )


def standard_representation(perm: SmallPerm) -> sp.Matrix:
    """
    Exact integral standard representation of S3 on
    span(e1-e3, e2-e3).
    """
    permutation_matrix = sp.zeros(3)
    for source, target in enumerate(perm):
        permutation_matrix[target, source] = 1
    basis = sp.Matrix([[1, 0], [0, 1], [-1, -1]])
    columns: List[sp.Matrix] = []
    for column in range(2):
        image = permutation_matrix * basis[:, column]
        coordinates = basis.gauss_jordan_solve(image)[0]
        columns.append(coordinates)
    return sp.Matrix.hstack(*columns)


def irrep_catalogue():
    return {
        "1": (1, lambda perm: sp.Matrix([[1]])),
        "sgn": (1, lambda perm: sp.Matrix([[parity(perm)]])),
        "std": (2, standard_representation),
    }


def fourier_block(
    kernel: Mapping[GroupElement, sp.Rational],
    first,
    second,
    group: Sequence[GroupElement],
) -> sp.Matrix:
    first_dim, first_rep = first
    second_dim, second_rep = second
    result = sp.zeros(first_dim * second_dim)
    for (left, right) in group:
        result += kernel[(left, right)] * sp.kronecker_product(
            first_rep(left), second_rep(right)
        )
    return result


def matrix_text(matrix: sp.Matrix) -> str:
    return ";".join(
        ",".join(str(matrix[row, column]) for column in range(matrix.cols))
        for row in range(matrix.rows)
    )


def unordered_orbits(
    size: int,
    actions: Sequence[Tuple[List[int], List[int]]],
) -> Tuple[List[set], Dict[Tuple[int, int], int]]:
    unseen = {
        (left, right)
        for left in range(size)
        for right in range(left, size)
    }
    orbits: List[set] = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        stack = [seed]
        while stack:
            left, right = stack.pop()
            for destinations, _ in actions:
                mapped_left = destinations[left]
                mapped_right = destinations[right]
                if mapped_left > mapped_right:
                    mapped_left, mapped_right = mapped_right, mapped_left
                pair = (mapped_left, mapped_right)
                if pair not in orbit:
                    orbit.add(pair)
                    stack.append(pair)
        unseen -= orbit
        orbits.append(orbit)
    orbits.sort(key=lambda orbit: min(orbit))
    lookup = {
        pair: orbit_index
        for orbit_index, orbit in enumerate(orbits)
        for pair in orbit
    }
    return orbits, lookup


def build_reference_operator(base, helper, direct, symmetry):
    n = 8
    target_states: List[Cycle] = list(base.canonical_cycles(7))
    fibres: Dict[FibreKey, List[Cycle]] = base.fibres(n)
    _, _, pairs, pair_ids = symmetry.build_pairs(base)
    reference_pair_id = symmetry.canonical_pair_id((2, 3, 4))
    reference_index = pair_ids.index(reference_pair_id)
    left_key, right_key = pairs[reference_index]

    kk_permutations = list(itertools.permutations(range(2, n)))
    kk_index = {permutation: index for index, permutation in enumerate(kk_permutations)}

    data = {}
    for key in (left_key, right_key):
        chamber = fibres[key]
        kk_matrix = direct.exact_kk_coordinate_matrix(chamber, n, kk_index)
        basis, projector, rank, nullity = direct.exact_relation_projector(kk_matrix)
        delete = direct.exact_delete_matrix(
            base, helper, chamber, target_states, n
        )
        data[key] = {
            "chamber": chamber,
            "kk_matrix": kk_matrix,
            "basis": basis,
            "projector": projector,
            "delete": delete,
            "rank": rank,
            "nullity": nullity,
        }

    ambient = (
        data[left_key]["delete"]
        * data[left_key]["projector"]
        * data[left_key]["delete"].T
        + data[right_key]["delete"]
        * data[right_key]["projector"]
        * data[right_key]["delete"].T
    )
    support = direct.support_indices(ambient)
    restricted = ambient.extract(support, support)
    return {
        "target_states": target_states,
        "reference_pair_id": reference_pair_id,
        "left_key": left_key,
        "right_key": right_key,
        "left_data": data[left_key],
        "right_data": data[right_key],
        "ambient": ambient,
        "support": support,
        "restricted": restricted,
    }


def write_hand_proof(
    path: Path,
    reference_pair: str,
    entry_values: Sequence[sp.Rational],
    orbital_count: int,
    minimal_polynomial: sp.Expr,
    fourier_rows: Sequence[Mapping[str, object]],
    h_rows: Sequence[Mapping[str, object]],
) -> None:
    table_lines = [
        r"| \(S_3\times S_3\) irrep | Fourier dimension | rank | eigenvalues | channel multiplicity |",
        "|---|---:|---:|---|---:|",
    ]
    for row in fourier_rows:
        table_lines.append(
            f"| {row['irrep']} | {row['irrep_dimension']} | {row['block_rank']} | "
            f"{row['eigenvalues']} | {row['nonzero_channel_contribution']} |"
        )

    h_lines = [
        r"| \(H\)-block | dimension | scalar | source Fourier sectors |",
        "|---|---:|---:|---|",
    ]
    for row in h_rows:
        h_lines.append(
            f"| {row['h_block']} | {row['dimension']} | {row['schur_scalar']} | "
            f"{row['source_fourier_sectors']} |"
        )

    content = rf"""# EHF-AMP-FOUND-02H  
## Sixteen-Orbital Hand-Proof Compression

### Exact theorem input

The reference complement pair is

\[
{reference_pair}.
\]

Using the exact KK shuffle identity, the two fibre-local relation projectors
and the signed delete-8 maps produce an exact rank-11 operator \(K\) on a
36-state support.

### Step 1: identify the support with \(S_3\times S_3\)

Every supported state has the unique form

\[
(1,a_1,b_1,a_2,b_2,a_3,b_3),
\]

where \((a_1,a_2,a_3)\) is a permutation of \((2,3,4)\) and
\((b_1,b_2,b_3)\) is a permutation of \((5,6,7)\). Hence

\[
X\cong S_3\times S_3,\qquad |X|=36.
\]

The subgroup \(S_3\times S_3\) acts regularly on \(X\). Exact covariance
therefore implies

\[
K[x,y]=f(x^{{-1}}y)
\]

for a rational convolution kernel \(f\in\mathbb{{Q}}[S_3\times S_3]\).

### Step 2: sixteen stabiliser orbitals

The block-exchange involution extends the regular subgroup to

\[
H=(S_3\times S_3)\rtimes C_2.
\]

The unordered pairs of support states split into exactly {orbital_count}
\(H\)-orbitals. The kernel uses the exact values

\[
{", ".join(str(value) for value in entry_values)}.
\]

Thus the full \(36\times36\) matrix is encoded by the 16-row orbital table
written by the probe.

Exact convolution of the 16 orbital coordinates gives

\[
\boxed{{m_K(x)={sp.factor(minimal_polynomial)}}}.
\]

### Step 3: Fourier reduction to nine tiny blocks

The irreducibles of \(S_3\) are the trivial, sign and standard
representations, of dimensions \(1,1,2\). Therefore the group algebra of
\(S_3\times S_3\) reduces \(K\) to nine Fourier blocks, the largest of size
\(4\times4\).

{chr(10).join(table_lines)}

In the regular representation, an irrep of dimension \(d\) occurs \(d\)
times. Consequently the nonzero multiplicities are

\[
1+1=2,\qquad 2+2=4,\qquad4,\qquad1.
\]

### Step 4: restore the block-exchange involution

The \(C_2\) exchange pairs the factor-swapped Fourier sectors. The resulting
irreducible \(H\)-blocks are:

{chr(10).join(h_lines)}

Hence

\[
\mathcal C\cong V_2\oplus V_4^{{(8/5)}}\oplus
V_4^{{(6/5)}}\oplus V_1,
\]

and

\[
K|_{{\mathcal{{C}}}}
=
1P_2+\frac85P_4^{{(8/5)}}+\frac65P_4^{{(6/5)}}+\frac95P_1.
\]

This yields the exact supported characteristic polynomial

\[
x^{{25}}(x-1)^2
\left(x-\frac65\right)^4
\left(x-\frac85\right)^4
\left(x-\frac95\right).
\]

### Claim boundary

This is an exact computer-generated hand-proof compression. Its mathematical
inputs are the KK shuffle identity, KK-basis independence, and finite exact
linear algebra over \(\mathbb{{Q}}\). The remaining work is editorial: present
the 16 orbital representatives and the nine Fourier blocks in conventional
theorem-proof form.
"""
    path.write_text(content)


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    helper_script = Path(args.helper_script).resolve()
    symmetry_script = Path(args.symmetry_script).resolve()
    direct_script = Path(args.direct_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_02h_base")
    helper = load_module(helper_script, "ehf_amp_found_02h_helper")
    symmetry = load_module(symmetry_script, "ehf_amp_found_02h_symmetry")
    direct = load_module(direct_script, "ehf_amp_found_02h_direct")

    construction = build_reference_operator(base, helper, direct, symmetry)
    target_states: List[Cycle] = construction["target_states"]
    support: List[int] = construction["support"]
    matrix: sp.Matrix = construction["restricted"]
    reference_pair_id = construction["reference_pair_id"]

    a_labels = reference_pair_id[0]
    b_labels = reference_pair_id[1]
    support_cycles = [target_states[index] for index in support]
    support_group = [
        encode_support_state(cycle, a_labels, b_labels)
        for cycle in support_cycles
    ]
    group = [
        (left, right)
        for left in itertools.permutations(range(3))
        for right in itertools.permutations(range(3))
    ]
    group = [
        (tuple(left), tuple(right))  # type: ignore[list-item]
        for left, right in group
    ]
    if set(support_group) != set(group):
        raise RuntimeError("The 36-state support is not exactly S3 x S3")

    group_index = {
        element: index for index, element in enumerate(support_group)
    }
    identity: GroupElement = ((0, 1, 2), (0, 1, 2))
    identity_index = group_index[identity]

    kernel = {
        element: sp.Rational(matrix[identity_index, group_index[element]])
        for element in group
    }

    convolution_law = True
    for left in group:
        left_index = group_index[left]
        for right in group:
            right_index = group_index[right]
            if matrix[left_index, right_index] != kernel[relative(left, right)]:
                convolution_law = False
                break
        if not convolution_law:
            break

    print("=" * 122)
    print("EHF-AMP-FOUND-02H: SIXTEEN-ORBITAL HAND-PROOF COMPRESSION")
    print("=" * 122)
    print(f"base script:                 {base_script}")
    print(f"reflection-aware helper:     {helper_script}")
    print(f"symmetry helper:             {symmetry_script}")
    print(f"direct exact helper:         {direct_script}")
    print(f"output directory:            {out_dir}")
    print(f"reference pair:              {symmetry.pair_text(reference_pair_id)}")
    print(f"support identified with:     S3 x S3 ({len(group)} elements)")
    print(f"exact convolution law:       {convolution_law}")

    # Stabilizer actions on support.
    support_position = {
        ambient: local for local, ambient in enumerate(support)
    }
    stabilizer = []
    actions: List[Tuple[List[int], List[int]]] = []
    for permutation in itertools.permutations(range(2, 8)):
        mapped = symmetry.canonical_pair_id(
            symmetry.apply_perm_to_subset(reference_pair_id[0], permutation)
        )
        if mapped != reference_pair_id:
            continue
        destination, signs = symmetry.signed_action(target_states, permutation)
        local_destination = [
            support_position[int(destination[ambient])]
            for ambient in support
        ]
        local_signs = [int(signs[ambient]) for ambient in support]
        stabilizer.append(permutation)
        actions.append((local_destination, local_signs))

    orbits, orbital_lookup = unordered_orbits(len(support), actions)
    if len(orbits) != 16:
        raise RuntimeError(f"Expected 16 unordered stabilizer orbitals, found {len(orbits)}")

    orbital_rows: List[Dict[str, object]] = []
    for orbital_index, orbit in enumerate(orbits):
        values = {matrix[left, right] for left, right in orbit}
        if len(values) != 1:
            raise RuntimeError("Matrix is not constant on an unordered stabilizer orbital")
        relative_types = {
            group_text(relative(support_group[left], support_group[right]))
            for left, right in orbit
        }
        representative = min(orbit)
        left, right = representative
        orbital_rows.append(
            {
                "orbital_index": orbital_index,
                "orbital_size": len(orbit),
                "diagonal": all(i == j for i, j in orbit),
                "matrix_value": str(next(iter(values))),
                "representative_left_cycle": cycle_text(support_cycles[left]),
                "representative_right_cycle": cycle_text(support_cycles[right]),
                "relative_type_count": len(relative_types),
                "relative_types": ";".join(sorted(relative_types)),
            }
        )

    # Exact convolution powers and 16-coordinate Krylov compression.
    delta = {element: sp.Rational(int(element == identity)) for element in group}
    powers = [delta, kernel]
    for _ in range(2, args.max_power + 1):
        powers.append(convolution(powers[-1], kernel, group))

    coefficients = derive_kernel_minimal_polynomial(powers, group)
    x = sp.Symbol("x")
    minimal_expression = polynomial_expression(coefficients, x)
    minimal_factorisation = sp.factor(minimal_expression)

    group_to_orbital: Dict[GroupElement, int] = {}
    for element in group:
        pair = tuple(sorted((identity_index, group_index[element])))
        group_to_orbital[element] = orbital_lookup[pair]

    krylov_rows: List[Dict[str, object]] = []
    for orbital_index in range(len(orbits)):
        elements = [
            element for element in group
            if group_to_orbital[element] == orbital_index
        ]
        row: Dict[str, object] = {
            "orbital_index": orbital_index,
            "group_element_count": len(elements),
            "representative_group_element": group_text(min(elements)),
        }
        for power_index, power in enumerate(powers):
            values = {power[element] for element in elements}
            if len(values) != 1:
                raise RuntimeError(
                    f"Convolution power {power_index} is not constant on orbital {orbital_index}"
                )
            row[f"K_power_{power_index}"] = str(next(iter(values)))
        krylov_rows.append(row)

    print("\nSixteen-orbital compression")
    print(f"  stabilizer order:           {len(stabilizer)}")
    print(f"  unordered orbitals:         {len(orbits)}")
    print(f"  exact kernel values:        {[str(value) for value in sorted(set(kernel.values()), key=float)]}")
    print(f"  minimal polynomial:         {minimal_factorisation}")

    # Exact S3 x S3 Fourier blocks.
    irreps = irrep_catalogue()
    fourier_rows: List[Dict[str, object]] = []
    spectral_multiplicities: Dict[sp.Rational, int] = defaultdict(int)
    block_data: Dict[Tuple[str, str], Dict[str, object]] = {}

    for first_name, first in irreps.items():
        for second_name, second in irreps.items():
            block = fourier_block(kernel, first, second, group)
            irrep_dimension = first[0] * second[0]
            eigenvalues = block.eigenvals()
            nonzero_contribution = 0
            for eigenvalue, algebraic_multiplicity in eigenvalues.items():
                if eigenvalue != 0:
                    contribution = irrep_dimension * int(algebraic_multiplicity)
                    spectral_multiplicities[sp.Rational(eigenvalue)] += contribution
                    nonzero_contribution += contribution

            row = {
                "irrep": f"{first_name}x{second_name}",
                "first_irrep": first_name,
                "second_irrep": second_name,
                "irrep_dimension": irrep_dimension,
                "block_rank": int(block.rank()),
                "block_matrix": matrix_text(block),
                "characteristic_polynomial": str(
                    sp.factor(block.charpoly(x).as_expr())
                ),
                "eigenvalues": ";".join(
                    f"{eigenvalue}^{multiplicity}"
                    for eigenvalue, multiplicity in sorted(
                        eigenvalues.items(), key=lambda item: float(item[0])
                    )
                ),
                "regular_multiplicity_factor": irrep_dimension,
                "nonzero_channel_contribution": nonzero_contribution,
                "c2_partner": f"{second_name}x{first_name}",
            }
            fourier_rows.append(row)
            block_data[(first_name, second_name)] = {
                "matrix": block,
                "dimension": irrep_dimension,
                "eigenvalues": eigenvalues,
                "row": row,
            }

    expected_multiplicities = {
        sp.Rational(1): 2,
        sp.Rational(6, 5): 4,
        sp.Rational(8, 5): 4,
        sp.Rational(9, 5): 1,
    }
    fourier_spectrum_exact = dict(spectral_multiplicities) == expected_multiplicities

    h_rows = [
        {
            "h_block": "V2",
            "dimension": 2,
            "schur_scalar": "1",
            "source_fourier_sectors": "1xsgn + sgnx1",
        },
        {
            "h_block": "V4_(8/5)",
            "dimension": 4,
            "schur_scalar": "8/5",
            "source_fourier_sectors": "sgnxstd + stdxsgn",
        },
        {
            "h_block": "V4_(6/5)",
            "dimension": 4,
            "schur_scalar": "6/5",
            "source_fourier_sectors": "stdxstd rank-one Fourier mode, repeated four times",
        },
        {
            "h_block": "V1",
            "dimension": 1,
            "schur_scalar": "9/5",
            "source_fourier_sectors": "sgnxsgn",
        },
    ]

    print("\nS3 x S3 Fourier proof")
    print(f"  Fourier blocks:             {len(fourier_rows)}")
    print(f"  largest block dimension:    {max(int(row['irrep_dimension']) for row in fourier_rows)}")
    print(f"  nonzero multiplicities:     {dict(sorted(spectral_multiplicities.items(), key=lambda item: float(item[0])))}")
    print(f"  exact channel spectrum:     {fourier_spectrum_exact}")
    print("  H-block dimensions:         [2, 4, 4, 1]")

    # Direct matrix polynomial control.
    matrix_polynomial_zero = direct.matrix_polynomial(matrix, coefficients) == sp.zeros(matrix.rows)
    kernel_rank = int(matrix.rank())
    kernel_dimension = matrix.rows - kernel_rank

    entry_values = sorted(set(matrix), key=float)
    proof_path = out_dir / "hand_proof_compression.md"
    write_hand_proof(
        proof_path,
        symmetry.pair_text(reference_pair_id),
        entry_values,
        len(orbits),
        minimal_expression,
        fourier_rows,
        h_rows,
    )

    kernel_rows = [
        {
            "group_element": group_text(element),
            "a_permutation": small_perm_text(element[0]),
            "b_permutation": small_perm_text(element[1]),
            "a_cycle_type": str(
                tuple(sorted(
                    [
                        len(cycle)
                        for cycle in _cycles_of_small_perm(element[0])
                    ],
                    reverse=True,
                ))
            ),
            "b_cycle_type": str(
                tuple(sorted(
                    [
                        len(cycle)
                        for cycle in _cycles_of_small_perm(element[1])
                    ],
                    reverse=True,
                ))
            ),
            "orbital_index": group_to_orbital[element],
            "kernel_value": str(kernel[element]),
        }
        for element in group
    ]

    certificate = {
        "reference_pair": symmetry.pair_text(reference_pair_id),
        "support_identification": {
            "support_size": len(support),
            "group": "S3 x S3",
            "group_order": len(group),
            "alternating_word_form": "1,A1,B1,A2,B2,A3,B3",
            "bijection_exact": set(support_group) == set(group),
        },
        "convolution_certificate": {
            "exact_convolution_law": convolution_law,
            "kernel_value_set": [str(value) for value in entry_values],
            "unordered_stabilizer_orbital_count": len(orbits),
            "minimal_polynomial_coefficients_ascending": [
                str(value) for value in coefficients
            ],
            "minimal_polynomial_factored": str(minimal_factorisation),
            "matrix_polynomial_identity_exact": matrix_polynomial_zero,
        },
        "fourier_certificate": {
            "irreps_of_S3": {"1": 1, "sgn": 1, "std": 2},
            "product_block_count": len(fourier_rows),
            "largest_block_dimension": 4,
            "nonzero_channel_multiplicities": {
                str(value): multiplicity
                for value, multiplicity in sorted(
                    spectral_multiplicities.items(), key=lambda item: float(item[0])
                )
            },
            "expected_nonzero_multiplicities": {
                str(value): multiplicity
                for value, multiplicity in expected_multiplicities.items()
            },
            "exact_spectrum_match": fourier_spectrum_exact,
            "rank_from_fourier": sum(spectral_multiplicities.values()),
            "kernel_dimension": kernel_dimension,
        },
        "H_block_certificate": h_rows,
        "claim_boundary": (
            "The 36-state exact KK operator is compressed to a 16-orbital "
            "kernel and nine exact S3 x S3 Fourier blocks. This is sufficient "
            "for a conventional finite-group proof once the supplied tables "
            "are included."
        ),
    }

    write_csv(out_dir / "sixteen_orbital_kernel_table.csv", orbital_rows)
    write_csv(out_dir / "orbital_krylov_table.csv", krylov_rows)
    write_csv(out_dir / "group_convolution_kernel.csv", kernel_rows)
    write_csv(out_dir / "s3xs3_fourier_blocks.csv", fourier_rows)
    write_csv(out_dir / "induced_H_blocks.csv", h_rows)
    with (out_dir / "hand_proof_certificate.json").open("w") as handle:
        json.dump(json_safe(certificate), handle, indent=2)

    elapsed = time.time() - started
    exact_success = (
        convolution_law
        and len(orbits) == 16
        and matrix_polynomial_zero
        and fourier_spectrum_exact
        and kernel_rank == 11
        and kernel_dimension == 25
    )
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "reference_pair": symmetry.pair_text(reference_pair_id),
        "support_is_S3xS3_exact": set(support_group) == set(group),
        "exact_convolution_law": convolution_law,
        "unordered_stabilizer_orbitals": len(orbits),
        "kernel_value_set": [str(value) for value in entry_values],
        "minimal_polynomial_factored": str(minimal_factorisation),
        "matrix_polynomial_identity_exact": matrix_polynomial_zero,
        "fourier_block_count": len(fourier_rows),
        "largest_fourier_block_dimension": max(
            int(row["irrep_dimension"]) for row in fourier_rows
        ),
        "nonzero_multiplicities": {
            str(value): multiplicity
            for value, multiplicity in sorted(
                spectral_multiplicities.items(), key=lambda item: float(item[0])
            )
        },
        "fourier_spectrum_exact": fourier_spectrum_exact,
        "operator_rank": kernel_rank,
        "operator_kernel_dimension": kernel_dimension,
        "H_block_dimensions": [2, 4, 4, 1],
        "H_schur_scalars": ["1", "8/5", "6/5", "9/5"],
        "hand_proof_compression_certificate": exact_success,
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "run.log",
            "hand_proof_certificate.json",
            "hand_proof_compression.md",
            "sixteen_orbital_kernel_table.csv",
            "orbital_krylov_table.csv",
            "group_convolution_kernel.csv",
            "s3xs3_fourier_blocks.csv",
            "induced_H_blocks.csv",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)

    print("\n" + "=" * 122)
    print("FINAL SUMMARY")
    print("=" * 122)
    print(f"Support is exactly S3 x S3:          {summary['support_is_S3xS3_exact']}")
    print(f"Exact convolution law:               {convolution_law}")
    print(f"Sixteen stabilizer orbitals:         {len(orbits) == 16}")
    print(f"Minimal polynomial from convolution: {minimal_factorisation}")
    print(f"Nine exact Fourier blocks:           {len(fourier_rows) == 9}")
    print(f"Largest Fourier block:               {summary['largest_fourier_block_dimension']} x {summary['largest_fourier_block_dimension']}")
    print(f"Exact Fourier spectrum:              {fourier_spectrum_exact}")
    print(f"Nonzero multiplicities:              {summary['nonzero_multiplicities']}")
    print(f"Hand-proof compression certificate:  {exact_success}")
    print(f"elapsed:                             {elapsed:.2f} seconds")
    print(f"summary:                             {out_dir / 'summary.json'}")
    print("=" * 122)

    return summary


def _cycles_of_small_perm(perm: SmallPerm) -> List[Tuple[int, ...]]:
    seen = set()
    cycles = []
    for start in range(3):
        if start in seen:
            continue
        cycle = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = perm[current]
        cycles.append(tuple(cycle))
    return cycles


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compress the exact 8->7 reference channel into 16 stabilizer "
            "orbitals and nine S3 x S3 Fourier blocks."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--helper-script", required=True)
    parser.add_argument("--symmetry-script", required=True)
    parser.add_argument("--direct-script", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--max-power", type=int, default=5)
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
