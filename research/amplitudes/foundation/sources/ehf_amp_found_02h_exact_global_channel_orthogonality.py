#!/usr/bin/env python3
"""Exact cross-channel orthogonality audit for EHF-AMP-FOUND-02H.

Rebuilds the ten complement-pair operators directly from the exact KK
construction and verifies over Q that K_i K_j = 0 for i != j and that the
sum has rank 110.
"""
from __future__ import annotations
import argparse, importlib.util, itertools, json, sys, time
from pathlib import Path
import sympy as sp


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-script', required=True)
    parser.add_argument('--helper-script', required=True)
    parser.add_argument('--symmetry-script', required=True)
    parser.add_argument('--direct-script', required=True)
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args()

    started = time.time()
    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    base = load(Path(args.base_script).resolve(), 'ehf_02h_global_base')
    helper = load(Path(args.helper_script).resolve(), 'ehf_02h_global_helper')
    symmetry = load(Path(args.symmetry_script).resolve(), 'ehf_02h_global_symmetry')
    direct = load(Path(args.direct_script).resolve(), 'ehf_02h_global_direct')

    n = 8
    targets = list(base.canonical_cycles(7))
    fibres = base.fibres(n)
    active, _, pairs, pair_ids = symmetry.build_pairs(base)
    kk_perms = list(itertools.permutations(range(2, n)))
    kk_index = {p: i for i, p in enumerate(kk_perms)}

    data = {}
    for key in active:
        chamber = fibres[key]
        q = direct.exact_kk_coordinate_matrix(chamber, n, kk_index)
        _, projector, _, _ = direct.exact_relation_projector(q)
        deletion = direct.exact_delete_matrix(base, helper, chamber, targets, n)
        data[key] = projector, deletion

    operators = []
    ranks = []
    for left, right in pairs:
        p_l, d_l = data[left]
        p_r, d_r = data[right]
        k = d_l * p_l * d_l.T + d_r * p_r * d_r.T
        operators.append(k)
        ranks.append(int(k.rank()))

    nonzero_cross_products = []
    for i in range(len(operators)):
        for j in range(i + 1, len(operators)):
            if operators[i] * operators[j] != sp.zeros(len(targets)):
                nonzero_cross_products.append([i, j])

    total = sum(operators, sp.zeros(len(targets)))
    total_rank = int(total.rank())
    result = {
        'channel_count': len(operators),
        'channel_ranks': ranks,
        'all_channel_ranks_11': all(rank == 11 for rank in ranks),
        'nonzero_cross_products': nonzero_cross_products,
        'pairwise_orthogonal_exact': not nonzero_cross_products,
        'total_rank_exact': total_rank,
        'rank_sum': sum(ranks),
        'direct_sum_exact': not nonzero_cross_products and total_rank == sum(ranks) == 110,
        'elapsed_seconds': time.time() - started,
    }
    with (out / 'exact_global_channel_orthogonality.json').open('w') as handle:
        json.dump(result, handle, indent=2)

    print('Exact channel ranks:', ranks)
    print('Nonzero cross-products:', nonzero_cross_products)
    print('Exact total rank:', total_rank)
    print('Exact orthogonal direct sum:', result['direct_sum_exact'])
    print('Output:', out / 'exact_global_channel_orthogonality.json')
    return 0 if result['direct_sum_exact'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
