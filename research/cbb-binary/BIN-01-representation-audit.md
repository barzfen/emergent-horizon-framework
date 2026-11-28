# EHF-CBB-BIN-01 — Representation audit

Status: exact elementary mathematical findings; no physical claims. Date: 2026-11-10.

## Definitions
Let H_n be labelled undirected Hamiltonian cycles on [n] modulo rotation and reversal, n>=3. Let B_n={(C,b):C in H_n, b:E(C)->F_2, sum_{e in E(C)} b(e)=0}. A binary vertex potential s:V(C)->F_2 gives b(uv)=s(u)+s(v); potentials s and s+1 give the same b.

## Proposition 1 (fibre count)
For each C, there are 2^(n-1) admissible edge-bit decorations. Proof: choose n-1 edge bits freely; the final bit is uniquely determined by XOR closure. Thus |B_n|=(n-1)! 2^(n-2) for n>=3. The projection p:B_n->H_n is many-to-one and not an isomorphism of state sets.

n | |H_n| | |B_n|
3 | 1 | 4
4 | 3 | 24
5 | 12 | 192
6 | 60 | 1920
7 | 360 | 23040
8 | 2520 | 322560

## Proposition 2 (natural equivariant binary decorations are uniform)
Suppose f assigns to each uncoloured labelled Hamiltonian cycle C a binary edge decoration f(C), and f is equivariant under **every permutation of vertex labels**: f(sigma C)=sigma f(C). Every cycle has dihedral automorphisms (permutations of its vertices preserving its edge set), and these act transitively on its edges. Therefore f(C) must have the same bit a on every edge. XOR closure requires n*a=0 in F_2. Hence:
- odd n: only the all-zero edge assignment;
- even n: either all-zero or all-one edge assignment.
Because the symmetric group acts transitively on H_n, a chosen uniform assignment cannot depend on which labelled cycle C is presented (though it may depend on n).
This does **not** prohibit non-equivariant encodings, encodings using distinguished roots/labels/ambient structures, or richer binary encodings; it limits natural edge decorations derived from a bare unrooted cycle.

## Proposition 3 (growth-compatible equivariant sections)
Let insertion replace edge bit b by x,y with x+y=b in F_2. For a uniform-bit section f_n(C)=a_n on all n edges, requiring **every** lifted insertion of f_n(C) to equal f_{n+1}(I_e C) would imply both unchanged edges have bit a_{n+1}=a_n and the two replacement edges have bit a_{n+1}, hence 2a_{n+1}=a_n. For n>=3 this forces a_n=0 and a_{n+1}=0. Thus the all-zero decoration is the only fully symmetric all-slot insertion-compatible uniform section. This is a *section* (faithful embedding into decorated states) but does not encode new intrinsic cycle information.

## Interpretation and next tests
The elementary XOR edge-potential construction is a binary **extension** of CBB, not a nontrivial intrinsic encoding. The only canonical all-slot-compatible edge-bit section under full relabelling symmetry is trivial. A promising next direction is to add explicitly specified structure (growth history, a rooted insertion edge, an ambient graph, or an LR3 move) and ask whether a nontrivial binary observable is induced, while retaining symmetry equivariance with respect to the appropriate smaller symmetry group.

Do not equate this obstruction with a theorem about all conceivable binary encodings. LR3 sector parity remains to be tested against its exact original definition.
