"""Derive the cancellation character counts from inactive shuffle columns."""
from itertools import product
import json

from boundary import SWAPS, relabel
from branches import kernel
from probe import combine
from probe import cut, cuts, words
from reconstruct import axpy, can, kk, rref


def orbit_columns(source, signs):
    """One nonzero signed orbit sum per orbit, without any rank calculation."""
    seen = set()
    for word in sorted(source):
        if word in seen:
            continue
        orbit = {}
        for powers in product((0, 1), repeat=2):
            image, sign = word, 1
            for power, pair, eigenvalue in zip(powers, SWAPS, signs):
                if power:
                    image = relabel(image, pair)
                    sign *= eigenvalue
            seen.add(image)
            axpy(orbit, sign, {image: 1})
        if orbit:
            yield orbit


def inactive_columns(source, signs):
    for orbit in orbit_columns((w for w in source if w[-1] != 9), signs):
        image = {}
        for word, coeff in orbit.items():
            axpy(image, coeff, kk(word))
        yield image


def quotient_key(interior, active):
    if interior not in active:
        return (0, interior)
    return (1, can((1, *interior)))


def rank(columns):
    return len(rref(columns))


def main():
    cuts[14] = cut((2, 2, 4), words)
    active = {w[1:-1] for w in words if w[-1] == 9}
    assert len(active) == 144
    records = []
    for signs in product((1, -1), repeat=2):
        # S_d is the inactive shuffle span. Its projection adds the two active
        # orientations for each target word and preserves all other rows.
        # The kernel on S_d is exactly the cancellation space in cut d.
        rows = {d: list(inactive_columns(source, signs)) for d, source in cuts.items()}
        rows["sum"] = rows[8] + rows[9]
        assert rank(rows["sum"] + rows[14]) == rank(rows["sum"]) == rank(rows[14])
        metrics = {}
        active_images = {}
        cancellation_images = {}
        for d, columns in rows.items():
            exterior = [{(0, key): c for key, c in column.items() if key not in active}
                        for column in columns]
            folded = []
            for column in columns:
                projected = {}
                for key, c in column.items():
                    axpy(projected, c, {quotient_key(key, active): 1})
                folded.append(projected)
            all_rank, outside_rank, folded_rank = map(rank, (columns, exterior, folded))
            active_images[d] = rref(combine(columns, coeffs) for coeffs in kernel(exterior))
            cancellation_images[d] = rref(combine(columns, coeffs) for coeffs in kernel(folded))
            assert len(active_images[d]) == all_rank - outside_rank
            assert len(cancellation_images[d]) == all_rank - folded_rank
            metrics[d] = dict(inactive_rank=all_rank, exterior_rank=outside_rank,
                              folded_rank=folded_rank,
                              active_rank=all_rank-outside_rank,
                              cancellation_rank=all_rank-folded_rank)
        # S_8 + S_9 equals S_14, but intersection with the active span need
        # not commute with that sum. Compute the middle space separately.
        joined = rref(active_images[8] + active_images[9])
        fold_rows = []
        for row in joined:
            folded = {}
            for key, coeff in row.items():
                axpy(folded, coeff, {quotient_key(key, active): 1})
            fold_rows.append(folded)
        middle_space = rref(combine(joined, coeffs) for coeffs in kernel(fold_rows))
        separate_space = rref(cancellation_images[8] + cancellation_images[9])
        middle = len(middle_space)
        separate = len(separate_space)
        assert metrics[2]["cancellation_rank"] == 0
        assert separate == metrics[8]["cancellation_rank"] + metrics[9]["cancellation_rank"]
        assert rank(separate_space + middle_space) == middle
        assert rank(middle_space + cancellation_images[14]) == len(cancellation_images[14])
        oriented_orbits = [{w[1:-1]: c for w, c in orbit.items()}
                           for orbit in orbit_columns((w for w in words if w[-1] == 9), signs)]
        paired_orbits = []
        for orbit in oriented_orbits:
            paired = {}
            for key, coeff in orbit.items():
                axpy(paired, coeff, {quotient_key(key, active): 1})
            paired_orbits.append(paired)
        chamber_cancellations = len(oriented_orbits) - rank(paired_orbits)
        records.append(dict(chamber_cancellations=chamber_cancellations, character="".join("+" if s == 1 else "-" for s in signs),
                            cuts=metrics, separate=separate, middle=middle,
                            union=metrics[14]["cancellation_rank"]))
    assert [(r["middle"]-r["separate"],r["union"]-r["middle"]) for r in records] == [
        (0,0), (1,0), (0,0), (0,1)]
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
