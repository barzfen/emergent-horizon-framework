#!/usr/bin/env python3
"""Independent GROW-LIFT-03 verification: direct swaps + SciPy assignment.

Requires scipy (and numpy). The primary probe uses only Python stdlib.
"""
from collections import deque, Counter, defaultdict
from itertools import permutations
from pathlib import Path
import json
from scipy.optimize import linear_sum_assignment

R={1,2,3}

def canonical(x):
    z=list(x);a=z.index(0);z=z[a:]+z[:a]
    r=[0]+z[:0:-1]
    return tuple(z) if tuple(z)<tuple(r) else tuple(r)

def permitted(seq):
    t=[z in R for z in seq];m=len(seq)
    return all(t[i]==t[i-1] or t[i]==t[(i+1)%m] for i in range(m))

def all_words(n):
    return [(0,)+a for a in permutations(range(1,n)) if a[0]<a[-1] and permitted((0,)+a)]

def signature(word):return frozenset(word[::2])

def graph(words,preserve_pi):
    n=len(words[0]);index={s:i for i,s in enumerate(words)}
    neighbours=[set() for _ in words]
    for i,s in enumerate(words):
        for distance in (1,2):
            for p in range(n):
                t=list(s);q=(p+distance)%n;t[p],t[q]=t[q],t[p]
                canonical_t=canonical(t);j=index.get(canonical_t)
                if j is not None and j!=i and (not preserve_pi or signature(s)==signature(canonical_t)):
                    neighbours[i].add(j)
    return neighbours

def delete_two(s):
    for _ in range(2):s=canonical([x for x in s if x!=len(s)-1])
    return s

def distances(adj,start_set):
    q=deque(start_set);dist={j:0 for j in start_set}
    while q:
        x=q.popleft()
        for j in adj[x]:
            if j not in dist:dist[j]=dist[x]+1;q.append(j)
    return dist

def limited(adj,start,depth):
    q=deque([start]);d={start:0}
    while q:
        x=q.popleft()
        if d[x]>=depth:continue
        for y in adj[x]:
            if y not in d:d[y]=d[x]+1;q.append(y)
    return d

def component_ids(adj):
    labels={};p=0
    for i in range(len(adj)):
        if i in labels:continue
        q=[i];labels[i]=p
        while q:
            for v in adj[q.pop()]:
                if v not in labels:labels[v]=p;q.append(v)
        p+=1
    return labels,p

def matching(A,B,adj,W,depth):
    C=[]
    for x in A:
        z=limited(adj,x,depth)
        C.append([(0 if signature(W[x])==signature(W[y]) else 1) if y in z else 10000 for y in B])
    import numpy as np
    matrix=np.asarray(C,dtype=int)
    rows,cols=linear_sum_assignment(matrix)
    used=int(sum(matrix[i,j]<10000 for i,j in zip(rows,cols)))
    cost=int(sum(matrix[i,j] for i,j in zip(rows,cols))) if used==len(A) else None
    return used,cost

def main():
    data=json.loads(Path(__file__).with_name('results.json').read_text())
    W={n:all_words(n) for n in (7,9)};I={n:{s:i for i,s in enumerate(W[n])} for n in W}
    assert [len(W[n]) for n in (7,9)]==[72,2160]
    Gpi={n:graph(W[n],True) for n in W}
    Gno=graph(W[9],False)
    assert sum(map(len,Gpi[7]))//2==84
    assert sum(map(len,Gpi[9]))//2==4080
    labels,cc=component_ids(Gpi[9]);assert cc==111
    fibers=defaultdict(list)
    for i,s in enumerate(W[9]):fibers[delete_two(s)].append(i)
    assert len(fibers)==72 and set(map(len,fibers.values()))=={30}
    for a in data['cross_fiber_audits']:
        A=fibers[tuple(a['from'])];B=fibers[tuple(a['to'])]
        d=distances(Gpi[9],B);d_no=distances(Gno,B)
        assert Counter(d.get(x,-1) for x in A)=={-1:3,1:20,2:7}
        assert Counter(d_no.get(x,-1) for x in A)=={1:28,2:2}
        la=Counter(labels[x] for x in A);lb=Counter(labels[x] for x in B)
        assert sum(min(la[k],lb[k]) for k in la.keys()|lb.keys())==23
        sigA=Counter(signature(W[9][x]) for x in A)
        sigB=Counter(signature(W[9][y]) for y in B)
        assert sum(min(sigA[s],sigB[s]) for s in sigA.keys()|sigB.keys())==26
        assert matching(A,B,Gpi[9],W[9],1)[0]==20
        assert matching(A,B,Gpi[9],W[9],2)[0]==22
        assert matching(A,B,Gno,W[9],2)==(30,8)
        assert matching(A,B,Gno,W[9],3)==(30,5)
        assert matching(A,B,Gno,W[9],4)==(30,4)
    sample=data['sample_repaired_arc']['nine_vertex_microstep_path']
    assert len(sample)==3
    for a,b in zip(sample,sample[1:]):
        assert I[9][tuple(b)] in Gno[I[9][tuple(a)]]
        assert permitted(a) and permitted(b)
    assert delete_two(sample[0])==tuple(data['sample_repaired_arc']['seven_vertex_arc'][0])
    assert delete_two(sample[-1])==tuple(data['sample_repaired_arc']['seven_vertex_arc'][1])
    print('PASS: independent direct-swap graphs, component bounds, 12 arc audits, SciPy matching and witness')

if __name__=='__main__':main()
