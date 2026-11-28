"""First-cycle probabilities for a controller with one local edge marker."""
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "rare-channel-02" / "results.json"
SLIDES = HERE.parent / "local-reconnect-04" / "probe.py"
spec = importlib.util.spec_from_file_location("rev04", SLIDES)
rev04 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rev04)
HORIZON = 6
BOOST = 4


def marker_after(marker, add, cut, pivot, old_end, new_end, step, policy):
    if policy != "tagged_connection":
        return None
    if step == 1:
        return pivot, old_end, new_end
    if marker is None:
        return None
    anchor, _, current = marker
    if cut != rev04.edge(anchor, current):
        return marker
    if pivot == anchor:
        return pivot, old_end, new_end
    return None


def trial(source, ones, pi, blocked, witness, policy):
    n = len(source)
    active = {source: {None: 1.0}}
    absorbed = Counter()
    target_mass = 0.0
    snapshots = []
    for step in range(1, HORIZON + 1):
        following = defaultdict(Counter)
        for graph, memories in active.items():
            adj = rev04.adjacency(graph, n)
            moves = []
            for dest, (add, cut) in rev04.slides(graph, n, ones):
                pivot, = set(add) & set(cut)
                old_end, = set(cut) - {pivot}
                new_end, = set(add) - {pivot}
                repair = len(adj[old_end]) == 3 and len(adj[new_end]) == 1
                moves.append((dest, add, cut, pivot, old_end, new_end, repair))
            if not moves:
                absorbed["stalled"] += sum(memories.values())
                continue
            for marker, mass in memories.items():
                weights = []
                for _, _, _, pivot, old_end, new_end, repair in moves:
                    continuing = (
                        marker is not None and (pivot, old_end) == (marker[0], marker[2])
                        and new_end != marker[1]
                    )
                    boosted = (
                        (policy == "branch_repair" and repair)
                        or (policy == "tagged_connection" and continuing)
                    )
                    weights.append(BOOST if boosted else 1)
                total_rate = sum(weights)
                for move, weight in zip(moves, weights):
                    dest, add, cut, pivot, old_end, new_end, _ = move
                    tag = marker_after(marker, add, cut, pivot, old_end, new_end, step, policy)
                    following[dest][tag] += mass * weight / total_rate
        active = {}
        for graph, memories in following.items():
            adj = rev04.adjacency(graph, n)
            if any(len(neighbours) != 2 for neighbours in adj):
                active[graph] = memories
                continue
            mass = sum(memories.values())
            if graph == source:
                outcome = "original"
            elif graph in blocked:
                outcome = "blocked_lr4"
            else:
                tour = [0, min(adj[0])]
                while len(tour) < n:
                    tour.append(next(v for v in adj[tour[-1]] if v != tour[-2]))
                outcome = "other_same_pi" if set(tour[::2]) == pi else "different_pi"
            absorbed[outcome] += mass
            if graph == witness:
                target_mass += mass
        open_mass = sum(sum(memories.values()) for memories in active.values())
        assert abs(open_mass + sum(absorbed.values()) - 1) < 1e-10
        snapshots.append({"slides": step, **absorbed, "still_open": open_mass,
                          "particular_witness": target_mass,
                          "open_graphs": len(active),
                          "open_graph_marker_states": sum(map(len, active.values()))})
    return snapshots


def run():
    source_bytes = PARENT.read_bytes()
    parent = json.loads(source_bytes)
    carrier = parent["carrier"]
    tours = carrier["states"]
    seed = carrier["states"].index(parent["seed"])
    graphs = [rev04.cycle_edges(tour) for tour in tours]
    groups = {v: i for i, component in enumerate(carrier["fast_groups"]) for v in component}
    blocked = {
        graphs[j if i == seed else i] for i, j in carrier["slow_edges"]
        if seed in (i, j) and groups[i] != groups[j]
    }
    witness = rev04.cycle_edges([0, 1, 2, 7, 6, 5, 4, 3, 8])
    assert witness in blocked
    args = graphs[seed], set(parent["ones"]), set(parent["Pi"]), blocked, witness
    return {
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "slide_source_sha256": hashlib.sha256(SLIDES.read_bytes()).hexdigest(),
        "seed": tours[seed], "boost": BOOST, "horizon": HORIZON,
        "blocked_targets": len(blocked),
        "policies": {policy: trial(*args, policy) for policy in
                     ("equal", "branch_repair", "tagged_connection")},
    }


if __name__ == "__main__":
    result = run()
    (HERE / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    for name, rows in result["policies"].items():
        print(name, json.dumps(rows[-1]))
