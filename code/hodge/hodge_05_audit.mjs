function h5AuditRange(maxN=18){
  const gcd=(a,b)=>{while(b){[a,b]=[b,a%b];}return Math.abs(a);};
  const assert=(x,msg)=>{if(!x)throw new Error(msg);};
  const rotate=(a,k)=>a.slice(k).concat(a.slice(0,k));
  const mod=(a,n)=>(a%n+n)%n;
  const popcount=x=>{let c=0;while(x){x&=x-1;c++;}return c;};
  const binomial=(n,k)=>{let x=1n;for(let j=1;j<=k;j++)x=x*BigInt(n-k+j)/BigInt(j);return x;};
  const rows=[];
  for(let n=5;n<=maxN;n++){
    const bit=(w,i)=>(w>>>mod(i,n))&1;
    const valid=w=>{for(let i=0;i<n;i++)if(bit(w,i)===bit(w,i+2)&&bit(w,i)!==bit(w,i+1))return false;return true;};
    const asWord=w=>Array.from({length:n},(_,i)=>bit(w,i)).join("");
    const states=[];const meta=new Map();
    for(let w=0;w<2**n;w++)if(valid(w)){
      const starts=Array.from({length:n},(_,i)=>i).filter(i=>bit(w,i)!==bit(w,i-1));
      const markers=[];
      starts.forEach((s,a)=>{let len=mod(starts[(a+1)%starts.length]-s,n);for(let t=2;t<len;t++)markers.push({p:mod(s+t,n),c:bit(w,s)});});
      markers.sort((a,b)=>a.p-b.p);
      const E=markers.length;const colors=markers.map(x=>x.c);
      let chi="",cuts=[],l=0,T=0,H=null,d=0,rho=null;
      if(E){
        const rots=colors.map((_,i)=>rotate(colors,i).join(""));
        chi=rots.reduce((a,b)=>a<b?a:b);
        cuts=rots.map((s,i)=>s===chi?i:-1).filter(i=>i>=0);
        l=Array.from({length:E},(_,i)=>i+1).find(k=>E%k===0&&chi===chi.slice(0,k).repeat(E/k));
        T=Array.from({length:E},(_,i)=>chi[i]!==chi[(i+1)%E]?1:0).reduce((a,b)=>a+b,0);
        H=(starts.length-T)/2;
        assert(Number.isInteger(H)&&H>=0,"invalid slack");
        d=gcd(4,l);rho=markers[cuts[0]].p%d;
        assert(cuts.every(a=>markers[a].p%d===rho),"ambiguous phase");
        // Check the complete gap reconstruction rule independently of connectivity.
        markers.forEach((x,a)=>{
          const y=markers[(a+1)%E];
          const gap=mod(y.p-x.p,n)||n;
          const base=1+2*(x.c!==y.c);
          assert(gap>=base&&(gap-base)%4===0,"gap residue");
          const h=(gap-base)/4;
          const prediction=[];
          for(let q=0;q<h;q++)prediction.push(1-x.c,1-x.c,x.c,x.c);
          if(x.c!==y.c)prediction.push(1-x.c,1-x.c);
          assert(prediction.length===gap-1,"gap length");
          prediction.forEach((b,k)=>assert(b===bit(w,x.p+k+1),"gap reconstruction"));
        });
      }
      const key=E&&H>0?JSON.stringify([starts.length,chi,rho]):null;
      states.push(w);meta.set(w,{D:starts.length,E,m:popcount(w),chi,l,T,H,d,rho,key,markers});
    }
    const adjacency=new Map(states.map(w=>[w,[]]));let edges=0;
    for(const w of states)for(let i=0;i<n;i++)if(bit(w,i)!==bit(w,i+2)){
      const v=w^(1<<i)^(1<<mod(i+2,n));
      if(meta.has(v)){adjacency.get(w).push(v);if(w<v)edges++;}
    }
    const seen=new Set(),component=new Map(),mobile=[],frozen=[];
    for(const root of states)if(!seen.has(root)){
      const stack=[root],vertices=[];seen.add(root);
      while(stack.length){const w=stack.pop();vertices.push(w);for(const v of adjacency.get(w))if(!seen.has(v)){seen.add(v);stack.push(v);}}
      const id=mobile.length+frozen.length;
      vertices.forEach(w=>component.set(w,id));
      if(vertices.length===1){assert(meta.get(root).key===null,"moving signature on frozen state");frozen.push(root);continue;}
      const a=meta.get(root);
      assert(a.key!==null,"missing mobile signature");
      assert(vertices.every(w=>meta.get(w).key===a.key),"key varies on component");
      const expectedNumerator=BigInt(n*a.l)*binomial(a.H+a.E-1,a.E-1);
      const expectedDenominator=BigInt(a.E*a.d);
      assert(expectedNumerator%expectedDenominator===0n,"noninteger component size");
      const expected=Number(expectedNumerator/expectedDenominator);
      assert(vertices.length===expected,"component size formula");
      // Reconstruct integral boundary winding image from a spanning tree.
      const potential=new Map([[root,0]]),queue=[root];let windingGcd=0;
      for(let q=0;q<queue.length;q++){
        const w=queue[q];
        for(const v of adjacency.get(w)){
          let label=-1;
          for(let i=0;i<n;i++)if((w^(1<<i)^(1<<mod(i+2,n)))===v){label=i;break;}
          assert(label>=0,"no edge label");
          const kappa=bit(w,label)===bit(w,label+1)?1:-1;
          if(!potential.has(v)){potential.set(v,potential.get(w)+kappa);queue.push(v);}
          else{
            const period=kappa-(potential.get(v)-potential.get(w));
            assert(period%n===0,"nonintegral winding");
            windingGcd=gcd(windingGcd,period/n);
          }
        }
      }
      assert(windingGcd===a.l/a.d,"winding image formula");
      mobile.push({D:a.D,m:a.m,chi:a.chi,primitive_period:a.l,slack:a.H,phase_modulus:a.d,phase:a.rho,vertices:vertices.length,predicted_vertices:expected,boundary_winding_gcd:windingGcd,predicted_winding_gcd:a.l/a.d,representative:asWord(root)});
    }
    let positiveDiamonds=0;
    for(const w of states){
      const a=meta.get(w);if(!a.key)continue;
      const marks=a.markers;const predicted=new Set(),positive=[];
      for(let t=0;t<marks.length;t++){
        const x=marks[t],next=marks[(t+1)%marks.length],prev=marks[mod(t-1,marks.length)];
        const gap=mod(next.p-x.p,n)||n,pgap=mod(x.p-prev.p,n)||n;
        const h=(gap-1-2*(x.c!==next.c))/4;
        const hp=(pgap-1-2*(prev.c!==x.c))/4;
        if(h>0){const v=w^(1<<x.p)^(1<<mod(x.p+2,n));predicted.add(v);positive.push({v,i:x.p});}
        if(hp>0){const i=mod(x.p-4,n);predicted.add(w^(1<<i)^(1<<mod(i+2,n)));}
      }
      assert(predicted.size===adjacency.get(w).length&&adjacency.get(w).every(v=>predicted.has(v)),"gap move correspondence");
      for(let i=0;i<positive.length;i++)for(let j=i+1;j<positive.length;j++){
        const a=positive[i],b=positive[j];
        const aw=[a.i,mod(a.i+1,n),mod(a.i+2,n)];
        const bw=[b.i,mod(b.i+1,n),mod(b.i+2,n)];
        assert(!aw.some(x=>bw.includes(x)),"overlap in positive diamond");
        const end=a.v^w^b.v;
        assert(meta.has(end)&&new Set([w,a.v,b.v,end]).size===4,"invalid positive diamond");
        positiveDiamonds++;
      }
    }
    const keyGroups=new Map();
    for(const w of states){const key=meta.get(w).key;if(key!==null){if(!keyGroups.has(key))keyGroups.set(key,new Set());keyGroups.get(key).add(component.get(w));}}
    assert([...keyGroups.values()].every(ids=>ids.size===1),"classifier collision");
    const necklaces=new Map();
    mobile.forEach(a=>{const k=JSON.stringify([a.D,a.chi]);if(!necklaces.has(k))necklaces.set(k,[]);necklaces.get(k).push(a);});
    necklaces.forEach(v=>assert(v.length===v[0].phase_modulus&&new Set(v.map(x=>x.phase)).size===v.length,"phase class count"));
    let counterexample=null;
    for(const entries of necklaces.values())if(entries.length>1){
      counterexample={D:entries[0].D,chi:entries[0].chi,primitive_period:entries[0].primitive_period,phase_modulus:entries[0].phase_modulus,components:entries.map(a=>({phase:a.phase,representative:a.representative,vertices:a.vertices}))};break;
    }
    rows.push({n,states:states.length,undirected_edges:edges,frozen_states:frozen.length,mobile_components:mobile.length,mobile_necklaces:necklaces.size,phase_moduli:[...new Set(mobile.map(a=>a.phase_modulus))].sort(),colour_word_only_counterexample:counterexample,positive_diamonds_checked:positiveDiamonds,components:mobile,checks:{gap_reconstruction:"PASS",gap_move_correspondence:"PASS",positive_diamonds:"PASS",canonical_phase:"PASS",classifier_exactness:"PASS",component_size_formula:"PASS",winding_image_formula:"PASS"}});
  }
  return {probe:"EHF-HODGE-05",date:"2026-10-21",runtime:"JavaScript (ECMAScript BigInt for exact component-size formula)",range:[5,maxN],integer_arithmetic_only:true,audit:rows,total_states:rows.reduce((a,r)=>a+r.states,0),total_edges:rows.reduce((a,r)=>a+r.undirected_edges,0),total_mobile_components:rows.reduce((a,r)=>a+r.mobile_components,0)};
}

function h5OrderedLiftControls(){
 const valid=(u,H)=>u.every((x,i)=>i===0||u[i-1]<=x)&&u[u.length-1]<=u[0]+H;
 const regions=[];let pairs=0,diamonds=0;
 for(let E=1;E<=6;E++)for(let H=1;H<=4;H++){
  const points=[];
  function gen(a){if(a.length===E){if(valid(a,H))points.push(a);return;}for(let j=0;j<4;j++)gen(a.concat(j));}
  gen([]);
  for(const u of points){
   const eligible=[];
   for(let i=0;i<E;i++){const v=u.slice();v[i]++;if(valid(v,H))eligible.push(i);}
   for(let a=0;a<eligible.length;a++)for(let b=a+1;b<eligible.length;b++){
    const v=u.slice();v[eligible[a]]++;v[eligible[b]]++;
    if(!valid(v,H))throw new Error("Diamond failure");diamonds++;
   }
   for(const v of points)if(u.every((x,i)=>x<=v[i])){
    let current=u.slice();let steps=0;
    while(current.some((x,i)=>x!==v[i])){
     let next=null;
     for(let i=0;i<E;i++)if(current[i]<v[i]){
      const z=current.slice();z[i]++;if(valid(z,H)){next=z;break;}
     }
     if(next===null)throw new Error("Monotone path failure");
     current=next;if(++steps>100)throw new Error("Invalid loop");
    }
    pairs++;
   }
  }
  regions.push({E,H,points:points.length});
 }
 return {regions,comparable_pairs_checked:pairs,positive_diamonds_checked:diamonds,coordinate_window:[0,3],status:"PASS; finite checks of proof lemmas, not the all-size proof"};
}

// Node.js entry point. The pure functions were executed in the JavaScript
// tool runtime. The terminal/Node wrapper was unavailable during this audit.
const maximum = process.argv[2] === undefined ? 18 : Number(process.argv[2]);
if (!Number.isInteger(maximum) || maximum < 5 || maximum > 22) {
  throw new RangeError("Requested max n must be an integer from 5 to 22.");
}
const result = h5AuditRange(maximum);
result.ordered_lift_controls = h5OrderedLiftControls();
console.log(JSON.stringify(result, null, 2));
