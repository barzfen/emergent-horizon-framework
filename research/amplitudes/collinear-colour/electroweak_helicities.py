"""Matched six-vector electroweak scan summed over transverse helicities."""
from itertools import product
import json
import sys

import numpy as np

from electroweak_rate import CHANNELS, HELICITIES, evaluate
from six_soft import COUNT, HEL, amplitudes
from su2_mass_control import event, tensor, transverse_polarizations
from su2_real_rate import colour_basis


def pair_rates(a):
    plus = (a[0,:,0]-a[1,:,1]+1j*(a[0,:,1]+a[1,:,0]))/2
    neutral = a[2,:,2]
    return np.array([np.vdot(v,v).real for v in (plus,neutral)])


def fraction(channels):
    return float(channels[0]/(3*sum(channels)))


def main(tilt):
    theta = np.radians(tilt)
    beam = (5/13*np.cos(theta),np.sin(theta),12/13*np.cos(theta))
    pair,mw = .48,.144
    words,basis = colour_basis()
    p0 = event(pair,0,beam)
    pm = event(pair,mw,beam)
    massless = np.einsum('wabc,wh->abch',basis,amplitudes(p0,words))
    polarizations = transverse_polarizations(pm)
    totals = {}
    rows = []
    # Global helicity reversal conjugates the tree amplitude up to a
    # colour transformation. Verify this on one configuration per tilt.
    check = evaluate(pair,mw,beam,.23,helicities=HELICITIES,return_rates=True)
    reverse = evaluate(pair,mw,beam,.23,helicities=-HELICITIES,return_rates=True)
    np.testing.assert_allclose(list(check.values()),list(reverse.values()),rtol=1e-8,atol=1e-13)
    for i,h in enumerate(HEL):
        if h[0]!=1:
            continue
        raw = evaluate(pair,mw,beam,.23,helicities=h,return_rates=True)
        models = np.zeros((3,5))
        models[0,:2] = pair_rates(massless[...,i])
        models[1,:2] = pair_rates(tensor(pm,mw,polarizations[:,i]).reshape(3,81,3))
        models[2] = [raw[k] for k in CHANNELS]
        # Each selected representative counts once together with its
        # global helicity reverse. Sum weights before forming ratios.
        labels = ["all_transverse"]
        if h[0]==h[-1]:
            labels += ["equal_daughters"]
            if COUNT[i] in (2,4):
                labels += ["equal_MHV_or_conjugate"]
            if COUNT[i]==3:
                labels += ["equal_NMHV"]
        else:
            labels += ["opposite_daughters"]
        for label in labels:
            totals[label] = totals.get(label,0)+2*models
        rows.append(dict(helicities=h.tolist(),massless=models[0].tolist(),
                         custodial=models[1].tolist(),electroweak=models[2].tolist()))
    summary = {}
    for name,weights in totals.items():
        a,b,c = map(fraction,weights)
        summary[name] = dict(massless=a,custodial=b,electroweak=c,
                             common_mass_shift=b-a,additional_mixing_shift=c-b,
                             electroweak_channel_shares=(weights[2]/sum(weights[2])).tolist())
    print(json.dumps(dict(tilt=tilt,pair_over_Q=pair/12,mW_over_pair=mw/pair,
                          sin_squared=.23,channels=CHANNELS,summary=summary,rows=rows),indent=2))


if __name__=='__main__':
    main(float(sys.argv[1]))
