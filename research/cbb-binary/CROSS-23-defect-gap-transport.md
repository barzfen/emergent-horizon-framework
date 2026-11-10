# EHF-CBB-CROSS-23 — Gap transport and a trapped defect triple

Date: 2026-11-11. Status: exact local derivation; finite n=9 certificate. No arbitrary-n connectivity theorem.

## Setup
A proper cyclic three-colour word has orientation signs s_i in {+,-}. Negative signs are orientation defects. Let D be their number. For D>0, write the cyclic gap vector (g_1,...,g_D), where g_j is the number of + signs between consecutive - signs, with sum g_j=n-D. Colour closure implies D is a multiple of 3, but not every such sign cycle represents a balanced colour word.

## Exact LR3 gap rule
The sole nontrivial LR3 orientation rewrite is
```
-++- <-> +--+
```
If the gap between the two affected consecutive negative signs is exactly 2, and the immediately preceding and succeeding defect gaps are a and b, then the gap rewrite is
```
(a,2,b) -> (a+1,0,b+1).
```
Its inverse is
```
(a,0,b) -> (a-1,2,b-1), provided a,b>=1.
```
For D>=3 these are three consecutive cyclic gaps. The sum of gaps and D are conserved, so winding W=(n-2D)/3 is conserved. This is a local pair-compression/expansion operation, not a generic free translation of an isolated defect.

## LR4 elimination when D=3
For a proper word with exactly three negative edges, an LR4 move that raises W by 2 must eliminate all three negatives. Among the seven exact five-sign upward LR4 patterns, only `+---+ -> +++++` has exactly three negatives. Therefore an upward LR4 move exists iff the three negatives form a contiguous cyclic run with positive signs immediately outside. For n>=6 and D=3 the outside signs are automatically positive if all three negatives are contiguous.

## Explicit trapped balanced nine-cycle
Take `ACABABCBC`, colour encoding (0,2,0,1,0,1,2,1,2). Its sign word is
```
-++-++-++
```
with cyclic gap vector (2,2,2), D=3 and W=+1. Exhaustively applying admissible LR3 reversals gives exactly four indexed colour words:
```
ACABABCBC  -++-++-++
ABACABCBC  +--+++-++
ACABCBABC  -+++--+++
BCABABCAC  +++-+++--
```
None has a cyclic run of three consecutive negative signs. Hence no member of this LR3 component admits an upward LR4 move to W=3. The obstruction is entirely visible in the gap geometry. This is a finite witness for the failure of monotone defect elimination, not a disconnected component of the LR3+LR4 graph.

## Reproducible verification
```python
from collections import deque
w=tuple('ABC'.index(x) for x in 'ACABABCBC');n=len(w)
def rev(u,k,i):
 ix=[(i+j)%n for j in range(k)];v=list(u)
 for a,b in zip(ix,reversed([u[t] for t in ix])):v[a]=b
 return tuple(v)
def proper(u):return all(u[i]!=u[(i+1)%n] for i in range(n))
def signs(u):
 return ''.join('+' if (u[(i+1)%n]-u[i])%3==1 else '-' for i in range(n))
Q=deque([w]);seen={w}
while Q:
 u=Q.popleft()
 for i in range(n):
  v=rev(u,3,i)
  if proper(v) and v not in seen:seen.add(v);Q.append(v)
assert len(seen)==4
for u in sorted(seen):
 assert '---' not in signs(u)+signs(u)[:2]
 assert not any(proper(rev(u,4,i)) and signs(rev(u,4,i)).count('-')==0 for i in range(n))
 print(''.join('ABC'[x] for x in u),signs(u))
```

## Interpretation and next question
LR3 reshuffles gap lengths locally; LR4 can eliminate a triple once the correct five-edge motif is present. The n=9 trap shows that LR3 alone need not assemble that motif. Next: derive the LR4-induced gap creation/annihilation rules and seek a defect-transport macro that uses one temporary triple creation and subsequently eliminates more defects than it created, with a rigorous termination potential. The physics analogy is mathematical only; no physical identification is established.
