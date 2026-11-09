# COLLATZ-02 · Exact census of first-descent families

This follows the [Hamiltonian parity example](../../../research/collatz/README.md). The question is how much of the positive integers can be handled by proving descent one residue class at a time.

**COMPUTATIONAL.** At 30 shortcut steps, exactly **12,771,274 of the $2^{30}$ residue classes** still have no descent. The other **98.810582422%** consist entirely of starts $n>1$ that have dropped below $n$ by then. There were **zero exceptions** where the coefficient first contracted but the offset kept the integer at or above its start. The census is exhaustive at this depth and makes no claim about larger depths.

## What qualifies as a certificate

Use the shortcut map $T(n)=n/2$ for even $n$ and $T(n)=(3n+1)/2$ for odd $n$. A word of $d$ parity decisions is realised by exactly one residue class modulo $2^d$. On that class the endpoint has the form

$$
T^d(n)=\frac{An+B}{M},\qquad M=2^d,\qquad A=3^a,
$$

where $a$ counts odd steps and $B\ge0$ depends on their order. The even extension takes $(A,B,M)$ to $(A,B,2M)$, and the odd extension takes it to $(3A,3B+M,2M)$. The two lifts of a residue from modulus $M$ to $2M$ have endpoints differing by the odd number $A$, so one lift takes each branch. This gives a complete traversal starting at $(1,0,1)$.

- If $A\ge M$, the endpoint is at least $n$.
- If $A<M$, the endpoint is strictly below $n$ exactly when $n>\lfloor B/(M-A)\rfloor$.

Stop at the **first** prefix where $A<M$. All earlier endpoints are at least the start. The new class is a first-descent certificate for every member above the cutoff. To check the whole class, compare its least member greater than $1$ with the cutoff. If the least member fails, the code records each failing member explicitly. The prefix and its finite exception list together describe exactly which members descend at that step.

This is the classical distinction between **coefficient stopping time** and **first descent**. Terras's periodicity, sufficiently-large-start result and modified binomial recurrence give the underlying theory, and Everett independently proved the density-one result for eventual first descent. Equality of the two stopping times for every $n>1$ is the coefficient stopping time conjecture described by Lagarias. [Terras (1976), Theorems 1.2, 1.9, 1.14 and 1.17](https://doi.org/10.4064/aa-30-3-241-252) · [Everett (1977)](https://doi.org/10.1016/0001-8708(77)90087-1) · [Lagarias (1985), Theorem C and discussion](https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/theorem-C.html) · [Coefficient stopping time conjecture](https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/node5.html)

## Census results

These are counts of residue classes, each of which represents infinitely many starts. The percentage is the natural density of starts that first descend by the given depth, rounded for display.

| Depth $d$ | Classes modulo $2^d$ with no drop by $d$ | Starts covered | Least start still uncovered |
|---:|---:|---:|---:|
| 1 | 1 | 50.000000% | 3 |
| 2 | 1 | 75.000000% | 3 |
| 4 | 3 | 81.250000% | 7 |
| 12 | 226 | 94.482422% | 27 |
| 20 | 27,328 | 97.393799% | 27 |
| 24 | 286,581 | 98.291844% | 27 |
| 29 | 6,385,637 | 98.810582% | 27 |
| 30 | 12,771,274 | 98.810582% | 27 |

The least remaining start at depth 30 is $27$. Direct iteration gives its first drop on shortcut step 59, when it reaches $23$.

The largest integer cutoff anywhere in the census was $108$, attained at depth 27 by the residue $96{,}361{,}467\bmod 2^{27}$, with $A=129{,}140{,}163$ and $B=548{,}440{,}271$. Thus any disagreement through depth 30 would have to occur among the individual starts $2$ through $108$. None did.

### What the shorter description preserves

For counting paths that have yet to contract, the current depth and odd-step count suffice. Each state sends its count to the two possible next odd-step counts. Discard the child when $3^a<2^d$. This independent recurrence, equivalent to Terras's modified binomial recurrence, agrees with the full traversal at all 30 depths. It leaves about **0.023868%** of residue classes with no coefficient contraction by depth 100. The depth-100 recurrence does not check the offsets or least starts of the contracted classes.

The shortened description forgets the offset. For example, the starts $39$ and $123$ both first contract at depth 8, with $A=243$ and $M=256$. Their offsets are $251$ and $319$, yielding cutoffs $19$ and $24$. So the same depth and odd-step count suffice to count these families, while checking every member requires more arithmetic.

The flat percentage from depth 29 to 30 has a direct explanation. A first contraction must end on an even step, which leaves $A=3^a$ unchanged. Thus it can happen at depth $d$ only if

$$
2^{d-1}\le 3^a<2^d.
$$

Conversely, when this interval contains $3^a$, the word consisting of $a$ odd steps followed by $d-a$ even steps achieves first contraction at $d$. The odd steps all increase the coefficient, and the even steps decrease it monotonically. The interval for $d=30$ contains no power of three, so every remaining residue class splits in two with no new certificate.

## Reproduce

From this directory, run the verifier and compare its output.

```sh
python3 verify.py > /tmp/collatz-02.json
diff -u results.json /tmp/collatz-02.json
```

The script uses Python's standard library and exact integer arithmetic. It compares the two censuses and directly checks the predicted first descent for each of the $2^{18}$ starts in one full residue window. The complete counts, cutoff witness and exception list are in [results.json](results.json).

## Open question

At every finite depth $d$, the all-odd word is still present, in the class $n\equiv-1\bmod 2^d$. Its members include $2^d-1$, which increases for the first $d$ shortcut steps. Yet a single integer in all these nested classes would have to equal $-1$. That is an exact example of an indefinitely surviving branch with no positive integer on it. The unresolved question is whether every indefinitely surviving branch excludes integer starts greater than $1$.

This is a reproducible baseline for EHF's question about what a compressed description preserves. We consulted the relevant statements in Terras and Lagarias and the abstract for Everett. AI assistance was used for source review, the implementation and the write-up. The census makes no priority claim.
