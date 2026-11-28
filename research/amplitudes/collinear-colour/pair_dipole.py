"""Test the first finite hard-pair colour correlation at six gluons."""
from collections import defaultdict
import json

import numpy as np

from orders import tensor_rows
from six_soft import HEL, amplitudes, event, gram, mhv_check
from su3_probe import METRIC


OPENINGS = np.array([.004, .002, .001, .0005])
PLANAR_SHARES = np.array([1/6, 1/3, 1/2])
EIGENVALUES = np.array([-3, -1.5, 1])


def singlet_gram(words):
    traces = defaultdict(lambda: np.zeros(len(words)))
    columns = {word: index for index, word in enumerate(words)}
    for key, word, value in tensor_rows(6):
        if key[0] == key[-1]:
            traces[key[1:-1]][columns[word]] += float(value / METRIC[key[0]])
    result = np.zeros((len(words), len(words)))
    for spectators, trace in traces.items():
        result += np.outer(trace, trace) / (8 * np.prod(np.array(METRIC)[list(spectators)]))
    return result


def quadratic(vector, matrix):
    return np.vdot(vector, matrix @ vector).real


def extrapolate(values):
    return (4 * values[1:] - values[:-1]) / 3


def probe(angle, grams, singlet, reverse):
    words, hard, soft = grams
    dipole = soft[:, 0, :, -1]
    theta = np.radians(angle)
    beam = (5/13 * np.cos(theta), np.sin(theta), 12/13 * np.cos(theta))
    helicity = np.flatnonzero(np.all(HEL == (1,-1,-1,1,1,1), axis=1))[0]
    poles, finite, measured = [], [], []
    for t in OPENINGS:
        p = event(beam, t)
        amplitudes_at_t = amplitudes(p, words)
        mhv_check(p, words, amplitudes_at_t)
        full = amplitudes_at_t[:, helicity]
        swapped = amplitudes(event(beam, -t), words)[:, helicity]
        np.testing.assert_allclose(swapped, full[reverse], rtol=1e-7, atol=1e-7)
        poles.append(t * (full - swapped) / 2)
        finite.append((full + swapped) / 2)
        scaled = t * full
        measured.append(quadratic(scaled, dipole + 1.5 * hard)
                        / quadratic(scaled, hard) / t**2)

    leading = extrapolate(np.array(poles))[-1]
    regular = extrapolate(np.array(finite))[-1]
    lead_norm = quadratic(leading, hard)
    finite_norm = quadratic(regular, hard)
    np.testing.assert_allclose(quadratic(leading, dipole) / lead_norm, -1.5, atol=1e-10)

    mean = quadratic(regular, dipole) / finite_norm
    # The symmetric sector has three distinct eigenvalues. The singlet
    # trace and the first moment determine all shares given unit total.
    singlet_share = quadratic(regular, singlet) / finite_norm
    share_27 = (mean + 1.5 + 1.5 * singlet_share) / 2.5
    shares = np.array([singlet_share, 1 - singlet_share - share_27, share_27])
    assert np.all(shares >= 0)
    norm_ratio = finite_norm / lead_norm
    predicted = norm_ratio * (mean + 1.5)
    independent = extrapolate(np.array(measured))
    np.testing.assert_allclose(independent[-2:], predicted, rtol=1e-5, atol=1e-7)
    return {
        "shares": shares.tolist(),
        "finite_pair_dipole": mean,
        "finite_to_pole_squared_norm": norm_ratio,
        "full_amplitude_shift_coefficient": independent[-1],
        "raw_shift_coefficients": measured,
        "predicted_shift_coefficient": predicted,
        "shift_coefficient_if_planar_shares_at_same_norm": norm_ratio,
        "channel_contributions_to_shift_per_norm_vs_planar": (
            (shares - PLANAR_SHARES) * (EIGENVALUES + 1.5)).tolist(),
    }


if __name__ == "__main__":
    grams = gram()
    words = grams[0]
    reverse = [words.index((w[0], *w[1:-1][::-1], w[-1])) for w in words]
    singlet = singlet_gram(words)
    rows = {angle: probe(angle, grams, singlet, reverse)
            for angle in (0, 2, -2, 5, 10, 20, 35, 60)}
    np.testing.assert_allclose(rows[0]["shares"], PLANAR_SHARES, atol=1e-8)
    for name in ("shares", "full_amplitude_shift_coefficient"):
        np.testing.assert_allclose(rows[2][name], rows[-2][name], rtol=1e-6)
    print(json.dumps({"opening_parameter": "t in six_soft.event",
                      "openings": OPENINGS.tolist(), "beam_tilt_degrees": rows}, indent=2))
