# EHF-CBB-TRI-04 — Exact local LR3 selection rule and frozen colour bracelets

Date: 2026-11-10. Status: local theorem and exhaustive balanced n=9,12 enumeration. Corrects TRI-02's claim of one frozen colour bracelet.

## Model
Cyclic proper three-colour words over fixed A,B,C (adjacent letters distinct), with fixed equal counts. A nontrivial colour LR3 move swaps the endpoint letters of a length-three substring at positions i,i+2; the middle position is fixed. Rotations and reversals are identified into bracelets, but colour names are not permuted.

## Exact local theorem
For n>=5, a colour-changing LR3 swap is admissible iff the cyclic five-letter neighbourhood at positions i-1 through i+3 has the form X Y X Z X with X,Y,Z pairwise distinct. The move exchanges Y and Z:
XYXZX <-> XZXYX.
Proof: Write neighbourhood (l,a,b,c,r) and swapped (l,c,b,a,r), with a != c. Properness before and after implies b differs from both a,c, hence b is their unique third colour X. Both l and r differ from both a and c, hence l=r=X. Conversely both arrangements are proper. The six oriented instantiations are ABACA<->ACABA, BABCB<->BCBAB, CACBC<->CBCAC. No other colour-changing LR3 move exists.

Corollary: a proper colour word has no admissible *colour-changing* LR3 move iff it contains no cyclic five-letter substring XYXZX with all three colours distinct. It may still allow same-colour endpoint swaps that change the **labelled** Hamiltonian cycle but not its colour word.

## Exhaustive checks
For n=9 balanced (3,3,3): 132 proper linear colour words, 8 dihedral bracelets, 5 bracelet-graph components, sizes [4,1,1,1,1]. Exactly FOUR bracelets have zero colour-changing legal moves. They are:
ABACBACBC
ABCABCABC
ABCABCACB
ABCABCBAC.
The four-class connected component is:
ABABCACBC
ABABCBCAC
ABACABCBC
ABCACABCB.
Three of the four frozen bracelets have |W|=1, while ABCABCABC has |W|=3. Thus winding alone is insufficient, and local arrest completes the component explanation for n=9.

For n=12 balanced (4,4,4): 804 proper linear words, 41 bracelets, 23 bracelet-graph components with sizes [3]*9+[1]*14. Exactly FOURTEEN bracelets have no colour-changing legal moves, and they coincide with the 14 singleton components in this case. Legal colour-changing move-count distribution across the 41 bracelet representatives: {0:14,1:9,2:15,3:3}.

## Reproduction
```python
from itertools import combinations
from collections import Counter

def audit(n):
    words=[]
    for aa in combinations(range(n),n//3):
        rem=[i for i in range(n) if i not in aa]
        for bb in combinations(rem,n//3):
            w=['C']*n
            for i in aa:w[i]='A'
            for i in bb:w[i]='B'
            if all(w[i]!=w[(i+1)%n] for i in range(n)):
                words.append(tuple(w))
    def canon(w):
        return min(tuple(v[i:]+v[:i])
                   for v in (w,w[::-1]) for i in range(n))
    bracelets=sorted(set(map(canon,words)))
    ids={w:i for i,w in enumerate(bracelets)}
    adj=[set() for _ in bracelets]
    legal_counts=[]
    for i,w in enumerate(bracelets):
        count=0
        for j in range(n):
            v=list(w);k=(j+2)%n
            if v[j]==v[k]:continue
            v[j],v[k]=v[k],v[j]
            if all(v[t]!=v[(t+1)%n] for t in range(n)):
                count+=1
                adj[i].add(ids[canon(tuple(v))])
        legal_counts.append(count)
    seen=set();components=[]
    for i in range(len(bracelets)):
        if i in seen:continue
        stack=[i];seen.add(i);comp=[]
        while stack:
            u=stack.pop();comp.append(u)
            for v in adj[u]:
                if v not in seen:seen.add(v);stack.append(v)
        components.append(comp)
    return len(words),len(bracelets),sorted(map(len,components),reverse=True),Counter(legal_counts)

assert audit(9)==(132,8,[4,1,1,1,1],Counter({0:4,1:3,3:1}))
assert audit(12)==(804,41,[3]*9+[1]*14,Counter({0:14,1:9,2:15,3:3}))
print(audit(9),audit(12))
```

## Scope and interpretation
This is a finite-state local selection rule, not a complete invariant for arbitrary n. At n=9 and n=12 the singleton colour-bracelet components coincide with colour-frozen bracelets, but this may fail at larger n: moves may remain within one bracelet. The full labelled graph may have same-colour swaps and additional components. These results do not establish any relationship to QCD/SU(3).

## Next
Seek an invariant or constructive classification of all *mobile* components at larger n; analyze n=15 balanced (5,5,5) with efficient colour-word enumeration, and determine whether distinct mobile components share the same winding and whether local defect patterns characterize them.
