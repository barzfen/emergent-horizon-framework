"""Compress the nine-point lift equations using two-term exterior rows."""
import argparse
from collections import defaultdict
from itertools import product
import json

from boundary import SWAPS, relabel
from branches import kernel
from probe import combine, cut, cuts, words
from reconstruct import axpy, rref
from shuffle_sectors import inactive_columns, orbit_columns, quotient_key

ACTIVE = {w[1:-1] for w in words if w[-1] == 9}


def exterior(column):
    return {k: v for k, v in column.items() if k not in ACTIVE}


def fold(column):
    out = {}
    for k, v in column.items():
        axpy(out, v, {quotient_key(k, ACTIVE): 1})
    return out


def compress(columns):
    rows = defaultdict(list)
    for j, column in enumerate(columns):
        for k, v in exterior(column).items():
            rows[k].append((j, v))
    edges = defaultdict(list)
    forced = set()
    for row in rows.values():
        if len(row) == 1:
            forced.add(row[0][0])
        if len(row) == 2:
            (i, a), (j, b) = row
            edges[i].append((j, -a/b))
            edges[j].append((i, -b/a))

    seen, bundles, killed = set(), [], 0
    for j in range(len(columns)):
        if j in seen:
            continue
        bundle = {j: 1}
        pending = [j]
        inconsistent = False
        while pending:
            i = pending.pop()
            for k, factor in edges[i]:
                expected = bundle[i] * factor
                if k not in bundle:
                    bundle[k] = expected
                    pending.append(k)
                elif bundle[k] != expected:
                    inconsistent = True
        seen.update(bundle)
        if inconsistent or forced.intersection(bundle):
            killed += len(bundle)
        else:
            bundles.append(bundle)
    return [combine(columns, b) for b in bundles], bundles, killed


def active_images(columns):
    return rref(combine(columns, v) for v in kernel(map(exterior, columns)))


def examine(source, signs, reduced):
    columns = list(inactive_columns(source, signs))
    smaller, bundles, killed = compress(columns) if reduced else (columns, [], 0)
    active = active_images(smaller)
    return active, dict(source_columns=len(columns), bundle_variables=len(smaller),
                        forced_zero_columns=killed, active=len(active),
                        transmitted=len(rref(map(fold, active))),
                        largest_bundle=max(map(len, bundles), default=0))


def audit(sources, reduced):
    result = {}
    for signs in product((1, -1), repeat=2):
        character = ''.join('+' if sign == 1 else '-' for sign in signs)
        images, info = {}, {}
        for name, source in sources.items():
            images[name], info[name] = examine(source, signs, reduced)
        joined = rref(images['left'] + images['right'])
        assert len(rref(joined + images['union'])) == len(images['union'])
        left, right, union = (info[k] for k in ('left', 'right', 'union'))
        joined_folded = len(rref(map(fold, joined)))
        result[character] = dict(cuts=info,
            extra_shared=left['transmitted'] + right['transmitted'] - joined_folded
                         - (left['active'] + right['active'] - len(joined)),
            extra_union_cancel=union['active'] - len(joined)
                               - (union['transmitted'] - joined_folded))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--scan', action='store_true')
    args = parser.parse_args()
    left, right, union = map(set, (cuts[8], cuts[9], cut((2, 2, 4), words)))
    # Holdout chosen by a fixed ordering before evaluating its ranks.
    orbit = set(next(orbit_columns((w for w in right-left if w[-1] != 9), (1,1))))
    assert all({relabel(w, pair) for w in orbit} == orbit for pair in SWAPS)
    cases = {'original': dict(left=left, right=right, union=union),
             'holdout': dict(left=left, right=right-orbit, union=union-orbit)}
    if args.scan:
        scan = []
        for name, branch, other in (('left', left, right), ('right', right, left)):
            for orbit in orbit_columns((w for w in branch-other if w[-1] != 9), (1,1)):
                removed = set(orbit)
                modified = dict(left=left, right=right, union=union-removed)
                modified[name] = branch-removed
                scan.append(dict(branch=name, removed=sorted(removed),
                                 characters=audit(modified, not args.verify)))
        print(json.dumps(scan, indent=2))
        return
    print(json.dumps(dict(method='unreduced' if args.verify else 'support_reduced',
                          holdout_removed=sorted(orbit),
                          cases={k: audit(v, not args.verify) for k, v in cases.items()}),
                     indent=2))


if __name__ == '__main__':
    main()
