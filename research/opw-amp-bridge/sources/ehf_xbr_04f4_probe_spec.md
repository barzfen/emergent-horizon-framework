# EHF-XBR-04F4: Exact-Rule Stability and Mechanism Audit


## Purpose


EHF-XBR-04F3 found an exact three-regime classifier on the 20 proper n=9
OPW3/AMP channels. For an ordered subset


\[
A=(a,b,c),\qquad a<b<c,
\]


the compact descriptive rule is:


\[
\begin{aligned}
&b=6\ \text{and}\ 2\le b-a\le3
&&\Longrightarrow \text{null},\\
&a=2\ \text{or}\ a+b+c=15
&&\Longrightarrow \text{invertible},\\
&\text{otherwise}
&&\Longrightarrow \text{mixed}.
\end{aligned}
\]


EHF-XBR-04F4 tests whether this rule is structurally stable or merely one of
many post-hoc encodings of a 20-row census.


## Audit layers


### 1. Fixed-rule certification


Apply the displayed rule to all 20 proper channels and require exact agreement
with the 04F3 null/mixed/invertible labels.


This locks the candidate being audited. It does not establish mechanism.


### 2. Minimum-description-length competition


Reconstruct the same subset-geometry predicate family used by 04F3:


- exact equality predicates;
- exact threshold predicates;
- conjunctions and disjunctions of up to three atomic predicates;
- ordered three-class rule lists.


Rank exact rule lists by:


1. total atomic terms;
2. number of distinct features;
3. character count;
4. lexical order as a deterministic tie-break.


Record the number of exact competitors and the number tied at minimum
complexity. A large tie count means the compact rule is not uniquely selected
by the finite data.


### 3. Leave-one-channel-out recovery


For each of the 20 channels:


1. remove that channel and its regime label;
2. rebuild the exact subset-geometry rule family on the remaining 19;
3. select a deterministic minimum-description-length rule;
4. predict the held-out regime;
5. record all minimum-MDL tie predictions;
6. test whether the selected training rule is exact on the restored 20-row
   census.


This measures internal stability. It is not fresh-n validation because every
held-out subset belongs to the same finite n=9 atlas.


### 4. Exact proxy equivalences


Audit the following finite-census equivalences:


\[
\text{null locus}
\iff
\text{observed null regime},
\]


\[
\text{boundary-or-balance locus}
\iff
\text{observed invertible regime},
\]


\[
\text{null regime}
\iff
\dim \mathcal K_A^\perp\le10,
\]


\[
\text{invertible regime}
\iff
\nu(\operatorname{Adj}_A)=0,
\]


and


\[
\text{mixed regime}
\iff
\nu(\operatorname{Adj}_A)>0
\ \text{and}\
\dim \mathcal K_A^\perp>10.
\]


These equivalences reveal whether the label conditions are proxies for simpler
chamber properties. They remain finite-census statements until derived.


### 5. Relabelling audit


Enumerate all


\[
7!=5040
\]


permutations of the internal labels \(2,\ldots,8\).


Record:


- the automorphism group of the 20-subset proper-channel hypergraph;
- the subgroup preserving the null/mixed/invertible colouring;
- the orbit size of the coloured partition under all label permutations;
- whether reflection \(x\mapsto10-x\) is an automorphism.


A trivial regime-preserving group indicates that the compact rule is strongly
coordinate-dependent. A nontrivial group identifies exact relabelling
covariance that a mechanism should respect.


### 6. Independent pre-action mechanism proxies


Search numeric XBR-04C/04D source fields while excluding columns containing
adjacency action, rank, nullity, spectrum, characteristic-polynomial or
certificate-result information.


For each pre-action feature, find the best single equality or threshold
predicate for:


- the null locus;
- lower-boundary contact;
- central balance \(a+b+c=15\);
- the complete invertible-geometry locus.


This distinguishes independent chamber correlates from spectral restatements.


### 7. Null-module symmetry discrimination


When supplied with the existing 04F result directories, read the exact
certificates for


\[
(3,6,7),\qquad(4,6,7),\qquad(4,6,8).
\]


Compare:


- complement dimension;
- characteristic and minimal polynomials;
- chamber automorphism-group order;
- representation-image order;
- fixed-space distribution;
- trace distribution.


This tests whether symmetry distinguishes the 10-, 2- and 9-dimensional null
modules. It does not establish a spinor interpretation.


## Inputs


The probe requires:


- `runs/ehf_xbr_04f3/classification_ledger.csv`;
- `runs/ehf_xbr_04f3/run_summary.json`;
- the 04F3 Python script, imported for its exact feature and rule-search
  conventions.


The optional null-symmetry audit uses:


- `runs/ehf_xbr_04f_4_6_7`;
- `runs/ehf_xbr_04f_low_dim_panel`.


## Outputs


- `fixed_rule_audit.csv`
- `mdl_rule_competition.csv`
- `loo_rule_recovery.csv`
- `exact_equivalence_audit.csv`
- `label_relabelling_automorphisms.csv`
- `mechanism_proxy_single_predicates.csv`
- `mechanism_group_summary.csv`
- `null_symmetry_audit.csv`
- `stability_mechanism_report.md`
- `run_summary.json`


## Self-test


```bash
python3 scripts/ehf_xbr_04f4_exact_rule_stability_mechanism_audit.py \
  --self-test
```


Expected:


```text
EHF-XBR-04F4 self-test PASS
```


## Production command


```bash
python3 scripts/ehf_xbr_04f4_exact_rule_stability_mechanism_audit.py \
  --xbr04f3-dir runs/ehf_xbr_04f3 \
  --xbr04f3-script scripts/ehf_xbr_04f3_invisible_action_rank_nullity_classification.py \
  --xbr04f-dirs 'runs/ehf_xbr_04f_4_6_7;runs/ehf_xbr_04f_low_dim_panel' \
  --out-dir runs/ehf_xbr_04f4 \
  --strict
```


## Success verdict


```text
EHF_XBR_04F4_EXACT_RULE_STABILITY_MECHANISM_AUDIT_PASS
```


The pass verdict certifies that the stability and mechanism audit completed
consistently. It does not require leave-one-out recovery to be perfect. Weak
recovery is a scientific result, not an implementation failure.


## Claim boundary


A successful audit may establish that the finite n=9 rule is exact, internally
stable or unstable, coordinate-rigid or relabelling-covariant, and equivalent
to specific chamber proxies.


It does not establish:


- a universal rule beyond n=9;
- a causal mechanism;
- a Hamiltonian interpretation;
- a hidden particle sector;
- gauge or topological structure;
- a spinor field;
- or fermionic physics.