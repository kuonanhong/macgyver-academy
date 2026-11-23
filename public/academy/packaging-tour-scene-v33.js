/* MacGyver V33 — deterministic, locally rendered advanced-packaging flyover.
 * Teaching reconstruction, not manufacturer CAD or filmed factory footage.
 * No external textures, requests or animations outside render(timeSeconds).
 */
(() => {
  'use strict';
  const T = window.THREE;
  const VIEWS = ['overview','architecture','interconnect','assembly','cross-section','signal','thermal','inspection','tradeoff','roadmap'];
  const IDS = ['interposer','fanout','hybrid','bridge','chiplet','thermal'];
  const clamp = (x,a,b) => Math.max(a,Math.min(b,x));
  const ease = x => { x=clamp(x,0,1); return x*x*(3-2*x); };
  const mix = (a,b,t) => a+(b-a)*t;
  function create({canvas,onError=()=>{}}={}) {
    if (!T || !canvas) { const e=new Error('Three.js and a canvas are required.'); onError(e); throw e; }
    let renderer;
    try { renderer=new T.WebGLRenderer({canvas,antialias:true,alpha:false,preserveDrawingBuffer:true,powerPreference:'high-performance'}); }
    catch(e) { onError(e); throw e; }
    renderer.outputColorSpace=T.SRGBColorSpace;
    renderer.toneMapping=T.ACESFilmicToneMapping;
    renderer.toneMappingExposure=1.12;
    renderer.shadowMap.enabled=true;
    renderer.shadowMap.type=T.PCFSoftShadowMap;
    const scene=new T.Scene(); scene.background=new T.Color('#050a13'); scene.fog=new T.Fog('#050a13',48,95);
    const camera=new T.PerspectiveCamera(37,16/9,.1,180);
    let width=1280,height=720,disposed=false,current='interposer',lastTime=0,lastView='overview',explosion=0;
    const resources=new Set(),moving=[],labels=[],signals=[],heatObjects=[],highlights=[],sectionMeshes=[];
    const keep=o=>(resources.add(o),o);
    const material=(color,metalness=.1,roughness=.5,extra={})=>keep(new T.MeshPhysicalMaterial({color,metalness,roughness,...extra}));
    const mats={
      copper:material('#c58348',.98,.19), gold:material('#e5ba64',.85,.24), solder:material('#bcc7d2',.92,.2),
      silicon:material('#363657',.79,.20,{clearcoat:1,clearcoatRoughness:.12,iridescence:.5,iridescenceIOR:1.3,iridescenceThicknessRange:[160,310]}), memory:material('#24374c',.72,.25,{clearcoat:.8}),
      substrate:material('#123e3d',.22,.48), dielectric:material('#477878',.15,.47), mold:material('#232d3e',.05,.68),
      ceramic:material('#606b7e',.32,.42), aluminum:material('#8a9baa',.88,.24), black:material('#101c29',.4,.4),
      table:material('#111a25',.82,.28), floor:material('#080f1b',.52,.44), cyan:material('#54eadf',.22,.3,{emissive:'#21b8b0',emissiveIntensity:1.1}),
      warm:material('#e6ae6e',.5,.36), glass:material('#80c5d5',.05,.2,{transparent:true,opacity:.14,depthWrite:false}),
      red:material('#ff8664',.35,.38,{emissive:'#b53715',emissiveIntensity:.5})
    };
    // Procedural studio softboxes provide controlled, physically lit reflections.
    const envCanvas=document.createElement('canvas');envCanvas.width=1024;envCanvas.height=512;
    const ec=envCanvas.getContext('2d'),eg=ec.createLinearGradient(0,0,0,512);
    eg.addColorStop(0,'#c4d4e2');eg.addColorStop(.46,'#586b83');eg.addColorStop(.52,'#192b3d');eg.addColorStop(1,'#354c65');
    ec.fillStyle=eg;ec.fillRect(0,0,1024,512);ec.fillStyle='#ffffff';ec.fillRect(120,90,190,100);ec.fillRect(620,110,90,150);ec.fillStyle='#e4bf89';ec.fillRect(885,160,65,80);
    const envTex=keep(new T.CanvasTexture(envCanvas));envTex.mapping=T.EquirectangularReflectionMapping;envTex.colorSpace=T.SRGBColorSpace;
    const pmrem=new T.PMREMGenerator(renderer); const envTarget=pmrem.fromEquirectangular(envTex); resources.add(envTarget); scene.environment=envTarget.texture; scene.environmentIntensity=.8;pmrem.dispose();
    scene.add(new T.HemisphereLight('#c3d9ff','#090b14',.8));
    const key=new T.DirectionalLight('#fff0d3',5.0);key.position.set(-13,28,15);key.castShadow=true;
    key.shadow.mapSize.set(2048,2048);key.shadow.camera.left=-25;key.shadow.camera.right=25;key.shadow.camera.top=25;key.shadow.camera.bottom=-25;key.shadow.camera.near=1;key.shadow.camera.far=65;key.shadow.bias=-.0003;key.shadow.normalBias=.035;key.shadow.radius=3;scene.add(key);
    const rim=new T.DirectionalLight('#829cff',3.8);rim.position.set(17,15,-18);scene.add(rim);
    const fill=new T.DirectionalLight('#ffc488',1.6);fill.position.set(15,8,15);scene.add(fill);
    const unitBox=keep(new T.BoxGeometry(1,1,1));
    const sphere=keep(new T.SphereGeometry(1,12,8));
    const cylinder=keep(new T.CylinderGeometry(1,1,1,16));
    const plane=keep(new T.PlaneGeometry(1,1));
    const core=new T.Group();core.name='packaging-hero';core.position.y=1.38;scene.add(core);
    const background=new T.Group();scene.add(background);
    let model=new T.Group();core.add(model);
    const lineMaterial=keep(new T.LineBasicMaterial({color:'#72c5d5',transparent:true,opacity:.3}));
    function box(parent,w,h,d,x,y,z,mat=mats.silicon) { const m=new T.Mesh(unitBox,mat);m.scale.set(w,h,d);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m; }
    function cyl(parent,r,h,x,y,z,mat=mats.copper) {const m=new T.Mesh(cylinder,mat);m.scale.set(r,h,r);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
    function tube(parent,points,r,mat=mats.copper) {const curve=new T.CatmullRomCurve3(points.map(p=>new T.Vector3(...p)),false,'centripetal');const g=keep(new T.TubeGeometry(curve,Math.max(8,points.length*7),r,6,false));const m=new T.Mesh(g,mat);m.castShadow=true;parent.add(m);return {mesh:m,curve};}
    function layer(name,y,lift) {const g=new T.Group();g.name=name;g.position.y=y;model.add(g);moving.push({node:g,y,lift});return g;}
    function label(key,en,zh,parent,position) {labels.push({key,en,zh,parent,position:new T.Vector3(...position)});}
    function balls(parent,nx,nz,dx,dz,y,r=.13,mat=mats.solder) {const m=new T.InstancedMesh(sphere,mat,nx*nz);const dummy=new T.Object3D();let n=0;for(let x=0;x<nx;x++)for(let z=0;z<nz;z++){dummy.position.set((x-(nx-1)/2)*dx,y,(z-(nz-1)/2)*dz);dummy.scale.setScalar(r);dummy.updateMatrix();m.setMatrixAt(n++,dummy.matrix);}m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
    function pads(parent,nx,nz,dx,dz,y,r=.055,h=.035,mat=mats.copper) {const m=new T.InstancedMesh(cylinder,mat,nx*nz);const dummy=new T.Object3D();let n=0;for(let x=0;x<nx;x++)for(let z=0;z<nz;z++){dummy.position.set((x-(nx-1)/2)*dx,y,(z-(nz-1)/2)*dz);dummy.scale.set(r,h,r);dummy.updateMatrix();m.setMatrixAt(n++,dummy.matrix);}m.castShadow=true;parent.add(m);return m;}
    function boxes(parent,items,mat) {const m=new T.InstancedMesh(unitBox,mat,items.length);const dummy=new T.Object3D();items.forEach((v,i)=>{dummy.scale.set(v[0],v[1],v[2]);dummy.position.set(v[3],v[4],v[5]);dummy.updateMatrix();m.setMatrixAt(i,dummy.matrix);});m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
    function etchedDie(parent,w,d,x,y,z,name='logic') {
      const g=new T.Group();g.position.set(x,y,z);parent.add(g);box(g,w,.48,d,0,0,0,name==='memory'?mats.memory:mats.silicon);
      // Distinct tiny IP blocks, reticle-like surface and metal perimeter.
      const nx=Math.max(3,Math.floor(w/.6)),nz=Math.max(3,Math.floor(d/.6));
      const blocks=[[],[]];for(let ix=0;ix<nx;ix++)for(let iz=0;iz<nz;iz++){blocks[(ix+iz)%5===0?1:0].push([w/nx*.78,.014,d/nz*.8,(ix-(nx-1)/2)*w/nx,.248,(iz-(nz-1)/2)*d/nz]);}boxes(g,blocks[0],mats.memory);boxes(g,blocks[1],mats.copper);
      for(const [ww,dd,xx,zz] of [[w,.025,0,-d/2+.08],[w,.025,0,d/2-.08],[.025,d,-w/2+.08,0],[.025,d,w/2-.08,0]])box(g,ww,.025,dd,xx,.258,zz,mats.gold);
      return g;
    }
    function trace(parent,points,r=.026,active=true) {const t=tube(parent,points,r,mats.copper);if(active){const dot=new T.Mesh(sphere,mats.cyan);dot.scale.setScalar(r*2.8);parent.add(dot);signals.push({dot,curve:t.curve,phase:signals.length*.137});}return t;}
    function base(w=14,d=10.2) {
      const g=layer('Organic substrate',.48,0);box(g,w,.52,d,0,0,0,mats.substrate);
      for(let i=0;i<3;i++)box(g,w+.02,.023,d+.02,0,-.18+i*.14,0,i===1?mats.copper:mats.dielectric);
      balls(g,13,9,(w-1.2)/12,(d-1.2)/8,-.43,.16);
      for(let i=0;i<12;i++){const x=(i-5.5)*(w-.8)/12;for(const z of [-d/2+.28,d/2-.28])box(g,.16,.025,.38,x,.27,z,mats.gold);}
      label('substrate','Organic substrate','有機封裝基板',g,[-w/2,.35,d/2]);return g;
    }
    function memoryStack(parent,x,z,tiers=6) {const g=new T.Group();g.position.set(x,-.14,z);parent.add(g);balls(g,6,7,.28,.29,-.20,.10);const layers=[[],[]],strips=[];for(let i=0;i<tiers;i++){layers[i%2].push([2,.20,2.3,0,i*.235,0]);for(let j=0;j<4;j++)strips.push([.025,.055,2.16,-.78+j*.52,i*.235+.11,0]);}boxes(g,layers[0],mats.silicon);boxes(g,layers[1],mats.memory);boxes(g,strips,mats.copper);box(g,1.96,.024,2.26,0,(tiers-1)*.235+.12,0,mats.silicon);return g;}
    function sectionBody(parent,w,h,d,x,y,z,mat){const sm=keep(mat.clone());sm.transparent=true;const mesh=box(parent,w,h,d,x,y,z,sm);sectionMeshes.push(mesh);return mesh;}
    function modelInterposer() {
      base();const inter=layer('Silicon interposer',1.01,.82);sectionBody(inter,12.5,.28,8.8,0,0,0,mats.silicon);
      pads(inter,13,9,.9,.87,0,.07,.36,mats.copper);
      const dies=layer('Logic and HBM',1.60,1.95);const chip=etchedDie(dies,4.7,5.1,0,0,0);label('logic','Compute die','運算晶粒',chip,[0,.3,1]);
      const bumps=new T.Group();bumps.position.set(0,-.34,0);dies.add(bumps);balls(bumps,15,16,.29,.29,0,.10);
      for(const x of [-4.2,4.2])for(const z of [-2.45,2.45]){const stack=memoryStack(dies,x,z);for(let i=0;i<6;i++){const zz=z+(i-2.5)*.15;trace(inter,[[Math.sign(x)*2.4,.18,zz],[Math.sign(x)*3.1,.18,zz+.15],[x,.18,zz+.15]],.023);}if(x>0&&z>0)label('hbm','Stacked HBM memory','HBM 堆疊記憶體',stack,[1,1.7,1]);}
      label('interposer','Silicon interposer + TSVs','矽中介層與 TSV',inter,[-5.2,.2,3.8]);label('microbumps','Microbump interface','微凸塊互連',dies,[2.3,-.4,2.4]);
    }
    function modelFanout() {
      base(14,10.2);const rdl=[];for(let k=0;k<3;k++){const l=layer('Redistribution layer '+k,1.05+k*.17,.7+k*.36);box(l,12.5,.07,8.8,0,0,0,mats.dielectric);rdl.push(l);for(let i=0;i<17;i++){const z=(i-8)*.39;const from=(i%2?-1:1)*2.2,to=(i%2?-1:1)*5.6;trace(l,[[from,.055,z*.65],[from+(to-from)*.38,.055,z*.65],[to-.5*Math.sign(to),.055,z],[to,.055,z]],.026,k===2);}}
      const mold=layer('Reconstructed mold',1.83,2.25);box(mold,12.5,.7,8.8,0,0,0,mats.mold);const die=etchedDie(mold,4.4,4.4,0,.13,0);label('die','Embedded die','嵌入模封的晶粒',die,[0,.4,1]);
      label('mold','Mold compound','模封材料',mold,[-5,.4,3.6]);label('rdl','Fan-out redistribution layers','扇出重佈線層 RDL',rdl[1],[-5,.15,3.9]);label('fanout','Connections extend beyond die','互連延伸至晶粒外',rdl[2],[5.4,.14,-2.4]);
      pads(rdl[0],18,12,.60,.62,-.07,.085,.04,mats.gold);
    }
    function modelHybrid() {
      base(11,10);const lower=layer('Lower die',1.18,.52);const ld=etchedDie(lower,7.8,7.5,0,0,0);label('bottom-die','Lower active die','下層主動晶粒',ld,[-3.7,.3,3.4]);
      const contact=layer('Planar Cu bond interface',1.47,1.4);box(contact,7.72,.035,7.42,0,0,0,mats.dielectric);pads(contact,22,21,.32,.32,.038,.07,.028);label('bond','Planar copper + dielectric bonds','平面銅與介電層混合鍵合',contact,[3.3,.10,3.5]);
      const upper=layer('Upper die',1.76,2.4);etchedDie(upper,7.7,7.4,0,0,0);pads(upper,22,21,.32,.32,-.255,.07,.025);label('top-die','Directly bonded upper die','直接鍵合的上層晶粒',upper,[3,.45,-3]);
      for(let x=-3;x<=3;x+=1.2)for(let z=-3;z<=3;z+=1.2){cyl(lower,.045,.55,x,0,z,mats.copper);cyl(upper,.045,.55,x,0,z,mats.copper);}
      for(let x=-2;x<=2;x+=1)trace(lower,[[x,-.25,2.2],[x,.08,2.2],[x,.3,2.2]],.035);
    }
    function modelBridge() {
      const b=base();sectionBody(b,12.8,.055,9,0,.29,0,mats.dielectric);
      const bridge=layer('Local embedded silicon bridge',.94,.65);sectionBody(bridge,2.8,.20,6.3,0,0,0,mats.silicon);
      for(let i=0;i<25;i++){const z=(i-12)*.23;trace(bridge,[[-1.2,.12,z],[-.65,.12,z+.06],[.65,.12,z+.06],[1.2,.12,z]],.023);}
      const dies=layer('Adjacent dies',1.47,1.9);etchedDie(dies,5.15,6.4,-2.85,0,0);etchedDie(dies,5.15,6.4,2.85,0,0);
      const bumpLeft=new T.Group();bumpLeft.position.x=-1.06;dies.add(bumpLeft);balls(bumpLeft,3,20,.18,.28,-.35,.052);const bumpRight=bumpLeft.clone();bumpRight.position.x=1.06;dies.add(bumpRight);
      label('bridge','Local silicon bridge','局部嵌入式矽橋',bridge,[0,.2,3]);label('dies','Neighbouring logic dies','相鄰運算晶粒',dies,[3.8,.4,2.8]);label('organic','Routing through organic substrate','有機基板上的其餘走線',b,[-5,.4,3.7]);
    }
    function modelChiplet() {
      base(15.5,11);const routing=layer('Die-to-die routing',.99,.7);box(routing,14.1,.16,9.7,0,0,0,mats.dielectric);
      const dies=layer('Modular chiplets',1.42,1.8);const io=etchedDie(dies,4,5.5,0,0,0);label('io','I/O hub','I/O 中樞晶粒',io,[0,.4,2.1]);
      for(const x of [-5,5])for(const z of [-2.65,2.65]){const die=etchedDie(dies,3.1,3.2,x,0,z);for(let i=0;i<6;i++){const dz=(i-2.5)*.18;trace(routing,[[x-Math.sign(x)*1.4,.12,z+dz],[x/2,.12,z+dz],[Math.sign(x)*2,.12,z*.65+dz]],.026);}if(x<0&&z>0)label('chiplet','Compute chiplet','運算小晶片',die,[-1,.4,1.2]);}
      label('link','Die-to-die physical links','晶粒間實體互連',routing,[2.9,.2,2.0]);label('ecosystem','Protocol, packaging and validation','協定、封裝與驗證協作',routing,[-3.8,.15,-3.7]);
    }
    function modelThermal() {
      base();const dies=layer('Heat-generating dies',1.15,.65);etchedDie(dies,4.4,5,0,0,0);for(const x of [-4,4])memoryStack(dies,x,0,4);box(dies,4.4,.44,5,0,.47,0,mats.silicon);label('source','Compute and memory heat sources','運算與記憶體熱源',dies,[0,.3,2.3]);
      const tim=layer('Thermal interface material',2.07,1.7);box(tim,11.5,.12,7.3,0,0,0,mats.ceramic);label('tim','Thermal interface material','導熱介面材料 TIM',tim,[-5,.1,3]);
      const lid=layer('Integrated heat spreader',2.43,2.6);box(lid,12.3,.46,8,0,0,0,mats.aluminum);label('lid','Heat spreader','均熱蓋',lid,[5,.3,3.2]);
      const sink=layer('Heat sink',2.85,3.45);box(sink,12.5,.24,8.2,0,0,0,mats.aluminum);for(let i=0;i<19;i++)box(sink,.19,2.7,8,-5.7+i*.63,1.45,0,mats.aluminum);label('cooler','Fins move heat into airflow','鰭片將熱帶入氣流',sink,[5,2.9,3]);
      const heatMat=material('#ff5f2b',.1,.5,{transparent:true,opacity:.38,depthWrite:false,emissive:'#ff3f0c',emissiveIntensity:.8});
      for(let i=0;i<5;i++){const g=new T.Mesh(keep(new T.TorusGeometry(1.1+i*.34,.035,5,48)),heatMat);g.rotation.x=Math.PI/2;g.position.y=1.7+i*.28;model.add(g);heatObjects.push({node:g,base:1.7+i*.28,phase:i*.23});}
    }
    // Metrology table and quiet lab context. Geometry remains intentionally schematic.
    box(background,110,.24,110,0,-.32,0,mats.floor);
    cyl(background,11.3,.7,0,.2,0,mats.table);cyl(background,11.05,.11,0,.61,0,mats.black);
    const ring=new T.Mesh(keep(new T.TorusGeometry(10.98,.022,8,160)),mats.cyan);ring.rotation.x=Math.PI/2;ring.position.y=.68;background.add(ring);
    for(const x of [-8,8])for(const z of [-6,6])cyl(background,.18,.05,x,.72,z,mats.aluminum);
    const brushedCanvas=document.createElement('canvas');brushedCanvas.width=256;brushedCanvas.height=256;const bc=brushedCanvas.getContext('2d');
    bc.fillStyle='#878787';bc.fillRect(0,0,256,256);for(let n=0;n<256;n++){const c=Math.round(126+9*Math.sin(n*13.7)+5*Math.sin(n*3.1));bc.fillStyle='rgb('+c+','+c+','+c+')';bc.fillRect(0,n,256,1);}const brushed=keep(new T.CanvasTexture(brushedCanvas));brushed.wrapS=brushed.wrapT=T.RepeatWrapping;brushed.repeat.set(5,5);mats.table.roughnessMap=brushed;mats.aluminum.roughnessMap=brushed;
    const engravingMat=material('#26323e',.78,.37);for(let n=0;n<4;n++){const engraving=new T.Mesh(keep(new T.TorusGeometry(10.4+n*.10,.012,5,160)),engravingMat);engraving.rotation.x=Math.PI/2;engraving.position.y=.675;background.add(engraving);}
    // Small route stations around the central package: wafers, routing, bonding,
    // inspection and cooling. Their path helps read the project as a process.
    const routePts=[];
    for(let i=0;i<6;i++){
      const angle=-Math.PI*.18+i*Math.PI*2/6,x=Math.cos(angle)*18.2,z=Math.sin(angle)*18.2;
      const g=new T.Group();g.position.set(x,0,z);background.add(g);cyl(g,2.35,.35,0,.16,0,mats.table);cyl(g,2.22,.025,0,.35,0,mats.black);
      const halo=new T.Mesh(keep(new T.TorusGeometry(2.24,.024,6,60)),mats.cyan);halo.rotation.x=Math.PI/2;halo.position.y=.39;g.add(halo);highlights.push(halo);
      if(i===0){const wafer=cyl(g,1.62,.06,0,.46,0,mats.silicon);for(let k=-3;k<=3;k++){box(g,2.9,.008,.018,0,.5,k*.4,mats.gold);box(g,.018,.008,2.9,k*.4,.51,0,mats.gold);}wafer.rotation.y=.2;}
      if(i===1){for(let k=0;k<3;k++){box(g,2.6,.06,2.6,0,.45+k*.23,0,mats.dielectric);for(let j=0;j<5;j++)trace(g,[[-1.1,.5+k*.23,(j-2)*.4],[0,.5+k*.23,(j-2)*.3],[1.1,.5+k*.23,(j-2)*.4]],.025,false);}}
      if(i===2){etchedDie(g,1.8,1.8,-.5,.72,-.5);etchedDie(g,1.8,1.8,.5,1.45,.5);}
      if(i===3){box(g,2.6,.25,2.6,0,.55,0,mats.substrate);etchedDie(g,1.8,1.8,0,.98,0);for(let k=-1;k<=1;k++)cyl(g,.06,.6,k*.45,1.65,.2,mats.copper);}
      if(i===4){box(g,2.8,.16,2.8,0,.5,0,mats.ceramic);cyl(g,.37,1.6,0,1.6,0,mats.aluminum);cyl(g,.52,.15,0,1.0,0,mats.black);}
      if(i===5){box(g,2.8,.16,2.5,0,.5,0,mats.aluminum);for(let k=0;k<7;k++)box(g,.12,.8,2.4,-1.2+k*.4,.98,0,mats.aluminum);}
      routePts.push([x,.08,z]);
    }
    routePts.push(routePts[0]);tube(background,routePts,.025,material('#3b778a',.3,.4,{emissive:'#1a6174',emissiveIntensity:.25}));
    // Dark architectural rails suggest a real optical bench without toy-like machines.
    for(const side of [-1,1]){
      box(background,2.4,.75,38,side*28,.18,-4,mats.table);
      box(background,.12,.04,37,side*27,.59,-4,mats.aluminum);
      box(background,.035,.016,36,side*26.8,.62,-4,mats.cyan);
      for(let k=0;k<8;k++)cyl(background,.13,.05,side*28,.59,-20+k*4.7,mats.aluminum);
    }
    // A sparsely marked floor grounds the aerial view without competing with it.
    for(let i=-3;i<=3;i++){const geom=keep(new T.BufferGeometry().setFromPoints([new T.Vector3(-45,-.185,i*10),new T.Vector3(45,-.185,i*10)]));background.add(new T.Line(geom,lineMaterial));}
    const builders={interposer:modelInterposer,fanout:modelFanout,hybrid:modelHybrid,bridge:modelBridge,chiplet:modelChiplet,thermal:modelThermal};
    const modelResources=new Set();
    function setTour(id) {
      if(!IDS.includes(id))id='interposer';current=id;
      // Release geometries and materials from the previous package, retaining the
      // shared studio and unit geometries/materials. No GPU growth when switching.
      for(const r of modelResources){r.dispose?.();resources.delete(r);}modelResources.clear();
      model.traverse(o=>{if(o.isInstancedMesh)o.dispose();});core.remove(model);model=new T.Group();core.add(model);moving.length=0;labels.length=0;signals.length=0;heatObjects.length=0;sectionMeshes.length=0;
      const before=new Set(resources);builders[id]();if(id!=='thermal'){const hm=material('#f5703b',.25,.4,{transparent:true,opacity:.36,depthWrite:false,emissive:'#e34b19',emissiveIntensity:.7});for(let k=0;k<3;k++){const h=new T.Mesh(keep(new T.TorusGeometry(1.8+k*.35,.035,6,56)),hm);h.rotation.x=Math.PI/2;h.position.y=2.3+k*.4;model.add(h);heatObjects.push({node:h,base:2.3+k*.4,phase:k*.29,thermalOnly:true});}}for(const r of resources)if(!before.has(r))modelResources.add(r);
      core.updateMatrixWorld(true);for(const l of moving){const b=new T.Box3().setFromObject(l.node),origin=l.node.getWorldPosition(new T.Vector3());l.bounds={min:b.min.sub(origin),max:b.max.sub(origin)};}
      render(0);return api;
    }
    const poses=[
      {az:.67,el:.65,r:29,ty:1.25,ex:0},
      {az:.38,el:.75,r:25,ty:2.0,ex:.06},
      {az:-.23,el:.54,r:22.5,ty:2.9,ex:.56},
      {az:.38,el:.58,r:25.5,ty:3.7,ex:1},
      {az:.42,el:.23,r:24.5,ty:4.0,ex:1},
      {az:.17,el:1.07,r:23.5,ty:3.3,ex:.65},
      {az:-.45,el:.73,r:25,ty:3.3,ex:.38},
      {az:-.75,el:.52,r:24.5,ty:3.0,ex:.35},
      {az:.10,el:.79,r:27,ty:2.3,ex:.2},
      {az:.66,el:1.02,r:31.5,ty:1.4,ex:0},
      {az:.83,el:1.06,r:32,ty:1.4,ex:0}
    ];
    function render(timeSeconds=0,options={}) {
      if(disposed)return;
      lastTime=clamp(Number(timeSeconds)||0,0,300);const index=Math.min(9,Math.floor(lastTime/30));lastView=VIEWS.includes(options.view)?options.view:VIEWS[index];
      const i=VIEWS.indexOf(lastView),p=lastTime===300?1:(lastTime%30)/30;
      // A short transition is followed by a calm look around the same structure.
      const prev=poses[Math.max(0,i-1)],target=poses[i],settle=ease(p/.24);
      const az=mix(prev.az,target.az,settle)+Math.sin(p*Math.PI)*.09;
      const el=mix(prev.el,target.el,settle),r=mix(prev.r,target.r,settle);
      explosion=typeof options.exploded==='number'?clamp(options.exploded,0,1.6):options.exploded===true?1:options.exploded===false?0:mix(prev.ex,target.ex,settle);
      for(const l of moving)l.node.position.y=l.y+l.lift*explosion;
      const focusY=mix(prev.ty,target.ty,settle)+(current==='thermal'?1.1:0);
      const portrait=width/height<1;let dist=r*(portrait?Math.max(1.38,.96/(width/height)):1);
      // Keep the whole package between title and captions. Oblique views remain
      // close; steep or tall exploded views pull back just enough to fit safely.
      // This is derived from actual layer bounds, not an aspect-ratio guess.
      const frame=()=>{camera.clearViewOffset();camera.position.set(Math.sin(az)*Math.cos(el)*dist,Math.sin(el)*dist+focusY,Math.cos(az)*Math.cos(el)*dist);camera.lookAt(0,focusY,0);camera.updateMatrixWorld();let minX=1,maxX=-1,minY=1,maxY=-1;for(const l of moving){if(!l.bounds)continue;for(const x of [l.bounds.min.x,l.bounds.max.x])for(const y of [l.bounds.min.y,l.bounds.max.y])for(const z of [l.bounds.min.z,l.bounds.max.z]){const p=new T.Vector3(x,y+l.node.position.y+core.position.y,z).project(camera);minX=Math.min(minX,p.x);maxX=Math.max(maxX,p.x);minY=Math.min(minY,p.y);maxY=Math.max(maxY,p.y);}}return {minX,maxX,minY,maxY};};
      let bounds=frame();const maxFrameWidth=portrait?1.76:1.24,maxFrameHeight=portrait?1.04:1.20;
      for(let attempt=0;attempt<3;attempt++){const need=Math.max((bounds.maxX-bounds.minX)/maxFrameWidth,(bounds.maxY-bounds.minY)/maxFrameHeight,1);if(need<=1.006)break;dist*=need*1.015;bounds=frame();}
      const centerY=(bounds.minY+bounds.maxY)/2,desiredCenterY=.08;camera.setViewOffset(width,height,0,height*(desiredCenterY-centerY)/2,width,height);camera.updateMatrixWorld();
      const sectionWeight=i===4?settle:i===5?1-settle:0,sectionOpacity=1-.82*sectionWeight;for(const mesh of sectionMeshes){mesh.material.opacity=sectionOpacity;mesh.material.depthWrite=sectionOpacity===1;}
      for(const s of signals){const q=(lastTime*.13+s.phase)%1;s.dot.position.copy(s.curve.getPoint(q));s.dot.visible=['signal','interconnect','overview','roadmap'].includes(lastView);}
      for(const h of heatObjects){const phase=(lastTime*.16+h.phase)%1;h.node.position.y=h.base+phase*3.5+explosion*1.8;h.node.scale.setScalar(.9+phase*.65);h.node.visible=h.thermalOnly?lastView==='thermal':['thermal','overview','roadmap'].includes(lastView);}
      for(let k=0;k<highlights.length;k++){highlights[k].scale.setScalar(1+((Math.floor(lastTime/50)%6)===k?.025*Math.sin(lastTime*1.7):0));}
      renderer.render(scene,camera);
    }
    function resize(w,h,pixelRatio=Math.min(window.devicePixelRatio||1,2)) {width=Math.max(1,w);height=Math.max(1,h);renderer.setPixelRatio(clamp(pixelRatio,1,2));renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix();render(lastTime,{view:lastView});}
    function getLabels() {
      return labels.map(l=>{const point=l.parent.localToWorld(l.position.clone()),ndc=point.clone().project(camera);const visible=ndc.z>-1&&ndc.z<1&&ndc.x>-.94&&ndc.x<.94&&ndc.y>-.9&&ndc.y<.9;
        return {key:l.key,en:l.en,zh:l.zh,x:(ndc.x*.5+.5)*width,y:(-.5*ndc.y+.5)*height,visible};});
    }
    function getState(){return {tour:current,time:lastTime,view:lastView,explosion,width,height,webgl:true,triangles:renderer.info.render.triangles,calls:renderer.info.render.calls,teachingReconstruction:true,camera:{x:camera.position.x,y:camera.position.y,z:camera.position.z}};}
    function dispose(){if(disposed)return;disposed=true;scene.traverse(o=>{if(o.isInstancedMesh)o.dispose();});for(const r of resources)r.dispose?.();renderer.dispose();scene.clear();}
    const api={setTour,render,resize,getLabels,getState,dispose,canvas};
    resize(canvas.clientWidth||1280,canvas.clientHeight||720);setTour(current);return api;
  }
  window.MG_PACKAGING_SCENE={version:'33.0.0',create,views:[...VIEWS],tourIds:[...IDS]};
})();
