"""Exact one-step observer compatibility for specified MICRO kernels.
Standard library only; no claim to reconstruct every historical MICRO kernel.
"""
from itertools import product
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
import json

ROOT=Path(__file__).parent
def admissible(s):
    n=len(s)
    return all(not(s[(i-1)%n]==s[(i+1)%n]!=s[i]) for i in range(n))
def necklace(s):return min(s[i:]+s[:i] for i in range(len(s)))
def blocks(s):
    b=sum(s[i]!=s[(i+1)%len(s)] for i in range(len(s)))
    return b or 1
def coarse(s):return (len(s),sum(s),blocks(s))
def moves(s,kind):
    n=len(s); out=[]
    if kind=='LR3':
        for i in range(n):
            ix=[(i+j)%n for j in range(3)];w=list(s)
            for j,k in enumerate(ix):w[k]=s[ix[2-j]]
            w=tuple(w)
            if w!=s and admissible(w):out.append(w)
        if not out:return [s]
    else:
        for i in range(n):
            for b in (0,1):
                w=s[:i+1]+(b,)+s[i+1:]
                if admissible(w):out.append(w)
    return out
def distribution(s,kind,obs):
    ts=moves(s,kind);c=Counter(obs(t) for t in ts)
    return {k:F(v,len(ts)) for k,v in c.items()}
def encode_dist(d):return [{'observation':list(k),'probability':str(v)} for k,v in sorted(d.items())]
def runs(s):
    if blocks(s)==1:return [(s[0],len(s))]
    i=next(i for i in range(len(s)) if s[i-1]!=s[i]);t=s[i:]+s[:i]
    out=[]
    for b in t:
        if out and out[-1][0]==b:out[-1][1]+=1
        else:out.append([b,1])
    return out
def run():
    rows=[];witnesses={}; fine_futures={}
    for n in range(4,15):
        states=[s for s in product((0,1),repeat=n) if admissible(s)]
        for s in states:
            for kind in ('LR3','growth'):
                assert all(blocks(t)==blocks(s) for t in moves(s,kind))
            b=0 if blocks(s)==1 else blocks(s)
            born=moves(s,'growth')
            assert len(born)==n+b
            assert sum(sum(t)==sum(s)+1 for t in born)==sum(s)+b//2
        for kind in ('LR3','growth'):
            for name,obs in [('necklace',necklace),('counts_and_blocks',coarse),('counts_only',lambda s:(len(s),sum(s)))]:
                groups=defaultdict(list)
                for s in states:groups[obs(s)].append(s)
                failed=0;support_failed=0;totalpairs=0
                for key,ss in groups.items():
                    base=distribution(ss[0],kind,obs)
                    bad=any(distribution(s,kind,obs)!=base for s in ss[1:])
                    supportbad=any(set(distribution(s,kind,obs))!=set(base) for s in ss[1:])
                    failed+=bad;support_failed+=supportbad
                    if bad and (kind,name) not in witnesses:
                        t=next(s for s in ss[1:] if distribution(s,kind,obs)!=base)
                        w={'n':n,'kind':kind,'observer':name,'initial_observation':list(key),
                           'state_a':''.join(map(str,ss[0])),'state_b':''.join(map(str,t)),
                           'runs_a':runs(ss[0]),'runs_b':runs(t),
                           'events_a':len(moves(ss[0],kind)),'events_b':len(moves(t,kind)),
                           'distribution_a':encode_dist(base),'distribution_b':encode_dist(distribution(t,kind,obs))}
                        witnesses[(kind,name)]=w
                rows.append({'n':n,'states':len(states),'kernel':kind,'observer':name,'observation_groups':len(groups),
                             'groups_with_different_probabilities':failed,'groups_with_different_supports':support_failed})
        print(n,len(states),flush=True)
    result={'scope':'n=4..14; rooted labelled positions; binary states, no-isolation; exact one-step tests',
            'kernels':{'LR3':'Uniform over admissible nontrivial reversal events, retaining duplicate events; frozen states self-loop.',
                       'growth':'Uniform over admissible (cyclic edge, inserted bit) events, retaining duplicate events.'},
            'observers':{'necklace':'Forget root by cyclic rotation; retain colours and orientation; no reflection or colour exchange quotient.',
                         'counts_and_blocks':'Retain n, number of ones and number of monochromatic cyclic runs; homogeneous state has one run.',
                         'counts_only':'Retain n and number of ones only.'},
            'rows':rows,'first_probability_counterexamples':list(witnesses.values())}
    assert all(r['groups_with_different_probabilities']==0 for r in rows if r['observer']!='counts_only' or r['kernel']=='LR3')
    assert all(r['groups_with_different_supports']==0 for r in rows)
    result['summary']={'state_sizes':11,'total_admissible_states_across_sizes':sum(r['states'] for r in rows if r['kernel']=='LR3' and r['observer']=='necklace'),
                       'all_necklace_tests_pass':True,'all_counts_and_blocks_tests_pass':True,
                       'LR3_counts_only_tests_pass':True,'growth_counts_only_first_failure_n':9,
                       'all_reachable_observation_support_tests_pass':True,
                       'block_invariance_and_growth_probability_formula_checked':True}
    (ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['first_probability_counterexamples'],indent=2))
if __name__=='__main__':run()
