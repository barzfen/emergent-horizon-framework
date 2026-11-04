"""Independent edge-rewiring/DFS verifier. Standard library only; no probe import."""
from itertools import permutations, combinations, product
from pathlib import Path
from collections import Counter
import hashlib
import json


def walk(edges, n):
    neighbours = {v: [] for v in range(n)}
    for a, b in edges:
        neighbours[a].append(b)
        neighbours[b].append(a)
    assert all(len(ns) == 2 for ns in neighbours.values())
    out = [0, min(neighbours[0])]
    while len(out) < n:
        a, b = out[-2:]
        out.append(next(v for v in neighbours[b] if v != a))
    assert len(set(out)) == n and 0 in neighbours[out[-1]]
    return tuple(out)


def edge(a, b):
    return tuple(sorted((a, b)))


def edges_of(c):
    return frozenset(edge(a, b) for a, b in zip(c, c[1:] + c[:1]))


def valid(es, n, ones):
    return all(any((v in ones) == (b in ones) for a, b in es if a == v) or
               any((v in ones) == (a in ones) for a, b in es if b == v)
               for v in range(n))


def wall_count(es, ones):
    return sum((a in ones) != (b in ones) for a, b in es)


def pi(c):
    return frozenset(c[::2])


def verify_case(n, row):
    ones = set(row['ones'])
    # Generate undirected cycles as edge sets, then reconstruct orientation by traversal.
    all_es = {edges_of((0,) + p) for p in permutations(range(1, n))}
    states = {walk(es, n): es for es in all_es if valid(es, n, ones)}
    assert len(states) == row['states']
    graphs = {name: {c: set() for c in states} for name in row['models']}
    length_edges = {length: set() for length in range(2, n - 1)}
    length_pi = {length: set() for length in range(2, n - 1)}
    for c, es in states.items():
        for i, j in combinations(range(n), 2):
            if j - i in (1, n - 1):
                continue
            # Remove two nonadjacent edges and reconnect into the other single cycle.
            a, b, d, e = c[i], c[(i + 1) % n], c[j], c[(j + 1) % n]
            target_edges = (es - {edge(a, b), edge(d, e)}) | {edge(a, d), edge(b, e)}
            if not valid(target_edges, n, ones):
                continue
            target = walk(target_edges, n)
            assert target in states and target != c
            pair = tuple(sorted((c, target)))
            lengths = {j - i, n - (j - i)}
            same_pi = pi(c) == pi(target)
            for length in lengths:
                length_edges[length].add(pair)
                if same_pi:
                    length_pi[length].add(pair)
            graphs['all_MICRO'][c].add(target)
            if same_pi:
                graphs['all_Pi'][c].add(target)
                if 3 in lengths:
                    graphs['OPW3'][c].add(target)
                if lengths & {2, 3}:
                    graphs['OPW23'][c].add(target)
    for length, pairs in length_edges.items():
        assert row['lengths'][str(length)] == {'MICRO_edges': len(pairs), 'MICRO_Pi_edges': len(length_pi[length])}
    for c in states:
        w = wall_count(states[c], ones)
        if w > 2:
            assert any(wall_count(states[d], ones) == w - 2 for d in graphs['all_MICRO'][c])
    for name, graph in graphs.items():
        seen = set()
        sizes = []
        for start in graph:
            if start in seen:
                continue
            stack = [start]
            seen.add(start)
            size = 0
            while stack:
                c = stack.pop()
                size += 1
                for d in graph[c]:
                    assert c in graph[d]
                    if d not in seen:
                        seen.add(d)
                        stack.append(d)
            sizes.append(size)
        pairs = [(c, d) for c in graph for d in graph[c] if c < d]
        stats = {'edges': len(pairs), 'components': len(sizes), 'largest': max(sizes, default=0),
                 'isolated': sum(not ds for ds in graph.values()),
                 'component_sizes': {str(k): v for k, v in sorted(Counter(sizes).items())},
                 'Pi_changing_edges': sum(pi(c) != pi(d) for c, d in pairs),
                 'wall_changing_edges': sum(wall_count(states[c], ones) != wall_count(states[d], ones) for c, d in pairs)}
        assert stats == row['models'][name], (n, row['mask'], name, stats, row['models'][name])
    return {'n': n, 'mask': row['mask'], 'states': len(states), 'models': list(graphs)}


def check_boundary_rule():
    checks = 0
    for n in range(4, 11):
        for bits in product((0, 1), repeat=n):
            ok = lambda w: all(w[i] in (w[(i-1) % n], w[(i+1) % n]) for i in range(n))
            if not ok(bits):
                continue
            for s in range(n):
                for length in range(2, n-1):
                    p, a, b, c, d, e, f, q = [bits[j % n] for j in
                        (s-2, s-1, s, s+1, s+length-2, s+length-1, s+length, s+length+1)]
                    predicted = ((a == p or a == e) and (e == d or e == a) and
                                 (b == c or b == f) and (f == q or f == b))
                    word = list(bits)
                    slots = [(s+j) % n for j in range(length)]
                    for slot, value in zip(slots, reversed([bits[j] for j in slots])):
                        word[slot] = value
                    assert predicted == ok(word)
                    if length == 2 and predicted:
                        assert b == e
                    checks += 1
    return checks


if __name__ == '__main__':
    here = Path(__file__).parent
    result = json.loads((here / 'results.json').read_text())
    assert result['probe_sha256'] == hashlib.sha256((here / 'probe.py').read_bytes()).hexdigest()
    checks = []
    for run in result['runs']:
        n = run['n']
        selected = run['colourings'] if n <= 7 else [r for r in run['colourings'] if r['mask'] in (6, 14, 30)]
        for row in selected:
            checks.append(verify_case(n, row))
        print('Verified', n, len(selected), 'colourings', flush=True)
    boundary_checks = check_boundary_rule()
    out = {'boundary_rule_checks': boundary_checks, 'status': 'PASS', 'method': 'undirected edge rewiring; neighbour-based admissibility; cycle traversal; DFS',
           'scope': 'all 80 complement representatives at n=5,7 including empty and constant cases; three n=9 representatives, ones={1,2}, {1,2,3}, {1,2,3,4}',
           'cases': checks, 'probe_sha256': result['probe_sha256'],
           'verify_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (here / 'independent-checks.json').write_text(json.dumps(out, indent=2) + '\n')
    print('INDEPENDENT CHECKS PASSED')
