# EHF-CBB-CROSS-31 — Explicit all-t LR3 escape construction and parity invariant

Date: 2026-11-11. Status: constructive upper bound for arbitrary t; lower bound conjectural.

## Setup
F_t=A(BC)^(t+2)(AC)^(t+1)(AB)^(t+1), length n=6t+9. It is cyclically proper and exactly balanced for all t>=1. An LR3 reversal reverses three consecutive vertices at cyclic start index i, and the associated orientation-sign rule acts on four consecutive edges (i-1,i,i+1,i+2):
```
-++- <-> +--+
```
All other sign windows are ineligible for a nontrivial legal LR3 move.

## Explicit upper bound
From F_t, perform LR3 reversals at zero-indexed vertex starts
```
0, 2, 4, ..., 2t-2
```
There are exactly t moves. The first operation uses the cyclic sign window at edges n-1,0,1,2. Subsequent operations use the -++- window generated at the advancing front. Every move is legal and preserves balance. After the last operation, an LR4 move is legal at vertex start 2t+1 (for t>=2; for t=1 there are legal LR4 starts 3 and 11). This can be checked symbolically from the alternating-block construction and the LR3 local rewrite, without a finite-size hypothesis. Thus e(F_t)<=t for all t>=1.

## New LR3 invariant: even/odd defect counts
In a sign word of even length, every -++- <-> +--+ operation has one negative sign at an even edge index and one at an odd edge index on each side, hence the counts of negatives on even and odd indices are separately invariant under LR3. **Caution:** n=6t+9 is odd! Cyclic wraparound changes parity labels, so this is NOT a globally well-defined invariant for F_t. In particular, no parity-based lower bound may be asserted for the odd-length family. The correct unconditional LR3 invariant is total negative count D (equivalently winding W). This parity observation may be relevant to even-length cycles only.

## Computational checks of the explicit sequence
t=1,2,3,4,5,8,15 all succeed with exactly t LR3 moves and then at least one legal LR4 move. CROSS-30 exhaustive BFS established e(F_t)=t for t=1..8. The explicit sequence establishes an all-t upper bound, NOT optimality.

## Reproduction
```python
def rev(w,k,i):
 n=len(w);ix=[(i+j)%n for j in range(k)];v=list(w)
 for a,b in zip(ix,reversed([w[j] for j in ix])):v[a]=b
 return ''.join(v)
def proper(w):
 return all(w[i]!=w[(i+1)%len(w)] for i in range(len(w)))
def legal_moves(w,k):
 return [i for i in range(len(w)) if (v:=rev(w,k,i))!=w and proper(v)]
for t in range(1,101):
 w='A'+'BC'*(t+2)+'AC'*(t+1)+'AB'*(t+1)
 assert proper(w) and all(w.count(c)==2*t+3 for c in 'ABC')
 assert not legal_moves(w,4)
 for i in range(0,2*t,2):
  v=rev(w,3,i)
  assert v!=w and proper(v)
  w=v
 assert legal_moves(w,4)
 assert (2*t+1) in legal_moves(w,4) if t>=2 else True
print('Constructive sequence checked through t=100')
```

## Important remaining gap
To establish e(F_t)=t for arbitrary t, prove every LR3-only sequence of length <t leaves F_t LR4-frozen. The exhibited t-move sequence is only an upper bound. A naive argument that defects can move only one edge per LR3 is not enough because moves may occur at multiple interfaces; an invariant must cover *all* possible choices of legal LR3 moves and cyclic wraparound.

## Next
Develop a combinatorial lower-bound certificate from the LR3-only rewrite graph, potentially a defect-pair transport metric or an admissible-pattern distance that is 1-Lipschitz under every LR3 operation and zero exactly at LR4-active configurations.
