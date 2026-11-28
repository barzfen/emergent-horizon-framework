"""Integrate the photon-initial transverse rates over a matched patch."""
from concurrent.futures import ProcessPoolExecutor
from itertools import product
import json
import sys

import numpy as np

from electroweak_rate import HELICITIES, evaluate, momenta
from six_soft import HEL, amplitudes
from su2_incoming_rotation import fraction
from su2_incoming_average import rates
from su2_real_rate import colour_basis

PAIR = .48
MASS = .30*PAIR
MIXING = .23
BOUNDS = ((np.cos(np.radians(75)),np.cos(np.radians(60))),
          (0.,np.radians(25)),(-np.radians(20),np.radians(20)),(3.92,4.08))


def nodes(order):
    x,w = np.polynomial.legendre.leggauss(order)
    axes = [[((a+b+(b-a)*u)/2,v/2) for u,v in zip(x,w)] for a,b in BOUNDS]
    for point in product(*axes):
        yield tuple(u for u,w in point),float(np.prod([w for u,w in point]))


def point(args):
    coords, weight, massive = args
    cosine,azimuth,opening,recoil = coords
    transverse = np.sqrt(1-cosine*cosine)
    beam = (cosine,transverse*np.sin(azimuth),transverse*np.cos(azimuth))
    words,basis = colour_basis()
    p = momenta(PAIR,np.zeros((1,6)),beam,opening,recoil)[0]
    a = np.einsum('wabc,wh->abch',basis,amplitudes(p,words)).reshape(3,3,3,9,3,len(HEL))
    amplitudes_by_channel = rates(a)
    fixed = amplitudes_by_channel[:,2,2]
    spin0 = np.trace(amplitudes_by_channel,axis1=1,axis2=2)/3
    spin2 = fixed-spin0
    cross = 2*np.sum((spin0.conj()*spin2).real,axis=(1,2))
    total = np.sum(np.abs(fixed)**2,axis=(1,2))
    symmetric = (amplitudes_by_channel+amplitudes_by_channel.swapaxes(1,2))/2
    trace_part = np.eye(3)[None,:,:,None,None]*spin0[:,None,None]
    spin2_norm = np.sum(np.abs(symmetric-trace_part)**2,axis=(1,2,3,4))
    aligned = np.sum(np.abs(spin0)**2,axis=(1,2))+2*spin2_norm/15
    heavy = None
    if massive:
        heavy = evaluate(PAIR,MASS,beam,MIXING,helicities=HEL[HEL[:,0]==1],
                         return_rates=True,incoming=(3,3),
                         opening_azimuth=opening,recoil_energy=recoil)
    return dict(coords=coords,weight=weight,massless=total.tolist(),
                interference=cross.tolist(),aligned=aligned.tolist(),massive=heavy)


def integrate(executor,order,massive):
    rows = list(executor.map(point,((coord,w,massive) for coord,w in nodes(order))))
    def combine(key):
        return np.sum([row['weight']*np.array(row[key]) for row in rows],axis=0)
    light,cross,aligned = (combine(k) for k in ('massless','interference','aligned'))
    summary = dict(massless=fraction(light),without_interference=fraction(light-cross),
                   aligned=fraction(aligned),interference_over_massless=(cross/light).tolist(),
                   cross_sign_counts=np.sum(np.sign([row['interference'] for row in rows]),axis=0).tolist(),
                   nodes=len(rows))
    if massive:
        heavy = {k:sum(row['weight']*row['massive'][k] for row in rows)
                 for k in rows[0]['massive']}
        summary['massive'] = fraction([heavy['++'],sum(v for k,v in heavy.items() if k!='++')])
        summary['massive_shift'] = summary['massive']-summary['massless']
        summary['massive_channel_weights'] = heavy
    return dict(summary=summary,nodes=rows)


def validate_batch():
    beam = (.4,.2,np.sqrt(.8))
    hs = np.array([HELICITIES,-HELICITIES])
    options = dict(return_rates=True,incoming=(3,3),opening_azimuth=.12,recoil_energy=4.04)
    separate = [evaluate(PAIR,MASS,beam,MIXING,helicities=h,ward=True,**options) for h in hs]
    np.testing.assert_allclose(list(separate[0].values()),list(separate[1].values()),rtol=1e-9,atol=1e-13)
    batch = evaluate(PAIR,MASS,beam,MIXING,helicities=hs,**options)
    np.testing.assert_allclose(list(batch.values()),np.sum([list(x.values()) for x in separate],axis=0),rtol=1e-10)
    massless = evaluate(PAIR,0,beam,MIXING,helicities=HEL[HEL[:,0]==1],**options)
    point_result = point(((beam[0],np.arctan2(beam[1],beam[2]),.12,4.04),1.,False))
    np.testing.assert_allclose(fraction([massless['++'],sum(v for k,v in massless.items() if k!='++')]),
                               fraction(point_result['massless']),rtol=1e-9)


if __name__ == '__main__':
    validate_batch()
    order = int(sys.argv[1])
    with ProcessPoolExecutor(max_workers=6) as executor:
        print(json.dumps(integrate(executor,order,'--massless' not in sys.argv),indent=2))
