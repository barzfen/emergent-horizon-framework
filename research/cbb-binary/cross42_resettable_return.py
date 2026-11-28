"""Verify a two-reading clock and its counterexample with growth between readings."""

from cross41_growth_and_return import (
    RECEIVER,
    apply_history,
    explore,
    read,
    seed,
    split_edge,
)


ACKNOWLEDGEMENT = "++--+-+++-"


def observe(signs):
    return read(signs, 5, 10)


def control_components(full):
    remaining = set(full)
    while remaining:
        component = explore(next(iter(remaining)), clamp_receiver=True)
        remaining.difference_update(component)
        yield component


def shortest_clock_cycle(full, ready):
    lengths = []
    for state, outbound in full.items():
        if observe(state) != ACKNOWLEDGEMENT:
            continue
        lengths.extend(
            outbound + inbound
            for destination, inbound in explore(state).items()
            if observe(destination) in ready
        )
    return min(lengths, default=None)


def main():
    parent = seed(2)
    ready = {observe(signs) for signs in (parent, split_edge(parent, 6), split_edge(parent, 7))}
    assert ready == {"+-++-+-+-+", "+++++-+-+-", "+---+-+-+-"}
    expected = {None: (6, 12), 6: (None, None), 7: (21, 30)}
    for slot in (None, *range(6, len(parent))):
        initial = parent if slot is None else split_edge(parent, slot)
        full = explore(initial)
        for component in control_components(full):
            readings = {observe(state) for state in component}
            assert ACKNOWLEDGEMENT not in readings or readings.isdisjoint(ready), slot
        if slot in expected:
            first = min(
                (depth for state, depth in full.items() if observe(state) == ACKNOWLEDGEMENT),
                default=None,
            )
            cycle = shortest_clock_cycle(full, ready)
            assert (first, cycle) == expected[slot], (slot, first, cycle)
            print(f"Slot {slot}: first acknowledgement {first}, first local rearm cycle {cycle}")

    witnesses = (
        (parent, (6, 4, 2, 8, 6, 13)),
        (split_edge(parent, 7), (21, 1, 3, 6, 8, 10, 12, 19, 17, 15, 21, 1, 4, 6, 8, 10, 13, 19, 21, 2, 4)),
    )
    for initial, path in witnesses:
        response = apply_history(initial, path)
        assert observe(response) == ACKNOWLEDGEMENT
        assert apply_history(response, path[::-1]) == initial

    # Same parent, armed at the seed, with one insertion between the two readings.
    before_growth = (20, 1, 3, 18, 16, 20, 1, 18, 20)
    after_growth = (5, 3, 1, 8, 6, 4, 10, 8, 12, 10, 15, 13)
    assert RECEIVER not in before_growth + after_growth
    grown = split_edge(apply_history(parent, before_growth), 8)
    assert observe(apply_history(grown, after_growth)) == ACKNOWLEDGEMENT
    print("All 16 fixed preparations passed the soundness check. Mid-run growth counterexample verified.")


if __name__ == "__main__":
    main()
