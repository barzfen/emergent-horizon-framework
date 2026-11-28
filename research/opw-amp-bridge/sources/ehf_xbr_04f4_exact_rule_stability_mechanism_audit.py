#!/usr/bin/env python3
r"""
EHF-XBR-04F4: Exact-Rule Stability and Mechanism Audit


Consumes the EHF-XBR-04F3 n=9 proper-channel classification and audits the
compact subset-geometry rule at four distinct levels:


1. exact finite-census reproduction;
2. leave-one-channel-out minimum-description-length rule recovery;
3. sensitivity under all 7! relabellings of the internal labels 2..8;
4. exact equivalences and independent pre-action mechanism proxies.


The locked descriptive rule is, for A=(a,b,c), a<b<c:


    null       if b=6 and 2 <= b-a <= 3;
    invertible elif a=2 or a+b+c=15;
    mixed      otherwise.


This probe does not promote the rule to a theorem of mechanism.  It explicitly
separates exact finite-census identities from stable recovery, coordinate
symmetry and independently measured chamber structure.
"""


from __future__ import annotations


import argparse
import ast
import csv
import importlib.util
import itertools
import json
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple


SCRIPT_VERSION = "ehf_xbr_04f4_2026-07-27"
REGIMES = ("null", "mixed", "invertible")
LABELS = tuple(range(2, 9))
Subset = Tuple[int, int, int]
TERM_PATTERN = re.compile(r"^\(([^ ]+) (==|<=|>=) (.+)\)$")




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




def integer(row: Mapping[str, object], key: str) -> int:
    return int(str(row[key]))




def truthy(value: object) -> bool:
    return str(value).strip().lower() == "true"




def parse_dirs(text: str) -> List[Path]:
    if not text.strip():
        return []
    return [Path(item.strip()).resolve() for item in text.split(";") if item.strip()]




def geometry(subset: Subset) -> Dict[str, object]:
    a, b, c = subset
    return {
        "label_min": a,
        "label_mid": b,
        "label_max": c,
        "gap_left": b - a,
        "gap_right": c - b,
        "span": c - a,
        "label_sum": a + b + c,
        "touches_lower_boundary": int(a == 2),
        "touches_upper_boundary": int(c == 8),
    }




def canonical_flags(subset: Subset) -> Dict[str, bool]:
    a, b, c = subset
    null_locus = b == 6 and 2 <= b - a <= 3
    lower_boundary = a == 2
    central_balance = a + b + c == 15
    invertible_locus = (not null_locus) and (lower_boundary or central_balance)
    return {
        "null_locus": null_locus,
        "lower_boundary": lower_boundary,
        "central_balance": central_balance,
        "invertible_locus": invertible_locus,
        "mixed_remainder": not null_locus and not invertible_locus,
    }




def canonical_rule(subset: Subset) -> str:
    flags = canonical_flags(subset)
    if flags["null_locus"]:
        return "null"
    if flags["invertible_locus"]:
        return "invertible"
    return "mixed"




def mechanism_class(subset: Subset) -> str:
    flags = canonical_flags(subset)
    if flags["null_locus"]:
        return "null_locus"
    if flags["lower_boundary"]:
        return "boundary_invertible"
    if flags["central_balance"]:
        return "balanced_invertible"
    return "mixed_remainder"




def parse_literal(text: str) -> object:
    text = text.strip()
    if text.startswith(("'", '"')):
        return ast.literal_eval(text)
    if re.fullmatch(r"-?\d+/\d+", text):
        numerator, denominator = text.split("/", 1)
        return Fraction(int(numerator), int(denominator))
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    try:
        return float(text)
    except ValueError:
        return text




def apply_operator(value: object, operator: str, threshold: object) -> bool:
    if operator == "==":
        return value == threshold
    if operator == "<=":
        return bool(value <= threshold)  # type: ignore[operator]
    if operator == ">=":
        return bool(value >= threshold)  # type: ignore[operator]
    raise ValueError(operator)




def expression_terms(expression: str) -> Tuple[str, List[Tuple[str, str, object]]]:
    if " AND " in expression:
        kind = "and"
        pieces = expression.split(" AND ")
    elif " OR " in expression:
        kind = "or"
        pieces = expression.split(" OR ")
    else:
        kind = "single"
        pieces = [expression]
    terms: List[Tuple[str, str, object]] = []
    for piece in pieces:
        match = TERM_PATTERN.fullmatch(piece.strip())
        if match is None:
            raise ValueError(f"cannot parse expression term: {piece}")
        feature, operator, threshold = match.groups()
        terms.append((feature, operator, parse_literal(threshold)))
    return kind, terms




def evaluate_expression(expression: str, features: Mapping[str, object]) -> bool:
    kind, terms = expression_terms(expression)
    values = [
        apply_operator(features[feature], operator, threshold)
        for feature, operator, threshold in terms
    ]
    if kind == "and":
        return all(values)
    if kind == "or":
        return any(values)
    return values[0]




def expression_feature_set(expression: str) -> Set[str]:
    return {feature for feature, _, _ in expression_terms(expression)[1]}




def evaluate_rule(rule: Mapping[str, object], features: Mapping[str, object]) -> str:
    if evaluate_expression(str(rule["first_expression"]), features):
        return str(rule["first_regime"])
    if evaluate_expression(str(rule["second_expression"]), features):
        return str(rule["second_regime"])
    return str(rule["else_regime"])




def rule_candidates(
    f3,
    rows: Sequence[Mapping[str, object]],
    expression_limit: int,
    expression_top: int,
) -> Tuple[List[dict], int]:
    records = [
        {
            "subset": row["subset"],
            "regime": row["regime"],
            "features": f3.subset_geometry_features(parse_subset(str(row["subset"]))),
        }
        for row in rows
    ]
    predicates = f3.build_predicates(records)
    exact_by: Dict[str, List[dict]] = {}
    for regime in REGIMES:
        exact_by[regime] = f3.exact_expressions(
            predicates,
            f3.regime_mask(records, regime),
            max_terms=3,
            limit=expression_limit,
        )


    candidates: Dict[str, dict] = {}
    for first_regime, second_regime in itertools.permutations(REGIMES, 2):
        third_regime = next(
            regime for regime in REGIMES
            if regime not in {first_regime, second_regime}
        )
        for first in exact_by[first_regime][:expression_top]:
            for second in exact_by[second_regime][:expression_top]:
                features = expression_feature_set(first["expression"])
                features |= expression_feature_set(second["expression"])
                text = (
                    f"IF {first['expression']} THEN {first_regime}; "
                    f"ELIF {second['expression']} THEN {second_regime}; "
                    f"ELSE {third_regime}"
                )
                candidates[text] = {
                    "first_regime": first_regime,
                    "second_regime": second_regime,
                    "else_regime": third_regime,
                    "first_expression": first["expression"],
                    "second_expression": second["expression"],
                    "total_terms": int(first["term_count"]) + int(second["term_count"]),
                    "distinct_feature_count": len(features),
                    "features": ";".join(sorted(features)),
                    "character_count": len(text),
                    "rule_list": text,
                }
    result = sorted(
        candidates.values(),
        key=lambda row: (
            row["total_terms"],
            row["distinct_feature_count"],
            row["character_count"],
            row["rule_list"],
        ),
    )
    return result, len(predicates)




def mdl_primary(rule: Mapping[str, object]) -> Tuple[int, int, int]:
    return (
        int(rule["total_terms"]),
        int(rule["distinct_feature_count"]),
        int(rule["character_count"]),
    )




def enrich_rule_predictions(
    rule: Mapping[str, object],
    rows: Sequence[Mapping[str, object]],
    f3,
) -> Tuple[int, str]:
    correct = 0
    predictions: List[str] = []
    for row in rows:
        features = f3.subset_geometry_features(parse_subset(str(row["subset"])))
        prediction = evaluate_rule(rule, features)
        predictions.append(prediction)
        correct += int(prediction == row["regime"])
    return correct, ";".join(predictions)




def comparison_row(name: str, left: Set[Subset], right: Set[Subset]) -> dict:
    return {
        "comparison": name,
        "left_count": len(left),
        "right_count": len(right),
        "equal": left == right,
        "left_only": ";".join(subset_text(value) for value in sorted(left - right)),
        "right_only": ";".join(subset_text(value) for value in sorted(right - left)),
    }




def mapped_subset(subset: Subset, mapping: Mapping[int, int]) -> Subset:
    return tuple(sorted(mapping[value] for value in subset))  # type: ignore[return-value]




def permutation_text(mapping: Mapping[int, int]) -> str:
    return ";".join(f"{label}->{mapping[label]}" for label in LABELS)




def cycle_text(mapping: Mapping[int, int]) -> str:
    visited: Set[int] = set()
    cycles: List[str] = []
    for start in LABELS:
        if start in visited or mapping[start] == start:
            visited.add(start)
            continue
        cycle: List[int] = []
        current = start
        while current not in visited:
            visited.add(current)
            cycle.append(current)
            current = mapping[current]
        cycles.append("(" + " ".join(map(str, cycle)) + ")")
    return "".join(cycles) if cycles else "identity"




def parse_number(value: object) -> Fraction | float | int | None:
    text = str(value).strip()
    if not text or text.lower() in {"true", "false", "none", "null"}:
        return None
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+/\d+", text):
        numerator, denominator = text.split("/", 1)
        return Fraction(int(numerator), int(denominator))
    try:
        return float(text)
    except ValueError:
        return None




def numeric_feature_columns(rows: Sequence[Mapping[str, object]]) -> List[str]:
    explicit = {"source_chamber_size", "closure_dimension", "complement_dimension"}
    forbidden = (
        "action", "adjacency", "nullity", "rank", "spectrum", "eigen",
        "factor", "charpoly", "minimal", "pass", "hash", "sha", "path",
        "elapsed", "matrix", "denominator", "numerator", "zero", "nonzero",
        "certificate", "verdict",
    )
    candidates: Set[str] = set(explicit)
    for key in rows[0]:
        if key.startswith(("xbr04c_", "xbr04d_")):
            lowered = key.lower()
            if not any(token in lowered for token in forbidden):
                candidates.add(key)
    valid: List[str] = []
    for key in sorted(candidates):
        values = [parse_number(row.get(key, "")) for row in rows]
        if all(value is not None for value in values) and len(set(values)) > 1:
            valid.append(key)
    return valid




def best_binary_proxy(
    rows: Sequence[Mapping[str, object]],
    feature: str,
    target_name: str,
    target_values: Sequence[bool],
) -> dict:
    values = [parse_number(row[feature]) for row in rows]
    if any(value is None for value in values):
        raise ValueError(feature)
    numeric_values = list(values)  # type: ignore[assignment]
    unique = sorted(set(numeric_values))
    candidates: List[Tuple[str, object]] = [("==", value) for value in unique]
    candidates.extend(("<=", value) for value in unique[:-1])
    candidates.extend((">=", value) for value in unique[1:])
    best = None
    for operator, threshold in candidates:
        base = [apply_operator(value, operator, threshold) for value in numeric_values]
        for direction in (True, False):
            predicted = base if direction else [not value for value in base]
            tp = sum(p and t for p, t in zip(predicted, target_values))
            fp = sum(p and not t for p, t in zip(predicted, target_values))
            fn = sum((not p) and t for p, t in zip(predicted, target_values))
            tn = sum((not p) and (not t) for p, t in zip(predicted, target_values))
            correct = tp + tn
            predicate = f"{feature} {operator} {threshold}"
            if not direction:
                predicate = f"NOT ({predicate})"
            score = (correct, tp, -fp, -fn, -len(predicate))
            row = {
                "target": target_name,
                "feature": feature,
                "predicate": predicate,
                "correct": correct,
                "total": len(rows),
                "accuracy": f"{correct}/{len(rows)}",
                "true_positive": tp,
                "false_positive": fp,
                "false_negative": fn,
                "true_negative": tn,
                "exact": correct == len(rows),
            }
            if best is None or score > best[0]:
                best = (score, row)
    if best is None:
        raise ValueError(f"no proxy for {feature}")
    return best[1]




def json_compact(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))




def symmetry_audit(null_subsets: Sequence[Subset], directories: Sequence[Path]) -> List[dict]:
    rows: List[dict] = []
    for subset in null_subsets:
        found = None
        for directory in directories:
            path = directory / "channels" / subset_slug(subset) / "certificate.json"
            if path.exists():
                found = path
                break
        if found is None:
            rows.append({
                "subset": subset_text(subset),
                "certificate_found": False,
                "certificate_path": "",
            })
            continue
        certificate = read_json(found)
        spectrum = certificate.get("spectrum", {})
        symmetry = certificate.get("symmetry", {})
        charpoly = spectrum.get("complement_characteristic_polynomial", {})
        minpoly = spectrum.get("complement_minimal_polynomial", {})
        signature_payload = {
            "group_order": symmetry.get("opw3_chamber_automorphism_group_order"),
            "image_order": symmetry.get("representation_image_order_if_full"),
            "fixed": symmetry.get("fixed_space_distribution_if_full"),
            "trace": symmetry.get("trace_distribution_if_full"),
        }
        rows.append({
            "subset": subset_text(subset),
            "certificate_found": True,
            "certificate_path": str(found),
            "complement_dimension": certificate.get("dimensions", {}).get(
                "complement", certificate.get("complement_dimension", "")
            ),
            "characteristic_polynomial": charpoly.get("text", ""),
            "minimal_polynomial": minpoly.get("text", ""),
            "automorphism_group_order": symmetry.get(
                "opw3_chamber_automorphism_group_order", ""
            ),
            "representation_image_order": symmetry.get(
                "representation_image_order_if_full", ""
            ),
            "generators": json_compact(symmetry.get("generators", [])),
            "fixed_space_distribution": json_compact(
                symmetry.get("fixed_space_distribution_if_full", {})
            ),
            "trace_distribution": json_compact(
                symmetry.get("trace_distribution_if_full", {})
            ),
            "symmetry_signature": json_compact(signature_payload),
        })
    return rows




def self_test() -> None:
    expected = {
        (3, 6, 7): "null",
        (4, 6, 7): "null",
        (4, 6, 8): "null",
        (2, 3, 6): "invertible",
        (3, 4, 8): "invertible",
        (3, 4, 6): "mixed",
    }
    assert all(canonical_rule(subset) == regime for subset, regime in expected.items())
    expression = "(gap_left <= 3) AND (gap_left >= 2) AND (label_mid == 6)"
    assert evaluate_expression(expression, {"gap_left": 3, "label_mid": 6})
    assert not evaluate_expression(expression, {"gap_left": 1, "label_mid": 6})
    identity = {label: label for label in LABELS}
    assert mapped_subset((3, 6, 7), identity) == (3, 6, 7)
    assert cycle_text(identity) == "identity"
    print("EHF-XBR-04F4 self-test PASS")




def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit exact-rule stability, relabelling and mechanism proxies."
    )
    parser.add_argument("--xbr04f3-dir")
    parser.add_argument("--xbr04f3-script")
    parser.add_argument(
        "--xbr04f-dirs",
        default="",
        help="semicolon-separated XBR-04F output directories for null symmetry audit",
    )
    parser.add_argument("--expression-limit", type=int, default=50)
    parser.add_argument("--expression-top", type=int, default=5)
    parser.add_argument("--out-dir", default="runs/ehf_xbr_04f4")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()


    if args.self_test:
        self_test()
        return 0


    missing = [
        name for name in ("xbr04f3_dir", "xbr04f3_script")
        if not getattr(args, name)
    ]
    if missing:
        parser.error("missing required arguments: " + ", ".join(missing))


    started = time.perf_counter()
    f3_dir = Path(args.xbr04f3_dir).resolve()
    f3_script_path = Path(args.xbr04f3_script).resolve()
    symmetry_dirs = parse_dirs(args.xbr04f_dirs)
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)


    ledger_path = f3_dir / "classification_ledger.csv"
    summary_path = f3_dir / "run_summary.json"
    for path in (ledger_path, summary_path, f3_script_path):
        if not path.exists():
            raise FileNotFoundError(path)


    f3 = load_module(f3_script_path, "ehf_xbr_04f4_source_f3")
    rows = read_csv(ledger_path)
    rows.sort(key=lambda row: parse_subset(row["subset"]))
    f3_summary = read_json(summary_path)
    regime_counts = Counter(row["regime"] for row in rows)


    print("=" * 128)
    print("EHF-XBR-04F4: EXACT-RULE STABILITY AND MECHANISM AUDIT")
    print("=" * 128)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"XBR-04F3 directory:   {f3_dir}")
    print(f"proper channels:      {len(rows)}")
    print(
        "regimes:             "
        f"null={regime_counts['null']} "
        f"mixed={regime_counts['mixed']} "
        f"invertible={regime_counts['invertible']}"
    )
    print(f"symmetry directories: {len(symmetry_dirs)}")
    print(f"output directory:     {out_dir}")
    print(f"strict:               {args.strict}")
    print()


    fixed_rows: List[dict] = []
    for row in rows:
        subset = parse_subset(row["subset"])
        prediction = canonical_rule(subset)
        flags = canonical_flags(subset)
        fixed_rows.append({
            "subset": row["subset"],
            "observed_regime": row["regime"],
            "predicted_regime": prediction,
            "correct": prediction == row["regime"],
            "mechanism_class": mechanism_class(subset),
            **flags,
        })
    fixed_correct = sum(truthy(row["correct"]) for row in fixed_rows)
    write_csv(out_dir / "fixed_rule_audit.csv", fixed_rows)


    full_candidates, full_predicate_count = rule_candidates(
        f3,
        rows,
        args.expression_limit,
        args.expression_top,
    )
    if not full_candidates:
        raise RuntimeError("no exact full-census rule candidates")
    minimum_primary = mdl_primary(full_candidates[0])
    minimum_rules = [
        rule for rule in full_candidates if mdl_primary(rule) == minimum_primary
    ]
    competition_rows: List[dict] = []
    for rank, rule in enumerate(full_candidates, start=1):
        correct, predictions = enrich_rule_predictions(rule, rows, f3)
        competition_rows.append({
            "rank": rank,
            "minimum_mdl_tie": mdl_primary(rule) == minimum_primary,
            "full_census_correct": correct,
            "full_census_total": len(rows),
            "full_census_exact": correct == len(rows),
            "prediction_sequence": predictions,
            **rule,
        })
    write_csv(out_dir / "mdl_rule_competition.csv", competition_rows)


    loo_rows: List[dict] = []
    for held_index, held_row in enumerate(rows):
        training = [row for index, row in enumerate(rows) if index != held_index]
        candidates, predicate_count = rule_candidates(
            f3,
            training,
            args.expression_limit,
            args.expression_top,
        )
        if not candidates:
            loo_rows.append({
                "held_out_subset": held_row["subset"],
                "held_out_regime": held_row["regime"],
                "status": "no_exact_training_rule",
            })
            continue
        primary = mdl_primary(candidates[0])
        ties = [rule for rule in candidates if mdl_primary(rule) == primary]
        chosen = sorted(ties, key=lambda rule: rule["rule_list"])[0]
        held_features = f3.subset_geometry_features(parse_subset(held_row["subset"]))
        chosen_prediction = evaluate_rule(chosen, held_features)
        tie_predictions = Counter(
            evaluate_rule(rule, held_features) for rule in ties
        )
        full_correct, _ = enrich_rule_predictions(chosen, rows, f3)
        loo_rows.append({
            "held_out_subset": held_row["subset"],
            "held_out_regime": held_row["regime"],
            "status": "completed",
            "training_channels": len(training),
            "predicate_count": predicate_count,
            "exact_training_rule_count": len(candidates),
            "minimum_mdl_terms": primary[0],
            "minimum_mdl_distinct_features": primary[1],
            "minimum_mdl_characters": primary[2],
            "minimum_mdl_tie_count": len(ties),
            "minimum_tie_prediction_counts": json_compact(dict(tie_predictions)),
            "minimum_tie_consensus": len(tie_predictions) == 1,
            "chosen_prediction": chosen_prediction,
            "chosen_correct": chosen_prediction == held_row["regime"],
            "chosen_full_census_correct": full_correct,
            "chosen_full_census_exact": full_correct == len(rows),
            "canonical_prediction": canonical_rule(parse_subset(held_row["subset"])),
            "canonical_correct": canonical_rule(parse_subset(held_row["subset"])) == held_row["regime"],
            "chosen_rule": chosen["rule_list"],
        })
    write_csv(out_dir / "loo_rule_recovery.csv", loo_rows)
    loo_audited = len(loo_rows)
    loo_completed = [row for row in loo_rows if row.get("status") == "completed"]
    loo_chosen_correct = sum(truthy(row.get("chosen_correct", False)) for row in loo_completed)
    loo_consensus = sum(truthy(row.get("minimum_tie_consensus", False)) for row in loo_completed)
    loo_full_exact = sum(truthy(row.get("chosen_full_census_exact", False)) for row in loo_completed)


    by_subset = {parse_subset(row["subset"]): row for row in rows}
    proper_set = set(by_subset)
    observed_sets = {
        regime: {subset for subset, row in by_subset.items() if row["regime"] == regime}
        for regime in REGIMES
    }
    candidate_null = {subset for subset in proper_set if canonical_flags(subset)["null_locus"]}
    candidate_invertible = {
        subset for subset in proper_set if canonical_flags(subset)["invertible_locus"]
    }
    candidate_mixed = proper_set - candidate_null - candidate_invertible
    small_complement = {
        subset for subset, row in by_subset.items()
        if integer(row, "complement_dimension") <= 10
    }
    chamber_nonsingular = {
        subset for subset, row in by_subset.items()
        if integer(row, "chamber_adjacency_nullity") == 0
    }
    chamber_singular_large_complement = {
        subset for subset, row in by_subset.items()
        if integer(row, "chamber_adjacency_nullity") > 0
        and integer(row, "complement_dimension") > 10
    }
    boundary_or_balance = {
        subset for subset in proper_set
        if subset[0] == 2 or sum(subset) == 15
    }
    equivalence_rows = [
        comparison_row("candidate_null_equals_observed_null", candidate_null, observed_sets["null"]),
        comparison_row("candidate_invertible_equals_observed_invertible", candidate_invertible, observed_sets["invertible"]),
        comparison_row("candidate_mixed_equals_observed_mixed", candidate_mixed, observed_sets["mixed"]),
        comparison_row("null_equals_complement_dimension_le_10", observed_sets["null"], small_complement),
        comparison_row("invertible_equals_chamber_adjacency_nullity_zero", observed_sets["invertible"], chamber_nonsingular),
        comparison_row("boundary_or_balance_equals_chamber_nonsingular", boundary_or_balance, chamber_nonsingular),
        comparison_row("mixed_equals_singular_large_complement", observed_sets["mixed"], chamber_singular_large_complement),
    ]
    write_csv(out_dir / "exact_equivalence_audit.csv", equivalence_rows)


    automorphism_rows: List[dict] = []
    partition_orbit: Set[Tuple[Tuple[Subset, ...], Tuple[Subset, ...], Tuple[Subset, ...]]] = set()
    permutations_audited = 0
    proper_automorphism_count = 0
    regime_automorphism_count = 0
    for permutation in itertools.permutations(LABELS):
        permutations_audited += 1
        mapping = dict(zip(LABELS, permutation))
        mapped_partition = tuple(
            tuple(sorted(mapped_subset(subset, mapping) for subset in observed_sets[regime]))
            for regime in REGIMES
        )
        partition_orbit.add(mapped_partition)  # type: ignore[arg-type]
        mapped_proper = {mapped_subset(subset, mapping) for subset in proper_set}
        if mapped_proper != proper_set:
            continue
        proper_automorphism_count += 1
        regime_preserving = all(
            by_subset[mapped_subset(subset, mapping)]["regime"] == by_subset[subset]["regime"]
            for subset in proper_set
        )
        regime_automorphism_count += int(regime_preserving)
        automorphism_rows.append({
            "permutation": permutation_text(mapping),
            "cycles": cycle_text(mapping),
            "proper_set_automorphism": True,
            "regime_partition_automorphism": regime_preserving,
            "is_identity": all(mapping[label] == label for label in LABELS),
            "is_reflection_10_minus_label": all(mapping[label] == 10 - label for label in LABELS),
        })
    write_csv(out_dir / "label_relabelling_automorphisms.csv", automorphism_rows)


    mechanism_columns = numeric_feature_columns(rows)
    mechanism_targets = {
        "null_locus": [canonical_flags(parse_subset(row["subset"]))["null_locus"] for row in rows],
        "lower_boundary": [canonical_flags(parse_subset(row["subset"]))["lower_boundary"] for row in rows],
        "central_balance": [canonical_flags(parse_subset(row["subset"]))["central_balance"] for row in rows],
        "invertible_geometry": [canonical_flags(parse_subset(row["subset"]))["invertible_locus"] for row in rows],
    }
    proxy_rows: List[dict] = []
    for target_name, target_values in mechanism_targets.items():
        for feature in mechanism_columns:
            proxy_rows.append(best_binary_proxy(rows, feature, target_name, target_values))
    proxy_rows.sort(
        key=lambda row: (
            row["target"],
            -int(row["correct"]),
            len(str(row["predicate"])),
            row["feature"],
        )
    )
    write_csv(out_dir / "mechanism_proxy_single_predicates.csv", proxy_rows)


    group_summary_rows: List[dict] = []
    core_features = [
        feature for feature in (
            "source_chamber_size", "closure_dimension", "complement_dimension",
            "chamber_adjacency_nullity", "visible_action_nullity",
        ) if feature in rows[0]
    ]
    for group in ("null_locus", "boundary_invertible", "balanced_invertible", "mixed_remainder"):
        members = [row for row in rows if mechanism_class(parse_subset(row["subset"])) == group]
        for feature in core_features:
            values = [parse_number(row[feature]) for row in members]
            group_summary_rows.append({
                "mechanism_class": group,
                "feature": feature,
                "channel_count": len(members),
                "minimum": min(values) if values else "",
                "maximum": max(values) if values else "",
                "unique_values": ";".join(map(str, sorted(set(values)))) if values else "",
                "subsets": ";".join(row["subset"] for row in members),
            })
    write_csv(out_dir / "mechanism_group_summary.csv", group_summary_rows)


    null_subsets = sorted(observed_sets["null"])
    symmetry_rows = symmetry_audit(null_subsets, symmetry_dirs) if symmetry_dirs else []
    write_csv(out_dir / "null_symmetry_audit.csv", symmetry_rows)
    symmetry_found = sum(truthy(row.get("certificate_found", False)) for row in symmetry_rows)
    symmetry_signatures = {
        row.get("symmetry_signature") for row in symmetry_rows
        if truthy(row.get("certificate_found", False))
    }


    checks: Dict[str, bool] = {
        "source_f3_verdict_pass": (
            f3_summary.get("verdict")
            == "EHF_XBR_04F3_INVISIBLE_ACTION_RANK_NULLITY_CLASSIFICATION_PASS"
        ),
        "proper_channel_count_20": len(rows) == 20,
        "regime_counts_3_8_9": (
            regime_counts["null"] == 3
            and regime_counts["mixed"] == 8
            and regime_counts["invertible"] == 9
        ),
        "fixed_candidate_rule_exact_20_of_20": fixed_correct == 20,
        "full_mdl_rule_candidates_exist": bool(full_candidates),
        "loo_holdouts_audited_20": loo_audited == 20,
        "all_exact_equivalence_rows_hold": all(truthy(row["equal"]) for row in equivalence_rows),
        "all_5040_label_permutations_audited": permutations_audited == 5040,
        "identity_is_proper_regime_automorphism": any(
            truthy(row["is_identity"]) and truthy(row["regime_partition_automorphism"])
            for row in automorphism_rows
        ),
        "mechanism_proxy_audit_nonempty": bool(proxy_rows),
        "null_symmetry_sources_complete_if_requested": (
            not symmetry_dirs or symmetry_found == 3
        ),
    }
    strict_pass = all(checks.values())
    verdict = (
        "EHF_XBR_04F4_EXACT_RULE_STABILITY_MECHANISM_AUDIT_PASS"
        if strict_pass
        else "EHF_XBR_04F4_EXACT_RULE_STABILITY_MECHANISM_AUDIT_FAIL"
    )


    stability_label = (
        "stable_unique_consensus"
        if loo_chosen_correct == 20 and loo_consensus == 20
        else "stable_chosen_rule_only"
        if loo_chosen_correct == 20
        else "partial_or_unstable_recovery"
    )
    symmetry_label = (
        "coordinate_rigid"
        if regime_automorphism_count == 1
        else "nontrivial_regime_relabelling_symmetry"
    )
    symmetry_status = (
        "not_requested"
        if not symmetry_dirs
        else "all_three_distinguished"
        if symmetry_found == 3 and len(symmetry_signatures) == 3
        else "available_but_not_all_distinguished"
        if symmetry_found == 3
        else "incomplete"
    )


    report_lines = [
        "# EHF-XBR-04F4 Stability and Mechanism Report",
        "",
        f"- Fixed candidate accuracy: {fixed_correct}/20",
        f"- Full exact MDL candidates: {len(full_candidates)}",
        f"- Minimum MDL score: {minimum_primary}",
        f"- Minimum MDL tie count: {len(minimum_rules)}",
        f"- Leave-one-out holdouts audited: {loo_audited}/20",
        f"- Leave-one-out exact rules available: {len(loo_completed)}/20",
        f"- Leave-one-out chosen-rule accuracy when available: {loo_chosen_correct}/{len(loo_completed)}",
        f"- Leave-one-out minimum-tie consensus: {loo_consensus}/{len(loo_completed)}",
        f"- Leave-one-out chosen rules exact on all 20: {loo_full_exact}/{len(loo_completed)}",
        f"- Stability classification: {stability_label}",
        f"- Proper-set relabelling automorphisms: {proper_automorphism_count}",
        f"- Regime-preserving relabelling automorphisms: {regime_automorphism_count}",
        f"- Coloured-partition orbit size under S7: {len(partition_orbit)}",
        f"- Relabelling classification: {symmetry_label}",
        f"- Null symmetry status: {symmetry_status}",
        "",
        "## Exact mechanism-proxy equivalences",
        "",
    ]
    for row in equivalence_rows:
        report_lines.append(f"- {row['comparison']}: {row['equal']}")
    report_lines.extend([
        "",
        "## Claim boundary",
        "",
        "The displayed subset rule remains an exact description of the finite n=9",
        "proper-channel census. Leave-one-out recovery measures stability inside",
        "that same finite atlas; it is not fresh-n validation. Exact equivalence to",
        "chamber nonsingularity or complement-size thresholds identifies proxies,",
        "not yet causes. Relabelling rigidity measures coordinate dependence.",
        "",
    ])
    (out_dir / "stability_mechanism_report.md").write_text(
        "\n".join(report_lines), encoding="utf-8"
    )


    elapsed = time.perf_counter() - started
    summary = {
        "probe": "EHF-XBR-04F4",
        "title": "Exact-Rule Stability and Mechanism Audit",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "counts": {
            "proper_channels": len(rows),
            "fixed_rule_correct": fixed_correct,
            "full_predicate_count": full_predicate_count,
            "full_exact_rule_candidates": len(full_candidates),
            "minimum_mdl_tie_count": len(minimum_rules),
            "loo_holdouts_audited": loo_audited,
            "loo_rules_available": len(loo_completed),
            "loo_chosen_correct": loo_chosen_correct,
            "loo_minimum_tie_consensus": loo_consensus,
            "loo_chosen_full_census_exact": loo_full_exact,
            "label_permutations_audited": permutations_audited,
            "proper_set_automorphism_order": proper_automorphism_count,
            "regime_partition_automorphism_order": regime_automorphism_count,
            "coloured_partition_orbit_size": len(partition_orbit),
            "mechanism_numeric_feature_count": len(mechanism_columns),
            "mechanism_proxy_rows": len(proxy_rows),
            "null_symmetry_certificates_found": symmetry_found,
            "null_symmetry_distinct_signatures": len(symmetry_signatures),
        },
        "minimum_mdl_score": {
            "total_terms": minimum_primary[0],
            "distinct_features": minimum_primary[1],
            "character_count": minimum_primary[2],
        },
        "stability_classification": stability_label,
        "relabeling_classification": symmetry_label,
        "null_symmetry_status": symmetry_status,
        "checks": checks,
        "strict_pass": strict_pass,
        "verdict": verdict,
        "elapsed_seconds": elapsed,
    }
    write_json(out_dir / "run_summary.json", summary)


    print("[fixed candidate rule]")
    print(f"  exact={fixed_correct}/20")
    print("[minimum-description-length competition]")
    print(
        f"  predicates={full_predicate_count} exact_rules={len(full_candidates)} "
        f"minimum={minimum_primary} ties={len(minimum_rules)}"
    )
    print("[leave-one-channel-out recovery]")
    print(
        f"  audited={loo_audited} rules_available={len(loo_completed)} "
        f"chosen_correct={loo_chosen_correct} tie_consensus={loo_consensus} "
        f"full_exact={loo_full_exact}"
    )
    print("[label relabelling audit]")
    print(
        f"  permutations={permutations_audited} proper_aut={proper_automorphism_count} "
        f"regime_aut={regime_automorphism_count} orbit={len(partition_orbit)}"
    )
    print("[mechanism equivalences]")
    for row in equivalence_rows:
        print(f"  {row['comparison']}={row['equal']}")
    print("[null symmetry audit]")
    print(
        f"  status={symmetry_status} found={symmetry_found}/3 "
        f"distinct_signatures={len(symmetry_signatures)}"
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