"""Check the local oscillator and passive insertion counters under growth."""

from collections import Counter
from fractions import Fraction
from math import exp, fsum, log, prod, sqrt

from cross46_local_clock import INITIAL, PHASES, observe, updates
from cross57_growth_phase import refine
from cross59_growth_ratios import initial_colours


def clock_targets(signs):
    clock, growth = [], []
    for kind, target in updates(signs, len(signs) + 1):
        if kind == "clock":
            clock.append(target)
        elif kind == "growth":
            growth.append(target)
    assert len(clock) == 1 and len(growth) == len(signs) - 12
    phase = PHASES.index(observe(signs))
    assert observe(clock[0]) == PHASES[(phase + 1) % len(PHASES)]
    assert all(observe(target) == PHASES[phase] for target in growth)
    return clock[0], growth


def clock_trace(grow_at_midpoint):
    signs = INITIAL
    trace = []
    for tick in range(7):
        if tick == 3:
            for _ in range(grow_at_midpoint):
                _, growth = clock_targets(signs)
                signs = growth[0]
        trace.append(signs[-4:] + signs[:8])
        if tick < 6:
            signs, _ = clock_targets(signs)
    return len(signs), tuple(trace)


def clock_mass(n, m, rate, max_ticks):
    """Convolve the per-size waiting laws, keeping exact low-count masses."""
    mass = [Fraction(1)] + [Fraction(0)] * max_ticks
    for size in range(n, n + m):
        growth_slots = size - 12
        ratio = Fraction(rate, growth_slots + rate)
        next_mass = []
        for count in range(max_ticks + 1):
            following = (1 - ratio) * mass[count]
            if count:
                following += ratio * next_mass[-1]
            next_mass.append(following)
        mass = next_mass
    return mass


def explicit_clock_mass(m, rate, max_ticks):
    mass = [Fraction(0)] * (max_ticks + 1)
    histories = 0

    def visit(signs, grows, ticks, weight):
        nonlocal histories
        if grows == m:
            mass[ticks] += weight
            histories += 1
            return
        clock, growth = clock_targets(signs)
        per_weight = weight / (len(growth) + rate)
        for target in growth:
            visit(target, grows + 1, ticks, per_weight)
        if ticks < max_ticks:
            visit(clock, grows, ticks + 1, rate * per_weight)

    visit(INITIAL, 0, 0, Fraction(1))
    return mass, histories


def passive_mass(n, m, ports):
    mass = [Fraction(1)]
    for size in range(n, n + m):
        hit = Fraction(ports, size)
        following = [Fraction(0)] * (len(mass) + 1)
        for count, weight in enumerate(mass):
            following[count] += (1 - hit) * weight
            following[count + 1] += hit * weight
        mass = following
    return mass


def explicit_port_counts(colours, m, anchors):
    counts = Counter()

    def read(tour, colours):
        neighbours = dict(zip(tour, tour[1:] + tour[:1]))
        return tuple((colours[neighbours[anchor]] - colours[anchor]) % 3 for anchor in anchors)

    def visit(tour, colours, reading, depth, ticks):
        if depth == m:
            counts[ticks] += 1
            return
        for slot, source in enumerate(tour):
            child, child_colours = refine(tour, colours, slot)
            following = read(child, child_colours)
            flips = sum(a != b for a, b in zip(reading, following))
            assert flips == int(source in anchors)
            visit(child, child_colours, following, depth + 1, ticks + flips)

    tour = tuple(range(len(colours)))
    visit(tour, colours, read(tour, colours), 0, 0)
    return counts


def main():
    n = len(INITIAL)
    stay, baseline = clock_trace(0)
    doubled, grown = clock_trace(n)
    assert (stay, doubled) == (n, 2 * n) and baseline == grown
    print(f"Identical local clock traces with final sizes {stay} and {doubled}.")

    for rate in (1, 2):
        mass, histories = explicit_clock_mass(3, rate, 3)
        assert mass == clock_mass(n, 3, rate, 3)
    print(f"Checked {histories:,} protected-clock histories per rate through three growth events and up to three ticks.")

    n = 6
    m = 4
    colours = initial_colours(n, 3, 1)
    histories = prod(range(n, n + m))
    for anchors in ((0,), (0, 1)):
        counts = explicit_port_counts(colours, m, anchors)
        assert counts.total() == histories
        assert [Fraction(counts[k], histories) for k in range(m + 1)] == passive_mass(n, m, len(anchors))
    print(f"Checked all {histories:,} labelled insertion histories for each passive readout.")

    n = 100_000
    mean = fsum(1 / size for size in range(n - 12, 2 * n - 12))
    no_clock_tick = Fraction(n - 12, 2 * n - 12)
    assert abs(mean - log(2)) < 0.0001 and abs(no_clock_tick - 0.5) < 0.0001
    print(f"Six-reversal clock, rate one, doubling from {n:,}: mean {mean:.6f}, zero ticks {float(no_clock_tick):.6f}.")
    for ports in (1, 2, 16, 64):
        no_hit = exp(-ports * log(2))
        standard_deviation = sqrt(log(2) / ports)
        print(f"Doubling limit, {ports:2d} passive ports: zero ticks {no_hit:.6g}, log-growth SD {standard_deviation:.6f}.")


if __name__ == "__main__":
    main()
