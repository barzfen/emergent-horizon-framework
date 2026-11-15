# EHF-CBB-CROSS-36 — Single-front activation disproves the two-front collision hypothesis

**Update (2026-11-13).** [CROSS-39](CROSS-39-equal-pair-ancestry.md) proves the matching lower bound for all `t` and corrects the global triple-freeness claim quoted below.

Date: 2026-11-11. Status: exact counterexample to a proposed proof mechanism; explicit construction; general optimality OPEN.

## Setup
The balanced cyclic family F_t=A(BC)^(t+2)(AC)^(t+1)(AB)^(t+1) has orientation sign string S_t=++(-+)^t-++(-+)^t-++(-+)^t-, length n=6t+9. Legal LR3 sign rewrites are -++- <-> +--+. By CROSS-35, triple-freeness is invariant and LR4 activation is equivalent to the presence of ++-++ or --+--.

## Counterexample to mandatory collision of two independently propagating fronts
For each t>=1, start with S_t and apply LR3 at **sign-window** start indices
```
2t+2, 2t, 2t-2, ..., 4.
```
There are t rewrites. Each subsequent window overlaps the previous one, creating a single contiguous ancestry chain. The final word contains ++-++ at sign index 0. Thus LR4 activation can result from one moving rewrite front reaching a pre-existing ++ pair. It is false that two independently initiated moving fronts must collide to activate LR4.

This is an explicit upper-bound construction, consistent with CROSS-31 (whose indices refer to vertex reversals, not sign windows). It does not prove that fewer than t LR3 rewrites are impossible by some different route.

## Finite checks
Exact sign-rewrite simulation for t=1..6:
t=1: [4] -> activation at sign indices 0,7
t=2: [6,4] -> activation at 0
t=3: [8,6,4] -> activation at 0
t=4: [10,8,6,4] -> activation at 0
t=5: [12,10,8,6,4] -> activation at 0
t=6: [14,12,10,8,6,4] -> activation at 0

## Reproducible Python
```python
def S(t):return '++'+'-+'*t+'-++'+'-+'*t+'-++'+'-+'*t+'-'
def rewrite(s,i):
 n=len(s);p=''.join(s[(i+j)%n] for j in range(4))
 assert p in ('-++-','+--+')
 v=list(s)
 for j,x in enumerate('+--+' if p=='-++-' else '-++-'):v[(i+j)%n]=x
 return ''.join(v)
for t in range(1,101):
 s=S(t)
 for i in range(2*t+2,3,-2):s=rewrite(s,i)
 assert s[:5]=='++-++'
print('Single-front witness checked through t=100')
```

## Next proof task
Construct a lower-bound certificate that accounts for all possible rewrites, not merely the exhibited chain. A candidate is a weighted transport potential on the alternating arc, but it must also handle alternative initial seeds, wraparound, and the other LR4 trigger --+--. A statement such as 'a front moves two edges per move' is not by itself a global lower bound. Exact escape depth e(F_t)=t is verified computationally for t<=12 and has an all-t upper bound, but the arbitrary-t lower bound remains unproved.
