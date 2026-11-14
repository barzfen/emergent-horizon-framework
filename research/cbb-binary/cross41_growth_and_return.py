"""Check receiver activation and local acknowledgements after one proper insertion."""

from collections import deque

from cross39_equal_pair_ancestry import LR3, rewrite, seed


RECEIVER = 2
SOURCE = 6
OLD_ACK = "-+-+-"
NEW_ACK = "-+++"


def split_edge(signs, index):
    opposite = "-" if signs[index] == "+" else "+"
    return signs[:index] + opposite * 2 + signs[index + 1:]


def read(signs, start, width):
    return (signs + signs[:width - 1])[start:start + width]


def explore(initial, clamp_receiver=False):
    depths = {initial: 0}
    queue = deque([initial])
    while queue:
        state = queue.popleft()
        extended = state + state[:3]
        for start in range(len(state)):
            if clamp_receiver and start == RECEIVER:
                continue
            replacement = LR3.get(extended[start:start + 4])
            if replacement is None:
                continue
            neighbour = rewrite(state, start, replacement)
            if neighbour not in depths:
                depths[neighbour] = depths[state] + 1
                queue.append(neighbour)
    return depths


def first_receiver(depths):
    return min(
        (depth for state, depth in depths.items() if read(state, RECEIVER, 4) in LR3),
        default=None,
    )


def first_pattern(depths, pattern):
    return min(
        (depth for state, depth in depths.items() if read(state, SOURCE, len(pattern)) == pattern),
        default=None,
    )


def apply_history(signs, starts):
    for start in starts:
        signs = rewrite(signs, start, LR3[read(signs, start, 4)])
    return signs


def colours(signs):
    result = [0]
    for sign in signs:
        result.append((result[-1] + (1 if sign == "+" else -1)) % 3)
    assert result[-1] == result[0]
    return result[:-1]


def main():
    parent = seed(2)
    for slot in (6, 7):
        child = colours(split_edge(parent, slot))
        assert child[:slot + 1] + child[slot + 2:] == colours(parent)
        assert child[slot + 1] not in (child[slot], child[slot + 2])
    expectations = {
        # (full size, clamped size, receiver enabled, old ack full/clamped, new ack full/clamped)
        None: (229, 201, 2, 6, None, 3, 3),
        6: (56, 56, None, None, None, None, None),
        7: (924, 564, 11, 6, 6, 31, None),
    }
    for slot, expected in expectations.items():
        initial = parent if slot is None else split_edge(parent, slot)
        full = explore(initial)
        clamped = explore(initial, clamp_receiver=True)
        actual = (
            len(full), len(clamped), first_receiver(full),
            first_pattern(full, OLD_ACK), first_pattern(clamped, OLD_ACK),
            first_pattern(full, NEW_ACK), first_pattern(clamped, NEW_ACK),
        )
        assert actual == expected, (slot, actual)
        print(f"Insertion slot {slot}: {actual}")

    echo = (6, 4, 2, 8, 6, 4)
    assert read(apply_history(parent, echo[:2]), RECEIVER, 4) == "-++-"
    assert read(apply_history(parent, echo[:3]), RECEIVER, 4) == "+--+"
    assert read(apply_history(parent, echo[:3]), SOURCE, 5) == "-+-++"
    assert read(apply_history(parent, echo), SOURCE, 5) == OLD_ACK

    false_echo = (21, 1, 3, 6, 8, 10)
    assert read(apply_history(split_edge(parent, 7), false_echo), SOURCE, 5) == OLD_ACK


if __name__ == "__main__":
    main()
