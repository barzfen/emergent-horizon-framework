#!/usr/bin/env python3
"""Independent LR3 reconstruction and assertions for the growth-lift audit."""
from probe import canon, states, edges, components, delete_new, micro
from opw_audit import audit


def edges_by_swap(S):
    ids={s:i for i,s in enumerate(S)}
    out=set()
    for i,c in enumerate(S):
        for j in range(len(c)):
            t=list(c)
            t[j],t[(j+2)%len(t)]=t[(j+2)%len(t)],t[j]
            t=canon(t)
            if t in ids and t!=c:
                out.add(tuple(sorted((i,ids[t]))))
    return out


if __name__=='__main__':
    expected={5:(12,30,1),6:(60,90,10),7:(360,1260,1),
              8:(2520,10080,35),9:(20160,90720,1)}
    for n,(count,ecount,ccount) in expected.items():
        S=states(n)
        e=edges(S,3)
        assert e == edges_by_swap(S)
        assert (len(S),len(e),len(components(S,e)))==(count,ecount,ccount)
        print('LR3 independently checked:',n,count,ecount,ccount)
    for n,expect in [(7,(72,432,144)),(8,(432,2880,576))]:
        R={1,2,3,4}
        parents=[s for s in states(n) if micro(s,R)]
        children=[s for s in states(n+1) if micro(s,R)]
        bad=[c for c in children if not micro(delete_new(c),R)]
        assert (len(parents),len(children),len(bad))==expect
        if n==7:
            assert bad[0]==(0,1,2,5,6,3,4,7)
        print('MICRO deletion obstruction:',n,n+1,expect)
    r=audit(7,{1,2,3})
    assert r['models']['OPW3']['edge_types']=={
        'identity':576,'FORBIDDEN-parent-edge':1128,'allowed-parent-edge':1296}
    assert r['models']['OPW23']['edge_types']=={
        'identity':1152,'FORBIDDEN-parent-edge':1320,'allowed-parent-edge':1608}
    print('OPW3/OPW23 projection counts confirmed')
    print('ALL VERIFICATION CHECKS PASSED')
