#!/usr/bin/env python3
"""HODGE-04: exact marker-potential identity for the MICRO model.

Standard library only, Python 3.10+. From repository root:
python code/hodge/hodge_04_audit.py --output data/hodge/hodge-04-results.json

The all-size argument is in formal/hodge/TRANSPORT-POTENTIAL.md.
This finite audit tests an explicit state formula on every admissible edge.
"""
import argparse
from collections import Counter
from itertools import product
from pathlib import Path
import json
import platform

def valid(word):
    n = len(word)
    return all(not(word[i] == word[(i+2)%n] != word[(i+1)%n]) for i in range(n))

def runs(word):
    n = len(word)
    starts = [i for i in range(n) if word[i] != word[(i-1)%n]]
    if not starts:
        return []
    return [(s,(starts[(a+1)%len(starts)]-s)%n,word[s])
            for a,s in enumerate(starts)]

def markers(word):
    """Discard the first two bits of each nonconstant run."""
    n = len(word)
    return tuple(sorted(((s+t)%n,b) for s,length,b in runs(word)
                        for t in range(2,length)))

def cyclic_data(word):
    marked = markers(word)
    n = len(word)
    if not marked:
        return {"potential":0,"signature":(),"markers":marked,
                "canonical_cut_count":0,"E0":0,"E1":0}
    colors = tuple(b for p,b in marked)
    rotations = [colors[a:]+colors[:a] for a in range(len(marked))]
    signature = min(rotations)
    E0 = sum(b == 0 for p,b in marked)
    E1 = len(marked)-E0
    values = []
    for a,rotation in enumerate(rotations):
        if rotation != signature:
            continue
        lifted = marked[a:]+tuple((p+n,b) for p,b in marked[:a])
        values.append(sum((E0 if b else -E1)*p for p,b in lifted))
    assert len(set(values)) == 1, (word,values)
    return {"potential":values[0],"signature":signature,"markers":marked,
            "canonical_cut_count":len(values),"E0":E0,"E1":E1}

def audit(n):
    words = [w for w in product((0,1),repeat=n) if valid(w)]
    data = {w:cyclic_data(w) for w in words}
    edges = []
    wrap_edges = 0
    nonzero_q = 0
    right_checks = Counter()
    example = None
    for w in words:
        assert data[w[1:]+w[:1]]["potential"] == data[w]["potential"]
        chart = runs(w)
        D = len(chart)
        if chart:
            assert data[w]["E1"] == sum(w)-D
            assert data[w]["E0"] == n-sum(w)-D
        for i in range(n):
            z = list(w)
            z[i],z[(i+2)%n] = z[(i+2)%n],z[i]
            v = tuple(z)
            if v not in data or not w < v:
                continue
            edges.append((w,v))
            m = sum(w)
            assert m == sum(v) and D == len(runs(v))
            j = 2*(w[i]-w[(i+2)%n])
            kappa = 1 if w[i] == w[(i+1)%n] else -1
            E = n-2*D
            q = E*j-2*(n-2*m)*kappa
            assert data[v]["potential"]-data[w]["potential"] == q
            assert data[v]["signature"] == data[w]["signature"]
            old,new = set(data[w]["markers"]),set(data[v]["markers"])
            removed,added = old-new,new-old
            assert len(removed) == len(added) == 1
            p,b = next(iter(removed))
            pp,bb = next(iter(added))
            assert b == bb and (pp-p+4*kappa)%n == 0
            # The moving marker crosses no other marker, even at the ring seam.
            positions = {a for a,color in old}
            step = -kappa
            assert all((p+step*t)%n not in positions for t in range(1,5))
            weight = data[w]["E0"] if b else -data[w]["E1"]
            assert q == weight*(-4*kappa)
            wrap_edges += int(p-4*kappa < 0 or p-4*kappa >= n)
            nonzero_q += int(q != 0)
            right_checks[str(kappa)] += 1
            if q and example is None:
                example = {"source":"".join(map(str,w)),
                    "target":"".join(map(str,v)),"move_label":i,
                    "source_potential":data[w]["potential"],
                    "target_potential":data[v]["potential"],
                    "j":j,"kappa":kappa,"n":n,"m":m,"D":D,"E":E,"q":q,
                    "removed_marker":[p,b],"added_marker":[pp,bb],
                    "cyclic_marker_signature":list(data[w]["signature"])}
    # For n>=5, distinct non-self neighbours have a unique move label.
    assert len(edges) == len(set(edges))
    return {"n":n,"states":len(words),"undirected_edges":len(edges),
        "nonzero_potential_difference_edges":nonzero_q,
        "marker_seam_crossing_edges":wrap_edges,
        "orientation_counts":dict(right_checks),
        "mixed_periodic_signature_states":sum(
            d["canonical_cut_count"]>1 and d["E0"]>0 and d["E1"]>0 for d in data.values()),
        "potential_min":min(d["potential"] for d in data.values()),
        "potential_max":max(d["potential"] for d in data.values()),
        "example_nonzero_identity":example,
        "checks":{"edge_identity":"PASS","single_marker_displacement":"PASS",
            "no_marker_passing":"PASS","canonical_cut_independence":"PASS",
            "rotation_invariance":"PASS","cyclic_color_word_invariance":"PASS"}}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    parser.add_argument("--max-n",type=int,default=18)
    args = parser.parse_args()
    if args.max_n < 5:
        parser.error("--max-n must be >=5")
    rows = []
    for n in range(5,args.max_n+1):
        row = audit(n)
        rows.append(row)
        print("n",n,"states",row["states"],"edges",row["undirected_edges"],
              "nonzero dF",row["nonzero_potential_difference_edges"],
              "PASS",flush=True)
    result = {"probe":"EHF-HODGE-04","environment":{"python":platform.python_version()},
        "status":"Exact bounded verification of an explicit formula; all-size proof supplied separately",
        "range":[5,args.max_n],"audit":rows,
        "total_states":sum(r["states"] for r in rows),
        "total_undirected_edges":sum(r["undirected_edges"] for r in rows),
        "total_marker_seam_crossing_edges":sum(r["marker_seam_crossing_edges"] for r in rows),
        "identity":"F(v)-F(w)=(n-2D)j(w,v)-2(n-2m)kappa(w,v)",
        "integer_arithmetic_only":True}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS; total states",result["total_states"],
          "total edges",result["total_undirected_edges"],flush=True)

if __name__ == "__main__":
    main()

