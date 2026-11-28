#!/usr/bin/env python3
"""Cross-scale MICRO+Pi OPW3/OPW23 projection audit for odd n -> n+2."""
import json
from collections import Counter
from probe import states, delete_new, edges, components, micro


def pi(c):
    return frozenset(c[::2])


def audit(n, R):
    old=[c for c in states(n) if micro(c,R)]
    new=[c for c in states(n+2) if micro(c,R)]
    old_idx={c:i for i,c in enumerate(old)}
    old_E2=edges(old,2);old_E3=edges(old,3)
    new_E2=edges(new,2);new_E3=edges(new,3)
    old_valid={k:{(i,j) for i,j in ee if pi(old[i])==pi(old[j])}
               for k,ee in [(2,old_E2),(3,old_E3)]}
    new_valid={k:{(i,j) for i,j in ee if pi(new[i])==pi(new[j])}
               for k,ee in [(2,new_E2),(3,new_E3)]}
    out={}
    for model,ks in [('OPW3',[3]),('OPW23',[2,3])]:
        p_edges=set().union(*(old_valid[k] for k in ks))
        c_edges=set().union(*(new_valid[k] for k in ks))
        types=Counter(); witness={}
        invalid_parent=0
        parents=[]
        for c in new:
            p=delete_new(delete_new(c))
            parents.append(old_idx.get(p))
            invalid_parent += (p not in old_idx)
        for i,j in sorted(c_edges):
            a=parents[i];b=parents[j]
            if a is None or b is None: tag='parent-invalid'
            elif a==b: tag='identity'
            elif (min(a,b),max(a,b)) in p_edges: tag='allowed-parent-edge'
            else: tag='FORBIDDEN-parent-edge'
            types[tag]+=1
            if tag not in witness:
                witness[tag]={'old_start':old[a] if a is not None else None,
                              'old_end':old[b] if b is not None else None,
                              'new_start':new[i], 'new_end':new[j]}
        out[model]={'parent_components':len(components(old,p_edges)),
                    'child_components':len(components(new,c_edges)),
                    'parent_edges':len(p_edges),'child_edges':len(c_edges),
                    'invalid_parent_states':invalid_parent,
                    'edge_types':dict(types),'witnesses':witness}
    return {'n_to_nplus2':f'{n}->{n+2}','marked_labels':sorted(R),
            'parent_states':len(old),'child_states':len(new),'models':out}


if __name__=='__main__':
    a=[audit(n,frozenset((1,2,3))) for n in (5,7)]
    with open('opw-results.json','w') as f:json.dump(a,f,indent=2)
    for row in a:
        print(row['n_to_nplus2'],row['parent_states'],row['child_states'])
        for model,d in row['models'].items():
            print(model,{k:v for k,v in d.items() if k!='witnesses'})
            print('forbidden witness',d['witnesses'].get('FORBIDDEN-parent-edge'))
