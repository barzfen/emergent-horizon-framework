# Probe-dependent access to Hamiltonian networks — exploration 01

29 October 2026

**Result:** changing a probe's allowed cycle transitions changes its diffusion on a fixed network. A cycle-confined probe has the return law of a one-dimensional ring, regardless of the geometry of the union graph. Switching permits wider access. The tested locally grown graphs do not exhibit a robust position-return exponent near three. These are classical Markov probes with imposed restrictions, not emergent particles or a derivation of quantum spin.

## Experiment

Inputs are saved Hamiltonian triads from Growth Probe 02. Seven graphs were examined: strict one-step-local growth, run 0 at N=64,256,512,1024; strict-local runs 1 and 2 at N=512; and global growth run 0 at N=512. This is a small exploratory sample, not an ensemble scaling study. Full input snapshots are included.

A probe state is (v,k), consisting of vertex v and cycle label k in {0,1,2}. In continuous time it:

- moves to either neighbor of v in cycle k, at rate 1/2 each;
- changes k to either other label, staying at v, at rate kappa/2 each.

The mean spatial hop rate is one for every kappa. Switching therefore does not simply slow the clock for movement. Kappa=0 confines the probe to one Hamiltonian cycle. Positive rates 0.001,0.01,0.1,1,10 were tested. At each start vertex the initial cycle label is uniformly distributed. Start vertices are also averaged uniformly.

If A_k is the undirected adjacency matrix of cycle k, the positive semidefinite generator L=-Q has diagonal blocks (1+kappa)I-A_k/2 and off-diagonal blocks -kappa I/2. This is a real symmetric 3N-by-3N matrix with zero row sums. The transition matrix at time t is exp(-tL). Label changes have been imposed as a classical process. No complex probability amplitudes, quantum measurements, or spin transformations occur.

## What was measured

Position return ignores the final cycle label:

    p_pos(t) = (1/(3N)) sum_v sum_k sum_j [exp(-tL)]_(v,k),(v,j).

Returning to the full starting state instead gives

    p_full(t) = Tr(exp(-tL))/(3N).

These are different observables. At positive kappa their stationary limits are 1/N and 1/(3N), respectively. Counting internal-state returns as though they were position returns would confound internal relaxation with spatial exploration. Both series are saved; the main figure uses position return.

For L=U diag(lambda_i) U^T, position return equals sum_i w_i exp(-lambda_i t), where

    w_i = (1/(3N)) sum_v [sum_k U_(v,k),i]^2.

The weights are nonnegative and sum to one. This makes it possible to compute the expectation over ALL starting states, without trajectory-sampling noise. “Exact” here means finite-matrix calculations in floating-point arithmetic, not symbolic exactness.

The plotted diagnostic is

    d_pos(t) = -2 d log p_pos(t)/d log t
             = 2t [sum_i w_i lambda_i exp(-lambda_i t)] / p_pos(t).

For a scale range with p_pos(t) proportional to t^(-d/2), this equals d. On a graph with internal labels this is explicitly a position-return diagnostic for the chosen dynamics, not a universal graph dimension. The derivative is evaluated analytically from the spectrum, not by noisy finite differences.

All curves begin with microscopic transients and eventually encounter finite-size saturation. Saturation drives this diagnostic toward zero and must not be interpreted as a zero-dimensional universe. In the two grown-graph exponent panels, solid lines denote t>=2 and p_pos>=10/N; faint dotted lines show the remaining computed curve. This screen is only a heuristic precaution: it does not prove that the solid portions are asymptotic or free of finite-size effects. A plateau must survive increasing sizes and a widening scale window.

## Findings

On strict-local run 0, N=1024, at t=100 (100 spatial hops on average):

| Access | Position return probability | Position-return exponent |
|---|---:|---:|
| One cycle, kappa=0 | 0.0399444 | 1.0025 |
| kappa=0.001 | 0.0385527 | 1.0668 |
| kappa=0.01 | 0.0300557 | 1.3956 |
| kappa=0.1 | 0.0161668 | 1.4662 |
| kappa=1 | 0.0091821 | 1.5851 |
| kappa=10 | 0.0073519 | 1.6122 |

These are values at one time, not fitted dimensions. The last two are below the conservative 10/N return threshold. The full curves, smaller sizes, and two additional local realizations at N=512 show the same qualitative distinction between confinement and switching. They do not justify a universal fractional dimension.

The globally grown N=512 graph produces a pronounced transient peak under faster switching, not a stable three-dimensional plateau. Passing through three at one time is insufficient evidence for 3D scaling.

The earlier mean-distance diagnostic and this diffusion diagnostic are different measurements at different sizes and scales. Their numerical disagreement is not a logical contradiction. Their identification would require additional regularity and scaling assumptions, which we have not established.

## Exact checks and controls

1. Every input cycle is checked to visit all vertices exactly once, and every union edge is checked to occur in at most two cycles.
2. Each lifted generator is checked to have zero row sums; its spectrum is nonnegative to numerical tolerance; position-return spectral weights sum to one.
3. On a 16-vertex input, four direct matrix exponentials independently reproduce the spectral position-return formula, with maximum absolute difference 1.33e-14. Transition matrices are also checked for nonnegativity and unit row sums.
4. Three direct cycle matrix exponentials match the Fourier cycle formula.
5. Reference controls use exact separable Fourier heat traces for periodic grids of sizes 8x8x8, 64x64x64, and 4096x8x8. The latter two have the same 262,144 vertices. The isotropic grid has an intermediate plateau near three; the long tube crosses toward one after its narrow directions are mixed. These are deliberately constructed controls, not networks generated by our growth rule.

For confinement on a cycle of N vertices, regardless of which Hamiltonian tour is chosen,

    p_cycle(t) = (1/N) sum_(j=0)^(N-1) exp[-t(1-cos(2pi j/N))].

For 1 << t << N^2 this has the one-dimensional return behavior. For a d-factor periodic grid with side lengths L_a and total spatial hop rate one, the exact return probability factorizes:

    p_grid(t) = product_a { (1/L_a) sum_j exp[-(t/d)(1-cos(2pi j/L_a))] }.

Hamiltonian decomposability of products of three cycles is established by Foregger's theorem, referenced below. We do not construct those decompositions here; the grid controls test the unrestricted walker. Thus the theorem plus the confinement formula supplies an existence example of different probe behavior on one 3D-grid graph, but not a dynamical selection mechanism.

## An important comparison detail

Very rapid cycle switching averages the cycle-specific hopping generators. Its effective position generator is

    L_fast = I - (A_0+A_1+A_2)/6.

An edge present in two cycles consequently has twice the weight of an edge present in one. This differs from an unrestricted walk choosing each DISTINCT union neighbor equally. Both controls are computed and saved. On edge-disjoint triads the two coincide. Kappa=10 is a finite rate, not the mathematical infinite-switching limit.

## What this establishes and what it does not

It establishes, within this specified toy model, that operational access matters even with network topology and spatial hop rate held fixed. Confinement is one-dimensional by construction. The experiment quantifies what happens when that restriction is softened.

It does not explain why a physical particle would be cycle-confined, why switching has a particular rate, why three cycles are fundamental, or how a stable excitation arises. The three-state classical cycle label is not a spin-1/2 degree of freedom. No Stern–Gerlach probabilities, quark flavors, quantum interference or relativistic propagation have been derived.

A well-defined next task is to seek a persistent localized excitation in the cycle-rearrangement dynamics and derive its allowed transitions. That would replace the externally assigned probe rule with a rule following from the construction. Separately, larger ensembles and additional volume/bottleneck diagnostics are needed before assigning an asymptotic geometry to the grown networks.

## Files and reproduction

- explore.py: generators, spectral calculations and independent small-matrix checks.
- build_report.py: figure and compact numeric summary.
- input/: eight original snapshots, including the small validation input.
- results.json: all return curves, full-state returns, spectra-derived gaps, and validation results.
- summary.json: numeric excerpts at t=10,100,1000.
- probe_access.png: four-panel scientific figure.

Requires Python 3, NumPy, SciPy and Matplotlib. Versions used: NumPy 2.3.5, SciPy 1.17.0. From this folder:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python explore.py --fresh
    python build_report.py

Without --fresh, the script resumes saved graph results. A fresh run is required after changes to the model. The 1024-vertex case uses a 3072-by-3072 eigendecomposition; memory and time costs grow quickly with N.

Reference: M. F. Foregger, “Hamiltonian decompositions of products of cycles,” Discrete Mathematics 24(3), 251–260 (1978), https://doi.org/10.1016/0012-365X(78)90096-1. This reference concerns decomposition, not our diffusion or particle interpretation.
