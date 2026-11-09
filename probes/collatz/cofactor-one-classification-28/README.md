# COLLATZ-28 · Classify one-join returns to stripped cofactor one

[COLLATZ-27](../cofactor-pair-lifts-27/README.md) proves that fixing two stripped cofactors and the number of joins leaves only finitely many genuine histories. This note gives an exact classification for one join with both cofactors equal to $1$. **There are exactly seven joins.** The bound is global over positive starts.

Use the shortcut rule $T(x)=x/2$ on even inputs and $T(x)=(3x+1)/2$ on odd inputs. A join goes from the start of an odd run to the next odd-run start, after the intervening halvings. A stripped cofactor is the factor of $x+1$ remaining after removing all powers of two and three.

| Total exponent $q$ at the peak | Halvings $E$ | Starting values | Next odd-run start |
|---:|---:|---|---:|
| 1 | 1 | $1$ | $1$ |
| 2 | 3 | $3,5$ | $1$ |
| 4 | 4 | $15,23,35,53$ | $5$ |

Every nontrivial join on the list strictly decreases the starting value.

## Reduce the join to two logarithms

A start with stripped cofactor $1$ has $x+1=2^L3^a$, where $L\ge1$ and $a\ge0$. Put $q=L+a$. The $L$ odd steps end at $3^q-1$ and are followed by exactly $E=v_2(3^q-1)$ halvings. If the next odd start $y$ has the same stripped cofactor, then $y+1=2^R3^b$ with $R\ge1$, $b\ge0$. Hence

$$
2^{E+R}3^b=3^q+2^E-1. \tag{1}
$$

Conversely, for a given $q$, compute $E$ and $y=(3^q-1)/2^E$. If $y+1$ has stripped cofactor $1$, every split $q=L+a$ with $1\le L\le q$ gives the corresponding valid start $x=2^L3^{q-L}-1$.

For odd $q$, $E=1$ by reduction modulo four. For even $q=2^t m$ with $m$ odd, factoring $3^{2m}-1$ gives valuation three, since $3^m\equiv3\bmod8$. Each subsequent squaring adds one to the valuation. Thus $E=2+v_2(q)$ in the even case, and in all cases $2^E\le4q$.

Set $s=E+R$ and $n=q-b$. Equation (1) gives $s<1+q\log_2 3<3q$. Also $s\ge2$ and the right side is less than $2\cdot3^q$, so $b<q$ and $1\le n\le q$. We obtain

$$
0<\Gamma=2^s3^{-n}-1=\frac{2^E-1}{3^q}<\frac{4q}{3^q}. \tag{2}
$$

## Certify a finite cutoff

Use Matveev's positive-real product-minus-one bound with two bases, $2,3$, over the rationals. Take height parameters $\log 2,\log 3$ and the exponent bound $3q$, with natural logarithms. The coefficient $1.4\cdot30^5\cdot2^{4.5}\log 2\log 3$ is less than $10^9$. Thus (2) implies

$$
q\log 3<10^9(1+\log(3q))+\log(4q). \tag{3}
$$

For $q\ge10^{11}$, the function $q-10^9(1+\log(3q))-\log(4q)$ is increasing, and it is positive at $10^{11}$ since $\log(4\cdot10^{11})<30$. As $\log3>1$, inequality (3) proves $q<10^{11}$. [Explicit form of Matveev's bound, Theorem 2.3](https://link.springer.com/article/10.1007/s10998-025-00649-x)

Now let

$$
P=1193652440098,\qquad Q=753110839881,\qquad
\left|\log_2 3-\frac PQ\right|<\frac1{Q^2}.
$$

The last inequality is verified by rational upper and lower bounds for $\log 2$ and $\log 3$ in [verify.py](verify.py). In particular it does not depend on trusting a rounded decimal. The verifier uses the first 64 terms of $2\sum_{j\ge0}z^{2j+1}/(2j+1)$, where $z=(a-1)/(a+1)$ for $\log a$, with a geometric bound on the positive remainder.

Since $\gcd(P,Q)=1$ and $1\le n<10^{11}<Q/2$, the rational $s-nP/Q$ is nonzero and has magnitude at least $1/Q$. Therefore

$$
|s-n\log_2 3|>\frac1{2Q},\qquad
\Gamma>\log(1+\Gamma)=(s-n\log_2 3)\log 2>\frac1{4Q}.
$$

The sign of the linear form is positive by (2). Combining the inequalities gives $3^q<16Qq$. The exact integer comparison $3^{31}>16Q\cdot31$ and monotonicity of $3^q/q$ yield $q\le30$.

## Exhaust the remaining cases

The verifier checks $q=1,\ldots,30$ by integer arithmetic. Only $q=1,2,4$ give a destination of stripped cofactor $1$. It expands every admissible split $q=L+a$ and directly iterates the odd run and the halvings to the stated destination.

Run from this directory with standard-library Python:

    python3 verify.py

## Transfer and scope

The initial logarithmic bound also works with any fixed destination stripped cofactor $w$ and source cofactor $1$. In (2), replace the product $2^s3^{-n}$ by $2^s w3^{-n}$, adding the fixed base $w$ to the lower-bound theorem when $w>1$. The valuation bound $2^E\le4q$ still comes from the source cofactor $1$. The three-base estimate gives an effective preliminary bound depending on $w$. The small cutoff above specifically uses the homogeneous two-base form for $w=1$.

The classification concerns one join and this exact cofactor pair. It supplies no general mechanism forcing an orbit to reach the pair.
