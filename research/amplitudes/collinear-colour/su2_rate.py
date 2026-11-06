"""Test a pole-free rate combination in pure SU(2) at finite opening."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations
from math import prod
import json

from color_probe import add, bracket
from orders import kinematics
from su2_ratio import chains, tensors


def full_tensor(n, sample, t):
    base, slopes = kinematics(n,sample)
    spinors = [add(a,b,t) for a,b in zip(base,slopes)]
    numerator = bracket(spinors[1],spinors[2])**4
    chain_rows = [((a,*tail),sign) for a in range(3) for tail,sign in chains(a,n-2)]
    tensor = defaultdict(F)
    for middle in permutations(range(1,n-1)):
        word = (0,*middle,n-1)
        value = F(numerator,prod(bracket(spinors[a],spinors[b])
                                 for a,b in zip(word,word[1:]+word[:1])))
        for colors,sign in chain_rows:
            key = [0]*n
            for index,color in zip(word,colors):
                key[index] = color
            tensor[tuple(key)] += sign*value
    return tensor


def squares(tensor):
    spectators = {key[1:-1] for key in tensor}
    same_sign,neutral,even,odd = [F(0) for _ in range(4)]
    for rest in spectators:
        def value(a,b):
            return tensor.get((a,*rest,b),0)
        same_sign += ((value(0,0)-value(1,1))**2+(value(0,1)+value(1,0))**2)/F(4)
        neutral += value(2,2)**2
        for a in range(3):
            for b in range(3):
                even += (value(a,b)+value(b,a))**2/F(4)
                odd += (value(a,b)-value(b,a))**2/F(4)
    assert even == 3*(same_sign+neutral)
    assert even+odd == sum(v*v for v in tensor.values())
    return same_sign,neutral,even,odd


def audit(n,sample):
    pole,finite = tensors(n,sample)
    pp,nn,base,_ = squares(finite)
    assert pp/base==F(1,9) and nn/base==F(2,9)
    results = []
    for denom in (128,256,512,1024):
        t = F(1,denom)
        pp,nn,even,odd = squares(full_tensor(n,sample,t))
        candidate = pp/(3*(pp+nn))
        naive = pp/(even+odd)
        results.append(dict(opening=str(t),same_sign_to_neutral=float(pp/nn),
                            candidate=float(candidate),naive=float(naive),
                            candidate_error_over_t_squared=float((candidate-F(1,9))/t**2),
                            naive_over_t_squared=float(naive/t**2)))
    assert abs(results[-1]['candidate']-1/9)<abs(results[0]['candidate']-1/9)
    expected = float(squares(finite)[0]/sum(v*v for v in pole.values()))
    assert abs(results[-1]['naive_over_t_squared']-expected) < abs(results[0]['naive_over_t_squared']-expected)
    return dict(gluons=n,sample=sample,points=results)


if __name__ == '__main__':
    print(json.dumps([audit(n,1) for n in (5,6,7)],indent=2))
