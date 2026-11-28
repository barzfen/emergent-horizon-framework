#!/usr/bin/env python3
"""Independent direct-swap check for EHF-HOL-05, no third-party dependencies."""
from collections import deque
from itertools import permutations
from pathlib import Path
import json

MARK={1,2,3}

def norm(x):
    z=list(x);i=z.index(0);z=z[i:]+z[:i]
    r=[z[0]]+z[:0:-1]
    return tuple(z) if z<r else tuple(r)

def valid(x):
    b=[v in MARK for v in x]
    return all(b[i]==b[i-1] or b[i]==b[(i+1)%len(b)] for i in range(len(b)))

def carrier(n):
    return [(0,)+p for p in permutations(range(1,n)) if p[0]<p[-1] and valid((0,)+p)]

def transitions(S,moves):
    idx={x:i for i,x in enumerate(S)};d={};g=[set() for x in S]
    for i,x in enumerate(S):
        for k in moves:
            for start in range(len(x)):
                raw=list(x);j=(start+k-1)%len(x)
                raw[start],raw[j]=raw[j],raw[start]
                t=raw.index(0);raw=tuple(raw[t:]+raw[:t]);y=norm(raw)
                z=idx.get(y)
                if z is None or z==i or set(x[::2])!=set(y[::2]):continue
                voltage=int(raw!=y)
                if (i,z) in d:assert d[i,z]==voltage
                d[i,z]=voltage;g[i].add(z)
    assert all(d[i,j]==d[j,i] for i,row in enumerate(g) for j in row)
    return d,g

def count_parts(g):
    assigned={};parts=[]
    for i in range(len(g)):
        if i in assigned:continue
        stack=[i];assigned[i]=len(parts);comp=[]
        while stack:
            x=stack.pop();comp.append(x)
            for y in g[x]:
                if y not in assigned:assigned[y]=len(parts);stack.append(y)
        parts.append(comp)
    return assigned,parts

def is_exact(g,d):
    pot={}
    for root in range(len(g)):
        if root in pot:continue
        pot[root]=0;stack=[root]
        while stack:
            a=stack.pop()
            for b in g[a]:
                target=pot[a]^d[a,b]
                if b not in pot:pot[b]=target;stack.append(b)
                elif pot[b]!=target:return False
    return True

def project(c):
    for t in (len(c)-1,len(c)-2):
        c=norm([v for v in c if v!=t])
    return c

def main():
    data=json.loads(Path(__file__).with_name('results.json').read_text())
    cache={}
    for rec in data['systems']:
        n=rec['vertices'];ks=tuple(rec['moves']);S=carrier(n)
        voltage,g=transitions(S,ks)
        ids={c:i for i,c in enumerate(S)}
        E=sum(map(len,g))//2
        lab,parts=count_parts(g)
        assert (len(S),E,len(parts))==(rec['states'],rec['edges'],rec['components'])
        assert E-len(S)+len(parts)==rec['graph_H1']
        if rec['witness']:
            w=rec['witness'];bits=0
            assert w[0]['cycle']==w[-1]['cycle']
            assert w[0]['orientation_bit']==0 and w[-1]['orientation_bit']==1
            for a,b in zip(w,w[1:]):
                x=ids[tuple(a['cycle'])];y=ids[tuple(b['cycle'])]
                assert y in g[x]
                bits^=voltage[x,y]
                assert bits==b['orientation_bit']
            assert bits==1
        cache[n,ks]=(S,voltage,g)
        print('independent graph and holonomy witness',n,ks,'OK')
    for ks in ((3,),(2,3)):
        low,_,gl=cache[7,ks];upper,d,gu=cache[9,ks]
        lowids={s:i for i,s in enumerate(low)}
        p=[lowids[project(c)] for c in upper]
        good=[set() for _ in upper];bad=0
        for i,ns in enumerate(gu):
            for j in ns:
                if j<=i:continue
                a,b=p[i],p[j]
                if a==b or b in gl[a]:good[i].add(j);good[j].add(i)
                else:bad+=1
        assert bad==data['growth'][str(ks)]['nonprojectable_edges']
        assert is_exact(good,d)
        _,parts=count_parts(good)
        assert len(parts)==data['growth'][str(ks)]['compatible_components']
        print('independent growth-compatible exactness',ks,'OK')
    print('ALL INDEPENDENT CHECKS PASSED')

if __name__=='__main__':main()
