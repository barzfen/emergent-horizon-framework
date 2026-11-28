"""Test visible-object tagging and channel migration on the photon patch."""

import argparse
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
import json
import sys

import numpy as np
from scipy.stats import qmc

from electroweak_photon_decays import CUTS, FINAL, production
from electroweak_photon_longitudinal import BASIS, ENDS, MINUS, PHOTON, PLUS, fraction
from electroweak_photon_patch import BOUNDS, MASS, MIXING, PAIR, nodes
from electroweak_rate import CHANNELS, dot


THRESHOLDS = (CUTS[0][0], CUTS[-1][0])
MAX_ETA = CUTS[0][1]
RESOLUTIONS = (0., .10, .20, .30)
Z_MASS = MASS / np.sqrt(1 - MIXING)
Z_WINDOW = .10
LABELS = ("WW", "ZZ", "Zgamma", "gammagamma", "unassigned")
TRUTH_TO_LABEL = (0, 1, 2, 2, 3)
METRICS = ("uncut", "all_objects_pass", "true_tag_selected",
           "separation_loss_within_parent_only", "separation_loss_between_parents_only",
           "separation_loss_both")


@lru_cache(maxsize=None)
def sample(power, seed):
    # Two angles, a lepton-flavour draw and a Z chirality draw per parent.
    return qmc.Sobol(d=16, scramble=True, seed=seed).random_base2(power).reshape(-1, 4, 4)


def daughters(parent, basis, mass, u):
    c = 2*u[:, 0] - 1
    phi = 2*np.pi*u[:, 1]
    sine = np.sqrt(1 - c*c)
    px = np.sqrt(2) * basis[2, 1:].real
    py = np.sqrt(2) * basis[2, 1:].imag
    magnitude = np.linalg.norm(parent[1:])
    axis = parent[1:] / magnitude
    transverse = sine[:, None] * (np.cos(phi)[:, None]*px + np.sin(phi)[:, None]*py)
    first = np.column_stack(((parent[0] + magnitude*c)/2,
                             (mass*transverse + (magnitude + parent[0]*c)[:, None]*axis)/2))
    return first, parent - first, c, phi


def decay_event(p, basis, masses, amplitudes, charges, u):
    momenta, signs, flavours, parents = [], [], [], []
    factors, massive_axes, photon_axes = [], [], []
    for i, (leg, charge) in enumerate(zip(FINAL, charges)):
        if not masses[leg]:
            momenta.append(np.broadcast_to(p[leg], (len(u), 4)))
            signs.append(0)
            flavours.append(np.full(len(u), -1))
            parents.append(leg)
            photon_axes.append(i + 1)
            continue
        first, second, c, phi = daughters(p[leg], basis[leg], masses[leg], u[:, i])
        flavour = u[:, i, 2] < .5
        momenta.append(first)
        signs.append(charge if charge else -1)
        flavours.append(flavour)
        parents.append(leg)
        spin = charge
        if not charge:
            momenta.append(second)
            signs.append(1)
            flavours.append(flavour)
            parents.append(leg)
            left, right = (-.5 + MIXING)**2, MIXING**2
            spin = np.where(u[:, i, 3] < right/(left+right), 1, -1)
        phase = np.exp(1j*phi)
        factors.append(np.sqrt(3)*np.column_stack(((c+spin)*phase/2,
                                                  -np.sqrt((1-c*c)/2),
                                                  (c-spin)*phase.conj()/2)))
        massive_axes.append(i + 1)

    # Sum external photon polarizations incoherently. Contract massive
    # production helicities coherently with their decay amplitudes.
    kernel = factors[0]
    for factor in factors[1:]:
        kernel = (kernel[:, :, None]*factor[:, None, :]).reshape(len(u), -1)
    production_matrix = amplitudes.transpose(0, *photon_axes, *massive_axes)
    chain = kernel @ production_matrix.reshape(-1, kernel.shape[1]).T
    weights = np.sum(np.abs(chain)**2, axis=1)
    return np.stack(momenta, axis=1), np.array(signs), np.stack(flavours, axis=1), np.array(parents), weights


def visible_kinematics(objects, beam):
    # Azimuth about the incoming photon axis.
    x = np.cross([0., 1., 0.], beam)
    x /= np.linalg.norm(x)
    y = np.cross(beam, x)
    spatial = objects[..., 1:]
    qx, qy, qz = spatial @ x, spatial @ y, spatial @ beam
    pt = np.hypot(qx, qy)
    with np.errstate(divide="ignore"):
        eta = np.arcsinh(qz/pt)
    phi = np.arctan2(qy, qx)
    dphi = np.abs(phi[:, :, None] - phi[:, None, :])
    distance = np.hypot(eta[:, :, None]-eta[:, None, :], np.minimum(dphi, 2*np.pi-dphi))
    return pt, eta, distance


def resolve(passes, pt_order, distance, radius):
    if not radius:
        return passes
    rows = np.arange(len(passes))
    remaining = passes.copy()
    resolved = np.zeros_like(passes)
    for index in pt_order.T:
        keep = remaining[rows, index]
        resolved[rows, index] = keep
        remaining &= ~(keep[:, None] & (distance[rows, index] < radius))
    return resolved


def pair_candidates(objects, signs, flavours):
    lepton_indices = np.flatnonzero(signs)
    i, j = np.triu_indices(len(lepton_indices), k=1)
    i, j = lepton_indices[i], lepton_indices[j]
    opposite = signs[i] != signs[j]
    ossf = opposite & (flavours[:, i] == flavours[:, j])
    combined = objects[:, i] + objects[:, j]
    z_score = np.abs(np.sqrt(np.maximum(0, dot(combined, combined)))/Z_MASS - 1)
    z_score = np.where(ossf & (z_score < Z_WINDOW), z_score, np.inf)
    disjoint = (i[:, None] != i) & (i[:, None] != j) & (j[:, None] != i) & (j[:, None] != j)
    a, b = np.where(np.triu(disjoint, k=1))
    return i, j, opposite, z_score, a, b


def classify(keep, signs, distance, candidates):
    """Classify using visible quantities only, with no parent labels."""
    i, j, opposite, z_score, a, b = candidates
    labels = np.full(len(keep), len(LABELS)-1)
    selected = np.full((len(keep), 4), -1)
    n_plus = keep[:, signs > 0].sum(axis=1)
    n_minus = keep[:, signs < 0].sum(axis=1)
    n_photon = keep[:, signs == 0].sum(axis=1)
    pairs_kept = keep[:, i] & keep[:, j]
    z_score = np.where(pairs_kept, z_score, np.inf)

    rows = np.flatnonzero((n_plus == 2) & (n_minus == 2) & (n_photon == 0))
    if len(rows):
        d = distance[rows[:, None], i, j]
        closest = np.argmin(np.where(pairs_kept[rows] & ~opposite, d, np.inf), axis=1)
        labels[rows] = 0
        selected[rows, :2] = np.stack((i[closest], j[closest]), axis=1)

    rows = np.flatnonzero((n_plus == 3) & (n_minus == 3) & (n_photon == 0))
    if len(rows):
        score = z_score[rows][:, a] + z_score[rows][:, b]
        best = np.argmin(score, axis=1)
        valid = np.isfinite(score[np.arange(len(rows)), best])
        rows, best = rows[valid], best[valid]
        labels[rows] = 1
        selected[rows] = np.stack((i[a[best]], j[a[best]], i[b[best]], j[b[best]]), axis=1)

    rows = np.flatnonzero((n_plus == 2) & (n_minus == 2) & (n_photon == 1))
    if len(rows):
        score = z_score[rows]
        best = np.argmin(score, axis=1)
        valid = np.isfinite(score[np.arange(len(rows)), best])
        rows, best = rows[valid], best[valid]
        labels[rows] = 2
        selected[rows, :2] = np.stack((i[best], j[best]), axis=1)

    labels[(n_plus == 1) & (n_minus == 1) & (n_photon == 2)] = 3
    return labels, selected


def correct_tag(channel, labels, selected, parents):
    accepted = labels == TRUTH_TO_LABEL[channel]
    if channel == 0:
        return accepted & np.all(np.sort(parents[selected[:, :2]], axis=1) == (0, 5), axis=1)
    if channel == 1:
        paired = parents[selected]
        return accepted & (paired[:, 0] == paired[:, 1]) & (paired[:, 2] == paired[:, 3])
    if channel in (2, 3):
        return accepted & np.all(parents[selected[:, :2]] == (0 if channel == 2 else 5), axis=1)
    return accepted


def score(channel, objects, signs, flavours, parents, weights, beam):
    pt, eta, distance = visible_kinematics(objects, beam)
    pt_order = np.argsort(-pt, axis=1)
    candidates = pair_candidates(objects, signs, flavours)
    migration = np.zeros((len(THRESHOLDS), len(RESOLUTIONS), len(LABELS)))
    metrics = np.zeros((*migration.shape[:2], len(METRICS)))
    first, second = np.triu_indices(len(signs), k=1)
    within_parent = parents[first] == parents[second]
    for ci, pt_min in enumerate(THRESHOLDS):
        passes = (pt > pt_min*MASS) & (np.abs(eta) < MAX_ETA)
        all_pass = passes.all(axis=1)
        all_pass_distances = distance[all_pass][:, first, second]
        passing_weights = weights[all_pass]
        for ri, radius in enumerate(RESOLUTIONS):
            keep = resolve(passes, pt_order, distance, radius)
            labels, selected = classify(keep, signs, distance, candidates)
            migration[ci, ri] = np.bincount(labels, weights=weights, minlength=len(LABELS))
            correct = correct_tag(channel, labels, selected, parents)
            all_resolved = keep.all(axis=1)
            metrics[ci, ri, :3] = weights.sum(), weights[all_resolved].sum(), weights[correct].sum()
            # Attribute the strict all-object loss after scoring. This
            # bookkeeping never affects which visible objects are retained.
            close = all_pass_distances < radius
            within = np.any(close[:, within_parent], axis=1)
            between = np.any(close[:, ~within_parent], axis=1)
            metrics[ci, ri, 3:] = (passing_weights[within & ~between].sum(),
                                    passing_weights[between & ~within].sum(),
                                    passing_weights[within & between].sum())
            np.testing.assert_allclose(metrics[ci, ri, 3:].sum(),
                                       weights[all_pass & ~all_resolved].sum(), rtol=1e-12)
    return migration / len(weights), metrics / len(weights)


def production_point(args):
    coords, quadrature, power, seeds = args
    migration = np.zeros((len(seeds), len(THRESHOLDS), len(RESOLUTIONS), len(CHANNELS), len(LABELS)))
    metrics = np.zeros((*migration.shape[:-1], len(METRICS)))
    uncut = np.zeros(len(CHANNELS))
    photon = BASIS[PHOTON]
    for channel, (a, b) in enumerate(ENDS):
        recoils = ((-1, -1),) if channel == 0 else ((1, -1), (-1, 1))
        for charges in recoils:
            external = np.array([a, photon, photon, PLUS if charges[0] == 1 else MINUS,
                                 PLUS if charges[1] == 1 else MINUS, b])
            p, basis, beam, masses, amplitudes = production(external, coords)
            uncut[channel] += np.vdot(amplitudes, amplitudes).real
            selected_charge = 1 if channel == 0 else None
            all_charges = (selected_charge, *charges, selected_charge)
            for si, seed in enumerate(seeds):
                event = decay_event(p, basis, masses, amplitudes, all_charges, sample(power, seed))
                rows, controls = score(channel, *event, beam)
                migration[si, :, :, channel] += rows
                metrics[si, :, :, channel] += controls
    return quadrature*migration, quadrature*metrics, quadrature*uncut


def summarize(migration, metrics, uncut):
    np.testing.assert_allclose(migration.sum(axis=-1), metrics[..., 0], rtol=1e-12)
    results = []
    for ci, pt in enumerate(THRESHOLDS):
        for ri, radius in enumerate(RESOLUTIONS):
            rows = migration[:, ci, ri]
            control = metrics[:, ci, ri]
            columns = rows.sum(axis=1)
            reco = columns[:, :-1]
            ratios = [fraction(w) for w in reco]
            strict = [fraction(w) for w in control[..., 1]]
            mean = rows.mean(axis=0)
            label_efficiency = mean[np.arange(len(CHANNELS)), TRUTH_TO_LABEL] / uncut
            ww_purity = mean[0, 0]/mean[:, 0].sum()
            ww_pair_purity = control[:, 0, 2].mean()/mean[0, 0]
            results.append(dict(pt_over_mw=pt, min_delta_r=radius,
                                reconstructed_fraction=np.mean(ratios),
                                reconstructed_replicates=ratios,
                                all_objects_fraction=np.mean(strict),
                                all_objects_replicates=strict,
                                label_efficiency=label_efficiency.tolist(),
                                ww_purity=ww_purity, ww_pair_purity=ww_pair_purity,
                                migration_weights=mean.tolist(),
                                metrics=control.mean(axis=0).tolist()))
    return results


def validate():
    # A small resolved sample checks on-shell daughter momenta and inclusive
    # decay normalization independently of the production amplitudes.
    u = sample(15, 91)
    p = np.array([1.5, np.sqrt(1.5**2-MASS**2), 0., 0.])
    pols = np.array([[0, 0, 1, -1j], [0, 0, 0, 0], [0, 0, 1, 1j]])/np.sqrt(2)
    a, b, c, phi = daughters(p, pols, MASS, u[:, 0])
    np.testing.assert_allclose(a+b, np.broadcast_to(p, a.shape), atol=1e-12)
    np.testing.assert_allclose(dot(a, a), 0, atol=2e-15)
    np.testing.assert_allclose(dot(b, b), 0, atol=2e-15)
    phase = np.exp(1j*phi)
    vectors = np.sqrt(3)*np.column_stack(((1+c)*phase/2, -np.sqrt((1-c*c)/2),
                                          (c-1)*phase.conj()/2))
    np.testing.assert_allclose(vectors.conj().T @ vectors / len(u), np.eye(3), atol=2e-5)
    distance = np.array([[[0., .1, .2], [.1, 0., .1], [.2, .1, 0.]]])
    survivors = resolve(np.ones((1, 3), bool), np.array([[0, 1, 2]]), distance, .15)
    np.testing.assert_array_equal(survivors, [[True, False, True]])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("orders", type=int, nargs="+")
    parser.add_argument("--power", type=int, default=12)
    parser.add_argument("--replicates", type=int, default=4)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    validate()
    seeds = [1471 + 113*i for i in range(args.replicates)]
    output = dict(pair_mass=PAIR, w_mass=MASS, sin2_theta_w=MIXING, bounds=BOUNDS, max_eta=MAX_ETA,
                  fractional_z_window=Z_WINDOW, truth_channels=CHANNELS, reconstructed_channels=LABELS,
                  metrics=METRICS, sobol_points_per_replicate=2**args.power, seeds=seeds, grids={})
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        for order in args.orders:
            arguments = ((c, w, args.power, seeds) for c, w in nodes(order))
            values = list(executor.map(production_point, arguments))
            migration, metrics, uncut = (np.sum(x, axis=0) for x in zip(*values))
            output["grids"][order] = dict(nodes=order**4, production_weights=uncut.tolist(),
                                          results=summarize(migration, metrics, uncut))
            print(f"Completed production order {order} ({order**4} nodes)", file=sys.stderr, flush=True)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
