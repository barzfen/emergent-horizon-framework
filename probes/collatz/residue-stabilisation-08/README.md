# COLLATZ-08 · When fitting residues force an actual orbit

[COLLATZ-07](../residue-size-07/README.md) constructed coefficient survivors whose early residues are too large for a polynomially bounded orbit. Here we examine the other outcome, when the residues fit the bound.

**PROVED.** At one scale, sufficiently small adjacent representatives give an exact finite orbit segment. Across scales, if a fixed denominator passes often enough, its decoded starting numerator stabilises. For the parameters in COLLATZ-07, passing at lower density greater than $24.466\ldots\%$ among dyadic scale indices suffices. The lower-density threshold is sharp for the single-window residue test on unrestricted parity words.

## Fitting windows at one scale

Fix an odd positive denominator $q$. In the fixed-denominator map $T_q$, an even numerator $p$ goes to $p/2$ and an odd numerator goes to $(3p+q)/2$. As in [COLLATZ-05](../multiplier-band-05/README.md), a length-$d$ parity word determines one numerator residue modulo $2^d$. The case $q=1$ is Terras's parity coding. Multiplying an odd-denominator rational orbit by its denominator gives this same numerator map. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252) · [Bernstein and Lagarias (1996), §§1 and 4](https://websites.umich.edu/~lagarias/doc/bernstein.pdf)

Suppose the length-$d$ windows at positions $0,\ldots,N-1$ each have a representative $p_i$ with $|p_i|\le X$. Since neighbouring windows overlap in $d-1$ bits,

$$
T_q(p_i)\equiv p_{i+1}\pmod{2^{d-1}}.
$$

But $|T_q(p_i)-p_{i+1}|\le (5X+q)/2$. If $2^d>5X+q$, the congruence is therefore an equality for every adjacent pair. Each representative really follows its own length-$d$ window by parity coding. So the full length-$(N+d-1)$ parity prefix is realised by the rational start $p_0/q$. This is a finite statement. The representative of the starting window could change when the scale changes.

## Fitting at many scales locks the starting value

At scale $m\ge1$, take $N_m=2^m$ and inspect the first $D m$ parity bits, for an integer $D\ge2$. Let $r_m$ be the representative in $[-2^{Dm-1},2^{Dm-1})$ of the starting numerator modulo $2^{Dm}$. Fix $K>0$ and $0<s<D$. Say a scale fits if $|r_m|\le K2^{s m}$.

For two fitting scales $m<m'$, compatibility gives $r_{m'}\equiv r_m\pmod{2^{Dm}}$. If they differ, then

$$
2^{Dm}\le |r_{m'}-r_m|\le 2K\,2^{s m'},
\qquad
m'\ge \frac{D}{s}m-\frac{\log_2(2K)}{s}.
$$

Thus a change in the decoded start requires a gap between fitting scales when these are consecutive fits. In particular:

- If every sufficiently large scale fits, the decoded start eventually stays constant. More generally, infinitely many fits suffice if the ratios of successive fitting indices are eventually bounded by a fixed number strictly below $D/s$.
- More generally, if the set of fitting indices has lower asymptotic density greater than $s/D$, the decoded start also stabilises along the fitting indices. Indeed, if it changed infinitely often between consecutive fits $m,m'$, at index $m'-1$ there would be at most $m$ fits. Along those pairs the fraction of fits is at most $m/(m'-1)\le s/D+o(1)$, contradicting the lower-density hypothesis.

In either case the constant numerator $p$ realises arbitrarily long prefixes and thus the whole word. For $q=1$, requiring $2\le r_m\le K2^{s m}$ at the counted scales makes the resulting start a positive integer greater than one. The same proof applies to this stricter test. If the stronger test on **all** early windows fits on that many scales, its first window already provides the hypothesis.

## The consequence for the open Collatz case

Suppose the word is a coefficient survivor with $1\le P_i=O((i+1)^\beta)$. Set $s=\beta+1$ and choose $D>s$. For any genuine fixed-denominator orbit, COLLATZ-05 bounds all its first $N_m$ numerator values by $K N_m^s$ for some fixed $K$. At sufficiently large scales these actual numerators are the signed representatives. Thus a genuine positive integer lift greater than one passes the positive starting-window test and the full size bound eventually. Conversely, eventual positive fits, or positive fits at lower density greater than $s/D$, give that genuine lift.

With $\beta=4\log_2 3$ and $D=30$, as in COLLATZ-07, $s/D=0.2446616667\ldots$ and $D/s=4.08727\ldots$. The multiplier is at least one at every step, and the nonnegative affine offset ensures that an orbit starting at $n>1$ never falls below $n$. So a positive lift here would be a counterexample to Collatz. The reconstruction criterion does not produce such a lift or prove that none exists. It characterises the persistent-fit case within this polynomially bounded coefficient-survivor class. [Lagarias (1985), first descent and coefficient stopping times](https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/node5.html)

## Sharpness for the single-window test

Let $u_j=2^{j^2}$ and consider the 2-adic numerator

$$
x=\sum_{j\ge1}2^{D u_j}.
$$

This is irrational. If $x=p/q$ for odd $q>0$, the truncation $S_j=\sum_{i\le j}2^{D u_i}$ would satisfy $qS_j\equiv p\pmod{2^{D u_{j+1}}}$. For large $j$, $0<|qS_j-p|<2^{D u_{j+1}}$, a contradiction.

For $u_j<m\le u_{j+1}$, the signed representative of $x$ is $S_j$, since $D\ge2$ and $S_j<2^{D u_j+1}$. In this interval the test with $K=1$ first fits at $b_j=\lceil\log_2(S_j)/s\rceil=(D/s)u_j+O(1)$, then fits through $u_{j+1}$. Since $u_{j+1}/u_j\to\infty$, the fit fraction tends to one along $u_j$. During each failure block the fraction decreases and during each fitting block it increases. Its minima at $b_j-1$ tend to $s/D$. Hence fits can have upper density one and lower density exactly $s/D$ even for an irrational lift.

This control uses the first window alone and imposes no coefficient-survival condition on the full word. It can also be made to match any prescribed finite parity prefix by placing its high bits above the desired residue and fixing the low bits to that residue. This changes the estimates only by a bounded amount. It does not establish sharpness within the infinite coefficient survivor tree or for the full set of fitting windows.

The argument uses the classical parity congruence cited above. The finite stitching, density argument and sharpness control are given here with no priority claim. We checked the finite reconstruction against signed rational trajectories for five odd denominators and checked the fit transitions of initial truncations in the control. AI assistance was used for derivation, checks and drafting.
