# EHF-CBB-CROSS-35 — Triple-free LR3 invariant and reduction to two LR4 triggers

Date: 2026-11-11. Status: proved invariant for arbitrary proper cyclic three-colour words under LR3; finite BFS observations for the frozen family; general escape-depth lower bound remains open.

## Exact setting
A proper cyclic three-colour word has orientation signs + and -. Legal nontrivial LR3 reversals act on four consecutive cyclic edge signs by -++- <-> +--+. Legal LR4 reversals correspond to 14 five-sign patterns:
```
----- ----+ ---+- --+-- -+--- +---- +---+
-+++- -++++ +-+++ ++-++ +++-+ ++++- +++++
```

## Theorem: triple-freeness is LR3-invariant
Define a cyclic sign word to be *triple-free* if it contains neither +++ nor --- in any three consecutive cyclic positions.

**Claim.** If a cyclic sign word of length at least six is triple-free, every legal LR3 rewrite produces another triple-free sign word.

**Proof.** The two replacement blocks -++- and +--+ are each triple-free internally. The only possible newly created triples must cross a boundary of the four-sign replacement. Write a and b for the immediately preceding and succeeding signs. If the original block is -++-, the new block is +--+. A triple crossing the left boundary would require a++ at the start of the replacement, but the replacement starts +-, not ++. A triple crossing the right boundary would require ++b at its end, but the replacement ends -+, not ++. For the inverse replacement, the new block -++- begins -+ and ends +-, so again no triple can cross either boundary. All other triples are unchanged. Therefore triple-freeness is preserved. (The boundary checks are valid cyclically, including wraparound.)

Equivalently, for each direction and each a,b in {+,-}, if a(original)b is triple-free then a(replacement)b is triple-free; in fact, neither replacement can create a boundary triple for any a,b.

## Corollary: only two LR4 triggers remain
Of the fourteen LR4-active five-sign patterns, exactly twelve contain +++ or ---. The remaining two are
```
++-++
--+--
```
Thus for any triple-free LR3-reachable configuration, LR4 is active if and only if the cyclic sign word contains ++-++ or --+--.

This is an exact necessary-and-sufficient criterion **within the triple-free class**, not a characterization of all LR4-active words.

## Application to the frozen family
For t>=1,
```
F_t = A(BC)^(t+2)(AC)^(t+1)(AB)^(t+1)
S_t = ++(-+)^t-++(-+)^t-++(-+)^t-
```
is cyclically triple-free. Therefore every LR3-only descendant is triple-free. To prove the conjectured escape-depth lower bound e(F_t)>=t, it suffices to show neither ++-++ nor --+-- can appear in fewer than t LR3 moves.

## Finite check of first-activation types
A breadth-first search in sign space for t=1..6 shows the first LR4-active configurations occur at depth t and all first-activation windows are of type ++-++. Counts of first-activation windows across distinct first-active states at depth t are 6,9,12,15,18,21 for t=1..6, respectively. These are finite observations, not proof that --+-- is globally unreachable or cannot appear first at larger t.

## Reproduction
```python
from itertools import product
bad={'-----','----+','---+-','--+--','-+---','+----','+---+',
     '-+++-','-++++','+-+++','++-++','+++-+','++++-','+++++'}
assert {p for p in bad if '+++' not in p and '---' not in p} == {'++-++','--+--'}
for before,after in [('-++-','+--+'),('+--+','-++-')]:
 for a,b in product('+-',repeat=2):
  x=a+before+b;y=a+after+b
  if '+++' not in x and '---' not in x:
   assert '+++' not in y and '---' not in y
print('All boundary contexts verified; two surviving LR4 triggers.')
```

## Remaining challenge
Find a combinatorial metric or propagation argument that bounds the earliest possible creation of either ++-++ or --+-- in S_t under arbitrary sequences of -++- <-> +--+. The new invariant removes triple-run possibilities but does not by itself prove the t-step lower bound.
