/* Continuous engineering world. Geometry is an educational model;
   credited photographs on evidence boards remain photographic references. */
import {normalizeWalkSettings} from './walk-v28.js';
import {clamp,normalizeInput,moveWithCollisions,cameraRelativeMove,findPath,nearestStation,isWalkable,angleDelta,approachVelocity,stationObstacles,cameraClearFraction} from './walk-physics-v22.js';

export function createWalkWorld({container,THREE:T,config,onNear=()=>{},onInteract=()=>{},onMove=()=>{},onView=()=>{},onManual=()=>{},onPhoto=()=>{},onError=()=>{}}) {
  if(!container||!T?.WebGLRenderer)throw Error('The local Three.js renderer is required.');
  const scene=new T.Scene(),camera=new T.PerspectiveCamera(58,1,.1,140);
  const renderer=new T.WebGLRenderer({antialias:true,alpha:false,powerPreference:'high-performance'});
  const compact = matchMedia('(pointer: coarse)').matches;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  renderer.setPixelRatio(Math.min(devicePixelRatio||1,compact ? 1.35 : 1.7));renderer.setSize(container.clientWidth||innerWidth,container.clientHeight||innerHeight);
  renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;
  renderer.domElement.className='walk-canvas';renderer.domElement.style.cssText='display:block;width:100%;height:100%;touch-action:none;outline:none';
  renderer.domElement.tabIndex=0;renderer.domElement.setAttribute('aria-label','Walkable engineering scene');container.append(renderer.domElement);
  const labelLayer=document.createElement('div');labelLayer.className='walk-label-layer';labelLayer.style.cssText='position:absolute;inset:0;overflow:hidden;pointer-events:none';container.append(labelLayer);
  const raycaster=new T.Raycaster(), pointer=new T.Vector2(),v3=new T.Vector3(),lookAt=new T.Vector3(),cameraAim=new T.Vector3(),cameraWanted=new T.Vector3(),cameraAnchor=new T.Vector3();
  const clock=new T.Clock(),loader=new T.TextureLoader(),keys=new Set(),listeners=[],pointers=new Map();
  let world=new T.Group(),worldMaterials=[],worldGeometries=[],worldTextures=[],stations=[],obstacles=[],labels=[],bounds={width:30,depth:38};
  let disposed=false,paused=false,language='zh-TW',view='follow',yaw=0,pitch=.34,distance=6.6,position={x:0,z:14},external={x:0,z:0},path=[],near=null,lastNear='',walkTime=0,lastEmit=0,frame=0,configEpoch=0,lastPinch=0,drag=null,completed=new Set();
  const cameraDefaults = {follow:[.34,6.6], close:[.28,3.7], first:[.04,0], overview:[.92,13]};
  let velocity={x:0,z:0},heading=0,firstFov=72,manualLookUntil=0,objectiveId='',snapCamera=true;
  let displaySettings=normalizeWalkSettings(),frameRate=60,frameSamples=0,frameSeconds=0,adaptiveRatio=compact?1.1:1.4,speedMps=0;
  scene.add(world);
  const palette={metal:0x9cabb2,dark:0x24383f,body:0xe0e7e9,black:0x15252d,yellow:0xe6b64a,cyan:0x73dbc6};
  const makeMaterial=(color,roughness=.45,metalness=.25,other={})=>{const m=new T.MeshStandardMaterial({color,roughness,metalness,...other});worldMaterials.push(m);return m;};
  let mats={};
  function mesh(geometry,material,parent,x=0,y=0,z=0){worldGeometries.push(geometry);const m=new T.Mesh(geometry,material);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
  const box=(p,w,h,d,x,y,z,m)=>mesh(new T.BoxGeometry(w,h,d),m,p,x,y,z);
  const cylinder=(p,rt,rb,h,x,y,z,m,n=24)=>mesh(new T.CylinderGeometry(rt,rb,h,n),m,p,x,y,z);
  function pipe(p,from,to,r,m){const a=new T.Vector3(...from),b=new T.Vector3(...to),v=b.clone().sub(a);const obj=cylinder(p,r,r,v.length(),...a.clone().add(b).multiplyScalar(.5).toArray(),m,12);obj.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),v.normalize());return obj;}
  const sphere=(p,r,x,y,z,m)=>mesh(new T.SphereGeometry(r,18,12),m,p,x,y,z);
  function textureCanvas(draw,width=512,height=256){const c=document.createElement('canvas');c.width=width;c.height=height;draw(c.getContext('2d'),width,height);const texture=new T.CanvasTexture(c);texture.colorSpace=T.SRGBColorSpace;worldTextures.push(texture);return texture;}
  function screen(p,w,h,x,y,z,variant=0){const map=textureCanvas((ctx,W,H)=>{ctx.fillStyle='#071d2a';ctx.fillRect(0,0,W,H);ctx.fillStyle='#72e2d0';ctx.font='bold 25px monospace';ctx.fillText(variant?'PROCESS / DEMO':'SYSTEM / DEMO',24,42);ctx.strokeStyle='#214856';ctx.lineWidth=1;for(let i=0;i<12;i++){ctx.beginPath();ctx.moveTo(20,65+i*13);ctx.lineTo(W-20,65+i*13);ctx.stroke();}ctx.strokeStyle='#83e2c4';ctx.lineWidth=3;ctx.beginPath();for(let x=24;x<W-20;x++){const y=145+Math.sin(x*.035+variant)*24+Math.sin(x*.11)*5;x===24?ctx.moveTo(x,y):ctx.lineTo(x,y);}ctx.stroke();ctx.fillStyle='#e4bb5b';for(let i=0;i<5;i++)ctx.fillRect(30+i*80,H-40,50,8+Math.sin(i)*7);});const material=makeMaterial(0xffffff,.5,.1,{map,emissive:0x9cfff0,emissiveIntensity:.18});const s=box(p,w,h,.055,x,y,z,material);return s;}
  function statusLight(p,x,y,z){const g=new T.Group();g.position.set(x,y,z);p.add(g);cylinder(g,.055,.055,.48,0,0,0,mats.dark);for(let i=0;i<3;i++)cylinder(g,.11,.11,.11,0,.08+i*.13,0,i===2?mats.glow:mats.amber,14);}
  function platform(p){box(p,3.3,.14,2.7,0,.07,0,mats.dark);box(p,3.38,.045,.08,0,.16,1.36,mats.yellow);}
  function machine(p,kind,index){platform(p);
    if(kind==='rf-bench'||kind==='timing-bench'){
      box(p,3,.14,1.8,0,1.05,0,mats.body);for(const x of [-1.2,1.2])box(p,.13,.94,1.4,x,.51,0,mats.metal);
      box(p,1.25,.65,1,-.65,1.46,0,mats.metal);screen(p,1.02,.4,-.65,1.5,.54,index);
      for(let j=0;j<4;j++){const knob=cylinder(p,.065,.065,.07,-1+j*.23,1.25,.58,mats.dark,12);knob.rotation.x=Math.PI/2;}
      box(p,.9,.48,.75,.8,1.37,0,mats.dark);screen(p,.64,.25,.8,1.44,.42,index+1);
      for(let j=0;j<2;j++){pipe(p,[-.15,1.25,.62],[.17,1.18,.83+j*.11],.022,mats.amber);pipe(p,[.17,1.18,.83+j*.11],[.5,1.23,.55],.022,mats.amber);}
      if(kind==='rf-bench'){for(const x of [.45,1.2]){pipe(p,[x,1.66,-.1],[x,2.5,-.1],.026,mats.metal);for(let j=0;j<4;j++)pipe(p,[x-.22,2+j*.12,-.1],[x+.22,2+j*.12,-.1],.018,mats.accent);}}
      else{box(p,1.2,.07,.5,0,1.18,.8,mats.cyan);for(let j=0;j<6;j++)box(p,.1,.05,.12,-.46+j*.18,1.24,.8,mats.dark);}
    }else if(kind==='fiber-link'){
      box(p,2.9,.15,1.8,0,1.05,0,mats.body);for(const x of [-1.2,1.2])box(p,.13,.94,1.4,x,.51,0,mats.metal);
      for(const x of [-.95,.95]){box(p,.7,.65,.7,x,1.46,0,mats.dark);screen(p,.5,.3,x,1.52,.39,index);}
      const coil=mesh(new T.TorusGeometry(.43,.025,8,36),mats.amber,p,0,1.2,.1);coil.rotation.x=Math.PI/2;
      pipe(p,[-.55,1.25,.1],[-.3,1.25,.4],.025,mats.amber);pipe(p,[.3,1.25,.4],[.55,1.25,.1],.025,mats.amber);
      for(let j=0;j<3;j++)box(p,.22,.13,.2,-.3+j*.3,1.17,.75,mats.cyan);
    }else if(kind==='packet-wall'){
      box(p,3,2.25,.2,0,1.75,-.2,mats.dark);for(const x of [-1.2,1.2])box(p,.13,.8,.9,x,.54,-.2,mats.metal);
      for(let row=0;row<3;row++)for(let col=0;col<5;col++)box(p,.4,.3,.05,-1.08+col*.54,1.03+row*.6,-.06,(row+col)%3===0?mats.amber:mats.cyan);
      for(let j=0;j<3;j++)pipe(p,[-1.3,.8+j*.6,.02],[1.3,.8+j*.6,.02],.02,mats.metal);
      box(p,3.1,.16,.9,0,.77,.1,mats.body);
    }else if(kind==='satellite'){
      box(p,1.12,1.2,1.02,0,1.25,0,mats.amber);
      box(p,.94,.86,.045,0,1.28,.54,mats.body);
      for(const side of [-1,1]){
        pipe(p,[side*.49,1.32,0],[side*.75,1.32,0],.035,mats.metal);
        box(p,.95,.045,1.42,side*1.15,1.32,0,mats.dark);
        for(let x=0;x<3;x++)for(let z=0;z<6;z++)box(p,.27,.018,.212,side*1.15-.29+x*.29,1.353,-.56+z*.225,mats.cyan);
      }
      const dish=mesh(new T.SphereGeometry(.44,24,12,0,Math.PI*2,0,Math.PI*.44),mats.body,p,0,2,0);
      dish.rotation.x=Math.PI*.68;
      pipe(p,[0,2,0],[.01,2.32,.4],.026,mats.metal);
      cylinder(p,.14,.14,.72,0,.64,0,mats.dark);
      box(p,1.7,.15,1.3,0,.27,0,mats.metal);
    }else if(kind==='cryostat'){
      cylinder(p,.85,.85,2.45,0,1.55,0,mats.metal);
      for(let j=0;j<5;j++){cylinder(p,.7-j*.1,.7-j*.1,.08,0,.55+j*.42,0,mats.amber);for(const side of [-1,1])pipe(p,[side*(.6-j*.1),.6+j*.42,0],[side*(.5-j*.1),1+j*.42,.12],.025,mats.cyan);}
      box(p,1.45,2.25,.05,0,1.55,.77,mats.glass);
      screen(p,.7,.45,1.15,1.5,.65,index);statusLight(p,1.15,2.2,.4);
    }else if(kind==='accelerator'){
      box(p,2.8,.35,1.7,0,1.25,0,mats.dark);
      for(let j=0;j<4;j++){box(p,.48,.1,.7,-.9+j*.6,1.48,0,mats.cyan);for(let k=0;k<7;k++)box(p,.04,.25,.68,-1.08+j*.6+k*.06,1.65,0,mats.metal);}
      for(const z of [-.65,.65])pipe(p,[-1.25,1.52,z],[1.25,1.52,z],.045,mats.accent);
      for(const x of [-1.1,1.1])box(p,.12,1.05,1.2,x,.65,0,mats.metal);screen(p,1.8,.72,0,2.3,-.55,index);
    }else if(kind==='hpc-node'){
      box(p,2.8,2.55,1.55,0,1.52,0,mats.dark);
      for(let j=0;j<4;j++){box(p,2.5,.43,.10,0,.57+j*.58,.82,mats.metal);for(let k=0;k<4;k++){box(p,.35,.26,.04,-.91+k*.61,.58+j*.58,.89,mats.cyan);statusLight(p,-.86+k*.61,.59+j*.58,.93);}}
      pipe(p,[-1.3,.3,-.6],[-1.3,2.8,-.6],.07,mats.cyan);pipe(p,[1.3,.3,-.6],[1.3,2.8,-.6],.07,mats.amber);
    }else if(kind==='network-fabric'){
      for(const x of [-1.25,1.25])box(p,.1,2.35,.8,x,1.35,0,mats.metal);
      for(let j=0;j<3;j++){box(p,2.5,.44,.72,0,.66+j*.7,0,mats.dark);for(let k=0;k<8;k++)box(p,.16,.13,.04,-1+k*.28,.67+j*.7,.39,mats.cyan);}
      for(let j=0;j<4;j++){pipe(p,[-.9+j*.55,.7,.45],[-.9+j*.55,1.08,.75],.025,j%2?mats.amber:mats.cyan);pipe(p,[-.9+j*.55,1.08,.75],[.8-j*.48,1.4,.45],.025,j%2?mats.amber:mats.cyan);}
    }else if(kind==='storage-array'||kind==='log-archive'){
      box(p,2.7,2.3,1.5,0,1.4,0,mats.dark);
      for(let row=0;row<5;row++)for(let col=0;col<4;col++){box(p,.55,.33,.08,-.93+col*.62,.49+row*.43,.8,mats.metal);box(p,.33,.04,.04,-.93+col*.62,.49+row*.43,.86,mats.black);statusLight(p,-.74+col*.62,.49+row*.43,.87);}
      if(kind==='log-archive')screen(p,1.6,.54,0,2.65,.2,index);
    }else if(kind==='memory-bench'){
      box(p,2.9,.14,1.8,0,1.05,0,mats.body);for(const x of [-1.2,1.2])box(p,.12,.95,1.4,x,.52,0,mats.metal);
      box(p,1.8,.08,1.3,-.25,1.19,0,mats.accent);for(let row=0;row<4;row++){box(p,1.45,.30,.08,-.25,1.39,-.45+row*.3,mats.cyan);for(let col=0;col<5;col++)box(p,.19,.18,.09,-.83+col*.29,1.42,-.45+row*.3,mats.dark);}screen(p,.6,.5,1.03,1.8,.7,index);
    }else if(kind==='availability-panel'){
      for(const side of [-1,1]){box(p,.92,2.1,1.15,side*.76,1.3,0,mats.dark);screen(p,.66,.56,side*.76,1.7,.6,index);for(let j=0;j<3;j++)box(p,.69,.18,.06,side*.76,.6+j*.27,.61,mats.metal);}
      pipe(p,[-.75,2.48,0],[.75,2.48,0],.06,mats.amber);statusLight(p,-.75,2.52,.3);statusLight(p,.75,2.52,.3);
    }else if(kind==='cooling-cdu'){
      box(p,2.15,2.3,1.65,-.2,1.4,0,mats.body);screen(p,.85,.55,-.35,1.97,.87,index);
      for(const side of [-1,1]){pipe(p,[side*.58,.55,.93],[side*.58,1.45,.93],.09,side<0?mats.cyan:mats.amber);cylinder(p,.17,.17,.12,side*.58,1,.93,mats.metal);}
      for(let j=0;j<7;j++)box(p,.04,1.4,1.05,.86+j*.07,1.1,0,mats.metal);statusLight(p,.68,2.55,.5);
    }else if(kind==='soc-console'||kind==='recovery-bench'){
      box(p,3,.15,1.5,0,1.1,0,mats.body);for(const x of [-1.3,1.3])box(p,.13,1.02,1.2,x,.54,0,mats.metal);
      for(const side of [-1,1]){screen(p,1.2,.8,side*.7,2.1,-.15,index);box(p,.1,.5,.1,side*.7,1.42,-.2,mats.dark);box(p,.9,.045,.35,side*.7,1.21,.45,mats.dark);}
      if(kind==='recovery-bench'){box(p,.7,.4,.7,0,.45,.15,mats.accent);for(let j=0;j<3;j++)box(p,.51,.07,.05,0,.35+j*.11,.53,mats.metal);}
    }else if(kind==='asset-board'){
      box(p,2.8,1.8,.13,0,1.8,0,mats.dark);for(const x of [-1.1,1.1])box(p,.1,.9,.6,x,.47,0,mats.metal);
      for(let row=0;row<3;row++)for(let col=0;col<5;col++)box(p,.38,.35,.04,-1.04+col*.52,1.24+row*.48,.10,row===2&&col===4?mats.amber:mats.cyan);
      box(p,2.9,.1,.45,0,.85,.15,mats.metal);
    }else if(kind==='backup-vault'){
      box(p,2.2,2.45,1.65,0,1.47,0,mats.metal);box(p,1.95,2.18,.12,0,1.47,.91,mats.dark);
      for(let row=0;row<4;row++)for(let col=0;col<3;col++)box(p,.45,.35,.05,-.6+col*.6,.71+row*.47,.99,mats.body);
      box(p,.12,1.6,.07,.87,1.47,1.02,mats.amber);screen(p,.6,.26,0,2.69,.1,index);
    }else if(kind==='certificate-terminal'){
      box(p,2.8,.15,1.7,0,1.05,0,mats.body);for(const x of [-1.15,1.15])box(p,.12,.94,1.25,x,.51,0,mats.metal);
      screen(p,1.65,1.0,-.3,2.2,-.2,index);box(p,.12,.5,.15,-.3,1.42,-.25,mats.dark);box(p,1.25,.06,.48,-.3,1.17,.5,mats.dark);
      box(p,.55,.62,.6,1,1.42,.3,mats.accent);box(p,.36,.12,.04,1,1.45,.63,mats.amber);statusLight(p,1,1.83,.5);
    }else if(kind==='vacuum'){
      const chamber=cylinder(p,.88,.88,1.8,0,1.3,-.16,mats.metal);
      chamber.rotation.x=Math.PI/2;
      const flange=cylinder(p,.93,.93,.12,0,1.3,.77,mats.dark);flange.rotation.x=Math.PI/2;
      const window=cylinder(p,.53,.53,.095,0,1.3,.87,mats.glass);window.rotation.x=Math.PI/2;
      for(let j=0;j<12;j++){const a=j*Math.PI/6;sphere(p,.041,Math.sin(a)*.8,1.3+Math.cos(a)*.8,.85,mats.body);}
      pipe(p,[.58,2.06,0],[.88,2.44,.3],.085,mats.accent);
      box(p,.55,.56,.65,1.15,.5,.3,mats.dark);
      screen(p,.48,.33,1.15,1.19,.73,index);
      statusLight(p,1.15,1.8,.4);
    }else if(kind==='rocket'){
      cylinder(p,.35,.4,1.6,0,1.44,0,mats.body);
      cylinder(p,.0,.35,.65,0,2.56,0,mats.body);
      cylinder(p,.43,.36,.24,0,.55,0,mats.dark);
      cylinder(p,.37,.37,.13,0,1.36,0,mats.accent);
      for(let j=0;j<3;j++){
        const brace=new T.Group();brace.rotation.y=j*2*Math.PI/3;p.add(brace);
        pipe(brace,[.31,1.38,0],[.76,.23,0],.048,mats.metal);
        box(brace,.35,.13,.36,.76,.23,0,mats.amber);
      }
      screen(p,.63,.45,1.02,1.06,.76,index);
    }else if(kind==='vehicle'||kind==='train'){
      const rail=kind==='train';box(p,rail?2.6:2.7,.56,1.25,0,.86,0,mats.accent);box(p,1.4,.55,1.15,rail?0:-.15,1.36,0,mats.body);box(p,.93,.38,1.19,-.1,1.42,0,mats.glass);box(p,2.2,.1,1.05,0,.45,0,mats.dark);
      for(const x of [-.95,.95])for(const z of [-.68,.68]){const wheel=cylinder(p,.35,.35,.19,x,.5,z,mats.black);wheel.rotation.x=Math.PI/2;const hub=cylinder(p,.19,.19,.2,x,.5,z,mats.metal);hub.rotation.x=Math.PI/2;}
      for(const x of [-1.45,1.45]){box(p,.13,.12,.82,x,.82,0,mats.glow);}
      if(rail)for(const z of [-.68,.68])box(p,3.4,.07,.06,0,.21,z,mats.metal);
    }else if(kind==='robot'){
      cylinder(p,.65,.8,.4,0,.4,0,mats.dark);cylinder(p,.36,.36,.65,0,.9,0,mats.accent);sphere(p,.32,0,1.22,0,mats.amber);pipe(p,[0,1.22,0],[.8,2.2,0],.21,mats.accent);sphere(p,.28,.8,2.2,0,mats.dark);pipe(p,[.8,2.2,0],[1.23,1.65,.5],.16,mats.amber);sphere(p,.2,1.23,1.65,.5,mats.metal);pipe(p,[1.23,1.65,.5],[1.1,1.27,.65],.10,mats.dark);box(p,.52,.12,.28,1.1,1.17,.65,mats.metal);box(p,.85,.65,.7,-.9,.5,.6,mats.body);screen(p,.57,.36,-.9,.92,.97,index);
    }else if(kind==='tank'||kind==='furnace'){
      cylinder(p,1,1,2.3,0,1.45,0,mats.metal);sphere(p,1,0,2.6,0,mats.metal).scale.y=.36;
      for(const x of [-.68,.68])for(const z of [-.65,.65])cylinder(p,.09,.09,.56,x,.4,z,mats.dark,12);
      box(p,1.05,.7,.09,0,1.5,1.02,kind==='furnace'?mats.amber:mats.dark);screen(p,.7,.42,0,1.55,1.085,index);pipe(p,[-1.1,.65,0],[-1.1,2.8,0],.1,mats.accent);pipe(p,[-1.1,2.8,0],[.1,2.8,0],.1,mats.accent);statusLight(p,1.1,2.7,.5);
    }else if(kind==='turbine'){
      const shell=cylinder(p,1,1,2.2,0,1.35,0,mats.body);shell.rotation.x=Math.PI/2;
      const rim=cylinder(p,.83,.83,.1,0,1.35,1.16,mats.dark);rim.rotation.x=Math.PI/2;
      const fan=new T.Group();fan.position.set(0,1.35,1.23);p.add(fan);for(let j=0;j<12;j++){const blade=box(fan,.15,.7,.06,0,.39,0,mats.metal);blade.rotation.z=j*Math.PI/6;blade.position.set(Math.sin(j*Math.PI/6)*.43,Math.cos(j*Math.PI/6)*.43,0);}sphere(p,.23,0,1.35,1.25,mats.metal);p.userData.rotor=fan;box(p,1.6,.25,1.8,0,.32,0,mats.accent);
    }else if(kind==='aircraft'){
      const body=cylinder(p,.29,.1,2.8,0,1.15,0,mats.body);body.rotation.z=Math.PI/2;box(p,1.3,.08,2.65,-.15,1.15,0,mats.accent);box(p,.7,.08,1.2,-1.07,1.2,0,mats.metal);box(p,.6,.6,.08,-1.04,1.49,0,mats.accent);sphere(p,.19,.65,1.38,0,mats.glass).scale.x=2;for(const x of [-.7,.7])cylinder(p,.07,.07,.65,x,.6,0,mats.dark,10);
    }else if(kind==='ship'){
      const hull=box(p,2.85,.62,1.07,0,.75,0,mats.accent);hull.geometry.translate(0,0,0);box(p,2.55,.12,1.16,0,1.1,0,mats.body);box(p,1.05,.55,.82,-.35,1.43,0,mats.body);box(p,.8,.25,.88,-.3,1.78,0,mats.glass);cylinder(p,.035,.035,1.15,.35,1.78,0,mats.metal,8);for(let i=0;i<6;i++)box(p,.25,.23,.4,.6+i*.21,1.28,0,mats.amber);box(p,3.1,.15,1.4,0,.33,0,mats.dark);
    }else if(kind==='bridge'){
      for(const x of [-1.2,1.2]){box(p,.22,2.2,.3,x,1.35,0,mats.metal);box(p,.42,.1,.6,x,2.46,0,mats.accent);}
      box(p,3.1,.17,.9,0,1.1,0,mats.dark);for(const z of [-.4,.4]){pipe(p,[-1.2,2.4,z],[0,1.2,z],.022,mats.body);pipe(p,[1.2,2.4,z],[0,1.2,z],.022,mats.body);for(const x of [-.9,-.45,0,.45,.9])pipe(p,[x,1.23,z],[x,1.48+Math.abs(x)*.72,z],.018,mats.body);}
    }else if(kind==='crane'){
      for(const x of [-1.2,1.2])box(p,.23,2.4,.25,x,1.4,-.3,mats.amber);box(p,2.85,.23,.42,0,2.65,-.3,mats.amber);box(p,.65,.32,.52,.2,2.43,-.3,mats.dark);pipe(p,[.2,2.35,-.3],[.2,1,-.3],.025,mats.metal);box(p,.7,.6,.7,.2,.7,-.3,mats.body);
    }else if(kind==='dish'){
      cylinder(p,.36,.5,.24,0,.4,0,mats.dark);pipe(p,[0,.5,0],[0,1.8,-.1],.15,mats.metal);const dish=mesh(new T.SphereGeometry(1.24,32,18,0,Math.PI*2,0,Math.PI*.44),mats.body,p,0,2.07,0);dish.rotation.x=Math.PI*.65;pipe(p,[0,1.7,.1],[0,2.4,1.05],.035,mats.accent);sphere(p,.13,0,2.4,1.05,mats.dark);
    }else if(kind==='rack'){
      box(p,2.6,2.5,1.25,0,1.5,0,mats.dark);for(let j=0;j<8;j++){box(p,2.3,.21,.08,0,.45+j*.29,.66,mats.metal);for(let k=0;k<5;k++)box(p,.055,.04,.025,-.95+k*.16,.47+j*.29,.714,k%2?mats.glow:mats.amber);}for(const x of [-1.2,0,1.2])box(p,.04,2.4,.05,x,1.5,.72,mats.black);
    }else if(kind==='lithography'){
      box(p,3.1,2.2,2.2,0,1.3,-.1,mats.body);box(p,1.25,1.6,.08,-.65,1.45,1.04,mats.glass);box(p,.09,1.7,.12,-.02,1.4,1.1,mats.metal);screen(p,.87,.65,.92,1.83,1.1,index);cylinder(p,.45,.45,.15,-.67,.76,1.27,mats.metal);const wafer=cylinder(p,.32,.32,.025,-.67,.87,1.27,mats.cyan);wafer.rotation.y=.2;statusLight(p,1.22,2.65,.65);box(p,.7,.25,.25,.91,1.28,1.17,mats.dark);
    }else{
      box(p,2.9,.13,1.8,0,1.08,0,mats.body);for(const x of [-1.25,1.25])for(const z of [-.7,.7])box(p,.1,.95,.1,x,.55,z,mats.metal);
      box(p,1.13,.75,.75,-.67,1.53,0,mats.accent);screen(p,.87,.46,-.67,1.58,.41,index);box(p,.7,.2,.65,.65,1.25,0,mats.dark);cylinder(p,.12,.12,.8,.65,1.73,0,mats.metal);pipe(p,[.65,2.12,0],[.2,2.12,.3],.1,mats.dark);cylinder(p,.3,.3,.06,.65,1.39,.44,mats.metal);statusLight(p,1.23,1.5,-.5);
    }
  }
  function makeAvatar(){const a=new T.Group();const suit=new T.MeshStandardMaterial({color:0x285e69,roughness:.85}),vest=new T.MeshStandardMaterial({color:0xf3b954,roughness:.75}),skin=new T.MeshStandardMaterial({color:0xd5b28c,roughness:.85}),boot=new T.MeshStandardMaterial({color:0x192a32,roughness:.8}),helmet=new T.MeshStandardMaterial({color:0xe8eeee,roughness:.4});
    const mm=(geo,mat,parent,x,y,z)=>{const m=new T.Mesh(geo,mat);m.position.set(x,y,z);m.castShadow=true;parent.add(m);return m;};
    mm(new T.CylinderGeometry(.21,.25,.64,12),suit,a,0,1.12,0);mm(new T.BoxGeometry(.46,.48,.31),vest,a,0,1.18,-.005);
    for(const x of [-.12,.12]){mm(new T.BoxGeometry(.04,.4,.015),helmet,a,x,1.19,-.167);mm(new T.BoxGeometry(.04,.4,.015),helmet,a,x,1.19,.16);}
    mm(new T.SphereGeometry(.17,16,12),skin,a,0,1.62,0);const h=mm(new T.SphereGeometry(.19,16,12,0,Math.PI*2,0,Math.PI/2),helmet,a,0,1.68,0);mm(new T.CylinderGeometry(.23,.23,.035,18),helmet,a,0,1.69,0);mm(new T.BoxGeometry(.18,.1,.04),boot,a,0,1.64,-.15);
    const limbs=[];for(const side of [-1,1]){const leg=new T.Group();leg.position.set(side*.125,.88,0);a.add(leg);mm(new T.CylinderGeometry(.095,.085,.63,10),suit,leg,0,-.30,0);mm(new T.BoxGeometry(.19,.13,.3),boot,leg,0,-.66,-.065);const arm=new T.Group();arm.position.set(side*.31,1.4,0);a.add(arm);mm(new T.CylinderGeometry(.075,.065,.52,10),suit,arm,0,-.24,0);mm(new T.SphereGeometry(.072,12,10),skin,arm,0,-.53,0);limbs.push({leg,arm,side});}
    scene.add(a);return {object:a,limbs,suit,vest,helmet,dispose(){a.traverse(o=>{o.geometry?.dispose();});for(const m of [suit,vest,skin,boot,helmet])m.dispose();scene.remove(a);}};
  }
  const avatar=makeAvatar();
  const ambient=new T.HemisphereLight(0xd6edff,0x526258,2.1);scene.add(ambient);
  const sun=new T.DirectionalLight(0xfff3d6,3.2);sun.position.set(9,19,12);sun.castShadow=true;sun.shadow.mapSize.set(compact?768:1024,compact?768:1024);sun.shadow.camera.left=-22;sun.shadow.camera.right=22;sun.shadow.camera.top=25;sun.shadow.camera.bottom=-25;sun.shadow.camera.near=1;sun.shadow.camera.far=70;sun.shadow.bias=-.0007;sun.shadow.normalBias=.035;scene.add(sun);
  const fill=new T.DirectionalLight(0xc1e8fa,1.3);fill.position.set(-10,10,-12);scene.add(fill);
  const markerMaterial=new T.MeshBasicMaterial({color:0xe8ca73,transparent:true,opacity:.85,side:T.DoubleSide});
  const marker=new T.Mesh(new T.RingGeometry(.3,.4,32),markerMaterial);marker.rotation.x=-Math.PI/2;marker.position.y=.03;marker.visible=false;scene.add(marker);
  const routeGuide=new T.Line(new T.BufferGeometry(),new T.LineDashedMaterial({color:0xf3d17c,dashSize:.32,gapSize:.22,transparent:true,opacity:.65}));routeGuide.visible=false;scene.add(routeGuide);
  function drawRoute(){routeGuide.geometry.dispose();routeGuide.geometry=new T.BufferGeometry().setFromPoints([position,...path].map(p=>new T.Vector3(p.x,.045,p.z)));routeGuide.computeLineDistances();routeGuide.visible=path.length>0;}
  function disposeWorld(){for(const m of worldMaterials)m.dispose();for(const g of worldGeometries)g.dispose();for(const t of worldTextures)t.dispose();worldMaterials=[];worldGeometries=[];worldTextures=[];scene.remove(world);world=new T.Group();scene.add(world);labelLayer.replaceChildren();labels=[];}
  function room(c){const outdoor=['outdoor','yard'].includes(c.layout),W=bounds.width,D=bounds.depth;
    scene.background=new T.Color(outdoor?0xb5cbd2:0x13242e);scene.fog=new T.Fog(outdoor?0xb5cbd2:0x607e8c,45,105);
    mats={metal:makeMaterial(palette.metal,.3,.7),dark:makeMaterial(palette.dark,.45,.55),body:makeMaterial(palette.body,.42,.3),black:makeMaterial(palette.black,.75,.1),yellow:makeMaterial(palette.yellow,.68,.15),amber:makeMaterial(0xe0a94d,.4,.25),accent:makeMaterial(c.color||0x477f89,.42,.4),glass:makeMaterial(0x315b6b,.16,.6),cyan:makeMaterial(0x4498a9,.15,.85),glow:makeMaterial(0x96f0b9,.3,.2,{emissive:0x6cf7a8,emissiveIntensity:.7})};
    const floorMap=textureCanvas((ctx,w,h)=>{ctx.fillStyle=outdoor?'#718085':'#778d98';ctx.fillRect(0,0,w,h);ctx.strokeStyle=outdoor?'#819095':'#94a5ad';ctx.lineWidth=2;ctx.strokeRect(1,1,w-2,h-2);for(let i=0;i<500;i++){const x=(i*137.53)%w,y=(i*71.17)%h;ctx.fillStyle=i%2?'#ffffff08':'#00000009';ctx.fillRect(x,y,2,2);}},256,256);floorMap.wrapS=floorMap.wrapT=T.RepeatWrapping;floorMap.repeat.set(W/3,D/3);
    const floor=box(world,W,.2,D,0,-.11,0,makeMaterial(0xffffff,.88,.1,{map:floorMap}));floor.userData.ground=true;
    box(world,4.7,.018,D-2,0,.003,0,makeMaterial(outdoor?0x687e7b:0x476870,.8,.12));
    for(const x of [-2.4,2.4])box(world,.08,.025,D-2,x,.015,0,mats.yellow);
    for(let z=-D/2+4;z<D/2-2;z+=4){for(const side of [-1,1]){const stripe=box(world,.085,.025,.7,side*.34,.02,z,mats.body);stripe.rotation.y=side*Math.PI/4;}box(world,.08,.025,1,0,.02,z-.7,mats.body);}
    // Keep decorative architecture outside the walkable envelope, with no hidden props in aisles.
    const wall=makeMaterial(outdoor?0x718d91:0xc4d0d3,.78,.1);
    box(world,W+.3,7,.2,0,3.4,-D/2-.12,wall);
    if(!outdoor){for(const side of [-1,1]){box(world,.2,7,D,side*(W/2+.12),3.4,0,wall);for(let z=-D/2+3;z<D/2-2;z+=4.5){box(world,.05,2.2,3.25,side*(W/2-.012),3.7,z,mats.glass);box(world,.07,.08,3.3,side*(W/2-.05),3.7,z,mats.metal);}}
      for(let z=-D/2+4;z<D/2;z+=6){box(world,W,.18,.18,0,6.6,z,mats.dark);for(const x of [-W*.26,W*.26])box(world,3.5,.065,.35,x,6.46,z,makeMaterial(0xe6f7ff,.2,.1,{emissive:0xc4e6ff,emissiveIntensity:.8}));}
    }else{for(const side of [-1,1]){box(world,.2,.5,D,side*(W/2+.13),.22,0,mats.dark);for(let z=-D/2;z<D/2;z+=4)box(world,.12,2.1,.12,side*(W/2+.13),1,z,mats.metal);}for(let z=-D/2;z<D/2;z+=3)box(world,W,.04,.04,0,6.2,z,mats.dark);}
    for(const side of [-1,1])for(const z of [-D/2+.3,D/2-.3])box(world,.45,6.5,.45,side*(W/2-.1),3.15,z,mats.dark);
    const sign=textureCanvas((ctx,w,h)=>{ctx.fillStyle='#14363f';ctx.fillRect(0,0,w,h);ctx.fillStyle='#c9ecd7';ctx.font='bold 31px sans-serif';ctx.fillText('MACGYVER  /  '+String(c.domainId||'ENGINEERING').toUpperCase(),25,66);ctx.font='20px monospace';ctx.fillStyle='#a9c5c7';ctx.fillText('LEARN  ·  INSPECT  ·  VERIFY',25,113);},1024,160);
    box(world,Math.min(W-3,17),2.1,.04,0,4.5,-D/2+.03,makeMaterial(0xffffff,.6,.1,{map:sign}));
    const portal=box(world,4.5,3.6,.15,0,1.8,-D/2+.14,mats.dark);box(world,3.8,3.1,.05,0,1.55,-D/2+.25,mats.glass);box(world,.08,3.1,.07,0,1.55,-D/2+.3,mats.body);
  }
  // Architectural motifs stay above 5.4 m or beyond the traversable boundary.
  // They therefore cannot become invisible obstacles in the teaching aisles.
  function specialtyArchitecture(c){
    const W=bounds.width,D=bounds.depth,domain=c.domainId;
    const beam=(z,color=mats.accent)=>{box(world,W+.7,.24,.3,0,5.7,z,color);};
    if(['semiconductor','packaging','biomedical','instruments'].includes(domain)){
      for(let z=-D/2+3;z<D/2;z+=5)for(const x of [-W*.27,0,W*.27]){box(world,3.8,.16,2.8,x,6.3,z,mats.body);for(let j=0;j<5;j++)box(world,3.5,.02,.04,x,6.21,z-1+j*.5,mats.dark);}
    }
    if(domain==='computing'){
      for(const side of [-1,1]){pipe(world,[side*W*.28,5.65,-D/2],[side*W*.28,5.65,D/2],.15,side<0?mats.cyan:mats.amber);for(let z=-D/2+3;z<D/2;z+=6){box(world,1.8,.18,3,side*W*.28,5.9,z,mats.dark);}}
      for(let x=-W/2+3;x<W/2;x+=3)screen(world,2.35,1.15,x,5.4,-D/2+.3,1);
    }
    if(c.specialty==='hpc'||c.specialty==='security'){
      const soc=c.specialty==='security';
      const banner=textureCanvas((ctx,w,h)=>{ctx.fillStyle=soc?'#172739':'#153a40';ctx.fillRect(0,0,w,h);ctx.fillStyle='#c3ede4';ctx.font='bold 36px sans-serif';ctx.fillText(soc?'DEFENSIVE SOC / SYNTHETIC EVIDENCE':'HPC CLUSTER / TEACHING MODEL',28,58);ctx.font='22px monospace';ctx.fillText(soc?'OBSERVE  ·  VALIDATE  ·  RECOVER':'COMPUTE  ·  TRANSFER  ·  RESTORE',28,104);},1024,144);
      box(world,Math.min(W-3,18),1.55,.04,0,5.75,-D/2+.4,makeMaterial(0xffffff,.7,.1,{map:banner}));
      if(soc)for(const side of [-1,1])for(let z=-D/2+4;z<D/2-2;z+=6)screen(world,2.5,1.35,side*(W/2-1.4),5.7,z,2);
    }
    if(['underground','rail'].includes(domain)){
      for(let z=-D/2+1;z<D/2;z+=5){beam(z,mats.metal);for(const side of [-1,1])pipe(world,[side*(W/2+.25),0,z],[side*(W/2+.25),5.7,z],.12,mats.metal);}
      if(domain==='rail')for(const x of [-W*.39,W*.39])for(const side of [-1,1])box(world,.08,.025,D-1,x+side*.65,.02,0,mats.metal);
    }
    if(['manufacturing','materials','aerospace','space','automotive','structures'].includes(domain)){
      for(const x of [-W*.38,W*.38])box(world,.35,.35,D,x,6,0,mats.amber);
      for(const z of [-D*.28,D*.28]){beam(z,mats.amber);box(world,2.2,.5,1.1,0,5.7,z,mats.dark);}
    }
    if(['water','marine','environment'].includes(domain)){
      for(const side of [-1,1]){box(world,7,.12,D+12,side*(W/2+4),-.24,0,mats.cyan);for(let z=-D/2;z<D/2;z+=3){pipe(world,[side*(W/2+.18),.4,z],[side*(W/2+.18),1.4,z],.035,mats.body);}pipe(world,[side*(W/2+.18),1.4,-D/2],[side*(W/2+.18),1.4,D/2],.045,mats.body);}
    }
    if(['energy','process'].includes(domain)){
      for(let j=0;j<4;j++)pipe(world,[-W/2-.35,2+j*.6,-D/2],[-W/2-.35,2+j*.6,D/2],.12,j%2?mats.amber:mats.metal);
      for(let z=-D/2+2;z<D/2;z+=7){beam(z,mats.metal);for(const x of [-W*.22,W*.22])pipe(world,[x,5.6,z],[x,5.6,z+5],.18,mats.accent);}
    }
    if(['electronics','megascience'].includes(domain)){
      for(let z=-D/2+2;z<D/2;z+=5){beam(z);for(const side of [-1,1]){box(world,.14,3.6,2.2,side*(W/2-.03),2,z,mats.dark);screen(world,2,1.1,side*(W/2-1.2),5.5,z,1);}}
    }
  }
  function referenceGallery(c,epoch){
    const photos=(c.referencePhotos||[]).slice(0,4),W=bounds.width,D=bounds.depth;
    photos.forEach((photo,i)=>{
      if(!localPhotoPath(photo.src))return;
      const wall=new T.Group(),side=i%2?-1:1;wall.position.set(side*(W/2-.18),0,(i<2?-.27:.27)*D);wall.rotation.y=side<0?Math.PI/2:-Math.PI/2;world.add(wall);
      box(wall,7.3,4.3,.09,0,3.3,0,mats.dark);
      loader.load(photo.src,texture=>{if(disposed||epoch!==configEpoch){texture.dispose();return;}texture.colorSpace=T.SRGBColorSpace;texture.anisotropy=Math.min(renderer.capabilities.getMaxAnisotropy(),4);worldTextures.push(texture);const ratio=(texture.image.width||16)/(texture.image.height||9),w=Math.min(7.1,3.8*ratio),h=w/ratio;const mat=makeMaterial(0xffffff,1,0,{map:texture,emissive:0xffffff,emissiveIntensity:.22});box(wall,w,h,.025,0,3.3,.065,mat).userData.photoId=photo.id;},undefined,()=>{});
      const caption=textureCanvas((ctx,w,h)=>{ctx.fillStyle='#102b32';ctx.fillRect(0,0,w,h);ctx.fillStyle='#d4ebcb';ctx.font='bold 26px sans-serif';ctx.fillText('PHOTOGRAPHIC REFERENCE / '+String(i+1).padStart(2,'0'),20,37);ctx.fillStyle='#b9d2d5';ctx.font='19px sans-serif';const credit=String(photo.author||'')+' · '+String(photo.license||'');ctx.fillText(credit,20,72,w-40);},1024,96);
      box(wall,7.3,.68,.035,0,.77,.065,makeMaterial(0xffffff,1,0,{map:caption,emissive:0xffffff,emissiveIntensity:.2})).userData.photoId=photo.id;
    });
  }
  function domainLandmark(c){
    const W=bounds.width,D=bounds.depth,far=-D/2-5,p=c.domainId;
    if(c.specialty==='communications'){
      for(const side of [-1,1]){pipe(world,[side*(W/2+3),0,far],[side*(W/2+3),12,far],.16,mats.metal);for(let j=0;j<6;j++){box(world,.6,.8,.2,side*(W/2+3),8+j*.55,far,mats.body);pipe(world,[side*(W/2+1),0,far-2],[side*(W/2+3),10,far],.035,mats.metal);}}
      const banner=textureCanvas((ctx,w,h)=>{ctx.fillStyle='#102e3b';ctx.fillRect(0,0,w,h);ctx.fillStyle='#9de8e6';ctx.font='bold 38px sans-serif';ctx.fillText('COMMUNICATIONS / NETWORK TESTBED',24,55);ctx.font='23px monospace';ctx.fillText('SIGNAL  →  LINK  →  PACKET  →  SERVICE',24,105);},1024,144);
      box(world,Math.min(W-3,20),1.7,.05,0,5.9,-D/2+.5,makeMaterial(0xffffff,.8,0,{map:banner}));
    }
    if(['space','aerospace','rail','automotive'].includes(p)){
      // Large translucent service-bay framing is a teaching-space landmark, not survey geometry.
      for(const side of [-1,1])for(let z=-D/2;z<D/2;z+=8){pipe(world,[side*(W/2+.4),0,z],[side*(W/2+.4),9,z],.16,mats.metal);pipe(world,[side*(W/2+.4),9,z],[0,12,z],.16,mats.metal);}
      for(let z=-D/2;z<D/2;z+=8)pipe(world,[0,12,z],[0,12,Math.min(z+8,D/2)],.13,mats.metal);
    }else if(['water','environment','marine'].includes(p)){
      for(const side of [-1,1]){const reservoir=box(world,8,.08,D+18,side*(W/2+6),-.18,0,mats.cyan);reservoir.receiveShadow=false;for(let j=0;j<10;j++)box(world,7,.01,.035,side*(W/2+6),-.12,-D/2+j*D/10,mats.body);}
    }else if(['energy','process','materials'].includes(p)){
      for(let j=0;j<3;j++){cylinder(world,1.4,2.1,8+j*2,-W/2-4-j*4,4+j,far+8*j,mats.metal);cylinder(world,1.5,1.5,.2,-W/2-4-j*4,8+j*2,far+8*j,mats.amber);}
    }else if(p==='structures'){
      const span=new T.Group();span.position.set(0,0,far-4);world.add(span);box(span,W+15,.6,4,0,7,0,mats.metal);for(const x of [-W*.35,W*.35]){box(span,.7,17,.8,x,8.5,0,mats.body);for(let j=1;j<5;j++)for(const side of [-1,1])pipe(span,[x,16,0],[x+side*j*2.6,7.4,0],.045,mats.amber);}
    }else if(p==='underground'){
      for(let z=-D/2;z<D/2;z+=5){const arc=mesh(new T.TorusGeometry(W/2+.8,.16,8,32,Math.PI),mats.metal,world,0,0,z);arc.rotation.z=0;}
    }
  }
  function localPhotoPath(src){return /^assets\/[A-Za-z0-9_./-]+\.(?:jpg|jpeg|png|webp)$/i.test(src||'')&&!src.includes('..');}
  function addPhoto(group,s,epoch){if(!localPhotoPath(s.photoSrc))return;const board=box(group,3.28,1.7,.08,0,4.15,-.05,mats.dark);
    loader.load(s.photoSrc,texture=>{if(disposed||epoch!==configEpoch){texture.dispose();return;}texture.colorSpace=T.SRGBColorSpace;texture.anisotropy=Math.min(renderer.capabilities.getMaxAnisotropy(),4);worldTextures.push(texture);const image=texture.image;const ratio=(image.width||16)/(image.height||9);const w=Math.min(3.12,1.52*ratio),h=w/ratio;const mat=makeMaterial(0xffffff,.8,.0,{map:texture,emissive:0xffffff,emissiveIntensity:.13});box(group,w,h,.025,0,4.15,.005,mat).userData.stationId=s.id;},undefined,()=>{/* Photographic evidence is optional; geometry stays navigable offline. */});
    for(const x of [-1.5,1.5])box(group,.045,1.3,.045,x,3.2,-.05,mats.metal);
    const credit=s.photoCredit||{};
    const plaque=textureCanvas((ctx,W,H)=>{
      ctx.fillStyle='#102a32';ctx.fillRect(0,0,W,H);
      const author=String(credit.author||'Photo reference').replace(/\s+/g,' ').trim();
      const license=String(credit.license||'See image source').replace(/\s+/g,' ').trim();
      let size=30;ctx.font=`${size}px sans-serif`;while(ctx.measureText(author).width>W-48&&size>12){size--;ctx.font=`${size}px sans-serif`;}
      ctx.fillStyle='#e3eee6';ctx.fillText(author,24,53);
      ctx.fillStyle='#a8c6bf';ctx.font='25px sans-serif';ctx.fillText(license,24,105);
    },1024,144);
    box(group,3.28,.46,.035,0,3.05,.015,makeMaterial(0xffffff,.8,.0,{map:plaque,emissive:0xffffff,emissiveIntensity:.12})).userData.stationId=s.id;
  }
  function makeStation(s,i,epoch){const g=new T.Group();g.position.set(s.x,0,s.z);g.rotation.y=s.x<0?Math.PI/2:-Math.PI/2;g.userData.stationId=s.id;world.add(g);machine(g,s.kind,i);addPhoto(g,s,epoch);g.traverse(o=>{if(o.isMesh)o.userData.stationId=s.id;});
    // Painted work bay sits below the equipment and never blocks movement.
    const bay=box(world,4.25,.018,4.4,s.x,.012,s.z,makeMaterial(0x4d6266,.85,.1));for(const z of [-2.18,2.18])box(world,4.25,.022,.055,s.x,.025,s.z+z,mats.yellow);
    const label=document.createElement('button');label.className='walk-station-label';
    label.addEventListener('pointerdown',e=>e.stopPropagation());label.addEventListener('click',e=>{e.stopPropagation();onManual();if(near?.id===s.id)interact();else goToStation(s.id);});labelLayer.append(label);const beacon=mesh(new T.RingGeometry(.32,.41,24),makeMaterial(0xe8c26d,.5,.15,{side:T.DoubleSide}),world,s.approach.x,.04,s.approach.z);beacon.rotation.x=-Math.PI/2;labels.push({element:label,station:s,group:g,beacon,number:i+1});
  }
  function setConfig(next){if(disposed)return;snapCamera=true;const epoch=++configEpoch;config=next||{};completed=new Set();disposeWorld();bounds={width:Math.max(22,config.bounds?.width||30),depth:Math.max(28,config.bounds?.depth||38)};room(config);specialtyArchitecture(config);domainLandmark(config);referenceGallery(config,epoch);avatar.suit.color.set(config.layout==='cleanroom'?0xd7e2e6:0x285e69);avatar.vest.color.set(config.layout==='cleanroom'?0xa5c8d4:0xf3b954);avatar.helmet.color.set(['outdoor','yard'].includes(config.layout)?0xf0c859:0xe8eeee);obstacles=[];stations=(config.stations||[]).map((s,i)=>{const x=Number.isFinite(s.x)?s.x:(i%2?7:-7),z=Number.isFinite(s.z)?s.z:-bounds.depth/2+7+Math.floor(i/2)*8;return {...s,x,z,approach:s.approach||{x:s.approachX??(x-Math.sign(x||1)*2.95),z:s.approachZ??z}};});obstacles=stationObstacles(stations);stations.forEach((s,i)=>makeStation(s,i,epoch));position={x:0,z:bounds.depth/2-4};stopMovement();yaw=heading=0;firstFov=displaySettings.fov;manualLookUntil=0;[pitch,distance]=cameraDefaults[view];near=null;lastNear='';avatar.object.position.set(position.x,0,position.z);avatar.object.rotation.y=0;cameraAim.set(position.x,1.15,position.z);camera.position.set(0,4.3,position.z+6);marker.visible=false;routeGuide.visible=false;onNear(null);updateLabels();onMove(getState());}
  function name(s){return language.startsWith('zh')?s.title||s.titleEn||s.id:s.titleEn||s.title||s.id;}
  function updateLabels(){const W=container.clientWidth||innerWidth,H=container.clientHeight||innerHeight;for(const label of labels){const s=label.station,p=v3.set(s.x,s.photoSrc?5.25:3.35,s.z).project(camera),d=Math.hypot(position.x-s.approach.x,position.z-s.approach.z);const visible=displaySettings.labels&&p.z>-1&&p.z<1&&Math.abs(p.x)<.97&&p.y>-.89&&p.y<.78&&(d<19||s.id===objectiveId||view==='overview');label.element.hidden=!visible;if(!visible)continue;label.element.style.left=((p.x*.5+.5)*W)+'px';label.element.style.top=((-p.y*.5+.5)*H)+'px';label.element.style.opacity=d<16||s.id===objectiveId?'1':'.63';
      label.element.classList.toggle('station-target',s.id===objectiveId);
      label.element.classList.toggle('station-near',near?.id===s.id);
      label.element.classList.toggle('station-done',completed.has(s.id));
      label.element.textContent=`${completed.has(s.id)?'✓':String(label.number).padStart(2,'0')}  ${name(s)} · ${d.toFixed(1)} m`;
      const action=near?.id===s.id?(language.startsWith('zh')?'操作工作站：':'Operate station: '):(language.startsWith('zh')?'走向工作站：':'Walk to station: ');
      label.element.setAttribute('aria-label',action+name(s));}}
  function focusAllowed(target){return !target?.closest?.('input,textarea,select,dialog,[contenteditable]:not([contenteditable=false]),.mentor-panel');}
  function listen(target,type,fn,options){target.addEventListener(type,fn,options);listeners.push(()=>target.removeEventListener(type,fn,options));}
  function clearRoute(){path=[];marker.visible=false;routeGuide.visible=false;}
  function stopMovement(){keys.clear();external={x:0,z:0};velocity={x:0,z:0};clearRoute();pointers.clear();drag=null;lastPinch=0;}
  function keydown(e){if(paused||!focusAllowed(e.target)||e.ctrlKey||e.metaKey||e.altKey)return;const k=e.key.toLowerCase();if(['w','a','s','d','arrowup','arrowdown','arrowleft','arrowright','shift'].includes(k)){e.preventDefault();keys.add(k);clearRoute();onManual();}else if(k==='e'){e.preventDefault();interact();}else if(k==='1')setView('first');else if(k==='2')setView('close');else if(k==='3')setView('follow');else if(k==='4')setView('overview');}
  listen(document,'keydown',keydown);listen(document,'keyup',e=>keys.delete(e.key.toLowerCase()));listen(document,'focusin',e=>{if(!focusAllowed(e.target))stopMovement();});listen(window,'blur',stopMovement);listen(document,'visibilitychange',()=>{if(document.hidden)stopMovement();});
  const canvas=renderer.domElement;
  function coord(e){const r=canvas.getBoundingClientRect();pointer.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);raycaster.setFromCamera(pointer,camera);}
  function clickWorld(e){coord(e);const hits=raycaster.intersectObjects(world.children,true);const hit=hits.find(h=>h.object.userData.photoId||h.object.userData.stationId||h.object.userData.ground);if(!hit)return;onManual();if(hit.object.userData.photoId){stopMovement();onPhoto(hit.object.userData.photoId);return;}if(hit.object.userData.stationId){if(near?.id===hit.object.userData.stationId)interact();else goToStation(hit.object.userData.stationId);return;}path=findPath(position,{x:hit.point.x,z:hit.point.z},bounds,obstacles);if(path.length){marker.position.set(path.at(-1).x,.03,path.at(-1).z);marker.visible=true;drawRoute();}}
  listen(canvas,'pointerdown',e=>{if(paused||e.button>0)return;canvas.focus({preventScroll:true});pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});canvas.setPointerCapture?.(e.pointerId);if(pointers.size===1)drag={id:e.pointerId,x:e.clientX,y:e.clientY,total:0};else{drag=null;const p=[...pointers.values()];lastPinch=Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y);}});
  listen(canvas,'pointermove',e=>{if(document.pointerLockElement===canvas){if(!paused)look(-e.movementX*.003,-e.movementY*.003);return;}const p=pointers.get(e.pointerId);if(!p||paused)return;const dx=e.clientX-p.x,dy=e.clientY-p.y;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pointers.size===2){const q=[...pointers.values()],d=Math.hypot(q[0].x-q[1].x,q[0].y-q[1].y);if(lastPinch>0)zoom(lastPinch/Math.max(d,1));lastPinch=d;
    }else if(drag){
      drag.total+=Math.hypot(dx,dy);
      if(drag.total>=5){look(-dx*.005,(view==='first'?-1:1)*dy*.004);}
    }
  });
  function pointerEnd(e){if(drag?.id===e.pointerId&&drag.total<7&&!paused)clickWorld(e);pointers.delete(e.pointerId);drag=null;lastPinch=0;}
  listen(canvas,'pointerup',pointerEnd);const cancelPointer=e=>{pointers.delete(e.pointerId);drag=null;lastPinch=0;};listen(canvas,'pointercancel',cancelPointer);listen(canvas,'lostpointercapture',cancelPointer);listen(canvas,'wheel',e=>{if(paused)return;e.preventDefault();zoom(Math.exp(clamp(e.deltaY,-150,150)*.0015));},{passive:false});listen(canvas,'contextmenu',e=>e.preventDefault());
  listen(canvas,'webglcontextlost',e=>{e.preventDefault();paused=true;stopMovement();onError(Error(language.startsWith('zh')?'3D 繪圖暫停，請重新開啟場景。':'3D graphics paused. Reopen the scene.'));});
  function look(deltaYaw,deltaPitch){if(paused)return;yaw=angleDelta(0,yaw+(Number(deltaYaw)||0));pitch=clamp(pitch+(Number(deltaPitch)||0),view==='first'?-Math.PI/2+.03:.06,view==='first'?Math.PI/2-.03:1.35);manualLookUntil=performance.now()+2200;}
  async function lockLook(){if(paused||!canvas.requestPointerLock)return false;try{setView('first');await canvas.requestPointerLock();return true;}catch{return false;}}
  listen(document,'pointerlockchange',()=>{container.classList.toggle('pointer-locked',document.pointerLockElement===canvas);if(document.pointerLockElement!==canvas)stopMovement();});
  function setView(next){if(!Object.hasOwn(cameraDefaults,next))return;view=next;[pitch,distance]=cameraDefaults[next];firstFov=displaySettings.fov;avatar.object.visible=next!=='first';onView(view);onMove(getState());}
  function zoom(multiplier){
    if(view==='first')firstFov=clamp(firstFov*multiplier,42,90);
    else distance=clamp(distance*multiplier,view==='close'?2.8:view==='overview'?8:3.8,view==='close'?7:18);
  }
  function recenter(){yaw=heading;[pitch,distance]=cameraDefaults[view];firstFov=displaySettings.fov;manualLookUntil=0;onMove(getState());}
  function setObjective(id){objectiveId=id;updateLabels();}
  function setMove(x,z){external=normalizeInput(Number(x)||0,Number(z)||0);if(external.x||external.z){clearRoute();onManual();}}
  function goToStation(id){const s=stations.find(s=>s.id===id);if(!s)return false;velocity={x:0,z:0};path=findPath(position,s.approach,bounds,obstacles);if(path.length){marker.position.set(s.approach.x,.03,s.approach.z);marker.visible=true;drawRoute();return true;}return Math.hypot(position.x-s.approach.x,position.z-s.approach.z)<.5;}
  function interact(){if(paused)return false;const current=nearestStation(position,stations,2.25);if(!current)return false;stopMovement();onInteract(current);return true;}
  function setPosition(saved){if(!saved||!Number.isFinite(saved.x)||!Number.isFinite(saved.z))return false;const next={x:clamp(saved.x,-bounds.width/2+.4,bounds.width/2-.4),z:clamp(saved.z,-bounds.depth/2+.4,bounds.depth/2-.4)};if(!isWalkable(next.x,next.z,bounds,obstacles))return false;snapCamera=true;stopMovement();position=next;if(Number.isFinite(saved.yaw))yaw=heading=angleDelta(0,saved.yaw);avatar.object.rotation.y=heading;avatar.object.position.set(position.x,0,position.z);cameraAim.set(position.x,view==='first'?1.67:1.25,position.z);near=nearestStation(position,stations,2.25);lastNear=near?.id||'';onNear(near);onMove(getState());return true;}
  function resetPosition(){heading=0;recenter();setPosition({x:0,z:bounds.depth/2-4,yaw:0});}
  function setCompleted(ids){completed=new Set(Array.isArray(ids)?ids:[]);for(const l of labels){l.beacon.material.color.set(completed.has(l.station.id)?0x83e8ae:0xe8c26d);l.beacon.material.emissive.set(completed.has(l.station.id)?0x33774b:0x000000);l.beacon.material.emissiveIntensity=.3;}updateLabels();}
  function getState(){return {x:position.x,z:position.z,yaw,moving:Math.hypot(external.x,external.z)>0||keys.size>0||path.length>0,view,nearId:near?.id||null,pathRemaining:path.length,domainId:config?.domainId,renderer:'webgl',speedMps,fps:frameRate,fov:camera.fov,quality:displaySettings.quality};}
  function resize(){if(disposed)return;const w=container.clientWidth||innerWidth,h=container.clientHeight||innerHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}
  listen(window,'resize',resize);
  function animate(){
    if(disposed)return;
    frame=requestAnimationFrame(animate);
    const elapsed=clock.getDelta(),dt=Math.min(elapsed,.10);
    if(!paused&&!document.hidden&&elapsed>0&&elapsed<.25){frameSeconds+=elapsed;frameSamples++;if(frameSeconds>=3){frameRate=frameSamples/frameSeconds;if(displaySettings.quality==='auto'){const next=frameRate<34?Math.max(.75,adaptiveRatio-.15):frameRate>56?Math.min(compact?1.35:1.7,adaptiveRatio+.1):adaptiveRatio;if(Math.abs(next-adaptiveRatio)>.01){adaptiveRatio=next;renderer.setPixelRatio(adaptiveRatio);renderer.shadowMap.enabled=adaptiveRatio>1;resize();}}frameSeconds=0;frameSamples=0;}}
    let moved=0;
    if(!paused){
      const input={x:external.x,z:external.z};
      if(keys.has('w')||keys.has('arrowup'))input.z-=1;
      if(keys.has('s')||keys.has('arrowdown'))input.z+=1;
      if(keys.has('a')||keys.has('arrowleft'))input.x-=1;
      if(keys.has('d')||keys.has('arrowright'))input.x+=1;
      let delta={x:0,z:0};
      if(path.length){
        while(path.length&&Math.hypot(path[0].x-position.x,path[0].z-position.z)<.12)path.shift();
        if(path.length){
          const dx=path[0].x-position.x,dz=path[0].z-position.z,len=Math.hypot(dx,dz);
          const step=Math.min(len,3.35*displaySettings.speed*dt);
          delta={x:dx/len*step,z:dz/len*step};
          if(view!=='overview'&&performance.now()>manualLookUntil){
            yaw=angleDelta(0,yaw+angleDelta(yaw,Math.atan2(-dx,-dz))*(1-Math.exp(-dt*3.5)));
          }
        }else clearRoute();
      }else{
        const dir=cameraRelativeMove(input,yaw),speed=(keys.has('shift')?5.3:3.2)*displaySettings.speed;
        velocity=approachVelocity(velocity,{x:dir.x*speed,z:dir.z*speed},dt);
        delta={x:velocity.x*dt,z:velocity.z*dt};
      }
      const previous=position;
      position=moveWithCollisions(position,delta,bounds,obstacles);
      moved=Math.hypot(position.x-previous.x,position.z-previous.z);
      if(moved>.0001){
        heading=Math.atan2(previous.x-position.x,previous.z-position.z);
        avatar.object.rotation.y+=angleDelta(avatar.object.rotation.y,heading)*(1-Math.exp(-dt*13));
        walkTime+=moved*4.2;
      }
      avatar.object.position.set(position.x,0,position.z);
      for(const l of avatar.limbs){
        const swing=moved>.001&&!reducedMotion.matches?Math.sin(walkTime)*.57*l.side:0;
        l.leg.rotation.x=T.MathUtils.lerp(l.leg.rotation.x,swing,.3);
        l.arm.rotation.x=T.MathUtils.lerp(l.arm.rotation.x,-swing*.8,.3);
      }
      near=nearestStation(position,stations,2.25);
      if((near?.id||'')!==lastNear){lastNear=near?.id||'';onNear(near);}
      if(!reducedMotion.matches)for(const l of labels)if(l.group.userData.rotor)l.group.userData.rotor.rotation.z+=dt*.3;
    }
    speedMps=dt>0?moved/dt:0;
    const first=view==='first',fieldOfView=first?firstFov:displaySettings.fov;
    if(Math.abs(camera.fov-fieldOfView)>.08){
      camera.fov=T.MathUtils.lerp(camera.fov,fieldOfView,1-Math.exp(-dt*16));
      camera.updateProjectionMatrix();
    }
    const eye=first?1.67:1.25;
    cameraAnchor.set(position.x,eye,position.z);
    if(first){
      camera.position.copy(cameraAnchor);
      v3.set(-Math.sin(yaw)*Math.cos(pitch),Math.sin(pitch),-Math.cos(yaw)*Math.cos(pitch));
      camera.lookAt(lookAt.copy(camera.position).add(v3));
    }else{
      const side=view==='close'?.68:0;
      cameraAim.lerp(lookAt.set(position.x,eye,position.z),reducedMotion.matches?1:1-Math.exp(-dt*12));
      cameraWanted.set(
        position.x+Math.sin(yaw)*distance*Math.cos(pitch)+Math.cos(yaw)*side,
        eye+Math.sin(pitch)*distance,
        position.z+Math.cos(yaw)*distance*Math.cos(pitch)-Math.sin(yaw)*side
      );
      cameraWanted.x=clamp(cameraWanted.x,-bounds.width/2+.32,bounds.width/2-.32);
      cameraWanted.z=clamp(cameraWanted.z,-bounds.depth/2+.32,bounds.depth/2-.32);
      camera.position.lerp(cameraWanted,snapCamera||reducedMotion.matches?1:1-Math.exp(-dt*12));
      const clearance=cameraClearFraction(cameraAnchor,camera.position,obstacles);
      if(clearance<1)camera.position.lerpVectors(cameraAnchor,camera.position,clearance);
      camera.lookAt(cameraAim);
    }
    snapCamera=false;
    // A fixed capture can use its own GPU/CPU while the walking world is paused.
    if(!document.body.classList.contains('media-open'))renderer.render(scene,camera);
    if(performance.now()-lastEmit>110){
      updateLabels();onMove({...getState(),moving:moved>.001});lastEmit=performance.now();
    }
  }
  function setDisplaySettings(value){
    displaySettings=normalizeWalkSettings(value);firstFov=displaySettings.fov;
    adaptiveRatio=displaySettings.quality==='low'?Math.min(devicePixelRatio||1,.85):displaySettings.quality==='high'?Math.min(devicePixelRatio||1,compact?1.5:2):Math.min(devicePixelRatio||1,compact?1.1:1.4);
    renderer.setPixelRatio(adaptiveRatio);renderer.shadowMap.enabled=displaySettings.quality!=='low'&&adaptiveRatio>1;resize();updateLabels();
  }
  function setPaused(value){paused=!!value;if(paused){stopMovement();if(document.pointerLockElement===canvas)document.exitPointerLock?.();}}
  function setLanguage(value){language=String(value||'en');canvas.setAttribute('aria-label',language.startsWith('zh')?'可行走工程場景，WASD 或方向鍵移動，E 操作':'Walkable engineering scene. WASD or arrows move. E interacts.');updateLabels();onNear(near);}
  function dispose(){if(disposed)return;disposed=true;configEpoch++;cancelAnimationFrame(frame);stopMovement();listeners.forEach(f=>f());disposeWorld();avatar.dispose();marker.geometry.dispose();markerMaterial.dispose();routeGuide.geometry.dispose();routeGuide.material.dispose();renderer.dispose();renderer.forceContextLoss();canvas.remove();labelLayer.remove();}
  setConfig(config);resize();animate();
  return {setConfig,setView,setMove,goToStation,interact,resize,dispose,getState,setPaused,setLanguage,setPosition,resetPosition,setCompleted,setObjective,recenter,look,lockLook,setDisplaySettings,stop:stopMovement};
}
