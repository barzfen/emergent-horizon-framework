"""Verify endpoint ambiguity and a two-sign history detector with growth."""

from collections import deque

from cross41_growth_and_return import LR3, RECEIVER, read, rewrite, seed, split_edge
from cross42_resettable_return import ACKNOWLEDGEMENT, observe


PARENT = seed(2)
RECEIVE = ("reverse", RECEIVER)
TRACE = ("-+", "+-", "-+", "--", "++", "--", "-+", "+-")
ONE_INSERTION = (
    ("reverse", 6), ("reverse", 4), RECEIVE, ("insert", 9),
    ("reverse", 14), ("reverse", 12), ("reverse", 10), ("reverse", 7),
    ("reverse", 5), ("reverse", 5), RECEIVE, ("reverse", 7), ("reverse", 4),
)
TWO_INSERTIONS = (
    ("reverse", 6), ("reverse", 6), ("insert", 7), ("reverse", 14),
    ("reverse", 12), ("reverse", 10), ("reverse", 8), ("reverse", 5),
    ("reverse", 5), ("insert", 7), ("reverse", 9), ("reverse", 6),
)


def moves(signs, max_size):
    for index in range(len(signs)):
        replacement = LR3.get(read(signs, index, 4))
        if replacement is not None:
            yield ("reverse", index), rewrite(signs, index, replacement)
        if index >= 6 and len(signs) < max_size:
            yield ("insert", index), split_edge(signs, index)


def local(signs):
    return read(signs, 6, 2)


def reachable(initial, max_size, clamp=False):
    seen = {initial}
    queue = deque([initial])
    while queue:
        signs = queue.popleft()
        for event, target in moves(signs, max_size):
            if target not in seen and (not clamp or event != RECEIVE):
                seen.add(target)
                queue.append(target)
    return seen


def trace_is_possible(initials, trace, max_size, clamp=False):
    seen = {(signs, 0) for signs in initials if local(signs) == trace[0]}
    queue = deque(seen)
    while queue:
        signs, index = queue.popleft()
        if index == len(trace) - 1:
            return True
        for event, target in moves(signs, max_size):
            if clamp and event == RECEIVE:
                continue
            if local(target) == trace[index]:
                following = index
            elif local(target) == trace[index + 1]:
                following = index + 1
            else:
                continue
            state = target, following
            if state not in seen:
                seen.add(state)
                queue.append(state)
    return False


def replay(events, max_size):
    signs = PARENT
    tour = list(range(len(signs)))
    colour = 0
    colours = []
    for sign in signs:
        colours.append(colour)
        colour = (colour + (1 if sign == "+" else -1)) % 3
    assert colour == 0
    trace = [local(signs)]
    for event in events:
        operation, index = event
        signs = dict(moves(signs, max_size))[event]
        size = len(tour)
        if operation == "insert":
            colours.append(3 - colours[tour[index]] - colours[tour[(index + 1) % size]])
            tour.insert(index + 1, size)
        else:
            left, right = (index + 1) % size, (index + 3) % size
            tour[left], tour[right] = tour[right], tour[left]
        increments = [(colours[b] - colours[a]) % 3 for a, b in zip(tour, tour[1:] + tour[:1])]
        assert all(increments)
        assert signs == "".join("+" if step == 1 else "-" for step in increments)
        if local(signs) != trace[-1]:
            trace.append(local(signs))
    return signs, tour, colours, tuple(trace)


def main():
    before = tuple(("reverse", i) for i in (20, 1, 3, 18, 16, 20, 1, 18, 20))
    after = tuple(("reverse", i) for i in (5, 3, 1, 8, 6, 4, 10, 8, 12, 10, 15, 13, 17, 19, 21))
    common = before + (("insert", 8),) + after
    off = (("reverse", 6),) * 2 + common
    on = common + (RECEIVE,) * 2
    assert off.count(RECEIVE) == 0 and on.count(RECEIVE) == 2
    assert len(off) == len(on) == 27
    endpoint, tour, colours, _ = replay(off, 22)
    assert replay(on, 22)[:3] == (endpoint, tour, colours)
    assert observe(endpoint) == ACKNOWLEDGEMENT

    preparations = reachable(PARENT, 22)
    ready = {signs for signs in preparations if local(signs) == TRACE[0]}
    assert len(preparations) == 8783 and len(ready) == 3299
    assert trace_is_possible({PARENT}, TRACE[:-1], 22, clamp=True)
    assert not trace_is_possible(ready, TRACE, 22, clamp=True)
    assert replay(ONE_INSERTION, 22)[3] == TRACE
    assert RECEIVE in ONE_INSERTION
    assert TWO_INSERTIONS.count(RECEIVE) == 0
    assert replay(TWO_INSERTIONS, 23)[3] == TRACE
    print("Matched endpoints: 27 events, identical labelled cycles, zero vs two receiver reversals.")
    print("One insertion: all 3299 reachable ready states passed the control.")
    print("Two insertions: a legal receiver-free history matches the complete trace.")


if __name__ == "__main__":
    main()
