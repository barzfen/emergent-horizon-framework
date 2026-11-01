"""Event-written Hamiltonian-triad structure and symmetric move noise.

Copyright (c) 2026 Barry Fensom. SPDX-License-Identifier: MIT
AI-assisted. NumPy/SciPy for finite continuous-time transition probabilities.
Cycle conventions and LR2 moves follow EHF-RW-001, implemented standalone.
"""
from collections import deque
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import platform

import numpy as np
import scipy
from scipy.linalg import eigh, expm

HERE = Path(__file__).resolve().parent
A = ((0, 1, 2, 3, 4), (0, 1, 2, 3, 4), (0, 2, 4, 1, 3))
B = ((0, 1, 3, 2, 4), A[1], A[2])


def canonical(cycle):
    c = tuple(cycle)
    i = c.index(0)
    c = c[i:]+c[:i]
    return min(c, c[:1]+c[:0:-1])


def edges(cycle):
    return frozenset(tuple(sorted((cycle[i], cycle[(i+1) % 5]))) for i in range(5))


def neighbors(cycle):
    out = set()
    for i in range(5):
        c = list(cycle)
        j = (i+1) % 5
        c[i], c[j] = c[j], c[i]
        out.add(canonical(c))
    return out-{cycle}


def projection_tv(a, b, categories):
    return float(sum(abs(sum(a[i]-b[i] for i, value in enumerate(categories)
                             if value == category)) for category in set(categories))/2)


def run():
    tours = sorted({canonical((0,)+p) for p in permutations(range(1, 5))})
    assert len(tours) == 12
    ti = {t: i for i, t in enumerate(tours)}
    es = [edges(t) for t in tours]
    states = [s for s in product(range(12), repeat=3)
              if not (es[s[0]] & es[s[1]] & es[s[2]])]
    si = {s: i for i, s in enumerate(states)}
    single = [{ti[c] for c in neighbors(t)} for t in tours]
    adj = []
    for s in states:
        adj.append({si[t] for k in range(3) for j in single[s[k]]
                    if (t := s[:k]+(j,)+s[k+1:]) in si})
    for i, ns in enumerate(adj):
        assert all(i in adj[j] for j in ns)
    unseen = set(range(len(states)))
    component_sizes = []
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        queue = deque([seed])
        count = 0
        while queue:
            i = queue.popleft()
            count += 1
            for j in adj[i] & unseen:
                unseen.remove(j)
                queue.append(j)
        component_sizes.append(count)
    assert component_sizes == [516]
    ai = si[tuple(ti[canonical(c)] for c in A)]
    bi = si[tuple(ti[canonical(c)] for c in B)]
    assert bi in adj[ai] and ai in adj[bi]

    def writer(i):
        s = states[i]
        # Selected event is unique to cycle 2; cycle 0 must not acquire it.
        if [k for k in range(3) if (0, 2) in es[s[k]]] != [2]:
            return i
        c = tours[s[0]]
        swapped = canonical(tuple(3 if v == 2 else 2 if v == 3 else v for v in c))
        j = ti[swapped]
        target = (j, s[1], s[2])
        if j not in single[s[0]] or target not in si or (0, 2) in es[j]:
            return i
        return si[target]

    write = [writer(i) for i in range(len(states))]
    assert write[ai] == bi and write[bi] == ai
    for i, j in enumerate(write):
        assert write[j] == i
        assert j == i or j in adj[i]
    writable_states = sum(i != j for i, j in enumerate(write))
    # The structural writer can be coupled to the inherited spatial walk
    # without adding a bit. Verify every coupled spatial transition in the
    # 516*15-state joint model, not just the selected A -> B witness.
    coupled_hops = changed_hops = 0
    for i, s in enumerate(states):
        for k in range(3):
            c = tours[s[k]]
            for position, v in enumerate(c):
                for w in (c[(position-1) % 5], c[(position+1) % 5]):
                    j = write[i] if (v, w) == (2, 0) else i
                    assert tuple(sorted((v, w))) in es[states[j][k]]
                    coupled_hops += 1
                    changed_hops += int(j != i)
    assert changed_hops == writable_states
    # Row generator: each permitted distinct reconfiguration has rate 1/10.
    max_degree = max(map(len, adj))
    q = np.zeros((len(states), len(states)))
    for i, ns in enumerate(adj):
        q[i, list(ns)] = 1/max_degree
        q[i, i] = -len(ns)/max_degree
    assert np.max(np.abs(q-q.T)) == 0
    assert np.max(np.abs(q.sum(axis=1))) < 2e-15
    eigenvalues, u = eigh(q)
    assert abs(eigenvalues[-1]) < 2e-14
    gap = -float(eigenvalues[-2])
    assert gap > 0
    counts = [sum((1, 2) in es[t] for t in s) for s in states]
    boundary = [tuple(sum(edge in es[t] for t in s) for edge in ((0, 1), (0, 2), (1, 2)))
                for s in states]
    assert counts[ai] == 2 and counts[bi] == 1
    assert [k for k, c in enumerate(A) if (0, 2) in edges(c)] == [2]
    assert [k for k, c in enumerate(B) if (0, 2) in edges(c)] == [2]

    rows = []
    for t in (0, .1, 1, 3, 10, 30, 100):
        if t == 0:
            a, b = np.eye(len(states))[ai], np.eye(len(states))[bi]
        else:
            decay = np.exp(t*eigenvalues)
            a = (u[ai]*decay) @ u.T
            b = (u[bi]*decay) @ u.T
        assert min(a.min(), b.min()) > -2e-13
        assert abs(a.sum()-1)+abs(b.sum()-1) < 5e-12
        full = float(np.abs(a-b).sum()/2)
        link = projection_tv(a, b, counts)
        visible = projection_tv(a, b, boundary)
        # Specified one-hop experiment: choose a cycle uniformly at vertex 1,
        # take one of its two spatial neighbors uniformly, and ask if it is 2.
        # Freeze the network during this readout; no cycle label read required.
        click_a = float(a @ np.array(counts)/6)
        click_b = float(b @ np.array(counts)/6)
        one_hop = abs(click_a-click_b)
        assert one_hop <= link+5e-12 <= visible+1e-11 <= full+2e-11
        rows.append({'scaled_noise_time': t, 'full_tv': full,
                     'single_link_multiplicity_tv': link,
                     'all_boundary_multiplicities_tv': visible,
                     'one_hop_click_probability_blank': click_a,
                     'one_hop_click_probability_written': click_b,
                     'one_hop_tv': one_hop,
                     'one_hop_balanced_success': (1+one_hop)/2,
                     'ideal_link_balanced_success': (1+link)/2})
        if t in (1, 10):
            independent = expm(t*q)
            assert np.max(np.abs(a-independent[ai])) < 3e-13
            assert np.max(np.abs(b-independent[bi])) < 3e-13
    assert all(rows[i+1]['full_tv'] <= rows[i]['full_tv']+2e-12 for i in range(len(rows)-1))
    # Linear-algebra form of the component invariant: only constants lie in
    # this connected move generator's nullspace.
    assert np.count_nonzero(np.abs(eigenvalues) < 1e-12) == 1
    output = {'audit': 'EHF assumption audit 04', 'date': '2026-11-01',
              'python': platform.python_version(), 'numpy': np.__version__,
              'scipy': scipy.__version__,
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'blank_triad_A': A, 'written_triad_B': B,
              'states': len(states), 'undirected_move_edges': sum(map(len, adj))//2,
              'component_sizes': component_sizes,
              'degree_min': min(map(len, adj)), 'degree_max': max_degree,
              'writer_nontrivial_states': writable_states,
              'writer_nontrivial_pairs': writable_states//2,
              'coupled_probe_network_states': len(states)*15,
              'coupled_spatial_transitions_checked': coupled_hops,
              'event_transitions_that_reconfigure': changed_hops,
              'writer_involution_checked_on_all_states': True,
              'noise_each_move_rate_at_eta_1': 1/max_degree,
              'noise_spectral_gap_at_eta_1': gap,
              'same_move_class_sector_write_impossible': True,
              'retention_protocol': 'one event write, writer disabled during storage, symmetric LR2 perturbations, frozen network during one-hop readout',
              'rows': rows, 'all_assertions_passed': True}
    (HERE/'results.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    run()
