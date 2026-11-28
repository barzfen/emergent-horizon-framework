"""Distinguish the incoming direction from the alignment of incoming colours."""
from itertools import product
import json

import numpy as np

from six_soft import HEL, amplitudes
from su2_mass_control import event
from su2_real_rate import colour_basis


def rates(tensor):
    charged = (tensor[0,...,0,:]-tensor[1,...,1,:]
               +1j*(tensor[0,...,1,:]+tensor[1,...,0,:]))/2
    neutral = tensor[2,...,2,:]
    return np.array([charged,neutral])


def summarize(tensor, mask):
    amp = rates(tensor[...,mask])
    # Keep the two incoming colour axes. Sum only recoil and helicity
    # axes when constructing each incoming-state contribution.
    swap = amp.swapaxes(1,2)
    symmetric = (amp+swap)/2
    antisymmetric = (amp-swap)/2
    trace = np.trace(amp,axis1=1,axis2=2)
    scalar = np.eye(3)[None,:,:,None,None]*trace[:,None,None,:,:]/3
    sectors = np.array([np.sum(np.abs(a)**2,axis=(1,2,3,4))
                        for a in (scalar,antisymmetric,symmetric-scalar)])
    fixed = np.sum(np.abs(amp[:,2,2])**2,axis=(1,2))
    independent = sectors.sum(axis=0)/9
    aligned = sectors[0]/3+2*sectors[2]/15
    # The axes and cube corners reproduce the sphere's fourth moment.
    cube = np.array(list(product((-1,1),repeat=3)))/np.sqrt(3)
    def directional_average(directions):
        v = np.einsum('ni,nj,cijrh->cnrh',directions,directions,amp)
        return np.mean(np.sum(np.abs(v)**2,axis=(2,3)),axis=1)
    np.testing.assert_allclose(aligned,.4*directional_average(np.eye(3))
                               +.6*directional_average(cube),rtol=1e-11)
    np.testing.assert_allclose(independent,np.sum(np.abs(amp)**2,axis=(1,2,3,4))/9,rtol=1e-11)
    return {name:dict(fraction=float(v[0]/(3*sum(v))),weights=v.tolist())
            for name,v in zip(("fixed_W3","aligned_average","independent_average",
                               "initial_spin0","initial_spin1","initial_spin2"),
                              (fixed,aligned,independent,*sectors))}


def main():
    words,basis = colour_basis()
    fixed = np.all(HEL==(1,-1,-1,1,1,1),axis=1)
    masks = {"all_transverse":np.ones(len(HEL),dtype=bool),
             "fixed_MHV":fixed,"equal_daughters":HEL[:,0]==HEL[:,-1]}
    results = []
    for tilt,pair in product((0,20),(.48,.06)):
        theta = np.radians(tilt)
        beam = (5/13*np.cos(theta),np.sin(theta),12/13*np.cos(theta))
        p = event(pair,0,beam)
        tensor = np.einsum('wabc,wh->abch',basis,amplitudes(p,words)).reshape(3,3,3,9,3,len(HEL))
        result = {name:summarize(tensor,mask) for name,mask in masks.items()}
        results.append(dict(tilt=tilt,Q_over_pair=12/pair,results=result))
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
