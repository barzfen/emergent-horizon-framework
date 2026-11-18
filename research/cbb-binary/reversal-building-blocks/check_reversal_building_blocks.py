"""Check the two-prefix-reversal construction on raw and three-colour cycles."""

from itertools import pairwise


def reverse_prefix(block, length):
    return block[:length][::-1] + block[length:]


def proper_local_words(length):
    words = [(colour,) for colour in range(3)]
    for _ in range(length - 1):
        words = [
            word + (colour,)
            for word in words
            for colour in range(3)
            if colour != word[-1]
        ]
    return words


def is_proper(colours):
    return all(left != right for left, right in pairwise(colours))


def orbit_with_fixed_flanks(colours):
    left, *initial, right = range(len(colours))
    initial = tuple(initial)
    block = initial
    label_orbit = set()
    colour_orbit = set()
    block_length = len(block)

    def read_colours(labels):
        return tuple(colours[label] for label in (left, *labels, right))

    for _ in range(block_length):
        label_orbit.add(block)
        colour_orbit.add(read_colours(block))
        for length in (block_length - 1, block_length):
            block = reverse_prefix(block, length)
            if not is_proper(read_colours(block)):
                return None

    assert block == initial
    return len(label_orbit), len(colour_orbit)


def check_raw():
    for length in range(3, 257):
        initial = tuple(range(length))
        block = initial
        labels_seen = set()
        for _ in range(length):
            labels_seen.add(block)
            shifted = reverse_prefix(reverse_prefix(block, length - 1), length)
            assert shifted == block[-1:] + block[:-1]
            block = shifted
        assert block == initial and len(labels_seen) == length
    print("Raw cycles: exact shift and period for block lengths 3–256.")


def check_three_colours():
    checked = 0
    repeatable = 0
    for length in range(3, 11):
        for colours in proper_local_words(length + 2):
            left, *block, right = colours
            can_repeat = (
                length % 2 == 0
                and left == right
                and left not in block
                and len(set(block)) == 2
            )
            orbit = orbit_with_fixed_flanks(colours)
            assert (orbit is not None) == can_repeat, (colours, orbit)
            if orbit is not None:
                assert orbit == (length, 2), (colours, orbit)
                for index in range(1, length):
                    swapped = (
                        colours[:index]
                        + colours[index : index + 2][::-1]
                        + colours[index + 2 :]
                    )
                    assert not is_proper(swapped), (colours, index)
                repeatable += 1
            checked += 1
    print(f"Three colours: {checked:,} proper local words, lengths 3–10.")
    print(f"Repeatable: {repeatable}. Every survivor has label period m and colour period 2.")
    print("Every adjacent swap inside a surviving block is blocked.")


if __name__ == "__main__":
    check_raw()
    check_three_colours()
