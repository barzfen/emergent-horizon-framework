#!/usr/bin/env python3
r"""
EHF-XBR-04F2: Invisible-Kernel Law Census


Tests, for every selected OPW3/AMP channel A, whether the exact XBR-04D
invisible complement satisfies


    K_A^perp subseteq ker(Adj_A).


For the reducing decomposition certified by XBR-04D, this is equivalent to
Adj_A restricted to K_A^perp being the zero matrix, to
im(Adj_A) subseteq K_A, and to equality of the chamber and visible ranks.


The theorem target is the set of nonzero proper XBR-04C sectors. Full-chamber
channels are vacuous passes. Zero-image channels are audited but excluded.
"""


from __future__ import annotations


import argparse
import csv
import importlib.util
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Set, Tuple


from flint import fmpq_mat, fmpz_mat


SCRIPT_VERSION = "ehf_xbr_04f2_2026-07-27"
Subset = Tuple[int, int, int]
IntegerRows = List[List[int]]
DEFAULT_DIRECT_PANEL = {(3, 6, 7), (4, 6, 7), (4, 6, 8)}




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
    if any(value not in range(2, 9) for value in values):
        raise ValueError(f"subset labels must lie in 2..8: {text}")
    return tuple(sorted(values))  # type: ignore[return-value]




def parse_selection(text: str) -> Set[Subset] | None:
    value = text.strip().lower()
    if value == "all":
        return None
    if value in {"", "none", "off"}:
        return set()
    result: Set[Subset] = set()
    for item in text.split(";"):
        item = item.strip()
        if item:
            result.add(parse_subset(item))
    return result




def subset_text(subset: Subset) -> str:
    return ",".join(map(str, subset))




def subset_slug(subset: Subset) -> str:
    return "A_" + "_".join(map(str, subset))




def truthy(value: object) -> bool:
    return str(value).strip().lower() == "true"




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




def adjacency_rows(neighbors: Sequence[Sequence[int]]) -> IntegerRows:
    size = len(neighbors)
    rows = [[0] * size for _ in range(size)]
    for source, targets in enumerate(neighbors):
        for target in targets:
            rows[source][target] = 1
    return rows




def adjacency_symmetric(neighbors: Sequence[Sequence[int]]) -> bool:
    target_sets = [set(targets) for targets in neighbors]
    return all(
        source in target_sets[target]
        for source, targets in enumerate(neighbors)
        for target in targets
    )




def exact_integer_rank(rows: IntegerRows) -> int:
    if not rows:
        return 0
    return int(fmpz_mat(rows).rank())




def exact_rational_rank(matrix: fmpq_mat) -> int:
    if int(matrix.nrows()) == 0 or int(matrix.ncols()) == 0:
        return 0
    numerator, _ = matrix.numer_denom()
    return int(numerator.rank())




def exact_zero_matrix(matrix: fmpq_mat) -> bool:
    return all(
        matrix[i, j] == 0
        for i in range(int(matrix.nrows()))
        for j in range(int(matrix.ncols()))
    )




def exact_action(
    basis_rows: IntegerRows,
    neighbors: Sequence[Sequence[int]],
    backend,
    xbr04d,
) -> tuple[fmpq_mat, bool]:
    dimension = len(basis_rows)
    if dimension == 0:
        return fmpq_mat(0, 0), True
    targets = xbr04d.multiply_rows_by_adjacency(basis_rows, neighbors)
    pivots = backend.pivot_columns(basis_rows)
    action = backend.coordinates(basis_rows, targets, pivots)
    exact = backend.verify_coordinates(action, basis_rows, targets)
    return action, bool(exact)




def self_test() -> None:
    full = fmpz_mat([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 0],
    ])
    visible = fmpq_mat([
        [0, 1],
        [1, 0],
    ])
    invisible = fmpq_mat([[0]])
    assert int(full.rank()) == 2
    assert exact_rational_rank(visible) == 2
    assert exact_rational_rank(invisible) == 0
    assert exact_zero_matrix(invisible)
    assert int(full.rank()) == (
        exact_rational_rank(visible) + exact_rational_rank(invisible)
    )
    failing = fmpq_mat([[1]])
    assert exact_rational_rank(failing) == 1
    assert not exact_zero_matrix(failing)
    print("EHF-XBR-04F2 self-test PASS")




def main() -> int:
    parser = argparse.ArgumentParser(
        description="Exact OPW3 invisible-kernel law census."
    )
    parser.add_argument("--xbr04c-dir")
    parser.add_argument("--xbr04d-dir")
    parser.add_argument("--xbr04c-script")
    parser.add_argument("--xbr04d-script")
    parser.add_argument("--opw-base-script")
    parser.add_argument("--amp-base-script")
    parser.add_argument("--amp-rank-script")
    parser.add_argument(
        "--subsets",
        type=parse_selection,
        default=None,
        help="'all' or semicolon-separated triples; default all",
    )
    parser.add_argument(
        "--direct-image-subsets",
        type=parse_selection,
        default=DEFAULT_DIRECT_PANEL,
        help=(
            "'none', 'all', or semicolon-separated triples for direct "
            "rank([V_A; Adj_A]) containment checks"
        ),
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--out-dir", default="runs/ehf_xbr_04f2")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()


    if args.self_test:
        self_test()
        return 0


    required_names = (
        "xbr04c_dir",
        "xbr04d_dir",
        "xbr04c_script",
        "xbr04d_script",
        "opw_base_script",
        "amp_base_script",
        "amp_rank_script",
    )
    missing = [name for name in required_names if not getattr(args, name)]
    if missing:
        parser.error("missing required arguments: " + ", ".join(missing))


    started = time.perf_counter()
    xbr04c_dir = Path(args.xbr04c_dir).resolve()
    xbr04d_dir = Path(args.xbr04d_dir).resolve()
    xbr04c_script_path = Path(args.xbr04c_script).resolve()
    xbr04d_script_path = Path(args.xbr04d_script).resolve()
    opw_path = Path(args.opw_base_script).resolve()
    amp_base_path = Path(args.amp_base_script).resolve()
    amp_rank_path = Path(args.amp_rank_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    channel_root = out_dir / "channels"
    channel_root.mkdir(parents=True, exist_ok=True)


    required_paths = (
        xbr04c_dir / "run_summary.json",
        xbr04d_dir / "run_summary.json",
        xbr04d_dir / "complement_ledger.csv",
        xbr04c_script_path,
        xbr04d_script_path,
        opw_path,
        amp_base_path,
        amp_rank_path,
    )
    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(path)


    xbr04c_summary = read_json(xbr04c_dir / "run_summary.json")
    xbr04d_summary = read_json(xbr04d_dir / "run_summary.json")
    source_rows = read_csv(xbr04d_dir / "complement_ledger.csv")
    source_by_subset = {
        parse_subset(row["subset"]): row for row in source_rows
    }


    selected_filter: Set[Subset] | None = args.subsets
    selected = [
        subset
        for subset in sorted(source_by_subset)
        if selected_filter is None or subset in selected_filter
    ]
    direct_filter: Set[Subset] | None = args.direct_image_subsets
    direct_selected = (
        set(selected) if direct_filter is None else set(direct_filter)
    )
    unknown = (set(selected) | direct_selected) - set(source_by_subset)
    if unknown:
        raise ValueError(f"unknown channel subsets: {sorted(unknown)}")


    print("=" * 132)
    print("EHF-XBR-04F2: INVISIBLE-KERNEL LAW CENSUS")
    print("=" * 132)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"XBR-04C directory:    {xbr04c_dir}")
    print(f"XBR-04D directory:    {xbr04d_dir}")
    print(f"selected channels:    {len(selected)}")
    print(f"direct image checks:  {len(direct_selected)}")
    print(f"output directory:     {out_dir}")
    print(f"strict:               {args.strict}")
    print()


    xbr04c = load_module(xbr04c_script_path, "ehf_xbr_04f2_xbr04c")
    xbr04d = load_module(xbr04d_script_path, "ehf_xbr_04f2_xbr04d")
    opw = load_module(opw_path, "ehf_xbr_04f2_opw")
    amp_base = load_module(amp_base_path, "ehf_xbr_04f2_amp_base")
    amp_rank = load_module(amp_rank_path, "ehf_xbr_04f2_amp_rank")
    backend = xbr04c.choose_backend("flint")


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


    ledger_path = out_dir / "kernel_law_ledger.csv"
    ledger: List[dict] = []
    completed: Dict[Subset, dict] = {}


    if args.resume:
        for subset in selected:
            path = channel_root / subset_slug(subset) / "certificate.json"
            if not path.exists():
                continue
            try:
                certificate = read_json(path)
                if (
                    certificate.get("script_version") == SCRIPT_VERSION
                    and certificate.get("strict_pass")
                ):
                    row = dict(certificate["ledger_row"])
                    ledger.append(row)
                    completed[subset] = row
            except (OSError, ValueError, KeyError, json.JSONDecodeError):
                continue
        write_csv(ledger_path, ledger)


    all_channels_pass = True
    all_targets_pass = True
    target_count = 0
    target_passes = 0
    full_vacuous = 0
    zero_excluded = 0
    direct_completed = 0
    direct_passes = 0
    counterexamples: List[str] = []


    for number, subset in enumerate(selected, start=1):
        if subset in completed:
            row = completed[subset]
            all_channels_pass &= truthy(row["channel_certificate_pass"])
            if truthy(row["kernel_law_applicable"]):
                target_count += 1
                passed = truthy(row["kernel_law_pass"])
                target_passes += int(passed)
                all_targets_pass &= passed
                if not passed:
                    counterexamples.append(subset_text(subset))
            elif row["law_status"] == "vacuous_full_chamber":
                full_vacuous += 1
            elif row["law_status"] == "excluded_zero_image":
                zero_excluded += 1
            if truthy(row["direct_image_check_requested"]):
                direct_completed += 1
                direct_passes += int(
                    truthy(row["direct_image_check_pass"])
                )
            print(
                f"[channel {number}/{len(selected)}] A={subset} resumed"
            )
            continue


        channel_started = time.perf_counter()
        source_row = source_by_subset[subset]
        channel_class = source_row["channel_class"]
        chamber_size = int(source_row["source_chamber_size"])
        closure_dimension = int(source_row["closure_dimension"])
        complement_dimension = int(source_row["complement_dimension"])


        source_dir = xbr04c_dir / "channels" / subset_slug(subset)
        complement_dir = xbr04d_dir / "channels" / subset_slug(subset)
        source_certificate = read_json(source_dir / "certificate.json")
        complement_certificate = read_json(
            complement_dir / "certificate.json"
        )


        source_key = amp_rank.key_from_subset_9(subset)
        source_cycles = source_fibres[source_key]
        global_ids = [
            index9[tuple(label - 1 for label in cycle)]
            for cycle in source_cycles
        ]
        neighbors = xbr04d.local_neighbors(graph9.adjacency, global_ids)
        chamber_matrix_rows = adjacency_rows(neighbors)
        chamber_rank = exact_integer_rank(chamber_matrix_rows)
        chamber_nullity = chamber_size - chamber_rank


        if closure_dimension == 0:
            source_basis: IntegerRows = []
        else:
            source_basis = xbr04d.read_integer_coordinate_gzip(
                source_dir / "basis_matrix.coordinate.json.gz"
            )
        source_basis_rank = xbr04d.exact_rank(source_basis, "flint")
        source_hash = xbr04d.sha256_integer_rows(source_basis)
        certified_source_hash = (
            source_certificate.get("basis", {}).get("sha256_dense_rows")
            if closure_dimension else source_hash
        )


        complement_basis = xbr04d.integer_right_nullspace(
            source_basis,
            chamber_size,
            "flint",
        )
        complement_basis_rank = xbr04d.exact_rank(
            complement_basis,
            "flint",
        )
        complement_hash = xbr04d.sha256_integer_rows(complement_basis)
        certified_complement_hash = complement_certificate.get(
            "decomposition", {}
        ).get("basis_sha256")


        visible_action, visible_action_exact = exact_action(
            source_basis,
            neighbors,
            backend,
            xbr04d,
        )
        invisible_action, invisible_action_exact = exact_action(
            complement_basis,
            neighbors,
            backend,
            xbr04d,
        )


        visible_rank = exact_rational_rank(visible_action)
        invisible_rank = exact_rational_rank(invisible_action)
        visible_nullity = closure_dimension - visible_rank
        invisible_nullity = complement_dimension - invisible_rank
        invisible_zero = exact_zero_matrix(invisible_action)


        rank_sum_exact = chamber_rank == visible_rank + invisible_rank
        nullity_sum_exact = (
            chamber_nullity == visible_nullity + invisible_nullity
        )
        rank_equivalence_exact = (
            (invisible_rank == 0) == (chamber_rank == visible_rank)
        )


        applicable = channel_class == "proper_sector_nonzero_complement"
        if applicable:
            target_count += 1
            law_pass = (
                invisible_zero
                and invisible_rank == 0
                and invisible_nullity == complement_dimension
                and chamber_rank == visible_rank
            )
            law_status = "target_pass" if law_pass else "target_fail"
            target_passes += int(law_pass)
            all_targets_pass &= law_pass
            if not law_pass:
                counterexamples.append(subset_text(subset))
        elif channel_class == "full_chamber_zero_complement":
            law_pass = True
            law_status = "vacuous_full_chamber"
            full_vacuous += 1
        elif channel_class == "zero_image_whole_complement":
            law_pass = False
            law_status = "excluded_zero_image"
            zero_excluded += 1
        else:
            raise ValueError(f"unknown channel class: {channel_class}")


        direct_requested = subset in direct_selected
        direct_contains = None
        direct_pass = None
        if direct_requested:
            direct_completed += 1
            stacked_rank = xbr04d.exact_rank(
                source_basis + chamber_matrix_rows,
                "flint",
            )
            direct_contains = stacked_rank == closure_dimension
            direct_pass = direct_contains == (invisible_rank == 0)
            direct_passes += int(bool(direct_pass))


        checks: Dict[str, bool] = {
            "source_xbr04c_certificate_pass": bool(
                source_certificate.get("strict_pass")
            ),
            "source_xbr04d_certificate_pass": bool(
                complement_certificate.get("strict_pass")
            ),
            "source_fibre_size_matches_chamber": (
                len(global_ids) == chamber_size
            ),
            "local_adjacency_symmetric": adjacency_symmetric(neighbors),
            "source_basis_rank_matches_closure": (
                source_basis_rank == closure_dimension
            ),
            "source_basis_hash_matches": (
                source_hash == certified_source_hash
            ),
            "complement_basis_rank_matches_dimension": (
                complement_basis_rank == complement_dimension
            ),
            "complement_basis_hash_matches": (
                complement_hash == certified_complement_hash
            ),
            "visible_action_exact": visible_action_exact,
            "invisible_action_exact": invisible_action_exact,
            "rank_decomposition_exact": rank_sum_exact,
            "nullity_decomposition_exact": nullity_sum_exact,
            "kernel_rank_equivalence_exact": rank_equivalence_exact,
            "proper_kernel_law_if_applicable": (
                (not applicable) or law_pass
            ),
            "direct_image_check_if_requested": (
                (not direct_requested) or bool(direct_pass)
            ),
        }
        channel_pass = all(checks.values())
        all_channels_pass &= channel_pass
        elapsed_channel = time.perf_counter() - channel_started


        row = {
            "subset": subset_text(subset),
            "channel_class": channel_class,
            "source_chamber_size": chamber_size,
            "closure_dimension": closure_dimension,
            "complement_dimension": complement_dimension,
            "chamber_adjacency_rank": chamber_rank,
            "chamber_adjacency_nullity": chamber_nullity,
            "visible_action_rank": visible_rank,
            "visible_action_nullity": visible_nullity,
            "invisible_action_rank": invisible_rank,
            "invisible_action_nullity": invisible_nullity,
            "invisible_action_zero_exact": invisible_zero,
            "rank_decomposition_exact": rank_sum_exact,
            "nullity_decomposition_exact": nullity_sum_exact,
            "kernel_law_applicable": applicable,
            "kernel_law_pass": law_pass,
            "law_status": law_status,
            "image_containment_inferred_exact": invisible_rank == 0,
            "direct_image_check_requested": direct_requested,
            "direct_image_contains": (
                "" if direct_contains is None else direct_contains
            ),
            "direct_image_check_pass": (
                "" if direct_pass is None else direct_pass
            ),
            "channel_certificate_pass": channel_pass,
            "elapsed_seconds": elapsed_channel,
        }


        certificate = {
            "probe": "EHF-XBR-04F2",
            "title": "Invisible-Kernel Law Census",
            "script_version": SCRIPT_VERSION,
            "utc_completed": utc_now(),
            "subset": list(subset),
            "dimensions": {
                "chamber": chamber_size,
                "visible_sector": closure_dimension,
                "invisible_complement": complement_dimension,
            },
            "ranks": {
                "chamber_adjacency": chamber_rank,
                "visible_restriction": visible_rank,
                "invisible_restriction": invisible_rank,
            },
            "nullities": {
                "chamber_adjacency": chamber_nullity,
                "visible_restriction": visible_nullity,
                "invisible_restriction": invisible_nullity,
            },
            "kernel_law": {
                "applicable": applicable,
                "status": law_status,
                "pass": law_pass,
                "invisible_action_zero_exact": invisible_zero,
                "image_containment_inferred_exact": invisible_rank == 0,
                "direct_image_check_requested": direct_requested,
                "direct_image_contains": direct_contains,
                "direct_image_check_pass": direct_pass,
            },
            "checks": checks,
            "strict_pass": channel_pass,
            "ledger_row": row,
            "elapsed_seconds": elapsed_channel,
        }
        channel_out = channel_root / subset_slug(subset)
        channel_out.mkdir(parents=True, exist_ok=True)
        write_json(channel_out / "certificate.json", certificate)
        ledger.append(row)
        completed[subset] = row
        write_csv(ledger_path, ledger)


        display = {
            "target_pass": "PASS",
            "target_fail": "FAIL",
            "vacuous_full_chamber": "vacuous",
            "excluded_zero_image": "excluded",
        }[law_status]
        print(
            f"[channel {number}/{len(selected)}] A={subset} "
            f"class={channel_class} closure={closure_dimension}/{chamber_size} "
            f"ker={chamber_nullity} visible0={visible_nullity} "
            f"invisible0={invisible_nullity} invisible_rank={invisible_rank} "
            f"law={display} pass={channel_pass} "
            f"elapsed={elapsed_channel:.2f}s"
        )


    ledger.sort(key=lambda row: parse_subset(row["subset"]))
    write_csv(ledger_path, ledger)


    full_selection = set(selected) == set(source_by_subset)
    class_counts = {
        "zero_image_whole_complement": sum(
            row["channel_class"] == "zero_image_whole_complement"
            for row in ledger
        ),
        "proper_sector_nonzero_complement": sum(
            row["channel_class"] == "proper_sector_nonzero_complement"
            for row in ledger
        ),
        "full_chamber_zero_complement": sum(
            row["channel_class"] == "full_chamber_zero_complement"
            for row in ledger
        ),
    }


    checks: Dict[str, bool] = {
        "source_xbr04c_summary_pass": bool(
            xbr04c_summary.get("strict_pass")
        ),
        "source_xbr04d_summary_pass": bool(
            xbr04d_summary.get("strict_pass")
        ),
        "selected_channels_complete": set(completed) == set(selected),
        "all_selected_channel_certificates_pass": all_channels_pass,
        "all_applicable_proper_channels_satisfy_kernel_law": (
            all_targets_pass
        ),
        "direct_image_checks_pass_if_requested": (
            direct_completed == direct_passes
        ),
    }
    if full_selection:
        checks.update({
            "full_census_channel_count_35": len(selected) == 35,
            "full_census_class_trichotomy_4_20_11": (
                class_counts["zero_image_whole_complement"] == 4
                and class_counts["proper_sector_nonzero_complement"] == 20
                and class_counts["full_chamber_zero_complement"] == 11
            ),
            "source_xbr04c_full_verdict": (
                xbr04c_summary.get("verdict")
                == "EHF_XBR_04C_EXACT_RESTRICTED_ACTION_CERTIFICATE_PASS"
            ),
            "source_xbr04d_full_verdict": (
                xbr04d_summary.get("verdict")
                == "EHF_XBR_04D_EXACT_LATTICE_INVISIBLE_COMPLEMENT_PASS"
            ),
        })


    strict_pass = all(checks.values())
    if full_selection and strict_pass:
        verdict = "EHF_XBR_04F2_INVISIBLE_KERNEL_LAW_CENSUS_PASS"
    elif strict_pass:
        verdict = (
            "EHF_XBR_04F2_SELECTED_INVISIBLE_KERNEL_CERTIFICATES_PASS"
        )
    else:
        verdict = "EHF_XBR_04F2_INVISIBLE_KERNEL_LAW_CENSUS_FAIL"


    elapsed = time.perf_counter() - started
    summary = {
        "probe": "EHF-XBR-04F2",
        "title": "Invisible-Kernel Law Census",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "counts": {
            "selected_channels": len(selected),
            "completed_channels": len(completed),
            **class_counts,
            "proper_target_channels": target_count,
            "proper_target_passes": target_passes,
            "full_vacuous_channels": full_vacuous,
            "zero_image_excluded_channels": zero_excluded,
            "direct_image_checks_completed": direct_completed,
            "direct_image_checks_passed": direct_passes,
        },
        "counterexamples": counterexamples,
        "checks": checks,
        "strict_pass": strict_pass,
        "verdict": verdict,
        "elapsed_seconds": elapsed,
    }
    write_json(out_dir / "run_summary.json", summary)


    print()
    print("[invisible-kernel law certification]")
    print(f"  selected={len(selected)} completed={len(completed)}")
    print(f"  proper targets={target_count} passes={target_passes}")
    print(
        f"  full vacuous={full_vacuous} "
        f"zero-image excluded={zero_excluded}"
    )
    print(f"  direct image checks={direct_passes}/{direct_completed}")
    print(f"  counterexamples={counterexamples}")
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