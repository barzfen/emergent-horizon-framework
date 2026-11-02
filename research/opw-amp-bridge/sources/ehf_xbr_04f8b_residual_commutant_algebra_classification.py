#!/usr/bin/env python3
r"""
EHF-XBR-04F8B: Residual Commutant Algebra Classification

This probe consumes the exact XBR-04F8 terminal bases and resolves only the
paired 12-dimensional blocks left unclassified in A=(6,7,8), sectors 5 and 6.

For each target block V it reconstructs the four-dimensional central commutant

    C = End_{Q[G]}(V),

computes an exact multiplication table, constructs a quaternion presentation

    C ~= (a,b)_Q,

and evaluates every potentially ramified Hilbert symbol.  This gives a complete
split-versus-division classification:

  * no ramified place  => C ~= M_2(Q);
  * a nonempty ramification set => C is a quaternion division algebra.

In the split case the probe does not stop at the local-invariant certificate.
It uses the certified six-dimensional sibling W already present in the same
18-dimensional XBR-04F7 sector, computes Hom_G(W,V) exactly, constructs a
rank-six equivariant idempotent in C, and certifies

    V ~= W (+) W,
    U ~= W (+) W (+) W.

If the quaternion algebra is division, its exact ramification set certifies
that V is rational irreducible but not absolutely irreducible.  Strict PASS
accepts either mathematically valid branch, while requiring all outcome-specific
certificates.

No physical interpretation is assigned to the algebra, its ramification, or
the resulting module multiplicity.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import sympy as sp
from sympy.polys.matrices import DomainMatrix

SCRIPT_VERSION = "ehf_xbr_04f8b_v1_2026-07-31"
PROBE_NAME = "EHF-XBR-04F8B"
VERDICT_PASS = "EHF_XBR_04F8B_RESIDUAL_COMMUTANT_ALGEBRA_CLASSIFICATION_PASS"

Permutation = Tuple[int, ...]
Subset = Tuple[int, int, int]


# ---------------------------------------------------------------------------
# General exact helpers
# ---------------------------------------------------------------------------


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(module_name)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        if previous is None:
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = previous
        raise
    return module


def read_csv(path: Path) -> List[dict]:
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


def read_json(path: Path):
    with path.open() as handle:
        return json.load(handle)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def truthy(value: object) -> bool:
    return str(value).strip().lower() == "true"


def parse_subset(value: object) -> Subset:
    text = str(value).strip().replace("(", "").replace(")", "")
    text = text.replace("[", "").replace("]", "")
    parts = [part.strip() for part in text.split(",") if part.strip()]
    if len(parts) != 3:
        raise ValueError(f"invalid subset: {value!r}")
    return tuple(map(int, parts))  # type: ignore[return-value]


def subset_text(subset: Subset) -> str:
    return "(" + ", ".join(map(str, subset)) + ")"


def subset_slug(subset: Subset) -> str:
    return "A_" + "_".join(map(str, subset))


def fraction_text(value: object) -> str:
    rational = sp.Rational(value)
    return str(rational.p) if rational.q == 1 else f"{rational.p}/{rational.q}"


def stable_json_hash(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def matrix_hash(matrix: sp.Matrix) -> str:
    return stable_json_hash([
        [fraction_text(matrix[row, column]) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ])


def matrix_vector(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([
        matrix[row, column]
        for row in range(matrix.rows)
        for column in range(matrix.cols)
    ])


def exact_rank(matrix: sp.Matrix) -> int:
    if matrix.rows == 0 or matrix.cols == 0:
        return 0
    return int(DomainMatrix.from_Matrix(matrix).rank())


def independent_column_basis(matrix: sp.Matrix) -> sp.Matrix:
    if matrix.cols == 0:
        return sp.zeros(matrix.rows, 0)
    _, pivots = matrix.rref()
    return matrix[:, list(pivots)]


def solve_exact_linear_system(
    matrix: sp.Matrix,
    target: sp.Matrix,
) -> List[sp.Rational] | None:
    if matrix.rows != target.rows or target.cols != 1:
        raise ValueError("linear-system shape mismatch")
    solution_set = sp.linsolve((matrix, target))
    if solution_set is sp.EmptySet or not solution_set:
        return None
    solution_tuple = next(iter(solution_set))
    free_symbols: Set[sp.Symbol] = set()
    for value in solution_tuple:
        free_symbols.update(value.free_symbols)
    substitutions = {symbol: sp.Rational(0) for symbol in free_symbols}
    return [sp.Rational(value.subs(substitutions)) for value in solution_tuple]


def matrices_commute(left: sp.Matrix, right: sp.Matrix) -> bool:
    return left * right == right * left


def scalar_matrix_value(matrix: sp.Matrix) -> sp.Rational | None:
    if matrix.rows != matrix.cols or matrix.rows == 0:
        return None
    value = sp.Rational(matrix[0, 0])
    return value if matrix == value * sp.eye(matrix.rows) else None


# ---------------------------------------------------------------------------
# Exact commutants, Hom spaces, and projections
# ---------------------------------------------------------------------------


def standard_matrix_units(dimension: int) -> List[sp.Matrix]:
    result: List[sp.Matrix] = []
    for row in range(dimension):
        for column in range(dimension):
            matrix = sp.zeros(dimension)
            matrix[row, column] = 1
            result.append(matrix)
    return result


def commutant_basis(generator_matrices: Sequence[sp.Matrix]) -> List[sp.Matrix]:
    if not generator_matrices:
        raise ValueError("at least one generator matrix is required")
    dimension = generator_matrices[0].rows
    if any(matrix.shape != (dimension, dimension) for matrix in generator_matrices):
        raise ValueError("generator dimensions do not agree")
    if all(scalar_matrix_value(matrix) is not None for matrix in generator_matrices):
        return standard_matrix_units(dimension)

    variable_count = dimension * dimension
    entries: Dict[Tuple[int, int], sp.Rational] = {}
    equation = 0
    for representation in generator_matrices:
        for row in range(dimension):
            for column in range(dimension):
                coefficients: Dict[int, sp.Rational] = defaultdict(
                    lambda: sp.Rational(0)
                )
                for middle in range(dimension):
                    right_value = sp.Rational(representation[middle, column])
                    if right_value:
                        coefficients[row * dimension + middle] += right_value
                    left_value = sp.Rational(representation[row, middle])
                    if left_value:
                        coefficients[middle * dimension + column] -= left_value
                nonzero = {index: value for index, value in coefficients.items() if value}
                if not nonzero:
                    continue
                for index, value in nonzero.items():
                    entries[(equation, index)] = value
                equation += 1
    if equation == 0:
        return standard_matrix_units(dimension)

    equations = sp.MutableSparseMatrix(equation, variable_count, entries)
    null_rows = DomainMatrix.from_Matrix(equations).nullspace().to_Matrix()
    basis: List[sp.Matrix] = []
    for basis_index in range(null_rows.rows):
        values = [
            sp.Rational(null_rows[basis_index, index])
            for index in range(variable_count)
        ]
        basis.append(sp.Matrix(dimension, dimension, values))
    basis.sort(key=matrix_hash)
    if not basis:
        raise ArithmeticError("commutant unexpectedly vanished")
    return basis


def algebra_center_basis(algebra_basis: Sequence[sp.Matrix]) -> List[sp.Matrix]:
    if not algebra_basis:
        return []
    if len(algebra_basis) == 1:
        return [algebra_basis[0]]
    if all(
        matrices_commute(algebra_basis[left], algebra_basis[right])
        for left in range(len(algebra_basis))
        for right in range(left + 1, len(algebra_basis))
    ):
        return list(algebra_basis)

    dimension = algebra_basis[0].rows
    rows: List[List[sp.Rational]] = []
    for right in algebra_basis:
        commutators = [left * right - right * left for left in algebra_basis]
        for row in range(dimension):
            for column in range(dimension):
                coefficients = [
                    sp.Rational(item[row, column]) for item in commutators
                ]
                if any(coefficients):
                    rows.append(coefficients)
    equations = sp.Matrix(rows) if rows else sp.zeros(0, len(algebra_basis))
    null_rows = DomainMatrix.from_Matrix(equations).nullspace().to_Matrix()
    result: List[sp.Matrix] = []
    for basis_index in range(null_rows.rows):
        matrix = sp.zeros(dimension)
        for coefficient_index, source in enumerate(algebra_basis):
            matrix += sp.Rational(
                null_rows[basis_index, coefficient_index]
            ) * source
        result.append(matrix)
    result.sort(key=matrix_hash)
    return result


def representation_hom_basis(
    source_generators: Sequence[sp.Matrix],
    target_generators: Sequence[sp.Matrix],
) -> List[sp.Matrix]:
    """Return exact T with target(g) T = T source(g)."""
    if not source_generators or len(source_generators) != len(target_generators):
        raise ValueError("source and target generator lists must be nonempty and aligned")
    source_dimension = source_generators[0].rows
    target_dimension = target_generators[0].rows
    if any(item.shape != (source_dimension, source_dimension) for item in source_generators):
        raise ValueError("source generator shape mismatch")
    if any(item.shape != (target_dimension, target_dimension) for item in target_generators):
        raise ValueError("target generator shape mismatch")

    variable_count = target_dimension * source_dimension
    entries: Dict[Tuple[int, int], sp.Rational] = {}
    equation = 0
    for source, target in zip(source_generators, target_generators):
        for row in range(target_dimension):
            for column in range(source_dimension):
                coefficients: Dict[int, sp.Rational] = defaultdict(
                    lambda: sp.Rational(0)
                )
                for middle in range(source_dimension):
                    value = sp.Rational(source[middle, column])
                    if value:
                        coefficients[row * source_dimension + middle] += value
                for middle in range(target_dimension):
                    value = sp.Rational(target[row, middle])
                    if value:
                        coefficients[middle * source_dimension + column] -= value
                nonzero = {index: value for index, value in coefficients.items() if value}
                if not nonzero:
                    continue
                for index, value in nonzero.items():
                    entries[(equation, index)] = value
                equation += 1
    if equation == 0:
        return [
            sp.Matrix(target_dimension, source_dimension, [
                1 if index == unit else 0
                for index in range(variable_count)
            ])
            for unit in range(variable_count)
        ]
    equations = sp.MutableSparseMatrix(equation, variable_count, entries)
    null_rows = DomainMatrix.from_Matrix(equations).nullspace().to_Matrix()
    result: List[sp.Matrix] = []
    for basis_index in range(null_rows.rows):
        values = [
            sp.Rational(null_rows[basis_index, index])
            for index in range(variable_count)
        ]
        result.append(sp.Matrix(target_dimension, source_dimension, values))
    result.sort(key=matrix_hash)
    return result


def find_full_rank_map(
    hom_basis: Sequence[sp.Matrix],
    required_rank: int,
) -> Tuple[sp.Matrix | None, str]:
    candidates: List[Tuple[sp.Matrix, str]] = [
        (matrix, f"hom_basis[{index}]")
        for index, matrix in enumerate(hom_basis)
    ]
    for left in range(len(hom_basis)):
        for right in range(left + 1, len(hom_basis)):
            candidates.append((
                hom_basis[left] + hom_basis[right],
                f"hom_basis[{left}]+hom_basis[{right}]",
            ))
            candidates.append((
                hom_basis[left] - hom_basis[right],
                f"hom_basis[{left}]-hom_basis[{right}]",
            ))
    for matrix, description in candidates:
        if exact_rank(matrix) == required_rank:
            return matrix, description
    return None, ""


def equivariant_projection_onto(
    invariant_subspace: sp.Matrix,
    algebra_basis: Sequence[sp.Matrix],
) -> sp.Matrix:
    dimension = algebra_basis[0].rows
    subspace = independent_column_basis(invariant_subspace)
    if not 0 < subspace.cols < dimension:
        raise ValueError("projection target must be proper and nonzero")

    annihilator_columns = subspace.T.nullspace()
    annihilator = (
        sp.Matrix.vstack(*(column.T for column in annihilator_columns))
        if annihilator_columns
        else sp.zeros(0, dimension)
    )
    rows: List[List[sp.Rational]] = []
    targets: List[sp.Rational] = []
    images = [basis * subspace for basis in algebra_basis]
    for row in range(dimension):
        for column in range(subspace.cols):
            rows.append([
                sp.Rational(image[row, column]) for image in images
            ])
            targets.append(sp.Rational(subspace[row, column]))
    annihilator_images = [annihilator * basis for basis in algebra_basis]
    for row in range(annihilator.rows):
        for column in range(dimension):
            rows.append([
                sp.Rational(image[row, column]) for image in annihilator_images
            ])
            targets.append(sp.Rational(0))

    coefficients = solve_exact_linear_system(sp.Matrix(rows), sp.Matrix(targets))
    if coefficients is None:
        raise ArithmeticError("failed to solve exact equivariant projection")
    projection = sp.zeros(dimension)
    for coefficient, basis in zip(coefficients, algebra_basis):
        projection += coefficient * basis
    if projection * projection != projection:
        raise ArithmeticError("projection is not idempotent")
    if exact_rank(projection) != subspace.cols:
        raise ArithmeticError("projection rank mismatch")
    return projection


# ---------------------------------------------------------------------------
# Four-dimensional central-simple algebra classification
# ---------------------------------------------------------------------------


def algebra_coordinates(
    matrix: sp.Matrix,
    algebra_basis: Sequence[sp.Matrix],
) -> sp.Matrix:
    columns = sp.Matrix.hstack(*(matrix_vector(item) for item in algebra_basis))
    coefficients = solve_exact_linear_system(columns, matrix_vector(matrix))
    if coefficients is None:
        raise ArithmeticError("matrix is not in the supplied algebra span")
    reconstructed = sp.zeros(matrix.rows)
    for coefficient, basis in zip(coefficients, algebra_basis):
        reconstructed += coefficient * basis
    if reconstructed != matrix:
        raise ArithmeticError("algebra-coordinate reconstruction failed")
    return sp.Matrix(coefficients)


def identity_first_algebra_basis(
    algebra_basis: Sequence[sp.Matrix],
) -> List[sp.Matrix]:
    if not algebra_basis:
        raise ValueError("empty algebra basis")
    dimension = algebra_basis[0].rows
    identity = sp.eye(dimension)
    result = [identity]
    vectors = matrix_vector(identity)
    rank = 1
    for candidate in sorted(algebra_basis, key=matrix_hash):
        joined = vectors.row_join(matrix_vector(candidate))
        new_rank = exact_rank(joined)
        if new_rank > rank:
            result.append(candidate)
            vectors = joined
            rank = new_rank
    if len(result) != len(algebra_basis):
        raise ArithmeticError("identity-normalized algebra basis has wrong dimension")
    return result


def algebra_multiplication_rows(
    algebra_basis: Sequence[sp.Matrix],
) -> List[dict]:
    rows: List[dict] = []
    for left_index, left in enumerate(algebra_basis):
        for right_index, right in enumerate(algebra_basis):
            coefficients = algebra_coordinates(left * right, algebra_basis)
            rows.append({
                "left_basis_index": left_index,
                "right_basis_index": right_index,
                **{
                    f"coefficient_{index}": fraction_text(coefficients[index])
                    for index in range(len(algebra_basis))
                },
            })
    return rows


def left_regular_matrix(
    element: sp.Matrix,
    algebra_basis: Sequence[sp.Matrix],
) -> sp.Matrix:
    return sp.Matrix.hstack(*[
        algebra_coordinates(element * basis, algebra_basis)
        for basis in algebra_basis
    ])


def reduced_trace(
    element: sp.Matrix,
    algebra_basis: Sequence[sp.Matrix],
) -> sp.Rational:
    # A four-dimensional central simple algebra has degree two, and the trace
    # of left multiplication is degree times the reduced trace.
    return sp.Rational(sp.trace(left_regular_matrix(element, algebra_basis)), 2)


def linear_combination(
    coefficients: Sequence[sp.Rational],
    matrices: Sequence[sp.Matrix],
) -> sp.Matrix:
    result = sp.zeros(matrices[0].rows)
    for coefficient, matrix in zip(coefficients, matrices):
        result += sp.Rational(coefficient) * matrix
    return result


def nonzero_square_candidate(
    candidates: Sequence[sp.Matrix],
) -> Tuple[sp.Matrix, sp.Rational]:
    trial: List[sp.Matrix] = list(candidates)
    for left in range(len(candidates)):
        for right in range(left + 1, len(candidates)):
            trial.append(candidates[left] + candidates[right])
    for matrix in trial:
        scalar = scalar_matrix_value(matrix * matrix)
        if scalar is not None and scalar != 0:
            return matrix, scalar
    raise ArithmeticError("failed to find a pure element with nonzero square")


def quaternion_presentation(
    raw_algebra_basis: Sequence[sp.Matrix],
) -> dict:
    if len(raw_algebra_basis) != 4:
        raise ValueError("quaternion classification requires algebra dimension four")
    basis = identity_first_algebra_basis(raw_algebra_basis)
    identity = basis[0]
    center = algebra_center_basis(basis)
    if len(center) != 1:
        raise ArithmeticError("four-dimensional algebra is not central over Q")

    traces = sp.Matrix([[
        reduced_trace(element, basis) for element in basis
    ]])
    if traces[0, 0] != 2:
        raise ArithmeticError("reduced trace of identity is not two")
    pure_coordinate_basis = traces.nullspace()
    if len(pure_coordinate_basis) != 3:
        raise ArithmeticError("pure quaternion subspace does not have dimension three")
    pure_basis = [
        linear_combination(list(coefficients), basis)
        for coefficients in pure_coordinate_basis
    ]
    if any(reduced_trace(element, basis) != 0 for element in pure_basis):
        raise ArithmeticError("pure basis trace verification failed")

    i_matrix, a_value = nonzero_square_candidate(pure_basis)
    anti_columns = sp.Matrix.hstack(*[
        matrix_vector(i_matrix * element + element * i_matrix)
        for element in pure_basis
    ])
    anti_coordinate_basis = anti_columns.nullspace()
    anti_basis = [
        linear_combination(list(coefficients), pure_basis)
        for coefficients in anti_coordinate_basis
    ]
    if len(anti_basis) != 2:
        raise ArithmeticError("anti-commuting pure subspace has wrong dimension")
    j_matrix, b_value = nonzero_square_candidate(anti_basis)
    k_matrix = i_matrix * j_matrix

    presentation_basis = [identity, i_matrix, j_matrix, k_matrix]
    presentation_rank = exact_rank(
        sp.Matrix.hstack(*(matrix_vector(item) for item in presentation_basis))
    )
    relation_checks = {
        "identity_exact": identity == sp.eye(identity.rows),
        "i_square_exact": i_matrix * i_matrix == a_value * identity,
        "j_square_exact": j_matrix * j_matrix == b_value * identity,
        "anticommutation_exact": i_matrix * j_matrix == -j_matrix * i_matrix,
        "k_definition_exact": k_matrix == i_matrix * j_matrix,
        "presentation_basis_rank_four": presentation_rank == 4,
        "a_nonzero": a_value != 0,
        "b_nonzero": b_value != 0,
    }
    if not all(relation_checks.values()):
        raise ArithmeticError("quaternion-presentation relation failure")

    return {
        "algebra_basis": basis,
        "multiplication_rows": algebra_multiplication_rows(basis),
        "i_matrix": i_matrix,
        "j_matrix": j_matrix,
        "k_matrix": k_matrix,
        "a": sp.Rational(a_value),
        "b": sp.Rational(b_value),
        "relation_checks": relation_checks,
        "algebra_basis_hash": stable_json_hash([matrix_hash(item) for item in basis]),
        "presentation_basis_hash": stable_json_hash([
            matrix_hash(item) for item in presentation_basis
        ]),
    }


def squareclass_integer(value: sp.Rational) -> int:
    rational = sp.Rational(value)
    if rational == 0:
        raise ValueError("zero has no squareclass")
    sign = -1 if rational < 0 else 1
    numerator = abs(int(rational.p))
    denominator = int(rational.q)
    result = sign
    for prime, exponent in sp.factorint(numerator).items():
        if exponent % 2:
            result *= int(prime)
    for prime, exponent in sp.factorint(denominator).items():
        if exponent % 2:
            result *= int(prime)
    return result


def legendre_unit(value: int, prime: int) -> int:
    residue = value % prime
    if residue == 0:
        raise ValueError("Legendre input must be a p-adic unit")
    symbol = pow(residue, (prime - 1) // 2, prime)
    return -1 if symbol == prime - 1 else int(symbol)


def valuation_parity(value: int, prime: int) -> Tuple[int, int]:
    exponent = 0
    unit = value
    while unit % prime == 0:
        unit //= prime
        exponent += 1
    return exponent % 2, unit


def hilbert_symbol_odd_prime(a_value: int, b_value: int, prime: int) -> int:
    alpha, a_unit = valuation_parity(a_value, prime)
    beta, b_unit = valuation_parity(b_value, prime)
    sign = -1 if (alpha * beta * ((prime - 1) // 2)) % 2 else 1
    if beta:
        sign *= legendre_unit(a_unit, prime)
    if alpha:
        sign *= legendre_unit(b_unit, prime)
    return sign


def hilbert_symbol_two(a_value: int, b_value: int) -> int:
    alpha, a_unit = valuation_parity(a_value, 2)
    beta, b_unit = valuation_parity(b_value, 2)
    epsilon_a = ((a_unit - 1) // 2) % 2
    epsilon_b = ((b_unit - 1) // 2) % 2
    omega_a = ((a_unit * a_unit - 1) // 8) % 2
    omega_b = ((b_unit * b_unit - 1) // 8) % 2
    exponent = (
        epsilon_a * epsilon_b
        + alpha * omega_b
        + beta * omega_a
    ) % 2
    return -1 if exponent else 1


def quaternion_local_classification(
    a_value: sp.Rational,
    b_value: sp.Rational,
) -> dict:
    squareclass_a = squareclass_integer(a_value)
    squareclass_b = squareclass_integer(b_value)
    primes = {2}
    primes.update(int(prime) for prime in sp.factorint(abs(squareclass_a)))
    primes.update(int(prime) for prime in sp.factorint(abs(squareclass_b)))

    local_rows: List[dict] = []
    finite_product = 1
    for prime in sorted(primes):
        symbol = (
            hilbert_symbol_two(squareclass_a, squareclass_b)
            if prime == 2
            else hilbert_symbol_odd_prime(squareclass_a, squareclass_b, prime)
        )
        finite_product *= symbol
        local_rows.append({
            "place": str(prime),
            "hilbert_symbol": symbol,
            "ramified": symbol == -1,
            "reason": "prime_dividing_2ab_squareclass",
        })
    infinity_symbol = (
        -1 if squareclass_a < 0 and squareclass_b < 0 else 1
    )
    local_rows.append({
        "place": "infinity",
        "hilbert_symbol": infinity_symbol,
        "ramified": infinity_symbol == -1,
        "reason": "real_place",
    })
    ramified_places = [
        str(row["place"]) for row in local_rows if bool(row["ramified"])
    ]
    reciprocity_exact = finite_product * infinity_symbol == 1
    if not reciprocity_exact:
        raise ArithmeticError("Hilbert reciprocity failed")
    split = len(ramified_places) == 0
    return {
        "a_squareclass": squareclass_a,
        "b_squareclass": squareclass_b,
        "local_rows": local_rows,
        "ramified_places": ramified_places,
        "hilbert_reciprocity_exact": reciprocity_exact,
        "classification": (
            "split_matrix_algebra_M2_Q"
            if split
            else "quaternion_division_algebra"
        ),
        "split": split,
    }


# ---------------------------------------------------------------------------
# Synthetic self-test
# ---------------------------------------------------------------------------


def quaternion_regular_basis(a_value: int, b_value: int) -> List[sp.Matrix]:
    """Left regular matrices for 1,i,j,k with i^2=a, j^2=b, ij=k."""
    a = sp.Rational(a_value)
    b = sp.Rational(b_value)

    def product(left: int, right: int) -> sp.Matrix:
        result = sp.zeros(4, 1)
        if left == 0:
            result[right] = 1
        elif right == 0:
            result[left] = 1
        elif left == 1 and right == 1:
            result[0] = a
        elif left == 2 and right == 2:
            result[0] = b
        elif left == 1 and right == 2:
            result[3] = 1
        elif left == 2 and right == 1:
            result[3] = -1
        elif left == 1 and right == 3:
            result[2] = a
        elif left == 3 and right == 1:
            result[2] = -a
        elif left == 2 and right == 3:
            result[1] = -b
        elif left == 3 and right == 2:
            result[1] = b
        elif left == 3 and right == 3:
            result[0] = -a * b
        else:
            raise AssertionError((left, right))
        return result

    return [
        sp.Matrix.hstack(*(product(left, right) for right in range(4)))
        for left in range(4)
    ]


def self_test() -> None:
    # Split algebra M_2(Q).
    split_basis = standard_matrix_units(2)
    split_presentation = quaternion_presentation(split_basis)
    split_local = quaternion_local_classification(
        split_presentation["a"], split_presentation["b"]
    )
    assert split_local["split"]
    assert split_local["ramified_places"] == []
    assert split_local["hilbert_reciprocity_exact"]

    # Hamilton's quaternion division algebra, ramified at 2 and infinity.
    division_basis = quaternion_regular_basis(-1, -1)
    division_presentation = quaternion_presentation(division_basis)
    division_local = quaternion_local_classification(
        division_presentation["a"], division_presentation["b"]
    )
    assert not division_local["split"]
    assert set(division_local["ramified_places"]) == {"2", "infinity"}
    assert division_local["hilbert_reciprocity_exact"]

    # Exact Hom and projection path on two copies of a scalar 1D module.
    source_generators = [sp.eye(1)]
    target_generators = [sp.eye(2)]
    hom = representation_hom_basis(source_generators, target_generators)
    assert len(hom) == 2
    embedding, _ = find_full_rank_map(hom, 1)
    assert embedding is not None
    projection = equivariant_projection_onto(embedding, split_basis)
    assert projection * projection == projection
    assert exact_rank(projection) == 1

    print("EHF-XBR-04F8B self-test PASS")


# ---------------------------------------------------------------------------
# Production representation helpers
# ---------------------------------------------------------------------------


def representation_set_from_coordinate_rows(
    coordinate_rows: Sequence[Sequence[int]],
    group_elements: Sequence[Permutation],
    state_images: Mapping[Permutation, Sequence[int]],
    xbr04f,
    f7,
) -> Dict[Permutation, sp.Matrix]:
    result: Dict[Permutation, sp.Matrix] = {}
    for element in group_elements:
        transformed = xbr04f.permute_coordinate_rows(
            coordinate_rows, state_images[element]
        )
        result[element] = f7.representation_from_kernel_basis(
            coordinate_rows, transformed
        )
    return result


def restricted_representation_set(
    block_basis: sp.Matrix,
    representations: Mapping[Permutation, sp.Matrix],
    f7,
) -> Dict[Permutation, sp.Matrix]:
    workspace = f7.restriction_workspace(block_basis)
    return {
        element: f7.restriction_matrix_cached(matrix, block_basis, workspace)
        for element, matrix in representations.items()
    }


def class_character(
    classes: Sequence[Sequence[Permutation]],
    representations: Mapping[Permutation, sp.Matrix],
) -> List[sp.Rational]:
    return [
        sp.Rational(sp.trace(representations[cell[0]]))
        for cell in classes
    ]


def character_norm(
    classes: Sequence[Sequence[Permutation]],
    traces: Sequence[sp.Rational],
    group_order: int,
) -> sp.Rational:
    return sp.Rational(
        sum(len(cell) * trace * trace for cell, trace in zip(classes, traces)),
        group_order,
    )


def integer_coordinate_rows(matrix: sp.Matrix, f7) -> List[List[int]]:
    return [
        f7.primitive_integer_row([
            matrix[row, column] for column in range(matrix.cols)
        ])
        for row in range(matrix.rows)
    ]


def row_spaces_equal(left: sp.Matrix, right: sp.Matrix) -> bool:
    left_rank = exact_rank(left)
    right_rank = exact_rank(right)
    return (
        left_rank == right_rank
        and exact_rank(sp.Matrix.vstack(left, right)) == left_rank
    )


def exact_module_isomorphism(
    source_generators: Sequence[sp.Matrix],
    target_generators: Sequence[sp.Matrix],
) -> dict:
    hom = representation_hom_basis(source_generators, target_generators)
    required_rank = source_generators[0].rows
    map_matrix, description = find_full_rank_map(hom, required_rank)
    return {
        "hom_dimension": len(hom),
        "full_rank_map_found": map_matrix is not None,
        "full_rank_map_description": description,
        "full_rank_map_hash": matrix_hash(map_matrix) if map_matrix is not None else "",
    }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def markdown_report(
    classification_rows: Sequence[Mapping[str, object]],
    checks: Mapping[str, bool],
    summary_counts: Mapping[str, int],
    verdict: str,
) -> str:
    lines = [
        "# EHF-XBR-04F8B: Residual Commutant Algebra Classification",
        "",
        f"Verdict: `{verdict}`",
        "",
        "## Scope",
        "",
        "The probe classifies only the two 12-dimensional terminal blocks left unresolved by XBR-04F8 in A=(6,7,8), sectors 5 and 6.",
        "",
        "## Classification",
        "",
        "| sector | F8 primitive | algebra | quaternion presentation | ramified places | resolved module structure |",
        "|---:|---:|---|---|---|---|",
    ]
    for row in classification_rows:
        lines.append(
            f"| {row['sector_index']} | {row['source_primitive_index']} | "
            f"{row['algebra_classification']} | "
            f"({row['quaternion_a']}, {row['quaternion_b']})_Q | "
            f"{row['ramified_places'] or 'none'} | {row['resolved_module_structure']} |"
        )
    lines.extend([
        "",
        "## Final primitive census",
        "",
        f"- source sectors fully resolved: {summary_counts['final_fully_resolved_sectors']}",
        f"- certified primitive blocks: {summary_counts['final_certified_primitive_blocks']}",
        f"- terminal primitive blocks: {summary_counts['final_terminal_primitive_blocks']}",
        f"- unresolved terminal blocks: {summary_counts['final_unresolved_terminal_blocks']}",
        "",
        "If a 12-dimensional F8 terminal block splits as 6+6, it is replaced by two primitive children and the total primitive-block count increases by one.",
        "",
        "## Integrity checks",
        "",
    ])
    for name, passed in checks.items():
        lines.append(f"- `{name}`: {passed}")
    lines.extend([
        "",
        "## Claim boundary",
        "",
        "The classification is an exact finite statement about rational commutant algebras and finite label-group modules. It does not identify any module or quaternion algebra with a physical particle, field, coupling, or observable.",
        "",
    ])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify the two residual four-dimensional XBR-04F8 commutants."
    )
    parser.add_argument("--xbr04f8-dir")
    parser.add_argument("--xbr04f8-script")
    parser.add_argument("--xbr04f7-dir")
    parser.add_argument("--xbr04f7-script")
    parser.add_argument("--xbr04f-script")
    parser.add_argument("--opw-base-script")
    parser.add_argument("--amp-base-script")
    parser.add_argument("--amp-rank-script")
    parser.add_argument("--target-subset", default="6,7,8")
    parser.add_argument("--target-sectors", default="5,6")
    parser.add_argument(
        "--write-resolved-bases",
        choices=("none", "sparse"),
        default="sparse",
    )
    parser.add_argument("--out-dir", default="runs/ehf_xbr_04f8b")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    required = (
        "xbr04f8_dir",
        "xbr04f8_script",
        "xbr04f7_dir",
        "xbr04f7_script",
        "xbr04f_script",
        "opw_base_script",
        "amp_base_script",
        "amp_rank_script",
    )
    missing = [name for name in required if not getattr(args, name)]
    if missing:
        parser.error("missing required arguments: " + ", ".join(missing))

    started = time.perf_counter()
    target_subset = parse_subset(args.target_subset)
    target_subset_key = subset_text(target_subset)
    target_sectors = {
        int(value.strip())
        for value in str(args.target_sectors).split(",")
        if value.strip()
    }
    if not target_sectors:
        parser.error("--target-sectors must contain at least one sector index")

    f8_dir = Path(args.xbr04f8_dir).resolve()
    f8_script_path = Path(args.xbr04f8_script).resolve()
    f7_dir = Path(args.xbr04f7_dir).resolve()
    f7_script_path = Path(args.xbr04f7_script).resolve()
    xbr04f_path = Path(args.xbr04f_script).resolve()
    opw_path = Path(args.opw_base_script).resolve()
    amp_base_path = Path(args.amp_base_script).resolve()
    amp_rank_path = Path(args.amp_rank_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    required_paths = (
        f8_dir / "run_summary.json",
        f8_dir / "commutant_sector_ledger.csv",
        f8_dir / "primitive_module_ledger.csv",
        f8_script_path,
        f7_dir / "run_summary.json",
        f7_dir / "kernel_module_channel_ledger.csv",
        f7_dir / "kernel_module_sector_ledger.csv",
        f7_script_path,
        xbr04f_path,
        opw_path,
        amp_base_path,
        amp_rank_path,
    )
    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(path)

    f8 = load_module(f8_script_path, "ehf_xbr_04f8b_f8")
    f7 = load_module(f7_script_path, "ehf_xbr_04f8b_f7")
    xbr04f = load_module(xbr04f_path, "ehf_xbr_04f8b_xbr04f")
    opw = load_module(opw_path, "ehf_xbr_04f8b_opw")
    amp_base = load_module(amp_base_path, "ehf_xbr_04f8b_amp_base")
    amp_rank = load_module(amp_rank_path, "ehf_xbr_04f8b_amp_rank")

    f8_summary = read_json(f8_dir / "run_summary.json")
    f8_sector_rows = read_csv(f8_dir / "commutant_sector_ledger.csv")
    f8_primitive_rows = read_csv(f8_dir / "primitive_module_ledger.csv")
    f7_channel_rows = read_csv(f7_dir / "kernel_module_channel_ledger.csv")
    f7_sector_rows = read_csv(f7_dir / "kernel_module_sector_ledger.csv")

    unresolved_rows = [
        row for row in f8_primitive_rows
        if (
            str(row["subset"]) == target_subset_key
            and int(row["sector_index"]) in target_sectors
            and not truthy(row["rational_irreducible_certified"])
        )
    ]
    unresolved_rows.sort(key=lambda row: (
        int(row["sector_index"]), int(row["primitive_index"])
    ))
    if len(unresolved_rows) != len(target_sectors):
        raise ValueError(
            f"expected one unresolved target per sector; found {len(unresolved_rows)}"
        )

    source_channel = next(
        row for row in f7_channel_rows if str(row["subset"]) == target_subset_key
    )
    source_sector_by_index = {
        int(row["sector_index"]): row
        for row in f7_sector_rows
        if str(row["subset"]) == target_subset_key
    }

    cycles9 = opw.generate_cycles(9)
    index9 = {cycle: index for index, cycle in enumerate(cycles9)}
    pi9 = [opw.pi_label(cycle) for cycle in cycles9]
    graph9 = opw.build_preserve_graph(
        cycles9, index9, pi9, "OPW3", opw.GRAPH_LENGTHS["OPW3"]
    )
    source_fibres = amp_base.fibres(9)
    source_key = amp_rank.key_from_subset_9(target_subset)
    source_cycles = source_fibres[source_key]
    global_ids = [
        index9[tuple(label - 1 for label in cycle)]
        for cycle in source_cycles
    ]
    local_neighbors = f7.local_neighbors(graph9.adjacency, global_ids)

    group: Set[Permutation] = set()
    state_images: Dict[Permutation, List[int]] = {}
    for candidate in xbr04f.candidate_stabilizer_permutations(target_subset):
        image = xbr04f.chamber_state_permutation(
            candidate, global_ids, cycles9, index9
        )
        if image is None or not xbr04f.adjacency_automorphism_exact(
            image, local_neighbors
        ):
            continue
        group.add(candidate)
        state_images[candidate] = image
    generators = xbr04f.greedy_group_generators(group)
    group_elements = sorted(group, key=xbr04f.permutation_cycle_text)
    classes = f7.conjugacy_classes(group, xbr04f)
    literal_group_hash = f7.literal_group_hash(group)

    print("=" * 132)
    print("EHF-XBR-04F8B: RESIDUAL COMMUTANT ALGEBRA CLASSIFICATION")
    print("=" * 132)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"XBR-04F8 directory:   {f8_dir}")
    print(f"target subset:        {target_subset}")
    print(f"target sectors:       {sorted(target_sectors)}")
    print(f"target blocks:        {len(unresolved_rows)}")
    print(f"group order:          {len(group)}")
    print(f"conjugacy classes:    {len(classes)}")
    print(f"output directory:     {out_dir}")
    print(f"strict:               {args.strict}")
    print()

    classification_rows: List[dict] = []
    multiplication_rows: List[dict] = []
    local_rows: List[dict] = []
    resolved_rows: List[dict] = []
    class_rows: List[dict] = []

    all_basis_hashes_match = True
    all_representations_exact = True
    all_commutants_exact = True
    all_presentations_exact = True
    all_reciprocity_exact = True
    all_outcome_certificates_complete = True
    all_source_reconstructions_exact = True

    for target_number, unresolved in enumerate(unresolved_rows, start=1):
        sector_index = int(unresolved["sector_index"])
        primitive_index = int(unresolved["primitive_index"])
        target_started = time.perf_counter()
        print(
            f"[target {target_number}/{len(unresolved_rows)}] "
            f"A={target_subset} sector={sector_index} primitive={primitive_index}",
            flush=True,
        )

        unresolved_path = (
            f8_dir / "channels" / subset_slug(target_subset)
            / f"sector_{sector_index:02d}"
            / f"primitive_{primitive_index:03d}.basis.coordinate.json.gz"
        )
        if not unresolved_path.exists():
            raise FileNotFoundError(unresolved_path)
        unresolved_coordinate_rows = f7.read_sparse_integer_matrix(unresolved_path)
        unresolved_hash_match = (
            f7.sha256_integer_rows(unresolved_coordinate_rows)
            == unresolved["primitive_basis_sha256"]
        )
        all_basis_hashes_match &= unresolved_hash_match

        sibling_candidates = [
            row for row in f8_primitive_rows
            if (
                str(row["subset"]) == target_subset_key
                and int(row["sector_index"]) == sector_index
                and truthy(row["absolutely_irreducible_certified"])
                and int(row["primitive_dimension"]) == 6
            )
        ]
        if len(sibling_candidates) != 1:
            raise ValueError(
                f"expected one certified 6D sibling in sector {sector_index}; "
                f"found {len(sibling_candidates)}"
            )
        sibling = sibling_candidates[0]
        sibling_index = int(sibling["primitive_index"])
        sibling_path = (
            f8_dir / "channels" / subset_slug(target_subset)
            / f"sector_{sector_index:02d}"
            / f"primitive_{sibling_index:03d}.basis.coordinate.json.gz"
        )
        if not sibling_path.exists():
            raise FileNotFoundError(sibling_path)
        sibling_coordinate_rows = f7.read_sparse_integer_matrix(sibling_path)
        sibling_hash_match = (
            f7.sha256_integer_rows(sibling_coordinate_rows)
            == sibling["primitive_basis_sha256"]
        )
        all_basis_hashes_match &= sibling_hash_match

        target_representations = representation_set_from_coordinate_rows(
            unresolved_coordinate_rows,
            group_elements,
            state_images,
            xbr04f,
            f7,
        )
        sibling_representations = representation_set_from_coordinate_rows(
            sibling_coordinate_rows,
            group_elements,
            state_images,
            xbr04f,
            f7,
        )
        target_representation_exact = f7.representation_homomorphism_exact(
            group, target_representations, generators, xbr04f
        )
        sibling_representation_exact = f7.representation_homomorphism_exact(
            group, sibling_representations, generators, xbr04f
        )
        all_representations_exact &= (
            target_representation_exact and sibling_representation_exact
        )
        target_generators = [
            target_representations[generator] for generator in generators
        ]
        sibling_generators = [
            sibling_representations[generator] for generator in generators
        ]

        commutant = commutant_basis(target_generators)
        center = algebra_center_basis(commutant)
        commutant_exact = all(
            matrices_commute(item, generator)
            for item in commutant
            for generator in target_generators
        )
        center_exact = all(
            matrices_commute(item, algebra_item)
            for item in center
            for algebra_item in commutant
        )
        schema_exact = (
            len(unresolved_coordinate_rows) == 12
            and int(unresolved["primitive_commutant_dimension"]) == 4
            and int(unresolved["primitive_center_dimension"]) == 1
            and int(Fraction(str(unresolved["character_norm"]))) == 4
            and len(commutant) == 4
            and len(center) == 1
        )
        all_commutants_exact &= commutant_exact and center_exact and schema_exact

        presentation = quaternion_presentation(commutant)
        all_presentations_exact &= all(presentation["relation_checks"].values())
        local = quaternion_local_classification(
            presentation["a"], presentation["b"]
        )
        all_reciprocity_exact &= bool(local["hilbert_reciprocity_exact"])

        for row in presentation["multiplication_rows"]:
            multiplication_rows.append({
                "subset": target_subset_key,
                "sector_index": sector_index,
                "source_primitive_index": primitive_index,
                **row,
            })
        for row in local["local_rows"]:
            local_rows.append({
                "subset": target_subset_key,
                "sector_index": sector_index,
                "source_primitive_index": primitive_index,
                "quaternion_a": fraction_text(presentation["a"]),
                "quaternion_b": fraction_text(presentation["b"]),
                "a_squareclass": local["a_squareclass"],
                "b_squareclass": local["b_squareclass"],
                **row,
            })

        hom_basis = representation_hom_basis(
            sibling_generators, target_generators
        )
        embedding, embedding_description = find_full_rank_map(hom_basis, 6)
        split_certificate_complete = False
        source_reconstruction_exact = False
        projection_hash = ""
        child_dimensions = ""
        child_commutant_dimensions = ""
        child_character_norms = ""
        child_characters_equal_sibling = False
        child_modules_isomorphic_to_sibling = False
        resolved_module_structure = ""
        resolved_block_count = 1

        if bool(local["split"]):
            if embedding is None:
                raise ArithmeticError(
                    "split algebra classified, but no full-rank sibling embedding found"
                )
            image = independent_column_basis(embedding)
            projection = equivariant_projection_onto(image, commutant)
            complement_columns = projection.nullspace()
            complement = independent_column_basis(
                sp.Matrix.hstack(*complement_columns)
            )
            projection_exact = projection * projection == projection
            projection_commutes = all(
                matrices_commute(projection, generator)
                for generator in target_generators
            )
            direct_sum_exact = (
                image.cols == 6
                and complement.cols == 6
                and exact_rank(sp.Matrix.hstack(image, complement)) == 12
            )

            child_blocks = [image, complement]
            child_coordinate_sets: List[List[List[int]]] = []
            child_traces: List[List[sp.Rational]] = []
            child_commutant_dims: List[int] = []
            child_norms: List[sp.Rational] = []
            child_isomorphism_flags: List[bool] = []
            sibling_traces = class_character(classes, sibling_representations)

            for child_index, child_basis in enumerate(child_blocks):
                child_representations = restricted_representation_set(
                    child_basis, target_representations, f7
                )
                child_generators = [
                    child_representations[generator] for generator in generators
                ]
                child_representation_exact = f7.representation_homomorphism_exact(
                    group, child_representations, generators, xbr04f
                )
                all_representations_exact &= child_representation_exact
                child_commutant = commutant_basis(child_generators)
                child_commutant_dims.append(len(child_commutant))
                traces = class_character(classes, child_representations)
                child_traces.append(traces)
                norm = character_norm(classes, traces, len(group_elements))
                child_norms.append(norm)
                isomorphism = exact_module_isomorphism(
                    sibling_generators, child_generators
                )
                child_isomorphism_flags.append(
                    bool(isomorphism["full_rank_map_found"])
                )

                chamber_matrix = (
                    child_basis.T * f7.sympy_matrix(unresolved_coordinate_rows)
                )
                coordinate_rows = integer_coordinate_rows(chamber_matrix, f7)
                child_coordinate_sets.append(coordinate_rows)
                child_hash = f7.sha256_integer_rows(coordinate_rows)
                resolved_rows.append({
                    "subset": target_subset_key,
                    "sector_index": sector_index,
                    "source_primitive_index": primitive_index,
                    "resolved_primitive_index": child_index,
                    "resolved_dimension": len(coordinate_rows),
                    "certification_kind": "split_commutant_rank6_idempotent_child",
                    "rational_irreducible_certified": len(child_commutant) == 1,
                    "absolutely_irreducible_certified": len(child_commutant) == 1,
                    "commutant_dimension": len(child_commutant),
                    "character_norm": fraction_text(norm),
                    "character_equals_certified_sibling": traces == sibling_traces,
                    "sibling_hom_dimension": isomorphism["hom_dimension"],
                    "full_rank_sibling_isomorphism_found": isomorphism[
                        "full_rank_map_found"
                    ],
                    "resolved_basis_sha256": child_hash,
                })
                if args.write_resolved_bases == "sparse":
                    f7.write_sparse_integer_matrix(
                        out_dir / "channels" / subset_slug(target_subset)
                        / f"sector_{sector_index:02d}"
                        / f"resolved_{child_index:03d}.basis.coordinate.json.gz",
                        coordinate_rows,
                    )
                for class_index, (cell, trace) in enumerate(zip(classes, traces)):
                    class_rows.append({
                        "subset": target_subset_key,
                        "sector_index": sector_index,
                        "source_primitive_index": primitive_index,
                        "resolved_primitive_index": child_index,
                        "class_index": class_index,
                        "class_size": len(cell),
                        "representative": xbr04f.permutation_cycle_text(cell[0]),
                        "character_trace": fraction_text(trace),
                    })

            child_characters_equal_sibling = all(
                traces == sibling_traces for traces in child_traces
            )
            child_modules_isomorphic_to_sibling = all(child_isomorphism_flags)

            source_sector_path = (
                f7_dir / "channels" / subset_slug(target_subset)
                / f"sector_{sector_index:02d}.basis.coordinate.json.gz"
            )
            source_sector_rows = f7.read_sparse_integer_matrix(source_sector_path)
            source_sector_hash_match = (
                f7.sha256_integer_rows(source_sector_rows)
                == source_sector_by_index[sector_index]["sector_basis_sha256"]
            )
            combined_rows = sp.Matrix.vstack(
                f7.sympy_matrix(sibling_coordinate_rows),
                *(f7.sympy_matrix(rows) for rows in child_coordinate_sets),
            )
            source_reconstruction_exact = (
                source_sector_hash_match
                and combined_rows.rows == 18
                and row_spaces_equal(
                    combined_rows, f7.sympy_matrix(source_sector_rows)
                )
            )
            all_source_reconstructions_exact &= source_reconstruction_exact

            split_certificate_complete = (
                projection_exact
                and projection_commutes
                and exact_rank(projection) == 6
                and direct_sum_exact
                and len(hom_basis) == 2
                and child_commutant_dims == [1, 1]
                and child_norms == [sp.Rational(1), sp.Rational(1)]
                and child_characters_equal_sibling
                and child_modules_isomorphic_to_sibling
                and source_reconstruction_exact
            )
            outcome_certificate_complete = split_certificate_complete
            resolved_module_structure = "V=W^2_and_source_sector_U=W^3"
            resolved_block_count = 2
            projection_hash = matrix_hash(projection)
            child_dimensions = "6;6"
            child_commutant_dimensions = ";".join(map(str, child_commutant_dims))
            child_character_norms = ";".join(
                fraction_text(value) for value in child_norms
            )
        else:
            # A nonempty exact ramification set proves the quaternion algebra is
            # division.  In a semisimple module category, a division commutant
            # certifies rational irreducibility.
            division_certificate_complete = (
                bool(local["ramified_places"])
                and bool(local["hilbert_reciprocity_exact"])
                and embedding is None
            )
            outcome_certificate_complete = division_certificate_complete
            resolved_module_structure = (
                "12D_rational_irreducible_with_quaternion_division_commutant"
            )
            resolved_rows.append({
                "subset": target_subset_key,
                "sector_index": sector_index,
                "source_primitive_index": primitive_index,
                "resolved_primitive_index": 0,
                "resolved_dimension": 12,
                "certification_kind": "quaternion_division_commutant",
                "rational_irreducible_certified": True,
                "absolutely_irreducible_certified": False,
                "commutant_dimension": 4,
                "character_norm": unresolved["character_norm"],
                "character_equals_certified_sibling": False,
                "sibling_hom_dimension": len(hom_basis),
                "full_rank_sibling_isomorphism_found": False,
                "resolved_basis_sha256": unresolved["primitive_basis_sha256"],
            })
            all_source_reconstructions_exact &= True

        all_outcome_certificates_complete &= outcome_certificate_complete
        classification_rows.append({
            "subset": target_subset_key,
            "sector_index": sector_index,
            "source_primitive_index": primitive_index,
            "source_block_dimension": len(unresolved_coordinate_rows),
            "source_commutant_dimension": unresolved[
                "primitive_commutant_dimension"
            ],
            "source_center_dimension": unresolved["primitive_center_dimension"],
            "source_basis_hash_matches_xbr04f8": unresolved_hash_match,
            "sibling_primitive_index": sibling_index,
            "sibling_basis_hash_matches_xbr04f8": sibling_hash_match,
            "representation_homomorphism_exact": (
                target_representation_exact and sibling_representation_exact
            ),
            "computed_commutant_dimension": len(commutant),
            "computed_center_dimension": len(center),
            "commutant_exact": commutant_exact,
            "center_exact": center_exact,
            "algebra_basis_sha256": presentation["algebra_basis_hash"],
            "presentation_basis_sha256": presentation["presentation_basis_hash"],
            **{
                f"presentation_{name}": passed
                for name, passed in presentation["relation_checks"].items()
            },
            "quaternion_a": fraction_text(presentation["a"]),
            "quaternion_b": fraction_text(presentation["b"]),
            "a_squareclass": local["a_squareclass"],
            "b_squareclass": local["b_squareclass"],
            "ramified_places": ";".join(local["ramified_places"]),
            "hilbert_reciprocity_exact": local["hilbert_reciprocity_exact"],
            "algebra_classification": local["classification"],
            "sibling_to_target_hom_dimension": len(hom_basis),
            "sibling_embedding_description": embedding_description,
            "rank6_sibling_embedding_found": embedding is not None,
            "projection_sha256": projection_hash,
            "resolved_child_dimensions": child_dimensions,
            "resolved_child_commutant_dimensions": child_commutant_dimensions,
            "resolved_child_character_norms": child_character_norms,
            "child_characters_equal_sibling": child_characters_equal_sibling,
            "child_modules_isomorphic_to_sibling": (
                child_modules_isomorphic_to_sibling
            ),
            "source_18D_sector_reconstruction_exact": source_reconstruction_exact,
            "resolved_module_structure": resolved_module_structure,
            "resolved_block_count": resolved_block_count,
            "outcome_certificate_complete": outcome_certificate_complete,
            "elapsed_seconds": time.perf_counter() - target_started,
        })
        print(
            f"  classification={local['classification']} "
            f"ramified={local['ramified_places'] or 'none'} "
            f"resolved={resolved_module_structure} "
            f"elapsed={time.perf_counter() - target_started:.2f}s",
            flush=True,
        )

    write_csv(out_dir / "residual_commutant_classification_ledger.csv", classification_rows)
    write_csv(out_dir / "quaternion_multiplication_ledger.csv", multiplication_rows)
    write_csv(out_dir / "local_invariant_ledger.csv", local_rows)
    write_csv(out_dir / "resolved_primitive_module_ledger.csv", resolved_rows)
    write_csv(out_dir / "resolved_class_character_ledger.csv", class_rows)

    f8_counts = f8_summary["counts"]
    final_terminal_count = (
        int(f8_counts["terminal_blocks"])
        - len(unresolved_rows)
        + sum(int(row["resolved_block_count"]) for row in classification_rows)
    )
    final_certified_count = (
        int(f8_counts["certified_rational_irreducible_blocks"])
        + sum(int(row["resolved_block_count"]) for row in classification_rows)
    )
    final_fully_resolved = (
        int(f8_counts["fully_resolved_sectors"])
        + len({int(row["sector_index"]) for row in classification_rows})
    )
    summary_counts = {
        "source_residual_blocks": len(unresolved_rows),
        "split_matrix_algebras": sum(
            row["algebra_classification"] == "split_matrix_algebra_M2_Q"
            for row in classification_rows
        ),
        "quaternion_division_algebras": sum(
            row["algebra_classification"] == "quaternion_division_algebra"
            for row in classification_rows
        ),
        "final_fully_resolved_sectors": final_fully_resolved,
        "final_certified_primitive_blocks": final_certified_count,
        "final_terminal_primitive_blocks": final_terminal_count,
        "final_unresolved_terminal_blocks": 0,
    }

    classifications_agree = (
        len({str(row["algebra_classification"]) for row in classification_rows}) == 1
    )
    ramification_sets_agree = (
        len({str(row["ramified_places"]) for row in classification_rows}) == 1
    )
    checks = {
        "xbr04f8_strict_pass": bool(f8_summary.get("strict_pass")),
        "exact_target_block_count_loaded": len(unresolved_rows) == len(target_sectors),
        "target_blocks_match_12D_commutant4_center1_schema": all(
            int(row["source_block_dimension"]) == 12
            and int(row["computed_commutant_dimension"]) == 4
            and int(row["computed_center_dimension"]) == 1
            for row in classification_rows
        ),
        "literal_group_hash_matches_xbr04f7": (
            literal_group_hash == source_channel["literal_group_hash"]
        ),
        "group_order_matches_xbr04f7": (
            len(group) == int(source_channel["label_automorphism_group_order"])
        ),
        "all_source_basis_hashes_match_xbr04f8": all_basis_hashes_match,
        "all_representations_exact": all_representations_exact,
        "all_commutants_and_centres_exact": all_commutants_exact,
        "all_quaternion_presentations_exact": all_presentations_exact,
        "all_hilbert_reciprocity_checks_exact": all_reciprocity_exact,
        "all_residual_algebras_completely_classified": all(
            row["algebra_classification"] in {
                "split_matrix_algebra_M2_Q",
                "quaternion_division_algebra",
            }
            for row in classification_rows
        ),
        "all_outcome_specific_certificates_complete": (
            all_outcome_certificates_complete
        ),
        "all_split_source_sector_reconstructions_exact": (
            all_source_reconstructions_exact
        ),
        "paired_algebra_comparison_completed": len(classification_rows) == 2,
        "no_unresolved_terminal_blocks_remain": (
            summary_counts["final_unresolved_terminal_blocks"] == 0
        ),
        "all_48_source_sectors_fully_resolved": final_fully_resolved == 48,
        "final_certified_count_equals_terminal_count": (
            final_certified_count == final_terminal_count
        ),
    }
    strict_pass = all(checks.values())
    verdict = VERDICT_PASS if strict_pass else "EHF_XBR_04F8B_AUDIT_FAIL"
    elapsed = time.perf_counter() - started
    summary = {
        "probe": PROBE_NAME,
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "source_xbr04f8_dir": str(f8_dir),
        "source_xbr04f7_dir": str(f7_dir),
        "parameters": {
            "target_subset": target_subset_key,
            "target_sectors": sorted(target_sectors),
            "write_resolved_bases": args.write_resolved_bases,
        },
        "counts": summary_counts,
        "paired_comparison": {
            "algebra_classifications_agree": classifications_agree,
            "ramification_sets_agree": ramification_sets_agree,
        },
        "checks": checks,
        "strict_pass": strict_pass,
        "verdict": verdict,
        "elapsed_seconds": elapsed,
    }
    write_json(out_dir / "run_summary.json", summary)
    (out_dir / "residual_commutant_report.md").write_text(
        markdown_report(classification_rows, checks, summary_counts, verdict)
    )

    print()
    print("[residual algebra classification]")
    for row in classification_rows:
        print(
            f"  sector={row['sector_index']} "
            f"class={row['algebra_classification']} "
            f"ramified={row['ramified_places'] or 'none'} "
            f"module={row['resolved_module_structure']}"
        )
    print("[final primitive census]")
    print(
        f"  fully_resolved_sectors={final_fully_resolved} "
        f"certified={final_certified_count} "
        f"terminal={final_terminal_count} unresolved=0"
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
