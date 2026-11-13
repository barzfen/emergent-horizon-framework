#!/usr/bin/env python3
"""EHF-HOL-05: exact F2 orientation-voltage audit on MICRO/OPW3 and OPW23.

No nonstandard Python dependencies; run using Python 3.10+.
"""
from collections import Counter, defaultdict, deque
from itertools import permutations
import json
from pathlib import Path

MARKED = {1, 2, 3}


def canon(seq):
    a = tuple(seq)
    k = a.index(0)
    a = a[k:] + a[:k]
    return min(a, a[:1] + a[:0:-1])


def micro(a):
    n = len(a)
    return all((a[i] in MARKED) == (a[(i-1) % n] in MARKED) or
               (a[i] in MARKED) == (a[(i+1) % n] in MARKED)
               for i in range(n))


def states(n):
    return [(0,)+p for p in permutations(range(1,n))
            if p[0] < p[-1] and micro((0,)+p)]


def event(c, length, start):
    a = list(c)
    positions = [(start+j) % len(a) for j in range(length)]
    for i,v in zip(positions, [c[t] for t in positions][::-1]):
        a[i] = v
    idx = a.index(0)
    return tuple(a[idx:] + a[:idx])  # oriented; NOT reflection-quotiented


def build(S, lengths):
    ids = {c:i for i,c in enumerate(S)}
    directed = defaultdict(list)
    for i,c in enumerate(S):
        for length in lengths:
            for start in range(len(c)):
                raw = event(c,length,start)
                d = canon(raw)
                j = ids.get(d)
                if j is None or i == j or set(c[::2]) != set(d[::2]):
                    continue
                bit = int(raw != d)
                directed[i,j].append((length,start,bit))
    edges = sorted({tuple(sorted((i,j))) for i,j in directed})
    adj = [set() for _ in S]
    for i,j in edges:
        adj[i].add(j); adj[j].add(i)
    ambiguous = sum(len({x[2] for x in records}) > 1
                    for records in directed.values())
    reciprocal = all((j,i) in directed and
                     {x[2] for x in records} == {x[2] for x in directed[j,i]}
                     for (i,j),records in directed.items())
    return edges,adj,directed,ambiguous,reciprocal


def components(adj):
    seen = set();out=[]
    for i in range(len(adj)):
        if i in seen:continue
        seen.add(i);todo=[i];comp=[]
        while todo:
            v=todo.pop();comp.append(v)
            for w in adj[v]:
                if w not in seen:seen.add(w);todo.append(w)
        out.append(comp)
    return out


def simple_cycles(adj,n):
    """Simple length-n cycles once, up to rotation and reversal."""
    out=[]
    for root in range(len(adj)):
        def dfs(path):
            if len(path) == n:
                if root in adj[path[-1]] and path[1] < path[-1]:
                    out.append(tuple(path))
                return
            for v in adj[path[-1]]:
                if v > root and v not in path:
                    dfs(path+[v])
        for v in adj[root]:
            if v > root:dfs([root,v])
    return out


def xor_rank(bitsets):
    pivots={}
    for word in bitsets:
        while word:
            top=word.bit_length()-1
            if top in pivots:word ^= pivots[top]
            else:pivots[top]=word;break
    return len(pivots)


def shortest_orientation_loop(adj,events,source):
    start=(source,0);goal=(source,1)
    pred={start:None}; q=deque([start])
    while q:
        v,b=q.popleft()
        for w in sorted(adj[v]):
            dest=(w,b^events[v,w][0][2])
            if dest in pred:continue
            pred[dest]=(v,b)
            if dest == goal:
                path=[dest]
                while path[-1] != start:path.append(pred[path[-1]])
                return path[::-1]
            q.append(dest)
    return None


def oriented_ancestor(c):
    for label in (len(c)-1, len(c)-2):
        c=[x for x in c if x!=label]
        i=c.index(0)
        c=tuple(c[i:]+c[:i])
    return c


def ancestor(c):
    return canon(oriented_ancestor(c))


def analyze(n,lengths):
    S=states(n)
    edges,adj,ev,amb,recip=build(S,lengths)
    assert not amb and recip, (n,lengths,amb,recip)
    comps=components(adj)
    beta=len(edges)-len(S)+len(comps)
    ids={e:i for i,e in enumerate(edges)}
    row={'vertices':n,'moves':list(lengths),'states':len(S),'edges':len(edges),
         'components':len(comps),'graph_H1':beta,
         'component_sizes':dict(Counter(map(len,comps))),
         'oriented_edge_lift_ambiguous':amb,'inverse_consistent':recip}
    faces=[]
    for length in (4,5,6,8):
        cyc=simple_cycles(adj,length)
        nonzero=0
        for c in cyc:
            if sum(ev[a,b][0][2] for a,b in zip(c,c[1:]+c[:1]))%2:
                nonzero+=1
        row['simple_'+str(length)+'_cycles']=len(cyc)
        row['nonzero_orientation_'+str(length)+'_cycles']=nonzero
        if length in (4,6,8):assert nonzero==0
        if length in (4,6):
            for c in cyc:
                bits=0
                for a,b in zip(c,c[1:]+c[:1]):
                    bits^=1<<ids[tuple(sorted((a,b)))]
                faces.append(bits)
            rank=xor_rank(faces)
            row['filled_4_6_rank_to_'+str(length)]=rank
            row['H1_after_faces_to_'+str(length)]=beta-rank
    nontrivial=[];best=None
    for comp in comps:
        p=shortest_orientation_loop(adj,ev,comp[0])
        if p:
            nontrivial.append(len(comp))
            if best is None or len(p)<len(best):best=p
    row['nontrivial_orientation_components']=len(nontrivial)
    row['nontrivial_orientation_component_sizes']=dict(Counter(nontrivial))
    row['shortest_found_orientation_loop']=len(best)-1 if best else None
    row['witness']=[{'cycle':list(S[i]),'orientation_bit':b} for i,b in best] if best else None
    return row,S,edges,adj,ev


def growth_check(lower,upper):
    loS,loE,loA,loEv=lower
    hiS,hiE,hiA,hiEv=upper
    loIds={c:i for i,c in enumerate(loS)}
    pi=[loIds[ancestor(c)] for c in hiS]
    allowed=set(loE)
    good=set();bad=set();vertical=0
    for i,j in hiE:
        p,q=pi[i],pi[j]
        if p==q: good.add((i,j));vertical+=1
        elif tuple(sorted((p,q))) in allowed:good.add((i,j))
        else:bad.add((i,j))
    graph=[set() for _ in hiS]
    for a,b in good:graph[a].add(b);graph[b].add(a)
    comps=components(graph)
    nontrivial=sum(shortest_orientation_loop(graph,hiEv,c[0]) is not None for c in comps)
    assert nontrivial==0
    component_of={v:k for k,block in enumerate(comps) for v in block}
    potential={}
    for block in comps:
        root=block[0];potential[root]=0;todo=[root]
        while todo:
            u=todo.pop()
            for v in graph[u]:
                val=potential[u]^hiEv[u,v][0][2]
                if v not in potential:potential[v]=val;todo.append(v)
                else:assert potential[v]==val
    assert all(component_of[a]!=component_of[b] for a,b in bad)
    crossed=defaultdict(set)
    for a,b in bad:
        pair=tuple(sorted((component_of[a],component_of[b])))
        crossed[pair].add(potential[a]^potential[b]^hiEv[a,b][0][2])
    two_crossing_pairs=sum(len(signs)==2 for signs in crossed.values())
    if len(loE)==84:assert two_crossing_pairs>0
    # Verify oriented projection agrees up to choice of canonical chart.
    for a,b in good:
        for x,y in ((a,b),(b,a)):
            p,q=pi[x],pi[y]
            length,start,alpha=hiEv[x,y][0]
            raw=event(hiS[x],length,start)
            up_src=oriented_ancestor(hiS[x]);up_dst=oriented_ancestor(raw)
            source_chart=int(canon(up_src)!=up_src)
            target_chart=int(canon(up_dst)!=up_dst)
            if p==q:
                assert source_chart==target_chart
            else:
                assert (source_chart^target_chart)==loEv[p,q][0][2]
    return {'total_edges':len(hiE),'projectable_edges':len(good),
            'nonprojectable_edges':len(bad),'vertical_edges':vertical,
            'compatible_components':len(comps),
            'compatible_components_with_nontrivial_orientation':nontrivial,
            'all_nonprojectable_edges_connect_distinct_compatible_components':True,
            'minimum_nonprojectable_edges_per_nonzero_holonomy_loop':(2 if two_crossing_pairs else None),
            'component_pairs_witnessing_two_crossings':two_crossing_pairs,
            'oriented_projection_consistent_on_projectable_edges':True}


def main():
    results=[];systems={}
    for n in (7,9):
        for lengths in ((3,),(2,3)):
            row,S,E,A,ev=analyze(n,lengths)
            results.append(row);systems[n,lengths]=(S,E,A,ev)
            print(n,lengths,'graph H1',row['graph_H1'],
                  'after 4/6',row['H1_after_faces_to_6'],
                  'orientation-positive components',row['nontrivial_orientation_components'],
                  'shortest loop',row['shortest_found_orientation_loop'],flush=True)
    growth={str(k):growth_check(systems[7,k],systems[9,k])
            for k in ((3,),(2,3))}
    print('GROWTH',growth,flush=True)
    results_data={'setup':'MICRO marked labels {1,2,3}, canonical undirected cycles, Pi-preserving OPW3/OPW23',
                  'systems':results,'growth':growth}
    Path(__file__).with_name('results.json').write_text(json.dumps(results_data,indent=2)+'\n')
    assert [x['nontrivial_orientation_components'] for x in results]==[0,3,0,9]
    assert [x['H1_after_faces_to_6'] for x in results]==[0,3,0,51]
    assert growth['(2, 3)']['nonprojectable_edges']==1320
    print('ALL EXACT CHECKS PASSED',flush=True)


if __name__=='__main__':main()
