"""Exhaustive labelled-graph audit; Python standard library only.

Copyright (c) 2026 Barry Fensom. SPDX-License-Identifier: MIT
AI-assisted implementation. Elementary graph facts; no novelty claim.
"""
import itertools
import json
from pathlib import Path


def adjacency(n, edges):
    rows = [0] * n
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return rows


def connected(rows):
    seen, frontier = 1, 1
    while frontier:
        following = 0
        for u in range(len(rows)):
            if frontier & (1 << u):
                following |= rows[u]
        frontier = following & ~seen
        seen |= frontier
    return seen == (1 << len(rows)) - 1


def vertex_transitive(rows):
    """Direct automorphism check, not a degree-only approximation."""
    n = len(rows)
    degrees = [row.bit_count() for row in rows]
    if len(set(degrees)) > 1:
        return False  # Unequal degrees cannot lie in one automorphism orbit.
    reached = {0}
    for permutation in itertools.permutations(range(n)):
        if permutation[0] in reached:
            continue
        if all(((rows[u] >> v) & 1) ==
               ((rows[permutation[u]] >> permutation[v]) & 1)
               for u in range(n) for v in range(u + 1, n)):
            reached.add(permutation[0])
            if len(reached) == n:
                return True
    return False


def circulant(n, d):
    edges = set()
    for u in range(n):
        for k in range(1, d // 2 + 1):
            edges.add(tuple(sorted((u, (u + k) % n))))
        if d % 2:
            assert n % 2 == 0
            edges.add(tuple(sorted((u, (u + n // 2) % n))))
    return adjacency(n, edges)


def run():
    results = []
    all_buckets = []
    for n in range(3, 7):
        pairs = list(itertools.combinations(range(n), 2))
        buckets = {}
        connected_count = transitive_count = 0
        for mask in range(1 << len(pairs)):
            edges = [edge for i, edge in enumerate(pairs) if mask & (1 << i)]
            rows = adjacency(n, edges)
            if not connected(rows):
                continue
            m = len(edges)
            is_transitive = vertex_transitive(rows)
            if (2 * m) % n:
                assert not is_transitive
            bucket = buckets.setdefault(m, {"connected": 0, "vertex_transitive": 0})
            bucket["connected"] += 1
            bucket["vertex_transitive"] += int(is_transitive)
            connected_count += 1
            transitive_count += int(is_transitive)
        for m, bucket in sorted(buckets.items()):
            forced = (2 * m) % n != 0
            assert (bucket["vertex_transitive"] == 0) == forced
            all_buckets.append({"n": n, "m": m, **bucket,
                                "all_have_multiple_roles": forced})
        results.append({"n": n, "all_labelled_graphs": 1 << len(pairs),
                        "connected_graphs": connected_count,
                        "vertex_transitive_connected_graphs": transitive_count})

    construction_checks = 0
    for n in range(3, 41):
        for d in range(2, n):
            if n * d % 2:
                continue
            rows = circulant(n, d)
            assert connected(rows)
            assert all(row.bit_count() == d for row in rows)
            # Verify that cyclic rotation is an automorphism: it is transitive.
            assert all(((rows[u] >> v) & 1) ==
                       ((rows[(u + 1) % n] >> ((v + 1) % n)) & 1)
                       for u in range(n) for v in range(n))
            construction_checks += 1

    witnesses = {}
    for name, n, edges in [
        ("P3", 3, [(0, 1), (1, 2)]),
        ("C4", 4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
        ("two_disjoint_edges", 4, [(0, 1), (2, 3)]),
        ("K2", 2, [(0, 1)]),
        ("triangle_with_leaf", 4, [(0, 1), (1, 2), (2, 0), (0, 3)]),
    ]:
        rows = adjacency(n, edges)
        witnesses[name] = {"n": n, "edges": edges, "connected": connected(rows),
                           "degrees": [r.bit_count() for r in rows],
                           "vertex_transitive": vertex_transitive(rows)}
    assert not witnesses["P3"]["vertex_transitive"]
    assert witnesses["C4"]["vertex_transitive"]
    assert witnesses["two_disjoint_edges"]["vertex_transitive"]
    assert witnesses["K2"]["vertex_transitive"]
    assert not witnesses["triangle_with_leaf"]["vertex_transitive"]
    output = {"scope": "finite simple undirected graphs; structural roles only",
              "summary": results, "buckets": all_buckets,
              "circulant_checks_n_3_to_40": construction_checks,
              "witnesses": witnesses, "assertions_passed": True}
    Path(__file__).with_name("results.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"summary": results, "construction_checks": construction_checks,
                      "assertions_passed": True}, indent=2))


if __name__ == "__main__":
    run()
