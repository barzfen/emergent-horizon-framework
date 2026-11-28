"""Verify the LR3 signal and oscillator controls in CROSS-40."""

from collections import Counter

from cross39_equal_pair_ancestry import LR3, LR4, rewrite, seed


CLOCK = "+++++-++++++--++++"
CLOCK_START = 11


def ring_windows(signs, width):
    extended = signs + signs[:width - 1]
    return (extended[i:i + width] for i in range(len(signs)))


def move(signs, start):
    window = (signs + signs[:3])[start:start + 4]
    return rewrite(signs, start, LR3[window])


def check_balanced(signs):
    colour = 0
    counts = Counter()
    for sign in signs:
        counts[colour] += 1
        colour = (colour + (1 if sign == "+" else -1)) % 3
    assert colour == 0
    assert set(counts.values()) == {len(signs) // 3}
    assert len(counts) == 3


def check(t):
    front = seed(t)
    initial = front + CLOCK + CLOCK
    check_balanced(initial)
    clock_starts = [len(front) + CLOCK_START, len(front) + len(CLOCK) + CLOCK_START]
    signs = initial
    clock_phases = (CLOCK, move(CLOCK, CLOCK_START))
    assert clock_phases[1] == "+++++-+++++-++-+++"
    assert move(clock_phases[1], CLOCK_START) == CLOCK

    for phase in clock_phases:
        clock_moves = [i for i, window in enumerate(ring_windows(phase, 4)) if window in LR3]
        assert clock_moves == [CLOCK_START]
        assert any(window in LR4 for window in ring_windows(phase, 5))
        check_balanced(phase)

    signal_starts = list(range(2 * t + 2, 3, -2))
    for start in signal_starts:
        assert signs[2:6] not in LR3
        next_marker = start - 1
        assert signs[next_marker] != signs[next_marker + 1]
        signs = move(signs, start)
        assert signs[next_marker] == signs[next_marker + 1]
    arrival = signs
    assert arrival[:5] == "++-++"
    assert arrival[2:6] == "-++-"
    received = move(arrival, 2)
    assert received[:3] == "+++"
    assert move(received, 2) == arrival
    assert received[len(front):] == CLOCK + CLOCK
    check_balanced(received)

    for toggles in range(5):
        for chosen_clock in clock_starts:
            during = initial
            for start in signal_starts:
                for _ in range(toggles):
                    during = move(during, chosen_clock)
                during = move(during, start)
            delayed = arrival
            for _ in range(toggles * t):
                delayed = move(delayed, chosen_clock)
            assert during == delayed

    for returns in range(1, 9):
        outcomes = []
        for chosen_clock in clock_starts:
            with_ticks = initial
            for _ in range(2 * returns):
                with_ticks = move(with_ticks, chosen_clock)
            for start in signal_starts:
                with_ticks = move(with_ticks, start)
            outcomes.append(with_ticks)
        assert outcomes == [arrival, arrival]


if __name__ == "__main__":
    for t in range(1, 101):
        check(t)
    print("Checked clock phases, signal paths, receiver activation, and matched histories for t=1..100.")
