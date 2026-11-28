# EHF research handover

Last updated 28 November 2026 (Australia/Brisbane).

Start here when returning to EHF or handing the research to someone else. The [main index](README.md#full-research-index) locates individual notes, the [status page](STATUS.md) records the wider programme assessment, and the [roadmap](ROADMAP.md) describes its longer-term goals.

## Current focus

**Records in growing systems.** The Wheeler run-growth law resolves the open long-time question in Julstce. In the reference experiment, an observer who sees only the sequence of inserted colours has a 50% chance of identifying which detector acted first. An observer who sees only the final unmarked ring has a 62.64% chance after 32 insertions, converging to about **58.3%**. The [proof and reproduction commands](#a-result-linking-wheeler-and-julstce) are below.

**Next experiment.** Interleave uniform legal insertions with occasional valid reversals. Use the same two preparations and equal priors. Compare no reversals with a declared rate and length distribution of randomly attempted reversals. Start with reversals that preserve the number of runs, which keeps the inserted-colour sequence blind to the preparation. Treat reversals that can change the run count as a separate case and measure the colour readout too. Recover the baseline with zero reversal rate, then measure how well the final shape identifies the preparation at increasing sizes. Finite-horizon evidence of decay or persistence, by itself, leaves the limit open.

**Where the physics connection stands.** The memory theorem concerns classical growth under an explicit sampling rule. The signed reversal probes demonstrate interference in a supplied coherent walk. Connecting either result to physical dynamics requires a derivation of the preparation, moves and readout in a specified physical system. The higher-multiplicity collinear colour result is a separate physics-facing thread with an open attribution question.

**Keep this page current.** When a result changes, update its evidence level, link the proof or reproduction, record the next unresolved check and update the date above. Put individual run logs in the relevant probe.

## Where the research fits together

| Research threads | What the comparison supports |
| --- | --- |
| Wheeler run growth, MICRO observers and Julstce | The Wheeler run representation gives a long-time result for detector-order memory in Julstce. The MICRO observer audit explains why a coarser readout can have closed predictive dynamics while still throwing away information. |
| Reversal events, label parity and coherent walks | Distinct histories can have the same visible endpoint and leave different label permutations. A supplied coherent walk can read out some signs. The both-colour case and the restriction to reversals of lengths 2–4 give exact cases where the chosen readout hides them. An earlier orientation-holonomy study also found trivial holonomy on the tested growth-projectable moves in its own model. |
| CBB growth and reference | The [lineage](research/cbb-binary/CROSS-62-blind-growth.md) and [reference](research/cbb-binary/CROSS-58-growth-reference.md) probes expose two separate issues: what the observations can identify, and which coherent phases can be defined consistently during growth. Their carrier differs from the binary no-isolation rings, so they supply questions and controls for a comparison. |
| Amplitudes, ordering and collinear colour | The [nine-point reconstruction](research/amplitudes/nine-point-tail/README.md) is a separate exact result in its stated scope. For the [collinear work](research/amplitudes/collinear-colour/literature.md), ordinary four-gluon colour algebra already gives the symmetric ratio. The possible contribution is the precise higher-multiplicity finite-coefficient statement on the specified path. Its relation to existing amplitude identities needs to be settled before making a priority claim. |
| Hamiltonian-cycle and dimension work | These threads establish results about combinatorial reconstruction, continuation and the geometry of specific configuration spaces. A physical interpretation would require an independently justified map between those structures and physical observables. |

## A result linking Wheeler and Julstce

Choose detector order with a fair coin, then grow the resulting binary ring by uniformly choosing a legal edge-and-colour insertion. The reader receives only the final ring shape, identifying rotations and reflections while preserving colour. The two initial ring words are `1100110011111000` and `0011110011100110`. Both preparations produce the same law for any finite sequence of inserted colours.

| Growth steps | Optimal probability of correctly guessing detector order |
| --- | ---: |
| 1 | 93.181818% |
| 8 | 71.837380% |
| 16 | 66.213587% |
| 32 | 62.636270% |
| Limit | **Approximately 58.3%** |

Finite entries were reproduced with the repository's exact calculation. The limiting estimate from 1,000,000 samples was 58.299259%, with a 95% Hoeffding interval of 58.231354%–58.367164% for sampling error. A separate seed gave 58.285094%.

### Growth law and limit

For a binary ring without isolated bits, all runs have length at least two. Every legal insertion extends one existing run. A run of length \(L_i\) has \(L_i-1\) internal edges and two boundary edges where an insertion of its colour is legal, so its selection weight is \(L_i+1\). Each update increases its weight by one. This is the classical Pólya urn, also used in the [Wheeler manuscript](research/wheeler/paper-v0.1/manuscript.md). See the abstract of Svante Janson’s [Rate of convergence for traditional Pólya urns](https://doi.org/10.1017/jpr.2020.59) (2020) for the established Dirichlet limit. Labels for the runs can be fixed for the calculation and forgotten at readout.

Let \(b\) be the number of runs, \(m=\sum L_i\), and \(N=m+t\) the length after \(t\) insertions. For a labelled endpoint \(\ell=(\ell_1,\dots,\ell_b)\), the Dirichlet-multinomial formula gives

\[
p_{L,N}(\ell)=\frac{\prod_i\binom{\ell_i}{L_i}}{\binom{N+b-1}{m+b-1}}.
\]

Writing \(x=\ell/N\), expand the binomial polynomials. Uniformly over the full simplex lattice, \(N^{b-1}p_{L,N}(\ell)\) converges to the density

\[
f_L(x)=\frac{(m+b-1)!}{\prod_i L_i!}\prod_i x_i^{L_i}.
\]

Use Lebesgue measure in the first \(b-1\) simplex coordinates. Binomial coefficients for an integer \(\ell_i<L_i\) are zero. Thus the expansion also applies on the boundary and at unreachable endpoints.

Start each run list at a zero run. The admissible dihedral operations are even cyclic shifts and their compositions with the reflection that keeps index zero fixed. Average each distribution over those permutations. An orbit's total probability stays the same, and the averaged mass is constant on that orbit. Therefore the sum of absolute differences over the whole lattice equals the sum of absolute differences over orbits. Uniform convergence and the Riemann sum give the limiting equal-prior Bayes accuracy

\[
\frac12+\frac14\int_{\Delta_{b-1}}|\bar f_A(x)-\bar f_B(x)|\,dx .
\]

For the numerical calculation, sample from the equal mixture of the two original Dirichlet laws and average \(\max(\bar f_A,\bar f_B)/(\bar f_A+\bar f_B)\). The statistic is invariant under the group, so the mean is the same under the original and the symmetrized mixtures. It lies in \([1/2,1]\), giving the stated Hoeffding interval.

### When is there a surviving signal?

Fix the initial size and the number of runs, and compare two initial shapes that preserve the colour labels. The averaged Dirichlet density of each is a positive sum of monomials whose exponent vectors form precisely that shape's orbit. Two different orbits have disjoint monomial supports. Because these polynomials are homogeneous of the same degree, equality on the interior of the simplex would imply equality throughout the positive orthant by scaling. Distinct supports make this impossible. Thus the limiting accuracy is strictly greater than one half exactly when the two initial shapes differ. The densities are positive in the interior, so the accuracy is strictly below one for different shapes.

When the pair also has matching initial colour totals, grouping the urn coordinates by colour gives identical two-colour urn parameters. All insertion-colour sequences then have identical probabilities. The original Julstce witness is one instance of a family with a permanently blind readout and a final-shape readout with persistent order information.

## Tests for a physical interpretation

The larger physics question is whether one independently specified dynamics supplies the preparation, allowed moves and measurable readout. A physical candidate would need a regime where its couplings and rates predict a real observable, with a baseline that matches transition magnitudes and other known effects. The present growth calculation is classical, and the signed coherent comparison uses an imposed coherent dynamics. A tile experiment could directly implement the specified sampling process. A physical Ising system would need a separate derivation of how its dynamics implement that process or a justified extension of it.

The mathematical result is suitable for focused review. The underlying urn and Dirichlet law are established mathematics. The exact combination of symmetry reduction, persistent shape distinguishability and an identically blind colour record is the result to compare against prior work.

## Reproduce

From the repository root, run the exact finite calculation and the limiting estimate.

```sh
python3 probes/micro/julstce/probe.py
python3 probes/micro/julstce/limit_probe.py
python3 probes/micro/julstce/limit_probe.py --seed 516
```

The limiting calculation uses NumPy. Codex assisted in deriving the limit, writing the estimation code and consolidating the repository notes.

- [EHF research index](README.md#full-research-index)
- [Wheeler paper draft](research/wheeler/paper-v0.1/README.md)
- [Julstce exact finite probe](probes/micro/julstce/README.md)
- [MICRO observer compatibility](probes/micro/observer-compatibility-01/README.md)
- [Same-colour label parity](probes/qm-bridge/label-parity/README.md)
- [Orientation holonomy](probes/reversals/orientation-holonomy-13/README.md)
- [Amplitude results and limits](research/amplitudes/README.md)
