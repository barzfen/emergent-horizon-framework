# COLLATZ-17 · Smaller starts and the limits of short merges

[COLLATZ-16](../survival-count-16/README.md) leaves the location of the least surviving start $m_d$ open. Here a merge into the same orbit excludes an explicit arithmetic progression from being least. A divisibility argument also shows why this particular test needs unbounded search depths.

Use the shortcut map $T(n)=n/2$ on even inputs and $T(n)=(3n+1)/2$ on odd inputs. A prefix of $s$ steps with $a$ odd inputs has multiplier $3^a/2^s$. A prefix survives if each of its cumulative multipliers is at least one.

## A smaller start can inherit survival

Suppose $T^s(n)=T^t(m)$ for $0<m<n$. Write $P$ for the multiplier from $n$ to the meeting value and $Q$ for the multiplier from $m$ to that value. If $Q\ge P$ and the $t$-step prefix from $m$ survives, then any $d$-step survival of $n$, for $d\ge s$, gives $(d-s+t)$-step survival of $m$. Indeed, after the meeting point the two trajectories have the same multiplier factors. Before the meeting point the survival of $m$ is part of the hypothesis.

When $t\ge s$, the comparison excludes $n$ from being $m_d$ at every depth $d\ge s$. For infinite survival, the restriction $t\ge s$ is unnecessary. Related common-future and multiplier comparisons are discussed in the [rStation inverse-minima thread](https://rstation.ai/r/collatz/posts/2).

### A progression of multiples of three

For $k\ge0$, take

$$
n=273+1458k,\qquad m=191+1024k.
$$

The single odd step from $n$ and the ten steps with parity word $1111110100$ from $m$ meet at $410+2187k$. The ten-step affine map is

$$
T^{10}(m)=\frac{2187m+2123}{1024}.
$$

At $m=191$ the prefix visits $191,287,431,647,971,1457,2186,1093,1640,820,410$. The translation by $1024k$ preserves the ten parities by the finite parity-residue bijection. The only places where the multiplier decreases are steps 7, 9 and 10. At those steps it is $729/128,\ 2187/512,\ 2187/1024$, respectively. All exceed one, and the last exceeds the original multiplier $3/2$.

Thus every surviving start in this progression has a smaller start that survives nine more steps. The argument works even though $n$ is a multiple of three. Such an $n$ has only even-step prehistories into $n$ itself, since no odd step outputs a multiple of three and doubling preserves divisibility by three. This example uses a meeting point one step farther along. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252)

## A divisibility bound for all-odd prefixes

**Proposition.** Let $h=v_3(n)$, the exponent of three dividing $n>0$. Suppose the first $s$ steps of $n$ are all odd, allowing $s=0$. An alternate path of length $t$ with $b$ odd steps into the same endpoint, whose multiplier is at least $(3/2)^s$, must satisfy

$$
b>s+h
$$

unless it is exactly the original path. When $h\ge1$, any such alternate path has at least two even steps and therefore $t\ge s+h+3$. At $s=0$ and $h\ge1$ no such alternate path exists.

**Proof.** The true endpoint and a comparison endpoint are

$$
y=(3/2)^s(n+1)-1,\qquad y_0=(3/2)^s-1.
$$

They differ by $3^s n/2^s$, which is divisible by $3^{s+h}$ in the ring of rationals with a power-of-two denominator. Reverse the alternate path from both endpoints, using $z\mapsto 2z$ for an even step and $z\mapsto(2z-1)/3$ for an odd step. In this ring, the latter operation stays in the ring precisely when $z\equiv2\bmod3$. Each reverse odd step consumes one power of three in the difference, and a reverse even step preserves it. Hence if $b\le s+h$, all the operations also stay in the ring when started at $y_0$.

A multiplier at least $(3/2)^s$ requires $t\ge s$, because each forward step contributes at most $3/2$. At reverse time $j\le s$, the value started from $y_0$ is at least $(3/2)^{s-j}-1$. Both inverse branches are increasing functions, and for nonnegative inputs $2z>(2z-1)/3$. Thus the all-odd reverse path gives the lower bound, with strict inequality after any even branch within those $s$ steps. Each reverse step removes at least one power of two from a nonintegral denominator, so after $s$ steps the comparison value is a nonnegative integer. Once integral, every legal reverse operation preserves nonnegativity and cannot take a positive value to zero.

Write $m_0$ for the resulting comparison start and $Q=3^b/2^t$ for the alternate multiplier. The forward affine formula for that path gives $y_0=Qm_0+C$ with $C\ge0$. Since $Q\ge(3/2)^s>y_0$, the integer $m_0$ must be zero. This requires the first $s$ reverse steps to be odd and all later steps to be even, since the only legal inverse at zero is doubling. If there were later steps, $Q=(3/2)^s2^{-(t-s)}<(3/2)^s$. So $t=s$ and the path is exactly the original.

For $h\ge1$, reversing all $s$ original odd steps reaches $n\equiv0\bmod3$, where any further reverse steps can only double. Since an alternate path needs $b>s+h$, its first deviation must occur before then. At that deviation, the original reverse state is $2\bmod3$, since at least one of the original odd steps still precedes it. The alternate even inverse doubles it to $1\bmod3$. Its next step must also be even, and a next step is required because it still needs more than $s$ odd steps in total. This proves the extra two-step bound.

## What bounded merge searches leave out

For any positive integers $D$ and $R$, the simultaneous conditions

$$
n\equiv-1\pmod{2^D},\qquad n\equiv0\pmod{3^R}
$$

give an infinite positive arithmetic progression. These starts have $D$ initial odd steps, so they survive through $D$. At every meeting point $T^s(n)$ for $0\le s\le D$, the proposition excludes all distinct alternate paths of length at most $R$ with at least the original multiplier. This holds even before requiring survival along the alternate path.

A comparison limited to those two fixed depths therefore leaves an entire progression among the finite survivors. The result does not determine what happens after the all-odd prefix, or whether a longer merge works. The limit $m_d\to\infty$ remains open.

## Exact checks

The divisibility bound $b>s+v_3(n)$ was checked independently by enumerating all inverse branches through length 12 from the first eight all-odd endpoints, where available, of every odd $n<2^{13}$. Among paths with $m\ne n$ and $3^b2^s\ge3^s2^t$, all 13,545 passed. The two paths in the progression example were also iterated directly for $0\le k<100$. The proposition and the affine identities give the infinite statements.
