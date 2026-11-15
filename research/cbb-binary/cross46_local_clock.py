"""Check the prepared LR3 clock with protected growth and a classical Bell control."""

from collections import Counter, deque
from fractions import Fraction
from itertools import product

from cross41_growth_and_return import apply_history, split_edge
from cross43_local_history import moves
from cross44_cycle_record import CLEAR
from cross45_fresh_reply import records


# Observation order around the seam: tail, two unused signs, core.
PHASES = (
    ("-++-+-", "+--+"),
    ("+--++-", "+--+"),
    ("+-+--+", "+--+"),
    ("+-+--+", "-++-"),
    ("+--++-", "-++-"),
    ("-++-+-", "-++-"),
)
STARTS = (2, 4, -4, 4, 2, -4)
RULE = dict(zip(PHASES, STARTS))
INITIAL = apply_history(records()[21], CLEAR)


def observe(signs):
    return signs[2:8], signs[-4:]


def support(size):
    return set(range(2, 8)) | set(range(size - 4, size))


def updates(signs, cap, protect_growth=True):
    size = len(signs)
    patch = support(size)
    clock_start = RULE.get(observe(signs))
    for (operation, start), target in moves(signs, cap):
        if operation == "insert":
            if not protect_growth or start not in patch:
                yield "growth", target
        elif clock_start is not None and start == clock_start % size:
            yield "clock", target
        elif patch.isdisjoint((start + offset) % size for offset in range(4)):
            yield "background", target


def census(cap, protect_growth=True):
    pending = deque([INITIAL])
    seen = {INITIAL}
    while pending:
        state = pending.popleft()
        phase = observe(state)
        clock_edges = 0
        for operation, target in updates(state, cap, protect_growth):
            next_phase = observe(target)
            if operation == "clock":
                clock_edges += 1
                assert next_phase == PHASES[(PHASES.index(phase) + 1) % len(PHASES)]
            elif protect_growth or operation == "background":
                assert next_phase == phase
            if target not in seen:
                seen.add(target)
                pending.append(target)
        assert clock_edges == int(phase in RULE)
    return Counter((len(state), observe(state) in RULE) for state in seen)


def check_growth():
    assert observe(INITIAL) == PHASES[0]
    assert census(24) == {(21, True): 6, (22, True): 144, (23, True): 1134, (24, True): 4560}
    assert census(22, protect_growth=False) == {(21, True): 6, (22, True): 144, (22, False): 36}
    broken = split_edge(INITIAL, 6)
    assert ("growth", broken) in set(updates(INITIAL, 22, protect_growth=False))
    assert observe(broken) not in RULE
    assert all(kind != "clock" for kind, _ in updates(broken, 22, protect_growth=False))

    # The original undirected move relation can always undo a legal move.
    assert apply_history(INITIAL, (2, 2)) == INITIAL

    # Even with protected growth and the local rule, background events can starve the clock.
    grown, detour = next(
        (child, target)
        for operation, child in updates(INITIAL, 22) if operation == "growth"
        for kind, target in updates(child, 22) if kind == "background"
    )
    assert ("growth", grown) in set(updates(INITIAL, 22))
    assert ("background", grown) in set(updates(detour, 22))

    # The two previously studied insertion slots are permitted in any of the six phases.
    state = INITIAL
    for phase, start in zip(PHASES, STARTS):
        assert observe(state) == phase
        child = split_edge(state, 14)
        grandchild = split_edge(child, 17)
        assert ("growth", child) in set(updates(state, 23))
        assert ("growth", grandchild) in set(updates(child, 23))
        assert observe(grandchild) == phase
        state = apply_history(state, (start % len(state),))
    assert state == INITIAL


def value(sign):
    return 1 if sign == "+" else -1


def bell_control():
    # A fair shared preparation selects phase 0 or 3 before choosing either setting.
    state = INITIAL
    for start in STARTS[:3]:
        state = apply_history(state, (start % len(state),))
    pairs = [observe(INITIAL), observe(state)]
    assert pairs == [PHASES[0], PHASES[3]]
    correlations = []
    for x, y in product(range(2), repeat=2):
        outcomes = [(value(core[x]), value(tail[y])) for core, tail in pairs]
        assert sum(a for a, _ in outcomes) == sum(b for _, b in outcomes) == 0
        correlations.append(Fraction(sum(a * b for a, b in outcomes), len(pairs)))
    assert correlations == [-1, 1, 1, -1]
    assert abs(sum(correlations[:3]) - correlations[3]) == 2


if __name__ == "__main__":
    check_growth()
    bell_control()
    print("Protected clock: 5844 reachable states through three insertions, all with one clock move.")
    print("Unrestricted single insertion: 36 reachable states without a clock move.")
    print("Classical CHSH control: unbiased marginals, correlations (-1, 1, 1, -1), S=2.")
