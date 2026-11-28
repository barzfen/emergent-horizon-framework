#!/usr/bin/env python3
r"""
EHF-AMP-FOUND-03K: Anchor-Change Covariance and Full Fibre-Atlas Closure
========================================================================

The fixed-anchor 9 -> 8 theorem was proved first in the anchor-1 chart. 03K
constructs the complete atlas over every surviving anchor

    a in {1,...,8},

while label 9 remains the deleted leg.

For each anchor a, let rho_a be the canonical anchor-normalisation permutation

    rho_a(a)=1,
    rho_a(9)=9,

with the remaining labels in {1,...,8}\{a} sent increasingly to 2,...,8.
Each anchor chart has 35 active fibres

    E={a,9} union A,
    O={1,...,8}\({a} union A),

where A is a three-subset of the seven surviving non-anchor labels.

The script proves exact column-level covariance for the source KK map and the
delete-9 map:

    Q^(1)_{rho_a(A)} P_a = R_a Q^(a)_A,
    D^(1)_{rho_a(A)} P_a = T_a D^(a)_A.

P_a is a signed source-state permutation. The sign is the odd-point
Parke--Taylor reflection character introduced when an anchor-relative ordering
must be reversed to return to the global anchor-1 canonical representative.
T_a is the corresponding unsigned target-state permutation because the target
multiplicity is even.

Consequently every anchor-a transmitted image is exactly transported to the
anchor-1 image indexed by rho_a(A). After the existing ordered-block transport,
all 8*35=280 channels collapse to the same six subspaces

    V0,V2,V8,V9,V14,V15.

The exact rank law is therefore anchor-covariant: it depends on the two largest
entries of the normalised triple rho_a(A), not on the original numerical anchor.

For anchor transitions

    pi_(b<-a)=rho_b^{-1} rho_a,

the signed source-state maps, unsigned target-state maps, KK row maps, fibre
maps, and transmitted-image maps obey exact cocycle consistency.

Example
-------

caffeinate -i python3 scripts/ehf_amp_found_03k_anchor_change_covariance_full_fibre_atlas.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --lattice-script scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --out-dir runs/ehf_amp_found_03k \
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
from typing import Dict, Iterable, Iterator, List, Mapping, MutableMapping, Sequence, Tuple

import sympy as sp
import numpy as np

Cycle = Tuple[int, ...]
FibreKey = Tuple[Tuple[int, ...], Tuple[int, ...]]
Subset = Tuple[int, int, int]
PermutationMap = Dict[int, int]


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
                seen.add(key)
                fields.append(key)
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


def cycle_text(cycle: Sequence[int]) -> str:
    return ",".join(map(str, cycle))


def subset_text(subset: Sequence[int]) -> str:
    return ",".join(map(str, subset))


def mapping_text(mapping: Mapping[int, int]) -> str:
    return ";".join(f"{source}->{target}" for source, target in sorted(mapping.items()))


def anchor_representative_info(
    cycle: Sequence[int],
    anchor: int,
) -> Tuple[Cycle, int, bool]:
    """Return anchor-relative canonical representative and PT orientation sign.

    The sign s is defined by

        PT(global canonical cycle) = s * PT(anchor-relative representative).
    """
    c = tuple(cycle)
    position = c.index(anchor)
    rotated = c[position:] + c[:position]
    reversed_cycle = (anchor,) + rotated[:0:-1]
    if rotated <= reversed_cycle:
        return rotated, 1, False
    sign = -1 if len(c) % 2 else 1
    return reversed_cycle, sign, True


def anchor_fibre_key(cycle: Sequence[int], anchor: int) -> FibreKey:
    representative, _, _ = anchor_representative_info(cycle, anchor)
    return (
        tuple(sorted(representative[0::2])),
        tuple(sorted(representative[1::2])),
    )


def anchor_fibres(
    cycles: Sequence[Cycle],
    anchor: int,
) -> Dict[FibreKey, List[Cycle]]:
    grouped: MutableMapping[FibreKey, List[Cycle]] = defaultdict(list)
    for cycle in cycles:
        grouped[anchor_fibre_key(cycle, anchor)].append(cycle)
    return {
        key: sorted(values)
        for key, values in sorted(grouped.items(), key=lambda item: item[0])
    }


def anchor_normalisation(anchor: int) -> PermutationMap:
    remaining = [label for label in range(1, 9) if label != anchor]
    mapping: PermutationMap = {anchor: 1, 9: 9}
    mapping.update(dict(zip(remaining, range(2, 9))))
    return mapping


def invert_mapping(mapping: Mapping[int, int]) -> PermutationMap:
    return {target: source for source, target in mapping.items()}


def compose_mapping(
    left: Mapping[int, int],
    right: Mapping[int, int],
) -> PermutationMap:
    """Return left after right."""
    return {label: left[right[label]] for label in right}


def relabel_canonical_with_sign(
    cycle: Sequence[int],
    mapping: Mapping[int, int],
) -> Tuple[Cycle, int, bool]:
    """Relabel and return global anchor-1 representative with PT sign."""
    relabelled = tuple(mapping[label] for label in cycle)
    position = relabelled.index(1)
    rotated = relabelled[position:] + relabelled[:position]
    reversed_cycle = (1,) + rotated[:0:-1]
    if rotated <= reversed_cycle:
        return rotated, 1, False
    sign = -1 if len(cycle) % 2 else 1
    return reversed_cycle, sign, True


def kk_expansion(
    direct_module,
    cycle: Sequence[int],
    n: int,
    anchor: int,
    endpoint: int,
) -> Dict[Tuple[int, ...], int]:
    """Exact KK expansion of the global PT state in basis (anchor,sigma,endpoint)."""
    representative, orientation_sign, _ = anchor_representative_info(cycle, anchor)
    position = representative.index(endpoint)
    alpha = representative[1:position]
    beta = representative[position + 1 :]
    shuffle_sign = -1 if len(beta) % 2 else 1
    coefficient = orientation_sign * shuffle_sign
    output: Dict[Tuple[int, ...], int] = {}
    for sigma in direct_module.shuffles(alpha, tuple(reversed(beta))):
        output[sigma] = output.get(sigma, 0) + coefficient
    return output


def mapped_expansion(
    expansion: Mapping[Tuple[int, ...], int],
    mapping: Mapping[int, int],
) -> Dict[Tuple[int, ...], int]:
    return {
        tuple(mapping[label] for label in sigma): coefficient
        for sigma, coefficient in expansion.items()
    }


def delete_nine_at_anchor(
    base,
    cycle: Sequence[int],
    anchor: int,
) -> Tuple[int, Cycle] | None:
    """Exact signed delete-9 map in an arbitrary surviving-anchor chart."""
    representative, orientation_sign, _ = anchor_representative_info(cycle, anchor)
    if representative[1] == 9:
        side_sign = 1
        reduced = (anchor,) + representative[2:]
    elif representative[-1] == 9:
        side_sign = -1
        reduced = representative[:-1]
    else:
        return None
    # The target multiplicity is even, so global reflection canonicalisation
    # contributes no additional Parke--Taylor sign.
    target = base.canon(reduced)
    return orientation_sign * side_sign, target


def source_key(anchor: int, subset: Subset) -> FibreKey:
    selected = set(subset)
    even = tuple(sorted((anchor, 9) + tuple(subset)))
    odd = tuple(
        label
        for label in range(1, 9)
        if label != anchor and label not in selected
    )
    return even, odd


def target_key(anchor: int, subset: Subset) -> FibreKey:
    selected = set(subset)
    even = tuple(sorted((anchor,) + tuple(subset)))
    odd = tuple(
        label
        for label in range(1, 9)
        if label != anchor and label not in selected
    )
    return even, odd


def rank_multiplicity_text(counter: Mapping[int, int]) -> str:
    return ";".join(f"{rank}:{counter[rank]}" for rank in sorted(counter))


def write_markdown(
    path: Path,
    anchor_rows: Sequence[Mapping[str, object]],
    class_rows: Sequence[Mapping[str, object]],
) -> None:
    lines = [
        "# EHF-AMP-FOUND-03K",
        "## Anchor-change covariance and full fibre-atlas closure",
        "",
        "For every surviving anchor `a=1,...,8`, define the canonical normalisation",
        "",
        r"\[\rho_a(a)=1,\qquad \rho_a(9)=9,\]",
        "",
        "with the remaining surviving labels mapped increasingly to `2,...,8`.",
        "The exact source KK and delete maps obey",
        "",
        r"\[Q^{(1)}_{\rho_a(A)}P_a=R_aQ^{(a)}_A,\]",
        "",
        r"\[D^{(1)}_{\rho_a(A)}P_a=T_aD^{(a)}_A.\]",
        "",
        "## Anchor census",
        "",
        "| Anchor | Channels | Active source incidences | Rank multiplicities | All covariance checks |",
        "|---:|---:|---:|---|---|",
    ]
    for row in anchor_rows:
        lines.append(
            f"| {row['anchor']} | {row['channel_count']} | "
            f"{row['active_source_state_count']} | "
            f"`{row['rank_multiplicities']}` | "
            f"{'yes' if row['all_channel_covariance_exact'] else 'no'} |"
        )
    lines.extend([
        "",
        "## Six common transported subspaces",
        "",
        "| Class | Rank | Channels per anchor | Channels in full atlas |",
        "|---|---:|---:|---:|",
    ])
    for row in class_rows:
        lines.append(
            f"| {row['space_name']} | {row['rank']} | "
            f"{row['count_per_anchor']} | {row['count_full_atlas']} |"
        )
    lines.extend([
        "",
        "The 280 anchor-relative channels therefore collapse, after exact anchor "
        "normalisation and ordered-block transport, to the same six spaces",
        "",
        r"\[V_0,V_2,V_8,V_9,V_{14},V_{15}.\]",
        "",
        "The anchor transition maps satisfy exact state, KK-row, fibre, and image "
        "cocycles. The atlas is closed over all eight surviving anchors.",
        "",
    ])
    path.write_text("\n".join(lines))


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()

    base_script = Path(args.base_script).resolve()
    helper_script = Path(args.helper_script).resolve()
    rank_script = Path(args.rank_script).resolve()
    lattice_script = Path(args.lattice_script).resolve()
    direct_script = Path(args.direct_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_03k_base")
    helper = load_module(helper_script, "ehf_amp_found_03k_helper")
    rank_module = load_module(rank_script, "ehf_amp_found_03k_rank")
    lattice = load_module(lattice_script, "ehf_amp_found_03k_lattice")
    direct = load_module(direct_script, "ehf_amp_found_03k_direct")

    source_cycles: List[Cycle] = base.canonical_cycles(9)
    target_cycles: List[Cycle] = base.canonical_cycles(8)
    reference_source_fibres = base.fibres(9)
    reference_target_fibres = base.fibres(8)
    reference_subset: Subset = (2, 3, 4)
    reference_states = reference_target_fibres[
        rank_module.key_from_subset_8(reference_subset)
    ]

    kk9_permutations = list(itertools.permutations(range(2, 9)))
    kk9_index = {
        permutation: index
        for index, permutation in enumerate(kk9_permutations)
    }

    print("=" * 126)
    print("EHF-AMP-FOUND-03K: ANCHOR-CHANGE COVARIANCE AND FULL FIBRE-ATLAS CLOSURE")
    print("=" * 126)
    print(f"base script:                 {base_script}")
    print(f"reflection-aware helper:     {helper_script}")
    print(f"exact rank helper:           {rank_script}")
    print(f"exact lattice helper:        {lattice_script}")
    print(f"exact KK helper:             {direct_script}")
    print(f"output directory:            {out_dir}")
    print("surviving anchors:           {1,2,3,4,5,6,7,8}")
    print("deleted label:               9")
    print("coefficient domain:          QQ")

    # ------------------------------------------------------------------
    # Reference exact images and six-space lattice.
    # ------------------------------------------------------------------
    reference_images: Dict[Subset, sp.Matrix] = {}
    reference_metadata: Dict[Subset, Dict[str, object]] = {}
    class_spaces: MutableMapping[str, List[sp.Matrix]] = defaultdict(list)

    for subset in itertools.combinations(range(2, 9), 3):
        image, metadata = lattice.exact_channel_image(
            base,
            helper,
            rank_module,
            subset,
            reference_source_fibres,
            reference_target_fibres,
            kk9_index,
        )
        destination, _ = lattice.canonical_target_transport(
            base,
            rank_module,
            subset,
            reference_target_fibres,
            reference_subset,
            reference_states,
        )
        transported = lattice.transport_rows(image, destination)
        reference_images[subset] = transported
        reference_metadata[subset] = metadata
        class_spaces[rank_module.rank_class_name(subset)].append(transported)

    equal_within_class = all(
        all(space == spaces[0] for space in spaces)
        for spaces in class_spaces.values()
    )
    distinct_reference_spaces = {
        str(space.tolist())
        for space in reference_images.values()
    }

    class_name_to_space_name = {
        "B_LE_4_C_LE_5": "V0",
        "B_LE_4_C_EQ_6": "V2",
        "B_EQ_5_C_EQ_6": "V8",
        "B_LE_4_C_GE_7": "V9",
        "B_EQ_5_C_GE_7": "V14",
        "B_GE_6": "V15",
    }
    space_by_name = {
        class_name_to_space_name[class_name]: spaces[0]
        for class_name, spaces in class_spaces.items()
    }
    v3 = lattice.intersection_basis(space_by_name["V8"], space_by_name["V9"])
    lattice_exact = (
        space_by_name["V0"].rows == 0
        and lattice.is_subspace(space_by_name["V2"], v3)
        and v3.rows == 3
        and lattice.rowspace_sum(space_by_name["V8"], space_by_name["V9"])
        == space_by_name["V14"]
        and space_by_name["V15"].rows == 15
    )

    # ------------------------------------------------------------------
    # All eight anchor charts and all 280 channels.
    # ------------------------------------------------------------------
    channel_rows: List[Dict[str, object]] = []
    anchor_rows: List[Dict[str, object]] = []
    global_rank_counter: Counter[int] = Counter()

    all_source_bijections = True
    all_target_bijections = True
    all_kk_covariance = True
    all_delete_covariance = True
    all_diagonal_targets = True
    all_two_preimage_counts = True
    all_active_counts = True
    all_rank_laws = True
    all_transported_spaces = True

    normalisations = {
        anchor: anchor_normalisation(anchor)
        for anchor in range(1, 9)
    }

    for anchor in range(1, 9):
        anchor_started = time.time()
        source_fibres = anchor_fibres(source_cycles, anchor)
        target_fibres = anchor_fibres(target_cycles, anchor)
        rho = normalisations[anchor]
        labels = [label for label in range(1, 9) if label != anchor]

        anchor_rank_counter: Counter[int] = Counter()
        active_source_count = 0
        source_reversal_count = 0
        anchor_exact = True

        for channel_index, subset in enumerate(itertools.combinations(labels, 3)):
            subset = tuple(subset)  # type: ignore[assignment]
            source_chamber = source_fibres[source_key(anchor, subset)]
            target_chamber = target_fibres[target_key(anchor, subset)]
            normalised_subset: Subset = tuple(
                sorted(rho[label] for label in subset)
            )  # type: ignore[assignment]
            reference_source = reference_source_fibres[
                rank_module.key_from_subset_9(normalised_subset)
            ]
            reference_target = reference_target_fibres[
                rank_module.key_from_subset_8(normalised_subset)
            ]

            source_images: List[Cycle] = []
            source_signed_images: List[Tuple[Cycle, int]] = []
            target_images: List[Cycle] = []
            preimage_counter: Counter[Cycle] = Counter()

            channel_kk_exact = True
            channel_delete_exact = True
            channel_target_exact = True
            active_count = 0

            for cycle in source_chamber:
                normalised_cycle, source_sign, reversed_orientation = (
                    relabel_canonical_with_sign(cycle, rho)
                )
                source_images.append(normalised_cycle)
                source_signed_images.append((normalised_cycle, source_sign))
                source_reversal_count += int(reversed_orientation)

                anchor_expansion = kk_expansion(
                    direct,
                    cycle,
                    9,
                    anchor,
                    9,
                )
                reference_expansion = kk_expansion(
                    direct,
                    normalised_cycle,
                    9,
                    1,
                    9,
                )
                mapped = mapped_expansion(anchor_expansion, rho)
                expected = {
                    sigma: source_sign * coefficient
                    for sigma, coefficient in reference_expansion.items()
                }
                if mapped != expected:
                    channel_kk_exact = False

                deletion = delete_nine_at_anchor(base, cycle, anchor)
                reference_deletion = delete_nine_at_anchor(
                    base,
                    normalised_cycle,
                    1,
                )
                if (deletion is None) != (reference_deletion is None):
                    channel_delete_exact = False
                    continue
                if deletion is None:
                    continue

                active_count += 1
                coefficient, target = deletion
                reference_coefficient, reference_target_state = reference_deletion
                normalised_target, target_sign, _ = relabel_canonical_with_sign(
                    target,
                    rho,
                )
                if target_sign != 1:
                    channel_delete_exact = False
                if (
                    normalised_target != reference_target_state
                    or coefficient != source_sign * reference_coefficient
                ):
                    channel_delete_exact = False
                if target not in target_chamber:
                    channel_target_exact = False
                preimage_counter[target] += 1

            for target in target_chamber:
                normalised_target, target_sign, _ = relabel_canonical_with_sign(
                    target,
                    rho,
                )
                if target_sign != 1:
                    channel_target_exact = False
                target_images.append(normalised_target)

            source_bijection = (
                len(source_images) == len(set(source_images))
                and set(source_images) == set(reference_source)
            )
            target_bijection = (
                len(target_images) == len(set(target_images))
                and set(target_images) == set(reference_target)
            )
            diagonal_target = channel_target_exact and set(preimage_counter) == set(target_chamber)
            two_preimages = (
                len(preimage_counter) == len(target_chamber)
                and all(count == 2 for count in preimage_counter.values())
            )
            active_count_exact = active_count == 144

            predicted_rank = rank_module.predicted_rank_from_two_rightmost(
                normalised_subset
            )
            transported = reference_images[normalised_subset]
            rank_exact = transported.rows == predicted_rank
            class_name = rank_module.rank_class_name(normalised_subset)
            space_name = class_name_to_space_name[class_name]
            transported_space_exact = transported == space_by_name[space_name]

            all_source_bijections &= source_bijection
            all_target_bijections &= target_bijection
            all_kk_covariance &= channel_kk_exact
            all_delete_covariance &= channel_delete_exact
            all_diagonal_targets &= diagonal_target
            all_two_preimage_counts &= two_preimages
            all_active_counts &= active_count_exact
            all_rank_laws &= rank_exact
            all_transported_spaces &= transported_space_exact
            anchor_exact &= all([
                source_bijection,
                target_bijection,
                channel_kk_exact,
                channel_delete_exact,
                diagonal_target,
                two_preimages,
                active_count_exact,
                rank_exact,
                transported_space_exact,
            ])

            anchor_rank_counter[predicted_rank] += 1
            global_rank_counter[predicted_rank] += 1
            active_source_count += active_count

            metadata = reference_metadata[normalised_subset]
            channel_rows.append({
                "anchor": anchor,
                "channel_index_within_anchor": channel_index,
                "anchor_subset_A": subset_text(subset),
                "normalised_subset_rhoA": subset_text(normalised_subset),
                "source_fibre_key": str(source_key(anchor, subset)),
                "target_fibre_key": str(target_key(anchor, subset)),
                "source_fibre_size": len(source_chamber),
                "target_fibre_size": len(target_chamber),
                "active_source_states": active_count,
                "two_preimages_per_target": two_preimages,
                "source_state_bijection": source_bijection,
                "target_state_bijection": target_bijection,
                "exact_KK_column_covariance": channel_kk_exact,
                "exact_delete_column_covariance": channel_delete_exact,
                "exact_diagonal_target": diagonal_target,
                "rank_class": class_name,
                "space_name": space_name,
                "predicted_rank": predicted_rank,
                "exact_transmitted_rank": transported.rows,
                "rank_law_exact": rank_exact,
                "transported_subspace_exact": transported_space_exact,
                "exact_source_relation_dim": metadata["source_relation_dim"],
                "exact_source_residue_kernel_dim": metadata[
                    "source_residue_kernel_dim"
                ],
                "anchor_normalisation": mapping_text(rho),
            })

        anchor_rows.append({
            "anchor": anchor,
            "channel_count": 35,
            "source_fibre_count": len(source_fibres),
            "target_fibre_count": len(target_fibres),
            "active_source_state_count": active_source_count,
            "source_reversal_sign_count": source_reversal_count,
            "rank_multiplicities": rank_multiplicity_text(anchor_rank_counter),
            "rank_sum": sum(rank * count for rank, count in anchor_rank_counter.items()),
            "all_channel_covariance_exact": anchor_exact,
            "elapsed_seconds": f"{time.time() - anchor_started:.4f}",
        })
        print(
            f"  anchor={anchor}: channels=35 active={active_source_count} "
            f"ranks={dict(sorted(anchor_rank_counter.items()))} exact={anchor_exact}"
        )

    write_csv(out_dir / "all_anchor_channel_ledger.csv", channel_rows)
    write_csv(out_dir / "anchor_chart_summary.csv", anchor_rows)

    # ------------------------------------------------------------------
    # Exact transition cocycles between anchor charts.
    # Precompute all 64 pair maps, then audit the 512 triples by array
    # composition. This is exact finite permutation/sign arithmetic.
    # ------------------------------------------------------------------
    transitions: Dict[Tuple[int, int], PermutationMap] = {}
    for source_anchor in range(1, 9):
        for target_anchor in range(1, 9):
            transitions[(target_anchor, source_anchor)] = compose_mapping(
                invert_mapping(normalisations[target_anchor]),
                normalisations[source_anchor],
            )

    source_cycle_index = {cycle: index for index, cycle in enumerate(source_cycles)}
    target_cycle_index = {cycle: index for index, cycle in enumerate(target_cycles)}
    anchor_bases = {
        anchor: list(
            itertools.permutations(
                label for label in range(1, 9) if label != anchor
            )
        )
        for anchor in range(1, 9)
    }
    anchor_basis_indices = {
        anchor: {sigma: index for index, sigma in enumerate(basis)}
        for anchor, basis in anchor_bases.items()
    }
    anchor_subsets = {
        anchor: list(
            itertools.combinations(
                [label for label in range(1, 9) if label != anchor],
                3,
            )
        )
        for anchor in range(1, 9)
    }
    anchor_subset_indices = {
        anchor: {tuple(subset): index for index, subset in enumerate(subsets)}
        for anchor, subsets in anchor_subsets.items()
    }

    source_pair_maps: Dict[Tuple[int, int], Tuple[np.ndarray, np.ndarray]] = {}
    target_pair_maps: Dict[Tuple[int, int], np.ndarray] = {}
    row_pair_maps: Dict[Tuple[int, int], np.ndarray] = {}
    fibre_pair_maps: Dict[Tuple[int, int], np.ndarray] = {}

    for source_anchor in range(1, 9):
        for target_anchor in range(1, 9):
            transition = transitions[(target_anchor, source_anchor)]

            source_destination = np.empty(len(source_cycles), dtype=np.int32)
            source_sign = np.empty(len(source_cycles), dtype=np.int8)
            for index, cycle in enumerate(source_cycles):
                image, sign, _ = relabel_canonical_with_sign(cycle, transition)
                source_destination[index] = source_cycle_index[image]
                source_sign[index] = sign
            source_pair_maps[(target_anchor, source_anchor)] = (
                source_destination,
                source_sign,
            )

            target_destination = np.empty(len(target_cycles), dtype=np.int32)
            for index, cycle in enumerate(target_cycles):
                image, sign, _ = relabel_canonical_with_sign(cycle, transition)
                if sign != 1:
                    raise RuntimeError("Even target relabelling produced a reflection sign")
                target_destination[index] = target_cycle_index[image]
            target_pair_maps[(target_anchor, source_anchor)] = target_destination

            target_basis_index = anchor_basis_indices[target_anchor]
            row_destination = np.empty(len(anchor_bases[source_anchor]), dtype=np.int32)
            for index, sigma in enumerate(anchor_bases[source_anchor]):
                image = tuple(transition[label] for label in sigma)
                row_destination[index] = target_basis_index[image]
            row_pair_maps[(target_anchor, source_anchor)] = row_destination

            target_subset_index = anchor_subset_indices[target_anchor]
            fibre_destination = np.empty(35, dtype=np.int16)
            for index, subset in enumerate(anchor_subsets[source_anchor]):
                image = tuple(sorted(transition[label] for label in subset))
                fibre_destination[index] = target_subset_index[image]
            fibre_pair_maps[(target_anchor, source_anchor)] = fibre_destination

    permutation_cocycle_exact = True
    source_state_cocycle_exact = True
    target_state_cocycle_exact = True
    kk_row_cocycle_exact = True
    fibre_cocycle_exact = True
    cocycle_rows: List[Dict[str, object]] = []

    for source_anchor in range(1, 9):
        for middle_anchor in range(1, 9):
            for target_anchor in range(1, 9):
                first = transitions[(middle_anchor, source_anchor)]
                second = transitions[(target_anchor, middle_anchor)]
                direct_transition = transitions[(target_anchor, source_anchor)]
                permutation_exact = (
                    compose_mapping(second, first) == direct_transition
                )
                permutation_cocycle_exact &= permutation_exact

                source_first_destination, source_first_sign = source_pair_maps[
                    (middle_anchor, source_anchor)
                ]
                source_second_destination, source_second_sign = source_pair_maps[
                    (target_anchor, middle_anchor)
                ]
                source_direct_destination, source_direct_sign = source_pair_maps[
                    (target_anchor, source_anchor)
                ]
                source_exact = (
                    np.array_equal(
                        source_second_destination[source_first_destination],
                        source_direct_destination,
                    )
                    and np.array_equal(
                        source_first_sign
                        * source_second_sign[source_first_destination],
                        source_direct_sign,
                    )
                )
                source_state_cocycle_exact &= source_exact

                target_first = target_pair_maps[(middle_anchor, source_anchor)]
                target_second = target_pair_maps[(target_anchor, middle_anchor)]
                target_direct = target_pair_maps[(target_anchor, source_anchor)]
                target_exact = np.array_equal(
                    target_second[target_first],
                    target_direct,
                )
                target_state_cocycle_exact &= target_exact

                row_first = row_pair_maps[(middle_anchor, source_anchor)]
                row_second = row_pair_maps[(target_anchor, middle_anchor)]
                row_direct = row_pair_maps[(target_anchor, source_anchor)]
                row_exact = np.array_equal(row_second[row_first], row_direct)
                kk_row_cocycle_exact &= row_exact

                fibre_first = fibre_pair_maps[(middle_anchor, source_anchor)]
                fibre_second = fibre_pair_maps[(target_anchor, middle_anchor)]
                fibre_direct = fibre_pair_maps[(target_anchor, source_anchor)]
                chart_exact = np.array_equal(
                    fibre_second[fibre_first],
                    fibre_direct,
                )
                fibre_cocycle_exact &= chart_exact

                cocycle_rows.append({
                    "source_anchor": source_anchor,
                    "middle_anchor": middle_anchor,
                    "target_anchor": target_anchor,
                    "permutation_cocycle_exact": permutation_exact,
                    "source_signed_state_cocycle_exact": source_exact,
                    "target_state_cocycle_exact": target_exact,
                    "KK_row_cocycle_exact": row_exact,
                    "fibre_chart_cocycle_exact": chart_exact,
                })

    write_csv(out_dir / "anchor_transition_cocycle_audit.csv", cocycle_rows)

    expected_per_anchor = {0: 4, 2: 3, 8: 3, 9: 6, 14: 6, 15: 13}
    expected_global = {rank: 8 * count for rank, count in expected_per_anchor.items()}
    per_anchor_multiplicities_exact = all(
        {
            int(item.split(":")[0]): int(item.split(":")[1])
            for item in str(row["rank_multiplicities"]).split(";")
        }
        == expected_per_anchor
        for row in anchor_rows
    )
    global_multiplicities_exact = dict(sorted(global_rank_counter.items())) == expected_global

    class_rows: List[Dict[str, object]] = []
    for rank_value, count_per_anchor in expected_per_anchor.items():
        matching_space = next(
            space_name
            for space_name, space in space_by_name.items()
            if space.rows == rank_value
        )
        class_rows.append({
            "space_name": matching_space,
            "rank": rank_value,
            "count_per_anchor": count_per_anchor,
            "count_full_atlas": 8 * count_per_anchor,
        })
    write_csv(out_dir / "all_anchor_subspace_class_summary.csv", class_rows)
    write_markdown(
        out_dir / "exact_anchor_covariance_audit.md",
        anchor_rows,
        class_rows,
    )

    exact_covariance = all([
        all_source_bijections,
        all_target_bijections,
        all_kk_covariance,
        all_delete_covariance,
        all_diagonal_targets,
        all_two_preimage_counts,
        all_active_counts,
        all_rank_laws,
        all_transported_spaces,
    ])
    exact_cocycle = all([
        permutation_cocycle_exact,
        source_state_cocycle_exact,
        target_state_cocycle_exact,
        kk_row_cocycle_exact,
        fibre_cocycle_exact,
    ])
    exact_certificate = all([
        equal_within_class,
        len(distinct_reference_spaces) == 6,
        lattice_exact,
        exact_covariance,
        per_anchor_multiplicities_exact,
        global_multiplicities_exact,
        exact_cocycle,
        len(channel_rows) == 280,
        sum(int(row["active_source_state_count"]) for row in anchor_rows) == 40320,
    ])

    verdict = (
        "EHF_AMP_FOUND_03K_EXACT_ALL_ANCHOR_FIBRE_ATLAS_COVARIANCE_PROVED"
        if exact_certificate
        else "EHF_AMP_FOUND_03K_ANCHOR_COVARIANCE_FAILED"
    )

    certificate = {
        "theorem": (
            "For every surviving anchor a in {1,...,8}, the exact delete-9 "
            "fibre system is covariant under the canonical normalisation rho_a. "
            "All 280 anchor-relative channels reduce to the same 35 anchor-1 "
            "channels and, after ordered-block transport, to the same six "
            "target subspaces. Anchor transitions satisfy exact cocycles."
        ),
        "anchor_normalisation": (
            "rho_a(a)=1, rho_a(9)=9, and the remaining surviving labels map "
            "in increasing order to 2,...,8"
        ),
        "exact_covariance_equations": [
            "Q^(1)_{rho_a(A)} P_a = R_a Q^(a)_A",
            "D^(1)_{rho_a(A)} P_a = T_a D^(a)_A",
        ],
        "atlas": {
            "surviving_anchor_count": 8,
            "channels_per_anchor": 35,
            "total_anchor_fibre_channels": 280,
            "active_source_incidence_per_anchor": 5040,
            "total_active_source_incidences": 40320,
            "rank_multiplicities_per_anchor": expected_per_anchor,
            "rank_multiplicities_full_atlas": expected_global,
            "total_rank_per_anchor": 363,
            "total_rank_full_atlas": 2904,
            "common_transported_subspace_count": 6,
            "common_subspace_dimensions": [0, 2, 8, 9, 14, 15],
        },
        "cocycle": {
            "transition": "pi_(b<-a)=rho_b^{-1} rho_a",
            "anchor_triples_checked": len(cocycle_rows),
            "permutation_cocycle": permutation_cocycle_exact,
            "signed_source_state_cocycle": source_state_cocycle_exact,
            "target_state_cocycle": target_state_cocycle_exact,
            "KK_row_cocycle": kk_row_cocycle_exact,
            "fibre_chart_cocycle": fibre_cocycle_exact,
        },
        "checks": {
            "reference_six_space_lattice": lattice_exact,
            "all_source_state_bijections": all_source_bijections,
            "all_target_state_bijections": all_target_bijections,
            "all_KK_column_covariances": all_kk_covariance,
            "all_delete_column_covariances": all_delete_covariance,
            "all_diagonal_targets": all_diagonal_targets,
            "all_two_preimage_counts": all_two_preimage_counts,
            "all_anchor_rank_laws": all_rank_laws,
            "all_transported_subspaces": all_transported_spaces,
            "exact_transition_cocycle": exact_cocycle,
        },
        "claim_boundary": (
            "The theorem covers all eight surviving anchors while label 9 is "
            "deleted, using the stated canonical anchor normalisations and the "
            "ordered-block target transport. It does not include anchor 9, a "
            "different deleted leg, arbitrary n, or anchor-independent physical "
            "dynamics."
        ),
        "exact_certificate": exact_certificate,
    }
    with (out_dir / "exact_anchor_covariance_certificate.json").open("w") as handle:
        json.dump(json_safe(certificate), handle, indent=2)

    elapsed = time.time() - started
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "verdict": verdict,
        "surviving_anchor_count": 8,
        "channels_per_anchor": 35,
        "total_anchor_fibre_channels": len(channel_rows),
        "total_active_source_incidences": sum(
            int(row["active_source_state_count"]) for row in anchor_rows
        ),
        "rank_multiplicities_per_anchor": expected_per_anchor,
        "rank_multiplicities_full_atlas": dict(sorted(global_rank_counter.items())),
        "common_transported_subspace_count": len(distinct_reference_spaces),
        "all_channel_covariance_exact": exact_covariance,
        "all_anchor_transition_cocycles_exact": exact_cocycle,
        "exact_all_anchor_fibre_atlas_covariance": exact_certificate,
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "verdict.json",
            "run.log",
            "exact_anchor_covariance_certificate.json",
            "anchor_chart_summary.csv",
            "all_anchor_channel_ledger.csv",
            "all_anchor_subspace_class_summary.csv",
            "anchor_transition_cocycle_audit.csv",
            "exact_anchor_covariance_audit.md",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)
    with (out_dir / "verdict.json").open("w") as handle:
        json.dump(
            {
                "verdict": verdict,
                "exact_all_anchor_fibre_atlas_covariance": exact_certificate,
                "total_anchor_fibre_channels": len(channel_rows),
                "common_transported_subspace_count": len(distinct_reference_spaces),
            },
            handle,
            indent=2,
        )

    strict_failures: List[str] = []
    if args.strict:
        checks = {
            "reference_six_space_lattice": (
                equal_within_class
                and len(distinct_reference_spaces) == 6
                and lattice_exact
            ),
            "source_state_bijections": all_source_bijections,
            "target_state_bijections": all_target_bijections,
            "KK_column_covariance": all_kk_covariance,
            "delete_column_covariance": all_delete_covariance,
            "diagonal_targets": all_diagonal_targets,
            "two_preimages": all_two_preimage_counts,
            "active_counts": all_active_counts,
            "anchor_rank_laws": all_rank_laws,
            "transported_subspaces": all_transported_spaces,
            "per_anchor_rank_multiplicities": per_anchor_multiplicities_exact,
            "global_rank_multiplicities": global_multiplicities_exact,
            "transition_cocycles": exact_cocycle,
            "280_channels": len(channel_rows) == 280,
            "40320_active_incidences": (
                sum(int(row["active_source_state_count"]) for row in anchor_rows)
                == 40320
            ),
        }
        strict_failures = [name for name, passed in checks.items() if not passed]

    print("\nFull surviving-anchor atlas")
    print(f"  anchors:                            8")
    print(f"  channels per anchor:                35")
    print(f"  total anchor-fibre channels:        {len(channel_rows)}")
    print(f"  active source incidences:           {summary['total_active_source_incidences']}")
    print(f"  rank multiplicities per anchor:     {expected_per_anchor}")
    print(f"  rank multiplicities full atlas:     {dict(sorted(global_rank_counter.items()))}")
    print(f"  common transported subspaces:       {len(distinct_reference_spaces)}")

    print("\nExact anchor covariance")
    print(f"  source state bijections:            {all_source_bijections}")
    print(f"  target state bijections:            {all_target_bijections}")
    print(f"  KK column covariance:               {all_kk_covariance}")
    print(f"  delete-map covariance:              {all_delete_covariance}")
    print(f"  diagonal target fibres:             {all_diagonal_targets}")
    print(f"  two preimages per target:           {all_two_preimage_counts}")
    print(f"  anchor-normalised rank law:         {all_rank_laws}")
    print(f"  six-space collapse:                 {all_transported_spaces}")

    print("\nAnchor transition cocycle")
    print(f"  permutation cocycle:                {permutation_cocycle_exact}")
    print(f"  signed source-state cocycle:        {source_state_cocycle_exact}")
    print(f"  target-state cocycle:               {target_state_cocycle_exact}")
    print(f"  KK-row cocycle:                     {kk_row_cocycle_exact}")
    print(f"  fibre-chart cocycle:                {fibre_cocycle_exact}")

    print("\n" + "=" * 126)
    print("FINAL SUMMARY")
    print("=" * 126)
    print(f"Exact all-anchor covariance:          {exact_covariance}")
    print(f"Exact anchor transition cocycle:      {exact_cocycle}")
    print(f"Same six transported subspaces:       {len(distinct_reference_spaces) == 6}")
    print(f"Full 280-channel atlas closed:        {exact_certificate}")
    print(f"Verdict:                              {verdict}")
    print(f"elapsed:                              {elapsed:.2f} seconds")
    print(f"summary:                              {out_dir / 'summary.json'}")
    if args.strict:
        print(
            "strict checks:                        "
            f"{'PASS' if not strict_failures else 'FAIL'}"
        )
        if strict_failures:
            print("failed checks:                        " + ", ".join(strict_failures))
    print("=" * 126)

    if strict_failures:
        raise SystemExit(2)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prove exact anchor-change covariance and closure of the complete "
            "eight-anchor, 280-channel fixed-delete-9 fibre atlas."
        )
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--helper-script", required=True)
    parser.add_argument("--rank-script", required=True)
    parser.add_argument("--lattice-script", required=True)
    parser.add_argument("--direct-script", required=True)
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
