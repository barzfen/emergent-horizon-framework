# EHF-CBB-CROSS-38 — Cyclic defect dipole conservation and transport lower bounds

Date: 2026-11-12. Status: exact general LR3 invariant proved. Sharp escape-depth lower bound remains open.

## Definitions
A proper cyclic three-colour word of length n has sign s_i=+ for colour increment +1 mod3 and - otherwise. Define x_i=1 if s_i=-, and x_i=0 otherwise. LR3 sign rewrites are -++- <-> +--+, i.e. 1001 <-> 0110 in defect variables.

## Theorem 1: cyclic dipole conservation
Define D(x)=sum_i x_i and M(x)=sum_{i=0}^{n-1} i*x_i mod n.

Every legal LR3 move preserves D and M.

**Proof.** For a rewrite at cyclic edge-window start j, 1001 -> 0110 changes defect occupations by (-1,+1,+1,-1) at cyclic indices j,j+1,j+2,j+3. Hence delta D=0 and delta M=-j+(j+1)+(j+2)-(j+3)=0 mod n. The reverse move negates these changes. Reducing indices modulo n handles wraparound. QED.

This is a precise invariant for position-indexed sign words. A cyclic rotation of a word by k changes M by kD mod n (up to sign convention), so M is not automatically a rotation-invariant numerical label. Do not infer disconnected LR3 components solely from different values of M for rotated representatives.

## Polynomial form
Let X(z)=sum_i x_i z^i in Z[z]/(z^n-1). A nonwrapping forward rewrite has
delta X(z)=z^j(-1+z+z^2-z^3)=-z^j(1-z)(1-z^2).
The polynomial identity is valid modulo z^n-1 for wraparound. It exposes conservation of particle number and a first-moment congruence; ordinary derivatives at z=1 require care in the quotient because z^n-1 has nonzero derivative n at 1.

## Transport lower bound for any prescribed endpoint
Equip the cycle C_n with graph distance d_C. For two defect configurations x,y with the same number of defects, define the minimum matching cost T(x,y) by optimally matching the occupied positions of x to those of y, with cost d_C per pair. A single LR3 rewrite moves two defects one edge each (the other sites are empty), so T(x,x')<=2. By the triangle inequality, any LR3 path of length k from x to y satisfies T(x,y)<=2k, hence k>=ceil(T(x,y)/2).

For a target set A of LR4-active configurations in the same D and M sector, the rigorous general bound is
e(x)>=ceil( min_{y in A} T(x,y) / 2 ).
This is a valid *weighted transport potential*; it is not yet known whether its value for the family S_t grows as t. In particular, dropping LR3 reachability constraints when minimizing over A can make the bound weak. A proposed certificate must compute or lower-bound the target-set minimum, not assume it.

## Family and test
For F_t=A(BC)^(t+2)(AC)^(t+1)(AB)^(t+1), n=6t+9 and S_t=++(-+)^t-++(-+)^t-++(-+)^t-, D=3(t+1). The computed M mod n for t=1..8 is:
t=1:3, 2:15, 3:6, 4:24, 5:9, 6:33, 7:12, 8:42.
This sequence is diagnostic only; M conservation by itself does not establish the desired e(F_t)>=t.

## Reproducible code
```python
def S(t):return '++'+'-+'*t+'-++'+'-+'*t+'-++'+'-+'*t+'-'
def dipole(s):
 n=len(s)
 return sum(i for i,c in enumerate(s) if c=='-')%n
def lr3(s,j):
 n=len(s)
 p=''.join(s[(j+k)%n] for k in range(4))
 assert p in ('-++-','+--+')
 q='+--+' if p=='-++-' else '-++-'
 out=list(s)
 for k,c in enumerate(q):out[(j+k)%n]=c
 return ''.join(out)
for t in range(1,101):
 s=S(t);n=len(s)
 for j in range(n):
  p=''.join(s[(j+k)%n] for k in range(4))
  if p in ('-++-','+--+'):
   v=lr3(s,j)
   assert v.count('-')==s.count('-')
   assert dipole(v)==dipole(s)
print('All initially legal LR3 moves preserve dipole for t=1..100.')
```

## Open question
Can a finite-state weighted transducer or a constrained matching potential certify min_{LR4-active y in same LR3-reachable component} T(S_t,y)>=2t-1 for all t? This is NOT established; the unqualified minimum over active states may be too small. Explore local automaton certificates accounting for admissible LR3 histories rather than just endpoint defect positions.
