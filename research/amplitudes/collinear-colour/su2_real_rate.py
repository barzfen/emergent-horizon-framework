"""Test the SU(2) rate combination on real six-boson scattering events."""
from itertools import permutations
import json

import numpy as np

from six_soft import HEL, amplitudes, event, mhv_check
from su2_ratio import chains


def colour_basis():
    words = [(0,*middle,5) for middle in permutations(range(1,5))]
    tensors = np.zeros((len(words),3,81,3))
    for j,word in enumerate(words):
        for first in range(3):
            for suffix,sign in chains(first,4):
                key = [0]*6
                for index, colour in zip(word,(first,*suffix)):
                    key[index] = colour
                spectator = sum(key[i]*3**(4-i) for i in range(1,5))
                tensors[j,key[0],spectator,key[5]] = sign
    return words,tensors


def measurements(tensor, mask):
    tensor = tensor[...,mask]
    pp = (tensor[0,:,0]-tensor[1,:,1]+1j*(tensor[0,:,1]+tensor[1,:,0]))/2
    nn = tensor[2,:,2]
    rp,rn = (np.sum(np.abs(a)**2) for a in (pp,nn))
    symmetric = (tensor+tensor.swapaxes(0,2))/2
    np.testing.assert_allclose(3*(rp+rn), np.sum(np.abs(symmetric)**2), rtol=1e-10)
    return float(rp/(3*(rp+rn))),float(rp/rn)


def main():
    words,basis = colour_basis()
    equal = HEL[:,0]==HEL[:,-1]
    fixed = np.all(HEL==(1,-1,-1,1,1,1),axis=1)
    masks = {"fixed_MHV":fixed,"equal_pair_all_spectator_helicities":equal,
             "all_helicities":np.ones(len(HEL),dtype=bool)}
    result = {}
    for angle in (0,10,20):
        theta = np.radians(angle)
        beam = (5/13*np.cos(theta),np.sin(theta),12/13*np.cos(theta))
        rows = []
        for t in (.008,.004,.002,.001):
            p = event(beam,t)
            vals = amplitudes(p,words)
            mhv_check(p,words,vals)
            tensor = np.einsum('wabc,wh->abch',basis,vals)
            values = {key:measurements(tensor,mask) for key,mask in masks.items()}
            rows.append(dict(t=t,weights=values))
        if angle==0:
            assert abs(rows[-1]['weights']['fixed_MHV'][0]-1/9)<1e-5
        result[angle] = rows
    print(json.dumps(dict(columns=['candidate_fraction','same_sign_to_neutral'],
                          beam_tilt_degrees=result),indent=2))


if __name__=='__main__':
    main()
