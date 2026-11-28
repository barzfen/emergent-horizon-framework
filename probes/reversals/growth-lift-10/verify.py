#!/usr/bin/env python3
"""Independent EHF-GROW-LIFT-02 check via direct positional swaps."""
from itertools import permutations
from collections import defaultdict
import json
from pathlib import Path

R={1,2,3}

def normalize(a):
    a=list(a);j=a.index(0);a=a[j:]+a[:j]
    b=[a[0]]+a[:0:-1]
    return min(tuple(a),tuple(b))

def admissible(a):
    z=[v in R for v in a];n=len(a)
    return all(z[(i-1)%n]==z[i] or z[(i+1)%n]==z[i] for i in range(n))

def words(n):
    return [(0,)+p for p in permutations(range(1,n)) if p[0]<p[-1] and admissible((0,)+p)]

def edge_set(n,ks):
    S=words(n);ix={s:i for i,s in enumerate(S)};edges=set()
    for k,a in enumerate(S):
        for d in ks:
            for start in range(n):
                b=list(a)
                if d==2: u,v=start,(start+1)%n
                elif d==3:u,v=start,(start+2)%n
                else:raise ValueError(d)
                b[u],b[v]=b[v],b[u]
                b=normalize(b)
                j=ix.get(b)
                if j is not None and j!=k and frozenset(a[::2])==frozenset(b[::2]):
                    edges.add((min(k,j),max(k,j)))
    return S,edges

def ancestor(c,count=2):
    for _ in range(count):
        c=normalize([v for v in c if v!=len(c)-1])
    return c

def flip(c):
    idx=[i for i,v in enumerate(c) if v in R]
    assert idx==list(range(idx[0],idx[0]+3))
    c=list(c);c[idx[0]],c[idx[2]]=c[idx[2]],c[idx[0]]
    return normalize(c)

def main():
    data=json.loads(Path(__file__).with_name('results.json').read_text())
    assert data['states']=={'5':6,'7':72,'9':2160}
    L={};E={};IX={}
    for n in (5,7,9):
        a,e2=edge_set(n,(2,3)); b,e3=edge_set(n,(3,)); assert a==b
        L[n]=a;E[n]={'OPW3':e3,'OPW23':e2}; IX[n]={s:i for i,s in enumerate(a)}
        assert len(e3)==int(data['move_edges'][str(n)]['OPW3'])
        assert len(e2)==int(data['move_edges'][str(n)]['OPW23'])
        assert all(tuple(sorted((i,IX[n][flip(s)]))) in e3 for i,s in enumerate(a))
    # Four-step alternating LR3/LR2 orbit; all Pi labels agree.
    cycle=[(0,4,5,1,2,3,6),(0,4,5,3,2,1,6),
           (0,4,6,1,2,3,5),(0,4,6,3,2,1,5)]
    edges_in_cycle=[tuple(sorted((IX[7][cycle[i]],IX[7][cycle[(i+1)%4]]))) for i in range(4)]
    assert all(e in E[7]['OPW23'] for e in edges_in_cycle)
    assert [e in E[7]['OPW3'] for e in edges_in_cycle]==[True,False,True,False]
    assert all(frozenset(c[::2])==frozenset(cycle[0][::2]) for c in cycle)
    assert len({ancestor(c) for c in cycle})==2
    par9={s:ancestor(s) for s in L[9]}
    children=defaultdict(list)
    for s in L[9]:children[par9[s]].append(s)
    assert set(map(len,children.values()))=={30}
    for obj in data['twist_7to9_obstructions']:
        u=tuple(obj['source_parent']);v=tuple(obj['target_parent'])
        hits=set()
        for c in children[u]:
            for d in (2,3):
                for j in range(9):
                    nxt=list(c)
                    x,y=j,(j+d-1)%9
                    nxt[x],nxt[y]=nxt[y],nxt[x]
                    nxt=normalize(nxt)
                    if admissible(nxt) and frozenset(nxt[::2])==frozenset(c[::2]) and par9[nxt]==v:
                        hits.add(c)
        assert len(hits)==20 and len(children[u])-len(hits)==10
        assert tuple(obj['witness']) in set(children[u])-hits
    print('INDEPENDENT DIRECT-SWAP CHECKS PASSED')

if __name__=='__main__':main()
