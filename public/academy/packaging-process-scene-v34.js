/* C01: requirements engineering as a ten-station aerial design route.
 * Original teaching geometry. No factory footage, vendor CAD or solved fields.
 * Deterministic render(t) permits frame-accurate seeking and offline recording.
 * Requires the local THREE r170 classic bundle. No network or wall-clock state.
 */
(() => {
  'use strict';
  const T = window.THREE;
  const KEYS = ['mission','workload','requirements','bandwidth','thermal','envelope','testability','alternatives','failure-evidence','baseline'];
  const TITLES = [
    ['Mission / conditions / evidence','任務／條件／證據'],['Sustained workload','持續工作負載'],
    ['Measurable requirements','可量測的需求'],['Useful bandwidth','有效頻寬'],['System thermal budget','系統熱預算'],
    ['Envelope and power','空間與供電'],['Test access','測試入口'],['Alternative architectures','候選架構'],
    ['Challenge assumptions','檢查假設與失效'],['Traceable baseline → C02','可追溯基線 → C02']
  ];
  const POSITIONS = [[0,0],[-18,-12],[-5,-17],[10,-16],[23,-7],[23,8],[9,18],[-8,18],[-23,9],[-23,-5]];
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  const mix=(a,b,t)=>a+(b-a)*t;
  const smooth=t=>{t=clamp(t,0,1);return t*t*(3-2*t);};
  const vector=v=>new T.Vector3(...v);
  function create({canvas,onError=()=>{}}={}) {
    if(!T||!canvas)throw new Error('C01 requires a canvas and the bundled Three.js.');
    let renderer;
    try { renderer=new T.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true,powerPreference:'high-performance'}); }
    catch(error){onError(error);throw error;}
    renderer.outputColorSpace=T.SRGBColorSpace;
    renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.3;
    renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;
    const scene=new T.Scene();scene.background=new T.Color('#071322');scene.fog=new T.FogExp2('#071322',.0038);
    const camera=new T.PerspectiveCamera(39,16/9,.1,260);
    const owned=new Set(),animations=[],labels=[],stations=[],routeDots=[];
    let width=1280,height=720,time=0,index=0,disposed=false,pose=null;
    const keep=o=>(owned.add(o),o);
    const mat=(color,metalness=.1,roughness=.5,more={})=>keep(new T.MeshPhysicalMaterial({color,metalness,roughness,...more}));
    const m={
      navy:mat('#28475c',.55,.34),floor:mat('#142437',.35,.44),board:mat('#28756b',.24,.43),
      copper:mat('#d09255',.95,.22),gold:mat('#edc27c',.86,.24),silver:mat('#a1b3c4',.9,.24),
      silicon:mat('#7d70a6',.64,.22,{clearcoat:1,clearcoatRoughness:.12,iridescence:.4}),
      memory:mat('#476d91',.55,.3),mold:mat('#435b72',.08,.6),polymer:mat('#58a5a1',.2,.46),
      cyan:mat('#6de5dc',.4,.3,{emissive:'#24b7aa',emissiveIntensity:.8}),
      amber:mat('#ffd08b',.45,.28,{emissive:'#ad5e20',emissiveIntensity:.45}),
      red:mat('#ff9b78',.3,.33,{emissive:'#c63e17',emissiveIntensity:.65}),
      glass:mat('#8dc6da',.1,.18,{transparent:true,opacity:.12,depthWrite:false}),
      muted:mat('#41515f',.5,.45),white:mat('#dce8ec',.18,.37)
    };
    const unit=keep(new T.BoxGeometry(1,1,1)),ball=keep(new T.SphereGeometry(1,12,8)),cylinder=keep(new T.CylinderGeometry(1,1,1,20));
    const envCanvas=document.createElement('canvas');envCanvas.width=1024;envCanvas.height=512;
    const env2d=envCanvas.getContext('2d'),gradient=env2d.createLinearGradient(0,0,0,512);
    gradient.addColorStop(0,'#bec8dc');gradient.addColorStop(.45,'#405775');gradient.addColorStop(.54,'#0f1c2a');gradient.addColorStop(1,'#324259');
    env2d.fillStyle=gradient;env2d.fillRect(0,0,1024,512);env2d.fillStyle='#ffffff';env2d.fillRect(100,60,210,110);env2d.fillRect(600,110,110,120);env2d.fillStyle='#d8a96f';env2d.fillRect(830,85,90,100);
    const envTexture=keep(new T.CanvasTexture(envCanvas));envTexture.mapping=T.EquirectangularReflectionMapping;envTexture.colorSpace=T.SRGBColorSpace;
    const pmrem=new T.PMREMGenerator(renderer),environment=keep(pmrem.fromEquirectangular(envTexture));scene.environment=environment.texture;scene.environmentIntensity=1.2;pmrem.dispose();
    scene.add(new T.HemisphereLight('#d8e8ff','#647e9d',2.0));
    const keyLight=new T.DirectionalLight('#fff0d9',7.0);keyLight.position.set(-18,45,22);keyLight.castShadow=true;
    Object.assign(keyLight.shadow.camera,{left:-38,right:38,top:34,bottom:-34,near:1,far:100});
    keyLight.shadow.mapSize.set(2048,2048);keyLight.shadow.normalBias=.04;keyLight.shadow.bias=-.0003;scene.add(keyLight);
    const rim=new T.DirectionalLight('#a6baff',5.0);rim.position.set(26,24,-20);scene.add(rim);
    const fill=new T.DirectionalLight('#ffe0b7',3.2);fill.position.set(-25,22,-18);scene.add(fill);
    function box(parent,w,h,d,x,y,z,material=m.navy){const o=new T.Mesh(unit,material);o.scale.set(w,h,d);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o;}
    function cyl(parent,r,h,x,y,z,material=m.copper){const o=new T.Mesh(cylinder,material);o.scale.set(r,h,r);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o;}
    function sphere(parent,r,x,y,z,material=m.cyan){const o=new T.Mesh(ball,material);o.scale.setScalar(r);o.position.set(x,y,z);parent.add(o);return o;}
    function group(parent,x=0,y=0,z=0){const g=new T.Group();g.position.set(x,y,z);parent.add(g);return g;}
    function tube(parent,points,r=.035,material=m.copper){const curve=new T.CatmullRomCurve3(points.map(vector));const mesh=new T.Mesh(keep(new T.TubeGeometry(curve,Math.max(12,points.length*7),r,6,false)),material);parent.add(mesh);return curve;}
    function instanced(parent,geometry,items,material){const o=new T.InstancedMesh(geometry,material,items.length),dummy=new T.Object3D();items.forEach((v,i)=>{dummy.scale.set(v[0],v[1],v[2]);dummy.position.set(v[3],v[4],v[5]);dummy.updateMatrix();o.setMatrixAt(i,dummy.matrix);});o.castShadow=true;o.receiveShadow=true;parent.add(o);return o;}
    function dots(parent,nx,nz,dx,dz,y,r=.08,material=m.silver){const items=[];for(let x=0;x<nx;x++)for(let z=0;z<nz;z++)items.push([r,r,r,(x-(nx-1)/2)*dx,y,(z-(nz-1)/2)*dz]);return instanced(parent,ball,items,material);}
    function tag(parent,key,en,zh,position,chapter){labels.push({parent,key,en,zh,position:vector(position),chapter});}
    function tileText(parent,text,w,d,x,y,z,color='#d6ede9'){
      const c=document.createElement('canvas');c.width=512;c.height=128;const ctx=c.getContext('2d');ctx.fillStyle='#102131';ctx.fillRect(0,0,c.width,c.height);ctx.font='600 48px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=color;ctx.fillText(text,256,64,490);
      const texture=keep(new T.CanvasTexture(c));texture.colorSpace=T.SRGBColorSpace;
      const material=keep(new T.MeshBasicMaterial({map:texture,transparent:false}));
      const mesh=new T.Mesh(keep(new T.PlaneGeometry(w,d)),material);mesh.rotation.x=-Math.PI/2;mesh.position.set(x,y,z);parent.add(mesh);return mesh;
    }
    function die(parent,x,y,z,w=2.6,d=2.2){const g=group(parent,x,y,z);box(g,w,.32,d,0,0,0,m.silicon);const items=[];for(let i=0;i<5;i++)for(let j=0;j<4;j++)items.push([w/6,.012,d/5,(i-2)*w/5.3,.168,(j-1.5)*d/4.4]);instanced(g,unit,items,m.memory);for(const zz of [-d*.44,d*.44])box(g,w*.9,.018,.035,0,.18,zz,m.copper);return g;}
    function packageModel(parent,{w=8,d=6,at=[0,0,0]}={}){
      const g=group(parent,...at);box(g,w,.42,d,0,.4,0,m.board);dots(g,11,8,(w-.8)/10,(d-.8)/7,.02,.1);
      die(g,-1.4,.91,0,3.1,3.4);die(g,1.5,.91,-1.1,1.65,1.8);die(g,1.5,.91,1.1,1.65,1.8);
      for(let z=-1.35;z<1.4;z+=.22)tube(g,[[-.05,.7,z],[.28,.75,z],[.55,.7,z]],.018,m.copper);
      return g;
    }
    function traces(parent,x1,x2,zs,y=.72,material=m.copper){return zs.map(z=>tube(parent,[[x1,y,z],[mix(x1,x2,.5),y+.08,z],[x2,y,z]],.025,material));}
    function packet(curve,parent,phase=0,speed=.2,material=m.cyan,r=.08){const dot=sphere(parent,r,0,0,0,material);animations.push(t=>dot.position.copy(curve.getPointAt((t*speed+phase)%1)));return dot;}
    function arrow(parent,start,end,material=m.cyan,r=.05){tube(parent,[start,end],r,material);const a=vector(start),b=vector(end),direction=b.clone().sub(a).normalize();const head=new T.Mesh(keep(new T.ConeGeometry(r*3.4,r*7,12)),material);head.position.copy(b);head.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),direction);parent.add(head);}
    function heatTower(parent,x,z,{hot=false,scale=1}={}){
      const g=group(parent,x,0,z);g.scale.setScalar(scale);box(g,4,.4,3.2,0,.5,0,m.board);die(g,0,1,0,2.6,2.3);
      box(g,2.65,.12,2.35,0,1.6,0,m.polymer);box(g,4,.25,3.4,0,2.05,0,m.copper);
      const fins=[];for(let i=0;i<12;i++)fins.push([.16,1.3,3.3,(i-5.5)*.32,2.82,0]);instanced(g,unit,fins,m.silver);
      for(let i=0;i<4;i++){const a=arrow(g,[-1.05+i*.7,1.16,.4],[-1.05+i*.7,4.45,.4],hot?m.red:m.amber,.035);void a;}
      const spot=sphere(g,.4,.45,1.2,-.25,hot?m.red:m.amber);animations.push(t=>spot.scale.setScalar(.34+.035*Math.sin(t*1.3)));
      return g;
    }
    // Dark instrument deck: procedural studio, not a miniature factory.
    box(scene,110,.8,90,0,-1.0,0,m.floor);
    for(let x=-42;x<=42;x+=6)box(scene,.018,.014,70,x,-.58,0,m.muted);
    for(let z=-30;z<=30;z+=6)box(scene,90,.014,.018,0,-.58,z,m.muted);
    POSITIONS.forEach(([x,z],i)=>{
      const g=group(scene,x,0,z);g.name=KEYS[i];const w=i===7?16:i===0?14:11,d=i===0?11:8;
      box(g,w,.46,d,0,-.15,0,m.navy);box(g,w+.06,.018,d+.06,0,.09,0,m.copper);
      box(g,w-.12,.04,d-.12,0,.12,0,m.navy);
      tileText(g,`C01 / ${String(i+1).padStart(2,'0')}`,3.5,.88,-w/2+2.15,.16,d/2-.65);
      const line=box(g,w-.7,.035,.06,0,.16,-d/2+.28,m.cyan);
      stations.push({group:g,highlight:line,bounds:null});
      tag(g,`station-${i}`,TITLES[i][0],TITLES[i][1],[0,1.0,-d/2],-1);
    });
    // The aerial trace is a teaching sequence, never a mixed manufacturing line.
    for(let i=0;i<POSITIONS.length-1;i++){
      const a=POSITIONS[i],b=POSITIONS[i+1],curve=tube(scene,[[a[0],.2,a[1]],[mix(a[0],b[0],.5),.35,mix(a[1],b[1],.5)],[b[0],.2,b[1]]],.035,m.muted);
      const dot=sphere(scene,.12,0,0,0,m.cyan);routeDots.push({curve,dot,i});
    }
    // 01 — mission: generic system blocks, no selected interposer architecture.
    {
      const g=stations[0].group;packageModel(g);
      const nodes=[[-5,0,'LOAD'],[5,0,'DATA'],[0,-4,'HEAT'],[0,4,'TEST']];
      nodes.forEach(([x,z,text],i)=>{box(g,1.8,.3,1.4,x,.5,z,m.mold);tileText(g,text,1.6,.5,x,.67,z);const c=tube(g,[[x,.7,z],[x*.5,1.8,z*.5],[0,1.0,0]],.04,i===2?m.amber:m.copper);packet(c,g,i*.2,.12,i===2?m.amber:m.cyan);});
      tag(g,'mission-package','Architecture not selected','尚未選定製造架構',[0,2.1,0],0);
    }
    // 02 — workload: read/write and burst/sustained are visually distinguishable.
    {
      const g=stations[1].group;
      const bursts=[.3,.6,.4,2.9,.55,.4,2.5,.3,.8,.4,2.8,.4],sustained=Array(12).fill(1.15);
      [bursts,sustained].forEach((values,row)=>values.forEach((h,j)=>box(g,.46,h,.8,-3.7+j*.64,.35+h/2,(row-.5)*2.2,row?m.cyan:m.amber)));
      for(const z of [-1.1,1.1])arrow(g,[-4.2,.25,z+1],[4.3,.25,z+1],m.copper,.026);
      const marker=box(g,.04,3.8,4.7,-4,2,0,m.glass);animations.push(t=>{marker.position.x=-4+(t%12)/12*8;});
      tag(g,'burst','Burst demand','突發需求',[-2,3,-1.1],1);tag(g,'sustained','Sustained load','持續負載',[1,1.9,1.1],1);
    }
    // 03 — requirements are a set of open, versioned evidence obligations.
    {
      const g=stations[2].group,ids=['BW-01','TH-01','ME-01','DFT-01'];
      ids.forEach((id,i)=>{const x=(i%2-.5)*4.1,z=(Math.floor(i/2)-.5)*2.7;box(g,3.5,.28,2,x,.5,z,m.mold);tileText(g,id,2.7,.67,x,.66,z-.25);for(let j=0;j<4;j++)box(g,.52,.045,.2,x-1+j*.68,.67,z+.53,m.amber);});
      tag(g,'req-state','PROPOSED / OPEN','提案／待定',[0,1.5,0],2);
    }
    // 04 — exactly 64 lanes (eight banks of eight) for the declared arithmetic.
    {
      const g=stations[3].group;die(g,-3.7,.85,0,1.1,5.8);die(g,3.7,.85,0,1.1,5.8);
      for(let lane=0;lane<64;lane++){const z=(lane-31.5)*.078;const curve=tube(g,[[-3.1,.82,z],[-1.2,.84,z],[1.2,.84,z],[3.1,.82,z]],.012,m.copper);packet(curve,g,lane*.037,.2,lane%5===4?m.muted:m.cyan,.034);}
      tileText(g,'64 x 16 x 0.80 / 8',5.5,.7,0,.2,-3.1);tag(g,'bw-value','102.4 GB/s · assumed useful rate','102.4 GB/s・假設有效資料率',[0,1.5,0],3);
    }
    // 05 — exploded thermal path and illustrative hot spot, not solver output.
    {
      const g=stations[4].group;heatTower(g,-1,0);for(let i=0;i<3;i++){
        const curve=tube(g,[[2.2+i*.65,1.2,1.5],[2.4+i*.65,2.8,.4],[2.6+i*.65,4.2,-1.8]],.025,m.cyan);packet(curve,g,i*.23,.12,m.cyan,.065);
      }
      tag(g,'thermal-screen','80 °C · lumped estimate','80°C・簡化穩態估算',[-1,4.7,0],4);tag(g,'thermal-spot','Local hot spot still unverified','局部熱點尚未驗證',[.2,1.2,1.2],4);
    }
    // 06 — body envelope is separate from cooling and board/power reservations.
    {
      const g=stations[5].group;box(g,9,.22,6,0,.33,0,m.board);packageModel(g,{w:4.5,d:3.6});
      box(g,4.8,2.3,3.9,0,1.32,0,m.glass);box(g,5.6,.16,4.6,0,3.2,0,m.silver);
      for(let j=0;j<7;j++)box(g,.16,.65,4.5,(j-3)*.73,3.57,0,m.silver);
      for(let j=0;j<4;j++){box(g,.5,.6,.7,-3.3,.72,(j-1.5)*1.1,m.mold);tube(g,[[-3.1,.5,(j-1.5)*1.1],[-2.4,.56,(j-1.5)*1.1],[-1.7,.6,(j-1.5)*.6]],.055,j%2?m.cyan:m.copper);}
      arrow(g,[-3,.3,2.6],[3,.3,2.6],m.amber,.025);arrow(g,[3,.3,2.6],[3,2.6,2.6],m.amber,.025);
      tag(g,'envelope-body','60 × 60 × 4 mm · example body only','60×60×4mm・僅教學本體預留',[0,1.3,2.4],5);tag(g,'envelope-cooler','Cooler budgeted separately','冷卻器另計',[0,4.4,0],5);
    }
    // 07 — access and evidence across assembly stages; probes are symbolic.
    {
      const g=stations[6].group;box(g,8,.35,5,0,.5,0,m.board);const left=die(g,-2,1,0,2.5,3),right=die(g,2,1,0,2.5,3);
      for(let i=0;i<6;i++){const x=-3.1+i*.45;const probe=cyl(g,.055,2.1,x,2.35,1.3,m.silver);animations.push(t=>probe.position.y=2.35+.12*Math.sin(t*.8+i*.2));}
      const paths=traces(g,-.7,.7,[-.8,-.3,.3,.8],1,m.copper);paths.forEach((c,i)=>packet(c,g,i*.2,.18));
      const lid=box(g,3,.22,3.5,2,2.7,0,m.mold);animations.push(t=>{lid.position.y=2.65+.3*Math.sin(t*.3);});
      sphere(right,.13,0,.3,0,m.amber);void left;
      tag(g,'test-die','Die-stage evidence','裸晶階段證據',[-2,3,0],6);tag(g,'test-package','Post-assembly test access','組裝後測試入口',[2,3.4,0],6);
    }
    // 08 — genuinely different route miniatures, never one chained product.
    {
      const g=stations[7].group;
      [-5.5,-1.8,1.8,5.5].forEach((x,i)=>{
        const p=group(g,x,.2,0);box(p,3.2,.32,3.6,0,.3,0,m.board);
        if(i===0){box(p,2.9,.22,2.9,0,.63,0,m.silicon);for(let z=-.9;z<1;z+=.3)cyl(p,.035,.6,0,.55,z,m.copper);die(p,-.7,.94,0,1.1,2);die(p,.7,.94,0,1.1,2);}
        if(i===1){box(p,2.95,.48,2.95,0,.68,0,m.mold);box(p,3,.08,3,0,.4,0,m.polymer);die(p,-.7,.82,0,1.1,2);die(p,.7,.82,0,1.1,2);for(let j=0;j<7;j++)tube(p,[[-1.3,.95,(j-3)*.27],[0,1.01,(j-3)*.27],[1.3,.95,(j-3)*.27]],.017,m.copper);}
        if(i===2){box(p,.65,.16,2.15,0,.5,0,m.silicon);die(p,-.76,.85,0,1.3,2.4);die(p,.76,.85,0,1.3,2.4);for(let j=0;j<8;j++)box(p,.61,.025,.035,0,.6,(j-3.5)*.22,m.copper);}
        if(i===3){die(p,0,.73,0,2.1,2.3);die(p,0,1.43,0,2.1,2.3);const pads=[];for(let x=0;x<8;x++)for(let z=0;z<8;z++)pads.push([.045,.03,.045,(x-3.5)*.23,1.1,(z-3.5)*.25]);instanced(p,cylinder,pads,m.copper);}
        tileText(p,['INTERPOSER','FAN-OUT','BRIDGE','HYBRID'][i],2.8,.6,0,.49,2.4);
      });
      tag(g,'alternatives-choice','Candidates · not mandatory sequential steps','候選路線・不是必經串接工序',[0,3,0],7);
    }
    // 09 — changed assumption plus evidence ledger. Neither case is a pass.
    {
      const g=stations[8].group;heatTower(g,-2.5,0,{scale:.85});heatTower(g,2.5,0,{hot:true,scale:.85});
      tileText(g,'80 C / EST.',3,.65,-2.5,.2,2.4);tileText(g,'90 C / EST.',3,.65,2.5,.2,2.4,'#ffb38e');
      const comparison=box(g,.25,1.3,.28,0,.9,-2,m.amber);animations.push(t=>{comparison.scale.y=1.2+.25*Math.sin(t*.7);});
      tag(g,'failure-screen','Changed cooling assumption → risk','冷卻假設改變 → 風險',[0,4.1,0],8);
    }
    // 10 — evidence baseline has open issues, no fake product certification.
    {
      const g=stations[9].group;const positions=[[-3,0],[-1,1.5],[1,1.5],[3,0]];
      positions.forEach(([x,z],i)=>{box(g,1.5,.28,1.6,x,.6,z,m.mold);tileText(g,['BW','TH','ME','DFT'][i],1.2,.5,x,.76,z);const c=tube(g,[[x,.85,z],[x*.5,1.5,z*.5],[0,1,-1.4]],.04,m.copper);packet(c,g,i*.2,.14,m.amber);});
      box(g,3,.6,1.7,0,.7,-1.5,m.navy);tileText(g,'REV A',2.1,.7,0,1.02,-1.5);
      arrow(g,[0,.55,-2.7],[0,.55,-4.7],m.cyan,.07);tileText(g,'C02',2,.7,0,.58,-5.5);
      tag(g,'baseline-revision','Baseline + open issues','需求基線＋未決事項',[0,1.8,-1.5],9);
    }
    scene.updateMatrixWorld(true);
    for(const station of stations){station.bounds=new T.Box3().setFromObject(station.group);}
    const aim=new T.Vector3();
    const worldRegion={min:[-32,-.3,-23],max:[31,5,25]};
    const regionFor=i=>({min:stations[i].bounds.min.toArray(),max:stations[i].bounds.max.toArray()});
    const SHOTS=[
      {az:.7,el:1.02,distance:23,y:1.1},
      {az:1.18,el:.61,distance:18,y:1.5},
      {az:.2,el:1.26,distance:17,y:.5},
      {az:-.6,el:.78,distance:18,y:1},
      {az:.6,el:.68,distance:17,y:2},
      {az:-.75,el:.58,distance:18,y:1.7},
      {az:1.0,el:.61,distance:18,y:1.5},
      {az:.24,el:.92,distance:25,y:1},
      {az:-.3,el:.75,distance:20,y:1.8},
      {az:.65,el:.98,distance:18,y:.9}
    ];
    function chapterPose(chapter,local){
      const shot=SHOTS[chapter],pos=POSITIONS[chapter],u=clamp(local/30,0,1);
      const az=shot.az+(u-.5)*.33,el=shot.el+.04*Math.sin(u*Math.PI),distance=shot.distance*(1-.06*Math.sin(u*Math.PI));
      return {aim:[pos[0],shot.y,pos[1]],offset:[Math.sin(az)*Math.cos(el)*distance,Math.sin(el)*distance,Math.cos(az)*Math.cos(el)*distance],focus:chapter,region:regionFor(chapter)};
    }
    function globalPose(local=0){const az=.25+local*.003,d=78;return {aim:[0,0,1],offset:[Math.sin(az)*d*.35,d*.86,Math.cos(az)*d*.35],focus:-1,region:worldRegion};}
    function blendPose(a,b,t){return {aim:a.aim.map((v,i)=>mix(v,b.aim[i],t)),offset:a.offset.map((v,i)=>mix(v,b.offset[i],t)),focus:t<.5?a.focus:b.focus,region:{min:a.region.min.map((v,i)=>mix(v,b.region.min[i],t)),max:a.region.max.map((v,i)=>mix(v,b.region.max[i],t))}};}
    function frame(next){
      const aspect=width/height,portrait=aspect<1;
      aim.fromArray(next.aim);camera.position.copy(aim).add(vector(next.offset));camera.lookAt(aim);camera.updateMatrixWorld();
      const bounds=new T.Box3(vector(next.region.min),vector(next.region.max));
      // Fit actual world bounds into a caption-safe rectangle on both orientations.
      const desiredX=portrait?.88:.76,desiredY=portrait?.47:.56;
      const project=()=>{let minX=1e3,maxX=-1e3,minY=1e3,maxY=-1e3;for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){const p=new T.Vector3(x,y,z).project(camera);minX=Math.min(minX,p.x);maxX=Math.max(maxX,p.x);minY=Math.min(minY,p.y);maxY=Math.max(maxY,p.y);}return {minX,maxX,minY,maxY};};
      camera.clearViewOffset();let projected=project();
      const factor=Math.max((projected.maxX-projected.minX)/(desiredX*2),(projected.maxY-projected.minY)/(desiredY*2),1);
      if(factor>1){const offset=camera.position.clone().sub(aim).multiplyScalar(factor*1.03);camera.position.copy(aim).add(offset);camera.updateMatrixWorld();projected=project();}
      // Target the model center at 43% height, leaving space for captions below.
      const centerY=(projected.minY+projected.maxY)/2,desiredCenter=.14;
      camera.setViewOffset(width,height,0,(desiredCenter-centerY)*height/2,width,height);camera.updateMatrixWorld();
      return project();
    }
    function render(seconds=0,options={}){
      if(disposed)return;
      time=clamp(Number(seconds)||0,0,300);index=clamp(Number.isInteger(options.chapterIndex)?options.chapterIndex:Math.floor(Math.min(time,299.999)/30),0,9);
      const local=clamp(time-index*30,0,30);let next=chapterPose(index,local);
      if(index===0&&local<9)next=blendPose(globalPose(local),chapterPose(0,9),smooth((local-2)/7));
      else if(local<2&&index>0)next=blendPose(chapterPose(index-1,30),next,smooth(local/2));
      if(index===9&&local>21)next=blendPose(next,globalPose(time),smooth((local-21)/8));
      for(const animate of animations)animate(time);
      stations.forEach((station,i)=>{station.highlight.material=i===index?m.cyan:m.muted;});
      routeDots.forEach(({curve,dot,i})=>{dot.position.copy(curve.getPointAt((time*.07+i*.1)%1));dot.visible=next.focus<0||i===Math.max(0,index-1);});
      scene.updateMatrixWorld(true);const bounds=frame(next);renderer.render(scene,camera);pose={...next,bounds};
      return getState();
    }
    function resize(w,h,pixelRatio=Math.min(window.devicePixelRatio||1,2)){
      width=Math.max(1,Number(w)||1280);height=Math.max(1,Number(h)||720);renderer.setPixelRatio(clamp(pixelRatio,1,2));renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix();return render(time);
    }
    function getLabels(){
      return labels.map(l=>{const p=l.parent.localToWorld(l.position.clone()).project(camera),isOverview=pose?.focus===-1;
        return {key:l.key,en:l.en,zh:l.zh,x:(p.x*.5+.5)*width,y:(.5-p.y*.5)*height,visible:(l.chapter===index||l.chapter===-1&&isOverview)&&p.z>-1&&p.z<1&&p.x>-.94&&p.x<.94&&p.y>-.72&&p.y<.75};});
    }
    function getState(){return {processId:'C01',time,chapterIndex:index,view:KEYS[index],width,height,teachingReconstruction:true,fieldVisualization:'illustrative_not_solved',architectureSelected:false,webgl:true,calls:renderer.info.render.calls,triangles:renderer.info.render.triangles,camera:{x:camera.position.x,y:camera.position.y,z:camera.position.z},focus:pose?.focus??0,projectedBounds:pose?.bounds??null};}
    function dispose(){if(disposed)return;disposed=true;scene.traverse(o=>{if(o.isInstancedMesh)o.dispose();});for(const r of owned)r.dispose?.();renderer.dispose();scene.clear();}
    const api={render,resize,getLabels,getState,dispose,setProcess(id){if(id!=='C01')throw new Error(`Process film ${id} has not been implemented.`);return render(0);}};
    resize(canvas.clientWidth||1280,canvas.clientHeight||720);return api;
  }
  window.MG_PACKAGING_PROCESS_SCENE={version:'34.0.0-C01',create,processIds:['C01'],views:[...KEYS],durationSeconds:300};
})();
