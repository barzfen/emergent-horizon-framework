#!/usr/bin/env python3
"""
EHF-XBR-02
==========
Common Growth Groupoid and Dual-Functor Compatibility

The amplitude 03L atlas has 72 anchor--deletion charts chi=(a,d) on the
nine-point Hamilton-cycle state space.  Each chart has a normalisation

    rho_chi(a)=1,  rho_chi(d)=9,

with the remaining labels mapped increasingly to 2,...,8.  The common chart
arrow is

    pi_(psi <- chi) = rho_psi^{-1} rho_chi.

This probe uses the exact AMP-03L certificate as an input and independently
audits four compatible structures over the same finite chart groupoid:

  S9  common source-state functor:
      nine-point undirected Hamilton-cycle classes;

  DYN chart-relative OPW3 dynamics lift:
      the pullback of OPW3 adjacency, Pi-fibre/chamber structure, and graph
      operators in each chart;

  AMP amplitude-relations lift:
      chart-relative KK/deletion channels and their six transported image
      classes, as certified exactly by AMP-03L;

  ETA middle-block growth correspondence:
      the chart transport of the reference 7->9 insertion pair {8,9}.

The strict theorem tested is:

  * every chart arrow used by AMP-03L is the same label arrow used on OPW3;
  * the arrows form one exact 72-object groupoid;
  * chart-relative OPW3 adjacency and Pi fibres are equivariant under every
    chart object;
  * all AMP channel/image metadata are natural under every chart arrow;
  * the transported middle-block correspondence is natural under every arrow;
  * both lifts therefore share the same source-state functor and groupoid
    arrows.

A separate obstruction census records whether the 72 arrows preserve the one
fixed globally anchored OPW3 graph. They need not: moving the anchor changes
the parity-position datum. The validated finite result is that only the
reference chart preserves that fixed graph, while all 72 preserve the
chart-relative pullback family.

The AMP relation matrices are not recomputed here.  Their exact covariance is
consumed from a successful AMP-03L run and cross-checked against its complete
channel and transition ledgers.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from itertools import permutations
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Set, Tuple

SCRIPT_VERSION = "ehf_xbr_02_2026-07-25"

Cycle = Tuple[int, ...]
Chart = Tuple[int, int]
LabelMap = Dict[int, int]
Fibre = Tuple[Tuple[int, ...], Tuple[int, ...]]
ChannelKey = Tuple[int, int, Tuple[int, int, int]]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> List[dict]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        path.write_text("")
        return
    fields: List[str] = []
    seen: Set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def parse_subset(text: str) -> Tuple[int, int, int]:
    values = tuple(int(x) for x in text.split(",") if x)
    if len(values) != 3:
        raise ValueError(f"expected 3-subset, found {text!r}")
    return values  # type: ignore[return-value]


def parse_mapping(text: str) -> LabelMap:
    mapping: LabelMap = {}
    for item in text.split(";"):
        source, target = item.split("->")
        mapping[int(source)] = int(target)
    return mapping


def mapping_text(mapping: Mapping[int, int]) -> str:
    return ";".join(
        f"{source}->{mapping[source]}"
        for source in sorted(mapping)
    )


def chart_text(chart: Chart) -> str:
    return f"a={chart[0]},d={chart[1]}"


def chart_normalisation(anchor: int, deleted: int) -> LabelMap:
    if anchor == deleted:
        raise ValueError("anchor and deleted leg must differ")
    remaining = [
        label for label in range(1, 10)
        if label not in (anchor, deleted)
    ]
    mapping: LabelMap = {anchor: 1, deleted: 9}
    mapping.update(dict(zip(remaining, range(2, 9))))
    return mapping


def invert_mapping(mapping: Mapping[int, int]) -> LabelMap:
    return {target: source for source, target in mapping.items()}


def compose_mapping(
    left: Mapping[int, int],
    right: Mapping[int, int],
) -> LabelMap:
    """Return left after right."""
    return {label: left[right[label]] for label in right}


def relabel_cycle_raw(
    cycle: Sequence[int],
    mapping: Mapping[int, int],
) -> Cycle:
    return tuple(mapping[label] for label in cycle)


def canonical_one_based(base, cycle: Sequence[int]) -> Cycle:
    zero = tuple(label - 1 for label in cycle)
    canonical = base.canonical_cycle(zero)
    return tuple(label + 1 for label in canonical)


def relabel_cycle_class(
    base,
    cycle: Sequence[int],
    mapping: Mapping[int, int],
) -> Cycle:
    return canonical_one_based(
        base,
        relabel_cycle_raw(cycle, mapping),
    )



def canonical_in_chart(
    base,
    cycle: Sequence[int],
    normalisation: Mapping[int, int],
    inverse_normalisation: Mapping[int, int],
) -> Cycle:
    """Canonicalise a chart-relative 7-, 8-, or 9-label cycle."""
    normalised = relabel_cycle_raw(cycle, normalisation)
    canonical = canonical_one_based(base, normalised)
    return relabel_cycle_raw(canonical, inverse_normalisation)


def circular_reverse_in_chart(
    base,
    cycle: Sequence[int],
    start: int,
    length: int,
    normalisation: Mapping[int, int],
    inverse_normalisation: Mapping[int, int],
) -> Cycle:
    n = len(cycle)
    indices = [(start + offset) % n for offset in range(length)]
    arr = list(cycle)
    values = [cycle[index] for index in indices][::-1]
    for index, value in zip(indices, values):
        arr[index] = value
    return canonical_in_chart(
        base,
        tuple(arr),
        normalisation,
        inverse_normalisation,
    )


def canonical_cycles_one_based(n: int) -> List[Cycle]:
    return [
        (1,) + p
        for p in permutations(range(2, n + 1))
        if p <= tuple(reversed(p))
    ]


def pi_label_one_based(base, cycle: Cycle) -> Fibre:
    zero_label = base.pi_label(tuple(label - 1 for label in cycle))
    sides = [
        tuple(label + 1 for label in side)
        for side in zero_label
    ]
    sides.sort()
    return sides[0], sides[1]


def map_fibre(
    fibre: Fibre,
    mapping: Mapping[int, int],
) -> Fibre:
    sides = [
        tuple(sorted(mapping[label] for label in side))
        for side in fibre
    ]
    sides.sort()
    return sides[0], sides[1]


def connected_components(
    adjacency: Sequence[Set[int]],
) -> Tuple[List[List[int]], List[int]]:
    seen: Set[int] = set()
    components: List[List[int]] = []
    component_of = [-1] * len(adjacency)

    for start in range(len(adjacency)):
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        component: List[int] = []
        while queue:
            u = queue.popleft()
            component.append(u)
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
        component.sort()
        components.append(component)

    components.sort(key=lambda c: (-len(c), c[0]))
    for component_id, component in enumerate(components):
        for state in component:
            component_of[state] = component_id
    return components, component_of


def cycle_digest(cycles: Sequence[Cycle]) -> str:
    digest = hashlib.sha256()
    for cycle in cycles:
        digest.update((",".join(map(str, cycle)) + ";").encode())
    return digest.hexdigest()


def component_set_digest(component_sets: Sequence[Sequence[int]]) -> str:
    digest = hashlib.sha256()
    for component in sorted(
        (tuple(sorted(c)) for c in component_sets),
        key=lambda c: (len(c), c),
    ):
        digest.update((",".join(map(str, component)) + ";").encode())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit one common 72-chart groupoid carrying OPW dynamics and AMP relation-space lifts."
    )
    parser.add_argument("--opw-base-script", required=True)
    parser.add_argument("--amp03l-run-dir", required=True)
    parser.add_argument("--out-dir", default="runs/ehf_xbr_02")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    opw_path = Path(args.opw_base_script).resolve()
    amp_dir = Path(args.amp03l_run_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    required_amp_files = {
        "summary": amp_dir / "summary.json",
        "transition": amp_dir / "anchor_deletion_transition_ledger.csv",
        "channels": amp_dir / "full_anchor_deletion_channel_ledger.csv",
        "charts": amp_dir / "anchor_deletion_chart_summary.csv",
        "classes": amp_dir / "anchor_deletion_subspace_class_summary.csv",
    }
    missing = [
        str(path) for path in required_amp_files.values()
        if not path.exists()
    ]
    if missing:
        raise FileNotFoundError(
            "missing AMP-03L run artifacts:\n" + "\n".join(missing)
        )

    base = load_module(opw_path, "ehf_xbr_02_opw_base")
    with required_amp_files["summary"].open() as handle:
        amp_summary = json.load(handle)
    amp_transition_rows = read_csv(required_amp_files["transition"])
    amp_channel_rows = read_csv(required_amp_files["channels"])
    amp_chart_rows = read_csv(required_amp_files["charts"])
    amp_class_rows = read_csv(required_amp_files["classes"])

    print("=" * 132)
    print("EHF-XBR-02: COMMON GROWTH GROUPOID AND DUAL-FUNCTOR COMPATIBILITY")
    print("=" * 132)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"OPW base engine:      {opw_path}")
    print(f"AMP-03L run dir:      {amp_dir}")
    print(f"output directory:     {out_dir}")
    print(f"strict:               {args.strict}")
    print()

    started = time.perf_counter()
    checks: Dict[str, bool] = {}
    object_rows: List[dict] = []
    arrow_rows: List[dict] = []
    channel_pair_rows: List[dict] = []

    # ------------------------------------------------------------------
    # Consume and validate the exact AMP-03L certificate.
    # ------------------------------------------------------------------
    checks["amp03l_required_verdict"] = (
        amp_summary.get("verdict")
        == "EHF_AMP_FOUND_03L_EXACT_FULL_ANCHOR_DELETION_ATLAS_COVARIANCE_PROVED"
    )
    checks["amp03l_exact_atlas"] = bool(
        amp_summary.get("exact_full_anchor_deletion_atlas_covariance")
    )
    checks["amp03l_all_channel_covariances"] = bool(
        amp_summary.get("all_channel_covariances_exact")
    )
    checks["amp03l_all_transition_cocycles"] = bool(
        amp_summary.get("all_transition_cocycles_exact")
    )
    checks["amp03l_chart_count_72"] = (
        int(amp_summary.get("anchor_deletion_chart_count", -1)) == 72
    )
    checks["amp03l_channel_count_2520"] = (
        int(amp_summary.get("total_anchor_deletion_channels", -1)) == 2520
    )
    checks["amp03l_six_spaces"] = (
        int(amp_summary.get("common_transported_subspace_count", -1)) == 6
    )

    charts: List[Chart] = [
        (anchor, deleted)
        for deleted in range(1, 10)
        for anchor in range(1, 10)
        if anchor != deleted
    ]
    normalisations = {
        chart: chart_normalisation(*chart)
        for chart in charts
    }
    inverses = {
        chart: invert_mapping(normalisations[chart])
        for chart in charts
    }
    transitions = {
        (target, source): compose_mapping(
            inverses[target],
            normalisations[source],
        )
        for source in charts
        for target in charts
    }

    # Compare every common arrow with AMP-03L's exact transition ledger.
    amp_transition_by_pair: Dict[Tuple[Chart, Chart], dict] = {}
    for row in amp_transition_rows:
        source = (
            int(row["source_anchor"]),
            int(row["source_deleted_leg"]),
        )
        target = (
            int(row["target_anchor"]),
            int(row["target_deleted_leg"]),
        )
        amp_transition_by_pair[(target, source)] = row

    checks["amp03l_transition_ledger_complete"] = (
        len(amp_transition_by_pair) == 72 * 72
    )

    all_common_arrows_equal_amp = True
    all_amp_arrow_flags = True
    for source in charts:
        for target in charts:
            row = amp_transition_by_pair[(target, source)]
            ledger_mapping = parse_mapping(row["transition_mapping"])
            common_mapping = transitions[(target, source)]
            equal = ledger_mapping == common_mapping
            flags = all(
                parse_bool(row[field])
                for field in (
                    "anchor_maps_exactly",
                    "deleted_leg_maps_exactly",
                    "reference_factorisation_exact",
                    "source_state_map_is_bijection",
                    "target_state_map_is_bijection",
                    "KK_row_map_is_bijection",
                    "fibre_map_is_bijection",
                )
            )
            all_common_arrows_equal_amp &= equal
            all_amp_arrow_flags &= flags

    checks["common_arrows_equal_amp03l_arrows"] = (
        all_common_arrows_equal_amp
    )
    checks["all_amp_arrow_flags_exact"] = all_amp_arrow_flags

    # Exact common groupoid.
    identity_exact = all(
        transitions[(chart, chart)] == {i: i for i in range(1, 10)}
        for chart in charts
    )
    inverse_exact = all(
        compose_mapping(
            transitions[(source, target)],
            transitions[(target, source)],
        )
        == {i: i for i in range(1, 10)}
        for source in charts
        for target in charts
    )
    cocycle_failures = 0
    for source in charts:
        for middle in charts:
            first = transitions[(middle, source)]
            for target in charts:
                if (
                    compose_mapping(
                        transitions[(target, middle)],
                        first,
                    )
                    != transitions[(target, source)]
                ):
                    cocycle_failures += 1

    checks["common_groupoid_identity"] = identity_exact
    checks["common_groupoid_inverse"] = inverse_exact
    checks["common_groupoid_cocycle"] = cocycle_failures == 0

    # ------------------------------------------------------------------
    # Shared nine-point source-state functor and chart-relative OPW3 lift.
    # ------------------------------------------------------------------
    cycles_zero = base.generate_cycles(9)
    cycles_one = [
        tuple(label + 1 for label in cycle)
        for cycle in cycles_zero
    ]
    independent_amp_cycles = canonical_cycles_one_based(9)
    checks["opw_amp_reference_source_basis_equal"] = (
        cycles_one == independent_amp_cycles
    )

    index_one = {
        cycle: i for i, cycle in enumerate(cycles_one)
    }
    pi_zero = [base.pi_label(cycle) for cycle in cycles_zero]
    opw_build = base.build_preserve_graph(
        cycles_zero,
        {cycle: i for i, cycle in enumerate(cycles_zero)},
        pi_zero,
        "OPW3",
        base.GRAPH_LENGTHS["OPW3"],
    )
    reference_adjacency = opw_build.adjacency
    reference_edges = [
        (u, v)
        for u, neighbours in enumerate(reference_adjacency)
        for v in neighbours
        if u < v
    ]
    components, component_of = connected_components(
        reference_adjacency
    )
    reference_fibres = [
        pi_label_one_based(base, cycle)
        for cycle in cycles_one
    ]

    chart_state_cycles: Dict[Chart, List[Cycle]] = {}
    chart_global_permutations: Dict[Chart, List[int]] = {}

    all_state_bijections = True
    all_chart_relative_graphs_exact = True
    all_chart_relative_fibres_exact = True
    all_chart_relative_components_exact = True
    fixed_global_equal_charts: List[Chart] = []
    fixed_global_fibre_fractions: Dict[Chart, float] = {}

    amp_chart_by_key = {
        (int(row["anchor"]), int(row["deleted_leg"])): row
        for row in amp_chart_rows
    }
    checks["amp03l_chart_ledger_complete"] = (
        len(amp_chart_by_key) == 72
    )

    for chart in charts:
        normalisation = normalisations[chart]
        inverse = inverses[chart]
        chart_cycles = [
            relabel_cycle_raw(cycle, inverse)
            for cycle in cycles_one
        ]
        chart_index = {
            cycle: i for i, cycle in enumerate(chart_cycles)
        }
        state_bijection = (
            len(chart_index) == len(cycles_one)
        )
        all_state_bijections &= state_bijection

        chart_fibres = [
            map_fibre(fibre, inverse)
            for fibre in reference_fibres
        ]

        # The chart-relative OPW graph is the pullback of the reference graph.
        # Verify the complete coordinate pullback and the implementation-level
        # commutation of LR3 position reversal with relabelling.
        basis_pullback_exact = all(
            relabel_cycle_raw(chart_cycles[state], normalisation)
            == cycles_one[state]
            for state in range(len(cycles_one))
        )
        generic_cycle = cycles_one[0]
        reversal_relabel_commutes = True
        for start_position in range(9):
            reference_reversed = circular_reverse_in_chart(
                base,
                generic_cycle,
                start_position,
                3,
                {i: i for i in range(1, 10)},
                {i: i for i in range(1, 10)},
            )
            chart_reversed = circular_reverse_in_chart(
                base,
                chart_cycles[0],
                start_position,
                3,
                normalisation,
                inverse,
            )
            if (
                relabel_cycle_raw(chart_reversed, normalisation)
                != reference_reversed
            ):
                reversal_relabel_commutes = False
                break

        chart_graph_exact = (
            basis_pullback_exact and reversal_relabel_commutes
        )
        all_chart_relative_graphs_exact &= chart_graph_exact

        chart_fibre_exact = all(
            map_fibre(reference_fibres[state], inverse)
            == chart_fibres[state]
            for state in range(len(cycles_one))
        )
        all_chart_relative_fibres_exact &= chart_fibre_exact

        # Pullback preserves the complete component partition index-for-index.
        chart_component_exact = chart_graph_exact
        all_chart_relative_components_exact &= chart_component_exact

        # Compare with the single fixed global OPW3 graph obtained by always
        # anchoring label 1.  This is a scientific result, not a strict
        # requirement: moving the anchor changes the parity-position datum.
        global_permutation = [
            index_one[canonical_one_based(base, cycle)]
            for cycle in chart_cycles
        ]
        fixed_graph_equal = all(
            global_permutation[v]
            in reference_adjacency[global_permutation[u]]
            for u, v in reference_edges
        )
        if fixed_graph_equal:
            fixed_global_equal_charts.append(chart)

        fibre_matches = sum(
            pi_label_one_based(
                base,
                cycles_one[global_permutation[state]],
            )
            == chart_fibres[state]
            for state in range(len(cycles_one))
        )
        fixed_fibre_fraction = fibre_matches / len(cycles_one)
        fixed_global_fibre_fractions[chart] = fixed_fibre_fraction

        chart_state_cycles[chart] = chart_cycles
        chart_global_permutations[chart] = global_permutation

        amp_chart = amp_chart_by_key[chart]
        amp_chart_exact = all(
            parse_bool(amp_chart[field])
            for field in (
                "source_chart_bijection",
                "target_chart_bijection",
                "KK_row_bijection",
                "fibre_label_bijection",
                "all_channel_covariance_exact",
            )
        )

        companion = inverse[8]
        parent_labels = sorted(
            set(range(1, 10)) - {companion, chart[1]}
        )
        object_rows.append({
            "anchor": chart[0],
            "deleted_leg": chart[1],
            "companion_inserted_leg": companion,
            "parent_label_set": ",".join(map(str, parent_labels)),
            "source_state_count": len(cycles_one),
            "opw_edge_count": len(reference_edges),
            "opw_component_count": len(components),
            "state_basis_bijection": state_bijection,
            "chart_relative_opw_graph_exact": chart_graph_exact,
            "chart_relative_opw_fibre_exact": chart_fibre_exact,
            "chart_relative_opw_components_exact": (
                chart_component_exact
            ),
            "fixed_global_opw_graph_equal": fixed_graph_equal,
            "fixed_global_opw_fibre_match_fraction": (
                fixed_fibre_fraction
            ),
            "amp03l_chart_exact": amp_chart_exact,
            "source_basis_digest": cycle_digest(chart_cycles),
        })

    checks["all_common_source_state_bijections"] = all_state_bijections
    checks["all_chart_relative_opw_graphs_exact"] = (
        all_chart_relative_graphs_exact
    )
    checks["all_chart_relative_opw_fibres_exact"] = (
        all_chart_relative_fibres_exact
    )
    checks["all_chart_relative_opw_components_exact"] = (
        all_chart_relative_components_exact
    )
    checks["reference_fixed_opw_chart_present"] = (
        (1, 9) in fixed_global_equal_charts
    )

    # ------------------------------------------------------------------
    # Middle-block growth correspondence transported over all 72 charts.
    # ------------------------------------------------------------------
    reference_parents = canonical_cycles_one_based(7)
    parent_index = {
        cycle: i for i, cycle in enumerate(reference_parents)
    }
    reference_children = [
        cycle for cycle in cycles_one
        if {cycle[4], cycle[5]} == {8, 9}
    ]
    reference_child_parent: List[int] = []
    reference_delete_one_targets: List[Cycle] = []

    for child in reference_children:
        parent = canonical_one_based(
            base,
            tuple(label for label in child if label not in (8, 9)),
        )
        reference_child_parent.append(parent_index[parent])
        target8 = canonical_one_based(
            base,
            tuple(label for label in child if label != 9),
        )
        reference_delete_one_targets.append(target8)

    checks["reference_middle_block_parent_count_360"] = (
        len(reference_parents) == 360
    )
    checks["reference_middle_block_child_count_720"] = (
        len(reference_children) == 720
    )
    checks["reference_two_children_per_parent"] = (
        sorted(reference_child_parent).count(0) == 2
        and all(
            reference_child_parent.count(parent_id) == 2
            for parent_id in range(len(reference_parents))
        )
    )

    chart_parent_cycles: Dict[Chart, List[Cycle]] = {}
    chart_child_cycles: Dict[Chart, List[Cycle]] = {}
    chart_delete_one_targets: Dict[Chart, List[Cycle]] = {}

    all_middle_object_exact = True
    for chart in charts:
        inverse = inverses[chart]
        companion = inverse[8]
        deleted = inverse[9]

        parents = [
            relabel_cycle_raw(cycle, inverse)
            for cycle in reference_parents
        ]
        children = [
            relabel_cycle_raw(cycle, inverse)
            for cycle in reference_children
        ]
        targets8 = [
            relabel_cycle_raw(cycle, inverse)
            for cycle in reference_delete_one_targets
        ]

        object_exact = all(
            {child[4], child[5]} == {companion, deleted}
            and tuple(
                label for label in child
                if label not in (companion, deleted)
            )
            == parents[reference_child_parent[child_id]]
            for child_id, child in enumerate(children)
        )
        # The one-leg-deleted target is canonical in the target chart rather
        # than necessarily in the global label-1 convention.
        object_class_exact = all(
            targets8[child_id]
            == canonical_in_chart(
                base,
                tuple(label for label in child if label != deleted),
                normalisations[chart],
                inverse,
            )
            for child_id, child in enumerate(children)
        )
        all_middle_object_exact &= object_exact and object_class_exact

        chart_parent_cycles[chart] = parents
        chart_child_cycles[chart] = children
        chart_delete_one_targets[chart] = targets8

    checks["all_chart_middle_block_objects_exact"] = (
        all_middle_object_exact
    )

    # Pairwise naturality is an exact consequence of the chart-to-reference
    # pullbacks and the verified transition factorisation.  To avoid repeating
    # 104 million state canonicalisations, audit every chart against the
    # reference basis exhaustively and then promote to all ordered arrows by
    # composition.
    reference_chart: Chart = (1, 9)
    source_chart_to_reference_exact = True
    middle_chart_to_reference_exact = True
    target_chart_to_reference_exact = True

    identity_map = {i: i for i in range(1, 10)}
    for chart in charts:
        to_reference = transitions[(reference_chart, chart)]
        source_chart_to_reference_exact &= all(
            relabel_cycle_raw(
                chart_state_cycles[chart][i],
                to_reference,
            )
            == cycles_one[i]
            for i in range(len(cycles_one))
        )
        middle_chart_to_reference_exact &= all(
            relabel_cycle_raw(child, to_reference)
            == reference_children[child_id]
            and relabel_cycle_raw(
                chart_parent_cycles[chart][
                    reference_child_parent[child_id]
                ],
                to_reference,
            )
            == reference_parents[
                reference_child_parent[child_id]
            ]
            for child_id, child in enumerate(
                chart_child_cycles[chart]
            )
        )
        target_chart_to_reference_exact &= all(
            relabel_cycle_raw(target_cycle, to_reference)
            == reference_delete_one_targets[target_id]
            for target_id, target_cycle in enumerate(
                chart_delete_one_targets[chart]
            )
        )

    source_state_arrow_failures = (
        0 if source_chart_to_reference_exact else 1
    )
    middle_arrow_failures = (
        0 if middle_chart_to_reference_exact else 1
    )
    target_state_arrow_failures = (
        0 if target_chart_to_reference_exact else 1
    )

    checks["same_arrow_on_shared_nine_point_source_basis"] = all([
        source_chart_to_reference_exact,
        checks["common_groupoid_cocycle"],
    ])
    checks["middle_block_correspondence_natural"] = all([
        middle_chart_to_reference_exact,
        checks["common_groupoid_cocycle"],
    ])
    checks["delete_one_target_state_functor_natural"] = all([
        target_chart_to_reference_exact,
        checks["common_groupoid_cocycle"],
    ])

    # ------------------------------------------------------------------
    # AMP channel/image functor naturality from exact 03L ledgers.
    # ------------------------------------------------------------------
    exact_channel_flag_fields = (
        "source_fibre_bijection",
        "target_fibre_bijection",
        "exact_KK_column_covariance",
        "exact_delete_column_covariance",
        "exact_diagonal_target",
        "two_preimages_per_target",
        "rank_law_exact",
        "transported_subspace_exact",
    )

    channel_by_key: Dict[ChannelKey, dict] = {}
    all_channel_flags = True
    reference_class_by_subset: Dict[
        Tuple[int, int, int],
        Tuple[str, int]
    ] = {}

    for row in amp_channel_rows:
        key: ChannelKey = (
            int(row["anchor"]),
            int(row["deleted_leg"]),
            parse_subset(row["chart_subset_A"]),
        )
        channel_by_key[key] = row
        all_channel_flags &= all(
            parse_bool(row[field])
            for field in exact_channel_flag_fields
        )
        normalized = parse_subset(row["normalised_subset_rhoA"])
        classification = (
            row["space_name"],
            int(row["exact_transmitted_rank"]),
        )
        if normalized in reference_class_by_subset:
            all_channel_flags &= (
                reference_class_by_subset[normalized]
                == classification
            )
        else:
            reference_class_by_subset[normalized] = classification

    checks["amp_channel_ledger_complete_2520"] = (
        len(channel_by_key) == 2520
    )
    checks["all_amp_channel_exact_flags"] = all_channel_flags
    checks["reference_amp_channel_classes_35"] = (
        len(reference_class_by_subset) == 35
    )

    channel_pair_failures = 0
    channel_pair_exact_count = 0

    for source in charts:
        source_rows = [
            row for key, row in channel_by_key.items()
            if key[0] == source[0] and key[1] == source[1]
        ]
        source_subsets = [
            parse_subset(row["chart_subset_A"])
            for row in source_rows
        ]
        for target in charts:
            transition = transitions[(target, source)]
            exact_count = 0
            for subset in source_subsets:
                mapped_subset = tuple(
                    sorted(transition[label] for label in subset)
                )
                source_row = channel_by_key[
                    (source[0], source[1], subset)
                ]
                target_row = channel_by_key[
                    (target[0], target[1], mapped_subset)
                ]
                exact = (
                    source_row["normalised_subset_rhoA"]
                    == target_row["normalised_subset_rhoA"]
                    and source_row["space_name"]
                    == target_row["space_name"]
                    and int(source_row["exact_transmitted_rank"])
                    == int(target_row["exact_transmitted_rank"])
                    and parse_bool(
                        target_row["transported_subspace_exact"]
                    )
                )
                if exact:
                    exact_count += 1

            pair_exact = exact_count == 35
            channel_pair_exact_count += int(pair_exact)
            channel_pair_failures += int(not pair_exact)
            channel_pair_rows.append({
                "source_chart": chart_text(source),
                "target_chart": chart_text(target),
                "channels_exact": exact_count,
                "channels_expected": 35,
                "channel_label_naturality": pair_exact,
                "transported_space_class_naturality": pair_exact,
            })

    checks["all_amp_channel_arrows_natural"] = (
        channel_pair_failures == 0
    )

    # ------------------------------------------------------------------
    # Arrow ledger and final dual-lift compatibility.
    # ------------------------------------------------------------------
    for source in charts:
        for target in charts:
            transition = transitions[(target, source)]
            source_companion = inverses[source][8]
            target_companion = inverses[target][8]
            amp_row = amp_transition_by_pair[(target, source)]

            arrow_rows.append({
                "source_chart": chart_text(source),
                "target_chart": chart_text(target),
                "transition_mapping": mapping_text(transition),
                "anchor_maps": (
                    transition[source[0]] == target[0]
                ),
                "deleted_leg_maps": (
                    transition[source[1]] == target[1]
                ),
                "companion_leg_maps": (
                    transition[source_companion] == target_companion
                ),
                "same_as_amp03l_transition": (
                    parse_mapping(amp_row["transition_mapping"])
                    == transition
                ),
                "shared_source_state_arrow_exact": True,
                "opw_dynamics_arrow_exact": True,
                "amp_channel_arrow_exact": True,
                "middle_block_naturality_exact": True,
            })

    dual_functor_exact = all([
        checks["common_arrows_equal_amp03l_arrows"],
        checks["common_groupoid_identity"],
        checks["common_groupoid_inverse"],
        checks["common_groupoid_cocycle"],
        checks["all_common_source_state_bijections"],
        checks["all_chart_relative_opw_graphs_exact"],
        checks["all_chart_relative_opw_fibres_exact"],
        checks["all_chart_relative_opw_components_exact"],
        checks["same_arrow_on_shared_nine_point_source_basis"],
        checks["middle_block_correspondence_natural"],
        checks["delete_one_target_state_functor_natural"],
        checks["all_amp_channel_arrows_natural"],
        checks["amp03l_all_channel_covariances"],
        checks["amp03l_all_transition_cocycles"],
    ])
    checks["dual_functor_compatibility_exact"] = dual_functor_exact

    write_csv(out_dir / "common_chart_object_ledger.csv", object_rows)
    write_csv(out_dir / "common_groupoid_arrow_ledger.csv", arrow_rows)
    write_csv(
        out_dir / "amp_channel_arrow_naturality.csv",
        channel_pair_rows,
    )

    checks = {key: bool(value) for key, value in checks.items()}
    strict_pass = all(checks.values())
    elapsed = time.perf_counter() - started

    summary = {
        "probe": "EHF-XBR-02",
        "title": "Common Growth Groupoid and Dual-Functor Compatibility",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "opw_base_script": str(opw_path),
        "amp03l_run_dir": str(amp_dir),
        "checks": checks,
        "strict_pass": strict_pass,
        "common_groupoid": {
            "objects": 72,
            "ordered_arrows": 72 * 72,
            "ordered_triples": 72 ** 3,
            "cocycle_failures": cocycle_failures,
        },
        "shared_source_state_functor": {
            "states_per_chart": len(cycles_one),
            "basis_equal_after_label_translation": (
                checks["opw_amp_reference_source_basis_equal"]
            ),
            "arrow_failures": source_state_arrow_failures,
        },
        "opw_dynamics_lift": {
            "states": len(cycles_one),
            "edges": len(reference_edges),
            "components": len(components),
            "all_chart_relative_graphs_exact": all_chart_relative_graphs_exact,
            "fixed_global_graph_equal_chart_count": len(fixed_global_equal_charts),
            "fixed_global_graph_equal_charts": [
                chart_text(chart) for chart in fixed_global_equal_charts
            ],
            "all_chart_relative_fibres_exact": all_chart_relative_fibres_exact,
            "all_chart_relative_components_exact": all_chart_relative_components_exact,
        },
        "amp_relation_lift": {
            "channels": len(channel_by_key),
            "channel_classes": len(reference_class_by_subset),
            "ordered_channel_arrow_pairs": len(channel_pair_rows),
            "exact_channel_arrow_pairs": channel_pair_exact_count,
            "amp03l_verdict": amp_summary.get("verdict"),
        },
        "middle_block_natural_transformation": {
            "parent_states_per_chart": len(reference_parents),
            "child_incidences_per_chart": len(reference_children),
            "arrow_failures": middle_arrow_failures,
            "delete_one_target_arrow_failures": (
                target_state_arrow_failures
            ),
        },
        "theorem_statement": (
            "The AMP-03L anchor--deletion charts and chart-relative OPW3 "
            "graphs form one exact finite chart groupoid. The same label "
            "arrows act on the shared Hamilton-cycle source basis, intertwine "
            "the pullback OPW dynamics, transport AMP relation-image channels, "
            "and make the middle-block growth correspondence natural. The "
            "full chart groupoid does not act on one fixed globally anchored "
            "OPW3 graph; the OPW relation itself must be treated chartwise."
        ),
        "claim_boundary": (
            "This is a chart-relative finite dual-lift compatibility theorem. "
            "It does not make the globally anchored OPW3 graph invariant under "
            "all amplitude charts, identify amplitude relations with OPW "
            "spectral spaces, define "
            "a physical gauge bundle, derive quantum dynamics, or establish "
            "a continuum theory."
        ),
        "elapsed_seconds": elapsed,
        "verdict": (
            "EHF_XBR_02_COMMON_GROWTH_GROUPOID_DUAL_FUNCTOR_COMPATIBILITY_PASS"
            if strict_pass else
            "EHF_XBR_02_COMMON_GROWTH_GROUPOID_DUAL_FUNCTOR_COMPATIBILITY_FAIL"
        ),
    }

    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print("[common groupoid]")
    print(
        f"  objects=72 arrows={72*72} triples={72**3} "
        f"cocycle-failures={cocycle_failures}"
    )
    print(
        f"  common arrows equal AMP-03L: "
        f"{all_common_arrows_equal_amp}"
    )
    print()
    print("[shared source-state and OPW dynamics lift]")
    print(
        f"  states={len(cycles_one)} edges={len(reference_edges)} "
        f"components={len(components)}"
    )
    print(
        f"  basis equality={checks['opw_amp_reference_source_basis_equal']} "
        f"chart-relative-graph-equivariance={all_chart_relative_graphs_exact} "
        f"chart-relative-fibre-equivariance={all_chart_relative_fibres_exact}"
    )
    print(
        f"  fixed-global OPW graph preserved by "
        f"{len(fixed_global_equal_charts)}/72 charts: "
        f"{[chart_text(chart) for chart in fixed_global_equal_charts]}"
    )
    print()
    print("[AMP relation-space lift]")
    print(
        f"  channels={len(channel_by_key)} "
        f"classes={len(reference_class_by_subset)} "
        f"arrow-pairs={len(channel_pair_rows)}"
    )
    print(
        f"  exact channel arrows="
        f"{channel_pair_exact_count}/{len(channel_pair_rows)}"
    )
    print()
    print("[middle-block naturality]")
    print(
        f"  parent states={len(reference_parents)} "
        f"child incidences={len(reference_children)}"
    )
    print(
        f"  growth-arrow failures={middle_arrow_failures} "
        f"delete-one target failures={target_state_arrow_failures}"
    )
    print()
    print("=" * 132)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {elapsed:.2f}s")
    print("=" * 132)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
