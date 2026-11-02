"""MICRO x OPW: exhaustive fixed-colouring induced-graph audit. Python3, numpy, scipy."""
import itertools as it
import json
import hashlib
from pathlib import Path
from collections import Counter
import numpy as np
import scipy
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components


def canon(c):
    c = tuple(c)
    p = c.index(0)
    a = c[p:] + c[:p]
    return min(a, a[:1] + a[:0:-1])


def pi(c):
    return sum(1 << v for v in c[::2])  # odd n: larger parity set identifies unordered pair


def reversal(c, start, length):
    a = list(c)
    slots = [(start+j) % len(c) for j in range(length)]
    for j, v in zip(slots, reversed([a[k] for k in slots])):
        a[j] = v
    return canon(a)


def components(nv, edges):
    if len(edges):
        u, v = edges.T
        a = coo_matrix((np.ones(2*len(u)), (np.r_[u,v], np.r_[v,u])), shape=(nv,nv)).tocsr()
    else:
        a = coo_matrix((nv,nv)).tocsr()
    count, labels = connected_components(a, directed=False)
    return int(count), labels, a


def census(n):
    tours = [(0,)+p for p in it.permutations(range(1,n)) if p[0] < p[-1]]
    index = {c:i for i,c in enumerate(tours)}
    edge_sets = {2:set(), 3:set()}
    for i,c in enumerate(tours):
        for length in (2,3):
            for start in range(n):
                d = reversal(c,start,length)
                assert canon(d) == d
                if pi(d) == pi(c):
                    j = index[d]
                    if i != j:
                        edge_sets[length].add(tuple(sorted((i,j))))
    e3 = np.array(sorted(edge_sets[3]),dtype=int).reshape(-1,2)
    e23 = np.array(sorted(edge_sets[2]|edge_sets[3]),dtype=int).reshape(-1,2)
    base3, lab3, _ = components(len(tours),e3)
    base23, lab23, _ = components(len(tours),e23)
    assert base3 == base23 == {5:5,7:19,9:69}[n]
    assert len(e3) == {5:8,7:600,9:53760}[n]
    assert len(e23) == {5:8,7:840,9:67200}[n]
    assert all(len(set(lab23[lab3==k]))==1 for k in range(base3))
    for labs in (lab3,lab23):
        assert all(len({pi(tours[i]) for i in np.flatnonzero(labs==k)})==1 for k in range(base3))
    ta=np.array(tours)
    # Global bit complement preserves MICRO; choose colour(0)=0, enumerate every other assignment.
    records=[]
    witness=None
    for halfmask in range(1,1 << (n-1)):
        mask=halfmask << 1
        bits=((mask >> ta)&1).astype(np.int8)
        bad=np.sum((bits != np.roll(bits,1,axis=1)) & (bits != np.roll(bits,-1,axis=1)),axis=1)
        keep=bad==0
        ids=np.flatnonzero(keep)
        remap=np.full(len(tours),-1,dtype=int)
        remap[ids]=np.arange(len(ids))
        weight=mask.bit_count()
        r={"mask":mask,"ones_vertices":[v for v in range(n) if (mask>>v)&1],"ones":weight,"minority":min(weight,n-weight),"states":len(ids)}
        if not len(ids):
            r["empty"]=True
            records.append(r)
            continue
        assert np.all(np.sum(bits[ids],axis=1)==weight)
        walls=np.sum(bits != np.roll(bits,1,axis=1),axis=1)
        r["original_chambers_represented"]=len(set(lab3[ids].tolist()))
        labels={}
        for name,edges in (("OPW3",e3),("OPW23",e23)):
            survives=keep[edges[:,0]]&keep[edges[:,1]]
            filtered=edges[survives]
            count,labs,a=components(len(ids),remap[filtered])
            degree=np.diff(a.indptr)
            sizes=np.bincount(labs)
            labels[name]=labs
            # Independent union-find component verification for n<=7, all colourings.
            if n<=7:
                parent=list(range(len(ids)))
                def root(x):
                    while parent[x]!=x:
                        parent[x]=parent[parent[x]]
                        x=parent[x]
                    return x
                for x,y in remap[filtered]:
                    x,y=root(int(x)),root(int(y))
                    if x!=y: parent[y]=x
                assert len({root(x) for x in parent})==count
            # New components must refine original chambers; no-isolation is an induced-state restriction.
            assert all(len(set(lab3[ids[labs==k]].tolist()))==1 for k in range(count))
            assert np.all(walls[filtered[:,0]]==walls[filtered[:,1]])
            r[name]={"edges":len(filtered),"components":count,"largest":int(max(sizes)),"isolated":int(np.sum(degree==0)),"moving_states":int(np.sum(degree>0)),"component_sizes":dict(sorted(Counter(map(int,sizes)).items()))}
        assert r["OPW23"]["components"]<=r["OPW3"]["components"]
        merges={int(k):sorted(set(labels["OPW3"][labels["OPW23"]==k].tolist())) for k in set(labels["OPW23"].tolist())}
        r["OPW23_components_merging_OPW3"]=sum(len(x)>1 for x in merges.values())
        if witness is None and any(len(x)>1 for x in merges.values()):
            k=next(k for k,v in merges.items() if len(v)>1)
            e2=np.array(sorted(edge_sets[2]-edge_sets[3]),dtype=int).reshape(-1,2)
            for x,y in e2:
                if keep[x] and keep[y] and labels["OPW3"][remap[x]]!=labels["OPW3"][remap[y]]:
                    witness={"n":n,"mask":mask,"ones_vertices":r["ones_vertices"],"cycle_A":tours[x],"cycle_B":tours[y],"bits_A":bits[x].tolist(),"bits_B":bits[y].tolist(),"Pi_even_vertices":tours[x][::2],"reason":"MICRO-valid LR2 edge crosses induced OPW3 components"}
                    break
        # Any MICRO-valid LR2 move swaps equal bits; check directly at slot level, independently of edge deduplication.
        if n<=7:
            for i in ids:
                c=tours[i]
                for start in range(n):
                    d=reversal(c,start,2)
                    if pi(c)==pi(d) and keep[index[d]]:
                        assert ((mask>>c[start])&1)==((mask>>c[(start+1)%n])&1)
        records.append(r)
    summary=[]
    for minority in range(1,n//2+1):
        rows=[r for r in records if r["minority"]==minority]
        nonempty=[r for r in rows if r["states"]]
        item={"minority":minority,"assignments":len(rows),"nonempty_assignments":len(nonempty),"states_per_assignment":sorted({r["states"] for r in rows})}
        for name in ("OPW3","OPW23"):
            item[name]={key:sorted({r[name][key] for r in nonempty}) for key in ("edges","components","largest","isolated","moving_states")}
        item["assignments_with_reconnection"]=sum(r.get("OPW23_components_merging_OPW3",0)>0 for r in rows)
        summary.append(item)
    return {"n":n,"baseline":{"states":len(tours),"OPW3_edges":len(e3),"OPW23_edges":len(e23),"chambers":base3},"summary":summary,"reconnection_witness":witness,"colourings":records}


if __name__=="__main__":
    out={"definition":"fixed vertex colours; canonical anchor 0; hard cyclic no-isolation; induced OPW graphs; all nonconstant colourings modulo global bit complement","versions":{"numpy":np.__version__,"scipy":scipy.__version__},"runs":[]}
    for n in (5,7,9):
        result=census(n)
        out["runs"].append(result)
        print(json.dumps({k:v for k,v in result.items() if k!="colourings"}),flush=True)
    out["source_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_name("results.json").write_text(json.dumps(out,indent=2)+"\n")
    print("ALL CHECKS PASSED",flush=True)
