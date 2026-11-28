# EHF-HC-RAW-13 — Graded HC Compatibility / Naturality Audit
 EHF-HC-RAW-13 — Graded HC Compatibility / Naturality Audit

## 342.1 Purpose

RAW-12 added a new foundational distinction:

- static fixed-\(n\) Hamilton-cycle comparison geometry;
- graded one-atom substrate growth.

That addition changes the symmetry bookkeeping.

At a fixed layer:

\[
HC_n
\]

still has full relabelling covariance under:

\[
S_n.
\]

But a chosen singleton tower:

\[
V_1\subset V_2\subset\cdots\subset V_N
\]

has a unique first-appearance stage for every atom and therefore has trivial atom-level self-automorphism.

RAW-13 asks whether these facts are compatible and whether all previously certified constructions commute correctly with isomorphisms of graded towers.

The answer is:

\[
\boxed{\textbf{yes}.}
\]

No contradiction was found.

The tower changes dependency and symmetry status, but not the earlier combinatorial theorems.

---

# 343. Static covariance versus tower symmetry

The following statements must be distinguished.

## Static fixed-layer covariance

For any bijection:

\[
\phi:V_n\to V_n',
\]

relabel every atom in every Hamilton-cycle state.

Then:

\[
\boxed{
HC(\phi):HC(V_n)\to HC(V_n')
}
\]

is a bijection.

Thus the static Hamilton-cycle object is fully relabelling-covariant.

If:

\[
V_n=V_n',
\]

then:

\[
S_n
\]

acts as the usual fixed-layer relabelling symmetry.

## Chosen-tower self-symmetry

For a \(V_1\)-seeded singleton filtration:

\[
V_1\subset V_2\subset\cdots\subset V_N,
\]

each atom has a unique first-appearance stage.

Any automorphism preserving every filtration level must fix every atom.

Therefore:

\[
\boxed{
\operatorname{Aut}_{\rm atom}(\mathcal V_N)=\{e\}.
}
\]

These statements are not inconsistent.

The second object carries strictly more structure than the first.

---

# 344. Tower isomorphisms

Let:

\[
\mathcal V=(V_n,\iota_n)
\]

and:

\[
\mathcal V'=(V_n',\iota_n')
\]

be singleton towers.

A tower isomorphism is a compatible family:

\[
\phi_n:V_n\to V_n'
\]

such that:

\[
\boxed{
\phi_{n+1}\circ\iota_n
=
\iota_n'\circ\phi_n.
}
\]

Equivalently, the atom born at stage \(j\) is mapped to the atom born at stage \(j\).

Naturality means that every derived HC construction commutes with these maps.

This is the correct symmetry notion once growth history is retained.

---

# 345. HC-state naturality

A Hamilton-cycle state is an undirected cyclic ordering modulo the dihedral action.

Relabelling every atom by:

\[
\phi_n
\]

does not alter:

- cyclic incidence;
- degree-two structure;
- dihedral equivalence.

Therefore:

\[
\boxed{
HC(\phi_n)
}
\]

is well defined and bijective.

RAW-13 directly checked this on complete HC state sets through:

\[
n=7
\]

under multiple nontrivial relabellings.

Thus RAW-12's canonical growth chart does not modify the raw HC state definition.

---

# 346. Raw overlap naturality

For:

\[
C,D\in HC(V_n),
\]

define:

\[
o(C,D)=|E(C)\cap E(D)|.
\]

Since a bijection maps unordered edges bijectively:

\[
E(\phi C)=\phi(E(C)),
\]

we have:

\[
\boxed{
o(\phi C,\phi D)=o(C,D).
}
\]

Hence:

\[
d_E(C,D)=n-o(C,D)
\]

is also preserved.

Likewise the common-edge graph is carried isomorphically to the relabelled common-edge graph.

Therefore its component/path-size data are natural.

This includes the intrinsic pair data used in RAW-03 and RAW-04B.

---

# 347. Reversal-support naturality

Let:

\[
D=R_{s,\ell}(C)
\]

be obtained by reversing a circular block of length:

\[
\ell.
\]

Relabelling changes only the atom names, not the cyclic positions.

Therefore:

\[
\boxed{
\phi(R_{s,\ell}(C))
=
R_{s,\ell}(\phi C).
}
\]

Hence every reversal-support relation:

\[
LR_\ell
\]

is natural.

In particular:

\[
\boxed{
C\sim_{LR3}D
\iff
\phi C\sim_{LR3}\phi D.
}
\]

The intrinsic common-path support:

\[
\{\ell,n-\ell\}
\]

is preserved as well.

Thus the entire RAW-04B/05A reversal-support classification survives unchanged.

---

# 348. Intrinsic bipartition naturality

For even:

\[
n=2m,
\]

every Hamilton cycle is bipartite.

Let:

\[
\Pi_{\rm intr}(C)
=
\{A_C,B_C\}.
\]

Relabelling gives:

\[
\boxed{
\Pi_{\rm intr}(\phi C)
=
\{\phi(A_C),\phi(B_C)\}.
}
\]

Therefore:

- the bipartition sector relation is natural;
- LR odd/even preservation status is natural;
- even LR3 components remain intrinsic bipartition fibres under every relabelling.

The sector construction does not depend on the tower chart.

---

# 349. All-slot growth naturality

Let:

\[
x_{n+1}
\]

be the new atom in:

\[
V_{n+1}\setminus V_n.
\]

For:

\[
C\in HC_n
\]

and:

\[
e\in E(C),
\]

let:

\[
\Gamma_n(C,e)
\]

insert \(x_{n+1}\) into \(e\).

For a tower isomorphism:

\[
\phi,
\]

the new atom maps to:

\[
x_{n+1}'=\phi_{n+1}(x_{n+1}),
\]

and the edge maps to:

\[
\phi_n(e).
\]

Then:

\[
\boxed{
HC(\phi_{n+1})
\big(
\Gamma_n(C,e)
\big)
=
\Gamma_n'
\big(
HC(\phi_n)(C),
\phi_n(e)
\big).
}
\]

Thus the insertion square commutes.

Symbolically:

\[
\begin{array}{ccc}
HC_n\times E(C) & \xrightarrow{\Gamma_n} & HC_{n+1}\\
\downarrow \phi_n && \downarrow \phi_{n+1}\\
HC_n'\times E(\phi C) & \xrightarrow{\Gamma_n'} & HC_{n+1}'
\end{array}
\]

commutes.

RAW-13 certified this exhaustively/sampled through target size:

\[
N=8.
\]

---

# 350. Deletion naturality

Let:

\[
\pi_{x_{n+1}}
:
HC_{n+1}\to HC_n
\]

delete the newest atom and restore its two neighbours as one edge.

Then:

\[
\boxed{
HC(\phi_n)
\circ
\pi_{x_{n+1}}
=
\pi_{x_{n+1}'}
\circ
HC(\phi_{n+1}).
}
\]

So the deletion square also commutes.

This is the exact compatibility required by:

- RAW-06 growth analysis;
- RAW-07 support filtration;
- RAW-09A horizontal/vertical LR2 classification.

---

# 351. Support-filtration naturality

Take a target reversal pair:

\[
(C,D)\in LR_\ell^{(n+1)}.
\]

Delete the newest atom:

\[
(\pi C,\pi D).
\]

RAW-07 showed that its support lies in:

\[
LR_\ell^{(n)}
\cup
LR_{\ell-1}^{(n)}
\]

with the appropriate half-cycle and identity boundary cases.

RAW-13 verifies that tower relabelling commutes with this projection.

Hence the diagram:

\[
LR_\ell^{(n+1)}
\longrightarrow
LR_\ell^{(n)}
\cup
LR_{\ell-1}^{(n)}
\]

is natural with respect to tower isomorphisms.

Therefore the reversal-support filtration is genuinely graded rather than an artifact of the canonical numeric chart.

---

# 352. First-appearance rank naturality

Let:

\[
\beta(v)
=
\min\{n:v\in V_n\}.
\]

For a tower isomorphism:

\[
\phi,
\]

compatibility of the filtration implies:

\[
\boxed{
\beta'(\phi(v))
=
\beta(v).
}
\]

Thus:

\[
\beta
\]

is a tower-natural scalar.

It is not a static-layer invariant if the tower structure is held fixed and one arbitrarily permutes terminal atom names without relabelling the tower.

This distinction resolves the apparent tension between:

- full \(S_n\) covariance of static HC geometry;
- unique birth ranks in a chosen singleton tower.

---

# 353. Newest-site Johnson chart naturality

At even target size:

\[
N=2m,
\]

let:

\[
x_N
\]

be the newest atom.

The intrinsic sector:

\[
P=\{A,A^c\}
\]

is charted by selecting the side containing \(x_N\).

Using the historical \(m\)-subset convention on the parent labels gives a subset:

\[
S(P)\subset V_{N-1},
\qquad
|S(P)|=m.
\]

Now apply a tower isomorphism:

\[
\phi.
\]

The target chart gives:

\[
S'(\phi P)
\subset V_{N-1}'.
\]

Applying the target first-appearance rank:

\[
\beta'
\]

recovers exactly the same rank subset:

\[
\boxed{
\beta'(S'(\phi P))
=
\beta(S(P)).
}
\]

Thus the Johnson chart is natural **relative to the graded tower**.

Literal atom names disappear after passing to first-appearance coordinates.

---

# 354. Horizontal LR2 selector naturality

RAW-09A classified target LR2 edges using newest-site deletion.

For:

\[
C\sim_{LR2}D,
\]

define:

### Horizontal

\[
\pi_x(C)\ne\pi_x(D).
\]

### Vertical

\[
\pi_x(C)=\pi_x(D).
\]

Since deletion commutes with tower isomorphism:

\[
\boxed{
\text{horizontal/vertical status is natural}.
}
\]

The newest-site Johnson chart then gives:

\[
\boxed{
\text{horizontal}
\iff
d_J=1,
}
\]

and:

\[
\boxed{
\text{vertical}
\iff
d_J=m-1.
}
\]

RAW-13 verified that these Johnson distances are unchanged after arbitrary tested tower relabellings and subsequent conversion back to birth-rank coordinates.

Therefore:

\[
\boxed{
LR2_{\rm horizontal}
\to
A_1
}
\]

is a natural graded construction.

---

# 355. Naturality hierarchy

The rebuilt objects now fall into three classes.

## Static-natural

Defined without growth history and covariant under arbitrary atom bijections:

- \(HC_n\);
- raw overlap;
- common-path pair geometry;
- \(LR_\ell\);
- LR3;
- intrinsic even bipartition.

## Graded-natural

Require the tower but commute with tower isomorphisms:

- newest atom;
- insertion/deletion;
- support filtration across layers;
- first-appearance rank \(\beta\).

## Graded/chart-natural

Require the tower and a derived coordinate representation:

- newest-site Johnson subset chart;
- historical rank subset \([2k-1]\);
- horizontal \(LR2\to A_1\);
- birth-rank observable \(h\).

This vocabulary should replace the looser use of “intrinsic” for all three situations.

---

# 356. No symmetry contradiction

A common possible confusion is:

> If the graded tower has trivial automorphism, have we destroyed the \(S_n\) symmetry that supported the HC theorems?

No.

The \(S_n\) action remains the covariance group of the **static fixed-layer construction**.

Adding a particular history selects one structured object from among many isomorphic towers.

The correct analogy is:

\[
\boxed{
\text{covariance of a construction}
\ne
\text{automorphism group of one structured instance}.
}
\]

All fixed-layer formulas remain independent of which tower chart is used.

---

# 357. RAW-12 does not change earlier HC counts or theorems

RAW-13 found no change to:

- \(|HC_n|=(n-1)!/2\);
- incidence neutrality;
- raw overlap;
- nearest-shell 2-opt characterization;
- reversal-support decomposition;
- LR3 parity theorem;
- even LR3 component theorem;
- all-slot state completion;
- reversal-support deletion filtration;
- intrinsic bipartition sector counts;
- weighted Johnson association operator;
- growth-selected \(A_1\).

RAW-12 therefore changes:

\[
\boxed{
\text{dependency bookkeeping and history status},
}
\]

not:

\[
\boxed{
\text{certified fixed-layer combinatorics}.
}
\]

---

# 358. Commuting dependency diagram

The current architecture can be summarized as:

\[
\begin{array}{ccccc}
V_n
&\longrightarrow&
HC_n
&\longrightarrow&
\text{raw pair geometry}\\[1mm]
\downarrow
&&
\downarrow
&&
\downarrow\\[1mm]
V_{n+1}
&\longrightarrow&
HC_{n+1}
&\longrightarrow&
\text{raw pair geometry}
\end{array}
\]

where:

- the left vertical arrow is atom inclusion;
- the middle vertical structure is all-slot completion/deletion;
- the right vertical structure is reversal-support filtration.

For even layers an additional branch is:

\[
HC_{2m}
\to
\mathcal B_m
\to
\text{newest-site Johnson chart}
\to
A_1,
\]

while independently:

\[
V_1\subset\cdots\subset V_{2m-1}
\to
\beta
\to
h.
\]

Every audited square commutes under tower isomorphism.

---

# 359. Exact status of the word “natural”

RAW-13 uses “natural” in the structural sense:

> A construction is natural if applying a compatible atom relabelling before the construction gives the same result as applying the construction first and relabelling the output.

This is essentially functorial/equivariant behaviour.

No category-theoretic machinery is required for the present proofs, though the architecture can be formalized categorically later.

Avoid reading “natural” as:

- physically necessary;
- uniquely selected by nature;
- probabilistically preferred.

It is a covariance statement.

---

# 360. Computational certification

RAW-13 used multiple deterministic and seeded-random tower isomorphisms.

It checked:

### Fixed layers

Through:

\[
n=7,
\]

for:

- HC state relabelling;
- raw overlap;
- common-path data;
- all effective reversal supports;
- LR3;
- even intrinsic bipartitions.

### Cross-layer growth

Through target:

\[
N=8,
\]

for:

- insertion commuting squares;
- deletion commuting squares;
- projected support type;
- first-appearance rank covariance.

### Even sector / Johnson bridge

For:

\[
N=4,6,8,
\]

for:

- intrinsic sector relabelling;
- newest-anchor chart covariance;
- birth-rank subset recovery;
- horizontal/vertical LR2 status;
- Johnson \(A_1/A_{m-1}\) distance preservation.

Final result:

\[
\boxed{
317/317
}
\]

strict checks passed.

---

# 361. RAW-13 verdict

The graded substrate introduced in RAW-12 is compatible with the previously certified HC-RAW structure.

The exact status is:

\[
\boxed{
\text{static HC constructions remain fully relabelling-covariant},
}
\]

while:

\[
\boxed{
\text{growth-history constructions are natural under tower isomorphisms}.
}
\]

The tower does not alter raw HC mathematics.

It supplies additional cross-layer structure that:

- selects the newest atom;
- reconstructs first-appearance rank;
- makes deletion/growth coherent;
- turns the historical Johnson rank chart into a graded coordinate.

Thus RAW-12 is a foundational enrichment rather than a revision of the earlier fixed-layer theorems.

---

# 362. Recommended next step

The foundation is now sufficiently coherent for a consolidation audit.

### EHF-HC-RAW-14 — Primitive Data / Redundancy / Dependency-Minimality Audit

Candidate questions:

1. Which objects are genuinely primitive?
2. Which are definitional conveniences?
3. Which are exact consequences?
4. Is singleton atom growth stronger than required by any downstream theorem?
5. Which historical structures can be removed without losing:
   - LR3 selection;
   - support filtration;
   - Johnson \(A_1\);
   - birth-rank transport?
6. Can the entire current foundation be represented as a dependency DAG with no circular edges?

This would be a useful final foundation check before either opening the queued graph-emergence programme or returning to downstream physics bridges.
