# Wheeler series through WHEELER-62: mathematical results, physics relevance and novelty

**Date:** 19 October 2026 (Australia/Brisbane).

**Scope:** the Wheeler series and its current reviewed continuation, not an assessment of every EHF research branch. Based on the repository through `cdca2e45330f1caba003ca036f4fb7c4ab66c5f2`, [REVIEW-01](REVIEW-01.md), [ERRATA-01](../../probes/wheeler/ERRATA-01.md), and a targeted literature check on this date. This is a research synthesis and provisional originality assessment, not external peer review or a comprehensive priority search.

## 1. Overall assessment

The strongest current product is a concrete mathematical study of constrained cyclic growth, probability measures, coarse observations and entropy. It contains exact combinatorics, explicit counterexamples and an all-time theorem. It has not established that this model describes the physical universe.

The most compelling recent result is a contrast within one fixed event-uniform growth model: some deterministic seeds produce a decrease of ordinary rotation-class entropy, while the minimal four-run seed has strict entropy increase at every event. A precise symmetry correction explains the difference.

This is a better research claim than a universal assertion that growth creates entropy. It identifies exactly which assumptions make an entropy law succeed or fail.

## 2. The concrete model and what has been assumed

The principal current model is a binary cycle with no isolated bit: cyclic 010 and 101 are forbidden. Growth inserts one bit while retaining that constraint. In the event-uniform version, all admissible labelled insertion events from the current state have equal probability.

These choices define the model. The cycle, binary alphabet, admissibility condition, growth operation and probability rule have not all been uniquely derived from the broader EHF choice of admissible comparison as primitive data.

A run is a consecutive block of identical bits. D counts boundaries between runs. Admissible growth preserves D. Observations can retain the complete rooted word, forget the arbitrary starting point and retain a rotation class, or retain only statistics such as size n and the count N1 of ones. These observation choices are mathematically explicit; they are not yet fully implemented physical observers with derived memory and energy costs.

## 3. Cumulative results worth retaining

| Part of the series | Strongest retained contribution | Qualification |
|---|---|---|
| Early structural and MICRO probes, roughly 01–24 | Explicit constrained configurations; components, conserved sectors, growth/reversal examples and negative tests of proposed particle interpretations | Original 01–08 were available only as summaries in the review; some early current/physical arguments remain conditional |
| Core-C, 25–28 | Identification with a substring-reversal quotient gives the exact combinatorial gap n−1 | The normalized gap tends to zero; the expander claim was withdrawn; the underlying spectral theorem is established literature |
| Clocks and observers, 29–39 | Exact macro growth probabilities, closure criteria, hidden-sector inference and preparation dependence | Growth and comparison rates require a specified coupling; a missing observable does not make every preparation non-Markov |
| Observer costs, 40–49 | Useful questions about records, compression and inference resources | Infinite-history information cannot be priced as one event; memory capacity is not erased entropy |
| Measures and entropy, 50–57 | Exact counts, rooted entropy conditions, weighted counterexamples and the event/state distinction | Entropy laws depend on the kernel and reference measure; event primacy does not uniquely force uniform rates |
| 58 | Consistent history measures under fixed preparation; rooted distinct-successor count D+1 for D>0 | Both event-uniform and rooted state-uniform constructions are coherent; consistency alone selects neither |
| 59 | Event-uniform growth descends to rotation classes; rooted state-uniform growth generally does not; inherited orbit-weighted entropy is nondecreasing | Other rotation-independent kernels exist; ordinary quotient majorization fails |
| 60–61 | Ordinary rotation-class entropy can decrease, including in unconditioned growth from a deterministic seed | These are Shannon snapshot-entropy results, not thermodynamic violations |
| 62 | Strict ordinary class-entropy increase for the minimal seed (2,2,2,2), for every event; leading growth 3 log₂ t+O(1) | Specific preparation and four-run sector; the asymptotic scaling has established Dirichlet-multinomial precedents |

Earlier useful exact structure includes

`P(insert 1 | n,N1,D)=(N1+D/2)/(n+D)`.

Thus `(n,N1,D)` predicts its own next macrostate without knowing every run arrangement. At the individual-run level, a run of length ℓ is extended with probability proportional to ℓ+1, giving a classical Pólya-urn representation. The value here is the exact reduction from the specified cyclic process, not the invention of Pólya urns.

## 4. What is most interesting to a mathematician?

### First: the entropy theorem and counterexample together

The clearest candidate for a focused mathematical paper is the sequence WHEELER-59–62.

Starting from `(2,100,2,100)`, with no filtering or reweighting, ordinary class entropy decreases from approximately 1.321337 to 1.307664 bits between events two and three. Rational logarithm bounds certify the negative sign. By contrast, the seed `(2,2,2,2)` has strictly increasing ordinary class entropy at every event, proved by exact inequalities.

For pair-symmetric four-run seeds, the key identity is

`H(rotation class)=H(ordered runs)−1+P(periodic run pattern)`.

The entropy chain rule supplies the identity. The substantive model work is in calculating the periodic-pattern probability and controlling its change against ordered-run entropy production. For the minimal seed this produces an all-time theorem; for other seeds the correction explains a decrease.

The interesting question is therefore which preparations and symmetry groups preserve monotonicity. It is a concrete question in probability, combinatorics and information theory, independently of a physical interpretation.

### Second: an exact test of representation-independent dynamics

Giving each admissible event equal probability and giving each distinct rooted successor equal probability are different prescriptions. WHEELER-59 shows that the first has a representative-independent rotation quotient and the second generally does not.

This is a useful model-building test: if the starting point of a cycle is meant to be arbitrary, predictions about the unrooted cycle should not depend on it. The result narrows viable prescriptions but does not establish a unique probability law.

### Third: tractable combinatorics and observer reductions

Conserved D, exact insertion counts, rooted fibre counts, D+1 distinct rooted successors, and explicit macro kernels make the model analytically accessible. It supports exact calculations rather than relying entirely on numerical patterns. The known-urn reduction also makes comparison with established probability theory straightforward.

### What not to lead with

The known spectral gap, generic use of Pólya urns, the entropy chain rule, ordinary lumpability, or existence of a process from normalized kernels should not be advertised as newly invented mathematics. They are established tools or results applied to this setting. A researcher will want the precise additional theorem or counterexample isolated from that background.

## 5. What is most interesting for physics?

### Most relevant: entropy, observations and preparation

The model gives a controlled example in which one underlying stochastic growth rule supports different entropy conclusions depending on what distinctions are retained and how the system is prepared. Rooted Shannon entropy, ordinary class entropy, inherited orbit-weighted entropy, and history entropy are different quantities.

This is relevant to the methodological questions of statistical physics: what constitutes a physical state, which labels are redundant, which probabilities describe the preparation, and what information an observation retains. The general importance of coarse-graining is established; the present contribution is an exactly analyzable example with explicit successes and failures.

A possible interpretation to investigate is that an observed entropy arrow can require a suitable preparation and observation scheme. The toy model illustrates this possibility; it does not derive the physical arrow of time or identify the universe's initial condition.

### Next: exact effective descriptions and hidden information

The macro kernel shows how a coarse description can remain predictive without retaining the entire configuration. Other projections can lose universal Markov closure, while fixed preparation and retained sufficient statistics can still allow prediction. This is relevant to effective descriptions and memory, but is classical stochastic inference, not a derivation of quantum hidden variables or quantum measurement.

### Longer-term: spectra, growth and clocks

Exact graph spectra give a route to studying relaxation. But a physical relaxation law requires an explicit generator, rates and their size scaling. A combined growth/comparison process also needs the action of growth on the modes being compared. The corrected Core-C result is useful infrastructure, not a Yang–Mills mass-gap result.

### Physics not yet obtained

The reviewed Wheeler work has not derived quantum amplitudes or interference, the Born rule, unitary dynamics, relativistic spacetime, gravity, the Standard Model, a Yang–Mills mass gap, or a new experimentally validated prediction. The coefficient three in `3 log₂ t` counts independent run-extension coordinates; it does not establish three physical spatial dimensions.

The present model is most accurately described as a classical stochastic growth model motivated by broader foundational questions.

## 6. Novelty: what the literature check changes

Novelty has several levels: a result can be new within this project, an independent derivation of known mathematics, a new application, or new to the literature. Only the first is automatically established by our work history.

The targeted search found close prior work that should be acknowledged:

- **Growing necklaces and urns:** Toshio Nakata's 2009 paper *Necklace Processes Via Pólya Urns* studies insertion processes, colour counts and runs [1]. Its published abstract establishes a directly relevant predecessor. Full rule-by-rule comparison remains to be done; the abstract alone neither establishes nor rules out equivalence to our constrained model.
- **Dirichlet-multinomial entropy:** Turowski, Jacquet and Szpankowski give a more detailed entropy asymptotic, with leading term `(m−1) log n`, in Theorem 2 [2]. Taking m=4 and noting that a two-element quotient changes entropy by at most one bit already gives the same leading `3 log₂ t+O(1)` scaling. Our elementary proof is useful, but the leading law is not a sound standalone novelty claim.
- **Symmetry and Markov quotients:** orbit-chain constructions and their relation to symmetry have an established literature [3,4].
- **Lumping and information:** Geiger and Temmel study lumpability and entropy-rate preservation [5]. Their finite-state stationary entropy-rate setting differs from our growing-layer snapshot entropy question, but the broader information-loss issue is not new.
- **Core-C spectral input:** the substring-reversal gap used by the Core-C argument is a theorem of Chung and Tobin [6].

| Item | Responsible originality assessment |
|---|---|
| Pólya reduction and exact endpoint family | Established probability tools; specific cyclic-model reduction may be useful |
| Projective consistency and symmetry-induced closure | Established principles; model-specific verification |
| General entropy/orbit identity | Entropy chain rule plus symmetry; not a new general law |
| Leading 3 log₂ t scaling | Follows from known Dirichlet-multinomial asymptotics and bounded quotient correction |
| Rooted event/state distinction and root-dependence example | Model-specific result; candidate contribution pending closer literature comparison |
| Exact ordinary class-entropy counterexamples, especially the unconditioned single-seed example | Strong candidate contribution; priority unverified |
| All-time minimal-seed quotient-entropy theorem, periodicity formula and explicit positivity certificate | Strongest current positive candidate contribution; priority unverified |
| A new law of physics | Not established |

I did not identify an exact match for the WHEELER-61/62 theorem–counterexample pair in the targeted search. That is a statement about this search, not proof of novelty. A serious novelty claim requires closer comparison with necklace-process and reinforced-process literature and an independent mathematical reading.

## 7. Plain-language summary for Barz

Imagine a necklace of black and white beads. No colour is allowed to appear as a single isolated bead. We let the necklace grow by inserting beads in allowed places.

We can now calculate exactly how that growth behaves. We know which properties remain fixed, what information is enough to predict certain observations, and how different ways of choosing the next move affect the answers.

Then we asked whether uncertainty must always increase as the necklace grows. It depends on which distinctions are counted. If you mark a starting bead, you distinguish more arrangements. If you remove that mark, several drawings become the same necklace. Repeated patterns make that loss of distinction vary during growth.

We found one starting necklace whose observed uncertainty briefly decreases under ordinary growth. We also proved that the smallest four-block starting necklace never has such a decrease, however long it grows. We can explain both outcomes using the same calculation.

Entropy here means uncertainty across repeated possible outcomes, not a claim that each individual necklace becomes messier. A model can gain beads and gain possible outcomes while its probability distribution becomes more concentrated.

This is real progress in understanding a mathematical model. We have not established that the universe is made of these necklaces or that EHF has recovered quantum mechanics. What we have is a precise, reproducible way to investigate how growth, symmetry, observation and preparation shape effective laws.

## 8. Suggested research presentation and next steps

A focused working-paper title would be **“Entropy and symmetry in constrained cyclic growth.”** Lead with the exact model, quotient kernel, single-seed counterexample and minimal-seed theorem. Present EHF as motivation rather than as a conclusion established by those results.

Before asserting originality, compare the insertion rules and observables with Nakata and the earlier Mallows–Shepp necklace process, and compare the entropy claims with existing urn and quotient literature. Cite the established asymptotic law explicitly. Independent proof review would then determine whether the remaining model-specific results form a useful contribution.

WHEELER-63 remains a natural mathematical continuation: minimal seeds with D=6,8,…, where more rotation symmetries can occur. It should follow the correct group-action entropy correction. A separate physics-focused branch would repair the combined growth/comparison clock and identify an observable physical prediction; simply proving more combinatorial theorems does not complete that bridge automatically.

## Sources and reading map

Primary literature checked on 19 October 2026:

1. Toshio Nakata, *Necklace Processes Via Pólya Urns*, Journal of Applied Probability 46(1), 284–295 (2009). Publisher abstract and bibliographic record inspected; full-paper comparison outstanding. https://doi.org/10.1239/jap/1238592130
2. Krzysztof Turowski, Philippe Jacquet and Wojciech Szpankowski, *Asymptotics of Entropy of the Dirichlet-Multinomial Distribution*, ISIT 2019, especially Theorem 2. Primary author-hosted paper inspected. https://www.cs.purdue.edu/homes/spa/papers/isit19-dirichlet.pdf
3. Stephen Boyd, Persi Diaconis, Pablo Parrilo and Lin Xiao, *Symmetry Analysis of Reversible Markov Chains*, author manuscript revised 29 November 2004. https://web.stanford.edu/~boyd/papers/pdf/symmetry.pdf
4. Mathias Niepert, *Markov Chains on Orbits of Permutation Groups* (2012). https://arxiv.org/abs/1206.5396
5. Bernhard C. Geiger and Christoph Temmel, *Lumpings of Markov chains, entropy rate preservation, and higher-order lumpability* (preprint 2012). Abstract and scope inspected. https://arxiv.org/abs/1212.4375
6. Fan Chung and Josh Tobin, *The Spectral Gap of Graphs Arising From Substring Reversals*, Electronic Journal of Combinatorics 24(3), P3.4 (2017). https://doi.org/10.37236/6894

Project reading order: [review](REVIEW-01.md), [errata](../../probes/wheeler/ERRATA-01.md), [W58](../../probes/wheeler/WHEELER-58.md), [W59](../../probes/wheeler/WHEELER-59.md), [W60](../../probes/wheeler/WHEELER-60.md), [W61](../../probes/wheeler/WHEELER-61.md), [W62](../../probes/wheeler/WHEELER-62.md), and [reproducible code](../../code/wheeler/README.md).
