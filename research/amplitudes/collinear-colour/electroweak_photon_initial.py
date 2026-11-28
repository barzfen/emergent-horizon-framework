"""Compare the pole-free rate diagnostic for a fixed photon initial state."""
import json
import sys

import numpy as np

from electroweak_rate import CHANNELS, HELICITIES, evaluate
from electroweak_helicities import fraction, pair_rates
from six_soft import HEL, amplitudes
from su2_mass_control import event
from su2_real_rate import colour_basis


def run(tilt,pair):
    theta = np.radians(tilt)
    beam = (5/13*np.cos(theta),np.sin(theta),12/13*np.cos(theta))
    models = (0,.30*pair)
    incoming = (3,3)
    words,basis = colour_basis()
    p0 = event(pair,0,beam)
    massless = np.einsum('wabc,wh->abch',basis,amplitudes(p0,words))
    fixed_w3 = massless.reshape(3,3,3,9,3,len(HEL))[:,2,2]
    massless_weights = []
    pure_weights = []
    rows = []
    totals = np.zeros((3,2,len(CHANNELS)))
    for index,h in enumerate(HEL):
        if h[0]!=1:
            continue
        group = 1 if h[0]==h[-1] else 2
        reference = np.array_equal(h,HELICITIES)
        weights = np.array([list(evaluate(pair,mw,beam,.23,ward=reference,
                                          helicities=h,return_rates=True,incoming=incoming).values())
                            for mw in models])
        pure = pair_rates(fixed_w3[...,index])
        rotated = np.array([weights[0,0],weights[0,1:].sum()])
        massless_weights.append(rotated)
        pure_weights.append(pure)
        if reference:
            reverse = np.array([list(evaluate(pair,mw,beam,.23,helicities=-h,
                                               return_rates=True,incoming=incoming).values())
                                for mw in models])
            np.testing.assert_allclose(weights,reverse,rtol=1e-9,atol=1e-13)
        totals[0] += 2*weights
        totals[group] += 2*weights
        rows.append(dict(helicities=h.tolist(),weights=weights.tolist()))
    pure = np.array(pure_weights)
    rotated = np.array(massless_weights)
    # Use a single common factor and compare unnormalized channel
    # weights, so vanishing helicity channels do not amplify roundoff.
    normalization = rotated.sum()/pure.sum()
    np.testing.assert_allclose(rotated,normalization*pure,rtol=1e-7,
                               atol=1e-9*rotated.max())
    summary = {}
    for name,weights in zip(("all_transverse","equal_daughters","opposite_daughters"),totals):
        base,physical = map(fraction,weights)
        summary[name] = dict(massless=base,electroweak=physical,shift=physical-base,
                             channel_shares=(weights/weights.sum(axis=1,keepdims=True)).tolist())
    return dict(tilt=tilt,pair_over_Q=pair/12,mW_over_pair=.30,
                initial=["gamma","gamma"],channels=CHANNELS,summary=summary,rows=rows)


if __name__ == '__main__':
    print(json.dumps(run(*map(float,sys.argv[1:])),indent=2))
