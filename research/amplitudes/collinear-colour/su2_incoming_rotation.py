"""Resolve the common incoming colour rotation into isospin contributions."""
from itertools import product
import json

import numpy as np

from six_soft import HEL, amplitudes
from su2_incoming_average import rates, summarize
from su2_mass_control import event
from su2_real_rate import colour_basis


def fraction(weights):
    return float(weights[0]/(3*sum(weights)))


def scan(tensor):
    amplitude = rates(tensor)
    spin0 = np.trace(amplitude,axis1=1,axis2=2)/3

    def decompose(x, azimuth=0):
        n = np.array([np.sqrt(1-x)*np.cos(azimuth),
                      np.sqrt(1-x)*np.sin(azimuth),np.sqrt(x)])
        value = np.einsum('i,j,cijrh->crh',n,n,amplitude)
        spin2 = value-spin0
        scalar = np.sum(np.abs(spin0)**2,axis=(1,2))
        tensor_weight = np.sum(np.abs(spin2)**2,axis=(1,2))
        cross = 2*np.sum((spin0.conj()*spin2).real,axis=(1,2))
        full = np.sum(np.abs(value)**2,axis=(1,2))
        np.testing.assert_allclose(scalar+tensor_weight+cross,full,rtol=1e-12)
        return np.array([full,scalar,tensor_weight,cross])

    samples = np.array([0,.5,1.])
    powers = np.vander(samples,3,increasing=True)
    weights = np.array([decompose(x) for x in samples])
    coefficients = np.linalg.solve(powers,weights.reshape(3,-1)).reshape(3,4,2)
    errors = []
    for x,azimuth in product((.08,.23,.37,.61,.77,.94),(.31,1.18)):
        predicted = np.einsum('k,kij->ij',[1,x,x*x],coefficients)
        observed = decompose(x,azimuth)
        np.testing.assert_allclose(observed,predicted,rtol=1e-9,
                                   atol=1e-11*np.max(weights))
        errors.append(float(np.max(np.abs(observed-predicted))/np.max(weights)))
    average = np.einsum('k,kij->ij',[1,1/3,1/5],coefficients)
    np.testing.assert_allclose(average[3],0,atol=1e-11*np.max(weights))
    expected = summarize(tensor,np.ones(tensor.shape[-1],dtype=bool))
    np.testing.assert_allclose(average[0],expected["aligned_average"]["weights"],rtol=1e-11)
    fixed = weights[-1]
    return dict(coefficient_order=["constant","x","x_squared"],
                components=["full","spin0","spin2","interference"],
                channels=["same_sign","neutral"],coefficients=coefficients.tolist(),
                max_holdout_error_relative_to_peak_weight=max(errors),
                fixed_weights=fixed.tolist(),aligned_weights=average.tolist(),
                fixed_fraction=fraction(fixed[0]),
                fixed_without_interference=fraction(fixed[1]+fixed[2]),
                aligned_fraction=fraction(average[0]),
                perpendicular_fraction=fraction(weights[0,0]),
                independent_fraction=expected["independent_average"]["fraction"])


def main():
    words,basis = colour_basis()
    fixed = np.all(HEL==(1,-1,-1,1,1,1),axis=1)
    rows = []
    for tilt,pair in product((0,20),(.48,.06)):
        theta = np.radians(tilt)
        beam = (5/13*np.cos(theta),np.sin(theta),12/13*np.cos(theta))
        p = event(pair,0,beam)
        amplitudes_by_colour = np.einsum('wabc,wh->abch',basis,amplitudes(p,words))
        a = amplitudes_by_colour.reshape(3,3,3,9,3,len(HEL))
        rows.append(dict(tilt=tilt,Q_over_pair=12/pair,
                         all_transverse=scan(a),fixed_MHV=scan(a[...,fixed])))
    print(json.dumps(rows,indent=2))


if __name__ == '__main__':
    main()
