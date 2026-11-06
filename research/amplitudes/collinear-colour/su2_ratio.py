"""Exact symmetric SU(2) colour-channel norms at five to seven gluons."""
from collections import defaultdict
from fractions import Fraction
from itertools import permutations
import json

from color_probe import ddm, epsilon
from orders import coefficients, kinematics


def chains(first, remaining):
    if remaining == 0:
        yield (first,), 1
        return
    for emitted in range(3):
        if first == emitted:
            continue
        last = 3-first-emitted
        for tail, sign in chains(last, remaining-1):
            yield (emitted,*tail), epsilon(first,emitted,last)*sign


def audit(n,sample):
    base, slopes = kinematics(n,sample)
    chain_rows = [((a,*tail), sign) for a in range(3) for tail,sign in chains(a,n-2)]
    assert all(len(colors)==n for colors, _ in chain_rows)
    if n == 5:
        assert all(ddm(colors) == sign for colors, sign in chain_rows)
    pole, finite = defaultdict(Fraction), defaultdict(Fraction)
    for middle in permutations(range(1,n-1)):
        word = (0,*middle,n-1)
        leading, regular = coefficients(word,base,slopes)[:2]
        for colors, sign in chain_rows:
            key = [0]*n
            for index,color in zip(word,colors):
                key[index] = color
            pole[tuple(key)] += sign*leading
            finite[tuple(key)] += sign*regular
    traces = defaultdict(Fraction)
    for (a,*spectators,b),value in finite.items():
        assert value==finite.get((b,*spectators,a),0)
        assert pole[a,*spectators,b]==-pole.get((b,*spectators,a),0)
        if a==b:
            traces[tuple(spectators)] += value
    singlet = sum(v*v for v in traces.values())/3
    total = sum(v*v for v in finite.values())
    five = total-singlet
    assert singlet>0 and 5*singlet==4*five
    return dict(gluons=n,sample=sample,squared_norms=list(map(str,(singlet,five))),
                normalized_shares=list(map(str,(singlet/total,five/total))))


if __name__ == '__main__':
    print(json.dumps([audit(n,sample) for n in (5,6,7) for sample in (1,2,3)],indent=2))
