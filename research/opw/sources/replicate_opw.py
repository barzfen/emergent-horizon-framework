"""Reconstructed shared machinery: canonical cycles and the Pi invariant.

Canonical form (per note S2.1): rotate so label 1 is at position 0; of the
two orientations, keep the one with c_1 < c_{n-1}.
Pi (per note S2.3): ordered pair (E, O) of even/odd-position label sets.
Chambers = Pi-fibers on canonical states (theorem candidate S4: these
coincide with preserve-world components at n=7,9,11).
"""
from itertools import permutations

def canon(seq):
    seq = list(seq)
    i = seq.index(1)
    a = tuple(seq[i:] + seq[:i])
    r = list(reversed(seq))
    j = r.index(1)
    b = tuple(r[j:] + r[:j])
    return a if a[1] < a[-1] else b

def Pi(c):
    return (frozenset(c[0::2]), frozenset(c[1::2]))

def canon_cycles(n):
    return [(1,) + p for p in permutations(range(2, n + 1)) if p[0] < p[-1]]

if __name__ == "__main__":
    from collections import Counter
    for n in (7, 8, 9):
        cyc = canon_cycles(n)
        ch = Counter(Pi(c) for c in cyc)
        sizes = sorted(ch.values(), reverse=True)
        print(f"n={n}: {len(cyc)} canonical states, {len(ch)} chambers; "
              f"size histogram head: {sizes[:8]}{'...' if len(sizes) > 8 else ''}")
