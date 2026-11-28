# EHF-CBB-CROSS-24 — LR4 defect reactions and a complete gap-space repair

Date: 2026-11-11. Status: exact local algebra; explicit verified finite certificate. General normalization remains open.

## Orientation and gap encoding
Encode A,B,C as 0,1,2. On cyclic edge i define s_i=+ if c_(i+1)-c_i=1 mod3 and - otherwise. A negative edge is a defect. If D>0, the cyclic gap vector lists counts of positive edges between successive negative edges. Sum gaps=n-D. D is divisible by 3 for a closed three-colour cycle; balanced colour populations impose additional constraints.

## Exhaustive LR4 local reactions
For a reversal of four vertices, inspect the five surrounding oriented edges. Enumerating all proper colour neighbourhoods gives exactly seven reversible nontrivial pairs. The direction shown eliminates three defects:
```
----- -> -+++-
----+ -> -++++
---+- -> +-+++
--+-- -> ++-++
-+--- -> +++-+
+---- -> ++++-
+---+ -> +++++
```
Every arrow changes D by -3 and W by +2, and the reverse creates three defects. This is a *local* rewrite list: to compute the complete gap-vector transformation, replace the specified five-sign window in the full cyclic sign word, then recalculate gaps. A fixed small-gap rewrite independent of the external surrounding gaps is generally insufficient.

## Exact three-step repair of an upward trap at n=9
All indices below are zero-based cyclic vertex reversal starts.
```
step  colour word  sign word   gaps                  D   W
0     ACABABCBC    -++-++-++   (2,2,2)               3  +1
1     ACBABACBC    ---+---++   (0,0,1,0,0,2)         6  -1   LR4 start 2
2     ABCABACBC    ++++---++   (0,0,6)               3  +1   LR4 start 0
3     ABCABCABC    +++++++++   ()                    0  +3   LR4 start 4
```
This path realizes a defect-count trajectory 3 -> 6 -> 3 -> 0, and winding +1 -> -1 -> +1 -> +3. Every word is balanced (three of each colour) and proper cyclically. Its initial LR3 component has no upward LR4 exit, so a winding decrease is necessary before reaching W=3. The three-step path is shortest because a single LR4 must lower W first and every LR4 changes W by exactly 2.

## Reproducible local and path checks
```python
from itertools import product
def signs(w):
 n=len(w)
 return ''.join('+' if (w[(i+1)%n]-w[i])%3==1 else '-' for i in range(n))
def reverse(w,k,i):
 n=len(w); ix=[(i+j)%n for j in range(k)]
 v=list(w)
 for a,b in zip(ix,reversed([w[t] for t in ix])):v[a]=b
 return tuple(v)
def proper(w):
 return all(w[i]!=w[(i+1)%len(w)] for i in range(len(w)))
def gaps(s):
 n=len(s);p=[i for i,c in enumerate(s) if c=='-']
 return tuple((p[(j+1)%len(p)]-p[j]-1)%n for j in range(len(p))) if p else ()
w=tuple('ABC'.index(x) for x in 'ACABABCBC')
expected=[('ACABABCBC','-++-++-++',(2,2,2)),('ACBABACBC','---+---++',(0,0,1,0,0,2)),('ABCABACBC','++++---++',(0,0,6)),('ABCABCABC','+++++++++',())]
for j,(word,s,g) in enumerate(expected):
 assert ''.join('ABC'[x] for x in w)==word
 assert signs(w)==s and gaps(s)==g
 assert proper(w) and all(w.count(x)==3 for x in range(3))
 if j<3:w=reverse(w,4,[2,0,4][j])
pairs={}
for a in product(range(3),repeat=6):
 if any(a[i]==a[i+1] for i in range(5)):continue
 b=(a[0],)+tuple(reversed(a[1:-1]))+(a[-1],)
 if any(b[i]==b[i+1] for i in range(5)):continue
 def sg(t):return ''.join('+' if (t[i+1]-t[i])%3==1 else '-' for i in range(5))
 if sg(a)!=sg(b):pairs[sg(a)]=sg(b)
assert len(pairs)==14
assert all(pairs[v]==k for k,v in pairs.items())
print('Local LR4 rule list and explicit gap repair verified')
```

## Interpretation
LR4 can change both the number and arrangement of orientation defects. The example demonstrates a finite create–rearrange–annihilate path with one downward winding excursion, but does not prove that every balanced proper cyclic word admits a similar repair, or that winding excursions are uniformly bounded. The physical analogy is not an empirical physics claim.

## Next
Find a formal gap-vector macro-move, track how it changes an ordering/spacing potential, and prove a terminating normalization algorithm while preserving balance and admissibility.
