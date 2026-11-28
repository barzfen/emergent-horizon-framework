#!/usr/bin/env python3
"""EHF-GROW-LIFT-01: exact RAW and MICRO insertion/LR3 projection audit."""
from itertools import permutations
from collections import Counter
import json


def canon(seq):
    z = tuple(seq)
    j = z.index(0)
    z = z[j:] + z[:j]
    return min(z, z[:1] + z[:0:-1])


def states(n):
    return [(0,) + p for p in permutations(range(1,n)) if p[0] < p[-1]]


def delete_new(c):
    return canon(tuple(x for x in c if x != len(c)-1))


def lr(c,k,start):
    a=list(c)
    inds=[(start+j)%len(c) for j in range(k)]
    vals=[a[i] for i in inds][::-1]
    for i,v in zip(inds,vals): a[i]=v
    return canon(a)


def edges(S,k):
    ids={c:i for i,c in enumerate(S)}
    E=set()
    for i,c in enumerate(S):
        for start in range(len(c)):
            t=lr(c,k,start)
            if t in ids and t != c:
                j=ids[t]
                E.add((min(i,j),max(i,j)))
    return E


def components(S,E):
    adj=[set() for _ in S]
    for i,j in E:
        adj[i].add(j)
        adj[j].add(i)
    comps=[];seen=set()
    for i in range(len(S)):
        if i in seen: continue
        todo=[i];seen.add(i);comp=[]
        while todo:
            v=todo.pop();comp.append(v)
            for j in adj[v]:
                if j not in seen:
                    seen.add(j);todo.append(j)
        comps.append(comp)
    comps.sort(key=lambda c:(-len(c),min(c)))
    return comps


def micro(c,R):
    n=len(c)
    return all((c[i] in R)==(c[(i-1)%n] in R) or
               (c[i] in R)==(c[(i+1)%n] in R) for i in range(n))


def data():
    results=[]
    for n in (5,6,7,8):
        A=states(n)
        B=states(n+1)
        Aidx={x:i for i,x in enumerate(A)}
        parent=[Aidx[delete_new(x)] for x in B]
        fibers=Counter(parent)
        assert set(fibers)==set(range(len(A)))
        assert set(fibers.values())=={n}
        # Reconstruct all children by inserting the new vertex into each edge.
        for p in A:
            children=set()
            for j in range(n):
                c=list(p)
                c.insert(j+1,n)
                children.add(canon(c))
            assert len(children)==n
            assert all(delete_new(t)==p for t in children)
        ea2=edges(A,2)
        ea3=edges(A,3)
        eb3=edges(B,3)
        ca3=components(A,ea3)
        cb3=components(B,eb3)
        ptypes=Counter()
        witness={}
        for i,j in sorted(eb3):
            x,y=parent[i],parent[j]
            pair=(min(x,y),max(x,y))
            if x==y: tag='same-parent'
            elif pair in ea3 and pair in ea2: tag='LR2-and-LR3'
            elif pair in ea3: tag='LR3'
            elif pair in ea2: tag='LR2-only'
            else: tag='neither-LR2-nor-LR3'
            ptypes[tag]+=1
            if tag not in witness:
                witness[tag]={'child_start':B[i], 'child_end':B[j],
                              'parent_start':A[x], 'parent_end':A[y]}
        R=frozenset((1,2,3))
        allowed_A=[c for c in A if micro(c,R)]
        allowed_B=[c for c in B if micro(c,R)]
        aa={x:i for i,x in enumerate(allowed_A)}
        pea3=edges(allowed_A,3)
        peb3=edges(allowed_B,3)
        pmapped=Counter()
        pmicro_invalid=[]
        for child in allowed_B:
            if delete_new(child) not in aa: pmicro_invalid.append(child)
        mwitness=None
        for i,j in sorted(peb3):
            x=delete_new(allowed_B[i]);y=delete_new(allowed_B[j])
            if x not in aa or y not in aa:
                tag='parent-not-MICRO'
                if mwitness is None:
                    mwitness={'child_start':allowed_B[i], 'child_end':allowed_B[j],
                              'parent_start':x, 'parent_end':y}
            elif x==y: tag='same-parent'
            elif (min(aa[x],aa[y]),max(aa[x],aa[y])) in pea3: tag='LR3'
            else:
                tag='not-LR3'
                if mwitness is None:
                    mwitness={'child_start':allowed_B[i], 'child_end':allowed_B[j],
                              'parent_start':x, 'parent_end':y}
            pmapped[tag]+=1
        result={'n_to_nplus1':f'{n}->{n+1}',
                'raw':{'parent_states':len(A),'child_states':len(B),'fiber_size':n,
                'parent_LR3_components':len(ca3),
                'parent_LR3_component_sizes':dict(sorted(Counter(map(len,ca3)).items())),
                'child_LR3_components':len(cb3),
                'child_LR3_component_sizes':dict(sorted(Counter(map(len,cb3)).items())),
                'child_LR3_edges':len(eb3),'projected_edge_types':dict(ptypes),
                'witnesses':witness},
                'micro':{'marked_labels':sorted(R),'parent_states':len(allowed_A),
                'child_states':len(allowed_B),
                'child_states_with_nonadmissible_parent':len(pmicro_invalid),
                'nonadmissible_parent_witness':
                    ({'child':pmicro_invalid[0],'parent':delete_new(pmicro_invalid[0])}
                     if pmicro_invalid else None),
                'parent_LR3_components':len(components(allowed_A,pea3)),
                'child_LR3_components':len(components(allowed_B,peb3)),
                'projected_edge_types':dict(pmapped), 'witness':mwitness}}
        print(json.dumps(result),flush=True)
        results.append(result)
    return results


if __name__=='__main__':
    result={'definition':'Canonical labelled undirected Hamiltonian cycles, parent delete newest label, raw LR2/LR3, fixed-bit MICRO with marked labels {1,2,3}.',
            'results':data()}
    with open('results.json','w') as f:json.dump(result,f,indent=2)
    print('ALL EXACT CHECKS PASSED')
