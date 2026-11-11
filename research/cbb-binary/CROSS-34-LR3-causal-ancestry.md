# EHF-CBB-CROSS-34 — Causal ancestry for LR3 rewrites

Date: 2026-11-11. Status: proved elementary causal ancestry lemma; tested finite shortest paths; sharp arbitrary-t lower bound remains OPEN.

## Definitions

The balanced proper cyclic family is F_t=A(BC)^(t+2)(AC)^(t+1)(AB)^(t+1), with n=6t+9. Its orientation sign word is S_t=++(-+)^t-++(-+)^t-++(-+)^t-. A legal LR3 move replaces a cyclic four-edge window -++- by +--+ or conversely. Every one of its four signs changes. A legal LR4 move exists iff a five-edge sign window belongs to the fourteen patterns recorded in CROSS-28.

The only initially LR3-eligible sign windows in S_t have starts 2t+2, 4t+5, and 6t+8, separated cyclically by 2t+3 positions.

## Lemma (new eligibility has ancestry)

Let s^(0),s^(1),...,s^(k) be any legal LR3 sequence. If a particular four-edge window at index i is LR3-ineligible in s^(0) but becomes eligible in s^(k), then some earlier LR3 move has changed at least one sign of that window. In particular, the window overlaps the four-edge support of an earlier move.

**Proof:** If none of the four signs in the window had ever changed, the four-sign word at i would be identical to its initial ineligible value. Contradiction.

A stronger inductive formulation: for any move at time j, either its window was initially eligible or it overlaps the support of some earlier move. This follows by applying the lemma to the window just before move j. By recursively following earlier overlapping moves, every noninitial rewrite has an overlap-dependency chain to one of the three initially eligible sites. This is a causal ancestry statement, not a speed-optimality theorem.

## Elementary geometric bound

Two length-four cyclic windows that overlap have starting indices at cyclic distance at most 3 (for n>=15). Thus an overlap-dependency chain of r moves can displace its window start from an initial seed by at most 3r edges along the chain. This is a coarse finite-speed bound. It is **insufficient** to establish the desired t-move LR4 activation lower bound because a five-edge LR4 window may be activated by changes near one front and different chains may interact. In particular, it would be invalid to assert that activation requires two fronts to meet without separately proving that isolated-front dynamics cannot activate LR4.

## Independent finite check

Sign-space BFS confirms the first LR4-active depth for t=1..6 equals t, with exact breadth-first layer sizes through the first activation:

| t | n | layers 0..t | first LR4-active depth |
|---|---|---|---|
| 1 | 15 | 1,3 | 1 |
| 2 | 21 | 1,3,9 | 2 |
| 3 | 27 | 1,3,9,22 | 3 |
| 4 | 33 | 1,3,9,22,51 | 4 |
| 5 | 39 | 1,3,9,22,51,108 | 5 |
| 6 | 45 | 1,3,9,22,51,108,221 | 6 |

For t=2..5, one shortest witness in zero-indexed **sign-window** starts is [2t+2, 2t, ..., 4]; these moves are distinct from the zero-indexed **vertex** reversal starts 0,2,...,2t-2 of CROSS-31. They should not be conflated.

## Reproduction

```python
from collections import deque,Counter
bad={'-----','----+','---+-','--+--','-+---','+----','+---+',
     '-+++-','-++++','+-+++','++-++','+++-+','++++-','+++++'}
def S(t):return '++'+'-+'*t+'-++'+'-+'*t+'-++'+'-+'*t+'-'
def moves(s):
 n=len(s)
 for i in range(n):
  p=''.join(s[(i+j)%n] for j in range(4))
  if p not in ('-++-','+--+'):continue
  v=list(s)
  for j,x in enumerate('+--+' if p=='-++-' else '-++-'):v[(i+j)%n]=x
  yield i,''.join(v)
def active(s):
 n=len(s)
 return any(''.join(s[(i+j)%n] for j in range(5)) in bad for i in range(n))
for t in range(1,7):
 s=S(t);q=deque([(s,0)]);seen={s};hist=Counter();first=None
 assert [i for i,_ in moves(s)]==[2*t+2,4*t+5,6*t+8]
 while q:
  u,d=q.popleft();hist[d]+=1
  if active(u):
   if first is None:first=d
   continue
  if d>=t:continue
  for i,v in moves(u):
   if v not in seen:seen.add(v);q.append((v,d+1))
 assert first==t
 print(t,len(s),dict(sorted(hist.items())))
```

## Missing proof obligation

Prove for all t and every sequence of fewer than t LR3 rewrites from S_t that none of the fourteen LR4-active five-edge windows appears. The ancestry lemma is a necessary preliminary but not sufficient. A promising next direction is to classify the LR3 dynamics within one alternating arc under a limited move budget, then show that creating an LR4 window requires exhausting an arc or coupling two fronts. No arbitrary-t escape-distance theorem is claimed.
