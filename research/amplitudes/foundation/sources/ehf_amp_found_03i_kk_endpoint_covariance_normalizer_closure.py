#!/usr/bin/env python3
r"""
EHF-AMP-FOUND-03I: KK-Endpoint Covariance and Two-Chart Normalizer Closure
===========================================================================

03H proved that the nontrivial residual normalizer element

    tau=(5 7)(6 8)

of G=< (2 3),(5 6),(7 8) > ~= C2^3 does not preserve the 21-template
catalogue constructed in the standard endpoint-8 Kleiss--Kuijf chart.
Thirteen template classes leave that catalogue, and residual closure contains
34 classes.

03I tests whether those thirteen classes are exactly the missing classes of
the tau-related endpoint-6 KK chart.

Let Q^(e) be the exact KK coordinate matrix in the basis

    { PT(1,sigma,e) : sigma permutes {2,...,8}\{e} }.

The exact endpoint-covariance equation is

    Q^(6) P_tau = R_tau Q^(8),

where P_tau relabels and canonicalises target states and R_tau relabels KK
basis rows. Since n=8 is even, canonical reversal contributes no sign.

The script also builds the universal Z[C2^3] rows independently in both
endpoint charts and proves:

1. both endpoint catalogues contain 21 primitive monomial classes with
   multiplicities 16^3, 8^6, 4^12;
2. tau maps the endpoint-8 catalogue bijectively onto the endpoint-6
   catalogue;
3. the catalogues intersect in exactly 8 classes and their union contains
   exactly 34 classes;
4. the union has 18 tau-orbits, precisely the normalizer closure found in
   03H;
5. the 13 classes that leave the fixed endpoint-8 catalogue are exactly the
   13 endpoint-6-only classes.

Thus the 03H obstruction is a one-chart obstruction, not a failure of
covariance of the underlying KK relation system.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_03i_kk_endpoint_covariance_normalizer_closure.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --template-script scripts/ehf_amp_found_03g_parameterised_shuffle_antisymmetriser_templates.py \
  --normalizer-script scripts/ehf_amp_found_03h_group_ring_factor_normalizer_audit.py \
  --out-dir runs/ehf_amp_found_03i \
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
GroupElement = Tuple[int, int, int]
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


def cycle_text(cycle: Sequence[int]) -> str:
    return ",".join(map(str, cycle))


def group_text(element: GroupElement) -> str:
    factors = [f"x{index}" for index, power in enumerate(element, start=1) if power]
    return "1" if not factors else "*".join(factors)


def exact_kk_coordinate_matrix_endpoint(
    direct,
    chamber: Sequence[Cycle],
    endpoint: int,
) -> Tuple[sp.MutableSparseMatrix, List[Tuple[int, ...]], Dict[Tuple[int, ...], int]]:
    labels = tuple(label for label in range(2, 9) if label != endpoint)
    permutations = list(itertools.permutations(labels))
    index = {permutation: row for row, permutation in enumerate(permutations)}
    entries: Dict[Tuple[int, int], int] = {}
    for column, cycle in enumerate(chamber):
        position = cycle.index(endpoint)
        alpha = cycle[1:position]
        beta = cycle[position + 1 :]
        sign = -1 if len(beta) % 2 else 1
        for sigma in direct.shuffles(alpha, tuple(reversed(beta))):
            row = index[sigma]
            entries[(row, column)] = entries.get((row, column), 0) + sign
    return (
        sp.MutableSparseMatrix(math.factorial(6), len(chamber), entries),
        permutations,
        index,
    )


def kk_row_relabelling_matrix(
    source_permutations: Sequence[Tuple[int, ...]],
    target_index: Mapping[Tuple[int, ...], int],
    mapping: Mapping[int, int],
) -> sp.MutableSparseMatrix:
    entries = {}
    for source_row, permutation in enumerate(source_permutations):
        image = tuple(mapping.get(label, label) for label in permutation)
        entries[(target_index[image], source_row)] = 1
    return sp.MutableSparseMatrix(len(source_permutations), len(source_permutations), entries)


def classify_universal_rows(
    template_module,
    rows: Sequence[PolynomialRow],
    group_elements: Sequence[GroupElement],
    orbit_count: int,
) -> Tuple[Dict[PolynomialRow, List[int]], Dict[int, Tuple[PolynomialRow, int, GroupElement]]]:
    catalogue: MutableMapping[PolynomialRow, List[int]] = defaultdict(list)
    records: Dict[int, Tuple[PolynomialRow, int, GroupElement]] = {}
    for row_index, row in enumerate(rows):
        if not any(row):
            continue
        canonical, scalar, shift = template_module.canonical_template(
            row,
            group_elements,
            orbit_count,
        )
        catalogue[canonical].append(row_index)
        records[row_index] = (canonical, scalar, shift)
    return dict(catalogue), records


def build_tau_action(
    base,
    states: Sequence[Cycle],
    orbit_representatives: Sequence[int],
    group_destinations: Sequence[Sequence[int]],
    tau_mapping: Mapping[int, int],
):
    tau_destination = base_target_destination(base, states, tau_mapping)
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
            if not slots:
                raise RuntimeError("Tau-transformed state has no orbit slot")
            orbit_slots.append(slots[0])
        slot_map.append(orbit_slots)

    def tau_action(row: PolynomialRow) -> PolynomialRow:
        nonlocal duplicate_consistency
        output = [0] * (len(orbit_representatives) * len(group_destinations))
        for orbit_index in range(len(orbit_representatives)):
            for group_index in range(len(group_destinations)):
                target_orbit, target_group = slot_map[orbit_index][group_index]
                state = group_destinations[group_index][orbit_representatives[orbit_index]]
                transformed = tau_destination[state]
                slot_values = {
                    row[candidate_orbit * len(group_destinations) + candidate_group]
                    for candidate_orbit, candidate_group in state_to_slots[transformed]
                }
                if len(slot_values) != 1:
                    duplicate_consistency = False
                output[orbit_index * len(group_destinations) + group_index] = (
                    row[target_orbit * len(group_destinations) + target_group]
                )
        return tuple(output)

    orbit_permutation = [slot_map[index][0][0] for index in range(len(slot_map))]
    return tau_action, tau_destination, orbit_permutation, lambda: duplicate_consistency


def base_target_destination(
    base,
    states: Sequence[Cycle],
    mapping: Mapping[int, int],
) -> List[int]:
    index = {cycle: position for position, cycle in enumerate(states)}
    output = []
    for cycle in states:
        relabelled = (1,) + tuple(mapping.get(label, label) for label in cycle[1:])
        output.append(index[base.canon(relabelled)])
    return output


def write_markdown(
    path: Path,
    map_rows: Sequence[Mapping[str, object]],
    atlas_rows: Sequence[Mapping[str, object]],
) -> None:
    lines = [
        "# EHF-AMP-FOUND-03I",
        "## KK-endpoint covariance and two-chart normalizer closure",
        "",
        r"Let \(Q^{(e)}\) be the exact eight-point KK matrix in endpoint chart \(e\).",
        r"For \(\tau=(5\,7)(6\,8)\), the exact coordinate covariance is",
        "",
        r"\[Q^{(6)}P_\tau=R_\tau Q^{(8)}.\]",
        "",
        "The endpoint-8 and endpoint-6 universal template catalogues each contain 21 classes.",
        "Their intersection has 8 classes and their union has 34 classes.",
        "The residual transformation maps the endpoint-8 catalogue bijectively onto the endpoint-6 catalogue.",
        "",
        "## Endpoint-8 to endpoint-6 template map",
        "",
        "| Endpoint-8 class | Endpoint-6 class | Shared class | Multiplicity preserved |",
        "|---|---|---|---|",
    ]
    for row in map_rows:
        lines.append(
            f"| {row['endpoint8_template_id']} | {row['endpoint6_template_id']} | "
            f"{'yes' if row['shared_between_charts'] else 'no'} | "
            f"{'yes' if row['multiplicity_preserved'] else 'no'} |"
        )
    lines.extend([
        "",
        "## Two-chart atlas",
        "",
        "| Atlas class | Endpoint 8 | Endpoint 6 | Tau image | Tau orbit |",
        "|---|---|---|---|---|",
    ])
    for row in atlas_rows:
        lines.append(
            f"| {row['atlas_class_id']} | {row['in_endpoint8']} | "
            f"{row['in_endpoint6']} | {row['tau_image_atlas_class']} | "
            f"{row['tau_orbit_id']} |"
        )
    lines.extend([
        "",
        "The thirteen classes that leave the fixed endpoint-8 catalogue are exactly the thirteen endpoint-6-only classes.",
        "Thus the 34-class normalizer closure is a covariant two-chart atlas, not an unexplained enlargement of the relation system.",
        "",
    ])
    path.write_text("\n".join(lines))


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    direct_script = Path(args.direct_script).resolve()
    normal_script = Path(args.normal_form_script).resolve()
    template_script = Path(args.template_script).resolve()
    normalizer_script = Path(args.normalizer_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_03i_base")
    direct = load_module(direct_script, "ehf_amp_found_03i_direct")
    normal = load_module(normal_script, "ehf_amp_found_03i_normal")
    template_module = load_module(template_script, "ehf_amp_found_03i_template")
    normalizer_module = load_module(normalizer_script, "ehf_amp_found_03i_normalizer")

    reference_key = ((1, 2, 3, 4), (5, 6, 7, 8))
    states: List[Cycle] = base.fibres(8)[reference_key]
    if len(states) != 72:
        raise RuntimeError("Expected 72 states in the reference target fibre")

    print("=" * 126)
    print("EHF-AMP-FOUND-03I: KK-ENDPOINT COVARIANCE AND TWO-CHART NORMALIZER CLOSURE")
    print("=" * 126)
    print(f"base script:                 {base_script}")
    print(f"exact KK helper:             {direct_script}")
    print(f"normal-form utilities:       {normal_script}")
    print(f"03G template utilities:      {template_script}")
    print(f"03H normalizer utilities:    {normalizer_script}")
    print(f"output directory:            {out_dir}")
    print("source KK endpoint:          8")
    print("tau-related KK endpoint:     6")
    print("coefficient domain:          QQ")

    q8, permutations8, index8 = exact_kk_coordinate_matrix_endpoint(direct, states, 8)
    q6, permutations6, index6 = exact_kk_coordinate_matrix_endpoint(direct, states, 6)

    generator_permutations = [
        normalizer_module.permutation_from_mapping({2: 3, 3: 2}),
        normalizer_module.permutation_from_mapping({5: 6, 6: 5}),
        normalizer_module.permutation_from_mapping({7: 8, 8: 7}),
    ]
    group_set = set(normalizer_module.generate_group(generator_permutations))
    stabilizer = normalizer_module.generate_stabilizer()
    normalizer = [
        permutation
        for permutation in stabilizer
        if all(
            normalizer_module.conjugate(permutation, generator) in group_set
            for generator in generator_permutations
        )
    ]
    tau_permutation = normalizer_module.permutation_from_mapping(
        {5: 7, 7: 5, 6: 8, 8: 6}
    )
    normalizer_exact = (
        len(stabilizer) == 144
        and len(group_set) == 8
        and len(normalizer) == 16
        and tau_permutation in normalizer
        and tau_permutation not in group_set
    )

    tau_mapping = {5: 7, 7: 5, 6: 8, 8: 6}
    tau_state_destination = base_target_destination(base, states, tau_mapping)
    p_tau = normal.permutation_matrix(tau_state_destination)
    r_tau = kk_row_relabelling_matrix(permutations8, index6, tau_mapping)

    coordinate_covariance = q6 * p_tau == r_tau * q8
    row_map_rows = []
    for endpoint8_row, permutation in enumerate(permutations8):
        image = tuple(tau_mapping.get(label, label) for label in permutation)
        endpoint6_row = index6[image]
        row_map_rows.append({
            "endpoint8_row": endpoint8_row,
            "endpoint8_basis_ordering": "1," + cycle_text(permutation) + ",8",
            "endpoint6_row": endpoint6_row,
            "endpoint6_basis_ordering": "1," + cycle_text(image) + ",6",
            "tau_relabelling_exact": True,
        })
    write_csv(out_dir / "kk_endpoint_row_relabelling.csv", row_map_rows)

    kernel8 = normal.canonical_rowspace(
        DomainMatrix.from_Matrix(q8).convert_to(QQ).nullspace().to_Matrix()
    )
    kernel6 = normal.canonical_rowspace(
        DomainMatrix.from_Matrix(q6).convert_to(QQ).nullspace().to_Matrix()
    )
    endpoint_kernel_equality = kernel8 == kernel6
    tau_kernel_covariance = normal.canonical_rowspace(kernel8 * p_tau.T) == kernel6

    generator_mappings = [
        {2: 3, 3: 2},
        {5: 6, 6: 5},
        {7: 8, 8: 7},
    ]
    generators: List[sp.Matrix] = []
    for mapping in generator_mappings:
        destination = base_target_destination(base, states, mapping)
        generators.append(normal.permutation_matrix(destination))

    group_elements: List[GroupElement] = list(itertools.product((0, 1), repeat=3))
    identity = sp.eye(len(states))
    group_destinations: List[List[int]] = []
    for element in group_elements:
        matrix = identity
        for power, generator in zip(element, generators):
            if power:
                matrix = matrix * generator
        group_destinations.append([
            next(row for row in range(len(states)) if matrix[row, column] == 1)
            for column in range(len(states))
        ])

    state_orbits = normal.state_orbits(len(states), group_destinations)
    orbit_representatives = [min(orbit) for orbit in state_orbits]
    orbit_distribution = Counter(len(orbit) for orbit in state_orbits)

    universal8 = template_module.universal_polynomial_rows(
        q8,
        orbit_representatives,
        group_destinations,
    )
    universal6 = template_module.universal_polynomial_rows(
        q6,
        orbit_representatives,
        group_destinations,
    )
    catalogue8, records8 = classify_universal_rows(
        template_module,
        universal8,
        group_elements,
        len(state_orbits),
    )
    catalogue6, records6 = classify_universal_rows(
        template_module,
        universal6,
        group_elements,
        len(state_orbits),
    )

    tau_action, _, orbit_permutation, duplicate_consistency = build_tau_action(
        base,
        states,
        orbit_representatives,
        group_destinations,
        tau_mapping,
    )

    raw_universal_covariance = True
    raw_covariance_rows = []
    for endpoint8_row, permutation in enumerate(permutations8):
        endpoint6_permutation = tuple(tau_mapping.get(label, label) for label in permutation)
        endpoint6_row = index6[endpoint6_permutation]
        exact = tau_action(universal8[endpoint8_row]) == universal6[endpoint6_row]
        raw_universal_covariance &= exact
        raw_covariance_rows.append({
            "endpoint8_row": endpoint8_row,
            "endpoint6_row": endpoint6_row,
            "endpoint8_nonzero": any(universal8[endpoint8_row]),
            "endpoint6_nonzero": any(universal6[endpoint6_row]),
            "exact_universal_tau_covariance": exact,
        })
    write_csv(out_dir / "universal_row_endpoint_covariance.csv", raw_covariance_rows)

    templates8 = sorted(catalogue8)
    templates6 = sorted(catalogue6)
    ids8 = {row: f"E8_T{index:02d}" for index, row in enumerate(templates8, start=1)}
    ids6 = {row: f"E6_T{index:02d}" for index, row in enumerate(templates6, start=1)}

    tau_images: Dict[PolynomialRow, PolynomialRow] = {}
    map_rows: List[Dict[str, object]] = []
    tau_catalogue_covariance = True
    multiplicity_preserved_all = True
    for row in templates8:
        transformed = tau_action(row)
        canonical, scalar, shift = template_module.canonical_template(
            transformed,
            group_elements,
            len(state_orbits),
        )
        tau_images[row] = canonical
        in_endpoint6 = canonical in catalogue6
        tau_catalogue_covariance &= in_endpoint6
        multiplicity_preserved = (
            in_endpoint6 and len(catalogue8[row]) == len(catalogue6[canonical])
        )
        multiplicity_preserved_all &= multiplicity_preserved
        map_rows.append({
            "endpoint8_template_id": ids8[row],
            "endpoint6_template_id": ids6.get(canonical, "MISSING"),
            "endpoint8_KK_row_multiplicity": len(catalogue8[row]),
            "endpoint6_KK_row_multiplicity": (
                len(catalogue6[canonical]) if in_endpoint6 else -1
            ),
            "multiplicity_preserved": multiplicity_preserved,
            "shared_between_charts": row in catalogue6,
            "tau_canonical_scalar": scalar,
            "tau_canonical_group_shift": group_text(shift),
            "tau_image_present_in_endpoint6": in_endpoint6,
        })
    write_csv(out_dir / "endpoint8_to_endpoint6_template_map.csv", map_rows)

    tau_image_set = set(tau_images.values())
    tau_bijection = tau_image_set == set(templates6) and len(tau_image_set) == len(templates8)

    set8 = set(templates8)
    set6 = set(templates6)
    intersection = set8 & set6
    only8 = set8 - set6
    only6 = set6 - set8
    union = set8 | set6

    # Build a deterministic two-chart atlas and tau action on the union.
    atlas_rows_by_template = sorted(union)
    atlas_ids = {
        row: f"A{index:02d}" for index, row in enumerate(atlas_rows_by_template, start=1)
    }
    union_tau_action: Dict[PolynomialRow, PolynomialRow] = {}
    union_closed = True
    involution_exact = True
    for row in atlas_rows_by_template:
        canonical, _, _ = template_module.canonical_template(
            tau_action(row),
            group_elements,
            len(state_orbits),
        )
        union_tau_action[row] = canonical
        union_closed &= canonical in union
        if canonical in union:
            twice, _, _ = template_module.canonical_template(
                tau_action(canonical),
                group_elements,
                len(state_orbits),
            )
            involution_exact &= twice == row

    unseen = set(union)
    tau_orbits: List[List[PolynomialRow]] = []
    while unseen:
        start = min(unseen)
        image = union_tau_action[start]
        orbit = sorted({start, image})
        tau_orbits.append(orbit)
        unseen -= set(orbit)
    tau_orbit_ids = {
        row: f"O{orbit_index:02d}"
        for orbit_index, orbit in enumerate(tau_orbits, start=1)
        for row in orbit
    }

    atlas_rows: List[Dict[str, object]] = []
    for row in atlas_rows_by_template:
        image = union_tau_action[row]
        atlas_rows.append({
            "atlas_class_id": atlas_ids[row],
            "endpoint8_template_id": ids8.get(row, ""),
            "endpoint6_template_id": ids6.get(row, ""),
            "in_endpoint8": row in set8,
            "in_endpoint6": row in set6,
            "shared_between_charts": row in intersection,
            "endpoint8_KK_row_multiplicity": (
                len(catalogue8[row]) if row in catalogue8 else ""
            ),
            "endpoint6_KK_row_multiplicity": (
                len(catalogue6[row]) if row in catalogue6 else ""
            ),
            "tau_image_atlas_class": atlas_ids[image],
            "tau_orbit_id": tau_orbit_ids[row],
            "fixed_by_tau": image == row,
        })
    write_csv(out_dir / "two_chart_template_atlas.csv", atlas_rows)

    intersection_rows = []
    for row in sorted(intersection):
        intersection_rows.append({
            "atlas_class_id": atlas_ids[row],
            "endpoint8_template_id": ids8[row],
            "endpoint6_template_id": ids6[row],
            "endpoint8_multiplicity": len(catalogue8[row]),
            "endpoint6_multiplicity": len(catalogue6[row]),
            "multiplicity_match": len(catalogue8[row]) == len(catalogue6[row]),
        })
    write_csv(out_dir / "endpoint_chart_intersection.csv", intersection_rows)

    multiplicity_distribution8 = Counter(len(rows) for rows in catalogue8.values())
    multiplicity_distribution6 = Counter(len(rows) for rows in catalogue6.values())
    union_multiplicity_distribution = Counter()
    for row in union:
        multiplicity = (
            len(catalogue8[row]) if row in catalogue8 else len(catalogue6[row])
        )
        if row in catalogue8 and row in catalogue6 and len(catalogue8[row]) != len(catalogue6[row]):
            raise RuntimeError("Shared template has inconsistent endpoint multiplicity")
        union_multiplicity_distribution[multiplicity] += 1

    expected_distribution = {4: 12, 8: 6, 16: 3}
    expected_union_distribution = {4: 18, 8: 11, 16: 5}
    endpoint_catalogue_census_exact = (
        len(catalogue8) == 21
        and len(catalogue6) == 21
        and dict(sorted(multiplicity_distribution8.items())) == expected_distribution
        and dict(sorted(multiplicity_distribution6.items())) == expected_distribution
    )
    two_chart_census_exact = (
        len(intersection) == 8
        and len(only8) == 13
        and len(only6) == 13
        and len(union) == 34
        and len(tau_orbits) == 18
        and dict(sorted(union_multiplicity_distribution.items()))
        == expected_union_distribution
    )
    missing_classes_identified = tau_image_set - set8 == only6

    write_markdown(
        out_dir / "exact_kk_endpoint_covariance_audit.md",
        map_rows,
        atlas_rows,
    )

    exact_certificate = (
        normalizer_exact
        and coordinate_covariance
        and endpoint_kernel_equality
        and tau_kernel_covariance
        and dict(sorted(orbit_distribution.items())) == {4: 2, 8: 8}
        and duplicate_consistency()
        and raw_universal_covariance
        and endpoint_catalogue_census_exact
        and tau_catalogue_covariance
        and tau_bijection
        and multiplicity_preserved_all
        and union_closed
        and involution_exact
        and two_chart_census_exact
        and missing_classes_identified
    )

    verdict = (
        "EHF_AMP_FOUND_03I_EXACT_TWO_CHART_KK_ENDPOINT_COVARIANCE_PROVED"
        if exact_certificate
        else "EHF_AMP_FOUND_03I_KK_ENDPOINT_COVARIANCE_FAILED"
    )

    certificate = {
        "theorem": (
            "The residual normalizer image of the endpoint-8 21-template "
            "catalogue is exactly the independently constructed endpoint-6 "
            "21-template catalogue. The 34-class closure is therefore a "
            "covariant two-chart KK atlas."
        ),
        "endpoint_covariance_equation": "Q^(6) P_tau = R_tau Q^(8)",
        "tau": "(5 7)(6 8)",
        "normalizer": {
            "target_fibre_stabilizer_order": len(stabilizer),
            "G_order": len(group_set),
            "normalizer_order": len(normalizer),
            "quotient_order": len(normalizer) // len(group_set),
            "tau_is_nontrivial_residual_element": normalizer_exact,
        },
        "endpoint_charts": [8, 6],
        "normalizer_exact": normalizer_exact,
        "coordinate_covariance_exact": coordinate_covariance,
        "relation_kernel": {
            "endpoint8_dimension": kernel8.rows,
            "endpoint6_dimension": kernel6.rows,
            "endpoint_kernels_equal": endpoint_kernel_equality,
            "tau_maps_endpoint8_kernel_to_endpoint6_kernel": tau_kernel_covariance,
        },
        "universal_rows": {
            "raw_tau_covariance_exact": raw_universal_covariance,
            "target_orbit_permutation": [value + 1 for value in orbit_permutation],
        },
        "endpoint8_catalogue": {
            "template_count": len(catalogue8),
            "multiplicity_distribution": dict(sorted(multiplicity_distribution8.items())),
        },
        "endpoint6_catalogue": {
            "template_count": len(catalogue6),
            "multiplicity_distribution": dict(sorted(multiplicity_distribution6.items())),
        },
        "two_chart_atlas": {
            "intersection_size": len(intersection),
            "endpoint8_only": len(only8),
            "endpoint6_only": len(only6),
            "union_size": len(union),
            "tau_orbit_count": len(tau_orbits),
            "union_multiplicity_distribution": dict(
                sorted(union_multiplicity_distribution.items())
            ),
            "tau_maps_endpoint8_catalogue_bijectively_to_endpoint6": tau_bijection,
            "thirteen_missing_classes_are_exactly_endpoint6_only": missing_classes_identified,
        },
        "interpretation": (
            "The residual-normalizer obstruction in 03H is caused by holding "
            "the standard KK endpoint fixed. Once the endpoint-6 chart related "
            "by tau is included, the universal template system is exactly "
            "covariant."
        ),
        "claim_boundary": (
            "This proves covariance for the two endpoint charts 8 and 6 under "
            "the specific residual normalizer element tau in the fixed anchor-1 "
            "reference fibre. It does not yet prove covariance for every KK "
            "endpoint, every target-fibre stabilizer element, a change of anchor, "
            "or general multiplicity."
        ),
        "exact_certificate": exact_certificate,
    }
    with (out_dir / "exact_kk_endpoint_covariance_certificate.json").open("w") as handle:
        json.dump(json_safe(certificate), handle, indent=2)

    elapsed = time.time() - started
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "coordinate_covariance_exact": coordinate_covariance,
        "endpoint_relation_kernel_dimension": kernel8.rows,
        "endpoint_kernels_equal": endpoint_kernel_equality,
        "tau_kernel_covariance": tau_kernel_covariance,
        "raw_universal_row_covariance": raw_universal_covariance,
        "endpoint8_template_count": len(catalogue8),
        "endpoint6_template_count": len(catalogue6),
        "template_intersection_size": len(intersection),
        "endpoint8_only_template_count": len(only8),
        "endpoint6_only_template_count": len(only6),
        "two_chart_union_size": len(union),
        "two_chart_tau_orbit_count": len(tau_orbits),
        "tau_catalogue_bijection": tau_bijection,
        "missing_classes_exactly_endpoint6_only": missing_classes_identified,
        "exact_two_chart_endpoint_covariance": exact_certificate,
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "exact_kk_endpoint_covariance_certificate.json",
            "kk_endpoint_row_relabelling.csv",
            "universal_row_endpoint_covariance.csv",
            "endpoint8_to_endpoint6_template_map.csv",
            "endpoint_chart_intersection.csv",
            "two_chart_template_atlas.csv",
            "exact_kk_endpoint_covariance_audit.md",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)
    with (out_dir / "verdict.json").open("w") as handle:
        json.dump(
            {
                "verdict": verdict,
                "exact_two_chart_endpoint_covariance": exact_certificate,
                "endpoint8_template_count": len(catalogue8),
                "endpoint6_template_count": len(catalogue6),
                "two_chart_union_size": len(union),
            },
            handle,
            indent=2,
        )

    strict_failures: List[str] = []
    if args.strict:
        checks = {
            "normalizer_exact": normalizer_exact,
            "coordinate_covariance": coordinate_covariance,
            "endpoint_kernel_equality": endpoint_kernel_equality,
            "tau_kernel_covariance": tau_kernel_covariance,
            "target_state_orbits": dict(sorted(orbit_distribution.items())) == {4: 2, 8: 8},
            "duplicate_slot_consistency": duplicate_consistency(),
            "raw_universal_covariance": raw_universal_covariance,
            "endpoint_catalogue_census": endpoint_catalogue_census_exact,
            "tau_catalogue_bijection": tau_bijection,
            "template_multiplicity_covariance": multiplicity_preserved_all,
            "two_chart_union_closed": union_closed,
            "tau_involution": involution_exact,
            "two_chart_census": two_chart_census_exact,
            "missing_classes_identified": missing_classes_identified,
        }
        strict_failures = [name for name, passed in checks.items() if not passed]

    print("\nResidual normalizer")
    print(f"  target-fibre stabilizer order:      {len(stabilizer)}")
    print(f"  normalizer order:                   {len(normalizer)}")
    print(f"  quotient N/G order:                 {len(normalizer) // len(group_set)}")
    print(f"  tau is nontrivial residual element: {normalizer_exact}")

    print("\nExact KK endpoint covariance")
    print(f"  Q6 P_tau = R_tau Q8:               {coordinate_covariance}")
    print(f"  endpoint kernels equal:             {endpoint_kernel_equality}")
    print(f"  tau kernel covariance:              {tau_kernel_covariance}")
    print(f"  raw universal row covariance:       {raw_universal_covariance}")

    print("\nTwo-chart template atlas")
    print(f"  endpoint-8 templates:               {len(catalogue8)}")
    print(f"  endpoint-6 templates:               {len(catalogue6)}")
    print(f"  shared templates:                   {len(intersection)}")
    print(f"  endpoint-8-only templates:          {len(only8)}")
    print(f"  endpoint-6-only templates:          {len(only6)}")
    print(f"  union size:                         {len(union)}")
    print(f"  tau orbits in union:                {len(tau_orbits)}")
    print(f"  tau catalogue bijection:            {tau_bijection}")

    print("\n" + "=" * 126)
    print("FINAL SUMMARY")
    print("=" * 126)
    print(f"Exact endpoint coordinate covariance: {coordinate_covariance}")
    print(f"Exact 21-to-21 template covariance:   {tau_bijection}")
    print(f"03H closure recovered as two charts:  {two_chart_census_exact}")
    print(f"Thirteen missing classes identified:  {missing_classes_identified}")
    print(f"Verdict:                              {verdict}")
    print(f"elapsed:                              {elapsed:.2f} seconds")
    print(f"summary:                              {out_dir / 'summary.json'}")
    if args.strict:
        print(f"strict checks:                        {'PASS' if not strict_failures else 'FAIL'}")
        if strict_failures:
            print(f"failed checks:                        {', '.join(strict_failures)}")
    print("=" * 126)

    if strict_failures:
        raise SystemExit(2)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prove exact KK endpoint covariance between endpoint-8 and "
            "tau-related endpoint-6 charts and identify the 03H 34-class "
            "normalizer closure as their two-chart template atlas."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--direct-script", required=True)
    parser.add_argument("--normal-form-script", required=True)
    parser.add_argument("--template-script", required=True)
    parser.add_argument("--normalizer-script", required=True)
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
