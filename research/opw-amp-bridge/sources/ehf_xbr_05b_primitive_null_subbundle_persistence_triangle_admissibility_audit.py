#!/usr/bin/env python3
"""
EHF-XBR-05B: Primitive Null-Subbundle Persistence and Triangle Admissibility Audit

XBR-05A proved that the complete null fibers change dimension on every
Johnson edge, so ordinary whole-kernel holonomy is undefined.  XBR-05B asks
the narrower prerequisite question:

    Does one exactly certified primitive module type recur with constant
    multiplicity at all three vertices of a minimal null-channel triangle?

The probe reconstructs the final primitive census by taking the XBR-04F8
primitive ledger and replacing its residual unresolved blocks with the exact
XBR-04F8B resolutions.  It then distinguishes:

* exact persistence: the same exact primitive type hash, hence the same
  literal acting group and primitive character, occurs at every vertex;
* coarse recurrence: dimension/order/trace data match across different
  literal groups, which is candidate evidence only;
* transport admissibility: exact persistence plus a complete certificate for
  all three cross-channel edge maps.

F8/F8B contain within-channel representation certificates.  They do not by
themselves define cross-channel comparison maps.  Therefore this probe never
promotes exact persistence to holonomy admissibility without an optional
external transport-certificate ledger satisfying the locked schema below.
It computes no loop matrix and assigns no physical interpretation.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Set, Tuple


SCRIPT_VERSION = "ehf_xbr_05b_v1_1_2026-07-31"
PROBE_NAME = "EHF-XBR-05B"
VERDICT_PASS = (
    "EHF_XBR_05B_PRIMITIVE_NULL_SUBBUNDLE_PERSISTENCE_"
    "TRIANGLE_ADMISSIBILITY_AUDIT_PASS"
)

Subset = Tuple[int, int, int]
Edge = Tuple[Subset, Subset]
Triangle = Tuple[Subset, Subset, Subset]
CertificateKey = Tuple[str, Edge, int]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "pass", "passed"}


def integer(row: Mapping[str, object], *names: str) -> int:
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return int(str(value))
    raise KeyError(f"none of the required integer fields is present: {names}")


def text_field(row: Mapping[str, object], *names: str) -> str:
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return str(value).strip()
    return ""


def parse_subset(text: object) -> Subset:
    # XBR-04F8/F8B serialize subsets as "(2, 3, 4)", whereas XBR-05A
    # uses "2,3,4". Accept both upstream representations, plus the
    # equivalent bracketed representation used by some intermediate ledgers.
    cleaned = str(text).strip()
    if (
        len(cleaned) >= 2
        and (cleaned[0], cleaned[-1]) in {("(", ")"), ("[", "]")}
    ):
        cleaned = cleaned[1:-1].strip()
    values = tuple(
        sorted(
            int(value.strip())
            for value in cleaned.split(",")
            if value.strip()
        )
    )
    if len(values) != 3 or len(set(values)) != 3:
        raise ValueError(f"invalid three-subset: {text!r}")
    if any(value not in range(2, 9) for value in values):
        raise ValueError(f"subset labels must lie in 2..8: {text!r}")
    return values  # type: ignore[return-value]


def subset_text(subset: Sequence[int]) -> str:
    return ",".join(map(str, subset))


def canonical_edge(left: Subset, right: Subset) -> Edge:
    if left == right:
        raise ValueError("a transport edge requires two distinct vertices")
    return (left, right) if left < right else (right, left)


def triangle_edges(triangle: Triangle) -> Tuple[Edge, Edge, Edge]:
    a, b, c = triangle
    return (
        canonical_edge(a, b),
        canonical_edge(b, c),
        canonical_edge(c, a),
    )


def parse_loop_word(text: object) -> Triangle:
    pieces = [piece.strip() for piece in str(text).split("->")]
    vertices = [parse_subset(piece) for piece in pieces if piece]
    if len(vertices) == 4 and vertices[0] == vertices[-1]:
        vertices = vertices[:-1]
    if len(vertices) != 3 or len(set(vertices)) != 3:
        raise ValueError(f"expected a closed triangle loop word, found {text!r}")
    return tuple(sorted(vertices))  # type: ignore[return-value]


def read_csv(path: Path) -> List[dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open() as handle:
        return json.load(handle)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_csv(
    path: Path,
    rows: Sequence[Mapping[str, object]],
    *,
    fields_if_empty: Sequence[str] = (),
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    seen: Set[str] = set()
    for row in rows:
        for field in row:
            if field not in seen:
                seen.add(field)
                fields.append(field)
    if not fields:
        fields = list(fields_if_empty)
    if not fields:
        path.write_text("")
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def occurrence_id(row: Mapping[str, object]) -> str:
    primitive_label = text_field(
        row, "final_primitive_index", "primitive_index", "resolved_primitive_index"
    )
    return (
        f"{row['subset']}#s{int(str(row['sector_index']))}"
        f"#p{primitive_label}"
    )


def normalized_f8_row(row: Mapping[str, object]) -> dict:
    return {
        "subset": subset_text(parse_subset(row["subset"])),
        "regime": row.get("regime", ""),
        "sector_index": integer(row, "sector_index"),
        "final_primitive_index": f"f8p{integer(row, 'primitive_index')}",
        "primitive_dimension": integer(row, "primitive_dimension"),
        "rational_irreducible_certified": truthy(
            row.get("rational_irreducible_certified")
        ),
        "absolutely_irreducible_certified": truthy(
            row.get("absolutely_irreducible_certified")
        ),
        "commutant_dimension": integer(
            row, "primitive_commutant_dimension", "commutant_dimension"
        ),
        "literal_group_hash": text_field(row, "literal_group_hash"),
        "exact_primitive_type_hash": text_field(
            row, "exact_primitive_type_hash"
        ),
        "coarse_primitive_type_hash": text_field(
            row, "coarse_primitive_type_hash"
        ),
        "primitive_basis_sha256": text_field(row, "primitive_basis_sha256"),
        "certification_kind": text_field(row, "certification_kind"),
        "source_stage": "XBR-04F8",
        "source_primitive_index": integer(row, "primitive_index"),
        "resolved_primitive_index": "",
        "type_inheritance_certificate": "native_f8_primitive_character",
    }


def reconstruct_final_primitives(
    f8_rows: Sequence[Mapping[str, object]],
    classification_rows: Sequence[Mapping[str, object]],
    resolved_rows: Sequence[Mapping[str, object]],
) -> Tuple[List[dict], dict]:
    """Replace the F8 residual blocks with their F8B certified resolutions."""
    f8_by_key: Dict[Tuple[str, int, int], Mapping[str, object]] = {}
    for row in f8_rows:
        key = (
            subset_text(parse_subset(row["subset"])),
            integer(row, "sector_index"),
            integer(row, "primitive_index"),
        )
        if key in f8_by_key:
            raise ValueError(f"duplicate F8 primitive key: {key}")
        f8_by_key[key] = row

    class_by_source: Dict[Tuple[str, int, int], Mapping[str, object]] = {}
    for row in classification_rows:
        key = (
            subset_text(parse_subset(row["subset"])),
            integer(row, "sector_index"),
            integer(row, "source_primitive_index"),
        )
        if key in class_by_source:
            raise ValueError(f"duplicate F8B classification source key: {key}")
        class_by_source[key] = row

    resolved_by_source: Dict[Tuple[str, int, int], List[Mapping[str, object]]] = (
        defaultdict(list)
    )
    for row in resolved_rows:
        key = (
            subset_text(parse_subset(row["subset"])),
            integer(row, "sector_index"),
            integer(row, "source_primitive_index"),
        )
        resolved_by_source[key].append(row)

    final_rows: List[dict] = []
    removed_sources = 0
    unresolved_without_f8b: List[Tuple[str, int, int]] = []
    for key, row in sorted(f8_by_key.items()):
        certified = truthy(row.get("rational_irreducible_certified"))
        if certified:
            final_rows.append(normalized_f8_row(row))
            continue
        if key not in class_by_source:
            unresolved_without_f8b.append(key)
            continue
        removed_sources += 1

    if unresolved_without_f8b:
        raise ValueError(
            "F8 contains unresolved blocks without an F8B resolution: "
            + repr(unresolved_without_f8b)
        )

    resolved_children_added = 0
    inheritance_failures: List[str] = []
    for source_key, classification in sorted(class_by_source.items()):
        if source_key not in f8_by_key:
            raise ValueError(
                f"F8B classification references absent F8 block: {source_key}"
            )
        source = f8_by_key[source_key]
        children = sorted(
            resolved_by_source.get(source_key, []),
            key=lambda row: integer(row, "resolved_primitive_index"),
        )
        expected_children = integer(classification, "resolved_block_count")
        if len(children) != expected_children:
            raise ValueError(
                f"F8B child count mismatch for {source_key}: "
                f"{len(children)} != {expected_children}"
            )

        algebra = text_field(classification, "algebra_classification")
        if algebra == "split_matrix_algebra_M2_Q":
            sibling_key = (
                source_key[0],
                source_key[1],
                integer(classification, "sibling_primitive_index"),
            )
            sibling = f8_by_key.get(sibling_key)
            if sibling is None or not truthy(
                sibling.get("rational_irreducible_certified")
            ):
                raise ValueError(
                    f"split F8B block lacks a certified F8 sibling: {source_key}"
                )
            inheritance_source = sibling
            inheritance_certificate = (
                "f8b_full_rank_isomorphism_to_certified_sibling"
            )
            classification_supports_inheritance = (
                truthy(classification.get("child_characters_equal_sibling"))
                and truthy(classification.get("child_modules_isomorphic_to_sibling"))
                and truthy(classification.get("outcome_certificate_complete"))
            )
        elif algebra == "quaternion_division_algebra":
            inheritance_source = source
            inheritance_certificate = (
                "f8b_division_commutant_certifies_source_character_primitive"
            )
            classification_supports_inheritance = truthy(
                classification.get("outcome_certificate_complete")
            )
        else:
            raise ValueError(
                f"unclassified F8B residual algebra for {source_key}: {algebra!r}"
            )

        for child in children:
            child_certified = truthy(
                child.get("rational_irreducible_certified")
            )
            child_inheritance_exact = classification_supports_inheritance
            if algebra == "split_matrix_algebra_M2_Q":
                child_inheritance_exact &= (
                    truthy(child.get("character_equals_certified_sibling"))
                    and truthy(child.get("full_rank_sibling_isomorphism_found"))
                )
            if not (child_certified and child_inheritance_exact):
                inheritance_failures.append(
                    f"{source_key}#r{integer(child, 'resolved_primitive_index')}"
                )

            final_rows.append({
                "subset": source_key[0],
                "regime": source.get("regime", ""),
                "sector_index": source_key[1],
                "final_primitive_index": (
                    f"f8bp{source_key[2]}r"
                    f"{integer(child, 'resolved_primitive_index')}"
                ),
                "primitive_dimension": integer(child, "resolved_dimension"),
                "rational_irreducible_certified": (
                    child_certified and child_inheritance_exact
                ),
                "absolutely_irreducible_certified": truthy(
                    child.get("absolutely_irreducible_certified")
                ),
                "commutant_dimension": integer(
                    child, "commutant_dimension"
                ),
                "literal_group_hash": text_field(
                    inheritance_source, "literal_group_hash"
                ),
                "exact_primitive_type_hash": text_field(
                    inheritance_source, "exact_primitive_type_hash"
                ),
                "coarse_primitive_type_hash": text_field(
                    inheritance_source, "coarse_primitive_type_hash"
                ),
                "primitive_basis_sha256": text_field(
                    child, "resolved_basis_sha256"
                ),
                "certification_kind": text_field(
                    child, "certification_kind"
                ),
                "source_stage": "XBR-04F8B",
                "source_primitive_index": source_key[2],
                "resolved_primitive_index": integer(
                    child, "resolved_primitive_index"
                ),
                "type_inheritance_certificate": inheritance_certificate,
            })
            resolved_children_added += 1

    final_rows.sort(
        key=lambda row: (
            parse_subset(row["subset"]),
            int(row["sector_index"]),
            str(row["final_primitive_index"]),
        )
    )
    diagnostics = {
        "f8_source_blocks": len(f8_rows),
        "f8_certified_blocks_retained": len(f8_rows) - removed_sources,
        "f8_residual_blocks_replaced": removed_sources,
        "f8b_resolved_children_added": resolved_children_added,
        "final_primitive_blocks": len(final_rows),
        "type_inheritance_failures": inheritance_failures,
    }
    return final_rows, diagnostics


def grouped_rows(
    rows: Sequence[Mapping[str, object]],
    hash_field: str,
) -> Dict[str, Dict[Subset, List[Mapping[str, object]]]]:
    result: Dict[str, Dict[Subset, List[Mapping[str, object]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for row in rows:
        type_hash = text_field(row, hash_field)
        if type_hash:
            result[type_hash][parse_subset(row["subset"])].append(row)
    return result


def persistence_ledger(
    exact_groups: Mapping[str, Mapping[Subset, Sequence[Mapping[str, object]]]],
) -> List[dict]:
    rows: List[dict] = []
    for type_hash, by_vertex in sorted(exact_groups.items()):
        flat = [row for values in by_vertex.values() for row in values]
        dimensions = sorted({integer(row, "primitive_dimension") for row in flat})
        literal_groups = sorted(
            {text_field(row, "literal_group_hash") for row in flat}
        )
        multiplicities = {
            subset_text(vertex): len(values)
            for vertex, values in sorted(by_vertex.items())
        }
        rows.append({
            "exact_primitive_type_hash": type_hash,
            "primitive_dimension": (
                dimensions[0] if len(dimensions) == 1 else ";".join(map(str, dimensions))
            ),
            "occurrence_count": len(flat),
            "distinct_channel_count": len(by_vertex),
            "channels": ";".join(subset_text(vertex) for vertex in sorted(by_vertex)),
            "channel_multiplicities": ";".join(
                f"{key}:{value}" for key, value in multiplicities.items()
            ),
            "literal_group_hash_count": len(literal_groups),
            "common_literal_group_exact": len(literal_groups) == 1,
            "triangle_persistence_possible": len(by_vertex) >= 3,
        })
    return rows


def load_transport_certificates(
    path: Path | None,
) -> Tuple[Dict[CertificateKey, dict], dict]:
    if path is None:
        return {}, {
            "provided": False,
            "rows": 0,
            "duplicate_keys": 0,
            "schema_errors": [],
        }
    rows = read_csv(path)
    certificates: Dict[CertificateKey, dict] = {}
    duplicate_keys = 0
    schema_errors: List[str] = []
    for index, row in enumerate(rows):
        try:
            type_hash = text_field(row, "exact_primitive_type_hash", "type_hash")
            left = parse_subset(
                text_field(row, "source_subset", "left_subset")
            )
            right = parse_subset(
                text_field(row, "target_subset", "right_subset")
            )
            rank = integer(
                row, "subbundle_rank", "fiber_rank", "expected_rank"
            )
            key = (type_hash, canonical_edge(left, right), rank)
            if not type_hash:
                raise ValueError("empty exact primitive type hash")
            if key in certificates:
                duplicate_keys += 1
            certificates[key] = dict(row)
        except Exception as exc:
            schema_errors.append(f"row {index}: {exc}")
    return certificates, {
        "provided": True,
        "rows": len(rows),
        "duplicate_keys": duplicate_keys,
        "schema_errors": schema_errors,
    }


def certificate_exact(
    row: Mapping[str, object] | None,
    *,
    expected_rank: int,
) -> Tuple[bool, str]:
    if row is None:
        return False, "missing"
    try:
        rank_fields_match = (
            integer(row, "subbundle_rank", "fiber_rank", "expected_rank")
            == expected_rank
            and integer(row, "source_subbundle_dimension", "source_dimension")
            == expected_rank
            and integer(row, "target_subbundle_dimension", "target_dimension")
            == expected_rank
            and integer(row, "forward_rank") == expected_rank
            and integer(row, "reverse_rank") == expected_rank
        )
    except (KeyError, TypeError, ValueError) as exc:
        return False, f"failed:certificate_schema:{exc}"
    boolean_fields = (
        "canonical_comparison_defined",
        "forward_reverse_identity_exact",
        "reverse_forward_identity_exact",
        "gauge_covariance_exact",
        "strict_pass",
    )
    booleans_match = all(truthy(row.get(field)) for field in boolean_fields)
    provenance = bool(
        text_field(row, "certificate_sha256", "certificate_artifact_sha256")
    )
    passed = rank_fields_match and booleans_match and provenance
    if passed:
        return True, "accepted_exact_reversible_transport_certificate"
    failed_parts: List[str] = []
    if not rank_fields_match:
        failed_parts.append("rank_or_dimension")
    if not booleans_match:
        failed_parts.append("reversal_backtrack_or_gauge")
    if not provenance:
        failed_parts.append("provenance")
    return False, "failed:" + ",".join(failed_parts)


def audit_triangles(
    triangles: Sequence[Triangle],
    final_rows: Sequence[Mapping[str, object]],
    certificates: Mapping[CertificateKey, Mapping[str, object]],
) -> Tuple[List[dict], List[dict], List[dict], List[dict]]:
    exact_groups = grouped_rows(final_rows, "exact_primitive_type_hash")
    coarse_groups = grouped_rows(final_rows, "coarse_primitive_type_hash")
    triangle_rows: List[dict] = []
    candidate_rows: List[dict] = []
    coarse_rows: List[dict] = []
    requirement_rows: List[dict] = []

    for triangle_index, triangle in enumerate(triangles):
        vertex_sets_exact = [
            {
                type_hash
                for type_hash, by_vertex in exact_groups.items()
                if vertex in by_vertex
            }
            for vertex in triangle
        ]
        exact_common = set.intersection(*vertex_sets_exact)
        vertex_sets_coarse = [
            {
                type_hash
                for type_hash, by_vertex in coarse_groups.items()
                if vertex in by_vertex
            }
            for vertex in triangle
        ]
        coarse_common = set.intersection(*vertex_sets_coarse)
        constant_candidates = 0
        transport_admissible_candidates = 0

        for type_hash in sorted(exact_common):
            by_vertex = exact_groups[type_hash]
            multiplicities = [len(by_vertex[vertex]) for vertex in triangle]
            dimensions = {
                integer(row, "primitive_dimension")
                for vertex in triangle
                for row in by_vertex[vertex]
            }
            literal_groups = {
                text_field(row, "literal_group_hash")
                for vertex in triangle
                for row in by_vertex[vertex]
            }
            all_certified = all(
                truthy(row.get("rational_irreducible_certified"))
                for vertex in triangle
                for row in by_vertex[vertex]
            )
            same_dimension = len(dimensions) == 1
            same_literal_group = len(literal_groups) == 1
            constant_multiplicity = len(set(multiplicities)) == 1
            persistence_exact = (
                all_certified
                and same_dimension
                and same_literal_group
                and constant_multiplicity
            )
            primitive_dimension = next(iter(dimensions)) if same_dimension else 0
            subbundle_rank = (
                primitive_dimension * multiplicities[0]
                if persistence_exact
                else 0
            )
            edge_statuses: List[str] = []
            edge_passes: List[bool] = []
            for edge_index, edge in enumerate(triangle_edges(triangle)):
                key = (type_hash, edge, subbundle_rank)
                certificate = certificates.get(key) if persistence_exact else None
                passed, status = (
                    certificate_exact(
                        certificate, expected_rank=subbundle_rank
                    )
                    if persistence_exact
                    else (False, "persistence_gate_failed")
                )
                edge_passes.append(passed)
                edge_statuses.append(status)
                requirement_rows.append({
                    "triangle_index": triangle_index,
                    "exact_primitive_type_hash": type_hash,
                    "edge_index": edge_index,
                    "source_subset": subset_text(edge[0]),
                    "target_subset": subset_text(edge[1]),
                    "expected_subbundle_rank": subbundle_rank,
                    "exact_persistence_prerequisite": persistence_exact,
                    "certificate_present": certificate is not None,
                    "certificate_accepted": passed,
                    "certificate_status": status,
                })
            transport_admissible = persistence_exact and all(edge_passes)
            constant_candidates += int(persistence_exact)
            transport_admissible_candidates += int(transport_admissible)
            candidate_rows.append({
                "triangle_index": triangle_index,
                "triangle": ";".join(subset_text(vertex) for vertex in triangle),
                "exact_primitive_type_hash": type_hash,
                "primitive_dimension": (
                    primitive_dimension if same_dimension else ""
                ),
                "multiplicity_profile": ";".join(map(str, multiplicities)),
                "constant_multiplicity": constant_multiplicity,
                "subbundle_rank": subbundle_rank,
                "all_blocks_rationally_irreducible_certified": all_certified,
                "same_literal_group_exact": same_literal_group,
                "exact_primitive_persistence": persistence_exact,
                "accepted_edge_transport_certificates": sum(edge_passes),
                "required_edge_transport_certificates": 3,
                "transport_admissible_triangle": transport_admissible,
                "holonomy_matrix_computed": False,
                "status": (
                    "transport_admissible_no_holonomy_computed"
                    if transport_admissible
                    else (
                        "exact_persistence_transport_certificates_missing_or_failed"
                        if persistence_exact
                        else "primitive_persistence_gate_failed"
                    )
                ),
                "members_by_vertex": "|".join(
                    f"{subset_text(vertex)}:"
                    + ",".join(occurrence_id(row) for row in by_vertex[vertex])
                    for vertex in triangle
                ),
                "edge_certificate_statuses": ";".join(edge_statuses),
            })

        exact_coarse_hashes = {
            text_field(row, "coarse_primitive_type_hash")
            for type_hash in exact_common
            for vertex in triangle
            for row in exact_groups[type_hash][vertex]
        }
        coarse_only = sorted(coarse_common - exact_coarse_hashes)
        for coarse_hash in coarse_only:
            by_vertex = coarse_groups[coarse_hash]
            exact_hashes = {
                text_field(row, "exact_primitive_type_hash")
                for vertex in triangle
                for row in by_vertex[vertex]
            }
            dimensions = {
                integer(row, "primitive_dimension")
                for vertex in triangle
                for row in by_vertex[vertex]
            }
            coarse_rows.append({
                "triangle_index": triangle_index,
                "triangle": ";".join(subset_text(vertex) for vertex in triangle),
                "coarse_primitive_type_hash": coarse_hash,
                "primitive_dimensions": ";".join(map(str, sorted(dimensions))),
                "distinct_exact_type_hashes": len(exact_hashes),
                "exact_type_hashes": ";".join(sorted(exact_hashes)),
                "candidate_only": True,
                "transport_admissible_triangle": False,
                "reason": (
                    "coarse_cross_group_recurrence_is_not_a_certified_"
                    "cross_channel_module_isomorphism"
                ),
            })

        triangle_rows.append({
            "triangle_index": triangle_index,
            "triangle": ";".join(subset_text(vertex) for vertex in triangle),
            "exact_common_primitive_type_count": len(exact_common),
            "constant_multiplicity_exact_persistence_count": constant_candidates,
            "coarse_only_common_type_count": len(coarse_only),
            "transport_admissible_subbundle_count": (
                transport_admissible_candidates
            ),
            "triangle_supports_exact_persistent_subbundle": (
                constant_candidates > 0
            ),
            "triangle_transport_admissible": (
                transport_admissible_candidates > 0
            ),
            "holonomy_matrix_computed": False,
        })

    return triangle_rows, candidate_rows, coarse_rows, requirement_rows


def markdown_report(
    summary: Mapping[str, object],
    triangle_rows: Sequence[Mapping[str, object]],
    candidate_rows: Sequence[Mapping[str, object]],
    checks: Mapping[str, bool],
) -> str:
    counts = summary["counts"]  # type: ignore[index]
    scientific = summary["scientific_conclusion"]  # type: ignore[index]
    lines = [
        "# EHF-XBR-05B: Primitive Null-Subbundle Persistence and Triangle Admissibility Audit",
        "",
        f"Integrity verdict: `{summary['verdict']}`",
        "",
        f"Scientific outcome: `{scientific['status']}`",  # type: ignore[index]
        "",
        "## Definition lock",
        "",
        "- Primitive identity is exact only when the F8/F8B exact primitive type hash matches. "
        "That hash includes the literal acting-group identity and the primitive character.",
        "- Equal dimension or a coarse order/trace signature is candidate evidence only.",
        "- A triangle is transport-admissible only when one exact type persists with constant "
        "multiplicity and all three edges carry accepted reversible, gauge-covariant comparison certificates.",
        "- No loop product or holonomy matrix is computed in this probe.",
        "",
        "## Census",
        "",
        f"- final certified primitive blocks: {counts['final_primitive_blocks']}",  # type: ignore[index]
        f"- minimal triangles audited: {counts['triangles']}",  # type: ignore[index]
        f"- exact persistent subbundle candidates: {counts['exact_persistence_candidates']}",  # type: ignore[index]
        f"- triangles with exact persistence: {counts['triangles_with_exact_persistence']}",  # type: ignore[index]
        f"- coarse-only triangle candidates: {counts['coarse_only_triangle_candidates']}",  # type: ignore[index]
        f"- transport-admissible subbundles: {counts['transport_admissible_subbundles']}",  # type: ignore[index]
        f"- transport-admissible triangles: {counts['transport_admissible_triangles']}",  # type: ignore[index]
        "",
        "## Triangle summary",
        "",
        "| triangle | exact common types | constant-rank persistence | coarse only | transport admissible |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in triangle_rows:
        lines.append(
            f"| {row['triangle']} | {row['exact_common_primitive_type_count']} | "
            f"{row['constant_multiplicity_exact_persistence_count']} | "
            f"{row['coarse_only_common_type_count']} | "
            f"{row['transport_admissible_subbundle_count']} |"
        )
    lines.extend([
        "",
        "## Exact persistence candidates",
        "",
    ])
    if candidate_rows:
        lines.extend([
            "| triangle | dimension | multiplicity | rank | exact persistence | accepted edges | transport admissible |",
            "|---|---:|---|---:|---|---:|---|",
        ])
        for row in candidate_rows:
            lines.append(
                f"| {row['triangle']} | {row['primitive_dimension']} | "
                f"{row['multiplicity_profile']} | {row['subbundle_rank']} | "
                f"{row['exact_primitive_persistence']} | "
                f"{row['accepted_edge_transport_certificates']}/3 | "
                f"{row['transport_admissible_triangle']} |"
            )
    else:
        lines.append("No exact primitive type occurs at all three vertices of a minimal triangle.")
    lines.extend([
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
        str(summary["claim_boundary"]),
        "",
    ])
    return "\n".join(lines)


def self_test() -> None:
    assert parse_subset("2,3,4") == (2, 3, 4)
    assert parse_subset("(4, 2, 3)") == (2, 3, 4)
    assert parse_subset("[3, 4, 2]") == (2, 3, 4)
    for invalid_subset in ("(2, 3)", "(2, 3, 3)", "(1, 2, 3)", "(2, 3, 9)"):
        try:
            parse_subset(invalid_subset)
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"invalid subset unexpectedly accepted: {invalid_subset!r}"
            )

    triangle: Triangle = ((2, 3, 4), (2, 3, 5), (2, 4, 5))
    rows: List[dict] = []
    for vertex in triangle:
        rows.append({
            "subset": subset_text(vertex),
            "sector_index": 0,
            "final_primitive_index": "p0",
            "primitive_dimension": 2,
            "rational_irreducible_certified": True,
            "literal_group_hash": "literal-g",
            "exact_primitive_type_hash": "exact-t",
            "coarse_primitive_type_hash": "coarse-t",
        })
    triangle_rows, candidates, _, requirements = audit_triangles(
        [triangle], rows, {}
    )
    assert triangle_rows[0]["triangle_supports_exact_persistent_subbundle"]
    assert not triangle_rows[0]["triangle_transport_admissible"]
    assert candidates[0]["subbundle_rank"] == 2
    assert len(requirements) == 3

    certificates: Dict[CertificateKey, dict] = {}
    for edge in triangle_edges(triangle):
        certificates[("exact-t", edge, 2)] = {
            "subbundle_rank": 2,
            "source_subbundle_dimension": 2,
            "target_subbundle_dimension": 2,
            "forward_rank": 2,
            "reverse_rank": 2,
            "canonical_comparison_defined": True,
            "forward_reverse_identity_exact": True,
            "reverse_forward_identity_exact": True,
            "gauge_covariance_exact": True,
            "strict_pass": True,
            "certificate_sha256": "fixture-certificate",
        }
    triangle_rows, candidates, _, _ = audit_triangles(
        [triangle], rows, certificates
    )
    assert triangle_rows[0]["triangle_transport_admissible"]
    assert candidates[0]["accepted_edge_transport_certificates"] == 3

    f8_rows = [
        {
            "subset": "(2, 3, 4)",
            "regime": "fixture",
            "sector_index": 0,
            "primitive_index": 0,
            "primitive_dimension": 1,
            "rational_irreducible_certified": True,
            "absolutely_irreducible_certified": True,
            "primitive_commutant_dimension": 1,
            "literal_group_hash": "g",
            "exact_primitive_type_hash": "t",
            "coarse_primitive_type_hash": "c",
            "primitive_basis_sha256": "b0",
            "certification_kind": "fixture",
        },
        {
            "subset": "(2, 3, 4)",
            "regime": "fixture",
            "sector_index": 0,
            "primitive_index": 1,
            "primitive_dimension": 2,
            "rational_irreducible_certified": False,
            "absolutely_irreducible_certified": False,
            "primitive_commutant_dimension": 4,
            "literal_group_hash": "g",
            "exact_primitive_type_hash": "u",
            "coarse_primitive_type_hash": "d",
            "primitive_basis_sha256": "b1",
            "certification_kind": "fixture",
        },
    ]
    classification = [{
        "subset": "(2, 3, 4)",
        "sector_index": 0,
        "source_primitive_index": 1,
        "sibling_primitive_index": 0,
        "resolved_block_count": 2,
        "algebra_classification": "split_matrix_algebra_M2_Q",
        "child_characters_equal_sibling": True,
        "child_modules_isomorphic_to_sibling": True,
        "outcome_certificate_complete": True,
    }]
    resolved = [
        {
            "subset": "(2, 3, 4)",
            "sector_index": 0,
            "source_primitive_index": 1,
            "resolved_primitive_index": index,
            "resolved_dimension": 1,
            "rational_irreducible_certified": True,
            "absolutely_irreducible_certified": True,
            "commutant_dimension": 1,
            "character_equals_certified_sibling": True,
            "full_rank_sibling_isomorphism_found": True,
            "resolved_basis_sha256": f"child-{index}",
            "certification_kind": "fixture_child",
        }
        for index in range(2)
    ]
    final, diagnostics = reconstruct_final_primitives(
        f8_rows, classification, resolved
    )
    assert len(final) == 3
    assert diagnostics["f8_residual_blocks_replaced"] == 1
    assert all(row["exact_primitive_type_hash"] == "t" for row in final)
    print("EHF-XBR-05B self-test PASS")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit exact primitive null-subbundle persistence and minimal-"
            "triangle transport admissibility."
        )
    )
    parser.add_argument("--xbr05a-dir")
    parser.add_argument("--xbr04f8-dir")
    parser.add_argument("--xbr04f8b-dir")
    parser.add_argument("--transport-certificate-ledger")
    parser.add_argument("--out-dir", default="runs/ehf_xbr_05b")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    required_arguments = ("xbr05a_dir", "xbr04f8_dir", "xbr04f8b_dir")
    missing = [
        name for name in required_arguments if not getattr(args, name)
    ]
    if missing:
        parser.error(
            "missing required arguments: " + ", ".join(missing)
        )

    xbr05a_dir = Path(args.xbr05a_dir).resolve()
    f8_dir = Path(args.xbr04f8_dir).resolve()
    f8b_dir = Path(args.xbr04f8b_dir).resolve()
    certificate_path = (
        Path(args.transport_certificate_ledger).resolve()
        if args.transport_certificate_ledger
        else None
    )
    out_dir = Path(args.out_dir).resolve()

    paths = {
        "xbr05a_summary": xbr05a_dir / "run_summary.json",
        "xbr05a_vertices": xbr05a_dir / "null_channel_vertex_ledger.csv",
        "xbr05a_triangles": xbr05a_dir / "minimal_loop_ledger.csv",
        "f8_summary": f8_dir / "run_summary.json",
        "f8_primitives": f8_dir / "primitive_module_ledger.csv",
        "f8b_summary": f8b_dir / "run_summary.json",
        "f8b_classifications": (
            f8b_dir / "residual_commutant_classification_ledger.csv"
        ),
        "f8b_resolved": f8b_dir / "resolved_primitive_module_ledger.csv",
    }
    for path in paths.values():
        if not path.exists():
            raise FileNotFoundError(path)
    if certificate_path is not None and not certificate_path.exists():
        raise FileNotFoundError(certificate_path)

    xbr05a_summary = read_json(paths["xbr05a_summary"])
    vertex_rows = read_csv(paths["xbr05a_vertices"])
    loop_rows = read_csv(paths["xbr05a_triangles"])
    f8_summary = read_json(paths["f8_summary"])
    f8_rows = read_csv(paths["f8_primitives"])
    f8b_summary = read_json(paths["f8b_summary"])
    classification_rows = read_csv(paths["f8b_classifications"])
    resolved_rows = read_csv(paths["f8b_resolved"])

    vertices = {
        parse_subset(row["subset"]): integer(row, "kernel_dimension")
        for row in vertex_rows
    }
    triangles = sorted({
        parse_loop_word(row["loop_word"])
        for row in loop_rows
        if integer(row, "length") == 3
    })
    final_rows, merge_diagnostics = reconstruct_final_primitives(
        f8_rows, classification_rows, resolved_rows
    )
    certificates, certificate_diagnostics = load_transport_certificates(
        certificate_path
    )
    (
        triangle_rows,
        candidate_rows,
        coarse_rows,
        requirement_rows,
    ) = audit_triangles(triangles, final_rows, certificates)

    by_vertex: Dict[Subset, List[dict]] = defaultdict(list)
    for row in final_rows:
        by_vertex[parse_subset(row["subset"])].append(row)
    channel_dimension_sums = {
        vertex: sum(
            integer(row, "primitive_dimension")
            for row in by_vertex.get(vertex, [])
        )
        for vertex in vertices
    }
    exact_groups = grouped_rows(final_rows, "exact_primitive_type_hash")
    persistence_rows = persistence_ledger(exact_groups)
    literal_groups_per_exact_hash = {
        type_hash: {
            text_field(row, "literal_group_hash")
            for values in by_channel.values()
            for row in values
        }
        for type_hash, by_channel in exact_groups.items()
    }
    dimensions_per_exact_hash = {
        type_hash: {
            integer(row, "primitive_dimension")
            for values in by_channel.values()
            for row in values
        }
        for type_hash, by_channel in exact_groups.items()
    }
    commutants_per_exact_hash = {
        type_hash: {
            integer(row, "commutant_dimension")
            for values in by_channel.values()
            for row in values
        }
        for type_hash, by_channel in exact_groups.items()
    }

    exact_persistence_candidates = sum(
        truthy(row["exact_primitive_persistence"]) for row in candidate_rows
    )
    triangles_with_exact_persistence = sum(
        truthy(row["triangle_supports_exact_persistent_subbundle"])
        for row in triangle_rows
    )
    transport_admissible_subbundles = sum(
        truthy(row["transport_admissible_triangle"])
        for row in candidate_rows
    )
    transport_admissible_triangles = sum(
        truthy(row["triangle_transport_admissible"])
        for row in triangle_rows
    )
    coarse_only_candidates = len(coarse_rows)

    expected_final_count = integer(
        f8b_summary.get("counts", {}),
        "final_terminal_primitive_blocks",
    )
    expected_certified_count = integer(
        f8b_summary.get("counts", {}),
        "final_certified_primitive_blocks",
    )
    checks = {
        "source_xbr05a_strict_pass": truthy(
            xbr05a_summary.get("strict_pass")
        ),
        "source_xbr04f8_strict_pass": truthy(f8_summary.get("strict_pass")),
        "source_xbr04f8b_strict_pass": truthy(f8b_summary.get("strict_pass")),
        "eleven_null_channel_vertices_loaded": len(vertices) == 11,
        "twenty_four_unique_minimal_triangles_loaded": len(triangles) == 24,
        "all_triangle_vertices_are_null_channels": all(
            vertex in vertices for triangle in triangles for vertex in triangle
        ),
        "f8b_resolutions_replace_every_f8_residual_block": (
            not merge_diagnostics["type_inheritance_failures"]
            and merge_diagnostics["f8_residual_blocks_replaced"]
            == len(classification_rows)
        ),
        "final_primitive_count_matches_xbr04f8b": (
            len(final_rows) == expected_final_count
        ),
        "final_certified_count_matches_xbr04f8b": (
            sum(
                truthy(row["rational_irreducible_certified"])
                for row in final_rows
            )
            == expected_certified_count
        ),
        "all_final_primitives_certified": all(
            truthy(row["rational_irreducible_certified"])
            for row in final_rows
        ),
        "all_final_primitives_have_exact_and_coarse_type_hashes": all(
            text_field(row, "exact_primitive_type_hash")
            and text_field(row, "coarse_primitive_type_hash")
            and text_field(row, "literal_group_hash")
            for row in final_rows
        ),
        "per_channel_primitive_dimensions_reconstruct_null_fibers": all(
            channel_dimension_sums[vertex] == vertices[vertex]
            for vertex in vertices
        ),
        "final_primitive_dimensions_sum_to_216": sum(
            integer(row, "primitive_dimension") for row in final_rows
        )
        == 216,
        "exact_type_hash_never_crosses_literal_group_identity": all(
            len(groups) == 1
            for groups in literal_groups_per_exact_hash.values()
        ),
        "exact_type_hash_has_unique_dimension_and_commutant": all(
            len(dimensions_per_exact_hash[type_hash]) == 1
            and len(commutants_per_exact_hash[type_hash]) == 1
            for type_hash in exact_groups
        ),
        "all_twenty_four_triangles_audited_once": (
            len(triangle_rows) == 24
            and len({int(row["triangle_index"]) for row in triangle_rows})
            == 24
        ),
        "transport_certificate_ledger_schema_valid": (
            certificate_diagnostics["duplicate_keys"] == 0
            and not certificate_diagnostics["schema_errors"]
        ),
        "no_coarse_candidate_promoted_to_exact_persistence": all(
            not truthy(row["transport_admissible_triangle"])
            for row in coarse_rows
        ),
        "transport_admissibility_requires_three_exact_edge_certificates": all(
            (
                not truthy(row["transport_admissible_triangle"])
                or (
                    truthy(row["exact_primitive_persistence"])
                    and integer(
                        row, "accepted_edge_transport_certificates"
                    )
                    == 3
                )
            )
            for row in candidate_rows
        ),
        "no_holonomy_matrix_computed": all(
            not truthy(row["holonomy_matrix_computed"])
            for row in (*triangle_rows, *candidate_rows)
        ),
    }
    strict_pass = all(checks.values())
    verdict = (
        VERDICT_PASS
        if strict_pass
        else "EHF_XBR_05B_INTEGRITY_CHECK_FAILED"
    )

    if transport_admissible_subbundles:
        scientific_status = "transport_admissible_primitive_triangles_found"
        scientific_reason = (
            "At least one exact constant-rank primitive subbundle has accepted "
            "reversible comparison certificates on all three triangle edges. "
            "A later probe may compute controlled holonomy."
        )
    elif exact_persistence_candidates:
        scientific_status = (
            "exact_primitive_persistence_found_transport_not_certified"
        )
        scientific_reason = (
            "At least one primitive type persists with constant multiplicity "
            "around a minimal triangle, but cross-channel transport is not "
            "yet certified. No holonomy is admissible."
        )
    elif coarse_only_candidates:
        scientific_status = (
            "coarse_triangle_recurrence_only_no_exact_subbundle"
        )
        scientific_reason = (
            "Only coarse cross-group recurrence reaches a triangle. This is "
            "not a certified common module or transportable subbundle."
        )
    else:
        scientific_status = "no_primitive_triangle_persistence"
        scientific_reason = (
            "No exact primitive type persists with constant multiplicity "
            "around any of the 24 minimal triangles."
        )

    counts = {
        "null_channel_vertices": len(vertices),
        "triangles": len(triangles),
        "f8_source_blocks": merge_diagnostics["f8_source_blocks"],
        "f8_residual_blocks_replaced": merge_diagnostics[
            "f8_residual_blocks_replaced"
        ],
        "f8b_resolved_children_added": merge_diagnostics[
            "f8b_resolved_children_added"
        ],
        "final_primitive_blocks": len(final_rows),
        "exact_primitive_types": len(exact_groups),
        "exact_persistence_candidates": exact_persistence_candidates,
        "triangles_with_exact_persistence": triangles_with_exact_persistence,
        "coarse_only_triangle_candidates": coarse_only_candidates,
        "transport_certificate_rows": certificate_diagnostics["rows"],
        "transport_admissible_subbundles": (
            transport_admissible_subbundles
        ),
        "transport_admissible_triangles": transport_admissible_triangles,
    }
    summary = {
        "probe": PROBE_NAME,
        "title": (
            "Primitive Null-Subbundle Persistence and Triangle "
            "Admissibility Audit"
        ),
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "sources": {
            name: {
                "path": str(path),
                "sha256": sha256_file(path),
            }
            for name, path in paths.items()
        },
        "transport_certificate_source": (
            {
                "path": str(certificate_path),
                "sha256": sha256_file(certificate_path),
            }
            if certificate_path is not None
            else None
        ),
        "counts": counts,
        "merge_diagnostics": merge_diagnostics,
        "transport_certificate_diagnostics": certificate_diagnostics,
        "scientific_conclusion": {
            "status": scientific_status,
            "reason": scientific_reason,
            "holonomy_computed": False,
            "next_gate": (
                "If exact persistence exists, construct canonical cross-channel "
                "intertwiners and certify reversal, immediate backtracks, and "
                "gauge covariance. Only then compute triangle holonomy."
                if not transport_admissible_subbundles
                else
                "Compute the first controlled loop products with gauge, "
                "reversal, re-rooting, and symmetry controls."
            ),
        },
        "checks": checks,
        "strict_pass": strict_pass,
        "verdict": verdict,
        "claim_boundary": (
            "Exact finite n=9 primitive-module persistence and transport-"
            "admissibility result only. Matching coarse signatures are not "
            "module isomorphisms; exact persistence is not itself a connection; "
            "no physical interpretation or holonomy matrix is asserted."
        ),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "final_primitive_module_ledger.csv", final_rows)
    write_csv(
        out_dir / "primitive_type_persistence_ledger.csv",
        persistence_rows,
    )
    write_csv(out_dir / "triangle_persistence_ledger.csv", triangle_rows)
    write_csv(
        out_dir / "exact_triangle_subbundle_candidate_ledger.csv",
        candidate_rows,
        fields_if_empty=(
            "triangle_index",
            "triangle",
            "exact_primitive_type_hash",
            "exact_primitive_persistence",
            "transport_admissible_triangle",
            "holonomy_matrix_computed",
        ),
    )
    write_csv(
        out_dir / "coarse_triangle_candidate_control_ledger.csv",
        coarse_rows,
        fields_if_empty=(
            "triangle_index",
            "triangle",
            "coarse_primitive_type_hash",
            "candidate_only",
            "transport_admissible_triangle",
        ),
    )
    write_csv(
        out_dir / "transport_certificate_requirement_ledger.csv",
        requirement_rows,
        fields_if_empty=(
            "triangle_index",
            "exact_primitive_type_hash",
            "edge_index",
            "source_subset",
            "target_subset",
            "expected_subbundle_rank",
            "certificate_present",
            "certificate_accepted",
        ),
    )
    write_json(out_dir / "run_summary.json", summary)
    (out_dir / "report.md").write_text(
        markdown_report(
            summary, triangle_rows, candidate_rows, checks
        )
    )

    print("=" * 108)
    print(
        "EHF-XBR-05B: PRIMITIVE NULL-SUBBUNDLE PERSISTENCE "
        "AND TRIANGLE ADMISSIBILITY AUDIT"
    )
    print("=" * 108)
    print(f"final certified primitives:       {len(final_rows)}")
    print(f"minimal triangles audited:        {len(triangles)}")
    print(
        f"exact persistence candidates:     "
        f"{exact_persistence_candidates}"
    )
    print(
        f"triangles with exact persistence: "
        f"{triangles_with_exact_persistence}"
    )
    print(f"coarse-only triangle candidates:  {coarse_only_candidates}")
    print(
        f"transport-admissible subbundles:  "
        f"{transport_admissible_subbundles}"
    )
    print(
        f"transport-admissible triangles:   "
        f"{transport_admissible_triangles}"
    )
    print(f"holonomy matrices computed:       0")
    print(f"scientific outcome:               {scientific_status}")
    print(f"strict checks:                    {sum(checks.values())}/{len(checks)}")
    print(f"output directory:                 {out_dir}")
    print(verdict)

    if args.strict and not strict_pass:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
