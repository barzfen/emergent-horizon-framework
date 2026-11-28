"""Independent exact gate equations and real-time renewal recurrence; no probe import."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib
import json
import numpy as np


def exact_solve(a,b):
    a=[[F(x) for x in row]+[F(v)] for row,v in zip(a,b)];n=len(a)
    for k in range(n):
        pivot=next(j for j in range(k,n) if a[j][k]);a[k],a[pivot]=a[pivot],a[k]
        for i in range(k+1,n):
            if a[i][k]:
                factor=a[i][k]/a[k][k]
                for j in range(k,n+1):a[i][j]-=factor*a[k][j]
    out=[F(0)]*n
    for i in range(n-1,-1,-1):out[i]=(a[i][-1]-sum(a[i][j]*out[j] for j in range(i+1,n)))/a[i][i]
    return out


def root(parent,i):
    while parent[i]!=i:i=parent[i]
    return i


if __name__=='__main__':
    here=Path(__file__).parent;r=json.loads((here/'results.json').read_text())
    source=here.parent/'rare-channel-02'/'results.json';prior=json.loads(source.read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==r['source_results_sha256']
    assert hashlib.sha256((here/'probe.py').read_bytes()).hexdigest()==r['probe_sha256']
    states=[tuple(c) for c in prior['carrier']['states']];n=len(states);ones=set(prior['ones'])
    edges={tuple(e) for key in ('fast_edges','slow_edges') for e in prior['carrier'][key]}
    support={}
    seen_aux=set();aux_count=0
    for c,d,s,k,first in r['scan_channels']:
        # Read the selected contiguous arc directly, then reconnect its two cut edges.
        tour=states[c];size=len(tour)
        arc=[tour[(s+j)%size] for j in range(k+1)]
        assert len(set(arc))==k+1
        es={frozenset((a,b)) for a,b in zip(tour,tour[1:]+tour[:1])}
        before,after=tour[(s-1)%size],tour[(s+k+1)%size]
        target=(es-{frozenset((before,arc[0])),frozenset((arc[-1],after))})|{frozenset((before,arc[-1])),frozenset((arc[0],after))}
        actual={frozenset((a,b)) for a,b in zip(states[d],states[d][1:]+states[d][:1])}
        assert target==actual and tuple(sorted((c,d))) in edges
        assert all(frozenset((a,b)) in es for a,b in zip(arc,arc[1:]))
        support[tuple(sorted((c,d)))]=k+1
        assert all(i not in seen_aux for i in range(first,first+k))
        seen_aux.update(range(first,first+k));aux_count+=k
    assert len(r['scan_channels'])==2*len(edges)
    assert n+aux_count==r['expanded_states'] and seen_aux==set(range(n,n+aux_count))
    parent=list(range(n))
    for e in prior['carrier']['fast_edges']:
        a,b=map(lambda x:root(parent,x),e);parent[b]=a
    crossing=sum(root(parent,a)!=root(parent,b) for a,b in prior['carrier']['slow_edges'])
    assert crossing==r['support4_edges_crossing_short_components']==76
    assert Counter(support.values())==Counter({2:48,3:112,4:88})
    wall=lambda c:sum((a in ones)!=(b in ones) for a,b in zip(c,c[1:]+c[:1]))
    A=[i for i,c in enumerate(states) if wall(c)==2];position={v:k for k,v in enumerate(A)}
    gate_checks=0;checks=[];exact_mean=None
    for row in r['rows']:
        a=F(row['launch_rate']);d=F(row['abort_rate']);u=F(1)
        trace=np.zeros((n,n));holding=np.ones(n)
        for k in (1,2,3):
            # Backward equations of one interrupted chain with absorbing success/failure.
            M=[[F(0)]*k for _ in range(k)];rhs=[F(0)]*k
            for j in range(k):
                M[j][j]=u+d
                if j+1<k:M[j][j+1]=-u
                else:rhs[j]=u
            probability=exact_solve(M,rhs)[0]
            busy=exact_solve(M,[F(1)]*k)[0]
            assert str(probability)==row['success_probability_by_support'][str(k+1)]
            assert str(busy)==row['mean_busy_time_by_support'][str(k+1)]
            assert a*probability==F(row['idle_trace_rate_by_support'][str(k+1)])
            for (i,j),length in support.items():
                if length==k+1:
                    q=float(a*probability);trace[i,j]+=q;trace[j,i]+=q
                    trace[i,i]-=q;trace[j,j]-=q
                    holding[i]+=float(a*busy);holding[j]+=float(a*busy)
            gate_checks+=1
        killed=-trace[np.ix_(A,A)]
        idle_h=np.linalg.solve(killed,np.ones(len(A)))
        real_h=np.linalg.solve(killed,holding[A])
        assert abs(float(np.mean(idle_h))-row['mean_first_exit_idle_time'])<1e-5
        assert abs(float(np.mean(real_h))-row['mean_first_exit_real_time'])<1e-4
        pi=holding/sum(holding)
        assert abs(float(sum(pi[A]))-row['stationary_visible_two_wall_probability'])<1e-12
        assert abs(float(n/sum(holding))-row['stationary_idle_fraction'])<1e-12
        if d==1 and a==1:
            # One exact whole-carrier recurrence, independently of the 1168-state solve.
            K=[[F(0)]*len(A) for _ in A];h=[F(1)]*len(A)
            for (i,j),length in support.items():
                p=F(1,2)**(length-1);busy=1-p
                for c,z in ((i,j),(j,i)):
                    if c in position:
                        ci=position[c];K[ci][ci]+=p;h[ci]+=busy
                        if z in position:K[ci][position[z]]-=p
            answer=exact_solve(K,h)
            assert all(sum(x*y for x,y in zip(kr,answer))==v for kr,v in zip(K,h))
            exact_mean=sum(answer)/len(A)
            assert abs(float(exact_mean)-row['mean_first_exit_real_time'])<1e-8
        checks.append({'abort_rate':str(d),'launch_rate':str(a),'recurrence_and_stationary_checks':'PASS'})
    out={'status':'PASS','expanded_states':r['expanded_states'],'scan_channels_checked':len(r['scan_channels']),
         'cross_component_obstruction_edges':crossing,'exact_single_gate_checks':gate_checks,
         'parameter_checks':checks,'exact_real_time_exit_mean_at_advance_abort_launch_1':str(exact_mean),
         'probe_sha256':r['probe_sha256'],'verify_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (here/'independent-checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
