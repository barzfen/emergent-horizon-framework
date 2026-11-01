# EHF assumption audit 01: when are different relational roles forced?

Date: 1 November 2026. Status: elementary mathematical deductions and exhaustive finite checks. No physical interpretation established; no novelty claim.

Research question posed by Barry Fensom. Mathematical development, implementation and exposition assisted by ChatGPT. This is a deliberately restricted audit, not a derivation of the EHF construction or an explanation of existence.

## Question and scope

Which assumptions force distinguishable relational roles, and which merely allow them? We temporarily set aside Hamiltonian cycles, growth, probabilities and observers. This tests a simpler model class; it does not replace EHF's definitions.

Let G=(V,E) be a finite simple undirected graph: n vertices, m edges, no loops, no multiple edges. An edge represents a symmetric admissible comparison. We have already assumed a finite collection, pairwise relations, symmetry and Boolean admissibility. None is derived here. More general directed, weighted, higher-order or infinite structures require a different audit.

Two vertices have the same **structural role** if an automorphism of G takes one to the other. An automorphism is a renaming that preserves every edge. Roles are automorphism orbits. Exactly one role means vertex-transitivity. This is a global structural definition, not a claim that an internal observer can detect every difference.

Different degrees certify different roles, since an automorphism preserves degree. Equal degrees do not generally certify equal roles. Our program checks actual automorphisms for regular graphs rather than equating regularity with vertex-transitivity.

## 1. Bare comparison does not force different roles

Empty graphs, complete graphs and cycles have just one vertex role. The cycle example shows that selective comparison, connectivity and nontrivial organisation can coexist with uniform vertex roles. A cycle is structured; it need not contain a preferred vertex.

The three-vertex path P3 has two roles: its middle and its endpoints. These roles are determined by its supplied relation. We have reconstructed a distinction from that relation, not explained the origin of the relation itself.

## 2. Exact forcing criterion for fixed size and edge count

**Proposition.** Fix n>=3 and n-1<=m<=n(n-1)/2. Among connected simple undirected graphs with n vertices and m edges, **every graph has at least two vertex roles if and only if n does not divide 2m**.

This is a statement about what the coarse assumptions (n,m,connectivity) force across a whole class. It is not a test saying that a particular graph has one role whenever n divides 2m. Some graphs in that class may have several roles.

**Proof, forcing direction.** A one-role graph must be regular, with some integer degree d. Counting edge endpoints gives nd=2m. If n does not divide 2m, regularity is impossible. There must be unequal degrees, hence distinct roles.

**Proof, converse by construction.** Suppose n divides 2m and set d=2m/n. Feasibility and connectivity's edge lower bound imply 2<=d<=n-1 for n>=3. On vertices Z/nZ, construct the following graph:

- For even d, connect each vertex i to i +/- 1, ..., i +/- d/2 modulo n.
- For odd d, n is even (nd is even). Connect i to i +/- 1, ..., i +/- (d-1)/2 and to its antipode i+n/2.

These are simple d-regular graphs, contain the cycle of +/-1 edges, and therefore are connected. Rotation i -> i+1 is an automorphism acting transitively. They have m edges and just one role. Thus the coarse assumptions do not force multiple roles. QED.

**Examples.** At n=5,m=4, roles must differ. At n=5,m=5, C5 is a one-role counterexample to universal forcing. At n=6,m=9, a one-role cubic circulant likewise exists. The criterion is not a claim of degree irregularity in every role-distinguishable graph.

This proof assembles standard elementary graph arguments (edge-endpoint counting, automorphism invariance and circulant constructions). We have not established research novelty or checked priority literature; do not market it as a new EHF theorem.

## 3. A small sufficient package and assumption removal

**Connected + acyclic + n>=3** forces different roles. A finite connected acyclic graph has m=n-1, and n does not divide 2n-2 for n>=3. Equivalently, it has leaves and at least one vertex of degree >=2.

Each hypothesis is needed for this particular sufficient package:

| Removed hypothesis | Counterexample retaining the others | Outcome |
| --- | --- | --- |
| Connectivity | Two disjoint edges | Four vertices, acyclic, one role |
| Acyclicity | C4 | Connected, four vertices, one role |
| n>=3 | K2 | Connected, acyclic, one role |

This package is **irredundant**, not uniquely weakest or necessary for every graph with different roles. A triangle with a pendant leaf has different roles despite containing a cycle. Alternative sufficient assumptions can be incomparable. There is no meaningful universal 'weakest foundation' until both the target property and permitted hypothesis language are fixed.

## 4. Structural distinction is not persistent memory

The previous results concern a static graph. No dynamics means no demonstrated persistence mechanism.

For a further exact restriction, suppose a state update F is deterministic and equivariant under renamings: F(p s)=p F(s). If the initial state s is fixed by a symmetry p, then F(s)=F(p s)=p F(s). By induction, every subsequent state retains that symmetry. Here the state includes any marks, records or other data; an asymmetric initial mark is an additional input.

Thus a symmetric deterministic model with symmetric initial data cannot uniquely select one of equivalent vertices while respecting that symmetry. This does not forbid structured symmetric outcomes, invariant subsets or evolution between graph structures. It does not establish a ban on stochastic symmetry breaking: an individual random outcome can be asymmetric even when its probability law is symmetric. Random rules and distributions would be additional assumptions to audit.

Nor do different static roles imply memory. To test memory we must specify updates, perturbations, encoding, readout and a retention criterion. Under arbitrary relation replacement, a P3 distinction disappears immediately if the relation is replaced by the complete graph on the same vertices. Under a fixed graph, role persistence is built into the frozen input. Neither supplies a derived recording mechanism.

## 5. Executed checks

Run with Python 3.10+; no external packages:

```sh
python3 foundation/assumption-audit-01/probe.py
```

The program enumerates every labelled simple graph on 3 through 6 vertices, filters for connectivity, and checks vertex-transitivity. For each feasible (n,m) bucket it verifies that the absence of any vertex-transitive member agrees exactly with n not dividing 2m.

| n | All labelled graphs examined | Connected graphs | Connected vertex-transitive graphs |
| --- | ---: | ---: | ---: |
| 3 | 8 | 4 | 1 |
| 4 | 64 | 38 | 4 |
| 5 | 1,024 | 728 | 13 |
| 6 | 32,768 | 26,704 | 146 |

Total: 33,864 labelled graphs, of which 27,474 are connected. These are labelled counts, not counts up to isomorphism. Every assertion passed. Separately, 570 feasible circulant constructions for 3<=n<=40 passed checks for connectivity, degree and transitive rotation symmetry. Five explicit assumption-removal/control witnesses were checked. Full output is in [results.json](results.json); code is in [probe.py](probe.py).

The finite enumeration checks the implementation and small instances. The proof above, not enumeration, supports the all-size proposition. The constructive checks do not enumerate all graphs above n=6.

## EHF implication and next decision

Admissible comparison is currently a chosen description, and a bare relation does not force distinct roles. A single unmarked Hamiltonian cycle also has just one vertex role. Several cycles can supply richer arrangements, but cycle labels, overlap rules and switching dynamics add assumptions that must be listed separately. This audit proves nothing about which roles all valid EHF triads must possess.

Next substantive target: state an explicit local recording dynamics and ask whether distinguishable records survive its allowed perturbations. Any robustness result must name the noise model and timescale. Do not claim that static role distinctions already constitute an observer, a clock, spatial dimensions or physical law.

## Attribution and potential contribution back

This is a self-contained use of standard graph theory, not a follow-up establishing a result from the previously discussed holography or reconfiguration papers. No third-party paper, code or dataset is reproduced. The graph enumeration is generated directly by the included standard-library program. There is no new result ready for external outreach. A priority review would be required before asserting novelty. Research-note and code terms follow the repository's [licensing policy](../../LICENSE.md).
