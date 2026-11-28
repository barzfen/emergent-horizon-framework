# EHF-CBB-CROSS-22 — Defect arrangement and upward-trapped components

Date: 2026-11-11 AEST. Status: local exact rewrite characterization and finite exhaustive classification, not a global connectivity proof.

## Sign representation and elimination criterion
For proper cyclic colours c_i in Z/3, s_i=+ if c_{i+1}-c_i=+1 mod3, otherwise -. Let D=#negative signs, n=3m, W=(n-2D)/3=m-2D/3. Closure requires D divisible by 3. A proper LR4 can increase W by 2 precisely when the five-edge sign window is one of the following seven patterns (each has 3, 4 or 5 negative signs):
```
----- -> -+++-
----+ -> -++++
---+- -> +-+++
--+-- -> ++-++
-+--- -> +++-+
+---- -> ++++-
+---+ -> +++++
```
These are the exact local legal LR4 upward rewrites. LR3 changes `-++- <-> +--+` and preserves D. In a balanced proper colour word, the vertex reversals preserve colour counts automatically. Conversely, a free sign-word rewrite calculation must still respect closure, starting phase, and colour balance.

## New exhaustive trap stratification
An upward-trapped LR3 component at W=a<m is a component having no LR4 increasing W from any member. Enumerate all balanced proper position-indexed colour words, then LR3 components. Results:
| n | words | LR3 components | trapped components by W (component sizes in parentheses) |
| 6 | 24 | 24 | none |
| 9 | 132 | 78 | W=1: 9 of size 4 |
| 12 | 804 | 342 | W=2: 12 of size 1, 36 of size 3 |
| 15 | 5196 | 1656 | W=1: 15 of size 29; W=3: 45 each of sizes 1,2,3 |
| 18 | 34872 | 8610 | W=2: 18 of size 1, 54 each of sizes 5,13,15,19, and 9 of size 18; W=4: 126 of size 1, 108 of size 2, 54 of size 3 |

These results show traps at D=3 and D=6 in larger tested cycles; a classification based on only one triple of negative signs is insufficient. All observed traps have positive winding, but the finite result does not establish a theorem that nonpositive winding never traps.

## Exact enumeration code
```python
from collections import Counter
for m in range(2,7):
 n=3*m; words=[]
 def rec(w,c):
  if len(w)==n:
   if w[-1]!=w[0]:words.append(tuple(w))
   return
  for x in range(3):
   if c[x]<m and (not w or w[-1]!=x):
    c[x]+=1;w.append(x);rec(w,c);w.pop();c[x]-=1
 rec([],[0]*3); S=set(words)
 def W(w):
  return sum(1 if (w[(i+1)%n]-w[i])%3==1 else -1 for i in range(n))//3
 def nei(w,k):
  for i in range(n):
   ix=[(i+j)%n for j in range(k)];v=list(w)
   for a,b in zip(ix,reversed([w[t] for t in ix])):v[a]=b
   v=tuple(v)
   if v!=w and v in S:yield v
 seen=set();traps=Counter();comps=0
 for w in words:
  if w in seen:continue
  comps+=1;stack=[w];seen.add(w);comp=[]
  while stack:
   u=stack.pop();comp.append(u)
   for v in nei(u,3):
    if v not in seen:seen.add(v);stack.append(v)
  a=W(w)
  if a<m and not any(W(v)>a for u in comp for v in nei(u,4)):
   traps[(a,len(comp))]+=1
 print(n,len(words),comps,dict(sorted(traps.items())))
```

## Implications
An LR4 elimination needs a suitable five-edge window, not merely D>=3. LR3 can rearrange signs at fixed D, but there are entire LR3 components without an elimination window. At n>=15, trapped components occur also at D=6. Thus a universal repair lemma must handle interactions between multiple defect triples and may need temporary D increases by 3. This remains a conjectural normalization strategy, not a proof.

## Next
Represent a sign configuration as a cyclic ordered list of negative-edge positions or positive gap lengths. Determine exact LR3-induced transformations on gaps and classify LR4-eliminable gap motifs. Seek a well-founded potential for repeated detour repairs.
