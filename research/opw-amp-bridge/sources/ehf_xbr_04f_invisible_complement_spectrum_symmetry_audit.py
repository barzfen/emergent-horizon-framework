#!/usr/bin/env python3
"""
EHF-XBR-04F
===========
Invisible-Complement Spectrum and Symmetry Audit


Consumes the exact XBR-04C restricted-sector certificates and XBR-04D
orthogonal-complement certificates.  For each selected AMP channel A it
reconstructs the exact OPW3-invariant invisible complement K_A^perp and audits:


1. its exact characteristic and minimal polynomials;
2. irreducible spectral factors and algebraic multiplicities;
3. exact overlap between visible and invisible spectral support;
4. sign symmetry, zero modes, Newton trace moments, and the semisimple
   spectral-commutant dimension;
5. exact label-induced chamber automorphisms in the setwise stabiliser
   S_A x S_{ {2,...,8} \ A };
6. the induced rational symmetry representation on K_A^perp, including
   generator orders, fixed-space dimensions, and commutation with adjacency.


The spectrum is represented exactly by factorised polynomials.  No physical
interpretation is assigned to an eigenvalue, multiplicity, or symmetry without
a separate bridge argument.
"""


from __future__ import annotations


import argparse
import csv
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple


from flint import fmpq_mat, fmpq_poly, fmpz_mat




SCRIPT_VERSION = "ehf_xbr_04f_2026-07-27"
DEFAULT_PANEL = "2,3,6;3,6,7;4,6,7;4,6,8"
Subset = Tuple[int, int, int]
IntegerRows = List[List[int]]
Permutation = Tuple[int, ...]




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
    if len(values) != 3:
        raise ValueError(f"invalid subset: {text}")
    if any(value not in range(2, 9) for value in values):
        raise ValueError(f"subset labels must lie in 2..8: {text}")
    if len(set(values)) != 3:
        raise ValueError(f"subset labels must be distinct: {text}")
    return tuple(sorted(values))  # type: ignore[return-value]




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




def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()




def identity_q(size: int) -> fmpq_mat:
    result = fmpq_mat(size, size)
    for i in range(size):
        result[i, i] = 1
    return result




def matrix_trace(matrix: fmpq_mat):
    return sum((matrix[i, i] for i in range(int(matrix.nrows()))), 0)




def matrix_power(matrix: fmpq_mat, exponent: int) -> fmpq_mat:
    if exponent < 0:
        raise ValueError("negative matrix exponent")
    result = identity_q(int(matrix.nrows()))
    base = matrix
    power = exponent
    while power:
        if power & 1:
            result = result * base
        power >>= 1
        if power:
            base = base * base
    return result




def matrix_rank(matrix: fmpq_mat) -> int:
    return int(matrix.rank())




def adjacency_integer_matrix(neighbors: Sequence[Sequence[int]]) -> fmpz_mat:
    size = len(neighbors)
    rows = [[0] * size for _ in range(size)]
    for source, targets in enumerate(neighbors):
        for target in targets:
            rows[source][target] = 1
    return fmpz_mat(rows)




def polynomial_coefficients(poly) -> List[str]:
    return [str(value) for value in poly.coeffs()]




def polynomial_payload(poly) -> dict:
    coefficients = polynomial_coefficients(poly)
    return {
        "degree": int(poly.degree()),
        "coefficients_ascending": coefficients,
        "text": str(poly),
        "sha256_coefficients": sha256_text("|".join(coefficients)),
    }




def polynomial_factor_exponent(poly: fmpq_poly, factor: fmpq_poly) -> int:
    current = poly
    exponent = 0
    while int(current.degree()) >= int(factor.degree()):
        quotient, remainder = divmod(current, factor)
        if remainder != 0:
            break
        exponent += 1
        current = quotient
    return exponent




def polynomial_sign_symmetric(poly: fmpq_poly) -> bool:
    degree = int(poly.degree())
    coefficients = poly.coeffs()
    return all(
        coefficient == 0
        for power, coefficient in enumerate(coefficients)
        if (power - degree) % 2 != 0
    )




def newton_trace_moments(poly: fmpq_poly, maximum_power: int) -> List[str]:
    """Return power sums of roots from a monic characteristic polynomial."""
    degree = int(poly.degree())
    if degree <= 0:
        return ["0"] * maximum_power
    coefficients = poly.coeffs()
    if coefficients[-1] != 1:
        raise ValueError("characteristic polynomial is not monic")
    # a[j] is the coefficient of x^(degree-j).
    a = [None] + [coefficients[degree - j] for j in range(1, degree + 1)]
    moments = [0]
    for power in range(1, maximum_power + 1):
        if power <= degree:
            total = sum(
                a[j] * moments[power - j]
                for j in range(1, power)
            )
            value = -(total + power * a[power])
        else:
            total = sum(
                a[j] * moments[power - j]
                for j in range(1, degree + 1)
            )
            value = -total
        moments.append(value)
    return [str(value) for value in moments[1:]]




def exact_factor_audit(
    complement_charpoly: fmpq_poly,
    complement_minpoly: fmpq_poly,
    visible_charpoly: fmpq_poly,
) -> tuple[List[dict], dict]:
    content, factors = complement_charpoly.factor(monic=True)
    min_content, min_factors = complement_minpoly.factor(monic=True)
    factor_rows: List[dict] = []
    reconstructed = fmpq_poly([1])
    distinct_product = fmpq_poly([1])
    shared_invisible_dimension = 0
    shared_algebraic_degree = 0
    centralizer_dimension = 0
    maximum_multiplicity = 0
    distinct_root_count = 0
    zero_multiplicity = 0


    for factor_number, (factor, complement_exponent_raw) in enumerate(
        factors,
        start=1,
    ):
        complement_exponent = int(complement_exponent_raw)
        visible_exponent = polynomial_factor_exponent(visible_charpoly, factor)
        degree = int(factor.degree())
        reconstructed *= factor ** complement_exponent
        distinct_product *= factor
        distinct_root_count += degree
        centralizer_dimension += degree * complement_exponent * complement_exponent
        maximum_multiplicity = max(maximum_multiplicity, complement_exponent)
        if visible_exponent > 0:
            shared_invisible_dimension += degree * complement_exponent
            shared_algebraic_degree += degree


        coefficients = factor.coeffs()
        root = ""
        if degree == 1:
            root = str(-coefficients[0] / coefficients[1])
            if coefficients[0] == 0:
                zero_multiplicity = complement_exponent


        factor_rows.append({
            "factor_number": factor_number,
            "factor_degree": degree,
            "complement_exponent": complement_exponent,
            "visible_exponent": visible_exponent,
            "shared_with_visible": visible_exponent > 0,
            "linear_root": root,
            "factor": str(factor),
            "factor_coefficients_ascending": json.dumps(
                [str(value) for value in coefficients]
            ),
        })


    min_reconstructed = fmpq_poly([1])
    min_exponents: List[int] = []
    for factor, exponent_raw in min_factors:
        exponent = int(exponent_raw)
        min_exponents.append(exponent)
        min_reconstructed *= factor ** exponent


    complement_dimension = int(complement_charpoly.degree())
    audit = {
        "factor_content": str(content),
        "minimal_factor_content": str(min_content),
        "factor_count": len(factors),
        "distinct_root_count_over_algebraic_closure": distinct_root_count,
        "maximum_algebraic_multiplicity": maximum_multiplicity,
        "zero_eigenvalue_multiplicity": zero_multiplicity,
        "shared_invisible_dimension": shared_invisible_dimension,
        "invisible_only_dimension": complement_dimension - shared_invisible_dimension,
        "shared_algebraic_degree": shared_algebraic_degree,
        "spectral_commutant_dimension": centralizer_dimension,
        "spectral_commutant_excess": centralizer_dimension - complement_dimension,
        "simple_spectrum_over_algebraic_closure": maximum_multiplicity <= 1,
        "charpoly_factor_reconstruction_exact": (
            reconstructed == complement_charpoly
        ),
        "minimal_factor_reconstruction_exact": (
            min_reconstructed == complement_minpoly
        ),
        "minimal_polynomial_squarefree": all(
            exponent == 1 for exponent in min_exponents
        ),
        "minimal_equals_distinct_charpoly_product": (
            complement_minpoly == distinct_product
        ),
    }
    return factor_rows, audit




def canonical_cycle(cycle: Sequence[int]) -> Tuple[int, ...]:
    values = tuple(int(value) for value in cycle)
    rotations = [
        values[offset:] + values[:offset]
        for offset in range(len(values))
    ]
    reversed_values = tuple(reversed(values))
    rotations.extend(
        reversed_values[offset:] + reversed_values[:offset]
        for offset in range(len(values))
    )
    return min(rotations)




def compose_permutations(left: Permutation, right: Permutation) -> Permutation:
    """Return left after right."""
    return tuple(left[right[index]] for index in range(len(left)))




def inverse_permutation(permutation: Permutation) -> Permutation:
    inverse = [0] * len(permutation)
    for source, target in enumerate(permutation):
        inverse[target] = source
    return tuple(inverse)




def permutation_order(permutation: Permutation) -> int:
    seen: Set[int] = set()
    order = 1
    for start in range(len(permutation)):
        if start in seen:
            continue
        length = 0
        current = start
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        if length:
            order = math.lcm(order, length)
    return order




def permutation_cycle_text(permutation: Permutation) -> str:
    seen: Set[int] = set()
    cycles: List[str] = []
    for start in range(len(permutation)):
        if start in seen or permutation[start] == start:
            seen.add(start)
            continue
        cycle: List[int] = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current + 1)
            current = permutation[current]
        cycles.append("(" + " ".join(map(str, cycle)) + ")")
    return "".join(cycles) if cycles else "()"




def candidate_stabilizer_permutations(subset: Subset) -> List[Permutation]:
    internal = tuple(range(1, 8))  # zero-based labels 2..8
    selected = tuple(value - 1 for value in subset)
    selected_set = set(selected)
    complement = tuple(value for value in internal if value not in selected_set)
    candidates: List[Permutation] = []
    for selected_image in itertools.permutations(selected):
        for complement_image in itertools.permutations(complement):
            mapping = list(range(9))
            for source, target in zip(selected, selected_image):
                mapping[source] = target
            for source, target in zip(complement, complement_image):
                mapping[source] = target
            candidates.append(tuple(mapping))
    candidates.sort(key=permutation_cycle_text)
    return candidates




def group_closure(generators: Sequence[Permutation]) -> Set[Permutation]:
    if generators:
        size = len(generators[0])
    else:
        size = 9
    identity = tuple(range(size))
    expanded = list(generators) + [inverse_permutation(g) for g in generators]
    closure: Set[Permutation] = {identity}
    queue: List[Permutation] = [identity]
    while queue:
        current = queue.pop()
        for generator in expanded:
            target = compose_permutations(generator, current)
            if target not in closure:
                closure.add(target)
                queue.append(target)
    return closure




def greedy_group_generators(group: Set[Permutation]) -> List[Permutation]:
    generators: List[Permutation] = []
    closure = group_closure(generators)
    for candidate in sorted(group, key=permutation_cycle_text):
        if candidate not in closure:
            generators.append(candidate)
            closure = group_closure(generators)
        if closure == group:
            break
    return generators




def group_axioms_exact(group: Set[Permutation]) -> bool:
    if not group:
        return False
    size = len(next(iter(group)))
    identity = tuple(range(size))
    if identity not in group:
        return False
    if any(inverse_permutation(element) not in group for element in group):
        return False
    return all(
        compose_permutations(left, right) in group
        for left in group
        for right in group
    )




def chamber_state_permutation(
    label_permutation: Permutation,
    global_states: Sequence[int],
    cycles: Sequence[Tuple[int, ...]],
    global_index: Mapping[Tuple[int, ...], int],
) -> List[int] | None:
    local_index = {
        global_state: local_state
        for local_state, global_state in enumerate(global_states)
    }
    image: List[int] = []
    for global_state in global_states:
        mapped_cycle = canonical_cycle(
            tuple(label_permutation[label] for label in cycles[global_state])
        )
        mapped_global = global_index.get(mapped_cycle)
        if mapped_global is None or mapped_global not in local_index:
            return None
        image.append(local_index[mapped_global])
    if len(set(image)) != len(image):
        return None
    return image




def adjacency_automorphism_exact(
    image: Sequence[int],
    neighbors: Sequence[Sequence[int]],
) -> bool:
    for source, targets in enumerate(neighbors):
        mapped_targets = {image[target] for target in targets}
        if mapped_targets != set(neighbors[image[source]]):
            return False
    return True




def permute_coordinate_rows(
    rows: Sequence[Sequence[int]],
    state_image: Sequence[int],
) -> IntegerRows:
    transformed: IntegerRows = []
    for row in rows:
        output = [0] * len(state_image)
        for source, target in enumerate(state_image):
            output[target] = int(row[source])
        transformed.append(output)
    return transformed




def complement_coordinate_solver(
    complement_rows: IntegerRows,
    pivot_columns: Sequence[int],
):
    dimension = len(complement_rows)
    basis = fmpq_mat(complement_rows)
    pivot_square = fmpq_mat([
        [complement_rows[row][column] for column in pivot_columns]
        for row in range(dimension)
    ])
    pivot_inverse = pivot_square.inv()


    def solve(target_rows: IntegerRows) -> tuple[fmpq_mat, bool]:
        target_pivots = fmpq_mat([
            [target_rows[row][column] for column in pivot_columns]
            for row in range(dimension)
        ])
        coordinates = target_pivots * pivot_inverse
        exact = coordinates * basis == fmpq_mat(target_rows)
        return coordinates, bool(exact)


    return solve




def symmetry_representation_row(
    label_permutation: Permutation,
    state_image: Sequence[int],
    complement_rows: IntegerRows,
    solve_coordinates,
    complement_action: fmpq_mat,
) -> tuple[dict, fmpq_mat | None]:
    dimension = len(complement_rows)
    transformed = permute_coordinate_rows(complement_rows, state_image)
    representation, exact = solve_coordinates(transformed)
    identity = identity_q(dimension)
    order = permutation_order(label_permutation)
    order_exact = exact and matrix_power(representation, order) == identity
    commutes = exact and representation * complement_action == complement_action * representation
    fixed_dimension = (
        dimension - matrix_rank(representation - identity)
        if exact else -1
    )
    anti_fixed_dimension = ""
    if exact and order == 2:
        anti_fixed_dimension = str(
            dimension - matrix_rank(representation + identity)
        )
    row = {
        "label_permutation": permutation_cycle_text(label_permutation),
        "label_permutation_order": order,
        "representation_exact": exact,
        "representation_order_exact": order_exact,
        "commutes_with_complement_action": commutes,
        "representation_trace": str(matrix_trace(representation)) if exact else "",
        "fixed_space_dimension": fixed_dimension,
        "anti_fixed_space_dimension": anti_fixed_dimension,
        "acts_trivially_on_complement": exact and representation == identity,
    }
    return row, representation if exact else None




def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit exact spectra and label-induced symmetries of XBR-04D "
            "OPW3 invisible complements."
        )
    )
    parser.add_argument("--xbr04c-dir", required=False)
    parser.add_argument("--xbr04d-dir", required=False)
    parser.add_argument("--xbr04c-script", required=False)
    parser.add_argument("--xbr04d-script", required=False)
    parser.add_argument("--opw-base-script", required=False)
    parser.add_argument("--amp-base-script", required=False)
    parser.add_argument("--amp-rank-script", required=False)
    parser.add_argument(
        "--subsets",
        type=parse_subset_selection,
        default=parse_subset_selection(DEFAULT_PANEL),
        help=(
            "'all' or semicolon-separated triples; default representative "
            f"panel {DEFAULT_PANEL}"
        ),
    )
    parser.add_argument("--moment-max", type=int, default=6)
    parser.add_argument(
        "--symmetry-full-max-dim",
        type=int,
        default=16,
        help=(
            "enumerate the full complement representation when its dimension "
            "does not exceed this value; otherwise certify group generators"
        ),
    )
    parser.add_argument(
        "--write-symmetry-matrices",
        choices=("none", "generators", "full"),
        default="generators",
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--out-dir", default="runs/ehf_xbr_04f")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()


    if args.self_test:
        assert canonical_cycle((0, 1, 2, 3)) == canonical_cycle((2, 3, 0, 1))
        assert canonical_cycle((0, 1, 2, 3)) == canonical_cycle((0, 3, 2, 1))


        swap = (2, 1, 0)
        assert permutation_order(swap) == 2
        assert compose_permutations(swap, swap) == (0, 1, 2)
        assert group_closure([swap]) == {(0, 1, 2), swap}


        complement_action = fmpq_mat([[0, 2], [1, 0]])
        complement_charpoly = complement_action.charpoly()
        complement_minpoly = complement_action.minpoly()
        chamber = fmpz_mat([[0, 0, 0], [0, 0, 2], [0, 1, 0]])
        chamber_charpoly = fmpq_poly(chamber.charpoly().coeffs())
        visible_charpoly, remainder = divmod(chamber_charpoly, complement_charpoly)
        assert remainder == 0
        assert visible_charpoly == fmpq_poly([0, 1])
        factors, audit = exact_factor_audit(
            complement_charpoly,
            complement_minpoly,
            visible_charpoly,
        )
        assert len(factors) == 1
        assert audit["charpoly_factor_reconstruction_exact"]
        assert audit["minimal_equals_distinct_charpoly_product"]
        assert newton_trace_moments(complement_charpoly, 4) == [
            "0", "4", "0", "8"
        ]


        basis = [[1, 0, -1]]
        pivots = [0]
        solve = complement_coordinate_solver(basis, pivots)
        transformed = permute_coordinate_rows(basis, [2, 1, 0])
        coordinates, exact = solve(transformed)
        assert exact
        assert coordinates == fmpq_mat([[-1]])
        print("EHF-XBR-04F self-test PASS")
        return 0


    required_names = [
        "xbr04c_dir",
        "xbr04d_dir",
        "xbr04c_script",
        "xbr04d_script",
        "opw_base_script",
        "amp_base_script",
        "amp_rank_script",
    ]
    missing = [name for name in required_names if not getattr(args, name)]
    if missing:
        parser.error("missing required arguments: " + ", ".join(missing))
    if args.moment_max < 0:
        parser.error("--moment-max must be nonnegative")
    if args.symmetry_full_max_dim < 0:
        parser.error("--symmetry-full-max-dim must be nonnegative")


    started = time.perf_counter()
    xbr04c_dir = Path(args.xbr04c_dir).resolve()
    xbr04d_dir = Path(args.xbr04d_dir).resolve()
    xbr04c_script_path = Path(args.xbr04c_script).resolve()
    xbr04d_script_path = Path(args.xbr04d_script).resolve()
    opw_path = Path(args.opw_base_script).resolve()
    amp_base_path = Path(args.amp_base_script).resolve()
    amp_rank_path = Path(args.amp_rank_script).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    channel_root = out_dir / "channels"
    channel_root.mkdir(parents=True, exist_ok=True)


    xbr04c_summary_path = xbr04c_dir / "run_summary.json"
    xbr04d_summary_path = xbr04d_dir / "run_summary.json"
    source_ledger_path = xbr04c_dir / "restricted_action_ledger.csv"
    for required in (
        xbr04c_summary_path,
        xbr04d_summary_path,
        source_ledger_path,
        xbr04c_script_path,
        xbr04d_script_path,
        opw_path,
        amp_base_path,
        amp_rank_path,
    ):
        if not required.exists():
            raise FileNotFoundError(required)


    with xbr04c_summary_path.open() as handle:
        xbr04c_summary = json.load(handle)
    with xbr04d_summary_path.open() as handle:
        xbr04d_summary = json.load(handle)
    source_rows = read_csv(source_ledger_path)
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
    unknown = (
        set() if selected_set is None else selected_set - set(source_by_subset)
    )
    if unknown:
        raise ValueError(
            f"subsets absent from XBR-04C ledger: {sorted(unknown)}"
        )


    print("=" * 132)
    print("EHF-XBR-04F: INVISIBLE-COMPLEMENT SPECTRUM AND SYMMETRY AUDIT")
    print("=" * 132)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"XBR-04C directory:    {xbr04c_dir}")
    print(f"XBR-04D directory:    {xbr04d_dir}")
    print(f"selected channels:    {len(selected_subsets)}")
    print(f"moment maximum:       {args.moment_max}")
    print(f"full symmetry max d:  {args.symmetry_full_max_dim}")
    print(f"write symmetry:       {args.write_symmetry_matrices}")
    print(f"output directory:     {out_dir}")
    print(f"strict:               {args.strict}")
    print()


    xbr04c = load_module(xbr04c_script_path, "ehf_xbr_04f_xbr04c")
    xbr04d = load_module(xbr04d_script_path, "ehf_xbr_04f_xbr04d")
    opw = load_module(opw_path, "ehf_xbr_04f_opw")
    amp_base = load_module(amp_base_path, "ehf_xbr_04f_amp_base")
    amp_rank = load_module(amp_rank_path, "ehf_xbr_04f_amp_rank")
    coordinate_backend = xbr04c.choose_backend("flint")


    cycles9 = opw.generate_cycles(9)
    if any(canonical_cycle(cycle) != tuple(cycle) for cycle in cycles9):
        raise RuntimeError("cycle canonicalisation convention mismatch")
    index9 = {cycle: state for state, cycle in enumerate(cycles9)}
    pi9 = [opw.pi_label(cycle) for cycle in cycles9]
    graph9 = opw.build_preserve_graph(
        cycles9,
        index9,
        pi9,
        "OPW3",
        opw.GRAPH_LENGTHS["OPW3"],
    )
    components9 = xbr04d.connected_components(graph9.adjacency)
    component_sets = {
        frozenset(component): component_id
        for component_id, component in enumerate(components9)
    }
    source_fibres = amp_base.fibres(9)


    spectrum_ledger_path = out_dir / "spectrum_ledger.csv"
    factor_ledger_path = out_dir / "factor_ledger.csv"
    symmetry_ledger_path = out_dir / "symmetry_ledger.csv"
    generator_ledger_path = out_dir / "symmetry_generator_ledger.csv"


    spectrum_rows: List[dict] = []
    factor_rows_all: List[dict] = []
    symmetry_rows_all: List[dict] = []
    generator_rows_all: List[dict] = []
    completed: Dict[Subset, dict] = {}
    if args.resume and spectrum_ledger_path.exists():
        for row in read_csv(spectrum_ledger_path):
            subset = parse_subset(row["subset"])
            if (
                subset in selected_subsets
                and truthy(row.get("channel_certificate_pass"))
            ):
                completed[subset] = row
                spectrum_rows.append(row)


    all_selected_pass = True
    full_representation_channels = 0
    generator_representation_channels = 0
    total_shared_invisible_dimension = 0
    total_nontrivial_automorphism_groups = 0


    for channel_number, subset in enumerate(selected_subsets, start=1):
        if subset in completed:
            row = completed[subset]
            channel_pass = truthy(row.get("channel_certificate_pass"))
            all_selected_pass &= channel_pass
            print(
                f"[channel {channel_number}/{len(selected_subsets)}] "
                f"A={subset} resumed"
            )
            continue


        channel_started = time.perf_counter()
        source_row = source_by_subset[subset]
        source_channel_dir = xbr04c_dir / "channels" / subset_slug(subset)
        complement_channel_dir = xbr04d_dir / "channels" / subset_slug(subset)
        source_certificate_path = source_channel_dir / "certificate.json"
        complement_certificate_path = complement_channel_dir / "certificate.json"
        with source_certificate_path.open() as handle:
            source_certificate = json.load(handle)
        with complement_certificate_path.open() as handle:
            complement_certificate = json.load(handle)


        chamber_size = int(source_row["source_chamber_size"])
        closure_dimension = int(source_row["closure_dimension"])
        complement_dimension = chamber_size - closure_dimension
        amp_dimension = int(source_row["amp_dimension"])


        source_key = amp_rank.key_from_subset_9(subset)
        source_cycles_one = source_fibres[source_key]
        source_global_ids = [
            index9[tuple(label - 1 for label in cycle)]
            for cycle in source_cycles_one
        ]
        source_component_id = component_sets.get(
            frozenset(source_global_ids)
        )
        neighbors = xbr04d.local_neighbors(
            graph9.adjacency,
            source_global_ids,
        )


        if amp_dimension == 0:
            source_basis: IntegerRows = []
        else:
            source_basis = xbr04d.read_integer_coordinate_gzip(
                source_channel_dir / "basis_matrix.coordinate.json.gz"
            )
        source_hash = xbr04d.sha256_integer_rows(source_basis)
        certified_source_hash = (
            source_certificate.get("basis", {}).get("sha256_dense_rows")
            if amp_dimension > 0 else source_hash
        )
        source_hash_matches = source_hash == certified_source_hash


        complement_rows = xbr04d.integer_right_nullspace(
            source_basis,
            chamber_size,
            "flint",
        )
        complement_hash = xbr04d.sha256_integer_rows(complement_rows)
        certified_complement_hash = complement_certificate.get(
            "decomposition", {}
        ).get("basis_sha256")
        complement_hash_matches = complement_hash == certified_complement_hash
        complement_rank = xbr04d.exact_rank(complement_rows, "flint")
        complement_targets = xbr04d.multiply_rows_by_adjacency(
            complement_rows,
            neighbors,
        )


        if complement_dimension:
            complement_pivots = coordinate_backend.pivot_columns(
                complement_rows
            )
            complement_action = coordinate_backend.coordinates(
                complement_rows,
                complement_targets,
                complement_pivots,
            )
            complement_action_exact = coordinate_backend.verify_coordinates(
                complement_action,
                complement_rows,
                complement_targets,
            )
            complement_self_adjoint = coordinate_backend.gram_self_adjoint(
                complement_action,
                complement_rows,
            )
        else:
            complement_pivots = []
            complement_action = fmpq_mat(0, 0)
            complement_action_exact = True
            complement_self_adjoint = True


        chamber_adjacency = adjacency_integer_matrix(neighbors)
        chamber_charpoly = fmpq_poly(chamber_adjacency.charpoly().coeffs())
        complement_charpoly = complement_action.charpoly()
        complement_minpoly = complement_action.minpoly()
        visible_charpoly, charpoly_remainder = divmod(
            chamber_charpoly,
            complement_charpoly,
        )
        charpoly_decomposition_exact = (
            charpoly_remainder == 0
            and int(visible_charpoly.degree()) == closure_dimension
            and visible_charpoly * complement_charpoly == chamber_charpoly
        )


        channel_factor_rows, factor_audit = exact_factor_audit(
            complement_charpoly,
            complement_minpoly,
            visible_charpoly,
        )
        for factor_row in channel_factor_rows:
            factor_row.update({
                "subset": subset_text(subset),
                "complement_dimension": complement_dimension,
            })
            factor_rows_all.append(factor_row)


        trace_moments = newton_trace_moments(
            complement_charpoly,
            args.moment_max,
        )
        sign_symmetric = polynomial_sign_symmetric(complement_charpoly)
        odd_moments_zero = all(
            trace_moments[power - 1] == "0"
            for power in range(1, args.moment_max + 1, 2)
        )


        candidates = candidate_stabilizer_permutations(subset)
        candidate_group_order = len(candidates)
        identity_label = tuple(range(9))
        graph_automorphisms: Set[Permutation] = set()
        graph_images: Dict[Permutation, List[int]] = {}
        channel_symmetry_rows: List[dict] = []


        for candidate in candidates:
            state_image = chamber_state_permutation(
                candidate,
                source_global_ids,
                cycles9,
                index9,
            )
            chamber_permutation = state_image is not None
            adjacency_automorphism = (
                chamber_permutation
                and adjacency_automorphism_exact(state_image, neighbors)
            )
            if adjacency_automorphism and state_image is not None:
                graph_automorphisms.add(candidate)
                graph_images[candidate] = state_image
            symmetry_row = {
                "subset": subset_text(subset),
                "label_permutation": permutation_cycle_text(candidate),
                "label_permutation_order": permutation_order(candidate),
                "candidate_setwise_stabilizer": True,
                "induces_chamber_permutation": chamber_permutation,
                "is_opw3_chamber_automorphism": adjacency_automorphism,
                "representation_tested": False,
                "representation_exact": "",
                "commutes_with_complement_action": "",
                "representation_trace": "",
                "fixed_space_dimension": "",
                "acts_trivially_on_complement": "",
            }
            channel_symmetry_rows.append(symmetry_row)


        graph_group_exact = group_axioms_exact(graph_automorphisms)
        graph_generators = greedy_group_generators(graph_automorphisms)
        generator_closure_exact = (
            group_closure(graph_generators) == graph_automorphisms
        )
        nontrivial_automorphism_group = len(graph_automorphisms) > 1
        total_nontrivial_automorphism_groups += int(
            nontrivial_automorphism_group
        )


        representation_full = (
            complement_dimension <= args.symmetry_full_max_dim
        )
        tested_permutations = (
            sorted(graph_automorphisms, key=permutation_cycle_text)
            if representation_full
            else graph_generators
        )
        if representation_full:
            full_representation_channels += 1
        else:
            generator_representation_channels += 1


        representation_exact_all = True
        representation_relations_all = True
        representation_commutes_all = True
        representation_matrices: Dict[Permutation, fmpq_mat] = {}
        generator_matrix_files: Dict[str, object] = {}
        trace_distribution: Counter[str] = Counter()
        fixed_distribution: Counter[str] = Counter()


        if complement_dimension:
            solve_complement = complement_coordinate_solver(
                complement_rows,
                complement_pivots,
            )
            symmetry_row_by_permutation = {
                row["label_permutation"]: row
                for row in channel_symmetry_rows
            }
            for tested_number, candidate in enumerate(
                tested_permutations,
                start=1,
            ):
                representation_row, representation = symmetry_representation_row(
                    candidate,
                    graph_images[candidate],
                    complement_rows,
                    solve_complement,
                    complement_action,
                )
                label_text = representation_row["label_permutation"]
                target_row = symmetry_row_by_permutation[label_text]
                target_row.update({
                    "representation_tested": True,
                    "representation_exact": representation_row[
                        "representation_exact"
                    ],
                    "representation_order_exact": representation_row[
                        "representation_order_exact"
                    ],
                    "commutes_with_complement_action": representation_row[
                        "commutes_with_complement_action"
                    ],
                    "representation_trace": representation_row[
                        "representation_trace"
                    ],
                    "fixed_space_dimension": representation_row[
                        "fixed_space_dimension"
                    ],
                    "anti_fixed_space_dimension": representation_row[
                        "anti_fixed_space_dimension"
                    ],
                    "acts_trivially_on_complement": representation_row[
                        "acts_trivially_on_complement"
                    ],
                })
                representation_exact_all &= bool(
                    representation_row["representation_exact"]
                )
                representation_relations_all &= bool(
                    representation_row["representation_order_exact"]
                )
                representation_commutes_all &= bool(
                    representation_row["commutes_with_complement_action"]
                )
                if representation is not None:
                    representation_matrices[candidate] = representation
                    trace_distribution[str(matrix_trace(representation))] += 1
                    fixed_distribution[str(
                        representation_row["fixed_space_dimension"]
                    )] += 1
                    should_write = (
                        args.write_symmetry_matrices == "full"
                        or (
                            args.write_symmetry_matrices == "generators"
                            and candidate in graph_generators
                        )
                    )
                    if should_write:
                        matrix_name = (
                            f"symmetry_{tested_number:03d}.coordinate.json.gz"
                        )
                        generator_matrix_files[label_text] = (
                            coordinate_backend.write_rational_matrix_coordinate_gzip(
                                out_dir / "channels" / subset_slug(subset)
                                / matrix_name,
                                representation,
                            )
                        )
        else:
            representation_exact_all = True
            representation_relations_all = True
            representation_commutes_all = True


        if representation_full:
            if complement_dimension == 0:
                sector_group_certified = True
                representation_kernel_size = len(graph_automorphisms)
                representation_image_order = 1
            else:
                sector_group_certified = (
                    len(representation_matrices) == len(graph_automorphisms)
                    and representation_exact_all
                    and representation_relations_all
                    and representation_commutes_all
                )
                representation_kernel_size = sum(
                    matrix == identity_q(complement_dimension)
                    for matrix in representation_matrices.values()
                )
                representation_image_order = (
                    len(graph_automorphisms) // representation_kernel_size
                    if representation_kernel_size else 0
                )
        else:
            sector_group_certified = (
                representation_exact_all
                and representation_relations_all
                and representation_commutes_all
                and generator_closure_exact
            )
            identity_representation = None
            representation_kernel_size = -1
            representation_image_order = -1


        for symmetry_row in channel_symmetry_rows:
            symmetry_rows_all.append(symmetry_row)


        for generator_number, generator in enumerate(graph_generators, start=1):
            label_text = permutation_cycle_text(generator)
            source_symmetry_row = next(
                row for row in channel_symmetry_rows
                if row["label_permutation"] == label_text
            )
            generator_row = {
                "subset": subset_text(subset),
                "generator_number": generator_number,
                **source_symmetry_row,
            }
            generator_rows_all.append(generator_row)


        total_shared_invisible_dimension += int(
            factor_audit["shared_invisible_dimension"]
        )


        source_04c_pass = bool(source_certificate.get("strict_pass"))
        source_04d_pass = bool(complement_certificate.get("strict_pass"))
        checks = {
            "source_xbr04c_certificate_pass": source_04c_pass,
            "source_xbr04d_certificate_pass": source_04d_pass,
            "source_basis_hash_matches": source_hash_matches,
            "complement_basis_hash_matches_04d": complement_hash_matches,
            "source_fibre_is_exact_opw_chamber": source_component_id is not None,
            "source_chamber_size_matches": len(source_global_ids) == chamber_size,
            "complement_rank_matches_codimension": (
                complement_rank == complement_dimension
            ),
            "complement_action_exact": complement_action_exact,
            "complement_gram_self_adjoint_exact": complement_self_adjoint,
            "characteristic_polynomial_decomposition_exact": (
                charpoly_decomposition_exact
            ),
            "characteristic_factorisation_exact": bool(
                factor_audit["charpoly_factor_reconstruction_exact"]
            ),
            "minimal_factorisation_exact": bool(
                factor_audit["minimal_factor_reconstruction_exact"]
            ),
            "self_adjoint_minimal_polynomial_squarefree": bool(
                factor_audit["minimal_polynomial_squarefree"]
                and factor_audit[
                    "minimal_equals_distinct_charpoly_product"
                ]
            ),
            "identity_is_chamber_automorphism": (
                identity_label in graph_automorphisms
            ),
            "label_automorphisms_form_exact_group": graph_group_exact,
            "selected_generators_generate_graph_group": generator_closure_exact,
            "complement_symmetry_representation_certified": (
                sector_group_certified
            ),
        }
        channel_pass = all(checks.values())
        all_selected_pass &= channel_pass


        channel_dir = channel_root / subset_slug(subset)
        channel_dir.mkdir(parents=True, exist_ok=True)
        elapsed_channel = time.perf_counter() - channel_started
        row = {
            "subset": subset_text(subset),
            "source_component_id": source_component_id,
            "source_chamber_size": chamber_size,
            "closure_dimension": closure_dimension,
            "complement_dimension": complement_dimension,
            "complement_factor_count": factor_audit["factor_count"],
            "distinct_root_count": factor_audit[
                "distinct_root_count_over_algebraic_closure"
            ],
            "maximum_algebraic_multiplicity": factor_audit[
                "maximum_algebraic_multiplicity"
            ],
            "zero_eigenvalue_multiplicity": factor_audit[
                "zero_eigenvalue_multiplicity"
            ],
            "shared_invisible_dimension": factor_audit[
                "shared_invisible_dimension"
            ],
            "invisible_only_dimension": factor_audit[
                "invisible_only_dimension"
            ],
            "spectral_commutant_dimension": factor_audit[
                "spectral_commutant_dimension"
            ],
            "spectral_commutant_excess": factor_audit[
                "spectral_commutant_excess"
            ],
            "simple_spectrum": factor_audit[
                "simple_spectrum_over_algebraic_closure"
            ],
            "sign_symmetric_spectrum": sign_symmetric,
            "odd_trace_moments_zero": odd_moments_zero,
            "trace_moments_1_to_k": json.dumps(trace_moments),
            "candidate_label_stabilizer_order": candidate_group_order,
            "opw3_label_automorphism_group_order": len(graph_automorphisms),
            "opw3_label_automorphism_generator_count": len(graph_generators),
            "full_label_stabilizer_is_opw3_automorphic": (
                len(graph_automorphisms) == candidate_group_order
            ),
            "symmetry_representation_mode": (
                "full_group" if representation_full else "generators"
            ),
            "symmetry_representation_kernel_size": representation_kernel_size,
            "symmetry_representation_image_order": representation_image_order,
            "channel_certificate_pass": channel_pass,
            "elapsed_seconds": elapsed_channel,
        }


        certificate = {
            "probe": "EHF-XBR-04F",
            "title": "Invisible-Complement Spectrum and Symmetry Audit",
            "script_version": SCRIPT_VERSION,
            "utc_completed": utc_now(),
            "subset": list(subset),
            "source": {
                "xbr04c_directory": str(xbr04c_dir),
                "xbr04d_directory": str(xbr04d_dir),
                "xbr04c_certificate": str(source_certificate_path),
                "xbr04d_certificate": str(complement_certificate_path),
                "source_chamber_size": chamber_size,
                "closure_dimension": closure_dimension,
                "complement_dimension": complement_dimension,
            },
            "spectrum": {
                "chamber_characteristic_polynomial": polynomial_payload(
                    chamber_charpoly
                ),
                "visible_characteristic_polynomial": polynomial_payload(
                    visible_charpoly
                ),
                "complement_characteristic_polynomial": polynomial_payload(
                    complement_charpoly
                ),
                "complement_minimal_polynomial": polynomial_payload(
                    complement_minpoly
                ),
                "factor_audit": factor_audit,
                "factors": channel_factor_rows,
                "sign_symmetric": sign_symmetric,
                "trace_moments": trace_moments,
            },
            "symmetry": {
                "candidate_group": (
                    "setwise stabiliser S_A x S_{internal complement}, "
                    "with labels 1 and 9 fixed"
                ),
                "candidate_group_order": candidate_group_order,
                "opw3_chamber_automorphism_group_order": len(
                    graph_automorphisms
                ),
                "graph_group_exact": graph_group_exact,
                "generators": [
                    permutation_cycle_text(generator)
                    for generator in graph_generators
                ],
                "generator_closure_exact": generator_closure_exact,
                "representation_mode": (
                    "full_group" if representation_full else "generators"
                ),
                "representation_certified": sector_group_certified,
                "trace_distribution_if_full": dict(trace_distribution),
                "fixed_space_distribution_if_full": dict(fixed_distribution),
                "representation_kernel_size_if_full": representation_kernel_size,
                "representation_image_order_if_full": representation_image_order,
                "matrix_files": generator_matrix_files,
            },
            "checks": checks,
            "strict_pass": channel_pass,
            "ledger_row": row,
            "elapsed_seconds": elapsed_channel,
        }
        write_json(channel_dir / "certificate.json", certificate)


        spectrum_rows.append(row)
        completed[subset] = row
        write_csv(spectrum_ledger_path, spectrum_rows)
        write_csv(factor_ledger_path, factor_rows_all)
        write_csv(symmetry_ledger_path, symmetry_rows_all)
        write_csv(generator_ledger_path, generator_rows_all)


        print(
            f"[channel {channel_number}/{len(selected_subsets)}] "
            f"A={subset} complement={complement_dimension} "
            f"factors={factor_audit['factor_count']} "
            f"shared={factor_audit['shared_invisible_dimension']} "
            f"sign={'yes' if sign_symmetric else 'no'} "
            f"aut={len(graph_automorphisms)}/{candidate_group_order} "
            f"sym={row['symmetry_representation_mode']} "
            f"pass={channel_pass} elapsed={elapsed_channel:.2f}s"
        )


    selected_complete = set(completed) == set(selected_subsets)
    full_selection = set(selected_subsets) == set(source_by_subset)
    source_04c_full_pass = (
        bool(xbr04c_summary.get("strict_pass"))
        and bool(xbr04c_summary.get("full_35_pass"))
        and xbr04c_summary.get("verdict")
        == "EHF_XBR_04C_EXACT_RESTRICTED_ACTION_CERTIFICATE_PASS"
    )
    source_04d_full_pass = (
        bool(xbr04d_summary.get("strict_pass"))
        and xbr04d_summary.get("verdict")
        == "EHF_XBR_04D_EXACT_LATTICE_INVISIBLE_COMPLEMENT_PASS"
    )
    checks = {
        "source_xbr04c_full_certificate_pass": source_04c_full_pass,
        "source_xbr04d_full_certificate_pass": source_04d_full_pass,
        "selected_channels_complete": selected_complete,
        "all_selected_channel_certificates_pass": all_selected_pass,
    }
    if full_selection:
        checks["full_census_channel_count_35"] = len(selected_subsets) == 35
    strict_pass = all(checks.values())
    if full_selection and strict_pass:
        verdict = (
            "EHF_XBR_04F_INVISIBLE_COMPLEMENT_SPECTRUM_SYMMETRY_AUDIT_PASS"
        )
    elif strict_pass:
        verdict = (
            "EHF_XBR_04F_SELECTED_INVISIBLE_COMPLEMENT_SPECTRUM_SYMMETRY_PASS"
        )
    else:
        verdict = "EHF_XBR_04F_INVISIBLE_COMPLEMENT_SPECTRUM_SYMMETRY_FAIL"


    elapsed = time.perf_counter() - started
    serializable_subsets = (
        "all"
        if selected_set is None
        else [list(subset) for subset in sorted(selected_set)]
    )
    summary = {
        "probe": "EHF-XBR-04F",
        "title": "Invisible-Complement Spectrum and Symmetry Audit",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": {
            **vars(args),
            "subsets": serializable_subsets,
        },
        "counts": {
            "selected_channels": len(selected_subsets),
            "completed_channels": len(completed),
            "full_representation_channels": full_representation_channels,
            "generator_representation_channels": generator_representation_channels,
            "channels_with_nontrivial_label_automorphisms": (
                total_nontrivial_automorphism_groups
            ),
            "total_shared_invisible_dimension": (
                total_shared_invisible_dimension
            ),
        },
        "checks": checks,
        "strict_pass": strict_pass,
        "exact_statement": (
            "For every selected channel, the XBR-04D invisible complement has "
            "an exact characteristic-polynomial decomposition inside the full "
            "OPW3 chamber spectrum. Its irreducible factors, multiplicities, "
            "visible-sector overlap, sign symmetry, and label-induced chamber "
            "symmetry representation are certified exactly."
        ),
        "claim_boundary": (
            "This is an exact finite spectral and representation-theoretic "
            "statement about OPW3 chamber adjacency. It does not identify an "
            "eigenvalue, multiplicity, or symmetry with a physical observable "
            "or fundamental symmetry."
        ),
        "elapsed_seconds": elapsed,
        "verdict": verdict,
    }
    write_json(out_dir / "run_summary.json", summary)


    print()
    print("[invisible-complement spectrum and symmetry certification]")
    print(
        f"  selected={len(selected_subsets)} completed={len(completed)}"
    )
    print(
        f"  full representations={full_representation_channels} "
        f"generator representations={generator_representation_channels}"
    )
    print(
        f"  nontrivial label-automorphism groups="
        f"{total_nontrivial_automorphism_groups}"
    )
    print(f"  all selected pass={strict_pass}")
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