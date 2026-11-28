"""Recover the invariant SU(2) weights from charged-basis diagonal entries."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json

from su2_ratio import tensors

# Integer components before division by sqrt(2) for each charged label.
# Each entry is (Cartesian index, power of i).
BASIS = {"+": ((0,0),(1,1)), "-": ((0,0),(1,3)), "0": ((2,0),)}


def audit(n, sample):
    _, finite = tensors(n,sample)
    spectators = {key[1:-1] for key in finite}
    diagonal = {}
    for first,last in product(BASIS,repeat=2):
        norm = F(0)
        for rest in spectators:
            real, imag = F(0),F(0)
            for (a,p),(b,q) in product(BASIS[first],BASIS[last]):
                value = finite.get((a,*rest,b),0)
                phase = (p+q)%4
                if phase in (0,2):
                    real += value if phase==0 else -value
                else:
                    imag += value if phase==1 else -value
            norm += real*real+imag*imag
        diagonal[first+last] = norm/2**((first!="0")+(last!="0"))

    total = sum(v*v for v in finite.values())
    assert sum(diagonal.values())==total
    shares = {k:v/total for k,v in diagonal.items()}
    expected = {"++":F(1,9),"--":F(1,9),"00":F(2,9),"+-":F(1,6),"-+":F(1,6),
                "+0":F(1,18),"0+":F(1,18),"-0":F(1,18),"0-":F(1,18)}
    assert shares==expected

    # Invariance of the spectator-summed density gives equal weights
    # for the five components of the symmetric traceless representation.
    five = 5*diagonal["++"]
    singlet = total-five
    trace = sum(sum(finite.get((a,*rest,a),0) for a in range(3))**2
                for rest in spectators)/3
    assert singlet==trace

    # Check redistribution for exact illustrative values of sin²(theta).
    for s2 in (F(0),F(1,5),F(1,2),F(1)):
        c2 = 1-s2
        rotated = defaultdict(F)
        def options(label):
            return (("Z",c2),("gamma",s2)) if label=="0" else ((label,F(1)),)
        for (first,last),weight in shares.items():
            for (a,wa),(b,wb) in product(options(first),options(last)):
                rotated[a,b] += weight*wa*wb
        assert sum(rotated.values())==1
        assert rotated["Z","gamma"]==F(2,9)*c2*s2
        assert 5*rotated["+","+"]==five/total
    return dict(gluons=n,sample=sample,ordered_shares={k:str(v) for k,v in shares.items()},
                reconstructed_shares=[str(singlet/total),str(five/total)])


if __name__ == "__main__":
    print(json.dumps([audit(n,s) for n in (5,6,7) for s in (1,2,3)],indent=2))
