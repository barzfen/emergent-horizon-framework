"""Exact first-return audit for the REV-06 seam-order controller."""
from collections import Counter
from fractions import Fraction
from functools import cache
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / "pi-closure-06" / "probe.py"
spec = importlib.util.spec_from_file_location("rev06", PREVIOUS)
rev06 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rev06)
rev04, rev05 = rev06.rev04, rev06.rev05


def run():
    parent = json.loads(rev05.PARENT.read_text())
    carrier = parent["carrier"]
    tours = carrier["states"]
    n = len(tours[0])
    ones = set(parent["ones"])
    even = set(parent["Pi"])
    graphs = [rev04.cycle_edges(tour) for tour in tours]
    index = {graph: i for i, graph in enumerate(graphs)}
    assert len(index) == 96
    assert all(set(tour[::2]) == even for tour in tours)
    group = {v: i for i, part in enumerate(carrier["fast_groups"]) for v in part}
    blocked = [(i, j) for i, j in carrier["slow_edges"] if group[i] != group[j]]
    assert len(blocked) == 76

    @cache
    def completed(graph):
        return all(len(adj) == 2 for adj in rev04.adjacency(graph, n))

    @cache
    def raw_moves(graph):
        return tuple(rev04.slides(graph, n, ones))

    @cache
    def endpoint_moves(graph):
        return tuple((dest, edit) for dest, edit in raw_moves(graph)
                     if rev06.compatible(edit[0], even))

    @cache
    def legal_moves(graph):
        moves = []
        for dest, (add, cut) in endpoint_moves(graph):
            if 0 in add or 0 in cut:
                neighbours = sorted(b for a, b in dest if a == 0)
                if (len(neighbours) == 2 and neighbours[0] in even
                        and neighbours[1] not in even):
                    continue
            pivot, = set(add) & set(cut)
            old, = set(cut) - {pivot}
            new, = set(add) - {pivot}
            moves.append((dest, add, cut, pivot, old, new))
        return tuple(moves)

    def open_ball(source, move_function):
        seen = {source}
        frontier = {source}
        for _ in range(3):
            frontier = {dest for graph in frontier for dest, *_ in move_function(graph)
                        if dest not in seen and not completed(dest)}
            seen.update(frontier)
        return seen - {source}

    raw_balls = [open_ball(graph, raw_moves) for graph in graphs]
    endpoint_balls = [open_ball(graph, endpoint_moves) for graph in graphs]
    legal_balls = [open_ball(graph, legal_moves) for graph in graphs]

    def propagate(source):
        active = {(source, None): Fraction(1)}
        returns = Counter()
        stalled = Fraction(0)
        for step in range(1, 7):
            next_active = Counter()
            for (graph, marker), mass in active.items():
                moves = legal_moves(graph)
                if not moves:
                    stalled += mass
                    continue
                weights = [
                    rev05.BOOST if marker is not None and (pivot, old) == (marker[0], marker[2])
                    and new != marker[1] else 1
                    for _, _, _, pivot, old, new in moves
                ]
                total = sum(weights)
                for (dest, add, cut, pivot, old, new), weight in zip(moves, weights):
                    probability = mass * Fraction(weight, total)
                    if completed(dest):
                        assert rev06.certificate(dest, rev04.adjacency(dest, n), even)
                        returns[dest] += probability
                    else:
                        tag = rev05.marker_after(marker, add, cut, pivot, old, new, step,
                                                 "tagged_connection")
                        next_active[dest, tag] += probability
            active = next_active
        remaining = sum(active.values(), Fraction(0))
        assert sum(returns.values(), Fraction(0)) + remaining + stalled == 1
        return returns, remaining, stalled

    propagated = [propagate(graph) for graph in graphs]
    records = []
    by_seed = [Counter() for _ in graphs]
    for i, j in blocked:
        raw_reachable = bool(raw_balls[i] & raw_balls[j])
        endpoint_reachable = bool(endpoint_balls[i] & endpoint_balls[j])
        reachable = bool(legal_balls[i] & legal_balls[j])
        assert not reachable or endpoint_reachable
        assert not endpoint_reachable or raw_reachable
        for source, target in ((i, j), (j, i)):
            probability = propagated[source][0][graphs[target]]
            assert bool(probability) == reachable
            by_seed[source]["blocked"] += 1
            by_seed[source]["reachable"] += reachable
            by_seed[source]["mass"] += probability
            records.append({"source": source, "target": target,
                            "raw_first_return_within_six": raw_reachable,
                            "endpoint_first_return_within_six": endpoint_reachable,
                            "seam_first_return_within_six": reachable,
                            "probability": str(probability)})
    seeds = []
    for i, (returns, remaining, stalled) in enumerate(propagated):
        outside = sum(mass for graph, mass in returns.items() if graph not in index)
        seeds.append({"source": i, "blocked_targets": by_seed[i]["blocked"],
                      "reachable_targets": by_seed[i]["reachable"],
                      "blocked_probability": str(by_seed[i]["mass"]),
                      "original": str(returns[graphs[i]]), "still_open": str(remaining),
                      "outside_carrier": str(outside), "stalled": str(stalled)})
    witness_index = tours.index(parent["seed"])
    assert Fraction(seeds[witness_index]["blocked_probability"]) == Fraction(317, 677376)
    positives = [Fraction(row["probability"]) for row in records if row["probability"] != "0"]
    summary = {
        "seeds": len(seeds), "directed_blocked_targets": len(records),
        "raw_first_return_targets": sum(row["raw_first_return_within_six"] for row in records),
        "endpoint_first_return_targets": sum(row["endpoint_first_return_within_six"] for row in records),
        "seam_first_return_targets": len(positives),
        "mean_blocked_return_per_million_uniform_seed": float(
            sum(Fraction(seed["blocked_probability"]) for seed in seeds) * 10**6 / len(seeds)),
        "asymmetric_positive_pairs": sum(
            a["probability"] != b["probability"] for a, b in zip(records[::2], records[1::2])),
        "open_percent_range": [
            float(extreme(Fraction(seed["still_open"]) for seed in seeds) * 100)
            for extreme in (min, max)],
        "minimum_positive_per_million": float(min(positives) * 10**6),
        "maximum_positive_per_million": float(max(positives) * 10**6),
        "seeds_with_blocked_targets": sum(row["blocked_targets"] > 0 for row in seeds),
        "seeds_with_reachable_targets": sum(row["reachable_targets"] > 0 for row in seeds),
        "seeds_with_outside_carrier_returns": sum(row["outside_carrier"] != "0" for row in seeds),
    }
    return {"summary": summary, "directions": records, "seeds": seeds}


if __name__ == "__main__":
    result = run()
    (HERE / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))
