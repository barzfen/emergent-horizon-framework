"""Compare endpoint parity rules with a completed-cycle Pi certificate."""
from collections import Counter, defaultdict
from functools import lru_cache
import importlib.util
import json
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAGGED = HERE.parent / "tagged-controller-05" / "probe.py"
spec = importlib.util.spec_from_file_location("rev05", TAGGED)
rev05 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rev05)
rev04 = rev05.rev04


def compatible(pair, even):
    a, b = pair
    return (a in even) != (b in even) or (a == 0 and b in even)


def certificate(graph, neighbours, even):
    return all(compatible(pair, even) for pair in graph) and max(neighbours[0]) in even


def canonical_even(neighbours):
    cycle = [0, min(neighbours[0])]
    while len(cycle) < len(neighbours):
        cycle.append(next(v for v in neighbours[cycle[-1]] if v != cycle[-2]))
    return set(cycle[::2])


def check_certificate(n, even):
    checked = positives = 0
    for tail in permutations(range(1, n)):
        if tail[0] > tail[-1]:
            continue
        cycle = (0,) + tail
        graph = rev04.cycle_edges(cycle)
        neighbours = rev04.adjacency(graph, n)
        expected = set(cycle[::2]) == even
        assert certificate(graph, neighbours, even) == expected
        positives += expected
        checked += 1
    return {"cycles_checked": checked, "same_pi_cycles": positives}


def trial(source, ones, even, blocked, policy, is_cycle, passes):
    n = len(source)
    active = {source: {None: 1.0}}
    absorbed = Counter()
    wrong_compatible = 0.0
    snapshots = []
    for step in range(1, rev05.HORIZON + 1):
        following = defaultdict(Counter)
        for graph, memories in active.items():
            options = []
            for dest, (add, cut) in rev04.slides(graph, n, ones):
                local_ok = compatible(add, even)
                if policy in ("hard_endpoint", "hard_endpoint_seam", "hard_endpoint_seam_order") and not local_ok:
                    continue
                if policy in ("hard_endpoint_seam", "hard_endpoint_seam_order") and (0 in add or 0 in cut):
                    at_anchor = sorted(b for a, b in dest if a == 0)
                    if len(at_anchor) == 2:
                        first_even = at_anchor[0] in even
                        last_even = at_anchor[1] in even
                        if first_even and not last_even:
                            continue
                        if policy == "hard_endpoint_seam" and first_even == last_even:
                            continue
                if policy == "cycle_oracle" and is_cycle(dest) and not passes(dest):
                    continue
                pivot, = set(add) & set(cut)
                old_end, = set(cut) - {pivot}
                new_end, = set(add) - {pivot}
                factor = rev05.BOOST if policy == "soft_endpoint" and local_ok else 1
                wrong_closure = is_cycle(dest) and not passes(dest)
                options.append((dest, add, cut, pivot, old_end, new_end, factor,
                                wrong_closure and local_ok))
            if not options:
                absorbed["stalled"] += sum(memories.values())
                continue
            for marker, mass in memories.items():
                weights = []
                for _, _, _, pivot, old_end, new_end, factor, _ in options:
                    continuing = (marker is not None and (pivot, old_end) == (marker[0], marker[2])
                                  and new_end != marker[1])
                    weights.append(factor * (rev05.BOOST if continuing else 1))
                total = sum(weights)
                for option, weight in zip(options, weights):
                    dest, add, cut, pivot, old_end, new_end, _, missed = option
                    tag = rev05.marker_after(marker, add, cut, pivot, old_end, new_end, step,
                                             "tagged_connection")
                    probability = mass * weight / total
                    following[dest][tag] += probability
                    if missed:
                        wrong_compatible += probability
        active = {}
        for graph, memories in following.items():
            if not is_cycle(graph):
                active[graph] = memories
                continue
            if graph == source:
                outcome = "original"
            elif graph in blocked:
                outcome = "blocked_lr4"
            else:
                outcome = "other_same_pi" if passes(graph) else "different_pi"
            absorbed[outcome] += sum(memories.values())
        open_mass = sum(sum(memories.values()) for memories in active.values())
        assert abs(open_mass + sum(absorbed.values()) - 1) < 1e-10
        snapshots.append({"slides": step, **absorbed, "still_open": open_mass,
                          "wrong_pi_with_compatible_final_join": wrong_compatible,
                          "open_graphs": len(active)})
    return snapshots


def run():
    data = json.loads(rev05.PARENT.read_text())
    previous = json.loads((TAGGED.parent / "results.json").read_text())
    carrier = data["carrier"]
    cycles = carrier["states"]
    index = cycles.index(data["seed"])
    graphs = [rev04.cycle_edges(cycle) for cycle in cycles]
    n = len(data["seed"])
    even = set(data["Pi"])
    groups = {v: k for k, group in enumerate(carrier["fast_groups"]) for v in group}
    blocked = {graphs[j if i == index else i] for i, j in carrier["slow_edges"]
               if index in (i, j) and groups[i] != groups[j]}

    @lru_cache(maxsize=30000)
    def is_cycle(graph):
        degree = [0] * n
        for a, b in graph:
            degree[a] += 1
            degree[b] += 1
        return all(d == 2 for d in degree)

    @lru_cache(maxsize=None)
    def passes(graph):
        adj = rev04.adjacency(graph, n)
        verdict = certificate(graph, adj, even)
        assert verdict == (canonical_even(adj) == even)
        return verdict

    result = {"seed": data["seed"], "even": data["Pi"],
              "certificate_check": check_certificate(n, even), "policies": {}}
    for policy in ("tagged", "soft_endpoint", "hard_endpoint", "hard_endpoint_seam", "hard_endpoint_seam_order", "cycle_oracle"):
        rows = trial(graphs[index], set(data["ones"]), even, blocked, policy, is_cycle, passes)
        result["policies"][policy] = rows
        print(policy, json.dumps(rows[-1]), flush=True)
    for earlier, current in zip(previous["policies"]["tagged_connection"],
                                result["policies"]["tagged"]):
        for key in ("original", "blocked_lr4", "different_pi", "other_same_pi", "still_open"):
            assert abs(earlier.get(key, 0) - current.get(key, 0)) < 1e-12
    for policy in ("hard_endpoint_seam", "hard_endpoint_seam_order", "cycle_oracle"):
        assert all(row.get("different_pi", 0) == 0 for row in result["policies"][policy])
    return result


if __name__ == "__main__":
    result = run()
    (HERE / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(result["certificate_check"])
