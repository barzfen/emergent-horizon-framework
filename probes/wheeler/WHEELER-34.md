# WHEELER-34 — Lumpability / Emergent-Memory Audit

## Question
When does an observer projection of a Markov-complete EHF substrate remain Markov, and when does coarse-graining generate apparent memory?

## Setup
Let the full substrate state be a continuous-time Markov state X with generator q(x,z). Let the observer see only Y = pi(X), where pi partitions microscopic states into observable macrostates.

## Exact criterion
The projection is strongly lumpable iff for every pair x,x' with pi(x)=pi(x')=y, and for every observable macrostate y',

    sum_{z: pi(z)=y'} q(x,z) = sum_{z: pi(z)=y'} q(x',z).

If this holds, the observer-level generator is well defined by the common value above, and Y is Markov for every initial distribution.

If the equality fails for even one target macrostate, then two hidden microstates that look identical to the observer have different future hazards. The observer's next-step statistics therefore depend on the posterior distribution over hidden states within the current macrostate, and that posterior generally depends on past observations. Hence memory can emerge under projection. Failure of strong lumpability rules out a single preparation-independent macro kernel; it does not imply non-Markov behaviour for every fixed initial law. WHEELER-37 gives a preparation-dependent Markov example.

## Minimal example
Take hidden states a,b with pi(a)=pi(b)=A and visible state c with pi(c)=B. Suppose q(a,c)=1 while q(b,c)=3. Then the visible hazard A->B is not determined by A alone. It depends on the conditional probability of being in a versus b, which is history-dependent. The substrate is Markov; the projection is not.

## EHF interpretation
- Full-state Markov sufficiency and observer-level memory are compatible.
- Memory need not be fundamental; it can arise because observer records coarse-grain distinct substrate states.
- The relevant technical object is not merely a projection but whether the observer partition is lumpable.
- Exact symmetries can produce lumpable observables: if all microstates in an observer class have identical aggregated rates to every observer class, Markov behavior survives.
- Broken lumpability gives an operational measure of hidden-state relevance.

## Relation to prior Wheeler probes
WHEELER-32 showed that history composition alone does not imply a semigroup. WHEELER-33 identified a possible Markov lift on an augmented state tuple. WHEELER-34 now specifies exactly when projecting that lift preserves the Markov property.

## Verdict
PASS: exact lumpability criterion identified.
PASS: failure of the criterion removes a universal Markov closure; particular initial laws can still yield a Markov projection (see WHEELER-37).
PASS: Markov substrate and emergent observer memory are mathematically compatible.
UNRESOLVED: which existing EHF observer variables or quotients are lumpable under the actual transition generator.

## Recommended next probe
WHEELER-35 — Observer Partition / Lumpability Audit: choose one concrete EHF coarse-graining already used in prior observer/record work and test the aggregated transition-rate equality explicitly. If it fails, quantify the induced memory by comparing hidden-state posteriors after different observed histories.