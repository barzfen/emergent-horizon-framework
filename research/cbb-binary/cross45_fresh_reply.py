"""Audit fresh write and reset transitions in the joint growth graph."""

from collections import deque

from cross41_growth_and_return import apply_history, read, split_edge
from cross43_local_history import PARENT, RECEIVE, moves, reachable
from cross44_cycle_record import CLEAR, PATTERNS, REARM, SIZES, WRITE, outside_receiver


def records():
    written = apply_history(PARENT, WRITE)
    first_child = split_edge(written, 14)
    second_child = split_edge(first_child, 17)
    return dict(zip(SIZES, (written, first_child, second_child)))


def observe(signs, extra):
    width = len(PATTERNS[len(signs)][0])
    exterior = read(signs, 7, width)
    return exterior if extra is None else (exterior, signs[extra])


def no_receiver_closure(initial, max_size):
    seen = set(initial)
    queue = deque(seen)
    while queue:
        signs = queue.popleft()
        for event, target in moves(signs, max_size):
            if event != RECEIVE and target not in seen:
                seen.add(target)
                queue.append(target)
    return seen


def phase_sets(full, witnesses, extra):
    clear_reads = {n: observe(apply_history(record, CLEAR), extra) for n, record in witnesses.items()}
    write_reads = {n: observe(record, extra) for n, record in witnesses.items()}
    cleared, written = set(), set()
    for signs in full:
        size = len(signs)
        reading = observe(signs, extra)
        if reading == write_reads[size]:
            written.add(signs)
        if reading == clear_reads[size]:
            cleared.add(signs)
    return cleared, written


def audit_witnesses(witnesses):
    for size, written in witnesses.items():
        halfway = apply_history(written, CLEAR[:1])
        cleared = apply_history(written, CLEAR)
        assert outside_receiver(halfway) == outside_receiver(cleared)
        assert halfway[2] == "+" and cleared[2] == "-"
        assert apply_history(halfway, CLEAR[:1]) == written
        assert apply_history(cleared, REARM) == written
        assert observe(halfway, 2) not in {observe(cleared, 2), observe(written, 2)}
        print(f"{size}: halfway and cleared look identical outside the receiver.")

    written = witnesses[21]
    cleared = apply_history(written, CLEAR)
    assert CLEAR == (4, 2) and REARM == (2, 4)
    # Start clear at 21, fire the receiver, grow twice, and finish writing at 23.
    pending = apply_history(cleared, REARM[:1])
    pending = split_edge(split_edge(pending, 14), 17)
    assert apply_history(pending, REARM[1:]) == witnesses[23]
    # Alternatively start written at 21, begin clearing, grow, and finish at 23.
    pending = apply_history(written, CLEAR[:1])
    pending = split_edge(split_edge(pending, 14), 17)
    assert apply_history(pending, CLEAR[1:]) == apply_history(witnesses[23], CLEAR)


def main():
    max_size = max(SIZES)
    witnesses = records()
    audit_witnesses(witnesses)
    full = reachable(PARENT, max_size)
    assert len(full) == 130056

    expected = {
        None: ((15, 15, 14), True),
        2: ((4, 4, 3), False),
        3: ((10, 10, 10), False),
        4: ((11, 11, 11), True),
        5: ((11, 11, 11), True),
    }
    for extra, (counts, false_transition) in expected.items():
        cleared, written = phase_sets(full, witnesses, extra)
        assert tuple(sum(len(s) == n for s in cleared) for n in SIZES) == counts
        assert tuple(sum(len(s) == n for s in written) for n in SIZES) == (4, 4, 3)
        false_write = bool(no_receiver_closure(cleared, max_size) & written)
        false_clear = bool(no_receiver_closure(written, max_size) & cleared)
        assert false_write == false_clear == false_transition
        print(f"Extra sign {extra}: false write {false_write}, false clear {false_clear}.")


if __name__ == "__main__":
    main()
