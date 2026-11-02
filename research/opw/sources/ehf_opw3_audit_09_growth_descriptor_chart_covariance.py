#!/usr/bin/env python3
"""
EHF-OPW3-AUDIT-09
=================
Growth-Descriptor Chart Covariance

Tests whether the growth information used to complete the residual OPW3 slow
sector is intrinsic or merely an artefact of the original canonical chart.

Charts vary:
  * anchor among all old/source labels;
  * anchored orientation policy: lexicographic minimum or maximum;
  * insertion order of the two newest labels.

For each chart the probe reconstructs the exact n-2 -> n growth bijection,
computes chart-relative LR3 active signatures and insertion descriptors, and
tests:

  1. parent-state invariance;
  2. descriptor transition determinism after conditioning on the source and
     target dihedral chart transitions;
  3. covariance of LR3-signature equitable closures;
  4. covariance of the residual slow-sector completions;
  5. inclusion of the complete lowest nontrivial eigenspace, not merely equality
     of the first eigenvalue.

The scientific outcomes (partition equality, raw descriptor invariance, and
all-chart recovery) are recorded, not assumed by --strict. Strict mode checks
only implementation identities and exact consistency requirements.

Dependencies: numpy, scipy
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import statistics
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Hashable, Iterable, List, Mapping, Sequence, Set, Tuple

import numpy as np
from scipy import sparse

SCRIPT_VERSION = "ehf_opw3_audit_09_2026-07-24"

Cycle = Tuple[int, ...]
Descriptor = Tuple[int, int]
Transform = Tuple[int, int]  # (reflection bit, cyclic shift)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_int_csv(text: str) -> List[int]:
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def load_base(path: Path):
    spec = importlib.util.spec_from_file_location("ehf_opw3_audit_01_base", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load base script: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rotate(sequence: Sequence[int], shift: int) -> Cycle:
    n = len(sequence)
    shift %= n
    return tuple(sequence[shift:]) + tuple(sequence[:shift])


def anchored_orientations(cycle: Cycle, anchor: int) -> Tuple[Cycle, Cycle]:
    pos = cycle.index(anchor)
    forward = rotate(cycle, pos)
    reverse = (anchor,) + tuple(reversed(forward[1:]))
    return forward, reverse


def chart_representative(cycle: Cycle, anchor: int, policy: str) -> Cycle:
    forward, reverse = anchored_orientations(cycle, anchor)
    if policy == "LEX_MIN":
        return min(forward, reverse)
    if policy == "LEX_MAX":
        return max(forward, reverse)
    raise ValueError(f"unknown orientation policy {policy}")


def dihedral_apply(sequence: Cycle, transform: Transform) -> Cycle:
    reflected, shift = transform
    base = tuple(reversed(sequence)) if reflected else sequence
    return rotate(base, shift)


def dihedral_transform(source: Cycle, target: Cycle) -> Transform:
    matches: List[Transform] = []
    n = len(source)
    for reflected in (0, 1):
        for shift in range(n):
            transform = (reflected, shift)
            if dihedral_apply(source, transform) == target:
                matches.append(transform)
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one dihedral transform, found {len(matches)}"
        )
    return matches[0]


def insert_after_gap(sequence: Sequence[int], gap: int, label: int) -> Cycle:
    arr = list(sequence)
    if gap < 0 or gap >= len(arr):
        raise ValueError(f"gap {gap} outside 0..{len(arr)-1}")
    arr.insert(gap + 1, label)
    return tuple(arr)


@dataclass(frozen=True)
class Chart:
    anchor: int
    policy: str
    order_name: str
    first_label: int
    second_label: int

    @property
    def orientation_id(self) -> str:
        return f"a{self.anchor}_{self.policy}"

    @property
    def chart_id(self) -> str:
        return f"{self.orientation_id}_{self.order_name}"


def chart_set(source_n: int) -> List[Chart]:
    charts = []
    for anchor in range(source_n):
        for policy in ("LEX_MIN", "LEX_MAX"):
            charts.append(
                Chart(
                    anchor=anchor,
                    policy=policy,
                    order_name="LOW_THEN_HIGH",
                    first_label=source_n,
                    second_label=source_n + 1,
                )
            )
            charts.append(
                Chart(
                    anchor=anchor,
                    policy=policy,
                    order_name="HIGH_THEN_LOW",
                    first_label=source_n + 1,
                    second_label=source_n,
                )
            )
    charts.sort(key=lambda chart: chart.chart_id)
    return charts


def orientation_charts(charts: Sequence[Chart]) -> List[Chart]:
    seen = set()
    result = []
    for chart in charts:
        if chart.orientation_id not in seen:
            seen.add(chart.orientation_id)
            result.append(chart)
    return result


def build_chart_growth_map(
    base,
    chart: Chart,
    source_cycles: Sequence[Cycle],
    target_index: Mapping[Cycle, int],
) -> Tuple[List[int], List[Descriptor], List[Cycle], List[Cycle]]:
    target_count = len(target_index)
    parent = [-1] * target_count
    descriptor: List[Descriptor | None] = [None] * target_count

    source_representatives = [
        chart_representative(cycle, chart.anchor, chart.policy)
        for cycle in source_cycles
    ]

    for source_id, source_rep in enumerate(source_representatives):
        source_n = len(source_rep)
        for gap1 in range(source_n):
            intermediate = insert_after_gap(
                source_rep, gap1, chart.first_label
            )
            for gap2 in range(source_n + 1):
                child_rep = insert_after_gap(
                    intermediate, gap2, chart.second_label
                )
                child = base.canonical_cycle(child_rep)
                target_id = target_index[child]
                if parent[target_id] != -1:
                    raise RuntimeError(
                        f"chart {chart.chart_id} produced duplicate child"
                    )
                parent[target_id] = source_id
                descriptor[target_id] = (gap1, gap2)

    if any(value < 0 for value in parent):
        raise RuntimeError(f"chart {chart.chart_id} missed target states")
    if any(value is None for value in descriptor):
        raise RuntimeError(f"chart {chart.chart_id} missed descriptors")

    target_cycles_by_id = [None] * target_count
    for cycle, target_id in target_index.items():
        target_cycles_by_id[target_id] = cycle

    target_representatives = [
        chart_representative(cycle, chart.anchor, chart.policy)
        for cycle in target_cycles_by_id
    ]

    return (
        parent,
        [value for value in descriptor if value is not None],
        source_representatives,
        target_representatives,
    )


def chart_active_signatures(
    base,
    cycles: Sequence[Cycle],
    cycle_index: Mapping[Cycle, int],
    pi_labels: Sequence[Hashable],
    anchor: int,
    policy: str,
) -> List[Tuple[int, ...]]:
    signatures: List[Tuple[int, ...]] = []
    for state_id, cycle in enumerate(cycles):
        representative = chart_representative(cycle, anchor, policy)
        active = []
        for slot in range(len(representative)):
            target_rep = base.circular_reverse(representative, slot, 3)
            target = base.canonical_cycle(target_rep)
            target_id = cycle_index[target]
            if target_id != state_id and pi_labels[target_id] == pi_labels[state_id]:
                active.append(slot)
        signatures.append(tuple(active))
    return signatures


def connected_components(adjacency: Sequence[Set[int]]):
    seen: Set[int] = set()
    components: List[List[int]] = []
    component_of: Dict[int, int] = {}
    for start in range(len(adjacency)):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        component = []
        while stack:
            u = stack.pop()
            component.append(u)
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        component.sort()
        components.append(component)
    components.sort(key=lambda comp: (-len(comp), comp[0]))
    for component_id, component in enumerate(components):
        for state in component:
            component_of[state] = component_id
    return components, component_of


def local_graph(global_adjacency: Sequence[Set[int]], vertices: Sequence[int]):
    index = {state: i for i, state in enumerate(vertices)}
    adjacency = [
        sorted(index[v] for v in global_adjacency[state] if v in index)
        for state in vertices
    ]
    return adjacency


def encode(values: Sequence[Hashable]) -> List[int]:
    unique = sorted(set(values), key=repr)
    mapping = {value: i for i, value in enumerate(unique)}
    return [mapping[value] for value in values]


def equitable_refinement(
    adjacency: Sequence[Sequence[int]],
    initial_values: Sequence[Hashable],
) -> List[int]:
    colors = encode(initial_values)
    while True:
        keys = []
        for u, neighbours in enumerate(adjacency):
            histogram = Counter(colors[v] for v in neighbours)
            keys.append((colors[u], tuple(sorted(histogram.items()))))
        unique = sorted(set(keys), key=repr)
        mapping = {key: i for i, key in enumerate(unique)}
        new_colors = [mapping[key] for key in keys]
        if new_colors == colors:
            return colors
        if len(set(new_colors)) == len(set(colors)):
            return new_colors
        colors = new_colors


def partition_key(colors: Sequence[int], vertices: Sequence[int]) -> Set[frozenset[int]]:
    cells: Dict[int, List[int]] = defaultdict(list)
    for local_state, color in enumerate(colors):
        cells[color].append(vertices[local_state])
    return {frozenset(cell) for cell in cells.values()}


def quotient_chain(
    adjacency: Sequence[Sequence[int]],
    colors: Sequence[int],
):
    cells = sorted(set(colors))
    position = {cell: i for i, cell in enumerate(cells)}
    members: Dict[int, List[int]] = defaultdict(list)
    for u, color in enumerate(colors):
        members[color].append(u)

    q = len(cells)
    counts = np.zeros((q, q), dtype=float)
    degrees = np.zeros(q, dtype=float)
    sizes = np.zeros(q, dtype=float)

    for cell in cells:
        i = position[cell]
        reps = members[cell]
        sizes[i] = len(reps)
        reference = None
        for u in reps:
            row = np.zeros(q, dtype=float)
            for v in adjacency[u]:
                row[position[colors[v]]] += 1.0
            if reference is None:
                reference = row
            elif not np.array_equal(reference, row):
                raise RuntimeError("partition is not equitable")
        counts[i] = reference
        degrees[i] = reference.sum()

    if q == 1 and degrees[0] == 0:
        return np.array([[1.0]]), np.array([1.0]), degrees

    p = np.divide(
        counts,
        degrees[:, None],
        out=np.zeros_like(counts),
        where=degrees[:, None] > 0,
    )
    volume = float(np.dot(sizes, degrees))
    pi = sizes * degrees / volume
    return p, pi, degrees


def quotient_spectrum(p: np.ndarray, pi: np.ndarray) -> np.ndarray:
    if p.shape[0] == 1:
        return np.array([0.0])
    root = np.sqrt(pi)
    symmetric = np.divide(
        root[:, None] * p,
        root[None, :],
        out=np.zeros_like(p),
        where=root[None, :] > 0,
    )
    symmetric = 0.5 * (symmetric + symmetric.T)
    mu = np.linalg.eigvalsh(symmetric)
    lam = np.sort(1.0 - mu)
    lam[np.abs(lam) < 1e-11] = 0.0
    return lam


def full_normalized_modes(
    adjacency: Sequence[Sequence[int]],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(adjacency)
    degrees = np.array([len(row) for row in adjacency], dtype=float)
    rows, cols = [], []
    for u, neighbours in enumerate(adjacency):
        for v in neighbours:
            rows.append(u)
            cols.append(v)
    matrix = sparse.csr_matrix(
        (np.ones(len(rows)), (rows, cols)),
        shape=(n, n),
        dtype=float,
    )
    inv = 1.0 / np.sqrt(degrees)
    symmetric = sparse.diags(inv) @ matrix @ sparse.diags(inv)
    mu, vectors = np.linalg.eigh(symmetric.toarray())
    order = np.argsort(mu)[::-1]
    mu = mu[order]
    vectors = vectors[:, order]
    lam = 1.0 - mu
    order = np.argsort(lam)
    lam = lam[order]
    vectors = vectors[:, order]
    lam[np.abs(lam) < 1e-11] = 0.0
    return lam, vectors, degrees


def quotient_basis(colors: Sequence[int], degrees: np.ndarray) -> np.ndarray:
    columns = []
    for cell in sorted(set(colors)):
        vector = np.zeros(len(colors), dtype=float)
        members = [i for i, color in enumerate(colors) if color == cell]
        vector[members] = np.sqrt(degrees[members])
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm
        columns.append(vector)
    return np.column_stack(columns)


def eigenspace_projection_mass(
    colors: Sequence[int],
    degrees: np.ndarray,
    modes: np.ndarray,
) -> float:
    basis = quotient_basis(colors, degrees)
    return float(
        np.linalg.norm(basis.T @ modes, ord="fro") ** 2 / modes.shape[1]
    )


def transition_ambiguity(
    reference_descriptors: Sequence[Descriptor],
    chart_descriptors: Sequence[Descriptor],
    source_transforms: Sequence[Transform],
    target_transforms: Sequence[Transform],
    parent: Sequence[int],
):
    raw: Dict[Hashable, Set[Descriptor]] = defaultdict(set)
    source_conditioned: Dict[Hashable, Set[Descriptor]] = defaultdict(set)
    full_conditioned: Dict[Hashable, Set[Descriptor]] = defaultdict(set)

    for target_id, descriptor_ref in enumerate(reference_descriptors):
        descriptor_chart = chart_descriptors[target_id]
        source_transform = source_transforms[parent[target_id]]
        target_transform = target_transforms[target_id]

        raw[descriptor_ref].add(descriptor_chart)
        source_conditioned[
            (source_transform, descriptor_ref)
        ].add(descriptor_chart)
        full_conditioned[
            (source_transform, target_transform, descriptor_ref)
        ].add(descriptor_chart)

    def summary(mapping):
        ambiguous = sum(len(images) > 1 for images in mapping.values())
        max_images = max((len(images) for images in mapping.values()), default=0)
        return len(mapping), ambiguous, max_images

    return summary(raw), summary(source_conditioned), summary(full_conditioned)


def pi_text(label) -> str:
    return "|".join(",".join(str(x) for x in side) for side in label)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit growth-descriptor chart covariance in OPW3."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--target-ns", type=parse_int_csv, default=[7, 9])
    parser.add_argument("--gap-match-tolerance", type=float, default=1e-7)
    parser.add_argument("--eigenspace-tolerance", type=float, default=1e-7)
    parser.add_argument("--out-dir", default="runs/ehf_opw3_audit_09")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    base_path = Path(args.base_script).resolve()
    base = load_base(base_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 124)
    print("EHF-OPW3-AUDIT-09: GROWTH-DESCRIPTOR CHART COVARIANCE")
    print("=" * 124)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"target n values:      {args.target_ns}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    checks: Dict[str, bool] = {}
    chart_rows: List[dict] = []
    closure_rows: List[dict] = []
    residual_rows: List[dict] = []
    summaries: Dict[str, dict] = {}
    started_all = time.perf_counter()

    for target_n in args.target_ns:
        source_n = target_n - 2
        started = time.perf_counter()

        source_cycles = base.generate_cycles(source_n)
        source_index = {cycle: i for i, cycle in enumerate(source_cycles)}
        source_pi = [base.pi_label(cycle) for cycle in source_cycles]

        target_cycles = base.generate_cycles(target_n)
        target_index = {cycle: i for i, cycle in enumerate(target_cycles)}
        target_pi = [base.pi_label(cycle) for cycle in target_cycles]

        source_build = base.build_preserve_graph(
            source_cycles,
            source_index,
            source_pi,
            "OPW3",
            base.GRAPH_LENGTHS["OPW3"],
        )
        target_build = base.build_preserve_graph(
            target_cycles,
            target_index,
            target_pi,
            "OPW3",
            base.GRAPH_LENGTHS["OPW3"],
        )
        target_components, _ = connected_components(target_build.adjacency)

        charts = chart_set(source_n)
        orient_charts = orientation_charts(charts)
        reference_chart = next(
            chart for chart in charts
            if chart.anchor == 0
            and chart.policy == "LEX_MIN"
            and chart.order_name == "LOW_THEN_HIGH"
        )

        chart_growth = {}
        orientation_source_signatures = {}
        orientation_target_signatures = {}

        for chart in charts:
            parent, descriptors, source_reps, target_reps = build_chart_growth_map(
                base,
                chart,
                source_cycles,
                target_index,
            )
            chart_growth[chart.chart_id] = {
                "parent": parent,
                "descriptors": descriptors,
                "source_reps": source_reps,
                "target_reps": target_reps,
            }
            checks[f"n{target_n}_{chart.chart_id}_bijection"] = (
                len(parent) == len(target_cycles)
                and len(descriptors) == len(target_cycles)
                and len(set(zip(parent, descriptors))) == len(target_cycles)
            )

        for chart in orient_charts:
            orientation_source_signatures[chart.orientation_id] = (
                chart_active_signatures(
                    base,
                    source_cycles,
                    source_index,
                    source_pi,
                    chart.anchor,
                    chart.policy,
                )
            )
            orientation_target_signatures[chart.orientation_id] = (
                chart_active_signatures(
                    base,
                    target_cycles,
                    target_index,
                    target_pi,
                    chart.anchor,
                    chart.policy,
                )
            )

        reference = chart_growth[reference_chart.chart_id]
        reference_parent = reference["parent"]
        reference_descriptors = reference["descriptors"]

        parent_invariant_all = True
        for chart in charts:
            data = chart_growth[chart.chart_id]
            parent_invariant = data["parent"] == reference_parent
            parent_invariant_all &= parent_invariant
            checks[f"n{target_n}_{chart.chart_id}_parent_invariant"] = (
                parent_invariant
            )

            source_transforms = [
                dihedral_transform(
                    reference["source_reps"][state_id],
                    data["source_reps"][state_id],
                )
                for state_id in range(len(source_cycles))
            ]
            target_transforms = [
                dihedral_transform(
                    reference["target_reps"][state_id],
                    data["target_reps"][state_id],
                )
                for state_id in range(len(target_cycles))
            ]

            raw, source_cond, full_cond = transition_ambiguity(
                reference_descriptors,
                data["descriptors"],
                source_transforms,
                target_transforms,
                reference_parent,
            )
            checks[
                f"n{target_n}_{chart.chart_id}_fully_conditioned_functional"
            ] = full_cond[1] == 0

            chart_rows.append({
                "target_n": target_n,
                "source_n": source_n,
                "chart_id": chart.chart_id,
                "orientation_id": chart.orientation_id,
                "anchor": chart.anchor,
                "orientation_policy": chart.policy,
                "insertion_order": chart.order_name,
                "states": len(target_cycles),
                "parent_invariant": parent_invariant,
                "raw_descriptor_keys": raw[0],
                "raw_ambiguous_keys": raw[1],
                "raw_max_images": raw[2],
                "source_conditioned_keys": source_cond[0],
                "source_conditioned_ambiguous_keys": source_cond[1],
                "source_conditioned_max_images": source_cond[2],
                "fully_conditioned_keys": full_cond[0],
                "fully_conditioned_ambiguous_keys": full_cond[1],
                "fully_conditioned_max_images": full_cond[2],
            })

        # Signature-closure covariance across every chamber and orientation chart.
        reference_orientation = reference_chart.orientation_id
        reference_target_signature = orientation_target_signatures[
            reference_orientation
        ]
        reference_partitions = {}

        for component_id, vertices in enumerate(target_components):
            local = local_graph(target_build.adjacency, vertices)
            ref_colors = equitable_refinement(
                local,
                [reference_target_signature[state] for state in vertices],
            )
            reference_partitions[component_id] = partition_key(
                ref_colors, vertices
            )

            for chart in orient_charts:
                signature = orientation_target_signatures[chart.orientation_id]
                colors = equitable_refinement(
                    local,
                    [signature[state] for state in vertices],
                )
                key = partition_key(colors, vertices)
                closure_rows.append({
                    "target_n": target_n,
                    "component_id": component_id,
                    "pi_label": pi_text(target_pi[vertices[0]]),
                    "component_states": len(vertices),
                    "orientation_id": chart.orientation_id,
                    "anchor": chart.anchor,
                    "orientation_policy": chart.policy,
                    "cells": len(key),
                    "equals_reference_partition": (
                        key == reference_partitions[component_id]
                    ),
                })

        # Discover canonical residuals after parent-signature completion.
        canonical_source_signature = orientation_source_signatures[
            reference_orientation
        ]
        canonical_target_signature = orientation_target_signatures[
            reference_orientation
        ]
        residual_components = []
        full_modes_cache = {}

        for component_id, vertices in enumerate(target_components):
            local = local_graph(target_build.adjacency, vertices)
            values = [
                (
                    canonical_target_signature[state],
                    canonical_source_signature[reference_parent[state]],
                )
                for state in vertices
            ]
            colors = equitable_refinement(local, values)
            p, pi, _ = quotient_chain(local, colors)
            qspec = quotient_spectrum(p, pi)
            if len(set(colors)) <= 1:
                continue

            lam, vectors, degrees = full_normalized_modes(local)
            full_gap = float(lam[1])
            quotient_gap = float(qspec[1])
            if quotient_gap - full_gap > args.gap_match_tolerance:
                residual_components.append(component_id)
                lowest = [
                    i for i in range(1, len(lam))
                    if abs(float(lam[i]) - full_gap)
                    <= args.gap_match_tolerance
                ]
                full_modes_cache[component_id] = (
                    local,
                    lam,
                    vectors[:, lowest],
                    degrees,
                )

        candidate_names = (
            "CURRENT_SIGNATURE",
            "CURRENT_PLUS_PARENT_SIGNATURE",
            "CURRENT_PLUS_DESCRIPTOR",
            "CURRENT_PLUS_PARENT_SIGNATURE_PLUS_DESCRIPTOR",
        )

        reference_candidate_partitions = {}

        for component_id in residual_components:
            vertices = target_components[component_id]
            local, lam, lowest_modes, degrees = full_modes_cache[component_id]
            full_gap = float(lam[1])

            for chart in charts:
                data = chart_growth[chart.chart_id]
                target_signature = orientation_target_signatures[
                    chart.orientation_id
                ]
                source_signature = orientation_source_signatures[
                    chart.orientation_id
                ]

                candidate_values = {
                    "CURRENT_SIGNATURE": [
                        target_signature[state] for state in vertices
                    ],
                    "CURRENT_PLUS_PARENT_SIGNATURE": [
                        (
                            target_signature[state],
                            source_signature[data["parent"][state]],
                        )
                        for state in vertices
                    ],
                    "CURRENT_PLUS_DESCRIPTOR": [
                        (
                            target_signature[state],
                            data["descriptors"][state],
                        )
                        for state in vertices
                    ],
                    "CURRENT_PLUS_PARENT_SIGNATURE_PLUS_DESCRIPTOR": [
                        (
                            target_signature[state],
                            source_signature[data["parent"][state]],
                            data["descriptors"][state],
                        )
                        for state in vertices
                    ],
                }

                for candidate_name in candidate_names:
                    colors = equitable_refinement(
                        local, candidate_values[candidate_name]
                    )
                    key = partition_key(colors, vertices)
                    p, pi, _ = quotient_chain(local, colors)
                    qspec = quotient_spectrum(p, pi)
                    qgap = float(qspec[1]) if len(qspec) > 1 else 0.0
                    gap_visible = (
                        len(set(colors)) > 1
                        and abs(qgap - full_gap)
                        <= args.gap_match_tolerance
                    )
                    eigenspace_mass = eigenspace_projection_mass(
                        colors, degrees, lowest_modes
                    )
                    eigenspace_complete = (
                        abs(eigenspace_mass - 1.0)
                        <= args.eigenspace_tolerance
                    )

                    ref_key_id = (component_id, candidate_name)
                    if chart.chart_id == reference_chart.chart_id:
                        reference_candidate_partitions[ref_key_id] = key

                    residual_rows.append({
                        "target_n": target_n,
                        "component_id": component_id,
                        "pi_label": pi_text(target_pi[vertices[0]]),
                        "component_states": len(vertices),
                        "chart_id": chart.chart_id,
                        "orientation_id": chart.orientation_id,
                        "anchor": chart.anchor,
                        "orientation_policy": chart.policy,
                        "insertion_order": chart.order_name,
                        "candidate": candidate_name,
                        "final_cells": len(key),
                        "compression_ratio": len(key) / len(vertices),
                        "full_gap": full_gap,
                        "quotient_gap": qgap,
                        "gap_ratio": qgap / full_gap,
                        "slow_gap_visible": gap_visible,
                        "lowest_eigenspace_projection_mass": eigenspace_mass,
                        "lowest_eigenspace_complete": eigenspace_complete,
                        "equals_reference_partition": None,
                    })

        # Fill reference-partition equality after all reference keys exist.
        for row in residual_rows:
            if row["target_n"] != target_n:
                continue
            component_id = row["component_id"]
            candidate_name = row["candidate"]
            vertices = target_components[component_id]
            chart_id = row["chart_id"]
            chart = next(chart for chart in charts if chart.chart_id == chart_id)
            data = chart_growth[chart_id]
            target_signature = orientation_target_signatures[
                chart.orientation_id
            ]
            source_signature = orientation_source_signatures[
                chart.orientation_id
            ]
            local = full_modes_cache[component_id][0]

            if candidate_name == "CURRENT_SIGNATURE":
                values = [target_signature[state] for state in vertices]
            elif candidate_name == "CURRENT_PLUS_PARENT_SIGNATURE":
                values = [
                    (
                        target_signature[state],
                        source_signature[data["parent"][state]],
                    )
                    for state in vertices
                ]
            elif candidate_name == "CURRENT_PLUS_DESCRIPTOR":
                values = [
                    (
                        target_signature[state],
                        data["descriptors"][state],
                    )
                    for state in vertices
                ]
            else:
                values = [
                    (
                        target_signature[state],
                        source_signature[data["parent"][state]],
                        data["descriptors"][state],
                    )
                    for state in vertices
                ]

            colors = equitable_refinement(local, values)
            key = partition_key(colors, vertices)
            row["equals_reference_partition"] = (
                key == reference_candidate_partitions[
                    (component_id, candidate_name)
                ]
            )

        closure_here = [
            row for row in closure_rows if row["target_n"] == target_n
        ]
        residual_here = [
            row for row in residual_rows if row["target_n"] == target_n
        ]

        closure_equal_fraction = (
            sum(row["equals_reference_partition"] for row in closure_here)
            / len(closure_here)
        )

        candidate_summary = {}
        for candidate_name in candidate_names:
            rows = [
                row for row in residual_here
                if row["candidate"] == candidate_name
            ]
            candidate_summary[candidate_name] = {
                "chart_component_cases": len(rows),
                "gap_visible_cases": sum(
                    row["slow_gap_visible"] for row in rows
                ),
                "eigenspace_complete_cases": sum(
                    row["lowest_eigenspace_complete"] for row in rows
                ),
                "partition_equal_reference_cases": sum(
                    row["equals_reference_partition"] for row in rows
                ),
                "mean_compression_ratio": (
                    statistics.fmean(
                        row["compression_ratio"] for row in rows
                    )
                    if rows else None
                ),
            }

        summaries[f"n{target_n}"] = {
            "source_n": source_n,
            "source_states": len(source_cycles),
            "target_states": len(target_cycles),
            "charts": len(charts),
            "orientation_charts": len(orient_charts),
            "parent_invariant_all_charts": parent_invariant_all,
            "signature_closure_equal_reference_fraction": (
                closure_equal_fraction
            ),
            "canonical_residual_components": residual_components,
            "candidate_summary": candidate_summary,
            "elapsed_seconds": time.perf_counter() - started,
        }

        print(
            f"[{source_n}->{target_n}] charts={len(charts)} "
            f"orientation-charts={len(orient_charts)} "
            f"parent-invariant={parent_invariant_all}"
        )
        print(
            f"  LR3 closure covariance: "
            f"{sum(r['equals_reference_partition'] for r in closure_here)}/"
            f"{len(closure_here)}"
        )
        print(
            f"  canonical residual chambers={residual_components}"
        )
        for name, result in candidate_summary.items():
            print(
                f"    {name:<47} "
                f"gap={result['gap_visible_cases']}/"
                f"{result['chart_component_cases']} "
                f"eigenspace={result['eigenspace_complete_cases']}/"
                f"{result['chart_component_cases']} "
                f"partition={result['partition_equal_reference_cases']}/"
                f"{result['chart_component_cases']} "
                f"mean-compression={result['mean_compression_ratio']:.6f}"
            )
        print(f"  elapsed={summaries[f'n{target_n}']['elapsed_seconds']:.2f}s")
        print()

    write_csv(out_dir / "chart_summary.csv", chart_rows)
    write_csv(out_dir / "signature_closure_covariance.csv", closure_rows)
    write_csv(out_dir / "residual_completion_chart_covariance.csv", residual_rows)

    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-OPW3-AUDIT-09",
        "title": "Growth-Descriptor Chart Covariance",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "interpretation_guardrail": (
            "Chart-relative descriptors are coordinate data unless their "
            "completed partitions or slow subspaces are shown to be chart "
            "covariant. Slow modes remain structural diffusion modes."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_OPW3_AUDIT_09_GROWTH_DESCRIPTOR_CHART_COVARIANCE_PASS"
            if strict_pass else
            "EHF_OPW3_AUDIT_09_GROWTH_DESCRIPTOR_CHART_COVARIANCE_FAIL"
        ),
    }
    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print("=" * 124)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {summary['elapsed_seconds']:.2f}s")
    print("=" * 124)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
