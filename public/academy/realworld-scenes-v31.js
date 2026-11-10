/* V31 educational scene geometry. All dimensions below are illustrative metres,
   not an as-built reconstruction of any named site. No remote dependencies. */
(function(root){'use strict';
const profiles={
semiconductor:{name:['潔淨室與晶圓製程','Cleanroom and wafer processing'],accent:0x63d6d1,models:['cleanroom','wafer','robot']},
packaging:{name:['封裝與光學量測室','Packaging and optical metrology'],accent:0xb1a5f1,models:['chip','laser','robot']},
electronics:{name:['電路與功率實驗室','Circuit and power laboratory'],accent:0xefc466,models:['board','transformer','scope']},
computing:{name:['資料中心與網路機房','Data centre and network room'],accent:0x7ac5f0,models:['racks','racks','cooling']},
instruments:{name:['精密光學與量測室','Precision optics and metrology'],accent:0x9ac9d0,models:['laser','scope','dish']},
structures:{name:['橋梁與結構試驗場','Bridge and structural test yard'],accent:0xea9d6e,models:['bridge','tower','frame']},
underground:{name:['隧道與地下工程','Tunnel and underground works'],accent:0xd7ba7c,models:['tunnel','cutter','conveyor']},
water:{name:['水工與泵浦試驗場','Hydraulic and pump test yard'],accent:0x71d1e1,models:['dam','pump','tank']},
rail:{name:['鐵道維修與運轉場','Rail maintenance and operations'],accent:0xd0d8de,models:['train','gantry','transformer']},
environment:{name:['環境監測與處理廠','Environmental monitoring and treatment'],accent:0x8cd2a0,models:['clarifier','filter','tank']},
aerospace:{name:['航空維修與風洞','Aircraft maintenance and wind tunnel'],accent:0x8fc8eb,models:['plane','tunnel','engine']},
marine:{name:['海事與船舶工程','Marine and ship engineering'],accent:0x6ec9d7,models:['ship','crane','pump']},
automotive:{name:['車輛與電驅測試場','Vehicle and electric-drive testing'],accent:0xe6a066,models:['car','charger','robot']},
space:{name:['發射與航太整合場','Launch and space integration'],accent:0xe0e6e9,models:['rocket','dish','gantry']},
manufacturing:{name:['製造與自動化產線','Manufacturing and automation line'],accent:0xf0b86c,models:['robot','conveyor','gantry']},
energy:{name:['能源轉換與電網','Energy conversion and grids'],accent:0x85cbb5,models:['turbine','solar','transformer']},
materials:{name:['材料與資源工程','Materials and resources engineering'],accent:0xd2af79,models:['furnace','mill','conveyor']},
biomedical:{name:['生醫研究與儀器室','Biomedical research and instrumentation'],accent:0x83d4cd,models:['scanner','cleanroom','scope']},
process:{name:['製程與公用系統','Process and utility systems'],accent:0xdba179,models:['column','tank','pump']},
megascience:{name:['大型科學與探測設施','Large scientific and detector facilities'],accent:0x94afe7,models:['accelerator','dish','laser']},
oil:{name:['海陸油氣工程教學場','Oilfield engineering teaching site'],accent:0xe4b568,models:['derrick','pumpjack','separator']},
gas:{name:['天然氣與 LNG 工程教學場','Natural gas and LNG teaching site'],accent:0x80c7dc,models:['lng','compressor','pipeline']},
mine:{name:['採礦與選礦工程教學場','Mining and mineral-processing teaching site'],accent:0xd3ac78,models:['mine','truck','conveyor']}
};
function validInputs(values,bounds){for(const [key,value] of Object.entries(values)){if(!Number.isFinite(value))return false;const b=bounds?.[key];if(!b)continue;if(Number.isFinite(b.min)&&(b.exclusiveMin?value<=b.min:value<b.min))return false;if(Number.isFinite(b.max)&&value>b.max)return false;if(b.integer&&!Number.isInteger(value))return false;}return true;}
function intersects(x,z,r,b){return x+r>b.x-b.w/2&&x-r<b.x+b.w/2&&z+r>b.z-b.d/2&&z-r<b.z+b.d/2;}
function move(x,z,dx,dz,boxes,r=.45){let nx=x+dx,nz=z+dz;for(const b of boxes)if(intersects(nx,z,r,b))nx=x;for(const b of boxes)if(intersects(nx,nz,r,b))nz=z;return {x:nx,z:nz};}
function create(T,domain,kind){
 const profile=profiles[kind]||profiles[domain]||profiles.materials,root=new T.Group(),obstacles=[],anim=[];root.name='V31 instructional geometry';
 const mats={};function mat(c){return mats[c]||(mats[c]=new T.MeshLambertMaterial({color:c}));}
 function box(g,x,y,z,w,h,d,c=0x526975){const m=new T.Mesh(new T.BoxGeometry(w,h,d),mat(c));m.position.set(x,y,z);g.add(m);return m;}
 function cyl(g,x,y,z,r,h,c=0xa8b8c1,r2=r){const m=new T.Mesh(new T.CylinderGeometry(r2,r,h,12),mat(c));m.position.set(x,y,z);g.add(m);return m;}
 function beam(g,a,b,r,c=0x718b96){const aa=new T.Vector3(...a),bb=new T.Vector3(...b),v=bb.clone().sub(aa),m=cyl(g,0,0,0,r,v.length(),c);m.position.copy(aa.add(bb).multiplyScalar(.5));m.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),v.normalize());return m;}
 function torus(g,x,y,z,r,t,c=0xb1c2c9){const m=new T.Mesh(new T.TorusGeometry(r,t,6,24),mat(c));m.position.set(x,y,z);g.add(m);return m;}
 const white=0xd6e0e4,dark=0x263d49,yellow=profile.accent,steel=0x7b959f,blue=0x317a96;
 function model(type,x,z,angle=0){
  const g=new T.Group();g.position.set(x,0,z);g.rotation.y=angle;root.add(g);let w=14,d=12;
  box(g,0,.18,0,16,.36,15,0x334e5b);
  const tank=(tx,tz,r=3,h=7)=>{cyl(g,tx,h/2,tz,r,h,white);cyl(g,tx,h+.15,tz,r+.15,.3,yellow);for(let i=0;i<3;i++)cyl(g,tx,1.6+i*2.2,tz,r+.03,.08,steel);};
  const frame=(h=12)=>{for(const a of [-1,1])for(const b of [-1,1])beam(g,[a*5,0,b*4],[a*3,h,b*2],.22,steel);for(let j=1;j<=3;j++){const yy=h*j/3;box(g,0,yy,0,10-4*j/3,.3,8-4*j/3,yellow);}};
  if(type==='racks'){for(let i=0;i<4;i++){box(g,(i-1.5)*3,4,0,2.2,8,4,dark);for(let j=0;j<7;j++){box(g,(i-1.5)*3,1+j,2.02,1.8,.68,.06,steel);box(g,(i-1.5)*3+.65,1+j,2.08,.12,.13,.08,0x65e9b3);}}}
  else if(type==='cleanroom'){box(g,0,4,-3,13,8,2,white);for(const q of [-4,0,4]){box(g,q,3,1,3.5,6,5,white);box(g,q,4,3.53,2.8,2.7,.1,blue);cyl(g,q,7,1,1,1,steel);}box(g,0,8.5,0,15,1,10,steel);}
  else if(type==='wafer'||type==='chip'||type==='board'){box(g,0,1,0,12,2,10,steel);if(type==='wafer'){const wafer=cyl(g,0,2.3,0,4.2,.35,0x536baa);for(let a=-3;a<=3;a++)for(let b=-3;b<=3;b++)if(a*a+b*b<13)box(g,a,2.5,b,.7,.04,.7,0xa7b7ef);}else{box(g,0,2.3,0,10,.3,8,0x286854);for(let i=0;i<12;i++)box(g,(i%4-1.5)*2.3,2.9,(Math.floor(i/4)-1)*2.3,1.3,1,1.3,dark);}}
  else if(type==='laser'||type==='scope'){box(g,0,2,0,12,.6,9,steel);for(const a of [-1,1])for(const b of [-1,1])box(g,a*5,1,b*3.5,.6,2,.6,dark);for(let i=0;i<4;i++){cyl(g,i*2-3,3,0,.5,1.4,white);box(g,i*2-3,4,0,1.5,1.2,.3,blue);}beam(g,[-5,3.5,0],[5,3.5,0],.06,0xff665e);}
  else if(type==='robot'){for(const x0 of [-4,4]){cyl(g,x0,1,0,1.8,2,dark);beam(g,[x0,2,0],[x0*.55,6,-1],.7,yellow);cyl(g,x0*.55,6,-1,.85,.8,steel);beam(g,[x0*.55,6,-1],[0,7,2],.5,yellow);box(g,0,6.5,2,1,.8,1,dark);}box(g,0,1.3,3,13,1,3,steel);}
  else if(type==='tower'||type==='derrick'||type==='gantry'||type==='frame'){frame(type==='derrick'?22:14);if(type==='derrick')beam(g,[0,0,0],[0,23,0],.23,dark);else{box(g,0,14,0,12,1,5,yellow);beam(g,[1,14,1],[1,5,1],.07,dark);box(g,1,4,1,3,2,3,steel);}}
  else if(type==='turbine'){cyl(g,0,10,0,.55,20,white,.35);const hub=new T.Group();hub.position.set(0,20,.8);g.add(hub);cyl(hub,0,0,0,.9,1.2,yellow);for(let k=0;k<3;k++){const blade=box(hub,0,4.7,0,.7,9,.2,white);blade.position.set(Math.sin(k*2*Math.PI/3)*4.7,Math.cos(k*2*Math.PI/3)*4.7,0);blade.rotation.z=-k*2*Math.PI/3;}anim.push({group:hub,axis:'z',speed:.35});}
  else if(type==='solar'){for(let j=0;j<3;j++){const p=box(g,0,1.7+j*.05,(j-1)*4,12,.18,3,0x315e91);p.rotation.x=-.3;for(let i=0;i<5;i++)box(g,(i-2)*2.3,1.1,(j-1)*4,.13,2,.13,steel);}}
  else if(type==='transformer'||type==='cooling'){box(g,0,3,0,7,6,7,steel);for(let i=-5;i<=5;i++)box(g,i*.7,3,3.7,.2,5,.8,dark);for(const x0 of [-2,0,2]){cyl(g,x0,7,0,.45,2.5,yellow);for(let j=0;j<4;j++)cyl(g,x0,6.3+j*.5,0,.7,.1,white);}}
  else if(type==='tank'||type==='lng'){tank(-3.8,0,type==='lng'?3.4:3,8);tank(3.8,0,type==='lng'?3.4:3,8);beam(g,[-6,1,5],[6,1,5],.35,blue);for(const q of [-3.8,3.8])beam(g,[q,1,5],[q,1,1],.35,blue);}
  else if(type==='pump'||type==='compressor'||type==='separator'){for(const q of [-3.5,3.5]){const m=cyl(g,q,3,0,1.6,7,white);m.rotation.x=Math.PI/2;box(g,q,1,0,3,.8,8,steel);cyl(g,q,5,-2,.28,3,yellow);}beam(g,[-6,2,5],[6,2,5],.35,blue);}
  else if(type==='pipeline'){for(const zz of [-3,0,3]){beam(g,[-7,3,zz],[7,3,zz],.65,white);for(const xx of [-5,5])box(g,xx,1.5,zz,1,3,1,steel);const v=torus(g,0,4.3,zz,1,.15,0xcc6754);v.rotation.x=Math.PI/2;}}
  else if(type==='column'||type==='furnace'){for(const q of [-3.6,3.6]){cyl(g,q,7,0,2.1,14,white);for(let i=0;i<4;i++)cyl(g,q,2+i*3.3,0,2.4,.25,yellow);beam(g,[q,1,0],[q,1,6],.5,blue);}box(g,0,3,5,4,4,3,steel);}
  else if(type==='conveyor'||type==='mill'){box(g,0,2,0,14,.7,4,dark);for(let i=-6;i<=6;i+=2){const roller=cyl(g,i,2.5,0,.45,4,steel);roller.rotation.x=Math.PI/2;box(g,i,1,0,.4,2,4,steel);}for(let i=-4;i<=4;i+=3)box(g,i,3.1,0,1.4,1,1.2,yellow);if(type==='mill'){const m=cyl(g,0,5,0,3,8,white);m.rotation.z=Math.PI/2;}}
  else if(type==='bridge'){w=22;box(g,0,8,0,22,1,6,steel);for(const xx of [-8,8]){box(g,xx,8,0,1,16,1,yellow);beam(g,[xx,16,0],[-11,8,-2],.1,white);beam(g,[xx,16,0],[11,8,2],.1,white);}for(let i=-10;i<=10;i+=2)box(g,i,8.55,0,.7,.05,.2,white);}
  else if(type==='tunnel'||type==='cutter'){const ring=torus(g,0,5,0,4.7,1,steel);if(type==='tunnel'){for(let i=1;i<5;i++)torus(g,0,5,-i*2,4.7,.55,white);}else{const wheel=new T.Group();wheel.position.set(0,5,0);g.add(wheel);for(let i=0;i<8;i++){const a=i*Math.PI/4;beam(wheel,[0,0,0],[Math.sin(a)*4,Math.cos(a)*4,0],.2,yellow);}anim.push({group:wheel,axis:'z',speed:.2});}}
  else if(type==='dam'){box(g,0,6,0,14,12,5,steel);for(let i=-4;i<=4;i+=4){box(g,i,5,2.6,2.5,8,.2,blue);box(g,i,11,3,3,.6,3,white);}box(g,0,.45,6,16,.1,5,0x3f899e);}
  else if(type==='train'){box(g,0,3,0,13,4,4,white);box(g,0,3.7,2.02,11,1.5,.1,blue);for(const q of [-4,4])for(const zz of [-2,2]){const m=cyl(g,q,1,zz,.8,.4,dark);m.rotation.x=Math.PI/2;}for(const zz of [-1.6,1.6])beam(g,[-8,.4,zz],[8,.4,zz],.16,steel);}
  else if(type==='plane'){const fus=cyl(g,0,4,0,1.5,14,white);fus.rotation.x=Math.PI/2;box(g,0,3.8,0,18,.3,3,steel);box(g,0,4,-6,7,.3,2,steel);box(g,0,6,-6,.4,4,2,yellow);for(const q of [-5,5]){const eng=cyl(g,q,2.7,1,1,4,dark);eng.rotation.x=Math.PI/2;}}
  else if(type==='engine'){const a=cyl(g,0,4,0,3.2,9,steel);a.rotation.x=Math.PI/2;torus(g,0,4,4.6,3,.4,white);for(let i=0;i<10;i++){const aa=i*Math.PI/5;beam(g,[0,4,4.7],[Math.sin(aa)*2.5,4+Math.cos(aa)*2.5,4.7],.15,yellow);}}
  else if(type==='ship'){box(g,0,2,0,8,4,15,blue);box(g,0,4.2,0,8,.4,15,white);box(g,0,6,-4,5,4,5,white);beam(g,[0,6,-4],[0,13,-4],.2,steel);for(let i=0;i<4;i++)box(g,(i%2-.5)*3,5,(Math.floor(i/2)-.5)*4+2,2.5,2,3,yellow);}
  else if(type==='crane'){box(g,0,6,0,1,12,1,yellow);beam(g,[0,12,0],[7,15,0],.3,yellow);beam(g,[7,15,0],[7,5,0],.05,dark);box(g,0,3,0,5,2,5,steel);}
  else if(type==='car'||type==='truck'){box(g,0,2,0,6,2,11,yellow);box(g,0,4,2,5,2.5,4,white);box(g,0,4,4.1,4,1.6,.1,blue);for(const q of [-3,3])for(const zz of [-3.5,3.5]){const a=cyl(g,q,1.5,zz,1.5,.8,dark);a.rotation.z=Math.PI/2;}if(type==='truck')box(g,0,4,-2.5,6,2,5.5,steel);}
  else if(type==='charger'){for(const q of [-4,0,4]){box(g,q,3,0,2,6,2,white);box(g,q,4,1.05,1.4,1.5,.1,blue);beam(g,[q+.8,4,1],[q+1.7,1,1],.1,dark);}}
  else if(type==='rocket'){cyl(g,0,8,0,1.6,16,white);cyl(g,0,17.5,0,1.6,3,white,0);for(const q of [-1,1])box(g,q*2,2,0,2,4,.4,yellow);box(g,0,.7,0,8,1.4,8,steel);}
  else if(type==='dish'){cyl(g,0,3,0,.8,6,steel);const dish=new T.Mesh(new T.SphereGeometry(5,16,8,0,Math.PI*2,0,Math.PI*.35),new T.MeshLambertMaterial({color:white,side:T.DoubleSide}));dish.rotation.x=-.7;dish.position.set(0,6,0);g.add(dish);beam(g,[0,6,0],[0,11,3],.14,yellow);}
  else if(type==='scanner'){const ring=torus(g,0,5,0,4,1.7,white);box(g,0,2,4,3,1,9,steel);box(g,0,2.65,4,2.5,.3,8,blue);}
  else if(type==='accelerator'){const ring=torus(g,0,3,0,5,1.3,blue);ring.rotation.x=Math.PI/2;for(let i=0;i<8;i++){const a=i*Math.PI/4;box(g,Math.cos(a)*5,1.2,Math.sin(a)*5,1,2.4,1,steel);}}
  else if(type==='clarifier'||type==='filter'){cyl(g,0,1.5,0,6,3,steel);cyl(g,0,3.05,0,5.6,.08,0x5897a0);beam(g,[-6,3.5,0],[6,3.5,0],.25,white);cyl(g,0,3.8,0,.8,1.5,yellow);}
  else if(type==='pumpjack'){box(g,0,3,0,3,6,3,steel);const walk=new T.Group();walk.position.set(0,6,0);g.add(walk);box(walk,0,0,0,11,1,1.2,yellow);box(walk,5,-1.2,0,1,3,2,yellow);beam(g,[5,5,0],[5,.2,0],.1,white);cyl(g,-4,2,0,1.5,2,dark);anim.push({group:walk,axis:'z',speed:.0,sway:true});}
  else if(type==='mine'){for(let i=0;i<4;i++){box(g,0,i*1.6,0,16-i*3,1.6,14-i*2.5,0x877259);}for(let i=0;i<5;i++)box(g,-6+i*2.5,1.3+i,5-i*1.5,2.5,.25,3.4,yellow);}
  obstacles.push({x,z,w,d});return g;
 }
 // Wide unobstructed approach to four workstations; equipment is kept outside the aisle.
 box(root,0,-.12,-15,86,.2,110,0x283e48);box(root,0,.02,-10,12,.04,90,0x405967);
 for(const x of [-7,7])box(root,x,.06,-10,.15,.04,90,0xd1b65e);
 for(let z=-45;z<33;z+=8)box(root,0,.07,z,.18,.04,3,0x95afb8);
 for(const x of [-39,39])for(const z of [-45,-15,15]){cyl(root,x,5,z,.18,10,steel);box(root,x,10,z,4,.3,1,white);}
 model(profile.models[0],-23,-18,0.25);model(profile.models[1],23,-20,-.25);model(profile.models[2],-23,-48,.1);model(profile.models[1],23,-50,-.2);
 box(root,0,8,-61,74,1,1.2,yellow);for(const x of [-36,36])box(root,x,4,-61,.8,8,.8,steel);
 // Low kerbs mark the exercise zone; no perimeter wall traps the learner.
 for(const x of [-42,42])box(root,x,.35,-15,.7,.7,110,0x657b80);
 return {group:root,obstacles,animations:anim,profile};
}
/* CPU renderer for browsers where WebGL creation fails. Uses actual projected
   teaching geometry and the same camera, with flat shading and a limited pixel
   budget. It is a compatibility mode, not a photorealistic GPU renderer. */
function canvasRenderer(T){
 const canvas=document.createElement('canvas'),ctx=canvas.getContext('2d',{alpha:false});let width=1,height=1,ratio=1,last=0;
 const renderer={domElement:canvas,isSoftware:true,capabilities:{getMaxAnisotropy:()=>1},setPixelRatio(v){ratio=Math.min(v,1.2);},setSize(w,h){width=w;height=h;canvas.width=Math.round(w*ratio);canvas.height=Math.round(h*ratio);canvas.style.width=w+'px';canvas.style.height=h+'px';},render(scene,camera){
  const now=performance.now();if(now-last<45)return;last=now;scene.updateMatrixWorld(true);camera.updateMatrixWorld(true);camera.matrixWorldInverse.copy(camera.matrixWorld).invert();
  ctx.setTransform(ratio,0,0,ratio,0,0);const sky=ctx.createLinearGradient(0,0,0,height);sky.addColorStop(0,'#7297ad');sky.addColorStop(.5,'#c0d2d8');sky.addColorStop(1,'#243e4a');ctx.fillStyle=sky;ctx.fillRect(0,0,width,height);
  const view=new T.Matrix4().multiplyMatrices(camera.projectionMatrix,camera.matrixWorldInverse),faces=[],sprites=[];
  function project(v){const a=new T.Vector4(v.x,v.y,v.z,1).applyMatrix4(view);return {x:(a.x/a.w*.5+.5)*width,y:(-.5*a.y/a.w+.5)*height,z:a.w,clip:a.z/a.w};}
  scene.traverseVisible(o=>{
   if(o.isSprite){const p=new T.Vector3().setFromMatrixPosition(o.matrixWorld),q=project(p),scale=new T.Vector3();o.getWorldScale(scale);if(q.z>.1&&o.material?.map?.image)sprites.push({q,image:o.material.map.image,w:scale.x*height/(2*Math.tan(camera.fov*Math.PI/360)*q.z),h:scale.y*height/(2*Math.tan(camera.fov*Math.PI/360)*q.z)});return;}
   if(!o.isMesh||o.userData?.softwareIgnore||!o.geometry?.attributes?.position)return;const geom=o.geometry,attr=geom.attributes.position,uv=geom.attributes.uv,index=geom.index,mat=Array.isArray(o.material)?o.material[0]:o.material;if(!mat||mat.opacity===0)return;
   if(!geom.boundingSphere)geom.computeBoundingSphere();const centre=geom.boundingSphere.center.clone().applyMatrix4(o.matrixWorld),cq=project(centre),worldScale=new T.Vector3();o.getWorldScale(worldScale);const radius=geom.boundingSphere.radius*Math.max(worldScale.x,worldScale.y,worldScale.z);if(cq.z+radius<.18||cq.z-radius>220)return;
   const coords=[],mvp=new T.Matrix4().multiplyMatrices(view,o.matrixWorld).elements;for(let i=0;i<attr.count;i++){const x=attr.getX(i),y=attr.getY(i),z=attr.getZ(i),w=mvp[3]*x+mvp[7]*y+mvp[11]*z+mvp[15];coords.push({x:((mvp[0]*x+mvp[4]*y+mvp[8]*z+mvp[12])/w*.5+.5)*width,y:(-.5*(mvp[1]*x+mvp[5]*y+mvp[9]*z+mvp[13])/w+.5)*height,z:w});}
   const normalMatrix=new T.Matrix3().getNormalMatrix(o.matrixWorld),normals=geom.attributes.normal,sun=new T.Vector3(-.4,.8,.4).normalize(),normal=new T.Vector3();
   const size=index?index.count:attr.count,base=mat.color||new T.Color(0x80949c),image=mat.map?.image;
   for(let j=0;j<size;j+=3){const ids=index?[index.getX(j),index.getX(j+1),index.getX(j+2)]:[j,j+1,j+2],a=coords[ids[0]],b=coords[ids[1]],c=coords[ids[2]];if(!a||!b||!c||Math.min(a.z,b.z,c.z)<.18)continue;if(Math.max(a.x,b.x,c.x)<0||Math.min(a.x,b.x,c.x)>width||Math.max(a.y,b.y,c.y)<0||Math.min(a.y,b.y,c.y)>height)continue;
    const signed=(b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x);if(mat.side!==T.DoubleSide&&((mat.side===T.BackSide&&signed<0)||(mat.side!==T.BackSide&&signed>0)))continue;
    const light=normals?(.48+.52*Math.max(0,normal.fromBufferAttribute(normals,ids[0]).applyMatrix3(normalMatrix).normalize().dot(sun))):.75;
    const color=`rgb(${Math.round(Math.sqrt(base.r)*255*light)},${Math.round(Math.sqrt(base.g)*255*light)},${Math.round(Math.sqrt(base.b)*255*light)})`;
    faces.push({a,b,c,z:(a.z+b.z+c.z)/3,color,alpha:mat.transparent?mat.opacity:1,image:uv&&image&&image.width&&image.height?image:null,uv:uv?ids.map(i=>[uv.getX(i),1-uv.getY(i)]):null});
   }
  });
  faces.sort((a,b)=>b.z-a.z);
  for(const f of faces){const {a,b,c}=f;ctx.globalAlpha=f.alpha;ctx.fillStyle=f.color;const cx0=(a.x+b.x+c.x)/3,cy0=(a.y+b.y+c.y)/3,expand=p=>{const dx=p.x-cx0,dy=p.y-cy0,l=Math.hypot(dx,dy)||1;return {x:p.x+dx/l*.35,y:p.y+dy/l*.35}};const aa=expand(a),bb=expand(b),cc=expand(c);ctx.beginPath();ctx.moveTo(aa.x,aa.y);ctx.lineTo(bb.x,bb.y);ctx.lineTo(cc.x,cc.y);ctx.closePath();ctx.fill();
   if(f.image&&f.z<140){const [u,v,w]=f.uv.map(p=>[p[0]*f.image.width,p[1]*f.image.height]),den=u[0]*(v[1]-w[1])+v[0]*(w[1]-u[1])+w[0]*(u[1]-v[1]);if(Math.abs(den)>1e-8){const ax=(a.x*(v[1]-w[1])+b.x*(w[1]-u[1])+c.x*(u[1]-v[1]))/den,bx=(a.y*(v[1]-w[1])+b.y*(w[1]-u[1])+c.y*(u[1]-v[1]))/den,cx=(a.x*(w[0]-v[0])+b.x*(u[0]-w[0])+c.x*(v[0]-u[0]))/den,dx=(a.y*(w[0]-v[0])+b.y*(u[0]-w[0])+c.y*(v[0]-u[0]))/den,ex=a.x-ax*u[0]-cx*u[1],fx=a.y-bx*u[0]-dx*u[1];ctx.save();ctx.clip();ctx.transform(ax,bx,cx,dx,ex,fx);try{ctx.drawImage(f.image,0,0);}catch{}ctx.restore();}}
  }
  renderer.lastStats={milliseconds:performance.now()-now,faces:faces.length,sprites:sprites.length};ctx.globalAlpha=1;for(const s of sprites){if(s.q.x+s.w/2<0||s.q.x-s.w/2>width||s.q.y+s.h/2<0||s.q.y-s.h/2>height)continue;ctx.drawImage(s.image,s.q.x-s.w/2,s.q.y-s.h/2,s.w,s.h);}
 },dispose(){}};return renderer;
}
const api={profiles,create,move,intersects,validInputs,canvasRenderer};if(typeof module==='object'&&module.exports)module.exports=api;root.MG_SCENES_V31=api;
})(typeof window!=='undefined'?window:globalThis);
