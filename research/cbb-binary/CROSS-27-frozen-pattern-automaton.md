# EHF-CBB-CROSS-27 — Forbidden-pattern automaton and frozen configurations at n=21

Date: 2026-11-11. Status: exhaustive enumeration of *frozen sign words* through n=21 (not full configuration graph at n=21). No general connectivity theorem.

## Exact LR4 criterion
For proper cyclic three-colour words, an LR4 move is legal and nontrivial iff its five-edge orientation window is one of these 14 strings:
```
----- ----+ ---+- --+-- -+--- +---- +---+
-+++- -++++ +-+++ ++-++ +++-+ ++++- +++++
```
Therefore LR4-frozen cyclic sign words avoid all 14 windows. Their enumeration is a finite-type forbidden-word problem: use a 16-state automaton whose states are length-4 binary sign histories, retaining a transition only if the five-character concatenation is not forbidden. Cyclic walks of length n correspond to indexed cyclic sign sequences, with the standard cyclic closure condition.

## Enumeration, colour closure and balance
For a sign word s, reconstruct c_0=0 and c_(i+1)=c_i+1 mod3 for '+' or c_i-1 mod3 for '-'. The cyclic sign word is colour-closed iff #minus is divisible by 3 when n=3m. It is balanced iff each colour appears exactly m times. Each balanced sign word has exactly three global colour-phase lifts to indexed balanced colour words.

| n | LR4-frozen closed sign words | balanced frozen indexed colour words | defect counts among balanced frozen words |
| 6 | 14 | 0 | — |
| 9 | 0 | 0 | — |
| 12 | 126 | 0 | — |
| 15 | 10 | 30 | D=6:15, D=9:15 |
| 18 | 1238 | 0 | — |
| 21 | 350 | 168 | D=9:84, D=12:84 |

The closed sign-word counts include many sign words whose reconstructed colour word is NOT balanced. This distinction is essential.

## LR3 exits
Every balanced LR4-frozen indexed word at n=15 has exactly 3 nontrivial legal LR3 moves (30 words). At n=21, 126 words have exactly 5 legal LR3 moves and 42 words have exactly 3. Hence none of these frozen words is isolated in the combined LR3+LR4 graph. This does not establish that the LR3 moves necessarily lead to a region with an LR4 exit, nor that the combined graph is connected at n=21.

## Explicit n=21 example
Colour word: `ABCBCBCACACACABABABCB`
Sign word: `++-+-++-+-+-++-+-++--`
This is a balanced proper cyclic word with no legal LR4 moves.

## Reproducible Python
```python
from itertools import product
from collections import Counter
up=['-----','----+','---+-','--+--','-+---','+----','+---+']
dn=['-+++-','-++++','+-+++','++-++','+++-+','++++-','+++++']
bad=set(up+dn)
for n in (6,9,12,15,18,21):
 closed=0;balanced=Counter();lr3=Counter()
 for s in product('+-',repeat=n):
  if any(''.join(s[(i+j)%n] for j in range(5)) in bad for i in range(n)):continue
  if s.count('-')%3:continue
  closed+=1
  w=[0]
  for b in s[:-1]:w.append((w[-1]+(1 if b=='+' else -1))%3)
  if any(w.count(x)!=n//3 for x in range(3)):continue
  balanced[s.count('-')]+=3
  for phase in range(3):
   u=tuple((x+phase)%3 for x in w);count=0
   for i in range(n):
    ix=[(i+j)%n for j in range(3)];v=list(u)
    for a,b in zip(ix,reversed([u[t] for t in ix])):v[a]=b
    if tuple(v)!=u and all(v[j]!=v[(j+1)%n] for j in range(n)):count+=1
   lr3[count]+=1
 print(n,closed,sum(balanced.values()),dict(balanced),dict(lr3))
```

## Implications and next work
The 15-position LR4-only exception recurs at 21 positions, while n=18 has no balanced LR4-frozen words. The existence of LR3 exits suggests—but does not prove—escape from LR4 freezing. Next classify all cyclic forbidden-pattern sign words using the 16-state transfer graph, and test whether an LR3 exit always reaches an LR4-active state within bounded LR3 steps. Do not infer periodicity or a general formula from the finite sequence 0,0,0,30,0,168.
