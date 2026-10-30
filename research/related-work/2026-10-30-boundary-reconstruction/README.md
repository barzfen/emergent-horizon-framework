# EHF-RW-002 — What can a boundary observer reconstruct?

30 October 2026. **COMPUTATIONAL:** exhaustive exact finite tests on Hamiltonian-triad unions. **PROVED in the specified linear model:** an internal-edge ambiguity survives the complete boundary response. This is a reconstruction audit inspired by a question raised by holography, not a test or derivation of celestial holography.

## Sources and attribution

1. Sabrina Pasterski, Monica Pate and Ana-Maria Raclariu, *Celestial Holography* (2021), [arXiv:2111.11392v1](https://arxiv.org/abs/2111.11392v1), [HTML](https://arxiv.org/html/2111.11392v1). Sections 1–3 were consulted on 30 October 2026 for motivation and the distinction between changing the description and discarding information. This work supplies the physical question, not the graph-response construction used below. No full review of its technical programme or verification of its cited results was performed.
2. Florian Dörfler and Francesco Bullo, *Kron Reduction of Graphs with Applications to Electrical Networks*, [arXiv:1102.2950v1](https://arxiv.org/abs/1102.2950v1); journal version, IEEE Transactions on Circuits and Systems I 60(1), 150–163 (2013), [DOI:10.1109/TCSI.2012.2215780](https://doi.org/10.1109/TCSI.2012.2215780). The arXiv abstract and IEEE publication record were consulted on 30 October 2026. The established Laplacian Schur-complement/Kron-reduction method is credited here; this entry does not claim to reproduce their full paper. We derive the block-elimination identity directly below.

No figures, code or substantial passages are copied from either source. Probe code was developed with AI assistance for this investigation. The reductions, non-uniqueness mechanism and observability principles are standard mathematics; no novelty claim is made.

## Question and EHF construction

Can measurements restricted to a chosen boundary distinguish different interiors of our finite Hamiltonian networks? Compare sparse observations with a richer transport response, and look for explicit failures of reconstruction.

Use precisely the triad ensemble defined in [EHF-RW-001](../2026-10-30-kazazi-reconfiguration/README.md): three Hamiltonian cycles on labelled vertices 0,…,N−1, with no undirected edge present in all three. Each tour is modulo rotation and reflection. Repeated component tours are permitted if the constraint holds. Enumeration is exhaustive for N=4,5,6. The present code is standalone and regenerates every input.

For this experiment, replace each triad by its **simple union graph**: edge multiplicities and cycle identities are discarded. Assign unit conductance to every distinct union edge, and use its combinatorial Laplacian L=D−A. This defines a classical linear diffusion model with generator −L; it is an imposed probe law, not derived particle dynamics.

Choose B={0,…,b−1} as the observed vertices and I as the interior. This boundary is imposed by labels, not reconstructed from graph geometry; it need not be a surface or a separator. No spatial embedding, celestial sphere, dimensional claim, scattering amplitude or quantum theory is introduced.

The reconstruction target is the union graph **up to permutations of interior vertices fixing every boundary vertex pointwise**. This removes ambiguity from hidden names while retaining boundary labels. Reconstruction of the original triad is a stronger task and already fails when the union map merges different cycle decompositions.

## Boundary measurements and exact reduction

We compare four observers:

| Observer | Retained information |
| --- | --- |
| Boundary edges | Adjacency among vertices in B only |
| Static response | Effective boundary response after interior equilibration |
| Static plus z=1 | Static response and one positive Laplace-parameter response |
| Complete transfer | The exact rational boundary-response function for every z>0 |

For zero initial conditions, externally imposed boundary values x_B and no interior forcing, the Laplace-transformed interior equation is

    (z I + L_II) x_I = −L_IB x_B.

Eliminating x_I gives the boundary forcing f_B = S(z) x_B, where

    S(z) = z I + L_BB − L_BI (z I + L_II)^−1 L_IB.

At z=0, this is standard static Kron reduction. The grounded interior Laplacian is invertible because the graph is connected and B is nonempty. At z>0, all inverses used here exist, and

    S(z)^−1 = [(z I + L)^−1]_BB.

Thus S(z) captures the boundary-to-boundary response of this linear system. This is a genuine exact reduction for the declared inputs and outputs; it need not be an invertible encoding of the interior.

**Complete-function comparison is exact, not a finite-frequency guess.** With m=|I|, the code retains L_BB and the first 2m moments L_BI L_II^k L_IB for k=0,…,2m−1. For two graphs of this known size, their transfer-function difference has a block-diagonal realization of dimension 2m. Cayley–Hamilton implies that if its first 2m moments vanish, all later moments vanish. Together with equal L_BB this proves equality of S(z) as a rational function. Conversely, equal rational functions have equal large-z coefficients. We also check response equality at independent z=2,3 as a numerical-free implementation check.

## Exhaustive results

The ensembles contain respectively 6, 516 and 80,940 ordered labelled triads. After forgetting cycle labels there are 1, 92 and 13,580 triads. Their distinct labelled simple union graphs number 1, 11 and 596.

Each row below compares graphs after quotienting only interior labels. An observation class may contain several inequivalent graphs; that is a reconstruction failure.

| N | Boundary vertices | Graph classes | Boundary-edge observations | Static observations | Static plus z=1 observations | Complete-transfer observations |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 1 | 3 | 1 | 1 | 2 | 2 |
| 5 | 2 | 5 | 2 | 3 | 4 | 4 |
| 5 | 3 | 8 | 4 | 7 | 7 | 7 |
| 5 | 4 | 11 | 7 | 11 | 11 | 11 |
| 6 | 1 | 17 | 1 | 1 | 7 | 7 |
| 6 | 2 | 49 | 2 | 22 | 34 | 34 |
| 6 | 3 | 137 | 8 | 121 | 121 | 121 |
| 6 | 4 | 334 | 38 | 324 | 324 | 324 |

N=4 has only one union graph, K_4, so every tested observer is trivially injective over that ensemble. This is not evidence for general reconstruction. Full access B=V is an additional positive control: S(z)=zI+L reconstructs every union graph immediately.

For N=6 with two observed vertices, transport information improves discrimination from 2 edge-only observations to 34 complete responses, but there are 49 inequivalent interiors. In these tiny ensembles, static plus z=1 happens to discriminate exactly as many graphs as the complete function; this is an enumerated observation, not a theorem about larger networks.

## An explicit ambiguity and why it persists

Take N=5, B={0,1,2}, I={3,4}. Compare K_5 with K_5 missing just the edge {3,4}. Both occur as valid triad unions; the generating cycles are retained in [witness_checks.json](witness_checks.json). They are non-isomorphic even without boundary labels because their edge counts differ.

Both hidden vertices have exactly the same boundary neighbors. Boundary forcing drives their equal-value mode, while the internal edge acts only on their difference. That difference mode is invisible at B. Adding the edge changes a hidden decay eigenvalue from 3 to 5 without changing any boundary response.

More generally, take a complete boundary graph on b vertices and connect all of them to all m hidden vertices. Let the hidden vertices carry any simple graph H, with Laplacian L_H. Then

    L_BB = N I_b − J_b,
    L_BI = −1_(b×m),
    L_II = b I_m + L_H.

Since L_H 1=0,

    S(z) = (N+z) I_b − [1 + m/(b+z)] J_b.

This is independent of H. The algebra applies to this general graph family; **membership in the constrained-triad ensemble is explicitly established here only for the retained N=5 and N=6 witness pairs**. The general family is not claimed to consist entirely of triad unions.

For the five-vertex pair, the static map is 5 I_3 − (5/3) J_3, and at z=1 the map is 6 I_3 − (3/2) J_3. Equality holds for every z≥0, not just these examples. The independent verification script checks the closed formula at z=0,1/7,1,2,3,17 and compares complete moment signatures.

## Information already lost before the boundary restriction

For K_5 the enumeration finds **72 distinct unordered triad decompositions**. Any observer depending only on its simple union Laplacian must identify all of these, even if every vertex is observed. Richer boundary measurements cannot restore cycle labels, multiplicities or decomposition information that the probe law never uses.

This separates two issues: loss in replacing a triad by its union graph, and further loss in observing that graph through a restricted boundary. The outputs include examples of both.

## Verification, reproduction and limits

All arithmetic uses integers and exact fractions. Assertions check Laplacian row sums, response symmetry, static row sums, the block inverse identity using an independent full-matrix inversion, invariance under interior relabelling, complete-signature agreement at additional z values, and the full-access control. The witness script independently checks the closed-form expression.

From the repository root, Python 3 standard library only:

```bash
python3 research/related-work/2026-10-30-boundary-reconstruction/probe.py
python3 research/related-work/2026-10-30-boundary-reconstruction/verify_witness.py
```

[results.json](results.json) retains all counts, ambiguity statistics and counterexample graphs with generating triads. [witness_checks.json](witness_checks.json) retains the independently checked pair. Both record their source hashes. There are no random seeds, fitted parameters or external datasets.

These probes establish exact statements about specified finite graph observers. They do not show area-law information scaling, dimensional reduction, a celestial CFT, a lossless bulk/boundary duality, or a physical obstruction to celestial holography. The positive and negative cases depend on the target, model class, dynamics, inputs and available observations.

## Potential contribution back and next test

**Nothing ready for researcher outreach.** The Schur reduction and invisible-mode mechanism are established ideas. The EHF-specific contribution is a reproducible audit within a small constrained ensemble; priority has not been assessed against inverse-graph and boundary-control literature. The current results do not challenge the celestial-holography programme.

A focused next test is to add observables that break the hidden symmetry: move one hidden vertex into B, introduce a separately declared unequal probe coupling, or retain cycle labels and multiplicities in a lifted transport model. Test each change independently and report whether it removes the ambiguity. Any proposed EHF dual description must state what information it intends to reconstruct before claiming to preserve it.
