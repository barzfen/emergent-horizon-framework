#!/usr/bin/env python3
"""Independent EHF-HOL-06 event support, phase, and growth audit.

Does not import probe.py. Run after python3 probe.py.
"""
import json
from itertools import permutations
from collections import Counter
from pathlib import Path

MARK={1,2,3}

def rt(seq):
    a=list(seq);t=a.index(0);return tuple(a[t:]+a[:t])

def norm(seq):
    a=rt(seq);return min(a,(0,)+a[:0:-1])

def isvalid(seq):
    n=len(seq)
    return all((seq[i] in MARK)==(seq[(i-1)%n] in MARK) or
               (seq[i] in MARK)==(seq[(i+1)%n] in MARK) for i in range(n))

def allstates(n):
    return [(0,)+p for p in permutations(range(1,n))
            if p[0]<p[-1] and isvalid((0,)+p)]

def apply_support(s,block):
    s=list(s);k=len(block);n=len(s)
    if k<2:return rt(s)
    windows=[[(i+j)%n for j in range(k)] for i in range(n)]
    inds=[w for w in windows if set(s[x] for x in w)==set(block)]
    assert len(inds)==1,(s,block)
    for i,j in zip(inds[0][:k//2],inds[0][::-1][:k//2]):
        s[i],s[j]=s[j],s[i]
    return rt(s)

def deletion(s):
    for v in (len(s)-1,len(s)-2):
        s=rt(x for x in s if x!=v)
    return s

def independent_census(n,pi_filter):
    S=allstates(n);idx={s:i for i,s in enumerate(S)}
    arc_count=Counter();multi={}
    for i,s in enumerate(S):
        for k in (2,3):
            for start in range(n):
                block=tuple(s[(start+j)%n] for j in range(k))
                raw=apply_support(s,block)
                j=idx.get(norm(raw))
                if j is None or i==j:continue
                if pi_filter and set(s[::2])!=set(S[j][::2]):continue
                arc_count[k]+=1
                multi.setdefault((i,j),set()).add((k,block,int(raw!=S[j])))
                if n>5:
                    lhs=deletion(raw)
                    rhs=apply_support(deletion(s),tuple(x for x in block if x<n-2))
                    assert lhs==rhs,(n,s,block,lhs,rhs)
                    x=norm(deletion(s));y=norm(lhs)
                    a=int(raw!=S[j])
                    ap=int(apply_support(x,[v for v in block if v<n-2])!=y)
                    gs=int(deletion(s)!=x);gt=int(deletion(S[j])!=y)
                    assert a==ap^gs^gt
    return {'states':len(S),
            'directed_events':sum(len(v) for v in multi.values()),
            'directed_pairs':len(multi),
            'multiplicity':dict(Counter(map(len,multi.values())))}

def witness_audit(witness,events):
    assert len(witness)==len(events)+1
    source=tuple(witness[0]['cycle']);actual=source
    for i,m in enumerate(events):
        assert norm(actual)==tuple(witness[i]['cycle'])
        assert int(actual!=tuple(witness[i]['cycle']))==witness[i]['orientation']
        actual=apply_support(actual,m['block'])
        assert norm(actual)==tuple(witness[i+1]['cycle'])
        assert int(actual!=tuple(witness[i+1]['cycle']))==witness[i+1]['orientation']
    assert actual==(0,)+source[:0:-1]

if __name__=='__main__':
    r=json.loads(Path(__file__).with_name('results.json').read_text())
    for model in ('OPW','MICRO'):
        for n in (5,7,9):
            observed=independent_census(n,model=='OPW')
            expected=r['models'][f'{model}_{n}']
            assert all(observed[k]==expected[k]
                       for k in ('states','directed_events'))
            if expected['witness']:
                witness_audit(expected['witness'],expected['witness_events'])
            print(model,n,observed,'witness verified')
    print('ALL INDEPENDENT DIRECT-EVENT AND GROWTH IDENTITIES PASSED')
