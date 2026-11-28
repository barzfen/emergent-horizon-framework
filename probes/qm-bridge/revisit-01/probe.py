"""Rebuild retained MICRO–OPW carrier independently; compare stochastic and supplied coherent lifts."""
import itertools, json, hashlib
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import expm

def canon(c):
    c=tuple(c); j=c.index(0); c=c[j:]+c[:j]
    return min(c,(c[0],)+c[:0:-1])
def pi(c): return frozenset(c[::2])
def valid(c):
    bit=lambda v:int(v in {1,2,3})
    return all(bit(c[i]) in {bit(c[(i-1)%7]),bit(c[(i+1)%7])} for i in range(7))
def reverse(c,s,l):
    q=list(c); ix=[(s+j)%7 for j in range(l)]
    for j,v in zip(ix,[c[j] for j in ix][::-1]): q[j]=v
    return canon(q)
def component(adj,s):
    seen={s}; todo=[s]
    while todo:
        for q in adj[todo.pop()]-seen: seen.add(q); todo.append(q)
    return seen
states=sorted((0,)+p for p in itertools.permutations(range(1,7)) if p[0]<p[-1] and valid((0,)+p))
ss=set(states)
def graph(lengths):
    return {c:{q for l in lengths for s in range(7) if (q:=reverse(c,s,l)) in ss and q!=c and pi(q)==pi(c)} for c in states}
g3=graph([3]); g23=graph([2,3]); A=(0,1,2,3,4,5,6); B=(0,5,4,3,2,1,6)
ca=component(g3,A); cb=component(g3,B); carrier=sorted(component(g23,A)); ix={c:i for i,c in enumerate(carrier)}
assert len(states)==72 and len(ca)==4 and len(cb)==2 and set(carrier)==ca|cb and B in g23[A]
adj=np.array([[int(d in g23[c]) for d in carrier] for c in carrier])
assert np.array_equal(adj,adj.T)
L=np.diag(adj.sum(axis=1))-adj; Q=-L
# Rates: one per distinct undirected LR2/LR3 edge; this is a new explicit benchmark clock.
# Coherent H=L is supplied, not derived from Q or admissibility.
R=np.diag([int(c in cb) for c in carrier]); read=np.diag(R)
local=[sum(v in {1,2,3} for v in (c[(c.index(0)-1)%7],c[(c.index(0)+1)%7])) for c in carrier]
assert all(local[ix[c]]==1 for c in ca) and all(local[ix[c]]==0 for c in cb)
eA=np.eye(6)[:,ix[A]];eB=np.eye(6)[:,ix[B]]
plus=(eA+1j*eB)/np.sqrt(2);minus=(eA-1j*eB)/np.sqrt(2); p0=(eA+eB)/2
assert np.allclose(abs(plus)**2,p0) and np.allclose(abs(minus)**2,p0)
# Exact integer algebra: all static deterministic readout projectors are diagonal.
projectors=[np.diag([int(mask>>i&1) for i in range(6)]) for mask in range(64)]
comm=max(int(np.max(abs(a@b-b@a))) for a in projectors for b in projectors)
assert comm==0
rows=[]
for t in [0,0.05,0.1,0.25,0.5,1,2]:
    T=expm(Q*t);U=expm(-1j*L*t)
    assert np.allclose(T.sum(axis=1),1) and T.min()>-1e-12
    assert np.allclose(U.conj().T@U,np.eye(6))
    cp=float(read@(T@p0)); pp=float(read@abs(U@plus)**2); pm=float(read@abs(U@minus)**2)
    # Incoherent mixture evolves each localized input separately, then adds probabilities.
    mix=float((read@abs(U@eA)**2+read@abs(U@eB)**2)/2)
    assert abs((pp+pm)/2-mix)<1e-12
    rows.append(dict(t=t,markov_B=cp,coherent_plus_B=pp,coherent_minus_B=pm,incoherent_unitary_B=mix,phase_contrast=abs(pp-pm)))
def slope(psi):return float(2*np.real(np.vdot(psi,R@(-1j*L@psi))))
assert abs(slope(plus)+slope(minus))<1e-12 and abs(abs(slope(plus))-1)<1e-12
# Exact classical path addition: all restricted path contributions are nonnegative.
# No diagonal readout creates quantum measurement disturbance; instruments require extra rules.
result={'scope':'retained n=7 six-state MICRO-OPW23 carrier; benchmark only','states':carrier,'A_component':sorted(ca),'B_component':sorted(cb),'adjacency':adj.tolist(),'L':L.tolist(),'edges':int(adj.sum()//2),'rates':'1 per distinct LR2/LR3 edge; H=L supplied separately','static_projectors':64,'projector_pairs_checked':4096,'max_static_commutator':comm,'same_initial_probabilities':p0.tolist(),'initial_coherent_B_slopes':[slope(plus),slope(minus)],'time_checks':rows,'max_sampled_phase_contrast':max(x['phase_contrast'] for x in rows),'checks':'PASS','numpy':np.__version__,'scipy':scipy.__version__,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
