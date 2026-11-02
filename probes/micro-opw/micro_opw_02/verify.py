"""Independent edge-set/vertex-neighbour verification, without importing the main probe."""
import sys,json,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'micro_opw_01'))
from verify_witness import edges, representative

def main():
    bit=lambda v:int(v in (1,2,3))
    records={}
    for p in itertools.permutations(range(1,7)):
        g=edges((0,)+p)
        if g in records:continue
        c,ng=representative(g,7)
        if all(any(bit(v)==bit(w) for w in ng[v]) for v in range(7)):
            records[g]=(c,ng)
    adj={g:set() for g in records}
    for g,(c,_) in records.items():
        for i in range(7):
            r=c[i:]+c[:i]
            h=edges(r[:3][::-1]+r[3:])
            if h in records and set(records[h][0][::2])==set(c[::2]) and h!=g:adj[g].add(h)
    def component(seed):
        seen={seed};todo=[seed]
        while todo:
            for g in adj[todo.pop()]-seen:seen.add(g);todo.append(g)
        return seen
    a=component(edges(tuple(range(7))))
    b=component(edges((0,5,4,3,2,1,6)))
    assert len(a)==4 and len(b)==2 and a.isdisjoint(b)
    assert {sum(bit(w) for w in records[g][1][0]) for g in a}=={1}
    assert {sum(bit(w) for w in records[g][1][0]) for g in b}=={0}
    assert {tuple(sorted(sum(bit(w) for w in ng[v]) for v in range(7))) for _,ng in records.values()}=={(0,0,1,1,1,1,2)}
    # Verify all 351 component-pair comparisons independently in edge-set representation.
    unseen=set(records);cs=[]
    while unseen:
        x=component(next(iter(unseen)));cs.append(x);unseen-=x
    pairs=sum(any({sum(bit(w) for w in records[g][1][v]) for g in x}.isdisjoint({sum(bit(w) for w in records[g][1][v]) for g in y}) for v in range(7)) for x,y in itertools.combinations(cs,2))
    reference=json.loads(Path(__file__).with_name('results.json').read_text())
    assert pairs==reference['secondary_all_component_pair_scan']['pairs_with_some_perfect_local_bit_count']==333
    out={'states':len(records),'components':len(cs),'witness_component_sizes':[len(a),len(b)],'vertex0_type1_neighbour_counts':{'A':[1],'B':[0]},'unanchored_neighbour_count_histogram':[0,0,1,1,1,1,2],'perfect_local_component_pairs':pairs,'checks':'PASS'}
    Path(__file__).with_name('independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
