# Hamiltonian Cycle and admissible comparisons

[EHF-HC-02 · Stable neighbour refinement](HC-02.md) fixes the HC-01 square and finds two minimal eleven-vertex failures, including one with no bridges in the residual graph.

[EHF-HC-03 · Vertex connectivity](HC-03.md) gives the first biconnected failure, tests two-vertex separators and one-step lookahead, and constructs failures at arbitrary connectivity.

[EHF-HC-04 · Exact path composition](HC-04.md) joins disjoint local paths across separators and finds the smallest failures of three simpler tests.

[EHF-HC-05 · Boundary pairings](HC-05.md) proves exact successive joins, identifies a smallest pair-marginal failure, and audits representative matching tables.

## EHF-HC-01 · Which partial routes can share a search state?

**PROVED.** On a fixed undirected graph, two rooted simple paths with the same unvisited vertices and the same endpoint attachment set have exactly the same legal completion sequences. **NEGATIVE.** A cheaper comparison based on counts of attachment types can give the wrong answer about whether a route can finish. The smallest graph exhibiting that failure has seven vertices. **COMPUTATIONAL.** The [verifier](verify_hc_01.py) checked all 33,864 labelled graphs of orders three through six and explicit witnesses of orders seven through ten.

### Research question

Admissible comparison is the chosen primitive data of the framework. Here the comparison asks which partial routes admit the same continuations in a fixed input graph. The [Hamiltonian growth-lift audit](../../probes/reversals/growth-lift-09/README.md) starts with existing cycles and studies how transitions behave under insertion. In this problem the graph is already supplied and each route must follow its existing edges. Growing a legal simple path by one edge gives a complete search, since every Hamiltonian cycle can be read from an arbitrary root. The aim is to reduce duplicate search while preserving exact answers.

### Exact comparison

Fix a simple undirected graph $G=(V,E)$ with at least three vertices and a root $r$. Let $P$ be a legal simple path from $r$ to $t$ using at least one edge. Put $U=V\setminus V(P)$, $A=N_G(r)\cap U$ and $B=N_G(t)\cap U$. For $U\ne\varnothing$, a completion is an ordering $(u_1,\ldots,u_k)$ of $U$ in which $u_1\in B$, successive vertices are adjacent in $G[U]$, and $u_k\in A$. These conditions are necessary and sufficient by reading the edges of the completed cycle in order. When $U=\varnothing$, the empty suffix is legal exactly when $tr\in E$.

For fixed $G$ and $r$, a safe key is therefore $(U,B)$, with the closing-edge flag in place of $B$ when $U=\varnothing$. It can merge paths with different endpoints. For example, in $K_4$ the paths $(0,1,2)$ and $(0,2,1)$ share the same remaining vertex $3$, and both have the single legal suffix $(3)$.

For a sharper characterization, let $F\subseteq U$ consist of the vertices from which a spanning path of $G[U]$ can end in $A$. A one-vertex path is allowed. A prefix can finish exactly when $B\cap F\ne\varnothing$. For a fixed nonempty $U$, two prefixes have identical sets of legal suffixes exactly when their intersections $B\cap F$ coincide. Each vertex in $F$ has a witnessing suffix with that vertex first, which proves the reverse implication. Computing $F$ directly requires solving a spanning-path problem on the residual graph. The exact attachment key avoids that computation.

### Smallest failure of the attachment counts

For fixed $G$, $r$ and $U\ne\varnothing$, replace $B$ with the count of its vertices of each type $(\deg_{G[U]}(v),\mathbf{1}_{v\in A})$. This retains the residual graph and the exact root attachment set. It forgets which individual vertices the endpoint can enter within each type. For $U=\varnothing$ it uses the same closing-edge flag as the exact key.

Build a graph on vertices $0$ through $6$ from a triangle $0$–$1$–$2$–$0$, a square $3$–$4$–$5$–$6$–$3$, and the three edges $0$–$3$, $1$–$4$, $2$–$5$. With root $0$, compare these prefixes.

| Prefix | Entry into the square | Can finish? |
| --- | --- | --- |
| $0,2,1$ | $4$ | Yes, via $4,5,6,3,0$ |
| $0,1,2$ | $5$ | No |

In each row the endpoint attaches to one degree-two vertex outside $A=\{3\}$. Any spanning path of a cycle deletes one edge, so its endpoints must be neighbours on the cycle. Vertex $4$ is adjacent to the required exit $3$, while vertex $5$ is opposite it. Replacing the square with a cycle of length $m\ge4$ and attaching the two endpoints to its first and second vertices after $3$ gives the same obstruction at every order $m+3$.

**Minimality.** Equal visited sets with different endpoints require at least three visited vertices. In a graph of order at most six, this leaves at most three unvisited vertices. If $G[U]$ is disconnected and $U$ is nonempty, neither prefix can finish. For each connected residual graph on at most three vertices, every permutation within each degree class preserves adjacency. Restrict those permutations to the two root-attachment types within each degree class so that they also preserve $A$. Equal type counts then give a permutation taking one attachment set to the other and taking legal suffixes bijectively to legal suffixes. They therefore give the same existence answer. Equal endpoints already give the exact key, and the empty residual case uses the closing flag.

The counts can lose the *identity* of legal suffixes as early as order five. Use the visited triangle, one residual edge $3$–$4$, root attachments to both $3$ and $4$, and other attachments $1$–$3$ and $2$–$4$. The two prefixes each finish, using opposite orderings of $3,4$. With fewer than five vertices, distinct endpoints on the same visited set leave at most one unvisited vertex, where the counts determine the exact attachment set.

### Reproduction

From the repository root, run with Python 3.12. The script uses only the standard library.

```sh
python3 research/hamiltonian-cycle/verify_hc_01.py
```

The reference oracle tries every ordering of the unvisited set and checks every edge of the full proposed tour. It groups all legal rooted prefixes separately for each graph, with root fixed to label $0$. Every rooted graph in the orders tested can be relabelled to have that root. A conflict is one profile group with different suffix sets or different existence answers, respectively. The two open-completable columns require a nonempty unvisited set and at least one legal suffix.

| Vertices | Graphs | Prefixes | Subset/end states | Exact attachment states | Open completable subset/end | Open completable attachment | Profile suffix conflicts | Profile decision conflicts |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 8 | 12 | 12 | 11 | 2 | 2 | 0 | 0 |
| 4 | 64 | 240 | 234 | 208 | 45 | 42 | 0 | 0 |
| 5 | 1,024 | 9,728 | 8,848 | 7,606 | 1,864 | 1,670 | 12 | 0 |
| 6 | 32,768 | 860,160 | 680,620 | 562,918 | 156,950 | 135,160 | 2,040 | 0 |

Both the subset/end and exact attachment keys preserved the full suffix sets in every group. At order six the exact key used 13.9% fewer distinct open completable states in this census. The census measures the size of the quotient across all legal prefixes. Fully tabulating that quotient on a complete $n$-vertex graph still visits $2^{n-1}-1$ distinct residual subsets, since every proper subset of the nonroot vertices can remain unvisited. An actual solver can stop early when it finds a cycle.

### Established algorithms and next test

Hamiltonian Cycle is one of Karp's NP-complete problems. A deterministic polynomial-time decision algorithm for arbitrary input graphs would imply $\mathrm{P}=\mathrm{NP}$. The subset/end baseline is the state representation of the classical Bellman–Held–Karp subset dynamic programme. For more general partial solutions that can contain multiple path fragments, Cygan, Kratsch and Nederlof study exactly which endpoint matchings can be joined to form one cycle. That compatibility test supplies a benchmark for comparisons involving more than one fragment. Consulted Karp's reduction, the Princeton lecture derivation of subset dynamic programming, and the abstract and matching-connectivity statement of Cygan, Kratsch and Nederlof. [Karp (1972)](https://www2.seas.gwu.edu/~simhaweb/champalg/tsp/papers/KarpOriginal.pdf) · [Held and Karp (1962)](https://doi.org/10.1137/0110015) · [Princeton lecture](https://www.cs.princeton.edu/courses/archive/spring13/cos423/lectures/IntractabilityIII.pdf) · [Cygan, Kratsch and Nederlof (2018)](https://doi.org/10.1145/3148227)

The square example splits after one round when each type is refined by its neighbours' types and membership in $A$ stays marked. [HC-02](HC-02.md) follows that comparison to stability and determines the smallest remaining decision failure. Automorphisms of $G[U]$ that preserve $A$ give a proved control because they carry each legal completion to a legal completion.

The proof, witness and verifier were prepared with AI assistance. Priority for the exact attachment comparison or the obstruction has not been evaluated.
