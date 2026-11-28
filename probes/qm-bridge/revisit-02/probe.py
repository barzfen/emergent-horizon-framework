"""Orientation transport of actual circular LR2/LR3 events; no amplitudes supplied."""
import itertools,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter,deque

def oriented(c):
 c=tuple(c);j=c.index(0);return c[j:]+c[:j]
def flip(c):return (c[0],)+c[:0:-1]
def canon(c):
 c=oriented(c);return min(c,flip(c))
def pi(c):return frozenset(c[::2])
def valid(c,ones):
 n=len(c);return all((c[i] in ones) in ((c[(i-1)%n] in ones),(c[(i+1)%n] in ones)) for i in range(n))
def move(c,s,l):
 a=list(c);ix=[(s+j)%len(c) for j in range(l)]
 for i,v in zip(ix,[c[j] for j in ix][::-1]):a[i]=v
 return oriented(a)
def build(n,ones):
 states=[(0,)+p for p in itertools.permutations(range(1,n)) if p[0]<p[-1] and valid((0,)+p,ones)]
 ss=set(states);events={c:[] for c in states}
 for c in states:
  for l in (2,3):
   for s in range(n):
    raw=move(c,s,l);d=canon(raw)
    if d in ss and d!=c and pi(d)==pi(c):events[c].append((d,int(raw!=d),s,l))
 # Check reverse EVENT multiplicity, including orientation transport.
 mult={c:Counter((d,b) for d,b,_,_ in ev) for c,ev in events.items()}
 for c in states:
  for (d,b),m in mult[c].items():assert mult[d][c,b]==m
 return states,events

def analyze(n,ones):
 states,events=build(n,ones);seen=set();comps=[];negative=[];ambiguous=[]
 for root in states:
  if root in seen:continue
  labels={root:0};parent={root:None};todo=deque([root]);bad=[];edges=set()
  while todo:
   c=todo.popleft();seen.add(c)
   for d,b,s,l in events[c]:
    edges.add(tuple(sorted((c,d))))
    if d not in labels:labels[d]=labels[c]^b;parent[d]=c;todo.append(d)
    elif labels[d]!=(labels[c]^b):bad.append((c,d,b,s,l))
  comp=sorted(labels); row={'states':len(comp),'edges':len(edges),'flat':not bad}
  for c in comp:
   by=defaultdict(set)
   for d,b,_,_ in events[c]:by[d].add(b)
   for d,bs in by.items():
    if len(bs)>1:ambiguous.append([c,d])
  # Explicit BFS of doubled cover checks connectedness criterion.
  cover={(root,0)};stack=[(root,0)]
  while stack:
   c,b=stack.pop()
   for d,f,_,_ in events[c]:
    q=(d,b^f)
    if q not in cover:cover.add(q);stack.append(q)
  assert len(cover)==len(comp)*(2 if bad else 1)
  row['reachable_orientation_states']=len(cover);comps.append(row)
  if bad and not negative:
   c,d,b,s,l=bad[0]
   def path(v):
    p=[]
    while v is not None:p.append(v);v=parent[v]
    return p[::-1]
   pc,pd=path(c),path(d)
   # Closed walk root->c->d->root, possibly repeated tree edges.
   walk=pc+[d]+pd[-2::-1];bits=[]
   for a,z in zip(walk,walk[1:]):
    bs={f for q,f,_,_ in events[a] if q==z}
    f=b if a==c and z==d else next(iter(bs));bits.append(f)
   assert walk[0]==walk[-1] and sum(bits)%2==1
   negative=[{'walk':walk,'edge_flip_bits':bits,'length':len(bits),'transport_product':-1}]
 return {'n':n,'ones':sorted(ones),'states':len(states),'events':sum(map(len,events.values())),'components':len(comps),'flat_components':sum(x['flat'] for x in comps),'nonflat_components':sum(not x['flat'] for x in comps),'mixed_orientation_edges':len(ambiguous),'component_details':comps,'first_negative_closed_walk':negative},states,events

def lifted_check(states,events,seed,steps):
 # Exact probability evolution of orientation as a classical memory bit.
 P={(seed,0):F(1)};signed={seed:F(1)};ordinary={seed:F(1)};history=[]
 for t in range(steps+1):
  plus=defaultdict(F);minus=defaultdict(F)
  for (c,b),p in P.items():(minus if b else plus)[c]+=p
  assert sum(P.values())==1 and all(p>=0 for p in P.values())
  for c in states:
   assert plus[c]-minus[c]==signed.get(c,0)
   assert plus[c]+minus[c]==ordinary.get(c,0)
  canceled=[{'state':c,'positive':str(plus[c]),'negative':str(minus[c]),'signed':str(plus[c]-minus[c]),'occupancy':str(plus[c]+minus[c])} for c in states if plus[c]>0 and minus[c]>0]
  history.append({'steps':t,'overlap_states':len(canceled),'example':canceled[:1], 'exact_zero_examples':[x for x in canceled if x['signed']=='0'][:1], 'signed_L1':str(sum(abs(v) for v in signed.values())), 'signed_square_sum':str(sum(v*v for v in signed.values()))})
  newP=defaultdict(F);newS=defaultdict(F);newO=defaultdict(F)
  for (c,b),p in P.items():
   ev=events[c] or [(c,0,0,0)]
   for d,f,_,_ in ev:newP[d,b^f]+=p/len(ev)
  for c,p in signed.items():
   ev=events[c] or [(c,0,0,0)]
   for d,f,_,_ in ev:newS[d]+=p*((-1)**f)/len(ev)
  for c,p in ordinary.items():
   ev=events[c] or [(c,0,0,0)]
   for d,f,_,_ in ev:newO[d]+=p/len(ev)
  P,signed,ordinary=newP,newS,newO
 return history

if __name__=='__main__':
 outputs=[]; models=[]
 for n in (7,9):
  r,ss,ev=analyze(n,{1,2,3});outputs.append(r);models.append((ss,ev))
 # A retained control and a nonflat example, if found.
 checks=[]
 for r,(ss,ev) in zip(outputs,models):
  seed=tuple(r['first_negative_closed_walk'][0]['walk'][0]) if r['first_negative_closed_walk'] else ss[0]
  checks.append({'n':r['n'],'seed':seed,'history':lifted_check(ss,ev,seed,12)})
 # Rebuild prior retained six-state carrier without executing prior probe.
 ss,ev=models[0];A=(0,1,2,3,4,5,6);seen={A};stack=[A]
 while stack:
  for d,*_ in ev[stack.pop()]:
   if d not in seen:seen.add(d);stack.append(d)
 assert len(seen)==6
 retained=lifted_check(sorted(seen),ev,A,12)
 out={'models':outputs,'exact_lift_checks':checks,'retained_six_state_history':retained,'sampling':'uniform accepted indexed LR2/LR3 event; frozen self-loop','checks':'PASS','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='models'},indent=2))
 for r in outputs:print(json.dumps({k:v for k,v in r.items() if k!='component_details'},indent=2))
