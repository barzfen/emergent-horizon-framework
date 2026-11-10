# EHF-CBB-TRI-01 — Balanced three-colour LR3 quotient at n=9

Date: 2026-11-10. Status: independently executed exhaustive enumeration of balanced colour words and exact reduced transition counts. No identification with QCD or SU(3).

## Model
Nine cyclic positions, exactly three A, three B and three C. Colour names are fixed (not quotiented by S3); only rotations and reversal are identified. The 1680 linear words reduce to 94 dihedral bracelets. LR3 reverses three consecutive positions, equivalently swaps colours at positions i and i+2. Count all nine proposals, including those that leave the bracelet class unchanged. These self-class moves need not be self-loops in the fully labelled cycle graph.

## Rules and results
| rule | valid linear words | valid bracelets | connected components in bracelet graph |
| unrestricted | 1680 | 94 | 1 |
| MICRO: every position touches a same-colour neighbour | 18 | 1 | 1 |
| separation: every adjacent pair has different colours | 132 | 8 | 5 |

The five separation components have bracelet-class sizes [4,1,1,1,1]. The bracelet ABCABCABC has zero legal LR3 proposals and is isolated even at the word level. MICRO has one bracelet AAABBBCCC and three of nine proposals remain MICRO-valid (all stay within its bracelet class).

For separation, the eight bracelets and numbers of legal proposals are:
ABABCACBC 5
ABABCBCAC 9
ABACABCBC 5
ABACBACBC 2
ABCABCABC 0
ABCABCACB 2
ABCABCBAC 2
ABCACABCB 5

Note: connected components are of the *colour-bracelet quotient*, not necessarily of all individually labelled Hamiltonian cycles. The quotient has weighted transition counts, and some within-class moves can change the labelled configuration. The full labelled-component structure has not yet been tested.

## Exact general quotient
For any fixed colour counts and any number of colours, LR3 swaps positions i and i+2. The dihedral bracelet of the colour word is an equitable partition of the unrestricted LR3 graph. If admissibility is a predicate of the colour bracelet (MICRO, separation), restriction to legal colour bracelets retains equitability. If Pi or label-order constraints are added, this may fail, as shown in BIN-12.

## Reproduction
```python
from itertools import permutations
from collections import Counter
n=9
words=set(permutations('AAABBBCCC'))
def canon(w):
    w=tuple(w);r=w[::-1]
    return min([w[i:]+w[:i] for i in range(n)]
               +[r[i:]+r[:i] for i in range(n)])
classes=sorted({canon(w) for w in words})
index={w:i for i,w in enumerate(classes)}
M=[[0]*len(classes) for _ in classes]
for a,w in enumerate(classes):
    for i in range(n):
        v=list(w);j=(i+2)%n;v[i],v[j]=v[j],v[i]
        M[a][index[canon(v)]]+=1
assert len(words)==1680 and len(classes)==94
assert all(sum(row)==9 for row in M)
def micro(w):
    return all(w[i]==w[(i-1)%n] or w[i]==w[(i+1)%n]
               for i in range(n))
def sep(w):
    return all(w[i]!=w[(i+1)%n] for i in range(n))
def component_sizes(allowed):
    allowed=set(allowed);seen=set();sizes=[]
    for a in allowed:
        if a in seen:continue
        stack=[a];seen.add(a);size=0
        while stack:
            u=stack.pop();size+=1
            for v,cnt in enumerate(M[u]):
                if cnt and v in allowed and v not in seen:
                    seen.add(v);stack.append(v)
        sizes.append(size)
    return sorted(sizes,reverse=True)
for pred,expected in ((lambda w:True,(1680,94,[94])),
                      (micro,(18,1,[1])),
                      (sep,(132,8,[4,1,1,1,1]))):
    good=[i for i,w in enumerate(classes) if pred(w)]
    assert (sum(pred(w) for w in words),len(good),
            component_sizes(good))==expected
```

## Cautions and next probes
The 94x94 quotient is exact for colour-pattern transition counts, not for all label-sensitive observables. Three discrete colours are not QCD colour charge; S3 colour-name permutation is not SU(3). Compare full labelled Hamiltonian-cycle components, distinguish rejection/stay versus legal-move protocols, and test n=12 balanced 4+4+4 to see whether the separation-sector phenomenon persists.
