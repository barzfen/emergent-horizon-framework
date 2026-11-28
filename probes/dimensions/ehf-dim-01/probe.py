"""EHF-DIM-01: n=7 OPW3 vs OPW23 ball growth and random-walk returns.
Requires numpy; graph enumeration is independent of earlier audits.
"""
from itertools import permutations
from collections import deque, Counter
import numpy as np

def canon(c):
    c=list(c); k=c.index(0); c=c[k:]+c[:k]
    return min(tuple(c),(0,)+tuple(reversed(c[1:])))
def rev(c,k,length):
    a=list(c); ix=[(k+j)%len(c) for j in range(length)]
    for i,x in zip(ix,[a[j] for j in ix][::-1]): a[i]=x
    return canon(a)

n=7
states=sorted({canon((0,)+p) for p in permutations(range(1,n))})
lookup={s:i for i,s in enumerate(states)}
def build(lengths):
    adj=[set() for _ in states]
    for i,s in enumerate(states):
        for length in lengths:
            for k in range(n):
                t=rev(s,k,length)
                if t!=s and frozenset(t[::2])==frozenset(s[::2]):
                    j=lookup[t]; adj[i].add(j);adj[j].add(i)
    unseen=set(range(len(states))); comps=[]
    while unseen:
        root=unseen.pop(); stack=[root]; comp={root}
        while stack:
            v=stack.pop()
            for w in adj[v]&unseen:
                unseen.remove(w);comp.add(w);stack.append(w)
        comps.append(comp)
    return adj,comps

for name,lengths,expected_edges,expected_degree,expected_balls in [
    ('OPW3',(3,),600,4,[1,5,13,23,31,35,36]),
    ('OPW23',(2,3),840,6,[1,7,27,36])]:
    adj,comps=build(lengths)
    assert len(states)==360 and len(comps)==19
    assert sum(map(len,adj))//2==expected_edges
    largest=sorted(max(comps,key=len))
    assert len(largest)==36
    loc={v:i for i,v in enumerate(largest)}
    A=np.zeros((36,36))
    for i,v in enumerate(largest):
        for w in adj[v]:A[i,loc[w]]=1
    degrees=A.sum(axis=1)
    assert np.all(degrees==expected_degree)
    distance_lists=[]
    for root in largest:
        distances={root:0};q=deque([root])
        while q:
            v=q.popleft()
            for w in adj[v]:
                if w not in distances:
                    distances[w]=distances[v]+1;q.append(w)
        distance_lists.append(list(distances.values()))
    diameter=max(map(max,distance_lists))
    balls=[sum(sum(d<=r for d in distances) for distances in distance_lists)/36 for r in range(diameter+1)]
    assert balls==expected_balls
    eigenvalues=np.linalg.eigvalsh(A/expected_degree)
    returns=[float(np.mean(eigenvalues**t)) for t in (2,4,6,8,10,12)]
    print(name,'edges',expected_edges,'diameter',diameter,'balls',balls)
    print('even-time mean return probabilities:',returns)
print('PASS')
