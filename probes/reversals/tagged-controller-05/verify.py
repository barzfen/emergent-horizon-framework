"""Enumerate successful histories and sum their probabilities exactly."""
from fractions import Fraction
import json

from probe import HERE, HORIZON, BOOST, PARENT, rev04

parent = json.loads(PARENT.read_text())
result = json.loads((HERE / "results.json").read_text())
carrier = parent["carrier"]
tours = carrier["states"]
seed = tours.index(parent["seed"])
start = rev04.cycle_edges(tours[seed])
n = len(tours[seed])
ones = set(parent["ones"])
component_of = {v: i for i, group in enumerate(carrier["fast_groups"]) for v in group}
targets = {
    rev04.cycle_edges(tours[j if i == seed else i]) for i, j in carrier["slow_edges"]
    if seed in (i, j) and component_of[i] != component_of[j]
}
witness = rev04.cycle_edges([0, 1, 2, 7, 6, 5, 4, 3, 8])
backward = {}
for target in targets:
    for graph, suffix in rev04.slide_ball(target, n, ones).items():
        backward[graph] = min(backward.get(graph, HORIZON), len(suffix))


def moves(graph):
    return list(rev04.slides(graph, n, ones))


def successful_histories(graph, history):
    depth = len(history)
    if depth and all(len(a) == 2 for a in rev04.adjacency(graph, n)):
        if graph in targets:
            yield graph, history
        return
    if depth == HORIZON or (depth >= 3 and backward.get(graph, 7) > HORIZON - depth):
        return
    options = moves(graph)
    for choice in options:
        yield from successful_histories(choice[0], history + [(graph, options, choice)])


def weighted_probability(history, policy):
    probability = Fraction(1)
    marker = None
    previous = None
    for step, (graph, options, choice) in enumerate(history):
        degree = list(map(len, rev04.adjacency(graph, n)))

        def rate(option):
            _, (added, removed) = option
            if policy == "branch_repair":
                left = next(v for v in removed if v not in added)
                right = next(v for v in added if v not in removed)
                return BOOST if degree[left] == 3 and degree[right] == 1 else 1
            if policy == "tagged_connection" and marker is not None:
                return BOOST if removed == marker and anchor in added and added != previous else 1
            return 1

        probability *= Fraction(rate(choice), sum(map(rate, options)))
        _, (added, removed) = choice
        if step == 0:
            anchor = next(v for v in added if v in removed)
            marker, previous = added, removed
        elif removed == marker:
            marker, previous = (added, removed) if anchor in added else (None, None)
    return probability


histories = list(successful_histories(start, []))
assert histories
checks = {}
for policy, rows in result["policies"].items():
    contributions = [(g, weighted_probability(h, policy)) for g, h in histories]
    total = sum(p for _, p in contributions)
    particular = sum(p for g, p in contributions if g == witness)
    assert abs(float(total) - rows[-1]["blocked_lr4"]) < 1e-15
    assert abs(float(particular) - rows[-1]["particular_witness"]) < 1e-15
    checks[policy] = {"blocked_lr4": str(total), "particular_witness": str(particular)}

report = {"successful_first_return_histories": len(histories),
          "histories_to_particular_witness": sum(g == witness for g, _ in histories),
          "exact_probabilities": checks}
(HERE / "independent-checks.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
