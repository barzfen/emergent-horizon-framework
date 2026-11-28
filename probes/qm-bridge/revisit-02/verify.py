"""Independent check using oriented tours directly and endpoint swaps, no import from probe."""
import itertools,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
root=Path(__file__).resolve().parent
report=json.loads((root/'results.json').read_text())

def rotate_zero(c):
 j=c.index(0);return tuple(c[j:]+c[:j])
def reflected(c):return (0,)+c[:0:-1]
def canonical(c):return min(c,reflected(c))
def key(c):return tuple(sorted(c[::2]))
def admissible(c):
 # Independent local-neighbour definition via undirected edge sets.
 edges={frozenset((a,b)) for a,b in zip(c,c[1:]+c[:1])}
 return all(any(v in e and all((x in {1,2,3})==(v in {1,2,3}) for x in e) for e in edges) for v in c)
checks=[]
for row,trial in zip(report['models'],report['exact_lift_checks']):
 n=row['n'];oriented_states=[(0,)+p for p in itertools.permutations(range(1,n)) if admissible((0,)+p)]
 ss=set(oriented_states); E={}
 for c in oriented_states:
  ev=[]
  for distance in (1,2):
   for j in range(n):
    q=list(c);k=(j+distance)%n;q[j],q[k]=q[k],q[j];d=rotate_zero(q)
    if d in ss and canonical(c)!=canonical(d) and key(canonical(c))==key(canonical(d)):ev.append(d)
  E[c]=ev
 assert len(ss)==2*row['states']
 assert sum(len(E[c]) for c in ss)==2*row['events']
 for c in ss:
  for d,k in Counter(E[c]).items():assert Counter(E[d])[c]==k
 seen=set();components=0
 for c in oriented_states:
  if c in seen:continue
  components+=1;todo=[c];seen.add(c)
  while todo:
   for d in E[todo.pop()]:
    if d not in seen:seen.add(d);todo.append(d)
 assert components==2*row['flat_components']+row['nonflat_components']
 if n==7:
  a=(0,1,2,3,4,5,6);retained={a};todo=[a]
  while todo:
   for d in E[todo.pop()]:
    if d not in retained:retained.add(d);todo.append(d)
  assert len(retained)==6
 # Verify nontrivial closed walk by following actual oriented swaps.
 w=row['first_negative_closed_walk'][0];c=tuple(w['walk'][0]);start=c;orientation=0
 for target,b in zip(w['walk'][1:],w['edge_flip_bits']):
  orientation^=b;d=tuple(target);desired=reflected(d) if orientation else d
  assert desired in E[c];c=desired
 assert c==reflected(start)
 # Exact independent forward process on oriented tours.
 P={tuple(trial['seed']):F(1)};first_paths={tuple(trial['seed']):[]};path_witness=None
 for saved in trial['history']:
  plus=defaultdict(F);minus=defaultdict(F)
  for c,p in P.items():(plus if c==canonical(c) else minus)[canonical(c)]+=p
  assert sum(P.values())==1
  assert str(sum(abs(plus[c]-minus[c]) for c in set(plus)|set(minus)))==saved['signed_L1']
  assert str(sum((plus[c]-minus[c])**2 for c in set(plus)|set(minus)))==saved['signed_square_sum']
  overlap=[c for c in set(plus)&set(minus) if plus[c]>0 and minus[c]>0]
  assert len(overlap)==saved['overlap_states']
  if saved['example']:
   e=saved['example'][0];q=tuple(e['state'])
   assert str(plus[q])==e['positive'] and str(minus[q])==e['negative']
   if path_witness is None:
    p1=first_paths[q];p2=first_paths[reflected(q)]
    assert len(p1)==len(p2)==saved['steps']
    path_witness={'steps':saved['steps'],'same_undirected_endpoint':q,'oriented_path_1':[trial['seed']]+p1,'oriented_path_2':[trial['seed']]+p2,'probability_plus':str(plus[q]),'probability_minus':str(minus[q])}
  new=defaultdict(F);paths={}
  for c,p in P.items():
   ev=E[c] or [c]
   for d in ev:
    new[d]+=p/len(ev)
    if d not in paths:paths[d]=first_paths[c]+[d]
  P,first_paths=new,paths
 checks.append({'n':n,'oriented_states':len(ss),'oriented_components':components,'exact_forward_steps_checked':13,'same_length_opposite_orientation_witness':path_witness,'checks':'PASS'})
(root/'verification.json').write_text(json.dumps({'checks':checks,'status':'PASS'},indent=2)+'\n')
print(json.dumps({'status':'PASS','models':[{'n':c['n'],'oriented_states':c['oriented_states'],'oriented_components':c['oriented_components'],'first_overlap':None if c['same_length_opposite_orientation_witness'] is None else c['same_length_opposite_orientation_witness']['steps']} for c in checks]},indent=2))
