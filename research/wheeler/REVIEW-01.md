# EHF Wheeler series: independent review 01

Date: 18 October 2026 (Australia/Brisbane)

Source snapshot: `barzfen/emergent-horizon-framework`, commit `106783d120bf5895cdcd67c8086ab382feebfb8c`.

> Repository integration note: this review describes the pre-correction snapshot above. Corrections are now recorded in [ERRATA-01](../../probes/wheeler/ERRATA-01.md); [WHEELER-58](../../probes/wheeler/WHEELER-58.md) is the subsequent continuation. Results: [review-01-results.json](../../data/wheeler/review-01-results.json).

## Overall assessment

Continue the programme, but correct several claims before WHEELER-58. The strongest retained work is the explicit MICRO growth combinatorics, the associated probability model, and the conditional entropy results. The series also contains useful negative results and explicit corrections of earlier interpretations. It does not establish a physical mass gap, particle species, thermodynamics, or a uniquely compelled probability measure.

This assessment is based on arguments and reproducible checks, not on the model used to write the original reports. A replacement model's confidence is not a validation method.

## Scope and limits

Read all standalone WHEELER-09–57 reports and the series index, which contains summaries of 01–08. Full original 01–08 reports were not present in the inspected tree. The tree contains Markdown reports but no original computational scripts or raw numerical outputs for these audits. Thus this is a critical review with independent reconstruction of selected calculations, not a formal certification of every claim or a reproduction of every original experiment.

The accompanying `../../code/wheeler/review_audit.py` reconstructs the cyclic binary model and the Hamilton-cycle graph from their written definitions. All finite tests below were actually run. The script uses labelled binary words, distinct graph neighbours, and insertion before positions 0 through n−1. Rotations are identified only in the separately labelled component-quotient checks. These conventions matter.

## Priority findings

### R1. Growth rates do not automatically determine comparison rates

**Affected: WHEELER-29–31; related hybrid construction in 44–46. Status: substantive missing model connection.**

WHEELER-28 correctly gives a frozen-size comparison relaxation gap

`Delta_n = R_C(n) (n−1)/d_n`, where `d_n=n(n−3)/2`.

Here `R_C` is the total rate of comparison events. Counting n insertion sites and assigning each growth site hazard r establishes `R_G=rn`. It does not establish `R_C=rn`. Comparisons and growth are different event families. Locality and additive growth hazards do not supply a coupling between them.

Consequently, the limit `Delta_n -> 2r` remains valid for an explicitly chosen comparison generator with total rate rn, but has not been derived solely from the insertion-site argument. In particular, a fixed-layer gap calculation is not automatically the spectral gap of the full size-changing process.

**Repair:** introduce separate comparison and growth generators and their rates. Specify whether a growth opportunity triggers a comparison, whether both clocks compete, or whether time is measured by growth-event count. These are distinct processes.

There is a promising conditional calculation: at a fixed layer let comparisons have per-edge rate alpha and growth have total hazard beta*n. An eigenmode with comparison decay rate alpha*(n−1), observed just before an independent exponential growth time, is attenuated in expectation by

`beta*n / [beta*n + alpha*(n−1)] -> beta/(beta+alpha)`.

This is a precise frozen-layer statement. A theorem across growth additionally needs the insertion operator's action on those modes. It must not be presented as a completed growing-system or physical mass-gap proof.

WHEELER-45 also combines Core-C event counts with a MICRO hidden-sector inference task. A shared state space and actual combined dynamics are needed to make this one endogenous observer model rather than an assumed cost analogy.

### R2. Memory capacity is not erased entropy

**Affected: WHEELER-49. Status: confirmed incorrect lower bound.**

The inference from an M-bit register to `Q_reset >= M k_B T ln 2` is not generally valid. In the standard reset setting the Landauer bound concerns entropy decrease, not allocated storage capacity [2]. For a classical memory distribution P reset to a known value, with the usual bath assumptions and no useful side information, its entropy contribution is `k_B T ln(2) H_bits(P)`.

A counter that is already known has zero Shannon uncertainty even if its representation uses many bits. If it is uniform on values 0,…,n, its entropy is log2(n+1), not necessarily the ceiling of that number. For n=21, five storage bits are needed, but uniform uncertainty over the 22 valid values is about 4.459 bits; a known counter value has zero uncertainty.

The source report moves from “at most M bits” to a lower bound proportional to M. That direction of inference is incorrect. Storage gives an upper bound on this entropy contribution, not a universal lower bound on heat; actual dissipation also depends on implementation and bath conditions.

**Repair:** specify the counter ensemble, retained side information, and reset protocol. Keep the distinction between storage, entropy and dissipation. Reversible counter updates are possible with appropriate inputs/side records, but deleting those records cannot simply be omitted from whole-device accounting. The earlier memory-versus-recomputation argument remains conditional on its operational cost model; WHEELER-49 does not derive an intrinsic thermodynamic cost from EHF.

### R3. “Finite observer cost” uses an infinite-history observation

**Affected: WHEELER-40–46, especially 45. Status: mismatch between information and resource units.**

The Beta-law Chernoff information is information from the exact limiting fraction of an infinite growth trajectory. WHEELER-45 divides that per-trajectory information by the expected work to detect one growth event. Those are not costs of the same experiment. Recovering the numerical optimizer n=21 is an optimization of the stated proxy, not a derivation of an optimal finite-budget experiment.

The earlier reports do sometimes flag the infinite-horizon assumption. That caveat must be carried forward when the observer is described as having a finite budget.

**Repair:** for L growth observations use the beta-binomial endpoint distribution

`P_D(A=a)=C(L,a) (alpha_D)_a (beta_D)_(L−a)/(alpha_D+beta_D)_L`,

where the parentheses denote rising factorials. Because the symbol process is exchangeable, the endpoint count retains its D-information for a fixed preparation. Charge preparation and observation costs for that same L-event experiment. Under the hypothetical equal-rate Core-C event competition, expected processed work across L growth events is `sum_{j=0}^{L−1}(n0+j−1)/2`, not just `(n0−1)/2`. Establishing that cost physically still requires R1's common model.

### R4. Event primacy is not full event symmetry

**Affected: WHEELER-55–57. Status: retain conditional theorem; narrow interpretation.**

The finite-set theorem in WHEELER-57 is correct: full permutation symmetry on a primitive event set implies uniform event probability, and push-forward gives probabilities proportional to target multiplicity.

But transformations being primitive does not imply every transformation has the same rate. Their source neighbourhoods, targets, or structural roles can distinguish them. WHEELER-55 already constructs nonuniform local rates compatible with the weaker symmetries. Maximum entropy also presupposes the reference sample space and specified constraints.

**Repair:** state the premises as “event-labelled alternatives plus admissibility-only maximum entropy/full event symmetry.” Both event-uniform and state-uniform constructions are mathematically coherent stochastic models. State-uniformity is incompatible with full event permutation symmetry when fibres differ; it is not incompatible with probability consistency itself. The choice of primitive comparisons alone has not eliminated measure selection.

### R5. A transcription error in the weighted entropy counterexample

**Affected: WHEELER-53. Status: independently confirmed; main negative result survives.**

For the explicit words `11000` and `11100`, n=5, D=2, q=0.05, and the insertion convention reproducing WHEELER-56's example:

| Probability on 11000 | Probability on 11100 | Entropy change, nats |
|---:|---:|---:|
| 0.345, as written | 0.655 | +0.1338801664 |
| 0.6554918178 | 0.3445081822 | −0.0126756464 |

The negative entropy change is real, but the source report reverses the probability assignment for those named words. Correct the word/probability pairing and state the root/insertion convention. At q=0.01 the reconstructed two-word optimum gives approximately −0.2089179624 nats, matching the reported scale.

## Other points to tighten

### The early reversal-to-current argument needs an explicit construction

WHEELER-11 asserts that an elementary reversal changes adjacent coarse boundary counts by exactly +1 and −1. The report does not define a concrete history embedding, observer partition and microscopic reversal sufficiently to prove that assertion. Conservation of an additive total does not by itself determine unit size, two-site support or nearest-neighbour locality.

Treat the transfer rule as a model assumption until a lemma derives it from explicit objects. WHEELER-12's algebraic conclusions are valid conditional on that integer transfer rule. This is a missing derivation, not a claimed numerical counterexample. It does not undermine the separately defined MICRO insertion counts.

### Markov claims need their precise hypotheses

WHEELER-34's strong-lumpability criterion is correct, but failure means the projection is not Markov for every initial law. It does not mean every particular preparation yields a non-Markov process. WHEELER-37 correctly supplies the qualification: with fixed preparation/prior, the embedded growth chain has an endpoint-sufficient posterior. Propagate that correction back into the earlier blanket language.

WHEELER-32 should restrict the exponential holding-time conclusion to the appropriate time-homogeneous, finite-rate pure-jump model. A time-homogeneous Markov semigroup in general can include continuous state evolution; Markovianity alone is not a universal exponential-waiting-time theorem.

### Timed likelihood needs rate-density factors

WHEELER-37's conclusion about endpoint counts plus total elapsed time is sound. Its discussion of adding timing factors to the embedded-chain likelihood is incomplete if used as a likelihood formula: an exponential density contributes its rate as well as its survival factor.

For L fully observed growth events, counts a,b, and complete holding times tau_j, the D-dependent joint likelihood under per-event rate r is proportional to

`(k0+D/2)_a (n0−k0+D/2)_b exp(−r D T)`, where `T=sum tau_j`.

The factors `r^L exp(−r sum n_j tau_j)` are common to D. The embedded-chain denominator `(n0+D)_L` cancels against the waiting-time rate factors. Do not use the discrete likelihood multiplied only by `exp(−rDT)`. Endpoint/time compression survives this correction.

### Complexity and locality are separate

WHEELER-47–48's O(1) counter update should identify a word-RAM or amortized model; binary increment is not worst-case O(1) bit operations. Access to a global cardinality counter also does not by itself establish a physically local observer implementation. These are modelling qualifications, not a refutation of the storage tradeoff.

### Keep existing corrections visible

WHEELER-25's expander interpretation was explicitly withdrawn in 26. The corrected normalized Core-C gap tends to zero. WHEELER-23's cycle component is a mobile subset of D=2; many other D=2 states are frozen under the chosen reversals. Neither an internal relaxation gap nor its closing should be identified with a quantum energy gap above a vacuum without an actual Hamiltonian and its energy reference.

## Results retained and independently checked

| Result | Review evidence | Assessment |
|---|---|---|
| Zero-cost MICRO states and reversal components | Complete enumeration n=4…14; all tabulated values through n=12 match | Retain in specified model |
| Translation-quotiented components | n=4…14; matches published sequence | Retain |
| Balanced/unbalanced growth merging, W19 | 6 and 48 source words; 26 and 156 descendants; intersection 26 | Retain |
| Growth preserves D; counts q0=n−N1+D/2, q1=N1+D/2 | Exact integer checks for every valid source n=4…14; local proof reviewed | Retain |
| Observer fibre-count formula, W50 | Exact rational/combinatorial check for every feasible macrostate n=4…14 | Retain; labelled-word convention |
| Uniform microscopic column bound, W52 | Every sector n=4…14; representative maxima reproduced | Retain; fixed event/root convention |
| Shannon growth under uniform kernel | Majorization argument reviewed; seeded distribution checks n=4…10 | Retain; measure-dependent |
| Symbol-biased protected family, W54 | Algebra checked by hand: numerator simplifies to `(k−1)Z(a+b)+ab(1+x+y)` and matches the report | Retain conditional on stated incoming-event representation |
| Run-biased failure of entropy monotonicity | Three maximum-column examples and two entropy decreases reproduced | Retain; correct R5 |
| Event/state distinction | `00111` has multiplicities 3,1,3 exactly | Retain |
| Core-C gap n−1 | Reconstructed graphs n=4…8; gaps 3,4,5,6,7; cited theorem verified [1] | Retain for the specified Hamilton-cycle/2-opt graph |
| Chernoff information | Beta(5,5) vs Beta(6,6): 0.00226480774; edge n=21: 0.01063077287 | Numerical values reproduced |
| Claimed n=21 cost optima | Edge-family search n=8…400 for C/n and C/(n−1) | Reproduced for those proxy objectives, not a universal physical optimum |

The Core-C argument has a sound route: anchor a vertex, represent cycles by permutations of n−1 labels modulo reversal, and restrict the substring-reversal operator to orientation-invariant functions. Full reversal becomes a removable loop. The known covering-graph gap gives a lower bound, while the edge-incidence eigenfunction supplies equality. The graph identification remains a stated condition; vertex counts alone would not uniquely identify an archived graph. The journal's authoritative bibliographic record gives volume 24(3), P3.4 (2017), although the PDF itself contains a 23(3) footer [1].

The Pólya-urn reduction follows directly from the verified insertion probabilities. Its hidden-sector interpretation is conditional on a fixed preparation and prior. The single-history versus repeated-preparation distinction is mathematically appropriate; no implication for physical quantum hidden variables follows.

## Coverage map

| Entries | Review status |
|---|---|
| 01–08 | Summary-level only; basic crossing/closure arguments plausible under regularity assumptions; physical interpretation and threefold selection remain conditional |
| 09–16 | Structural/model reasoning reviewed; no new full spectral sweep; W11 derivation needs explicit definitions |
| 17–24 | MICRO counts substantially reproduced; negative localization and relaxation conclusions remain limited to the model |
| 25–28 | Existing correction checked; published spectral theorem located and relevant quotient argument reviewed |
| 29–34 | Rate bridge and Markov/lumpability qualifications identified |
| 35–39 | Growth kernel reproduced; inference reasoning reviewed; timed likelihood clarified |
| 40–48 | Selected Chernoff calculations reproduced; resource mismatch and implementation assumptions identified; all optimization tables not exhaustively rerun |
| 49 | Erasure-capacity lower bound requires correction against primary source |
| 50–54 | Main combinatorial/entropy claims reviewed and finite checks reproduced; counterexample pairing corrected |
| 55–57 | Conditional finite-set probability arguments retained; stronger foundational interpretation not established |

## Recommended order of work

1. Record R1–R5 as errata and carry earlier corrections into a current status summary.
2. Put the explicit model conventions, reproducible code, and results beside the reports.
3. Proceed with WHEELER-58 using a fixed initial state, or an explicitly fixed initial distribution. Do not silently maximize entropy over initial sectors and histories together: sectors with different D have different continuation counts.
4. Prove horizon consistency for the chosen event process. Push-forward to observer histories preserves probability consistency when the observation maps commute with truncation; it does not automatically preserve Markov closure, uniformity or entropy monotonicity. State those as separate questions.
5. Treat the clock and finite-resource branches as separate repair tasks, rather than dependencies of the valid uniform-growth path-measure construction.

There is no need to discard the Wheeler series. The review supports a narrower, reproducible mathematical programme and identifies where its claims should stop.

## Primary external sources checked

[1] Fan Chung and Josh Tobin, *The Spectral Gap of Graphs Arising From Substring Reversals*, Electronic Journal of Combinatorics 24(3), P3.4 (2017), Theorem 1. DOI: https://doi.org/10.37236/6894 . Full text: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i3p4/pdf/ .

[2] David Reeb and Michael M. Wolf, *An improved Landauer Principle with finite-size corrections*, New Journal of Physics 16, 103011 (2014), especially the entropy-decrease formulation and assumptions. https://arxiv.org/abs/1306.4352 .

Repository snapshot: https://github.com/barzfen/emergent-horizon-framework/tree/106783d120bf5895cdcd67c8086ab382feebfb8c .
