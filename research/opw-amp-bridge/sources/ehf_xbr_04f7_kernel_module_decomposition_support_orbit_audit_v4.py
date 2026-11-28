#!/usr/bin/env python3
r"""
EHF-XBR-04F7: Kernel Module Decomposition and Support-Orbit Audit

This probe consumes the completed EHF-XBR-04F6 exact chamber-kernel output.
It does not recompute chamber nullspaces.

For every singular proper OPW3 chamber it reconstructs the exact action of the
label-induced chamber automorphism group on the stored integer kernel basis and
then computes:

  * the exact rational central-isotypic decomposition of the kernel module;
  * exact sector characters and character norms;
  * absolute-irreducibility certificates when the character norm is one;
  * exact recurring module types for identical literal label groups;
  * coarse cross-group character/order fingerprints, explicitly diagnostic only;
  * basis-independent sector coordinate activity and projective coordinate classes;
  * automorphism-orbit restriction ranks, vanishing dimensions, and orbit-local
    support dimensions.

The central-isotypic decomposition is the common rational primary decomposition
of all conjugacy-class sums.  It is a canonical module decomposition determined
by the image of the centre of Q[G].  A sector with character norm greater than
one is not automatically split further: multiplicity, Galois packets, or Schur
structure may remain.  The script records that limitation instead of treating a
central-isotypic sector as an irreducible module without proof.

No physical interpretation is assigned to a module, character, sign sector, or
support pattern without a separate bridge argument.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import tempfile
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Set, Tuple

import sympy as sp

SCRIPT_VERSION = "ehf_xbr_04f7_v4_2026-07-30"
PROBE_NAME = "EHF-XBR-04F7"
VERDICT_PASS = "EHF_XBR_04F7_KERNEL_MODULE_DECOMPOSITION_SUPPORT_ORBIT_AUDIT_PASS"

Permutation = Tuple[int, ...]
Subset = Tuple[int, int, int]


# ---------------------------------------------------------------------------
# General I/O and scalar helpers
# ---------------------------------------------------------------------------


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_module(path: Path, module_name: str):
    """Load a source module with Python 3.12 dataclass compatibility.

    dataclasses resolves annotations through sys.modules while the class body is
    being processed.  Dynamic modules must therefore be registered before
    exec_module(), just as the normal import machinery registers them.
    """
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
    fieldnames: List[str] = []
    seen: Set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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


def integer(row: Mapping[str, object], key: str) -> int:
    value = str(row[key]).strip()
    if value.lower() in {"true", "false"}:
        return int(value.lower() == "true")
    return int(Fraction(value))


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
    if isinstance(value, sp.Rational):
        if value.q == 1:
            return str(value.p)
        return f"{value.p}/{value.q}"
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return str(value)


def stable_json_hash(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_integer_rows(rows: Sequence[Sequence[int]]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        digest.update((",".join(map(str, row)) + "\n").encode("utf-8"))
    return digest.hexdigest()


# ---------------------------------------------------------------------------
# Sparse basis I/O
# ---------------------------------------------------------------------------


def read_sparse_integer_matrix(path: Path) -> List[List[int]]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("ring") != "ZZ":
        raise ValueError(f"expected ZZ matrix in {path}")
    nrows, ncols = map(int, payload["shape"])
    rows = [[0] * ncols for _ in range(nrows)]
    for i, j, value in payload["entries"]:
        rows[int(i)][int(j)] = int(value)
    expected = payload.get("sha256_dense_rows", "")
    if expected and sha256_integer_rows(rows) != expected:
        raise ValueError(f"kernel basis hash mismatch in {path}")
    return rows


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


# ---------------------------------------------------------------------------
# Exact matrix helpers
# ---------------------------------------------------------------------------


def sympy_matrix(rows: Sequence[Sequence[object]]) -> sp.Matrix:
    return sp.Matrix([
        [sp.Rational(str(value)) for value in row]
        for row in rows
    ])


def exact_matrix_rank(matrix: sp.Matrix) -> int:
    """Exact rank through SymPy's domain-matrix engine."""
    from sympy.polys.matrices import DomainMatrix
    if matrix.rows == 0 or matrix.cols == 0:
        return 0
    return int(DomainMatrix.from_Matrix(matrix).rank())


def matrix_payload(matrix: sp.Matrix) -> List[List[str]]:
    return [
        [fraction_text(matrix[i, j]) for j in range(matrix.cols)]
        for i in range(matrix.rows)
    ]


def matrix_hash(matrix: sp.Matrix) -> str:
    return stable_json_hash(matrix_payload(matrix))


def primitive_integer_row(values: Sequence[object]) -> List[int]:
    rationals = [sp.Rational(value) for value in values]
    denominator_lcm = 1
    for value in rationals:
        denominator_lcm = math.lcm(denominator_lcm, int(value.q))
    integers = [int(value * denominator_lcm) for value in rationals]
    common = 0
    for value in integers:
        common = math.gcd(common, abs(value))
    if common > 1:
        integers = [value // common for value in integers]
    first = next((value for value in integers if value), 0)
    if first < 0:
        integers = [-value for value in integers]
    return integers


def canonical_integer_row_basis(matrix: sp.Matrix) -> List[List[int]]:
    if matrix.rows == 0 or matrix.cols == 0:
        return []
    reduced, _ = matrix.rref()
    rows: List[List[int]] = []
    for i in range(reduced.rows):
        row = [reduced[i, j] for j in range(reduced.cols)]
        if any(value != 0 for value in row):
            rows.append(primitive_integer_row(row))
    return rows


def canonical_column_basis(matrix: sp.Matrix) -> sp.Matrix:
    if matrix.cols == 0:
        return sp.zeros(matrix.rows, 0)
    reduced, _ = matrix.T.rref()
    rank = matrix.rank()
    rows = [
        [reduced[i, j] for j in range(reduced.cols)]
        for i in range(rank)
    ]
    return sp.Matrix(rows).T


def restriction_matrix(operator: sp.Matrix, basis: sp.Matrix) -> sp.Matrix:
    """Return A with operator*basis = basis*A for a full-column-rank basis."""
    if basis.cols == 0:
        return sp.zeros(0, 0)
    if basis.rank() != basis.cols:
        raise ValueError("restriction basis is not independent")
    _, pivot_rows_tuple = basis.T.rref()
    pivot_rows = list(pivot_rows_tuple)
    if len(pivot_rows) != basis.cols:
        raise RuntimeError("failed to find restriction pivot rows")
    square = basis.extract(pivot_rows, list(range(basis.cols)))
    target = (operator * basis).extract(pivot_rows, list(range(basis.cols)))
    restricted = square.inv() * target
    if operator * basis != basis * restricted:
        raise ArithmeticError("operator does not preserve the supplied subspace")
    return restricted


def restriction_workspace(basis: sp.Matrix) -> Tuple[List[int], sp.Matrix]:
    """Cache the pivot rows and inverse used by repeated restrictions.

    The v3 diagnostic path recomputed basis rank, an RREF, and a matrix inverse
    for every group element and every class sum.  On the 64-dimensional kernel
    this repeated the same exact work hundreds of times.  A workspace is exact
    and basis-specific, and is reused throughout one sector.
    """
    if basis.cols == 0:
        return [], sp.zeros(0, 0)
    _, pivot_rows_tuple = basis.T.rref()
    pivot_rows = list(pivot_rows_tuple)
    if len(pivot_rows) != basis.cols:
        raise ValueError("restriction basis is not independent")
    square = basis.extract(pivot_rows, list(range(basis.cols)))
    return pivot_rows, square.inv()


def restriction_matrix_cached(
    operator: sp.Matrix,
    basis: sp.Matrix,
    workspace: Tuple[Sequence[int], sp.Matrix],
    *,
    verify: bool = True,
) -> sp.Matrix:
    """Exact restriction using a cached sector workspace."""
    if basis.cols == 0:
        return sp.zeros(0, 0)
    pivot_rows, square_inverse = workspace
    product = operator * basis
    target = product.extract(list(pivot_rows), list(range(basis.cols)))
    restricted = square_inverse * target
    if verify and product != basis * restricted:
        raise ArithmeticError("operator does not preserve the supplied subspace")
    return restricted


def independent_integer_rows(matrix: sp.Matrix) -> List[List[int]]:
    """Integerise an already independent deterministic row basis.

    sector_basis.T * kernel_basis has independent rows because both maps are
    injective on the sector.  RREF canonicalisation over hundreds of chamber
    coordinates is therefore redundant and was a major post-decomposition
    bottleneck in v3.
    """
    rows = [
        primitive_integer_row([matrix[i, j] for j in range(matrix.cols)])
        for i in range(matrix.rows)
    ]
    if len(rows) != matrix.rows or any(not any(row) for row in rows):
        raise ArithmeticError("sector coordinate row vanished")
    return rows


def polynomial_matrix(poly: sp.Poly, matrix: sp.Matrix) -> sp.Matrix:
    identity = sp.eye(matrix.rows)
    result = sp.zeros(matrix.rows)
    for coefficient in poly.all_coeffs():
        result = result * matrix + sp.Rational(coefficient) * identity
    return result


def charpoly_factor_payload(matrix: sp.Matrix) -> List[Tuple[str, int]]:
    variable = sp.Symbol("x")
    poly = sp.Poly(matrix.charpoly(variable).as_expr(), variable, domain=sp.QQ)
    _, factors = sp.factor_list(poly)
    return [(str(factor.as_expr()), int(exponent)) for factor, exponent in factors]


def split_subspace_by_central_operator(
    basis: sp.Matrix,
    operator: sp.Matrix,
) -> List[sp.Matrix]:
    restricted = restriction_matrix(operator, basis)
    if restricted.rows <= 1:
        return [basis]
    scalar = restricted[0, 0]
    if restricted == scalar * sp.eye(restricted.rows):
        return [basis]

    variable = sp.Symbol("x")
    poly = sp.Poly(restricted.charpoly(variable).as_expr(), variable, domain=sp.QQ)
    _, factors = sp.factor_list(poly)
    distinct = [factor for factor, _ in factors]
    if len(distinct) <= 1:
        return [basis]

    pieces: List[sp.Matrix] = []
    for factor in distinct:
        kernel = polynomial_matrix(factor, restricted).nullspace()
        if not kernel:
            continue
        coordinate_basis = sp.Matrix.hstack(*kernel)
        piece = canonical_column_basis(basis * coordinate_basis)
        if piece.cols:
            pieces.append(piece)

    if not pieces:
        return [basis]
    combined = sp.Matrix.hstack(*pieces)
    if combined.cols != basis.cols or combined.rank() != basis.cols:
        raise ArithmeticError("central primary decomposition did not form a direct sum")
    return pieces


def central_isotypic_decomposition(
    dimension: int,
    central_operators: Sequence[sp.Matrix],
    progress_label: str | None = None,
) -> List[sp.Matrix]:
    sectors = [sp.eye(dimension)]
    total = len(central_operators)
    for operator_index, operator in enumerate(central_operators, start=1):
        operator_started = time.perf_counter()
        before = len(sectors)
        if progress_label is not None:
            print(
                f"{progress_label} phase=central_operator "
                f"operator={operator_index}/{total} sectors={before}",
                flush=True,
            )
        refined: List[sp.Matrix] = []
        for sector_index, sector in enumerate(sectors, start=1):
            sector_started = time.perf_counter()
            if progress_label is not None:
                print(
                    f"{progress_label} phase=central_operator_sector "
                    f"operator={operator_index}/{total} "
                    f"sector={sector_index}/{before} dim={sector.cols}",
                    flush=True,
                )
            pieces = split_subspace_by_central_operator(sector, operator)
            refined.extend(pieces)
            if progress_label is not None:
                print(
                    f"{progress_label} phase=central_operator_sector_done "
                    f"operator={operator_index}/{total} "
                    f"sector={sector_index}/{before} dim={sector.cols} "
                    f"pieces={len(pieces)} "
                    f"piece_dims={';'.join(str(piece.cols) for piece in pieces)} "
                    f"elapsed={time.perf_counter() - sector_started:.2f}s",
                    flush=True,
                )
        sectors = refined
        if progress_label is not None:
            print(
                f"{progress_label} phase=central_operator_done "
                f"operator={operator_index}/{total} sectors={len(sectors)} "
                f"split={len(sectors) - before} "
                f"elapsed={time.perf_counter() - operator_started:.2f}s",
                flush=True,
            )
    # Every newly created piece is canonicalised at the split where it is
    # created, and every split is checked as an exact direct sum.  Re-running
    # rational RREF on every final sector and then ranking the 64 x 64 combined
    # matrix is redundant and became pathological after the final operator in
    # the largest channel.
    if progress_label is not None:
        print(
            f"{progress_label} phase=central_finalize sectors={len(sectors)} "
            f"dims={';'.join(str(sector.cols) for sector in sectors)}",
            flush=True,
        )
    sectors.sort(key=lambda basis: (basis.cols, matrix_hash(basis)))
    if sum(sector.cols for sector in sectors) != dimension:
        raise ArithmeticError("central sectors do not reconstruct the full module")
    if progress_label is not None:
        print(
            f"{progress_label} phase=central_finalize_done sectors={len(sectors)}",
            flush=True,
        )
    return sectors


def projective_column_key(values: Sequence[object]) -> Tuple[int, ...] | None:
    row = primitive_integer_row(values)
    if not any(row):
        return None
    return tuple(row)


# ---------------------------------------------------------------------------
# Graph, group, and representation helpers
# ---------------------------------------------------------------------------


def local_neighbors(
    global_adjacency: Sequence[Sequence[int]],
    global_ids: Sequence[int],
) -> List[List[int]]:
    local = {global_id: index for index, global_id in enumerate(global_ids)}
    return [
        sorted(local[target] for target in global_adjacency[global_id] if target in local)
        for global_id in global_ids
    ]


def permutation_orbits(
    size: int,
    images: Sequence[Sequence[int]],
) -> List[List[int]]:
    unseen = set(range(size))
    cells: List[List[int]] = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        queue = [seed]
        while queue:
            current = queue.pop()
            for image in images:
                target = int(image[current])
                if target not in orbit:
                    orbit.add(target)
                    queue.append(target)
        cell = sorted(orbit)
        unseen.difference_update(cell)
        cells.append(cell)
    return cells


def permutation_cycle_type(permutation: Permutation) -> str:
    seen: Set[int] = set()
    lengths: List[int] = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return ".".join(map(str, sorted(lengths, reverse=True)))


def literal_group_hash(group: Iterable[Permutation]) -> str:
    return stable_json_hash([list(item) for item in sorted(group)])


def conjugacy_classes(group: Set[Permutation], group_ops) -> List[List[Permutation]]:
    unseen = set(group)
    classes: List[List[Permutation]] = []
    while unseen:
        representative = min(unseen, key=group_ops.permutation_cycle_text)
        conjugates = {
            group_ops.compose_permutations(
                h,
                group_ops.compose_permutations(
                    representative,
                    group_ops.inverse_permutation(h),
                ),
            )
            for h in group
        }
        cell = sorted(conjugates, key=group_ops.permutation_cycle_text)
        unseen.difference_update(cell)
        classes.append(cell)
    classes.sort(
        key=lambda cell: (
            len(cell),
            group_ops.permutation_order(cell[0]),
            group_ops.permutation_cycle_text(cell[0]),
        )
    )
    return classes


def representation_from_kernel_basis(
    kernel_rows: Sequence[Sequence[int]],
    transformed_rows: Sequence[Sequence[int]],
) -> sp.Matrix:
    basis = sympy_matrix(kernel_rows)
    target = sympy_matrix(transformed_rows)
    _, pivot_columns_tuple = basis.rref()
    pivot_columns = list(pivot_columns_tuple)
    if len(pivot_columns) != basis.rows:
        raise ValueError("kernel basis is not independent")
    pivot_square = basis.extract(
        list(range(basis.rows)),
        pivot_columns,
    )
    target_square = target.extract(
        list(range(target.rows)),
        pivot_columns,
    )
    row_action = target_square * pivot_square.inv()
    if row_action * basis != target:
        raise ArithmeticError("failed to reconstruct exact kernel representation")
    return row_action.T  # standard column-action convention


def representation_homomorphism_exact(
    group: Set[Permutation],
    representations: Mapping[Permutation, sp.Matrix],
    generators: Sequence[Permutation],
    group_ops,
) -> bool:
    for generator in generators:
        for element in group:
            left = group_ops.compose_permutations(generator, element)
            right = group_ops.compose_permutations(element, generator)
            if representations[left] != representations[generator] * representations[element]:
                return False
            if representations[right] != representations[element] * representations[generator]:
                return False
    return True


def class_trace_constant(
    classes: Sequence[Sequence[Permutation]],
    representations: Mapping[Permutation, sp.Matrix],
) -> bool:
    return all(
        len({sp.trace(representations[element]) for element in cell}) == 1
        for cell in classes
    )


# ---------------------------------------------------------------------------
# Sector character and support diagnostics
# ---------------------------------------------------------------------------


def sector_character_data(
    sector_basis: sp.Matrix,
    group_elements: Sequence[Permutation],
    representations: Mapping[Permutation, sp.Matrix],
    group_ops,
) -> Tuple[Dict[Permutation, sp.Rational], Dict[Permutation, int], Dict[Permutation, int]]:
    traces: Dict[Permutation, sp.Rational] = {}
    fixed: Dict[Permutation, int] = {}
    anti_fixed: Dict[Permutation, int] = {}
    identity = sp.eye(sector_basis.cols)
    for element in group_elements:
        restricted = restriction_matrix(representations[element], sector_basis)
        traces[element] = sp.Rational(sp.trace(restricted))
        fixed[element] = int(sector_basis.cols - (restricted - identity).rank())
        if group_ops.permutation_order(element) == 2:
            anti_fixed[element] = int(sector_basis.cols - (restricted + identity).rank())
    return traces, fixed, anti_fixed


def character_norm(
    traces: Mapping[Permutation, sp.Rational],
) -> sp.Rational:
    return sp.Rational(sum(value * value for value in traces.values()), len(traces))


def order_trace_histogram(
    group_elements: Sequence[Permutation],
    traces: Mapping[Permutation, sp.Rational],
    group_ops,
) -> str:
    counter = Counter(
        (group_ops.permutation_order(element), fraction_text(traces[element]))
        for element in group_elements
    )
    return ";".join(
        f"o{order}:t{trace}:n{count}"
        for (order, trace), count in sorted(counter.items())
    )


def fixed_dimension_histogram(
    values: Mapping[Permutation, int],
    group_elements: Sequence[Permutation],
    group_ops,
) -> str:
    counter = Counter(
        (group_ops.permutation_order(element), int(values[element]))
        for element in group_elements
    )
    return ";".join(
        f"o{order}:d{dimension}:n{count}"
        for (order, dimension), count in sorted(counter.items())
    )


def sector_class_character_data(
    sector_basis: sp.Matrix,
    classes: Sequence[Sequence[Permutation]],
    representations: Mapping[Permutation, sp.Matrix],
    group_ops,
    workspace: Tuple[Sequence[int], sp.Matrix],
) -> Tuple[List[sp.Matrix], List[sp.Rational], List[int], List[int | None]]:
    """Compute character/fixed data once per conjugacy class.

    Trace, +1-eigenspace dimension, and (for involutions) -1-eigenspace
    dimension are conjugacy invariants.  Processing class representatives
    replaces hundreds of repeated exact restrictions by at most the class count.
    """
    restricted_by_class: List[sp.Matrix] = []
    traces: List[sp.Rational] = []
    fixed: List[int] = []
    anti: List[int | None] = []
    identity = sp.eye(sector_basis.cols)
    for cell in classes:
        representative = cell[0]
        restricted = restriction_matrix_cached(
            representations[representative], sector_basis, workspace
        )
        restricted_by_class.append(restricted)
        traces.append(sp.Rational(sp.trace(restricted)))
        fixed.append(int(sector_basis.cols - exact_matrix_rank(restricted - identity)))
        if group_ops.permutation_order(representative) == 2:
            anti.append(int(sector_basis.cols - exact_matrix_rank(restricted + identity)))
        else:
            anti.append(None)
    return restricted_by_class, traces, fixed, anti


def character_norm_from_classes(
    classes: Sequence[Sequence[Permutation]],
    traces: Sequence[sp.Rational],
    group_order: int,
) -> sp.Rational:
    return sp.Rational(
        sum(len(cell) * trace * trace for cell, trace in zip(classes, traces)),
        group_order,
    )


def order_trace_histogram_from_classes(
    classes: Sequence[Sequence[Permutation]],
    traces: Sequence[sp.Rational],
    group_ops,
) -> str:
    counter: Counter = Counter()
    for cell, trace in zip(classes, traces):
        counter[
            (group_ops.permutation_order(cell[0]), fraction_text(trace))
        ] += len(cell)
    return ";".join(
        f"o{order}:t{trace}:n{count}"
        for (order, trace), count in sorted(counter.items())
    )


def fixed_dimension_histogram_from_classes(
    classes: Sequence[Sequence[Permutation]],
    fixed_dimensions: Sequence[int],
    group_ops,
) -> str:
    counter: Counter = Counter()
    for cell, dimension in zip(classes, fixed_dimensions):
        counter[
            (group_ops.permutation_order(cell[0]), int(dimension))
        ] += len(cell)
    return ";".join(
        f"o{order}:d{dimension}:n{count}"
        for (order, dimension), count in sorted(counter.items())
    )


def support_orbit_rows(
    subset: Subset,
    regime: str,
    sector_index: int,
    sector_rows: Sequence[Sequence[int]],
    orbits: Sequence[Sequence[int]],
) -> Tuple[List[dict], dict]:
    matrix = sympy_matrix(sector_rows)
    dimension = matrix.rows
    size = matrix.cols
    active = [
        any(matrix[row, column] != 0 for row in range(dimension))
        for column in range(size)
    ]
    projective = [
        projective_column_key([matrix[row, column] for row in range(dimension)])
        for column in range(size)
    ]
    projective_counts = Counter(key for key in projective if key is not None)

    orbit_rows: List[dict] = []
    orbit_union_exact = True
    active_orbits = 0
    max_restriction_rank = 0
    max_orbit_local_dimension = 0
    full_rank_orbits = 0

    all_columns = set(range(size))
    for orbit_index, orbit in enumerate(orbits):
        orbit_columns = list(orbit)
        outside_columns = sorted(all_columns.difference(orbit_columns))
        active_count = sum(active[column] for column in orbit_columns)
        all_or_none = active_count in {0, len(orbit_columns)}
        orbit_union_exact &= all_or_none
        if active_count:
            active_orbits += 1
        restriction_rank = exact_matrix_rank(matrix[:, orbit_columns])
        outside_rank = exact_matrix_rank(matrix[:, outside_columns]) if outside_columns else 0
        vanishing_on_orbit_dimension = dimension - restriction_rank
        orbit_local_dimension = dimension - outside_rank
        max_restriction_rank = max(max_restriction_rank, restriction_rank)
        max_orbit_local_dimension = max(max_orbit_local_dimension, orbit_local_dimension)
        full_rank_orbits += int(restriction_rank == dimension)
        orbit_projective_classes = len({
            projective[column]
            for column in orbit_columns
            if projective[column] is not None
        })
        orbit_rows.append({
            "subset": subset_text(subset),
            "regime": regime,
            "sector_index": sector_index,
            "orbit_index": orbit_index,
            "orbit_size": len(orbit_columns),
            "active_coordinate_count": active_count,
            "activity_all_or_none": all_or_none,
            "restriction_rank": restriction_rank,
            "vanishing_on_orbit_dimension": vanishing_on_orbit_dimension,
            "orbit_local_dimension": orbit_local_dimension,
            "projective_coordinate_class_count": orbit_projective_classes,
            "coordinates": ";".join(map(str, orbit_columns)),
        })

    support_sizes = [sum(value != 0 for value in row) for row in sector_rows]
    signature = ";".join(
        f"s{row['orbit_size']}:r{row['restriction_rank']}:l{row['orbit_local_dimension']}:a{row['active_coordinate_count']}"
        for row in sorted(
            orbit_rows,
            key=lambda item: (
                int(item["orbit_size"]),
                int(item["restriction_rank"]),
                int(item["orbit_local_dimension"]),
                int(item["orbit_index"]),
            ),
        )
    )
    summary = {
        "coordinate_count": size,
        "active_coordinate_count": sum(active),
        "forced_zero_coordinate_count": size - sum(active),
        "full_coordinate_support": all(active),
        "projective_coordinate_class_count": len(projective_counts),
        "largest_projective_coordinate_class": max(projective_counts.values(), default=0),
        "automorphism_orbit_count": len(orbits),
        "active_automorphism_orbit_count": active_orbits,
        "support_is_union_of_automorphism_orbits": orbit_union_exact,
        "maximum_single_orbit_restriction_rank": max_restriction_rank,
        "full_rank_orbit_count": full_rank_orbits,
        "maximum_single_orbit_local_dimension": max_orbit_local_dimension,
        "has_nonzero_single_orbit_supported_vector": max_orbit_local_dimension > 0,
        "canonical_sector_basis_support_min": min(support_sizes, default=0),
        "canonical_sector_basis_support_max": max(support_sizes, default=0),
        "canonical_sector_basis_support_mean": fraction_text(
            sp.Rational(sum(support_sizes), len(support_sizes)) if support_sizes else 0
        ),
        "support_orbit_signature": signature,
    }
    return orbit_rows, summary


def vector_annihilated(neighbors: Sequence[Sequence[int]], vector: Sequence[int]) -> bool:
    return all(sum(vector[target] for target in targets) == 0 for targets in neighbors)


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


def markdown_report(
    channel_rows: Sequence[Mapping[str, object]],
    sector_rows: Sequence[Mapping[str, object]],
    recurrence_rows: Sequence[Mapping[str, object]],
    checks: Mapping[str, bool],
    verdict: str,
) -> str:
    absolute = sum(truthy(row["absolutely_irreducible_certified"]) for row in sector_rows)
    full_support = sum(truthy(row["full_coordinate_support"]) for row in sector_rows)
    orbit_local = sum(
        truthy(row["has_nonzero_single_orbit_supported_vector"])
        for row in sector_rows
    )
    exact_recurrences = sum(
        row["recurrence_kind"] == "exact_same_literal_group_character"
        for row in recurrence_rows
    )
    lines = [
        "# EHF-XBR-04F7: Kernel Module Decomposition and Support-Orbit Audit",
        "",
        f"Verdict: `{verdict}`",
        "",
        "## Scope",
        "",
        "The probe consumed the exact integer chamber kernels written by XBR-04F6 and reconstructed the exact label-automorphism representations. It did not recompute chamber nullspaces.",
        "",
        "## Headline census",
        "",
        f"- singular channels: {len(channel_rows)}",
        f"- rational central-isotypic sectors: {len(sector_rows)}",
        f"- sectors certified absolutely irreducible by character norm one: {absolute}",
        f"- sectors with full coordinate support: {full_support}",
        f"- sectors containing a nonzero vector supported on a single automorphism orbit: {orbit_local}",
        f"- exact recurring module-type groups: {exact_recurrences}",
        "",
        "## Interpretation boundary",
        "",
        "The central-isotypic decomposition is exact. A sector with character norm greater than one can still contain multiplicity, Galois-conjugate constituents, or nontrivial Schur structure. Such a sector is not labelled irreducible without a separate certificate.",
        "",
        "Canonical basis support ranges are basis-dependent diagnostics. Coordinate activity, projective coordinate classes, orbit restriction ranks, and orbit-local dimensions are basis-independent properties of the sector subspace.",
        "",
        "## Channel ledger",
        "",
        "| chamber | regime | kernel dim | sectors | absolute sectors | group order |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in channel_rows:
        lines.append(
            f"| {row['subset']} | {row['regime']} | {row['kernel_dimension']} | "
            f"{row['central_isotypic_sector_count']} | "
            f"{row['absolutely_irreducible_sector_count']} | "
            f"{row['label_automorphism_group_order']} |"
        )
    lines.extend([
        "",
        "## Integrity checks",
        "",
    ])
    for name, passed in checks.items():
        lines.append(f"- `{name}`: {passed}")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def self_test() -> None:
    # C2 acting as 1 (+) 2(-): centre must split dimensions 1 and 2.
    identity = sp.eye(3)
    sign = sp.diag(1, -1, -1)
    sectors = central_isotypic_decomposition(3, [identity + 2 * sign, sign])
    assert sorted(sector.cols for sector in sectors) == [1, 2]

    group = {(0, 1), (1, 0)}

    class Ops:
        @staticmethod
        def permutation_order(permutation):
            return 1 if permutation == (0, 1) else 2

    representations = {(0, 1): identity, (1, 0): sign}
    elements = sorted(group)
    norms = []
    for sector in sectors:
        traces, fixed, anti = sector_character_data(
            sector, elements, representations, Ops
        )
        norms.append(character_norm(traces))
        assert all(value >= 0 for value in fixed.values())
        assert anti[(1, 0)] >= 0
    assert sorted(norms) == [1, 4]

    chamber_basis = sp.eye(3)
    sector_rows = canonical_integer_row_basis(sectors[0].T * chamber_basis)
    orbit_rows, support = support_orbit_rows(
        (1, 2, 3), "test", 0, sector_rows, [[0], [1], [2]]
    )
    assert len(orbit_rows) == 3
    assert support["support_is_union_of_automorphism_orbits"]

    poly = sp.Poly(sp.Symbol("x") - 1, sp.Symbol("x"), domain=sp.QQ)
    assert polynomial_matrix(poly, sp.eye(2)) == sp.zeros(2)

    # Python 3.12 regression guard: @dataclass consults sys.modules while a
    # dynamically loaded module is executing.
    with tempfile.TemporaryDirectory() as temporary_directory:
        module_path = Path(temporary_directory) / "dynamic_dataclass_module.py"
        module_path.write_text(
            "from dataclasses import dataclass\n"
            "@dataclass\n"
            "class Record:\n"
            "    value: int\n"
        )
        module_name = "ehf_xbr_04f7_selftest_dataclass"
        sys.modules.pop(module_name, None)
        loaded = load_module(module_path, module_name)
        assert loaded.Record(7).value == 7
        assert sys.modules[module_name] is loaded
        sys.modules.pop(module_name, None)

    # Regression: one generic central separator plus all class sums is sufficient;
    # no squared-coefficient generic operator is required.
    synthetic_ops = [sp.diag(1, 1, -1, -1), sp.diag(2, 2, 3, 3)]
    synthetic_sectors = central_isotypic_decomposition(4, synthetic_ops)
    assert sorted(sector.cols for sector in synthetic_sectors) == [2, 2]

    # Cached restriction and class-compressed character diagnostics must agree
    # with the direct element-by-element path.
    workspace = restriction_workspace(sectors[0])
    assert restriction_matrix_cached(identity, sectors[0], workspace) == sp.eye(1)
    class_cells = [[(0, 1)], [(1, 0)]]
    restricted, class_traces, class_fixed, class_anti = sector_class_character_data(
        sectors[0], class_cells, representations, Ops, workspace
    )
    direct_traces, direct_fixed, direct_anti = sector_character_data(
        sectors[0], elements, representations, Ops
    )
    assert character_norm_from_classes(class_cells, class_traces, 2) == character_norm(direct_traces)
    assert class_traces == [direct_traces[(0, 1)], direct_traces[(1, 0)]]
    assert class_fixed == [direct_fixed[(0, 1)], direct_fixed[(1, 0)]]
    assert class_anti[1] == direct_anti[(1, 0)]
    independent_rows = independent_integer_rows(sp.Matrix([[sp.Rational(1, 2), 0], [0, sp.Rational(2, 3)]]))
    assert independent_rows == [[1, 0], [0, 1]]

    print("EHF-XBR-04F7 self-test PASS")


# ---------------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Decompose exact OPW3 chamber kernels as rational group modules."
    )
    parser.add_argument("--xbr04f6-dir")
    parser.add_argument("--xbr04f-script")
    parser.add_argument("--opw-base-script")
    parser.add_argument("--amp-base-script")
    parser.add_argument("--amp-rank-script")
    parser.add_argument(
        "--write-sector-bases",
        choices=("none", "sparse"),
        default="sparse",
    )
    parser.add_argument("--out-dir", default="runs/ehf_xbr_04f7")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    required_names = (
        "xbr04f6_dir",
        "xbr04f_script",
        "opw_base_script",
        "amp_base_script",
        "amp_rank_script",
    )
    missing = [name for name in required_names if not getattr(args, name)]
    if missing:
        parser.error("missing required arguments: " + ", ".join(missing))

    started = time.perf_counter()
    f6_dir = Path(args.xbr04f6_dir).resolve()
    xbr04f_path = Path(args.xbr04f_script).resolve()
    opw_path = Path(args.opw_base_script).resolve()
    amp_base_path = Path(args.amp_base_script).resolve()
    amp_rank_path = Path(args.amp_rank_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    channel_out_root = out_dir / "channels"
    out_dir.mkdir(parents=True, exist_ok=True)
    channel_out_root.mkdir(parents=True, exist_ok=True)

    required_paths = (
        f6_dir / "run_summary.json",
        f6_dir / "kernel_channel_ledger.csv",
        xbr04f_path,
        opw_path,
        amp_base_path,
        amp_rank_path,
    )
    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(path)

    f6_summary = read_json(f6_dir / "run_summary.json")
    channel_source_rows = read_csv(f6_dir / "kernel_channel_ledger.csv")
    channel_source_rows.sort(key=lambda row: parse_subset(row["subset"]))

    xbr04f = load_module(xbr04f_path, "ehf_xbr_04f7_xbr04f")
    opw = load_module(opw_path, "ehf_xbr_04f7_opw")
    amp_base = load_module(amp_base_path, "ehf_xbr_04f7_amp_base")
    amp_rank = load_module(amp_rank_path, "ehf_xbr_04f7_amp_rank")

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
    print("EHF-XBR-04F7: KERNEL MODULE DECOMPOSITION AND SUPPORT-ORBIT AUDIT")
    print("=" * 132)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"XBR-04F6 directory:   {f6_dir}")
    print(f"singular channels:    {len(channel_source_rows)}")
    print(f"write sector bases:   {args.write_sector_bases}")
    print(f"output directory:     {out_dir}")
    print(f"strict:               {args.strict}")
    print()

    channel_rows: List[dict] = []
    sector_rows: List[dict] = []
    class_rows: List[dict] = []
    support_rows: List[dict] = []

    all_basis_hashes_match = True
    all_group_orders_match = True
    all_representation_images_match = True
    all_homomorphisms_exact = True
    all_class_traces_constant = True
    all_central_operators_commute = True
    all_decompositions_direct = True
    all_sectors_invariant = True
    all_sectors_central_pure = True
    all_character_norms_integral = True
    all_support_orbit_unions_exact = True
    all_sector_vectors_in_kernel = True

    for channel_number, source in enumerate(channel_source_rows, start=1):
        channel_started = time.perf_counter()
        subset = parse_subset(source["subset"])
        subset_key = subset_text(subset)
        regime = str(source["regime"])
        chamber_size = integer(source, "source_chamber_size")
        kernel_dimension = integer(source, "kernel_basis_dimension")
        basis_path = (
            f6_dir
            / "channels"
            / subset_slug(subset)
            / "kernel_basis.coordinate.json.gz"
        )
        if not basis_path.exists():
            raise FileNotFoundError(
                f"missing XBR-04F6 sparse basis for {subset_key}: {basis_path}"
            )
        kernel_rows = read_sparse_integer_matrix(basis_path)
        if len(kernel_rows) != kernel_dimension:
            raise ValueError(f"kernel dimension mismatch for {subset_key}")
        if kernel_rows and len(kernel_rows[0]) != chamber_size:
            raise ValueError(f"kernel width mismatch for {subset_key}")
        basis_hash_match = (
            sha256_integer_rows(kernel_rows) == source["kernel_basis_sha256"]
        )
        all_basis_hashes_match &= basis_hash_match

        source_key = amp_rank.key_from_subset_9(subset)
        source_cycles = source_fibres[source_key]
        global_ids = [
            index9[tuple(label - 1 for label in cycle)]
            for cycle in source_cycles
        ]
        neighbors = local_neighbors(graph9.adjacency, global_ids)

        print(
            f"[channel {channel_number}/{len(channel_source_rows)}] A={subset} "
            f"phase=representation kernel_dim={kernel_dimension} size={chamber_size}",
            flush=True,
        )

        candidates = xbr04f.candidate_stabilizer_permutations(subset)
        group: Set[Permutation] = set()
        state_images: Dict[Permutation, List[int]] = {}
        representations: Dict[Permutation, sp.Matrix] = {}
        for candidate in candidates:
            image = xbr04f.chamber_state_permutation(
                candidate, global_ids, cycles9, index9
            )
            if image is None or not xbr04f.adjacency_automorphism_exact(image, neighbors):
                continue
            transformed = xbr04f.permute_coordinate_rows(kernel_rows, image)
            group.add(candidate)
            state_images[candidate] = image
            representations[candidate] = representation_from_kernel_basis(
                kernel_rows, transformed
            )

        group_order_match = len(group) == integer(source, "label_automorphism_group_order")
        all_group_orders_match &= group_order_match
        representation_image_order = len({matrix_hash(value) for value in representations.values()})
        image_order_match = representation_image_order == integer(
            source, "kernel_representation_image_order"
        )
        all_representation_images_match &= image_order_match

        generators = xbr04f.greedy_group_generators(group)
        homomorphism_exact = representation_homomorphism_exact(
            group, representations, generators, xbr04f
        )
        all_homomorphisms_exact &= homomorphism_exact

        group_elements = sorted(group, key=xbr04f.permutation_cycle_text)
        classes = conjugacy_classes(group, xbr04f)
        traces_constant = class_trace_constant(classes, representations)
        all_class_traces_constant &= traces_constant

        class_sums: List[sp.Matrix] = []
        for cell in classes:
            class_sum = sp.zeros(kernel_dimension)
            for element in cell:
                class_sum += representations[element]
            class_sums.append(class_sum)

        central_commute = all(
            class_sum * representations[generator]
            == representations[generator] * class_sum
            for class_sum in class_sums
            for generator in generators
        )
        all_central_operators_commute &= central_commute

        # Deterministic generic central elements usually separate the sectors early;
        # all class sums follow and certify/refine the common primary decomposition.
        generic_one = sum(
            ((index + 1) * class_sum for index, class_sum in enumerate(class_sums)),
            sp.zeros(kernel_dimension),
        )
        # A second generic element with squared class coefficients was used in v2.
        # It is mathematically redundant because every class sum is processed below,
        # and on the largest 64-dimensional module it caused pathological exact
        # characteristic-polynomial factorisation.  One small generic separator
        # followed by all exact class sums gives the same common primary
        # decomposition with substantially smaller coefficients.
        central_operators = [generic_one] + class_sums

        print(
            f"[channel {channel_number}/{len(channel_source_rows)}] A={subset} "
            f"phase=central_decomposition group={len(group)} classes={len(classes)}",
            flush=True,
        )
        decomposition_started = time.perf_counter()
        sectors = central_isotypic_decomposition(
            kernel_dimension,
            central_operators,
            progress_label=(
                f"[channel {channel_number}/{len(channel_source_rows)}] A={subset}"
            ),
        )
        # central_isotypic_decomposition begins from the identity module and
        # certifies every split as an exact direct sum.  Dimension conservation
        # is therefore the exact final reconstruction certificate.
        decomposition_direct = sum(sector.cols for sector in sectors) == kernel_dimension
        all_decompositions_direct &= decomposition_direct

        print(
            f"[channel {channel_number}/{len(channel_source_rows)}] A={subset} "
            f"phase=post_decomposition_start sectors={len(sectors)}",
            flush=True,
        )
        orbit_cells = permutation_orbits(
            chamber_size,
            [state_images[element] for element in group_elements],
        )
        group_hash = literal_group_hash(group)
        group_order_histogram = Counter(
            xbr04f.permutation_order(element) for element in group_elements
        )
        group_order_signature = ";".join(
            f"o{order}:n{count}"
            for order, count in sorted(group_order_histogram.items())
        )

        channel_absolute_count = 0
        channel_full_support_count = 0
        channel_orbit_local_count = 0
        channel_sector_dimensions: List[int] = []

        element_class_index: Dict[Permutation, int] = {}
        for class_index, cell in enumerate(classes):
            for element in cell:
                element_class_index[element] = class_index

        kernel_matrix = sympy_matrix(kernel_rows)

        for sector_index, sector_basis in enumerate(sectors):
            sector_started = time.perf_counter()
            sector_dimension = sector_basis.cols
            channel_sector_dimensions.append(sector_dimension)
            progress_prefix = (
                f"[channel {channel_number}/{len(channel_source_rows)}] "
                f"A={subset} sector={sector_index + 1}/{len(sectors)} "
                f"dim={sector_dimension}"
            )
            print(f"{progress_prefix} phase=diagnostics_start", flush=True)

            workspace_started = time.perf_counter()
            workspace = restriction_workspace(sector_basis)
            print(
                f"{progress_prefix} phase=workspace_done "
                f"elapsed={time.perf_counter() - workspace_started:.2f}s",
                flush=True,
            )

            # Exact invariance is certified by constructing and verifying the
            # restricted action.  This replaces repeated augmented-matrix ranks.
            invariant_started = time.perf_counter()
            for generator in generators:
                restriction_matrix_cached(
                    representations[generator], sector_basis, workspace
                )
            sector_invariant = True
            all_sectors_invariant &= sector_invariant
            print(
                f"{progress_prefix} phase=invariance_done "
                f"generators={len(generators)} "
                f"elapsed={time.perf_counter() - invariant_started:.2f}s",
                flush=True,
            )

            # Record exact class-sum primary factors.  These are at most
            # sector_dimension x sector_dimension and reuse the same workspace.
            central_started = time.perf_counter()
            central_factor_signature_parts: List[str] = []
            central_pure = True
            for class_index, class_sum in enumerate(class_sums):
                restricted = restriction_matrix_cached(
                    class_sum, sector_basis, workspace
                )
                factors = charpoly_factor_payload(restricted)
                central_pure &= len(factors) == 1
                central_factor_signature_parts.append(
                    f"c{class_index}:" + ",".join(
                        f"{factor}^{exponent}" for factor, exponent in factors
                    )
                )
            all_sectors_central_pure &= central_pure
            print(
                f"{progress_prefix} phase=central_signature_done "
                f"classes={len(class_sums)} pure={central_pure} "
                f"elapsed={time.perf_counter() - central_started:.2f}s",
                flush=True,
            )

            character_started = time.perf_counter()
            (
                class_restrictions,
                class_traces,
                class_fixed_dimensions,
                class_anti_fixed_dimensions,
            ) = sector_class_character_data(
                sector_basis,
                classes,
                representations,
                xbr04f,
                workspace,
            )
            norm = character_norm_from_classes(
                classes, class_traces, len(group_elements)
            )
            norm_integral = bool(norm.q == 1)
            all_character_norms_integral &= norm_integral
            absolutely_irreducible = norm == 1
            channel_absolute_count += int(absolutely_irreducible)

            character_vector = [
                fraction_text(class_traces[element_class_index[element]])
                for element in group_elements
            ]
            order_trace_signature = order_trace_histogram_from_classes(
                classes, class_traces, xbr04f
            )
            fixed_dimension_signature = fixed_dimension_histogram_from_classes(
                classes, class_fixed_dimensions, xbr04f
            )
            anti_values = [
                value for value in class_anti_fixed_dimensions
                if value is not None
            ]
            maximum_anti_fixed = max(anti_values, default=0)

            exact_type_hash = stable_json_hash({
                "literal_group_hash": group_hash,
                "character": character_vector,
            })
            coarse_type_hash = stable_json_hash({
                "group_order": len(group),
                "group_element_order_signature": group_order_signature,
                "sector_dimension": sector_dimension,
                "order_trace_histogram": order_trace_signature,
                "character_norm": fraction_text(norm),
            })
            print(
                f"{progress_prefix} phase=character_done "
                f"norm={fraction_text(norm)} "
                f"elapsed={time.perf_counter() - character_started:.2f}s",
                flush=True,
            )

            coordinate_started = time.perf_counter()
            chamber_sector_matrix = sector_basis.T * kernel_matrix
            sector_integer_rows = independent_integer_rows(chamber_sector_matrix)
            # Independence follows exactly from the injective composition
            # sector_basis.T -> kernel_basis; the cached workspace has already
            # certified that sector_basis has full column rank.
            sector_rank_exact = len(sector_integer_rows) == sector_dimension
            sector_vectors_exact = (
                sector_rank_exact
                and all(vector_annihilated(neighbors, row) for row in sector_integer_rows)
            )
            all_sector_vectors_in_kernel &= sector_vectors_exact
            print(
                f"{progress_prefix} phase=coordinate_basis_done "
                f"rows={len(sector_integer_rows)} "
                f"elapsed={time.perf_counter() - coordinate_started:.2f}s",
                flush=True,
            )

            support_started = time.perf_counter()
            orbit_rows, support_summary = support_orbit_rows(
                subset,
                regime,
                sector_index,
                sector_integer_rows,
                orbit_cells,
            )
            support_rows.extend(orbit_rows)
            all_support_orbit_unions_exact &= bool(
                support_summary["support_is_union_of_automorphism_orbits"]
            )
            channel_full_support_count += int(
                support_summary["full_coordinate_support"]
            )
            channel_orbit_local_count += int(
                support_summary["has_nonzero_single_orbit_supported_vector"]
            )
            print(
                f"{progress_prefix} phase=support_orbit_done "
                f"orbits={len(orbit_cells)} "
                f"elapsed={time.perf_counter() - support_started:.2f}s",
                flush=True,
            )

            if args.write_sector_bases == "sparse":
                write_sparse_integer_matrix(
                    channel_out_root
                    / subset_slug(subset)
                    / f"sector_{sector_index:02d}.basis.coordinate.json.gz",
                    sector_integer_rows,
                )

            sector_row = {
                "subset": subset_key,
                "regime": regime,
                "sector_index": sector_index,
                "sector_dimension": sector_dimension,
                "central_isotypic": True,
                "central_primary_pure": central_pure,
                "character_norm": fraction_text(norm),
                "endomorphism_dimension_over_C": fraction_text(norm),
                "character_norm_integral": norm_integral,
                "absolutely_irreducible_certified": absolutely_irreducible,
                "literal_group_hash": group_hash,
                "exact_module_type_hash": exact_type_hash,
                "coarse_module_type_hash": coarse_type_hash,
                "group_order": len(group),
                "group_element_order_signature": group_order_signature,
                "order_trace_histogram": order_trace_signature,
                "fixed_dimension_histogram": fixed_dimension_signature,
                "maximum_involution_anti_fixed_dimension": maximum_anti_fixed,
                "has_full_sign_involution": maximum_anti_fixed == sector_dimension,
                "central_factor_signature": "|".join(
                    central_factor_signature_parts
                ),
                "sector_basis_dimension_exact": sector_vectors_exact,
                "sector_basis_sha256": sha256_integer_rows(sector_integer_rows),
                **support_summary,
            }
            sector_rows.append(sector_row)

            for class_index, cell in enumerate(classes):
                representative = cell[0]
                restricted = class_restrictions[class_index]
                class_rows.append({
                    "subset": subset_key,
                    "regime": regime,
                    "sector_index": sector_index,
                    "class_index": class_index,
                    "class_size": len(cell),
                    "representative": xbr04f.permutation_cycle_text(representative),
                    "representative_order": xbr04f.permutation_order(representative),
                    "representative_cycle_type": permutation_cycle_type(representative),
                    "character_trace": fraction_text(class_traces[class_index]),
                    "fixed_space_dimension": class_fixed_dimensions[class_index],
                    "anti_fixed_space_dimension": (
                        class_anti_fixed_dimensions[class_index]
                        if class_anti_fixed_dimensions[class_index] is not None
                        else ""
                    ),
                })

            print(
                f"{progress_prefix} phase=diagnostics_done "
                f"elapsed={time.perf_counter() - sector_started:.2f}s",
                flush=True,
            )

        print(
            f"[channel {channel_number}/{len(channel_source_rows)}] A={subset} "
            f"phase=post_decomposition_done elapsed="
            f"{time.perf_counter() - decomposition_started:.2f}s",
            flush=True,
        )

        channel_row = {
            "subset": subset_key,
            "regime": regime,
            "source_chamber_size": chamber_size,
            "kernel_dimension": kernel_dimension,
            "kernel_basis_hash_matches_xbr04f6": basis_hash_match,
            "label_automorphism_group_order": len(group),
            "label_automorphism_group_matches_xbr04f6": group_order_match,
            "kernel_representation_image_order": representation_image_order,
            "representation_image_matches_xbr04f6": image_order_match,
            "literal_group_hash": group_hash,
            "group_element_order_signature": group_order_signature,
            "conjugacy_class_count": len(classes),
            "representation_homomorphism_exact": homomorphism_exact,
            "class_traces_constant": traces_constant,
            "class_sums_central_exact": central_commute,
            "central_isotypic_sector_count": len(sectors),
            "central_isotypic_dimensions": ";".join(map(str, channel_sector_dimensions)),
            "central_decomposition_direct_exact": decomposition_direct,
            "absolutely_irreducible_sector_count": channel_absolute_count,
            "nonabsolute_central_sector_count": len(sectors) - channel_absolute_count,
            "full_coordinate_support_sector_count": channel_full_support_count,
            "single_orbit_local_sector_count": channel_orbit_local_count,
            "automorphism_orbit_count": len(orbit_cells),
            "elapsed_seconds": time.perf_counter() - channel_started,
        }
        channel_rows.append(channel_row)

        # Durable checkpoints: a later expensive channel cannot erase completed
        # exact work.  These ledgers are overwritten atomically at channel
        # boundaries and become the final ledgers when all channels finish.
        write_csv(out_dir / "kernel_module_channel_ledger.csv", channel_rows)
        write_csv(out_dir / "kernel_module_sector_ledger.csv", sector_rows)
        write_csv(out_dir / "kernel_module_class_character_ledger.csv", class_rows)
        write_csv(out_dir / "kernel_module_support_orbit_ledger.csv", support_rows)

        write_json(
            channel_out_root / subset_slug(subset) / "certificate.json",
            {
                "probe": PROBE_NAME,
                "script_version": SCRIPT_VERSION,
                "utc_completed": utc_now(),
                "channel_row": channel_row,
                "sector_rows": [
                    row for row in sector_rows if row["subset"] == subset_key
                ],
            },
        )

        print(
            f"[channel {channel_number}/{len(channel_source_rows)}] A={subset} "
            f"sectors={len(sectors)} dims={channel_row['central_isotypic_dimensions']} "
            f"absolute={channel_absolute_count} full_support={channel_full_support_count} "
            f"orbit_local={channel_orbit_local_count} "
            f"elapsed={time.perf_counter() - channel_started:.2f}s",
            flush=True,
        )

    # Exact recurrences require the same literal label group and the same full
    # character.  Coarse recurrences are candidates only and never promoted to
    # exact module equivalences.
    exact_groups: MutableMapping[str, List[Mapping[str, object]]] = defaultdict(list)
    coarse_groups: MutableMapping[str, List[Mapping[str, object]]] = defaultdict(list)
    for row in sector_rows:
        exact_groups[str(row["exact_module_type_hash"])].append(row)
        coarse_groups[str(row["coarse_module_type_hash"])].append(row)

    recurrence_rows: List[dict] = []
    for type_hash, members in sorted(exact_groups.items()):
        if len(members) < 2:
            continue
        recurrence_rows.append({
            "recurrence_kind": "exact_same_literal_group_character",
            "type_hash": type_hash,
            "member_count": len(members),
            "channel_count": len({row["subset"] for row in members}),
            "group_order": members[0]["group_order"],
            "sector_dimension": members[0]["sector_dimension"],
            "character_norm": members[0]["character_norm"],
            "members": ";".join(
                f"{row['subset']}#s{row['sector_index']}" for row in members
            ),
            "interpretation": "exact_QG_module_equivalence_for_identical_literal_group",
        })
    for type_hash, members in sorted(coarse_groups.items()):
        if len(members) < 2:
            continue
        exact_hashes = {row["exact_module_type_hash"] for row in members}
        if len(exact_hashes) == 1:
            continue
        recurrence_rows.append({
            "recurrence_kind": "coarse_cross_group_candidate",
            "type_hash": type_hash,
            "member_count": len(members),
            "channel_count": len({row["subset"] for row in members}),
            "group_order": members[0]["group_order"],
            "sector_dimension": members[0]["sector_dimension"],
            "character_norm": members[0]["character_norm"],
            "members": ";".join(
                f"{row['subset']}#s{row['sector_index']}" for row in members
            ),
            "interpretation": "candidate_only_not_a_certified_cross_group_isomorphism",
        })

    write_csv(out_dir / "kernel_module_channel_ledger.csv", channel_rows)
    write_csv(out_dir / "kernel_module_sector_ledger.csv", sector_rows)
    write_csv(out_dir / "kernel_module_class_character_ledger.csv", class_rows)
    write_csv(out_dir / "kernel_module_support_orbit_ledger.csv", support_rows)
    write_csv(out_dir / "kernel_module_recurrence_ledger.csv", recurrence_rows)

    checks = {
        "xbr04f6_strict_pass": bool(f6_summary.get("strict_pass")),
        "eleven_singular_channels_loaded": len(channel_rows) == 11,
        "all_kernel_basis_hashes_match": all_basis_hashes_match,
        "all_group_orders_match_xbr04f6": all_group_orders_match,
        "all_representation_images_match_xbr04f6": all_representation_images_match,
        "all_representation_homomorphisms_exact": all_homomorphisms_exact,
        "all_class_traces_constant": all_class_traces_constant,
        "all_class_sums_central_exact": all_central_operators_commute,
        "all_central_decompositions_direct": all_decompositions_direct,
        "all_central_sectors_invariant": all_sectors_invariant,
        "all_central_sectors_primary_pure": all_sectors_central_pure,
        "all_character_norms_integral": all_character_norms_integral,
        "all_sector_supports_are_orbit_unions": all_support_orbit_unions_exact,
        "all_sector_basis_vectors_remain_in_chamber_kernel": all_sector_vectors_in_kernel,
        "sector_dimensions_sum_to_216": sum(int(row["sector_dimension"]) for row in sector_rows) == 216,
    }
    strict_pass = all(checks.values())
    verdict = VERDICT_PASS if strict_pass else "EHF_XBR_04F7_AUDIT_FAIL"

    absolute_count = sum(
        truthy(row["absolutely_irreducible_certified"]) for row in sector_rows
    )
    nonabsolute_count = len(sector_rows) - absolute_count
    exact_recurrence_count = sum(
        row["recurrence_kind"] == "exact_same_literal_group_character"
        for row in recurrence_rows
    )
    coarse_recurrence_count = sum(
        row["recurrence_kind"] == "coarse_cross_group_candidate"
        for row in recurrence_rows
    )
    module_status = (
        "absolute_irreducible_decomposition_complete"
        if nonabsolute_count == 0
        else "rational_central_isotypic_decomposition_complete_nonabsolute_sectors_remain"
    )
    support_status = (
        "orbit_local_submodules_detected"
        if any(truthy(row["has_nonzero_single_orbit_supported_vector"]) for row in sector_rows)
        else "all_sectors_orbit_delocalised"
    )
    recurrence_status = (
        "exact_recurring_module_types_found"
        if exact_recurrence_count
        else "no_exact_recurring_module_types_for_identical_literal_groups"
    )

    elapsed = time.perf_counter() - started
    summary = {
        "probe": PROBE_NAME,
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "source_xbr04f6_dir": str(f6_dir),
        "counts": {
            "channels": len(channel_rows),
            "central_isotypic_sectors": len(sector_rows),
            "sector_dimension_total": sum(int(row["sector_dimension"]) for row in sector_rows),
            "absolutely_irreducible_sectors": absolute_count,
            "nonabsolute_central_sectors": nonabsolute_count,
            "class_character_rows": len(class_rows),
            "support_orbit_rows": len(support_rows),
            "exact_recurring_module_type_groups": exact_recurrence_count,
            "coarse_candidate_type_groups": coarse_recurrence_count,
        },
        "module_decomposition_status": module_status,
        "support_orbit_status": support_status,
        "module_recurrence_status": recurrence_status,
        "checks": checks,
        "strict_pass": strict_pass,
        "verdict": verdict,
        "elapsed_seconds": elapsed,
    }
    write_json(out_dir / "run_summary.json", summary)
    (out_dir / "module_report.md").write_text(
        markdown_report(channel_rows, sector_rows, recurrence_rows, checks, verdict)
    )

    print()
    print("[rational kernel-module decomposition]")
    print(
        f"  channels={len(channel_rows)} sectors={len(sector_rows)} "
        f"dimension_total={sum(int(row['sector_dimension']) for row in sector_rows)}"
    )
    print(
        f"  absolutely_irreducible={absolute_count} "
        f"nonabsolute_central={nonabsolute_count} status={module_status}"
    )
    print("[support-orbit audit]")
    print(
        f"  full_support={sum(truthy(row['full_coordinate_support']) for row in sector_rows)} "
        f"orbit_local={sum(truthy(row['has_nonzero_single_orbit_supported_vector']) for row in sector_rows)} "
        f"status={support_status}"
    )
    print("[recurring module types]")
    print(
        f"  exact={exact_recurrence_count} coarse_candidates={coarse_recurrence_count} "
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
