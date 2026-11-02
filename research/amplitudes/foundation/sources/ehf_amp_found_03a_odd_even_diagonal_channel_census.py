#!/usr/bin/env python3
"""
EHF-AMP-FOUND-03A: Odd-to-Even Diagonal Channel Census at 9 -> 8
================================================================

Purpose
-------
Determine the fixed-anchor structure of reflection-aware delete-9
factorisation from local n=9 Parke--Taylor relation spaces into the 35 local
n=8 parity-position fibres.

At n=9, the canonical chart with anchor 1 admits anchor-adjacent label 9 only
in the 35 fibres

    E = {1,9} union A,
    O = {2,...,8} \\ A,

where A is a 3-subset of {2,...,8}. Deleting 9 preserves A and lands in the
single n=8 fibre

    E = {1} union A,
    O = {2,...,8} \\ A.

The probe tests whether this combinatorial diagonal map remains diagonal on
local relation spaces, and measures the transmitted rank in every channel.

The relation bases are the same independently validated numerical
Parke--Taylor nullspaces used by EHF-AMP-FOUND-02A. The residue incidence
operators and fibre mapping are exact combinatorial objects.

Primary questions
-----------------
1. Are there exactly 35 active source fibres and 35 distinct target fibres?
2. Does every active source fibre reach exactly its A-labelled target fibre?
3. Is each residue image contained in that target's 15-dimensional local
   relation space?
4. What is the channel rank r_A?
5. Do the disjoint target supports give total rank sum_A r_A = 363?
6. Are exactly 13 of the 35 target local spaces recovered completely?
7. Which elementary subset statistics predict the nonuniform rank profile?

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_03a_odd_even_diagonal_channel_census.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --base-run-dir runs/ehf_amp_found_01_amp18_20 \
  --out-dir runs/ehf_amp_found_03a \
  --seed 11 \
  --strict

Structural smoke test, requiring no relation bases:

python3 scripts/ehf_amp_found_03a_odd_even_diagonal_channel_census.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --out-dir runs/ehf_amp_found_03a_structure_smoke \
  --structure-only
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
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import numpy as np

Cycle = Tuple[int, ...]
FibreKey = Tuple[Tuple[int, ...], Tuple[int, ...]]
Subset = Tuple[int, ...]


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
                fields.append(key)
                seen.add(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def json_safe(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


def fmt(value: float) -> str:
    return f"{float(value):.17g}"


def subset_text(subset: Sequence[int]) -> str:
    return ",".join(map(str, subset))


def key_from_subset_9(subset: Subset) -> FibreKey:
    universe = set(range(2, 9))
    return (
        tuple(sorted((1, 9) + tuple(subset))),
        tuple(sorted(universe - set(subset))),
    )


def key_from_subset_8(subset: Subset) -> FibreKey:
    universe = set(range(2, 9))
    return (
        tuple(sorted((1,) + tuple(subset))),
        tuple(sorted(universe - set(subset))),
    )


def source_subset_from_key(key: FibreKey) -> Subset:
    return tuple(value for value in key[0] if value not in (1, 9))


def subset_features(subset: Subset) -> Dict[str, object]:
    universe = tuple(range(2, 9))
    subset_set = set(subset)
    complement = tuple(value for value in universe if value not in subset_set)
    word = "".join("1" if value in subset_set else "0" for value in universe)
    inversions = sum(left > right for left in subset for right in complement)
    transitions = sum(word[index] != word[index + 1] for index in range(len(word) - 1))
    one_runs = sum(
        bit == "1" and (index == 0 or word[index - 1] == "0")
        for index, bit in enumerate(word)
    )
    gaps = (
        subset[0] - 2,
        subset[1] - subset[0] - 1,
        subset[2] - subset[1] - 1,
        8 - subset[2],
    )
    reflected = tuple(sorted(10 - value for value in subset))
    return {
        "subset_word": word,
        "subset_sum": sum(subset),
        "subset_span": subset[-1] - subset[0],
        "inversion_count": inversions,
        "word_transition_count": transitions,
        "one_run_count": one_runs,
        "gap_signature": "-".join(map(str, gaps)),
        "reflected_subset": subset_text(reflected),
        "predicted_source_fibre_size": 36 * (4 + inversions),
    }


def rankdata(values: Sequence[float]) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    order = np.argsort(values, kind="mergesort")
    result = np.empty(len(values), dtype=float)
    index = 0
    while index < len(values):
        end = index + 1
        while end < len(values) and values[order[end]] == values[order[index]]:
            end += 1
        average_rank = 0.5 * ((index + 1) + end)
        result[order[index:end]] = average_rank
        index = end
    return result


def pearson(left: Sequence[float], right: Sequence[float]) -> float:
    x = np.asarray(left, dtype=float)
    y = np.asarray(right, dtype=float)
    if len(x) < 2 or np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def spearman(left: Sequence[float], right: Sequence[float]) -> float:
    return pearson(rankdata(left), rankdata(right))


def seed_offset_for_n(n: int) -> int:
    return 7 if n % 2 == 0 else 1


def build_selected_bases(
    base,
    n: int,
    fibres: Mapping[FibreKey, Sequence[Cycle]],
    selected_keys: Sequence[FibreKey],
    cache_dir: Path,
    args: argparse.Namespace,
    basis_rows: List[Dict[str, object]],
) -> Dict[FibreKey, object]:
    selected = set(selected_keys)
    result: Dict[FibreKey, object] = {}
    items = list(fibres.items())
    offset = seed_offset_for_n(n)
    print(f"\nBuilding/loading n={n} bases: {len(selected)} selected fibres")
    started = time.time()
    completed = 0
    for fibre_index, (key, chamber) in enumerate(items):
        if key not in selected:
            continue
        t0 = time.time()
        basis = base.load_or_compute_relation_basis(
            chamber=chamber,
            n=n,
            fibre_index=fibre_index,
            cache_dir=cache_dir,
            train_seed=args.seed + offset,
            validation_seed=args.seed + offset + 100_000 + fibre_index,
            rows_multiplier=args.rows_multiplier,
            min_rows=args.min_rows,
            validation_rows=args.validation_rows,
            svd_relative_tolerance=args.svd_tolerance,
            force_rebuild=args.force_rebuild,
        )
        result[key] = basis
        completed += 1
        singular_gap = ""
        if 0 < basis.numerical_rank < len(basis.singular_values):
            kept = float(basis.singular_values[basis.numerical_rank - 1])
            discarded = float(basis.singular_values[basis.numerical_rank])
            if discarded > 0:
                singular_gap = fmt(math.log10(kept / discarded))
        basis_rows.append({
            "n": n,
            "fibre_index": fibre_index,
            "fibre_key": base.key_text(key),
            "fibre_size": len(chamber),
            "numerical_rank": basis.numerical_rank,
            "relation_dim": basis.relation_dim,
            "validation_max_relative_residual": fmt(
                basis.validation_max_relative_residual
            ),
            "singular_gap_decades": singular_gap,
            "from_cache": basis.from_cache,
            "elapsed_seconds": f"{time.time() - t0:.3f}",
        })
        if completed % 5 == 0 or completed == len(selected):
            print(
                f"  [{completed:02d}/{len(selected):02d}] "
                f"size={len(chamber):3d} r={basis.relation_dim:3d} "
                f"validation={basis.validation_max_relative_residual:.2e} "
                f"{'cache' if basis.from_cache else 'computed'}"
            )
    print(f"Completed selected n={n} bases in {(time.time() - started) / 60:.2f} minutes.")
    if set(result) != selected:
        missing = selected - set(result)
        raise RuntimeError(f"Missing selected n={n} fibres: {missing}")
    return result


def group_summary(
    channel_rows: Sequence[Mapping[str, object]],
    field: str,
) -> List[Dict[str, object]]:
    grouped: MutableMapping[str, List[Mapping[str, object]]] = defaultdict(list)
    for row in channel_rows:
        grouped[str(row[field])].append(row)
    output: List[Dict[str, object]] = []
    for value, rows in sorted(grouped.items(), key=lambda item: item[0]):
        ranks = [int(row["residue_rank"]) for row in rows]
        source_dims = [int(row["source_relation_dim"]) for row in rows]
        output.append({
            "group_field": field,
            "group_value": value,
            "channel_count": len(rows),
            "rank_min": min(ranks),
            "rank_max": max(ranks),
            "rank_mean": fmt(float(np.mean(ranks))),
            "distinct_ranks": ";".join(map(str, sorted(set(ranks)))),
            "source_relation_dim_min": min(source_dims),
            "source_relation_dim_max": max(source_dims),
            "complete_target_count": sum(bool(row["complete_target_recovery"]) for row in rows),
        })
    return output


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    helper_script = Path(args.helper_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_03a_base")
    helper = load_module(helper_script, "ehf_amp_found_03a_helper")

    if args.cache_dir:
        cache_dir = Path(args.cache_dir).resolve()
    elif args.base_run_dir:
        cache_dir = Path(args.base_run_dir).resolve() / "cache"
    else:
        cache_dir = out_dir / "cache"

    fibres8: Dict[FibreKey, List[Cycle]] = base.fibres(8)
    fibres9: Dict[FibreKey, List[Cycle]] = base.fibres(9)
    subsets = list(itertools.combinations(range(2, 9), 3))
    if args.max_channels > 0:
        subsets = subsets[: args.max_channels]

    source_keys = [key_from_subset_9(subset) for subset in subsets]
    target_keys = [key_from_subset_8(subset) for subset in subsets]

    print("=" * 118)
    print("EHF-AMP-FOUND-03A: ODD-TO-EVEN DIAGONAL CHANNEL CENSUS AT 9 -> 8")
    print("=" * 118)
    print(f"base script:                    {base_script}")
    print(f"reflection-aware helper:        {helper_script}")
    print(f"cache directory:                {cache_dir}")
    print(f"output directory:               {out_dir}")
    print(f"seed:                           {args.seed}")
    print(f"channels selected:              {len(subsets)}/35")
    print(f"structure only:                 {args.structure_only}")

    # ------------------------------------------------------------------
    # Exact combinatorial diagonal mapping.
    # ------------------------------------------------------------------
    structure_rows: List[Dict[str, object]] = []
    all_single_target = True
    all_expected_target = True
    all_active_count_144 = True
    all_row_preimage_two = True
    all_standard_minus_chart = True
    reached_targets = set()

    for channel_index, (subset, source_key, target_key) in enumerate(
        zip(subsets, source_keys, target_keys)
    ):
        source = fibres9[source_key]
        operator_map = helper.build_child_residue_operator_map(
            base, source, fibres8, 9
        )
        single_target = len(operator_map) == 1
        all_single_target &= single_target
        if not single_target:
            reached_key = None
            full = plus = minus = np.zeros((0, len(source)))
        else:
            reached_key, (full, plus, minus) = next(iter(operator_map.items()))
            reached_targets.add(reached_key)
        expected = reached_key == target_key
        all_expected_target &= expected

        active_columns = int(np.count_nonzero(np.any(full != 0, axis=0)))
        plus_columns = int(np.count_nonzero(np.any(plus != 0, axis=0)))
        minus_columns = int(np.count_nonzero(np.any(minus != 0, axis=0)))
        row_multiplicities = (
            np.count_nonzero(full, axis=1)
            if full.shape[0]
            else np.zeros(0, dtype=int)
        )
        row_preimage_two = (
            row_multiplicities.size == 72
            and np.all(row_multiplicities == 2)
        )
        standard_minus_chart = plus_columns == 0 and minus_columns == 144
        all_active_count_144 &= active_columns == 144
        all_row_preimage_two &= row_preimage_two
        all_standard_minus_chart &= standard_minus_chart

        features = subset_features(subset)
        structure_rows.append({
            "channel_index": channel_index,
            "A": subset_text(subset),
            **features,
            "source_key": base.key_text(source_key),
            "target_key_expected": base.key_text(target_key),
            "target_key_reached": "" if reached_key is None else base.key_text(reached_key),
            "single_target": single_target,
            "expected_target": expected,
            "source_fibre_size": len(source),
            "source_size_formula_exact": (
                len(source) == features["predicted_source_fibre_size"]
            ),
            "active_source_state_count": active_columns,
            "plus_chart_state_count": plus_columns,
            "minus_chart_state_count": minus_columns,
            "standard_chart_minus_only": standard_minus_chart,
            "target_row_preimage_min": (
                "" if row_multiplicities.size == 0 else int(np.min(row_multiplicities))
            ),
            "target_row_preimage_max": (
                "" if row_multiplicities.size == 0 else int(np.max(row_multiplicities))
            ),
            "every_target_state_has_two_preimages": row_preimage_two,
        })

    target_bijection = len(reached_targets) == len(subsets)
    full_structure = len(subsets) == 35
    structural_success = (
        all_single_target
        and all_expected_target
        and target_bijection
        and all_active_count_144
        and all_row_preimage_two
        and all_standard_minus_chart
    )

    print("\nExact combinatorial channel map")
    print(f"  active source channels:          {len(subsets)}")
    print(f"  one target per source:           {all_single_target}")
    print(f"  A-labelled target preserved:     {all_expected_target}")
    print(f"  distinct targets reached:        {len(reached_targets)}")
    print(f"  144 active states per source:    {all_active_count_144}")
    print(f"  two preimages per target state:  {all_row_preimage_two}")
    print(f"  standard chart is minus-only:    {all_standard_minus_chart}")

    write_csv(out_dir / "diagonal_structure_ledger.csv", structure_rows)

    if args.structure_only:
        summary = {
            "script": Path(__file__).name,
            "parameters": vars(args),
            "selected_channel_count": len(subsets),
            "full_35_channel_census": full_structure,
            "one_target_per_source": all_single_target,
            "A_label_preserved": all_expected_target,
            "target_bijection": target_bijection,
            "active_state_count_144": all_active_count_144,
            "two_preimages_per_target_state": all_row_preimage_two,
            "standard_chart_minus_only": all_standard_minus_chart,
            "structural_diagonal_certificate": structural_success,
            "elapsed_seconds": time.time() - started,
            "output_files": [
                "summary.json",
                "run.log",
                "diagonal_structure_ledger.csv",
            ],
        }
        with (out_dir / "summary.json").open("w") as handle:
            json.dump(json_safe(summary), handle, indent=2)
        print("\n" + "=" * 118)
        print("FINAL STRUCTURAL SUMMARY")
        print("=" * 118)
        print(f"Fixed-anchor diagonal structure:   {structural_success}")
        print(f"Full 35-channel census:            {full_structure}")
        print(f"summary:                           {out_dir / 'summary.json'}")
        print("=" * 118)
        return summary

    # ------------------------------------------------------------------
    # Relation bases.
    # ------------------------------------------------------------------
    basis_rows: List[Dict[str, object]] = []
    bases8 = build_selected_bases(
        base, 8, fibres8, target_keys, cache_dir, args, basis_rows
    )
    bases9 = build_selected_bases(
        base, 9, fibres9, source_keys, cache_dir, args, basis_rows
    )
    write_csv(out_dir / "relation_basis_summary.csv", basis_rows)

    # ------------------------------------------------------------------
    # Channelwise relation transmission.
    # ------------------------------------------------------------------
    channel_rows: List[Dict[str, object]] = []
    max_image_pt_residual = 0.0
    max_image_containment_residual = 0.0
    all_images_relational = True
    all_images_local = True
    all_intersection_matches_rank = True

    for channel_index, (subset, source_key, target_key) in enumerate(
        zip(subsets, source_keys, target_keys)
    ):
        source = fibres9[source_key]
        target = fibres8[target_key]
        operator_map = helper.build_child_residue_operator_map(
            base, source, fibres8, 9
        )
        reached_key, (full, plus, minus) = next(iter(operator_map.items()))
        if reached_key != target_key:
            raise RuntimeError("Diagonal structure changed between passes")

        source_basis_record = bases9[source_key]
        target_basis_record = bases8[target_key]
        source_basis = source_basis_record.basis
        target_basis = target_basis_record.basis

        image = full @ source_basis
        plus_image = plus @ source_basis
        minus_image = minus @ source_basis
        residue_rank, singular_values = helper.safe_rank(
            image, args.rank_tolerance, args.rank_absolute_tolerance
        )
        plus_rank, _ = helper.safe_rank(
            plus_image, args.rank_tolerance, args.rank_absolute_tolerance
        )
        minus_rank, _ = helper.safe_rank(
            minus_image, args.rank_tolerance, args.rank_absolute_tolerance
        )
        image_q = helper.orthonormal_span(
            image, args.rank_tolerance, args.rank_absolute_tolerance
        )
        intersection, principal_cosines = helper.intersection_basis(
            target_basis, image_q, args.containment_tolerance
        )
        inherited_rank = intersection.shape[1]
        image_containment = helper.max_subspace_residual(image, target_basis)
        target_residual = helper.max_subspace_residual(target_basis, image_q)
        pt_residual = helper.pt_residual(
            base,
            target,
            8,
            image,
            args.seed + 700_000 + channel_index,
            args.residue_validation_rows,
        )

        max_image_pt_residual = max(max_image_pt_residual, pt_residual)
        max_image_containment_residual = max(
            max_image_containment_residual, image_containment
        )
        image_relational = pt_residual < args.relation_verdict_tolerance
        image_local = image_containment < args.containment_tolerance
        intersection_matches = inherited_rank == residue_rank
        all_images_relational &= image_relational
        all_images_local &= image_local
        all_intersection_matches_rank &= intersection_matches

        source_dim = source_basis.shape[1]
        target_dim = target_basis.shape[1]
        capacity = min(source_dim, target_dim)
        residue_kernel_dim = source_dim - residue_rank
        complete = inherited_rank == target_dim

        if source_dim == 0:
            channel_class = "NO_SOURCE_RELATIONS"
        elif complete:
            channel_class = (
                "TARGET_COMPLETE_INJECTIVE"
                if residue_kernel_dim == 0
                else "TARGET_COMPLETE_WITH_SOURCE_KERNEL"
            )
        elif residue_rank == source_dim:
            channel_class = "SOURCE_LIMITED_INJECTIVE"
        elif residue_rank == capacity:
            channel_class = "CAPACITY_SATURATED_PARTIAL_TARGET"
        else:
            channel_class = "LOSSY_PARTIAL"

        features = subset_features(subset)
        smallest_kept = (
            ""
            if residue_rank == 0
            else fmt(float(singular_values[residue_rank - 1]))
        )
        first_discarded = (
            ""
            if residue_rank >= len(singular_values)
            else fmt(float(singular_values[residue_rank]))
        )

        channel_rows.append({
            "channel_index": channel_index,
            "A": subset_text(subset),
            **features,
            "source_key": base.key_text(source_key),
            "target_key": base.key_text(target_key),
            "source_fibre_size": len(source),
            "source_relation_dim": source_dim,
            "source_basis_validation_residual": fmt(
                source_basis_record.validation_max_relative_residual
            ),
            "target_fibre_size": len(target),
            "target_relation_dim": target_dim,
            "target_basis_validation_residual": fmt(
                target_basis_record.validation_max_relative_residual
            ),
            "residue_rank": residue_rank,
            "residue_kernel_dim": residue_kernel_dim,
            "rank_capacity_min_source_target": capacity,
            "rank_deficit_to_capacity": capacity - residue_rank,
            "inherited_target_local_rank": inherited_rank,
            "target_missing_dim": target_dim - inherited_rank,
            "complete_target_recovery": complete,
            "channel_class": channel_class,
            "plus_only_rank": plus_rank,
            "minus_only_rank": minus_rank,
            "image_pt_residual": fmt(pt_residual),
            "image_to_target_local_residual": fmt(image_containment),
            "target_local_to_image_residual": fmt(target_residual),
            "image_is_valid_relation": image_relational,
            "image_is_target_local": image_local,
            "intersection_rank_matches_residue_rank": intersection_matches,
            "principal_cosine_min": (
                ""
                if principal_cosines.size == 0
                else fmt(float(principal_cosines[-1]))
            ),
            "principal_cosine_max": (
                ""
                if principal_cosines.size == 0
                else fmt(float(principal_cosines[0]))
            ),
            "smallest_kept_residue_singular_value": smallest_kept,
            "first_discarded_residue_singular_value": first_discarded,
        })

    write_csv(out_dir / "diagonal_channel_census.csv", channel_rows)

    # ------------------------------------------------------------------
    # Rank distributions and elementary feature tests.
    # ------------------------------------------------------------------
    rank_counts = Counter(int(row["residue_rank"]) for row in channel_rows)
    class_counts = Counter(str(row["channel_class"]) for row in channel_rows)
    rank_distribution_rows = [
        {
            "residue_rank": rank,
            "channel_count": count,
            "complete_target_count": sum(
                bool(row["complete_target_recovery"])
                for row in channel_rows
                if int(row["residue_rank"]) == rank
            ),
        }
        for rank, count in sorted(rank_counts.items())
    ]
    write_csv(out_dir / "rank_distribution.csv", rank_distribution_rows)

    group_rows: List[Dict[str, object]] = []
    for field in (
        "source_fibre_size",
        "source_relation_dim",
        "inversion_count",
        "gap_signature",
        "one_run_count",
        "channel_class",
    ):
        group_rows.extend(group_summary(channel_rows, field))
    write_csv(out_dir / "feature_group_summary.csv", group_rows)

    numeric_features = (
        "source_fibre_size",
        "source_relation_dim",
        "inversion_count",
        "subset_sum",
        "subset_span",
        "word_transition_count",
        "one_run_count",
    )
    ranks = [float(row["residue_rank"]) for row in channel_rows]
    correlation_rows = []
    for field in numeric_features:
        values = [float(row[field]) for row in channel_rows]
        correlation_rows.append({
            "feature": field,
            "pearson_with_residue_rank": fmt(pearson(values, ranks)),
            "spearman_with_residue_rank": fmt(spearman(values, ranks)),
        })
    write_csv(out_dir / "feature_rank_correlations.csv", correlation_rows)

    # Johnson J(7,3) edge audit.
    row_by_subset = {
        tuple(map(int, str(row["A"]).split(","))): row
        for row in channel_rows
    }
    selected_set = set(row_by_subset)
    johnson_rows: List[Dict[str, object]] = []
    edge_differences: List[float] = []
    nonedge_differences: List[float] = []
    edge_status_agreement: List[bool] = []
    for left_index, left in enumerate(subsets):
        for right in subsets[left_index + 1 :]:
            left_rank = int(row_by_subset[left]["residue_rank"])
            right_rank = int(row_by_subset[right]["residue_rank"])
            is_edge = len(set(left) & set(right)) == 2
            difference = abs(left_rank - right_rank)
            if is_edge:
                edge_differences.append(difference)
                edge_status_agreement.append(
                    bool(row_by_subset[left]["complete_target_recovery"])
                    == bool(row_by_subset[right]["complete_target_recovery"])
                )
            else:
                nonedge_differences.append(difference)
            johnson_rows.append({
                "left_A": subset_text(left),
                "right_A": subset_text(right),
                "intersection_size": len(set(left) & set(right)),
                "is_J7_3_edge": is_edge,
                "left_rank": left_rank,
                "right_rank": right_rank,
                "absolute_rank_difference": difference,
                "complete_status_agrees": (
                    bool(row_by_subset[left]["complete_target_recovery"])
                    == bool(row_by_subset[right]["complete_target_recovery"])
                ),
            })
    write_csv(out_dir / "johnson_pair_rank_audit.csv", johnson_rows)

    # Label-order reflection A -> {10-a}.
    reflection_rows: List[Dict[str, object]] = []
    visited = set()
    for subset in subsets:
        reflected = tuple(sorted(10 - value for value in subset))
        if reflected not in selected_set:
            continue
        pair_id = tuple(sorted((subset, reflected)))
        if pair_id in visited:
            continue
        visited.add(pair_id)
        left = row_by_subset[subset]
        right = row_by_subset[reflected]
        reflection_rows.append({
            "left_A": subset_text(subset),
            "right_A": subset_text(reflected),
            "self_reflected": subset == reflected,
            "left_source_size": left["source_fibre_size"],
            "right_source_size": right["source_fibre_size"],
            "left_source_relation_dim": left["source_relation_dim"],
            "right_source_relation_dim": right["source_relation_dim"],
            "left_residue_rank": left["residue_rank"],
            "right_residue_rank": right["residue_rank"],
            "rank_equal": left["residue_rank"] == right["residue_rank"],
            "rank_sum": int(left["residue_rank"]) + int(right["residue_rank"]),
            "complete_status_equal": (
                bool(left["complete_target_recovery"])
                == bool(right["complete_target_recovery"])
            ),
        })
    write_csv(out_dir / "label_order_reflection_audit.csv", reflection_rows)

    # ------------------------------------------------------------------
    # Global summary.
    # ------------------------------------------------------------------
    global_rank = sum(int(row["residue_rank"]) for row in channel_rows)
    complete_targets = sum(
        bool(row["complete_target_recovery"]) for row in channel_rows
    )
    total_source_relations = sum(
        int(row["source_relation_dim"]) for row in channel_rows
    )
    total_source_kernel = sum(
        int(row["residue_kernel_dim"]) for row in channel_rows
    )
    total_target_local_dim = sum(
        int(row["target_relation_dim"]) for row in channel_rows
    )
    total_target_missing = sum(
        int(row["target_missing_dim"]) for row in channel_rows
    )
    expected_rank_ok = (
        not full_structure or global_rank == args.expected_global_rank
    )
    expected_complete_ok = (
        not full_structure or complete_targets == args.expected_complete_targets
    )
    basis_valid = all(
        float(row["validation_max_relative_residual"])
        < args.relation_verdict_tolerance
        for row in basis_rows
    )
    diagonal_relation_law = (
        structural_success
        and basis_valid
        and all_images_relational
        and all_images_local
        and all_intersection_matches_rank
    )

    if diagonal_relation_law and expected_rank_ok and expected_complete_ok:
        verdict = "EHF_AMP_FOUND_03A_FIXED_ANCHOR_DIAGONAL_CHANNEL_LAW_SUPPORTED"
    elif diagonal_relation_law:
        verdict = "EHF_AMP_FOUND_03A_DIAGONAL_STRUCTURE_SUPPORTED_RANK_PROFILE_REVISED"
    else:
        verdict = "EHF_AMP_FOUND_03A_DIAGONAL_CHANNEL_LAW_NOT_SUPPORTED"

    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "selected_channel_count": len(subsets),
        "full_35_channel_census": full_structure,
        "structural_certificate": {
            "one_target_per_source": all_single_target,
            "A_label_preserved": all_expected_target,
            "target_bijection": target_bijection,
            "active_state_count_144": all_active_count_144,
            "two_preimages_per_target_state": all_row_preimage_two,
            "standard_chart_minus_only": all_standard_minus_chart,
        },
        "relation_certificate": {
            "all_bases_freshly_validated": basis_valid,
            "all_residue_images_are_PT_relations": all_images_relational,
            "all_residue_images_are_target_local": all_images_local,
            "all_intersection_ranks_match_image_ranks": (
                all_intersection_matches_rank
            ),
            "max_residue_PT_residual": fmt(max_image_pt_residual),
            "max_target_local_containment_residual": fmt(
                max_image_containment_residual
            ),
        },
        "rank_census": {
            "global_direct_sum_rank": global_rank,
            "expected_global_rank": args.expected_global_rank,
            "expected_global_rank_match": expected_rank_ok,
            "complete_target_count": complete_targets,
            "expected_complete_target_count": args.expected_complete_targets,
            "expected_complete_target_count_match": expected_complete_ok,
            "rank_distribution": dict(sorted(rank_counts.items())),
            "channel_class_distribution": dict(sorted(class_counts.items())),
            "total_source_relation_dimension": total_source_relations,
            "total_source_residue_kernel_dimension": total_source_kernel,
            "total_target_local_dimension": total_target_local_dim,
            "total_target_missing_dimension": total_target_missing,
        },
        "johnson_audit": {
            "edge_count": len(edge_differences),
            "mean_absolute_rank_difference_on_edges": (
                fmt(float(np.mean(edge_differences)))
                if edge_differences else None
            ),
            "mean_absolute_rank_difference_on_nonedges": (
                fmt(float(np.mean(nonedge_differences)))
                if nonedge_differences else None
            ),
            "complete_status_agreement_rate_on_edges": (
                fmt(float(np.mean(edge_status_agreement)))
                if edge_status_agreement else None
            ),
        },
        "claim_boundary": (
            "The diagonal fibre map and signed incidence operator are exact. "
            "Channel ranks use independently validated numerical PT relation "
            "bases. This probe establishes the fixed-anchor 9->8 rank census, "
            "not yet an exact symbolic rank formula or a physical parity law."
        ),
        "elapsed_seconds": time.time() - started,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "diagonal_structure_ledger.csv",
            "relation_basis_summary.csv",
            "diagonal_channel_census.csv",
            "rank_distribution.csv",
            "feature_group_summary.csv",
            "feature_rank_correlations.csv",
            "johnson_pair_rank_audit.csv",
            "label_order_reflection_audit.csv",
        ],
    }

    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)
    with (out_dir / "verdict.json").open("w") as handle:
        json.dump(
            {
                "verdict": verdict,
                "global_rank": global_rank,
                "complete_targets": complete_targets,
                "diagonal_relation_law": diagonal_relation_law,
            },
            handle,
            indent=2,
        )

    strict_failures = []
    if args.strict:
        checks = {
            "full_35_channel_census": full_structure,
            "structural_diagonal_certificate": structural_success,
            "basis_validation": basis_valid,
            "residue_relation_validation": all_images_relational,
            "target_local_containment": all_images_local,
            "intersection_rank_consistency": all_intersection_matches_rank,
            "expected_global_rank": expected_rank_ok,
            "expected_complete_targets": expected_complete_ok,
        }
        strict_failures = [name for name, passed in checks.items() if not passed]

    print("\n" + "=" * 118)
    print("FINAL SUMMARY")
    print("=" * 118)
    print(f"Fixed-anchor diagonal structure:      {structural_success}")
    print(f"All residue images target-local:     {all_images_local}")
    print(f"All residue images PT-valid:         {all_images_relational}")
    print(f"Global direct-sum rank:               {global_rank}")
    print(f"Expected global rank:                 {args.expected_global_rank}")
    print(f"Complete target fibres:               {complete_targets}/{len(subsets)}")
    print(f"Expected complete targets:            {args.expected_complete_targets}")
    print(f"Rank distribution:                    {dict(sorted(rank_counts.items()))}")
    print(f"Channel classes:                      {dict(sorted(class_counts.items()))}")
    print(f"Verdict:                              {verdict}")
    print(f"elapsed:                              {time.time() - started:.2f} seconds")
    print(f"summary:                              {out_dir / 'summary.json'}")
    if args.strict:
        print(f"strict checks:                        {'PASS' if not strict_failures else 'FAIL'}")
        if strict_failures:
            print(f"failed checks:                        {', '.join(strict_failures)}")
    print("=" * 118)

    if strict_failures:
        raise SystemExit(2)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fixed-anchor 9->8 diagonal Parke--Taylor channel census."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--helper-script", required=True)
    parser.add_argument("--base-run-dir")
    parser.add_argument("--cache-dir")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--rows-multiplier", type=float, default=3.0)
    parser.add_argument("--min-rows", type=int, default=400)
    parser.add_argument("--validation-rows", type=int, default=120)
    parser.add_argument("--residue-validation-rows", type=int, default=160)
    parser.add_argument("--svd-tolerance", type=float, default=1e-11)
    parser.add_argument("--rank-tolerance", type=float, default=1e-10)
    parser.add_argument("--rank-absolute-tolerance", type=float, default=1e-12)
    parser.add_argument("--containment-tolerance", type=float, default=1e-8)
    parser.add_argument("--relation-verdict-tolerance", type=float, default=1e-8)
    parser.add_argument("--expected-global-rank", type=int, default=363)
    parser.add_argument("--expected-complete-targets", type=int, default=13)
    parser.add_argument("--max-channels", type=int, default=0)
    parser.add_argument("--force-rebuild", action="store_true")
    parser.add_argument("--structure-only", action="store_true")
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
