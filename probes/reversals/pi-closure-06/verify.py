"""Check the rare-event outcomes by summing exact path probabilities."""
from fractions import Fraction
import json

from probe import HERE, rev04, rev05

data = json.loads(rev05.PARENT.read_text())
result = json.loads((HERE / "results.json").read_text())
carrier = data["carrier"]
tours = carrier["states"]
seed = tours.index(data["seed"])
source = rev04.cycle_edges(tours[seed])
n = len(tours[seed])
ones = set(data["ones"])
parity = [v in data["Pi"] for v in range(n)]
group = {v: i for i, part in enumerate(carrier["fast_groups"]) for v in part}
targets = {rev04.cycle_edges(tours[j if i == seed else i])
           for i, j in carrier["slow_edges"] if seed in (i, j) and group[i] != group[j]}
backward = {}
for target in targets:
    for graph, suffix in rev04.slide_ball(target, n, ones).items():
        backward[graph] = min(backward.get(graph, 7), len(suffix))


def completed(graph):
    return all(len(a) == 2 for a in rev04.adjacency(graph, n))


def good_cycle(graph):
    adj = rev04.adjacency(graph, n)
    order = [0, min(adj[0])]
    while len(order) < n:
        order.append(next(v for v in adj[order[-1]] if v != order[-2]))
    return all(parity[v] == (i % 2 == 0) for i, v in enumerate(order))


def histories(graph, steps):
    depth = len(steps)
    if depth and completed(graph):
        if graph in targets:
            yield steps
        return
    if depth == 6 or (depth >= 3 and backward.get(graph, 7) > 6 - depth):
        return
    choices = list(rev04.slides(graph, n, ones))
    for move in choices:
        yield from histories(move[0], steps + [(choices, move)])


def path_probability(path, policy):
    probability = Fraction(1)
    marked = previous = None
    for step, (choices, move) in enumerate(path):
        def rate(choice):
            dest, (added, removed) = choice
            a, b = added
            good_edge = parity[a] != parity[b] or (0 in added and parity[a] and parity[b])
            if policy.startswith("hard_endpoint") and not good_edge:
                return 0
            if policy.startswith("hard_endpoint_seam"):
                neighbours = sorted(rev04.adjacency(dest, n)[0])
                if len(neighbours) == 2:
                    first, last = [parity[v] for v in neighbours]
                    if first and not last or (policy == "hard_endpoint_seam" and first == last):
                        return 0
            if policy == "cycle_oracle" and completed(dest) and not good_cycle(dest):
                return 0
            advancing = removed == marked and pivot in added and added != previous
            return (4 if advancing else 1) * (4 if policy == "soft_endpoint" and good_edge else 1)

        weight = rate(move)
        if not weight:
            return Fraction(0)
        probability *= Fraction(weight, sum(map(rate, choices)))
        _, (added, removed) = move
        if step == 0:
            pivot = next(v for v in added if v in removed)
            marked, previous = added, removed
        elif removed == marked:
            marked, previous = (added, removed) if pivot in added else (None, None)
    return probability


paths = list(histories(source, []))
assert len(paths) == 12
checks = {}
for policy, rows in result["policies"].items():
    probabilities = [path_probability(path, policy) for path in paths]
    total = sum(probabilities)
    assert abs(float(total) - rows[-1].get("blocked_lr4", 0)) < 1e-15
    checks[policy] = {"surviving_paths": sum(p > 0 for p in probabilities),
                      "exact_blocked_lr4": str(total)}
(HERE / "independent-checks.json").write_text(json.dumps(checks, indent=2) + "\n")
print(json.dumps(checks, indent=2))
