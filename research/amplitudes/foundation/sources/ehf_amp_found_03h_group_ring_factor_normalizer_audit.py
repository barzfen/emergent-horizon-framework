#!/usr/bin/env python3
"""
EHF-AMP-FOUND-03H: Group-Ring Factor Types and Residual-Normalizer Audit
========================================================================

03G compressed the fixed-anchor 9 -> 8 KK proof to 21 primitive rows over
Z[C2^3]. 03H asks two exact structural questions.

1. What are the intrinsic factor types of the nonzero orbit polynomials?
2. Does the residual normalizer of C2^3 inside the target-fibre stabilizer
   reduce the 21-template catalogue further?

Every nonzero orbit polynomial is proved to be an affine-subgroup sum

    epsilon * x^a * sum_{h in H} x^h
      = epsilon * x^a * product_{v in B}(1+x^v),

where H <= F2^3 and B is a basis of H.  Across the 21 templates there are 54
nonzero orbit-polynomial blocks, with factor-rank distribution

    rank 0: 29, rank 1: 19, rank 2: 5, rank 3: 1.

The 21 templates collapse to seven coarse factor-rank profiles.

The target-fibre stabilizer is S3 x S4. The normalizer of

    G = <(2 3),(5 6),(7 8)> ~= C2^3

inside S3 x S4 has order 16, so N/G ~= C2.  A nontrivial representative is

    tau=(5 7)(6 8),

which swaps x2 and x3.  In the fixed standard KK chart, tau preserves only
8 of the 21 template classes.  Thirteen images lie outside the original
catalogue; normalizer closure enlarges the catalogue from 21 to 34 classes.
Thus the residual target-fibre normalizer is obstructed by the fixed KK chart
rather than producing a smaller master-template list.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_03h_group_ring_factor_normalizer_audit.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --template-catalog runs/ehf_amp_found_03g/universal_shuffle_template_catalog.csv \
  --template-polynomials runs/ehf_amp_found_03g/universal_shuffle_template_polynomials.csv \
  --out-dir runs/ehf_amp_found_03h \
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

GroupElement = Tuple[int, int, int]
SignTriple = Tuple[int, int, int]
Permutation = Tuple[int, ...]
PolynomialRow = Tuple[int, ...]

GROUP_ELEMENTS: List[GroupElement] = list(itertools.product((0, 1), repeat=3))
MONOMIAL_COLUMNS = [
    "coefficient_1",
    "coefficient_x3",
    "coefficient_x2",
    "coefficient_x2*x3",
    "coefficient_x1",
    "coefficient_x1*x3",
    "coefficient_x1*x2",
    "coefficient_x1*x2*x3",
]


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
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


def xor(left: GroupElement, right: GroupElement) -> GroupElement:
    return tuple(a ^ b for a, b in zip(left, right))  # type: ignore[return-value]


def group_text(element: GroupElement) -> str:
    terms = [f"x{index}" for index, power in enumerate(element, start=1) if power]
    return "1" if not terms else "*".join(terms)


def sign_text(signs: SignTriple) -> str:
    return "".join("+" if sign == 1 else "-" for sign in signs)


def character_value(signs: SignTriple, element: GroupElement) -> int:
    result = 1
    for sign, power in zip(signs, element):
        if power:
            result *= sign
    return result


def subgroup_span(vectors: Iterable[GroupElement]) -> Tuple[GroupElement, ...]:
    span = {(0, 0, 0)}
    for vector in vectors:
        span |= {xor(item, vector) for item in list(span)}
    return tuple(sorted(span))


def independent_basis(subgroup: Sequence[GroupElement]) -> Tuple[GroupElement, ...]:
    current = subgroup_span([])
    basis: List[GroupElement] = []
    for vector in sorted(subgroup):
        if vector == (0, 0, 0):
            continue
        enlarged = subgroup_span([*basis, vector])
        if len(enlarged) > len(current):
            basis.append(vector)
            current = enlarged
    if tuple(current) != tuple(sorted(subgroup)):
        raise RuntimeError("Failed to construct an exact F2 basis")
    return tuple(basis)


def factor_block(coefficients: Sequence[int]) -> Dict[str, object]:
    support = [
        GROUP_ELEMENTS[index]
        for index, value in enumerate(coefficients)
        if int(value) != 0
    ]
    if not support:
        return {
            "zero": True,
            "scalar": 0,
            "offset": (0, 0, 0),
            "subgroup": tuple(),
            "basis": tuple(),
            "rank": -1,
        }

    values = [int(coefficients[GROUP_ELEMENTS.index(item)]) for item in support]
    if len(set(values)) != 1:
        raise RuntimeError("Orbit polynomial does not have constant nonzero coefficients")
    scalar = values[0]
    offset = min(support)
    subgroup = tuple(sorted(xor(item, offset) for item in support))
    if (0, 0, 0) not in subgroup:
        raise RuntimeError("Translated support does not contain the identity")
    if any(xor(left, right) not in subgroup for left in subgroup for right in subgroup):
        raise RuntimeError("Translated support is not a subgroup of F2^3")
    if len(subgroup) not in (1, 2, 4, 8):
        raise RuntimeError("Unexpected subgroup order")
    basis = independent_basis(subgroup)
    rank = int(math.log2(len(subgroup)))
    if len(basis) != rank:
        raise RuntimeError("Subgroup rank mismatch")

    reconstructed = [0] * 8
    for element in subgroup:
        target = xor(offset, element)
        reconstructed[GROUP_ELEMENTS.index(target)] = scalar
    if tuple(reconstructed) != tuple(int(value) for value in coefficients):
        raise RuntimeError("Affine-subgroup factor reconstruction failed")

    return {
        "zero": False,
        "scalar": scalar,
        "offset": offset,
        "subgroup": subgroup,
        "basis": basis,
        "rank": rank,
    }


def factor_notation(factor: Mapping[str, object]) -> str:
    if factor["zero"]:
        return "0"
    scalar = int(factor["scalar"])
    offset = factor["offset"]
    basis = factor["basis"]
    parts: List[str] = []
    if scalar == -1:
        parts.append("-")
    elif scalar != 1:
        parts.append(str(scalar))
    if offset != (0, 0, 0):
        parts.append(group_text(offset))
    for vector in basis:
        parts.append(f"(1+{group_text(vector)})")
    return "*".join(parts) if parts else "1"


def predicted_character_evaluation(
    factor: Mapping[str, object],
    signs: SignTriple,
) -> int:
    if factor["zero"]:
        return 0
    subgroup = factor["subgroup"]
    if any(character_value(signs, element) != 1 for element in subgroup):
        return 0
    return (
        int(factor["scalar"])
        * character_value(signs, factor["offset"])
        * len(subgroup)
    )


def direct_character_evaluation(coefficients: Sequence[int], signs: SignTriple) -> int:
    return sum(
        int(coefficient) * character_value(signs, element)
        for coefficient, element in zip(coefficients, GROUP_ELEMENTS)
    )


def identity_permutation() -> Permutation:
    return tuple(range(9))


def permutation_from_mapping(mapping: Mapping[int, int]) -> Permutation:
    values = list(range(9))
    for source, target in mapping.items():
        values[source] = target
    return tuple(values)


def compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(9))


def inverse(permutation: Permutation) -> Permutation:
    output = [0] * 9
    for source, target in enumerate(permutation):
        output[target] = source
    return tuple(output)


def conjugate(permutation: Permutation, element: Permutation) -> Permutation:
    return compose(compose(permutation, element), inverse(permutation))


def permutation_text(permutation: Permutation) -> str:
    seen = set()
    cycles: List[str] = []
    for start in range(1, 9):
        if start in seen or permutation[start] == start:
            continue
        cycle = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = permutation[current]
        cycles.append("(" + " ".join(map(str, cycle)) + ")")
    return "id" if not cycles else "".join(cycles)


def generate_stabilizer() -> List[Permutation]:
    output: List[Permutation] = []
    for left in itertools.permutations((2, 3, 4)):
        for right in itertools.permutations((5, 6, 7, 8)):
            mapping = {1: 1}
            mapping.update(dict(zip((2, 3, 4), left)))
            mapping.update(dict(zip((5, 6, 7, 8), right)))
            output.append(permutation_from_mapping(mapping))
    return output


def generate_group(generators: Sequence[Permutation]) -> List[Permutation]:
    output = []
    for powers in itertools.product((0, 1), repeat=len(generators)):
        element = identity_permutation()
        for power, generator in zip(powers, generators):
            if power:
                element = compose(element, generator)
        output.append(element)
    return sorted(set(output))


def group_element_permutation(
    element: GroupElement,
    generators: Sequence[Permutation],
) -> Permutation:
    result = identity_permutation()
    for power, generator in zip(element, generators):
        if power:
            result = compose(result, generator)
    return result


def monomial_shift(
    row: Sequence[int],
    shift: GroupElement,
    orbit_count: int,
) -> PolynomialRow:
    group_index = {element: index for index, element in enumerate(GROUP_ELEMENTS)}
    output: List[int] = []
    for orbit_index in range(orbit_count):
        block = row[orbit_index * 8 : (orbit_index + 1) * 8]
        for element in GROUP_ELEMENTS:
            output.append(block[group_index[xor(element, shift)]])
    return tuple(output)


def canonical_template(
    raw_row: Sequence[int],
    orbit_count: int,
) -> Tuple[PolynomialRow, int, GroupElement]:
    raw = tuple(int(value) for value in raw_row)
    if not any(raw):
        return raw, 0, (0, 0, 0)
    gcd_value = 0
    for value in raw:
        gcd_value = math.gcd(gcd_value, abs(value))
    primitive = tuple(value // gcd_value for value in raw)
    candidates = []
    for shift in GROUP_ELEMENTS:
        shifted = monomial_shift(primitive, shift, orbit_count)
        first = next(value for value in shifted if value)
        sign = 1 if first > 0 else -1
        normalised = tuple(sign * value for value in shifted)
        candidates.append((normalised, gcd_value * sign, shift))
    canonical, scalar, shift = min(candidates, key=lambda item: item[0])
    reconstructed = tuple(
        scalar * value for value in monomial_shift(canonical, shift, orbit_count)
    )
    if reconstructed != raw:
        raise RuntimeError("Canonical template reconstruction failed")
    return canonical, scalar, shift


def target_destination(base, states: Sequence[Tuple[int, ...]], mapping: Mapping[int, int]) -> List[int]:
    index = {cycle: position for position, cycle in enumerate(states)}
    output = []
    for cycle in states:
        relabelled = (1,) + tuple(mapping.get(label, label) for label in cycle[1:])
        output.append(index[base.canon(relabelled)])
    return output


def state_orbits(state_count: int, destinations: Sequence[Sequence[int]]) -> List[List[int]]:
    unseen = set(range(state_count))
    output = []
    while unseen:
        representative = min(unseen)
        orbit = sorted({destination[representative] for destination in destinations})
        output.append(orbit)
        unseen -= set(orbit)
    return output


def load_templates(
    catalog_path: Path,
    polynomial_path: Path,
) -> Tuple[
    Dict[str, PolynomialRow],
    Dict[str, int],
    List[Dict[str, object]],
    List[Dict[str, object]],
]:
    with catalog_path.open(newline="") as handle:
        catalog_rows = list(csv.DictReader(handle))
    multiplicities = {
        row["template_id"]: int(row["kk_row_multiplicity"])
        for row in catalog_rows
    }

    with polynomial_path.open(newline="") as handle:
        polynomial_rows = list(csv.DictReader(handle))
    grouped: MutableMapping[str, Dict[str, Dict[str, str]]] = defaultdict(dict)
    for row in polynomial_rows:
        grouped[row["template_id"]][row["orbit_id"]] = row

    orbit_ids = [f"O{index:02d}" for index in range(1, 11)]
    templates: Dict[str, PolynomialRow] = {}
    for template_id in sorted(grouped):
        values: List[int] = []
        for orbit_id in orbit_ids:
            row = grouped[template_id][orbit_id]
            values.extend(int(row[column]) for column in MONOMIAL_COLUMNS)
        templates[template_id] = tuple(values)
    return templates, multiplicities, catalog_rows, polynomial_rows


def write_markdown(
    path: Path,
    profile_rows: Sequence[Mapping[str, object]],
    direction_rows: Sequence[Mapping[str, object]],
    residual_rows: Sequence[Mapping[str, object]],
) -> None:
    lines = [
        "# EHF-AMP-FOUND-03H",
        "## Group-ring factor types and residual-normalizer audit",
        "",
        "Every nonzero orbit polynomial factors exactly as",
        "",
        r"\[p(x)=\epsilon x^a\sum_{h\in H}x^h"
        r"=\epsilon x^a\prod_{v\in B}(1+x^v),\]",
        "",
        r"with \(H\leq\mathbb F_2^3\).",
        "",
        "## Seven factor-rank profiles",
        "",
        "| Profile | Sorted block ranks | Template count | Templates |",
        "|---|---|---:|---|",
    ]
    for row in profile_rows:
        lines.append(
            f"| {row['profile_id']} | `{row['factor_rank_profile']}` | "
            f"{row['template_count']} | `{row['templates']}` |"
        )
    lines.extend([
        "",
        "## Factor-direction census",
        "",
        "| Rank | Subgroup basis | Count | Active characters per block |",
        "|---:|---|---:|---:|",
    ])
    for row in direction_rows:
        lines.append(
            f"| {row['factor_rank']} | `{row['basis_text']}` | "
            f"{row['block_count']} | {row['active_character_count']} |"
        )
    lines.extend([
        "",
        "## Residual normalizer",
        "",
        r"The target-fibre normalizer has order \(16\), with "
        r"\(N/G\cong C_2\). A nontrivial representative is "
        r"\(\tau=(5\,7)(6\,8)\), which swaps \(x_2\) and \(x_3\).",
        "",
        "| Template | Residual image | Status |",
        "|---|---|---|",
    ])
    for row in residual_rows:
        lines.append(
            f"| {row['template_id']} | `{row['image_class_id']}` | "
            f"{row['closure_status']} |"
        )
    lines.extend([
        "",
        "Only 8 of the 21 fixed-chart templates map back into the original "
        "catalogue. Thirteen produce new classes, and normalizer closure has "
        "34 classes. The residual target-fibre symmetry therefore does not "
        "reduce the fixed standard-KK template list.",
        "",
    ])
    path.write_text("\n".join(lines))


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    catalog_path = Path(args.template_catalog).resolve()
    polynomial_path = Path(args.template_polynomials).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_03h_base")
    templates, multiplicities, catalog_rows, polynomial_rows = load_templates(
        catalog_path,
        polynomial_path,
    )

    print("=" * 124)
    print("EHF-AMP-FOUND-03H: GROUP-RING FACTOR TYPES AND RESIDUAL-NORMALIZER AUDIT")
    print("=" * 124)
    print(f"base script:                 {base_script}")
    print(f"03G template catalog:        {catalog_path}")
    print(f"03G template polynomials:    {polynomial_path}")
    print(f"output directory:            {out_dir}")
    print("coefficient ring:            Z[C2^3]")

    if len(templates) != 21:
        raise RuntimeError(f"Expected 21 templates, found {len(templates)}")

    factor_rows: List[Dict[str, object]] = []
    activation_rows: List[Dict[str, object]] = []
    rank_distribution: Counter[int] = Counter()
    direction_distribution: Counter[Tuple[int, Tuple[GroupElement, ...]]] = Counter()
    template_profiles: Dict[str, Tuple[int, ...]] = {}
    all_factorisations_exact = True
    all_character_predictions_exact = True

    polynomial_lookup = {
        (row["template_id"], row["orbit_id"]): row
        for row in polynomial_rows
    }

    for template_id, template in sorted(templates.items()):
        ranks: List[int] = []
        for orbit_index in range(10):
            orbit_id = f"O{orbit_index + 1:02d}"
            block = template[orbit_index * 8 : (orbit_index + 1) * 8]
            factor = factor_block(block)
            if factor["zero"]:
                continue
            rank = int(factor["rank"])
            ranks.append(rank)
            rank_distribution[rank] += 1
            basis = tuple(factor["basis"])
            direction_distribution[(rank, basis)] += 1

            source_row = polynomial_lookup[(template_id, orbit_id)]
            factor_rows.append({
                "template_id": template_id,
                "orbit_id": orbit_id,
                "orbit_size": int(source_row["orbit_size"]),
                "orbit_representative_cycle": source_row["orbit_representative_cycle"],
                "factor_rank": rank,
                "scalar": int(factor["scalar"]),
                "coset_offset": group_text(factor["offset"]),
                "subgroup_order": len(factor["subgroup"]),
                "subgroup_elements": ";".join(group_text(item) for item in factor["subgroup"]),
                "subgroup_basis": ";".join(group_text(item) for item in basis),
                "factor_notation": factor_notation(factor),
                "active_character_count": 2 ** (3 - rank),
                "exact_affine_subgroup_factor": True,
            })

            for signs in itertools.product((1, -1), repeat=3):
                direct_value = direct_character_evaluation(block, signs)
                predicted_value = predicted_character_evaluation(factor, signs)
                exact = direct_value == predicted_value
                all_character_predictions_exact &= exact
                activation_rows.append({
                    "template_id": template_id,
                    "orbit_id": orbit_id,
                    "factor_rank": rank,
                    "character": sign_text(signs),
                    "direct_evaluation": direct_value,
                    "predicted_evaluation": predicted_value,
                    "active": direct_value != 0,
                    "exact_prediction": exact,
                })
        template_profiles[template_id] = tuple(sorted(ranks))

    write_csv(out_dir / "orbit_polynomial_factorization.csv", factor_rows)
    write_csv(out_dir / "character_activation_audit.csv", activation_rows)

    profile_distribution: MutableMapping[Tuple[int, ...], List[str]] = defaultdict(list)
    for template_id, profile in template_profiles.items():
        profile_distribution[profile].append(template_id)

    expected_profiles = {
        (3,): 1,
        (2,): 3,
        (1, 2): 2,
        (1, 1): 6,
        (0, 0, 1): 2,
        (0, 0, 0, 1): 3,
        (0, 0, 0, 0): 4,
    }
    profile_order = [
        (3,),
        (2,),
        (1, 2),
        (1, 1),
        (0, 0, 1),
        (0, 0, 0, 1),
        (0, 0, 0, 0),
    ]
    profile_rows: List[Dict[str, object]] = []
    template_profile_rows: List[Dict[str, object]] = []
    for profile_index, profile in enumerate(profile_order, start=1):
        members = sorted(profile_distribution.get(profile, []))
        profile_rows.append({
            "profile_id": f"F{profile_index}",
            "factor_rank_profile": ",".join(map(str, profile)),
            "template_count": len(members),
            "expected_template_count": expected_profiles[profile],
            "count_match": len(members) == expected_profiles[profile],
            "templates": ";".join(members),
        })
        for template_id in members:
            template_profile_rows.append({
                "template_id": template_id,
                "kk_row_multiplicity": multiplicities[template_id],
                "profile_id": f"F{profile_index}",
                "factor_rank_profile": ",".join(map(str, profile)),
                "nonzero_block_count": len(profile),
            })

    write_csv(out_dir / "factor_profile_census.csv", profile_rows)
    write_csv(out_dir / "template_factor_profiles.csv", template_profile_rows)

    direction_rows: List[Dict[str, object]] = []
    for (rank, basis), count in sorted(
        direction_distribution.items(),
        key=lambda item: (item[0][0], item[0][1]),
    ):
        direction_rows.append({
            "factor_rank": rank,
            "basis_text": ";".join(group_text(item) for item in basis) or "1",
            "subgroup_elements": ";".join(group_text(item) for item in subgroup_span(basis)),
            "block_count": count,
            "active_character_count": 2 ** (3 - rank),
        })
    write_csv(out_dir / "factor_direction_census.csv", direction_rows)

    expected_rank_distribution = {0: 29, 1: 19, 2: 5, 3: 1}
    rank_distribution_match = dict(sorted(rank_distribution.items())) == expected_rank_distribution
    profile_distribution_match = {
        profile: len(members) for profile, members in profile_distribution.items()
    } == expected_profiles

    # Exact residual normalizer inside S_{234} x S_{5678}.
    g1 = permutation_from_mapping({2: 3, 3: 2})
    g2 = permutation_from_mapping({5: 6, 6: 5})
    g3 = permutation_from_mapping({7: 8, 8: 7})
    generator_permutations = [g1, g2, g3]
    group_permutations = generate_group(generator_permutations)
    group_set = set(group_permutations)
    stabilizer = generate_stabilizer()
    normalizer = [
        permutation
        for permutation in stabilizer
        if {
            conjugate(permutation, element)
            for element in group_permutations
        } == group_set
    ]

    normalizer_rows: List[Dict[str, object]] = []
    for permutation in normalizer:
        conjugated_generators = [
            conjugate(permutation, generator)
            for generator in generator_permutations
        ]
        generator_coordinates = []
        for conjugated in conjugated_generators:
            coordinate = next(
                element
                for element in GROUP_ELEMENTS
                if group_element_permutation(element, generator_permutations) == conjugated
            )
            generator_coordinates.append(group_text(coordinate))
        normalizer_rows.append({
            "permutation": permutation_text(permutation),
            "in_G": permutation in group_set,
            "conjugate_g1": generator_coordinates[0],
            "conjugate_g2": generator_coordinates[1],
            "conjugate_g3": generator_coordinates[2],
        })
    write_csv(out_dir / "residual_normalizer_elements.csv", normalizer_rows)

    tau = permutation_from_mapping({5: 7, 7: 5, 6: 8, 8: 6})
    tau_in_normalizer = tau in normalizer
    tau_not_in_group = tau not in group_set
    tau_conjugation = []
    for generator in generator_permutations:
        conjugated = conjugate(tau, generator)
        coordinate = next(
            element
            for element in GROUP_ELEMENTS
            if group_element_permutation(element, generator_permutations) == conjugated
        )
        tau_conjugation.append(coordinate)
    tau_swaps_x2_x3 = tau_conjugation == [(1, 0, 0), (0, 0, 1), (0, 1, 0)]

    reference_states = base.fibres(8)[((1, 2, 3, 4), (5, 6, 7, 8))]
    group_destinations = []
    for element in GROUP_ELEMENTS:
        mapping: Dict[int, int] = {}
        permutation = group_element_permutation(element, generator_permutations)
        for label in range(1, 9):
            mapping[label] = permutation[label]
        group_destinations.append(target_destination(base, reference_states, mapping))
    target_orbits = state_orbits(len(reference_states), group_destinations)
    orbit_representatives = [min(orbit) for orbit in target_orbits]

    # Verify that CSV orbit representatives use the same ordering.
    csv_orbit_representatives = {}
    for row in polynomial_rows:
        csv_orbit_representatives.setdefault(
            row["orbit_id"],
            int(row["orbit_representative_state_index"]),
        )
    expected_csv_reps = [
        csv_orbit_representatives[f"O{index:02d}"]
        for index in range(1, 11)
    ]
    orbit_order_match = orbit_representatives == expected_csv_reps

    tau_mapping = {label: tau[label] for label in range(1, 9)}
    tau_destination = target_destination(base, reference_states, tau_mapping)
    state_to_slots: MutableMapping[int, List[Tuple[int, int]]] = defaultdict(list)
    for orbit_index, representative in enumerate(orbit_representatives):
        for group_index, destination in enumerate(group_destinations):
            state_to_slots[destination[representative]].append((orbit_index, group_index))

    slot_map: List[List[Tuple[int, int]]] = []
    duplicate_consistency = True
    for orbit_index, representative in enumerate(orbit_representatives):
        orbit_slots = []
        for destination in group_destinations:
            state = destination[representative]
            transformed = tau_destination[state]
            slots = sorted(state_to_slots[transformed])
            orbit_slots.append(slots[0])
        slot_map.append(orbit_slots)

    residual_orbit_rows = []
    orbit_permutation = []
    for orbit_index in range(10):
        target_orbit = slot_map[orbit_index][0][0]
        orbit_permutation.append(target_orbit)
        residual_orbit_rows.append({
            "source_orbit": f"O{orbit_index + 1:02d}",
            "target_orbit": f"O{target_orbit + 1:02d}",
            "source_representative_cycle": ",".join(map(str, reference_states[orbit_representatives[orbit_index]])),
            "target_representative_cycle": ",".join(map(str, reference_states[orbit_representatives[target_orbit]])),
        })
    write_csv(out_dir / "residual_target_orbit_permutation.csv", residual_orbit_rows)

    def tau_action(row: PolynomialRow) -> PolynomialRow:
        output = [0] * 80
        for orbit_index in range(10):
            for group_index in range(8):
                target_orbit, target_group = slot_map[orbit_index][group_index]
                # All slots representing the same target state must carry the same coefficient.
                state = group_destinations[group_index][orbit_representatives[orbit_index]]
                transformed = tau_destination[state]
                slot_values = {
                    row[candidate_orbit * 8 + candidate_group]
                    for candidate_orbit, candidate_group in state_to_slots[transformed]
                }
                if len(slot_values) != 1:
                    nonlocal_duplicate_consistency[0] = False
                output[orbit_index * 8 + group_index] = row[target_orbit * 8 + target_group]
        return tuple(output)

    # Mutable cell for the nested function.
    nonlocal_duplicate_consistency = [True]
    original_by_row = {row: template_id for template_id, row in templates.items()}
    tau_images: Dict[str, PolynomialRow] = {}
    residual_rows: List[Dict[str, object]] = []
    internal_count = 0
    outside_count = 0
    profile_preserved = True

    for template_id, row in sorted(templates.items()):
        transformed = tau_action(row)
        transformed_twice = tau_action(transformed)
        if transformed_twice != row:
            raise RuntimeError("Residual involution did not square to identity")
        canonical, scalar, shift = canonical_template(transformed, 10)
        tau_images[template_id] = canonical
        image_template = original_by_row.get(canonical)
        if image_template is None:
            outside_count += 1
            status = "outside_fixed_KK_catalogue"
            image_class_id = "NEW"
        else:
            internal_count += 1
            status = "inside_fixed_KK_catalogue"
            image_class_id = image_template
        image_profile = tuple(
            sorted(
                int(factor_block(canonical[index * 8 : (index + 1) * 8])["rank"])
                for index in range(10)
                if not factor_block(canonical[index * 8 : (index + 1) * 8])["zero"]
            )
        )
        profile_ok = image_profile == template_profiles[template_id]
        profile_preserved &= profile_ok
        residual_rows.append({
            "template_id": template_id,
            "kk_row_multiplicity": multiplicities[template_id],
            "factor_rank_profile": ",".join(map(str, template_profiles[template_id])),
            "image_class_id": image_class_id,
            "closure_status": status,
            "canonical_scalar": scalar,
            "canonical_group_shift": group_text(shift),
            "factor_profile_preserved": profile_ok,
        })

    # Name external classes deterministically and form the complete closure.
    external_rows = sorted({
        row for row in tau_images.values() if row not in original_by_row
    })
    external_ids = {row: f"U{index:02d}" for index, row in enumerate(external_rows, start=1)}
    for row in residual_rows:
        if row["image_class_id"] == "NEW":
            source = row["template_id"]
            row["image_class_id"] = external_ids[tau_images[source]]

    closure_rows: Dict[str, PolynomialRow] = dict(templates)
    closure_rows.update({identifier: row for row, identifier in external_ids.items()})
    closure_by_row = {row: identifier for identifier, row in closure_rows.items()}
    closure_action: Dict[str, str] = {}
    closure_catalog_rows: List[Dict[str, object]] = []
    for class_id, row in sorted(closure_rows.items()):
        canonical, _, _ = canonical_template(tau_action(row), 10)
        if canonical not in closure_by_row:
            raise RuntimeError("Residual closure is not closed")
        image_id = closure_by_row[canonical]
        closure_action[class_id] = image_id
        closure_catalog_rows.append({
            "class_id": class_id,
            "origin": "03G" if class_id.startswith("T") else "residual_image",
            "residual_image": image_id,
            "fixed_by_residual_involution": image_id == class_id,
            "inherited_kk_row_multiplicity": (
                multiplicities[class_id]
                if class_id.startswith("T")
                else multiplicities[next(
                    source for source, image in tau_images.items() if external_ids.get(image) == class_id
                )]
            ),
        })
    write_csv(out_dir / "residual_template_action.csv", residual_rows)
    write_csv(out_dir / "residual_normalizer_closure_catalog.csv", closure_catalog_rows)

    unseen = set(closure_action)
    closure_orbits: List[List[str]] = []
    while unseen:
        start = min(unseen)
        orbit = sorted({start, closure_action[start]})
        closure_orbits.append(orbit)
        unseen -= set(orbit)

    fixed_classes = sorted(
        class_id for class_id, image_id in closure_action.items() if class_id == image_id
    )
    internal_pairs = sorted({
        tuple(sorted((template_id, image_id)))
        for template_id, image_id in closure_action.items()
        if template_id.startswith("T")
        and image_id.startswith("T")
        and template_id != image_id
    })

    closure_multiplicity_distribution = Counter(
        int(row["inherited_kk_row_multiplicity"])
        for row in closure_catalog_rows
    )

    expected_orbit_permutation = [6, 1, 7, 8, 4, 9, 0, 2, 3, 5]
    normalizer_exact = (
        len(stabilizer) == 144
        and len(group_set) == 8
        and len(normalizer) == 16
        and tau_in_normalizer
        and tau_not_in_group
        and tau_swaps_x2_x3
    )
    residual_exact = (
        orbit_order_match
        and orbit_permutation == expected_orbit_permutation
        and nonlocal_duplicate_consistency[0]
        and internal_count == 8
        and outside_count == 13
        and len(external_rows) == 13
        and len(closure_rows) == 34
        and len(closure_orbits) == 18
        and fixed_classes == ["T15", "T16"]
        and internal_pairs == [
            ("T02", "T17"),
            ("T04", "T18"),
            ("T12", "T13"),
        ]
        and profile_preserved
        and dict(sorted(closure_multiplicity_distribution.items()))
        == {4: 18, 8: 11, 16: 5}
    )

    write_markdown(
        out_dir / "exact_factor_normalizer_audit.md",
        profile_rows,
        direction_rows,
        residual_rows,
    )

    exact_certificate = (
        len(factor_rows) == 54
        and all_factorisations_exact
        and all_character_predictions_exact
        and rank_distribution_match
        and profile_distribution_match
        and normalizer_exact
        and residual_exact
    )
    verdict = (
        "EHF_AMP_FOUND_03H_AFFINE_SUBGROUP_FACTOR_THEOREM_AND_RESIDUAL_NORMALIZER_OBSTRUCTION_PROVED"
        if exact_certificate
        else "EHF_AMP_FOUND_03H_FACTOR_NORMALIZER_AUDIT_FAILED"
    )

    certificate = {
        "theorem": (
            "Every nonzero orbit polynomial in the 21-template 03G catalogue "
            "is an affine subgroup sum in Z[C2^3]. The residual normalizer "
            "N/G~=C2 does not close on the fixed standard-KK catalogue: 8 of "
            "21 classes remain inside and 13 leave it, producing a 34-class "
            "normalizer closure."
        ),
        "factor_formula": (
            "p(x)=epsilon*x^a*sum_{h in H}x^h="
            "epsilon*x^a*product_{v in B}(1+x^v)"
        ),
        "nonzero_orbit_polynomial_count": len(factor_rows),
        "factor_rank_distribution": dict(sorted(rank_distribution.items())),
        "factor_profile_distribution": {
            ",".join(map(str, profile)): len(members)
            for profile, members in profile_distribution.items()
        },
        "character_evaluation_formula": (
            "p(chi)=0 unless chi is trivial on H; otherwise "
            "p(chi)=epsilon*chi(a)*|H|."
        ),
        "normalizer": {
            "target_fibre_stabilizer_order": len(stabilizer),
            "G_order": len(group_set),
            "normalizer_order": len(normalizer),
            "quotient_order": len(normalizer) // len(group_set),
            "residual_representative": "tau=(5 7)(6 8)",
            "group_variable_action": "x1->x1, x2<->x3",
            "target_orbit_permutation": [index + 1 for index in orbit_permutation],
        },
        "fixed_KK_chart_action": {
            "templates_in_original_catalogue": internal_count,
            "templates_leaving_original_catalogue": outside_count,
            "normalizer_closure_size": len(closure_rows),
            "normalizer_orbit_count": len(closure_orbits),
            "fixed_classes": fixed_classes,
            "internal_pairs": internal_pairs,
            "closure_multiplicity_distribution": dict(
                sorted(closure_multiplicity_distribution.items())
            ),
        },
        "interpretation": (
            "The simple binomial factors explain character activation and "
            "annihilation exactly. The target-fibre residual symmetry is not "
            "a symmetry of the chosen standard KK coordinate chart; closing "
            "under it enlarges rather than reduces the template catalogue."
        ),
        "claim_boundary": (
            "This classifies finite factor types and proves a fixed-chart "
            "normalizer obstruction. It does not derive the 03G row "
            "multiplicities 4,8,16 from orbit-stabilizer data, restore anchor "
            "covariance, or give a general-n template theorem."
        ),
        "exact_certificate": exact_certificate,
    }
    with (out_dir / "exact_factor_normalizer_certificate.json").open("w") as handle:
        json.dump(json_safe(certificate), handle, indent=2)

    elapsed = time.time() - started
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "template_count": len(templates),
        "nonzero_orbit_polynomial_count": len(factor_rows),
        "factor_rank_distribution": dict(sorted(rank_distribution.items())),
        "factor_profile_count": len(profile_distribution),
        "all_affine_subgroup_factorizations_exact": all_factorisations_exact,
        "all_character_activation_predictions_exact": all_character_predictions_exact,
        "target_fibre_stabilizer_order": len(stabilizer),
        "normalizer_order": len(normalizer),
        "normalizer_quotient_order": len(normalizer) // len(group_set),
        "templates_closed_inside_fixed_KK_catalogue": internal_count,
        "templates_leaving_fixed_KK_catalogue": outside_count,
        "normalizer_closure_size": len(closure_rows),
        "normalizer_closure_orbit_count": len(closure_orbits),
        "exact_factor_and_normalizer_obstruction": exact_certificate,
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "exact_factor_normalizer_certificate.json",
            "orbit_polynomial_factorization.csv",
            "character_activation_audit.csv",
            "factor_profile_census.csv",
            "template_factor_profiles.csv",
            "factor_direction_census.csv",
            "residual_normalizer_elements.csv",
            "residual_target_orbit_permutation.csv",
            "residual_template_action.csv",
            "residual_normalizer_closure_catalog.csv",
            "exact_factor_normalizer_audit.md",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)
    with (out_dir / "verdict.json").open("w") as handle:
        json.dump({
            "verdict": verdict,
            "exact_factor_and_normalizer_obstruction": exact_certificate,
            "factor_profile_count": len(profile_distribution),
            "normalizer_closure_size": len(closure_rows),
        }, handle, indent=2)

    strict_failures: List[str] = []
    if args.strict:
        checks = {
            "twenty_one_templates": len(templates) == 21,
            "fifty_four_nonzero_blocks": len(factor_rows) == 54,
            "affine_subgroup_factorizations": all_factorisations_exact,
            "character_activation_formula": all_character_predictions_exact,
            "factor_rank_distribution": rank_distribution_match,
            "seven_factor_profiles": profile_distribution_match,
            "normalizer_order_sixteen": normalizer_exact,
            "residual_fixed_chart_obstruction": residual_exact,
        }
        strict_failures = [name for name, passed in checks.items() if not passed]

    print("\nAffine-subgroup factor census")
    print(f"  nonzero orbit-polynomial blocks:    {len(factor_rows)}")
    print(f"  factor-rank distribution:           {dict(sorted(rank_distribution.items()))}")
    print(f"  coarse factor-rank profiles:        {len(profile_distribution)}")
    print(f"  character activation formula:       {all_character_predictions_exact}")

    print("\nResidual-normalizer audit")
    print(f"  target-fibre stabilizer order:       {len(stabilizer)}")
    print(f"  normalizer order:                    {len(normalizer)}")
    print(f"  quotient N/G order:                  {len(normalizer) // len(group_set)}")
    print(f"  templates staying in catalogue:     {internal_count}")
    print(f"  templates leaving catalogue:        {outside_count}")
    print(f"  normalizer closure size:             {len(closure_rows)}")
    print(f"  residual closure orbits:             {len(closure_orbits)}")

    print("\n" + "=" * 124)
    print("FINAL SUMMARY")
    print("=" * 124)
    print(f"All affine-subgroup factors exact:    {all_factorisations_exact}")
    print(f"Seven factor profiles exact:          {profile_distribution_match}")
    print(f"Residual normalizer obstruction:      {residual_exact}")
    print(f"Verdict:                              {verdict}")
    print(f"elapsed:                              {elapsed:.2f} seconds")
    print(f"summary:                              {out_dir / 'summary.json'}")
    if args.strict:
        print(f"strict checks:                        {'PASS' if not strict_failures else 'FAIL'}")
        if strict_failures:
            print("failed checks:                        " + ", ".join(strict_failures))
    print("=" * 124)

    if strict_failures:
        raise SystemExit(2)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Classify the 21 exact 03G group-ring templates by affine-subgroup "
            "factor type and audit closure under the residual target-fibre "
            "normalizer."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--template-catalog", required=True)
    parser.add_argument("--template-polynomials", required=True)
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
