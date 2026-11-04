"""Explicit interrupted assembly gates over the retained REV-02 carrier."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def canon(c):
    c=tuple(c);i=c.index(0);c=c[i:]+c[:i]
    return min(c,c[:1]+c[:0:-1])


def reverse(c,s,length):
    a=list(c);ix=[(s+j)%len(c) for j in range(length)]
    for i,v in zip(ix,reversed([c[j] for j in ix])):a[i]=v
    return canon(a)


def walls(c,ones):
    return sum((a in ones)!=(b in ones) for a,b in zip(c,c[1:]+c[:1]))


def run():
    parent=Path(__file__).parent.parent/'rare-channel-02'/'results.json'
    prior=json.loads(parent.read_text());states=[tuple(c) for c in prior['carrier']['states']]
    index={c:i for i,c in enumerate(states)};size=len(states);ones=set(prior['ones'])
    pairs={}
    for i,c in enumerate(states):
        for length in (2,3,4):
            for start in range(len(c)):
                d=reverse(c,start,length)
                if d in index and d!=c:
                    pair=tuple(sorted((i,index[d])))
                    pairs[pair]=min(pairs.get(pair,9),length)
    assert sorted(e for e,l in pairs.items() if l<=3)==[tuple(e) for e in prior['carrier']['fast_edges']]
    assert sorted(e for e,l in pairs.items() if l==4)==[tuple(e) for e in prior['carrier']['slow_edges']]
    group={i:j for j,g in enumerate(prior['carrier']['fast_groups']) for i in g}
    cross=sum(group[i]!=group[j] for (i,j),l in pairs.items() if l==4)
    directions=[(i,j,l-1) for (i,j),l in sorted(pairs.items()) for i,j in ((i,j),(j,i))]
    # One launch state per visible cycle. A direction has k=l-1 advance stages.
    owners=list(range(size));stages=[];scan_channels=[]
    for c,d,k in directions:
        first=len(owners);owners.extend([c]*k)
        stages.append((c,d,k,first))
        start=next(s for s in range(len(states[c])) if reverse(states[c],s,k+1)==states[d])
        scan_channels.append([c,d,start,k,first])
    owners=np.array(owners);wall=np.array([walls(states[i],ones) for i in owners]);A=wall==2
    idle_A=np.flatnonzero(wall[:size]==2)
    rows=[]
    for delta in (0,1,9):
        p=F(1,1+delta)
        success={k:p**k for k in (1,2,3)}
        busy={k:(F(k) if delta==0 else (1-p**k)/delta) for k in (1,2,3)}
        for launch in (F(1,1000),F(1,100),F(1,10),F(1)):
            transitions=[]
            for c,d,k,first in stages:
                transitions.append((c,first,float(launch)))
                for j in range(k):
                    state=first+j
                    transitions.append((state,first+j+1 if j+1<k else d,1.))
                    if delta:transitions.append((state,c,float(delta)))
            ii=[];jj=[];vv=[];diag=np.zeros(len(owners))
            for i,j,q in transitions:
                ii.append(i);jj.append(j);vv.append(q);diag[i]-=q
            ii.extend(range(len(owners)));jj.extend(range(len(owners)));vv.extend(diag)
            Q=coo_matrix((vv,(ii,jj)),shape=(len(owners),len(owners))).tocsr()
            assert np.max(np.abs(np.asarray(Q.sum(axis=1)).ravel()))<1e-10
            trace=np.zeros((size,size));holding=np.ones(size)
            stationary=np.ones(len(owners))
            for c,d,k,first in stages:
                q=float(launch*success[k]);trace[c,d]+=q;trace[c,c]-=q
                holding[c]+=float(launch*busy[k])
                for j in range(k):stationary[first+j]=float(launch*p**j/(1+delta))
            stationary/=sum(stationary)
            assert np.max(np.abs(stationary@Q))<1e-10
            visible=np.bincount(owners,weights=stationary,minlength=size)
            assert np.max(np.abs(visible-holding/sum(holding)))<1e-12
            # Exact elimination of all gate states: stochastic complement in idle-time clock.
            Qii=Q[:size,:size].toarray();Qig=Q[:size,size:];Qgi=Q[size:,:size];Qgg=Q[size:,size:]
            reduced=Qii+Qig@spsolve(-Qgg.tocsc(),Qgi.toarray())
            assert np.max(np.abs(reduced-trace))<1e-10
            h=spsolve(-Q[A][:,A].tocsc(),np.ones(int(sum(A))))
            residual=np.max(np.abs((-Q[A][:,A])@h-1))
            assert residual<1e-7
            positions={int(v):i for i,v in enumerate(np.flatnonzero(A))}
            real_mean=float(np.mean([h[positions[int(i)]] for i in idle_A]))
            killed=-trace[np.ix_(idle_A,idle_A)]
            trace_h=np.linalg.solve(killed,np.ones(len(idle_A)))
            real_recurrence=np.linalg.solve(killed,holding[idle_A])
            assert abs(real_mean-float(np.mean(real_recurrence)))<1e-6
            rows.append({'advance_rate':1,'abort_rate':delta,'launch_rate':str(launch),
                'success_probability_by_support':{str(k+1):str(v) for k,v in success.items()},
                'mean_busy_time_by_support':{str(k+1):str(v) for k,v in busy.items()},
                'idle_trace_rate_by_support':{str(k+1):str(launch*v) for k,v in success.items()},
                'idle_trace_rate_ratios_to_LR2':{str(k+1):str(v/success[1]) for k,v in success.items()},
                'stationary_idle_fraction':float(sum(stationary[:size])),
                'stationary_visible_two_wall_probability':float(sum(visible[idle_A])),
                'visible_stationary_total_variation_from_uniform':float(sum(abs(visible-1/size))/2),
                'mean_first_exit_idle_time':float(np.mean(trace_h)),
                'mean_first_exit_real_time':real_mean,
                'ratio_real_to_idle_exit':real_mean/float(np.mean(trace_h)),
                'elimination_max_error':float(np.max(np.abs(reduced-trace))),
                'killed_equation_max_residual':float(residual)})
    return {'source_results_sha256':hashlib.sha256(parent.read_bytes()).hexdigest(),
        'visible_states':size,'directed_attempt_channels':len(stages),'expanded_states':len(owners),
        'support_edge_counts':dict(sorted(Counter(pairs.values()).items())),
        'support4_edges_crossing_short_components':cross,
        'advance_stages':'support minus one; progress is auxiliary, cycle changes only on final atomic commit',
        'projection':'idle c and every gate launched from c are observed as c until commit',
        'wallclock_caveat':'idle-time trace is Markov; observed real-time process is not strongly lumpable',
        'scan_channels':scan_channels,
        'rows':rows,'probe_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    r=run();Path(__file__).with_name('results.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('rows','scan_channels')},indent=2))
    for row in r['rows']:
        if row['launch_rate'] in ('1/1000','1'):
            print(json.dumps(row))
