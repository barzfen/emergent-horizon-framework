"""Exact colour channel norms across a symmetric collinear expansion."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations, product
from math import lcm
import json
from su3_probe import D_TABLE, F_TABLE, METRIC, I, norm2
from color_probe import bracket, add, laurent


def kinematics(n, sample):
    p, r = (1,0), (0,1)
    hard = [(1,sample+1), (sample+2,1)]
    squares = [(2,3), (3,-1)]
    if n >= 6:
        hard.append((2,2*sample+5))
        squares.append((1,-4))
    if n == 7:
        hard.append((3,-2*sample-1))
        squares.append((-2,5))
    rbar = (2,-1)
    pbar = tuple(-F(sum(a[0]*b[j] for a,b in zip(hard,squares)),2) for j in range(2))
    r_hard = tuple(-sum(a[1]*b[j] for a,b in zip(hard,squares)) for j in range(2))
    base = (p,*hard,r,p)
    slopes = (r,*([(0,0)]*(n-2)),(0,-1))
    for t in (F(0), F(1,13), F(-1,17)):
        angles = [add(a,b,t) for a,b in zip(base,slopes)]
        square = (add(pbar,rbar,t),*squares,add(r_hard,rbar,-2*t*t),add(pbar,rbar,-t))
        assert all(sum(a[i]*b[j] for a,b in zip(angles,square)) == 0
                   for i,j in product(range(2),repeat=2))
    return base, slopes


def coefficients(word, base, slopes):
    p = [F(1)]
    n = len(word)
    for a,b in zip(word,word[1:]+word[:1]):
        x = bracket(base[a],base[b])
        y = bracket(slopes[a],base[b])+bracket(base[a],slopes[b])
        assert not bracket(slopes[a],slopes[b])
        if not x:
            assert (a,b) == (n-1,0)
            x,y = y,0
        nxt = [F(0)]*(len(p)+1)
        for j,c in enumerate(p):
            nxt[j] += x*c
            nxt[j+1] += y*c
        p = nxt
    result = [F(bracket(base[1],base[2])**4,p[0])]
    for j in range(1,5):
        result.append(-sum(p[k]*result[j-k] for k in range(1,j+1))/p[0])
    return result


def chains(interior_count):
    def extend(colors, current, value, remaining):
        if not remaining:
            yield (*colors,current), value
            return
        for nxt in I:
            for index,coef in F_TABLE[current,nxt]:
                factor = coef/METRIC[index] if remaining>1 else coef
                yield from extend((*colors,nxt),index,value*factor,remaining-1)
    for first in I:
        yield from extend((first,),first,F(1),interior_count)


def tensor_rows(n):
    for colors, weight in chains(n-2):
        for middle in permutations(range(1,n-1)):
            word = (0,*middle,n-1)
            key = [0]*n
            for leg,color in zip(word,colors):
                key[leg] = color
            yield tuple(key),word,weight


def channel_norms(tensor, parity):
    singlet, octet_s, octet_a = (defaultdict(F) for _ in range(3))
    for key,value in tensor.items():
        a,*hard,e = key
        assert tensor.get((e,*hard,a),0) == parity*value
        if not value:
            continue
        weight = value/(METRIC[a]*METRIC[e])
        if a == e:
            singlet[tuple(hard)] += value/METRIC[a]
        for k, coef in D_TABLE[a,e]:
            octet_s[k,*hard] += coef*weight
        for k, coef in F_TABLE[a,e]:
            octet_a[k,*hard] += coef*weight
    s1,s8,a8 = norm2(singlet)/8,3*norm2(octet_s)/5,norm2(octet_a)/3
    total = norm2(tensor)
    if parity == 1:
        assert a8 == 0
        return {"1":s1,"8s":s8,"27":total-s1-s8,"8a":F(0),"10+10bar":F(0)}
    assert s1 == s8 == 0
    return {"1":F(0),"8s":F(0),"27":F(0),"8a":a8,"10+10bar":total-a8}


def audit(n,sample):
    base,slopes = kinematics(n,sample)
    values = {w:coefficients(w,base,slopes)
              for w in ((0,*m,n-1) for m in permutations(range(1,n-1)))}
    if n == 5:
        assert all(tuple(c[:2]) == laurent(tuple(i+1 for i in w),base,slopes)
                   for w,c in values.items())
    scales = [lcm(*(c[k].denominator for c in values.values())) for k in range(5)]
    scaled_values = {w: [int(v*scale) for v,scale in zip(c,scales)] for w,c in values.items()}
    tensors = [defaultdict(int) for _ in range(5)]
    colour_scale = 6**(n-2)
    scaled_colour = {}
    for key,word,weight in tensor_rows(n):
        if weight not in scaled_colour:
            exact = weight*colour_scale
            assert exact.denominator == 1
            scaled_colour[weight] = int(exact)
        for tensor,coef in zip(tensors,scaled_values[word]):
            if coef:
                tensor[key] += scaled_colour[weight]*coef
    # An overall scale on each order cancels in its channel fractions.
    tensors = [{key:F(v) for key,v in tensor.items() if v} for tensor in tensors]
    report = {}
    for k,tensor in enumerate(tensors,start=-1):
        norms = channel_norms(tensor,1 if k%2==0 else -1)
        total = sum(norms.values())
        assert total > 0 and all(v>=0 for v in norms.values())
        report[k] = {channel:str(v/total) for channel,v in norms.items()}
    assert report[-1]["8a"] == "1"
    return dict(n=n,sample=sample,fractions=report)


if __name__ == "__main__":
    print(json.dumps([audit(n,s) for n,s in ((5,1),(5,2),(6,1),(6,2),(7,1))],indent=2))
