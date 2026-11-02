#!/usr/bin/env python3
"""
EHF-AMP-FOUND-03G: Parameterised Shuffle--Antisymmetriser Templates
===================================================================

03F proved every minimum-support signed-orbit relation directly in the exact
720-dimensional eight-point Kleiss--Kuijf basis. 03G compresses those 720
coordinate equations into a single character-parameterised matrix over the
group ring of

    G = <(2 3),(5 6),(7 8)> ~= C2^3.

Let x=(x1,x2,x3), with xi^2=1.  For a reference target-state orbit Oj with
representative wj, and a KK basis coordinate sigma, define

    P_{sigma,j}(x)
      = sum_{h in C2^3} Q8[sigma, h.wj] x^h.

For a sign character chi=(chi1,chi2,chi3), evaluation xi=chii gives the KK
coordinate of the raw character antisymmetriser applied to wj.  Primitive
orbit normalisation then gives the exact character-reduced matrix

    M_chi = Q8 A_chi^T.

The 720 universal polynomial rows contain only 144 nonzero rows.  Up to an
overall integer scalar and multiplication by a group monomial x^h, those 144
rows collapse to exactly 21 primitive universal shuffle templates, with
multiplicity distribution

    16^3, 8^6, 4^12.

The script proves:

1. every nonzero universal KK row is reconstructed exactly from one of the
   21 templates;
2. for every sign character chi, the 21 specialised template rows have the
   same exact row space and kernel as M_chi;
3. all character nullities and the complete 9 -> 8 tail lattice are recovered;
4. all 15 minimum-support quotient-character relations satisfy the 21
   parameterised template equations;
5. the support profiles and total atom count 79 are unchanged.

This is a finite group-ring formula extraction.  It replaces 720 separate
KK-coordinate cancellations by 21 universal polynomial identities.  It is
not yet a one-line closed shuffle theorem.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_03g_parameterised_shuffle_antisymmetriser_templates.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --derivation-script scripts/ehf_amp_found_03f_direct_kk_shuffle_signed_orbit_derivation.py \
  --out-dir runs/ehf_amp_found_03g \
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
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

Cycle = Tuple[int, ...]
Subset = Tuple[int, int, int]
GroupElement = Tuple[int, int, int]
SignTriple = Tuple[int, int, int]
PolynomialRow = Tuple[int, ...]


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


def group_text(element: GroupElement) -> str:
    labels = []
    for index, power in enumerate(element, start=1):
        if power:
            labels.append(f"x{index}")
    return "1" if not labels else "*".join(labels)


def cycle_text(cycle: Sequence[int]) -> str:
    return ",".join(map(str, cycle))


def xor(left: GroupElement, right: GroupElement) -> GroupElement:
    return tuple(a ^ b for a, b in zip(left, right))  # type: ignore[return-value]


def character_value(signs: SignTriple, element: GroupElement) -> int:
    value = 1
    for sign, power in zip(signs, element):
        if power:
            value *= sign
    return value


def primitive_integer_values(values: Sequence[int]) -> Tuple[int, ...]:
    if not any(values):
        return tuple(int(value) for value in values)
    gcd_value = 0
    for value in values:
        gcd_value = math.gcd(gcd_value, abs(int(value)))
    output = [int(value) // gcd_value for value in values]
    first_nonzero = next(value for value in output if value)
    if first_nonzero < 0:
        output = [-value for value in output]
    return tuple(output)


def monomial_shift(
    row: Sequence[int],
    shift: GroupElement,
    group_elements: Sequence[GroupElement],
    orbit_count: int,
) -> Tuple[int, ...]:
    index = {element: position for position, element in enumerate(group_elements)}
    output: List[int] = []
    group_size = len(group_elements)
    for orbit_index in range(orbit_count):
        block = row[
            orbit_index * group_size : (orbit_index + 1) * group_size
        ]
        for element in group_elements:
            output.append(block[index[xor(element, shift)]])
    return tuple(output)


def canonical_template(
    raw_row: Sequence[int],
    group_elements: Sequence[GroupElement],
    orbit_count: int,
) -> Tuple[PolynomialRow, int, GroupElement]:
    """
    Return canonical, scalar, shift satisfying

        raw_row = scalar * shift(canonical, shift).

    The canonical row is primitive, sign-normalised, and lexicographically
    minimal over all group-monomial shifts.
    """
    raw = tuple(int(value) for value in raw_row)
    if not any(raw):
        return raw, 0, (0, 0, 0)

    gcd_value = 0
    for value in raw:
        gcd_value = math.gcd(gcd_value, abs(value))
    primitive = tuple(value // gcd_value for value in raw)

    candidates: List[Tuple[PolynomialRow, int, GroupElement]] = []
    for shift in group_elements:
        shifted = monomial_shift(
            primitive,
            shift,
            group_elements,
            orbit_count,
        )
        first_nonzero = next(value for value in shifted if value)
        sign = 1 if first_nonzero > 0 else -1
        normalised = tuple(sign * value for value in shifted)
        # canonical = sign * shift(primitive, shift)
        # primitive = sign * shift(canonical, shift), since shift^2=1.
        scalar = gcd_value * sign
        candidates.append((normalised, scalar, shift))

    canonical, scalar, shift = min(candidates, key=lambda item: item[0])
    reconstructed = tuple(
        scalar * value
        for value in monomial_shift(
            canonical,
            shift,
            group_elements,
            orbit_count,
        )
    )
    if reconstructed != raw:
        raise RuntimeError("Universal template reconstruction failed")
    return canonical, scalar, shift


def polynomial_notation(
    coefficients: Sequence[int],
    group_elements: Sequence[GroupElement],
) -> str:
    terms: List[str] = []
    for coefficient, element in zip(coefficients, group_elements):
        coefficient = int(coefficient)
        if coefficient == 0:
            continue
        monomial = group_text(element)
        if monomial == "1":
            body = str(abs(coefficient))
        elif abs(coefficient) == 1:
            body = monomial
        else:
            body = f"{abs(coefficient)}*{monomial}"
        if not terms:
            terms.append(body if coefficient > 0 else f"-{body}")
        else:
            terms.append(
                f"+ {body}" if coefficient > 0 else f"- {body}"
            )
    return "0" if not terms else " ".join(terms)


def evaluate_polynomial_block(
    coefficients: Sequence[int],
    signs: SignTriple,
    group_elements: Sequence[GroupElement],
) -> int:
    return sum(
        int(coefficient) * character_value(signs, element)
        for coefficient, element in zip(coefficients, group_elements)
    )


def raw_to_primitive_scale(
    raw: sp.Matrix,
    primitive: sp.Matrix,
) -> int:
    if not any(value != 0 for value in raw):
        raise ValueError("Raw orbit vector is zero")
    if not any(value != 0 for value in primitive):
        raise ValueError("Primitive orbit vector is zero")
    ratio = None
    for raw_value, primitive_value in zip(list(raw), list(primitive)):
        if primitive_value == 0:
            if raw_value != 0:
                raise RuntimeError("Raw and primitive orbit supports differ")
            continue
        current = sp.Rational(raw_value, primitive_value)
        if ratio is None:
            ratio = current
        elif ratio != current:
            raise RuntimeError("Raw orbit is not a scalar multiple of primitive")
    if ratio is None or ratio.q != 1:
        raise RuntimeError("Unexpected nonintegral orbit normalisation")
    if raw != int(ratio) * primitive:
        raise RuntimeError("Orbit normalisation check failed")
    return int(ratio)


def universal_polynomial_rows(
    q8: sp.Matrix,
    orbit_representatives: Sequence[int],
    group_destinations: Sequence[Sequence[int]],
) -> List[PolynomialRow]:
    rows: List[PolynomialRow] = []
    for kk_row in range(q8.rows):
        values: List[int] = []
        for representative in orbit_representatives:
            for destination in group_destinations:
                values.append(int(q8[kk_row, destination[representative]]))
        rows.append(tuple(values))
    return rows


def specialise_templates(
    templates: Sequence[PolynomialRow],
    signs: SignTriple,
    group_elements: Sequence[GroupElement],
    orbit_count: int,
    admissible_orbits: Sequence[int],
    normalisation_scales: Mapping[int, int],
) -> sp.Matrix:
    group_size = len(group_elements)
    rows: List[List[sp.Rational]] = []
    for template in templates:
        row: List[sp.Rational] = []
        for orbit_index in admissible_orbits:
            block = template[
                orbit_index * group_size : (orbit_index + 1) * group_size
            ]
            raw_value = evaluate_polynomial_block(
                block,
                signs,
                group_elements,
            )
            scale = normalisation_scales[orbit_index]
            row.append(sp.Rational(raw_value, scale))
        rows.append(row)
    return sp.Matrix(rows)


def write_template_markdown(
    path: Path,
    template_rows: Sequence[Mapping[str, object]],
    character_rows: Sequence[Mapping[str, object]],
    direction_rows: Sequence[Mapping[str, object]],
) -> None:
    lines = [
        "# EHF-AMP-FOUND-03G",
        "## Parameterised shuffle--antisymmetriser templates",
        "",
        "Let",
        "",
        r"\[G=\langle(2\,3),(5\,6),(7\,8)\rangle\cong C_2^3,\]",
        "",
        r"and let \(x_i^2=1\). For target-state orbit representative \(w_j\),",
        "",
        r"\[P_{\sigma j}(x)=\sum_{h\in G}"
        r"Q_8[\sigma,h\!\cdot\!w_j]x^h.\]",
        "",
        "Every nonzero KK-coordinate row is an integer scalar and group-monomial "
        "multiple of one of the 21 templates below.",
        "",
        "## Universal template census",
        "",
        "| Template | KK-row multiplicity | Nonzero orbit polynomials |",
        "|---|---:|---|",
    ]
    for row in template_rows:
        lines.append(
            f"| {row['template_id']} | {row['kk_row_multiplicity']} | "
            f"`{row['compact_polynomial_row']}` |"
        )

    lines.extend([
        "",
        "## Character specialisations",
        "",
        "| Character | Primitive atoms | Direct KK rank | Template rank | "
        "Kernel nullity | Exact row-space equality |",
        "|---|---:|---:|---:|---:|---|",
    ])
    for row in character_rows:
        lines.append(
            f"| `{row['character']}` | {row['primitive_atom_dimension']} | "
            f"{row['direct_KK_rank']} | {row['template_rank']} | "
            f"{row['kernel_nullity']} | "
            f"{'yes' if row['exact_rowspace_equality'] else 'no'} |"
        )

    lines.extend([
        "",
        r"For character \(\chi\), every signed-orbit relation coefficient row "
        r"\(c\) is proved by the 21 equations",
        "",
        r"\[\sum_j c_j\,P_{tj}(\chi)/s_{\chi j}=0,"
        r"\qquad t=1,\ldots,21,\]",
        "",
        r"where \(s_{\chi j}\) is the primitive-orbit normalisation.",
        "",
        "## Tail-filtration directions",
        "",
        "| Layer | Character | Direction | Atom support | "
        "Nontrivial template checks | All 21 equations |",
        "|---|---|---:|---:|---:|---|",
    ])
    for row in direction_rows:
        lines.append(
            f"| {row['layer_id']} | `{row['character']}` | "
            f"{row['direction_index']} | {row['atom_support_count']} | "
            f"{row['nontrivial_template_equation_count']} | "
            f"{'exact' if row['all_template_equations_zero'] else 'failed'} |"
        )

    lines.extend([
        "",
        "The 720-coordinate direct KK proof therefore factors through a "
        "21-row matrix over the group ring "
        r"\(\mathbb Z[C_2^3]\).",
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
    derivation_script = Path(args.derivation_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_03g_base")
    helper = load_module(helper_script, "ehf_amp_found_03g_helper")
    rank_module = load_module(rank_script, "ehf_amp_found_03g_rank")
    direct = load_module(direct_script, "ehf_amp_found_03g_direct")
    normal = load_module(normal_script, "ehf_amp_found_03g_normal")
    derivation = load_module(
        derivation_script,
        "ehf_amp_found_03g_derivation",
    )

    source_fibres = base.fibres(9)
    target_fibres = base.fibres(8)
    reference_subset: Subset = (2, 3, 4)
    reference_key = rank_module.key_from_subset_8(reference_subset)
    reference_states: List[Cycle] = target_fibres[reference_key]

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
    q8_kernel = normal.canonical_rowspace(
        DomainMatrix.from_Matrix(q8)
        .convert_to(QQ)
        .nullspace()
        .to_Matrix()
    )

    kk9_permutations = list(itertools.permutations(range(2, 9)))
    kk9_index = {
        permutation: index
        for index, permutation in enumerate(kk9_permutations)
    }

    print("=" * 126)
    print("EHF-AMP-FOUND-03G: PARAMETERISED SHUFFLE--ANTISYMMETRISER TEMPLATES")
    print("=" * 126)
    print(f"base script:                 {base_script}")
    print(f"reflection-aware helper:     {helper_script}")
    print(f"exact 9->8 rank helper:      {rank_script}")
    print(f"exact KK helper:             {direct_script}")
    print(f"normal-form utilities:       {normal_script}")
    print(f"03F derivation utilities:    {derivation_script}")
    print(f"output directory:            {out_dir}")
    print("coefficient domain:          QQ")
    print("universal coefficient ring:  Z[x1,x2,x3]/(xi^2-1)")

    generator_specs = [
        ("g1=(2 3)", {2: 3, 3: 2}),
        ("g2=(5 6)", {5: 6, 6: 5}),
        ("g3=(7 8)", {7: 8, 8: 7}),
    ]
    generators: List[sp.Matrix] = []
    for _, mapping in generator_specs:
        destination = normal.target_action_destination(
            base,
            reference_states,
            mapping,
        )
        generators.append(normal.permutation_matrix(destination))

    group_elements: List[GroupElement] = list(
        itertools.product((0, 1), repeat=3)
    )
    identity = sp.eye(len(reference_states))
    group_matrices: List[sp.Matrix] = []
    group_destinations: List[List[int]] = []
    for element in group_elements:
        matrix = identity
        for power, generator in zip(element, generators):
            if power:
                matrix = matrix * generator
        group_matrices.append(matrix)
        group_destinations.append([
            next(
                row
                for row in range(len(reference_states))
                if matrix[row, column] == 1
            )
            for column in range(len(reference_states))
        ])

    commuting_involutions = all(
        generator * generator == identity
        for generator in generators
    ) and all(
        generators[left] * generators[right]
        == generators[right] * generators[left]
        for left in range(3)
        for right in range(left + 1, 3)
    )

    state_orbits = normal.state_orbits(
        len(reference_states),
        group_destinations,
    )
    orbit_representatives = [min(orbit) for orbit in state_orbits]
    orbit_distribution = Counter(len(orbit) for orbit in state_orbits)
    orbit_count = len(state_orbits)

    universal_rows = universal_polynomial_rows(
        q8,
        orbit_representatives,
        group_destinations,
    )
    nonzero_kk_rows = [
        index for index, row in enumerate(universal_rows) if any(row)
    ]

    template_to_rows: MutableMapping[PolynomialRow, List[int]] = defaultdict(list)
    row_map_rows: List[Dict[str, object]] = []
    canonical_records: Dict[int, Tuple[PolynomialRow, int, GroupElement]] = {}

    for kk_row in nonzero_kk_rows:
        canonical, scalar, shift = canonical_template(
            universal_rows[kk_row],
            group_elements,
            orbit_count,
        )
        canonical_records[kk_row] = (canonical, scalar, shift)
        template_to_rows[canonical].append(kk_row)

    templates = sorted(template_to_rows)
    template_ids = {
        template: f"T{index:02d}"
        for index, template in enumerate(templates, start=1)
    }

    universal_reconstruction = True
    for kk_row in range(q8.rows):
        if kk_row not in canonical_records:
            row_map_rows.append({
                "kk_row_index": kk_row,
                "kk_basis_ordering": (
                    "1," + cycle_text(kk8_permutations[kk_row]) + ",8"
                ),
                "zero_universal_row": True,
                "template_id": "",
                "integer_scalar": 0,
                "group_monomial_shift": "",
                "exact_reconstruction": True,
            })
            continue
        template, scalar, shift = canonical_records[kk_row]
        reconstructed = tuple(
            scalar * value
            for value in monomial_shift(
                template,
                shift,
                group_elements,
                orbit_count,
            )
        )
        exact = reconstructed == universal_rows[kk_row]
        universal_reconstruction &= exact
        row_map_rows.append({
            "kk_row_index": kk_row,
            "kk_basis_ordering": (
                "1," + cycle_text(kk8_permutations[kk_row]) + ",8"
            ),
            "zero_universal_row": False,
            "template_id": template_ids[template],
            "integer_scalar": scalar,
            "group_monomial_shift": group_text(shift),
            "exact_reconstruction": exact,
        })

    write_csv(
        out_dir / "kk_coordinate_to_universal_template_map.csv",
        row_map_rows,
    )

    template_rows: List[Dict[str, object]] = []
    template_polynomial_rows: List[Dict[str, object]] = []
    group_size = len(group_elements)

    for template in templates:
        template_id = template_ids[template]
        compact_parts: List[str] = []
        for orbit_index in range(orbit_count):
            block = template[
                orbit_index * group_size : (orbit_index + 1) * group_size
            ]
            notation = polynomial_notation(block, group_elements)
            if notation != "0":
                compact_parts.append(f"O{orbit_index + 1:02d}:{notation}")
            template_polynomial_rows.append({
                "template_id": template_id,
                "orbit_id": f"O{orbit_index + 1:02d}",
                "orbit_size": len(state_orbits[orbit_index]),
                "orbit_representative_state_index": (
                    orbit_representatives[orbit_index]
                ),
                "orbit_representative_cycle": cycle_text(
                    reference_states[orbit_representatives[orbit_index]]
                ),
                "group_ring_polynomial": notation,
                **{
                    f"coefficient_{group_text(element)}": block[position]
                    for position, element in enumerate(group_elements)
                },
            })
        template_rows.append({
            "template_id": template_id,
            "kk_row_multiplicity": len(template_to_rows[template]),
            "representative_kk_row_index": min(template_to_rows[template]),
            "representative_kk_basis_ordering": (
                "1,"
                + cycle_text(
                    kk8_permutations[min(template_to_rows[template])]
                )
                + ",8"
            ),
            "nonzero_orbit_polynomial_count": len(compact_parts),
            "compact_polynomial_row": " | ".join(compact_parts),
        })

    write_csv(
        out_dir / "universal_shuffle_template_catalog.csv",
        template_rows,
    )
    write_csv(
        out_dir / "universal_shuffle_template_polynomials.csv",
        template_polynomial_rows,
    )

    expected_nullities = {
        "+++": 0,
        "++-": 1,
        "+-+": 1,
        "+--": 3,
        "-++": 1,
        "-+-": 3,
        "--+": 3,
        "---": 3,
    }
    expected_ranks = {
        "+++": 10,
        "++-": 7,
        "+-+": 7,
        "+--": 7,
        "-++": 7,
        "-+-": 7,
        "--+": 7,
        "---": 5,
    }

    atom_vectors: Dict[SignTriple, List[sp.Matrix]] = {}
    atom_ids: Dict[SignTriple, List[str]] = {}
    direct_matrices: Dict[SignTriple, sp.Matrix] = {}
    template_matrices: Dict[SignTriple, sp.Matrix] = {}
    character_rows: List[Dict[str, object]] = []

    all_specialisations_exact = True
    all_rowspaces_equal = True
    all_character_ranks = True
    all_character_nullities = True

    for signs in itertools.product((1, -1), repeat=3):
        vectors: List[sp.Matrix] = []
        identifiers: List[str] = []
        admissible_orbits: List[int] = []
        normalisation_scales: Dict[int, int] = {}

        for orbit_index, representative in enumerate(orbit_representatives):
            raw = sp.zeros(1, len(reference_states))
            for element, destination in zip(
                group_elements,
                group_destinations,
            ):
                raw[0, destination[representative]] += character_value(
                    signs,
                    element,
                )
            primitive = normal.signed_orbit_atom(
                representative,
                signs,
                group_elements,
                group_destinations,
                len(reference_states),
            )
            if not any(value != 0 for value in primitive):
                if any(value != 0 for value in raw):
                    raise RuntimeError(
                        "Primitive atom vanished while raw atom did not"
                    )
                continue
            scale = raw_to_primitive_scale(raw, primitive)
            vectors.append(primitive)
            identifiers.append(
                f"Omega_{sign_text(signs)}_O{orbit_index + 1:02d}"
            )
            admissible_orbits.append(orbit_index)
            normalisation_scales[orbit_index] = scale

        atom_basis = sp.Matrix.vstack(*vectors)
        direct_matrix = sp.Matrix(q8 * atom_basis.T)
        template_matrix = specialise_templates(
            templates,
            signs,
            group_elements,
            orbit_count,
            admissible_orbits,
            normalisation_scales,
        )

        direct_rowspace = normal.canonical_rowspace(direct_matrix)
        template_rowspace = normal.canonical_rowspace(template_matrix)
        rowspace_equal = direct_rowspace == template_rowspace
        all_rowspaces_equal &= rowspace_equal

        direct_rank = int(
            DomainMatrix.from_Matrix(direct_matrix).convert_to(QQ).rank()
        )
        template_rank = int(
            DomainMatrix.from_Matrix(template_matrix).convert_to(QQ).rank()
        )
        direct_kernel = normal.canonical_rowspace(
            DomainMatrix.from_Matrix(direct_matrix)
            .convert_to(QQ)
            .nullspace()
            .to_Matrix()
        )
        template_kernel = normal.canonical_rowspace(
            DomainMatrix.from_Matrix(template_matrix)
            .convert_to(QQ)
            .nullspace()
            .to_Matrix()
        )
        kernel_equal = direct_kernel == template_kernel
        all_specialisations_exact &= kernel_equal

        character = sign_text(signs)
        rank_match = (
            direct_rank == expected_ranks[character]
            and template_rank == expected_ranks[character]
        )
        nullity_match = (
            direct_kernel.rows == expected_nullities[character]
            and template_kernel.rows == expected_nullities[character]
        )
        all_character_ranks &= rank_match
        all_character_nullities &= nullity_match

        atom_vectors[signs] = vectors
        atom_ids[signs] = identifiers
        direct_matrices[signs] = direct_matrix
        template_matrices[signs] = template_matrix

        character_rows.append({
            "character": character,
            "primitive_atom_dimension": atom_basis.rows,
            "direct_KK_rank": direct_rank,
            "template_rank": template_rank,
            "expected_rank": expected_ranks[character],
            "rank_match": rank_match,
            "kernel_nullity": direct_kernel.rows,
            "template_kernel_nullity": template_kernel.rows,
            "expected_kernel_nullity": expected_nullities[character],
            "nullity_match": nullity_match,
            "nonzero_specialised_template_rows": sum(
                any(template_matrix[row, column] != 0
                    for column in range(template_matrix.cols))
                for row in range(template_matrix.rows)
            ),
            "exact_rowspace_equality": rowspace_equal,
            "exact_kernel_equality": kernel_equal,
        })

    write_csv(
        out_dir / "character_specialised_template_summary.csv",
        character_rows,
    )

    spaces = derivation.build_direct_tail_spaces(
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
    expected_dimensions = {
        "V0": 0,
        "V2": 2,
        "V3": 3,
        "V8": 8,
        "V9": 9,
        "V14": 14,
        "V15": 15,
    }
    dimensions_match = all(
        spaces[name].rows == dimension
        for name, dimension in expected_dimensions.items()
    )
    lattice_checks = {
        "V2_subset_V3": normal.is_subspace(spaces["V2"], spaces["V3"]),
        "V3_subset_V8": normal.is_subspace(spaces["V3"], spaces["V8"]),
        "V3_subset_V9": normal.is_subspace(spaces["V3"], spaces["V9"]),
        "V14_equals_V8_plus_V9": (
            spaces["V14"]
            == normal.rowspace_sum(spaces["V8"], spaces["V9"])
        ),
        "V15_equals_Q8_kernel": spaces["V15"] == q8_kernel,
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

    direction_rows: List[Dict[str, object]] = []
    equation_rows: List[Dict[str, object]] = []
    all_template_equations = True
    all_profiles_match = True
    all_quotients_reconstructed = True
    total_atom_count = 0
    direction_count = 0

    for layer_id, quotient_name, lower_name, upper_name in layers:
        lower_space = spaces[lower_name]
        upper_space = spaces[upper_name]

        for signs in itertools.product((1, -1), repeat=3):
            lower_character = normal.character_part(
                lower_space,
                generators,
                signs,
            )
            upper_character = normal.character_part(
                upper_space,
                generators,
                signs,
            )
            multiplicity = upper_character.rows - lower_character.rows
            if multiplicity == 0:
                continue

            atom_basis = sp.Matrix.vstack(*atom_vectors[signs])
            to_coordinates = normal.coordinate_map(atom_basis)
            lower_coordinates = normal.canonical_rowspace(
                to_coordinates(lower_character)
            )
            upper_coordinates = normal.canonical_rowspace(
                to_coordinates(upper_character)
            )

            selected, support_profile = (
                normal.exhaustive_minimum_quotient_basis(
                    upper_coordinates,
                    lower_coordinates,
                )
            )
            expected_profile = expected_profiles[
                (layer_id, sign_text(signs))
            ]
            profile_match = tuple(support_profile) == tuple(expected_profile)
            all_profiles_match &= profile_match

            reconstructed = normal.rowspace_sum(
                lower_coordinates,
                *selected,
            )
            reconstruction_ok = (
                reconstructed.rows == upper_coordinates.rows
            )
            all_quotients_reconstructed &= reconstruction_ok

            template_matrix = template_matrices[signs]

            for direction_index, coefficient_row in enumerate(
                selected,
                start=1,
            ):
                residual = template_matrix * coefficient_row.T
                all_zero = residual == sp.zeros(template_matrix.rows, 1)
                all_template_equations &= all_zero

                nontrivial_count = 0
                for template_index, template in enumerate(templates):
                    contributions: List[str] = []
                    total = 0
                    for atom_index, coefficient in enumerate(
                        list(coefficient_row)
                    ):
                        coefficient = int(coefficient)
                        matrix_value = template_matrix[
                            template_index,
                            atom_index,
                        ]
                        if coefficient == 0 or matrix_value == 0:
                            continue
                        product = sp.Rational(coefficient) * matrix_value
                        contributions.append(
                            f"{atom_ids[signs][atom_index]}:"
                            f"{coefficient}*{matrix_value}={product}"
                        )
                        total += product
                    if contributions:
                        nontrivial_count += 1
                        equation_rows.append({
                            "direction_id": (
                                f"{layer_id}_{sign_text(signs)}_"
                                f"d{direction_index}"
                            ),
                            "layer_id": layer_id,
                            "character": sign_text(signs),
                            "direction_index": direction_index,
                            "template_id": template_ids[template],
                            "contributions": ";".join(contributions),
                            "net_coefficient": str(total),
                            "exact_zero": total == 0,
                        })
                        all_template_equations &= total == 0

                support_count = sum(
                    coefficient != 0 for coefficient in coefficient_row
                )
                total_atom_count += support_count
                direction_count += 1
                direction_rows.append({
                    "direction_id": (
                        f"{layer_id}_{sign_text(signs)}_"
                        f"d{direction_index}"
                    ),
                    "layer_id": layer_id,
                    "quotient": quotient_name,
                    "character": sign_text(signs),
                    "direction_index": direction_index,
                    "quotient_character_multiplicity": multiplicity,
                    "atom_support_count": support_count,
                    "expected_atom_support": (
                        expected_profile[direction_index - 1]
                    ),
                    "support_match": (
                        support_count
                        == expected_profile[direction_index - 1]
                    ),
                    "nontrivial_template_equation_count": nontrivial_count,
                    "all_template_equations_zero": all_zero,
                    "atom_expression": normal.atom_expression(
                        coefficient_row,
                        atom_ids[signs],
                    ),
                })

            print(
                f"  {layer_id:3s} chi={sign_text(signs)} "
                f"mult={multiplicity} profile={support_profile} "
                f"templates=True"
            )

    write_csv(
        out_dir / "template_derived_signed_orbit_relations.csv",
        direction_rows,
    )
    write_csv(
        out_dir / "template_equation_cancellation_certificate.csv",
        equation_rows,
    )

    write_template_markdown(
        out_dir / "parameterised_shuffle_template_derivation.md",
        template_rows,
        character_rows,
        direction_rows,
    )

    multiplicity_distribution = Counter(
        len(template_to_rows[template]) for template in templates
    )
    expected_template_multiplicity_distribution = {4: 12, 8: 6, 16: 3}
    expected_orbit_distribution = {4: 2, 8: 8}
    expected_direction_count = 15
    expected_atom_count = 79

    exact_certificate = (
        commuting_involutions
        and dict(sorted(orbit_distribution.items()))
        == expected_orbit_distribution
        and len(nonzero_kk_rows) == 144
        and len(templates) == 21
        and dict(sorted(multiplicity_distribution.items()))
        == expected_template_multiplicity_distribution
        and universal_reconstruction
        and all_specialisations_exact
        and all_rowspaces_equal
        and all_character_ranks
        and all_character_nullities
        and dimensions_match
        and all(lattice_checks.values())
        and all_profiles_match
        and all_quotients_reconstructed
        and all_template_equations
        and direction_count == expected_direction_count
        and total_atom_count == expected_atom_count
    )

    verdict = (
        "EHF_AMP_FOUND_03G_EXACT_21_TEMPLATE_GROUP_RING_DERIVATION_PROVED"
        if exact_certificate
        else "EHF_AMP_FOUND_03G_PARAMETERISED_TEMPLATE_EXTRACTION_FAILED"
    )

    certificate = {
        "theorem": (
            "The exact 720-coordinate n=8 KK-shuffle proof of the fixed-anchor "
            "9->8 signed-orbit tail-filtration relations factors through 21 "
            "primitive rows over Z[C2^3]."
        ),
        "universal_formula": (
            "P_{sigma,j}(x)=sum_{h in C2^3} "
            "Q8[sigma,h.w_j] x^h, with x_i^2=1"
        ),
        "equivalence": (
            "Rows are identified up to an overall integer scalar and "
            "multiplication by a group monomial x^h."
        ),
        "universal_census": {
            "KK_coordinate_count": 720,
            "nonzero_universal_rows": len(nonzero_kk_rows),
            "primitive_template_count": len(templates),
            "template_multiplicity_distribution": dict(
                sorted(multiplicity_distribution.items())
            ),
        },
        "character_specialisation": (
            "Evaluate x_i=chi_i and divide each orbit column by its primitive "
            "raw-to-atom normalisation s_{chi,j}. The resulting 21-row matrix "
            "has exactly the same row space and kernel as M_chi=Q8 A_chi^T."
        ),
        "character_ranks": {
            row["character"]: row["template_rank"]
            for row in character_rows
        },
        "character_nullities": {
            row["character"]: row["kernel_nullity"]
            for row in character_rows
        },
        "tail_lattice_dimensions": {
            name: spaces[name].rows for name in expected_dimensions
        },
        "quotient_character_direction_count": direction_count,
        "minimum_atom_count": total_atom_count,
        "checks": {
            "universal_row_reconstruction": universal_reconstruction,
            "all_character_rowspaces_equal": all_rowspaces_equal,
            "all_character_kernels_equal": all_specialisations_exact,
            "tail_lattice_reconstructed": (
                dimensions_match and all(lattice_checks.values())
            ),
            "all_minimum_profiles_match": all_profiles_match,
            "all_21_template_equations_exact": all_template_equations,
        },
        "interpretation": (
            "The character antisymmetriser and the KK shuffle map combine into "
            "a 21-template group-ring operator. The 720 coordinate equations "
            "are repeated monomial/scalar copies of these templates."
        ),
        "claim_boundary": (
            "This is an exact parameterised finite template theorem. It does "
            "not yet classify the 21 templates by a shorter combinatorial "
            "formula, derive a single closed identity for arbitrary n, prove "
            "anchor independence, or demonstrate phenomenological utility."
        ),
    }
    with (
        out_dir / "exact_parameterised_shuffle_template_certificate.json"
    ).open("w") as handle:
        json.dump(json_safe(certificate), handle, indent=2)

    elapsed = time.time() - started
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "universal_KK_coordinate_count": q8.rows,
        "nonzero_universal_KK_rows": len(nonzero_kk_rows),
        "primitive_group_ring_template_count": len(templates),
        "template_multiplicity_distribution": dict(
            sorted(multiplicity_distribution.items())
        ),
        "all_universal_rows_reconstructed": universal_reconstruction,
        "all_character_rowspaces_equal": all_rowspaces_equal,
        "all_character_kernels_equal": all_specialisations_exact,
        "tail_lattice_reconstructed": (
            dimensions_match and all(lattice_checks.values())
        ),
        "quotient_character_direction_count": direction_count,
        "total_minimum_signed_orbit_atom_count": total_atom_count,
        "all_template_equations_exact": all_template_equations,
        "exact_21_template_group_ring_derivation": exact_certificate,
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "exact_parameterised_shuffle_template_certificate.json",
            "universal_shuffle_template_catalog.csv",
            "universal_shuffle_template_polynomials.csv",
            "kk_coordinate_to_universal_template_map.csv",
            "character_specialised_template_summary.csv",
            "template_derived_signed_orbit_relations.csv",
            "template_equation_cancellation_certificate.csv",
            "parameterised_shuffle_template_derivation.md",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)
    with (out_dir / "verdict.json").open("w") as handle:
        json.dump(
            {
                "verdict": verdict,
                "exact_21_template_group_ring_derivation": (
                    exact_certificate
                ),
                "template_count": len(templates),
                "direction_count": direction_count,
            },
            handle,
            indent=2,
        )

    strict_failures: List[str] = []
    if args.strict:
        checks = {
            "commuting_C2cubed": commuting_involutions,
            "state_orbit_distribution": (
                dict(sorted(orbit_distribution.items()))
                == expected_orbit_distribution
            ),
            "144_nonzero_universal_rows": len(nonzero_kk_rows) == 144,
            "21_primitive_templates": len(templates) == 21,
            "template_multiplicities": (
                dict(sorted(multiplicity_distribution.items()))
                == expected_template_multiplicity_distribution
            ),
            "universal_reconstruction": universal_reconstruction,
            "character_rowspaces": all_rowspaces_equal,
            "character_kernels": all_specialisations_exact,
            "character_ranks": all_character_ranks,
            "character_nullities": all_character_nullities,
            "tail_lattice": (
                dimensions_match and all(lattice_checks.values())
            ),
            "minimum_support_profiles": all_profiles_match,
            "quotient_reconstruction": all_quotients_reconstructed,
            "template_equations": all_template_equations,
            "fifteen_directions": direction_count == 15,
            "seventy_nine_atoms": total_atom_count == 79,
        }
        strict_failures = [
            name for name, passed in checks.items() if not passed
        ]

    print("\nUniversal group-ring template census")
    print(f"  KK coordinate rows:                 {q8.rows}")
    print(f"  nonzero universal rows:             {len(nonzero_kk_rows)}")
    print(f"  primitive monomial classes:         {len(templates)}")
    print(
        "  multiplicity distribution:         "
        f"{dict(sorted(multiplicity_distribution.items()))}"
    )

    print("\nCharacter specialisation")
    print(f"  exact row-space equality:           {all_rowspaces_equal}")
    print(f"  exact kernel equality:              {all_specialisations_exact}")
    print(f"  character ranks exact:              {all_character_ranks}")
    print(f"  character nullities exact:          {all_character_nullities}")

    print("\n" + "=" * 126)
    print("FINAL SUMMARY")
    print("=" * 126)
    print(f"Universal rows reconstructed:         {universal_reconstruction}")
    print(f"21-template theorem:                  {len(templates) == 21}")
    print(f"Tail lattice reconstructed:           {summary['tail_lattice_reconstructed']}")
    print(f"Quotient-character directions:        {direction_count}")
    print(f"All template equations exact:         {all_template_equations}")
    print(f"Total minimum signed-orbit atoms:      {total_atom_count}")
    print(f"Verdict:                              {verdict}")
    print(f"elapsed:                              {elapsed:.2f} seconds")
    print(f"summary:                              {out_dir / 'summary.json'}")
    if args.strict:
        print(
            "strict checks:                        "
            f"{'PASS' if not strict_failures else 'FAIL'}"
        )
        if strict_failures:
            print(
                "failed checks:                        "
                + ", ".join(strict_failures)
            )
    print("=" * 126)

    if strict_failures:
        raise SystemExit(2)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract and certify the exact 21-row group-ring shuffle--"
            "antisymmetriser template matrix underlying the fixed-anchor "
            "nine-to-eight tail-filtration relations."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--helper-script", required=True)
    parser.add_argument("--rank-script", required=True)
    parser.add_argument("--direct-script", required=True)
    parser.add_argument("--normal-form-script", required=True)
    parser.add_argument("--derivation-script", required=True)
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
            print(
                f"===== RUN START {time.strftime('%Y-%m-%d %H:%M:%S')} ====="
            )
            run(args)
            print(
                f"===== RUN END {time.strftime('%Y-%m-%d %H:%M:%S')} ====="
            )
            return 0
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr


if __name__ == "__main__":
    raise SystemExit(main())
