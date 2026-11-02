#!/usr/bin/env python3
r"""
EHF-AMP-FOUND-03J: Full Normalizer Endpoint Atlas and Cocycle Consistency
=========================================================================

03I proved exact covariance between the endpoint-8 and endpoint-6 KK charts
under the nontrivial residual normalizer element

    tau=(5 7)(6 8).

03J closes the endpoint-covariance problem for the complete order-16
normalizer

    N = N_{S3 x S4}(G),
    G = <(2 3),(5 6),(7 8)> ~= C2^3,
    N/G ~= C2.

For every endpoint e in {5,6,7,8} and every n in N, the script constructs
exact KK coordinate matrices Q^(e), state relabelling maps P_n, and KK-row
relabeling maps R_(n,e), then proves

    Q^(n(e)) P_n = R_(n,e) Q^(e).

It also verifies strict transition cocycles

    P_(mn) = P_m P_n,
    R_(mn,e) = R_(m,n(e)) R_(n,e),

and the corresponding raw universal group-ring row covariance.

The endpoint template catalogues split into exactly two chart classes:

    T_7 = T_8,
    T_5 = T_6,

with 21 templates per chart, overlap 8, and union 34. The complete normalizer
action on canonical template classes factors through N/G ~= C2. The subgroup G
acts trivially on the 34 canonical classes, while every element of the
nontrivial coset induces the same residual involution. The 34-class atlas has
18 quotient orbits: two fixed classes and sixteen two-cycles.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_03j_full_normalizer_endpoint_atlas_cocycle.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --template-script scripts/ehf_amp_found_03g_parameterised_shuffle_antisymmetriser_templates.py \
  --normalizer-script scripts/ehf_amp_found_03h_group_ring_factor_normalizer_audit.py \
  --endpoint-script scripts/ehf_amp_found_03i_kk_endpoint_covariance_normalizer_closure.py \
  --out-dir runs/ehf_amp_found_03j \
  --strict
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import itertools
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Dict, List, Mapping, MutableMapping, Sequence, Tuple

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

Cycle = Tuple[int, ...]
Permutation = Tuple[int, ...]
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


def permutation_mapping(permutation: Permutation) -> Dict[int, int]:
    return {label: permutation[label] for label in range(1, 9)}


def permutation_id_map(
    permutations: Sequence[Permutation],
    normalizer_module,
) -> Dict[Permutation, str]:
    ordered = sorted(permutations, key=lambda item: normalizer_module.permutation_text(item))
    return {permutation: f"N{index:02d}" for index, permutation in enumerate(ordered, start=1)}


def row_relabelling_array(
    source_permutations: Sequence[Tuple[int, ...]],
    target_index: Mapping[Tuple[int, ...], int],
    permutation: Permutation,
) -> List[int]:
    return [
        target_index[tuple(permutation[label] for label in source)]
        for source in source_permutations
    ]


def permutation_matrix_from_array(destination: Sequence[int]) -> sp.MutableSparseMatrix:
    return sp.MutableSparseMatrix(
        len(destination),
        len(destination),
        {(target, source): 1 for source, target in enumerate(destination)},
    )


def canonical_image(
    template_module,
    action: Callable[[PolynomialRow], PolynomialRow],
    row: PolynomialRow,
    group_elements: Sequence[GroupElement],
    orbit_count: int,
) -> PolynomialRow:
    canonical, _, _ = template_module.canonical_template(
        action(row),
        group_elements,
        orbit_count,
    )
    return canonical



def build_polynomial_pushforward_action(
    orbit_representatives: Sequence[int],
    group_destinations: Sequence[Sequence[int]],
    state_destination: Sequence[int],
):
    """
    Push coefficient data forward under a target-state permutation.

    Universal rows are functions of target states. For a relabelling n, the
    transformed row obeys output[n(s)] = input[s]. Orbit-size-four states have
    duplicate group slots; exact universal/template rows are constant across
    those duplicate slots.
    """
    state_to_slots: MutableMapping[int, List[Tuple[int, int]]] = defaultdict(list)
    for orbit_index, representative in enumerate(orbit_representatives):
        for group_index, destination in enumerate(group_destinations):
            state_to_slots[destination[representative]].append(
                (orbit_index, group_index)
            )

    inverse_destination = [0] * len(state_destination)
    for source, target in enumerate(state_destination):
        inverse_destination[target] = source

    consistency = {"exact": True}

    def action(row: PolynomialRow) -> PolynomialRow:
        output = [0] * (len(orbit_representatives) * len(group_destinations))
        for target_orbit, representative in enumerate(orbit_representatives):
            for target_group, destination in enumerate(group_destinations):
                target_state = destination[representative]
                source_state = inverse_destination[target_state]
                source_slots = state_to_slots[source_state]
                values = {
                    row[source_orbit * len(group_destinations) + source_group]
                    for source_orbit, source_group in source_slots
                }
                if len(values) != 1:
                    consistency["exact"] = False
                output[
                    target_orbit * len(group_destinations) + target_group
                ] = row[
                    source_slots[0][0] * len(group_destinations)
                    + source_slots[0][1]
                ]
        return tuple(output)

    return action, lambda: consistency["exact"]

def write_markdown(
    path: Path,
    endpoint_rows: Sequence[Mapping[str, object]],
    normalizer_rows: Sequence[Mapping[str, object]],
    orbit_rows: Sequence[Mapping[str, object]],
) -> None:
    lines = [
        "# EHF-AMP-FOUND-03J",
        "## Full normalizer endpoint atlas and cocycle consistency",
        "",
        r"Let \(N=N_{S_3\times S_4}(G)\), with",
        "",
        r"\[G=\langle(2\,3),(5\,6),(7\,8)\rangle\cong C_2^3.\]",
        "",
        r"The exact transition equation is",
        "",
        r"\[Q^{(n(e))}P_n=R_{n,e}Q^{(e)}.\]",
        "",
        "## Endpoint chart census",
        "",
        "| Endpoint | Chart class | Templates | Nonzero universal rows | Kernel dimension |",
        "|---:|---|---:|---:|---:|",
    ]
    for row in endpoint_rows:
        lines.append(
            f"| {row['endpoint']} | {row['chart_class']} | "
            f"{row['template_count']} | {row['nonzero_universal_rows']} | "
            f"{row['kernel_dimension']} |"
        )

    lines.extend([
        "",
        "The exact catalogue identities are",
        "",
        r"\[\mathcal T_7=\mathcal T_8,\qquad \mathcal T_5=\mathcal T_6.\]",
        "",
        r"Each chart contains 21 classes, the two chart classes overlap in 8, "
        r"and their union contains 34.",
        "",
        "## Normalizer elements",
        "",
        "| Element | Permutation | Coset | Image of endpoint 8 | Image chart | Covariance checks |",
        "|---|---|---|---:|---|---|",
    ])
    for row in normalizer_rows:
        checks = (
            row["all_endpoint_coordinate_covariance"]
            and row["all_endpoint_universal_covariance"]
            and row["all_endpoint_template_bijections"]
        )
        lines.append(
            f"| {row['normalizer_id']} | `{row['permutation']} ` | "
            f"{row['coset']} | {row['image_of_endpoint_8']} | "
            f"{row['image_chart_class']} | {'exact' if checks else 'failed'} |"
        )

    lines.extend([
        "",
        "## Quotient action on the 34-class atlas",
        "",
        "The action factors through",
        "",
        r"\[N/G\cong C_2.\]",
        "",
        r"Every element of \(G\) acts trivially on canonical template classes. "
        "Every element of the nontrivial coset induces the same involution.",
        "",
        "| Atlas orbit | Size | Fixed | Members |",
        "|---|---:|---|---|",
    ])
    for row in orbit_rows:
        lines.append(
            f"| {row['atlas_orbit_id']} | {row['orbit_size']} | "
            f"{'yes' if row['fixed'] else 'no'} | `{row['atlas_class_ids']}` |"
        )

    lines.extend([
        "",
        "## Exact cocycle",
        "",
        r"For all \(m,n\in N\) and all four endpoints,",
        "",
        r"\[P_{mn}=P_mP_n,\qquad "
        r"R_{mn,e}=R_{m,n(e)}R_{n,e}.\]",
        "",
        "The raw universal-row action and canonical template-class action obey "
        "the same composition law. The full normalizer atlas therefore closes "
        "at 34 classes and generates no additional endpoint-template classes.",
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
    endpoint_script = Path(args.endpoint_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_03j_base")
    direct = load_module(direct_script, "ehf_amp_found_03j_direct")
    normal = load_module(normal_script, "ehf_amp_found_03j_normal")
    template_module = load_module(template_script, "ehf_amp_found_03j_template")
    normalizer_module = load_module(normalizer_script, "ehf_amp_found_03j_normalizer")
    endpoint_module = load_module(endpoint_script, "ehf_amp_found_03j_endpoint")

    reference_key = ((1, 2, 3, 4), (5, 6, 7, 8))
    states: List[Cycle] = base.fibres(8)[reference_key]
    endpoints = (5, 6, 7, 8)

    print("=" * 126)
    print("EHF-AMP-FOUND-03J: FULL NORMALIZER ENDPOINT ATLAS AND COCYCLE CONSISTENCY")
    print("=" * 126)
    print(f"base script:                 {base_script}")
    print(f"exact KK helper:             {direct_script}")
    print(f"normal-form utilities:       {normal_script}")
    print(f"03G template utilities:      {template_script}")
    print(f"03H normalizer utilities:    {normalizer_script}")
    print(f"03I endpoint utilities:      {endpoint_script}")
    print(f"output directory:            {out_dir}")
    print("endpoints:                   {5,6,7,8}")
    print("coefficient domain:          QQ")

    generator_mappings = [
        {2: 3, 3: 2},
        {5: 6, 6: 5},
        {7: 8, 8: 7},
    ]
    generator_permutations = [
        normalizer_module.permutation_from_mapping(mapping)
        for mapping in generator_mappings
    ]
    group = normalizer_module.generate_group(generator_permutations)
    group_set = set(group)
    stabilizer = normalizer_module.generate_stabilizer()
    normalizer = sorted(
        [
            permutation
            for permutation in stabilizer
            if {
                normalizer_module.conjugate(permutation, element)
                for element in group_set
            }
            == group_set
        ],
        key=lambda item: normalizer_module.permutation_text(item),
    )
    normalizer_set = set(normalizer)
    normalizer_ids = permutation_id_map(normalizer, normalizer_module)

    exact_group_orders = (
        len(stabilizer) == 144
        and len(group) == 8
        and len(normalizer) == 16
    )

    # Exact KK matrices, kernels, and universal template catalogues in all four endpoint charts.
    q: Dict[int, sp.MutableSparseMatrix] = {}
    kk_permutations: Dict[int, List[Tuple[int, ...]]] = {}
    kk_indices: Dict[int, Dict[Tuple[int, ...], int]] = {}
    kernels: Dict[int, sp.Matrix] = {}

    for endpoint in endpoints:
        matrix, permutations, index = endpoint_module.exact_kk_coordinate_matrix_endpoint(
            direct,
            states,
            endpoint,
        )
        q[endpoint] = matrix
        kk_permutations[endpoint] = permutations
        kk_indices[endpoint] = index
        kernels[endpoint] = normal.canonical_rowspace(
            DomainMatrix.from_Matrix(matrix)
            .convert_to(QQ)
            .nullspace()
            .to_Matrix()
        )

    # Fixed G orbit coordinates for the universal group-ring rows.
    generators: List[sp.Matrix] = []
    for mapping in generator_mappings:
        destination = endpoint_module.base_target_destination(base, states, mapping)
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
    orbit_count = len(state_orbits)

    universal: Dict[int, List[PolynomialRow]] = {}
    catalogues: Dict[int, Dict[PolynomialRow, List[int]]] = {}
    records: Dict[int, Dict[int, Tuple[PolynomialRow, int, GroupElement]]] = {}
    multiplicity_distributions: Dict[int, Counter[int]] = {}

    endpoint_rows: List[Dict[str, object]] = []
    for endpoint in endpoints:
        universal[endpoint] = template_module.universal_polynomial_rows(
            q[endpoint],
            orbit_representatives,
            group_destinations,
        )
        catalogue, record = endpoint_module.classify_universal_rows(
            template_module,
            universal[endpoint],
            group_elements,
            orbit_count,
        )
        catalogues[endpoint] = catalogue
        records[endpoint] = record
        multiplicity_distributions[endpoint] = Counter(
            len(rows) for rows in catalogue.values()
        )

    chart_a = set(catalogues[8])
    chart_b = set(catalogues[6])
    chart_identifications = (
        set(catalogues[7]) == chart_a
        and set(catalogues[8]) == chart_a
        and set(catalogues[5]) == chart_b
        and set(catalogues[6]) == chart_b
        and chart_a != chart_b
    )
    chart_intersection = chart_a & chart_b
    atlas = chart_a | chart_b

    chart_class_by_endpoint = {
        5: "C56",
        6: "C56",
        7: "C78",
        8: "C78",
    }
    for endpoint in endpoints:
        endpoint_rows.append({
            "endpoint": endpoint,
            "chart_class": chart_class_by_endpoint[endpoint],
            "template_count": len(catalogues[endpoint]),
            "nonzero_universal_rows": sum(any(row) for row in universal[endpoint]),
            "kernel_dimension": kernels[endpoint].rows,
            "template_multiplicity_distribution": ";".join(
                f"{multiplicity}:{count}"
                for multiplicity, count in sorted(
                    multiplicity_distributions[endpoint].items()
                )
            ),
        })
    write_csv(out_dir / "endpoint_chart_summary.csv", endpoint_rows)

    endpoint_catalogue_census = (
        all(len(catalogues[endpoint]) == 21 for endpoint in endpoints)
        and all(
            dict(sorted(multiplicity_distributions[endpoint].items()))
            == {4: 12, 8: 6, 16: 3}
            for endpoint in endpoints
        )
        and len(chart_intersection) == 8
        and len(chart_a - chart_b) == 13
        and len(chart_b - chart_a) == 13
        and len(atlas) == 34
    )

    all_kernels_equal = all(kernels[endpoint] == kernels[8] for endpoint in endpoints)

    # State, row, and universal-row actions for every normalizer element.
    state_destinations: Dict[Permutation, List[int]] = {}
    state_matrices: Dict[Permutation, sp.Matrix] = {}
    polynomial_actions: Dict[Permutation, Callable[[PolynomialRow], PolynomialRow]] = {}
    duplicate_consistency_all = True
    polynomial_action_consistency: Dict[Permutation, Callable[[], bool]] = {}

    for permutation in normalizer:
        mapping = permutation_mapping(permutation)
        destination = endpoint_module.base_target_destination(base, states, mapping)
        state_destinations[permutation] = destination
        state_matrices[permutation] = normal.permutation_matrix(destination)
        action, duplicate_consistency = build_polynomial_pushforward_action(
            orbit_representatives,
            group_destinations,
            destination,
        )
        polynomial_actions[permutation] = action
        # The flag is evaluated again after all action calls below.
        polynomial_action_consistency[permutation] = duplicate_consistency

    row_maps: Dict[Tuple[Permutation, int], List[int]] = {}
    row_matrices: Dict[Tuple[Permutation, int], sp.MutableSparseMatrix] = {}
    for permutation in normalizer:
        for endpoint in endpoints:
            target_endpoint = permutation[endpoint]
            mapping = permutation_mapping(permutation)
            row_map = row_relabelling_array(
                kk_permutations[endpoint],
                kk_indices[target_endpoint],
                permutation,
            )
            row_maps[(permutation, endpoint)] = row_map
            row_matrices[(permutation, endpoint)] = permutation_matrix_from_array(row_map)

    covariance_rows: List[Dict[str, object]] = []
    normalizer_rows: List[Dict[str, object]] = []
    template_transition_rows: List[Dict[str, object]] = []
    all_coordinate_covariance = True
    all_kernel_covariance = True
    all_universal_covariance = True
    all_template_bijections = True
    all_multiplicity_preservation = True

    for permutation in normalizer:
        normalizer_id = normalizer_ids[permutation]
        permutation_text = normalizer_module.permutation_text(permutation)
        coset = "G" if permutation in group_set else "N\\G"
        element_coordinate_ok = True
        element_kernel_ok = True
        element_universal_ok = True
        element_template_ok = True

        for endpoint in endpoints:
            target_endpoint = permutation[endpoint]
            p_matrix = state_matrices[permutation]
            r_matrix = row_matrices[(permutation, endpoint)]
            coordinate_ok = (
                q[target_endpoint] * p_matrix
                == r_matrix * q[endpoint]
            )
            element_coordinate_ok &= coordinate_ok
            all_coordinate_covariance &= coordinate_ok

            kernel_ok = (
                normal.canonical_rowspace(
                    kernels[endpoint] * p_matrix.T
                )
                == kernels[target_endpoint]
            )
            element_kernel_ok &= kernel_ok
            all_kernel_covariance &= kernel_ok

            action = polynomial_actions[permutation]
            row_map = row_maps[(permutation, endpoint)]
            universal_ok = True
            for source_row, target_row in enumerate(row_map):
                if action(universal[endpoint][source_row]) != universal[target_endpoint][target_row]:
                    universal_ok = False
                    break
            element_universal_ok &= universal_ok
            all_universal_covariance &= universal_ok

            image_set = set()
            template_ok = True
            multiplicity_ok = True
            for source_template, source_rows in catalogues[endpoint].items():
                image = canonical_image(
                    template_module,
                    action,
                    source_template,
                    group_elements,
                    orbit_count,
                )
                image_set.add(image)
                present = image in catalogues[target_endpoint]
                multiplicity_match = (
                    present
                    and len(source_rows) == len(catalogues[target_endpoint][image])
                )
                template_ok &= present
                multiplicity_ok &= multiplicity_match
                template_transition_rows.append({
                    "normalizer_id": normalizer_id,
                    "normalizer_permutation": permutation_text,
                    "coset": coset,
                    "source_endpoint": endpoint,
                    "target_endpoint": target_endpoint,
                    "source_chart_class": chart_class_by_endpoint[endpoint],
                    "target_chart_class": chart_class_by_endpoint[target_endpoint],
                    "source_template_index": sorted(catalogues[endpoint]).index(source_template) + 1,
                    "target_template_index": (
                        sorted(catalogues[target_endpoint]).index(image) + 1
                        if present else -1
                    ),
                    "source_KK_row_multiplicity": len(source_rows),
                    "target_KK_row_multiplicity": (
                        len(catalogues[target_endpoint][image]) if present else -1
                    ),
                    "multiplicity_preserved": multiplicity_match,
                    "exact_template_transition": present,
                })
            bijection_ok = (
                template_ok
                and image_set == set(catalogues[target_endpoint])
                and len(image_set) == 21
            )
            element_template_ok &= bijection_ok
            all_template_bijections &= bijection_ok
            all_multiplicity_preservation &= multiplicity_ok

            covariance_rows.append({
                "normalizer_id": normalizer_id,
                "normalizer_permutation": permutation_text,
                "coset": coset,
                "source_endpoint": endpoint,
                "target_endpoint": target_endpoint,
                "source_chart_class": chart_class_by_endpoint[endpoint],
                "target_chart_class": chart_class_by_endpoint[target_endpoint],
                "coordinate_covariance": coordinate_ok,
                "kernel_covariance": kernel_ok,
                "universal_row_covariance": universal_ok,
                "template_catalogue_bijection": bijection_ok,
                "template_multiplicity_preservation": multiplicity_ok,
            })

        normalizer_rows.append({
            "normalizer_id": normalizer_id,
            "permutation": permutation_text,
            "coset": coset,
            "image_of_endpoint_8": permutation[8],
            "image_chart_class": chart_class_by_endpoint[permutation[8]],
            "all_endpoint_coordinate_covariance": element_coordinate_ok,
            "all_endpoint_kernel_covariance": element_kernel_ok,
            "all_endpoint_universal_covariance": element_universal_ok,
            "all_endpoint_template_bijections": element_template_ok,
        })

    write_csv(out_dir / "normalizer_element_ledger.csv", normalizer_rows)
    write_csv(out_dir / "normalizer_endpoint_covariance.csv", covariance_rows)
    write_csv(out_dir / "normalizer_template_transitions.csv", template_transition_rows)

    # Exact composition/cocycle audits.
    cocycle_rows: List[Dict[str, object]] = []
    state_cocycle_all = True
    row_cocycle_all = True
    raw_action_cocycle_all = True
    class_action_cocycle_all = True

    atlas_sorted = sorted(atlas)
    for left in normalizer:
        for right in normalizer:
            composition = normalizer_module.compose(left, right)
            if composition not in normalizer_set:
                raise RuntimeError("Normalizer is not closed under composition")

            state_ok = all(
                state_destinations[composition][source]
                == state_destinations[left][state_destinations[right][source]]
                for source in range(len(states))
            )
            state_cocycle_all &= state_ok

            raw_ok = all(
                polynomial_actions[left](polynomial_actions[right](row))
                == polynomial_actions[composition](row)
                for row in atlas_sorted
            )
            raw_action_cocycle_all &= raw_ok

            class_ok = all(
                canonical_image(
                    template_module,
                    polynomial_actions[left],
                    canonical_image(
                        template_module,
                        polynomial_actions[right],
                        row,
                        group_elements,
                        orbit_count,
                    ),
                    group_elements,
                    orbit_count,
                )
                == canonical_image(
                    template_module,
                    polynomial_actions[composition],
                    row,
                    group_elements,
                    orbit_count,
                )
                for row in atlas_sorted
            )
            class_action_cocycle_all &= class_ok

            for endpoint in endpoints:
                intermediate_endpoint = right[endpoint]
                row_ok = all(
                    row_maps[(composition, endpoint)][source_row]
                    == row_maps[(left, intermediate_endpoint)][
                        row_maps[(right, endpoint)][source_row]
                    ]
                    for source_row in range(len(kk_permutations[endpoint]))
                )
                row_cocycle_all &= row_ok
                cocycle_rows.append({
                    "left_normalizer_id": normalizer_ids[left],
                    "right_normalizer_id": normalizer_ids[right],
                    "composition_normalizer_id": normalizer_ids[composition],
                    "source_endpoint": endpoint,
                    "intermediate_endpoint": intermediate_endpoint,
                    "target_endpoint": composition[endpoint],
                    "state_transition_cocycle": state_ok,
                    "KK_row_transition_cocycle": row_ok,
                    "raw_group_ring_action_cocycle": raw_ok,
                    "canonical_template_class_cocycle": class_ok,
                })

    write_csv(out_dir / "normalizer_transition_cocycle_audit.csv", cocycle_rows)

    # Prove that the canonical atlas action factors through N/G ~= C2.
    atlas_ids = {row: f"A{index:02d}" for index, row in enumerate(atlas_sorted, start=1)}
    class_actions: Dict[Permutation, Dict[PolynomialRow, PolynomialRow]] = {}
    for permutation in normalizer:
        action = polynomial_actions[permutation]
        class_actions[permutation] = {
            row: canonical_image(
                template_module,
                action,
                row,
                group_elements,
                orbit_count,
            )
            for row in atlas_sorted
        }

    group_trivial = all(
        all(class_actions[element][row] == row for row in atlas_sorted)
        for element in group
    )
    nontrivial_coset = [element for element in normalizer if element not in group_set]
    representative_action = class_actions[nontrivial_coset[0]]
    coset_action_unique = all(
        class_actions[element] == representative_action
        for element in nontrivial_coset
    )
    residual_involution = all(
        representative_action[representative_action[row]] == row
        for row in atlas_sorted
    )

    unseen = set(atlas_sorted)
    atlas_orbits: List[List[PolynomialRow]] = []
    while unseen:
        start = min(unseen)
        image = representative_action[start]
        orbit = sorted({start, image})
        atlas_orbits.append(orbit)
        unseen -= set(orbit)

    atlas_orbit_rows: List[Dict[str, object]] = []
    atlas_ledger_rows: List[Dict[str, object]] = []
    orbit_id_by_row: Dict[PolynomialRow, str] = {}
    for orbit_index, orbit in enumerate(atlas_orbits, start=1):
        orbit_id = f"O{orbit_index:02d}"
        for row in orbit:
            orbit_id_by_row[row] = orbit_id
        atlas_orbit_rows.append({
            "atlas_orbit_id": orbit_id,
            "orbit_size": len(orbit),
            "fixed": len(orbit) == 1,
            "atlas_class_ids": ";".join(atlas_ids[row] for row in orbit),
        })

    for row in atlas_sorted:
        atlas_ledger_rows.append({
            "atlas_class_id": atlas_ids[row],
            "in_chart_C78": row in chart_a,
            "in_chart_C56": row in chart_b,
            "shared_between_charts": row in chart_intersection,
            "residual_image_atlas_class": atlas_ids[representative_action[row]],
            "atlas_orbit_id": orbit_id_by_row[row],
            "fixed_by_residual_quotient": representative_action[row] == row,
        })

    write_csv(out_dir / "full_normalizer_template_atlas.csv", atlas_ledger_rows)
    write_csv(out_dir / "normalizer_quotient_orbits.csv", atlas_orbit_rows)

    orbit_size_distribution = Counter(len(orbit) for orbit in atlas_orbits)
    quotient_factorization_exact = (
        group_trivial
        and coset_action_unique
        and residual_involution
        and len(atlas_orbits) == 18
        and dict(sorted(orbit_size_distribution.items())) == {1: 2, 2: 16}
    )

    endpoint_image_distribution = Counter(element[8] for element in normalizer)
    endpoint_orbit_exact = dict(sorted(endpoint_image_distribution.items())) == {
        5: 4,
        6: 4,
        7: 4,
        8: 4,
    }
    coset_chart_correspondence = all(
        (
            element in group_set
            and element[8] in (7, 8)
            and set(canonical_image(
                template_module,
                polynomial_actions[element],
                row,
                group_elements,
                orbit_count,
            ) for row in chart_a) == chart_a
        )
        or (
            element not in group_set
            and element[8] in (5, 6)
            and set(canonical_image(
                template_module,
                polynomial_actions[element],
                row,
                group_elements,
                orbit_count,
            ) for row in chart_a) == chart_b
        )
        for element in normalizer
    )

    full_normalizer_closure_exact = (
        set().union(
            *[
                {
                    canonical_image(
                        template_module,
                        polynomial_actions[element],
                        row,
                        group_elements,
                        orbit_count,
                    )
                    for row in chart_a
                }
                for element in normalizer
            ]
        )
        == atlas
        and len(atlas) == 34
    )

    duplicate_consistency_all = all(
        check() for check in polynomial_action_consistency.values()
    )

    exact_certificate = (
        exact_group_orders
        and dict(sorted(orbit_distribution.items())) == {4: 2, 8: 8}
        and endpoint_catalogue_census
        and chart_identifications
        and all_kernels_equal
        and duplicate_consistency_all
        and all_coordinate_covariance
        and all_kernel_covariance
        and all_universal_covariance
        and all_template_bijections
        and all_multiplicity_preservation
        and state_cocycle_all
        and row_cocycle_all
        and raw_action_cocycle_all
        and class_action_cocycle_all
        and endpoint_orbit_exact
        and coset_chart_correspondence
        and full_normalizer_closure_exact
        and quotient_factorization_exact
    )

    verdict = (
        "EHF_AMP_FOUND_03J_EXACT_FULL_NORMALIZER_ENDPOINT_ATLAS_AND_COCYCLE_PROVED"
        if exact_certificate
        else "EHF_AMP_FOUND_03J_FULL_NORMALIZER_ENDPOINT_ATLAS_FAILED"
    )

    certificate = {
        "theorem": (
            "For all n in the order-16 normalizer N and all endpoints "
            "e in {5,6,7,8}, the exact KK coordinate systems satisfy "
            "Q^(n(e)) P_n = R_(n,e) Q^(e), with strict state, row, raw "
            "group-ring, and canonical-template cocycle consistency."
        ),
        "groups": {
            "target_fibre_stabilizer_order": len(stabilizer),
            "G_order": len(group),
            "normalizer_order": len(normalizer),
            "quotient": "N/G ~= C2",
        },
        "endpoint_charts": {
            "C78": [7, 8],
            "C56": [5, 6],
            "T7_equals_T8": set(catalogues[7]) == set(catalogues[8]),
            "T5_equals_T6": set(catalogues[5]) == set(catalogues[6]),
            "templates_per_chart": 21,
            "shared_templates": len(chart_intersection),
            "union_size": len(atlas),
        },
        "endpoint_orbit_from_8": dict(sorted(endpoint_image_distribution.items())),
        "covariance": {
            "all_64_coordinate_identities": all_coordinate_covariance,
            "all_64_kernel_covariances": all_kernel_covariance,
            "all_64_universal_row_covariances": all_universal_covariance,
            "all_64_template_catalogue_bijections": all_template_bijections,
        },
        "cocycle": {
            "state_transition": state_cocycle_all,
            "KK_row_transition": row_cocycle_all,
            "raw_group_ring_action": raw_action_cocycle_all,
            "canonical_template_class_action": class_action_cocycle_all,
        },
        "quotient_action": {
            "G_acts_trivially_on_canonical_classes": group_trivial,
            "nontrivial_coset_action_unique": coset_action_unique,
            "residual_action_is_involution": residual_involution,
            "atlas_orbit_count": len(atlas_orbits),
            "atlas_orbit_size_distribution": dict(
                sorted(orbit_size_distribution.items())
            ),
        },
        "full_normalizer_closure": {
            "class_count": len(atlas),
            "exact": full_normalizer_closure_exact,
        },
        "checks": {
            "exact_group_orders": exact_group_orders,
            "endpoint_catalogue_census": endpoint_catalogue_census,
            "chart_identifications": chart_identifications,
            "all_endpoint_kernels_equal": all_kernels_equal,
            "all_coordinate_covariance": all_coordinate_covariance,
            "all_cocycles": (
                state_cocycle_all
                and row_cocycle_all
                and raw_action_cocycle_all
                and class_action_cocycle_all
            ),
            "quotient_factorization": quotient_factorization_exact,
        },
        "interpretation": (
            "The complete endpoint atlas is controlled by the quotient "
            "N/G ~= C2. The four normalizer-related endpoints form two "
            "equal-catalogue chart classes, and the full normalizer closure "
            "contains exactly the same 34 classes already seen in the "
            "endpoint-8/endpoint-6 two-chart atlas."
        ),
        "claim_boundary": (
            "This is restricted to the fixed anchor-1 reference fibre, the "
            "normalizer orbit of endpoints {5,6,7,8}, and n=8 target KK "
            "coordinates arising in the fixed-anchor 9->8 theorem. It does "
            "not prove anchor covariance or a general-n endpoint-atlas law."
        ),
    }
    with (out_dir / "exact_full_normalizer_endpoint_atlas_certificate.json").open("w") as handle:
        json.dump(json_safe(certificate), handle, indent=2)

    write_markdown(
        out_dir / "exact_full_normalizer_endpoint_atlas_audit.md",
        endpoint_rows,
        normalizer_rows,
        atlas_orbit_rows,
    )

    elapsed = time.time() - started
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "target_fibre_stabilizer_order": len(stabilizer),
        "G_order": len(group),
        "normalizer_order": len(normalizer),
        "endpoint_chart_classes": {"C78": [7, 8], "C56": [5, 6]},
        "endpoint_templates_each": 21,
        "endpoint_chart_overlap": len(chart_intersection),
        "full_normalizer_atlas_size": len(atlas),
        "normalizer_atlas_orbit_count": len(atlas_orbits),
        "normalizer_atlas_orbit_size_distribution": dict(
            sorted(orbit_size_distribution.items())
        ),
        "all_coordinate_covariance": all_coordinate_covariance,
        "all_kernel_covariance": all_kernel_covariance,
        "all_universal_row_covariance": all_universal_covariance,
        "all_template_catalogue_bijections": all_template_bijections,
        "all_transition_cocycles": (
            state_cocycle_all
            and row_cocycle_all
            and raw_action_cocycle_all
            and class_action_cocycle_all
        ),
        "normalizer_action_factors_through_C2": quotient_factorization_exact,
        "exact_full_normalizer_endpoint_atlas_and_cocycle": exact_certificate,
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "exact_full_normalizer_endpoint_atlas_certificate.json",
            "endpoint_chart_summary.csv",
            "normalizer_element_ledger.csv",
            "normalizer_endpoint_covariance.csv",
            "normalizer_template_transitions.csv",
            "normalizer_transition_cocycle_audit.csv",
            "full_normalizer_template_atlas.csv",
            "normalizer_quotient_orbits.csv",
            "exact_full_normalizer_endpoint_atlas_audit.md",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)
    with (out_dir / "verdict.json").open("w") as handle:
        json.dump(
            {
                "verdict": verdict,
                "exact_full_normalizer_endpoint_atlas_and_cocycle": exact_certificate,
                "atlas_size": len(atlas),
                "atlas_orbit_count": len(atlas_orbits),
            },
            handle,
            indent=2,
        )

    strict_failures: List[str] = []
    if args.strict:
        checks = {
            "group_orders": exact_group_orders,
            "state_orbit_distribution": (
                dict(sorted(orbit_distribution.items())) == {4: 2, 8: 8}
            ),
            "endpoint_catalogues": endpoint_catalogue_census,
            "two_chart_identification": chart_identifications,
            "endpoint_kernels": all_kernels_equal,
            "coordinate_covariance": all_coordinate_covariance,
            "kernel_covariance": all_kernel_covariance,
            "universal_covariance": all_universal_covariance,
            "template_bijections": all_template_bijections,
            "template_multiplicities": all_multiplicity_preservation,
            "state_cocycle": state_cocycle_all,
            "KK_row_cocycle": row_cocycle_all,
            "raw_action_cocycle": raw_action_cocycle_all,
            "class_action_cocycle": class_action_cocycle_all,
            "endpoint_orbit": endpoint_orbit_exact,
            "coset_chart_correspondence": coset_chart_correspondence,
            "full_normalizer_closure": full_normalizer_closure_exact,
            "quotient_C2_action": quotient_factorization_exact,
        }
        strict_failures = [name for name, passed in checks.items() if not passed]

    print("\nFull normalizer endpoint covariance")
    print(f"  target-fibre stabilizer order:      {len(stabilizer)}")
    print(f"  G order:                            {len(group)}")
    print(f"  normalizer order:                   {len(normalizer)}")
    print(f"  all 64 coordinate identities:       {all_coordinate_covariance}")
    print(f"  all 64 kernel covariances:          {all_kernel_covariance}")
    print(f"  all 64 universal covariances:       {all_universal_covariance}")
    print(f"  all 64 catalogue bijections:        {all_template_bijections}")

    print("\nEndpoint-chart atlas")
    print(f"  T7 = T8:                            {set(catalogues[7]) == set(catalogues[8])}")
    print(f"  T5 = T6:                            {set(catalogues[5]) == set(catalogues[6])}")
    print(f"  chart overlap:                      {len(chart_intersection)}")
    print(f"  full normalizer closure:            {len(atlas)}")
    print(f"  quotient atlas orbits:              {len(atlas_orbits)}")
    print(
        "  orbit-size distribution:           "
        f"{dict(sorted(orbit_size_distribution.items()))}"
    )

    print("\nCocycle consistency")
    print(f"  state transitions:                  {state_cocycle_all}")
    print(f"  KK row transitions:                 {row_cocycle_all}")
    print(f"  raw group-ring action:              {raw_action_cocycle_all}")
    print(f"  canonical template classes:         {class_action_cocycle_all}")
    print(f"  action factors through N/G ~= C2:   {quotient_factorization_exact}")

    print("\n" + "=" * 126)
    print("FINAL SUMMARY")
    print("=" * 126)
    print(f"Exact full-normalizer covariance:     {all_coordinate_covariance}")
    print(f"Exact endpoint transition cocycle:    {summary['all_transition_cocycles']}")
    print(f"Two endpoint chart classes:           {chart_identifications}")
    print(f"No classes beyond the 34 atlas:       {full_normalizer_closure_exact}")
    print(f"Verdict:                              {verdict}")
    print(f"elapsed:                              {elapsed:.2f} seconds")
    print(f"summary:                              {out_dir / 'summary.json'}")
    if args.strict:
        print(
            "strict checks:                        "
            f"{'PASS' if not strict_failures else 'FAIL'}"
        )
        if strict_failures:
            print("failed checks:                        " + ", ".join(strict_failures))
    print("=" * 126)

    if strict_failures:
        raise SystemExit(2)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prove exact full-normalizer KK endpoint covariance, two-chart "
            "template-atlas closure, and transition cocycle consistency."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--direct-script", required=True)
    parser.add_argument("--normal-form-script", required=True)
    parser.add_argument("--template-script", required=True)
    parser.add_argument("--normalizer-script", required=True)
    parser.add_argument("--endpoint-script", required=True)
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
