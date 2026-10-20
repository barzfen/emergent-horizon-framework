#!/usr/bin/env python3
"""HODGE-03: run coordinates and boundary winding on MICRO square complexes.

Run from repository root:
python code/hodge/hodge_03_audit.py --output data/hodge/hodge-03-results.json
Requires hodge_02_audit.py beside this file (and NumPy via that module).
All topology and period calculations in this audit are exact integers/rationals.
"""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd
from functools import reduce
from pathlib import Path
import json
import platform
import hodge_02_audit as h2

def runs(word):
    n = len(word)
    starts = [i for i in range(n) if word[i] != word[(i-1)%n]]
    if not starts:
        return []
    return [(s, (starts[(k+1)%len(starts)]-s)%n, word[s])
            for k,s in enumerate(starts)]

def run_neighbours(word):
    """Predict moves from length-two runs and a donor of length >=3."""
    n = len(word)
    chart = runs(word)
    result = set()
    for k,(s,length,bit) in enumerate(chart):
        if length != 2:
            continue
        for shift,donor in [(1,chart[(k+1)%len(chart)][1]),
                            (-1,chart[(k-1)%len(chart)][1])]:
            if donor < 3:
                continue
            v = list(word)
            if shift == 1:
                v[s],v[(s+2)%n] = 1-bit,bit
            else:
                v[(s-1)%n],v[(s+1)%n] = bit,1-bit
            result.add(tuple(v))
    return result

def moment_01(word):
    return sum(i for i in range(len(word))
               if word[i] == 0 and word[(i+1)%len(word)] == 1)

def local_overlap_certificate():
    """Disjoint endpoint swaps with overlapping windows are at offsets +/-1.

    For offset +1 write (a,b,1-a,1-b) and external bits (e,f).
    No assignment makes the original, both single swaps and double swap
    simultaneously free of 010/101 on this six-bit interval.
    """
    def linear_valid(w):
        return all(not(w[i] == w[i+2] != w[i+1]) for i in range(len(w)-2))
    report = []
    for a,b in product((0,1),repeat=2):
        count = 0
        for e,f in product((0,1),repeat=2):
            original = (e,a,b,1-a,1-b,f)
            corners = []
            for first,second in product((0,1),repeat=2):
                w = list(original)
                if first:
                    w[1],w[3] = w[3],w[1]
                if second:
                    w[2],w[4] = w[4],w[2]
                corners.append(tuple(w))
            count += all(map(linear_valid,corners))
        assert count == 0
        report.append({"four_bits":[a,b,1-a,1-b],
                       "external_assignments":4,"all_four_corners_valid":count})
    return report

def edge_integral(path, values, edge_index):
    return sum((1 if a < b else -1)*values[edge_index[tuple(sorted((a,b)))]]
               for a,b in zip(path,path[1:]))

def audit(n):
    words,ix,tr,edges,ei,adj,j,squares,triangles = h2.build(n)
    for a,w in enumerate(words):
        predicted = run_neighbours(w)
        actual = {words[b] for b in tr[a].values()}
        assert predicted == actual
    assert squares["endpoint_disjoint"] == squares["window_disjoint"]
    kappa = []
    for a,b in edges:
        label = next(i for i,v in tr[a].items() if v == b)
        k = 1 if words[a][label] == words[a][(label+1)%n] else -1
        kappa.append(k)
        assert (k-(moment_01(words[b])-moment_01(words[a]))) % n == 0
        assert h2.wall_count(words[a]) == h2.wall_count(words[b])
    comps,tree,pk,parent = h2.forest(adj,ei,kappa)
    comps_j,tree_j,pj,parent_j = h2.forest(adj,ei,j)
    assert comps == comps_j and tree == tree_j
    ci = {v:c for c,nodes in enumerate(comps) for v in nodes}
    rows = [[] for _ in comps]
    edge_counts = Counter()
    periods = [[] for _ in comps]
    face_counts = Counter()
    for face in sorted(squares["endpoint_disjoint"]):
        row = h2.face_row(face,ei)
        assert sum(s*kappa[e] for e,s in row.items()) == 0
        assert sum(s*j[e] for e,s in row.items()) == 0
        c = ci[face[0]]
        rows[c].append({e:s for e,s in row.items() if e not in tree})
        face_counts[c] += 1
    missed_witness = None
    for e,(a,b) in enumerate(edges):
        c = ci[a]
        edge_counts[c] += 1
        if e in tree:
            continue
        kp = kappa[e]-(pk[b]-pk[a])
        jp = j[e]-(pj[b]-pj[a])
        assert kp % n == 0 and jp % n == 0
        periods[c].append((kp,jp))
        if kp and not jp and missed_witness is None:
            path = h2.closed_path(a,b,parent)
            assert edge_integral(path,kappa,ei) == kp
            assert edge_integral(path,j,ei) == jp
            missed_witness = {
                "words":["".join(map(str,words[v])) for v in path],
                "ones":sum(words[a]),"walls":h2.wall_count(words[a]),
                "boundary_period":kp,"binary_period":jp,
                "initial_runs":[{"start":s,"length":r,"bit":b}
                                 for s,r,b in runs(words[a])]}
    mobile = []
    for c,nodes in enumerate(comps):
        if len(nodes) == 1:
            continue
        cycle_rank = edge_counts[c]-len(nodes)+1
        rank = h2.rank_q(rows[c])
        beta1 = cycle_rank-rank
        kgcd = reduce(gcd,(abs(kp//n) for kp,jp in periods[c]),0)
        jgcd = reduce(gcd,(abs(jp//n) for kp,jp in periods[c]),0)
        # Do not assume the conjecture: retain a counterexample if encountered.
        slope = None
        for kp,jp in periods[c]:
            if kp:
                slope = Fraction(jp,kp)
                break
        proportional = slope is not None and all(
            Fraction(jp) == slope*kp for kp,jp in periods[c])
        m = sum(words[nodes[0]])
        walls = h2.wall_count(words[nodes[0]])
        excess = n-2*walls
        assert excess > 0
        predicted_slope = Fraction(2*(n-2*m),excess)
        period_identity = all(excess*jp == 2*(n-2*m)*kp for kp,jp in periods[c])
        mobile.append({"vertices":len(nodes),"edges":edge_counts[c],
            "square_faces":face_counts[c],"rank_d1_Q":rank,"beta1_Q":beta1,
            "ones":sum(words[nodes[0]]),"walls":h2.wall_count(words[nodes[0]]),
            "boundary_winding_image_gcd":kgcd,
            "binary_winding_image_gcd":jgcd,
            "binary_to_boundary_period_ratio":str(slope) if slope is not None else None,
            "predicted_period_ratio":str(predicted_slope),
            "period_identity_pass":period_identity,
            "periods_proportional":proportional,
            "representative":"".join(map(str,words[nodes[0]])),
            "representative_run_lengths":[r for s,r,b in runs(words[nodes[0]])]})
    symmetries = {}
    for name,fun,sign in [
            ("rotation",lambda w:w[1:]+w[:1],1),
            ("reflection",lambda w:w[::-1],-1),
            ("complement",lambda w:tuple(1-x for x in w),1)]:
        permutation = [ix[fun(w)] for w in words]
        for e,(a,b) in enumerate(edges):
            u,v = permutation[a],permutation[b]
            image = ei[tuple(sorted((u,v)))]
            assert (1 if u < v else -1)*kappa[image] == sign*kappa[e]
        symmetries[name] = "PASS"
    counterexamples = [x for x in mobile if x["beta1_Q"] != 1 or
                       x["boundary_winding_image_gcd"] == 0]
    return {"n":n,"vertices":len(words),"edges":len(edges),
            "components":len(comps),"square_faces":len(squares["endpoint_disjoint"]),
            "mobile_components":mobile,"total_beta1_Q":sum(c["beta1_Q"] for c in mobile),
            "components_missed_by_binary_transport":sum(
                c["binary_winding_image_gcd"] == 0 for c in mobile),
            "components_missed_by_boundary_transport":sum(
                c["boundary_winding_image_gcd"] == 0 for c in mobile),
            "run_rule_checks":len(words),"symmetries":symmetries,
            "missed_cycle_witness":missed_witness,"conjecture_counterexamples":counterexamples}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    parser.add_argument("--max-n",type=int,default=18)
    args = parser.parse_args()
    if args.max_n < 5:
        parser.error("--max-n must be >=5")
    local = local_overlap_certificate()
    results = []
    for n in range(5,args.max_n+1):
        row = audit(n)
        results.append(row)
        print("n",n,"V",row["vertices"],"E",row["edges"],
              "mobile",len(row["mobile_components"]),"beta1",row["total_beta1_Q"],
              "missed(binary,boundary)",
              (row["components_missed_by_binary_transport"],
               row["components_missed_by_boundary_transport"]),flush=True)
    failures = sum(len(r["conjecture_counterexamples"]) for r in results)
    result = {"probe":"EHF-HODGE-03","environment":{"python":platform.python_version()},
        "status":"Exact finite audit; all-size conjecture unproved",
        "range":[5,args.max_n],"local_overlap_certificate":local,"audit":results,
        "conjecture_counterexample_count":failures,
        "period_identity_failure_count":sum(not c["period_identity_pass"]
            for r in results for c in r["mobile_components"]),
        "notes":["All ranks are over Q; no integral torsion computation.",
                 "Boundary winding detects rational H1 on scanned mobile components.",
                 "One-dimensional H1 does not imply circle homotopy type."]}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("COMPLETE; conjecture counterexamples:",failures,flush=True)

if __name__ == "__main__":
    main()

