"""Independent edge-set generator construction and floating linear-algebra checks."""
import itertools,json,sys
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.linalg import expm
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'micro_opw_01'))
from verify_witness import edges,representative

def main():
    bit=lambda v:int(v in (1,2,3))
    allgraphs={edges((0,)+p) for p in itertools.permutations(range(1,7))}
    reps={}
    for g in allgraphs:
        c,ng=representative(g,7)
        if all(any(bit(v)==bit(w) for w in ng[v]) for v in range(7)):reps[g]=(c,ng)
    moves={2:{g:set() for g in reps},3:{g:set() for g in reps}}
    gate={g:None for g in reps}
    for g,(c,_) in reps.items():
        for length in (2,3):
            for start in range(7):
                r=c[start:]+c[:start]
                h=edges(r[:length][::-1]+r[length:])
                if h in reps and h!=g and set(reps[h][0][::2])==set(c[::2]):
                    moves[length][g].add(h)
                    if length==2 and set(r[:2])=={0,6}:gate[g]=h
    a=edges(tuple(range(7)));b=gate[a]
    carrier={a};todo=[a]
    while todo:
        for g in (moves[2][todo[-1]]|moves[3][todo.pop()])-carrier:carrier.add(g);todo.append(g)
    assert len(carrier)==6
    carrier=sorted(carrier,key=lambda g:reps[g][0])
    states=[(g,v) for g in carrier for v in range(7)];ix={x:i for i,x in enumerate(states)}
    isB=np.array([sum(bit(w) for w in reps[g][1][0])==0 for g,v in states])
    assert sum(isB)==14
    post=ix[b,0];blank=ix[a,0];primed=ix[a,6]
    reference=json.loads(Path(__file__).with_name('results.json').read_text())
    checks=[]
    for run in reference['runs']:
        eta=float(F(run['eta_per_LR3_edge']));eps=float(F(run['epsilon_per_LR2_edge']))
        q=np.zeros((42,42))
        for i,(g,v) in enumerate(states):
            for w in reps[g][1][v]:q[i,ix[gate[g] if {v,w}=={0,6} and gate[g] is not None else g,w]]+=.5
            for h in moves[3][g]:q[i,ix[h,v]]+=eta
            for h in moves[2][g]:q[i,ix[h,v]]+=eps
            q[i,i]=-q[i].sum()
        assert np.max(abs(q-q.T))<1e-13 and np.max(abs(q.sum(axis=1)))<1e-13
        for selected,start,key in [(~isB,primed,'mean_first_write_from_primed_A'),(isB,post,'mean_first_reset_after_write')]:
            ids=np.flatnonzero(selected)
            h=np.linalg.solve(-q[np.ix_(ids,ids)],np.ones(len(ids)))
            assert abs(h[list(ids).index(start)]-float(F(run[key])))<1e-9
        assert abs(.5/(-q[post,post])-float(F(run['immediate_undo_next_event'])))<1e-12
        for row in run['table']:
            p=expm(row['t']*q)
            diff=p[post]-p[blank]
            assert abs((1+abs(sum(diff[isB])))/2-row['local_classification_success'])<1e-11
            idle=np.where(isB,0,1/28)
            assert abs(sum((idle@p)[isB])-row['idle_current_B'])<1e-11
        checks.append({'eta':run['eta_per_LR3_edge'],'epsilon':run['epsilon_per_LR2_edge'],'checks':'PASS'})
    Path(__file__).with_name('independent_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
