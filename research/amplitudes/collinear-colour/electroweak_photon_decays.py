"""Spin-correlated leptonic decays on the matched photon-beam patch."""

import argparse
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
import json
import sys

import numpy as np

from electroweak_photon_longitudinal import (BASIS, ENDS, MINUS, PHOTON, PLUS,
                                            fraction, polarization_basis)
from electroweak_photon_patch import BOUNDS, MASS, MIXING, PAIR, nodes
from electroweak_rate import CHANNELS, amplitude, momenta


FINAL = (0, 3, 4, 5)
CUTS = ((.25, 2.5), (.5, 2.5), (1., 2.5))
MODES = ('inclusive', 'transverse', 'diagonal', 'isotropic')
HELICITY_DIFFERENCE = np.arange(3)[None, :] - np.arange(3)[:, None]


@lru_cache(maxsize=None)
def decay_grid(order):
    c, weights = np.polynomial.legendre.leggauss(order)
    sine = np.sqrt(1 - c*c)
    # Each coefficient is multiplied by exp(-i h phi) in the decay amplitude.
    # The two rows correspond to spin +1 and -1 along the decay-lepton axis.
    coeff = np.array([np.column_stack(((c+s)/2, -sine/np.sqrt(2), (c-s)/2))
                      for s in (1, -1)])
    kernels = 1.5 * np.einsum('sai,saj,a->asij', coeff, coeff, weights)
    np.testing.assert_allclose(np.einsum('asii->si', kernels), 1, atol=2e-13)
    return c, sine, kernels


def beam_in_local_frame(p, basis, beam):
    u = basis[2, 1:].real * np.sqrt(2)
    v = basis[2, 1:].imag * np.sqrt(2)
    n = p[1:] / np.linalg.norm(p[1:])
    return np.stack((u, v, n)) @ beam


def visible(energy, parallel):
    thresholds, eta = np.array(CUTS).T
    pt_squared = np.maximum(energy**2 - parallel**2, 0)
    return ((pt_squared[..., None] > (thresholds * MASS)**2)
            & (np.abs(parallel[..., None]) < energy[..., None] * np.tanh(eta)))


def parallel_limit(energy, threshold, eta):
    limit = np.minimum(energy * np.tanh(eta),
                       np.sqrt(np.maximum(0, energy**2 - threshold**2)))
    return np.where(energy > threshold, limit, -1.)


def azimuth_moments(lower, upper, center, radius, phase):
    """Average exp(i k phi) over the accepted azimuths, for k = 0, 1, 2."""
    nonzero = radius > 0
    low = np.divide(lower - center, radius, out=np.zeros_like(radius), where=nonzero)
    high = np.divide(upper - center, radius, out=np.zeros_like(radius), where=nonzero)
    a = np.arccos(np.clip(high, -1., 1.))
    b = np.maximum(a, np.arccos(np.clip(low, -1., 1.)))
    zero = np.where(nonzero, (b-a)/np.pi, (lower < center) & (center < upper))
    one = np.where(nonzero, (np.sin(b)-np.sin(a))/np.pi, 0.) * np.exp(1j*phase)
    two = np.where(nonzero, (np.sin(2*b)-np.sin(2*a))/(2*np.pi), 0.) * np.exp(2j*phase)
    return np.stack((zero, one, two, two.conj(), one.conj()), axis=-1)


def decay_matrices(p, pols, beam, mass, order, charge=None):
    c, sine, kernels = decay_grid(order)
    local_beam = beam_in_local_frame(p, pols, beam)
    energy, momentum = p[0], np.linalg.norm(p[1:])
    lepton_energy = (energy + momentum*c) / 2
    center = (momentum + energy*c) * local_beam[2] / 2
    radius = mass * sine * np.linalg.norm(local_beam[:2]) / 2
    phase = np.arctan2(local_beam[1], local_beam[0])
    matrices = []
    for pt, eta in CUTS:
        first = parallel_limit(lepton_energy, pt*MASS, eta)
        low, high = -first, first
        if charge is None:
            second = parallel_limit(energy - lepton_energy, pt*MASS, eta)
            parent_parallel = momentum * local_beam[2]
            low = np.maximum(low, parent_parallel - second)
            high = np.minimum(high, parent_parallel + second)
        moments = azimuth_moments(low, high, center, radius, phase)
        raw = np.einsum('aij,asij->sij', moments[:, HELICITY_DIFFERENCE], kernels)
        if charge is None:
            left, right = (-.5 + MIXING)**2, MIXING**2
            matrices.append((right*raw[0] + left*raw[1]) / (left+right))
        else:
            matrices.append(raw[0 if charge == 1 else 1])
    return np.array(matrices)


def fold(a, matrices):
    """Contract the production amplitudes with four decay matrices."""
    b = a
    for leg, matrix in enumerate(matrices, start=1):
        b = np.moveaxis(np.tensordot(b, matrix, axes=(leg, 0)), -1, leg)
    weight = np.vdot(a, b)
    np.testing.assert_allclose(weight.imag, 0, atol=1e-8)
    return weight.real


def production(external, coords):
    cosine, azimuth, opening, recoil = coords
    sine = np.sqrt(1 - cosine*cosine)
    beam = np.array((cosine, sine * np.sin(azimuth), sine * np.cos(azimuth)))
    masses = np.array([MASS, MASS, MASS / np.sqrt(1 - MIXING), 0])
    masses = masses[np.argmax(np.abs(external), axis=-1)]
    p = momenta(PAIR, masses[None, :], beam, opening, recoil)[0]
    basis = polarization_basis(p, masses)
    choices = [(-1, 0, 1) if mass else (-1, 1) for mass in masses]
    shape = tuple(map(len, choices))
    # Broadcast the polarization product over the six external legs.
    hs = np.stack(np.meshgrid(*choices, indexing='ij'), axis=-1).reshape(-1, 6)
    eps = basis[np.arange(6), hs+1]
    ext = np.broadcast_to(external, (len(eps), 6, 4))
    values = amplitude(np.broadcast_to(p, eps.shape), eps, ext, MASS, MIXING)
    amplitudes = values.reshape(shape).transpose(1, 2, *FINAL).reshape(4, *(shape[i] for i in FINAL))
    return p, basis, beam, masses, amplitudes


def weights_at_point(coords, decay_orders):
    no_cuts = np.zeros((len(CHANNELS), 2))
    accepted = np.zeros((len(decay_orders), len(CUTS), len(CHANNELS), len(MODES)))
    cache = {}
    photon = BASIS[PHOTON]
    for channel, (a, b) in enumerate(ENDS):
        recoils = ((-1, -1),) if channel == 0 else ((1, -1), (-1, 1))
        for charges in recoils:
            external = np.array([a, photon, photon,
                                 PLUS if charges[0] == 1 else MINUS,
                                 PLUS if charges[1] == 1 else MINUS, b])
            p, basis, beam, masses, amplitudes = production(external, coords)
            tt = amplitudes.copy()
            for axis, leg in enumerate(FINAL, start=1):
                if masses[leg]:
                    tt.swapaxes(0, axis)[1] = 0
            no_cuts[channel] += [np.vdot(x, x).real for x in (amplitudes, tt)]

            decay_charges = (1 if channel == 0 else None, *charges, 1 if channel == 0 else None)
            for oi, order in enumerate(decay_orders):
                matrices = []
                for leg, charge in zip(FINAL, decay_charges):
                    key = (tuple(p[leg]), charge, order)
                    if key not in cache:
                        if masses[leg]:
                            cache[key] = decay_matrices(p[leg], basis[leg], beam, masses[leg],
                                                        order, charge)
                        else:
                            passes = visible(p[leg, 0], p[leg, 1:] @ beam)
                            cache[key] = passes[:, None, None] * np.eye(2)
                    matrices.append(cache[key])
                for ci, cut_matrices in enumerate(zip(*matrices)):
                    diagonal = [np.diag(np.diag(d)) for d in cut_matrices]
                    isotropic = np.prod([np.trace(d).real / len(d) for d in cut_matrices])
                    accepted[oi, ci, channel] += [
                        fold(amplitudes, cut_matrices),
                        fold(tt, cut_matrices),
                        fold(amplitudes, diagonal),
                        isotropic * np.vdot(amplitudes, amplitudes).real,
                    ]
    return no_cuts, accepted


def point(args):
    coords, weight, orders = args
    return tuple(weight * x for x in weights_at_point(coords, orders))


def summarize(no_cuts, accepted, orders):
    result = {'no_cuts': dict(zip(MODES[:2], (fraction(no_cuts[:, 0]), fraction(no_cuts[:, 1])))),
              'no_cut_weights': dict(zip(CHANNELS, no_cuts.tolist())), 'decay_orders': {}}
    for order, cut_results in zip(orders, accepted):
        result['decay_orders'][order] = [
            dict(pt_over_mw=pt, max_abs_eta=eta,
                 fractions={mode: fraction(values[:, i]) for i, mode in enumerate(MODES)},
                 efficiencies=dict(zip(CHANNELS, (values[:, 0] / no_cuts[:, 0]).tolist())),
                 weights=dict(zip(CHANNELS, values.tolist())))
            for (pt, eta), values in zip(CUTS, cut_results)]
    return result


def validate(orders):
    coords = (.4, .23, .12, 4.04)
    no_cuts, accepted = weights_at_point(coords, orders)
    rng = np.random.default_rng(7)
    a = rng.normal(size=(4, 3, 2, 3, 2)) + 1j*rng.normal(size=(4, 3, 2, 3, 2))
    vectors = [rng.normal(size=n) + 1j*rng.normal(size=n) for n in (3, 2, 3, 2)]
    direct = np.einsum('habcd,a,b,c,d->h', a, *vectors)
    np.testing.assert_allclose(fold(a, [np.outer(v, v.conj()) for v in vectors]),
                               np.vdot(direct, direct).real, rtol=1e-12)
    radius = np.array([1., 1., 1., 0.])
    moments = azimuth_moments(np.array([-2., -1., 2., -1.]),
                              np.array([2., 0., 3., 1.]), np.zeros(4), radius, 0.)
    np.testing.assert_allclose(moments[:, :3], [[1, 0, 0], [.5, -1/np.pi, 0],
                                                [0, 0, 0], [1, 0, 0]], atol=2e-13)
    assert np.all(accepted >= -1e-9)
    assert np.all(np.diff(accepted, axis=1) <= 1e-9)
    assert np.all(accepted[..., 0] <= no_cuts[:, 0])
    return summarize(no_cuts, accepted, orders)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('production_orders', type=int, nargs='*')
    parser.add_argument('--decay-orders', type=int, nargs='+', default=[128, 512, 1024])
    parser.add_argument('--workers', type=int, default=8)
    args = parser.parse_args()
    result = dict(pair_mass=PAIR, w_mass=MASS, sin2_theta_w=MIXING, bounds=BOUNDS,
                  modes=MODES, channels=CHANNELS, validation_point=validate(args.decay_orders),
                  grids={})
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        for order in args.production_orders:
            rows = list(executor.map(point, ((c, w, args.decay_orders) for c, w in nodes(order))))
            no_cuts, accepted = (np.sum(x, axis=0) for x in zip(*rows))
            result['grids'][order] = dict(nodes=order**4,
                                          **summarize(no_cuts, accepted, args.decay_orders))
            print(f'Completed order {order} ({order**4} nodes)', file=sys.stderr, flush=True)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
