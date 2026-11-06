"""Six-hard-gluon helicity sum of the leading soft angular moment."""
from collections import defaultdict
from itertools import product
from math import sqrt, prod
import json
import numpy as np

from angular_ensemble import grid
from orders import tensor_rows
from su3_probe import F_TABLE, METRIC, I
from color_probe import bracket

ETA = np.array([1,-1,-1,-1])
HEL = np.array(list(product((-1,1),repeat=6)))
COUNT = np.sum(HEL == -1,axis=1)


def event(beam,t):
    e,x = 6+1.5*t*t,-1.5*t*t
    # Total outgoing spatial recoil is -3t² along x.
    beams = [(e+s*x*beam[0],x+s*e*beam[0],s*sqrt(e*e-x*x)*beam[1],
              s*sqrt(e*e-x*x)*beam[2]) for s in (1,-1)]
    p = np.array([(1.5*(1+t*t),1.5*(1-t*t),0,3*t),*(-np.array(beams)),
                  (4,0,0,4),(5,-3,0,-4),(1.5*(1+t*t),1.5*(1-t*t),0,-3*t)])
    assert np.max(np.abs(p.sum(axis=0)))<1e-12
    assert np.max(np.abs(np.sum(p*p*ETA,axis=1)))<1e-12
    return p


def dot(a,b):
    return np.sum(a*b*ETA,axis=-1,keepdims=True)


def polarizations(p):
    out = []
    for j,v in enumerate(p):
        n = v[1:]/v[0]
        ref = np.array([0.,1.,0.]) if abs(n[1])<.9 else np.array([0.,0.,1.])
        transverse = ref-n*np.dot(n,ref)
        transverse /= np.linalg.norm(transverse)
        other = np.cross(n,transverse)
        out.append(np.column_stack((np.zeros(len(HEL)),transverse+1j*HEL[:,j,None]*other)))
    return np.array(out)/sqrt(2)


def amplitude(p,eps,word):
    ordered = p[list(word)]
    js = {(i,i+1):eps[leg] for i,leg in enumerate(word[:-1])}
    for length in range(2,6):
        for i in range(6-length):
            j=i+length
            value=0
            for k in range(i+1,j):
                a,b = js[i,k],js[k,j]
                q,r = ordered[i:k].sum(axis=0),ordered[k:j].sum(axis=0)
                value = value + dot(a,b)*(q-r)+b*dot(a,q+2*r)-a*dot(b,2*q+r)
            for k in range(i+1,j-1):
                for l in range(k+1,j):
                    a,b,c=js[i,k],js[k,l],js[l,j]
                    value = value+2*b*dot(a,c)-a*dot(b,c)-c*dot(a,b)
            if length==5:
                return dot(value,eps[word[-1]])[:,0]
            total=ordered[i:j].sum(axis=0)
            js[i,j]=value/dot(total,total)[0]


def amplitudes(p,words):
    eps=polarizations(p)
    values=np.array([amplitude(p,eps,w) for w in words])
    assert np.max(np.abs(values[:,(COUNT<2)|(COUNT>4)]))<1e-5
    test=eps.copy()
    test[0]=p[0]
    ward=amplitude(p,test,words[0])
    assert np.max(np.abs(ward))<1e-6
    return values


def gram():
    # The tensors use a diagonal colour metric. Build the full emitter Gram.
    base=defaultdict(lambda:defaultdict(float))
    for key,word,c in tensor_rows(6):
        base[word][key]+=float(c)
    words=sorted(base)
    size=8**6
    steps=np.array([8**j for j in reversed(range(6))])
    colours=(np.arange(size)[:,None]//steps)%8
    measure=1/np.sqrt(np.prod(np.array(METRIC)[colours],axis=1))
    vec=np.zeros((24,size))
    for j,w in enumerate(words):
        for key,c in base[w].items():
            vec[j,sum(int(v)*int(s) for v,s in zip(key,steps))]=c
    hard=(vec*measure)@(vec*measure).T
    soft=np.zeros((144,144))
    for g in I:
        V=np.zeros((24,6,size))
        for leg,step in enumerate(steps):
            for a in I:
                ix=np.flatnonzero(colours[:,leg]==a)
                for b,c in F_TABLE[g,a]:
                    V[:,leg,ix+(b-a)*step]+=float(c/METRIC[a])*vec[:,ix]
        assert np.max(np.abs(V.sum(axis=1)))<1e-10
        V=V.reshape(144,size)*measure
        soft+=V@V.T/METRIC[g]
    return words,hard,soft.reshape(24,6,24,6)


def mhv_check(p,words,values):
    spinors=[]
    for v in p:
        e,x,y,z=v*np.sign(v[0])
        spinors.append((1,(x+1j*y)/(e+z)) if e+z>=e-z else
                       ((x-1j*y)/(e-z),1))
    pt=np.array([1/prod(bracket(spinors[a],spinors[b])
                        for a,b in zip(w,w[1:]+w[:1])) for w in words])
    # Depending on the polarization sign convention, COUNT=2 is holomorphic
    # or antiholomorphic. Either way the normalized ordering vector is fixed.
    for h in np.flatnonzero((COUNT==2)|(COUNT==4)):
        expected = values[0,h]*pt/pt[0]
        error = min(np.max(np.abs(values[:,h]-expected)),
                    np.max(np.abs(values[:,h]-values[0,h]*np.conj(pt/pt[0]))))
        assert error < 1e-6*max(1,abs(values[0,h]))


def moments(beam,t,grams,directions,moment,return_weights=False,hard_momenta=None):
    words,hard,soft=grams
    p=event(beam,t) if hard_momenta is None else hard_momenta
    vals=amplitudes(p,words)
    mhv_check(p,words,vals)
    denominator=p[:,0,None]-p[:,1:]@directions.T
    kinematic=-np.einsum('ia,a,ja->ij',p,ETA,p)
    out={}
    for label,mask in (("MHV+anti", (COUNT==2)|(COUNT==4)),
                       ("NMHV", COUNT==3),("all",(COUNT>=2)&(COUNT<=4))):
        v=t*vals[:,mask]
        weight=np.einsum('ah,ab,bh->',v.conj(),hard,v).real
        corr=np.einsum('ah,aibj,bh->ij',v.conj(),soft,v,optimize=True).real/weight
        r=np.einsum('ij,ik,jk->k',kinematic*corr,1/denominator,1/denominator)
        row=np.array([np.mean(r),np.mean(r*moment),np.mean(r*moment)/np.mean(r)])
        out[label]=(row,weight) if return_weights else row
    return out


def main():
    grams=gram()
    coarse_directions,coarse_moment=grid(20,40,48)
    fine_directions,fine_moment=grid(20,40,96)
    report={}
    for name,beam in (("planar",(5/13,0,12/13)),("perpendicular",(0,1,0))):
        def calculate(directions,moment):
            vals=[moments(beam,t,grams,directions,moment) for t in (.008,.004,.002,.001)]
            diffs=[{k:(a[k]-b[k])/(.008**2/4**j*3/4) for k in a}
                   for j,(a,b) in enumerate(zip(vals,vals[1:]))]
            estimates=[{k:(4*b[k]-a[k])/3 for k in a} for a,b in zip(diffs,diffs[1:])]
            for k in estimates[0]:
                np.testing.assert_allclose(estimates[0][k],estimates[1][k],rtol=.002,atol=.02)
            return estimates[1]
        coarse=calculate(coarse_directions,coarse_moment)
        fine=calculate(fine_directions,fine_moment)
        for k in fine:
            np.testing.assert_allclose(coarse[k],fine[k],rtol=.002,atol=.02)
        report[name]={k:v.tolist() for k,v in fine.items()}
    print(json.dumps({"columns":["mean_K","mean_K_cos2phi","quadratic_normalized_moment"],
                      "beam_cases":report},indent=2))


if __name__=="__main__":
    main()
