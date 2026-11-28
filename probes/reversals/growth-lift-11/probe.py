#!/usr/bin/env python3
"""EHF-GROW-LIFT-03: exact finite macrostep/holonomy audit.

Three marked labels, MICRO, canonical Pi, odd sizes 5,7,9.
The relaxed experiment permits at most 2 MICRO-admissible LR2/LR3
microsteps per macrostep, potentially changing Pi, and requires the
projected macrostep endpoints to obey the selected F7 rule.

No probabilistic or physical dynamics is implied.
Standard-library Python only.
"""
from itertools import permutations
from collections import defaultdict, deque, Counter
from pathlib import Path
import json

MARKED=frozenset({1,2,3})

def canon(c):
    c=tuple(c); j=c.index(0); c=c[j:]+c[:j]
    return min(c,c[:1]+c[:0:-1])

def micro(c):
    bits=[x in MARKED for x in c]; n=len(c)
    return all(bits[i]==bits[(i-1)%n] or bits[i]==bits[(i+1)%n] for i in range(n))

def states(n):
    return [(0,)+p for p in permutations(range(1,n))
            if p[0]<p[-1] and micro((0,)+p)]

def pi(c): return frozenset(c[::2])

def lr(c,k,start):
    a=list(c);ind=[(start+j)%len(c) for j in range(k)]
    for slot,val in zip(ind,[c[j] for j in ind][::-1]):a[slot]=val
    return canon(a)

def parent2(c):
    for _ in range(2):c=canon([v for v in c if v!=len(c)-1])
    return c

def marked_flip(c):
    marked=[i for i,v in enumerate(c) if v in MARKED]
    assert marked==list(range(marked[0],marked[0]+3))
    return lr(c,3,marked[0])

def graph(S,pi_restriction):
    index={s:i for i,s in enumerate(S)}
    adj=[{} for _ in S]
    for i,c in enumerate(S):
        for k in (2,3):
            for start in range(len(c)):
                d=lr(c,k,start);j=index.get(d)
                if j is None or i==j or (pi_restriction and pi(c)!=pi(d)):continue
                adj[i][j]=min(adj[i].get(j,99),k)
    assert all(i in adj[j] for i,row in enumerate(adj) for j in row)
    return adj

def components(adj):
    label={};counts=Counter();blocks=defaultdict(list)
    for s in range(len(adj)):
        if s in label:continue
        k=len(counts);todo=[s];label[s]=k;z=0
        while todo:
            u=todo.pop();z+=1;blocks[k].append(u)
            for v in adj[u]:
                if v not in label:label[v]=k;todo.append(v)
        counts[k]=z
    return label,blocks

def bfs(adj,sources,depth=None):
    dist={s:0 for s in sources};pred={s:None for s in sources}
    todo=deque(sorted(sources))
    while todo:
        u=todo.popleft()
        if depth is not None and dist[u]>=depth:continue
        for v in sorted(adj[u]):
            if v not in dist:dist[v]=dist[u]+1;pred[v]=u;todo.append(v)
    return dist,pred

def hungarian(cost):
    """Minimum-cost bijection on square integer matrix; exact Hungarian method."""
    n=len(cost);assert all(len(r)==n for r in cost)
    u=[0]*(n+1);v=[0]*(n+1);p=[0]*(n+1);way=[0]*(n+1)
    for i in range(1,n+1):
        p[0]=i;j0=0;minv=[10**15]*(n+1);used=[False]*(n+1)
        while True:
            used[j0]=True;i0=p[j0];delta=10**15;j1=0
            for j in range(1,n+1):
                if not used[j]:
                    cur=cost[i0-1][j-1]-u[i0]-v[j]
                    if cur<minv[j]:minv[j]=cur;way[j]=j0
                    if minv[j]<delta:delta=minv[j];j1=j
            for j in range(n+1):
                if used[j]:u[p[j]]+=delta;v[j]-=delta
                else:minv[j]-=delta
            j0=j1
            if p[j0]==0:break
        while True:
            j1=way[j0];p[j0]=p[j1];j0=j1
            if j0==0:break
    assign=[None]*n
    for j in range(1,n+1):assign[p[j]-1]=j-1
    assert sorted(assign)==list(range(n))
    return assign,sum(cost[i][assign[i]] for i in range(n))

def count_orbits(f):
    assert sorted(f)==list(range(len(f)))
    seen=set();counts=Counter()
    for start in range(len(f)):
        if start in seen:continue
        x=start;k=0
        while x not in seen:
            seen.add(x);k+=1;x=f[x]
        assert x==start
        counts[k]+=1
    return dict(sorted(counts.items()))

def main():
    X={n:states(n) for n in (5,7,9)}
    assert list(map(lambda n:len(X[n]),(5,7,9)))==[6,72,2160]
    ix={n:{s:i for i,s in enumerate(X[n])} for n in X}
    A7=graph(X[7],True);A9=graph(X[9],True);B9=graph(X[9],False)
    p7=[ix[5][parent2(c)] for c in X[7]]
    p9=[ix[7][parent2(c)] for c in X[9]]
    fib7=defaultdict(list);fib9=defaultdict(list)
    for i,a in enumerate(p7):fib7[a].append(i)
    for i,a in enumerate(p9):fib9[a].append(i)
    assert set(map(len,fib7.values()))=={12}
    assert set(map(len,fib9.values()))=={30}
    f5=[ix[5][marked_flip(c)] for c in X[5]]
    f7=[ix[7][marked_flip(c)] for c in X[7]]
    # Replicate the selected F7 twisted controller from GROW-LIFT-02.
    special=[]
    for a in range(len(X[5])):
        b=f5[a]
        if a>=b:continue
        a_fib=set(fib7[a]);b_fib=set(fib7[b])
        alternate=[(v,u) for v in sorted(b_fib) for u in sorted(A7[v])
                   if u in a_fib and u!=f7[v] and A7[v][u]==2]
        assert len(alternate)==2
        for v,u in alternate:
            f7[v]=u
            special.append((v,u))
    assert count_orbits(f7)=={2:30,4:3}
    assert all(p7[f7[i]]==f5[p7[i]] for i in range(len(f7)))
    assert len(special)==6
    lab,blocks=components(A9)
    stats=[]
    # Both orientations of the six extra LR2 cross-fiber edges.
    extras=set()
    for v,u in special:extras.add(tuple(sorted((v,u))))
    assert len(extras)==6
    for v,u in sorted(extras):
        for source,target in ((v,u),(u,v)):
            AA=fib9[source]; BB=fib9[target]
            d_pi,_=bfs(A9,BB)
            d_raw,_=bfs(B9,BB)
            hpi=Counter(d_pi.get(x,-1) for x in AA)
            hraw=Counter(d_raw.get(x,-1) for x in AA)
            ccounts_a=Counter(lab[x] for x in AA)
            ccounts_b=Counter(lab[x] for x in BB)
            comp_matching_bound=sum(min(ccounts_a[c],ccounts_b[c])
                                    for c in set(ccounts_a)|set(ccounts_b))
            P_A=Counter(pi(X[9][x]) for x in AA)
            P_B=Counter(pi(X[9][x]) for x in BB)
            pi_matching_bound=sum(min(P_A[k],P_B[k]) for k in set(P_A)|set(P_B))
            costs={}
            for depth,adj in ((1,A9),(2,A9),(2,B9),(3,B9),(4,B9)):
                reach=[bfs(adj,[x],depth=depth)[0] for x in AA]
                M=[[(0 if pi(X[9][x])==pi(X[9][y]) else 1) if y in reach[i]
                    else 10000 for y in BB] for i,x in enumerate(AA)]
                pairing,score=hungarian(M)
                reachable_matches=sum(M[i][j]<10000 for i,j in enumerate(pairing))
                costs[f'{"PI" if adj is A9 else "MICRO"}_{depth}']={
                    'maximum_matched':reachable_matches,
                    'minimum_Pi_endpoint_changes':score if reachable_matches==30 else None}
            stats.append({'from':list(X[7][source]),'to':list(X[7][target]),
                          'one_step':hpi.get(1,0),'PI_shortest_distances':dict(sorted(hpi.items())),
                          'MICRO_shortest_distances':dict(sorted(hraw.items())),
                          'PI_component_matching_upper_bound':comp_matching_bound,
                          'same_Pi_endpoint_matching_upper_bound':pi_matching_bound,
                          'matching':costs})
            assert hpi=={-1:3,1:20,2:7},(source,target,hpi)
            assert hraw=={1:28,2:2},(source,target,hraw)
            assert comp_matching_bound==23
            assert pi_matching_bound==26
            assert costs['PI_1']['maximum_matched']==20
            assert costs['PI_2']['maximum_matched']==22
            assert costs['MICRO_2']=={'maximum_matched':30,'minimum_Pi_endpoint_changes':8}
            assert costs['MICRO_4']=={'maximum_matched':30,'minimum_Pi_endpoint_changes':4}
    # Build F9 as a selected bijection which projects to the F7 twist.
    # Each exceptional arc uses an independent min-cost perfect matching,
    # joined by <=2 MICRO-only LR2/LR3 moves per 9-vertex macrostep.
    f9_macro=[None]*len(X[9]);paths={};twisted_count=0;pi_broken=0
    for src in range(len(X[7])):
        target=f7[src]
        A=sorted(fib9[src]);B=sorted(fib9[target]);Bset=set(B)
        if target==ix[7][marked_flip(X[7][src])]:
            for x in A:
                y=ix[9][marked_flip(X[9][x])]
                assert y in Bset
                f9_macro[x]=y
                paths[x]=[x,y]
        else:
            twisted_count+=1
            D=[bfs(B9,[x],depth=2) for x in A]
            # Unreachable pairs have prohibitive cost.
            C=[[(0 if pi(X[9][x])==pi(X[9][y]) else 1) if y in D[i][0]
                   else 10000 for y in B] for i,x in enumerate(A)]
            match,score=hungarian(C)
            assert score==8
            for i,j in enumerate(match):
                x=A[i];y=B[j];f9_macro[x]=y
                d,pred=D[i]
                assert y in d and d[y]<=2
                rev=[y]
                while rev[-1]!=x:rev.append(pred[rev[-1]])
                paths[x]=rev[::-1]
                pi_broken+=(pi(X[9][x])!=pi(X[9][y]))
    assert twisted_count==6
    assert pi_broken==48
    assert all(v is not None for v in f9_macro)
    assert sorted(f9_macro)==list(range(len(X[9])))
    assert all(p9[f9_macro[i]]==f7[p9[i]] for i in range(len(X[9])))
    assert all(len(path)<=3 and all(y in B9[x] for x,y in zip(path,path[1:]))
               and path[0]==i and path[-1]==f9_macro[i] for i,path in paths.items())
    hist=count_orbits(f9_macro)
    witness=None
    for source,target in special:
        AA=fib9[source];BB=set(fib9[target])
        for x in AA:
            if x in [q for q in AA if B9[q].keys() & BB]:continue
            if p9[f9_macro[x]]==target:
                witness={'seven_vertex_arc':[list(X[7][source]),list(X[7][target])],
                         'nine_vertex_microstep_path':[list(X[9][z]) for z in paths[x]],
                         'Pi_before':sorted(pi(X[9][x])),
                         'Pi_after':sorted(pi(X[9][f9_macro[x]]))}
                break
        if witness:break
    assert witness is not None
    result={'definitions':'MICRO, marked vertices {1,2,3}, odd n=5,7,9; Pi-preserving LR2/LR3 versus MICRO-only LR2/LR3, projected two-insertion fibers.',
            'state_counts':{str(n):len(X[n]) for n in X},
            'seven_vertex_controller_orbits':count_orbits(f7),
            'nine_vertex_macro_controller_orbits':hist,
            'twisted_directed_seven_vertex_arcs':len(special),
            'cross_fiber_audits':stats,
            'nine_vertex_macro_controller':{'total_states':len(X[9]),
                'selected_two_step_or_less_MICRO_paths':sum(len(p)<=3 for p in paths.values()),
                'macrosteps_with_end_Pi_change':pi_broken,
                'commutes_with_twisted_F7':True,
                'is_bijective':True,
                'controller_choice':'globally optimized fiber matching; not a local autonomous rule'},
            'sample_repaired_arc':witness}
    Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('ALL AUDITS PASSED')
    print('n7 controller:',count_orbits(f7))
    print('n9 macro controller:',hist)
    print('PI changes out of 2160:',pi_broken)
    print('sample',witness)
    return result

if __name__=='__main__':main()
