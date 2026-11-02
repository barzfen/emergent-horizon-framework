#!/usr/bin/env python3
r"""
EHF-AMP-FOUND-04B: Full Multi-Prime Boundary-Corrected Three-Tail Audit
========================================================================

04A completed the 126-channel GF(2) discovery census for the canonical
anchor-1, delete-11 chart and found:

* no nontrivial pure suffix law at widths 1, 2, or 3;
* a three-rightmost-label near-law with seven one-dimensional boundary splits;
* two systematic characteristic-two defects, 35->36 and 59->60, in a
  representative GF(3) audit;
* 21 channels saturating the 296-dimensional target relation space.

04B performs the required full cross-field audit.

For every four-subset A={a<b<c<d} of {2,...,10}, it computes the reduced
11->10 transmitted-image rank over GF(3) and GF(5), imports the completed
GF(2) ledger from 04A, and constructs exact rational lower/upper bounds:

    lower_Q(A) = max_p r_p(A),

    upper_Q(A) = min( target_relation_upper_Q,
                      min_p source_relation_dim_p(A) ).

Because modular matrix rank is a lower bound for rational rank, modular
nullity is an upper bound for rational nullity.  Therefore lower_Q=upper_Q
certifies the exact rational transmitted rank without a direct QQ elimination.

The main discovery test is the boundary-corrected three-tail ansatz

    r(a,b,c,d) = base(b,c,d)
                 + 1[d=10 and b in {5,6} and a>=4],

where base(b,c,d) is the minimum rank in the fixed three-tail class.  The
indicator pattern is fixed in advance from the 04A audit; 04B tests whether it
survives both odd primes.  Width four is explicitly excluded from the notion
of a nontrivial tail law.

The output remains a multi-prime discovery/partial-certification result, not a
complete exact QQ theorem unless every channel's rational bounds collapse.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_04b_full_multi_prime_boundary_corrected_tail_audit.py \
  --base-script scripts/ehf_amp_found_04a_eleven_to_ten_tail_filtration_discovery_census.py \
  --gf2-census runs/ehf_amp_found_04a/channel_census_gf2.csv \
  --out-dir runs/ehf_amp_found_04b \
  --fields 3,5 \
  --resume \
  --strict
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import itertools
import json
import math
import multiprocessing as mp
import random
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

Subset = Tuple[int, int, int, int]
SparseOutside = Mapping[Tuple[int, ...], int]
SparseImage = Mapping[int, int]
Planes = Tuple[int, ...]


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


def subset_text(subset: Sequence[int]) -> str:
    return ",".join(map(str, subset))


def parse_fields(text: str) -> Tuple[int, ...]:
    fields = tuple(int(value) for value in text.split(",") if value.strip())
    if not fields:
        raise argparse.ArgumentTypeError("At least one field is required")
    for field in fields:
        if field not in (3, 5):
            raise argparse.ArgumentTypeError("04B supports GF(3) and GF(5)")
    if len(set(fields)) != len(fields):
        raise argparse.ArgumentTypeError("Duplicate fields are not allowed")
    return fields


def read_csv_by_key(path: Path, key: str = "A") -> Dict[str, Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


# ---------------------------------------------------------------------------
# One-hot bit-sliced arithmetic over a small odd prime.
# ---------------------------------------------------------------------------


def planes_nonzero(planes: Planes) -> int:
    output = 0
    for plane in planes:
        output |= plane
    return output


def planes_coefficient(planes: Planes, bit: int) -> int:
    for residue, plane in enumerate(planes, start=1):
        if plane & bit:
            return residue
    return 0


def planes_scalar_mul(planes: Planes, scalar: int, prime: int) -> Planes:
    scalar %= prime
    if scalar == 0:
        return tuple(0 for _ in planes)
    output = [0] * (prime - 1)
    for residue, plane in enumerate(planes, start=1):
        target = (scalar * residue) % prime
        if target:
            output[target - 1] |= plane
    return tuple(output)


def planes_add(left: Planes, right: Planes, prime: int, universe_mask: int) -> Planes:
    left_zero = universe_mask ^ planes_nonzero(left)
    right_zero = universe_mask ^ planes_nonzero(right)
    left_masks = (left_zero,) + left
    right_masks = (right_zero,) + right
    output = [0] * (prime - 1)
    for left_value, left_mask in enumerate(left_masks):
        if not left_mask:
            continue
        for right_value, right_mask in enumerate(right_masks):
            intersection = left_mask & right_mask
            if not intersection:
                continue
            result = (left_value + right_value) % prime
            if result:
                output[result - 1] |= intersection
    return tuple(output)


def planes_add_scaled(
    left: Planes,
    right: Planes,
    scalar: int,
    prime: int,
    universe_mask: int,
) -> Planes:
    return planes_add(
        left,
        planes_scalar_mul(right, scalar, prime),
        prime,
        universe_mask,
    )


def sparse_outside_to_planes(
    column: SparseOutside,
    row_index: Mapping[Tuple[int, ...], int],
    prime: int,
) -> Planes:
    output = [0] * (prime - 1)
    for row, coefficient in column.items():
        residue = int(coefficient) % prime
        if residue:
            output[residue - 1] |= 1 << row_index[row]
    return tuple(output)


def sparse_image_to_planes(column: SparseImage, prime: int) -> Planes:
    output = [0] * (prime - 1)
    for row, coefficient in column.items():
        residue = int(coefficient) % prime
        if residue:
            output[residue - 1] |= 1 << int(row)
    return tuple(output)


def paired_rank_prime(
    outside_columns: Sequence[SparseOutside],
    residue_columns: Sequence[SparseImage],
    prime: int,
    order_seed: int,
    target_dimension: int,
) -> Tuple[int, int, int]:
    if prime not in (3, 5):
        raise ValueError(f"Unsupported prime GF({prime})")

    rows = {row for column in outside_columns for row in column}
    ordered_rows = sorted(rows)
    random.Random(order_seed).shuffle(ordered_rows)
    row_index = {row: index for index, row in enumerate(ordered_rows)}

    outside_mask = (1 << len(ordered_rows)) - 1 if ordered_rows else 0
    image_mask = (1 << target_dimension) - 1

    outside_basis: Dict[int, Tuple[Planes, Planes]] = {}
    image_basis: Dict[int, Planes] = {}

    # Natural column order is faster and more stable for the odd-prime audit.
    for outside_column, image_column in zip(outside_columns, residue_columns):
        vector = sparse_outside_to_planes(outside_column, row_index, prime)
        image = sparse_image_to_planes(image_column, prime)

        while planes_nonzero(vector):
            pivot = planes_nonzero(vector).bit_length() - 1
            bit = 1 << pivot
            coefficient = planes_coefficient(vector, bit)
            stored = outside_basis.get(pivot)
            if stored is None:
                inverse = pow(coefficient, -1, prime)
                vector = planes_scalar_mul(vector, inverse, prime)
                image = planes_scalar_mul(image, inverse, prime)
                outside_basis[pivot] = (vector, image)
                break
            stored_vector, stored_image = stored
            scalar = (-coefficient) % prime
            vector = planes_add_scaled(
                vector, stored_vector, scalar, prime, outside_mask
            )
            image = planes_add_scaled(
                image, stored_image, scalar, prime, image_mask
            )

        if not planes_nonzero(vector) and planes_nonzero(image):
            while planes_nonzero(image):
                pivot = planes_nonzero(image).bit_length() - 1
                bit = 1 << pivot
                coefficient = planes_coefficient(image, bit)
                stored_image = image_basis.get(pivot)
                if stored_image is None:
                    inverse = pow(coefficient, -1, prime)
                    image = planes_scalar_mul(image, inverse, prime)
                    image_basis[pivot] = image
                    break
                image = planes_add_scaled(
                    image,
                    stored_image,
                    (-coefficient) % prime,
                    prime,
                    image_mask,
                )

    return len(outside_basis), len(image_basis), len(ordered_rows)


def ordinary_rank_prime(
    columns: Sequence[Mapping[Tuple[int, ...], int]],
    prime: int,
    order_seed: int,
) -> int:
    empty_images: List[Dict[int, int]] = [{} for _ in columns]
    rank, _, _ = paired_rank_prime(
        columns,
        empty_images,
        prime,
        order_seed,
        target_dimension=1,
    )
    return rank


# ---------------------------------------------------------------------------
# Isolated workers and resume ledgers.
# ---------------------------------------------------------------------------


def channel_worker(payload: Mapping[str, object]) -> Dict[str, object]:
    base_script = Path(str(payload["base_script"])).resolve()
    base = load_module(base_script, f"ehf_amp_found_04b_base_{mp.current_process().pid}")
    subset = tuple(int(value) for value in payload["subset"])
    prime = int(payload["field"])
    order_seed = int(payload["order_seed"])
    started = time.time()

    outside, residue, metadata = base.build_reduced_channel(11, subset)
    c_rank, residue_rank, outside_rows = paired_rank_prime(
        outside,
        residue,
        prime,
        order_seed,
        target_dimension=int(metadata["target_fibre_size"]),
    )
    source_relation_dim = len(outside) - c_rank
    result = {
        "A": subset_text(subset),
        "subset": subset,
        "field": prime,
        "order_seed": order_seed,
        "C_rank": c_rank,
        "source_relation_dim": source_relation_dim,
        "residue_rank": residue_rank,
        "elapsed_seconds": time.time() - started,
        **metadata,
    }
    result["structure_checks_pass"] = (
        metadata["source_fibre_size"] == metadata["source_fibre_size_formula"]
        and metadata["target_fibre_size"] == metadata["target_fibre_size_formula"]
        and metadata["active_source_columns"] == metadata["active_source_formula"]
        and metadata["target_preimage_min"] == 2
        and metadata["target_preimage_max"] == 2
        and outside_rows == metadata["outside_distinct_rows"]
    )
    return result


def run_subprocess_worker(
    script_path: Path,
    base_script: Path,
    subset: Subset,
    field: int,
    order_seed: int,
    timeout_seconds: float,
) -> Tuple[Optional[Dict[str, object]], str]:
    command = [
        sys.executable,
        str(script_path),
        "--internal-worker",
        "--base-script",
        str(base_script),
        "--internal-subset",
        subset_text(subset),
        "--internal-field",
        str(field),
        "--internal-order-seed",
        str(order_seed),
    ]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return None, "timeout"
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip()
        return None, f"worker_exit_{completed.returncode}: {message[-800:]}"
    try:
        return json.loads(completed.stdout.strip().splitlines()[-1]), "ok"
    except Exception as exc:
        return None, f"worker_json_error: {exc}: {completed.stdout[-800:]}"


def normalize_bool(value: object) -> bool:
    return str(value).strip().lower() in ("true", "1", "yes")


def normalize_int(value: object) -> int:
    return int(str(value).strip())


def channel_row_from_result(
    subset: Subset,
    result: Mapping[str, object],
    field: int,
    target_relation_dim: int,
    channel_index: int,
) -> Dict[str, object]:
    prefix = f"GF{field}"
    return {
        "channel_index": channel_index,
        "A": subset_text(subset),
        "a": subset[0],
        "b": subset[1],
        "c": subset[2],
        "d": subset[3],
        "last_3": subset_text(subset[-3:]),
        "source_fibre_size": result["source_fibre_size"],
        "inactive_source_columns": result["inactive_source_columns"],
        f"{prefix}_C_rank": result["C_rank"],
        f"{prefix}_source_relation_dim": result["source_relation_dim"],
        f"{prefix}_residue_rank": result["residue_rank"],
        f"{prefix}_target_relation_dim": target_relation_dim,
        f"{prefix}_target_missing_dim": target_relation_dim - int(result["residue_rank"]),
        f"{prefix}_complete_target_recovery": int(result["residue_rank"]) == target_relation_dim,
        "active_source_columns": result["active_source_columns"],
        "target_fibre_size": result["target_fibre_size"],
        "target_preimage_min": result["target_preimage_min"],
        "target_preimage_max": result["target_preimage_max"],
        "outside_distinct_rows": result["outside_distinct_rows"],
        "structure_checks_pass": result["structure_checks_pass"],
        "order_seed": result["order_seed"],
        "elapsed_seconds": f"{float(result['elapsed_seconds']):.6f}",
    }


# ---------------------------------------------------------------------------
# Audits and rational certification.
# ---------------------------------------------------------------------------


def tail_width_audit(
    combined_rows: Sequence[Mapping[str, object]],
    rank_field: str,
) -> Tuple[List[Dict[str, object]], Optional[int]]:
    output: List[Dict[str, object]] = []
    minimal_nontrivial = None
    for width in (1, 2, 3):
        groups: MutableMapping[Tuple[int, ...], List[int]] = defaultdict(list)
        for row in combined_rows:
            subset = tuple(map(int, str(row["A"]).split(",")))
            groups[subset[-width:]].append(int(row[rank_field]))
        bad = {
            key: sorted(set(values))
            for key, values in groups.items()
            if len(set(values)) > 1
        }
        constant = not bad
        if constant and minimal_nontrivial is None:
            minimal_nontrivial = width
        output.append({
            "rank_field": rank_field,
            "tail_width": width,
            "group_count": len(groups),
            "rank_constant_within_all_groups": constant,
            "nonconstant_group_count": len(bad),
            "nonconstant_examples": ";".join(
                f"{subset_text(key)}:{','.join(map(str, values))}"
                for key, values in sorted(bad.items())
            ),
        })
    return output, minimal_nontrivial


def boundary_corrected_three_tail_audit(
    rows: Sequence[Mapping[str, object]],
    rank_field: str,
) -> Tuple[List[Dict[str, object]], bool, List[Tuple[int, int, int]]]:
    groups: MutableMapping[Tuple[int, int, int], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        groups[(int(row["b"]), int(row["c"]), int(row["d"]))].append(row)

    audit_rows: List[Dict[str, object]] = []
    nonconstant_tails: List[Tuple[int, int, int]] = []
    formula_exact = True

    for tail, members in sorted(groups.items()):
        observed = sorted({int(member[rank_field]) for member in members})
        base_rank = min(observed)
        predictions = []
        member_details = []
        for member in sorted(members, key=lambda row: int(row["a"])):
            a, b, _, d = (
                int(member["a"]),
                int(member["b"]),
                int(member["c"]),
                int(member["d"]),
            )
            correction = int(d == 10 and b in (5, 6) and a >= 4)
            prediction = base_rank + correction
            actual = int(member[rank_field])
            predictions.append(prediction == actual)
            member_details.append(
                f"a={a}:actual={actual}:pred={prediction}:corr={correction}"
            )
        if len(observed) > 1:
            nonconstant_tails.append(tail)
        group_exact = all(predictions)
        formula_exact &= group_exact
        audit_rows.append({
            "rank_field": rank_field,
            "tail_b_c_d": subset_text(tail),
            "channel_count": len(members),
            "observed_ranks": ",".join(map(str, observed)),
            "base_rank": base_rank,
            "nonconstant": len(observed) > 1,
            "one_dimensional_split": len(observed) <= 2 and max(observed) - min(observed) <= 1,
            "boundary_indicator_formula_exact": group_exact,
            "members": ";".join(member_details),
        })

    return audit_rows, formula_exact, nonconstant_tails


def componentwise_monotonicity_audit(
    rows: Sequence[Mapping[str, object]],
    rank_field: str,
) -> Tuple[List[Dict[str, object]], bool, int]:
    parsed = [
        (tuple(map(int, str(row["A"]).split(","))), int(row[rank_field]))
        for row in rows
    ]
    violations: List[Dict[str, object]] = []
    comparable_pairs = 0
    for left_subset, left_rank in parsed:
        for right_subset, right_rank in parsed:
            if left_subset == right_subset:
                continue
            if all(left <= right for left, right in zip(left_subset, right_subset)):
                comparable_pairs += 1
                if left_rank > right_rank:
                    violations.append({
                        "rank_field": rank_field,
                        "left_A": subset_text(left_subset),
                        "left_rank": left_rank,
                        "right_A": subset_text(right_subset),
                        "right_rank": right_rank,
                    })
    return violations, not violations, comparable_pairs


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    script_path = Path(__file__).resolve()
    base_script = Path(args.base_script).resolve()
    gf2_path = Path(args.gf2_census).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    base = load_module(base_script, "ehf_amp_found_04b_base_main")

    fields = tuple(args.fields)
    all_subsets: List[Subset] = list(itertools.combinations(range(2, 11), 4))
    if args.subset:
        requested: List[Subset] = []
        for text in args.subset:
            subset = tuple(map(int, text.split(",")))
            if subset not in all_subsets:
                raise ValueError(f"Invalid four-subset: {text}")
            requested.append(subset)  # type: ignore[arg-type]
    else:
        requested = all_subsets[args.start_index:]
        if args.max_channels:
            requested = requested[:args.max_channels]

    print("=" * 128)
    print("EHF-AMP-FOUND-04B: FULL MULTI-PRIME BOUNDARY-CORRECTED THREE-TAIL AUDIT")
    print("=" * 128)
    print(f"04A engine:                   {base_script}")
    print(f"GF(2) census:                 {gf2_path}")
    print(f"output directory:             {out_dir}")
    print(f"odd-prime fields:             {fields}")
    print("reference chart:              anchor 1, delete 11")
    print("claim status:                 multi-prime discovery and partial QQ certification")

    gf2_rows = read_csv_by_key(gf2_path)
    missing_gf2 = [subset_text(subset) for subset in requested if subset_text(subset) not in gf2_rows]
    if missing_gf2:
        raise RuntimeError(f"GF(2) census is missing requested channels: {missing_gf2[:10]}")

    # Mandatory nine-point self-check over both odd primes.
    self_check_rows: List[Dict[str, object]] = []
    self_check_pass = True
    if not args.skip_nine_point_self_check:
        print("\nNine-point multi-prime engine self-check")
        for field in fields:
            for subset3 in itertools.combinations(range(2, 9), 3):
                outside, residue, metadata = base.build_reduced_channel(9, subset3)
                c_rank, image_rank, outside_rows = paired_rank_prime(
                    outside,
                    residue,
                    field,
                    args.order_seed,
                    target_dimension=int(metadata["target_fibre_size"]),
                )
                expected = base.known_rank_9(subset3)
                match = image_rank == expected
                structure = (
                    metadata["target_preimage_min"] == 2
                    and metadata["target_preimage_max"] == 2
                    and outside_rows == metadata["outside_distinct_rows"]
                )
                self_check_pass &= match and structure
                self_check_rows.append({
                    "field": field,
                    "A": subset_text(subset3),
                    "expected_exact_rank": expected,
                    "residue_rank": image_rank,
                    "C_rank": c_rank,
                    "match": match,
                    "structure_checks_pass": structure,
                })
            print(f"  GF({field}) recovered all 35 known ranks: {self_check_pass}")
    write_csv(out_dir / "nine_point_multi_prime_self_check.csv", self_check_rows)

    # Target relation dimensions by field.
    reference_subset: Subset = (2, 3, 4, 5)
    target_columns = base.build_target_kk_columns(11, reference_subset)
    target_dimensions: Dict[int, int] = {2: normalize_int(next(iter(gf2_rows.values()))["GF2_target_relation_dim"])}
    target_dimension_rows: List[Dict[str, object]] = [{
        "field": 2,
        "target_state_count": len(target_columns),
        "target_KK_rank": len(target_columns) - target_dimensions[2],
        "target_relation_dimension": target_dimensions[2],
    }]
    print("\nReference n=10 target relation dimensions")
    print(f"  GF(2): {target_dimensions[2]}")
    for field in fields:
        target_rank = ordinary_rank_prime(target_columns, field, args.order_seed)
        target_dimensions[field] = len(target_columns) - target_rank
        target_dimension_rows.append({
            "field": field,
            "target_state_count": len(target_columns),
            "target_KK_rank": target_rank,
            "target_relation_dimension": target_dimensions[field],
        })
        print(f"  GF({field}): {target_dimensions[field]}")
    write_csv(out_dir / "target_relation_dimension_by_field.csv", target_dimension_rows)

    failures: List[Dict[str, object]] = []
    field_ledgers: Dict[int, Dict[str, Dict[str, object]]] = {}

    for field in fields:
        ledger_path = out_dir / f"channel_census_gf{field}.csv"
        existing = read_csv_by_key(ledger_path) if args.resume and ledger_path.exists() else {}
        completed: Dict[str, Dict[str, object]] = {key: dict(value) for key, value in existing.items()}
        timeout = args.gf3_timeout if field == 3 else args.gf5_timeout

        print(f"\nFull GF({field}) channel census")
        for ordinal, subset in enumerate(requested, start=1):
            key = subset_text(subset)
            if key in completed:
                print(f"  [{ordinal:03d}/{len(requested):03d}] A={key:9s} resume")
                continue

            result = None
            status = "not_run"
            for seed in args.retry_order_seeds:
                result, status = run_subprocess_worker(
                    script_path,
                    base_script,
                    subset,
                    field,
                    seed,
                    timeout,
                )
                if result is not None:
                    break
            if result is None:
                failures.append({"field": field, "A": key, "status": status})
                print(f"  [{ordinal:03d}/{len(requested):03d}] A={key:9s} FAILED {status}")
                continue

            row = channel_row_from_result(
                subset,
                result,
                field,
                target_dimensions[field],
                all_subsets.index(subset),
            )
            completed[key] = row
            ordered = [completed[subset_text(item)] for item in all_subsets if subset_text(item) in completed]
            write_csv(ledger_path, ordered)
            print(
                f"  [{ordinal:03d}/{len(requested):03d}] A={key:9s} "
                f"r={row[f'GF{field}_residue_rank']:4d} "
                f"source={row['source_fibre_size']:5d} "
                f"{float(result['elapsed_seconds']):6.2f}s"
            )
        field_ledgers[field] = completed

    # Assemble only channels completed in every requested field.
    common_keys = [
        subset_text(subset)
        for subset in requested
        if all(subset_text(subset) in field_ledgers[field] for field in fields)
    ]
    combined_rows: List[Dict[str, object]] = []
    target_upper_q = min(target_dimensions.values())

    for key in common_keys:
        gf2 = gf2_rows[key]
        subset = tuple(map(int, key.split(",")))
        row: Dict[str, object] = {
            "channel_index": all_subsets.index(subset),
            "A": key,
            "a": subset[0],
            "b": subset[1],
            "c": subset[2],
            "d": subset[3],
            "last_3": subset_text(subset[-3:]),
            "source_fibre_size": normalize_int(gf2["source_fibre_size"]),
            "GF2_C_rank": normalize_int(gf2["GF2_C_rank"]),
            "GF2_source_relation_dim": normalize_int(gf2["GF2_source_relation_dim"]),
            "GF2_residue_rank": normalize_int(gf2["GF2_residue_rank"]),
            "GF2_target_relation_dim": normalize_int(gf2["GF2_target_relation_dim"]),
        }
        residue_ranks = [int(row["GF2_residue_rank"])]
        source_upper_bounds = [int(row["GF2_source_relation_dim"])]
        all_structure = normalize_bool(gf2["structure_checks_pass"])

        for field in fields:
            source = field_ledgers[field][key]
            prefix = f"GF{field}"
            for column in (
                f"{prefix}_C_rank",
                f"{prefix}_source_relation_dim",
                f"{prefix}_residue_rank",
                f"{prefix}_target_relation_dim",
            ):
                row[column] = normalize_int(source[column])
            residue_ranks.append(int(row[f"{prefix}_residue_rank"]))
            source_upper_bounds.append(int(row[f"{prefix}_source_relation_dim"]))
            all_structure &= normalize_bool(source["structure_checks_pass"])

        lower_q = max(residue_ranks)
        source_upper_q = min(source_upper_bounds)
        upper_q = min(target_upper_q, source_upper_q)
        exact = lower_q == upper_q

        row.update({
            "modular_residue_ranks": ";".join(
                f"GF{field}={rank}"
                for field, rank in zip((2,) + fields, residue_ranks)
            ),
            "all_tested_fields_agree": len(set(residue_ranks)) == 1,
            "GF3_GF5_agree": (
                int(row.get("GF3_residue_rank", -1))
                == int(row.get("GF5_residue_rank", -2))
                if 3 in fields and 5 in fields else ""
            ),
            "characteristic_two_defect": (
                int(row["GF2_residue_rank"])
                < max(residue_ranks[1:])
            ),
            "generic_modular_rank": max(residue_ranks[1:]),
            "rational_rank_lower_bound": lower_q,
            "rational_source_dimension_upper_bound": source_upper_q,
            "rational_target_dimension_upper_bound": target_upper_q,
            "rational_rank_upper_bound": upper_q,
            "rational_rank_exact_certified": exact,
            "exact_rational_rank": lower_q if exact else "",
            "exact_certificate_type": (
                "target_saturation"
                if exact and lower_q == target_upper_q
                else "source_or_combined_bound_saturation"
                if exact else "modular_bounds_open"
            ),
            "all_structure_checks_pass": all_structure,
        })
        combined_rows.append(row)

    write_csv(out_dir / "multi_prime_channel_census.csv", combined_rows)

    # Cross-field disagreement ledger.
    disagreement_rows: List[Dict[str, object]] = []
    for row in combined_rows:
        ranks = {field: int(row[f"GF{field}_residue_rank"]) for field in (2,) + fields}
        if len(set(ranks.values())) > 1:
            disagreement_rows.append({
                "A": row["A"],
                **{f"GF{field}_rank": rank for field, rank in ranks.items()},
                "rank_min": min(ranks.values()),
                "rank_max": max(ranks.values()),
                "spread": max(ranks.values()) - min(ranks.values()),
                "GF3_GF5_agree": row["GF3_GF5_agree"],
            })
    write_csv(out_dir / "field_disagreement_audit.csv", disagreement_rows)

    # Tail and boundary audits for each odd prime and the strongest modular lower bound.
    tail_rows: List[Dict[str, object]] = []
    boundary_rows: List[Dict[str, object]] = []
    minimal_nontrivial_by_rank: Dict[str, Optional[int]] = {}
    boundary_formula_by_rank: Dict[str, bool] = {}
    nonconstant_tails_by_rank: Dict[str, List[Tuple[int, int, int]]] = {}

    rank_fields = [f"GF{field}_residue_rank" for field in fields] + ["generic_modular_rank"]
    for rank_field in rank_fields:
        audit, minimal = tail_width_audit(combined_rows, rank_field)
        tail_rows.extend(audit)
        minimal_nontrivial_by_rank[rank_field] = minimal
        boundary, formula_exact, tails = boundary_corrected_three_tail_audit(
            combined_rows, rank_field
        )
        boundary_rows.extend(boundary)
        boundary_formula_by_rank[rank_field] = formula_exact
        nonconstant_tails_by_rank[rank_field] = tails
    write_csv(out_dir / "tail_width_audit_multi_prime.csv", tail_rows)
    write_csv(out_dir / "boundary_corrected_three_tail_audit.csv", boundary_rows)

    # Monotonicity.
    monotonicity_rows: List[Dict[str, object]] = []
    monotonicity_summary: Dict[str, Dict[str, object]] = {}
    for rank_field in rank_fields:
        violations, monotone, comparable = componentwise_monotonicity_audit(
            combined_rows, rank_field
        )
        monotonicity_rows.extend(violations)
        monotonicity_summary[rank_field] = {
            "componentwise_monotone": monotone,
            "comparable_ordered_pair_count": comparable,
            "violation_count": len(violations),
        }
    write_csv(out_dir / "componentwise_monotonicity_violations.csv", monotonicity_rows)

    # Complete-recovery criterion and exact-certification summaries.
    complete_rows = [row for row in combined_rows if int(row["generic_modular_rank"]) == target_upper_q]
    complete_criterion = bool(combined_rows) and all(
        (int(row["generic_modular_rank"]) == target_upper_q) == (int(row["b"]) >= 7)
        for row in combined_rows
    )
    write_csv(out_dir / "complete_recovery_channels.csv", complete_rows)

    exact_rows = [row for row in combined_rows if bool(row["rational_rank_exact_certified"])]
    exact_distribution = Counter(int(row["exact_rational_rank"]) for row in exact_rows)
    exact_summary_rows = [
        {
            "exact_rational_rank": rank,
            "certified_channel_count": count,
            "rank_contribution": rank * count,
        }
        for rank, count in sorted(exact_distribution.items())
    ]
    write_csv(out_dir / "exact_rank_certification_summary.csv", exact_summary_rows)

    full_requested = len(requested) == 126
    full_common = len(combined_rows) == len(requested)
    all_structure = bool(combined_rows) and all(bool(row["all_structure_checks_pass"]) for row in combined_rows)
    gf3_gf5_agree = (
        bool(combined_rows)
        and 3 in fields
        and 5 in fields
        and all(bool(row["GF3_GF5_agree"]) for row in combined_rows)
    )
    expected_boundary_tails = {
        (5, 6, 10),
        (5, 7, 10),
        (5, 8, 10),
        (5, 9, 10),
        (6, 7, 10),
        (6, 8, 10),
        (6, 9, 10),
    }
    generic_tails = set(nonconstant_tails_by_rank.get("generic_modular_rank", []))
    boundary_pattern_exact = (
        boundary_formula_by_rank.get("generic_modular_rank", False)
        and generic_tails == expected_boundary_tails
    )
    no_nontrivial_pure_tail = minimal_nontrivial_by_rank.get("generic_modular_rank") is None

    if (
        full_requested
        and full_common
        and self_check_pass
        and all_structure
        and gf3_gf5_agree
        and boundary_pattern_exact
        and no_nontrivial_pure_tail
        and complete_criterion
    ):
        verdict = "EHF_AMP_FOUND_04B_MULTI_PRIME_BOUNDARY_CORRECTED_THREE_TAIL_CANDIDATE_SUPPORTED"
    elif full_requested and full_common and not gf3_gf5_agree:
        verdict = "EHF_AMP_FOUND_04B_ODD_PRIME_FIELD_DEPENDENCE_DETECTED"
    elif full_common:
        verdict = "EHF_AMP_FOUND_04B_PARTIAL_MULTI_PRIME_AUDIT_COMPLETE"
    else:
        verdict = "EHF_AMP_FOUND_04B_MULTI_PRIME_AUDIT_INCOMPLETE"

    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "claim_status": "multi-prime discovery and rational bound certification; not yet a complete QQ theorem",
        "nine_point_multi_prime_self_check_pass": self_check_pass,
        "target_relation_dimensions": {str(field): value for field, value in sorted(target_dimensions.items())},
        "rational_target_relation_dimension_upper_bound": target_upper_q,
        "requested_channel_count": len(requested),
        "completed_all_requested_fields_count": len(combined_rows),
        "full_126_channel_multi_prime_census": full_requested and full_common,
        "all_structure_checks_pass": all_structure,
        "GF3_GF5_all_channels_agree": gf3_gf5_agree,
        "field_disagreement_count_including_GF2": len(disagreement_rows),
        "characteristic_two_defect_count": sum(bool(row["characteristic_two_defect"]) for row in combined_rows),
        "minimal_nontrivial_tail_width_by_rank": {
            key: value for key, value in minimal_nontrivial_by_rank.items()
        },
        "pure_tail_width_less_than_four_found": (
            not no_nontrivial_pure_tail if full_requested and full_common else None
        ),
        "boundary_corrected_three_tail_formula_exact": (
            boundary_pattern_exact if full_requested and full_common else None
        ),
        "nonconstant_generic_three_tails": [subset_text(tail) for tail in sorted(generic_tails)],
        "componentwise_monotonicity": monotonicity_summary,
        "complete_recovery_criterion_b_ge_7": (
            complete_criterion if full_requested and full_common else None
        ),
        "complete_recovery_channel_count": len(complete_rows),
        "rational_target_relation_dimension_exact_certified": bool(complete_rows),
        "exact_rational_target_relation_dimension": target_upper_q if complete_rows else "",
        "exact_rational_rank_certified_channel_count": len(exact_rows),
        "exact_rational_rank_distribution": dict(sorted(exact_distribution.items())),
        "all_126_rational_ranks_exact_certified": len(exact_rows) == 126,
        "failure_count": len(failures),
        "failures": failures,
        "elapsed_seconds": time.time() - started,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "nine_point_multi_prime_self_check.csv",
            "target_relation_dimension_by_field.csv",
            "channel_census_gf3.csv",
            "channel_census_gf5.csv",
            "multi_prime_channel_census.csv",
            "field_disagreement_audit.csv",
            "tail_width_audit_multi_prime.csv",
            "boundary_corrected_three_tail_audit.csv",
            "componentwise_monotonicity_violations.csv",
            "complete_recovery_channels.csv",
            "exact_rank_certification_summary.csv",
        ],
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    (out_dir / "verdict.json").write_text(json.dumps({
        "verdict": verdict,
        "full_126_channel_multi_prime_census": summary["full_126_channel_multi_prime_census"],
        "GF3_GF5_all_channels_agree": gf3_gf5_agree,
        "boundary_corrected_three_tail_formula_exact": summary["boundary_corrected_three_tail_formula_exact"],
        "pure_tail_width_less_than_four_found": summary["pure_tail_width_less_than_four_found"],
        "exact_rational_rank_certified_channel_count": len(exact_rows),
        "claim_status": summary["claim_status"],
    }, indent=2))

    strict_failures: List[str] = []
    if args.strict:
        if not self_check_pass:
            strict_failures.append("nine_point_multi_prime_self_check")
        if not full_common:
            strict_failures.append("requested_multi_prime_census_incomplete")
        if not all_structure:
            strict_failures.append("structure_checks")
        if full_requested and not gf3_gf5_agree:
            strict_failures.append("GF3_GF5_disagreement")
        if full_requested and not boundary_pattern_exact:
            strict_failures.append("boundary_corrected_three_tail_pattern")
        if full_requested and not no_nontrivial_pure_tail:
            strict_failures.append("unexpected_nontrivial_pure_tail")
        if full_requested and not complete_criterion:
            strict_failures.append("complete_recovery_criterion")
        if failures:
            strict_failures.append("worker_failures")

    print("\n" + "=" * 128)
    print("FINAL SUMMARY")
    print("=" * 128)
    print(f"Nine-point multi-prime self-check:    {self_check_pass}")
    print(f"Completed all-field channels:         {len(combined_rows)} / {len(requested)}")
    print(f"Target relation dimensions:           {dict(sorted(target_dimensions.items()))}")
    print(f"GF(3)/GF(5) all-channel agreement:    {gf3_gf5_agree}")
    print(f"Characteristic-two defect channels:   {summary['characteristic_two_defect_count']}")
    print(f"Nontrivial pure tail width < 4:        {summary['pure_tail_width_less_than_four_found']}")
    print(f"Boundary-corrected three-tail law:     {summary['boundary_corrected_three_tail_formula_exact']}")
    print(f"Complete recovery iff b>=7:           {summary['complete_recovery_criterion_b_ge_7']}")
    print(f"Exact QQ ranks certified:             {len(exact_rows)} / {len(combined_rows)}")
    print(f"Verdict:                              {verdict}")
    print(f"elapsed:                              {time.time() - started:.2f} seconds")
    print(f"summary:                              {out_dir / 'summary.json'}")
    if args.strict:
        print(f"strict checks:                        {'PASS' if not strict_failures else 'FAIL'}")
        if strict_failures:
            print(f"failed checks:                        {', '.join(strict_failures)}")
    print("=" * 128)

    if strict_failures:
        raise SystemExit(2)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the complete GF(3)/GF(5) 11->10 channel census, audit the "
            "boundary-corrected three-tail candidate, and derive rational "
            "rank bounds/certificates."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--gf2-census", default="")
    parser.add_argument("--out-dir", default="")
    parser.add_argument("--fields", type=parse_fields, default=(3, 5))
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--max-channels", type=int, default=0)
    parser.add_argument("--subset", action="append", help="Run a specific A, e.g. 2,3,4,8")
    parser.add_argument("--order-seed", type=int, default=1)
    parser.add_argument(
        "--retry-order-seeds",
        type=lambda text: tuple(map(int, text.split(","))),
        default=(1, 2, 3),
    )
    parser.add_argument("--gf3-timeout", type=float, default=240.0)
    parser.add_argument("--gf5-timeout", type=float, default=300.0)
    parser.add_argument("--skip-nine-point-self-check", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--internal-worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--internal-subset", default="", help=argparse.SUPPRESS)
    parser.add_argument("--internal-field", type=int, default=3, help=argparse.SUPPRESS)
    parser.add_argument("--internal-order-seed", type=int, default=1, help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.internal_worker:
        if not args.internal_subset:
            raise SystemExit("--internal-subset is required")
        subset = tuple(map(int, args.internal_subset.split(",")))
        result = channel_worker({
            "base_script": args.base_script,
            "subset": subset,
            "field": args.internal_field,
            "order_seed": args.internal_order_seed,
        })
        print(json.dumps(result, separators=(",", ":")))
        return 0

    if not args.out_dir:
        raise SystemExit("--out-dir is required")
    if not args.gf2_census:
        raise SystemExit("--gf2-census is required")
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "run.log").open("a" if args.resume else "w") as log:
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
