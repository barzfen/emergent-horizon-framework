"""Exact local-access audit for the retained seven-vertex MICRO-OPW witness."""
import itertools
import json
import hashlib
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'micro_opw_01'))
from probe import canon, pi, reversal


def bit(v): return int(v in (1,2,3))


def valid(c):
    return all(bit(c[i]) in (bit(c[(i-1)%7]),bit(c[(i+1)%7])) for i in range(7))


def neighbourhood(c,v):
    i=c.index(v)
    return (c[(i-1)%7],c[(i+1)%7])


def necklace(c):
    b=tuple(map(bit,c))
    return min(b[i:]+b[:i] for b in (b,b[::-1]) for i in range(7))


def orbit(adj,seed):
    seen={seed}; todo=[seed]
    while todo:
        for x in adj[todo.pop()]-seen:
            seen.add(x);todo.append(x)
    return sorted(seen)


def tv(a,b):
    ka=Counter(a); kb=Counter(b)
    return sum(abs(F(ka[k],len(a))-F(kb[k],len(b))) for k in ka.keys()|kb.keys())/2


def exact_solve(a,b):
    a=[list(row)+[rhs] for row,rhs in zip(a,b)]
    for i in range(len(a)):
        pivot=next(j for j in range(i,len(a)) if a[j][i])
        a[i],a[pivot]=a[pivot],a[i]
        scale=a[i][i]
        a[i]=[v/scale for v in a[i]]
        for j in range(len(a)):
            if j!=i:
                scale=a[j][i]
                a[j]=[v-scale*w for v,w in zip(a[j],a[i])]
    return [row[-1] for row in a]


def main():
    states=sorted((0,)+p for p in itertools.permutations(range(1,7)) if p[0]<p[-1] and valid((0,)+p))
    state_set=set(states)
    adj={c:{d for i in range(7) if (d:=reversal(c,i,3)) in state_set and pi(c)==pi(d)}-{c} for c in states}
    A=(0,1,2,3,4,5,6)
    B=(0,5,4,3,2,1,6)
    ca,cb=orbit(adj,A),orbit(adj,B)
    assert len(states)==72 and len(ca)==4 and len(cb)==2 and set(ca).isdisjoint(cb)
    assert pi(A)==pi(B) and reversal(A,6,2)==B
    assert all(adj[c]<=set(ca) for c in ca) and all(adj[c]<=set(cb) for c in cb)
    assert all(adj[c] for c in ca+cb)
    allcomps=[];unseen=set(states)
    while unseen:
        comp=orbit(adj,next(iter(unseen)));allcomps.append(comp);unseen-=set(comp)
    assert len(allcomps)==27
    readers={
        'unanchored_binary_necklace':necklace,
        'unanchored_neighbour_bit_count_histogram':lambda c:tuple(sorted(sum(bit(w) for w in neighbourhood(c,v)) for v in range(7))),
        'number_of_bit1_neighbours_at_vertex0':lambda c:sum(bit(v) for v in neighbourhood(c,0)),
        'edge_0_1_present':lambda c:int(1 in neighbourhood(c,0)),
        'neighbour_label_set_at_vertex0':lambda c:tuple(sorted(neighbourhood(c,0))),
    }
    results={}
    for name,r in readers.items():
        va=[r(c) for c in ca];vb=[r(c) for c in cb]
        d=tv(va,vb)
        results[name]={'A_values':list(sorted(set(va))),'B_values':list(sorted(set(vb))),'uniform_within_component_TV':str(d),'equal_prior_success':str((1+d)/2),'supports_disjoint':set(va).isdisjoint(vb)}
    assert results['unanchored_binary_necklace']['uniform_within_component_TV']=='0'
    assert results['unanchored_neighbour_bit_count_histogram']['uniform_within_component_TV']=='0'
    assert results['number_of_bit1_neighbours_at_vertex0']['A_values']==[1]
    assert results['number_of_bit1_neighbours_at_vertex0']['B_values']==[0]
    assert results['edge_0_1_present']['equal_prior_success']=='3/4'
    local={}
    for v in range(7):
        aa=sorted({sum(bit(w) for w in neighbourhood(c,v)) for c in ca})
        bb=sorted({sum(bit(w) for w in neighbourhood(c,v)) for c in cb})
        local[v]={'A_values':aa,'B_values':bb,'disjoint':set(aa).isdisjoint(bb)}
    # Explicit first-spatial-hop experiment. Structural rearrangements continue at rate eta per LR3 edge.
    # Probe stays at labelled vertex 0 until one spatial jump occurs; each current neighbour has rate 1/2.
    # The absorption equation is (I + eta*L)h = bit1_exit_rate. Solve with rational arithmetic.
    absorption=[]
    for eta in (F(0),F(1,10),F(1),F(10)):
        row={'eta_per_LR3_edge':str(eta)}
        for name,comp in [('A',ca),('B',cb)]:
            mat=[[F(int(i==j)) + eta*(F(len(adj[x])) if i==j else F(-int(y in adj[x]))) for j,y in enumerate(comp)] for i,x in enumerate(comp)]
            rhs=[F(sum(bit(v) for v in neighbourhood(c,0)),2) for c in comp]
            h=exact_solve(mat,rhs)
            target=F(1,2) if name=='A' else F(0)
            assert all(x==target for x in h)
            assert all(sum(mat[i][j]*h[j] for j in range(len(comp)))==rhs[i] for i in range(len(comp)))
            row[name+'_first_hop_bit1_probability']=str(h[0])
        absorption.append(row)
    # Pointwise value constancy proves the same result for any within-component starting law/rates
    # with equal 1/2 spatial edge rates, without assuming equilibrium or independence of carrier samples.
    assert all(sum(bit(v) for v in neighbourhood(c,0))==1 for c in ca)
    assert all(sum(bit(v) for v in neighbourhood(c,0))==0 for c in cb)
    repetitions=[{'trials':m,'error_given_A':str(F(1,2**m)),'error_given_B':'0','equal_prior_success':str(1-F(1,2**(m+1)))} for m in (1,2,3,5,10)]
    # Fraction of pairs of all 27 components distinguishable by one count at a single anchored vertex.
    # This is a bounded secondary diagnostic, not a fitted replacement for the selected witness.
    perfect_pairs=0
    for x,y in itertools.combinations(allcomps,2):
        if any({sum(bit(w) for w in neighbourhood(c,v)) for c in x}.isdisjoint({sum(bit(w) for w in neighbourhood(c,v)) for c in y}) for v in range(7)):
            perfect_pairs+=1
    output={'n':7,'bit1_vertices':[1,2,3],'A_component':ca,'B_component':cb,'readers':results,'local_bit_counts_by_anchor':local,'ongoing_rearrangement_first_hop':absorption,'repeated_first_hop_design':repetitions,'secondary_all_component_pair_scan':{'pairs':351,'pairs_with_some_perfect_local_bit_count':perfect_pairs},'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_probe_sha256':hashlib.sha256((Path(__file__).resolve().parents[1]/'micro_opw_01'/'probe.py').read_bytes()).hexdigest(),'checks':'PASS'}
    Path(__file__).with_name('results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
