"""EHF-DIM-09: exhaustive family-level check of general ordered-label theorem.
Pure Python. Checks n=5,7,9,11; n=11 has 14,400 states.
"""
from itertools import permutations
from collections import Counter
from math import factorial

def canonical(c):
    c=list(c);k=c.index(0);c=c[k:]+c[:k]
    return min(tuple(c),(0,)+tuple(reversed(c[1:])))

def lr3(c,start):
    a=list(c);n=len(a)
    ids=[(start+j)%n for j in range(3)]
    vals=[a[i] for i in ids][::-1]
    for i,v in zip(ids,vals):a[i]=v
    return canonical(a)

for m in (2,3,4,5):
    n=2*m+1
    odd_labels=tuple(range(1,m+1))
    even_labels=tuple(range(m+1,n))
    family=set()
    for o in permutations(odd_labels):
        for e in permutations(even_labels):
            family.add((0,)+tuple(v for pair in zip(o,e) for v in pair))
    assert len(family)==factorial(m)**2
    degree_counts=Counter()
    for c in family:
        assert canonical(c)==c
        pi=set(c[::2])
        admissible={lr3(c,k) for k in range(n)
                    if set(lr3(c,k)[::2])==pi and lr3(c,k)!=c}
        interior={lr3(c,k) for k in range(1,n-2)}
        assert admissible==interior
        assert admissible<=family
        assert len(interior)==2*(m-1)
        degree_counts[len(admissible)]+=1
    assert degree_counts=={2*(m-1):factorial(m)**2}
    print(f'PASS n={n}, states={len(family)}, degree={2*(m-1)}, predicted diameter={m*(m-1)}')
print('PASS all finite family audits')
