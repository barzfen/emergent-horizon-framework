"""Matched full and frozen-pole soft radiation for a fixed MHV assignment."""
import json

import numpy as np

from angular_ensemble import grid
from pair_dipole import OPENINGS, extrapolate, quadratic
from six_soft import ETA, HEL, amplitudes, event, gram, mhv_check

TERMS = ("finite_squared", "pole_finite_interference", "even_remainder")
GROUPS = ("daughter_pair", "daughter_spectator", "spectator_spectator")


def kernels(p, directions, harmonic):
    inv = 1 / (p[:, 0, None] - p[:, 1:] @ directions.T)
    dot = -(p * ETA) @ p.T
    weights = np.stack((np.ones(len(harmonic)), harmonic)) / len(harmonic)
    return np.einsum("ij,ik,jk,mk->mij", dot, inv, inv, weights)


def bilinear(left, right, soft):
    return np.einsum("a,aibj,b->ij", left.conj(), soft, right, optimize=True).real


def probe(angle, grams, angular_grids):
    words, hard, soft = grams
    theta = np.radians(angle)
    beam = (5/13 * np.cos(theta), np.sin(theta), 12/13 * np.cos(theta))
    helicity = np.flatnonzero(np.all(HEL == (1,-1,-1,1,1,1), axis=1))[0]
    rows = []
    for t in OPENINGS:
        p = event(beam, t)
        all_amplitudes = amplitudes(p, words)
        mhv_check(p, words, all_amplitudes)
        full = t * all_amplitudes[:, helicity]
        reversed_opening = t * amplitudes(event(beam, -t), words)[:, helicity]
        rows.append((p, full, (full - reversed_opening)/2, (full + reversed_opening)/2))

    pole = extrapolate(np.array([row[2] for row in rows]))[-1]
    pole_norm = quadratic(pole, hard)
    pole_colour = bilinear(pole, pole, soft) / pole_norm
    np.testing.assert_allclose(pole_colour.sum(axis=1), 0, atol=1e-10)
    np.testing.assert_allclose(pole_colour[0, -1], -1.5, atol=1e-10)

    daughters = np.isin(np.arange(6), (0, 5))
    masks = (daughters[:, None] & daughters, daughters[:, None] ^ daughters,
             ~daughters[:, None] & ~daughters)
    output = {}
    for n, (directions, harmonic) in angular_grids.items():
        sampled = []
        min_gap = 180.
        for t, (p, full, even, odd) in zip(OPENINGS, rows):
            k = kernels(p, directions, harmonic)
            cosine = (p[:, 1:]/p[:, :1]) @ directions.T
            min_gap = min(min_gap, np.degrees(np.arccos(np.clip(cosine.max(), -1, 1))))
            norm = quadratic(full, hard)
            full_colour = bilinear(full, full, soft) / norm
            full_m, frozen_m = (np.einsum("mij,ij->m", k, c)
                                for c in (full_colour, pole_colour))
            cf, cp = full_m[1]/full_m[0], frozen_m[1]/frozen_m[0]
            pairs = ((odd, odd), (2*even, odd), (even+pole, even-pole))
            colour = np.array([(bilinear(a, b, soft)
                               - np.vdot(a, hard @ b).real * pole_colour) / norm
                               for a, b in pairs])
            np.testing.assert_allclose(colour.sum(axis=0), full_colour-pole_colour, atol=1e-11)
            np.testing.assert_allclose(colour.sum(axis=1), 0, atol=1e-10)
            contrast_kernel = (k[1] - cp*k[0]) / full_m[0]
            parts = np.einsum("ij,aij,bij->ab", contrast_kernel, colour, masks)
            np.testing.assert_allclose(parts.sum(), cf-cp, atol=1e-12)
            sampled.append((cf, cp, (cf-cp)/t**2, parts/t**2))
        contrasts = np.array([row[:2] for row in sampled])
        slopes = -np.diff(contrasts, axis=0) / (.75*OPENINGS[:-1,None]**2)
        baseline = extrapolate(slopes)[-1]
        residual = extrapolate(np.array([row[2] for row in sampled]))
        table = extrapolate(np.array([row[3] for row in sampled]))
        np.testing.assert_allclose(baseline[0]-baseline[1], residual[-1], atol=3e-5)
        np.testing.assert_allclose(table[-1].sum(), residual[-1], atol=3e-5)
        np.testing.assert_allclose(table[-2], table[-1], rtol=.002, atol=3e-5)
        output[n] = {"full_and_pole_slopes": baseline.tolist(),
                     "residual": float(residual[-1]), "terms_by_emitter_group": table[-1].tolist(),
                     "minimum_soft_hard_gap_degrees": min_gap}
    return output


if __name__ == "__main__":
    grams = gram()
    angular_grids = {n: grid(20, 40, n) for n in (32, 64, 128)}
    data = {angle: probe(angle, grams, angular_grids) for angle in (0, 10, 20)}
    print(json.dumps({"terms": TERMS, "emitter_groups": GROUPS,
                      "openings": OPENINGS.tolist(), "beam_tilt_degrees": data}, indent=2))
