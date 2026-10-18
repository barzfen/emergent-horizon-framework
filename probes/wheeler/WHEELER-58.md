# WHEELER-58 — Projective Measure / Multi-Step Consistency Audit

**Date:** 18 October 2026. **Status:** PROVED within the specified model; finite exact checks reproduced.

**Outcome:** the uniform-event growth law defines one consistent infinite process. Compatible observer projections remain consistent. State-uniform growth also defines a consistent process, so horizon consistency does not uniquely select event-uniformity.

Read [ERRATA-01](ERRATA-01.md) for the corrected assumptions inherited from 55–57.

## 1. Model, preparation and conventions

A microstate is a labelled binary tuple `w=(w_0,...,w_(n−1))`, n≥4, with cyclic adjacency and no isolated bit: cyclic 010 and 101 are forbidden. Rotation-related tuples are distinct at this stage. Let D(w) count cyclic domain walls; D is even, with D=0 for homogeneous words.

An event is `(i,b)`, where `0<=i<n`, `b in {0,1}`; its deterministic target is

`w[:i] + (b,) + w[i:]`.

Thus insertion is before one of n positions. There is no additional n-th slot. The root/representation convention is explicit; rotation quotienting is a different operation, not silently applied here.

An event is admissible if its target remains zero-cost. From WHEELER-36:

`D(target)=D(w)`, and `A(w)=|E(w)|=n+D(w)`.

Fix an initial size n0 and a probability law μ on its finite admissible microstate set, independent of the horizon. A deterministic start is a special case. μ may mix sectors, but must remain the same preparation as the horizon changes.

The event-uniform kernel is an additional measure choice:

`q(e|w)=1/(n+D(w))` for admissible e.

We do not derive this choice from event ontology alone. No physical clock, temperature, amplitude rule or Core-C comparison scheduler is assumed.

## 2. Exact finite-history law

Let a length-L event history be `h_L=(w0,e0,w1,...,e_(L−1),wL)`, with each target determined by its event. Define

`P_L(h_L)=μ(w0) product_{j=0}^{L−1} 1/(n0+D(w0)+j)`.

Invalid histories have weight zero. The empty product is 1. Within a fixed start w0, the number of length-L event histories is

`N_L(w0)=product_{j=0}^{L−1}(n0+D(w0)+j)`.

Every conditional history has weight 1/N_L, so the law is normalized. When μ is fixed, maximizing conditional history entropy gives this same law. Global entropy is `H(μ)+sum_w μ(w) log N_L(w)` at that maximum; optimizing over μ would be a different preparation problem.

## 3. Projective consistency and infinite extension

Let t_L drop the final event and state. For any admissible prefix h_L,

`sum_{e in E(wL)} P_(L+1)(h_L,e,target(e))`

`= P_L(h_L) sum_e 1/(n0+D(w0)+L)`

`= P_L(h_L)`.

Therefore `(t_L)_* P_(L+1)=P_L`. Repeated truncation gives consistency between any two finite horizons. In particular, computing farther into the future does not change the probability assigned to an already specified prefix.

Each layer and each event set is finite. The initial law and normalized transition kernels therefore extend uniquely to a probability measure on infinite admissible event histories, with the cylinder sigma-algebra. This is a direct application of the standard extension theorem for recursive probability kernels [1], not a new general probability theorem.

An explicit realization chooses the start using μ and then draws independent uniform numbers to select among an ordered list of the current admissible events. Each cylinder has exactly the finite-history probability above. Individual infinite event histories have probability zero because N_L grows without bound; the construction does not assign a positive uniform probability to each infinite path.

**Scope:** this is an event-indexed process. It makes no claim about a physical time parametrization or infinitely many growth events within finite physical time.

## 4. Observer-history consistency

Let an observer map a finite event history to a finite observation history via Φ_L. Require the family to commute with truncation:

`s_L Φ_(L+1) = Φ_L t_L`,

where s_L drops the last observable record. Coordinatewise observations `Y_j=π_j(w_j)` satisfy this; causal record updates can also satisfy it. A horizon-dependent reinterpretation of earlier observations need not.

Define `Q_L=(Φ_L)_*P_L`. Then

`(s_L)_*Q_(L+1) = (s_L Φ_(L+1))_*P_(L+1)`

`= (Φ_L t_L)_*P_(L+1) = (Φ_L)_*P_L = Q_L`.

Thus observer probabilities are projectively consistent without assuming the observer dynamics is Markov. Probability push-forward and Markov closure are separate claims.

For `π(w)=(n,N1,D)` the uniform-event macro kernel is strongly lumpable:

`P(insert 1)=(N1+D/2)/(n+D)`;

`P(insert 0)=(n−N1+D/2)/(n+D)`.

For `(n,N1)` alone, a universal kernel across hidden sectors fails: at n=9,N1=4, the probability of a 1-insertion is 5/11 for D=2 and 6/13 for D=4. Both sectors are feasible. This is a strong-lumpability counterexample, not proof of non-Markov behaviour for every preparation [2].

Under WHEELER-37's fixed `(n0,k0)` preparation and prior over D, the event-sequence likelihood depends only on the final insertion counts. Its posterior can be endpoint-sufficient, giving a preparation-dependent Markov description. The present consistency theorem covers that case as well.

## 5. A second consistent measure: uniform distinct target states

Let `T(w)` be the distinct rooted target words. The alternative kernel chooses each target with probability `1/|T(w)|`. If event histories are required, lift it symmetrically within target fibres:

`q_S(e|w)=1/[|T(w)| m_(target(e))(w)]`,

where m is the number of events reaching that target. This is normalized and hence defines a projectively consistent process by the same kernel construction. It need not respect full permutation symmetry of all primitive events.

There is a stronger fact in this specific representation.

### Distinct-target theorem

For a nonhomogeneous admissible rooted word with D domain walls,

`|T(w)|=D+1`.

For a homogeneous word, `|T(w)|=1`.

**Proof.** Write w as a linear list of maximal constant runs. Inserting the same bit at any location within, or immediately next to, one linear run gives one distinct word extending that run. Different linear runs give different target words: moving an insertion of bit b across a source symbol different from b changes the resulting tuple.

If the first and last bits agree, the cyclic root cuts a run, so the linear representation has D+1 runs. All admissible insertions extend one of them, producing D+1 targets. Inserting the opposite bit at the root would create an isolated bit and is inadmissible.

If the first and last bits differ, the linear representation has D runs. Extending each gives D targets. One additional admissible event inserts the last bit before position zero; it extends the last cyclic run across the root, and yields a distinct word beginning with a new first bit. All other admissible insertions are already among the linear-run extensions. Total: D+1. Homogeneous words have a single target. QED.

D is growth-invariant. Therefore, from a fixed nonhomogeneous start there are exactly `(D+1)^L` distinct state histories of length L. The state-uniform process assigns each probability `(D+1)^(-L)`. Consequently, even **global finite-horizon maximum entropy over distinct state histories** is horizon-consistent here.

This is stronger than merely observing that some alternative normalized kernel exists. Both reference choices support internally coherent maximum-entropy history constructions in this model.

### Concrete disagreement

From `00111`, both coherent processes give different predictions:

| Target | Event multiplicity | Event-uniform | State-uniform |
|---|---:|---:|---:|
| 000111 | 3 | 3/7 | 1/3 |
| 100111 | 1 | 1/7 | 1/3 |
| 001111 | 3 | 3/7 | 1/3 |

Horizon consistency therefore cannot distinguish these measures. Choosing a reference measure, symmetry class or physical sampling mechanism remains necessary.

The D+1 theorem depends on rooted target words. It must not be transferred unchanged to rotation-equivalence classes.

## 6. Three failure modes to avoid

### Changing the initial law while extending the horizon

Consider two n0=8 initial words, `00001111` (D=2) and `00110011` (D=4). If all complete event histories from either root are given equal weight without constraining the root prior, their initial probabilities change with L:

| Horizon L | Probability of D=2 start | Probability of D=4 start |
|---:|---:|---:|
| 0 | 1/2 | 1/2 |
| 1 | 5/11 | 6/11 |
| 2 | 55/133 | 78/133 |

This unconstrained family is not projectively consistent. Fixing μ=(1/2,1/2) and using conditional kernels resolves the problem. One cannot count more future continuations and silently reinterpret that as the same initial preparation.

### Uniform complete histories on an irregular tree

If the root has two successors a,b, with respectively two and three continuations, uniform length-one histories give P(a)=1/2 while uniform length-two histories give P(a)=2/5. Local normalized kernels remain consistent; unconstrained uniformity over complete histories need not.

Layer regularity explains why the event and distinct-state maximum-entropy constructions above work. It is not required for the existence of a general kernel-defined process.

### Inferring entropy monotonicity from consistency

Any horizon-independent normalized local weighting defines a consistent process, including the run-biased weighting from WHEELER-53 that can decrease microstate Shannon entropy. Thus projective consistency does not imply majorization, entropy nondecrease or a physical second law. Those depend on separate properties of the chosen kernel.

## 7. Reproducible exact audit

Run `python code/wheeler/projective_audit.py` from the repository root. It uses standard-library rational arithmetic and writes [wheeler-58-results.json](../../data/wheeler/wheeler-58-results.json).

- Every valid source at n=4…14: checked event count n+D, D conservation, macro insertion counts and distinct-target count D+1 (or 1 when D=0).
- Every initial word at n=4…8, under both measures: exact normalization, prefix marginalization and observer push-forward through horizon 3; **228 start/measure cases passed**.
- Observer maps checked: full word, `(n,N1,D)`, `(n,N1)`, first bit with n, and constant observation.
- `00111` through horizon 4: event-history counts **1,7,56,504,5040**. For state-uniform growth the corresponding distinct state-history counts are **1,3,9,27,81**, all equally weighted.
- Fixed mixed D=2/D=4 prior through horizon 3: consistency passed despite unequal branching between sectors.
- Run-biased event weighting q=1/20 through horizon 3: consistency passed, illustrating that consistency does not enforce the uniform measure.
- The hidden-D transition counterexample and the equality of 01/10 likelihoods for fixed preparation were checked exactly.

Finite checks support the implementation and examples. The all-horizon claims rely on the proofs above, not numerical extrapolation.

## 8. Verdict and next probe

- **PROVED:** uniform-event finite histories extend to one coherent infinite event-indexed process for a fixed preparation.
- **PROVED:** compatible observer-history maps preserve probability consistency.
- **PROVED:** rooted distinct-target count is D+1 in nonzero sectors; the state-uniform maximum-entropy history family is also consistent.
- **NEGATIVE:** projective consistency does not uniquely select event-uniformity.
- **NEGATIVE:** consistency alone does not imply observer Markov closure or entropy monotonicity.
- **NOT CLAIMED:** a unique physical measure, physical time law, quantum probability or thermodynamic second law.

**WHEELER-59 — Root/Rotation Quotient / Measure-and-Entropy Audit.** Determine which distinctions are due to the rooted representation, how the two measures behave under a precisely defined rotation quotient, and which lumpability/entropy conclusions survive. Specify how the root moves under insertion rather than assuming that forgetting it commutes with dynamics. This tests an independently meaningful invariance requirement instead of demanding that a preferred measure win.

## References

[1] Cosma Shalizi, *Building Infinite Processes from Regular Conditional Probability Distributions*, lecture 3, Theorem 33 (Ionescu Tulcea extension), Carnegie Mellon University (2006): https://www.stat.cmu.edu/~cshalizi/754/2006/notes/lecture-03.pdf .

[2] J. G. Kemeny and J. L. Snell, *Finite Markov Chains*, sections 6.3–6.4, on lumpability and dependence on initial law: https://math.pku.edu.cn/teachers/yaoy/Fall2011/Kemeny-Snell_Chapter6.3-4.pdf .
