#!/usr/bin/env python3
r"""
EHF-AMP-FOUND-04C-T0: Odd-Prime Exceptional-Prime / 2-Primary Torsion Precursor Audit
======================================================================================

This probe runs independently of the direct exact-QQ 04C sweep.  It asks whether
any additional odd prime sees a rank drop or rank increase relative to the common
GF(3)/GF(5) eleven-to-ten transmitted-image rank discovered by 04B.

For each requested channel A={a<b<c<d} and odd prime p, it computes exactly over
GF(p):

    r_p(A) = rank([C_A; L_A]) - rank(C_A)

using a one-hot bit-sliced sparse elimination engine.  The calculation imports
only the exact integer channel construction from 04A; it does not import 04C
rational results.

The probe is evidence for or against the conjecture that all saturation defects
of the integral transmitted-image lattice are 2-primary.  Even agreement across
many odd primes is not a proof of that conjecture; a proof would require Smith
normal form, saturation, or determinantal-divisor control.

Recommended server run
----------------------

python3 scripts/ehf_amp_found_04c_t0_odd_prime_exceptional_prime_audit.py \
  --base-script scripts/ehf_amp_found_04a_eleven_to_ten_tail_filtration_discovery_census.py \
  --multi-prime-census runs/ehf_amp_found_04b/multi_prime_channel_census.csv \
  --out-dir runs/ehf_amp_found_04c_t0_frontier \
  --fields 7,11,13 \
  --scope frontier \
  --worker-timeout 7200 \
  --order-seeds 1,2 \
  --resume \
  --require-candidate-agreement \
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
                fields.append(key)
                seen.add(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def subset_text(subset: Sequence[int]) -> str:
    return ",".join(map(str, subset))


def normalize_bool(value: object) -> bool:
    return str(value).strip().lower() in ("true", "1", "yes")


def normalize_int(value: object, default: Optional[int] = None) -> Optional[int]:
    text = str(value).strip()
    if text == "":
        return default
    try:
        return int(text)
    except (TypeError, ValueError):
        return default


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    limit = int(math.isqrt(value))
    for divisor in range(3, limit + 1, 2):
        if value % divisor == 0:
            return False
    return True


def parse_fields(text: str) -> Tuple[int, ...]:
    fields = tuple(int(part.strip()) for part in text.split(",") if part.strip())
    if not fields:
        raise argparse.ArgumentTypeError("At least one odd prime is required")
    if len(set(fields)) != len(fields):
        raise argparse.ArgumentTypeError("Duplicate primes are not allowed")
    for field in fields:
        if field == 2 or not is_prime(field):
            raise argparse.ArgumentTypeError(f"{field} is not an odd prime")
        if field > 31:
            raise argparse.ArgumentTypeError(
                "Primes above 31 are intentionally disabled: the one-hot engine scales roughly quadratically in p"
            )
    return fields


def parse_int_tuple(text: str) -> Tuple[int, ...]:
    values = tuple(int(part.strip()) for part in text.split(",") if part.strip())
    if not values:
        raise argparse.ArgumentTypeError("At least one integer is required")
    return values


def parse_subsets(text: str) -> Tuple[Subset, ...]:
    output: List[Subset] = []
    for block in text.split(";"):
        block = block.strip()
        if not block:
            continue
        subset = tuple(int(part.strip()) for part in block.split(","))
        if len(subset) != 4 or tuple(sorted(subset)) != subset:
            raise argparse.ArgumentTypeError(f"Invalid ordered four-subset: {block}")
        if any(value < 2 or value > 10 for value in subset):
            raise argparse.ArgumentTypeError(f"Subset outside 2..10: {block}")
        output.append(subset)  # type: ignore[arg-type]
    return tuple(output)


# ---------------------------------------------------------------------------
# One-hot bit-sliced arithmetic over GF(p).
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


def planes_add_scaled(
    left: Planes,
    right: Planes,
    scalar: int,
    prime: int,
    universe_mask: int,
) -> Planes:
    """Return left + scalar*right with one-hot residue planes."""
    scalar %= prime
    if scalar == 0:
        return left
    scaled = planes_scalar_mul(right, scalar, prime)
    left_zero = universe_mask ^ planes_nonzero(left)
    right_zero = universe_mask ^ planes_nonzero(scaled)
    left_masks = (left_zero,) + left
    right_masks = (right_zero,) + scaled
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
    if prime == 2 or not is_prime(prime):
        raise ValueError(f"GF({prime}) is not an odd prime field")

    rows = {row for column in outside_columns for row in column}
    ordered_rows = sorted(rows)
    if order_seed:
        random.Random(order_seed).shuffle(ordered_rows)
    row_index = {row: index for index, row in enumerate(ordered_rows)}

    outside_mask = (1 << len(ordered_rows)) - 1 if ordered_rows else 0
    image_mask = (1 << target_dimension) - 1
    outside_basis: Dict[int, Tuple[Planes, Planes]] = {}
    image_basis: Dict[int, Planes] = {}

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
            vector = planes_add_scaled(vector, stored_vector, scalar, prime, outside_mask)
            image = planes_add_scaled(image, stored_image, scalar, prime, image_mask)

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


# ---------------------------------------------------------------------------
# Channel workers.
# ---------------------------------------------------------------------------


def channel_worker(payload: Mapping[str, object]) -> Dict[str, object]:
    base_script = Path(str(payload["base_script"])).resolve()
    base = load_module(base_script, f"ehf_amp_found_04c_t0_base_{mp.current_process().pid}")
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
    structure_checks_pass = (
        metadata["source_fibre_size"] == metadata["source_fibre_size_formula"]
        and metadata["target_fibre_size"] == metadata["target_fibre_size_formula"]
        and metadata["active_source_columns"] == metadata["active_source_formula"]
        and metadata["target_preimage_min"] == 2
        and metadata["target_preimage_max"] == 2
        and outside_rows == metadata["outside_distinct_rows"]
    )
    return {
        "A": subset_text(subset),
        "subset": subset,
        "field": prime,
        "order_seed": order_seed,
        "C_rank": c_rank,
        "source_relation_dim": source_relation_dim,
        "residue_rank": residue_rank,
        "elapsed_seconds": time.time() - started,
        "structure_checks_pass": structure_checks_pass,
        **metadata,
    }


def run_worker_subprocess(
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
        return None, f"worker_exit_{completed.returncode}: {message[-1000:]}"
    try:
        return json.loads(completed.stdout.strip().splitlines()[-1]), "ok"
    except Exception as exc:
        return None, f"worker_json_error:{exc}:{completed.stdout[-1000:]}"


# ---------------------------------------------------------------------------
# Scope selection and audits.
# ---------------------------------------------------------------------------


def boundary_correction(subset: Subset) -> int:
    a, b, _c, d = subset
    return int(d == 10 and b in (5, 6) and a >= 4)


def select_frontier(rows: Sequence[Mapping[str, object]]) -> List[Subset]:
    selected: set[Subset] = set()

    # Every characteristic-two defect channel.
    for row in rows:
        if normalize_bool(row.get("characteristic_two_defect", False)):
            selected.add(tuple(int(value) for value in str(row["A"]).split(",")))  # type: ignore[arg-type]

    # One least-complex representative per generic odd-prime rank class.
    by_rank: Dict[int, Tuple[int, Subset]] = {}
    for row in rows:
        rank = int(str(row["generic_modular_rank"]))
        subset = tuple(int(value) for value in str(row["A"]).split(","))
        complexity = int(str(row.get("source_fibre_size", 10**9)))
        current = by_rank.get(rank)
        if current is None or complexity < current[0]:
            by_rank[rank] = (complexity, subset)  # type: ignore[assignment]
    selected.update(value[1] for value in by_rank.values())

    # Include every member of each nonconstant three-tail class so the one-dimensional
    # boundary split is directly audited over the new primes.
    tails: MutableMapping[Tuple[int, int, int], List[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        subset = tuple(int(value) for value in str(row["A"]).split(","))
        tails[subset[-3:]].append(row)
    for members in tails.values():
        ranks = {int(str(member["generic_modular_rank"])) for member in members}
        if len(ranks) > 1:
            for member in members:
                selected.add(tuple(int(value) for value in str(member["A"]).split(",")))  # type: ignore[arg-type]

    return sorted(selected)


def select_scope(
    scope: str,
    rows: Sequence[Mapping[str, object]],
    explicit: Sequence[Subset],
) -> List[Subset]:
    all_subsets: List[Subset] = list(itertools.combinations(range(2, 11), 4))  # type: ignore[assignment]
    if scope == "all":
        return all_subsets
    if scope == "explicit":
        if not explicit:
            raise ValueError("--scope explicit requires --subsets")
        return sorted(set(explicit))
    if not rows:
        raise ValueError(f"--scope {scope} requires --multi-prime-census")
    if scope == "defects":
        return sorted(
            tuple(int(value) for value in str(row["A"]).split(","))
            for row in rows
            if normalize_bool(row.get("characteristic_two_defect", False))
        )  # type: ignore[return-value]
    if scope == "frontier":
        return select_frontier(rows)
    raise ValueError(scope)


def nine_point_self_check(base, primes: Sequence[int], order_seed: int) -> Dict[str, object]:
    expected_distribution = {0: 4, 2: 3, 8: 3, 9: 6, 14: 6, 15: 13}
    by_field: Dict[int, Dict[str, object]] = {}
    overall = True
    started = time.time()
    for prime in primes:
        observed = Counter()
        structure = True
        for subset3 in itertools.combinations(range(2, 9), 3):
            outside, residue, metadata = base.build_reduced_channel(9, subset3)
            _c_rank, image_rank, outside_rows = paired_rank_prime(
                outside,
                residue,
                prime,
                order_seed,
                target_dimension=int(metadata["target_fibre_size"]),
            )
            observed[image_rank] += 1
            structure &= (
                metadata["target_preimage_min"] == 2
                and metadata["target_preimage_max"] == 2
                and outside_rows == metadata["outside_distinct_rows"]
            )
        passed = dict(sorted(observed.items())) == expected_distribution and structure
        overall &= passed
        by_field[prime] = {
            "passed": passed,
            "distribution": dict(sorted(observed.items())),
            "structure_checks_pass": structure,
        }
    return {
        "passed": overall,
        "fields": by_field,
        "elapsed_seconds": time.time() - started,
    }


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    script_path = Path(__file__).resolve()
    base_script = args.base_script.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    base = load_module(base_script, "ehf_amp_found_04c_t0_base_main")

    census_rows: List[Dict[str, str]] = []
    census_by_a: Dict[str, Dict[str, str]] = {}
    if args.multi_prime_census:
        census_rows = read_csv(args.multi_prime_census.resolve())
        census_by_a = {row["A"]: row for row in census_rows}

    requested = select_scope(args.scope, census_rows, args.subsets)
    if args.max_channels > 0:
        requested = requested[: args.max_channels]

    log_path = out_dir / "run.log"
    with log_path.open("a") as log_handle:
        original_stdout = sys.stdout
        sys.stdout = Tee(original_stdout, log_handle)
        try:
            print("=" * 132)
            print("EHF-AMP-FOUND-04C-T0: ODD-PRIME EXCEPTIONAL-PRIME / 2-PRIMARY TORSION PRECURSOR AUDIT")
            print("=" * 132)
            print(f"04A engine:                   {base_script}")
            print(f"04B census:                   {args.multi_prime_census.resolve() if args.multi_prime_census else 'not supplied'}")
            print(f"output directory:             {out_dir}")
            print(f"scope:                        {args.scope}")
            print(f"requested channels:           {len(requested)}")
            print(f"new odd primes:               {args.fields}")
            print(f"worker timeout:               {args.worker_timeout:.0f} s")
            print(f"order-seed retries:           {args.order_seeds}")
            print("claim status:                 finite exceptional-prime audit; not a torsion proof")

            self_check: Dict[str, object] = {
                "passed": True,
                "skipped": True,
                "fields": {},
                "elapsed_seconds": 0.0,
            }
            if not args.skip_nine_point_self_check:
                print("\nExact nine-point odd-prime engine self-check")
                self_check = nine_point_self_check(base, args.fields, args.order_seeds[0])
                for prime, result in self_check["fields"].items():
                    print(
                        f"  GF({prime}) recovered 03B distribution: {result['passed']} "
                        f"{result['distribution']}"
                    )
                print(f"  elapsed:                            {self_check['elapsed_seconds']:.2f}s")

            field_ledgers: Dict[int, Dict[str, Dict[str, object]]] = {}
            failure_rows: List[Dict[str, object]] = []
            for prime in args.fields:
                ledger_path = out_dir / f"channel_census_gf{prime}.csv"
                completed: Dict[str, Dict[str, object]] = {}
                if args.resume and ledger_path.exists():
                    for row in read_csv(ledger_path):
                        if str(row.get("status", "")) == "exact_modular":
                            completed[row["A"]] = dict(row)

                print(f"\nFull GF({prime}) requested-channel census")
                for ordinal, subset in enumerate(requested, start=1):
                    key = subset_text(subset)
                    if key in completed:
                        print(f"  [{ordinal:03d}/{len(requested):03d}] A={key:9s} resume")
                        continue
                    candidate = normalize_int(census_by_a.get(key, {}).get("generic_modular_rank"), -1)
                    result: Optional[Dict[str, object]] = None
                    errors: List[str] = []
                    for order_seed in args.order_seeds:
                        result, status = run_worker_subprocess(
                            script_path,
                            base_script,
                            subset,
                            prime,
                            order_seed,
                            args.worker_timeout,
                        )
                        if result is not None:
                            break
                        errors.append(f"seed={order_seed}:{status}")
                    if result is None:
                        row = {
                            "A": key,
                            "field": prime,
                            "status": "failed",
                            "candidate_generic_modular_rank": candidate,
                            "attempt_errors": " | ".join(errors),
                        }
                        failure_rows.append(row)
                        completed[key] = row
                        print(f"  [{ordinal:03d}/{len(requested):03d}] A={key:9s} FAILED {row['attempt_errors']}")
                    else:
                        rank = int(result["residue_rank"])
                        match = candidate is None or candidate < 0 or rank == candidate
                        row = {
                            "channel_index": list(itertools.combinations(range(2, 11), 4)).index(subset),
                            "A": key,
                            "a": subset[0],
                            "b": subset[1],
                            "c": subset[2],
                            "d": subset[3],
                            "field": prime,
                            "status": "exact_modular",
                            "C_rank": result["C_rank"],
                            "source_relation_dim": result["source_relation_dim"],
                            "residue_rank": rank,
                            "candidate_generic_modular_rank": candidate if candidate is not None else "",
                            "candidate_match": match,
                            "rank_delta_vs_candidate": rank - candidate if candidate is not None and candidate >= 0 else "",
                            "structure_checks_pass": result["structure_checks_pass"],
                            "source_fibre_size": result["source_fibre_size"],
                            "target_fibre_size": result["target_fibre_size"],
                            "active_source_columns": result["active_source_columns"],
                            "outside_distinct_rows": result["outside_distinct_rows"],
                            "order_seed": result["order_seed"],
                            "elapsed_seconds": f"{float(result['elapsed_seconds']):.6f}",
                            "attempt_errors": " | ".join(errors),
                        }
                        completed[key] = row
                        print(
                            f"  [{ordinal:03d}/{len(requested):03d}] A={key:9s} "
                            f"r={rank:3d} candidate={candidate if candidate is not None else -1:3d} "
                            f"match={match} {float(result['elapsed_seconds']):.2f}s"
                        )

                    ordered = sorted(completed.values(), key=lambda row: tuple(int(v) for v in str(row["A"]).split(",")))
                    write_csv(ledger_path, ordered)
                    write_csv(out_dir / "worker_failures.csv", failure_rows)

                field_ledgers[prime] = {
                    key: row
                    for key, row in completed.items()
                    if str(row.get("status", "")) == "exact_modular"
                }

            common_keys = [
                subset_text(subset)
                for subset in requested
                if all(subset_text(subset) in field_ledgers[prime] for prime in args.fields)
            ]
            combined_rows: List[Dict[str, object]] = []
            exceptional_rows: List[Dict[str, object]] = []
            for key in common_keys:
                source = census_by_a.get(key, {})
                subset = tuple(int(value) for value in key.split(","))
                candidate = normalize_int(source.get("generic_modular_rank"), -1)
                ranks = {prime: int(field_ledgers[prime][key]["residue_rank"]) for prime in args.fields}
                all_new_agree = len(set(ranks.values())) == 1
                candidate_agree = candidate is None or candidate < 0 or all(rank == candidate for rank in ranks.values())
                row: Dict[str, object] = {
                    "A": key,
                    "a": subset[0],
                    "b": subset[1],
                    "c": subset[2],
                    "d": subset[3],
                    "candidate_GF3_GF5_rank": candidate if candidate is not None else "",
                    "GF2_rank": source.get("GF2_residue_rank", ""),
                    "characteristic_two_defect": source.get("characteristic_two_defect", ""),
                    "boundary_correction": boundary_correction(subset),
                    "all_new_odd_primes_agree": all_new_agree,
                    "all_new_odd_primes_match_candidate": candidate_agree,
                }
                for prime, rank in ranks.items():
                    row[f"GF{prime}_rank"] = rank
                    row[f"GF{prime}_delta_vs_candidate"] = (
                        rank - candidate if candidate is not None and candidate >= 0 else ""
                    )
                combined_rows.append(row)
                if not candidate_agree or not all_new_agree:
                    exceptional_rows.append(row)

            write_csv(out_dir / "multi_odd_prime_audit.csv", combined_rows)
            write_csv(out_dir / "exceptional_prime_ledger.csv", exceptional_rows)

            distribution_rows: List[Dict[str, object]] = []
            for prime in args.fields:
                distribution = Counter(int(row["residue_rank"]) for row in field_ledgers[prime].values())
                for rank, count in sorted(distribution.items()):
                    distribution_rows.append({"field": prime, "rank": rank, "count": count})
            write_csv(out_dir / "rank_distribution_by_field.csv", distribution_rows)

            complete = len(common_keys) == len(requested)
            structure_pass = all(
                normalize_bool(field_ledgers[prime][key].get("structure_checks_pass", False))
                for prime in args.fields
                for key in common_keys
            ) if common_keys else False
            new_fields_agree = bool(combined_rows) and all(
                normalize_bool(row["all_new_odd_primes_agree"]) for row in combined_rows
            )
            candidate_available = bool(census_rows) and bool(combined_rows) and all(
                normalize_int(row.get("candidate_GF3_GF5_rank"), -1) is not None
                and int(str(row.get("candidate_GF3_GF5_rank", -1))) >= 0
                for row in combined_rows
            )
            candidate_agreement = candidate_available and all(
                normalize_bool(row["all_new_odd_primes_match_candidate"]) for row in combined_rows
            )

            if not complete:
                verdict = "EHF_AMP_FOUND_04C_T0_ODD_PRIME_AUDIT_INCOMPLETE"
            elif exceptional_rows:
                verdict = "EHF_AMP_FOUND_04C_T0_ADDITIONAL_ODD_PRIME_EXCEPTION_DETECTED"
            elif candidate_available:
                verdict = "EHF_AMP_FOUND_04C_T0_NO_ADDITIONAL_ODD_PRIME_EXCEPTION_FOUND"
            else:
                verdict = "EHF_AMP_FOUND_04C_T0_TESTED_ODD_PRIMES_MUTUALLY_AGREE"

            strict_failures: List[str] = []
            if not bool(self_check.get("passed", False)):
                strict_failures.append("nine_point_self_check_failed")
            if not complete:
                strict_failures.append("requested_census_incomplete")
            if failure_rows:
                strict_failures.append("worker_failures")
            if not structure_pass:
                strict_failures.append("structure_checks_failed")
            if args.require_candidate_agreement and not candidate_agreement:
                strict_failures.append("new_odd_prime_candidate_disagreement")

            summary = {
                "probe": "EHF-AMP-FOUND-04C-T0",
                "scope": args.scope,
                "requested_channel_count": len(requested),
                "completed_all_field_channel_count": len(common_keys),
                "fields": list(args.fields),
                "nine_point_self_check": self_check,
                "all_new_odd_primes_agree": new_fields_agree,
                "GF3_GF5_candidate_available": candidate_available,
                "all_new_odd_primes_match_GF3_GF5_candidate": candidate_agreement,
                "additional_odd_prime_exception_count": len(exceptional_rows),
                "worker_failure_count": len(failure_rows),
                "all_structure_checks_pass": structure_pass,
                "supports_2_primary_torsion_precursor_hypothesis": (
                    complete and candidate_available and candidate_agreement and not exceptional_rows
                ),
                "claim_boundary": (
                    "Finite-prime evidence only. Agreement over tested odd primes does not prove "
                    "that the integral saturation quotient is 2-primary."
                ),
                "verdict": verdict,
                "elapsed_seconds": time.time() - started,
                "strict_checks_pass": not strict_failures,
                "strict_failures": strict_failures,
                "output_files": [
                    "run.log",
                    *[f"channel_census_gf{prime}.csv" for prime in args.fields],
                    "multi_odd_prime_audit.csv",
                    "exceptional_prime_ledger.csv",
                    "rank_distribution_by_field.csv",
                    "worker_failures.csv",
                    "summary.json",
                    "verdict.json",
                ],
            }
            (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
            (out_dir / "verdict.json").write_text(json.dumps({"verdict": verdict}, indent=2))

            print("\n" + "=" * 132)
            print("FINAL SUMMARY")
            print("=" * 132)
            print(f"Completed all-field channels:         {len(common_keys)} / {len(requested)}")
            print(f"Tested odd primes:                    {args.fields}")
            print(f"New odd primes mutually agree:        {new_fields_agree}")
            print(f"GF(3)/GF(5) candidate available:      {candidate_available}")
            print(f"New odd primes match GF(3)/GF(5):     {candidate_agreement if candidate_available else 'not audited'}")
            print(f"Additional odd-prime exceptions:      {len(exceptional_rows)}")
            print(f"2-primary precursor supported:        {summary['supports_2_primary_torsion_precursor_hypothesis']}")
            print(f"Verdict:                              {verdict}")
            print(f"elapsed:                              {summary['elapsed_seconds']:.2f} seconds")
            if args.strict:
                print(f"strict checks:                        {'PASS' if not strict_failures else 'FAIL'}")
                if strict_failures:
                    print(f"failed checks:                        {', '.join(strict_failures)}")
            print("=" * 132)

            if args.strict and strict_failures:
                raise SystemExit(2)
            return summary
        finally:
            sys.stdout = original_stdout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-script", type=Path, required=True)
    parser.add_argument("--multi-prime-census", type=Path)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--fields", type=parse_fields, default=(7, 11, 13))
    parser.add_argument(
        "--scope",
        choices=("defects", "frontier", "all", "explicit"),
        default="frontier",
    )
    parser.add_argument("--subsets", type=parse_subsets, default=tuple())
    parser.add_argument("--worker-timeout", type=float, default=7200.0)
    parser.add_argument("--order-seeds", type=parse_int_tuple, default=(1, 2))
    parser.add_argument("--max-channels", type=int, default=0)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--skip-nine-point-self-check", action="store_true")
    parser.add_argument("--require-candidate-agreement", action="store_true")
    parser.add_argument("--strict", action="store_true")

    parser.add_argument("--internal-worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--internal-subset", default="", help=argparse.SUPPRESS)
    parser.add_argument("--internal-field", type=int, default=7, help=argparse.SUPPRESS)
    parser.add_argument("--internal-order-seed", type=int, default=1, help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.internal_worker:
        subset = tuple(int(part) for part in args.internal_subset.split(","))
        result = channel_worker({
            "base_script": str(args.base_script),
            "subset": subset,
            "field": args.internal_field,
            "order_seed": args.internal_order_seed,
        })
        print(json.dumps(result, sort_keys=True))
        return 0
    if args.out_dir is None:
        raise SystemExit("--out-dir is required")
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
