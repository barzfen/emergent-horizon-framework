"""Independent standard-library check: represent cycles by undirected edge sets.

MICRO is checked from each vertex's two neighbours, not binary triple arrays.
Components are computed by direct DFS, not scipy's sparse graph routine.
"""
import itertools
import json
from pathlib import Path


def edges(order):
    return frozenset(frozenset((order[i],order[(i+1)%len(order)])) for i in range(len(order)))


def representative(graph,n):
    neighbours={v:[] for v in range(n)}
    for pair in graph:
        u,v=tuple(pair)
        neighbours[u].append(v)
        neighbours[v].append(u)
    path=[0,min(neighbours[0])]
    while len(path)<n:
        path.append(next(v for v in neighbours[path[-1]] if v!=path[-2]))
    return tuple(path),neighbours


def run(n):
    all_graphs={edges((0,)+p) for p in itertools.permutations(range(1,n))}
    colour=lambda v:int(v in (1,2,3))
    reps={}
    parity={}
    for g in all_graphs:
        order,neighbours=representative(g,n)
        if all(any(colour(v)==colour(w) for w in neighbours[v]) for v in range(n)):
            reps[g]=order
            parity[g]=frozenset(order[::2])
    graph3={g:set() for g in reps}
    graph23={g:set() for g in reps}
    legal_lr2=0
    for g,order in reps.items():
        for length in (2,3):
            for start in range(n):
                # Rotate to put the segment first, reverse prefix; edge encoding ignores gauge.
                rotated=order[start:]+order[:start]
                dest=edges(rotated[:length][::-1]+rotated[length:])
                if dest in reps and parity[dest]==parity[g] and dest!=g:
                    graph23[g].add(dest)
                    if length==3: graph3[g].add(dest)
                    else:
                        assert colour(rotated[0])==colour(rotated[1])
                        legal_lr2+=1
    def component_list(adj):
        unseen=set(adj)
        out=[]
        while unseen:
            seed=unseen.pop()
            comp={seed}
            stack=[seed]
            while stack:
                for v in adj[stack.pop()]:
                    if v not in comp:
                        comp.add(v)
                        unseen.discard(v)
                        stack.append(v)
            out.append(comp)
        return out
    c3=component_list(graph3)
    c23=component_list(graph23)
    a=edges(tuple(range(n)))
    # This is the same undirected graph as swapping labels n-1 and 0 in the identity cycle.
    b=edges((n-1,)+tuple(range(1,n-1))+(0,))
    assert b in graph23[a] and b not in next(c for c in c3 if a in c)
    expected=json.loads(Path(__file__).with_name('results.json').read_text())
    expected=next(x for x in expected['runs'] if x['n']==n)
    expected=next(x for x in expected['colourings'] if x['mask']==14)
    assert len(reps)==expected['states']
    for name,adj,comps in [('OPW3',graph3,c3),('OPW23',graph23,c23)]:
        assert all(u in adj[v] for u in adj for v in adj[u])
        assert len(comps)==expected[name]['components']
        assert sum(map(len,adj.values()))//2==expected[name]['edges']
        assert max(map(len,comps))==expected[name]['largest']
    return {'n':n,'states':len(reps),'OPW3_components':len(c3),'OPW23_components':len(c23),'witness_LR3_component_size':len(next(c for c in c3 if a in c)),'witness_LR23_component_size':len(next(c for c in c23 if a in c)),'checks':'PASS'}


if __name__=='__main__':
    output=[run(n) for n in (7,9)]
    Path(__file__).with_name('independent_checks.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
