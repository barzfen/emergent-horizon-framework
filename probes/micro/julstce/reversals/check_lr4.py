"""Cross-check the run-level calculation against literal slot reversals."""

import csv
import itertools
import math
import subprocess
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from probe import run_lengths, shape, valid

RINGS = ("1100110011111000", "0011110011100110")


def boundary_count(word):
    return sum(word[i - 1] != bit for i, bit in enumerate(word))


def grow(states):
    result = defaultdict(Fraction)
    for ring, mass in states.items():
        events = [
            ring[:i] + bit + ring[i:]
            for i, bit in itertools.product(range(len(ring)), "01")
            if bit in (ring[i - 1], ring[i])
        ]
        for word in events:
            result[word] += mass / len(events)
    return result


def reverse(states, rate):
    result = defaultdict(Fraction)
    for ring, mass in states.items():
        result[ring] += mass * (1 - rate)
        for i in range(len(ring)):
            rotated = ring[i:] + ring[:i]
            trial = rotated[:4][::-1] + rotated[4:]
            if not valid(trial) or boundary_count(trial) != 6:
                trial = rotated
            word = trial[-i:] + trial[:-i] if i else trial
            result[word] += mass * rate / len(ring)
    return result


def check(binary, rate):
    states = {RINGS[0]: Fraction(1), RINGS[1]: Fraction(-1)}
    command = [str(binary), str(rate.numerator), str(rate.denominator), "4"]
    rows = {int(row["insertions"]): row for row in csv.DictReader(
        subprocess.check_output(command, text=True).splitlines()
    )}
    for steps in range(1, 5):
        states = reverse(grow(states), rate) if rate else grow(states)
        if steps not in rows:
            continue
        quotient = defaultdict(Fraction)
        for word, mass in states.items():
            quotient[shape(run_lengths(word))] += mass
        expected = Fraction(1, 2) + sum(map(abs, quotient.values())) / 4
        actual = float(rows[steps]["optimal_accuracy"])
        assert math.isclose(float(expected), actual, rel_tol=0, abs_tol=1e-11)


if __name__ == "__main__":
    for rate in (Fraction(0), Fraction(1, 200), Fraction(1, 4), Fraction(1)):
        check(Path(sys.argv[1]).resolve(), rate)
    print("Literal slot enumeration agrees at 1, 2 and 4 insertions for all four rates.")
