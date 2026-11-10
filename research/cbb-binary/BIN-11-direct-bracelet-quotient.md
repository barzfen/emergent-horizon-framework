# EHF-CBB-BIN-11 — Direct binary-bracelet LR3 quotient

Date: 2026-11-10. Status: exact general theorem for unrestricted LR3 and computational verification through n=13.

## Theorem (equitable binary-bracelet quotient)
Let n>=5 and 0<=m<=n. Fix a marked set R of m labels. Map each undirected labelled Hamiltonian n-cycle to the binary cyclic word w of length n indicating marked positions, modulo the dihedral group D_n (rotation and reversal). An unrestricted LR3 reversal replaces positions (i,i+1,i+2) by their reverse, equivalently swaps w_i and w_{i+2}. For any two binary bracelets a,b, the number of LR3 moves from a cycle in class a to class b is
M[a,b]=sum_{i=0}^{n-1} 1{canon(swap_{i,i+2}(w))=b},
where w is any representative of a. This number is representative-independent, since dihedral symmetries permute the n move positions. Therefore the partition is equitable and M is an exact quotient of the full labelled-cycle LR3 adjacency operator. This proof requires no enumeration of labelled Hamiltonian cycles.

If a swap leaves the binary word unchanged, count it as a self-class transition: in the full labelled-cycle system the LR3 move still changes the labelled cycle, except at very small n outside the intended n>=5 regime.

## Reversibility
Let s_a be the size of bracelet a as an orbit of binary words under D_n. The stationary distribution for K=M/n is pi_a=s_a/binomial(n,m). Because each swap is an involution, s_a M[a,b]=s_b M[b,a]. Thus K is reversible in the weighted inner product, even though M need not be symmetric.

## Observational connection
For n=2m+1, adding vertex n to an n-cycle and observing the (m+1)+(m+1) LR3 parity sector containing the new vertex selects a fixed m-subset R iff R is independent on the old n-cycle. The unique bracelet with all gaps >=2 has gaps (2,...,2,3), so its indicator is an exact observable on this quotient. The original output-channel column equals this indicator divided by n.

## Verified class counts
| n | m | labelled undirected Hamiltonian cycles (n-1)!/2 | binary bracelet classes |
|---|---|---:|---:|
| 5 | 2 | 12 | 2 |
| 7 | 3 | 360 | 4 |
| 9 | 4 | 20,160 | 10 |
| 11 | 5 | 1,814,400 | 26 |
| 13 | 6 | 239,500,800 | 76 |
| 15 | 7 | 43,589,145,600 | 232 |
| 17 | 8 | 10,461,394,944,000 | 750 |

Counts 5-13 checked with quotient matrices and detailed balance. Counts 15,17 obtained by binary bracelet enumeration only. The count of classes is given in general by Burnside's lemma: B(n,m)=(1/(2n)) sum_{g in D_n} #{binary words w of length n and weight m fixed by g}. This is an exact counting formula.

## Reproducible standalone code
```python
from itertools import combinations
from collections import Counter
from math import comb, factorial

def canonical(word):
    w=tuple(word); n=len(w); r=w[::-1]
    return min([w[i:]+w[:i] for i in range(n)]
               +[r[i:]+r[:i] for i in range(n)])

def bracelets(n,m):
    classes=set()
    for marked in combinations(range(n),m):
        w=[0]*n
        for i in marked: w[i]=1
        classes.add(canonical(w))
    return sorted(classes)

def quotient(n,m):
    classes=bracelets(n,m)
    index={w:i for i,w in enumerate(classes)}
    M=[[0]*len(classes) for _ in classes]
    orbit_sizes=[]
    for a,w in enumerate(classes):
        reverse=w[::-1]
        orbit_sizes.append(len(set(
            [w[i:]+w[:i] for i in range(n)]
            +[reverse[i:]+reverse[:i] for i in range(n)]
        )))
        for i in range(n):
            v=list(w);j=(i+2)%n
            v[i],v[j]=v[j],v[i]
            M[a][index[canonical(v)]]+=1
    assert all(sum(row)==n for row in M)
    assert sum(orbit_sizes)==comb(n,m)
    assert all(orbit_sizes[a]*M[a][b]==orbit_sizes[b]*M[b][a]
               for a in range(len(M)) for b in range(len(M)))
    return classes,M,orbit_sizes

for n in (5,7,9,11,13):
    classes,M,sizes=quotient(n,(n-1)//2)
    print(n,len(classes), 'cycles',factorial(n-1)//2)
```

## Limitations and next work
This is an exact lumping for the **marked/unmarked LR3 dynamics**. It is not an exact description of all label-sensitive observables or of MICRO/Pi constraints unless those rules are constant on bracelet classes. The quotient size still grows exponentially in n, but is vastly smaller than factorially many labelled cycles. Future work: obtain explicit transfer rules in cyclic gap coordinates, symbolic characteristic/minimal polynomials for general n, and identify admissibility constraints compatible with the quotient.
