# COLLATZ-26 · What does a cofactor observer preserve?

This is a transfer audit from the main EHF repository to the Collatz recurrence question. The direct transfer is the observer test from [MICRO observer compatibility](../../micro/observer-compatibility-01/REPORT.md): check whether two underlying histories that look identical to an observer have the same continuation. [WHEELER-59](../../wheeler/WHEELER-59.md) supplies a positive example of a compatible projection under a specified kernel. [QM bridge revisit 02](../../qm-bridge/revisit-02/REPORT.md) supplies a complementary example in which a history carries orientation information hidden by the carrier observation. Here there is one deterministic Collatz move at each state, so the observer test compares exact next observations.

**Results.** For a modulus divisible by four, no finite record of modular cofactors and completed run lengths determines the next modular cofactor. In contrast, two consecutive **exact** stripped cofactors and the three intervening run lengths determine both underlying positive integers. Individually valid coarse joins can be concatenated precisely when their reconstructed middle integers agree.

## A modular observer with no finite memory bound

Let $x_i$ be successive odd-run starts of the shortcut map. At $x_i$, put $x_i+1=2^{L_i}3^{a_i}w_i$, with $w_i$ coprime to six. Let $E_i$ be the number of even steps between that odd run and the next one.

Fix a modulus $Q$ divisible by four and any history length $h\ge1$. Use the repeating $110$ construction of [COLLATZ-24](../cofactor-avoidance-24/README.md), taking $x_0=2^{3(h+1)}b-5$ and varying $b$. The first $h+1$ blocks have word $110$, and at their starts, for $0\le i\le h$,

$$
L_i=2,\qquad w_i(b)=9^i2^{3(h+1-i)-2}b-1
$$

if $3\mid b$. For $i<h$, the next state after the three-step block is odd, so $E_i=1$.

Compare $b=3$ and $b'=3+3Q/4$. For $i<h$, the difference between the two $w_i$ is divisible by $Q$. Thus the histories of the triples $(w_i\bmod Q,L_i,E_i)$ agree for all $0\le i<h$. At the next start, however,

$$
w_h(b')-w_h(b)=3\cdot9^h Q/2\equiv Q/2\pmod Q.
$$

Both next odd runs still have length two. The two genuine positive histories therefore disagree on the next cofactor residue, for every finite history length. Their multipliers survive throughout the prescribed blocks. This obstruction is for the displayed observer and does not exclude other choices of retained data.

## Exact local reconstruction

Now observe the exact $w=w_i$, $v=w_{i+1}$ and lengths $L=L_i$, $E=E_i$, $R=L_{i+1}$, all lengths positive. Set

$$
A=2^{E+R}v,\qquad B=w,\qquad D=2^E-1 .
$$

The [odd-run join identity](../odd-run-join-22/README.md) becomes

$$
A3^p-B3^q=D,\qquad
p=a_{i+1}\ge0,\qquad q=L+a_i\ge L .
$$

Here $A,B$ are units modulo three, and $0<D<A/2$ since $R\ge1$. Each ordering of $p,q$ occupies a disjoint range:

| Ordering | Necessary range | Reconstruction |
|---|---|---|
| $p<q$ | $B<A/3$ | $p=v_3(D)$, then $3^q=(A3^p-D)/B$ |
| $p=q$ | $A/2<B<A$ | $3^p=3^q=D/(A-B)$ |
| $p>q$ | $B>5A/2$ | $q=v_3(D)$, then $3^p=(D+B3^q)/A$ |

For the first range, positivity gives $A>B3^{q-p}\ge3B$. For the middle range, $0<A-B=D/3^p\le D<A/2$. For the last range, $B=A3^{p-q}-D/3^q>5A/2$. When the exponents differ, the smaller equals $v_3(D)$ because both coefficients are units modulo three. Thus at most one row can apply. In that row verify that the displayed powers are exact nonnegative powers of three and that the required exponent order and $q\ge L$ hold. For genuine observations the check succeeds.

The endpoints are recovered as

$$
x_i=2^L w\,3^{q-L}-1,\qquad
x_{i+1}=2^R v\,3^p-1.
$$

Conversely, if the observations have the prescribed lengths and coprimality and pass the arithmetic check, these endpoints are positive odd integers, the first has exactly $L$ odd steps, and the join identity gives $3^L u_i-1=2^E x_{i+1}$. Since $x_{i+1}$ is odd, there are exactly $E$ halvings to it. This proves sufficiency as well as uniqueness.

## An exact test for gluing joins

A sequence of overlapping records $(w_i,w_{i+1},L_i,E_i,L_{i+1})$ lifts to an actual orbit segment exactly when every record decodes and the two decoded versions of each intermediate integer agree. This follows by induction for finite histories and gives a single starting integer for an infinite compatible history. In particular, if a finite chain returns to its coarse initial label, checking closure at the decoded integer tests whether it is an actual cycle.

For a small counterexample to gluing only by coarse labels, $15\to5$ is an actual join with record $(1,1,4,4,1)$. The join $1\to1$ has record $(1,1,1,1,1)$. The target label $(w,L)=(1,1)$ of the first agrees with the source label of the second. Their decoded middle integers are $5$ and $1$. The actual join from $5$ has three halvings and record $(1,1,1,3,1)$.

This gives an arithmetic diagnostic for the recurrence programme. Coarse returns and locally feasible joins need a compatibility check before they imply a single integer history. The reconstruction uses the next exact cofactor and the lengths as inputs. It does not bound those inputs or force an escaping orbit to return.

## Check

Exact arithmetic reconstructed all 131,072 joins from odd inputs below $2^{18}$. All three exponent orders occurred. Direct comparisons verified 224 modular-history pairs, using seven moduli and every history length from one to 32, as well as the failed gluing example. The proofs above apply without those cutoffs.
