"""Matched tree-level transverse electroweak rate scan in the bosonic sector."""
from itertools import product
import json

import numpy as np

from six_soft import ETA
from su2_mass_control import EPS, dot, partitions, event, tensor, transverse_polarizations, HEL
from su2_real_rate import measurements

CHANNELS = ("++","ZZ","ZA","AZ","AA")
HELICITIES = np.array([1,-1,-1,1,1,1])


def momenta(pair, masses, beam):
    m1,mi,mj,ma,mb,m2 = masses.T
    e1,ea,eb = 1.5,4.,5.
    parent = np.sqrt(9-pair*pair)
    # Equal daughter energies, with longitudinal components fixed by
    # P dot p1 = (M²+m1²-m2²)/2.
    px = parent/2-(m1*m1-m2*m2)/(2*parent)
    pz = np.sqrt(e1*e1-m1*m1-px*px)
    a,b = np.sqrt(ea*ea-ma*ma),np.sqrt(eb*eb-mb*mb)
    ax = (b*b-parent*parent-a*a)/(2*parent)
    az = np.sqrt(a*a-ax*ax)
    ei = 6+(mi*mi-mj*mj)/24
    incoming = np.sqrt(ei*ei-mi*mi)[:,None]*beam
    z = np.zeros_like(ei)
    p = np.stack((np.column_stack((z+e1,px,z,pz)),
                  np.column_stack((-ei,-incoming)),
                  np.column_stack((ei-12,incoming)),
                  np.column_stack((z+ea,ax,z,az)),
                  np.column_stack((z+eb,-parent-ax,z,-az)),
                  np.column_stack((z+e1,parent-px,z,-pz))),axis=1)
    np.testing.assert_allclose(p.sum(axis=1),0,atol=1e-12)
    np.testing.assert_allclose(dot(p,p),masses**2,atol=1e-12)
    np.testing.assert_allclose(dot(p[:,0]+p[:,5],p[:,0]+p[:,5]),pair**2,atol=1e-12)
    return p


def transverse(p):
    n = p[...,1:]/p[...,:1]
    n /= np.linalg.norm(n,axis=-1,keepdims=True)
    normal = np.array([0.,1.,0.])-n*n[...,1:2]
    normal /= np.linalg.norm(normal,axis=-1,keepdims=True)
    pol = (normal+1j*HELICITIES[None,:,None]*np.cross(n,normal))/np.sqrt(2)
    eps = np.concatenate((np.zeros_like(p[...,:1]),pol),axis=-1)
    np.testing.assert_allclose(dot(eps,p),0,atol=1e-12)
    return eps


def amplitude(p, eps, external, mw, sine2):
    c,s = np.sqrt(1-sine2),np.sqrt(sine2)
    rotate = np.array([[1,0,0,0],[0,1,0,0],[0,0,c,s]])
    masses = np.array([mw,mw,mw/c,0])
    mh = 1.55*mw
    hv = masses**2/mw if mw else masses
    hhv = masses**2/(2*mw**2) if mw else masses
    triple_h = -3*mh**2/(2*mw) if mw else 0
    quartic_h = -3*1.55**2/4 if mw else 0

    def gauge(a):
        return np.einsum('ai,...im->...am',rotate,a)

    def physical(a):
        return np.einsum('ai,...am->...im',rotate,a)

    def cubic(a,b,q,r):
        v = np.einsum('abc,nbm,ncm,m->na',EPS,a,b,ETA)[...,None]*(q-r)[:,None,:]
        v += np.einsum('abc,nb,ncm->nam',EPS,dot(a,(q+2*r)[:,None,:]),b)
        v -= np.einsum('abc,nbm,nc->nam',EPS,a,dot(b,(2*q+r)[:,None,:]))
        return 1j*v

    def quartic(a,b,c):
        out = 0
        for x,y,z in ((a,b,c),(b,c,a),(c,a,b)):
            yz = np.einsum('nai,nbi,i->nab',y,z,ETA)
            out = out-2*x*np.trace(yz,axis1=-2,axis2=-1)[:,None,None]
            out += np.einsum('nbi,nab->nai',x,yz+yz.swapaxes(-1,-2))
        return out

    def hh_vec(x,a,b):
        return (a*b)[:,None,None]*hhv[None,:,None]*x

    zeros = np.zeros(len(p),complex)
    current = {1<<i:(external[:,i,:,None]*eps[:,i,None,:],zeros) for i in range(5)}
    momentum = {mask:p[:,[i for i in range(5) if mask&(1<<i)]].sum(axis=1)
                for mask in range(1,32)}
    longitudinal = np.zeros(4)
    np.divide(1,masses*masses,out=longitudinal,where=masses!=0)
    for mask in range(1,32):
        if mask in current:
            continue
        v,h = 0,0
        for a,b in partitions(mask,2):
            x,j = current[a]
            y,k = current[b]
            v = v+physical(cubic(gauge(x),gauge(y),momentum[a],momentum[b]))
            v += hv[None,:,None]*(j[:,None,None]*y+k[:,None,None]*x)
            h = h+np.sum(dot(x,y)*hv,axis=-1)+triple_h*j*k
        for a,b,c in partitions(mask,3):
            x,j = current[a]
            y,k = current[b]
            z,l = current[c]
            v += physical(quartic(gauge(x),gauge(y),gauge(z)))
            v += hh_vec(x,k,l)+hh_vec(y,j,l)+hh_vec(z,j,k)
            h += np.sum(hhv*(j[:,None]*dot(y,z)+k[:,None]*dot(x,z)+l[:,None]*dot(x,y)),axis=-1)
            h += quartic_h*j*k*l
        if mask==31:
            return np.sum(dot(v,eps[:,5,None,:])*external[:,5],axis=-1)
        q = momentum[mask]
        q2 = dot(q,q)
        v -= dot(v,q[:,None,:])[...,None]*longitudinal[None,:,None]*q[:,None,:]
        current[mask] = (v/(q2[:,None,None]-masses[None,:,None]**2),-h/(q2-mh**2))


def evaluate(pair,mw,beam,sine2,ward=False):
    # W1,W2 are degenerate, so the complete spectator sum can use
    # these Cartesian states in place of W+,W-.
    states = np.eye(4,dtype=complex)
    plus = np.array([1,1j,0,0])/np.sqrt(2)
    ends = [(plus,plus),(states[2],states[2]),(states[2],states[3]),
            (states[3],states[2]),(states[3],states[3])]
    middle = np.array(list(product(range(4),repeat=4)))
    masses = np.array([mw,mw,mw/np.sqrt(1-sine2),0])
    rates = {}
    for name,(a,b) in zip(CHANNELS,ends):
        external = np.zeros((len(middle),6,4),complex)
        external[:,0],external[:,5] = a,b
        external[:,1:5] = states[middle]
        assignment = masses[np.argmax(np.abs(external),axis=-1)]
        p = momenta(pair,assignment,beam)
        eps = transverse(p)
        values = amplitude(p,eps,external,mw,sine2)
        if ward and name in ("ZA","AZ","AA"):
            leg = 0 if name=="AZ" else 5
            eps[:,leg] = p[:,leg]
            check = amplitude(p,eps,external,mw,sine2)
            assert np.max(np.abs(check))<2e-7*max(1,np.max(np.abs(values)))
        rates[name] = float(np.vdot(values,values).real)
    total = sum(rates.values())
    return dict(fraction=rates["++"]/(3*total),
                channel_fractions={name:r/total for name,r in rates.items()})


def main():
    report = []
    helicity = np.flatnonzero(np.all(HEL==HELICITIES,axis=1))[0]
    for tilt,pair in product((0,20),(.24,.48,.96)):
        theta = np.radians(tilt)
        beam = (5/13*np.cos(theta),np.sin(theta),12/13*np.cos(theta))
        mw = .30*pair
        ref = evaluate(pair,0,beam,0)
        control = evaluate(pair,mw,beam,0)
        for mass,check in ((0,ref),(mw,control)):
            p = event(pair,mass,beam)
            expected = measurements(tensor(p,mass,transverse_polarizations(p)[:,helicity]).reshape(3,81,3,1),[True])[0]
            np.testing.assert_allclose(check['fraction'],expected,rtol=1e-8)
        for sine2 in (0,.115,.23):
            massless = evaluate(pair,0,beam,sine2)
            np.testing.assert_allclose(massless['fraction'],ref['fraction'],rtol=1e-8)
            massive = control if not sine2 else evaluate(pair,mw,beam,sine2,ward=True)
            report.append(dict(tilt=tilt,pair_over_Q=pair/12,mW_over_pair=.30,sine_squared=sine2,
                               massless=massless,massive=massive,
                               shift=massive['fraction']-massless['fraction']))
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
