#!/usr/bin/env python3
"""Independent EHF-GROW-LIFT-04 direct-swap and square-face verification."""
from itertools import permutations
from collections import Counter
from pathlib import Path
import json

MARK={1,2,3}

def normalize(a):
    a=list(a);i=a.index(0);a=a[i:]+a[:i]
    b=[0]+a[:0:-1]
    return tuple(a) if a<b else tuple(b)

def admissible(s):
    z=[v in MARK for v in s];n=len(s)
    return all(z[i]==z[i-1] or z[i]==z[(i+1)%n] for i in range(n))

def carrier(n):
    return [(0,)+p for p in permutations(range(1,n))
            if p[0]<p[-1] and admissible((0,)+p)]

def position_swap(c,i,k):
    a=list(c);j=(i+k)%len(c);a[i],a[j]=a[j],a[i]
    return normalize(a)

def graph(S):
    idx={s:i for i,s in enumerate(S)}
    g=[set() for _ in S]
    for i,s in enumerate(S):
        for j in range(len(s)):
            d=position_swap(s,j,2);t=idx.get(d)
            if t is not None and t!=i and frozenset(s[::2])==frozenset(d[::2]):
                g[i].add(t)
    return g

def blocks(g):
    used=set();cc=[]
    for i in range(len(g)):
        if i in used:continue
        todo=[i];used.add(i);block=[]
        while todo:
            x=todo.pop();block.append(x)
            for y in g[x]:
                if y not in used:used.add(y);todo.append(y)
        cc.append(block)
    return cc

def ref_phase(s):
    s=normalize(s)
    if s.index(4)>s.index(1):s=(0,)+s[:0:-1]
    m=[x for x in s if x in MARK]
    return int(m[0]<m[-1])

def parent(s):
    for x in (len(s)-1,len(s)-2):s=normalize(y for y in s if y!=x)
    return s

def flip(s):
    i=next(k for k,v in enumerate(s) if v in MARK)
    return position_swap(s,i,2)

def main():
    data=json.loads(Path(__file__).with_name('results.json').read_text())
    for n in (5,7,9):
        S=carrier(n);g=graph(S);cc=blocks(g)
        sizes=Counter(map(len,cc))
        assert len(S)==data[str(n)]['states']
        assert sum(map(len,g))//2==data[str(n)]['OPW3_edges']
        assert len(cc)==data[str(n)]['OPW3_components']
        assert dict(sizes)=={int(k):v for k,v in data[str(n)]['component_sizes'].items()}
        assert all(i in g[j] for i,row in enumerate(g) for j in row)
        for i,c in enumerate(S):
            f=flip(c)
            assert f in S and frozenset(f[::2])==frozenset(c[::2])
            assert ref_phase(f)==(ref_phase(c)^1)
            if n>5:
                assert parent(f)==flip(parent(c))
                assert ref_phase(parent(c))==ref_phase(c)
        if n==7:
            assert sizes=={2:18,4:9}
            for block in cc:
                if len(block)==2:
                    assert all(len(g[x])==1 for x in block)
                else:
                    assert len(block)==4 and all(len(g[x])==2 for x in block)
                    # Four-cycles are commuting marked and unmarked LR3 swaps.
                    a=block[0];f=next(j for j,c in enumerate(S) if c==flip(S[a]))
                    other=next(j for j in g[a] if j!=f)
                    fother=next(j for j,c in enumerate(S) if c==flip(S[other]))
                    assert fother in g[f]
            # Bare-graph Betti number nine; filling nine squares kills H1.
            assert sum(map(len,g))//2-len(S)+len(cc)==9
        print('verified',n,len(S),'states',len(cc),'components')
    # A reciprocal voltage assignment on one square can have nonzero
    # circulation but it must cancel along every edge and its reverse.
    print('PASS: independent direct-slot reversals, stable growth phase, nine squares')
if __name__=='__main__': main()
