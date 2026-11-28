#!/usr/bin/env python3
"""Exact minimum rank-14 repair size in the two exceptional nine-point fibres.

Standard library only. Modular 3D projections screen candidate triples; every
actual Q-dependence survives the projection, and every candidate is checked
over exact rational numbers before being counted.
Run: python3 rank14_minimal_triples.py
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import prod
from pathlib import Path
import json
import random
from signed_orientation_bridge import source, target, KK, canon, axpy, ranks

P=1000003
FIBRES=((2,5,7),(3,5,7))

def dual_indices(A, idx):
    """Order-preserving transport of the published rank-14 target dual."""
    B=tuple(x for x in range(2,9) if x not in A)
    mapping={1:1,4:A[0],5:A[1],8:A[2],2:B[0],3:B[1],6:B[2],7:B[3]}
    reference=((1,6,5,2,8,3,4,7),(1,6,5,3,8,2,4,7))
    return tuple(idx[canon(tuple(mapping[z] for z in w))] for w in reference)

def signature(q):
    p=min(q)
    return tuple((i,x/q[p]) for i,x in sorted(q.items()))

def setup(A):
    words=tuple(source(A))
    cut=tuple(sorted(w for w in words if w[1]<w[-1]))
    excluded=tuple(sorted(w for w in words if w[1]>w[-1]))
    idx={w:i for i,w in enumerate(target(A))}
    L=dual_indices(A,idx)
    basis={};image={}
    for w in cut:
        q=dict(KK(w))
        d={idx[canon(w[:-1])]:Fraction(1)} if w[-1]==9 else {}
        while q:
            p=min(q);c=q[p]
            if p not in basis:
                basis[p]=({k:v/c for k,v in q.items()},
                          {k:v/c for k,v in d.items()})
                break
            qq,dd=basis[p]
            axpy(q,-c,qq);axpy(d,-c,dd)
        if q:continue
        while d:
            p=min(d);c=d[p]
            if p not in image:
                image[p]={k:v/c for k,v in d.items()}
                break
            axpy(d,-c,image[p])
    assert len(image)==14
    assert all(sum(row.get(j,0) for j in L)==0 for row in image.values())
    quotients=[];defects=[];groups=defaultdict(list);zeros=[]
    for w in excluded:
        q=dict(KK(w));d={}
        for p,(qq,dd) in sorted(basis.items()):
            if p in q:
                c=q[p];axpy(q,-c,qq);axpy(d,-c,dd)
        ell=sum(d.get(j,0) for j in L)
        quotients.append(q);defects.append(ell)
        if not q:
            assert ell==0
            zeros.append(w)
        else:groups[signature(q)].append(w)
    index={w:i for i,w in enumerate(excluded)}
    # No zero-quotient word repairs. Members of any proportional quotient
    # class have proportional defects. Hence no pair can repair the image.
    for members in groups.values():
        i=index[members[0]]
        for w in members[1:]:
            j=index[w]
            factor=quotients[i][min(quotients[i])]/quotients[j][min(quotients[j])]
            assert defects[i]==factor*defects[j]
    assert ranks(cut,idx)[2]==14
    return dict(A=A,cut=cut,excluded=excluded,idx=idx,
                quotients=quotients,defects=defects,groups=groups,
                zeros=zeros,index=index)

def projected_groups(d):
    reps=[members[0] for members in d['groups'].values()]
    q=[d['quotients'][d['index'][w]] for w in reps]
    keys=sorted(set().union(*(set(row) for row in q)))
    for seed in range(971,1020):
        rng=random.Random(seed)
        coeff={k:tuple(rng.randrange(P) for _ in range(3)) for k in keys}
        pts=[]
        for row in q:
            pt=[0,0,0]
            for k,z in row.items():
                den=z.denominator%P
                assert den, 'Chosen prime divides a rational denominator'
                value=(z.numerator%P)*pow(den,-1,P)%P
                for i in range(3):
                    pt[i]=(pt[i]+value*coeff[k][i])%P
            pts.append(tuple(pt))
        degeneracy=False
        for i in range(len(reps)):
            a=pts[i]
            for j in range(i+1,len(reps)):
                b=pts[j]
                cross=((a[1]*b[2]-a[2]*b[1])%P,
                       (a[2]*b[0]-a[0]*b[2])%P,
                       (a[0]*b[1]-a[1]*b[0])%P)
                if cross==(0,0,0):
                    degeneracy=True;break
            if degeneracy:break
        if not degeneracy:return reps,q,pts,seed
    raise AssertionError('No suitable nondegenerate 3D projection')

def exact_dependence(a,b,c):
    keys=sorted(set(a)|set(b)|set(c))
    u=next(k for k in keys if a.get(k,0) or b.get(k,0))
    x=a.get(u,0);y=b.get(u,0)
    for v in keys:
        X=a.get(v,0);Y=b.get(v,0)
        determinant=x*Y-X*y
        if determinant:
            z=c.get(u,0);Z=c.get(v,0)
            alpha=(z*Y-Z*y)/determinant
            beta=(x*Z-X*z)/determinant
            if all(c.get(k,0)==alpha*a.get(k,0)+beta*b.get(k,0) for k in keys):
                return (alpha,beta,Fraction(-1))
            return None
    raise AssertionError('Projective compression left a dependent pair')

def full_certificate(A,cut,words,coeff):
    """Independent explicit KK-source relation with a nonzero target dual."""
    pivots={}
    for w in cut:
        q=dict(KK(w));certificate={w:Fraction(1)}
        while q:
            p=min(q);c=q[p]
            if p not in pivots:
                pivots[p]=({k:v/c for k,v in q.items()},
                           {k:v/c for k,v in certificate.items()})
                break
            pq,pc=pivots[p];axpy(q,-c,pq);axpy(certificate,-c,pc)
    relation={};qtotal={}
    for w,scalar in zip(words,coeff):
        q=dict(KK(w));cert={w:Fraction(1)}
        for p,(pq,pc) in sorted(pivots.items()):
            if p in q:
                c=q[p];axpy(q,-c,pq);axpy(cert,-c,pc)
        axpy(relation,scalar,cert);axpy(qtotal,scalar,q)
    assert not qtotal
    actual_q={};residue={}
    idx={w:i for i,w in enumerate(target(A))}
    for w,c in relation.items():
        axpy(actual_q,c,KK(w))
        if w[-1]==9:axpy(residue,c,{idx[canon(w[:-1])]:Fraction(1)})
    assert not actual_q
    L=sum(residue.get(j,0) for j in dual_indices(A,idx))
    assert L!=0
    assert all(relation.get(w)==c for w,c in zip(words,coeff))
    return {'source_relation_terms':len(relation),
            'nonzero_residue_coordinates':len(residue),
            'dual_on_residue':str(L),
            'source_relation':[[''.join(map(str,w)),str(c)]
                               for w,c in sorted(relation.items())]}

def audit(A):
    d=setup(A)
    reps,q,pts,seed=projected_groups(d)
    positives=[];screened=0;dependent=0
    for i in range(len(reps)-2):
        a=pts[i]
        for j in range(i+1,len(reps)-1):
            b=pts[j]
            cross=((a[1]*b[2]-a[2]*b[1])%P,
                   (a[2]*b[0]-a[0]*b[2])%P,
                   (a[0]*b[1]-a[1]*b[0])%P)
            assert cross!=(0,0,0)
            for k in range(j+1,len(reps)):
                c=pts[k]
                if sum(x*y for x,y in zip(cross,c))%P:continue
                screened+=1
                scalars=exact_dependence(q[i],q[j],q[k])
                if scalars is None:continue
                dependent+=1
                L=sum(s*d['defects'][d['index'][reps[t]]]
                      for s,t in zip(scalars,(i,j,k)))
                if not L:continue
                words=(reps[i],reps[j],reps[k])
                assert ranks(d['cut']+words,d['idx'])[2]==15
                multiplicity=prod(len(d['groups'][signature(q[t])])
                                  for t in (i,j,k))
                positives.append({'words':[''.join(map(str,w)) for w in words],
                                  'scalars':[str(x) for x in scalars],
                                  'dual_value':str(L),'multiplicity':multiplicity})
    assert positives
    first=positives[0]
    triple=tuple(tuple(int(c) for c in word) for word in first['words'])
    assert all(ranks(d['cut']+(w,),d['idx'])[2]==14 for w in triple)
    assert all(ranks(d['cut']+pair,d['idx'])[2]==14
               for pair in combinations(triple,2))
    cert=full_certificate(A,d['cut'],triple,
                          tuple(Fraction(s) for s in first['scalars']))
    result={'A':list(A),'cut_size':len(d['cut']),
            'excluded_size':len(d['excluded']),
            'single_or_pair_repairs':0,'minimum_repair_size':3,
            'projective_quotient_classes':len(reps),
            'zero_quotient_words':len(d['zeros']),
            'projection_prime':P,'projection_seed':seed,
            'screened_projective_triples':screened,
            'exact_dependent_projective_triples':dependent,
            'repairing_projective_triple_classes':len(positives),
            'repairing_actual_triples':sum(x['multiplicity'] for x in positives),
            'repair_classes':positives,'explicit_source_certificate':cert}
    print('A',A,'minimum 3; actual repairing triples',
          result['repairing_actual_triples'],'classes',len(positives),flush=True)
    return result

def main():
    result={'status':'PASS',
            'method':'exact rational KK quotient; lossless modular candidate screen; full certificate and rank verification',
            'fibres':[audit(A) for A in FIBRES]}
    assert [x['repairing_actual_triples'] for x in result['fibres']]==[66,322]
    Path(__file__).with_name('rank14-minimal-triples-results.json').write_text(
        json.dumps(result,indent=2)+'\n')
    print('PASS: both minimum repair sizes are exactly 3')

if __name__=='__main__':main()
