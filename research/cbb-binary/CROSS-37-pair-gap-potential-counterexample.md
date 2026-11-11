# EHF-CBB-CROSS-37 — Failure of naive pair-gap transport potential

Date: 2026-11-11. Status: explicit finite counterexamples to candidate progress measures; general lower-bound theorem remains open.

## Setup
For t>=1, F_t=A(BC)^(t+2)(AC)^(t+1)(AB)^(t+1), orientation sign word S_t=++(-+)^t-++(-+)^t-++(-+)^t-. LR3 sign rewrites are -++- <-> +--+. Triple-freeness is invariant (CROSS-35); within that class LR4 activates exactly when ++-++ or --+-- occurs.

## Candidate and counterexample
Let P(s) be the set of cyclic starts i for which s_i=s_(i+1)=+. Define g(s) as the smallest positive cyclic difference between distinct starts in P(s), if there are at least two such starts.

Initially P(S_t)={0,2t+3,4t+6}, so g(S_t)=2t+3. However, an LR3 move at sign-window index 2t+2 produces a state with g=4 for t>=2. Thus a *single* move changes g by 2t-1. The gap statistic is not uniformly Lipschitz, and cannot directly certify e(F_t)>=t. The initial configuration's nearest ++ pairs can be newly created by a local rewrite, so the notion of pair identity is not conserved.

Exact checks:
| t | n | initial g | g after one suitable LR3 |
| 2 | 21 | 7 | 4 |
| 3 | 27 | 9 | 4 |
| 4 | 33 | 11 | 4 |
| 5 | 39 | 13 | 4 |
| 6 | 45 | 15 | 4 |

This counterexample also defeats any simple potential proportional to the *unlabelled* minimum ++ pair separation.

## What survives
Activation ++-++ requires two ++ pair starts separated by exactly three indices, with the correct intervening sign. A separation of four does not itself activate LR4, and the time to create the precise pattern can remain long even after g has collapsed. A successful transport potential must track context/ancestry or a weighted multi-site configuration, rather than only a scalar nearest-pair gap.

## Reproducible test
```python
def S(t):return '++'+'-+'*t+'-++'+'-+'*t+'-++'+'-+'*t+'-'
def rewrite(s,i):
 n=len(s);p=''.join(s[(i+j)%n] for j in range(4))
 assert p in ('-++-','+--+')
 v=list(s);q='+--+' if p=='-++-' else '-++-'
 for j,c in enumerate(q):v[(i+j)%n]=c
 return ''.join(v)
def g(s):
 n=len(s);p=[i for i in range(n) if s[i]==s[(i+1)%n]=='+']
 return min((b-a)%n for a in p for b in p if a!=b)
for t in range(2,7):
 s=S(t);u=rewrite(s,2*t+2)
 print(t,len(s),g(s),g(u))
 assert g(s)==2*t+3 and g(u)==4
```

## A mathematically valid but nonconstructive benchmark
For a fixed n and fixed winding/defect sector, define h(s) to be the shortest LR3 distance from s to the set of LR4-active states, with h(s)=infinity if unreachable. Whenever finite, h is 1-Lipschitz along every LR3 edge by the triangle inequality. This *graph distance* is a rigorous potential, but its value at S_t is exactly the desired theorem; it does not prove the t-step lower bound or provide a local formula.

## Next
Search for a context-aware invariant using marked ancestry of original ++ pairs or a finite-state weighted transducer that assigns costs to local rewrite histories. A useful certificate must lower-bound the first appearance of either ++-++ or --+-- for all legal LR3 sequences, including cyclic wraparound and concurrent fronts. The previously verified e(F_t)=t for t<=12 and the constructive all-t upper bound are unchanged.
