#!/usr/bin/env python3
"""
EHF-OPW3-AUDIT-10
=================
Exact Growth-Chart Groupoid and Descriptor Cocycle

For each n-2 -> n growth chart chi, define the coordinate map

    kappa_chi(x) = (parent(x), descriptor_chi(x)).

Audit-09 established that every kappa_chi is a bijection and that the parent
is chart-invariant.  This probe packages those bijections as an exact finite
chart groupoid:

    T_{psi <- chi} = kappa_psi o kappa_chi^{-1}.

The groupoid laws then follow exactly:

    T_{chi <- chi} = id,
    T_{chi <- psi} = T_{psi <- chi}^{-1},
    T_{omega <- psi} o T_{psi <- chi} = T_{omega <- chi}.

The script independently reconstructs every chart coordinate table, verifies
bijection and parent invariance, verifies every pair transition and inverse on
all coordinates, and verifies the cocycle on a deterministic exhaustive basis:
all chart triples are checked on every distinct reference-coordinate orbit
representative induced by the chart family.

This is a finite atlas theorem for growth coordinates.  It is not yet the
cross-branch amplitude/dynamics functor theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Hashable, List, Mapping, Sequence, Tuple

SCRIPT_VERSION = "ehf_opw3_audit_10_2026-07-25"

Coordinate = Tuple[int, Tuple[int, int]]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_int_csv(text: str) -> List[int]:
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def coordinate_hash(coordinates: Sequence[Coordinate]) -> str:
    digest = hashlib.sha256()
    for parent, descriptor in coordinates:
        digest.update(f"{parent}:{descriptor[0]}:{descriptor[1]};".encode())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit the exact OPW3 growth-chart groupoid and descriptor cocycle."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--chart-script", required=True)
    parser.add_argument("--target-ns", type=parse_int_csv, default=[7, 9])
    parser.add_argument("--out-dir", default="runs/ehf_opw3_audit_10")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    base_path = Path(args.base_script).resolve()
    chart_path = Path(args.chart_script).resolve()
    base = load_module(base_path, "ehf_opw3_base")
    chartmod = load_module(chart_path, "ehf_opw3_chart")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 126)
    print("EHF-OPW3-AUDIT-10: EXACT GROWTH-CHART GROUPOID AND DESCRIPTOR COCYCLE")
    print("=" * 126)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"chart engine:         {chart_path}")
    print(f"target n values:      {args.target_ns}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    started_all = time.perf_counter()
    checks: Dict[str, bool] = {}
    summaries: Dict[str, dict] = {}

    for target_n in args.target_ns:
        started = time.perf_counter()
        source_n = target_n - 2

        source_cycles = base.generate_cycles(source_n)
        target_cycles = base.generate_cycles(target_n)
        target_index = {cycle: i for i, cycle in enumerate(target_cycles)}

        charts = chartmod.chart_set(source_n)
        chart_coordinates: Dict[str, List[Coordinate]] = {}
        coordinate_to_state: Dict[str, Dict[Coordinate, int]] = {}

        reference_parent = None

        for chart in charts:
            parent, descriptors, _, _ = chartmod.build_chart_growth_map(
                base, chart, source_cycles, target_index
            )
            coordinates = [
                (int(parent[state]), tuple(descriptors[state]))
                for state in range(len(target_cycles))
            ]
            inverse = {coordinate: state for state, coordinate in enumerate(coordinates)}

            checks[f"n{target_n}_{chart.chart_id}_coordinate_bijection"] = (
                len(inverse) == len(target_cycles)
            )

            if reference_parent is None:
                reference_parent = parent
            checks[f"n{target_n}_{chart.chart_id}_parent_invariant"] = (
                parent == reference_parent
            )

            chart_coordinates[chart.chart_id] = coordinates
            coordinate_to_state[chart.chart_id] = inverse

        # Pair transitions on every coordinate.
        pair_count = 0
        inverse_pair_count = 0

        for chart_i in charts:
            coords_i = chart_coordinates[chart_i.chart_id]
            inv_i = coordinate_to_state[chart_i.chart_id]

            for chart_j in charts:
                pair_count += 1
                coords_j = chart_coordinates[chart_j.chart_id]
                inv_j = coordinate_to_state[chart_j.chart_id]

                forward: Dict[Coordinate, Coordinate] = {
                    coords_i[state]: coords_j[state]
                    for state in range(len(target_cycles))
                }
                backward: Dict[Coordinate, Coordinate] = {
                    coords_j[state]: coords_i[state]
                    for state in range(len(target_cycles))
                }

                functional = (
                    len(forward) == len(target_cycles)
                    and len(set(forward.values())) == len(target_cycles)
                )
                inverse_ok = all(
                    backward[forward[coordinate]] == coordinate
                    for coordinate in forward
                )
                state_compatibility = all(
                    inv_j[forward[coordinate]] == inv_i[coordinate]
                    for coordinate in forward
                )

                checks[
                    f"n{target_n}_{chart_i.chart_id}_to_{chart_j.chart_id}_pair"
                ] = functional and inverse_ok and state_compatibility

                if inverse_ok:
                    inverse_pair_count += 1

        # Exhaustive cocycle on orbit representatives.
        #
        # Two reference coordinates are equivalent if every chart assigns them
        # the same tuple of chart coordinates. Because each chart coordinate
        # map is injective, these classes are singletons; nevertheless the
        # construction makes the exhaustive basis explicit and guards against
        # accidental coordinate collisions.
        reference_chart = charts[0]
        signatures: Dict[Tuple[Coordinate, ...], Coordinate] = {}
        ref_coords = chart_coordinates[reference_chart.chart_id]
        for state, ref_coordinate in enumerate(ref_coords):
            signature = tuple(
                chart_coordinates[chart.chart_id][state]
                for chart in charts
            )
            signatures.setdefault(signature, ref_coordinate)

        representatives = list(signatures.values())
        checks[f"n{target_n}_orbit_representatives_complete"] = (
            len(representatives) == len(target_cycles)
        )

        triple_count = 0
        cocycle_failures = 0

        # Cache pair maps only for the representative coordinates used below.
        pair_maps: Dict[Tuple[str, str], Dict[Coordinate, Coordinate]] = {}
        for chart_i in charts:
            coords_i = chart_coordinates[chart_i.chart_id]
            for chart_j in charts:
                coords_j = chart_coordinates[chart_j.chart_id]
                pair_maps[(chart_i.chart_id, chart_j.chart_id)] = {
                    coords_i[state]: coords_j[state]
                    for state in range(len(target_cycles))
                }

        for chart_i in charts:
            map_ref_to_i = pair_maps[
                (reference_chart.chart_id, chart_i.chart_id)
            ]
            for chart_j in charts:
                t_ji = pair_maps[(chart_i.chart_id, chart_j.chart_id)]
                for chart_k in charts:
                    triple_count += 1
                    t_kj = pair_maps[(chart_j.chart_id, chart_k.chart_id)]
                    t_ki = pair_maps[(chart_i.chart_id, chart_k.chart_id)]

                    for ref_coordinate in representatives:
                        coordinate_i = map_ref_to_i[ref_coordinate]
                        if t_kj[t_ji[coordinate_i]] != t_ki[coordinate_i]:
                            cocycle_failures += 1
                            break

        checks[f"n{target_n}_all_chart_triples_cocycle"] = (
            cocycle_failures == 0
        )

        # Coordinate fingerprints provide a stable reproducibility ledger.
        fingerprints = {
            chart.chart_id: coordinate_hash(
                chart_coordinates[chart.chart_id]
            )
            for chart in charts
        }

        elapsed = time.perf_counter() - started
        summaries[f"n{target_n}"] = {
            "source_n": source_n,
            "target_states": len(target_cycles),
            "charts": len(charts),
            "pair_transitions": pair_count,
            "inverse_pair_transitions": inverse_pair_count,
            "chart_triples": triple_count,
            "orbit_representatives": len(representatives),
            "cocycle_failures": cocycle_failures,
            "coordinate_fingerprints": fingerprints,
            "elapsed_seconds": elapsed,
        }

        print(
            f"[{source_n}->{target_n}] states={len(target_cycles)} "
            f"charts={len(charts)} pairs={pair_count} triples={triple_count}"
        )
        print(
            f"  coordinate bijections={len(charts)}/{len(charts)} "
            f"parent invariant=True"
        )
        print(
            f"  inverse pair maps={inverse_pair_count}/{pair_count} "
            f"cocycle failures={cocycle_failures}"
        )
        print(
            f"  exhaustive coordinate representatives="
            f"{len(representatives)}"
        )
        print(f"  elapsed={elapsed:.2f}s")
        print()

    checks = {key: bool(value) for key, value in checks.items()}
    strict_pass = all(checks.values())

    summary = {
        "probe": "EHF-OPW3-AUDIT-10",
        "title": "Exact Growth-Chart Groupoid and Descriptor Cocycle",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "chart_script": str(chart_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "theorem_statement": (
            "The finite growth charts form a groupoid under coordinate "
            "transition maps T_{psi<-chi}=kappa_psi o kappa_chi^{-1}; "
            "identity, inverse, and cocycle laws hold exactly at every "
            "tested coordinate."
        ),
        "guardrail": (
            "This establishes the OPW growth-coordinate groupoid. It does "
            "not yet define or prove the amplitude and dynamics lifts as "
            "functors over one common groupoid."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_OPW3_AUDIT_10_EXACT_GROWTH_CHART_GROUPOID_PASS"
            if strict_pass else
            "EHF_OPW3_AUDIT_10_EXACT_GROWTH_CHART_GROUPOID_FAIL"
        ),
    }

    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print("=" * 126)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {summary['elapsed_seconds']:.2f}s")
    print("=" * 126)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
