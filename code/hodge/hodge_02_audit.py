#!/usr/bin/env python3
"""HODGE-02: MICRO commuting-square complexes and signed binary transport.

Python 3.10+, NumPy. From repository root:
python code/hodge/hodge_02_audit.py --output data/hodge/hodge-02-results.json
"""
import argparse
from collections import Counter, deque
from itertools import combinations, product
from math import gcd
from functools import reduce
from pathlib import Path
import json
import platform
import numpy as np

def valid(w):
    return all(not(w[i] == w[(i+2)%len(w)] != w[(i+1)%len(w)])
               for i in range(len(w)))

def move(w, i):
    z = list(w)
    z[i], z[(i+2)%len(w)] = z[(i+2)%len(w)], z[i]
    v = tuple(z)
    return v if v != w and valid(v) else None

def wall_count(w):
    return sum(a != b for a,b in zip(w,w[1:]+w[:1]))

def primitive(row):
    row = {k:v for k,v in row.items() if v}
    if not row:
        return row
    g = reduce(gcd, (abs(v) for v in row.values()))
    sign = 1 if row[min(row)] > 0 else -1
    return {k:sign*v//g for k,v in row.items()}

def rank_q(rows):
    """Exact sparse fraction-free elimination over Q, with integer gcd reduction."""
    basis = {}
    for original in rows:
        row = primitive(original)
        while row:
            p = min(row)
            if p not in basis:
                basis[p] = row
                break
            other = basis[p]
            a, b = row[p], other[p]
            row = primitive({k:b*row.get(k,0)-a*other.get(k,0)
                             for k in row.keys() | other.keys()})
    return len(basis)

def canon_cycle(c):
    c = tuple(c)
    choices = [c[i:]+c[:i] for i in range(len(c))]
    c = tuple(reversed(c))
    choices += [c[i:]+c[:i] for i in range(len(c))]
    return min(choices)

def build(n):
    words = [w for w in product((0,1),repeat=n) if valid(w)]
    ix = {w:i for i,w in enumerate(words)}
    transitions = [{i:ix[v] for i in range(n) if (v:=move(w,i)) is not None}
                   for w in words]
    edges = sorted({tuple(sorted((a,b))) for a,t in enumerate(transitions) for b in t.values()})
    ei = {e:k for k,e in enumerate(edges)}
    adjacency = [set() for w in words]
    currents = []
    for a,b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
        labels = [i for i,v in transitions[a].items() if v == b]
        # For n>=5 the two changed bit positions identify one move label.
        assert len(labels) == 1
        i = labels[0]
        currents.append(2*(words[a][i]-words[a][(i+2)%n]))
        assert wall_count(words[a]) == wall_count(words[b])
        assert sum(words[a]) == sum(words[b])
    squares = {"window_disjoint":set(), "endpoint_disjoint":set()}
    for a,w in enumerate(words):
        for i,j in combinations(transitions[a],2):
            si, sj = {i,(i+2)%n}, {j,(j+2)%n}
            if si & sj:
                continue
            b,c = transitions[a][i], transitions[a][j]
            di, dj = transitions[b].get(j), transitions[c].get(i)
            if di is None or di != dj or len({a,b,c,di}) != 4:
                continue
            face = canon_cycle((a,b,di,c))
            squares["endpoint_disjoint"].add(face)
            if not ({i,(i+1)%n,(i+2)%n} & {j,(j+1)%n,(j+2)%n}):
                squares["window_disjoint"].add(face)
    triangles = set()
    for a in range(len(words)):
        for b in adjacency[a]:
            if b > a:
                for c in adjacency[a] & adjacency[b]:
                    if c > b:
                        triangles.add((a,b,c))
    return words, ix, transitions, edges, ei, adjacency, currents, squares, triangles

def face_row(face, ei):
    row = {}
    for a,b in zip(face, face[1:]+face[:1]):
        e = ei[tuple(sorted((a,b)))]
        row[e] = row.get(e,0)+(1 if a < b else -1)
    return {e:v for e,v in row.items() if v}

def forest(adjacency, ei, current):
    seen, tree_edges, components, potential, parent = set(), set(), [], {}, {}
    for root in range(len(adjacency)):
        if root in seen:
            continue
        seen.add(root)
        potential[root] = 0
        parent[root] = None
        nodes, queue = [], deque([root])
        while queue:
            a = queue.popleft()
            nodes.append(a)
            for b in sorted(adjacency[a]):
                if b not in seen:
                    seen.add(b)
                    e = ei[tuple(sorted((a,b)))]
                    tree_edges.add(e)
                    potential[b] = potential[a]+(current[e] if a < b else -current[e])
                    parent[b] = a
                    queue.append(b)
        components.append(nodes)
    return components, tree_edges, potential, parent

def closed_path(a,b,parent):
    aa, bb = [], []
    v = a
    while v is not None:
        aa.append(v)
        v = parent[v]
    v = b
    while v is not None:
        bb.append(v)
        v = parent[v]
    common = next(v for v in aa if v in set(bb))
    # a->b along chord, b->common along tree, common->a along tree.
    return [a]+bb[:bb.index(common)+1]+list(reversed(aa[:aa.index(common)]))

def harmonic_check(edges, current, components, faces, ei):
    """Euclidean projection of a proven closed current onto gradients + harmonic."""
    gradient = np.zeros(len(edges))
    for nodes in components:
        if len(nodes) == 1:
            continue
        lookup = {v:i for i,v in enumerate(nodes)}
        subset = [(k,a,b) for k,(a,b) in enumerate(edges) if a in lookup]
        d0 = np.zeros((len(subset),len(nodes)))
        x = np.array([current[k] for k,a,b in subset],dtype=float)
        for row,(k,a,b) in enumerate(subset):
            d0[row,lookup[a]], d0[row,lookup[b]] = -1, 1
        # Fix one vertex potential to 0.
        d = d0[:,1:]
        p = np.linalg.solve(d.T@d, d.T@x)
        fit = d@p
        for row,(k,a,b) in enumerate(subset):
            gradient[k] = fit[row]
    h = np.array(current,dtype=float)-gradient
    divergence = np.zeros(sum(len(c) for c in components))
    for k,(a,b) in enumerate(edges):
        divergence[a] -= h[k]
        divergence[b] += h[k]
    curl_residual = max((abs(sum(s*h[e] for e,s in face_row(f,ei).items()))
                         for f in faces),default=0.)
    assert np.max(np.abs(divergence),initial=0.) < 1e-8
    assert curl_residual < 1e-8
    return {"gradient_energy":float(gradient@gradient),"harmonic_energy":float(h@h),
            "divergence_max":float(np.max(np.abs(divergence),initial=0.)),
            "face_curl_max":float(curl_residual)}

def audit(n):
    words,ix,tr,edges,ei,adj,current,squares,triangles = build(n)
    components, tree, potential, parent = forest(adj,ei,current)
    cycle_rank = len(edges)-len(words)+len(components)
    rules = {"graph_only":set(), **squares,
             "endpoint_squares_plus_triangles":squares["endpoint_disjoint"]|triangles}
    reports = {}
    component_of = {v:k for k,nodes in enumerate(components) for v in nodes}
    component_edges = [[] for _ in components]
    for e,(a,b) in enumerate(edges):
        component_edges[component_of[a]].append(e)
    for name,faces in rules.items():
        rows = [face_row(f,ei) for f in sorted(faces)]
        # d1*d0=0 checked by divergence of each oriented face boundary.
        for row in rows:
            boundary = Counter()
            for e,s in row.items():
                a,b = edges[e]
                boundary[a] -= s
                boundary[b] += s
            assert all(v == 0 for v in boundary.values())
        # Restriction to non-tree edges is injective on the cycle space.
        rank = rank_q([{e:s for e,s in row.items() if e not in tree} for row in rows])
        periods = [sum(current[e]*s for e,s in row.items()) for row in rows]
        reports[name] = {"faces":len(faces),"rank_d1_Q":rank,"beta1_Q":cycle_rank-rank,
                         "nonzero_current_face_periods":sum(p != 0 for p in periods),
                         "max_abs_face_period":max(map(abs,periods),default=0)}
        if name == "endpoint_disjoint":
            component_rows = [[] for _ in components]
            for face,row in zip(sorted(faces),rows):
                component_rows[component_of[face[0]]].append(
                    {e:s for e,s in row.items() if e not in tree})
            mobile = []
            for k,nodes in enumerate(components):
                if len(nodes) == 1:
                    continue
                cr = len(component_edges[k])-len(nodes)+1
                b1 = cr-rank_q(component_rows[k])
                mobile.append({"vertices":len(nodes),"edges":len(component_edges[k]),
                               "ones":sum(words[nodes[0]]),"walls":wall_count(words[nodes[0]]),
                               "beta1_Q":b1})
            reports[name]["mobile_components"] = mobile
    assert all(reports[name]["nonzero_current_face_periods"] == 0
               for name in ["window_disjoint","endpoint_disjoint"])
    periods = []
    component_periods = [[] for _ in components]
    witness = None
    for e,(a,b) in enumerate(edges):
        if e in tree:
            continue
        period = current[e]-(potential[b]-potential[a])
        assert period % n == 0
        periods.append(period)
        component_periods[component_of[a]].append(period)
        if period and (witness is None or abs(period) < abs(witness["period"])):
            path = closed_path(a,b,parent)
            assert path[0] == path[-1]
            total = sum((1 if u < v else -1)*current[ei[tuple(sorted((u,v)))]]
                        for u,v in zip(path,path[1:]))
            assert total == period
            witness = {"period":period,"winding":period//n,
                       "words":["".join(map(str,words[v])) for v in path],
                       "ones":sum(words[a]),"walls":wall_count(words[a])}
    winding_gcd = reduce(gcd,(abs(p//n) for p in periods),0)
    component_details = reports["endpoint_disjoint"]["mobile_components"]
    cursor = 0
    for k,nodes in enumerate(components):
        if len(nodes) > 1:
            component_details[cursor]["winding_image_gcd"] = reduce(
                gcd,(abs(p//n) for p in component_periods[k]),0)
            cursor += 1
    translating_pair = [tuple(int((i-k)%n in (0,1)) for i in range(n)) for k in range(n)]
    pair_loop = translating_pair+[translating_pair[0]]
    pair_period = sum((1 if ix[u] < ix[v] else -1)*current[ei[tuple(sorted((ix[u],ix[v])))]]
                      for u,v in zip(pair_loop,pair_loop[1:]))
    assert pair_period == 2*n
    # Rotation, reflection and complement preserve graph and the two square rules.
    symmetry = {}
    for name,fun,current_sign in [
        ("rotation", lambda w:w[1:]+w[:1],1),
        ("reflection",lambda w:w[::-1],-1),
        ("complement",lambda w:tuple(1-x for x in w),-1)]:
        perm = [ix[fun(w)] for w in words]
        for e,(a,b) in enumerate(edges):
            u,v = perm[a],perm[b]
            ee = ei[tuple(sorted((u,v)))]
            assert current[ee]*(1 if u < v else -1) == current_sign*current[e]
        for rule,faces in squares.items():
            assert {canon_cycle(tuple(perm[a] for a in f)) for f in faces} == faces
        symmetry[name] = "PASS"
    hodge = harmonic_check(edges,current,components,squares["endpoint_disjoint"],ei)
    assert (hodge["harmonic_energy"] > 1e-8) == bool(winding_gcd)
    return {"n":n,"vertices":len(words),"edges":len(edges),"components":len(components),
            "component_size_histogram":dict(sorted(Counter(map(len,components)).items())),
            "graph_cycle_rank":cycle_rank,"rules":reports,
            "transport":{"nonzero_fundamental_periods":sum(p != 0 for p in periods),
                         "winding_image_gcd":winding_gcd,"witness":witness,
                         "translating_pair_period":pair_period,
                         "euclidean_hodge":hodge},
            "symmetries":symmetry}

def growth_audit(n):
    w,ix,tr,edges,ei,adj,*_ = build(n)
    target_words = {v for v in product((0,1),repeat=n+1) if valid(v)}
    def grow(word):
        return (word[0],)+word
    assert all(grow(word) in target_words for word in w)
    failures, witness = 0, None
    for a,b in edges:
        u,v = grow(w[a]),grow(w[b])
        images = {move(u,i) for i in range(n+1)}
        if v not in images:
            failures += 1
            if witness is None:
                witness = {"source":["".join(map(str,w[a])),"".join(map(str,w[b]))],
                           "images":["".join(map(str,u)),"".join(map(str,v))]}
    return {"n":n,"source_edges":len(edges),"nonadjacent_image_edges":failures,
            "witness":witness}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    parser.add_argument("--max-n",type=int,default=12)
    args=parser.parse_args()
    assert 5 <= args.max_n <= 14
    results = []
    for n in range(5,args.max_n+1):
        row = audit(n)
        results.append(row)
        print("n",n,"V",row["vertices"],"E",row["edges"],
              "beta1",{k:v["beta1_Q"] for k,v in row["rules"].items()},flush=True)
    result={"probe":"EHF-HODGE-02","environment":{"python":platform.python_version(),
             "numpy":np.__version__},"audit":results,
            "fixed_insertion_growth":[growth_audit(n) for n in range(5,args.max_n)],
            "status":"Finite exact topology/period checks with numerical Hodge projection"}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS",flush=True)

if __name__ == "__main__":
    main()

