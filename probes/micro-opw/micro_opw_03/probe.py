"""Reversible probe-enabled writing on the retained MICRO–OPW carrier. No RNG."""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.linalg import expm,eigh
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'micro_opw_01'))
from probe import canon,pi,reversal
import importlib.util
spec=importlib.util.spec_from_file_location('reader',Path(__file__).resolve().parents[1]/'micro_opw_02'/'probe.py')
reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)


def build(eta,epsilon):
    previous=json.loads((Path(__file__).resolve().parents[1]/'micro_opw_02'/'results.json').read_text())
    a=[tuple(c) for c in previous['A_component']];b=[tuple(c) for c in previous['B_component']]
    carriers=sorted(a+b);cs=set(carriers)
    states=[(c,v) for c in carriers for v in range(7)];ix={x:i for i,x in enumerate(states)}
    q=[[F(0) for _ in states] for _ in states]
    gate={};lr2={};lr3={}
    for c in carriers:
        assert reader.valid(c)
        lr3[c]={d for i in range(7) if (d:=reversal(c,i,3))!=c and d in cs and pi(d)==pi(c)}
        lr2[c]={d for i in range(7) if (d:=reversal(c,i,2))!=c and d in cs and pi(d)==pi(c)}
        d=canon(tuple(6 if v==0 else 0 if v==6 else v for v in c))
        gate[c]=d if 6 in reader.neighbourhood(c,0) and d in cs and pi(c)==pi(d) else None
    for i,(c,v) in enumerate(states):
        for w in reader.neighbourhood(c,v):
            d=gate[c] if {v,w}=={0,6} and gate[c] is not None else c
            q[i][ix[(d,w)]]+=F(1,2)
        for d in lr3[c]:q[i][ix[(d,v)]]+=eta
        for d in lr2[c]:q[i][ix[(d,v)]]+=epsilon
        q[i][i]=-sum(q[i])
    assert all(sum(row)==0 for row in q)
    assert all(q[i][j]==q[j][i] for i in range(42) for j in range(42))
    assert all(q[i][j]>=0 for i in range(42) for j in range(42) if i!=j)
    reached={0};todo=[0]
    while todo:
        i=todo.pop()
        for j,x in enumerate(q[i]):
            if j!=i and x>0 and j not in reached:reached.add(j);todo.append(j)
    assert len(reached)==42
    written=np.array([c in b for c,v in states])
    # Local bit-count readout agrees exactly with the chosen carrier component.
    assert all((sum(reader.bit(w) for w in reader.neighbourhood(c,0))==0)==(c in b) for c,v in states)
    original=tuple(range(7));dest=gate[original]
    assert dest==(0,5,4,3,2,1,6)
    source=ix[(original,6)];post=ix[(dest,0)];blank=ix[(original,0)]
    assert q[source][post]==q[post][source]==F(1,2)
    def passage(select,start):
        ids=np.flatnonzero(select).tolist()
        matrix=[[-q[i][j] for j in ids] for i in ids]
        h=reader.exact_solve(matrix,[F(1) for _ in ids])
        assert all(sum(matrix[i][j]*h[j] for j in range(len(ids)))==1 for i in range(len(ids)))
        return h[ids.index(start)],ids
    write_time,ai=passage(~written,source)
    reset_time,bi=passage(written,post)
    idle_write_time,_=passage(~written,blank)
    write_h=reader.exact_solve([[-q[i][j] for j in ai] for i in ai],[F(1) for _ in ai])
    idle_mean=sum(write_h,F(0))/len(ai)
    flux=sum(q[i][j] for i in range(42) if not written[i] for j in range(42) if written[j])/42
    assert flux==F(1,21)+F(1,3)*epsilon
    qn=np.array(q,dtype=float)
    vals,vec=eigh(qn)
    assert np.sum(np.abs(vals)<1e-11)==1 and np.max(vals)<1e-11
    idle=np.array([0 if x else 1/28 for x in written])
    times=[0,0.1,1,3,10,30,100]
    table=[]
    for t in times:
        p=np.eye(42) if t==0 else (vec*np.exp(t*vals))@vec.T
        assert np.max(abs(p.sum(axis=1)-1))<1e-11 and np.min(p)>-1e-12
        if t in (1,10):assert np.max(abs(p-expm(t*qn)))<2e-12
        diff=p[post]-p[blank]
        carrier_diff=[sum(diff[i] for i,(d,v) in enumerate(states) if d==c) for c in carriers]
        local=abs(sum(diff[written]))
        carrier=sum(abs(x) for x in carrier_diff)/2
        full=sum(abs(diff))/2
        assert local<=carrier+1e-12 and carrier<=full+1e-12
        survival=float(expm(t*qn[np.ix_(bi,bi)])[bi.index(post)].sum())
        assert survival<=sum(p[post,written])+1e-12
        table.append({'t':t,'local_classification_success':float((1+local)/2),'full_carrier_success':float((1+carrier)/2),'full_joint_success':float((1+full)/2),'written_history_current_B':float(sum(p[post,written])),'first_reset_survival':survival,'idle_current_B':float(sum((idle@p)[written]))})
    return {'eta_per_LR3_edge':str(eta),'epsilon_per_LR2_edge':str(epsilon),'joint_states':42,'carrier_A_states':4,'carrier_B_states':2,'immediate_undo_next_event':str(F(1,2)/(-q[post][post])),'mean_first_write_from_primed_A':str(write_time),'mean_first_reset_after_write':str(reset_time),'reset_to_write_time_ratio':float(reset_time/write_time),'mean_first_write_from_A_at0':str(idle_write_time),'mean_first_write_from_uniform_idle_A':str(idle_mean),'stationary_A_to_B_flux':str(flux),'stationary_B_mass':'1/3','table':table,'checks':'PASS'}


if __name__=='__main__':
    output={'definition':'carrier = retained A/B six-state OPW23 component; all LR3 rate eta; probe unbiased spatial hops; coupled 0--6 traversal swaps adjacent vertices 0 and 6 when Pi/MICRO valid; both directions active; optional LR2 leakage epsilon per distinct neighbour','runs':[]}
    for eta in (F(1,10),F(1),F(10)):
        for eps in (F(0),F(1,100)):
            r=build(eta,eps);output['runs'].append(r)
            print(json.dumps(r),flush=True)
    output['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    output['reader_input_sha256']=hashlib.sha256((Path(__file__).resolve().parents[1]/'micro_opw_02'/'results.json').read_bytes()).hexdigest()
    Path(__file__).with_name('results.json').write_text(json.dumps(output,indent=2)+'\n')
