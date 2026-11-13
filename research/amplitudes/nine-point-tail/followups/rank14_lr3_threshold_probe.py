#!/usr/bin/env python3
"""EHF-AMP-HOL-BRIDGE-05: one canonical LR3 pair and the cut-support poset.

Finite six-fibre theorem; exact rational computations and explicit seed KK
certificates, independently checked by direct residue-image rank elimination.
"""
import json
from itertools import combinations
from pathlib import Path
from rank14_event_pairs import oracle, certificates_for_reference
from signed_orientation_bridge import source, target, KK, D, canon, ranks, axpy

FIBRES=((2,5,7),(2,5,8),(3,5,7),(3,5,8),(4,5,7),(4,5,8))
POSITIVE_SEEDS=((2,5,8),(4,5,7))
NEGATIVE_SEED=(3,5,7)

def block_B(A):
    return tuple(x for x in range(2,9) if x not in A)

def counts(A):
    B=block_B(A)
    return tuple(sum(b<a for b in B) for a in A)

def cut(A):
    return set(w for w in source(A) if w[1]<w[-1])

def lr3_pair(A):
    a,mid,c=A
    b1,b2,b3,b4=block_B(A)
    u=(1,b3,9,b4,a,b1,c,b2,mid)
    v=(1,b4,9,b3,a,b1,c,b2,mid)
    assert u[2]==v[2]==9 and u[1]==v[3] and u[3]==v[1]
    assert u[4:]==v[4:]
    assert all(D(w)[0]==0 for w in (u,v))
    assert all(w not in cut(A) for w in (u,v))
    return tuple(sorted((u,v)))

def transport(w,old,new):
    mapping={1:1,9:9}
    mapping.update(zip(old,new))
    mapping.update(zip(block_B(old),block_B(new)))
    assert len(mapping)==9
    return tuple(mapping[x] for x in w)

def certificate(A):
    pair=lr3_pair(A)
    cert=certificates_for_reference(A,{pair})[pair]
    assert len(set(cert)-set(pair))==len(cert)-2
    return cert

def verify_cert(cert,A,pair):
    admitted=cut(A)
    assert set(cert)-set(pair)<=admitted
    assert all(w not in admitted for w in pair)
    q={};res={}
    idx={w:i for i,w in enumerate(target(A))}
    for w,c in cert.items():
        axpy(q,c,KK(w))
        s,t=D(w)
        if s:axpy(res,c,{idx[canon(t)]:s})
    assert not q and res
    assert ranks(tuple(sorted(admitted))+pair,idx)[2]==15
    return {'certificate_terms':len(cert),'nonzero_residue_coordinates':len(res)}

def main():
    records=[]
    for A in FIBRES:
        pair=lr3_pair(A)
        ids={w:i for i,w in enumerate(target(A))}
        S=tuple(w for w in source(A) if w[1]<w[-1])
        before=ranks(S,ids)[2]
        after=ranks(S+pair,ids)[2]
        expected=(A[0]==4 or A[2]==8)
        assert before==14 and after==(15 if expected else 14)
        records.append({'A':A,'comparison_counts':counts(A),
                        'canonical_lr3_pair':[''.join(map(str,w)) for w in pair],
                        'rank_before':before,'rank_after_pair':after,
                        'pair_repairs':bool(after==15),
                        'geometric_rule_predicts':expected})
        print('A',A,'counts',counts(A),'LR3 works?',after==15,flush=True)
    support_pairs=[]
    allcuts={A:cut(A) for A in FIBRES}
    for A in FIBRES:
        for B in FIBRES:
            smaller=all(counts(A)[i]<=counts(B)[i] for i in range(3))
            transformed={transport(w,A,B) for w in allcuts[A]}
            assert (transformed <= allcuts[B]) == smaller
            if smaller:support_pairs.append([A,B])
    certs={A:certificate(A) for A in POSITIVE_SEEDS}
    witnesses=[]
    for seed in POSITIVE_SEEDS:
        for dest in FIBRES:
            if not all(x<=y for x,y in zip(counts(seed),counts(dest))):continue
            mapped={transport(w,seed,dest):c for w,c in certs[seed].items()}
            m_pair=lr3_pair(dest)
            assert {transport(w,seed,dest) for w in lr3_pair(seed)}==set(m_pair)
            info=verify_cert(mapped,dest,m_pair)
            witnesses.append({'seed':seed,'destination':dest,**info})
            print('certificate',seed,'=>',dest,info,flush=True)
    no_pairs=oracle(NEGATIVE_SEED)
    assert not no_pairs['repair_pairs'] and not no_pairs['one_word_repairs']
    assert (2,5,7) in FIBRES and counts((2,5,7)) < counts(NEGATIVE_SEED)
    triple_witnesses={
        (2,5,7):('162374985','162894735','169473285'),
        (3,5,7):('145678923','163894725','165894723')}
    for A,ss in triple_witnesses.items():
        words=tuple(tuple(map(int,s)) for s in ss)
        S=tuple(sorted(allcuts[A]))
        ids={w:i for i,w in enumerate(target(A))}
        assert len(set(words))==3 and all(w not in S and D(w)[0]==0 for w in words)
        assert ranks(S+words,ids)[2]==15
        for two in combinations(words,2):
            assert ranks(S+two,ids)[2]==14
    result={
        'status':'PASS',
        'scope':'six rank-14 nine-point tail support cuts only',
        'geometric_threshold':'d_L=2 iff k_1=2 or k_3=4; otherwise d_L=3',
        'canonical_lr3_event':'reverse consecutive (b3,9,b4), with B sorted; source words 1 b3 9 b4 a b1 c b2 5 and 1 b4 9 b3 a b1 c b2 5',
        'rows':records,'cut_support_inclusions':support_pairs,
        'positive_seed_certificates':witnesses,
        'exact_positive_seed_relations':{
            ','.join(map(str,A)):
                [[''.join(map(str,w)),str(c)] for w,c in sorted(certs[A].items())]
                for A in POSITIVE_SEEDS},
        'negative_seed':NEGATIVE_SEED,
        'negative_seed_exhaustive_pair_repairs':0,
        'three_word_negative_witnesses':{
            ','.join(map(str,k)):list(v) for k,v in triple_witnesses.items()},
        'limitations':'threshold established on six fibers using two seed exact KK relation certificates, one exhaustive negative seed, and support inclusion; no rank-free proof of seeds or beyond-nine-point rule'
    }
    Path(__file__).with_name('rank14-lr3-threshold-results.json').write_text(
        json.dumps(result,indent=2)+'\n')
    print('PASS: six exact LR3 checks, support poset, transported KK witnesses, and 3-word negative witnesses')

if __name__=='__main__':
    main()
