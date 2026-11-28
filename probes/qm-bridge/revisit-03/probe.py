"""Represent orientation by an ordered adjacent marker pair and test its classical readout."""
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction as F
import importlib.util,json,hashlib
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'revisit-02'/'probe.py'
spec=importlib.util.spec_from_file_location('orientation_source',SOURCE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def bit(v):return int(v in {1,2,3})
def swap(v,a,b):return b if v==a else a if v==b else v
def neigh(c,v):
 i=c.index(v);return c[(i-1)%len(c)],c[(i+1)%len(c)]
def shift(c,p,forward=True):
 u,v=p
 if forward:return (v,next(w for w in neigh(c,v) if w!=u))
 return (next(w for w in neigh(c,u) if w!=v),u)
def mark_sign(c,p):
 u,v=p;i=c.index(u)
 assert v in neigh(c,u)
 return int(c[(i+1)%len(c)]!=v)
def transport(c,p,s,l):
 a,b=c[s],c[(s+l-1)%len(c)]
 d=m.canon(m.move(c,s,l));pair=tuple(swap(v,a,b) for v in p)
 assert pair[1] in neigh(d,pair[0])
 return d,pair

def port_read(c,p,port=0):
 # Freeze structural moves for this explicit readout protocol. Circulate until marker tail reaches port.
 steps=0
 while p[0]!=port:
  p=shift(c,p);steps+=1
  assert steps<len(c)
 return bit(p[1]),steps

def all_pairs(c):
 return [(c[i],c[(i+direction)%len(c)]) for i in range(len(c)) for direction in (1,-1)]

def joint_signature(c,p,ev,keep_direction,marker_gate=False):
 # Fixed-clock step: 1/2 structural attempt (uniform legal indexed events), 1/4 each shift.
 out=defaultdict(F)
 def key(d,q):return (d,q if keep_direction else tuple(sorted(q)))
 events=ev or [(c,0,0,0)]
 for d,flip,s,l in events:
  if marker_gate and l and not ({c[s],c[(s+l-1)%len(c)]}&set(p)):
   out[key(c,p)]+=F(1,2*len(events));continue
  q=p if l==0 else transport(c,p,s,l)[1]
  out[key(d,q)]+=F(1,2*len(events))
 out[key(c,shift(c,p))]+=F(1,4)
 out[key(c,shift(c,p,False))]+=F(1,4)
 assert sum(out.values())==1
 return dict(out)

censuses=[]
for n in (7,9):
 ss,events=m.build(n,{1,2,3});checked=0;symmetric_port=0;backreactive=0
 for c in ss:
  if bit(neigh(c,0)[0])==bit(neigh(c,0)[1]):symmetric_port+=1
  carrier_signatures=set()
  for p in all_pairs(c):
   z=mark_sign(c,p)
   assert shift(c,shift(c,p),False)==p
   assert mark_sign(c,shift(c,p))==z
   # Erasing marker roles gives identical reduced kernels for the two physical role assignments.
   assert joint_signature(c,p,events[c],False)==joint_signature(c,p[::-1],events[c],False)
   gated=joint_signature(c,p,events[c],False,True)
   assert gated==joint_signature(c,p[::-1],events[c],False,True)
   marginal=defaultdict(F)
   for (d,q),prob in gated.items():marginal[d]+=prob
   carrier_signatures.add(tuple(sorted(marginal.items())))
   for d,b,s,l in events[c]:
    target,pair=transport(c,p,s,l)
    assert target==d and mark_sign(d,pair)==(z^b)
    reverse_events=[(q,f,t,k) for q,f,t,k in events[d] if q==c and transport(d,pair,t,k)[1]==p]
    assert reverse_events
    checked+=1
  if len(carrier_signatures)>1:backreactive+=1
 censuses.append({'n':n,'carrier_states':len(ss),'ordered_marker_states':2*n*len(ss),'marker_event_checks':checked,'port0_orientation_distinguishable_states':len(ss)-symmetric_port,'port0_orientation_indistinguishable_states':symmetric_port,'unordered_marker_strong_lumpability':'PASS','gated_unordered_strong_lumpability':'PASS','states_with_marker_dependent_carrier_kernel':backreactive})

inp=json.loads((ROOT/'input_witness.json').read_text());w=inp['checks'][1]['same_length_opposite_orientation_witness']
paths=[]
for name in ('oriented_path_1','oriented_path_2'):
 path=[tuple(c) for c in w[name]];c=m.canon(path[0]);pair=(0,1);schedule=[]
 for before,after in zip(path,path[1:]):
  matches=[(s,l) for l in (2,3) for s in range(9) if m.move(before,s,l)==after]
  assert matches
  # Match the actual oriented event to the canonical chart used for transport.
  # Raw oriented history itself carries marker endpoints under its active endpoint-label swap.
  s,l=matches[0];a,b=before[s],before[(s+l-1)%9]
  pair=tuple(swap(v,a,b) for v in pair);c=m.canon(after)
  assert pair[1] in neigh(c,pair[0])
  assert mark_sign(c,pair)==int(after!=c)
  schedule.append({'oriented_source':before,'start':s,'length':l,'swapped_labels':[a,b],'oriented_target':after,'marker_after':pair})
 out,wait=port_read(c,pair)
 # Uniformize pointer position along its direction: same unordered-edge preparation in both histories.
 mixed=[pair]
 for _ in range(8):mixed.append(shift(c,mixed[-1]))
 assert len(set(mixed))==9 and len({port_read(c,q)[0] for q in mixed})==1
 unordered=Counter(tuple(sorted(q)) for q in mixed)
 paths.append({'path':name,'final_carrier':c,'final_markers':pair,'direction_bit':mark_sign(c,pair),'port0_next_type':out,'circulation_steps_to_port':wait,'schedule':schedule,'uniformized_directed_pairs':mixed,'uniformized_unordered_edges':sorted([list(e) for e in unordered]),'readout_success_equal_priors':'1'})
assert paths[0]['final_carrier']==paths[1]['final_carrier']
assert paths[0]['port0_next_type']==1 and paths[1]['port0_next_type']==0
assert paths[0]['uniformized_unordered_edges']==paths[1]['uniformized_unordered_edges']
# Matched unordered preparations have identical support and uniform weights, so TV=0 exactly.
# Detector reads next type once at port; optional reversible copy q -> q XOR type(v).
for q in (0,1):
 for t in (0,1):assert (q^t)^t==q
# Live first-arrival reader: no structural freeze, both directional roles still retained.
# Detector fires when marker tail first reaches port 0; output is type at the head.
# Fixed 12-step timeout is an explicit third outcome. Everything uses exact fractions.
def live_reader(initial_pairs,gated):
 carrier=tuple(paths[0]['final_carrier']);P={(carrier,tuple(p)):F(1,9) for p in initial_pairs};caught={0:F(0),1:F(0)};records=[]
 for t in range(13):
  remaining={}
  for (c,p),weight in P.items():
   if p[0]==0:caught[bit(p[1])]+=weight
   else:remaining[c,p]=weight
  P=remaining
  assert sum(P.values())+sum(caught.values())==1
  records.append({'step':t,'output0':str(caught[0]),'output1':str(caught[1]),'timeout':str(sum(P.values()))})
  if t==12:break
  nxt=defaultdict(F)
  for (c,p),weight in P.items():
   for state,prob in joint_signature(c,p,events[c],True,gated).items():nxt[state]+=weight*prob
  P=dict(nxt)
 return records
live=[]
for gated in (False,True):
 left=live_reader(paths[0]['uniformized_directed_pairs'],gated);right=live_reader(paths[1]['uniformized_directed_pairs'],gated)
 records=[]
 for a,b in zip(left,right):
  tv=sum(abs(F(a[k])-F(b[k])) for k in ('output0','output1','timeout'))/2
  records.append({'step':a['step'],'plus':a,'minus':b,'TV':str(tv),'equal_prior_success':str((1+tv)/2)})
 live.append({'marker_gate':gated,'records':records})
result={'censuses':censuses,'retained_histories':paths,'live_first_port_reader':live,'matched_unordered_preparation_TV':'0','directed_port_output_TV':'1','equal_prior_success_unordered':'1/2','equal_prior_success_directed_port':'1','carrier_backreaction':'primary passive co-transport plus secondary marker-gated structural attempts; carrier frozen during readout','assumptions':['distinguishable ordered markers','endpoint-permutation co-transport during carrier moves','named detectable port 0','readout stage freezes carrier','direction-preserving circulation and type-sensitive detector','uniform position mixing for matched preparation comparison'],'source_probe_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'input_witness_sha256':hashlib.sha256((ROOT/'input_witness.json').read_bytes()).hexdigest(),'implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':'PASS'}
(ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'censuses':censuses,'paths':[{'direction_bit':p['direction_bit'],'marker':p['final_markers'],'readout':p['port0_next_type']} for p in paths],'matched_unordered_TV':'0','directed_readout_TV':'1','checks':'PASS'},indent=2))
