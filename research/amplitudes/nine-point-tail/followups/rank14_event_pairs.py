#!/usr/bin/env python3
"""EHF-AMP-HOL-BRIDGE-03: exact two-word rank-14 repair audit.

Run beside signed_orientation_bridge.py; standard-library Python only.
Enumerate every possible successful two-word repair of all six rank-14
nine-point parity-fibre cuts, then test a reference-fitted ordering template.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
from signed_orientation_bridge import source, target, KK, D, canon, axpy, ranks

FIBRES=((2,5,7),(2,5,8),(3,5,7),(3,5,8),(4,5,7),(4,5,8))
REFERENCE=(4,5,8)

def fibre_basis(A):
    full=tuple(source(A))
    cut=tuple(w for w in full if w[1]<w[-1])
    excluded=tuple(w for w in full if w[1]>=w[-1])
    ids={w:i for i,w in enumerate(target(A))}; Q={}; I={}
    for w in cut:
        q={k:F(v) for k,v in KK(w).items()}
        s,t=D(w);d={ids[canon(t)]:F(s)} if s else {}
        while q:
            p=min(q);c=q[p]
            if p not in Q:
                Q[p]=({x:y/c for x,y in q.items()},
                      {x:y/c for x,y in d.items()})
                break
            axpy(q,-c,Q[p][0]);axpy(d,-c,Q[p][1])
        if q:continue
        while d:
            p=min(d);c=d[p]
            if p not in I:
                I[p]={x:y/c for x,y in d.items()};break
            axpy(d,-c,I[p])
    def remainder(w):
        q={k:F(v) for k,v in KK(w).items()}
        s,t=D(w);d={ids[canon(t)]:F(s)} if s else {}
        for p,(pq,pd) in sorted(Q.items()):
            if p in q:
                c=q[p];axpy(q,-c,pq);axpy(d,-c,pd)
        return q,d
    def image_remainder(d):
        d=dict(d)
        for p,row in sorted(I.items()):
            if p in d:axpy(d,-d[p],row)
        return d
    return cut,excluded,ids,len(Q),len(I),remainder,image_remainder

def signature(q):
    p=min(q);v=q[p]
    return tuple((i,x/v) for i,x in sorted(q.items()))

def oracle(A):
    cut,excluded,idx,kk_rank,image_rank,rem,rimg=fibre_basis(A)
    groups=defaultdict(list);singles=[]
    for w in excluded:
        q,d=rem(w)
        if not q:
            if rimg(d):singles.append(w)
        else:
            groups[signature(q)].append((w,q,d))
    repair=set();dep=0
    for group in groups.values():
        for (u,qu,du),(v,qv,dv) in combinations(group,2):
            factor=qu[min(qu)]/qv[min(qv)];d=dict(du)
            axpy(d,-factor,dv);dep+=1
            if rimg(d):repair.add(tuple(sorted((u,v))))
    return {'cut':cut,'excluded':excluded,'idx':idx,
            'kk_rank':kk_rank,'residue_rank':image_rank,
            'one_word_repairs':singles,'repair_pairs':repair,
            'quotient_dependent_pairs':dep}

def swap(word,a,b):
    return tuple(b if v==a else a if v==b else v for v in word)

def templates(A):
    a,mid,c=A
    bb=tuple(x for x in range(2,9) if x not in A)
    lo=bb[:2];hi=bb[2:];T3=set();T5=set()
    for aa in (a,mid):
        other_a=mid if aa==a else a
        for x in hi:
            y=hi[0] if x==hi[1] else hi[1]
            for u in lo:
                v=lo[0] if u==lo[1] else lo[1]
                T3.add((1,x,9,y,aa,u,c,v,other_a))
                T5.add((1,x,aa,y,9,u,c,v,other_a))
    assert len(T3)==len(T5)==8
    out=set();involutions=((a,mid),tuple(lo),tuple(hi))
    # Fitted after examining reference fibre A=(4,5,8); other fibres
    # are transported structural holdouts, not independent observations.
    for w in T3:
        for bits in product((0,1),repeat=3):
            if (bits[0]+bits[2])%2!=1:continue
            v=w
            for flag,(x,y) in zip(bits,involutions):
                if flag:v=swap(v,x,y)
            if v in T3 and w<v:out.add((w,v))
    for w in T5:
        v=swap(w,a,mid)
        if v in T5 and w<v:out.add((w,v))
    assert len(out)==20
    return out

def remap(word,A):
    B=tuple(x for x in range(2,9) if x not in A)
    lookup={1:1,9:9,4:A[0],5:A[1],8:A[2],
            2:B[0],3:B[1],6:B[2],7:B[3]}
    return tuple(lookup[x] for x in word)

def certificates_for_reference(A,successes):
    cut=tuple(sorted(w for w in source(A) if w[1]<w[-1]))
    basis={}
    for w in cut:
        q={k:F(c) for k,c in KK(w).items()}
        cert={w:F(1)}
        while q:
            p=min(q);c=q[p]
            if p not in basis:
                basis[p]=({x:y/c for x,y in q.items()},
                          {x:y/c for x,y in cert.items()})
                break
            pq,pc=basis[p]
            axpy(q,-c,pq);axpy(cert,-c,pc)
    def rem(w):
        q={k:F(c) for k,c in KK(w).items()}
        cert={w:F(1)}
        for p,(pq,pc) in sorted(basis.items()):
            if p in q:
                c=q[p];axpy(q,-c,pq);axpy(cert,-c,pc)
        return q,cert
    certs={}
    for u,v in successes:
        q1,c1=rem(u);q2,c2=rem(v)
        assert signature(q1)==signature(q2)
        ratio=q1[min(q1)]/q2[min(q2)]
        merged=dict(c1);axpy(merged,-ratio,c2)
        accum={}
        for w,c in merged.items():axpy(accum,c,KK(w))
        assert not accum
        certs[u,v]=merged
    return certs

def main():
    audited=[];positives={};cutsets={}
    for A in FIBRES:
        r=oracle(A);p=templates(A);good=r['repair_pairs']
        assert r['residue_rank']==14 and not r['one_word_repairs']
        assert good<=p
        checked_success=checked_failure=0
        for u,v in sorted(good):
            assert ranks(r['cut']+(u,v),r['idx'])[2]==15
            checked_success+=1
        for u,v in sorted(p-good)[:4]:
            assert ranks(r['cut']+(u,v),r['idx'])[2]==14
            checked_failure+=1
        info={'A':list(A),'cut_size':len(r['cut']),
            'excluded_size':len(r['excluded']),
            'total_excluded_pairs':len(r['excluded'])*(len(r['excluded'])-1)//2,
            'source_KK_rank':r['kk_rank'],'baseline_residue_rank':14,
            'one_word_repairs':0,'two_word_repairs':len(good),
            'quotient_dependent_pairs':r['quotient_dependent_pairs'],
            'template_predicted_pairs':len(p),
            'template_true_positives':len(good&p),
            'template_false_positives':len(p-good),
            'template_false_negatives':len(good-p),
            'direct_positives_checked':checked_success,
            'direct_negatives_checked':checked_failure}
        print('A',A,'repairs',len(good),'template TP',
              len(good&p),'FP',len(p-good),flush=True)
        audited.append(info);positives[A]=good;cutsets[A]=set(r['cut'])
    def inverse_map(word,A):
        B=tuple(x for x in range(2,9) if x not in A)
        to_A={1:1,9:9,A[0]:4,A[1]:5,A[2]:8,
              B[0]:2,B[1]:3,B[2]:6,B[3]:7}
        return tuple(to_A[x] for x in word)
    canonical_success={
        A:{tuple(sorted((inverse_map(u,A),inverse_map(v,A))))
           for u,v in positives[A]}
        for A in FIBRES}
    for A in FIBRES:
        for B in FIBRES:
            if A[0]<=B[0] and A[2]<=B[2]:
                assert canonical_success[A]<=canonical_success[B]
    refcert=certificates_for_reference(REFERENCE,positives[REFERENCE])
    assert len(refcert)==20
    for row in audited:
        A=tuple(row['A']);S=cutsets[A];detected=set()
        for (u,v),cert in refcert.items():
            mu,mv=remap(u,A),remap(v,A)
            if {remap(w,A) for w in cert if w not in (u,v)}<=S:
                detected.add(tuple(sorted((mu,mv))))
        assert detected<=positives[A]
        row['transferred_fixed_certificate_successes']=len(detected)
    ref=next(v for v in audited if v['A']==list(REFERENCE))
    assert ref['total_excluded_pairs']==10296
    assert ref['two_word_repairs']==20
    assert [v['two_word_repairs'] for v in audited]==[0,4,0,11,18,20]
    A=REFERENCE;R=oracle(A);excluded=set(R['excluded'])
    Aset=set(A);Bset=set(range(2,9))-Aset
    naive=set()
    for w in excluded:
        for block in (Aset,Bset):
            for x,y in combinations(sorted(block),2):
                v=swap(w,x,y)
                if v in excluded and w<v:naive.add((w,v))
    assert len(naive)==432 and len(naive&R['repair_pairs'])==12
    output={'status':'PASS',
        'method':'exact rational KK quotient with direct rank validation; template fitted on reference and tested on five transported fibres',
        'reference_two_word_pairs_total':10296,
        'reference_successful_repairs':20,
        'reference_same_block_swap_candidates':432,
        'reference_same_block_swap_true_positives':12,
        'total_direct_positive_checks':sum(x['direct_positives_checked'] for x in audited),
        'total_direct_negative_checks':sum(x['direct_negatives_checked'] for x in audited),
        'monotonic_repair_sets_verified':True,
        'fibres':audited,
        'reference_successful_pairs':[[list(u),list(v)] for u,v in sorted(positives[REFERENCE])],
        'interpretation':'Support/order template catches all 53 repairs but has 67 false positives; exact KK cancellation still needed for a complete selector.'}
    Path(__file__).with_name('rank14-event-pairs-results.json').write_text(
        json.dumps(output,indent=2)+'\n')
    print('PASS: 53 positives, 18 negatives, five-fibre holdout, certificate transfer, monotonicity')

if __name__=='__main__':
    main()
