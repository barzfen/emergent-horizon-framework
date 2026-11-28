#!/usr/bin/env python3
"""
EHF OPW normalized-Laplacian chamber spectra.

Graphs
------
OPW3_LR3_PI:
    Pi-preserving circular reversals of length 3.

OPW23_LR23_PI:
    Pi-preserving circular reversals of lengths 2 and 3
    (the enriched / legacy Odd Preserve World graph).

For each connected component ("chamber"), compute the complete spectrum of

    L_norm = I - D^(-1/2) A D^(-1/2).

For an isolated one-vertex chamber, the normalized Laplacian is defined as
the 1x1 zero matrix, so its spectrum is [0].

Outputs
-------
normalized_laplacian_eigenvalues.csv
    One row per eigenvalue.

normalized_laplacian_spectrum_grouped.csv
    Eigenvalues rounded to a configurable number of decimal places, with
    multiplicities.

chamber_summary.csv
    Chamber size, edges, degree statistics, lambda_1, lambda_max, checks.

run_summary.json
    Whole-run metadata and graph-level counts.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import os
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

# Keep small/medium eigendecompositions predictable on machines whose BLAS
# otherwise starts many threads.
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np
from scipy.sparse import csr_matrix, diags, eye
from scipy.sparse.csgraph import connected_components


GRAPH_SPECS = {
    "OPW3": ("OPW3_LR3_PI", (3,)),
    "OPW23": ("OPW23_LR23_PI", (2, 3)),
}

KNOWN_COUNTS = {
    ("OPW3_LR3_PI", 5): {"states": 12, "edges": 8, "chambers": 5},
    ("OPW3_LR3_PI", 7): {"states": 360, "edges": 600, "chambers": 19},
    ("OPW3_LR3_PI", 9): {"states": 20160, "edges": 53760, "chambers": 69},
    ("OPW23_LR23_PI", 5): {"states": 12, "edges": 8, "chambers": 5},
    ("OPW23_LR23_PI", 7): {"states": 360, "edges": 840, "chambers": 19},
    ("OPW23_LR23_PI", 9): {"states": 20160, "edges": 67200, "chambers": 69},
}


def parse_csv_ints(text: str) -> list[int]:
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values:
        raise argparse.ArgumentTypeError("At least one odd n value is required.")
    if any(n < 3 or n % 2 == 0 for n in values):
        raise argparse.ArgumentTypeError("All n values must be odd integers >= 3.")
    return values


def parse_graphs(text: str) -> list[str]:
    values = [x.strip().upper() for x in text.split(",") if x.strip()]
    invalid = [x for x in values if x not in GRAPH_SPECS]
    if invalid:
        raise argparse.ArgumentTypeError(
            f"Unknown graph(s): {invalid}. Use OPW3 and/or OPW23."
        )
    return values


def canonical_cycle(seq: Sequence[int]) -> tuple[int, ...]:
    """Canonicalize a Hamilton cycle modulo rotation and reflection."""
    seq = tuple(seq)

    i = seq.index(1)
    forward = seq[i:] + seq[:i]

    reversed_seq = tuple(reversed(seq))
    j = reversed_seq.index(1)
    backward = reversed_seq[j:] + reversed_seq[:j]

    return min(forward, backward)


def generate_cycles(n: int) -> list[tuple[int, ...]]:
    """Generate canonical Hamilton cycles on K_n, count (n-1)!/2."""
    cycles: list[tuple[int, ...]] = []
    for tail in itertools.permutations(range(2, n + 1)):
        forward = (1,) + tail
        backward = (1,) + tuple(reversed(tail))
        if forward <= backward:
            cycles.append(forward)
    return cycles


def pi_label(cycle: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Unordered pair of sorted even-slot and odd-slot label sets."""
    even = tuple(sorted(cycle[0::2]))
    odd = tuple(sorted(cycle[1::2]))
    return tuple(sorted((even, odd), key=lambda x: (len(x), x)))  # type: ignore[return-value]


def reverse_circular_segment(
    cycle: Sequence[int], start: int, length: int
) -> tuple[int, ...]:
    n = len(cycle)
    arr = list(cycle)
    indices = [(start + offset) % n for offset in range(length)]
    values = [arr[i] for i in indices]

    for i, value in zip(indices, reversed(values)):
        arr[i] = value

    return canonical_cycle(arr)


def build_opw_graph(
    n: int, lengths: Iterable[int]
) -> tuple[list[tuple[int, ...]], csr_matrix, np.ndarray, np.ndarray]:
    cycles = generate_cycles(n)
    expected = math.factorial(n - 1) // 2
    if len(cycles) != expected:
        raise RuntimeError(
            f"Canonical-cycle count failed for n={n}: {len(cycles)} != {expected}"
        )

    cycle_index = {cycle: i for i, cycle in enumerate(cycles)}
    rows: list[int] = []
    cols: list[int] = []

    for i, cycle in enumerate(cycles):
        label0 = pi_label(cycle)
        neighbors: set[int] = set()

        for length in lengths:
            for start in range(n):
                neighbor = reverse_circular_segment(cycle, start, length)
                if neighbor == cycle:
                    continue
                if pi_label(neighbor) != label0:
                    continue
                neighbors.add(cycle_index[neighbor])

        for j in neighbors:
            rows.append(i)
            cols.append(j)

    adjacency = csr_matrix(
        (np.ones(len(rows), dtype=np.float64), (rows, cols)),
        shape=(len(cycles), len(cycles)),
    )

    if (adjacency != adjacency.T).nnz:
        raise RuntimeError(f"Adjacency is not symmetric for n={n}, lengths={tuple(lengths)}")

    chamber_count, labels = connected_components(adjacency, directed=False)
    sizes = np.bincount(labels, minlength=chamber_count)
    return cycles, adjacency, labels, sizes


def normalized_laplacian_eigenvalues(adjacency: csr_matrix) -> np.ndarray:
    size = adjacency.shape[0]
    degree = np.asarray(adjacency.sum(axis=1)).ravel()

    if size == 1 and degree[0] == 0:
        return np.array([0.0], dtype=np.float64)

    inv_sqrt_degree = np.zeros(size, dtype=np.float64)
    positive = degree > 0
    inv_sqrt_degree[positive] = 1.0 / np.sqrt(degree[positive])

    # Chambers in this computation are connected. Non-singletons therefore
    # have no zero-degree vertices.
    if not np.all(positive):
        raise RuntimeError("Unexpected zero-degree vertex inside a nontrivial chamber.")

    normalized_adjacency = (
        inv_sqrt_degree[:, None]
        * adjacency.toarray()
        * inv_sqrt_degree[None, :]
    )
    laplacian = np.eye(size, dtype=np.float64) - normalized_adjacency
    eigenvalues = np.linalg.eigvalsh(laplacian)

    # Remove harmless floating-point noise at the theoretical endpoints.
    eigenvalues[np.abs(eigenvalues) < 1e-12] = 0.0
    eigenvalues[np.abs(eigenvalues - 2.0) < 1e-12] = 2.0
    return eigenvalues


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compute complete normalized-Laplacian spectra for OPW chambers."
    )
    parser.add_argument(
        "--n-values",
        type=parse_csv_ints,
        default=parse_csv_ints("5,7,9"),
        help="Comma-separated odd n values. Default: 5,7,9",
    )
    parser.add_argument(
        "--graphs",
        type=parse_graphs,
        default=parse_graphs("OPW3,OPW23"),
        help="Comma-separated graph names: OPW3,OPW23. Default: both",
    )
    parser.add_argument(
        "--round-digits",
        type=int,
        default=12,
        help="Decimal places used in the multiplicity-compressed output.",
    )
    parser.add_argument(
        "--max-states",
        type=int,
        default=250_000,
        help=(
            "Safety cap on the full HC_n state count. "
            "Full n=11 has 1,814,400 states and is intentionally blocked by default."
        ),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("runs/opw_normalized_laplacian_spectra"),
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    eigen_rows: list[dict] = []
    grouped_rows: list[dict] = []
    chamber_rows: list[dict] = []
    graph_run_rows: list[dict] = []

    for graph_key in args.graphs:
        graph_name, lengths = GRAPH_SPECS[graph_key]

        for n in args.n_values:
            expected_states = math.factorial(n - 1) // 2
            if expected_states > args.max_states:
                raise RuntimeError(
                    f"n={n} has {expected_states:,} HC states, above --max-states "
                    f"{args.max_states:,}. Increase the cap only if full enumeration is intended."
                )

            cycles, adjacency, labels, sizes = build_opw_graph(n, lengths)
            edge_count = adjacency.nnz // 2

            chambers = []
            for raw_label, size in enumerate(sizes):
                indices = np.flatnonzero(labels == raw_label)
                minimum_state = min(cycles[i] for i in indices)
                chambers.append((int(size), minimum_state, raw_label, indices))

            # Stable chamber numbering: descending size, then lexicographically
            # smallest state in the chamber.
            chambers.sort(key=lambda item: (-item[0], item[1]))

            known = KNOWN_COUNTS.get((graph_name, n))
            known_count_pass = (
                known is None
                or (
                    known["states"] == len(cycles)
                    and known["edges"] == edge_count
                    and known["chambers"] == len(chambers)
                )
            )

            if not known_count_pass:
                raise RuntimeError(
                    f"Known-count check failed for {graph_name}, n={n}: "
                    f"states={len(cycles)}, edges={edge_count}, chambers={len(chambers)}"
                )

            for chamber_rank, (size, minimum_state, raw_label, indices) in enumerate(chambers):
                subgraph = adjacency[indices][:, indices].tocsr()
                degree = np.asarray(subgraph.sum(axis=1)).ravel()
                eigenvalues = normalized_laplacian_eigenvalues(subgraph)

                zero_multiplicity = int(np.count_nonzero(np.abs(eigenvalues) < 1e-9))
                spectrum_count_pass = len(eigenvalues) == size
                zero_mode_pass = zero_multiplicity == 1
                bounds_pass = bool(
                    eigenvalues.min() >= -1e-9 and eigenvalues.max() <= 2.0 + 1e-9
                )

                expected_trace = 0.0 if size == 1 else float(size)
                trace_value = float(eigenvalues.sum())
                trace_pass = abs(trace_value - expected_trace) < 1e-8 * max(1, size)

                state_text = " ".join(map(str, minimum_state))
                chamber_id = f"{graph_name}_n{n}_c{chamber_rank:03d}"

                for eigen_index, value in enumerate(eigenvalues):
                    eigen_rows.append(
                        {
                            "graph": graph_name,
                            "n": n,
                            "chamber_id": chamber_id,
                            "chamber_rank": chamber_rank,
                            "raw_component_label": raw_label,
                            "chamber_size": size,
                            "minimum_state": state_text,
                            "eigen_index": eigen_index,
                            "eigenvalue": f"{float(value):.17g}",
                        }
                    )

                rounded_values = np.round(eigenvalues, args.round_digits)
                multiplicities = Counter(float(x) for x in rounded_values.tolist())
                for value, multiplicity in sorted(multiplicities.items()):
                    grouped_rows.append(
                        {
                            "graph": graph_name,
                            "n": n,
                            "chamber_id": chamber_id,
                            "chamber_rank": chamber_rank,
                            "chamber_size": size,
                            "minimum_state": state_text,
                            "eigenvalue_rounded": f"{value:.{args.round_digits}f}",
                            "multiplicity": multiplicity,
                        }
                    )

                lambda_1 = "" if size == 1 else f"{float(eigenvalues[1]):.17g}"
                chamber_rows.append(
                    {
                        "graph": graph_name,
                        "n": n,
                        "chamber_id": chamber_id,
                        "chamber_rank": chamber_rank,
                        "raw_component_label": raw_label,
                        "chamber_size": size,
                        "minimum_state": state_text,
                        "edges": int(subgraph.nnz // 2),
                        "degree_min": int(degree.min()),
                        "degree_max": int(degree.max()),
                        "degree_mean": f"{float(degree.mean()):.17g}",
                        "regular": bool(np.all(degree == degree[0])),
                        "lambda_0": f"{float(eigenvalues[0]):.17g}",
                        "lambda_1_spectral_gap": lambda_1,
                        "lambda_max": f"{float(eigenvalues[-1]):.17g}",
                        "distinct_eigenvalues_rounded": len(multiplicities),
                        "zero_multiplicity": zero_multiplicity,
                        "bipartite_from_lambda_max_2": bool(
                            abs(float(eigenvalues[-1]) - 2.0) < 1e-9
                        ),
                        "trace": f"{trace_value:.17g}",
                        "spectrum_count_pass": spectrum_count_pass,
                        "zero_mode_pass": zero_mode_pass,
                        "bounds_0_2_pass": bounds_pass,
                        "trace_pass": trace_pass,
                    }
                )

            graph_run_rows.append(
                {
                    "graph": graph_name,
                    "move_lengths": list(lengths),
                    "n": n,
                    "states": len(cycles),
                    "edges": int(edge_count),
                    "chambers": len(chambers),
                    "component_sizes_desc": [x[0] for x in chambers],
                    "known_count_check_available": known is not None,
                    "known_count_pass": known_count_pass,
                }
            )

            print(
                f"{graph_name:16s} n={n:2d} "
                f"states={len(cycles):7d} edges={edge_count:7d} "
                f"chambers={len(chambers):3d}"
            )

    write_csv(
        args.out_dir / "normalized_laplacian_eigenvalues.csv",
        [
            "graph",
            "n",
            "chamber_id",
            "chamber_rank",
            "raw_component_label",
            "chamber_size",
            "minimum_state",
            "eigen_index",
            "eigenvalue",
        ],
        eigen_rows,
    )
    write_csv(
        args.out_dir / "normalized_laplacian_spectrum_grouped.csv",
        [
            "graph",
            "n",
            "chamber_id",
            "chamber_rank",
            "chamber_size",
            "minimum_state",
            "eigenvalue_rounded",
            "multiplicity",
        ],
        grouped_rows,
    )
    write_csv(
        args.out_dir / "chamber_summary.csv",
        [
            "graph",
            "n",
            "chamber_id",
            "chamber_rank",
            "raw_component_label",
            "chamber_size",
            "minimum_state",
            "edges",
            "degree_min",
            "degree_max",
            "degree_mean",
            "regular",
            "lambda_0",
            "lambda_1_spectral_gap",
            "lambda_max",
            "distinct_eigenvalues_rounded",
            "zero_multiplicity",
            "bipartite_from_lambda_max_2",
            "trace",
            "spectrum_count_pass",
            "zero_mode_pass",
            "bounds_0_2_pass",
            "trace_pass",
        ],
        chamber_rows,
    )

    run_summary = {
        "definition": "L_norm = I - D^(-1/2) A D^(-1/2)",
        "isolated_vertex_convention": "A one-vertex isolated chamber has spectrum [0].",
        "n_values": args.n_values,
        "graphs": [GRAPH_SPECS[key][0] for key in args.graphs],
        "round_digits": args.round_digits,
        "graph_runs": graph_run_rows,
        "total_chambers": len(chamber_rows),
        "total_eigenvalues": len(eigen_rows),
        "all_chamber_checks_pass": all(
            row["spectrum_count_pass"]
            and row["zero_mode_pass"]
            and row["bounds_0_2_pass"]
            and row["trace_pass"]
            for row in chamber_rows
        ),
    }

    with (args.out_dir / "run_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(run_summary, handle, indent=2)

    print(f"\nWrote {len(chamber_rows)} chamber rows")
    print(f"Wrote {len(grouped_rows)} grouped spectrum rows")
    print(f"Wrote {len(eigen_rows)} eigenvalue rows")
    print(f"All chamber checks pass: {run_summary['all_chamber_checks_pass']}")
    print(f"Output: {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
