# WHEELER-45 — Internal Observer Budget / Endogenous Cost Audit

## Goal

Make the observer explicit and derive an operational processing cost from native EHF event counts rather than choosing a resource law after the fact.

We use the two event families already established in the Wheeler/Core-C branch:

- growth opportunities
  \[
  G_n=n,
  \]
- Core-C comparison opportunities
  \[
  d_n=\frac{n(n-3)}2.
  \]

The observer has a finite event-processing budget and samples substrate events according to their occurrence rates.

## Equal local-rate model

Assume every elementary growth opportunity and every elementary comparison opportunity carries the same local hazard and that processing one observed event costs one unit.

The total native event pool at size \(n\) is

\[
G_n+d_n
=n+\frac{n(n-3)}2
=\frac{n(n-1)}2.
\]

Hence the fraction of substrate events that are growth events is

\[
p_{\rm grow}(n)
=\frac{G_n}{G_n+d_n}
=\frac{n}{n(n-1)/2}
=\frac{2}{n-1}.
\]

Therefore the expected number of processed substrate events required to encounter one growth event is

\[
\mathbb E[W_n]
=\frac1{p_{\rm grow}(n)}
=\frac{n-1}{2}.
\]

Thus the observer's effective processing cost per informative growth event is linear in \(n\), derived from the native event competition rather than inserted by hand.

## Unequal local-rate model

Let each comparison opportunity have local hazard \(\alpha\) and each growth opportunity local hazard \(\beta\), independent of \(n\).

Then the total rates are

\[
R_C(n)=\alpha d_n,
\qquad
R_G(n)=\beta n.
\]

The growth fraction among all substrate events is

\[
p_{\rm grow}(n)
=\frac{\beta n}{\beta n+\alpha d_n}
=\frac{\beta}{\beta+\alpha(n-3)/2}.
\]

Hence

\[
\mathbb E[W_n]
=\frac1{p_{\rm grow}(n)}
=1+\frac{\alpha(n-3)}{2\beta}
\sim \frac{\alpha}{2\beta}n.
\]

So the linear scaling is robust under any fixed, size-independent local rate ratio \(\alpha/\beta\).

## Finite observer budget

Suppose the observer can process only \(B\) substrate events at layer \(n\).

The expected number of observed growth events is

\[
\mathbb E[N_G^{\rm obs}]
=B p_{\rm grow}(n).
\]

For equal local rates,

\[
\mathbb E[N_G^{\rm obs}]
=\frac{2B}{n-1}.
\]

Thus with fixed \(B\),

\[
\mathbb E[N_G^{\rm obs}]\to0
\qquad (n\to\infty).
\]

The probability of seeing at least one growth event in the budget window is

\[
P_{\ge1}
=1-(1-p_{\rm grow})^B.
\]

For fixed \(B\), \(P_{\ge1}\to0\).

To maintain a fixed target detection probability \(q\in(0,1)\), the required budget is

\[
B_q(n)
=\frac{\log(1-q)}{\log(1-p_{\rm grow}(n))}.
\]

Using \(p_{\rm grow}(n)\sim2/n\),

\[
B_q(n)
\sim -\frac{n}{2}\log(1-q).
\]

More generally, with fixed local-rate ratio \(\alpha/\beta\),

\[
B_q(n)
\sim -\frac{\alpha}{2\beta}n\log(1-q).
\]

Therefore the critical observer processing budget is linear in system size:

\[
\boxed{B_n=\Theta(n)}.
\]

This matches the critical linear rate scaling identified independently in WHEELER-28 through WHEELER-31.

## Link back to hidden-sector discrimination

For the WHEELER-41 edge preparation used to distinguish \(D=2\) from \(D=4\), the Chernoff information per preparation is \(C_{\rm Ch}(n)\).

Under equal local rates, the endogenous event-processing cost per observed growth event is

\[
W(n)=\frac{n-1}{2}.
\]

The natural observer-efficiency objective is therefore

\[
\eta(n)=\frac{C_{\rm Ch}(n)}{W(n)}
=\frac{2C_{\rm Ch}(n)}{n-1}.
\]

Scanning the shared feasible edge family \(N_{1,0}=4\) (or symmetrically \(n_0-4\)) gives the optimum at

\[
\boxed{n_0=21}.
\]

At this point

\[
C_{\rm Ch}\approx0.01063077,
\]

and

\[
\eta\approx1.06308\times10^{-3}
\]

per processed substrate event unit under this normalization.

Thus the \(n_0=21\) optimum from WHEELER-42 is recovered without assuming an abstract linear cost law: it follows from explicit competition between \(O(n)\) growth opportunities and \(O(n^2)\) comparison opportunities, provided the observer samples the native event stream and pays equal cost per processed event.

## Interpretation

The result is conditional, not universal.

It requires:

1. a native event stream containing both growth and comparison events;
2. size-independent local hazards for each event type;
3. an observer that samples/processes those events according to occurrence frequency;
4. approximately equal unit processing cost per event.

Under those assumptions, the linear observer cost is derived rather than chosen.

If the observer can selectively query growth events, ignores comparison events at zero cost, uses nonlocal summaries, or faces size-dependent local hazards, the scaling can change.

## Verdict

- **PASS:** native EHF event counts imply
  \[
  p_{\rm grow}(n)=2/(n-1)
  \]
  under equal local rates.
- **PASS:** expected processing work per growth event is
  \[
  (n-1)/2=\Theta(n).
  \]
- **PASS:** a fixed observer budget asymptotically loses access to growth events.
- **PASS:** maintaining a nonzero growth-detection probability requires
  \[
  B_n=\Theta(n).
  \]
- **PASS:** the same linear scaling survives unequal but size-independent local rate constants.
- **PASS:** using this endogenous cost recovers the finite discrimination optimum \(n_0=21\).
- **CONDITIONAL:** the derivation depends on the observer sampling the native event stream with finite per-event processing cost.
- **OPEN:** derive the observer architecture itself from EHF primitives rather than positing a sampling rule.

## Main structural lesson

\[
\boxed{\text{observer limitation can emerge from event competition, not from an imposed size penalty}.}
\]

More specifically, the coexistence of \(O(n)\) growth opportunities and \(O(n^2)\) comparison opportunities naturally produces a linear processing burden for an observer trying to remain sensitive to growth.
