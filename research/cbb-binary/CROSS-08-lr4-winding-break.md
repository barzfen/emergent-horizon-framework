# EHF-CBB-CROSS-08 — LR4 breaks absolute winding conservation

Date: 2026-11-10. Status: exhaustive colour-word computation for n=9 and explicit witness. Distinguish this discrete winding from the unrelated collinear amplitude 1:2:3 ratio.

## Model
Proper cyclic three-colour words of length 9, with exactly three occurrences each of A,B,C. A proper word has no equal adjacent colours. LRk reverses k consecutive cyclic positions and is admissible when the resulting word is proper. Oriented colour winding W=(1/3) sum_i s_i, where s_i=+1 for A->B->C->A and -1 for opposite direction. Reversing cycle orientation negates W, so |W| is invariant under reversal of the whole cycle.

## Exact witness
w=ABACBACBC, W=-1.
Apply LR4 at cyclic position i=7 (zero-based), reversing the positions (7,8,0,1). The result is v=CBACBACBA, W=-3.
Both are balanced and proper. Hence LR4 does not conserve |W|. In contrast, TRI-03 proved LR3 conserves W for oriented proper three-colour cycles.

## Exhaustive n=9 colour-word audit
There are 132 balanced proper linear colour words with fixed positions and fixed colour names. Across all starting words and cyclic LR4 locations, there are 648 nontrivial admissible directed move instances.

Signed winding transitions, counted as directed move instances:
(-1,+1):270; (+1,-1):270;
(-1,-3):27; (+1,+3):27;
(+3,+1):27; (-3,-1):27.

Thus 108 of 648 admissible LR4 move instances change |W|. The other 540 flip W's sign but preserve |W|. Counts include multiplicities from different start positions/move locations, not undirected edges or bracelet transitions.

## Reproduction
```python
from itertools import combinations
from collections import Counter
n=9;words=[]
for aa in combinations(range(n),3):
    rem=[i for i in range(n) if i not in aa]
    for bb in combinations(rem,3):
        w=['C']*n
        for i in aa:w[i]='A'
        for i in bb:w[i]='B'
        if all(w[i]!=w[(i+1)%n] for i in range(n)):
            words.append(''.join(w))
def winding(w):
    return sum(1 if ('ABC'.index(w[(i+1)%n])-'ABC'.index(w[i]))%3==1 else -1 for i in range(n))//3
stats=Counter()
for w in words:
    for i in range(n):
        v=list(w);ix=[(i+j)%n for j in range(4)]
        for a,b in zip(ix,[w[t] for t in ix][::-1]):v[a]=b
        v=''.join(v)
        if v==w or any(v[j]==v[(j+1)%n] for j in range(n)):continue
        stats[(winding(w),winding(v))]+=1
assert len(words)==132
assert sum(stats.values())==648
assert sum(count for (a,b),count in stats.items() if abs(a)!=abs(b))==108
assert winding('ABACBACBC')==-1 and winding('CBACBACBA')==-3
print(stats)
```

## Connection to earlier EHF collinear work
The earlier reported 1:2:3 ratio concerns squared norms of singlet, symmetric octet and 27 projections in a specific tree-level MHV collinear-amplitude setting (equal split, shared real spinor chart); its broader theorem and novelty remain to be independently verified. These quantities are not the same as the winding or LRk transition counts here. There is currently no derived map linking the two. A meaningful comparison would require matching definitions and invariant representations, not seeking the ratio in unrelated counts.

## Next
Derive a general local formula for ΔW under LRk and classify which k preserve |W| identically. Audit n=12 and 15, keeping balanced colour words and fixed colour names. Compare transformation-induced invariant sectors, not raw numerological ratios.
