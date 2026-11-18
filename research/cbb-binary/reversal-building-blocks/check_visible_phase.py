"""Verify observable reversal periods and their doubling by legal growth."""

from collections import Counter
from itertools import pairwise, permutations, product


EXTERIOR = "ACBCABC"


def proper(word):
    return all(left != right for left, right in pairwise(word + word[0]))


def encode(cells):
    return "".join("A" + colour for colour in cells) + EXTERIOR


def shift(cells):
    return cells[-1] + cells[:-1]


def reverse_twice(word, width):
    first = word[: width - 1][::-1] + word[width - 1 :]
    second = first[0] + first[1:width][::-1] + first[width:]
    assert proper(first) and proper(second)
    return second


def insert_third(word, index):
    colour, = set("ABC") - {word[index], word[index + 1]}
    return word[: index + 1] + colour + word[index + 1 :]


def grow(word, width):
    for index in range(width - 1, 0, -2):
        word = insert_third(word, index)
        assert proper(word)
        word = insert_third(word, index)
        assert proper(word)
    return word


def read_cells(word):
    pair_counts = Counter(frozenset(pair) for pair in pairwise(word + word[0]))
    rare, runner_up, _ = sorted(pair_counts, key=pair_counts.__getitem__)
    assert pair_counts[rare] < pair_counts[runner_up]
    shared, = set(word) - rare

    candidates = []
    for direction in (word, word[::-1]):
        doubled = direction + direction
        for seam, symbol in enumerate(direction):
            if symbol != shared:
                continue
            _, short, long, *_ = doubled[seam : seam + len(EXTERIOR)]
            exterior = shared + short + long + short + shared + long + short
            if {short, long} == rare and doubled.startswith(exterior, seam):
                block = doubled[seam + len(EXTERIOR) : seam + len(word)]
                assert block[::2] == shared * (len(block) // 2)
                candidates.append(block[1::2].translate(str.maketrans(long + short, "BC")))
    cells, = candidates
    return cells


def period(word):
    for step in range(1, len(word) + 1):
        if word[-step:] + word[:-step] == word:
            return step


def check_growth_word():
    checked = 0
    for width in range(1, 11):
        for letters in product("BC", repeat=width):
            cells = "".join(letters)
            morphism = "".join("BC" if colour == "B" else "CB" for colour in cells)
            assert grow(encode(cells), 2 * width) == encode(morphism)
            assert period(morphism) == 2 * period(cells)
            checked += 1
    print(f"Growth and exact period-doubling checked on {checked:,} binary words.")


def check_phase_orbits():
    cells = "BCCB"
    presentations = 0
    periods = []
    for _ in range(7):
        width = 2 * len(cells)
        seed = encode(cells)
        word = seed
        visited = set()
        for _ in cells:
            reading = read_cells(word)
            visited.add(reading)
            if len(cells) <= 16:
                for colour_order in permutations("ABC"):
                    renamed = word.translate(str.maketrans("ABC", "".join(colour_order)))
                    for direction in (renamed, renamed[::-1]):
                        for offset in range(len(word)):
                            assert read_cells(direction[offset:] + direction[:offset]) == reading
                            presentations += 1
            word = reverse_twice(word, width)
            assert read_cells(word) == shift(reading)
        assert word == seed and len(visited) == len(cells)
        periods.append(len(visited))

        grown = grow(seed, width)
        assert proper(grown)
        grow_after_shift = grow(reverse_twice(seed, width), width)
        shift_after_grow = reverse_twice(reverse_twice(grown, 2 * width), 2 * width)
        assert grow_after_shift == shift_after_grow
        cells = read_cells(grown)

    print(f"Distinct observable phase periods: {periods}.")
    print(f"Readout survived {presentations:,} changes of root, orientation and colour names.")


if __name__ == "__main__":
    check_growth_word()
    check_phase_orbits()
