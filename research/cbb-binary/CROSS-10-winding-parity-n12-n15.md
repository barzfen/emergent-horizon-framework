# EHF-CBB-CROSS-10 — General winding parity and n=12,15 tests

Date: 2026-11-10. Status: analytic theorem plus executed exhaustive enumeration of balanced proper cyclic three-colour words.

## Definitions
Colours A,B,C cyclically ordered. A proper oriented cyclic word of length n has adjacent unequal colours. Let N+ be the number of transitions A->B, B->C, C->A, and N- the reverse transitions. W=(N+-N-)/3, an integer since the sum of colour increments around a closed word is 0 mod 3.

## Theorem (even winding increments)
For any two proper cyclic three-colour words of the same length n, W' - W belongs to 2Z.

Proof: N+ + N-=n and 3W=N+-N-=2N+-n. For two words of the same n, 3(W'-W)=2(N+'-N+). Since W'-W is an integer and gcd(2,3)=1, 3 divides (N+'-N+), so W'-W=2((N+'-N+)/3) is even. QED.

IMPORTANT LIMITATION: This parity conservation is automatic for *all* proper three-colour cyclic words of fixed n. Indeed W=2(N+/3)-n/3 when n is a multiple of 3, so W mod 2 is fixed by n/3 mod 2; it is not a new dynamical sector invariant and cannot obstruct connectivity between admissible words. The actual nontrivial LR3 invariant is full signed W; LR4 breaks that invariant.

## Exhaustive balanced cyclic-word audit
Words are linear position-indexed cyclic words (no quotient by rotation, reflection, or colour permutations), exactly n/3 of each colour, no equal cyclic neighbours. Directed move instances count each starting word and starting index of LRk, excluding identity-on-colour-word outcomes. All reversals are checked for properness.

n=9: 132 words
n=12: 804 words
n=15: 5196 words

| n | k | signed DeltaW -> number of directed move instances |
| 12 | 2 | -2:1584, +2:1584 |
| 12 | 3 | 0:1008 |
| 12 | 4 | -2:2592, +2:2592 |
| 12 | 5 | -4:288, 0:2304, +4:288 |
| 12 | 6 | -2:2448, +2:2448 |
| 12 | 7 | -4:576, 0:2592, +4:576 |
| 12 | 8 | -6:72, -2:2520, +2:2520, +6:72 |
| 15 | 2 | -2:12060, +2:12060 |
| 15 | 3 | 0:8640 |
| 15 | 4 | -2:20160, +2:20160 |
| 15 | 5 | -4:1980, 0:18720, +4:1980 |
| 15 | 6 | -2:19800, +2:19800 |
| 15 | 7 | -4:4500, 0:22680, +4:4500 |
| 15 | 8 | -6:360, -2:19080, +2:19080, +6:360 |

These confirm the n=9 patterns for k<=7 and reveal ±6 transitions at k=8. Reversal-length parity is NOT itself the source of the even-increment theorem. All transformations between proper words of fixed length have even winding difference.

## Reproduction (Python 3)
```python
from collections import Counter
for n in (9,12,15):
    words=[]
    def rec(w,counts):
        if len(w)==n:
            if w[-1]!=w[0]: words.append(tuple(w))
            return
        for c in range(3):
            if counts[c]<n//3 and (not w or w[-1]!=c):
                counts[c]+=1;w.append(c);rec(w,counts);w.pop();counts[c]-=1
    rec([], [0]*3)
    def wind(w):
        return sum(1 if (w[(i+1)%n]-w[i])%3==1 else -1 for i in range(n))//3
    print('n',n,'balanced proper words',len(words))
    for k in range(2,min(9,n-1)):
        ct=Counter()
        for w in words:
            old=wind(w)
            for i in range(n):
                ix=[(i+j)%n for j in range(k)]
                a=list(w)
                for j,x in zip(ix,reversed([w[j] for j in ix])): a[j]=x
                if tuple(a)==w: continue
                if a[(i-1)%n]==a[i] or a[(i+k-1)%n]==a[(i+k)%n]:continue
                assert all(a[t]!=a[(t+1)%n] for t in range(n))
                ct[wind(a)-old]+=1
        assert all(d%2==0 for d in ct)
        print(k,dict(sorted(ct.items())))
```

## Research implications and next step
Full winding is an LR3-specific invariant but not an LR4 invariant. Even winding difference is a general arithmetic constraint on the proper three-colour state space, not an emergent conserved sector. Investigate more informative invariants: accessible W values, the graph of transitions between winding classes, and constructive LR3+LR4 connectivity for arbitrary balanced n. The observed 1:2:3 ratio from unrelated collinear work is not derived here.
