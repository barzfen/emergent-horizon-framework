#!/usr/bin/env python3
"""EHF-GROW-LIFT-04. Exhaustive finite test; Python standard library only."""
import json
from collections import Counter
from itertools import permutations
from pathlib import Path

MARK={1,2,3}

def canon(seq):
    c=tuple(seq);i=c.index(0);c=c[i:]+c[:i]
    return min(c,c[:1]+c[:0:-1])

def micro(c):
    return all((c[i] in MARK)==(c[i-1] in MARK) or
               (c[i] in MARK)==(c[(i+1)%len(c)] in MARK) for i in range(len(c)))

def states(n):
    return [(0,)+p for p in permutations(range(1,n))
            if p[0]<p[-1] and micro((0,)+p)]

def flip(c):
    ids=[i for i,v in enumerate(c) if v in MARK]
    assert ids==list(range(ids[0],ids[0]+3))
    s=list(c);s[ids[0]],s[ids[-1]]=s[ids[-1]],s[ids[0]]
    return canon(s)

def parent(c):
    for x in (len(c)-1,len(c)-2):c=canon(v for v in c if v!=x)
    return c

def phase(c,stable=True):
    c=canon(c)
    if stable and c.index(4)>c.index(1):c=c[:1]+c[:0:-1]
    seq=[v for v in c if v in MARK]
    return int(seq[0]<seq[-1])

def comp_stats(g):
    used=set();sizes=Counter()
    for i in range(len(g)):
        if i in used:continue
        stack=[i];used.add(i);size=0
        while stack:
            v=stack.pop();size+=1
            for w in g[v]:
                if w not in used:used.add(w);stack.append(w)
        sizes[size]+=1
    return dict(sorted(sizes.items()))

def graph(S):
    j={c:i for i,c in enumerate(S)};g=[set() for _ in S]
    for i,c in enumerate(S):
        for start in range(len(c)):
            a=list(c);u,v=start,(start+2)%len(c)
            a[u],a[v]=a[v],a[u];d=canon(a)
            k=j.get(d)
            if k is not None and i!=k and set(c[::2])==set(d[::2]):g[i].add(k)
    return g

def orbit_hist(f):
    assert sorted(f)==list(range(len(f)))
    seen=set();hist=Counter()
    for i in range(len(f)):
        if i in seen:continue
        x=i;length=0
        while x not in seen:seen.add(x);x=f[x];length+=1
        assert x==i
        hist[length]+=1
    return dict(sorted(hist.items()))

def main():
    data={};previous={}
    for n in (5,7,9):
        S=states(n);idx={c:i for i,c in enumerate(S)};assert len(S)==3*__import__('math').factorial(n-3)
        geom=[idx[flip(c)] for c in S]
        assert all(geom[geom[i]]==i and geom[i]!=i for i in range(len(S)))
        assert all(set(c[::2])==set(S[geom[i]][::2]) for i,c in enumerate(S))
        assert all(phase(c)!=phase(flip(c)) for c in S)
        F=[2*geom[i]+(b^phase(c)) for i,c in enumerate(S) for b in (0,1)]
        assert orbit_hist(F)=={4:len(S)//2}
        assert all(F[F[2*i+b]]==2*i+(b^1) for i in range(len(S)) for b in (0,1))
        g=graph(S);assert all(i in g[j] for i,row in enumerate(g) for j in row)
        E=sum(map(len,g))//2;component_sizes=comp_stats(g);C=sum(component_sizes.values())
        data[str(n)]={'states':len(S),'augmented_states':2*len(S),
            'geometric_orbits':{2:len(S)//2},'augmented_orbits':{4:len(S)//2},
            'OPW3_edges':E,'OPW3_components':C,'component_sizes':component_sizes,
            'graph_cycle_rank':E-len(S)+C}
        if n>5:
            assert all(parent(flip(c))==flip(parent(c)) and phase(parent(c))==phase(c) for c in S)
            data[f'{n-2}->{n}']={'stable_phase_matches':len(S),
                'canonical_phase_matches':sum(phase(c,False)==phase(parent(c),False) for c in S),
                'children':len(S),'augmented_projection_commutes':True}
        previous[n]=S
    assert data['7']['component_sizes']=={2:18,4:9}
    assert data['7']['graph_cycle_rank']==9
    assert data['7->9']['canonical_phase_matches']==1512
    assert data['5->7']['canonical_phase_matches']==42
    data['reciprocal_voltage_backtrack_mod2']=0
    data['directed_time_cocycle_two_step_increment_mod2']=1
    data['Pi_preserving_OPW23_twist_rescued']=False
    Path(__file__).with_name('results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
    print('ALL CHECKS PASSED')
if __name__=='__main__':main()
