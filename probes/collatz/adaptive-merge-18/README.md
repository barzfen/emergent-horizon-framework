# COLLATZ-18 · Choosing a meeting point after the odd run

[COLLATZ-17](../smaller-merge-17/README.md) gave families whose initial odd run defeats bounded searches for a smaller start. Here the length of that run selects a later meeting point. Two residue rules yield smaller starts with at least the same coefficient stopping time, even when the smaller start reaches the meeting point sooner.

## Transfer survival between different clocks

Let $T$ be the shortcut Collatz map. Write $P_j(n)=3^{a_j(n)}/2^j$ for its cumulative multiplier and $\kappa(n)=\min\{j\ge1:P_j(n)<1\}$, with $\kappa(n)=\infty$ if there is no contraction.

Suppose $T^s(n)=T^t(m)$, with $0<m<n$, and both prefixes survive through their meeting times. Put $a=a_s(n)$, $b=a_t(m)$, $P=P_s(n)$ and $Q=P_t(m)$. Suppose $Q\ge P$. For any $d\ge s$ with $d<\kappa(n)$, the shared suffix first gives survival of $m$ through $t+d-s$. At that time its multiplier is $(Q/P)P_d(n)\ge Q/P$. Each subsequent step multiplies by at least $1/2$. Thus $m$ survives through at least

$$
t+d-s+\lfloor\log_2(Q/P)\rfloor
=d+\lfloor (b-a)\log_2 3\rfloor.
$$

In particular, if $b\ge a$, then $Q\ge P$ suffices to preserve the entire original horizon even when $t<s$. Since both prefixes survive, $b\ge a$ and $t<s$ automatically imply $Q\ge P$. For such a merge, $\kappa(m)\ge\kappa(n)$ and $n$ cannot be the least survivor at any depth $d\ge s$.

For equal odd counts and $k=s-t\ge1$, there is also an exact equality test. Suppose $\ell=\kappa(n)$ is finite. At the original contraction, $1/2\le P_\ell(n)<1$, since only an even step can first contract. At time $\ell$ on the smaller path, the shared suffix has advanced $k$ extra steps on the original clock. Its multiplier is $P_\ell(n)3^c$, where $c$ counts odd inputs in the $k$ steps immediately after the original contraction. The transfer already guarantees survival through $\ell-1$. Therefore $\kappa(m)=\ell$ exactly when all those $k$ inputs are even. If any is odd, $\kappa(m)>\ell$.

## Two residue rules

Write an odd start as $n=2^Lu-1$, with $L=v_2(n+1)$ and $u$ odd. Choose $m=2^{L-1}u-1=(n-1)/2$. The two starts have initial runs of $L$ and $L-1$ odd steps, respectively. Put $w=3^Lu$. At the ends of these runs the values are

$$
x=w-1,\qquad z=w/3-1,\qquad x=3z+2.
$$

The following exact suffixes have equal lengths and give the same endpoint. A bit denotes the parity of the input to its step.

| Conditions | Suffix from $x$ | Suffix from $z$ | Meeting value |
|---|---|---|---|
| $L\ge4$, $w\equiv1\pmod4$ | $00$ | $01$ | $(3z+2)/4$ |
| $L\ge10$, $w\equiv43\pmod{256}$ | $01000001$ | $00011100$ | $(27z+152)/256$ |

In the first row $x\equiv0\bmod4$ and $z\equiv2\bmod4$. Two halvings from $x$ and an even step followed by an odd step from $z$ therefore meet. The smallest suffix multipliers are $1/4$ and $1/2$, and the initial odd runs provide enough multiplier for both when $L\ge4$. This two-step merger is the same identity used in LaDue's analysis of the consecutive pair $n,n-1$, since $T(n-1)=m$. Here the application is to coefficient stopping. [LaDue (2017), Example 1.1 and Theorem 4.1](https://arxiv.org/abs/1709.02979)

For the second row, $w\equiv43\bmod256$ gives $x\equiv42\bmod256$ and $z\equiv184\bmod256$. The stated parity words can be checked at $42$ and $184$, and remain valid on their residue classes. Their affine maps are $(9x+134)/256$ and $(27z+152)/256$, which agree at $x=3z+2$. The minimum suffix multipliers are $3/128$ and $27/256$, paid for by the initial odd runs when $L\ge10$. Related equal-odd-count common-future constructions appear in the rStation work on smaller sources. [*Smaller Collatz sources before first descent*, §3](https://rstation.ai/problems/collatz/papers/21)

In each row the smaller path uses one more odd step in the suffix and one fewer in the initial run, for equal total odd counts. It reaches the meeting point one shortcut step sooner, so $Q=2P$ and the transfer applies. The first row includes $15$ and $7$, which meet at $20$ after six and five steps. The second row includes $183295$ and $91647$, which meet at $371594$ after eighteen and seventeen steps.

For either row and any fixed admissible $L$, one may additionally require $3^h\mid n$ for any $h\ge1$. This imposes $2^Lu\equiv1\bmod3^h$ independently of the binary condition on $u$. The Chinese remainder theorem gives infinitely many choices. By COLLATZ-17, at every meeting point inside the initial odd run, a distinct alternate path with at least the original multiplier must use more than $s+h$ odd steps at original time $s$. These two rows reach beyond that run and bypass the restriction, even for arbitrarily large $h$.

## A lower bound on the lookahead for this partner

The choice $m=(n-1)/2$ does not give a bounded simultaneous search after the two initial runs. In fact, if $w\equiv3\bmod2^H$, then $z=(w-3)/3$ is divisible by $2^H$. With $w>3$, the next $H$ steps from $z$ are all halvings. From $x=3z+2$ each positive shortcut step takes a value to at least half that value. Hence for every $0\le j\le H$,

$$
T^j(x)\ge x/2^j>z/2^j=T^j(z).
$$

Thus there is no meeting at equal suffix lengths up to $H$ for the chosen partner. Such positive starts exist for arbitrarily large $H$ by taking $u\equiv3^{1-L}\bmod2^H$. We can also make both paths survive all of the tested steps by choosing $L$ with $(3/2)^{L-1}\ge2^H$. This is a limitation of the fixed partner and simultaneous suffix comparison. It leaves other partners, different suffix clocks and later meeting points open.

The two rules answer the adaptive selection question for explicit families and do not prove $m_d\to\infty$. The arithmetic checks replayed 912 pairs from the two families, including exact coefficient stopping times and the equality test, and 84 controls from the unresolved residue classes.
