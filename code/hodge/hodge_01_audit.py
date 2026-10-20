#!/usr/bin/env python3
"""HODGE-01: exact topology controls and independently enumerated RECUR transport.

Requires Python 3.10+ and NumPy. Run from repository root:
  python code/hodge/hodge_01_audit.py --output data/hodge/hodge-01-results.json
Finite numerical transport checks are not all-n proofs.
"""
import argparse
from fractions import Fraction
from itertools import combinations, permutations
import json
from math import acos, comb, factorial
from pathlib import Path
import numpy as np

TOL = 1e-9

def exact_rank(matrix):
    a = [[Fraction(int(x)) for x in row] for row in matrix]
    if not a:
        return 0
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        divisor = a[row][col]
        a[row] = [x / divisor for x in a[row]]
        for i in range(row + 1, len(a)):
            factor = a[i][col]
            if factor:
                a[i] = [x - factor*y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row

def incidence(n, edges, faces):
    lookup = {e: k for k, e in enumerate(edges)}
    d0 = np.zeros((len(edges), n), dtype=int)
    for k, (a, b) in enumerate(edges):
        d0[k, a], d0[k, b] = -1, 1
    d1 = np.zeros((len(faces), len(edges)), dtype=int)
    for k, (a, b, c) in enumerate(faces):
        for e, sign in [((a,b),1), ((b,c),1), ((a,c),-1)]:
            d1[k, lookup[e]] = sign
    assert not np.any(d1 @ d0)
    return d0, d1

def projection(a, f):
    if a.shape[1] == 0:
        return np.zeros_like(f, dtype=float)
    return a @ np.linalg.lstsq(a, f, rcond=None)[0]

def decompose(d0, d1, f):
    f = np.asarray(f, dtype=float)
    gradient = projection(d0, f)
    curl = projection(d1.T, f)
    harmonic = f - gradient - curl
    assert np.linalg.norm(d0.T @ harmonic) < TOL
    assert np.linalg.norm(d1 @ harmonic) < TOL
    assert abs(float(gradient @ curl)) < TOL
    return {name: float(x @ x) for name, x in
            [("gradient", gradient), ("curl", curl), ("harmonic", harmonic)]}

def topology_controls():
    results = []
    for n in range(4, 9):
        edges = list(combinations(range(n), 2))
        for fill in (False, True):
            faces = list(combinations(range(n), 3)) if fill else []
            d0, d1 = incidence(n, edges, faces)
            b1 = len(edges) - exact_rank(d0) - exact_rank(d1)
            assert b1 == (0 if fill else comb(n-1, 2))
            gradient = d0 @ np.arange(n)
            energies = decompose(d0, d1, gradient)
            assert energies["curl"] < TOL and energies["harmonic"] < TOL
            results.append({"n":n, "edges":len(edges), "faces":len(faces),
                            "rank_d0":exact_rank(d0), "rank_d1":exact_rank(d1),
                            "beta1":b1, "exact_gradient_energies":energies})
    # The same triangle circulation is harmonic without a face and curl with one.
    edges = [(0,1),(0,2),(1,2)]
    triangle = []
    for faces in ([], [(0,1,2)]):
        d0, d1 = incidence(3, edges, faces)
        energies = decompose(d0, d1, [1,-1,1])
        assert abs(energies["gradient"]) < TOL
        assert abs(energies["harmonic"] - (0 if faces else 3)) < TOL
        assert abs(energies["curl"] - (3 if faces else 0)) < TOL
        triangle.append({"faces":len(faces), "energies":energies})
    return results, triangle

def hamilton_observations(n):
    observations = []
    for tail in permutations(range(1,n)):
        # Fix root 0 and choose one of the two undirected orientations.
        if tail[0] > tail[-1]:
            continue
        cycle = (0,) + tail
        neighbours = {}
        for k, a in enumerate(cycle):
            neighbours[a] = tuple(sorted((cycle[k-1], cycle[(k+1)%n])))
        observations.append(neighbours)
    assert len(observations) == factorial(n-1)//2
    return observations

def polar_transport(n, observations, source, target):
    src = list(combinations([v for v in range(n) if v != source], 2))
    dst = list(combinations([v for v in range(n) if v != target], 2))
    si, ti = {v:i for i,v in enumerate(src)}, {v:i for i,v in enumerate(dst)}
    joint = np.zeros((len(dst), len(src)), dtype=int)
    for obs in observations:
        joint[ti[obs[target]], si[obs[source]]] += 1
    counts = joint.sum(axis=0)
    assert np.all(counts > 0) and len(set(counts)) == 1
    transport = joint / counts[None,:]
    assert np.max(np.abs(transport.sum(axis=0)-1)) < TOL
    u, s, vh = np.linalg.svd(transport)
    keep = s > TOL
    w = u[:,keep] @ vh[keep,:]
    return w, int(keep.sum())

def observer_checks():
    results = []
    for n in range(5, 9):
        obs = hamilton_observations(n)
        wab, r = polar_transport(n, obs, 0, 1)
        wbc, _ = polar_transport(n, obs, 1, 2)
        wca, _ = polar_transport(n, obs, 2, 0)
        loop = wca @ wbc @ wab
        eigenvalues = np.linalg.eigvals(loop)
        q = n-2
        cosine = Fraction(3*q*q-4, q**3)
        angle = acos(float(cosine))
        target = complex(float(cosine), np.sin(angle))
        residual = float(min(abs(eigenvalues-target)))
        assert residual < TOL
        assert r == 2*(n-2)
        reverse = wab.T @ wbc.T @ wca.T
        assert np.linalg.norm(reverse-loop.T) < TOL
        results.append({"n":n, "microstates":len(obs), "observer_dimension":comb(n-1,2),
                        "single_transport_rank":r,
                        "cosine_exact":str(cosine), "angle_radians":angle,
                        "rotation_eigenvalue_residual":residual,
                        "loop_minus_identity_frobenius":float(np.linalg.norm(loop-np.eye(loop.shape[0]))),
                        "unit_modulus_eigenvalues":[[float(z.real),float(z.imag)]
                            for z in sorted(eigenvalues, key=lambda z:(round(z.real,9),round(z.imag,9)))
                            if abs(abs(z)-1)<TOL]})
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    topology, triangles = topology_controls()
    result = {"probe":"EHF-HODGE-01", "status":"COMPUTATIONAL",
              "numpy_version":np.__version__, "tolerance":TOL,
              "topology_controls":topology, "triangle_face_controls":triangles,
              "recur_enumeration":observer_checks(),
              "conclusion":"Discrete Hodge fit supported; no bridge to Clay Hodge conjecture established."}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered)

if __name__ == "__main__":
    main()
