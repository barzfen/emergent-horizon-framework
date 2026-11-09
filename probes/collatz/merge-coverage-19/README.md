# COLLATZ-19 · Coverage of the half-source merge

The two [COLLATZ-18](../adaptive-merge-18/README.md) rules certify exactly $4097/131072$, or about $3.12576\%$, of all positive starts. Searching through 32 synchronized steps after the odd runs raises this to about $3.13630\%$. **Even an unlimited search with this partner, clock alignment and survival requirement covers at most $3.14863\%$ of all positive starts.** The bound comes from the exact weight of the branches still eligible after 32 steps.

## Which search is counted?

Write an odd start $n=2^Lu-1$ with $L=v_2(n+1)$ and $u$ odd. The partner is $m=(n-1)/2=2^{L-1}u-1$. For $L\ge2$ they begin with $L$ and $L-1$ odd steps. Their respective states at the ends of those runs are

$$
x=3^Lu-1,\qquad z=3^{L-1}u-1,\qquad x=3z+2.
$$

At suffix depth $j$ compare the states after $j$ additional steps on each path. Accept if the endpoints coincide, the $z$ suffix has used one more odd step than the $x$ suffix, and both full prefixes have kept their cumulative multipliers at least one. The paths then have the same total odd count, and COLLATZ-18 transfers the full finite survival horizon to the smaller start. A successful comparison is a certificate of that transfer. It does not certify the partner's eventual contraction.

Even $n$ are excluded from this comparison. For $L=1$ the partner is zero or even and cannot give such a surviving merge. For $L\le3$, no surviving merge is possible with this alignment. The first suffix step halves both values and cannot be a counted merge. Before the second suffix step the states are $3a+1$ and $a$, with $a=z/2$, so one of the two paths must halve again. Even the larger initial budget $(3/2)^3$ cannot pay for two halvings.

## Exact counts

| Suffix depth | Cofactor coverage with unlimited initial budget | Coverage at $L=10$ | Coverage among all positive starts |
|---:|---:|---:|---:|
| 2 | 50.00000% | 50.00000% | 3.125000% |
| 8 | 50.78125% | 50.78125% | 3.125763% |
| 16 | 54.67834% | 53.70789% | 3.134463% |
| 24 | 56.63204% | 54.06435% | 3.135831% |
| 32 | 58.05181% | 54.17350% | 3.136305% |

The first column of percentages ignores only the multiplier budgets. The second applies the budgets and conditions on a specified initial run length. The third averages over the actual run lengths and includes even starts in the denominator.

For the original two rules the weights are particularly simple. $L\ge4$ has density $1/16$ and the first residue rule selects half its odd cofactors. $L\ge10$ has density $1/1024$ and the second rule selects $1/128$ of its odd cofactors. The two cofactor tests are disjoint at each common run length because $43\equiv3\bmod4$. This gives $1/32+1/131072=4097/131072$. The census confirms that these are exactly the two first-merge possibilities through depth eight.

### Count first merges and remaining eligible branches

For fixed $L$, the map $u\mapsto z=3^{L-1}u-1$ bijects odd residues modulo $2^j$ with even residues. At a given even residue for $z\bmod2^j$, both suffix words are fixed. Write $a,b$ for their odd counts. If $z$ increases by $2^j$, the two endpoints increase by $3^{a+1}$ and $3^b$. Consequently a match with $b=a+1$ on one representative holds on the whole class. The first such match can be counted once and its descendants omitted.

For each prefix, store the smallest $L_*$ that pays for all its suffix steps on both paths. At step $i$, with respective suffix odd counts $a_i,b_i$, the two exact constraints on $L$ are

$$
3^{L+a_i}\ge2^{L+i},\qquad
3^{L-1+b_i}\ge2^{L-1+i}.
$$

Taking the maximum of the required values over the prefix gives $L_*$. A first-merge class at depth $j$ has conditional cofactor weight $2^{1-j}$. Since $v_2(n+1)=L$ has natural density $2^{-(L+1)}$, the class contributes $2^{1-j-L_*}$ to the density among all starts. The same weight applies to an unmatched class at the cutoff, using the minimum budget to survive the cutoff.

Let $D_H$ be the total weight of first merges by $H$, and $U_H$ the weight of unmatched classes at $H$ with their survival budgets applied. Any later admissible merge must be in $U_H$. A first match whose prefix has already contracted cannot become admissible at a later time. The exact depth-32 sums are

$$
D_{32}=\frac{289273043372030297}{9223372036854775808},\qquad
U_{32}=\frac{19065609900022250178309}{154742504910672534362390528}.
$$

These give the interval from $3.136304621\ldots\%$ to $3.148625482\ldots\%$ for coverage with unrestricted suffix depth. It is an interval for this search, with the partner and alignment fixed.

### The eventual density exists

At any fixed horizon the densities of the residue-class unions are well defined. First restrict $L$ to a finite range. The remaining high-$L$ starts belong to a single congruence class with density tending to zero as the range increases.

The upper and lower densities for the unrestricted search lie between $D_H$ and $D_H+U_H$. To show $U_H\to0$, it is enough to bound survival on the original path alone. For each fixed $L$, a complete cofactor system produces every even $x\bmod2^H$ once. The parity-residue bijection therefore makes the first suffix step even and the remaining parity bits fair and independent in this finite census. If $P_H$ is the suffix multiplier, its square-root moment is

$$
\mathbb E\sqrt{P_H}=2^{-1/2}q^{H-1},\qquad
q=\frac{1+\sqrt3}{2\sqrt2}<1.
$$

Survival to $L+H$ requires $\sqrt{P_H}\ge(2/3)^{L/2}$. Multiplying the moment bound by $(3/2)^{L/2}$ and averaging with weights $2^{-(L+1)}$ gives $U_H=O(q^H)$, since the resulting geometric ratio is $\sqrt{3/2}/2<1$. Thus the natural density of the unrestricted search exists. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252)

## Why the long-run and all-start answers differ

For large $L$, take $H=\lfloor(L-1)\log_2(3/2)\rfloor$. Even $H$ consecutive halvings cannot exhaust either initial budget. The counted synchronization bound of Leen, as quoted and applied by Weaver, gives an unmerged fraction $O(H^{-1/2})$ for the initial pair $(z,3z+2)$ with odd-count lead one. Conditioning on even $z$ costs a factor of at most two. Therefore the certified cofactor fraction in the shell $v_2(n+1)=L$ tends to one with failure $O(L^{-1/2})$. This statement imports the quoted synchronization theorem. The finite census and the overall density interval do not use it. Long initial runs themselves have exponentially small density in the all-start denominator. [Weaver, *Smaller Collatz sources before first descent*, §7, equation (23)](https://rstation.ai/problems/collatz/papers/21) · [Leen, *Quantitative synchronization of Collatz trajectories*](https://doi.org/10.5281/zenodo.23268755)

## Reproduce

Compile and run the exact histogram enumerator with GCC or Clang.

```sh
c++ -O3 -std=c++17 -Wall -Wextra coverage.cpp -o coverage
./coverage 32
```

Each output row has the kind, depth $j$, minimum run length $L_*$, and number of even $z$ classes at that depth. Multiply the final column by $2^{1-j-L_*}$ and sum `hit` and `live` separately to reproduce $D_{32}$ and $U_{32}$. For a fixed-$L$ fraction, sum $2^{1-j}$ over `hit` classes with $L_*\le L$, including their multiplicities. Direct iteration over all 8,192 even representatives at depth 14 independently reproduced every histogram cell.
