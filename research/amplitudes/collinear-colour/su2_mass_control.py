"""Tree-level transverse comparison in custodial SU(2) with one Higgs."""
from itertools import combinations, product
import json

import numpy as np

from six_soft import ETA, amplitudes, polarizations, HEL
from su2_real_rate import colour_basis, measurements

EPS = np.zeros((3,3,3))
for a,b,c in ((0,1,2),(1,2,0),(2,0,1)):
    EPS[a,b,c],EPS[a,c,b] = 1,-1


def dot(a,b):
    return np.sum(a*b*ETA,axis=-1)


def cubic(a,b,q,r):
    out = np.einsum('abc,...bi,...ci,i->...a',EPS,a,b,ETA)[...,None]*(q-r)
    out += np.einsum('abc,...b,...ci->...ai',EPS,dot(a,q+2*r),b)
    out -= np.einsum('abc,...bi,...c->...ai',EPS,a,dot(b,2*q+r))
    return 1j*out


def quartic(a,b,c):
    out = 0
    for x,y,z in ((a,b,c),(b,c,a),(c,a,b)):
        yz = np.einsum('...ai,...bi,i->...ab',y,z,ETA)
        out = out - 2*x*np.trace(yz,axis1=-2,axis2=-1)[...,None,None]
        out += np.einsum('...bi,...ab->...ai',x,yz+yz.swapaxes(-1,-2))
    return out


def partitions(mask,k):
    if k==1:
        yield (mask,)
        return
    low = mask & -mask
    part = (mask-1)&mask
    while part:
        if part&low:
            for tail in partitions(mask^part,k-1):
                yield (part,*tail)
        part = (part-1)&mask


def tensor(p,m,eps):
    mh = 1.55*m
    # Couplings at g=1, from (m²/2)(1+h/v)² W² and the Higgs potential.
    h3 = -3*mh**2/(2*m) if m else 0
    h4 = -3*(1.55**2)/4 if m else 0
    legs = len(p)-1
    full = (1<<legs)-1
    current = {}
    for i in range(legs):
        shape = [1]*legs
        shape[i] = 3
        current[1<<i] = (np.eye(3).reshape(*shape,3,1)*eps[i], 0.)
    momentum = {mask:p[[i for i in range(legs) if mask&(1<<i)]].sum(axis=0)
                for mask in range(1,full+1)}
    for mask in range(1,full+1):
        if mask in current:
            continue
        v,h = 0,0
        for a,b in partitions(mask,2):
            x,s = current[a]
            y,t = current[b]
            v = v + cubic(x,y,momentum[a],momentum[b])
            if m:
                v += m*(np.asarray(s)[...,None,None]*y+np.asarray(t)[...,None,None]*x)
                h = h + m*np.sum(dot(x,y),axis=-1)+h3*s*t
        for a,b,c in partitions(mask,3):
            x,s = current[a]
            y,t = current[b]
            z,u = current[c]
            v += quartic(x,y,z)
            if m:
                v += .5*(np.asarray(s*t)[...,None,None]*z+
                         np.asarray(s*u)[...,None,None]*y+np.asarray(t*u)[...,None,None]*x)
                h = h + .5*(s*np.sum(dot(y,z),axis=-1)+t*np.sum(dot(x,z),axis=-1)
                             +u*np.sum(dot(x,y),axis=-1))+h4*s*t*u
        if mask==full:
            return dot(v,eps[-1])
        q = momentum[mask]
        q2 = dot(q,q)
        if m:
            v = v-dot(v,q)[...,None]*q/m**2
        current[mask] = (v/(q2-m*m),-h/(q2-mh*mh) if m else 0.)


def event(pair_mass,m,beam):
    # Fixed hard energy and energy fractions for all masses.
    energy = 12.
    pair_energy = 3.
    a_energy,b_energy = 4.,5.
    parent = np.sqrt(pair_energy**2-pair_mass**2)
    a,b = np.sqrt(np.array([a_energy,b_energy])**2-m*m)
    cosine = (b*b-parent*parent-a*a)/(2*parent*a)
    az = a*np.sqrt(1-cosine*cosine)
    incoming = np.sqrt((energy/2)**2-m*m)*np.array(beam)
    split = np.sqrt((pair_mass/2)**2-m*m)
    p = np.array([(pair_energy/2,parent/2,0,split),
                  (-energy/2,*(-incoming)),(-energy/2,*incoming),
                  (a_energy,a*cosine,0,az),(b_energy,-parent-a*cosine,0,-az),
                  (pair_energy/2,parent/2,0,-split)])
    np.testing.assert_allclose(p.sum(axis=0),0,atol=1e-12)
    np.testing.assert_allclose(dot(p,p),m*m,atol=1e-12)
    np.testing.assert_allclose(dot(p[0]+p[-1],p[0]+p[-1]),pair_mass**2,atol=1e-12)
    return p


def check_neutral_higgs():
    m = 1.
    e = 3.
    k = np.sqrt(e*e-m*m)
    p = np.array([(-e,0,0,-k),(-e,0,0,k),(e,k,0,0),(e,-k,0,0)])
    eps = np.tile([0.,0.,1.,0.],(4,1))
    amplitude = tensor(p,m,eps)[2,2,2,2]
    expected = -m*m*sum(1/(dot(p[0]+p[j],p[0]+p[j])-(1.55*m)**2)
                        for j in (1,2,3))
    np.testing.assert_allclose(amplitude,expected,rtol=1e-12)
    return float(amplitude.real)


def main():
    helicity = np.flatnonzero(np.all(HEL==(1,-1,-1,1,1,1),axis=1))[0]
    words,basis = colour_basis()
    report = []
    for tilt,pair in product((0,20),(.24,.48,.96)):
        angle = np.radians(tilt)
        beam = (5/13*np.cos(angle),np.sin(angle),12/13*np.cos(angle))
        p = event(pair,0,beam)
        ref = np.einsum('wabc,w->abc',basis,amplitudes(p,words)[:,helicity])[...,None]
        check = tensor(p,0,polarizations(p)[:,helicity]).reshape(3,81,3,1)
        overlap = np.vdot(ref,check)/np.vdot(ref,ref)
        np.testing.assert_allclose(check,overlap*ref,atol=1e-8,rtol=1e-8)
        ref_share = measurements(ref,[True])[0]
        for ratio in (.15,.30,.45):
            pm = event(pair,ratio*pair,beam)
            massive = tensor(pm,ratio*pair,polarizations(pm)[:,helicity]).reshape(3,81,3,1)
            share = measurements(massive,[True])[0]
            report.append(dict(tilt=tilt,pair_over_Q=pair/12,m_over_pair=ratio,
                               massless=ref_share,massive=share,shift=share-ref_share))
    print(json.dumps(dict(neutral_higgs_check=check_neutral_higgs(),scan=report),indent=2))


if __name__ == '__main__':
    main()
