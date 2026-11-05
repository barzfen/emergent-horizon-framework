"""Exact five-gluon SU(2) colour projections through the collinear pole."""
from fractions import Fraction as F
from itertools import permutations, product
from math import prod
import json

PAULI = (((0, 1), (1, 0)), ((0, -1j), (1j, 0)), ((1, 0), (0, -1)))


def epsilon(a, b, c):
    if len({a, b, c}) != 3:
        return 0
    return 1 if (a, b, c) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1


def contraction(colors):
    a, b, c, d, e = colors
    return epsilon(a, e, b) * (c == d), (a == e) * epsilon(b, c, d)


def ddm(seq):
    a, b, c, d, e = seq
    return sum(epsilon(a, b, x) * epsilon(x, c, y) * epsilon(y, d, e)
               for x, y in product(range(3), repeat=2))


def trace(seq):
    matrix = ((1, 0), (0, 1))
    for label in seq:
        p = PAULI[label]
        matrix = tuple(tuple(sum(row[k]*p[k][j] for k in range(2)) for j in range(2))
                       for row in matrix)
    value = matrix[0][0]+matrix[1][1]
    assert value.real == 0 and value.imag == int(value.imag)
    return F(int(value.imag), -16)


def weights(words, color_factor):
    out = {}
    for word in words:
        coeffs = [0, 0]
        for colors in product(range(3), repeat=5):
            factor = color_factor(tuple(colors[i-1] for i in word))
            for j, weight in enumerate(contraction(colors)):
                coeffs[j] += factor*weight
        out[word] = coeffs
    return out


def bracket(a, b):
    return a[0]*b[1]-a[1]*b[0]


def add(a, b, scale=1):
    return tuple(x+scale*y for x, y in zip(a, b))


def spinors(sample):
    # lambda1=P+tR, lambda5=P-tR. The matching square spinors are
    # Pbar+tRbar and Pbar-tRbar. Shift tilde4 by -2t²Rbar with lambda4=R.
    p, r = (1, 0), (0, 1)
    two, three = (1, sample+1), (sample+2, 1)
    bar2, bar3, rbar = (2, 3), (3, -1), (2, -1)
    pbar = tuple(-F(two[0]*bar2[j]+three[0]*bar3[j], 2) for j in range(2))
    bar4 = tuple(-two[1]*bar2[j]-three[1]*bar3[j] for j in range(2))
    base = (p, two, three, r, p)
    slopes = (r, (0, 0), (0, 0), (0, 0), (0, -1))
    for t in (F(0), F(1, 13), F(-1, 17)):
        angle = [add(a, b, t) for a, b in zip(base, slopes)]
        square = (add(pbar, rbar, t), bar2, bar3, add(bar4, rbar, -2*t*t),
                  add(pbar, rbar, -t))
        assert all(sum(a[i]*b[j] for a, b in zip(angle, square)) == 0
                   for i, j in product(range(2), repeat=2))
    return base, slopes


def laurent(word, base, slopes):
    # Negative helicity on legs 2 and 3, whose angle spinors are fixed.
    num = bracket(base[1], base[2])**4
    edges = [(a-1, b-1) for a, b in zip(word, word[1:]+word[:1])]
    constants = [bracket(base[a], base[b]) for a, b in edges]
    linear = [bracket(slopes[a], base[b])+bracket(base[a], slopes[b]) for a, b in edges]
    zeros = [j for j, value in enumerate(constants) if not value]
    if not zeros:
        return F(0), F(num, prod(constants))
    pole, = zeros
    a, b = edges[pole]
    assert {a, b} == {0, 4} and bracket(slopes[a], slopes[b]) == 0
    regular = [j for j in range(5) if j != pole]
    leading = F(num, linear[pole]*prod(constants[j] for j in regular))
    finite = -leading*sum(F(linear[j], constants[j]) for j in regular)
    return leading, finite


def evaluate(weights, base, slopes):
    out = [[F(0), F(0)], [F(0), F(0)]]
    for w, coeffs in weights.items():
        values = laurent(w, base, slopes)
        for j, c in enumerate(coeffs):
            for k, v in enumerate(values):
                out[j][k] += c*v
    return out


def full_value(weights, base, slopes, t):
    angles = [add(a, b, t) for a, b in zip(base, slopes)]
    num = bracket(angles[1], angles[2])**4
    out = [F(0), F(0)]
    for w, coeffs in weights.items():
        denom = prod(bracket(angles[a-1], angles[b-1]) for a,b in zip(w,w[1:]+w[:1]))
        for j, coeff in enumerate(coeffs):
            out[j] += coeff*F(num, denom)
    return out


def main():
    tensors = [contraction(c) for c in product(range(3), repeat=5)]
    assert sum(a*a for a,s in tensors) == sum(s*s for a,s in tensors) == 18
    assert sum(a*s for a,s in tensors) == 0
    structure = weights(((1, *w, 5) for w in permutations((2, 3, 4))), ddm)
    traces = weights(((1, *w) for w in permutations((2, 3, 4, 5))), trace)
    results = []
    for sample in (1, 2, 3):
        base, slopes = spinors(sample)
        values = evaluate(structure, base, slopes)
        assert values == evaluate(traces, base, slopes)
        antisym, singlet = values
        assert antisym[0] and not antisym[1] and not singlet[0] and singlet[1]
        for t in (F(1, 13), F(1, 17)):
            a, s = full_value(structure, base, slopes, t)
            assert [a, s] == full_value(traces, base, slopes, t)
            assert [-a, s] == full_value(structure, base, slopes, -t)
        results.append(dict(sample=sample, A=[str(v) for v in antisym],
                            S=[str(v) for v in singlet],
                            A_plus_S=[str(a+b) for a,b in zip(antisym,singlet)],
                            A_minus_S=[str(a-b) for a,b in zip(antisym,singlet)]))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
