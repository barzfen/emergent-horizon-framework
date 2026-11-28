#!/usr/bin/env python3
"""
EHF-XBR-04C
============
Exact Restricted-Action Certificate

XBR-04 identified the minimal OPW3 adjacency-invariant Krylov closure generated
by each canonical deletion-adjoint AMP image. XBR-04B certified every reported
closure dimension and first stabilization depth over QQ.

For each channel A with nonzero lifted image, this probe reconstructs the exact
integer block-Krylov matrix through the certified stabilization depth d_A,
extracts a deterministic exact row basis V_A, and computes the unique restricted
action matrix R_A satisfying the row-vector convention

    V_A * Adj_A = R_A * V_A.

It also computes exact seed coordinates C_A satisfying

    G_A = C_A * V_A,

where G_A is the primitive-integer lifted AMP image. Thus the certificate gives
an explicit witness that

    im(G_A) is contained in rowspace(V_A),
    rowspace(V_A) is Adj_A-invariant,
    dim_Q rowspace(V_A) is the XBR-04B-certified closure dimension.

Because OPW adjacency is symmetric, an optional additional exact check verifies
self-adjointness in the induced Gram form:

    R_A H_A = H_A R_A^T,   H_A = V_A V_A^T.

The recommended backend is python-flint. A SymPy backend is included for small
smoke tests, but it may be impractical for the largest channels.
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
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Set, Tuple

import sympy as sp

SCRIPT_VERSION = "ehf_xbr_04c_2026-07-26"

Subset = Tuple[int, int, int]
IntegerRows = List[List[int]]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_subset(text: str) -> Subset:
    values = tuple(int(value.strip()) for value in text.split(","))
    if len(values) != 3:
        raise ValueError(f"invalid subset: {text}")
    return values  # type: ignore[return-value]


def parse_subset_selection(text: str) -> Set[Subset] | None:
    if text.strip().lower() == "all":
        return None
    selected: Set[Subset] = set()
    for item in text.split(";"):
        item = item.strip()
        if item:
            selected.add(parse_subset(item))
    if not selected:
        raise argparse.ArgumentTypeError(
            "expected 'all' or semicolon-separated triples"
        )
    return selected


def subset_text(subset: Subset) -> str:
    return ",".join(map(str, subset))


def subset_slug(subset: Subset) -> str:
    return "A_" + "_".join(map(str, subset))


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


def write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def truthy(value: object) -> bool:
    return str(value).strip().lower() == "true"


def connected_components(adjacency: Sequence[Set[int]]) -> List[List[int]]:
    seen: Set[int] = set()
    components: List[List[int]] = []

    for start in range(len(adjacency)):
        if start in seen:
            continue

        stack = [start]
        seen.add(start)
        component: List[int] = []

        while stack:
            state = stack.pop()
            component.append(state)
            for target in adjacency[state]:
                if target not in seen:
                    seen.add(target)
                    stack.append(target)

        component.sort()
        components.append(component)

    components.sort(key=lambda component: (-len(component), component[0]))
    return components


def local_neighbors(
    global_adjacency: Sequence[Set[int]],
    global_states: Sequence[int],
) -> List[List[int]]:
    local_index = {
        global_state: local_state
        for local_state, global_state in enumerate(global_states)
    }

    neighbors: List[List[int]] = [[] for _ in global_states]
    for global_state in global_states:
        source = local_index[global_state]
        neighbors[source] = sorted(
            local_index[target]
            for target in global_adjacency[global_state]
            if target in local_index
        )
    return neighbors


def adjacency_is_symmetric(neighbors: Sequence[Sequence[int]]) -> bool:
    neighbor_sets = [set(row) for row in neighbors]
    return all(
        source in neighbor_sets[target]
        for source, row in enumerate(neighbors)
        for target in row
    )


def multiply_rows_by_adjacency(
    rows: Sequence[Sequence[int]],
    neighbors: Sequence[Sequence[int]],
) -> IntegerRows:
    """Right-multiply row vectors by the unweighted local adjacency matrix."""
    return [
        [
            sum(row[source] for source in neighbors[target])
            for target in range(len(neighbors))
        ]
        for row in rows
    ]


def build_krylov_rows(
    generators: IntegerRows,
    neighbors: Sequence[Sequence[int]],
    max_depth: int,
) -> tuple[IntegerRows, List[dict], List[int]]:
    """
    Return rows [G, GA, ..., GA^max_depth], provenance, and cumulative counts.
    """
    all_rows: IntegerRows = []
    provenance: List[dict] = []
    cumulative_counts: List[int] = []
    current = [list(row) for row in generators]

    for depth in range(max_depth + 1):
        for generator_index, row in enumerate(current):
            all_rows.append(row)
            provenance.append({
                "krylov_row_index": len(all_rows) - 1,
                "depth": depth,
                "generator_index": generator_index,
            })
        cumulative_counts.append(len(all_rows))
        current = multiply_rows_by_adjacency(current, neighbors)

    return all_rows, provenance, cumulative_counts


def maximum_entry_bits(rows: Sequence[Sequence[int]]) -> int:
    return max(
        (abs(int(value)).bit_length() for row in rows for value in row),
        default=0,
    )


def sha256_integer_rows(rows: Sequence[Sequence[int]]) -> str:
    digest = hashlib.sha256()
    digest.update(f"ZZ:{len(rows)}:{len(rows[0]) if rows else 0}\n".encode())
    for row in rows:
        digest.update((",".join(str(int(value)) for value in row) + "\n").encode())
    return digest.hexdigest()


def write_integer_matrix_coordinate_gzip(
    path: Path,
    rows: Sequence[Sequence[int]],
) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    nrows = len(rows)
    ncols = len(rows[0]) if rows else 0
    nonzero = 0

    with gzip.open(path, "wt", encoding="utf-8") as handle:
        handle.write(
            json.dumps({
                "format": "coordinate",
                "domain": "ZZ",
                "nrows": nrows,
                "ncols": ncols,
            })[:-1]
        )
        handle.write(',"entries":[')
        first = True
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                value = int(value)
                if value == 0:
                    continue
                if not first:
                    handle.write(",")
                handle.write(json.dumps([i, j, str(value)]))
                first = False
                nonzero += 1
        handle.write("]}")

    return {
        "path": path.name,
        "format": "coordinate",
        "domain": "ZZ",
        "nrows": nrows,
        "ncols": ncols,
        "nonzero_entries": nonzero,
        "sha256_dense_rows": sha256_integer_rows(rows),
    }


def pivot_columns_from_dense_rref(
    nrows: int,
    ncols: int,
    entry,
    expected_rank: int,
) -> List[int]:
    pivots: List[int] = []
    for i in range(nrows):
        pivot = None
        for j in range(ncols):
            if entry(i, j) != 0:
                pivot = j
                break
        if pivot is not None:
            pivots.append(pivot)
    if len(pivots) != expected_rank:
        raise RuntimeError(
            f"RREF pivot extraction failed: got {len(pivots)}, "
            f"expected {expected_rank}"
        )
    return pivots


@dataclass
class RationalStats:
    nrows: int
    ncols: int
    nonzero_entries: int
    common_denominator: str
    maximum_numerator_bits: int
    maximum_denominator_bits: int
    sha256: str


class ExactBackend:
    name: str
    description: str

    def rank(self, rows: IntegerRows) -> int:
        raise NotImplementedError

    def independent_row_indices(self, rows: IntegerRows) -> List[int]:
        raise NotImplementedError

    def pivot_columns(self, rows: IntegerRows) -> List[int]:
        raise NotImplementedError

    def coordinates(
        self,
        basis_rows: IntegerRows,
        target_rows: IntegerRows,
        pivot_columns: Sequence[int],
    ):
        raise NotImplementedError

    def verify_coordinates(
        self,
        coordinates,
        basis_rows: IntegerRows,
        target_rows: IntegerRows,
    ) -> bool:
        raise NotImplementedError

    def gram_self_adjoint(self, restricted_action, basis_rows: IntegerRows) -> bool:
        raise NotImplementedError

    def rational_stats(self, matrix) -> RationalStats:
        raise NotImplementedError

    def write_rational_matrix_coordinate_gzip(self, path: Path, matrix) -> dict:
        raise NotImplementedError

    def determinant_of_integer_square(self, rows: IntegerRows) -> int:
        raise NotImplementedError


class FlintBackend(ExactBackend):
    name = "flint"
    description = "python-flint exact ZZ/QQ dense linear algebra"

    def __init__(self) -> None:
        try:
            from flint import fmpq_mat, fmpz_mat
        except ImportError as exc:
            raise RuntimeError(
                "python-flint is required for the flint backend. Install with "
                "python3 -m pip install python-flint"
            ) from exc
        self.fmpz_mat = fmpz_mat
        self.fmpq_mat = fmpq_mat

    def zmat(self, rows: IntegerRows):
        if not rows:
            return self.fmpz_mat(0, 0)
        return self.fmpz_mat([
            [int(value) for value in row]
            for row in rows
        ])

    def qmat(self, rows: IntegerRows):
        if not rows:
            return self.fmpq_mat(0, 0)
        return self.fmpq_mat([
            [int(value) for value in row]
            for row in rows
        ])

    def rank(self, rows: IntegerRows) -> int:
        if not rows:
            return 0
        return int(self.zmat(rows).rank())

    def independent_row_indices(self, rows: IntegerRows) -> List[int]:
        if not rows:
            return []
        matrix_t = self.zmat(rows).transpose()
        rref_num, _, rank = matrix_t.rref()
        return pivot_columns_from_dense_rref(
            int(rref_num.nrows()),
            int(rref_num.ncols()),
            lambda i, j: rref_num[i, j],
            int(rank),
        )

    def pivot_columns(self, rows: IntegerRows) -> List[int]:
        if not rows:
            return []
        matrix = self.zmat(rows)
        rref_num, _, rank = matrix.rref()
        return pivot_columns_from_dense_rref(
            int(rref_num.nrows()),
            int(rref_num.ncols()),
            lambda i, j: rref_num[i, j],
            int(rank),
        )

    def coordinates(
        self,
        basis_rows: IntegerRows,
        target_rows: IntegerRows,
        pivot_columns: Sequence[int],
    ):
        dimension = len(basis_rows)
        if len(pivot_columns) != dimension:
            raise ValueError("pivot column count must equal basis dimension")

        square = self.fmpz_mat([
            [int(row[column]) for column in pivot_columns]
            for row in basis_rows
        ])
        target_minor = self.fmpz_mat([
            [int(row[column]) for column in pivot_columns]
            for row in target_rows
        ])

        # X * square = target_minor  <=>  square^T * X^T = target_minor^T.
        return square.transpose().solve(target_minor.transpose()).transpose()

    def verify_coordinates(
        self,
        coordinates,
        basis_rows: IntegerRows,
        target_rows: IntegerRows,
    ) -> bool:
        basis_q = self.qmat(basis_rows)
        target_q = self.qmat(target_rows)
        return bool(coordinates * basis_q == target_q)

    def gram_self_adjoint(self, restricted_action, basis_rows: IntegerRows) -> bool:
        basis_z = self.zmat(basis_rows)
        gram_z = basis_z * basis_z.transpose()
        gram_q = self.fmpq_mat([
            [int(value) for value in row]
            for row in gram_z.tolist()
        ])
        return bool(
            restricted_action * gram_q
            == gram_q * restricted_action.transpose()
        )

    def rational_stats(self, matrix) -> RationalStats:
        nrows = int(matrix.nrows())
        ncols = int(matrix.ncols())
        common_num, common_den = matrix.numer_denom()
        nonzero = 0
        max_num_bits = 0
        max_den_bits = 0
        digest = hashlib.sha256()
        digest.update(f"QQ:{nrows}:{ncols}\n".encode())

        for i in range(nrows):
            for j in range(ncols):
                value = matrix[i, j]
                numerator = int(value.numer())
                denominator = int(value.denom())
                if numerator != 0:
                    nonzero += 1
                max_num_bits = max(max_num_bits, abs(numerator).bit_length())
                max_den_bits = max(max_den_bits, denominator.bit_length())
                digest.update(f"{numerator}/{denominator},".encode())
            digest.update(b"\n")

        return RationalStats(
            nrows=nrows,
            ncols=ncols,
            nonzero_entries=nonzero,
            common_denominator=str(int(common_den)),
            maximum_numerator_bits=max_num_bits,
            maximum_denominator_bits=max_den_bits,
            sha256=digest.hexdigest(),
        )

    def write_rational_matrix_coordinate_gzip(self, path: Path, matrix) -> dict:
        path.parent.mkdir(parents=True, exist_ok=True)
        stats = self.rational_stats(matrix)

        with gzip.open(path, "wt", encoding="utf-8") as handle:
            handle.write(
                json.dumps({
                    "format": "coordinate",
                    "domain": "QQ",
                    "nrows": stats.nrows,
                    "ncols": stats.ncols,
                })[:-1]
            )
            handle.write(',"entries":[')
            first = True
            for i in range(stats.nrows):
                for j in range(stats.ncols):
                    value = matrix[i, j]
                    numerator = int(value.numer())
                    if numerator == 0:
                        continue
                    denominator = int(value.denom())
                    if not first:
                        handle.write(",")
                    handle.write(json.dumps([
                        i,
                        j,
                        str(numerator),
                        str(denominator),
                    ]))
                    first = False
            handle.write("]}")

        return {
            "path": path.name,
            "format": "coordinate",
            "domain": "QQ",
            **stats.__dict__,
        }

    def determinant_of_integer_square(self, rows: IntegerRows) -> int:
        if not rows:
            return 1
        return int(self.zmat(rows).det())


class SympyBackend(ExactBackend):
    name = "sympy"
    description = "SymPy exact QQ linear algebra; intended mainly for smoke tests"

    def rank(self, rows: IntegerRows) -> int:
        if not rows:
            return 0
        return int(sp.Matrix(rows).rank())

    def independent_row_indices(self, rows: IntegerRows) -> List[int]:
        if not rows:
            return []
        _, pivots = sp.Matrix(rows).T.rref()
        return [int(value) for value in pivots]

    def pivot_columns(self, rows: IntegerRows) -> List[int]:
        if not rows:
            return []
        _, pivots = sp.Matrix(rows).rref()
        return [int(value) for value in pivots]

    def coordinates(
        self,
        basis_rows: IntegerRows,
        target_rows: IntegerRows,
        pivot_columns: Sequence[int],
    ):
        square = sp.Matrix([
            [int(row[column]) for column in pivot_columns]
            for row in basis_rows
        ])
        target_minor = sp.Matrix([
            [int(row[column]) for column in pivot_columns]
            for row in target_rows
        ])
        return square.T.inv() * target_minor.T

    @staticmethod
    def row_coordinates(matrix):
        # SymPy solve above returns X^T; normalize to X.
        return matrix.T

    def verify_coordinates(
        self,
        coordinates,
        basis_rows: IntegerRows,
        target_rows: IntegerRows,
    ) -> bool:
        coordinates = self.row_coordinates(coordinates)
        return bool(coordinates * sp.Matrix(basis_rows) == sp.Matrix(target_rows))

    def gram_self_adjoint(self, restricted_action, basis_rows: IntegerRows) -> bool:
        restricted_action = self.row_coordinates(restricted_action)
        basis = sp.Matrix(basis_rows)
        gram = basis * basis.T
        return bool(restricted_action * gram == gram * restricted_action.T)

    def rational_stats(self, matrix) -> RationalStats:
        matrix = self.row_coordinates(matrix)
        nrows, ncols = matrix.shape
        common_denominator = 1
        nonzero = 0
        max_num_bits = 0
        max_den_bits = 0
        digest = hashlib.sha256()
        digest.update(f"QQ:{nrows}:{ncols}\n".encode())

        for i in range(nrows):
            for j in range(ncols):
                value = sp.Rational(matrix[i, j])
                numerator = int(value.p)
                denominator = int(value.q)
                if numerator != 0:
                    nonzero += 1
                common_denominator = math.lcm(common_denominator, denominator)
                max_num_bits = max(max_num_bits, abs(numerator).bit_length())
                max_den_bits = max(max_den_bits, denominator.bit_length())
                digest.update(f"{numerator}/{denominator},".encode())
            digest.update(b"\n")

        return RationalStats(
            nrows=int(nrows),
            ncols=int(ncols),
            nonzero_entries=nonzero,
            common_denominator=str(common_denominator),
            maximum_numerator_bits=max_num_bits,
            maximum_denominator_bits=max_den_bits,
            sha256=digest.hexdigest(),
        )

    def write_rational_matrix_coordinate_gzip(self, path: Path, matrix) -> dict:
        matrix = self.row_coordinates(matrix)
        path.parent.mkdir(parents=True, exist_ok=True)
        stats = self.rational_stats(matrix.T)  # row_coordinates restores matrix

        with gzip.open(path, "wt", encoding="utf-8") as handle:
            handle.write(
                json.dumps({
                    "format": "coordinate",
                    "domain": "QQ",
                    "nrows": stats.nrows,
                    "ncols": stats.ncols,
                })[:-1]
            )
            handle.write(',"entries":[')
            first = True
            for i in range(stats.nrows):
                for j in range(stats.ncols):
                    value = sp.Rational(matrix[i, j])
                    numerator = int(value.p)
                    if numerator == 0:
                        continue
                    denominator = int(value.q)
                    if not first:
                        handle.write(",")
                    handle.write(json.dumps([
                        i,
                        j,
                        str(numerator),
                        str(denominator),
                    ]))
                    first = False
            handle.write("]}")

        return {
            "path": path.name,
            "format": "coordinate",
            "domain": "QQ",
            **stats.__dict__,
        }

    def determinant_of_integer_square(self, rows: IntegerRows) -> int:
        if not rows:
            return 1
        return int(sp.Matrix(rows).det())


def choose_backend(requested: str) -> ExactBackend:
    if requested in {"auto", "flint"}:
        try:
            return FlintBackend()
        except RuntimeError:
            if requested == "flint":
                raise
    return SympyBackend()


def backend_matrix_for_output(backend: ExactBackend, matrix):
    """SymPy stores coordinate solves transposed internally; normalize here."""
    if isinstance(backend, SympyBackend):
        return backend.row_coordinates(matrix)
    return matrix


def channel_ledger_row_from_certificate(certificate: Mapping[str, Any]) -> dict:
    row = certificate.get("ledger_row")
    if not isinstance(row, dict):
        raise ValueError("certificate missing ledger_row")
    return dict(row)


def run_self_test() -> None:
    backend = SympyBackend()

    # Path graph P4, with two seed rows. The Krylov closure is all of QQ^4.
    neighbors = [[1], [0, 2], [1, 3], [2]]
    generators = [[1, 0, 0, 0], [0, 1, 0, 0]]
    rows, provenance, counts = build_krylov_rows(generators, neighbors, 2)
    basis_indices = backend.independent_row_indices(rows)
    basis = [rows[index] for index in basis_indices]
    assert backend.rank(basis) == 4
    pivots = backend.pivot_columns(basis)
    action_targets = multiply_rows_by_adjacency(basis, neighbors)
    action = backend.coordinates(basis, action_targets, pivots)
    assert backend.verify_coordinates(action, basis, action_targets)
    seed_coords = backend.coordinates(basis, generators, pivots)
    assert backend.verify_coordinates(seed_coords, basis, generators)
    assert backend.gram_self_adjoint(action, basis)
    assert len(provenance) == counts[-1]
    print("EHF-XBR-04C self-test PASS")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Construct exact Krylov bases and restricted OPW adjacency actions "
            "for the XBR-04B-certified closures."
        )
    )
    parser.add_argument("--xbr04b-dir", required=False)
    parser.add_argument("--opw-base-script", required=False)
    parser.add_argument("--amp-base-script", required=False)
    parser.add_argument("--amp-helper-script", required=False)
    parser.add_argument("--amp-rank-script", required=False)
    parser.add_argument("--amp-lattice-script", required=False)
    parser.add_argument("--xbr04-script", required=False)
    parser.add_argument(
        "--backend",
        choices=("auto", "flint", "sympy"),
        default="auto",
    )
    parser.add_argument(
        "--subsets",
        type=parse_subset_selection,
        default=None,
        help="'all' or semicolon-separated triples; default all",
    )
    parser.add_argument(
        "--write-matrices",
        choices=("none", "restricted", "full"),
        default="full",
        help=(
            "none: metadata only; restricted: R and seed coordinates; "
            "full: also write the exact basis V"
        ),
    )
    parser.add_argument(
        "--skip-gram-check",
        action="store_true",
        help="skip the derived exact Gram self-adjointness identity",
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--out-dir", default="runs/ehf_xbr_04c")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return 0

    required_arguments = [
        "xbr04b_dir",
        "opw_base_script",
        "amp_base_script",
        "amp_helper_script",
        "amp_rank_script",
        "amp_lattice_script",
        "xbr04_script",
    ]
    missing = [name for name in required_arguments if not getattr(args, name)]
    if missing:
        parser.error("missing required arguments: " + ", ".join(missing))

    started = time.perf_counter()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    channel_root = out_dir / "channels"
    channel_root.mkdir(parents=True, exist_ok=True)

    xbr04b_dir = Path(args.xbr04b_dir).resolve()
    xbr04b_summary_path = xbr04b_dir / "run_summary.json"
    xbr04b_ledger_path = xbr04b_dir / "rational_certificate_ledger.csv"
    if not xbr04b_summary_path.exists():
        raise FileNotFoundError(xbr04b_summary_path)
    if not xbr04b_ledger_path.exists():
        raise FileNotFoundError(xbr04b_ledger_path)

    with xbr04b_summary_path.open() as handle:
        xbr04b_summary = json.load(handle)
    source_rows = read_csv(xbr04b_ledger_path)
    source_by_subset = {
        parse_subset(row["subset"]): row
        for row in source_rows
    }

    selected_set: Set[Subset] | None = args.subsets
    selected_subsets = [
        subset
        for subset in sorted(source_by_subset)
        if selected_set is None or subset in selected_set
    ]
    if selected_set is not None:
        unknown = selected_set - set(source_by_subset)
        if unknown:
            raise ValueError(f"subsets absent from XBR-04B ledger: {sorted(unknown)}")

    backend = choose_backend(args.backend)
    gram_check_enabled = not args.skip_gram_check

    opw_path = Path(args.opw_base_script).resolve()
    amp_base_path = Path(args.amp_base_script).resolve()
    amp_helper_path = Path(args.amp_helper_script).resolve()
    amp_rank_path = Path(args.amp_rank_script).resolve()
    amp_lattice_path = Path(args.amp_lattice_script).resolve()
    xbr04_path = Path(args.xbr04_script).resolve()

    print("=" * 132)
    print("EHF-XBR-04C: EXACT RESTRICTED-ACTION CERTIFICATE")
    print("=" * 132)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"XBR-04B directory:    {xbr04b_dir}")
    print(f"exact backend:        {backend.name} ({backend.description})")
    print(f"selected channels:    {len(selected_subsets)}")
    print(f"write matrices:       {args.write_matrices}")
    print(f"Gram check:           {gram_check_enabled}")
    print(f"output directory:     {out_dir}")
    print(f"strict:               {args.strict}")
    print()

    source_checks = {
        "xbr04b_summary_strict_pass": bool(xbr04b_summary.get("strict_pass")),
        "xbr04b_all_35_rationally_certified": bool(
            xbr04b_summary.get("rational", {}).get("all_35_certified")
        ),
        "xbr04b_ledger_has_35_channels": len(source_by_subset) == 35,
        "all_source_rows_rationally_certified": all(
            truthy(row.get("rational_certificate"))
            for row in source_rows
        ),
    }

    opw = load_module(opw_path, "ehf_xbr_04c_opw")
    amp_base = load_module(amp_base_path, "ehf_xbr_04c_amp_base")
    amp_helper = load_module(amp_helper_path, "ehf_xbr_04c_amp_helper")
    amp_rank = load_module(amp_rank_path, "ehf_xbr_04c_amp_rank")
    amp_lattice = load_module(amp_lattice_path, "ehf_xbr_04c_amp_lattice")
    xbr04 = load_module(xbr04_path, "ehf_xbr_04c_xbr04")

    cycles9 = opw.generate_cycles(9)
    index9 = {cycle: state for state, cycle in enumerate(cycles9)}
    pi9 = [opw.pi_label(cycle) for cycle in cycles9]
    graph9 = opw.build_preserve_graph(
        cycles9,
        index9,
        pi9,
        "OPW3",
        opw.GRAPH_LENGTHS["OPW3"],
    )
    components9 = connected_components(graph9.adjacency)
    component_sets = {
        frozenset(component): component_id
        for component_id, component in enumerate(components9)
    }

    source_fibres = amp_base.fibres(9)
    target_fibres = amp_base.fibres(8)
    kk_permutations = list(itertools.permutations(range(2, 9)))
    kk_index = {
        permutation: index
        for index, permutation in enumerate(kk_permutations)
    }

    ledger_path = out_dir / "restricted_action_ledger.csv"
    ledger_rows: List[dict] = []
    completed: Dict[Subset, dict] = {}

    if args.resume:
        for subset in selected_subsets:
            certificate_path = channel_root / subset_slug(subset) / "certificate.json"
            if not certificate_path.exists():
                continue
            try:
                with certificate_path.open() as handle:
                    certificate = json.load(handle)
                if certificate.get("strict_pass"):
                    row = channel_ledger_row_from_certificate(certificate)
                    completed[subset] = row
                    ledger_rows.append(row)
            except (OSError, ValueError, json.JSONDecodeError):
                continue
        write_csv(ledger_path, ledger_rows)

    all_selected_pass = True

    for channel_number, subset in enumerate(selected_subsets, start=1):
        if subset in completed:
            row = completed[subset]
            channel_pass = truthy(row.get("channel_certificate_pass"))
            all_selected_pass &= channel_pass
            print(
                f"[channel {channel_number}/{len(selected_subsets)}] "
                f"A={subset} resumed pass={channel_pass}"
            )
            continue

        channel_started = time.perf_counter()
        source_row = source_by_subset[subset]
        target_dimension = int(source_row["rational_closure_dimension"])
        target_depth = int(source_row["rational_stabilization_depth"])
        source_certified = truthy(source_row.get("rational_certificate"))

        source_key = amp_rank.key_from_subset_9(subset)
        source_cycles_one = source_fibres[source_key]
        source_global_ids = [
            index9[tuple(label - 1 for label in cycle)]
            for cycle in source_cycles_one
        ]
        source_component_id = component_sets.get(frozenset(source_global_ids))
        source_chamber_exact = source_component_id is not None
        neighbors = local_neighbors(graph9.adjacency, source_global_ids)
        local_adjacency_symmetric = adjacency_is_symmetric(neighbors)

        _, stacked_matrix, _ = amp_rank.exact_kk_and_stacked_matrices(
            amp_base,
            amp_helper,
            subset,
            source_fibres,
            target_fibres,
            kk_index,
        )
        deletion = stacked_matrix[math.factorial(7):, :]

        relation_image, _ = amp_lattice.exact_channel_image(
            amp_base,
            amp_helper,
            amp_rank,
            subset,
            source_fibres,
            target_fibres,
            kk_index,
        )
        amp_dimension = int(relation_image.rows)
        lifted_image = relation_image * deletion
        generators_array = xbr04.primitive_integer_rows(lifted_image)
        generators: IntegerRows = [
            [int(value) for value in row]
            for row in generators_array.tolist()
        ]

        channel_dir = channel_root / subset_slug(subset)
        channel_dir.mkdir(parents=True, exist_ok=True)

        if amp_dimension == 0:
            checks = {
                "source_rational_certificate": source_certified,
                "source_chamber_exact": source_chamber_exact,
                "local_adjacency_symmetric": local_adjacency_symmetric,
                "amp_dimension_zero": amp_dimension == 0,
                "lifted_generator_count_zero": len(generators) == 0,
                "certified_closure_dimension_zero": target_dimension == 0,
                "certified_stabilization_depth_zero": target_depth == 0,
            }
            channel_pass = all(checks.values())
            elapsed_channel = time.perf_counter() - channel_started
            row = {
                "subset": subset_text(subset),
                "source_component_id": source_component_id,
                "source_chamber_size": len(source_global_ids),
                "amp_dimension": amp_dimension,
                "closure_dimension": target_dimension,
                "stabilization_depth": target_depth,
                "basis_dimension": 0,
                "basis_max_depth": 0,
                "basis_pivot_minor_determinant": 1,
                "restricted_action_nonzero": 0,
                "restricted_action_density": 0.0,
                "restricted_action_common_denominator": 1,
                "seed_coordinate_nonzero": 0,
                "gram_self_adjoint": True,
                "channel_certificate_pass": channel_pass,
                "elapsed_seconds": elapsed_channel,
            }
            certificate = {
                "probe": "EHF-XBR-04C",
                "script_version": SCRIPT_VERSION,
                "subset": list(subset),
                "zero_image_certificate": True,
                "row_vector_convention": "V * Adj = R * V; G = C * V",
                "checks": checks,
                "strict_pass": channel_pass,
                "ledger_row": row,
                "elapsed_seconds": elapsed_channel,
            }
            write_json(channel_dir / "certificate.json", certificate)
            ledger_rows.append(row)
            completed[subset] = row
            write_csv(ledger_path, ledger_rows)
            all_selected_pass &= channel_pass

            print(
                f"[channel {channel_number}/{len(selected_subsets)}] "
                f"A={subset} zero-image certificate pass={channel_pass}"
            )
            continue

        print(
            f"[channel {channel_number}/{len(selected_subsets)}] "
            f"A={subset} chamber={len(source_global_ids)} amp={amp_dimension} "
            f"closure={target_dimension}@{target_depth}"
        )

        all_rows, provenance, cumulative_counts = build_krylov_rows(
            generators,
            neighbors,
            target_depth + 1,
        )
        rows_d = all_rows[:cumulative_counts[target_depth]]
        rows_next = all_rows[:cumulative_counts[target_depth + 1]]

        basis_indices = backend.independent_row_indices(rows_d)
        basis_rows = [rows_d[index] for index in basis_indices]
        basis_provenance = []
        for basis_index, krylov_row_index in enumerate(basis_indices):
            record = dict(provenance[krylov_row_index])
            record["basis_index"] = basis_index
            basis_provenance.append(record)

        basis_dimension = len(basis_rows)
        basis_rank = backend.rank(basis_rows)
        rank_rows_next = backend.rank(rows_next)
        basis_max_depth = max(
            (int(record["depth"]) for record in basis_provenance),
            default=0,
        )

        pivot_columns = backend.pivot_columns(basis_rows)
        pivot_minor_rows = [
            [row[column] for column in pivot_columns]
            for row in basis_rows
        ]
        pivot_minor_determinant = backend.determinant_of_integer_square(
            pivot_minor_rows
        )

        action_targets = multiply_rows_by_adjacency(basis_rows, neighbors)
        restricted_action_raw = backend.coordinates(
            basis_rows,
            action_targets,
            pivot_columns,
        )
        seed_coordinates_raw = backend.coordinates(
            basis_rows,
            generators,
            pivot_columns,
        )

        restricted_action_exact = backend.verify_coordinates(
            restricted_action_raw,
            basis_rows,
            action_targets,
        )
        seed_coordinates_exact = backend.verify_coordinates(
            seed_coordinates_raw,
            basis_rows,
            generators,
        )

        if gram_check_enabled:
            gram_self_adjoint = backend.gram_self_adjoint(
                restricted_action_raw,
                basis_rows,
            )
        else:
            gram_self_adjoint = None

        restricted_action = backend_matrix_for_output(
            backend,
            restricted_action_raw,
        )
        seed_coordinates = backend_matrix_for_output(
            backend,
            seed_coordinates_raw,
        )
        action_stats = backend.rational_stats(restricted_action_raw)
        seed_stats = backend.rational_stats(seed_coordinates_raw)

        matrix_files: Dict[str, object] = {}
        if args.write_matrices == "full":
            matrix_files["basis"] = write_integer_matrix_coordinate_gzip(
                channel_dir / "basis_matrix.coordinate.json.gz",
                basis_rows,
            )
        if args.write_matrices in {"restricted", "full"}:
            matrix_files["restricted_action"] = (
                backend.write_rational_matrix_coordinate_gzip(
                    channel_dir / "restricted_action.coordinate.json.gz",
                    restricted_action_raw,
                )
            )
            matrix_files["seed_coordinates"] = (
                backend.write_rational_matrix_coordinate_gzip(
                    channel_dir / "seed_coordinates.coordinate.json.gz",
                    seed_coordinates_raw,
                )
            )

        write_csv(channel_dir / "basis_provenance.csv", basis_provenance)

        checks: Dict[str, bool] = {
            "source_rational_certificate": source_certified,
            "source_chamber_exact": source_chamber_exact,
            "local_adjacency_symmetric": local_adjacency_symmetric,
            "amp_dimension_matches_source": (
                amp_dimension == int(source_row["amp_dimension"])
            ),
            "basis_dimension_matches_certified_closure": (
                basis_dimension == target_dimension
            ),
            "basis_rank_matches_dimension": basis_rank == basis_dimension,
            "next_krylov_rank_matches_closure": (
                rank_rows_next == target_dimension
            ),
            "basis_reaches_certified_stabilization_depth": (
                basis_max_depth == target_depth
            ),
            "pivot_column_count_matches_dimension": (
                len(pivot_columns) == basis_dimension
            ),
            "pivot_minor_nonsingular": pivot_minor_determinant != 0,
            "seed_coordinates_exact": seed_coordinates_exact,
            "restricted_action_exact": restricted_action_exact,
        }
        if gram_check_enabled:
            checks["gram_self_adjoint_exact"] = bool(gram_self_adjoint)

        channel_pass = all(checks.values())
        all_selected_pass &= channel_pass
        elapsed_channel = time.perf_counter() - channel_started

        restricted_density = (
            action_stats.nonzero_entries
            / (action_stats.nrows * action_stats.ncols)
            if action_stats.nrows and action_stats.ncols
            else 0.0
        )

        row = {
            "subset": subset_text(subset),
            "source_component_id": source_component_id,
            "source_chamber_size": len(source_global_ids),
            "amp_dimension": amp_dimension,
            "closure_dimension": target_dimension,
            "stabilization_depth": target_depth,
            "krylov_rows_through_d": len(rows_d),
            "krylov_rows_through_d_plus_1": len(rows_next),
            "krylov_maximum_entry_bits": maximum_entry_bits(rows_next),
            "basis_dimension": basis_dimension,
            "basis_max_depth": basis_max_depth,
            "basis_maximum_entry_bits": maximum_entry_bits(basis_rows),
            "basis_sha256": sha256_integer_rows(basis_rows),
            "basis_pivot_minor_determinant": str(pivot_minor_determinant),
            "basis_pivot_minor_determinant_bits": abs(
                pivot_minor_determinant
            ).bit_length(),
            "restricted_action_nonzero": action_stats.nonzero_entries,
            "restricted_action_density": restricted_density,
            "restricted_action_common_denominator": (
                action_stats.common_denominator
            ),
            "restricted_action_max_numerator_bits": (
                action_stats.maximum_numerator_bits
            ),
            "restricted_action_max_denominator_bits": (
                action_stats.maximum_denominator_bits
            ),
            "restricted_action_sha256": action_stats.sha256,
            "seed_coordinate_nonzero": seed_stats.nonzero_entries,
            "seed_coordinate_common_denominator": (
                seed_stats.common_denominator
            ),
            "seed_coordinate_sha256": seed_stats.sha256,
            "gram_self_adjoint": (
                gram_self_adjoint if gram_check_enabled else "skipped"
            ),
            "channel_certificate_pass": channel_pass,
            "backend": backend.name,
            "elapsed_seconds": elapsed_channel,
        }

        certificate = {
            "probe": "EHF-XBR-04C",
            "title": "Exact Restricted-Action Certificate",
            "script_version": SCRIPT_VERSION,
            "utc_completed": utc_now(),
            "subset": list(subset),
            "row_vector_convention": "V * Adj = R * V; G = C * V",
            "source": {
                "xbr04b_directory": str(xbr04b_dir),
                "source_component_id": source_component_id,
                "source_chamber_size": len(source_global_ids),
                "amp_dimension": amp_dimension,
                "certified_closure_dimension": target_dimension,
                "certified_stabilization_depth": target_depth,
            },
            "basis": {
                "dimension": basis_dimension,
                "selected_krylov_row_indices": basis_indices,
                "pivot_columns": pivot_columns,
                "maximum_depth": basis_max_depth,
                "sha256_dense_rows": sha256_integer_rows(basis_rows),
                "pivot_minor_determinant": str(pivot_minor_determinant),
            },
            "restricted_action": action_stats.__dict__,
            "seed_coordinates": seed_stats.__dict__,
            "matrix_files": matrix_files,
            "checks": checks,
            "strict_pass": channel_pass,
            "ledger_row": row,
            "elapsed_seconds": elapsed_channel,
        }
        write_json(channel_dir / "certificate.json", certificate)

        ledger_rows.append(row)
        completed[subset] = row
        write_csv(ledger_path, ledger_rows)

        print(
            f"  basis={basis_dimension} rank(next)={rank_rows_next} "
            f"R_nnz={action_stats.nonzero_entries} "
            f"den={action_stats.common_denominator} "
            f"action={restricted_action_exact} seed={seed_coordinates_exact} "
            f"gram={gram_self_adjoint if gram_check_enabled else 'skipped'} "
            f"pass={channel_pass} elapsed={elapsed_channel:.2f}s"
        )

    selected_complete = set(completed) == set(selected_subsets)
    selected_count = len(selected_subsets)
    selected_nonzero_count = sum(
        int(source_by_subset[subset]["amp_dimension"]) > 0
        for subset in selected_subsets
    )
    selected_zero_count = selected_count - selected_nonzero_count
    full_selection = set(selected_subsets) == set(source_by_subset)
    full_35_pass = (
        full_selection
        and selected_complete
        and all_selected_pass
        and all(source_checks.values())
    )
    strict_pass = (
        selected_complete
        and all_selected_pass
        and all(source_checks.values())
    )

    checks = {
        **source_checks,
        "selected_channels_complete": selected_complete,
        "all_selected_channel_certificates_pass": all_selected_pass,
    }
    if full_selection:
        checks["all_35_channel_certificates_pass"] = full_35_pass

    if full_35_pass:
        verdict = "EHF_XBR_04C_EXACT_RESTRICTED_ACTION_CERTIFICATE_PASS"
    elif strict_pass:
        verdict = "EHF_XBR_04C_SELECTED_CHANNEL_CERTIFICATES_PASS"
    else:
        verdict = "EHF_XBR_04C_CERTIFICATE_FAIL"

    elapsed = time.perf_counter() - started
    serializable_arguments = dict(vars(args))
    serializable_arguments["subsets"] = (
        "all"
        if selected_set is None
        else [list(subset) for subset in sorted(selected_set)]
    )

    summary = {
        "probe": "EHF-XBR-04C",
        "title": "Exact Restricted-Action Certificate",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": serializable_arguments,
        "backend": {
            "name": backend.name,
            "description": backend.description,
        },
        "counts": {
            "source_channels": len(source_by_subset),
            "selected_channels": selected_count,
            "selected_nonzero_channels": selected_nonzero_count,
            "selected_zero_channels": selected_zero_count,
            "completed_channels": len(completed),
        },
        "checks": checks,
        "strict_pass": strict_pass,
        "full_35_pass": full_35_pass,
        "exact_statement": (
            "For every certified nonzero channel, the emitted basis V has the "
            "XBR-04B-certified rational closure dimension, contains the lifted "
            "AMP image via G=C V, and carries the exact restricted OPW action "
            "V Adj=R V. Zero-image channels receive exact trivial certificates."
        ),
        "elapsed_seconds": elapsed,
        "verdict": verdict,
    }
    write_json(out_dir / "run_summary.json", summary)

    print()
    print("[exact restricted-action certification]")
    print(
        f"  selected={selected_count} completed={len(completed)} "
        f"nonzero={selected_nonzero_count} zero={selected_zero_count}"
    )
    print(f"  all selected pass={strict_pass}")
    print(f"  all 35 pass={full_35_pass}")
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
