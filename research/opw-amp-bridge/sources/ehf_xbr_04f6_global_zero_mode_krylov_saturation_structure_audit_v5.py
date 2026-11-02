#!/usr/bin/env python3
r"""
EHF-XBR-04F6: Global Zero-Mode and Krylov-Saturation Structure Audit


This probe continues the exact OPW3/AMP bridge audit after XBR-04F5.


Part A reconstructs exact chamber-adjacency kernel bases for every singular
proper n=9 chamber and audits:


    * deterministic primitive RREF-basis support/sign structure;
    * basis-independent coordinate activity and projective coordinate classes;
    * exact label-induced chamber automorphisms;
    * the induced rational representation on the full chamber kernel;
    * automorphism-orbit equitable quotients and exact quotient-kernel lifts;
    * structural colour-refinement equitable quotients.


Part B consumes the XBR-04F5 Krylov growth outputs and audits:


    * the exact two-feature rules separating the null/small-complement locus;
    * leave-one-channel-out recovery of minimum-complexity pair rules;
    * cumulative closure and residual-codimension curves;
    * exact low-order preterminal recurrence tests on growth increments and
      residual codimensions.


Canonical kernel-vector statistics depend on the deterministic nullspace basis.
Coordinate activity, kernel dimension, automorphism-fixed dimensions, orbit
quotient nullity, and exact quotient lifts are basis-independent.


No physical meaning is assigned to a zero mode, representation, support pattern,
or recurrence without a separate bridge argument.
"""


from __future__ import annotations


import argparse
import csv
import gzip
import hashlib
import importlib.util
import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Set, Tuple


import sympy as sp
from flint import fmpq_mat, fmpz_mat, nmod_mat


SCRIPT_VERSION = "ehf_xbr_04f6_v5_2026-07-28"
REGIMES = ("null", "mixed", "invertible")
Subset = Tuple[int, int, int]
IntegerRows = List[List[int]]
Permutation = Tuple[int, ...]


PAIR_PATTERN = re.compile(
    r"^(?P<neg>NOT \()?"
    r"\((?P<f1>[^ ]+) (?P<o1>==|<=|>=) (?P<t1>[^)]+)\) "
    r"(?P<join>AND|OR) "
    r"\((?P<f2>[^ ]+) (?P<o2>==|<=|>=) (?P<t2>[^)]+)\)"
    r"(?P<close>\))?$"
)




def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()




def load_module(path: Path, name: str):
    if not path.exists():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module




def parse_subset(text: str) -> Subset:
    values = tuple(int(value.strip()) for value in text.split(","))
    if len(values) != 3 or len(set(values)) != 3:
        raise ValueError(f"invalid subset: {text}")
    return tuple(sorted(values))  # type: ignore[return-value]




def subset_text(subset: Subset) -> str:
    return ",".join(map(str, subset))




def subset_slug(subset: Subset) -> str:
    return "A_" + "_".join(map(str, subset))




def truthy(value: object) -> bool:
    return str(value).strip().lower() == "true"




def integer(row: Mapping[str, object], key: str) -> int:
    return int(str(row[key]))




def read_csv(path: Path) -> List[dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))




def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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




def read_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open() as handle:
        return json.load(handle)




def write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)




def parse_number(value: object) -> int | Fraction | None:
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None
    if text.lower() in {"true", "false"}:
        return int(text.lower() == "true")
    try:
        if "/" in text:
            return Fraction(text)
        return int(text)
    except (ValueError, ZeroDivisionError):
        return None




def serialise_number(value: object) -> object:
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    return value




def primitive_integer_row(row: Sequence[int]) -> List[int]:
    values = [int(value) for value in row]
    row_gcd = 0
    for value in values:
        row_gcd = math.gcd(row_gcd, abs(value))
    if row_gcd > 1:
        values = [value // row_gcd for value in values]
    first = next((value for value in values if value), 0)
    if first < 0:
        values = [-value for value in values]
    return values




def sha256_integer_rows(rows: Sequence[Sequence[int]]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        digest.update((",".join(map(str, row)) + "\n").encode("utf-8"))
    return digest.hexdigest()




def write_sparse_integer_matrix(path: Path, rows: Sequence[Sequence[int]]) -> None:
    nrows = len(rows)
    ncols = len(rows[0]) if rows else 0
    entries = [
        [i, j, str(value)]
        for i, row in enumerate(rows)
        for j, value in enumerate(row)
        if value
    ]
    payload = {
        "ring": "ZZ",
        "shape": [nrows, ncols],
        "entries": entries,
        "sha256_dense_rows": sha256_integer_rows(rows),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        json.dump(payload, handle, separators=(",", ":"))




def row_basis_pivots(rows: IntegerRows) -> List[int]:
    if not rows:
        return []
    matrix = fmpz_mat(rows)
    rref_num, _, rank = matrix.rref()
    rank = int(rank)
    if rank != len(rows):
        raise ValueError(f"row basis is dependent: rank={rank}, rows={len(rows)}")
    pivots: List[int] = []
    for i in range(rank):
        pivot = next(
            (j for j in range(len(rows[0])) if int(rref_num[i, j]) != 0),
            None,
        )
        if pivot is None:
            raise RuntimeError("failed to extract kernel-basis pivot")
        pivots.append(pivot)
    return pivots




def vector_annihilated(matrix_rows: IntegerRows, vector: Sequence[int]) -> bool:
    return all(
        sum(int(value) * int(vector[column]) for column, value in enumerate(row)) == 0
        for row in matrix_rows
    )




def modular_rref_pivots(
    rows: IntegerRows,
    modulus: int,
) -> tuple[List[int], int]:
    """Return pivot columns from an exact RREF over the prime field F_p."""
    reduced, rank = nmod_mat(rows, modulus).rref()
    rank = int(rank)
    ncols = len(rows[0]) if rows else 0
    pivots: List[int] = []
    for row_index in range(rank):
        pivot = next(
            (
                column
                for column in range(ncols)
                if int(reduced[row_index, column]) % modulus != 0
            ),
            None,
        )
        if pivot is None:
            raise RuntimeError("failed to extract modular RREF pivot")
        pivots.append(pivot)
    return pivots, rank



def rational_vector_to_primitive_integers(
    values: Sequence[object],
) -> List[int]:
    fractions = [Fraction(str(value)) for value in values]
    denominator = 1
    for value in fractions:
        denominator = math.lcm(denominator, value.denominator)
    integers = [
        value.numerator * (denominator // value.denominator)
        for value in fractions
    ]
    return primitive_integer_row(integers)



def exact_right_nullspace_dixon(
    rows: IntegerRows,
    ncols: int,
    expected_nullity: int,
    pivot_primes: Sequence[int],
) -> tuple[IntegerRows, int]:
    """
    Construct an exact rational nullspace using modular pivot discovery and one
    multi-right-hand-side Dixon solve, then return a primitive integer row basis.

    Exactness does not rest on the modular calculation: the selected square
    pivot block is solved over Q and the caller verifies every resulting vector
    against the full integer matrix.  The expected rank is already certified by
    the XBR-04F3/04F5 ledger.
    """
    if len(rows) != ncols:
        raise ValueError("Dixon nullspace path currently requires a square matrix")
    expected_rank = ncols - expected_nullity
    if expected_nullity == 0:
        return [], 0

    selected_prime = None
    pivot_columns: List[int] = []
    pivot_rows: List[int] = []
    for prime in pivot_primes:
        candidate_columns, modular_rank = modular_rref_pivots(rows, prime)
        if modular_rank != expected_rank:
            continue
        restricted_transpose = [
            [int(rows[row][column]) for row in range(len(rows))]
            for column in candidate_columns
        ]
        candidate_rows, restricted_rank = modular_rref_pivots(
            restricted_transpose,
            prime,
        )
        if restricted_rank != expected_rank:
            continue
        selected_prime = prime
        pivot_columns = candidate_columns
        pivot_rows = candidate_rows
        break

    if selected_prime is None:
        raise RuntimeError(
            "no pivot prime reproduced the certified chamber rank; "
            f"tried {list(pivot_primes)}"
        )

    pivot_set = set(pivot_columns)
    free_columns = [column for column in range(ncols) if column not in pivot_set]
    if len(free_columns) != expected_nullity:
        raise RuntimeError(
            "modular pivot/free-column count mismatch: "
            f"free={len(free_columns)} expected={expected_nullity}"
        )

    pivot_block = [
        [int(rows[row][column]) for column in pivot_columns]
        for row in pivot_rows
    ]
    free_block_negative = [
        [-int(rows[row][column]) for column in free_columns]
        for row in pivot_rows
    ]
    left = fmpq_mat(pivot_block)
    right = fmpq_mat(free_block_negative)
    try:
        solution = left.solve(right, algorithm="dixon")
    except TypeError:
        # Compatibility with older python-flint builds that expose solve()
        # without the keyword selector.
        solution = left.solve(right)

    basis: IntegerRows = []
    for free_index, free_column in enumerate(free_columns):
        vector_q: List[object] = [0] * ncols
        for pivot_index, pivot_column in enumerate(pivot_columns):
            vector_q[pivot_column] = solution[pivot_index, free_index]
        vector_q[free_column] = 1
        basis.append(rational_vector_to_primitive_integers(vector_q))
    return basis, selected_prime




def exact_right_nullspace_dixon_auto(
    rows: IntegerRows,
    ncols: int,
    pivot_primes: Sequence[int],
) -> tuple[IntegerRows, int, int]:
    """Construct and certify an exact nullspace without a prior nullity.

    A modular rank r supplies a nonzero r-by-r minor, hence rank_Q >= r.
    The exact Dixon solve constructs n-r independent null vectors, hence
    rank_Q <= r. Exact annihilation and independence are checked before return.
    """
    if len(rows) != ncols:
        raise ValueError("Dixon auto-nullspace currently requires a square matrix")
    if ncols == 0:
        return [], 0, 0

    selected_prime = None
    selected_rank = -1
    pivot_columns: List[int] = []
    pivot_rows: List[int] = []
    for prime in pivot_primes:
        candidate_columns, modular_rank = modular_rref_pivots(rows, prime)
        if modular_rank < selected_rank:
            continue
        if modular_rank == 0:
            candidate_rows: List[int] = []
            restricted_rank = 0
        else:
            restricted_transpose = [
                [int(rows[row][column]) for row in range(len(rows))]
                for column in candidate_columns
            ]
            candidate_rows, restricted_rank = modular_rref_pivots(
                restricted_transpose,
                prime,
            )
        if restricted_rank != modular_rank:
            continue
        if modular_rank > selected_rank:
            selected_prime = prime
            selected_rank = modular_rank
            pivot_columns = candidate_columns
            pivot_rows = candidate_rows

    if selected_prime is None or selected_rank < 0:
        raise RuntimeError(
            "no pivot prime produced a certifiable quotient rank; "
            f"tried {list(pivot_primes)}"
        )

    pivot_set = set(pivot_columns)
    free_columns = [column for column in range(ncols) if column not in pivot_set]
    if selected_rank == 0:
        basis = [
            [1 if column == free_column else 0 for column in range(ncols)]
            for free_column in free_columns
        ]
    else:
        pivot_block = [
            [int(rows[row][column]) for column in pivot_columns]
            for row in pivot_rows
        ]
        free_block_negative = [
            [-int(rows[row][column]) for column in free_columns]
            for row in pivot_rows
        ]
        left = fmpq_mat(pivot_block)
        right = fmpq_mat(free_block_negative)
        try:
            solution = left.solve(right, algorithm="dixon")
        except TypeError:
            solution = left.solve(right)

        basis = []
        for free_index, free_column in enumerate(free_columns):
            vector_q: List[object] = [0] * ncols
            for pivot_index, pivot_column in enumerate(pivot_columns):
                vector_q[pivot_column] = solution[pivot_index, free_index]
            vector_q[free_column] = 1
            basis.append(rational_vector_to_primitive_integers(vector_q))

    if any(not vector_annihilated(rows, vector) for vector in basis):
        raise RuntimeError("Dixon auto-nullspace produced a non-null vector")
    if basis and int(fmpz_mat(basis).rank()) != len(basis):
        raise RuntimeError("Dixon auto-nullspace basis is dependent")
    if selected_rank + len(basis) != ncols:
        raise RuntimeError("Dixon auto-nullspace rank-nullity mismatch")
    return basis, selected_prime, selected_rank

def matrix_rank_q(matrix: fmpq_mat) -> int:
    if int(matrix.nrows()) == 0 or int(matrix.ncols()) == 0:
        return 0
    numerator, _ = matrix.numer_denom()
    return int(numerator.rank())




def identity_q(size: int) -> fmpq_mat:
    result = fmpq_mat(size, size)
    for index in range(size):
        result[index, index] = 1
    return result




def matrix_hash_q(matrix: fmpq_mat) -> str:
    digest = hashlib.sha256()
    for i in range(int(matrix.nrows())):
        for j in range(int(matrix.ncols())):
            digest.update((str(matrix[i, j]) + ";").encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()




def stacked_fixed_dimension(
    representations: Sequence[fmpq_mat],
    dimension: int,
) -> int:
    if dimension == 0:
        return 0
    if not representations:
        return dimension
    identity = identity_q(dimension)
    rows = []
    for representation in representations:
        difference = representation - identity
        rows.extend([
            [difference[i, j] for j in range(dimension)]
            for i in range(dimension)
        ])
    return dimension - matrix_rank_q(fmpq_mat(rows))




def support_components(
    neighbors: Sequence[Sequence[int]],
    support: Set[int],
) -> int:
    if not support:
        return 0
    unseen = set(support)
    count = 0
    while unseen:
        count += 1
        start = unseen.pop()
        queue = [start]
        while queue:
            source = queue.pop()
            for target in neighbors[source]:
                if target in unseen:
                    unseen.remove(target)
                    queue.append(target)
    return count




def vector_support_stats(
    vector: Sequence[int],
    neighbors: Sequence[Sequence[int]],
) -> dict:
    support = {index for index, value in enumerate(vector) if value}
    positive = {index for index, value in enumerate(vector) if value > 0}
    negative = {index for index, value in enumerate(vector) if value < 0}
    support_edges = 0
    boundary_edges = 0
    same_sign_edges = 0
    opposite_sign_edges = 0
    for source, targets in enumerate(neighbors):
        for target in targets:
            if target <= source:
                continue
            source_active = source in support
            target_active = target in support
            if source_active and target_active:
                support_edges += 1
                if (source in positive and target in positive) or (
                    source in negative and target in negative
                ):
                    same_sign_edges += 1
                else:
                    opposite_sign_edges += 1
            elif source_active != target_active:
                boundary_edges += 1
    nonzero_values = [int(value) for value in vector if value]
    abs_values = [abs(value) for value in nonzero_values]
    return {
        "support_size": len(support),
        "support_fraction": Fraction(len(support), len(vector)),
        "positive_count": len(positive),
        "negative_count": len(negative),
        "zero_count": len(vector) - len(support),
        "l1_norm": sum(abs_values),
        "l2_norm_sq": sum(value * value for value in nonzero_values),
        "max_abs_coefficient": max(abs_values, default=0),
        "distinct_nonzero_coefficients": len(set(nonzero_values)),
        "support_component_count": support_components(neighbors, support),
        "support_edge_count": support_edges,
        "support_boundary_edge_count": boundary_edges,
        "same_sign_support_edges": same_sign_edges,
        "opposite_sign_support_edges": opposite_sign_edges,
        "constant_on_support": len(set(nonzero_values)) <= 1,
        "binary_sign_vector": set(nonzero_values).issubset({-1, 1}),
    }




def normalised_projective_column(column: Sequence[int]) -> Tuple[int, ...]:
    return tuple(primitive_integer_row(column))




def coordinate_pattern_stats(kernel_rows: IntegerRows, chamber_size: int) -> dict:
    if not kernel_rows:
        return {
            "active_coordinate_count": 0,
            "forced_zero_coordinate_count": chamber_size,
            "exact_column_pattern_count": 1 if chamber_size else 0,
            "projective_column_class_count": 1 if chamber_size else 0,
            "largest_exact_column_pattern_class": chamber_size,
            "largest_projective_column_class": chamber_size,
        }
    columns = [
        tuple(int(kernel_rows[row][column]) for row in range(len(kernel_rows)))
        for column in range(chamber_size)
    ]
    active = sum(any(value != 0 for value in column) for column in columns)
    exact_counts = Counter(columns)
    projective_counts = Counter(normalised_projective_column(column) for column in columns)
    return {
        "active_coordinate_count": active,
        "forced_zero_coordinate_count": chamber_size - active,
        "exact_column_pattern_count": len(exact_counts),
        "projective_column_class_count": len(projective_counts),
        "largest_exact_column_pattern_class": max(exact_counts.values(), default=0),
        "largest_projective_column_class": max(projective_counts.values(), default=0),
    }




def permutation_orbits(
    size: int,
    images: Sequence[Sequence[int]],
) -> List[List[int]]:
    parent = list(range(size))


    def find(value: int) -> int:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value


    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root


    for image in images:
        for source, target in enumerate(image):
            union(source, target)
    groups: Dict[int, List[int]] = defaultdict(list)
    for value in range(size):
        groups[find(value)].append(value)
    return sorted(groups.values(), key=lambda group: (group[0], len(group)))




def equitable_quotient(
    neighbors: Sequence[Sequence[int]],
    cells: Sequence[Sequence[int]],
) -> tuple[IntegerRows, bool, List[int]]:
    vertex_cell = [0] * len(neighbors)
    for cell_index, cell in enumerate(cells):
        for vertex in cell:
            vertex_cell[vertex] = cell_index
    quotient: IntegerRows = []
    equitable = True
    for cell in cells:
        reference = [0] * len(cells)
        for target in neighbors[cell[0]]:
            reference[vertex_cell[target]] += 1
        for vertex in cell[1:]:
            counts = [0] * len(cells)
            for target in neighbors[vertex]:
                counts[vertex_cell[target]] += 1
            equitable &= counts == reference
        quotient.append(reference)
    return quotient, equitable, vertex_cell




def lift_cell_vector(
    cell_vector: Sequence[int],
    vertex_cell: Sequence[int],
) -> List[int]:
    return [int(cell_vector[cell]) for cell in vertex_cell]




def colour_refinement_cells(
    neighbors: Sequence[Sequence[int]],
) -> List[List[int]]:
    colours = [len(targets) for targets in neighbors]
    while True:
        signatures = []
        for vertex, targets in enumerate(neighbors):
            neighbour_counts = Counter(colours[target] for target in targets)
            signatures.append((colours[vertex], tuple(sorted(neighbour_counts.items()))))
        mapping = {
            signature: colour
            for colour, signature in enumerate(sorted(set(signatures), key=str))
        }
        updated = [mapping[signature] for signature in signatures]
        if updated == colours:
            break
        colours = updated
    cells: Dict[int, List[int]] = defaultdict(list)
    for vertex, colour in enumerate(colours):
        cells[colour].append(vertex)
    return sorted(cells.values(), key=lambda cell: cell[0])




def regime_summary_rows(channel_rows: Sequence[Mapping[str, object]]) -> List[dict]:
    result: List[dict] = []
    numeric_fields = (
        "chamber_adjacency_nullity",
        "active_coordinate_count",
        "forced_zero_coordinate_count",
        "canonical_basis_support_min",
        "canonical_basis_support_max",
        "canonical_basis_support_mean",
        "label_automorphism_group_order",
        "kernel_representation_image_order",
        "kernel_group_fixed_dimension",
        "automorphism_orbit_count",
        "orbit_constant_kernel_dimension",
        "maximum_involution_anti_fixed_dimension",
        "wl_cell_count",
        "wl_constant_kernel_dimension",
    )
    for regime in ("null", "mixed"):
        members = [row for row in channel_rows if row["regime"] == regime]
        for field in numeric_fields:
            values = [parse_number(row.get(field)) for row in members]
            typed = [value for value in values if isinstance(value, (int, Fraction))]
            if not typed:
                continue
            result.append({
                "regime": regime,
                "feature": field,
                "channel_count": len(members),
                "minimum": serialise_number(min(typed)),
                "maximum": serialise_number(max(typed)),
                "mean": serialise_number(
                    sum(Fraction(value) for value in typed) / len(typed)
                ),
                "subsets": ";".join(str(row["subset"]) for row in members),
            })
    return result




def growth_feature_map(row: Mapping[str, object]) -> Dict[str, int | Fraction]:
    columns = (
        "initial_increment",
        "final_increment",
        "penultimate_increment",
        "tail3_increment_sum",
        "peak_increment",
        "growth_after_seed",
        "maximum_depth",
        "active_depth_count",
        "mean_basis_depth",
        "initial_fraction_of_closure",
        "depths_contiguous",
    )
    output: Dict[str, int | Fraction] = {}
    for column in columns:
        value = parse_number(row.get(column))
        if value is not None:
            output[f"growth_{column}"] = value
    return output




def apply_operator(
    value: int | Fraction,
    operator: str,
    threshold: int | Fraction,
) -> bool:
    if operator == "==":
        return value == threshold
    if operator == "<=":
        return value <= threshold
    if operator == ">=":
        return value >= threshold
    raise ValueError(operator)




def parse_pair_expression(expression: str) -> dict:
    match = PAIR_PATTERN.match(expression.strip())
    if match is None:
        raise ValueError(f"unsupported pair expression: {expression}")
    groups = match.groupdict()
    if bool(groups["neg"]) != bool(groups["close"]):
        raise ValueError(f"malformed NOT pair expression: {expression}")
    threshold1 = parse_number(groups["t1"])
    threshold2 = parse_number(groups["t2"])
    if threshold1 is None or threshold2 is None:
        raise ValueError(f"non-numeric pair threshold: {expression}")
    return {
        "negated": bool(groups["neg"]),
        "feature1": groups["f1"],
        "operator1": groups["o1"],
        "threshold1": threshold1,
        "join": groups["join"],
        "feature2": groups["f2"],
        "operator2": groups["o2"],
        "threshold2": threshold2,
    }




def evaluate_pair_expression(
    expression: str,
    features: Mapping[str, int | Fraction],
) -> bool:
    parsed = parse_pair_expression(expression)
    left = apply_operator(
        features[parsed["feature1"]],
        parsed["operator1"],
        parsed["threshold1"],
    )
    right = apply_operator(
        features[parsed["feature2"]],
        parsed["operator2"],
        parsed["threshold2"],
    )
    value = left and right if parsed["join"] == "AND" else left or right
    return not value if parsed["negated"] else value




def sympy_fraction(value: sp.Rational) -> Fraction:
    return Fraction(int(value.p), int(value.q))




def fit_unique_recurrence(
    sequence: Sequence[int],
    order: int,
    window: int,
) -> List[Fraction] | None:
    if order <= 0 or len(sequence) < 2 * order + 1:
        return None
    start = max(order, len(sequence) - window)
    rows = []
    targets = []
    for index in range(start, len(sequence)):
        rows.append([
            sp.Rational(sequence[index - lag])
            for lag in range(1, order + 1)
        ])
        targets.append(sp.Rational(sequence[index]))
    matrix = sp.Matrix(rows)
    target = sp.Matrix(targets)
    if matrix.rank() < order:
        return None
    solutions = list(sp.linsolve((matrix, target)))
    if len(solutions) != 1:
        return None
    solution = solutions[0]
    if any(value.free_symbols for value in solution):
        return None
    coefficients = [sympy_fraction(value) for value in solution]
    for index in range(start, len(sequence)):
        predicted = sum(
            coefficients[lag - 1] * sequence[index - lag]
            for lag in range(1, order + 1)
        )
        if predicted != sequence[index]:
            return None
    return coefficients




def recurrence_prediction_rows(
    subset: str,
    regime: str,
    sequence_name: str,
    sequence: Sequence[int],
    max_order: int,
    window: int,
) -> List[dict]:
    rows: List[dict] = []
    for holdout_count in (1, 3):
        if len(sequence) <= holdout_count + 2:
            continue
        training = list(sequence[:-holdout_count])
        actual = list(sequence[-holdout_count:])
        for order in range(1, max_order + 1):
            coefficients = fit_unique_recurrence(training, order, window)
            if coefficients is None:
                continue
            generated = list(training)
            predictions: List[Fraction] = []
            for _ in range(holdout_count):
                predicted = sum(
                    coefficients[lag - 1] * generated[-lag]
                    for lag in range(1, order + 1)
                )
                predictions.append(predicted)
                generated.append(predicted)
            exact_steps = sum(
                prediction == target
                for prediction, target in zip(predictions, actual)
            )
            rows.append({
                "subset": subset,
                "regime": regime,
                "sequence": sequence_name,
                "holdout_count": holdout_count,
                "order": order,
                "coefficients": ";".join(map(str, coefficients)),
                "predictions": ";".join(map(str, predictions)),
                "actual": ";".join(map(str, actual)),
                "exact_steps": exact_steps,
                "all_exact": exact_steps == holdout_count,
                "training_length": len(training),
                "window": window,
            })
    return rows




def self_test() -> None:
    matrix = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
    kernel = [[0, 1, -1]]
    assert vector_annihilated(matrix, kernel[0])
    stats = vector_support_stats(kernel[0], [[1, 2], [0], [0]])
    assert stats["support_size"] == 2
    assert stats["opposite_sign_support_edges"] == 0


    cells = [[0], [1, 2]]
    quotient, equitable, vertex_cell = equitable_quotient(
        [[1, 2], [0], [0]], cells
    )
    assert equitable
    assert quotient == [[0, 2], [1, 0]]
    assert lift_cell_vector([3, 4], vertex_cell) == [3, 4, 4]


    features = {"growth_maximum_depth": 10, "growth_tail3_increment_sum": 2}
    expression = (
        "(growth_maximum_depth >= 8) AND "
        "(growth_tail3_increment_sum <= 3)"
    )
    assert evaluate_pair_expression(expression, features)


    coefficients = fit_unique_recurrence([1, 2, 4, 8, 16], 1, 10)
    assert coefficients == [Fraction(2, 1)]

    fast_kernel, used_prime = exact_right_nullspace_dixon(
        matrix, 3, 1, [1000003]
    )
    assert used_prime == 1000003
    assert len(fast_kernel) == 1
    assert vector_annihilated(matrix, fast_kernel[0])

    auto_kernel, auto_prime, auto_rank = exact_right_nullspace_dixon_auto(
        matrix, 3, [1000003]
    )
    assert auto_prime == 1000003
    assert auto_rank == 2
    assert len(auto_kernel) == 1
    assert vector_annihilated(matrix, auto_kernel[0])
    print("EHF-XBR-04F6 self-test PASS")




def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit global chamber zero modes and Krylov saturation structure."
    )
    parser.add_argument("--xbr04f3-dir")
    parser.add_argument("--xbr04f5-dir")
    parser.add_argument("--xbr04c-dir")
    parser.add_argument("--xbr04d-script")
    parser.add_argument("--xbr04f-script")
    parser.add_argument("--xbr04f5-script")
    parser.add_argument("--opw-base-script")
    parser.add_argument("--amp-base-script")
    parser.add_argument("--amp-rank-script")
    parser.add_argument(
        "--write-kernel-bases",
        choices=("none", "sparse"),
        default="sparse",
    )
    parser.add_argument(
        "--kernel-backend",
        choices=("dixon", "rref"),
        default="dixon",
        help=(
            "exact chamber-kernel backend; dixon uses modular pivots plus an "
            "exact multi-RHS rational solve and is the default"
        ),
    )
    parser.add_argument(
        "--pivot-primes",
        default="1000003,1000033,1000037,1000039,1000081",
        help="comma-separated primes used only to discover a full-rank pivot block",
    )
    parser.add_argument("--pair-search-limit", type=int, default=5000)
    parser.add_argument("--recurrence-max-order", type=int, default=3)
    parser.add_argument("--recurrence-window", type=int, default=16)
    parser.add_argument("--out-dir", default="runs/ehf_xbr_04f6")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()


    if args.self_test:
        self_test()
        return 0


    required_names = (
        "xbr04f3_dir",
        "xbr04f5_dir",
        "xbr04c_dir",
        "xbr04d_script",
        "xbr04f_script",
        "xbr04f5_script",
        "opw_base_script",
        "amp_base_script",
        "amp_rank_script",
    )
    missing = [name for name in required_names if not getattr(args, name)]
    if missing:
        parser.error("missing required arguments: " + ", ".join(missing))
    if args.pair_search_limit <= 0:
        parser.error("--pair-search-limit must be positive")
    if args.recurrence_max_order <= 0:
        parser.error("--recurrence-max-order must be positive")
    if args.recurrence_window <= 0:
        parser.error("--recurrence-window must be positive")
    try:
        pivot_primes = [
            int(value.strip())
            for value in args.pivot_primes.split(",")
            if value.strip()
        ]
    except ValueError as exc:
        parser.error(f"invalid --pivot-primes: {exc}")
    if not pivot_primes or any(value <= 2 for value in pivot_primes):
        parser.error("--pivot-primes must contain positive odd primes")


    started = time.perf_counter()
    f3_dir = Path(args.xbr04f3_dir).resolve()
    f5_dir = Path(args.xbr04f5_dir).resolve()
    c_dir = Path(args.xbr04c_dir).resolve()
    xbr04d_path = Path(args.xbr04d_script).resolve()
    xbr04f_path = Path(args.xbr04f_script).resolve()
    xbr04f5_path = Path(args.xbr04f5_script).resolve()
    opw_path = Path(args.opw_base_script).resolve()
    amp_base_path = Path(args.amp_base_script).resolve()
    amp_rank_path = Path(args.amp_rank_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    channel_root = out_dir / "channels"
    out_dir.mkdir(parents=True, exist_ok=True)
    channel_root.mkdir(parents=True, exist_ok=True)


    required_paths = (
        f3_dir / "classification_ledger.csv",
        f3_dir / "run_summary.json",
        f5_dir / "run_summary.json",
        f5_dir / "chamber_mechanism_ledger.csv",
        f5_dir / "krylov_growth_ledger.csv",
        f5_dir / "krylov_growth_by_depth.csv",
        f5_dir / "mechanism_exact_pair_proxies.csv",
        c_dir / "run_summary.json",
        xbr04d_path,
        xbr04f_path,
        xbr04f5_path,
        opw_path,
        amp_base_path,
        amp_rank_path,
    )
    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(path)


    xbr04d = load_module(xbr04d_path, "ehf_xbr_04f6_xbr04d")
    xbr04f = load_module(xbr04f_path, "ehf_xbr_04f6_xbr04f")
    xbr04f5 = load_module(xbr04f5_path, "ehf_xbr_04f6_xbr04f5")
    opw = load_module(opw_path, "ehf_xbr_04f6_opw")
    amp_base = load_module(amp_base_path, "ehf_xbr_04f6_amp_base")
    amp_rank = load_module(amp_rank_path, "ehf_xbr_04f6_amp_rank")


    f3_summary = read_json(f3_dir / "run_summary.json")
    f5_summary = read_json(f5_dir / "run_summary.json")
    c_summary = read_json(c_dir / "run_summary.json")
    proper_rows = read_csv(f3_dir / "classification_ledger.csv")
    proper_rows.sort(key=lambda row: parse_subset(row["subset"]))
    singular_rows = [
        row for row in proper_rows if integer(row, "chamber_adjacency_nullity") > 0
    ]
    regime_counts = Counter(row["regime"] for row in proper_rows)


    growth_rows = read_csv(f5_dir / "krylov_growth_ledger.csv")
    depth_rows = read_csv(f5_dir / "krylov_growth_by_depth.csv")
    depth_by_subset: Dict[str, List[dict]] = defaultdict(list)
    for row in depth_rows:
        depth_by_subset[row["subset"]].append(row)
    for subset in depth_by_subset:
        depth_by_subset[subset].sort(key=lambda row: integer(row, "depth"))


    source_pair_rows = [
        row
        for row in read_csv(f5_dir / "mechanism_exact_pair_proxies.csv")
        if row.get("feature_set") == "krylov_growth"
        and row.get("target") in {"small_complement", "null_regime"}
    ]


    cycles9 = opw.generate_cycles(9)
    index9 = {cycle: index for index, cycle in enumerate(cycles9)}
    pi9 = [opw.pi_label(cycle) for cycle in cycles9]
    graph9 = opw.build_preserve_graph(
        cycles9,
        index9,
        pi9,
        "OPW3",
        opw.GRAPH_LENGTHS["OPW3"],
    )
    source_fibres = amp_base.fibres(9)


    print("=" * 132)
    print("EHF-XBR-04F6: GLOBAL ZERO-MODE AND KRYLOV-SATURATION STRUCTURE AUDIT")
    print("=" * 132)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"XBR-04F3 directory:   {f3_dir}")
    print(f"XBR-04F5 directory:   {f5_dir}")
    print(f"proper channels:      {len(proper_rows)}")
    print(f"singular channels:    {len(singular_rows)}")
    print(
        "regimes:             "
        f"null={regime_counts['null']} mixed={regime_counts['mixed']} "
        f"invertible={regime_counts['invertible']}"
    )
    print(f"source pair rules:    {len(source_pair_rows)}")
    print(f"write kernel bases:   {args.write_kernel_bases}")
    print(f"kernel backend:       {args.kernel_backend}")
    print(f"pivot primes:         {','.join(map(str, pivot_primes))}")
    print(f"output directory:     {out_dir}")
    print(f"strict:               {args.strict}")
    print()


    channel_rows_out: List[dict] = []
    vector_rows_out: List[dict] = []
    symmetry_rows_out: List[dict] = []
    quotient_rows_out: List[dict] = []


    all_kernel_dimensions_match = True
    all_kernel_vectors_exact = True
    all_symmetry_groups_exact = True
    all_representations_exact = True
    all_orbit_partitions_equitable = True
    all_orbit_lifts_exact = True
    all_fixed_dimensions_match_quotient = True
    all_wl_partitions_equitable = True


    for number, source in enumerate(singular_rows, start=1):
        channel_started = time.perf_counter()
        subset = parse_subset(source["subset"])
        subset_key = subset_text(subset)
        chamber_size = integer(source, "source_chamber_size")
        expected_nullity = integer(source, "chamber_adjacency_nullity")


        source_key = amp_rank.key_from_subset_9(subset)
        source_cycles = source_fibres[source_key]
        global_ids = [
            index9[tuple(label - 1 for label in cycle)]
            for cycle in source_cycles
        ]
        neighbors = xbr04f5.local_neighbors(graph9.adjacency, global_ids)
        matrix_rows = xbr04f5.adjacency_rows(neighbors)


        print(
            f"[kernel {number}/{len(singular_rows)}] A={subset} "
            f"phase=nullspace backend={args.kernel_backend} size={chamber_size} "
            f"nullity={expected_nullity}",
            flush=True,
        )
        nullspace_started = time.perf_counter()
        if args.kernel_backend == "dixon":
            kernel_rows, selected_prime = exact_right_nullspace_dixon(
                matrix_rows,
                chamber_size,
                expected_nullity,
                pivot_primes,
            )
        else:
            kernel_rows = [
                primitive_integer_row(row)
                for row in xbr04d.integer_right_nullspace(
                    matrix_rows, chamber_size, "flint"
                )
            ]
            selected_prime = 0
        print(
            f"[kernel {number}/{len(singular_rows)}] A={subset} "
            f"phase=nullspace_done basis={len(kernel_rows)} "
            f"pivot_prime={selected_prime or 'n/a'} "
            f"elapsed={time.perf_counter() - nullspace_started:.2f}s",
            flush=True,
        )
        kernel_rank = xbr04d.exact_rank(kernel_rows, "flint")
        dimension_match = (
            len(kernel_rows) == expected_nullity
            and kernel_rank == expected_nullity
        )
        vectors_exact = all(
            vector_annihilated(matrix_rows, vector)
            for vector in kernel_rows
        )
        all_kernel_dimensions_match &= dimension_match
        all_kernel_vectors_exact &= vectors_exact


        if args.write_kernel_bases == "sparse":
            write_sparse_integer_matrix(
                channel_root / subset_slug(subset) / "kernel_basis.coordinate.json.gz",
                kernel_rows,
            )


        vector_supports: List[int] = []
        for vector_index, vector in enumerate(kernel_rows):
            stats = vector_support_stats(vector, neighbors)
            vector_supports.append(int(stats["support_size"]))
            vector_rows_out.append({
                "subset": subset_key,
                "regime": source["regime"],
                "kernel_vector_index": vector_index,
                **{
                    key: serialise_number(value)
                    for key, value in stats.items()
                },
            })


        coordinate_stats = coordinate_pattern_stats(kernel_rows, chamber_size)
        pivots = row_basis_pivots(kernel_rows)
        solve_kernel = xbr04f.complement_coordinate_solver(kernel_rows, pivots)


        print(
            f"[kernel {number}/{len(singular_rows)}] A={subset} phase=symmetry_scan",
            flush=True,
        )
        candidates = xbr04f.candidate_stabilizer_permutations(subset)
        graph_automorphisms: Set[Permutation] = set()
        graph_images: Dict[Permutation, List[int]] = {}
        for candidate in candidates:
            image = xbr04f.chamber_state_permutation(
                candidate, global_ids, cycles9, index9
            )
            if (
                image is not None
                and xbr04f.adjacency_automorphism_exact(image, neighbors)
            ):
                graph_automorphisms.add(candidate)
                graph_images[candidate] = image


        print(
            f"[kernel {number}/{len(singular_rows)}] A={subset} "
            f"phase=symmetry_scan_done automorphisms={len(graph_automorphisms)}",
            flush=True,
        )
        group_exact = xbr04f.group_axioms_exact(graph_automorphisms)
        generators = xbr04f.greedy_group_generators(graph_automorphisms)
        generator_closure_exact = (
            xbr04f.group_closure(generators) == graph_automorphisms
        )
        all_symmetry_groups_exact &= group_exact and generator_closure_exact


        representations: List[fmpq_mat] = []
        representation_hashes: Set[str] = set()
        representation_kernel_size = 0
        maximum_anti_fixed = 0
        involution_count = 0
        identity_matrix = identity_q(expected_nullity)


        for candidate in sorted(
            graph_automorphisms,
            key=xbr04f.permutation_cycle_text,
        ):
            transformed = xbr04f.permute_coordinate_rows(
                kernel_rows, graph_images[candidate]
            )
            representation, exact = solve_kernel(transformed)
            order = xbr04f.permutation_order(candidate)
            order_exact = exact and xbr04f.matrix_power(
                representation, order
            ) == identity_matrix
            fixed_dimension = (
                expected_nullity
                - matrix_rank_q(representation - identity_matrix)
                if exact else -1
            )
            anti_fixed_dimension: int | str = ""
            if exact and order == 2:
                involution_count += 1
                anti_fixed_dimension = (
                    expected_nullity
                    - matrix_rank_q(representation + identity_matrix)
                )
                maximum_anti_fixed = max(
                    maximum_anti_fixed, int(anti_fixed_dimension)
                )
            representation_hash = matrix_hash_q(representation) if exact else ""
            if exact:
                representations.append(representation)
                representation_hashes.add(representation_hash)
                representation_kernel_size += int(representation == identity_matrix)
            all_representations_exact &= exact and order_exact
            symmetry_rows_out.append({
                "subset": subset_key,
                "regime": source["regime"],
                "label_permutation": xbr04f.permutation_cycle_text(candidate),
                "label_permutation_order": order,
                "representation_exact": exact,
                "representation_order_exact": order_exact,
                "representation_trace": (
                    str(sum(representation[i, i] for i in range(expected_nullity)))
                    if exact else ""
                ),
                "fixed_space_dimension": fixed_dimension,
                "anti_fixed_space_dimension": anti_fixed_dimension,
                "acts_trivially_on_kernel": exact and representation == identity_matrix,
                "representation_hash": representation_hash,
            })


        group_fixed_dimension = stacked_fixed_dimension(
            representations, expected_nullity
        )


        orbit_cells = permutation_orbits(
            chamber_size,
            list(graph_images.values()),
        )
        orbit_quotient, orbit_equitable, orbit_vertex_cell = equitable_quotient(
            neighbors, orbit_cells
        )
        orbit_discrete = len(orbit_cells) == chamber_size
        print(
            f"[kernel {number}/{len(singular_rows)}] A={subset} "
            f"phase=orbit_quotient cells={len(orbit_cells)} "
            f"discrete={orbit_discrete} expected_nullity={group_fixed_dimension}",
            flush=True,
        )
        orbit_started = time.perf_counter()
        if orbit_discrete:
            orbit_kernel = kernel_rows
            orbit_prime = selected_prime
            orbit_rank = chamber_size - expected_nullity
        else:
            orbit_kernel, orbit_prime = exact_right_nullspace_dixon(
                orbit_quotient,
                len(orbit_cells),
                group_fixed_dimension,
                pivot_primes,
            )
            orbit_rank = len(orbit_cells) - len(orbit_kernel)
        orbit_lifts_exact = all(
            vector_annihilated(
                matrix_rows,
                lift_cell_vector(vector, orbit_vertex_cell),
            )
            for vector in orbit_kernel
        )
        orbit_constant_dimension = len(orbit_kernel)
        fixed_matches_quotient = (
            group_fixed_dimension == orbit_constant_dimension
        )
        print(
            f"[kernel {number}/{len(singular_rows)}] A={subset} "
            f"phase=orbit_quotient_done rank={orbit_rank} "
            f"nullity={orbit_constant_dimension} pivot_prime={orbit_prime or 'reused'} "
            f"elapsed={time.perf_counter() - orbit_started:.2f}s",
            flush=True,
        )
        all_orbit_partitions_equitable &= orbit_equitable
        all_orbit_lifts_exact &= orbit_lifts_exact
        all_fixed_dimensions_match_quotient &= fixed_matches_quotient


        quotient_rows_out.append({
            "subset": subset_key,
            "regime": source["regime"],
            "partition": "label_automorphism_orbits",
            "cell_count": len(orbit_cells),
            "cell_sizes": ";".join(map(str, sorted(map(len, orbit_cells)))),
            "equitable": orbit_equitable,
            "quotient_discrete": orbit_discrete,
            "quotient_backend": "reused_chamber_kernel" if orbit_discrete else "dixon",
            "quotient_pivot_prime": orbit_prime,
            "quotient_rank": orbit_rank,
            "quotient_nullity": orbit_constant_dimension,
            "lifted_kernel_vectors_exact": orbit_lifts_exact,
            "matches_group_fixed_dimension": fixed_matches_quotient,
        })


        wl_cells = colour_refinement_cells(neighbors)
        wl_quotient, wl_equitable, wl_vertex_cell = equitable_quotient(
            neighbors, wl_cells
        )
        wl_discrete = len(wl_cells) == chamber_size
        print(
            f"[kernel {number}/{len(singular_rows)}] A={subset} "
            f"phase=colour_refinement_quotient cells={len(wl_cells)} "
            f"discrete={wl_discrete}",
            flush=True,
        )
        wl_started = time.perf_counter()
        if wl_discrete:
            wl_kernel = kernel_rows
            wl_prime = selected_prime
            wl_rank = chamber_size - expected_nullity
        else:
            wl_kernel, wl_prime, wl_rank = exact_right_nullspace_dixon_auto(
                wl_quotient,
                len(wl_cells),
                pivot_primes,
            )
        wl_lifts_exact = all(
            vector_annihilated(
                matrix_rows,
                lift_cell_vector(vector, wl_vertex_cell),
            )
            for vector in wl_kernel
        )
        print(
            f"[kernel {number}/{len(singular_rows)}] A={subset} "
            f"phase=colour_refinement_quotient_done rank={wl_rank} "
            f"nullity={len(wl_kernel)} pivot_prime={wl_prime or 'reused'} "
            f"elapsed={time.perf_counter() - wl_started:.2f}s",
            flush=True,
        )
        all_wl_partitions_equitable &= wl_equitable
        quotient_rows_out.append({
            "subset": subset_key,
            "regime": source["regime"],
            "partition": "degree_colour_refinement",
            "cell_count": len(wl_cells),
            "cell_sizes": ";".join(map(str, sorted(map(len, wl_cells)))),
            "equitable": wl_equitable,
            "quotient_discrete": wl_discrete,
            "quotient_backend": "reused_chamber_kernel" if wl_discrete else "dixon_auto",
            "quotient_pivot_prime": wl_prime,
            "quotient_rank": wl_rank,
            "quotient_nullity": len(wl_kernel),
            "lifted_kernel_vectors_exact": wl_lifts_exact,
            "matches_group_fixed_dimension": "",
        })


        channel_row = {
            "subset": subset_key,
            "regime": source["regime"],
            "source_chamber_size": chamber_size,
            "chamber_adjacency_nullity": expected_nullity,
            "kernel_basis_dimension": len(kernel_rows),
            "kernel_basis_rank": kernel_rank,
            "kernel_dimension_matches_ledger": dimension_match,
            "all_kernel_basis_vectors_annihilated": vectors_exact,
            "kernel_basis_sha256": sha256_integer_rows(kernel_rows),
            "kernel_backend": args.kernel_backend,
            "kernel_pivot_prime": selected_prime,
            "canonical_basis_support_min": min(vector_supports, default=0),
            "canonical_basis_support_max": max(vector_supports, default=0),
            "canonical_basis_support_mean": serialise_number(
                Fraction(sum(vector_supports), len(vector_supports))
                if vector_supports else Fraction(0, 1)
            ),
            **coordinate_stats,
            "candidate_label_stabilizer_order": len(candidates),
            "label_automorphism_group_order": len(graph_automorphisms),
            "label_automorphism_generator_count": len(generators),
            "label_automorphism_group_exact": group_exact,
            "generator_closure_exact": generator_closure_exact,
            "kernel_representation_exact": all(
                truthy(row["representation_exact"])
                for row in symmetry_rows_out
                if row["subset"] == subset_key
            ),
            "kernel_representation_image_order": len(representation_hashes),
            "kernel_representation_kernel_size": representation_kernel_size,
            "kernel_group_fixed_dimension": group_fixed_dimension,
            "involution_count": involution_count,
            "maximum_involution_anti_fixed_dimension": maximum_anti_fixed,
            "has_full_sign_involution": maximum_anti_fixed == expected_nullity,
            "automorphism_orbit_count": len(orbit_cells),
            "orbit_constant_kernel_dimension": orbit_constant_dimension,
            "all_kernel_orbit_constant": orbit_constant_dimension == expected_nullity,
            "orbit_partition_equitable": orbit_equitable,
            "orbit_quotient_lifts_exact": orbit_lifts_exact,
            "group_fixed_equals_orbit_quotient_nullity": fixed_matches_quotient,
            "wl_cell_count": len(wl_cells),
            "wl_constant_kernel_dimension": len(wl_kernel),
            "wl_partition_equitable": wl_equitable,
            "wl_quotient_lifts_exact": wl_lifts_exact,
            "elapsed_seconds": time.perf_counter() - channel_started,
        }
        channel_rows_out.append(channel_row)
        write_json(
            channel_root / subset_slug(subset) / "certificate.json",
            {
                "probe": "EHF-XBR-04F6",
                "script_version": SCRIPT_VERSION,
                "utc_completed": utc_now(),
                "subset": list(subset),
                "channel_row": channel_row,
            },
        )


        print(
            f"[kernel {number}/{len(singular_rows)}] A={subset} "
            f"regime={source['regime']} nullity={expected_nullity} "
            f"support={channel_row['canonical_basis_support_min']}.."
            f"{channel_row['canonical_basis_support_max']} "
            f"aut={len(graph_automorphisms)} image={len(representation_hashes)} "
            f"fixed={group_fixed_dimension} orbit0={orbit_constant_dimension} "
            f"anti_max={maximum_anti_fixed} "
            f"pass={dimension_match and vectors_exact and orbit_lifts_exact} "
            f"elapsed={time.perf_counter() - channel_started:.2f}s"
        )


    write_csv(out_dir / "kernel_channel_ledger.csv", channel_rows_out)
    write_csv(out_dir / "kernel_vector_ledger.csv", vector_rows_out)
    write_csv(out_dir / "kernel_symmetry_ledger.csv", symmetry_rows_out)
    write_csv(out_dir / "kernel_quotient_ledger.csv", quotient_rows_out)
    write_csv(
        out_dir / "kernel_regime_summary.csv",
        regime_summary_rows(channel_rows_out),
    )


    growth_records: List[dict] = []
    for row in growth_rows:
        source = next(
            item for item in proper_rows if item["subset"] == row["subset"]
        )
        growth_records.append({
            "subset": row["subset"],
            "regime": source["regime"],
            "features": growth_feature_map(row),
            "targets": {
                "null_regime": source["regime"] == "null",
                "small_complement": integer(source, "complement_dimension") <= 10,
            },
        })


    pair_rule_rows: List[dict] = []
    all_source_pair_rules_exact = True
    for source_rule in source_pair_rows:
        expression = source_rule["expression"]
        target = source_rule["target"]
        correct = 0
        predictions = []
        for record in growth_records:
            predicted = evaluate_pair_expression(
                expression, record["features"]
            )
            actual = bool(record["targets"][target])
            correct += int(predicted == actual)
            predictions.append(
                f"{record['subset']}:{int(predicted)}"
            )
        exact = correct == len(growth_records)
        all_source_pair_rules_exact &= exact
        parsed = parse_pair_expression(expression)
        pair_rule_rows.append({
            **source_rule,
            "full_census_correct": correct,
            "full_census_total": len(growth_records),
            "full_census_exact": exact,
            "feature1": parsed["feature1"],
            "feature2": parsed["feature2"],
            "predictions": ";".join(predictions),
        })
    pair_rule_rows.sort(
        key=lambda row: (
            row["target"],
            int(row.get("distinct_features", 9)),
            int(row.get("character_count", 9999)),
            row["expression"],
        )
    )
    write_csv(out_dir / "krylov_pair_rule_ledger.csv", pair_rule_rows)


    loo_rows: List[dict] = []
    for held_index, held in enumerate(growth_records):
        training = [
            record for index, record in enumerate(growth_records)
            if index != held_index
        ]
        feature_names = sorted(held["features"])
        predicates = xbr04f5.build_predicates(training, feature_names)
        candidates = xbr04f5.exact_pair_proxies(
            training,
            predicates,
            "null_regime",
            limit=args.pair_search_limit,
        )
        if not candidates:
            loo_rows.append({
                "held_out_subset": held["subset"],
                "held_out_regime": held["regime"],
                "status": "no_exact_training_pair_rule",
                "predicate_count": len(predicates),
            })
            continue
        primary = (
            int(candidates[0]["distinct_features"]),
            int(candidates[0]["character_count"]),
        )
        ties = [
            row for row in candidates
            if (
                int(row["distinct_features"]),
                int(row["character_count"]),
            ) == primary
        ]
        tie_predictions = Counter(
            evaluate_pair_expression(row["expression"], held["features"])
            for row in ties
        )
        chosen = sorted(ties, key=lambda row: row["expression"])[0]
        predicted = evaluate_pair_expression(
            chosen["expression"], held["features"]
        )
        actual = bool(held["targets"]["null_regime"])
        loo_rows.append({
            "held_out_subset": held["subset"],
            "held_out_regime": held["regime"],
            "status": "completed",
            "predicate_count": len(predicates),
            "exact_training_pair_rule_count": len(candidates),
            "minimum_distinct_features": primary[0],
            "minimum_character_count": primary[1],
            "minimum_tie_count": len(ties),
            "minimum_tie_consensus": len(tie_predictions) == 1,
            "minimum_tie_prediction_counts": json.dumps(
                {str(key): value for key, value in tie_predictions.items()},
                sort_keys=True,
            ),
            "chosen_prediction_null": predicted,
            "actual_null": actual,
            "chosen_correct": predicted == actual,
            "chosen_expression": chosen["expression"],
        })
    write_csv(out_dir / "krylov_pair_loo.csv", loo_rows)


    curve_rows: List[dict] = []
    recurrence_rows: List[dict] = []
    all_curves_reconstruct = True
    for source in proper_rows:
        subset_key = source["subset"]
        channel_depth_rows = depth_by_subset[subset_key]
        increments = [
            integer(row, "new_independent_directions")
            for row in channel_depth_rows
        ]
        cumulative = [
            integer(row, "cumulative_closure_dimension")
            for row in channel_depth_rows
        ]
        residuals = [
            integer(row, "remaining_chamber_codimension")
            for row in channel_depth_rows
        ]
        closure_dimension = integer(source, "closure_dimension")
        complement_dimension = integer(source, "complement_dimension")
        reconstructs = (
            bool(cumulative)
            and cumulative[-1] == closure_dimension
            and residuals[-1] == complement_dimension
        )
        all_curves_reconstruct &= reconstructs
        for row in channel_depth_rows:
            curve_rows.append({
                "subset": subset_key,
                "regime": source["regime"],
                "closure_dimension": closure_dimension,
                "complement_dimension": complement_dimension,
                "curve_reconstructs_final_dimensions": reconstructs,
                **row,
            })
        recurrence_rows.extend(
            recurrence_prediction_rows(
                subset_key,
                source["regime"],
                "growth_increment",
                increments,
                args.recurrence_max_order,
                args.recurrence_window,
            )
        )
        recurrence_rows.extend(
            recurrence_prediction_rows(
                subset_key,
                source["regime"],
                "remaining_codimension",
                residuals,
                args.recurrence_max_order,
                args.recurrence_window,
            )
        )


    write_csv(out_dir / "krylov_cumulative_curves.csv", curve_rows)
    write_csv(out_dir / "krylov_recurrence_audit.csv", recurrence_rows)


    loo_completed = [row for row in loo_rows if row["status"] == "completed"]
    loo_correct = sum(truthy(row.get("chosen_correct")) for row in loo_completed)
    loo_consensus = sum(
        truthy(row.get("minimum_tie_consensus")) for row in loo_completed
    )
    recurrence_exact = sum(truthy(row["all_exact"]) for row in recurrence_rows)


    checks: Dict[str, bool] = {
        "source_f3_verdict_pass": (
            f3_summary.get("verdict")
            == "EHF_XBR_04F3_INVISIBLE_ACTION_RANK_NULLITY_CLASSIFICATION_PASS"
        ),
        "source_f5_verdict_pass": (
            f5_summary.get("verdict")
            == "EHF_XBR_04F5_CHAMBER_SINGULARITY_COMPLEMENT_DIMENSION_MECHANISM_AUDIT_PASS"
        ),
        "source_xbr04c_summary_pass": bool(c_summary.get("strict_pass")),
        "proper_channel_count_20": len(proper_rows) == 20,
        "singular_channel_count_11": len(singular_rows) == 11,
        "regime_counts_3_8_9": (
            regime_counts["null"] == 3
            and regime_counts["mixed"] == 8
            and regime_counts["invertible"] == 9
        ),
        "all_kernel_dimensions_match_ledger": all_kernel_dimensions_match,
        "all_kernel_basis_vectors_exact": all_kernel_vectors_exact,
        "all_label_symmetry_groups_exact": all_symmetry_groups_exact,
        "all_kernel_symmetry_representations_exact": all_representations_exact,
        "all_automorphism_orbit_partitions_equitable": all_orbit_partitions_equitable,
        "all_automorphism_quotient_kernel_lifts_exact": all_orbit_lifts_exact,
        "all_group_fixed_dimensions_match_orbit_quotients": all_fixed_dimensions_match_quotient,
        "all_colour_refinement_partitions_equitable": all_wl_partitions_equitable,
        "source_krylov_pair_rules_present": bool(source_pair_rows),
        "all_source_krylov_pair_rules_exact": all_source_pair_rules_exact,
        "all_20_pair_rule_loo_folds_audited": len(loo_rows) == 20,
        "all_krylov_curves_reconstruct_final_dimensions": all_curves_reconstruct,
        "recurrence_audit_nonempty": bool(recurrence_rows),
    }
    strict_pass = all(checks.values())
    verdict = (
        "EHF_XBR_04F6_GLOBAL_ZERO_MODE_KRYLOV_SATURATION_STRUCTURE_AUDIT_PASS"
        if strict_pass else
        "EHF_XBR_04F6_GLOBAL_ZERO_MODE_KRYLOV_SATURATION_STRUCTURE_AUDIT_FAIL"
    )


    kernel_orbit_complete = sum(
        truthy(row["all_kernel_orbit_constant"])
        for row in channel_rows_out
    )
    full_sign_channels = sum(
        truthy(row["has_full_sign_involution"])
        for row in channel_rows_out
    )
    kernel_status = (
        "orbit_quotient_complete"
        if kernel_orbit_complete == len(channel_rows_out)
        else "symmetry_resolved_partial"
        if any(integer(row, "orbit_constant_kernel_dimension") > 0 for row in channel_rows_out)
        else "no_orbit_constant_kernel_modes"
    )
    pair_stability = (
        "stable_unique_consensus"
        if loo_correct == 20 and loo_consensus == 20
        else "stable_chosen_rule_only"
        if loo_correct == 20
        else "partial_or_unstable_recovery"
    )
    recurrence_status = (
        "preterminal_exact_recurrences_found"
        if recurrence_exact > 0 else
        "no_exact_low_order_preterminal_recurrence"
    )


    report_lines = [
        "# EHF-XBR-04F6 Structure Report",
        "",
        f"- Singular chambers audited: {len(channel_rows_out)}",
        f"- Kernel vectors audited: {len(vector_rows_out)}",
        f"- Channels whose full kernel is orbit-constant: {kernel_orbit_complete}/{len(channel_rows_out)}",
        f"- Channels with an involution acting as -I on the full kernel: {full_sign_channels}/{len(channel_rows_out)}",
        f"- Kernel structure status: {kernel_status}",
        f"- Source exact Krylov pair rules: {len(source_pair_rows)}",
        f"- Pair-rule LOO folds with an exact training rule: {len(loo_completed)}/20",
        f"- Pair-rule LOO chosen accuracy: {loo_correct}/{len(loo_completed)}",
        f"- Pair-rule LOO tie consensus: {loo_consensus}/{len(loo_completed)}",
        f"- Pair-rule stability: {pair_stability}",
        f"- Exact preterminal recurrence rows: {recurrence_exact}/{len(recurrence_rows)}",
        f"- Recurrence status: {recurrence_status}",
        "",
        "## Claim boundary",
        "",
        "Canonical kernel-vector support statistics refer to the deterministic",
        "primitive RREF nullspace basis and are not basis-independent localisation",
        "theorems. Automorphism-fixed dimensions, orbit quotient nullity, exact",
        "quotient lifts, coordinate activity and kernel dimension are subspace-level",
        "facts. Pair rules and recurrences remain finite n=9 descriptive mechanisms",
        "until independently derived or validated.",
        "",
    ]
    (out_dir / "structure_report.md").write_text(
        "\n".join(report_lines), encoding="utf-8"
    )


    elapsed = time.perf_counter() - started
    summary = {
        "probe": "EHF-XBR-04F6",
        "title": "Global Zero-Mode and Krylov-Saturation Structure Audit",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "kernel_backend": args.kernel_backend,
        "pivot_primes": pivot_primes,
        "counts": {
            "proper_channels": len(proper_rows),
            "singular_channels": len(channel_rows_out),
            "kernel_vectors": len(vector_rows_out),
            "kernel_symmetry_rows": len(symmetry_rows_out),
            "kernel_quotient_rows": len(quotient_rows_out),
            "full_kernel_orbit_constant_channels": kernel_orbit_complete,
            "full_sign_involution_channels": full_sign_channels,
            "source_exact_krylov_pair_rules": len(source_pair_rows),
            "pair_loo_folds": len(loo_rows),
            "pair_loo_rules_available": len(loo_completed),
            "pair_loo_chosen_correct": loo_correct,
            "pair_loo_tie_consensus": loo_consensus,
            "krylov_curve_rows": len(curve_rows),
            "recurrence_rows": len(recurrence_rows),
            "exact_recurrence_rows": recurrence_exact,
        },
        "kernel_structure_status": kernel_status,
        "pair_rule_stability": pair_stability,
        "recurrence_status": recurrence_status,
        "checks": checks,
        "strict_pass": strict_pass,
        "verdict": verdict,
        "elapsed_seconds": elapsed,
    }
    write_json(out_dir / "run_summary.json", summary)


    print()
    print("[global zero-mode structure]")
    print(
        f"  singular={len(channel_rows_out)} kernel_vectors={len(vector_rows_out)} "
        f"orbit_complete={kernel_orbit_complete} full_sign={full_sign_channels}"
    )
    print(f"  status={kernel_status}")
    print("[Krylov pair-rule stability]")
    print(
        f"  source_rules={len(source_pair_rows)} loo_available={len(loo_completed)}/20 "
        f"chosen_correct={loo_correct} tie_consensus={loo_consensus}"
    )
    print(f"  status={pair_stability}")
    print("[late-growth recurrence]")
    print(
        f"  rows={len(recurrence_rows)} exact={recurrence_exact} "
        f"status={recurrence_status}"
    )
    print()
    print("=" * 132)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {verdict}")
    print(f"elapsed:              {elapsed:.2f}s")
    print("=" * 132)


    if args.strict and not strict_pass:
        return 2
    return 0




if __name__ == "__main__":
    raise SystemExit(main())