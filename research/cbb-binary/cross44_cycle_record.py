"""Verify a resettable cycle record and limits on preserving it under growth."""

from cross41_growth_and_return import apply_history, read, split_edge
from cross43_local_history import PARENT, RECEIVE, reachable, replay


WRITE = (6, 4, 2, 8, 6, 4, 13, 15, 17)
CLEAR = (4, 2)
REARM = CLEAR[::-1]
SIZES = (21, 22, 23)
PATTERNS = {
    21: ("+-+-", "--+-"),
    22: ("+-+-++++", "--+-++++"),
    23: ("+-+-+++++++", "--+-+++++++"),
}


def by_size(states):
    layers = {size: set() for size in SIZES}
    for state in states:
        layers[len(state)].add(state)
    return layers


def outside_receiver(signs):
    """Read every position except 2, 3, 4 and 5, in cyclic order."""
    return signs[6:] + signs[:2]


def children(signs):
    return (split_edge(signs, edge) for edge in range(6, len(signs)))


def check_record(full, clamped):
    written = apply_history(PARENT, WRITE)
    first_child = split_edge(written, 14)
    second_child = split_edge(first_child, 17)
    for record in (written, first_child, second_child):
        size = len(record)
        mark, blank = PATTERNS[size]
        assert read(record, 7, len(mark)) == mark
        assert record in full[size]
        assert not any(read(state, 7, len(mark)) == mark for state in clamped[size])

        cleared = apply_history(record, CLEAR)
        assert read(cleared, 7, len(blank)) == blank
        assert cleared in clamped[size]
        assert apply_history(cleared, REARM) == record
        print(f"{size} vertices: {mark} records a reply, {blank} clears it.")


def check_growth_limit(full, clamped):
    controls = {size: {outside_receiver(state) for state in layer} for size, layer in clamped.items()}
    records = full[21] - clamped[21]
    assert len(records) == 28
    for record in records:
        refinements = tuple(children(record))
        assert all(child in full[22] - clamped[22] for child in refinements)
        assert any(outside_receiver(child) in controls[22] for child in refinements)
    assert sum(
        all(grandchild not in clamped[23] for child in children(record) for grandchild in children(child))
        for record in records
    ) == 27

    child = split_edge(apply_history(PARENT, WRITE), 6)
    control_path = tuple(("reverse", i) for i in (6, 4, 8, 6))
    control_path += (("insert", 7),) + tuple(("reverse", i) for i in (14, 16, 18))
    assert RECEIVE not in control_path
    control, _, _, _ = replay(control_path, 22)
    assert child not in clamped[22] and control in clamped[22]
    assert outside_receiver(child) == outside_receiver(control)
    print("All 28 parent records retain whole-word evidence after one insertion.")
    print("Each has an insertion that makes every sign outside the receiver ambiguous.")


def main():
    full = by_size(reachable(PARENT, 23))
    clamped = by_size(reachable(PARENT, 23, clamp=True))
    assert tuple(map(len, full.values())) == (229, 8554, 121273)
    assert tuple(map(len, clamped.values())) == (201, 6568, 90931)
    check_record(full, clamped)
    check_growth_limit(full, clamped)


if __name__ == "__main__":
    main()
