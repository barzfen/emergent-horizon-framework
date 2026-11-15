"""Independently check the local colour rules and finite CROSS-39 bounds."""

from itertools import product


def reversal_rules(length):
    rules = {}
    for signs in map("".join, product("+-", repeat=length + 1)):
        colours = [0]
        for sign in signs:
            step = 1 if sign == "+" else -1
            colours.append((colours[-1] + step) % 3)
        reversed_colours = colours[:1] + colours[1:-1][::-1] + colours[-1:]
        if reversed_colours == colours:
            continue
        if any(a == b for a, b in zip(reversed_colours, reversed_colours[1:])):
            continue
        rules[signs] = "".join(
            "+" if (b - a) % 3 == 1 else "-"
            for a, b in zip(reversed_colours, reversed_colours[1:])
        )
    return rules


LR3 = reversal_rules(3)
LR4 = reversal_rules(4)


def pair_markers(signs):
    return tuple(a == b for a, b in zip(signs, signs[1:]))


def check_local_rules():
    assert LR3 == {"-++-": "+--+", "+--+": "-++-"}
    assert len(LR4) == 14
    for signs in LR4:
        markers = pair_markers(signs)
        assert markers == (True, False, False, True) or any(
            a and b for a, b in zip(markers, markers[1:])
        )
    for left, right in product("+-", repeat=2):
        for window, replacement in LR3.items():
            before = pair_markers(left + window + right)
            after = pair_markers(left + replacement + right)
            assert before[1:4] == (False, True, False)
            changes = tuple(i for i, pair in enumerate(zip(before, after)) if pair[0] != pair[1])
            assert changes == (0, 4)


def seed(t):
    return ("++" + "-+" * t + "-") * 3


def rewrite(signs, start, replacement):
    if start + 4 <= len(signs):
        return signs[:start] + replacement + signs[start + 4:]
    wrap = start + 4 - len(signs)
    return replacement[-wrap:] + signs[wrap:start] + replacement[:-wrap]


def first_times(t):
    initial = seed(t)
    size = len(initial)
    frontier = {initial}
    seen = {initial}
    first_lr4 = None
    first_triple = None
    for depth in range(t + 2):
        next_frontier = set()
        for signs in frontier:
            extended = signs + signs[:4]
            if first_lr4 is None and any(extended[i:i + 5] in LR4 for i in range(size)):
                first_lr4 = depth
            if first_triple is None and ("+++" in extended or "---" in extended):
                first_triple = depth
            if first_lr4 is not None and first_triple is not None:
                return first_lr4, first_triple
            if depth == t + 1:
                continue
            for i in range(size):
                replacement = LR3.get(extended[i:i + 4])
                if replacement is None:
                    continue
                neighbour = rewrite(signs, i, replacement)
                if neighbour not in seen:
                    next_frontier.add(neighbour)
                    seen.add(neighbour)
        frontier = next_frontier
    return first_lr4, first_triple


def main():
    check_local_rules()
    for t in range(1, 13):
        assert first_times(t) == (t, t + 1), t
    for t in range(1, 101):
        signs = seed(t)
        for i in range(2 * t + 2, 3, -2):
            signs = rewrite(signs, i, LR3[signs[i:i + 4]])
        assert signs[:7] == "++-++--"
        signs = rewrite(signs, 2, LR3[signs[2:6]])
        assert signs[:3] == "+++"
    print("Local rules verified. Exact BFS depths checked through t=12 and witnesses through t=100.")


if __name__ == "__main__":
    main()
