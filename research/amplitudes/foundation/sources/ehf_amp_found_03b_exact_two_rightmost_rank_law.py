#!/usr/bin/env python3
"""
EHF-AMP-FOUND-03B: Exact Two-Rightmost-Label Rank Law at 9 -> 8
================================================================

03A found, numerically, that the fixed-anchor reflection-aware 9 -> 8
factorisation map is diagonal on the 35 parity-position fibres and has channel
ranks

    0^4, 2^3, 8^3, 9^6, 14^6, 15^13.

03B removes the numerical rank-basis dependence.

For A={a<b<c} subset {2,...,8}, let Q_A be the exact integer KK-coordinate
matrix of the n=9 source fibre, and let D_A be the exact signed delete-9
incidence matrix into the A-labelled n=8 target fibre. The transmitted rank is

    r_A = rank_Q([Q_A ; D_A]) - rank_Q(Q_A).

This identity follows from

    r_A = dim D_A(ker Q_A)
        = dim ker Q_A - dim(ker Q_A intersect ker D_A).

All ranks are computed exactly over QQ using SymPy DomainMatrix. No random
kinematics, numerical SVD, cached relation basis, seed, or rational
reconstruction is used.

The probe proves exhaustively that r_A depends only on the two largest labels
b,c and not on a:

    c <= 5, b <= 4 : 0
    c = 6,  b <= 4 : 2
    c >= 7, b <= 4 : 9
    b = 5,  c = 6  : 8
    b = 5,  c >= 7 : 14
    b >= 6          : 15

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --census-csv runs/ehf_amp_found_03a/diagonal_channel_census.csv \
  --out-dir runs/ehf_amp_found_03b \
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
from typing import Dict, Iterator, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

Cycle = Tuple[int, ...]
FibreKey = Tuple[Tuple[int, ...], Tuple[int, ...]]
Subset = Tuple[int, int, int]


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
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


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


def shuffles(
    left: Sequence[int],
    right: Sequence[int],
) -> Iterator[Tuple[int, ...]]:
    if not left:
        yield tuple(right)
        return
    if not right:
        yield tuple(left)
        return
    for tail in shuffles(left[1:], right):
        yield (left[0],) + tail
    for tail in shuffles(left, right[1:]):
        yield (right[0],) + tail


def predicted_rank_from_two_rightmost(subset: Subset) -> int:
    _, b, c = subset
    if b >= 6:
        return 15
    if b == 5:
        return 8 if c == 6 else 14
    # b <= 4
    if c <= 5:
        return 0
    if c == 6:
        return 2
    return 9


def rank_class_name(subset: Subset) -> str:
    _, b, c = subset
    if b >= 6:
        return "B_GE_6"
    if b == 5 and c == 6:
        return "B_EQ_5_C_EQ_6"
    if b == 5:
        return "B_EQ_5_C_GE_7"
    if c <= 5:
        return "B_LE_4_C_LE_5"
    if c == 6:
        return "B_LE_4_C_EQ_6"
    return "B_LE_4_C_GE_7"


def gap_signature(subset: Subset) -> Tuple[int, int, int, int]:
    a, b, c = subset
    return a - 2, b - a - 1, c - b - 1, 8 - c


def inversion_count(subset: Subset) -> int:
    complement = set(range(2, 9)) - set(subset)
    return sum(a > b for a in subset for b in complement)


def source_fibre_size_formula(subset: Subset) -> int:
    return 36 * (4 + inversion_count(subset))


def exact_kk_and_stacked_matrices(
    base,
    helper,
    subset: Subset,
    source_fibres: Mapping[FibreKey, Sequence[Cycle]],
    target_fibres: Mapping[FibreKey, Sequence[Cycle]],
    kk_index: Mapping[Tuple[int, ...], int],
) -> Tuple[sp.MutableSparseMatrix, sp.MutableSparseMatrix, Dict[str, object]]:
    """
    Construct Q_A and [Q_A;D_A] exactly as sparse integer matrices.
    """
    source_key = key_from_subset_9(subset)
    target_key = key_from_subset_8(subset)
    source = source_fibres[source_key]
    target = target_fibres[target_key]
    target_index = {cycle: index for index, cycle in enumerate(target)}

    q_entries: Dict[Tuple[int, int], int] = {}
    stacked_entries: Dict[Tuple[int, int], int] = {}
    active_columns = 0
    target_preimages = [0] * len(target)

    for column, cycle in enumerate(source):
        position = cycle.index(9)
        alpha = cycle[1:position]
        beta = cycle[position + 1 :]
        kk_sign = -1 if len(beta) % 2 else 1

        for sigma in shuffles(alpha, tuple(reversed(beta))):
            row = kk_index[sigma]
            key = (row, column)
            q_entries[key] = q_entries.get(key, 0) + kk_sign
            stacked_entries[key] = stacked_entries.get(key, 0) + kk_sign

        if cycle[1] == 9 or cycle[-1] == 9:
            active_columns += 1
            sign, image, _, _, _ = helper.delete_new_label(base, cycle, 9)
            row = target_index[image]
            stacked_entries[(math.factorial(7) + row, column)] = int(sign)
            target_preimages[row] += 1

    q_matrix = sp.MutableSparseMatrix(
        math.factorial(7),
        len(source),
        q_entries,
    )
    stacked_matrix = sp.MutableSparseMatrix(
        math.factorial(7) + len(target),
        len(source),
        stacked_entries,
    )
    metadata = {
        "source_key": base.key_text(source_key),
        "target_key": base.key_text(target_key),
        "source_fibre_size": len(source),
        "target_fibre_size": len(target),
        "q_nonzeros": len(q_entries),
        "stacked_nonzeros": len(stacked_entries),
        "active_source_columns": active_columns,
        "target_preimage_min": min(target_preimages),
        "target_preimage_max": max(target_preimages),
    }
    return q_matrix, stacked_matrix, metadata


def exact_domain_rank(matrix: sp.MatrixBase) -> int:
    """
    Exact rank over QQ. DomainMatrix avoids the slow generic Matrix.rank path.
    """
    domain_matrix = DomainMatrix.from_Matrix(matrix).convert_to(QQ)
    return int(domain_matrix.rank())


def read_census(path: Optional[Path]) -> Dict[str, Dict[str, str]]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="") as handle:
        return {
            row["A"]: row
            for row in csv.DictReader(handle)
        }


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    helper_script = Path(args.helper_script).resolve()
    census_path = (
        Path(args.census_csv).resolve()
        if args.census_csv
        else None
    )
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_03b_base")
    helper = load_module(helper_script, "ehf_amp_found_03b_helper")

    source_fibres: Dict[FibreKey, List[Cycle]] = base.fibres(9)
    target_fibres: Dict[FibreKey, List[Cycle]] = base.fibres(8)
    subsets: List[Subset] = list(itertools.combinations(range(2, 9), 3))
    kk_permutations = list(itertools.permutations(range(2, 9)))
    kk_index = {
        permutation: index
        for index, permutation in enumerate(kk_permutations)
    }
    census = read_census(census_path)

    print("=" * 120)
    print("EHF-AMP-FOUND-03B: EXACT TWO-RIGHTMOST-LABEL RANK LAW AT 9 -> 8")
    print("=" * 120)
    print(f"base script:                 {base_script}")
    print(f"reflection-aware helper:     {helper_script}")
    print(f"03A census comparison:       {census_path if census_path else 'not supplied'}")
    print(f"output directory:            {out_dir}")
    print(f"source channels:             {len(subsets)}")
    print(f"KK basis dimension:          {len(kk_permutations)}")
    print("rank engine:                 exact DomainMatrix over QQ")
    print("numerical relation bases:    not used")

    channel_rows: List[Dict[str, object]] = []
    all_formula_matches = True
    all_structure_checks = True
    all_census_matches = True
    total_rank = 0

    for index, subset in enumerate(subsets, start=1):
        t0 = time.time()
        q_matrix, stacked_matrix, metadata = exact_kk_and_stacked_matrices(
            base,
            helper,
            subset,
            source_fibres,
            target_fibres,
            kk_index,
        )
        q_rank = exact_domain_rank(q_matrix)
        stacked_rank = exact_domain_rank(stacked_matrix)
        residue_rank = stacked_rank - q_rank
        source_relation_dim = q_matrix.cols - q_rank
        source_residue_kernel_dim = source_relation_dim - residue_rank
        predicted_rank = predicted_rank_from_two_rightmost(subset)
        formula_match = residue_rank == predicted_rank
        all_formula_matches &= formula_match
        total_rank += residue_rank

        structure_ok = (
            metadata["active_source_columns"] == 144
            and metadata["target_preimage_min"] == 2
            and metadata["target_preimage_max"] == 2
            and metadata["target_fibre_size"] == 72
            and metadata["source_fibre_size"] == source_fibre_size_formula(subset)
        )
        all_structure_checks &= structure_ok

        census_rank = ""
        census_source_dim = ""
        census_match = True
        if census:
            prior = census[subset_text(subset)]
            census_rank = int(prior["residue_rank"])
            census_source_dim = int(prior["source_relation_dim"])
            census_match = (
                census_rank == residue_rank
                and census_source_dim == source_relation_dim
            )
            all_census_matches &= census_match

        a, b, c = subset
        gaps = gap_signature(subset)
        row = {
            "channel_index": index - 1,
            "A": subset_text(subset),
            "a": a,
            "b": b,
            "c": c,
            "two_rightmost_pair": f"{b},{c}",
            "rank_class": rank_class_name(subset),
            "predicted_rank_from_b_c": predicted_rank,
            "exact_residue_rank": residue_rank,
            "rank_formula_match": formula_match,
            "source_fibre_size": metadata["source_fibre_size"],
            "source_fibre_size_formula": source_fibre_size_formula(subset),
            "source_size_formula_match": (
                metadata["source_fibre_size"]
                == source_fibre_size_formula(subset)
            ),
            "exact_Q_rank": q_rank,
            "exact_stacked_rank": stacked_rank,
            "exact_source_relation_dim": source_relation_dim,
            "exact_source_residue_kernel_dim": source_residue_kernel_dim,
            "target_relation_dim": 15,
            "target_missing_dim": 15 - residue_rank,
            "complete_target_recovery": residue_rank == 15,
            "inversion_count": inversion_count(subset),
            "gap_signature": "-".join(map(str, gaps)),
            "left_gap_sum_b_minus_3": gaps[0] + gaps[1],
            "right_tail_gap_8_minus_c": gaps[3],
            "active_source_columns": metadata["active_source_columns"],
            "target_preimage_min": metadata["target_preimage_min"],
            "target_preimage_max": metadata["target_preimage_max"],
            "structure_checks_pass": structure_ok,
            "Q_nonzeros": metadata["q_nonzeros"],
            "stacked_nonzeros": metadata["stacked_nonzeros"],
            "source_key": metadata["source_key"],
            "target_key": metadata["target_key"],
            "03A_residue_rank": census_rank,
            "03A_source_relation_dim": census_source_dim,
            "03A_exact_match": census_match,
            "elapsed_seconds": f"{time.time() - t0:.4f}",
        }
        channel_rows.append(row)

        if index % 5 == 0 or index == len(subsets):
            print(
                f"  [{index:02d}/35] A={subset_text(subset):5s} "
                f"rank(Q)={q_rank:3d} rank([Q;D])={stacked_rank:3d} "
                f"r_A={residue_rank:2d} "
                f"{'OK' if formula_match else 'MISMATCH'}"
            )

    write_csv(out_dir / "exact_channel_rank_ledger.csv", channel_rows)

    # ------------------------------------------------------------------
    # Exact classification by the two rightmost labels.
    # ------------------------------------------------------------------
    grouped: MutableMapping[Tuple[int, int], List[Dict[str, object]]] = defaultdict(list)
    for row in channel_rows:
        grouped[(int(row["b"]), int(row["c"]))].append(row)

    bc_rows: List[Dict[str, object]] = []
    all_a_independent = True
    for (b, c), rows in sorted(grouped.items()):
        ranks = sorted({int(row["exact_residue_rank"]) for row in rows})
        source_dims = sorted({int(row["exact_source_relation_dim"]) for row in rows})
        source_sizes = sorted({int(row["source_fibre_size"]) for row in rows})
        a_independent = len(ranks) == 1
        all_a_independent &= a_independent
        bc_rows.append({
            "b": b,
            "c": c,
            "allowed_a_values": ";".join(str(row["a"]) for row in rows),
            "a_count": len(rows),
            "exact_rank_values": ";".join(map(str, ranks)),
            "rank_independent_of_a": a_independent,
            "predicted_piecewise_rank": predicted_rank_from_two_rightmost(
                (2, b, c)
            ),
            "source_fibre_sizes": ";".join(map(str, source_sizes)),
            "source_relation_dims": ";".join(map(str, source_dims)),
            "source_data_vary_with_a": (
                len(source_sizes) > 1 or len(source_dims) > 1
            ),
        })
    write_csv(out_dir / "two_rightmost_pair_table.csv", bc_rows)

    # Six coarse cells of the piecewise law.
    cell_groups: MutableMapping[str, List[Dict[str, object]]] = defaultdict(list)
    for row in channel_rows:
        cell_groups[str(row["rank_class"])].append(row)

    class_order = [
        "B_LE_4_C_LE_5",
        "B_LE_4_C_EQ_6",
        "B_LE_4_C_GE_7",
        "B_EQ_5_C_EQ_6",
        "B_EQ_5_C_GE_7",
        "B_GE_6",
    ]
    cell_rows: List[Dict[str, object]] = []
    for name in class_order:
        rows = cell_groups[name]
        ranks = sorted({int(row["exact_residue_rank"]) for row in rows})
        cell_rows.append({
            "rank_class": name,
            "condition": {
                "B_LE_4_C_LE_5": "b<=4 and c<=5",
                "B_LE_4_C_EQ_6": "b<=4 and c=6",
                "B_LE_4_C_GE_7": "b<=4 and c>=7",
                "B_EQ_5_C_EQ_6": "b=5 and c=6",
                "B_EQ_5_C_GE_7": "b=5 and c>=7",
                "B_GE_6": "b>=6",
            }[name],
            "channel_count": len(rows),
            "exact_rank": ranks[0] if len(ranks) == 1 else ";".join(map(str, ranks)),
            "subsets": ";".join(str(row["A"]) for row in rows),
            "rank_constant_in_class": len(ranks) == 1,
            "total_rank_contribution": sum(
                int(row["exact_residue_rank"]) for row in rows
            ),
            "total_target_deficit": sum(
                int(row["target_missing_dim"]) for row in rows
            ),
        })
    write_csv(out_dir / "six_cell_rank_law.csv", cell_rows)

    rank_counts = Counter(int(row["exact_residue_rank"]) for row in channel_rows)
    distribution_rows = [
        {
            "exact_residue_rank": rank,
            "channel_count": count,
            "global_rank_contribution": rank * count,
            "target_deficit_per_channel": 15 - rank,
            "global_target_deficit": (15 - rank) * count,
        }
        for rank, count in sorted(rank_counts.items())
    ]
    write_csv(out_dir / "exact_rank_distribution.csv", distribution_rows)

    # Reflection A -> {10-a}.
    row_by_subset = {
        tuple(map(int, str(row["A"]).split(","))): row
        for row in channel_rows
    }
    reflection_rows: List[Dict[str, object]] = []
    visited = set()
    for subset in subsets:
        reflected = tuple(sorted(10 - value for value in subset))
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
            "left_rank": left["exact_residue_rank"],
            "right_rank": right["exact_residue_rank"],
            "rank_equal": (
                left["exact_residue_rank"] == right["exact_residue_rank"]
            ),
            "rank_sum": (
                int(left["exact_residue_rank"])
                + int(right["exact_residue_rank"])
            ),
            "left_source_relation_dim": left["exact_source_relation_dim"],
            "right_source_relation_dim": right["exact_source_relation_dim"],
        })
    write_csv(out_dir / "exact_label_reflection_audit.csv", reflection_rows)

    expected_distribution = {0: 4, 2: 3, 8: 3, 9: 6, 14: 6, 15: 13}
    expected_distribution_match = dict(sorted(rank_counts.items())) == expected_distribution
    complete_count = rank_counts[15]
    total_target_dim = 35 * 15
    total_deficit = total_target_dim - total_rank

    exact_law = (
        all_formula_matches
        and all_a_independent
        and expected_distribution_match
        and total_rank == 363
        and complete_count == 13
        and all_structure_checks
        and (not census or all_census_matches)
    )

    verdict = (
        "EHF_AMP_FOUND_03B_EXACT_TWO_RIGHTMOST_LABEL_RANK_LAW_PROVED"
        if exact_law
        else "EHF_AMP_FOUND_03B_EXACT_RANK_LAW_FAILED"
    )

    certificate = {
        "theorem": (
            "For A={a<b<c} subset {2,...,8}, the exact fixed-anchor 9->8 "
            "transmitted local KK-relation rank depends only on b,c."
        ),
        "rank_identity": (
            "r_A = rank_Q([Q_A;D_A]) - rank_Q(Q_A)"
        ),
        "piecewise_law": [
            {"condition": "b<=4 and c<=5", "rank": 0},
            {"condition": "b<=4 and c=6", "rank": 2},
            {"condition": "b<=4 and c>=7", "rank": 9},
            {"condition": "b=5 and c=6", "rank": 8},
            {"condition": "b=5 and c>=7", "rank": 14},
            {"condition": "b>=6", "rank": 15},
        ],
        "equivalent_gap_variables": {
            "b_minus_3": "g0+g1",
            "eight_minus_c": "g3",
            "statement": (
                "The exact rank depends only on (g0+g1,g3), not on the "
                "internal split g0 versus g1."
            ),
        },
        "exact_computation": {
            "coefficient_domain": "QQ",
            "KK_matrix_shape": "5040 x |F_A^(9)|",
            "stacked_matrix_shape": "5112 x |F_A^(9)|",
            "numerical_SVD_used": False,
            "random_kinematics_used": False,
            "cached_relation_bases_used": False,
            "rational_reconstruction_used": False,
        },
        "global_results": {
            "channel_count": 35,
            "rank_distribution": dict(sorted(rank_counts.items())),
            "global_direct_sum_rank": total_rank,
            "complete_target_count": complete_count,
            "target_local_dimension": total_target_dim,
            "target_missing_dimension": total_deficit,
        },
        "checks": {
            "rank_independent_of_a_at_fixed_b_c": all_a_independent,
            "piecewise_formula_matches_all_35": all_formula_matches,
            "expected_distribution_matches": expected_distribution_match,
            "exact_structure_checks": all_structure_checks,
            "03A_census_matches_exact_computation": (
                None if not census else all_census_matches
            ),
        },
        "claim_boundary": (
            "This proves the exact fixed-anchor n=9 to n=8 rank law from KK "
            "shuffle coordinates and the signed deletion map. It does not yet "
            "explain the six ranks by an intrinsic representation-theoretic "
            "decomposition, establish anchor independence, or prove the same "
            "parity architecture at general n."
        ),
    }
    with (out_dir / "exact_rank_law_certificate.json").open("w") as handle:
        json.dump(json_safe(certificate), handle, indent=2)

    elapsed = time.time() - started
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "exact_QQ_rank_computation": True,
        "channel_count": len(channel_rows),
        "two_rightmost_rank_law": all_formula_matches,
        "rank_independent_of_smallest_label": all_a_independent,
        "rank_distribution": dict(sorted(rank_counts.items())),
        "global_direct_sum_rank": total_rank,
        "complete_target_count": complete_count,
        "target_local_dimension": total_target_dim,
        "target_missing_dimension": total_deficit,
        "structure_checks": all_structure_checks,
        "03A_census_supplied": bool(census),
        "03A_census_exact_match": None if not census else all_census_matches,
        "exact_rank_law_certificate": exact_law,
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "exact_rank_law_certificate.json",
            "exact_channel_rank_ledger.csv",
            "two_rightmost_pair_table.csv",
            "six_cell_rank_law.csv",
            "exact_rank_distribution.csv",
            "exact_label_reflection_audit.csv",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)
    with (out_dir / "verdict.json").open("w") as handle:
        json.dump(
            {
                "verdict": verdict,
                "exact_rank_law_certificate": exact_law,
                "global_rank": total_rank,
                "complete_targets": complete_count,
            },
            handle,
            indent=2,
        )

    strict_failures = []
    if args.strict:
        checks = {
            "all_35_channels": len(channel_rows) == 35,
            "exact_structure_checks": all_structure_checks,
            "rank_independent_of_a": all_a_independent,
            "piecewise_formula": all_formula_matches,
            "rank_distribution": expected_distribution_match,
            "global_rank_363": total_rank == 363,
            "complete_targets_13": complete_count == 13,
            "03A_exact_match": (not census or all_census_matches),
        }
        strict_failures = [
            name for name, passed in checks.items() if not passed
        ]

    print("\n" + "=" * 120)
    print("FINAL SUMMARY")
    print("=" * 120)
    print(f"Exact QQ channel ranks:              True")
    print(f"Rank independent of smallest a:      {all_a_independent}")
    print(f"Six-cell (b,c) law matches 35/35:    {all_formula_matches}")
    print(f"Rank distribution:                   {dict(sorted(rank_counts.items()))}")
    print(f"Global direct-sum rank:               {total_rank}")
    print(f"Complete target fibres:               {complete_count}/35")
    print(f"03A numerical census exact match:     {all_census_matches if census else 'not tested'}")
    print(f"Verdict:                              {verdict}")
    print(f"elapsed:                              {elapsed:.2f} seconds")
    print(f"summary:                              {out_dir / 'summary.json'}")
    if args.strict:
        print(f"strict checks:                        {'PASS' if not strict_failures else 'FAIL'}")
        if strict_failures:
            print(f"failed checks:                        {', '.join(strict_failures)}")
    print("=" * 120)

    if strict_failures:
        raise SystemExit(2)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Exact QQ proof of the two-rightmost-label rank law for the "
            "fixed-anchor 9->8 diagonal factorisation channels."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--helper-script", required=True)
    parser.add_argument("--census-csv")
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
