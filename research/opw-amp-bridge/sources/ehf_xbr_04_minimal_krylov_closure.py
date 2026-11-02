#!/usr/bin/env python3
"""
EHF-XBR-04
==========
Minimal Krylov Closure and Delayed Intertwiner

XBR-03 proved that the direct and one-step middle-block/deletion bridges vanish,
that every joint bridge activates after exactly two OPW3 adjacency steps, and
that the deletion-adjoint amplitude image W_A is not itself adjacency-invariant.

For each nonzero AMP channel A, define the minimal adjacency-invariant Krylov
closure

    K_A = span(W_A, W_A A_A, W_A A_A^2, ...).

This probe computes K_A exactly over one or more large finite fields. For each
prime p it determines:

    * the exact closure dimension over F_p;
    * the first stabilization depth d with K_d = K_{d+1};
    * whether the closure fills the complete OPW chamber;
    * the expansion beyond the original AMP image.

A run over one prime is an exact finite-field theorem. Agreement across several
primes is a strong rational-reconstruction diagnostic, but is not by itself a
proof of the corresponding dimensions over QQ. The script therefore labels its
main result as a finite-field theorem and a rational candidate law.

Once K_A stabilizes, right multiplication by OPW adjacency restricts exactly
to K_A. This gives the canonical delayed intertwiner on the minimal closure.
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
from collections import defaultdict
from datetime import datetime, timezone
from math import gcd
from pathlib import Path
from typing import Dict, List, Mapping, MutableMapping, Sequence, Set, Tuple

import numpy as np
import sympy as sp
from scipy import sparse

SCRIPT_VERSION = "ehf_xbr_04_2026-07-26"

Cycle = Tuple[int, ...]
Subset = Tuple[int, int, int]


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


def parse_int_csv(text: str) -> List[int]:
    values = [int(value.strip()) for value in text.split(",") if value.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
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


def local_adjacency(
    global_adjacency: Sequence[Set[int]],
    global_states: Sequence[int],
) -> sparse.csr_matrix:
    local_index = {
        global_state: local_state
        for local_state, global_state in enumerate(global_states)
    }

    rows: List[int] = []
    cols: List[int] = []

    for global_state in global_states:
        source = local_index[global_state]
        for target_global in global_adjacency[global_state]:
            target = local_index.get(target_global)
            if target is not None:
                rows.append(source)
                cols.append(target)

    return sparse.csr_matrix(
        (
            np.ones(len(rows), dtype=np.int64),
            (rows, cols),
        ),
        shape=(len(global_states), len(global_states)),
        dtype=np.int64,
    )


def primitive_integer_rows(matrix: sp.MatrixBase) -> np.ndarray:
    """
    Clear denominators row-by-row and divide by the row gcd.

    Row scaling by a nonzero rational does not change the QQ rowspace.
    Primitive integer representatives are suitable for reduction modulo primes.
    """
    rows: List[List[int]] = []

    for i in range(matrix.rows):
        numerators: List[int] = []
        denominators: List[int] = []

        for j in range(matrix.cols):
            numerator, denominator = matrix[i, j].as_numer_denom()
            numerators.append(int(numerator))
            denominators.append(int(denominator))

        common_denominator = 1
        for denominator in denominators:
            common_denominator = math.lcm(
                common_denominator,
                denominator,
            )

        row = [
            numerator * (common_denominator // denominator)
            for numerator, denominator in zip(numerators, denominators)
        ]

        row_gcd = 0
        for value in row:
            row_gcd = gcd(row_gcd, abs(value))

        if row_gcd > 1:
            row = [value // row_gcd for value in row]

        rows.append(row)

    return np.asarray(rows, dtype=np.int64)


def add_rows_to_modular_basis(
    rows: np.ndarray,
    basis: Dict[int, np.ndarray],
    prime: int,
) -> int:
    added = 0

    for row in rows:
        vector = np.remainder(row, prime).astype(np.int64, copy=True)

        while True:
            nonzero = np.flatnonzero(vector)
            if nonzero.size == 0:
                break

            pivot = int(nonzero[0])
            existing = basis.get(pivot)

            if existing is None:
                inverse = pow(int(vector[pivot]), -1, prime)
                vector = np.remainder(vector * inverse, prime)
                basis[pivot] = vector
                added += 1
                break

            coefficient = int(vector[pivot])
            vector = np.remainder(
                vector - coefficient * existing,
                prime,
            )

    return added


def modular_krylov_closure(
    adjacency: sparse.csr_matrix,
    generators_integer: np.ndarray,
    prime: int,
    max_depth: int,
) -> dict:
    """
    Compute the exact block-Krylov closure over F_p.

    K_d = span(W, WA, ..., WA^d).

    The first depth k at which rank(K_k) == rank(K_{k-1}) certifies that
    K_{k-1} is invariant, so stabilization_depth = k-1.
    """
    if generators_integer.shape[0] == 0:
        return {
            "prime": prime,
            "initial_rank": 0,
            "closure_dimension": 0,
            "stabilization_depth": 0,
            "rank_sequence": [0],
            "invariant": True,
        }

    current = np.remainder(
        generators_integer,
        prime,
    ).astype(np.int64, copy=False)

    basis: Dict[int, np.ndarray] = {}
    rank_sequence: List[int] = []

    for depth in range(max_depth + 2):
        add_rows_to_modular_basis(current, basis, prime)
        rank_sequence.append(len(basis))

        if depth > 0 and rank_sequence[-1] == rank_sequence[-2]:
            return {
                "prime": prime,
                "initial_rank": rank_sequence[0],
                "closure_dimension": rank_sequence[-1],
                "stabilization_depth": depth - 1,
                "rank_sequence": rank_sequence,
                "invariant": True,
            }

        # Values are reduced before each multiplication. OPW degree is at
        # most four here, so int64 remains far from overflow for these primes.
        current = np.remainder(
            current @ adjacency,
            prime,
        ).astype(np.int64, copy=False)

    raise RuntimeError(
        f"Krylov closure did not stabilize by depth {max_depth}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compute minimal AMP-generated OPW adjacency closures over "
            "one or more finite fields."
        )
    )
    parser.add_argument("--opw-base-script", required=True)
    parser.add_argument("--amp-base-script", required=True)
    parser.add_argument("--amp-helper-script", required=True)
    parser.add_argument("--amp-rank-script", required=True)
    parser.add_argument("--amp-lattice-script", required=True)
    parser.add_argument("--xbr03-run-dir", required=True)
    parser.add_argument(
        "--primes",
        type=parse_int_csv,
        default=[1000003],
    )
    parser.add_argument("--max-depth", type=int, default=600)
    parser.add_argument("--out-dir", default="runs/ehf_xbr_04")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    if len(set(args.primes)) != len(args.primes):
        raise ValueError("--primes must not contain duplicates")
    if any(prime < 3 for prime in args.primes):
        raise ValueError("all primes must be odd and at least 3")

    opw_path = Path(args.opw_base_script).resolve()
    amp_base_path = Path(args.amp_base_script).resolve()
    amp_helper_path = Path(args.amp_helper_script).resolve()
    amp_rank_path = Path(args.amp_rank_script).resolve()
    amp_lattice_path = Path(args.amp_lattice_script).resolve()
    xbr03_summary_path = (
        Path(args.xbr03_run_dir).resolve() / "run_summary.json"
    )
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for required in (
        opw_path,
        amp_base_path,
        amp_helper_path,
        amp_rank_path,
        amp_lattice_path,
        xbr03_summary_path,
    ):
        if not required.exists():
            raise FileNotFoundError(required)

    opw = load_module(opw_path, "ehf_xbr_04_opw")
    amp_base = load_module(amp_base_path, "ehf_xbr_04_amp_base")
    amp_helper = load_module(
        amp_helper_path,
        "ehf_xbr_04_amp_helper",
    )
    amp_rank = load_module(amp_rank_path, "ehf_xbr_04_amp_rank")
    amp_lattice = load_module(
        amp_lattice_path,
        "ehf_xbr_04_amp_lattice",
    )

    with xbr03_summary_path.open() as handle:
        xbr03_summary = json.load(handle)

    print("=" * 128)
    print("EHF-XBR-04: MINIMAL KRYLOV CLOSURE AND DELAYED INTERTWINER")
    print("=" * 128)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"OPW engine:           {opw_path}")
    print(f"AMP exact rank:       {amp_rank_path}")
    print(f"AMP lattice:          {amp_lattice_path}")
    print(f"XBR-03 certificate:   {xbr03_summary_path}")
    print(f"primes:               {args.primes}")
    print(f"maximum depth:        {args.max_depth}")
    print(f"output directory:     {out_dir}")
    print(f"strict:               {args.strict}")
    print()

    started = time.perf_counter()
    checks: Dict[str, bool] = {}
    channel_rows: List[dict] = []
    prime_rows: List[dict] = []

    xbr03_exact = (
        bool(xbr03_summary.get("strict_pass"))
        and xbr03_summary.get("verdict")
        == "EHF_XBR_03_TWO_STEP_MEDIATED_BRIDGE_INTERTWINING_OBSTRUCTION_PASS"
    )
    checks["xbr03_bridge_obstruction_certificate"] = xbr03_exact

    cycles9 = opw.generate_cycles(9)
    index9 = {
        cycle: state
        for state, cycle in enumerate(cycles9)
    }
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

    all_source_chambers_exact = True
    all_prime_runs_invariant = True
    all_nonzero_prime_agreement = True
    all_initial_ranks_match_amp = True

    nonzero_channels = 0
    zero_channels = 0
    full_closure_channels = 0
    proper_closure_channels = 0
    closure_dimensions: List[int] = []
    stabilization_depths: List[int] = []
    closure_fractions: List[float] = []

    for subset_values in itertools.combinations(range(2, 9), 3):
        subset: Subset = tuple(subset_values)  # type: ignore[assignment]

        source_key = amp_rank.key_from_subset_9(subset)
        source_cycles_one = source_fibres[source_key]
        source_global_ids = [
            index9[tuple(label - 1 for label in cycle)]
            for cycle in source_cycles_one
        ]

        source_component_id = component_sets.get(
            frozenset(source_global_ids)
        )
        source_chamber_exact = source_component_id is not None
        all_source_chambers_exact &= source_chamber_exact

        adjacency = local_adjacency(
            graph9.adjacency,
            source_global_ids,
        )

        _, stacked_matrix, _ = (
            amp_rank.exact_kk_and_stacked_matrices(
                amp_base,
                amp_helper,
                subset,
                source_fibres,
                target_fibres,
                kk_index,
            )
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

        if amp_dimension == 0:
            generators_integer = np.zeros(
                (0, len(source_global_ids)),
                dtype=np.int64,
            )
            zero_channels += 1
        else:
            lifted_image = relation_image * deletion
            generators_integer = primitive_integer_rows(lifted_image)
            nonzero_channels += 1

        prime_results: List[dict] = []
        for prime in args.primes:
            result = modular_krylov_closure(
                adjacency,
                generators_integer,
                prime,
                args.max_depth,
            )
            prime_results.append(result)
            all_prime_runs_invariant &= bool(result["invariant"])

            prime_rows.append({
                "subset": ",".join(map(str, subset)),
                "prime": prime,
                "source_chamber_size": len(source_global_ids),
                "amp_dimension": amp_dimension,
                "initial_rank_mod_p": result["initial_rank"],
                "closure_dimension_mod_p": result["closure_dimension"],
                "stabilization_depth_mod_p": result[
                    "stabilization_depth"
                ],
                "closure_fraction_mod_p": (
                    result["closure_dimension"]
                    / len(source_global_ids)
                    if source_global_ids else 0.0
                ),
                "rank_sequence": json.dumps(
                    result["rank_sequence"]
                ),
                "invariant": result["invariant"],
            })

        signatures = {
            (
                int(result["initial_rank"]),
                int(result["closure_dimension"]),
                int(result["stabilization_depth"]),
            )
            for result in prime_results
        }
        prime_agreement = len(signatures) == 1
        if amp_dimension > 0:
            all_nonzero_prime_agreement &= prime_agreement

        initial_rank, closure_dimension, stabilization_depth = (
            next(iter(signatures))
            if prime_agreement
            else (-1, -1, -1)
        )

        initial_rank_matches = (
            amp_dimension == 0
            or initial_rank == amp_dimension
        )
        all_initial_ranks_match_amp &= initial_rank_matches

        full_closure = (
            amp_dimension > 0
            and prime_agreement
            and closure_dimension == len(source_global_ids)
        )
        proper_closure = (
            amp_dimension > 0
            and prime_agreement
            and closure_dimension < len(source_global_ids)
        )

        full_closure_channels += int(full_closure)
        proper_closure_channels += int(proper_closure)

        if amp_dimension > 0 and prime_agreement:
            closure_dimensions.append(closure_dimension)
            stabilization_depths.append(stabilization_depth)
            closure_fractions.append(
                closure_dimension / len(source_global_ids)
            )

        channel_rows.append({
            "subset": ",".join(map(str, subset)),
            "rank_class": amp_rank.rank_class_name(subset),
            "source_component_id": source_component_id,
            "source_chamber_size": len(source_global_ids),
            "source_chamber_exact": source_chamber_exact,
            "amp_dimension": amp_dimension,
            "prime_agreement": prime_agreement,
            "initial_rank": initial_rank,
            "closure_dimension": closure_dimension,
            "stabilization_depth": stabilization_depth,
            "closure_fraction": (
                closure_dimension / len(source_global_ids)
                if closure_dimension >= 0
                else ""
            ),
            "expansion_dimension": (
                closure_dimension - amp_dimension
                if closure_dimension >= 0
                else ""
            ),
            "expansion_factor": (
                closure_dimension / amp_dimension
                if amp_dimension > 0 and closure_dimension >= 0
                else ""
            ),
            "full_chamber_closure": full_closure,
            "proper_invariant_closure": proper_closure,
            "delayed_intertwiner_exists_mod_all_primes": (
                amp_dimension > 0
                and prime_agreement
                and all(result["invariant"] for result in prime_results)
            ),
        })

    checks["all_35_source_fibres_are_opw_chambers"] = (
        all_source_chambers_exact
    )
    checks["channel_count_35"] = len(channel_rows) == 35
    checks["nonzero_amp_channel_count_31"] = nonzero_channels == 31
    checks["zero_amp_channel_count_4"] = zero_channels == 4
    checks["all_initial_modular_ranks_match_amp_dimension"] = (
        all_initial_ranks_match_amp
    )
    checks["all_prime_closures_stabilize_invariantly"] = (
        all_prime_runs_invariant
    )
    checks["all_31_nonzero_channels_consistent_across_requested_primes"] = (
        all_nonzero_prime_agreement
    )
    checks["full_plus_proper_equals_31"] = (
        full_closure_channels + proper_closure_channels == 31
    )

    # Class summary.
    class_groups: MutableMapping[str, List[dict]] = defaultdict(list)
    for row in channel_rows:
        class_groups[str(row["rank_class"])].append(row)

    class_rows: List[dict] = []
    for class_name, rows in sorted(class_groups.items()):
        nonzero_rows = [
            row for row in rows
            if int(row["amp_dimension"]) > 0
        ]
        class_rows.append({
            "rank_class": class_name,
            "channel_count": len(rows),
            "nonzero_channels": len(nonzero_rows),
            "full_closure_channels": sum(
                bool(row["full_chamber_closure"])
                for row in nonzero_rows
            ),
            "proper_closure_channels": sum(
                bool(row["proper_invariant_closure"])
                for row in nonzero_rows
            ),
            "closure_dimensions": json.dumps([
                int(row["closure_dimension"])
                for row in nonzero_rows
            ]),
            "stabilization_depths": json.dumps([
                int(row["stabilization_depth"])
                for row in nonzero_rows
            ]),
            "mean_closure_fraction": (
                sum(float(row["closure_fraction"]) for row in nonzero_rows)
                / len(nonzero_rows)
                if nonzero_rows else 0.0
            ),
        })

    write_csv(out_dir / "krylov_channel_ledger.csv", channel_rows)
    write_csv(out_dir / "krylov_prime_ledger.csv", prime_rows)
    write_csv(out_dir / "krylov_class_summary.csv", class_rows)

    checks = {key: bool(value) for key, value in checks.items()}
    strict_pass = all(checks.values())
    elapsed = time.perf_counter() - started

    mean_fraction = (
        sum(closure_fractions) / len(closure_fractions)
        if closure_fractions else 0.0
    )
    median_fraction = (
        float(np.median(np.asarray(closure_fractions)))
        if closure_fractions else 0.0
    )
    mean_depth = (
        sum(stabilization_depths) / len(stabilization_depths)
        if stabilization_depths else 0.0
    )
    max_depth_observed = (
        max(stabilization_depths)
        if stabilization_depths else 0
    )

    verdict = (
        "EHF_XBR_04_FINITE_FIELD_KRYLOV_CLOSURE_DELAYED_INTERTWINER_PASS"
        if strict_pass
        else "EHF_XBR_04_KRYLOV_CLOSURE_AUDIT_FAIL"
    )

    summary = {
        "probe": "EHF-XBR-04",
        "title": "Minimal Krylov Closure and Delayed Intertwiner",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "checks": checks,
        "strict_pass": strict_pass,
        "counts": {
            "channels": len(channel_rows),
            "nonzero_amp_channels": nonzero_channels,
            "zero_amp_channels": zero_channels,
            "full_chamber_closures": full_closure_channels,
            "proper_invariant_closures": proper_closure_channels,
        },
        "aggregate": {
            "mean_closure_fraction": mean_fraction,
            "median_closure_fraction": median_fraction,
            "minimum_closure_fraction": (
                min(closure_fractions)
                if closure_fractions else 0.0
            ),
            "maximum_closure_fraction": (
                max(closure_fractions)
                if closure_fractions else 0.0
            ),
            "mean_stabilization_depth": mean_depth,
            "maximum_stabilization_depth": max_depth_observed,
        },
        "finite_field_statement": (
            "For every nonzero channel and every audited prime, the minimal "
            "Krylov space generated by the deletion-adjoint AMP image "
            "stabilizes exactly and carries the restricted OPW adjacency "
            "operator. Agreement across all audited primes gives a common "
            "closure dimension and stabilization depth for every channel."
        ),
        "rational_status": (
            "The common multi-prime dimensions are strong candidates for the "
            "QQ Krylov dimensions, but multi-prime agreement alone is not an "
            "exact rational-rank proof."
        ),
        "delayed_intertwiner": (
            "On each stabilized finite-field closure K_A, OPW adjacency "
            "restricts exactly to K_A, giving the minimal delayed intertwiner "
            "containing the canonical AMP lift."
        ),
        "elapsed_seconds": elapsed,
        "verdict": verdict,
    }

    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print("[channel census]")
    print(
        f"  channels=35 nonzero-AMP={nonzero_channels} "
        f"zero-AMP={zero_channels}"
    )
    print(
        f"  requested-prime consistency="
        f"{sum(bool(row['prime_agreement']) for row in channel_rows)}/35"
    )
    print()
    print("[minimal invariant closures]")
    print(
        f"  full chamber={full_closure_channels}/{nonzero_channels} "
        f"proper closure={proper_closure_channels}/{nonzero_channels}"
    )
    print(
        f"  closure fraction mean={mean_fraction:.6f} "
        f"median={median_fraction:.6f}"
    )
    print(
        f"  stabilization depth mean={mean_depth:.3f} "
        f"max={max_depth_observed}"
    )
    print()
    print("[claim boundary]")
    print(
        "  finite-field closures are exact; common QQ dimensions remain "
        "modular candidates pending rational certification"
    )
    print()
    print("=" * 128)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {verdict}")
    print(f"elapsed:              {elapsed:.2f}s")
    print("=" * 128)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
