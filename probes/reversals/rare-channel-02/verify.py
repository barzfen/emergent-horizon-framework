"""Independent carrier reconstruction, matrix-exponential and exact hitting-time checks."""
from pathlib import Path
from itertools import permutations, combinations
from collections import defaultdict, Counter
from fractions import Fraction
import hashlib
import json
import numpy as np
from scipy.linalg import expm


def edge(a, b):
    return tuple(sorted((a, b)))


def edge_set(c):
    return frozenset(edge(a, b) for a, b in zip(c, c[1:] + c[:1]))


def traverse(es):
    adj = defaultdict(list)
    for a, b in es:
        adj[a].append(b)
        adj[b].append(a)
    c = [0, min(adj[0])]
    while len(c) < len(adj):
        c.append(next(v for v in adj[c[-1]] if v != c[-2]))
    assert len(set(c)) == len(adj) and 0 in adj[c[-1]]
    return tuple(c)


def valid(es, ones):
    same = {v: 0 for e in es for v in e}
    for a, b in es:
        if (a in ones) == (b in ones):
            same[a] += 1
            same[b] += 1
    return all(same.values())


def connected(start, adj):
    seen, stack = {start}, [start]
    while stack:
        c = stack.pop()
        for d in adj[c]:
            if d not in seen:
                seen.add(d)
                stack.append(d)
    return seen


def exact_solve(matrix, rhs):
    a = [[Fraction(v) for v in row] + [Fraction(b)] for row,b in zip(matrix,rhs)]
    n = len(a)
    for k in range(n):
        pivot = next(j for j in range(k,n) if a[j][k])
        a[k],a[pivot] = a[pivot],a[k]
        for i in range(k+1,n):
            if not a[i][k]:
                continue
            ratio = a[i][k]/a[k][k]
            for j in range(k,n+1):
                a[i][j] -= ratio*a[k][j]
    out = [Fraction(0)]*n
    for i in range(n-1,-1,-1):
        out[i] = (a[i][-1]-sum(a[i][j]*out[j] for j in range(i+1,n)))/a[i][i]
    assert all(sum(Fraction(v)*x for v,x in zip(row,out)) == b for row,b in zip(matrix,rhs))
    return out


if __name__ == '__main__':
    here = Path(__file__).parent
    r = json.loads((here/'results.json').read_text())
    assert hashlib.sha256((here/'probe.py').read_bytes()).hexdigest() == r['probe_sha256']
    n, ones = r['n'], set(r['ones'])
    target_pi = set(r['Pi'])
    cycles = {edge_set((0,) + p) for p in permutations(range(1, n))}
    states = {traverse(es): es for es in cycles if valid(es, ones)}
    states = {c: es for c, es in states.items() if set(c[::2]) == target_pi}
    adj = {c: set() for c in states}
    support = {}
    for c, es in states.items():
        for i, j in combinations(range(n), 2):
            if j-i in (1, n-1):
                continue
            a,b,d,e = c[i],c[(i+1)%n],c[j],c[(j+1)%n]
            changed = (es - {edge(a,b),edge(d,e)}) | {edge(a,d),edge(b,e)}
            if not valid(changed, ones):
                continue
            z = traverse(changed)
            if z not in states:
                continue
            adj[c].add(z)
            support[tuple(sorted((c,z)))] = min(j-i,n-j+i)
    selected = sorted(connected(tuple(r['seed']), adj))
    assert selected == [tuple(c) for c in r['carrier']['states']]
    index = {c:i for i,c in enumerate(selected)}
    fast,slow = set(),set()
    for c in selected:
        for z in adj[c]:
            pair = tuple(sorted((index[c],index[z])))
            (fast if support[tuple(sorted((c,z)))] <= 3 else slow).add(pair)
    assert sorted(fast) == [tuple(e) for e in r['carrier']['fast_edges']]
    assert sorted(slow) == [tuple(e) for e in r['carrier']['slow_edges']]
    size = len(selected)
    wall = np.array([sum((a in ones)!=(b in ones) for a,b in states[c]) for c in selected])
    A = np.flatnonzero(wall == 2)
    f = (wall == 2).astype(float)-len(A)/size
    initial = (wall == 2).astype(float)/len(A)
    escape = Counter()
    for i,j in slow:
        if wall[i] != wall[j]:
            escape[i] += 1
            escape[j] += 1
    escape_histogram = {str(w): dict(sorted(Counter(escape[i] for i in range(size) if wall[i] == w).items())) for w in (2,4)}
    assert escape_histogram == {'2': {0:24,1:28}, '4': {0:28,1:4,2:12}}
    checks = []
    exact_checks = []
    for row in r['rows']:
        epsilon = row['epsilon']
        L = np.zeros((size,size))
        for pairs, rate in ((fast,1.),(slow,epsilon)):
            for i,j in pairs:
                L[i,i] += rate
                L[j,j] += rate
                L[i,j] -= rate
                L[j,i] -= rate
        # Verify evolution without spectral propagation.
        for t in (1.,1/epsilon):
            transition = expm(-t*L)
            assert np.min(transition) > -1e-10
            assert np.max(np.abs(transition.sum(axis=1)-1)) < 1e-8
            probability = float((initial @ transition)[A].sum())
            C = (probability-len(A)/size)/(1-len(A)/size)
            expected = row['correlation_at_times']['1'] if t == 1 else row['correlation_at_slow_times']['1']
            assert abs(C-expected) < 1e-8
        # Poisson equation independently gives the integrated normalized correlation.
        u = np.linalg.solve(L+np.ones((size,size))/size,f)
        time = float(f@u/(f@f))
        assert abs(time-row['integrated_wall_correlation_time']) < 1e-6
        assert abs(float(((wall==2).astype(float) @ L @ (wall==2).astype(float)))) > 0
        if epsilon in (1., .001):
            denominator = 1 if epsilon == 1 else 1000
            K = [[0]*len(A) for _ in A]
            position = {int(v): k for k,v in enumerate(A)}
            for pairs, numerator in ((fast,denominator),(slow,1)):
                for i,j in pairs:
                    if i in position:
                        K[position[i]][position[i]] += numerator
                    if j in position:
                        K[position[j]][position[j]] += numerator
                    if i in position and j in position:
                        K[position[i]][position[j]] -= numerator
                        K[position[j]][position[i]] -= numerator
            # Integer killed Laplacian solves exact rational first-exit times.
            h = exact_solve(K,[denominator]*len(A))
            mean = sum(h)/len(A)
            assert abs(float(mean)-row['mean_first_exit_from_two_wall_set']) < 1e-7
            exact_checks.append({'epsilon': str(Fraction(1,denominator)), 'exact_mean_first_exit': str(mean)})
        checks.append({'epsilon':epsilon,'matrix_exponential_checks':2,'poisson_check':True})
    out = {'status':'PASS','carrier_method':'two-edge reconnection, adjacency traversal and DFS; no probe import',
           'states':size,'fast_edges':len(fast),'slow_edges':len(slow),
           'numeric_tolerances':{'evolution':1e-8,'integrated_time':1e-6,'mean_exit':1e-7},
           'wall_escape_degree_histograms':escape_histogram,'dynamic_checks':checks,'exact_rational_first_exit_checks':exact_checks,
           'probe_sha256':r['probe_sha256'],
           'verify_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (here/'independent-checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
