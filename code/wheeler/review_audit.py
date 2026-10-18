"""Independent Wheeler checks. Python 3, numpy, scipy; run from repository root: python code/wheeler/review_audit.py.
Convention: labelled words, insert BEFORE positions 0..n-1 (not n).
Move graph: distinct non-self neighbours, cyclic length-3 reversal.
"""
import itertools, math, json, platform
import scipy
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix, diags
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import eigsh
from scipy.special import betaln
from scipy.optimize import minimize_scalar

def valid(w):
    return all(not(w[i]==w[(i+2)%len(w)]!=w[(i+1)%len(w)]) for i in range(len(w)))
def walls(w):
    return sum(w[i]!=w[(i+1)%len(w)] for i in range(len(w)))
def states(n):
    return [w for w in itertools.product((0,1),repeat=n) if valid(w)]
def canon(w):
    return min(w[i:]+w[:i] for i in range(len(w)))
def events(w):
    for i in range(len(w)):
        for b in (0,1):
            v=w[:i]+(b,)+w[i:]
            if valid(v): yield i,b,v
def neighbours(w):
    out=set()
    for i in range(len(w)):
        z=list(w); a=i; b=(i+2)%len(w)
        z[a],z[b]=z[b],z[a]; z=tuple(z)
        if z!=w and valid(z):out.add(z)
    return out
def graph(ws,quotient=False):
    nodes=sorted({canon(w) for w in ws}) if quotient else ws
    lookup={w:i for i,w in enumerate(nodes)}; rows=[]; cols=[]
    for w,i in lookup.items():
        for v in neighbours(w):
            j=lookup[canon(v) if quotient else v]
            if i!=j:rows.append(i);cols.append(j)
    A=csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(len(nodes),len(nodes)))
    A.data[:]=1
    return nodes,A
def entropy(p):
    p=np.asarray(p);p=p[p>0]
    return -float(np.dot(p,np.log(p)))
def run_length(v,i):
    if len(set(v))==1:return len(v)
    L=1;j=(i-1)%len(v)
    while v[j]==v[i]:L+=1;j=(j-1)%len(v)
    j=(i+1)%len(v)
    while v[j]==v[i]:L+=1;j=(j+1)%len(v)
    return L
def kernel(ws,weight=lambda w,i,b,v:1.):
    targets=sorted({v for w in ws for i,b,v in events(w)})
    ix={v:j for j,v in enumerate(targets)};K=np.zeros((len(ws),len(targets)))
    for k,w in enumerate(ws):
        for i,b,v in events(w):K[k,ix[v]]+=weight(w,i,b,v)
        K[k]/=sum(K[k])
    return targets,K
def cher(n,k):
    a,b=k+1,n-k+1;c,d=k+2,n-k+2
    f=lambda s:betaln(s*a+(1-s)*c,s*b+(1-s)*d)-s*betaln(a,b)-(1-s)*betaln(c,d)
    r=minimize_scalar(f,bounds=(0,1),method='bounded',options={'xatol':1e-12})
    return -float(r.fun)

results={"convention":__doc__,"seed":20261018,"enumeration":[],"weighted":[],"core_c":[]}
rng=np.random.default_rng(results['seed'])
for n in range(4,15):
    ws=states(n);counts=Counter((sum(w),walls(w)) for w in ws)
    incoming=defaultdict(Counter)
    for w in ws:
        D=walls(w);E=list(events(w));m=sum(w)
        assert len(E)==n+D
        assert Counter(b for i,b,v in E)==Counter({0:n-m+D//2,1:m+D//2})
        for i,b,v in E:
            assert walls(v)==D
            incoming[D][v]+=1
    for (m,D),count in counts.items():
        if D:
            k=D//2
            expected=Fraction(n,k)*math.comb(m-k-1,k-1)*math.comb(n-m-k-1,k-1)
            assert count==expected
    nodes,A=graph(ws);nc,labels=connected_components(A,directed=False)
    qnodes,QA=graph(ws,True);qc,qlabels=connected_components(QA,directed=False)
    maxcols={str(D):str(Fraction(max(c.values()),n+D)) for D,c in incoming.items()}
    assert all(Fraction(max(c.values()),n+D)<=1 for D,c in incoming.items())
    results['enumeration'].append(dict(n=n,states=len(ws),components=int(nc),rotation_components=int(qc),max_column=maxcols))
    if n==12:
        B=[w for w in ws if w in [tuple(map(int,s)) for s in ('000111000111','111000111000')] or canon(w)==canon(tuple(map(int,'000111000111')))]
        U=[w for w in ws if sum(w)==6 and walls(w)==4 and w not in B]
        bs={v for w in B for i,b,v in events(w)};us={v for w in U for i,b,v in events(w)}
        results['growth_19']=dict(balanced_sources=len(B),unbalanced_sources=len(U),balanced_descendants=len(bs),unbalanced_descendants=len(us),intersection=len(bs&us))
    if n<=10:
        for D in sorted(incoming):
            sw=[w for w in ws if walls(w)==D];ts,K=kernel(sw)
            for trial in range(20):
                p=rng.dirichlet(np.ones(len(sw)))
                assert entropy(p@K)>=entropy(p)-1e-12
    if n in (8,9):
        ds=[w for w in ws if walls(w)==2];dn,DA=graph(ds);nn,ll=connected_components(DA,directed=False)
        groups=Counter(ll);mobile=[c for c,s in groups.items() if s==n]
        for c in mobile:
            sub=DA[ll==c][:,ll==c]
            assert np.all(np.asarray(sub.sum(axis=1)).ravel()==2)
        results.setdefault('mobile_D2',[]).append(dict(n=n,component_sizes=dict(Counter(groups.values())),gap=4*math.sin(math.pi/n)**2))

for n,D,q in [(5,2,.2),(6,2,.5),(11,4,.5),(5,2,.05),(5,2,.01)]:
    ws=[w for w in states(n) if walls(w)==D]
    ts,K=kernel(ws,lambda w,i,b,v:q**run_length(v,i))
    rec=dict(n=n,D=D,q=q,max_column=float(K.sum(axis=0).max()))
    if n==5 and q<.1:
        a=ws.index(tuple(map(int,'11000')));b=ws.index(tuple(map(int,'11100')))
        f=lambda p:entropy(p*K[a]+(1-p)*K[b])-entropy([p,1-p])
        r=minimize_scalar(f,bounds=(0,1),method='bounded')
        rec.update(p_11000=float(r.x),delta_entropy=float(r.fun))
        if q==.05:rec['delta_entropy_using_reported_p_11000_0345']=f(.345)
    results['weighted'].append(rec)

for n in range(4,9):
    perms=[p for p in itertools.permutations(range(1,n)) if p<p[::-1]]
    ix={p:i for i,p in enumerate(perms)};rows=[];cols=[]
    for p,i in ix.items():
        out=set()
        for a in range(n-1):
            for b in range(a+2,n):
                v=p[:a]+p[a:b][::-1]+p[b:];v=min(v,v[::-1])
                if v!=p:out.add(ix[v])
        for j in out:rows.append(i);cols.append(j)
    A=csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(len(perms),len(perms)))
    degree=np.asarray(A.sum(axis=1)).ravel();assert np.all(degree==n*(n-3)/2)
    L=diags(degree)-A
    vals=np.linalg.eigvalsh(L.toarray()) if n<=6 else np.sort(eigsh(L,k=3,which='SM',return_eigenvectors=False,tol=1e-10,v0=np.linspace(1,2,len(perms))))
    results['core_c'].append(dict(n=n,V=len(perms),degree=int(degree[0]),gap=float(vals[1])))

C={n:cher(n,4) for n in range(8,401)}
results['cher']=dict(values={str(n):C[n] for n in [8,21,22,100,300]},best_per_n=max(C,key=lambda n:C[n]/n),best_per_n_minus_1=max(C,key=lambda n:C[n]/(n-1)))
results['event_example']={''.join(map(str,k)):v for k,v in Counter(v for i,b,v in events(tuple(map(int,'00111')))).items()}

# Symbol-bias numerator identity, independently expanded with sympy if installed.
try:
    import sympy as sp
    a,b,x,y,k=sp.symbols('a b x y k');Z=a*(x+k)+b*(y+k)
    actual=sp.expand((Z-a)*(Z-b)-a*x*(Z-b)-b*y*(Z-a))
    claimed=a*a*(k-1)*(x+k)+b*b*(k-1)*(y+k)+a*b*(k*(x+y)+2*k*(k-1)+1)
    results['symbol_bias_identity_residual']=str(sp.simplify(actual-claimed))
except ImportError: results['symbol_bias_identity_residual']='sympy unavailable'
results['environment']={'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__}
output=Path(__file__).resolve().parents[2]/'data/wheeler/review-01-results.json'
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
