"""Independent exact reconstruction from draft v1.5 sections 2--9.
Python standard library only. No saved EHF matrices or numerical ranks.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from collections import Counter
from functools import lru_cache
from pathlib import Path
from math import prod
import json, time

OUT=Path(__file__).parent

def can(w):
    rev=(w[0],)+tuple(reversed(w[1:]))
    return min(w,rev)

@lru_cache(None)
def shuffles(a,b):
    if not a: return (b,)
    if not b: return (a,)
    return tuple((a[0],)+s for s in shuffles(a[1:],b))+tuple((b[0],)+s for s in shuffles(a,b[1:]))

@lru_cache(None)
def kk(w):
    n=max(w); i=w.index(n); a=w[1:i]; b=w[i+1:]
    sign=(-1)**len(b)
    return {s:F(sign) for s in shuffles(a,tuple(reversed(b)))}

def fibre(A,n):
    odd=tuple(A)+((9,) if n==9 else ())
    even=tuple(x for x in range(2,9) if x not in A)
    words=[]
    for e in permutations(odd):
        for o in permutations(even):
            tail=[]
            for i in range(4):
                tail.append(o[i])
                if i<len(e): tail.append(e[i])
            w=(1,)+tuple(tail)
            if w[1]<w[-1]: words.append(w)
    return sorted(words)

def axpy(v,c,u):
    for k,x in u.items():
        y=v.get(k,0)+c*x
        if y: v[k]=y
        elif k in v: del v[k]

def norm(v,c):
    return {k:x/c for k,x in v.items()}

def add_basis(v,basis):
    v=dict(v)
    while v:
        p=min(v); c=v[p]
        if p not in basis:
            basis[p]=norm(v,c); return True
        axpy(v,-c,basis[p])
    return False

def rref(rows):
    basis={}
    for r in rows: add_basis(r,basis)
    for p in sorted(basis,reverse=True):
        for q in sorted(basis):
            if q<p and p in basis[q]: axpy(basis[q],-basis[q][p],basis[p])
    return [basis[p] for p in sorted(basis)]

def same(a,b):
    return rref(a)==rref(b)

def ranklaw(A):
    a,b,c=A
    if b<=4: return 0 if c<=5 else (2 if c==6 else 9)
    if b==5: return 8 if c==6 else 14
    return 15

def pt(w,z):
    return F(1,prod(z[a]-z[b] for a,b in zip(w,w[1:]+w[:1])))

def direct_residue(w,z):
    """Remove the unique (z9-z1) denominator factor and set z9=z1.
    Evaluates the product directly, independently of target canonicalisation.
    """
    edges=list(zip(w,w[1:]+w[:1]))
    if (9,1) not in edges and (1,9) not in edges: return F(0)
    pole=(9,1) if (9,1) in edges else (1,9)
    sign=1 if pole==(9,1) else -1
    values=dict(z); values[9]=values[1]
    return F(sign,prod(values[a]-values[b] for a,b in edges if (a,b)!=pole))

def encode(v): return [[k,str(x)] for k,x in sorted(v.items())]

def run():
    t0=time.perf_counter(); records=[]; representatives={}; checks=Counter()
    target_ref=fibre((2,3,4),8); ref_index={w:i for i,w in enumerate(target_ref)}
    q8ref=[kk(w) for w in target_ref]
    assert len(target_ref)==72 and len(rref(q8ref))==57
    zsets=[{i:i for i in range(1,10)}, {i:i*i+2 for i in range(1,10)}]
    for A in combinations(range(2,9),3):
        start=time.perf_counter(); source=fibre(A,9); target=fibre(A,8)
        tidx={w:i for i,w in enumerate(target)}
        qcols=[kk(w) for w in source]
        dcols=[{tidx[can(w[:-1])]:F(1)} if w[-1]==9 else {} for w in source]
        pre=Counter(next(iter(d)) for d in dcols if d)
        assert len(target)==72 and len(pre)==72 and set(pre.values())=={2}
        checks['active_source_states']+=sum(bool(d) for d in dcols)
        checks['source_states']+=len(source)
        # Exact comparison with the rational-factor collision residue.
        for z in zsets:
            vals=[pt(w,z) for w in target]
            for w,d in zip(source,dcols):
                assert direct_residue(w,z)==sum(v*vals[j] for j,v in d.items())
                checks['direct_residue_equalities']+=1
        # Column elimination with source and deletion certificates carried along.
        pivots={}; ibasis={}; relation_dim=0
        for j in sorted(range(len(source)),key=lambda j:(not bool(dcols[j]),source[j])):
            q=dict(qcols[j]); d=dict(dcols[j]); cert={j:F(1)}
            while q:
                p=min(q); c=q[p]
                if p not in pivots:
                    pivots[p]=(norm(q,c),norm(d,c),norm(cert,c)); break
                pq,pd,pc=pivots[p]
                axpy(q,-c,pq); axpy(d,-c,pd); axpy(cert,-c,pc)
            if q: continue
            relation_dim+=1
            while d:
                p=min(d); c=d[p]
                if p not in ibasis:
                    ibasis[p]=(norm(d,c),norm(cert,c)); break
                pd,pc=ibasis[p]; axpy(d,-c,pd); axpy(cert,-c,pc)
        images=[v[0] for p,v in sorted(ibasis.items())]
        certs=[v[1] for p,v in sorted(ibasis.items())]
        assert len(images)==ranklaw(A)
        # Independently multiply retained certificates into the original columns.
        for image,cert in zip(images,certs):
            qs={}; ds={}; qt={}
            for j,c in cert.items(): axpy(qs,c,qcols[j]); axpy(ds,c,dcols[j])
            for j,c in image.items(): axpy(qt,c,kk(target[j]))
            assert not qs and ds==image and not qt
            checks['certified_image_generators']+=1
            # Two common-numerator MHV checks (negative helicities 2,3).
            for z in zsets:
                numerator=(z[2]-z[3])**4
                val=sum(c*numerator*direct_residue(source[j],z) for j,c in cert.items())
                lower=sum(c*numerator*pt(target[j],z) for j,c in image.items())
                assert val==lower==0
                checks['MHV_residue_relation_checks']+=1
        mapping={1:1,**dict(zip(A,(2,3,4))),**dict(zip(sorted(set(range(2,9))-set(A)),(5,6,7,8)))}
        transport={j:ref_index[can(tuple(mapping[x] for x in w))] for j,w in enumerate(target)}
        transported=rref([{transport[j]:c for j,c in v.items()} for v in images])
        dim=len(images)
        if dim in representatives: assert same(representatives[dim],transported)
        else: representatives[dim]=transported
        rec={'A':A,'source_size':len(source),'source_rank':len(pivots),
             'source_relation_dimension':relation_dim,'image_dimension':dim,
             'active_states':144,'target_size':len(target),
             'source_orderings':source,'target_orderings':target,
             'image_basis':[encode(v) for v in images],
             'source_lifts':[encode(v) for v in certs]}
        records.append(rec)
        print(json.dumps({k:rec[k] for k in ['A','source_size','source_relation_dimension','image_dimension']}),flush=True)
    V=representatives
    assert set(V)=={0,2,8,9,14,15}
    assert same(V[8]+V[9],V[14])
    assert len(rref(V[8]+V[9]))==14 and 8+9-14==3
    assert same(V[2]+V[8],V[8]) and same(V[2]+V[9],V[9])
    for row in V[15]:
        total={}
        for j,c in row.items(): axpy(total,c,q8ref[j])
        assert not total
    # Construct exact character multiplicities via eigenspace equations on coefficients.
    chars={}
    gmaps=[]
    for a,b in [(2,3),(5,6),(7,8)]:
        swap=lambda x:a if x==b else b if x==a else x
        gmaps.append({j:ref_index[can(tuple(swap(x) for x in w))] for j,w in enumerate(target_ref)})
    from itertools import product
    for dim,rows in sorted(V.items()):
        mult=[]
        for chi in product([1,-1],repeat=3):
            columns=[]
            for row in rows:
                equations={}
                for g,(sgn,mp) in enumerate(zip(chi,gmaps)):
                    for j,c in row.items():
                        axpy(equations,F(1),{(g,mp[j]):c})
                        axpy(equations,F(-sgn),{(g,j):c})
                columns.append(equations)
            mult.append(dim-len(rref(columns)))
        chars[str(dim)]=mult
    expected={'0':[0]*8,'2':[0,0,1,0,0,0,0,1], '8':[0,0,1,1,1,1,2,2],
              '9':[0,1,1,3,0,1,1,2], '14':[0,1,1,3,1,2,3,3], '15':[0,1,1,3,1,3,3,3]}
    assert chars==expected
    summary={'status':'PASS','seconds':time.perf_counter()-t0,'checks':dict(checks),
             'rank_multiplicities':dict(Counter(r['image_dimension'] for r in records)),
             'target_relation_dimension':15,'six_space_collapse':True,
             'lattice_verified':True,'character_multiplicities':chars,
             'scope':'Reference (1,9) chart. No full 72-chart, minimum-support, or 21-template recertification.',
             'deletion_convention':'+1 before anchor, -1 after anchor; n=8 reflection unsigned. Only before-anchor branch occurs in canonical source fibres.'}
    (OUT/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
    (OUT/'certificates.json').write_text(json.dumps({'fibres':records,'reference_orderings':target_ref,'reference_images':{str(d):[encode(v) for v in rows] for d,rows in V.items()}},indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__': run()
