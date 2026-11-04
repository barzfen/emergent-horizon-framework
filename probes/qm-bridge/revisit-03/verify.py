"""Independent slot-based marker transport and unordered-kernel verification; no probe imports."""
from pathlib import Path
from itertools import permutations
from collections import Counter,defaultdict
from fractions import Fraction as F
import json
P=Path(__file__).resolve().parent
saved=json.loads((P/'results.json').read_text())
def edge_set(c):return {frozenset((c[i-1],c[i])) for i in range(len(c))}
def canonical(c):
 i=c.index(0);c=tuple(c[i:]+c[:i]);return min(c,(0,)+c[:0:-1])
def admissible(c):
 e=edge_set(c)
 return all(any(v in a and all((w in (1,2,3))==(v in (1,2,3)) for w in a) for a in e) for v in c)
def slot_event(c,start,length,i,direction):
 # Reversal changes the vertex occupying a slot; keep the marker slots attached to it.
 a=list(c);slots=[(start+j)%len(c) for j in range(length)]
 for pos,v in zip(slots,[c[k] for k in slots][::-1]):a[pos]=v
 return canonical(a),(a[i],a[(i+direction)%len(c)])
def pair_shift(c,i,direction,forward):
 j=(i+(direction if forward else -direction))%len(c)
 return c[j],c[(j+direction)%len(c)]
checks=[]
for reference in saved['censuses']:
 n=reference['n'];event_table={};states=[(0,)+p for p in permutations(range(1,n)) if p[0]<p[-1] and admissible((0,)+p)];ss=set(states)
 count=0;responsive=0;backreaction=0
 for c in states:
  if (c[1] in (1,2,3))!=(c[-1] in (1,2,3)):responsive+=1
  legal=[]
  for l in (2,3):
   for s in range(n):
    target,_=slot_event(c,s,l,0,1)
    if target in ss and target!=c and set(target[::2])==set(c[::2]):legal.append((s,l,target))
  event_table[c]=legal
  signatures=[]
  for i in range(n):
   for direction in (1,-1):
    pair=(c[i],c[(i+direction)%n]);swapped_i=(i+direction)%n
    for gated in (False,True):
     # Compare role assignments via slot coordinates, independent of active label permutations.
     laws=[]
     for j,dr in ((i,direction),(swapped_i,-direction)):
      law=defaultdict(F);q0=(c[j],c[(j+dr)%n]);choices=legal or [(0,0,c)]
      for s,l,d in choices:
       if l and not (gated and not ({c[s],c[(s+l-1)%n]}&set(q0))):
        z,q=slot_event(c,s,l,j,dr)
        assert z==d
       else:z,q=c,q0
       law[(z,tuple(sorted(q)))]+=F(1,2*len(choices))
      for fw in (False,True):law[(c,tuple(sorted(pair_shift(c,j,dr,fw))))]+=F(1,4)
      assert sum(law.values())==1;laws.append(dict(law))
     assert laws[0]==laws[1]
     if gated:
      marginal=defaultdict(F)
      for (d,q),p in laws[0].items():marginal[d]+=p
      signatures.append(tuple(sorted(marginal.items())))
    for s,l,d in legal:
     _,q=slot_event(c,s,l,i,direction)
     assert frozenset(q) in edge_set(d)
     count+=1
  if len(set(signatures))>1:backreaction+=1
 assert len(states)==reference['carrier_states'] and count==reference['marker_event_checks']
 assert responsive==reference['port0_orientation_distinguishable_states']
 assert backreaction==reference['states_with_marker_dependent_carrier_kernel']
 checks.append({'n':n,'carrier_states':len(states),'marker_events_checked':count,'responsive_ports':responsive,'backreactive_carrier_states':backreaction,'both_unordered_kernel_checks':'PASS'})
for entry in saved['retained_histories']:
 pair=(0,1)
 for ev in entry['schedule']:
  c=tuple(ev['oriented_source']);d=tuple(ev['oriented_target']);i=c.index(pair[0]);direction=1 if c[(i+1)%len(c)]==pair[1] else -1
  assert c[(i+direction)%len(c)]==pair[1]
  ctarget,pair=slot_event(c,ev['start'],ev['length'],i,direction)
  assert ctarget==canonical(d) and pair==tuple(ev['marker_after'])
 assert pair==tuple(entry['final_markers'])
 c=tuple(entry['final_carrier']);neighbours=defaultdict(set)
 for a in edge_set(c):
  u,v=tuple(a);neighbours[u].add(v);neighbours[v].add(u)
 u,v=pair;wait=0
 while u!=0:
  u,v=v,next(iter(neighbours[v]-{u}));wait+=1
  assert wait<len(c)
 assert int(v in (1,2,3))==entry['port0_next_type'] and wait==entry['circulation_steps_to_port']
 # Verify mixed preparations independently: each unordered cycle edge exactly once in each branch.
 assert Counter(frozenset(e) for e in entry['uniformized_directed_pairs'])==Counter(edge_set(c))
# Direct ordered-slot propagation independently checks the live first-port detector.
def direct_step(c,p,gated):
 i=c.index(p[0]);direction=1 if c[(i+1)%len(c)]==p[1] else -1
 out=defaultdict(F);ev=event_table[c] or [(0,0,c)]
 for start,length,d in ev:
  if length and not (gated and not ({c[start],c[(start+length-1)%len(c)]}&set(p))):target,q=slot_event(c,start,length,i,direction)
  else:target,q=c,p
  out[target,q]+=F(1,2*len(ev))
 for forward in (False,True):out[c,pair_shift(c,i,direction,forward)]+=F(1,4)
 return dict(out)
for live in saved['live_first_port_reader']:
 branches=[]
 for history in saved['retained_histories']:
  c=tuple(history['final_carrier']);law={(c,tuple(p)):F(1,9) for p in history['uniformized_directed_pairs']};counts={0:F(0),1:F(0)};rows=[]
  for t in range(13):
   active={}
   for (c,p),mass in law.items():
    if p[0]==0:counts[int(p[1] in (1,2,3))]+=mass
    else:active[c,p]=mass
   rows.append({'step':t,'output0':str(counts[0]),'output1':str(counts[1]),'timeout':str(sum(active.values()))})
   assert sum(counts.values())+sum(active.values())==1
   if t==12:break
   nxt=defaultdict(F)
   for (c,p),mass in active.items():
    for q,weight in direct_step(c,p,live['marker_gate']).items():nxt[q]+=mass*weight
   law=dict(nxt)
  branches.append(rows)
 for row,left,right in zip(live['records'],*branches):
  assert row['plus']==left and row['minus']==right
  tv=sum(abs(F(left[k])-F(right[k])) for k in ('output0','output1','timeout'))/2
  assert str(tv)==row['TV'] and str((1+tv)/2)==row['equal_prior_success']
result={'censuses':checks,'retained_histories_verified':2,'live_detector_models_verified':2,'live_detector_horizons_per_model':13,'matched_unordered_TV':'0','directed_port_output_TV':'1','status':'PASS'}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
