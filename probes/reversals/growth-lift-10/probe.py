#!/usr/bin/env python3
"""EHF-GROW-LIFT-02: exact growth-compatible local LR2/LR3 audit; Python 3."""
import json
from collections import Counter, defaultdict
from itertools import permutations
from math import factorial
from pathlib import Path

R={1,2,3}
def canon(c):
    c=tuple(c); i=c.index(0); c=c[i:]+c[:i]
    return min(c,c[:1]+c[:0:-1])
def micro(c):
    return all((c[i] in R)==(c[(i-1)%len(c)] in R) or
               (c[i] in R)==(c[(i+1)%len(c)] in R) for i in range(len(c)))
def states(n):
    return [(0,)+p for p in permutations(range(1,n))
            if p[0]<p[-1] and micro((0,)+p)]
def lr(c,k,i):
    a=list(c); positions=[(i+j)%len(c) for j in range(k)]
    for pos,value in zip(positions,[c[t] for t in positions][::-1]): a[pos]=value
    return canon(a)
def pi(c):return frozenset(c[::2])
def edges(S,ks):
    index={s:i for i,s in enumerate(S)}; E=set()
    for i,c in enumerate(S):
        for k in ks:
            for start in range(len(c)):
                d=lr(c,k,start); j=index.get(d)
                if j is not None and i!=j and pi(c)==pi(d):
                    E.add(tuple(sorted((i,j))))
    return E
def ancestor(c):
    for _ in range(2): c=canon([v for v in c if v!=len(c)-1])
    return c
def marked_flip(c):
    ix=[i for i,v in enumerate(c) if v in R]
    assert len(ix)==3 and ix[1]==ix[0]+1 and ix[2]==ix[1]+1
    return lr(c,3,ix[0])
def orbit_hist(f):
    assert set(f)==set(range(len(f)))
    seen=set(); lengths=Counter()
    for i in range(len(f)):
        if i in seen:continue
        x=i; k=0
        while x not in seen:seen.add(x); x=f[x]; k+=1
        assert x==i
        lengths[k]+=1
    return dict(sorted(lengths.items()))
def run():
    X={n:states(n) for n in (5,7,9)}
    assert [len(X[n]) for n in (5,7,9)]==[6,72,2160]
    J={n:{s:i for i,s in enumerate(X[n])} for n in X}
    G={n:{'OPW3':edges(X[n],(3,)), 'OPW23':edges(X[n],(2,3))} for n in X}
    assert [[len(G[n][m]) for m in ('OPW3','OPW23')] for n in (5,7,9)]==[[3,3],[54,84],[3000,4080]]
    F={n:[J[n][marked_flip(s)] for s in X[n]] for n in X}
    assert all(all(tuple(sorted((i,F[n][i]))) in G[n]['OPW3'] for i in range(len(X[n]))) for n in X)
    p7=[J[5][ancestor(c)] for c in X[7]]
    p9=[J[7][ancestor(c)] for c in X[9]]
    assert all(p7[F[7][i]]==F[5][p7[i]] for i in range(len(p7)))
    assert all(p9[F[9][i]]==F[7][p9[i]] for i in range(len(p9)))
    fibers7=defaultdict(list);fibers9=defaultdict(list)
    for i,p in enumerate(p7): fibers7[p].append(i)
    for i,p in enumerate(p9): fibers9[p].append(i)
    assert set(map(len,fibers7.values()))=={12} and set(map(len,fibers9.values()))=={30}
    # Each X5 marked-flip edge lifts to 12 LR3 matching edges plus two LR2 edges.
    twist=F[7][:]; squares=[]
    for a,b in sorted(G[5]['OPW3']):
        cross={m:{(i,j) for i,j in G[7][m] if {p7[i],p7[j]}=={a,b}}
               for m in ('OPW3','OPW23')}
        assert len(cross['OPW3'])==12 and len(cross['OPW23'])==14
        extra=cross['OPW23']-cross['OPW3'];assert len(extra)==2
        affected=set()
        for i,j in extra:
            v,u=(i,j) if p7[i]==b else (j,i)
            assert p7[v]==b and p7[u]==a and F[7][v]!=u
            twist[v]=u
            affected.update((v,u,F[7][v],F[7][u]))
        assert len(affected)==4
        squares.append([list(X[7][i]) for i in sorted(affected)])
    assert orbit_hist(twist)=={2:30,4:3}
    assert all(p7[twist[i]]==F[5][p7[i]] for i in range(len(twist)))
    assert all(tuple(sorted((i,twist[i]))) in G[7]['OPW23'] for i in range(len(twist)))
    changed=[i for i in range(len(twist)) if twist[i]!=F[7][i]]
    assert len(changed)==6
    # For each new LR2 arrow at X7, inspect all 30 source lifts at X9.
    obstruction=[]
    for v in changed:
        u=twist[v]; A=set(fibers9[v]); B=set(fibers9[u])
        cross={(i,j) for i,j in G[9]['OPW23']
               if (i in A and j in B) or (i in B and j in A)}
        hits={i for i,j in cross if i in A}|{j for i,j in cross if j in A}
        assert len(cross)==20 and len(hits)==20
        obstruction.append({'source_parent':list(X[7][v]),'target_parent':list(X[7][u]),
            'child_fiber':30,'edges_to_target':20,'unreachable_children':10,
            'witness':list(X[9][min(A-hits)])})
    # Exhaustive obstruction for both orientations of every extra cross-fiber
    # LR2 edge, not merely for the six arcs used by the selected controller.
    all_extra=[]
    for i,j in sorted(G[7]['OPW23']-G[7]['OPW3']):
        if tuple(sorted((p7[i],p7[j]))) not in G[5]['OPW3']:
            continue
        for src,dst in ((i,j),(j,i)):
            A=set(fibers9[src]);B=set(fibers9[dst])
            e={(a,b) for a,b in G[9]['OPW23'] if
               (a in A and b in B) or (a in B and b in A)}
            hits={a for a,b in e if a in A}|{b for a,b in e if b in A}
            assert len(e)==20 and len(hits)==20
            all_extra.append({'source_parent':list(X[7][src]),
                              'target_parent':list(X[7][dst]),
                              'unreachable_children':30-len(hits)})
    assert len(all_extra)==12
    result={'states':{str(n):len(X[n]) for n in X},
            'move_edges':{str(n):{m:len(e) for m,e in G[n].items()} for n in X},
            'marked_flip_orbits':{str(n):orbit_hist(F[n]) for n in X},
            'two_step_fibers':{'5->7':12,'7->9':30},
            'opw23_twist_n7_orbits':orbit_hist(twist),
            'four_state_square_examples':squares,
            'twisted_LR2_arcs':len(changed),
            'twist_7to9_obstructions':obstruction,
            'all_directed_extra_LR2_obstructions':all_extra}
    return result
if __name__=='__main__':
    r=run()
    Path(__file__).with_name('results.json').write_text(json.dumps(r,indent=2)+'\n')
    print('PASS',r['states'],r['marked_flip_orbits'],r['opw23_twist_n7_orbits'])
    print('OBSTRUCTIONS',len(r['twist_7to9_obstructions']), 'each blocks 10 of 30 children')
