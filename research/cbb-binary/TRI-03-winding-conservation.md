# EHF-CBB-TRI-03 — Winding-number conservation under three-colour separation LR3

Date: 2026-11-10. Status: exact invariant and exhaustive finite checks.

## Setup
A cyclic word over A,B,C is separation-admissible when neighbouring colours differ. Identify A,B,C with residues 0,1,2 modulo 3. For an oriented word w define s_i=+1 when w_(i+1)-w_i=+1 mod 3 and s_i=-1 when the difference is -1 mod 3. Define W(w)=(sum_i s_i)/3. Because the sum of the colour differences is zero modulo 3, W is an integer. Rotation preserves W, reversal changes its sign; |W| is an invariant of undirected colour bracelets. Global permutation of colour names can change the sign but not its absolute value.

## Theorem: legal LR3 preserves W
An LR3 proposal replaces the local five-letter window (l,a,b,c,r) with (l,c,b,a,r), swapping a and c. Both words are separation-admissible only if the eight adjacency inequalities l!=a,a!=b,b!=c,c!=r,l!=c,c!=b,b!=a,a!=r hold. Under these conditions, the sum of the four oriented colour increments in the window is unchanged. One elementary proof is exhaustive over the 3^5=243 five-letter assignments: filter by those eight inequalities, then compute the four increments before and after; every valid case has difference zero. The local calculation is exhaustive and independent of n (for n>=5, where the five positions are distinct). All other edge increments are unchanged. Thus W is conserved by each legal LR3 step.

## Exact enumeration
For fixed balanced counts n=9 (3 each) and n=12 (4 each), enumerate all separation-admissible colour bracelets and their legal LR3 transitions. Results:
n=9: 8 bracelets, |W|=1 for 7 bracelets and |W|=3 for 1.
n=12: 41 bracelets, |W|=0 for 27 bracelets, |W|=2 for 13, |W|=4 for 1.
No legal LR3 transition changes |W| in either system.

The maximal winding configurations ABCABC... and its reverse have |W|=n/3 and are frozen: every LR3 proposal violates separation.

## Important limitation
Winding alone is **not** a complete invariant of connected components. At n=9 the 7 bracelets of |W|=1 split into four disconnected components (sizes 4,1,1,1). At n=12 the |W|=0 and |W|=2 bracelets each occupy multiple disconnected components. This establishes a genuine necessary sector label, not a full classification.

## Reproduction of local theorem
```python
from itertools import product
C='ABC'
def step(a,b):
    return 1 if (C.index(b)-C.index(a))%3==1 else -1
checked=0
for l,a,b,c,r in product(C,repeat=5):
    old=(l,a,b,c,r);new=(l,c,b,a,r)
    if any(x==y for x,y in zip(old,old[1:])):continue
    if any(x==y for x,y in zip(new,new[1:])):continue
    d=sum(step(x,y) for x,y in zip(new,new[1:]))-sum(step(x,y) for x,y in zip(old,old[1:]))
    assert d==0
    checked+=1
assert checked>0
print('legal local windows',checked)
```

## Interpretation and next test
Winding is a discrete combinatorial invariant of an oriented proper three-colouring of a cycle, not a derivation of SU(3) or a physical conservation law. Next derive additional invariants to classify the components *within* fixed winding sectors, and test whether analogous winding labels survive other allowed reversal lengths.
