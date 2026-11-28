#!/usr/bin/env python3
r"""
EHF-AMP-FOUND-04C: Exact Rational Rank Certificate Sweep
=========================================================

04B established a complete 126-channel GF(2)/GF(3)/GF(5) census for the
canonical anchor-1, delete-11 chart.  GF(3) and GF(5) agreed everywhere, the
boundary-corrected three-tail law survived, and 34 channels were already
certified exactly over QQ by source/target saturation bounds.

04C attacks the remaining rational-rank problem directly.

For A={a<b<c<d} subset {2,...,10}, 04A constructs integer matrices C_A and
L_A such that over every field K

    r_A(K) = rank_K([C_A; L_A]) - rank_K(C_A).

04C builds those sparse integer matrices and asks SymPy's exact DomainMatrix
engine for both ranks over QQ.  Each completed worker therefore supplies a
literal exact certificate:

    r_A(QQ) = rank_QQ([C_A;L_A]) - rank_QQ(C_A).

The workers run in isolated subprocesses with timeouts and CSV checkpointing.
The sweep is ordered from the smallest unresolved channels upward and can be
resumed safely.  It supports three scopes:

    frontier         one representative per unresolved structural class;
    unresolved       every channel not already exact in 04B;
    all               all 126 channels, including independent rechecks;
    explicit          only --subsets entries.

A partial run is scientifically useful: every completed row is exact over QQ.
The theorem verdict is issued only when all 126 channels are exact and the
rational ranks satisfy the boundary-corrected three-tail law.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_04c_exact_rational_rank_certificate_sweep.py \
  --base-script scripts/ehf_amp_found_04a_eleven_to_ten_tail_filtration_discovery_census.py \
  --multi-prime-census runs/ehf_amp_found_04b/multi_prime_channel_census.csv \
  --out-dir runs/ehf_amp_found_04c \
  --scope unresolved \
  --worker-timeout 3600 \
  --column-orders natural,nnz_asc,nnz_desc \
  --resume \
  --strict
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import itertools
import json
import os
import resource
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

Subset = Tuple[int, int, int, int]


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


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def subset_text(subset: Sequence[int]) -> str:
    return ",".join(map(str, subset))


def parse_subsets(text: str) -> Tuple[Subset, ...]:
    if not text.strip():
        return tuple()
    output: List[Subset] = []
    for block in text.split(";"):
        values = tuple(int(value) for value in block.split(",") if value.strip())
        if len(values) != 4 or tuple(sorted(values)) != values:
            raise argparse.ArgumentTypeError(
                f"Invalid four-subset {block!r}; use a,b,c,d;..."
            )
        if min(values) < 2 or max(values) > 10:
            raise argparse.ArgumentTypeError(f"Subset out of range: {block!r}")
        output.append(values)  # type: ignore[arg-type]
    return tuple(output)


def parse_orders(text: str) -> Tuple[str, ...]:
    allowed = {"natural", "nnz_asc", "nnz_desc"}
    orders = tuple(value.strip() for value in text.split(",") if value.strip())
    if not orders:
        raise argparse.ArgumentTypeError("At least one column order is required")
    unknown = set(orders) - allowed
    if unknown:
        raise argparse.ArgumentTypeError(f"Unsupported column orders: {sorted(unknown)}")
    return orders


def normalize_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def normalize_int(value: object, default: Optional[int] = None) -> Optional[int]:
    text = str(value).strip()
    if text == "":
        return default
    return int(float(text))


def reorder_columns(outside, residue, order: str):
    indices = list(range(len(outside)))
    if order == "nnz_asc":
        indices.sort(key=lambda index: (len(outside[index]) + len(residue[index]), index))
    elif order == "nnz_desc":
        indices.sort(key=lambda index: (-(len(outside[index]) + len(residue[index])), index))
    elif order != "natural":
        raise ValueError(order)
    return [outside[index] for index in indices], [residue[index] for index in indices]


def build_domain_matrices(base, subset: Subset, column_order: str):
    from sympy.polys.matrices import DomainMatrix

    outside, residue, metadata = base.build_reduced_channel(11, subset)
    outside, residue = reorder_columns(outside, residue, column_order)
    column_count = len(outside)

    outside_rows = sorted({row for column in outside for row in column})
    outside_index = {row: index for index, row in enumerate(outside_rows)}

    c_dict: Dict[int, Dict[int, int]] = {}
    for column_index, column in enumerate(outside):
        for row, value in column.items():
            row_index = outside_index[row]
            c_dict.setdefault(row_index, {})[column_index] = int(value)

    c_matrix = DomainMatrix.from_dict_sympy(
        len(outside_rows), column_count, c_dict
    ).to_field()

    stacked_dict: Dict[int, Dict[int, int]] = {
        row: dict(values) for row, values in c_dict.items()
    }
    target_offset = len(outside_rows)
    for column_index, column in enumerate(residue):
        for row, value in column.items():
            stacked_dict.setdefault(target_offset + int(row), {})[column_index] = int(value)

    stacked_matrix = DomainMatrix.from_dict_sympy(
        len(outside_rows) + int(metadata["target_fibre_size"]),
        column_count,
        stacked_dict,
    ).to_field()

    return c_matrix, stacked_matrix, metadata


def exact_channel_worker(payload: Mapping[str, object]) -> Dict[str, object]:
    base_script = Path(str(payload["base_script"])).resolve()
    subset = tuple(int(value) for value in payload["subset"])
    column_order = str(payload["column_order"])
    candidate_rank = int(payload.get("candidate_rank", -1))
    base = load_module(base_script, f"ehf_amp_found_04c_base_{os.getpid()}")

    started = time.time()
    c_matrix, stacked_matrix, metadata = build_domain_matrices(
        base, subset, column_order
    )
    built_seconds = time.time() - started

    c_started = time.time()
    c_rank = int(c_matrix.rank())
    c_seconds = time.time() - c_started

    m_started = time.time()
    stacked_rank = int(stacked_matrix.rank())
    stacked_seconds = time.time() - m_started

    residue_rank = stacked_rank - c_rank
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    return {
        "A": subset_text(subset),
        "subset": subset,
        "column_order": column_order,
        "inactive_source_columns": int(metadata["inactive_source_columns"]),
        "outside_distinct_rows": int(metadata["outside_distinct_rows"]),
        "target_fibre_size": int(metadata["target_fibre_size"]),
        "QQ_C_rank": c_rank,
        "QQ_stacked_rank": stacked_rank,
        "QQ_residue_rank": residue_rank,
        "candidate_generic_modular_rank": candidate_rank,
        "candidate_match": candidate_rank < 0 or residue_rank == candidate_rank,
        "build_seconds": built_seconds,
        "C_rank_seconds": c_seconds,
        "stacked_rank_seconds": stacked_seconds,
        "elapsed_seconds": time.time() - started,
        "peak_rss_raw": int(peak_rss),
        "structure_checks_pass": (
            int(metadata["source_fibre_size"])
            == int(metadata["source_fibre_size_formula"])
            and int(metadata["target_fibre_size"])
            == int(metadata["target_fibre_size_formula"])
            and int(metadata["active_source_columns"])
            == int(metadata["active_source_formula"])
            and int(metadata["target_preimage_min"]) == 2
            and int(metadata["target_preimage_max"]) == 2
        ),
    }


def run_worker_subprocess(
    script_path: Path,
    base_script: Path,
    subset: Subset,
    candidate_rank: int,
    column_order: str,
    timeout_seconds: float,
) -> Tuple[Optional[Dict[str, object]], str]:
    command = [
        sys.executable,
        str(script_path),
        "--internal-worker",
        "--base-script",
        str(base_script),
        "--out-dir",
        str(script_path.parent / ".ehf_amp_found_04c_internal"),
        "--internal-subset",
        subset_text(subset),
        "--internal-candidate-rank",
        str(candidate_rank),
        "--internal-column-order",
        column_order,
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
        result = json.loads(completed.stdout.strip().splitlines()[-1])
        return result, "ok"
    except Exception as exc:
        return None, f"worker_json_error: {exc}: {completed.stdout[-1000:]}"


def exact_nine_point_self_check(base) -> Dict[str, object]:
    from sympy.polys.matrices import DomainMatrix

    expected = Counter({0: 4, 2: 3, 8: 3, 9: 6, 14: 6, 15: 13})
    observed: Counter[int] = Counter()
    failures: List[Dict[str, object]] = []
    started = time.time()

    for subset in itertools.combinations(range(2, 9), 3):
        outside, residue, metadata = base.build_reduced_channel(9, subset)
        outside_rows = sorted({row for column in outside for row in column})
        outside_index = {row: index for index, row in enumerate(outside_rows)}
        c_dict: Dict[int, Dict[int, int]] = {}
        for column_index, column in enumerate(outside):
            for row, value in column.items():
                c_dict.setdefault(outside_index[row], {})[column_index] = int(value)
        c_matrix = DomainMatrix.from_dict_sympy(
            len(outside_rows), len(outside), c_dict
        ).to_field()
        stacked = {row: dict(values) for row, values in c_dict.items()}
        offset = len(outside_rows)
        for column_index, column in enumerate(residue):
            for row, value in column.items():
                stacked.setdefault(offset + int(row), {})[column_index] = int(value)
        m_matrix = DomainMatrix.from_dict_sympy(
            len(outside_rows) + int(metadata["target_fibre_size"]),
            len(outside),
            stacked,
        ).to_field()
        rank = int(m_matrix.rank()) - int(c_matrix.rank())
        observed[rank] += 1

    passed = observed == expected
    if not passed:
        failures.append({"expected": dict(expected), "observed": dict(observed)})
    return {
        "passed": passed,
        "expected_distribution": dict(sorted(expected.items())),
        "observed_distribution": dict(sorted(observed.items())),
        "elapsed_seconds": time.time() - started,
        "failures": failures,
    }


def boundary_correction(subset: Subset) -> int:
    a, b, _c, d = subset
    return int(d == 10 and b in {5, 6} and a >= 4)


def boundary_law_audit(rows: Sequence[Mapping[str, object]], rank_key: str) -> Dict[str, object]:
    grouped: MutableMapping[Tuple[int, int, int], List[Tuple[int, int]]] = defaultdict(list)
    for row in rows:
        subset = tuple(int(value) for value in str(row["A"]).split(","))
        rank_value = normalize_int(row.get(rank_key))
        if rank_value is None:
            continue
        grouped[subset[-3:]].append((subset[0], rank_value))

    tested = 0
    failures: List[Dict[str, object]] = []
    for tail, values in sorted(grouped.items()):
        baseline = min(rank for _a, rank in values)
        for a, rank in values:
            subset = (a,) + tail
            predicted = baseline + boundary_correction(subset)  # type: ignore[arg-type]
            tested += 1
            if rank != predicted:
                failures.append({
                    "A": subset_text(subset),
                    "tail": subset_text(tail),
                    "rank": rank,
                    "baseline": baseline,
                    "predicted": predicted,
                })
    return {
        "tested_channels": tested,
        "complete_tail_classes": len(grouped),
        "passed_on_available_rows": tested > 0 and not failures,
        "failure_count": len(failures),
        "failures": failures,
    }


def select_frontier(rows: Sequence[Mapping[str, object]]) -> List[Subset]:
    classes: Dict[Tuple[int, int, int, int], Tuple[Subset, int]] = {}
    for row in rows:
        if normalize_bool(row.get("rational_rank_exact_certified", False)):
            continue
        subset = tuple(int(value) for value in str(row["A"]).split(","))
        generic = int(str(row["generic_modular_rank"]))
        source_upper = int(str(row["rational_source_dimension_upper_bound"]))
        boundary = boundary_correction(subset)  # type: ignore[arg-type]
        key = (generic, source_upper, subset[-1], boundary)
        complexity = int(str(row.get("source_fibre_size", 10**9)))
        current = classes.get(key)
        if current is None or complexity < current[1]:
            classes[key] = (subset, complexity)  # type: ignore[assignment]
    return sorted((value[0] for value in classes.values()), key=lambda s: s)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-script", type=Path, required=True)
    parser.add_argument("--multi-prime-census", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument(
        "--scope",
        choices=("frontier", "unresolved", "all", "explicit"),
        default="frontier",
    )
    parser.add_argument("--subsets", type=parse_subsets, default=tuple())
    parser.add_argument("--worker-timeout", type=float, default=3600.0)
    parser.add_argument(
        "--column-orders", type=parse_orders, default=("natural", "nnz_asc", "nnz_desc")
    )
    parser.add_argument("--max-channels", type=int, default=0)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--skip-nine-point-self-check", action="store_true")
    parser.add_argument("--strict", action="store_true")

    parser.add_argument("--internal-worker", action="store_true")
    parser.add_argument("--internal-subset", type=str)
    parser.add_argument("--internal-candidate-rank", type=int, default=-1)
    parser.add_argument("--internal-column-order", type=str, default="natural")
    args = parser.parse_args()

    if args.internal_worker:
        if not args.internal_subset:
            raise SystemExit("--internal-subset is required")
        subset = tuple(int(value) for value in args.internal_subset.split(","))
        result = exact_channel_worker({
            "base_script": str(args.base_script),
            "subset": subset,
            "candidate_rank": args.internal_candidate_rank,
            "column_order": args.internal_column_order,
        })
        print(json.dumps(result, sort_keys=True))
        return 0

    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "run.log"
    with log_path.open("a") as log_handle:
        original_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, log_handle)
        try:
            started = time.time()
            print("=" * 132)
            print("EHF-AMP-FOUND-04C: EXACT RATIONAL RANK CERTIFICATE SWEEP")
            print("=" * 132)
            print(f"04A engine:                   {args.base_script.resolve()}")
            print(f"04B census:                   {args.multi_prime_census.resolve() if args.multi_prime_census else 'not supplied'}")
            print(f"output directory:             {out_dir}")
            print(f"scope:                        {args.scope}")
            print(f"worker timeout:               {args.worker_timeout:.0f} s")
            print(f"column-order retries:         {args.column_orders}")
            print("coefficient domain:           QQ (exact SymPy DomainMatrix)")

            base = load_module(args.base_script.resolve(), "ehf_amp_found_04c_base_main")
            self_check = {
                "passed": True,
                "skipped": True,
                "observed_distribution": {},
                "elapsed_seconds": 0.0,
            }
            if not args.skip_nine_point_self_check:
                print("\nExact nine-point engine self-check")
                self_check = exact_nine_point_self_check(base)
                print(f"  recovered exact 03B distribution: {self_check['passed']}")
                print(f"  distribution:                       {self_check['observed_distribution']}")
                print(f"  elapsed:                            {self_check['elapsed_seconds']:.2f}s")

            census_rows: List[Dict[str, str]] = []
            census_by_a: Dict[str, Dict[str, str]] = {}
            if args.multi_prime_census:
                census_rows = read_csv(args.multi_prime_census.resolve())
                census_by_a = {row["A"]: row for row in census_rows}

            all_subsets: List[Subset] = list(itertools.combinations(range(2, 11), 4))  # type: ignore[assignment]
            if args.scope == "explicit":
                requested = list(args.subsets)
                if not requested:
                    raise ValueError("--scope explicit requires --subsets")
            elif args.scope == "all":
                requested = all_subsets
            else:
                if not census_rows:
                    raise ValueError(f"--scope {args.scope} requires --multi-prime-census")
                if args.scope == "frontier":
                    requested = select_frontier(census_rows)
                else:
                    requested = [
                        tuple(int(value) for value in row["A"].split(","))
                        for row in census_rows
                        if not normalize_bool(row.get("rational_rank_exact_certified", False))
                    ]

            def complexity(subset: Subset) -> Tuple[int, int, Subset]:
                row = census_by_a.get(subset_text(subset), {})
                source_size = normalize_int(row.get("source_fibre_size"), 10**9) or 10**9
                rank = normalize_int(row.get("generic_modular_rank"), 10**9) or 10**9
                return source_size, rank, subset

            requested = sorted(set(requested), key=complexity)
            if args.max_channels > 0:
                requested = requested[: args.max_channels]

            ledger_path = out_dir / "exact_qq_channel_ledger.csv"
            completed: Dict[str, Dict[str, object]] = {}
            if args.resume and ledger_path.exists():
                for row in read_csv(ledger_path):
                    if str(row.get("status", "")) == "exact":
                        completed[row["A"]] = dict(row)

            failure_rows: List[Dict[str, object]] = []
            print(f"\nRequested exact workers:      {len(requested)}")
            for ordinal, subset in enumerate(requested, start=1):
                key = subset_text(subset)
                if key in completed:
                    print(f"  [{ordinal:03d}/{len(requested):03d}] A={key:9s} resume exact")
                    continue
                candidate = normalize_int(census_by_a.get(key, {}).get("generic_modular_rank"), -1) or 0
                errors: List[str] = []
                result: Optional[Dict[str, object]] = None
                for column_order in args.column_orders:
                    print(
                        f"  [{ordinal:03d}/{len(requested):03d}] A={key:9s} "
                        f"order={column_order:8s}",
                        end="",
                        flush=True,
                    )
                    result, status = run_worker_subprocess(
                        Path(__file__).resolve(),
                        args.base_script.resolve(),
                        subset,
                        int(candidate),
                        column_order,
                        args.worker_timeout,
                    )
                    if result is not None:
                        row = {
                            **result,
                            "status": "exact",
                            "attempt_errors": " | ".join(errors),
                        }
                        completed[key] = row
                        print(
                            f" r_Q={int(result['QQ_residue_rank']):3d} "
                            f"candidate={candidate:3d} "
                            f"match={result['candidate_match']} "
                            f"{float(result['elapsed_seconds']):.2f}s"
                        )
                        break
                    errors.append(f"{column_order}:{status}")
                    print(f" {status}")

                if result is None:
                    failure = {
                        "A": key,
                        "candidate_generic_modular_rank": candidate,
                        "status": "failed",
                        "attempt_errors": " | ".join(errors),
                    }
                    failure_rows.append(failure)
                    completed[key] = failure

                ordered_ledger = sorted(completed.values(), key=lambda row: tuple(int(v) for v in str(row["A"]).split(",")))
                write_csv(ledger_path, ordered_ledger)
                write_csv(out_dir / "exact_qq_worker_failures.csv", failure_rows)

            exact_worker_rows = [row for row in completed.values() if str(row.get("status")) == "exact"]
            exact_worker_by_a = {str(row["A"]): row for row in exact_worker_rows}

            # Merge imported exact bounds and direct exact workers into one 126-row ledger.
            merged_rows: List[Dict[str, object]] = []
            for subset in all_subsets:
                key = subset_text(subset)
                source = census_by_a.get(key, {})
                imported_exact = normalize_bool(source.get("rational_rank_exact_certified", False))
                imported_rank = normalize_int(source.get("exact_rational_rank")) if imported_exact else None
                worker = exact_worker_by_a.get(key)
                worker_rank = normalize_int(worker.get("QQ_residue_rank")) if worker else None
                exact_rank = worker_rank if worker_rank is not None else imported_rank
                certificate_type = (
                    "direct_QQ_rank_difference"
                    if worker_rank is not None
                    else str(source.get("exact_certificate_type", "04B_bound_saturation"))
                    if imported_exact
                    else "open"
                )
                merged_rows.append({
                    "A": key,
                    "a": subset[0],
                    "b": subset[1],
                    "c": subset[2],
                    "d": subset[3],
                    "generic_modular_rank": source.get("generic_modular_rank", ""),
                    "04B_exact_certified": imported_exact,
                    "04B_exact_rank": imported_rank if imported_rank is not None else "",
                    "04C_direct_worker_completed": worker is not None,
                    "04C_QQ_C_rank": worker.get("QQ_C_rank", "") if worker else "",
                    "04C_QQ_stacked_rank": worker.get("QQ_stacked_rank", "") if worker else "",
                    "04C_QQ_residue_rank": worker_rank if worker_rank is not None else "",
                    "exact_rational_rank_certified": exact_rank is not None,
                    "exact_rational_rank": exact_rank if exact_rank is not None else "",
                    "certificate_type": certificate_type,
                    "candidate_match": worker.get("candidate_match", "") if worker else "",
                })
            write_csv(out_dir / "exact_rational_rank_master_ledger.csv", merged_rows)

            certified_rows = [row for row in merged_rows if normalize_bool(row["exact_rational_rank_certified"])]
            unresolved_rows = [row for row in merged_rows if not normalize_bool(row["exact_rational_rank_certified"])]
            direct_mismatches = [row for row in exact_worker_rows if not normalize_bool(row.get("candidate_match", False))]
            boundary_audit = boundary_law_audit(certified_rows, "exact_rational_rank")

            exact_distribution = Counter(int(row["exact_rational_rank"]) for row in certified_rows)
            distribution_rows = [
                {
                    "exact_rational_rank": rank,
                    "certified_channel_count": count,
                    "rank_contribution": rank * count,
                }
                for rank, count in sorted(exact_distribution.items())
            ]
            write_csv(out_dir / "exact_rational_rank_distribution.csv", distribution_rows)
            write_csv(out_dir / "unresolved_exact_rank_channels.csv", unresolved_rows)
            write_csv(out_dir / "direct_QQ_candidate_mismatches.csv", direct_mismatches)

            all_126_exact = len(certified_rows) == 126
            full_boundary_law = all_126_exact and bool(boundary_audit["passed_on_available_rows"])
            complete_recovery_exact = all_126_exact and all(
                (int(row["exact_rational_rank"]) == 296) == (int(row["b"]) >= 7)
                for row in certified_rows
            )
            exact_workers_clean = all(
                normalize_bool(row.get("candidate_match", False))
                and normalize_bool(row.get("structure_checks_pass", False))
                for row in exact_worker_rows
            )

            if all_126_exact and full_boundary_law and complete_recovery_exact and exact_workers_clean:
                verdict = "EHF_AMP_FOUND_04C_EXACT_RATIONAL_BOUNDARY_CORRECTED_THREE_TAIL_RANK_THEOREM_PROVED"
            elif exact_worker_rows and exact_workers_clean:
                verdict = "EHF_AMP_FOUND_04C_PARTIAL_EXACT_RATIONAL_CERTIFICATION_ADVANCED"
            elif direct_mismatches:
                verdict = "EHF_AMP_FOUND_04C_MODULAR_CANDIDATE_REVISED_BY_EXACT_QQ"
            else:
                verdict = "EHF_AMP_FOUND_04C_EXACT_RATIONAL_SWEEP_INCOMPLETE"

            summary = {
                "probe": "EHF-AMP-FOUND-04C",
                "scope": args.scope,
                "requested_worker_count": len(requested),
                "direct_exact_workers_completed": len(exact_worker_rows),
                "direct_exact_worker_failures": len(failure_rows),
                "direct_candidate_mismatch_count": len(direct_mismatches),
                "imported_or_direct_exact_channel_count": len(certified_rows),
                "unresolved_channel_count": len(unresolved_rows),
                "all_126_exact": all_126_exact,
                "boundary_law_exact_on_available_certificates": boundary_audit,
                "complete_recovery_iff_b_ge_7_exact": complete_recovery_exact if all_126_exact else None,
                "nine_point_self_check": self_check,
                "exact_rank_distribution": dict(sorted(exact_distribution.items())),
                "elapsed_seconds": time.time() - started,
                "verdict": verdict,
            }
            (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
            (out_dir / "verdict.json").write_text(json.dumps({"verdict": verdict}, indent=2))

            print("\n" + "=" * 132)
            print("FINAL SUMMARY")
            print("=" * 132)
            print(f"Nine-point exact self-check:        {self_check.get('passed', True)}")
            print(f"Direct QQ workers completed:        {len(exact_worker_rows)} / {len(requested)}")
            print(f"Direct candidate mismatches:        {len(direct_mismatches)}")
            print(f"Exact QQ ranks certified total:     {len(certified_rows)} / 126")
            print(f"Boundary law exact on certificates: {boundary_audit['passed_on_available_rows']}")
            print(f"All 126 exact:                      {all_126_exact}")
            print(f"Verdict:                            {verdict}")
            print(f"elapsed:                            {time.time() - started:.2f} seconds")

            failed_checks: List[str] = []
            if not self_check.get("passed", True):
                failed_checks.append("nine_point_exact_self_check_failed")
            if direct_mismatches:
                failed_checks.append("direct_QQ_modular_candidate_mismatch")
            if any(not normalize_bool(row.get("structure_checks_pass", False)) for row in exact_worker_rows):
                failed_checks.append("worker_structure_check_failed")
            if failure_rows:
                failed_checks.append("worker_failures_or_timeouts")
            if args.strict and failed_checks:
                print(f"strict checks:                      FAIL")
                print(f"failed checks:                      {', '.join(failed_checks)}")
                return 1
            print("strict checks:                      PASS")
            return 0
        finally:
            sys.stdout = original_stdout


if __name__ == "__main__":
    raise SystemExit(main())
