# WHEELER-37 — Observer-Memory Kernel / Hidden-D Reconstruction Audit

## Goal
Integrate out the growth-stable hidden domain-wall sector D from the zero-cost MICRO growth process and determine the exact effective dynamics seen by an observer who records only n and N1.

## Starting point
For a zero-cost cyclic word of size n with N1 ones and domain-wall count D, WHEELER-36 proved the admissible insertion counts

q0 = n - N1 + D/2,
q1 = N1 + D/2,

where q0 is the number of admissible insertions that leave N1 unchanged and q1 the number that increase N1 by one. The total count is

qtot = n + D,

and D is conserved by zero-cost growth.

## Embedded discrete growth chain
Condition on one growth event having occurred. Then

P(Delta N1 = 1 | n,N1,D) = (N1 + D/2)/(n + D),
P(Delta N1 = 0 | n,N1,D) = (n - N1 + D/2)/(n + D).

This is exactly a two-colour Polya-urn law with symmetric pseudo-count D/2 added to the two insertion types.

Let the initial observed state be (n0,k0), with k0=N1, and let pi0(D) be the observer's prior over the hidden D sector. After m growth events, suppose a inserted symbols were 1 and b=m-a were 0, so that

n = n0 + a + b,
k = k0 + a.

For a particular observed increment sequence, the D-dependent likelihood is

L_D(a,b)
= [(k0 + D/2)^(overline a) (n0-k0 + D/2)^(overline b)]
  / [(n0 + D)^(overline {a+b})],

where x^(overline m) is the rising factorial.

Crucially, L_D depends only on a and b, not on the order of the observed increments. Therefore

pi(D | observed history)
propto pi0(D) L_D(a,b)

depends only on the current endpoint (n,k), given the fixed preparation (n0,k0,pi0).

## Consequence: strong vs weak lumpability
The projection onto N1 is not strongly lumpable: at the same visible (n,k), distinct hidden D values have different microscopic transition probabilities and, in continuous time, different exit rates.

However, for a fixed initial preparation and prior over D, the discrete embedded growth chain is weakly lumpable. Its posterior over D is a function of the current endpoint only, so the next-step probability can be written

P(Delta N1=1 | n,k)
= sum_D pi_{n,k}(D) (k + D/2)/(n + D),

with pi_{n,k}(D) determined from the endpoint formula above.

Thus the previously stated idea that the full ordered N1 history is always required was too strong. In the embedded discrete chain, the event-order memory collapses to the current endpoint plus the fixed preparation/prior.

## Exact finite hidden-state filter
If the initial size is finite, only finitely many D sectors are admissible. The observer can therefore carry the finite posterior vector

Pi_t = {pi_t(D)}_D.

After observing the next increment x in {0,1}, update by Bayes:

pi_{t+1}(D)
propto pi_t(D) P(x | n_t,k_t,D).

The augmented observer state (n_t,k_t,Pi_t) is exactly Markov. No phenomenological memory kernel is required.

## Continuous-time version
Under the local-rate law from WHEELER-30/31, let each admissible insertion site fire at rate r. Then the total exit rate is

R(n,D)=r(n+D).

If the observer also measures complete holding times tau_j, each exponential density contributes

r(n_j+D) exp[-r(n_j+D) tau_j].

Multiplying these densities by the embedded symbol likelihood cancels its denominator (n0+D)^(overline m). Therefore, for a observed 1-insertions and b observed 0-insertions, the D-dependent joint likelihood is proportional to

[(k0+D/2)^(overline a) (n0-k0+D/2)^(overline b)] exp[-r D T].

The omitted factor r^m exp[-r sum_j n_j tau_j] is common to all D. Do not multiply the embedded likelihood only by the survival exponent: that would omit the rate-density factors.

The D-dependent waiting-time contribution depends on the elapsed time only through

exp[-r D T],

where T=sum_j tau_j. Hence the posterior can be compressed to endpoint counts plus elapsed internal time T; the detailed ordering of waiting times is unnecessary.

This yields a useful hierarchy:

- full substrate word: Markov;
- (N1,D): strongly lumpable/Markov for the growth process;
- N1-only, arbitrary preparation: not strongly lumpable;
- N1-only, fixed preparation/prior, embedded event chain: weakly lumpable because the hidden-sector posterior is endpoint-sufficient;
- N1-only continuous-time description: preparation/clock information matters through the hidden-D posterior; augmenting with the posterior restores Markov closure.

## Interpretation
The correct emergent-memory statement is subtler than WHEELER-35 initially suggested. Forgetting D does not necessarily produce irreducible path-order memory. Instead it produces hidden-sector uncertainty and preparation dependence. In this model the exact memory state is a finite Bayesian belief over D.

The observer's effective non-Markovianity is therefore epistemic/coarse-graining-induced relative to the reduced state description, while the full substrate dynamics remains Markov-complete.

## Verdict
- PASS: exact hidden-D Bayesian filter derived.
- PASS: conditional growth dynamics is a Polya-urn process.
- PASS: N1 projection is not strongly lumpable.
- PASS: for a fixed preparation/prior, the embedded event chain is weakly lumpable and endpoint-sufficient.
- CORRECTION: ordered event history is not generically required once the preparation/prior is fixed.
- PASS: augmenting the observer state by the posterior over D restores exact Markov closure.
- OPEN: characterize identifiability of D from one long trajectory and determine whether observer-relative time can make the hidden sector operationally measurable.

## Next probe
WHEELER-38 — Hidden-Sector Identifiability / Long-History Audit.

Question: from one arbitrarily long observed N1 trajectory (with or without event times), can an internal observer infer D uniquely, or does D remain permanently underdetermined despite infinite data?
