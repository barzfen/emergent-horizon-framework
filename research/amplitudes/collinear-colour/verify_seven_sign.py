"""Audit the quadratic 27-channel sign with up to five spectators."""

import argparse
from collections import defaultdict
from functools import reduce
from itertools import combinations, permutations, product
import json
from math import gcd, prod

import numpy as np

from orders import chains
from su3_probe import D_TABLE, METRIC


def gram_row(tensor, hard_count, leading):
    """Overlap the reference colour tensor with each spectator ordering."""
    support = np.nonzero(tensor)
    values = tensor[support]
    metric_weights = np.array([3 // m for m in METRIC], dtype=np.int64)
    weights = np.prod(metric_weights[np.stack(support)], axis=0)
    bound = int(np.max(np.abs(values)))**2 * int(weights.sum())
    if bound >= 2**62:
        values = values.astype(object)
    weighted = values * weights
    before = support[:leading]
    hard = support[leading:leading + hard_count]
    after = support[leading + hard_count:]
    orders = list(permutations(range(hard_count)))
    return np.array([weighted @ tensor[before + tuple(hard[i] for i in order) + after]
                     for order in orders], dtype=values.dtype)


def curvature_form(hard_count):
    n = hard_count + 2
    tensor = np.zeros((8,) * n, dtype=np.int64)
    scale = 6**hard_count
    for colors, coefficient in chains(hard_count):
        value = scale * coefficient
        assert value.denominator == 1
        tensor[colors] += int(value)
    tensor = tensor + tensor.swapaxes(0, -1)
    tensor //= np.gcd.reduce(tensor.ravel())
    singlet = sum(tensor[a, ..., a] * (3 // METRIC[a]) for a in range(8))
    octet = np.zeros((8,) * (n-1), dtype=np.int64)
    for (a, b), row in D_TABLE.items():
        for c, value in row:
            factor = 18 * value / (METRIC[a] * METRIC[b])
            assert factor.denominator == 1
            octet[c] += tensor[a, ..., b] * int(factor)

    # Each row has metric weights 3 / METRIC per free colour index.
    # Including the singlet and octet normalization factors, this
    # combination represents 27 norm minus half the full norm.
    total = gram_row(tensor, hard_count, 1)
    trace = gram_row(singlet, hard_count, 0)
    dnorm = gram_row(octet, hard_count, 1)
    row = 180*total.astype(object) - 45*trace.astype(object) - 2*dnorm.astype(object)
    row //= reduce(gcd, map(int, row))
    orders = list(permutations(range(hard_count)))
    lookup = dict(zip(orders, row.tolist()))
    q = np.array([[lookup[tuple(inverse[j] for j in v)] for v in orders]
                  for inverse in map(np.argsort, orders)], dtype=np.int64)
    assert np.array_equal(q, q.T)
    return orders, q


def ordering_factors(orders):
    all_edges = set(combinations(range(len(orders[0])), 2))
    result = []
    for order in orders:
        path = list(zip(order, order[1:]))
        used = {tuple(sorted(e)) for e in path}
        result.append(((-1)**sum(a > b for a, b in path),
                       [(order[0], order[-1]), *sorted(all_edges - used)]))
    return result


def numeric_gradient(factors, gaps):
    # All differences are nonzero in the sorted chart. Taking gap sums
    # avoids subtracting nearly equal coordinates in the numerical scan.
    gradient = np.zeros((len(gaps) - 1, len(factors)))
    for i, (sign, edges) in enumerate(factors):
        diffs = [sum(gaps[a:b]) if a < b else -sum(gaps[b:a]) for a, b in edges]
        value = sign * prod(diffs)
        for (a, b), difference in zip(edges, diffs):
            term = value / difference
            if a >= 2:
                gradient[a-2, i] -= term
            if b >= 2:
                gradient[b-2, i] += term
    return gradient


def search(factors, q, hard_count, samples, seed):
    rng = np.random.default_rng(seed)
    min_eigen = float('inf')
    min_case = None
    negative = 0
    tolerance = 1e-9
    for _ in range(samples):
        gaps = np.exp(rng.uniform(-7, 7, hard_count-1))
        gaps /= gaps.max()
        gradient = numeric_gradient(factors, gaps)
        # Scale individual tangent basis vectors by positive numbers.
        gradient /= np.linalg.norm(gradient, axis=1, keepdims=True)
        m = gradient @ q @ gradient.T
        m /= np.max(np.abs(m))
        eigen = float(np.linalg.eigvalsh((m+m.T)/2)[0])
        if eigen < min_eigen:
            min_eigen, min_case = eigen, gaps.tolist()
        negative += int(eigen < -tolerance)
    return dict(samples=samples, seed=seed, smallest_normalized_eigenvalue=min_eigen,
                gaps=min_case, negative_tolerance=tolerance, negative_below_tolerance=negative)


def add(a, b, scale=1):
    result = defaultdict(int, a)
    for key, value in b.items():
        result[key] += scale * value
    return {key: value for key, value in result.items() if value}


def multiply(a, b):
    result = defaultdict(int)
    for exponent, value in a.items():
        for other, second in b.items():
            result[tuple(x+y for x, y in zip(exponent, other))] += value * second
    return {key: value for key, value in result.items() if value}


def polynomial_gradients(factors, hard_count):
    dims = hard_count - 2
    zero = (0,) * dims
    units = [tuple(int(i == j) for i in range(dims)) for j in range(dims)]
    coords = [{}, {zero: 1}]
    for unit in units:
        coords.append(add(coords[-1], {unit: 1}))
    derivatives = [[] for _ in units]
    bases = []
    for sign, edges in factors:
        linear = [add(coords[b], coords[a], -1) for a, b in edges]
        bases.append(reduce(multiply, linear, {zero: sign}))
        for spectator, column in enumerate(derivatives, start=2):
            value = {}
            for j, (a, b) in enumerate(edges):
                scale = int(b == spectator) - int(a == spectator)
                if scale:
                    value = add(value, reduce(multiply, linear[:j] + linear[j+1:], {zero: sign}),
                                scale)
            column.append(value)
    return bases, derivatives


def coefficient_form(left, right, q):
    """Contract exact integer coefficient matrices before collecting monomials."""
    left_keys = sorted(set().union(*left))
    right_keys = sorted(set().union(*right))
    a = np.array([[p.get(key, 0) for p in left] for key in left_keys], dtype=object)
    b = np.array([[p.get(key, 0) for p in right] for key in right_keys], dtype=object)
    weights = a @ q.astype(object) @ b.T
    out = defaultdict(int)
    for i, u in enumerate(left_keys):
        for j, v in enumerate(right_keys):
            if weights[i, j]:
                out[tuple(x+y for x, y in zip(u, v))] += weights[i, j]
    return {key: value for key, value in out.items() if value}


def principal_minors(m):
    result = [m[0][0], add(multiply(m[0][0], m[1][1]), multiply(m[0][1], m[0][1]), -1)]
    if len(m) == 3:
        determinant = {}
        for order in permutations(range(3)):
            inversions = sum(a > b for a, b in combinations(order, 2))
            term = reduce(multiply, (m[i][j] for i, j in enumerate(order)))
            determinant = add(determinant, term, (-1)**inversions)
        result.append(determinant)
    return result


def summarize(polynomial):
    if not polynomial:
        return dict(terms=0)
    values = list(polynomial.values())
    return dict(terms=len(values), positive=sum(v > 0 for v in values),
                negative=sum(v < 0 for v in values), smallest=min(values), largest=max(values))


def certificate(factors, hard_count, q):
    base, gradient = polynomial_gradients(factors, hard_count)
    assert not coefficient_form(base, base, q)
    assert all(not coefficient_form(base, row, q) for row in gradient)
    m = [[coefficient_form(a, b, q) for b in gradient] for a in gradient]
    assert all(m[i][j] == m[j][i] for i in range(len(m)) for j in range(i))
    minors = principal_minors(m)
    assert all(p and min(p.values()) > 0 for p in minors)
    return minors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gluons", type=int, choices=(6, 7), default=7)
    parser.add_argument("--samples", type=int, default=0)
    parser.add_argument("--scan-only", action="store_true")
    parser.add_argument("--coefficients", action="store_true")
    args = parser.parse_args()
    hard_count = args.gluons - 2
    orders, q = curvature_form(hard_count)
    factors = ordering_factors(orders)
    result = dict(gluons=args.gluons, orderings=len(orders), gram_row=q[0].tolist())
    if args.samples:
        result["numerical_scan"] = search(factors, q, hard_count, args.samples, seed=15431)
    if not args.scan_only:
        minors = certificate(factors, hard_count, q)
        result["leading_minors"] = [summarize(p) for p in minors]
        if args.coefficients:
            result["coefficients"] = [[[*key, value] for key, value in sorted(p.items())]
                                      for p in minors]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
