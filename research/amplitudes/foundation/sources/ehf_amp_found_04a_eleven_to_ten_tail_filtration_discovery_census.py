#!/usr/bin/env python3
r"""
EHF-AMP-FOUND-04A: Eleven-to-Ten Tail-Filtration Discovery Census
==================================================================

This is the first scaling probe beyond the completed nine-to-eight theorem.
It works in one canonical anchor-1, delete-11 chart; the 03K/03L covariance
results make repetition over anchors and deleted legs unnecessary at this
stage.

For A={a<b<c<d} subset {2,...,10}, the source and target fibres are

    F_A^(11): E={1,11} union A, O={2,...,10}\A,
    F_A^(10): E={1} union A,    O={2,...,10}\A.

There are C(9,4)=126 diagonal channels.  Each target fibre has 1440 states,
each source channel has 2880 active delete-11 columns, and every target state
has two active source preimages.

Direct exact QQ ranks at n=11 would require matrices with up to 362880 KK rows
and 14400 source columns.  04A therefore uses an exact finite-field reduction.
The 2880 active source columns are unit KK-basis columns.  After eliminating
them, write C_A for the inactive-column KK coordinates outside the active row
set and L_A for the induced target residue map.  Then, over any field,

    r_A = rank([C_A;L_A]) - rank(C_A)
        = rank( L_A restricted to ker(C_A) ).

The implementation performs paired bitset elimination: it reduces C_A while
carrying the L_A image, so a dependent C_A column immediately contributes a
candidate residue vector.  GF(2) gives the complete discovery census.  An
optional GF(3) audit tests one minimum-source-size representative of every
observed GF(2) rank class.

The probe first applies the same engine to all 35 known 9->8 channels and must
recover the exact rank law 0,2,8,9,14,15.  This validates the reduction and
bitset implementation, but the 11->10 output remains a modular discovery
result rather than an exact QQ theorem.
"""

from __future__ import annotations

import argparse
import csv
import gc
import itertools
import json
import math
import multiprocessing as mp
import os
import random
import signal
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Mapping, MutableMapping, Optional, Sequence, Tuple

Cycle = Tuple[int, ...]
Subset = Tuple[int, ...]
SparseColumn = Dict[Tuple[int, ...] | int, int]


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


def canon(cycle: Sequence[int]) -> Cycle:
    cycle = tuple(cycle)
    position = cycle.index(1)
    rep = cycle[position:] + cycle[:position]
    rev = (rep[0],) + rep[:0:-1]
    return rep if rep <= rev else rev


def shuffle_patterns(left_size: int, right_size: int) -> List[Tuple[int, ...]]:
    total = left_size + right_size
    return list(itertools.combinations(range(total), left_size))


def apply_shuffle_pattern(
    left: Sequence[int],
    right: Sequence[int],
    positions: Sequence[int],
) -> Tuple[int, ...]:
    position_set = set(positions)
    left_index = 0
    right_index = 0
    output: List[int] = []
    for index in range(len(left) + len(right)):
        if index in position_set:
            output.append(left[left_index])
            left_index += 1
        else:
            output.append(right[right_index])
            right_index += 1
    return tuple(output)


def interleave_source(
    even_permutation: Sequence[int],
    odd_permutation: Sequence[int],
) -> Cycle:
    output = [1]
    for odd_label, even_label in zip(odd_permutation, even_permutation):
        output.extend((odd_label, even_label))
    return tuple(output)


def interleave_target(
    even_permutation: Sequence[int],
    odd_permutation: Sequence[int],
) -> Cycle:
    output = [1]
    for index, even_label in enumerate(even_permutation):
        output.extend((odd_permutation[index], even_label))
    output.append(odd_permutation[-1])
    return tuple(output)


def generate_target_fibre(n_odd: int, subset: Subset) -> List[Cycle]:
    m = (n_odd - 1) // 2
    universe = set(range(2, n_odd))
    even_labels = tuple(subset)
    odd_labels = tuple(sorted(universe - set(subset)))
    output: List[Cycle] = []
    for even_permutation in itertools.permutations(even_labels):
        for odd_permutation in itertools.permutations(odd_labels):
            cycle = interleave_target(even_permutation, odd_permutation)
            if cycle[1] < cycle[-1]:
                output.append(cycle)
    return output


def generate_source_fibre(n_odd: int, subset: Subset) -> List[Cycle]:
    universe = set(range(2, n_odd))
    even_labels = tuple(sorted((n_odd,) + tuple(subset)))
    odd_labels = tuple(sorted(universe - set(subset)))
    output: List[Cycle] = []
    for even_permutation in itertools.permutations(even_labels):
        for odd_permutation in itertools.permutations(odd_labels):
            cycle = interleave_source(even_permutation, odd_permutation)
            if cycle[1] < cycle[-1]:
                output.append(cycle)
    return output


def inversion_count(n_odd: int, subset: Subset) -> int:
    complement = set(range(2, n_odd)) - set(subset)
    return sum(left > right for left in subset for right in complement)


def source_size_formula(n_odd: int, subset: Subset) -> int:
    m = (n_odd - 1) // 2
    return math.factorial(m - 1) ** 2 * (m + inversion_count(n_odd, subset))


def target_size_formula(n_odd: int) -> int:
    m = (n_odd - 1) // 2
    return math.factorial(m - 1) * math.factorial(m) // 2


def active_count_formula(n_odd: int) -> int:
    m = (n_odd - 1) // 2
    return math.factorial(m - 1) * math.factorial(m)


def gap_signature(n_odd: int, subset: Subset) -> Tuple[int, ...]:
    values = [subset[0] - 2]
    values.extend(subset[index + 1] - subset[index] - 1 for index in range(len(subset) - 1))
    values.append((n_odd - 1) - subset[-1])
    return tuple(values)


def build_reduced_channel(
    n_odd: int,
    subset: Subset,
) -> Tuple[List[Dict[Tuple[int, ...], int]], List[Dict[int, int]], Dict[str, object]]:
    target = generate_target_fibre(n_odd, subset)
    source = generate_source_fibre(n_odd, subset)
    target_index = {cycle: index for index, cycle in enumerate(target)}

    active_coordinate: Dict[Tuple[int, ...], Tuple[int, int]] = {}
    target_preimages = [0] * len(target)
    inactive: List[Cycle] = []

    for cycle in source:
        if cycle[-1] == n_odd:
            kk_coordinate = cycle[1:-1]
            image = canon(cycle[:-1])
            target_row = target_index[image]
            # The new maximal label lies immediately before anchor 1.
            residue_sign = -1
            active_coordinate[kk_coordinate] = (target_row, residue_sign)
            target_preimages[target_row] += 1
        else:
            inactive.append(cycle)

    patterns: Dict[Tuple[int, int], List[Tuple[int, ...]]] = {}
    outside_columns: List[Dict[Tuple[int, ...], int]] = []
    residue_columns: List[Dict[int, int]] = []
    outside_nonzeros = 0
    residue_nonzeros = 0

    for cycle in inactive:
        position = cycle.index(n_odd)
        alpha = cycle[1:position]
        beta_reversed = tuple(reversed(cycle[position + 1 :]))
        sign = -1 if len(beta_reversed) % 2 else 1
        pattern_key = (len(alpha), len(beta_reversed))
        if pattern_key not in patterns:
            patterns[pattern_key] = shuffle_patterns(*pattern_key)

        outside: Dict[Tuple[int, ...], int] = {}
        residue: Dict[int, int] = {}
        for pattern in patterns[pattern_key]:
            sigma = apply_shuffle_pattern(alpha, beta_reversed, pattern)
            active = active_coordinate.get(sigma)
            if active is None:
                outside[sigma] = outside.get(sigma, 0) + sign
            else:
                target_row, residue_sign = active
                residue[target_row] = residue.get(target_row, 0) + sign * residue_sign

        outside = {key: value for key, value in outside.items() if value}
        residue = {key: value for key, value in residue.items() if value}
        outside_columns.append(outside)
        residue_columns.append(residue)
        outside_nonzeros += len(outside)
        residue_nonzeros += len(residue)

    metadata = {
        "source_fibre_size": len(source),
        "source_fibre_size_formula": source_size_formula(n_odd, subset),
        "target_fibre_size": len(target),
        "target_fibre_size_formula": target_size_formula(n_odd),
        "active_source_columns": len(active_coordinate),
        "active_source_formula": active_count_formula(n_odd),
        "inactive_source_columns": len(inactive),
        "target_preimage_min": min(target_preimages),
        "target_preimage_max": max(target_preimages),
        "outside_nonzeros": outside_nonzeros,
        "residue_nonzeros": residue_nonzeros,
        "outside_distinct_rows": len({row for column in outside_columns for row in column}),
    }
    return outside_columns, residue_columns, metadata


def add_gf3(one_a: int, two_a: int, one_b: int, two_b: int) -> Tuple[int, int]:
    result_one = ((~(one_a | two_a)) & one_b) | (one_a & ~(one_b | two_b)) | (two_a & two_b)
    result_two = ((~(one_a | two_a)) & two_b) | (two_a & ~(one_b | two_b)) | (one_a & one_b)
    return result_one, result_two


def paired_rank_gf2(
    outside_columns: Sequence[Mapping[Tuple[int, ...], int]],
    residue_columns: Sequence[Mapping[int, int]],
    order_seed: int,
) -> Tuple[int, int, int]:
    rows = {row for column in outside_columns for row in column}
    ordered_rows = sorted(rows)
    random.Random(order_seed).shuffle(ordered_rows)
    row_index = {row: index for index, row in enumerate(ordered_rows)}
    column_order = list(range(len(outside_columns)))
    random.Random(order_seed + 1000003).shuffle(column_order)

    basis: Dict[int, Tuple[int, int]] = {}
    image_basis: Dict[int, int] = {}

    for column_index in column_order:
        vector = 0
        for row, value in outside_columns[column_index].items():
            if value & 1:
                vector ^= 1 << row_index[row]
        image = 0
        for row, value in residue_columns[column_index].items():
            if value & 1:
                image ^= 1 << row

        while vector:
            pivot = vector.bit_length() - 1
            stored = basis.get(pivot)
            if stored is None:
                basis[pivot] = (vector, image)
                break
            vector ^= stored[0]
            image ^= stored[1]

        if vector == 0 and image:
            while image:
                pivot = image.bit_length() - 1
                stored_image = image_basis.get(pivot)
                if stored_image is None:
                    image_basis[pivot] = image
                    break
                image ^= stored_image

    return len(basis), len(image_basis), len(ordered_rows)


def paired_rank_gf3(
    outside_columns: Sequence[Mapping[Tuple[int, ...], int]],
    residue_columns: Sequence[Mapping[int, int]],
    order_seed: int,
) -> Tuple[int, int, int]:
    rows = {row for column in outside_columns for row in column}
    ordered_rows = sorted(rows)
    random.Random(order_seed).shuffle(ordered_rows)
    row_index = {row: index for index, row in enumerate(ordered_rows)}
    # Natural column order is materially more stable for the GF(3) audit.
    column_order = range(len(outside_columns))

    basis: Dict[int, Tuple[int, int, int, int]] = {}
    image_basis: Dict[int, Tuple[int, int]] = {}

    for column_index in column_order:
        one = 0
        two = 0
        for row, value in outside_columns[column_index].items():
            residue = value % 3
            if residue:
                bit = 1 << row_index[row]
                if residue == 1:
                    one |= bit
                else:
                    two |= bit

        image_one = 0
        image_two = 0
        for row, value in residue_columns[column_index].items():
            residue = value % 3
            if residue:
                bit = 1 << row
                if residue == 1:
                    image_one |= bit
                else:
                    image_two |= bit

        while one | two:
            pivot = (one | two).bit_length() - 1
            bit = 1 << pivot
            stored = basis.get(pivot)
            if stored is None:
                if two & bit:
                    one, two = two, one
                    image_one, image_two = image_two, image_one
                basis[pivot] = (one, two, image_one, image_two)
                break
            stored_one, stored_two, stored_image_one, stored_image_two = stored
            if one & bit:
                one, two = add_gf3(one, two, stored_two, stored_one)
                image_one, image_two = add_gf3(
                    image_one, image_two, stored_image_two, stored_image_one
                )
            else:
                one, two = add_gf3(one, two, stored_one, stored_two)
                image_one, image_two = add_gf3(
                    image_one, image_two, stored_image_one, stored_image_two
                )

        if not (one | two) and (image_one | image_two):
            while image_one | image_two:
                pivot = (image_one | image_two).bit_length() - 1
                bit = 1 << pivot
                stored = image_basis.get(pivot)
                if stored is None:
                    if image_two & bit:
                        image_one, image_two = image_two, image_one
                    image_basis[pivot] = (image_one, image_two)
                    break
                stored_one, stored_two = stored
                if image_one & bit:
                    image_one, image_two = add_gf3(
                        image_one, image_two, stored_two, stored_one
                    )
                else:
                    image_one, image_two = add_gf3(
                        image_one, image_two, stored_one, stored_two
                    )

    return len(basis), len(image_basis), len(ordered_rows)


def build_target_kk_columns(n_odd: int, subset: Subset) -> List[Dict[Tuple[int, ...], int]]:
    endpoint = n_odd - 1
    target = generate_target_fibre(n_odd, subset)
    patterns: Dict[Tuple[int, int], List[Tuple[int, ...]]] = {}
    columns: List[Dict[Tuple[int, ...], int]] = []
    for cycle in target:
        position = cycle.index(endpoint)
        alpha = cycle[1:position]
        beta_reversed = tuple(reversed(cycle[position + 1 :]))
        sign = -1 if len(beta_reversed) % 2 else 1
        key = (len(alpha), len(beta_reversed))
        if key not in patterns:
            patterns[key] = shuffle_patterns(*key)
        column: Dict[Tuple[int, ...], int] = {}
        for pattern in patterns[key]:
            sigma = apply_shuffle_pattern(alpha, beta_reversed, pattern)
            column[sigma] = column.get(sigma, 0) + sign
        columns.append({row: value for row, value in column.items() if value})
    return columns


def ordinary_rank_gf2(columns: Sequence[Mapping[Tuple[int, ...], int]], order_seed: int) -> int:
    empty = [{} for _ in columns]
    rank, _, _ = paired_rank_gf2(columns, empty, order_seed)
    return rank


def ordinary_rank_gf3(columns: Sequence[Mapping[Tuple[int, ...], int]], order_seed: int) -> int:
    empty = [{} for _ in columns]
    rank, _, _ = paired_rank_gf3(columns, empty, order_seed)
    return rank


def channel_worker(payload: Mapping[str, object]) -> Dict[str, object]:
    n_odd = int(payload["n_odd"])
    subset = tuple(int(value) for value in payload["subset"])
    field = int(payload["field"])
    order_seed = int(payload["order_seed"])
    started = time.time()
    outside, residue, metadata = build_reduced_channel(n_odd, subset)
    if field == 2:
        c_rank, residue_rank, outside_rows = paired_rank_gf2(outside, residue, order_seed)
    elif field == 3:
        c_rank, residue_rank, outside_rows = paired_rank_gf3(outside, residue, order_seed)
    else:
        raise ValueError(f"Unsupported field GF({field})")
    source_relation_dim = len(outside) - c_rank
    result = {
        "n_odd": n_odd,
        "A": subset_text(subset),
        "subset": subset,
        "field": field,
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


def worker_entry(payload: Mapping[str, object], connection) -> None:
    try:
        connection.send(("ok", channel_worker(payload)))
    except BaseException as exc:
        connection.send(("error", f"{type(exc).__name__}: {exc}"))
    finally:
        connection.close()


def run_fresh_process(
    payload: Mapping[str, object],
    timeout_seconds: float,
) -> Tuple[Optional[Dict[str, object]], str]:
    context = mp.get_context("spawn")
    parent_connection, child_connection = context.Pipe(duplex=False)
    process = context.Process(target=worker_entry, args=(payload, child_connection))
    process.start()
    child_connection.close()
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join()
        parent_connection.close()
        return None, "timeout"
    if not parent_connection.poll(1.0):
        exit_code = process.exitcode
        parent_connection.close()
        return None, f"worker_exit_{exit_code}"
    status, value = parent_connection.recv()
    parent_connection.close()
    if status == "ok":
        return value, "ok"
    return None, str(value)




class RecyclingWorkerPool:
    def __init__(self, max_tasks_per_child: int):
        self.context = mp.get_context("spawn")
        self.max_tasks_per_child = max(1, int(max_tasks_per_child))
        self.pool = None
        self._start()

    def _start(self) -> None:
        self.pool = self.context.Pool(
            processes=1,
            maxtasksperchild=self.max_tasks_per_child,
        )

    def _restart(self) -> None:
        if self.pool is not None:
            self.pool.terminate()
            self.pool.join()
        self._start()

    def run(
        self, payload: Mapping[str, object], timeout_seconds: float
    ) -> Tuple[Optional[Dict[str, object]], str]:
        assert self.pool is not None
        result = self.pool.apply_async(channel_worker, (payload,))
        try:
            return result.get(timeout_seconds), "ok"
        except mp.TimeoutError:
            self._restart()
            return None, "timeout"
        except BaseException as exc:
            self._restart()
            return None, f"{type(exc).__name__}: {exc}"

    def close(self) -> None:
        if self.pool is not None:
            self.pool.close()
            self.pool.join()
            self.pool = None


def run_timed_worker(
    payload: Mapping[str, object],
    timeout_seconds: float,
) -> Tuple[Optional[Dict[str, object]], str]:
    if not hasattr(signal, "SIGALRM"):
        return run_subprocess_worker(payload, timeout_seconds)

    def alarm_handler(signum, frame):
        raise TimeoutError("channel timeout")

    previous = signal.signal(signal.SIGALRM, alarm_handler)
    signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
    try:
        return channel_worker(payload), "ok"
    except TimeoutError:
        return None, "timeout"
    except BaseException as exc:
        return None, f"{type(exc).__name__}: {exc}"
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, previous)
        gc.collect()


def run_subprocess_worker(
    payload: Mapping[str, object],
    timeout_seconds: float,
) -> Tuple[Optional[Dict[str, object]], str]:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--internal-worker",
        "--internal-n-odd", str(payload["n_odd"]),
        "--internal-subset", subset_text(payload["subset"]),
        "--internal-field", str(payload["field"]),
        "--internal-order-seed", str(payload["order_seed"]),
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
        return None, f"worker_exit_{completed.returncode}: {message[-500:]}"
    try:
        return json.loads(completed.stdout.strip().splitlines()[-1]), "ok"
    except Exception as exc:
        return None, f"worker_json_error: {exc}: {completed.stdout[-500:]}"


def known_rank_9(subset: Subset) -> int:
    _, b, c = subset
    if b >= 6:
        return 15
    if b == 5:
        return 8 if c == 6 else 14
    if c <= 5:
        return 0
    if c == 6:
        return 2
    return 9


def read_existing_rows(path: Path) -> Dict[str, Dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return {}
    with path.open(newline="") as handle:
        return {row["A"]: row for row in csv.DictReader(handle)}


def tail_width_audit(rows: Sequence[Mapping[str, object]]) -> Tuple[List[Dict[str, object]], Optional[int]]:
    output: List[Dict[str, object]] = []
    minimal = None
    subset_size = len(tuple(rows[0]["subset"])) if rows else 0
    for width in range(1, subset_size + 1):
        groups: MutableMapping[Tuple[int, ...], List[int]] = defaultdict(list)
        for row in rows:
            subset = tuple(row["subset"])
            groups[subset[-width:]].append(int(row["residue_rank"]))
        bad = {key: sorted(set(values)) for key, values in groups.items() if len(set(values)) > 1}
        constant = not bad
        if constant and minimal is None:
            minimal = width
        output.append({
            "tail_width": width,
            "group_count": len(groups),
            "rank_constant_within_all_groups": constant,
            "nonconstant_group_count": len(bad),
            "nonconstant_examples": ";".join(
                f"{subset_text(key)}:{','.join(map(str, values))}"
                for key, values in list(sorted(bad.items()))[:20]
            ),
        })
    return output, minimal


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 124)
    print("EHF-AMP-FOUND-04A: ELEVEN-TO-TEN TAIL-FILTRATION DISCOVERY CENSUS")
    print("=" * 124)
    print(f"output directory:             {out_dir}")
    print("reference chart:              anchor 1, delete 11")
    print("source channels:              126")
    print("primary field:                GF(2)")
    print(f"GF(3) audit policy:           {args.gf3_audit}")
    print("claim status:                 modular discovery, not exact QQ theorem")

    # ------------------------------------------------------------------
    # Mandatory 9->8 self-check.
    # ------------------------------------------------------------------
    self_check_rows: List[Dict[str, object]] = []
    self_check_pass = True
    if not args.skip_nine_point_self_check:
        print("\nNine-point engine self-check")
        for index, subset in enumerate(itertools.combinations(range(2, 9), 3), start=1):
            result = channel_worker({
                "n_odd": 9,
                "subset": subset,
                "field": 2,
                "order_seed": args.order_seed,
            })
            expected = known_rank_9(subset)
            match = int(result["residue_rank"]) == expected
            self_check_pass &= match and bool(result["structure_checks_pass"])
            self_check_rows.append({
                "A": subset_text(subset),
                "expected_exact_rank": expected,
                "GF2_residue_rank": result["residue_rank"],
                "match": match,
                "structure_checks_pass": result["structure_checks_pass"],
            })
        print(f"  all 35 known ranks recovered:       {self_check_pass}")
    write_csv(out_dir / "nine_point_engine_self_check.csv", self_check_rows)

    # Target relation dimension in the reference n=10 fibre.
    reference_subset = (2, 3, 4, 5)
    target_columns = build_target_kk_columns(11, reference_subset)
    target_rank_gf2 = ordinary_rank_gf2(target_columns, args.order_seed)
    target_relation_dim_gf2 = len(target_columns) - target_rank_gf2
    print("\nReference n=10 target fibre")
    print(f"  target states:                       {len(target_columns)}")
    print(f"  GF(2) relation dimension:            {target_relation_dim_gf2}")

    all_subsets = list(itertools.combinations(range(2, 11), 4))
    if args.subset:
        requested = []
        for text in args.subset:
            subset = tuple(map(int, text.split(",")))
            if subset not in all_subsets:
                raise ValueError(f"Invalid four-subset: {text}")
            requested.append(subset)
    else:
        requested = all_subsets[args.start_index :]
        if args.max_channels:
            requested = requested[: args.max_channels]

    ledger_path = out_dir / "channel_census_gf2.csv"
    existing = read_existing_rows(ledger_path) if args.resume else {}
    completed_rows: Dict[str, Dict[str, object]] = {}
    for key, row in existing.items():
        completed_rows[key] = dict(row)

    print("\nGF(2) eleven-to-ten channel census")
    failures: List[Dict[str, object]] = []
    for ordinal, subset in enumerate(requested, start=1):
        key = subset_text(subset)
        if key in completed_rows:
            print(f"  [{ordinal:03d}/{len(requested):03d}] A={key:9s} resume")
            continue
        result = None
        status = "not_run"
        for retry, seed in enumerate(args.retry_order_seeds, start=1):
            payload = {
                "n_odd": 11,
                "subset": subset,
                "field": 2,
                "order_seed": seed,
            }
            result, status = run_subprocess_worker(payload, args.channel_timeout)
            if result is not None:
                break
        if result is None:
            failures.append({"A": key, "stage": "GF2", "status": status})
            print(f"  [{ordinal:03d}/{len(requested):03d}] A={key:9s} FAILED {status}")
            continue

        gaps = gap_signature(11, subset)
        row: Dict[str, object] = {
            "channel_index": all_subsets.index(subset),
            "A": key,
            "a": subset[0],
            "b": subset[1],
            "c": subset[2],
            "d": subset[3],
            "last_1": str(subset[-1]),
            "last_2": subset_text(subset[-2:]),
            "last_3": subset_text(subset[-3:]),
            "subset_word": "".join("1" if value in subset else "0" for value in range(2, 11)),
            "inversion_count": inversion_count(11, subset),
            "gap_signature": "-".join(map(str, gaps)),
            "source_fibre_size": result["source_fibre_size"],
            "inactive_source_columns": result["inactive_source_columns"],
            "GF2_C_rank": result["C_rank"],
            "GF2_source_relation_dim": result["source_relation_dim"],
            "GF2_residue_rank": result["residue_rank"],
            "residue_rank": result["residue_rank"],
            "GF2_target_relation_dim": target_relation_dim_gf2,
            "GF2_target_missing_dim": target_relation_dim_gf2 - int(result["residue_rank"]),
            "GF2_complete_target_recovery": int(result["residue_rank"]) == target_relation_dim_gf2,
            "active_source_columns": result["active_source_columns"],
            "target_fibre_size": result["target_fibre_size"],
            "target_preimage_min": result["target_preimage_min"],
            "target_preimage_max": result["target_preimage_max"],
            "outside_distinct_rows": result["outside_distinct_rows"],
            "outside_nonzeros": result["outside_nonzeros"],
            "residue_nonzeros": result["residue_nonzeros"],
            "structure_checks_pass": result["structure_checks_pass"],
            "order_seed": result["order_seed"],
            "elapsed_seconds": f"{float(result['elapsed_seconds']):.6f}",
        }
        completed_rows[key] = row
        ordered_for_write = [completed_rows[subset_text(item)] for item in all_subsets if subset_text(item) in completed_rows]
        write_csv(ledger_path, ordered_for_write)
        print(
            f"  [{ordinal:03d}/{len(requested):03d}] A={key:9s} "
            f"inv={row['inversion_count']:2d} r={row['GF2_residue_rank']:4d} "
            f"source={row['source_fibre_size']:5d} "
            f"{float(result['elapsed_seconds']):6.2f}s"
        )

    rows = [completed_rows[subset_text(item)] for item in all_subsets if subset_text(item) in completed_rows]
    # Normalize resumed CSV strings.
    normalized_rows: List[Dict[str, object]] = []
    for row in rows:
        subset = tuple(map(int, str(row["A"]).split(",")))
        normalized = dict(row)
        normalized["subset"] = subset
        normalized["residue_rank"] = int(row.get("GF2_residue_rank", row["residue_rank"]))
        normalized["inversion_count"] = int(row["inversion_count"])
        normalized["source_fibre_size"] = int(row["source_fibre_size"])
        normalized["structure_checks_pass"] = str(row["structure_checks_pass"]).lower() in ("true", "1")
        normalized_rows.append(normalized)

    tail_rows: List[Dict[str, object]] = []
    minimal_tail_width = None
    if normalized_rows:
        tail_rows, minimal_tail_width = tail_width_audit(normalized_rows)
    write_csv(out_dir / "tail_width_audit.csv", tail_rows)

    rank_counts = Counter(int(row["residue_rank"]) for row in normalized_rows)
    rank_distribution_rows = [
        {
            "GF2_residue_rank": rank,
            "channel_count": count,
            "rank_contribution": rank * count,
            "target_relation_dim_GF2": target_relation_dim_gf2,
            "complete_target_recovery": rank == target_relation_dim_gf2,
        }
        for rank, count in sorted(rank_counts.items())
    ]
    write_csv(out_dir / "rank_distribution_gf2.csv", rank_distribution_rows)

    # Tables grouped by the last two and last three selected labels.
    group_rows: List[Dict[str, object]] = []
    for width in (1, 2, 3, 4):
        groups: MutableMapping[Tuple[int, ...], List[Mapping[str, object]]] = defaultdict(list)
        for row in normalized_rows:
            groups[tuple(row["subset"])[-width:]].append(row)
        for tail, members in sorted(groups.items()):
            ranks = sorted({int(member["residue_rank"]) for member in members})
            group_rows.append({
                "tail_width": width,
                "tail": subset_text(tail),
                "channel_count": len(members),
                "rank_values": ";".join(map(str, ranks)),
                "rank_constant": len(ranks) == 1,
                "minimum_inversion_count": min(int(member["inversion_count"]) for member in members),
                "subsets": ";".join(str(member["A"]) for member in members),
            })
    write_csv(out_dir / "tail_signature_table.csv", group_rows)

    # Optional GF(3) representative audit.
    gf3_rows: List[Dict[str, object]] = []
    if args.gf3_audit != "none" and normalized_rows:
        if args.gf3_audit == "all":
            audit_members = normalized_rows
        else:
            representatives: Dict[int, Mapping[str, object]] = {}
            for row in normalized_rows:
                rank = int(row["residue_rank"])
                current = representatives.get(rank)
                key = (int(row["source_fibre_size"]), int(row["inversion_count"]), str(row["A"]))
                if current is None or key < (
                    int(current["source_fibre_size"]),
                    int(current["inversion_count"]),
                    str(current["A"]),
                ):
                    representatives[rank] = row
            audit_members = [representatives[key] for key in sorted(representatives)]
            if args.gf3_max_representatives:
                audit_members = audit_members[: args.gf3_max_representatives]

        print("\nGF(3) representative audit")
        for ordinal, row in enumerate(audit_members, start=1):
            subset = tuple(row["subset"])
            result = None
            status = "not_run"
            for seed in args.retry_order_seeds:
                result, status = run_subprocess_worker(
                    {"n_odd": 11, "subset": subset, "field": 3, "order_seed": seed},
                    args.gf3_timeout,
                )
                if result is not None:
                    break
            agreement = result is not None and int(result["residue_rank"]) == int(row["residue_rank"])
            gf3_rows.append({
                "A": row["A"],
                "GF2_residue_rank": row["residue_rank"],
                "GF3_residue_rank": "" if result is None else result["residue_rank"],
                "GF2_GF3_agree": agreement,
                "status": status,
                "GF3_elapsed_seconds": "" if result is None else f"{float(result['elapsed_seconds']):.6f}",
            })
            print(
                f"  [{ordinal:02d}/{len(audit_members):02d}] A={row['A']:9s} "
                f"GF2={row['residue_rank']} GF3={gf3_rows[-1]['GF3_residue_rank'] or status} "
                f"agree={agreement}"
            )
    write_csv(out_dir / "gf3_representative_audit.csv", gf3_rows)
    gf3_completed = sum(bool(str(row["GF3_residue_rank"])) for row in gf3_rows)
    gf3_all_completed_agree = bool(gf3_rows) and all(
        bool(row["GF2_GF3_agree"]) for row in gf3_rows if str(row["GF3_residue_rank"])
    ) and gf3_completed == len(gf3_rows)

    full_census = len(normalized_rows) == 126
    all_structure = bool(normalized_rows) and all(bool(row["structure_checks_pass"]) for row in normalized_rows)
    census_complete = full_census and not failures
    if census_complete and minimal_tail_width is not None:
        verdict = "EHF_AMP_FOUND_04A_ELEVEN_TO_TEN_MODULAR_TAIL_LAW_CANDIDATE_FOUND"
    elif census_complete:
        verdict = "EHF_AMP_FOUND_04A_ELEVEN_TO_TEN_MODULAR_DISCOVERY_CENSUS_COMPLETE"
    else:
        verdict = "EHF_AMP_FOUND_04A_PARTIAL_DISCOVERY_CENSUS"

    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "claim_status": "finite-field discovery; not an exact QQ theorem",
        "nine_point_self_check_pass": self_check_pass,
        "n10_reference_target_state_count": len(target_columns),
        "n10_reference_target_relation_dimension_GF2": target_relation_dim_gf2,
        "requested_channel_count": len(requested),
        "completed_unique_channel_count": len(normalized_rows),
        "full_126_channel_census": full_census,
        "all_structure_checks_pass": all_structure,
        "GF2_rank_distribution": dict(sorted(rank_counts.items())),
        "GF2_total_rank": sum(int(row["residue_rank"]) for row in normalized_rows),
        "GF2_complete_target_count": rank_counts.get(target_relation_dim_gf2, 0),
        "minimal_constant_tail_width": minimal_tail_width,
        "GF3_audit_row_count": len(gf3_rows),
        "GF3_completed_count": gf3_completed,
        "GF3_all_completed_agree": gf3_all_completed_agree,
        "failure_count": len(failures),
        "failures": failures,
        "elapsed_seconds": time.time() - started,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "nine_point_engine_self_check.csv",
            "channel_census_gf2.csv",
            "rank_distribution_gf2.csv",
            "tail_width_audit.csv",
            "tail_signature_table.csv",
            "gf3_representative_audit.csv",
        ],
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    (out_dir / "verdict.json").write_text(json.dumps({
        "verdict": verdict,
        "full_126_channel_census": full_census,
        "minimal_constant_tail_width": minimal_tail_width,
        "claim_status": summary["claim_status"],
    }, indent=2))

    strict_failures = []
    if args.strict:
        if not self_check_pass:
            strict_failures.append("nine_point_self_check")
        if not normalized_rows:
            strict_failures.append("no_eleven_point_channels")
        if not all_structure:
            strict_failures.append("structure_checks")
        if len(requested) == 126 and not census_complete:
            strict_failures.append("full_census_incomplete")
        if args.require_gf3 and not gf3_all_completed_agree:
            strict_failures.append("GF3_audit")

    print("\n" + "=" * 124)
    print("FINAL SUMMARY")
    print("=" * 124)
    print(f"Nine-point self-check:                {self_check_pass}")
    print(f"Completed n=11 channels:              {len(normalized_rows)} / 126")
    print(f"All structure checks:                 {all_structure}")
    print(f"Reference target relation dim GF(2):  {target_relation_dim_gf2}")
    print(f"Observed GF(2) rank classes:          {len(rank_counts)}")
    print(f"Minimal constant tail width:          {minimal_tail_width}")
    print(f"GF(3) completed/agreed:               {gf3_completed}/{len(gf3_rows)}; {gf3_all_completed_agree}")
    print(f"Verdict:                              {verdict}")
    print(f"elapsed:                              {time.time() - started:.2f} seconds")
    print(f"summary:                              {out_dir / 'summary.json'}")
    if args.strict:
        print(f"strict checks:                        {'PASS' if not strict_failures else 'FAIL'}")
        if strict_failures:
            print(f"failed checks:                        {', '.join(strict_failures)}")
    print("=" * 124)

    if strict_failures:
        raise SystemExit(2)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Modular 11->10 diagonal-channel and ordered-tail discovery census."
    )
    parser.add_argument("--out-dir", default="")
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--max-channels", type=int, default=0)
    parser.add_argument("--subset", action="append", help="Run a specific A, e.g. 2,3,4,10")
    parser.add_argument("--order-seed", type=int, default=1)
    parser.add_argument(
        "--retry-order-seeds",
        type=lambda text: tuple(map(int, text.split(","))),
        default=(1, 2, 3),
    )
    parser.add_argument("--channel-timeout", type=float, default=20.0)
    parser.add_argument("--gf3-timeout", type=float, default=180.0)
    parser.add_argument(
        "--gf3-audit",
        choices=("none", "representatives", "all"),
        default="representatives",
    )
    parser.add_argument("--gf3-max-representatives", type=int, default=0)
    parser.add_argument("--require-gf3", action="store_true")
    parser.add_argument("--skip-nine-point-self-check", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--internal-worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--internal-n-odd", type=int, default=11, help=argparse.SUPPRESS)
    parser.add_argument("--internal-subset", default="", help=argparse.SUPPRESS)
    parser.add_argument("--internal-field", type=int, default=2, help=argparse.SUPPRESS)
    parser.add_argument("--internal-order-seed", type=int, default=1, help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.internal_worker:
        if not args.internal_subset:
            raise SystemExit("--internal-subset is required")
        subset = tuple(map(int, args.internal_subset.split(",")))
        result = channel_worker({
            "n_odd": args.internal_n_odd,
            "subset": subset,
            "field": args.internal_field,
            "order_seed": args.internal_order_seed,
        })
        print(json.dumps(result, separators=(",", ":")))
        return 0
    if not args.out_dir:
        raise SystemExit("--out-dir is required")
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
