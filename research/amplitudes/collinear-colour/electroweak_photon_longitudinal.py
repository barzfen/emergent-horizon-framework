"""Sum physical final polarizations on the fixed photon-beam patch."""

from concurrent.futures import ProcessPoolExecutor
from itertools import product
import argparse
import json
import sys

import numpy as np

from electroweak_photon_patch import BOUNDS, MASS, MIXING, PAIR, nodes
from electroweak_rate import CHANNELS, amplitude, dot, evaluate, momenta, transverse
from six_soft import HEL


PHOTON = 3
TRANSVERSE = (-1, 1)
MASSIVE = (-1, 0, 1)
BASIS = np.eye(4, dtype=complex)
PLUS = np.array([1, 1j, 0, 0]) / np.sqrt(2)
MINUS = PLUS.conj()
ENDS = ((PLUS, PLUS), (BASIS[2], BASIS[2]), (BASIS[2], BASIS[3]),
        (BASIS[3], BASIS[2]), (BASIS[3], BASIS[3]))


def polarization_basis(p, masses):
    transverse_states = [transverse(p, np.full(6, h)) for h in TRANSVERSE]
    spatial = p[:, 1:]
    magnitude = np.linalg.norm(spatial, axis=-1)
    longitudinal = np.column_stack((magnitude, p[:, :1] * spatial / magnitude[:, None]))
    np.divide(longitudinal, masses[:, None], out=longitudinal, where=masses[:, None] > 0)
    longitudinal[masses == 0] = 0
    basis = np.stack((transverse_states[0], longitudinal, transverse_states[1]), axis=1)
    np.testing.assert_allclose(dot(basis, p[:, None, :]), 0, atol=1e-11)
    inner = dot(basis[:, :, None, :].conj(), basis[:, None, :, :])
    expected = np.tile(-np.eye(3), (len(p), 1, 1))
    expected[masses == 0, 1, 1] = 0
    np.testing.assert_allclose(inner, expected, atol=1e-11)
    return basis


def channel_amplitudes(external, coords, mw, all_incoming=False, rotated=False, ward=False):
    cosine, azimuth, opening, recoil = coords
    sine = np.sqrt(1 - cosine**2)
    beam = (cosine, sine * np.sin(azimuth), sine * np.cos(azimuth))
    mass_by_species = np.array([mw, mw, mw / np.sqrt(1 - MIXING), 0])
    masses = mass_by_species[np.argmax(np.abs(external), axis=-1)]
    p = momenta(PAIR, masses[None, :], beam, opening, recoil)[0]
    basis = polarization_basis(p, masses)
    if rotated:
        # Mix the three physical states at each massive leg independently
        # of the scattering plane. The total weight must be invariant.
        angle = .41
        c, s = np.cos(angle), np.sin(angle)
        rotation = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
        basis[masses > 0] = rotation @ basis[masses > 0]
    choices = [MASSIVE if mass else TRANSVERSE for mass in masses]
    if not all_incoming:
        choices[1] = (1,)
    helicities = np.array(list(product(*choices)))
    eps = basis[np.arange(6), helicities + 1]
    p = np.broadcast_to(p, eps.shape)
    external = np.broadcast_to(external, (len(eps), 6, 4))
    values = amplitude(p, eps, external, mw, MIXING)
    if ward:
        scale = np.maximum(1., np.abs(values))
        for leg in np.flatnonzero(masses == 0):
            replaced = eps.copy()
            replaced[:, leg] = p[:, leg]
            residual = amplitude(p, replaced, external, mw, MIXING)
            assert np.max(np.abs(residual) / scale) < 2e-7
    return helicities, values


def channel_weights(coords, mw=MASS, validate=False):
    weights = np.zeros((len(CHANNELS), 3, 3))
    photon = BASIS[PHOTON]
    for i, (a, b) in enumerate(ENDS):
        # Charge conservation fixes the recoil for ++ and permits either
        # ordering of W+ W- for neutral daughters. The all-neutral tree
        # vanishes: charged lines have no external endpoint and would loop.
        recoils = ((MINUS, MINUS),) if i == 0 else ((PLUS, MINUS), (MINUS, PLUS))
        for x, y in recoils:
            external = np.array([a, photon, photon, x, y, b])
            hs, values = channel_amplitudes(external, coords, mw, ward=validate)
            if validate:
                both, both_values = channel_amplitudes(external, coords, mw, all_incoming=True)
                _, rotated_values = channel_amplitudes(external, coords, mw, rotated=True)
                np.testing.assert_allclose(np.abs(values), np.abs(both_values[both[:, 1] == 1]),
                                           rtol=1e-9, atol=1e-10)
                np.testing.assert_array_equal(both, -both[::-1])
                np.testing.assert_allclose(np.abs(both_values), np.abs(both_values[::-1]),
                                           rtol=1e-9, atol=1e-10)
                np.testing.assert_allclose(np.vdot(values, values).real,
                                           np.vdot(rotated_values, rotated_values).real, rtol=1e-9)
            pair_long = np.count_nonzero(hs[:, (0, 5)] == 0, axis=1)
            recoil_long = np.count_nonzero(hs[:, (3, 4)] == 0, axis=1)
            np.add.at(weights[i], (pair_long, recoil_long), np.abs(values)**2)
    return weights


def fraction(weights):
    return float(weights[0] / (3 * np.sum(weights)))


def summarize(weights):
    return {
        'transverse': fraction(weights[:, 0, 0]),
        'pair_inclusive_recoil_transverse': fraction(weights[:, :, 0].sum(axis=1)),
        'pair_transverse_recoil_inclusive': fraction(weights[:, 0, :].sum(axis=1)),
        'fully_inclusive': fraction(weights.sum(axis=(1, 2))),
        'by_channel_pair_longitudinal_count_recoil_longitudinal_count': {
            name: channel.tolist() for name, channel in zip(CHANNELS, weights)
        }
    }


def point(args):
    coords, weight = args
    return weight * channel_weights(coords)


def validate():
    # Non-planar point with unequal recoil energies, inside the patch.
    coords = (.4, .23, .12, 4.04)
    cosine, azimuth, opening, recoil = coords
    sine = np.sqrt(1 - cosine**2)
    beam = (cosine, sine * np.sin(azimuth), sine * np.cos(azimuth))
    baseline = evaluate(PAIR, MASS, beam, MIXING, helicities=HEL[HEL[:, 0] == 1],
                        return_rates=True, incoming=(3, 3),
                        opening_azimuth=opening, recoil_energy=recoil)
    weights = channel_weights(coords, validate=True)
    np.testing.assert_allclose(weights[:, 0, 0], list(baseline.values()), rtol=1e-9)
    return summarize(weights)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('orders', type=int, nargs='*')
    parser.add_argument('--workers', type=int, default=6)
    args = parser.parse_args()
    result = dict(pair_mass=PAIR, w_mass=MASS, sin2_theta_w=MIXING, bounds=BOUNDS,
                  validation_point=validate(), grids={})
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        for order in args.orders:
            weights = np.sum(list(executor.map(point, nodes(order))), axis=0)
            result['grids'][order] = dict(nodes=order**4, **summarize(weights))
            print(f'Completed order {order} ({order**4} nodes)', file=sys.stderr, flush=True)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
