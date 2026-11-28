# EHF-GROW02 LR3 Onset Support-Limit Audit v0.2

## Question
Does the exact GROW-02 one-step rule support a half-density limit for LR3, and what initial condition does the canonical source specify?

## Source check
The attached cumulative GROW working document defines, at parent size \(n\),

\[
P_n(\ell,\ell)=\frac{n+1-\ell}{n+2},\qquad
P_n(\ell,\ell+1)=\frac{\ell+1}{n+2}
\]

for generic support, with the half-cycle boundary folded by colour exchange. It defines the unfolded coordinates by \(a=j+1\), \(b=n+1-j\), and \(\ell=\min(j,n-j)\). Thus \(\{a,b\}=\{\ell+1,n+1-\ell\}\), and the displayed recurrence is exactly the standard two-colour Pólya update after normalizing by total \(a+b=n+2\).

GROW-02 states the first size for support \(\ell\) is \(n=2\ell\). The LR3 onset is therefore \((n_0,\ell_0)=(6,3)\), giving \((a_0,b_0)=(4,4)\).

## Exact conclusion under the stated sampling convention
If each relation lift is sampled uniformly, the unfolded Pólya fraction converges in distribution to

\[
X_\infty\sim\operatorname{Beta}(4,4).
\]

Hence \(\mathbb E X_\infty=1/2\), but \(\operatorname{Var}(X_\infty)=1/36\). The limit is random and non-degenerate; there is no deterministic limiting density equal to one half. The half-mean is a consequence of the balanced initial LR3 onset state. For fixed \(\ell_0\) while taking \(n_0\to\infty\), the distinct family \(\operatorname{Beta}(\ell_0+1,n_0+1-\ell_0)\) has mean tending to zero.

## What this resolves
- The recurrence in the prior proposed computation matches the GROW-02 operator.
- The relevant canonical LR3 initial state is its onset at size 6, not an arbitrary large parent with support 3.
- The earlier claim that the half-mean route closes for LR3 was too broad. The corrected statement is that the onset-conditioned mean is one half, but the limiting fraction has persistent fluctuations.

## What it does not establish
This does not identify a critical point. It supplies no LR2 spectral scaling calculation, no scale-invariance result, and no CFT bridge. Beta convergence is conditional on uniform relation-lift sampling; the raw lift census alone is combinatorial rather than a physical probability law.
