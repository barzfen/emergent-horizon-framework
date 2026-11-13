#!/usr/bin/env python3
"""EHF-HOL-06: exact event-labelled orientation/deletion audit.

Retain cyclic ordered vertex lists as reversal-event labels. Check
MICRO-only and MICRO+Pi OPW23 at sizes 5,7,9. Standard library only.
"""
from collections import Counter, defaultdict, deque
from itertools import permutations
import json
from pathlib import Path

MARK=frozenset((1,2,3))

def rooted(c):
    c=tuple(c);k=c.index(0);return c[k:]+c[:k]

def canonical(c):
    c=rooted(c);return min(c,c[:1]+c[:0:-1])

def micro(c):
    n=len(c)
    return all(((c[i] in MARK)==(c[(i-1)%n] in MARK)) or
               ((c[i] in MARK)==(c[(i+1)%n] in MARK)) for i in range(n))

def carrier(n):
    return [(0,)+p for p in permutations(range(1,n))
            if p[0]<p[-1] and micro((0,)+p)]

def pival(c):return frozenset(c[::2])

def reverse_by_start(c,k,st):
    c=list(c);idx=[(st+t)%len(c) for t in range(k)]
    block=tuple(c[i] for i in idx)
    for i,v in zip(idx,block[::-1]):c[i]=v
    return rooted(c),block

def reverse_by_support(c,block):
    c=list(c);n=len(c);k=len(block)
    if k<=1:return rooted(c)
    starts=[st for st in range(n)
            if {c[(st+j)%n] for j in range(k)}==set(block)]
    assert len(starts)==1,(c,block,starts)
    return reverse_by_start(c,k,starts[0])[0]

def ancestor(c):
    for label in (len(c)-1,len(c)-2):
        c=rooted(x for x in c if x!=label)
    return c

def graph(n,opw):
    S=carrier(n);ids={c:i for i,c in enumerate(S)}
    d=defaultdict(list);adj=[set() for _ in S]
    for i,c in enumerate(S):
        for k in (2,3):
            for start in range(n):
                outcome,block=reverse_by_start(c,k,start)
                j=ids.get(canonical(outcome))
                if j is None or i==j or (opw and pival(c)!=pival(S[j])):
                    continue
                voltage=int(outcome!=S[j])
                d[i,j].append((k,block,voltage))
                adj[i].add(j)
    assert all((j,i) in d and
               sorted(x[-1] for x in ev)==sorted(x[-1] for x in d[j,i])
               for (i,j),ev in d.items())
    return S,ids,d,adj

def components(g):
    assigned=set();res=[]
    for root in range(len(g)):
        if root in assigned:continue
        assigned.add(root);stack=[root];part=[]
        while stack:
            u=stack.pop();part.append(u)
            for v in g[u]:
                if v not in assigned:assigned.add(v);stack.append(v)
        res.append(part)
    return res

def orientation_classes(parts,d,g):
    count=0;first=None
    for part in parts:
        pot={part[0]:0};stack=[part[0]];bad=False
        while stack:
            u=stack.pop()
            for v in g[u]:
                for _,_,a in d[u,v]:
                    nxt=pot[u]^a
                    if v not in pot:pot[v]=nxt;stack.append(v)
                    elif pot[v]!=nxt:bad=True
        if bad:
            count+=1
            if first is None:first=part[0]
    return count,first

def sample_loop(d,src):
    out=defaultdict(list)
    for (i,j),recs in d.items():
        for k,block,a in recs:out[i].append((j,k,block,a))
    q=deque([(src,0)]);pred={(src,0):None};move={}
    while q:
        a,phase=q.popleft()
        for b,k,block,voltage in out[a]:
            nxt=(b,phase^voltage)
            if nxt not in pred:
                pred[nxt]=(a,phase);move[nxt]=(k,block,voltage)
                if nxt==(src,1):
                    chain=[nxt]
                    while chain[-1]!=(src,0):chain.append(pred[chain[-1]])
                    chain.reverse()
                    return chain,[move[x] for x in chain[1:]]
                q.append(nxt)
    return None,None

def system_row(n,opw):
    S,ids,d,g=graph(n,opw)
    parts=components(g)
    positive,root=orientation_classes(parts,d,g)
    path,moves=sample_loop(d,root) if positive else (None,None)
    row={'n':n,'restriction':'MICRO+Pi' if opw else 'MICRO-only',
         'states':len(S),'unoriented_edges':sum(map(len,g))//2,
         'directed_events':sum(map(len,d.values())),
         'components':len(parts),'holonomy_nonzero_components':positive,
         'event_counts_per_ordered_pair':dict(Counter(map(len,d.values()))),
         'witness':([{'cycle':list(S[i]),'orientation':b}
                     for i,b in path] if path else None),
         'witness_events':([{'length':k,'block':list(block),'voltage':v}
                           for k,block,v in moves] if moves else None)}
    return row,(S,ids,d,g)

def check_projection(low,high):
    lowS,lowid,lowD,_=low;hiS,hiid,hiD,_=high
    n=len(lowS[0]);N=len(hiS[0]);assert N==n+2
    counts=Counter();example={};total=0
    for (i,j),records in hiD.items():
        s=hiS[i]
        for k,block,a in records:
            total+=1
            st=next(st for st in range(N)
                    if tuple(s[(st+z)%N] for z in range(k))==block)
            outcome,actual=reverse_by_start(s,k,st)
            assert actual==block and canonical(outcome)==hiS[j]
            psource=ancestor(s);ptarget=ancestor(outcome)
            retained=tuple(v for v in block if v<n)
            assert reverse_by_support(psource,retained)==ptarget
            ps=canonical(psource);pt=canonical(ptarget)
            x=lowid[ps];y=lowid[pt]
            permitted=x==y or (x,y) in lowD
            cat='collapse' if x==y else (
                'legal-parent' if permitted else 'forbidden-Pi')
            counts[k,len(retained),cat]+=1
            if (k,len(retained),cat) not in example:
                example[k,len(retained),cat]={
                    'child':list(s),'child_target':list(hiS[j]),
                    'child_block':list(block),'parent':list(ps),
                    'parent_target':list(pt),'projected_block':list(retained)}
            # Orientation voltage is natural under deletion up to chart gauge.
            projected_out=reverse_by_support(ps,retained)
            assert canonical(projected_out)==pt
            pa=int(projected_out!=pt)
            gauge_src=int(psource!=ps)
            gauge_dst=int(ancestor(hiS[j])!=pt)
            assert a==(gauge_src^pa^gauge_dst),(n,N,s,block)
            assert reverse_by_support(outcome,block)==rooted(s)
    return {'lower':n,'higher':N,'directed_events':total,
            'categories':{'/'.join(map(str,k)):v for k,v in sorted(counts.items())},
            'events_that_fail_parent_Pi':
                sum(v for key,v in counts.items() if key[2]=='forbidden-Pi'),
            'inverse_and_oriented_deletion_verified':True,
            'witness_examples':{'/'.join(map(str,k)):v for k,v in example.items()}}

def main():
    data={};sys={}
    for opw in (True,False):
        for n in (5,7,9):
            row,g=system_row(n,opw)
            sys[opw,n]=g
            key=f'{"OPW" if opw else "MICRO"}_{n}'
            data[key]=row
            print(key, row['directed_events'],
                  'directed events, orientation classes',
                  row['holonomy_nonzero_components'],flush=True)
    projections={}
    for opw in (True,False):
        for n in (5,7):
            row=check_projection(sys[opw,n],sys[opw,n+2])
            key=f'{"OPW" if opw else "MICRO"}_{n+2}_to_{n}'
            projections[key]=row
            print(key,'forbidden:',row['events_that_fail_parent_Pi'],flush=True)
    assert all(projections[f'MICRO_{m}_to_{m-2}']
               ['events_that_fail_parent_Pi']==0 for m in (7,9))
    assert projections['OPW_7_to_5']['events_that_fail_parent_Pi']==0
    assert projections['OPW_9_to_7']['events_that_fail_parent_Pi']==2640
    assert data['OPW_5']['event_counts_per_ordered_pair']=={2:6}
    assert data['OPW_5']['holonomy_nonzero_components']==3
    assert data['MICRO_9']['holonomy_nonzero_components']==1
    Path(__file__).with_name('results.json').write_text(
        json.dumps({'models':data,'projections':projections},indent=2)+'\n')
    print('ALL EVENT, INVERSE, HOLONOMY AND GROWTH CHECKS PASSED')

if __name__=='__main__':main()
