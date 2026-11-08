/* Original V22 continuous canvas fallback. Teaching geometry; never a reconstruction of real photographs. */
import {clamp,normalizeInput,isWalkable,moveWithCollisions,cameraRelativeMove,findPath,nearestStation,angleDelta,approachVelocity,stationObstacles} from './walk-physics-v22.js';

export function createFallbackWorld({container,config,onNear=()=>{},onInteract=()=>{},onMove=()=>{},onView=()=>{},onManual=()=>{}}={}) {
  if(!container)throw Error('A world container is required.');
  const canvas=document.createElement('canvas');
  canvas.className='walk-fallback-canvas';canvas.setAttribute('aria-label','Continuous engineering room · click floor to walk, WASD or arrow keys to move');
  canvas.tabIndex=0;canvas.style.cssText='display:block;position:absolute;inset:0;width:100%;height:100%;touch-action:none;outline:none';
  container.appendChild(canvas);
  const ctx=canvas.getContext('2d',{alpha:false});if(!ctx){canvas.remove();throw Error('Canvas rendering is unavailable.');}
  let world,stations=[],obstacles=[],bounds={width:30,depth:36},position={x:0,z:15},camera={x:0,z:15},yaw=Math.PI/4,view='follow',language='zh-TW',paused=false,disposed=false;
  let input={x:0,z:0},keys=new Set(),path=[],target=null,near=null,lastTime=null,lastEmit=0,walking=false,tick=0,zoom=1,pointers=new Map(),drag=null,pinch=0,width=1,height=1,dpr=1,frameId=0,labelRects=[],completed=new Set();
  const reducedMotion=window.matchMedia?.('(prefers-reduced-motion: reduce)');
  const removers=[];
  let objectiveId='',velocity={x:0,z:0},heading=Math.PI/4;
  const cameraAngle=()=>yaw-Math.PI/4;
  const listen=(el,type,fn,opts)=>{el.addEventListener(type,fn,opts);removers.push(()=>el.removeEventListener(type,fn,opts));};
  const localText=s=>language.startsWith('zh')?s.title||s.titleEn:s.titleEn||s.title;
  const hasDialog=()=>!!document.querySelector('dialog[open]')||['INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName)||!!document.activeElement?.closest('.mentor-panel');
  const spawn=()=>({x:0,z:bounds.depth/2-4});
  function emit(force=false){const now=performance.now();if(force||now-lastEmit>120){lastEmit=now;onMove(getState());}}
  function getState(){return {x:position.x,z:position.z,yaw,moving:walking,view,nearId:near?.id||null,pathRemaining:path.length,renderer:'canvas2d'};}
  function stationPosition(s){return s.approach||{x:s.x,z:s.z+2.9};}
  function updateNear(){const next=nearestStation(position,stations,2.25);if(next?.id!==near?.id){near=next;onNear(near);}}
  function setConfig(next){completed=new Set();world=next||{};bounds=world.bounds||{width:30,depth:36};stations=(world.stations||[]).map(s=>({...s,approach:stationPosition(s)}));
    obstacles=stationObstacles(stations);position=spawn();camera={...position};yaw=heading=Math.PI/4;clearMovement();near=null;updateNear();emit(true);}
  function setPosition(p){if(!p||!Number.isFinite(p.x)||!Number.isFinite(p.z)||!isWalkable(p.x,p.z,bounds,obstacles))return false;position={x:p.x,z:p.z};camera={...position};if(Number.isFinite(p.yaw))yaw=heading=angleDelta(0,p.yaw);clearMovement();updateNear();emit(true);return true;}
  function look(deltaYaw){if(!paused)yaw=angleDelta(0,yaw+(Number(deltaYaw)||0));}
  function resetPosition(){setPosition({...spawn(),yaw:Math.PI/4});}
  function goToStation(id){const s=stations.find(s=>s.id===id);if(!s)return false;velocity={x:0,z:0};path=findPath(position,s.approach,bounds,obstacles);target=path.length?s.approach:null;return path.length>0||Math.hypot(position.x-s.approach.x,position.z-s.approach.z)<.5;}
  function interact(){if(paused)return false;updateNear();if(near){clearMovement();onInteract(near);return true;}return false;}
  function setMove(x,z){input=normalizeInput(Number(x)||0,Number(z)||0);if(Math.hypot(input.x,input.z)>0){path=[];target=null;onManual();}}
  function clearMovement(){keys.clear();input={x:0,z:0};velocity={x:0,z:0};walking=false;path=[];target=null;pointers.clear();drag=null;pinch=0;}
  function setPaused(value){paused=!!value;if(paused)clearMovement();}
  function setCompleted(ids){completed=new Set(Array.isArray(ids)?ids.filter(id=>stations.some(s=>s.id===id)):[]);}
  function setView(value){if(!['follow','overview','close'].includes(value))return;view=value;zoom=view==='overview'?.66:view==='close'?1.3:1;onView(view);emit(true);}
  function recenter(){yaw=angleDelta(0,heading);emit(true);}
  function setObjective(id){objectiveId=id;}
  function setLanguage(value){language=String(value||'en');canvas.setAttribute('aria-label',language.startsWith('zh')?'連續工程場景：點地面行走，WASD 或方向鍵移動':'Continuous engineering room: click floor to walk, WASD or arrow keys to move');}
  function resize(){const r=container.getBoundingClientRect();width=Math.max(1,r.width);height=Math.max(1,r.height);dpr=Math.min(window.devicePixelRatio||1,2);canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);}
  const scale=()=>Math.max(20,Math.min(width,height)*.055)*zoom;
  function project(x,z,y=0){const dx=x-camera.x,dz=z-camera.z,c=Math.cos(cameraAngle()),s=Math.sin(cameraAngle()),rx=dx*c-dz*s,rz=dx*s+dz*c,S=scale();return {x:width*.5+(rx-rz)*S*.76,y:height*.60+(rx+rz)*S*.43-y*S};}
  function unproject(x,y){const S=scale(),u=(x-width*.5)/(.76*S),v=(y-height*.60)/(.43*S),rx=(u+v)/2,rz=(v-u)/2,c=Math.cos(cameraAngle()),s=Math.sin(cameraAngle());return {x:camera.x+rx*c+rz*s,z:camera.z-rx*s+rz*c};}
  function polygon(points,fill,stroke){ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.closePath();if(fill){ctx.fillStyle=fill;ctx.fill();}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=1;ctx.stroke();}}
  function line(a,b,color,width=1){ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.stroke();}
  function box(x,z,w,d,h,color='#c0d1d4',base=0){const a=project(x-w/2,z-d/2,base),b=project(x+w/2,z-d/2,base),c=project(x+w/2,z+d/2,base),e=project(x-w/2,z+d/2,base),at=project(x-w/2,z-d/2,base+h),bt=project(x+w/2,z-d/2,base+h),ct=project(x+w/2,z+d/2,base+h),et=project(x-w/2,z+d/2,base+h);
    polygon([b,c,ct,bt],shade(color,-42),'#31485355');polygon([e,c,ct,et],shade(color,-20),'#31485366');polygon([at,bt,ct,et],color,'#e6f5f533');}
  function shade(hex,delta){let v=String(hex||'#9caeb5').replace('#','');if(v.length!==6)return '#8eaaaf';const n=parseInt(v,16);return '#'+[n>>16,(n>>8)&255,n&255].map(c=>clamp(c+delta,0,255).toString(16).padStart(2,'0')).join('');}
  function circle(x,z,y,r,fill,stroke){const p=project(x,z,y);ctx.beginPath();ctx.ellipse(p.x,p.y,r*scale(),r*scale()*.62,0,0,Math.PI*2);if(fill){ctx.fillStyle=fill;ctx.fill();}if(stroke){ctx.strokeStyle=stroke;ctx.stroke();}}
  function cylinder(x,z,r,h,color,base=0){const p=project(x,z,base),q=project(x,z,base+h),S=scale();ctx.fillStyle=shade(color,-18);ctx.beginPath();ctx.ellipse(p.x,p.y,r*S,r*S*.43,0,0,Math.PI);ctx.lineTo(q.x-r*S,q.y);ctx.ellipse(q.x,q.y,r*S,r*S*.43,0,Math.PI,Math.PI*2);ctx.closePath();ctx.fill();circle(x,z,base+h,r,color,'#344c5c88');}
  function screen(x,z,y,w=1.0,h=.6){const p=project(x,z,y);ctx.fillStyle='#102b39';ctx.fillRect(p.x-w*scale()/2,p.y-h*scale(),w*scale(),h*scale());ctx.fillStyle='#67edc9';ctx.fillRect(p.x-w*scale()*.4,p.y-h*scale()*.8,w*scale()*.65,2);for(let i=0;i<3;i++)ctx.fillRect(p.x-w*scale()*.4,p.y-h*scale()*(.55-i*.12),w*scale()*(.5-i*.08),1);}
  function machine(s){const {x,z}=s,accent=completed.has(s.id)?'#b3df9c':world.color||'#83dfd9';box(x,z,4,3,.10,'#637b86');
    switch(s.kind){
      case 'satellite':{
        box(x,z,1.04,.98,1.2,'#d3ab57',.68);
        box(x,z,.86,.08,.56,'#dbe6e2',1.05);
        for(const side of [-1,1]){
          box(x+side*1.13,z,.98,1.45,.065,'#244e70',1.34);
          for(let row=0;row<5;row++)line(project(x+side*1.13-.43,z-.58+row*.29,1.42),project(x+side*1.13+.43,z-.58+row*.29,1.42),'#7fb5c9',1);
        }
        circle(x,z,2.09,.42,'#e3e8de','#68868c');
        break;
      }
      case 'cryostat':{cylinder(x,z,.85,2.6,'#9eafb6',.2);for(let j=0;j<5;j++)circle(x,z,.6+j*.43,.69-j*.09,'#e6ba59','#364a5c');screen(x+1.1,z+.4,1.8,.55,.4);break;}
      case 'accelerator':{box(x,z,2.8,1.7,.3,'#37505c',1.15);for(let j=0;j<4;j++){box(x-.9+j*.6,z,.48,.7,.25,'#7aaab4',1.45);}screen(x,z,2.5,1.7,.65);break;}
      case 'vacuum':{
        cylinder(x,z,.87,1.75,'#9cb4c0',.27);
        circle(x,z,2.02,.69,'#304f66','#e0ecee');
        circle(x,z,2.03,.43,'#65868f');
        box(x+1.15,z,.55,.64,.61,'#4b626f',.15);screen(x+1.15,z,1.16,.45,.29);
        break;
      }
      case 'rocket':{
        cylinder(x,z,.33,1.71,'#d8e8e7',.52);
        const nose=project(x,z,2.78),left=project(x-.33,z,2.19),right=project(x+.33,z,2.19);
        polygon([nose,left,right],'#e6f0ee','#92a6ad');
        for(const side of [-1,1])line(project(x+side*.18,z,1.22),project(x+side*.76,z,.32),'#e9b750',scale()*.08);
        break;
      }
      case 'vehicle':case 'train':{const long=s.kind==='train'?3.6:3;box(x,z,long,1.6,.55,accent,.55);box(x-.15,z,1.6,1.4,.65,'#cadae0',1.1);for(const a of [-1,1])for(const b of [-1,1])cylinder(x+a*1.05,z+b*.8,.34,.35,'#263642',.2);screen(x,z+.75,1.65,.8,.4);break;}
      case 'robot':{cylinder(x,z,.55,.45,'#8d9da5');const arm=[project(x,z,.5),project(x-.4,z,2.3),project(x+1.2,z,3.0),project(x+1.7,z+.2,2.05)];for(let i=1;i<arm.length;i++){line(arm[i-1],arm[i],'#efae57',scale()*.34);ctx.fillStyle='#435c68';ctx.beginPath();ctx.arc(arm[i].x,arm[i].y,scale()*.20,0,7);ctx.fill();}box(x+1.7,z+.2,.6,.6,.4,'#99bac0',1.7);break;}
      case 'aircraft':{box(x,z,3.9,.65,.5,'#d9e5e5',1.05);polygon([project(x-.2,z-2,1.2),project(x+1,z,1.2),project(x-.2,z+2,1.2),project(x-.6,z,1.2)],accent,'#526a78');polygon([project(x-1.7,z-.8,1.35),project(x-1.1,z,1.35),project(x-1.7,z+.8,1.35)],'#b7cdd6');cylinder(x-.8,z,.2,.9,'#344b5c');cylinder(x+1,z,.2,.9,'#344b5c');break;}
      case 'ship':{polygon([project(x-2,z,0.5),project(x-1.3,z-.8,.5),project(x+1.8,z-.65,.5),project(x+2.2,z,.5),project(x+1.8,z+.65,.5),project(x-1.3,z+.8,.5)],'#d5e1e0','#253e52');box(x,z,3.4,1.1,.7,accent,.5);box(x-.6,z,1.0,.9,.9,'#d9e3dc',1.2);line(project(x-.6,z,2),project(x-.6,z,3.0),'#b7c9c7',3);break;}
      case 'tank':{cylinder(x,z,.95,2.5,'#b4cbd0');cylinder(x,z,.5,.25,'#d6e1df',2.5);line(project(x+.95,z,1.2),project(x+1.5,z,1.2),'#76bdc5',5);line(project(x+1.5,z,1.2),project(x+1.5,z+.8,.3),'#76bdc5',5);screen(x,z+.9,1.9,.5,.3);break;}
      case 'bridge':{for(const k of [-1,1]){box(x+k*1.2,z,.4,.5,2.8,'#9cafb7');line(project(x+k*1.2,z,2.8),project(x,z,1.5),accent,2);}box(x,z,4,1.2,.18,'#d1dbda',1.3);break;}
      case 'crane':{box(x-1.4,z,.45,.6,4,'#daa84d');box(x,z,3.6,.4,.25,'#eac669',3.7);line(project(x+1.4,z,3.8),project(x+1.4,z,1.4),'#c4d9dc',2);box(x+1.4,z,.55,.55,.55,'#c9d6d7',.85);break;}
      case 'dish':{cylinder(x,z,.55,1.4,'#93aab8');const p=project(x,z,2.4);ctx.save();ctx.translate(p.x,p.y);ctx.rotate(-.45);ctx.fillStyle='#cedcdf';ctx.beginPath();ctx.ellipse(0,0,scale()*1.3,scale()*.6,0,0,7);ctx.fill();ctx.strokeStyle='#708e9b';ctx.stroke();ctx.restore();line(project(x,z,2.4),project(x+.8,z-.6,3.2),accent,3);break;}
      case 'turbine':{box(x,z,2.7,2,.7,'#839eac');const p=project(x,z+.7,1.6);ctx.fillStyle='#4d6c7b';ctx.beginPath();ctx.arc(p.x,p.y,scale()*.9,0,7);ctx.fill();for(let i=0;i<10;i++){const a=i*Math.PI/5+tick*.4;line({x:p.x+Math.cos(a)*scale()*.25,y:p.y+Math.sin(a)*scale()*.25},{x:p.x+Math.cos(a+.25)*scale()*.75,y:p.y+Math.sin(a+.25)*scale()*.75},'#b9d0d1',scale()*.10);}ctx.fillStyle=accent;ctx.beginPath();ctx.arc(p.x,p.y,scale()*.21,0,7);ctx.fill();break;}
      case 'rack':{box(x,z,2,1.5,3.1,'#405b68');for(let i=0;i<6;i++){box(x,z+.78,1.8,.06,.26,'#1d3c49',.24+i*.43);const p=project(x+.65,z+.83,.39+i*.43);ctx.fillStyle=i%2?'#78dbb7':'#b9e980';ctx.fillRect(p.x,p.y,3,3);}break;}
      case 'furnace':{box(x,z,2.9,2.0,2.7,'#7e8f96');box(x,z+1.02,1.7,.10,1.45,'#432b29',.45);box(x,z+1.10,1.2,.06,1.0,'#e99849',.65);box(x-1.2,z,0.35,1.8,.4,'#aabdc2',2.7);screen(x+.95,z+1.1,2.2,.5,.4);break;}
      case 'bench':{for(const dx of [-1.2,1.2])for(const dz of [-.6,.6])box(x+dx,z+dz,.14,.14,1.0,'#627d87');box(x,z,3.0,1.8,.18,'#c6d4cd',1.0);box(x-.6,z,.75,.6,.7,'#c8dad8',1.2);screen(x+.6,z+.2,1.8,.8,.55);break;}
      case 'instrument':{box(x,z,2,1.7,1.0,'#91a8b0');cylinder(x-.3,z,.3,.8,'#c2d3d2',1);box(x+.3,z,.7,.6,1.6,'#d9e6df',.8);screen(x+.4,z+.4,2.2,.6,.45);break;}
      default:{box(x,z,3.0,2.2,2.7,'#c4d6d8');box(x-.35,z+1.13,1.5,.08,1.8,'#537789',.5);box(x-.35,z+1.18,1.25,.04,1.4,'#153b51',.7);screen(x+1,z+1.2,2.15,.6,.65);circle(x-.4,z,1.8,.5,accent);line(project(x-1.25,z+1.2,.4),project(x+1.2,z+1.2,.4),accent,3);break;}
    }
    const a=stationPosition(s);circle(a.x,a.z,.03,.55,near?.id===s.id?'#e8fa8f88':s.id===objectiveId?'#ebbf6477':completed.has(s.id)?'#a5e3a566':'#9de6d333',near?.id===s.id?'#effca9':'#a0d8d566');
  }
  function avatar(){const gait=walking&&!reducedMotion?.matches?Math.sin(tick*10):0,base=project(position.x,position.z,.05);ctx.fillStyle='#05232b66';ctx.beginPath();ctx.ellipse(base.x,base.y+3,scale()*.4,scale()*.17,0,0,7);ctx.fill();
    for(const d of [-1,1]){const a=project(position.x+d*.12,position.z, .72),b=project(position.x+d*.13+gait*d*.13,position.z+gait*d*.16,.12);line(a,b,'#344d5e',scale()*.15);circle(position.x+d*.13+gait*d*.13,position.z+gait*d*.16,.08,.12,'#142d40');}
    box(position.x,position.z,.52,.35,.62,'#efbc5d',.65);for(const d of [-1,1])line(project(position.x+d*.32,position.z,1.23),project(position.x+d*.34,position.z+gait*d*.16,.73),'#dbc5a6',scale()*.11);
    circle(position.x,position.z,1.52,.20,'#e2c9a6');circle(position.x,position.z,1.72,.25,'#fbf1bc','#9a895f');const top=project(position.x,position.z,1.94);ctx.fillStyle='#f5fff8';ctx.font='bold 10px system-ui';ctx.textAlign='center';ctx.fillText(language.startsWith('zh')?'你':'YOU',top.x,top.y);}
  function draw(){ctx.setTransform(dpr,0,0,dpr,0,0);const gradient=ctx.createLinearGradient(0,0,0,height);gradient.addColorStop(0,'#193643');gradient.addColorStop(1,'#102730');ctx.fillStyle=gradient;ctx.fillRect(0,0,width,height);
    const w=bounds.width/2,d=bounds.depth/2,outdoor=['outdoor','yard'].includes(world.layout),floor=outdoor?'#617a7a':world.layout==='cleanroom'?'#92abad':'#6c868e';
    polygon([project(-w,-d),project(w,-d),project(w,d),project(-w,d)],floor,'#b2cccc88');
    for(let x=Math.ceil(-w);x<=w;x+=2)line(project(x,-d),project(x,d),'#d7eeeb1b');for(let z=Math.ceil(-d);z<=d;z+=2)line(project(-w,z),project(w,z),'#d7eeeb1b');
    polygon([project(-2,-d),project(2,-d),project(2,d),project(-2,d)],outdoor?'#526e7033':'#445f6b66');for(let z=-d+1;z<d;z+=2)line(project(-1.9,z),project(-1.9,z+1),'#d7e9a5',2);for(let z=-d+1;z<d;z+=2)line(project(1.9,z),project(1.9,z+1),'#d7e9a5',2);
    if(!outdoor){polygon([project(-w,-d),project(w,-d),project(w,-d,4.2),project(-w,-d,4.2)],'#8aa4ad','#d0e3e444');polygon([project(-w,-d),project(-w,d),project(-w,d,4.2),project(-w,-d,4.2)],'#627e8b','#d0e3e433');
      for(let x=-w+2;x<w;x+=4){box(x,-d+.08,2.6,.10,1.3,'#a5c8cd',1.8);line(project(x-1.3,-d+.14,2.5),project(x+1.3,-d+.14,2.5),'#c9e6e8',2);}}
    if(path.length){ctx.save();ctx.setLineDash([4,7]);let p=project(position.x,position.z,.08);for(const q of path){const r=project(q.x,q.z,.08);line(p,r,'#d2ed8c',2);p=r;}ctx.restore();}
    if(target)circle(target.x,target.z,.10,.45,null,'#e1f69d');
    const depth=(x,z)=>{const c=Math.cos(cameraAngle()),s=Math.sin(cameraAngle());return x*c-z*s+x*s+z*c;};
    const objects=stations.map(s=>({s,depth:depth(s.x,s.z)}));objects.push({player:true,depth:depth(position.x,position.z)});objects.sort((a,b)=>a.depth-b.depth);for(const o of objects)o.player?avatar():machine(o.s);
    labelRects=[];for(let i=0;i<stations.length;i++){const s=stations[i],p=project(s.x,s.z,3.4);if(p.x<-130||p.x>width+130||p.y<20||p.y>height-40)continue;const text=String(localText(s)||'').replace(/^\d+\s*[·.\-]\s*/,'');ctx.font='600 11px system-ui';const str=text.length>26?text.slice(0,24)+'…':text,W=Math.min(220,ctx.measureText(str).width+42),H=28;ctx.fillStyle=near?.id===s.id?'#d9eea5':s.id===objectiveId?'#f5d88d':completed.has(s.id)?'#244f3eee':'#102c38e8';ctx.beginPath();if(ctx.roundRect)ctx.roundRect(p.x-W/2,p.y-H/2,W,H,6);else ctx.rect(p.x-W/2,p.y-H/2,W,H);ctx.fill();ctx.strokeStyle=near?.id===s.id?'#edfccc':'#c3e5df55';ctx.stroke();ctx.fillStyle=near?.id===s.id||s.id===objectiveId?'#17372d':'#e0efec';ctx.textAlign='left';ctx.fillText(completed.has(s.id)?'✓':String(i+1).padStart(2,'0'),p.x-W/2+8,p.y+4);ctx.fillText(str,p.x-W/2+32,p.y+4);labelRects.push({s,x:p.x-W/2,y:p.y-H/2,w:W,h:H});}
    const shadeBottom=ctx.createLinearGradient(0,height*.78,0,height);shadeBottom.addColorStop(0,'#061c2500');shadeBottom.addColorStop(1,'#061c2577');ctx.fillStyle=shadeBottom;ctx.fillRect(0,height*.78,width,height*.22);
  }
  function animate(time){
    if(disposed)return;
    frameId=requestAnimationFrame(animate);
    const dt=Math.min(.10,Math.max(0,(time-(lastTime===null?time:lastTime))/1000));
    lastTime=time;walking=false;
    if(!paused&&!document.hidden&&!hasDialog()){
      const keyX=(keys.has('d')||keys.has('arrowright')?1:0)-(keys.has('a')||keys.has('arrowleft')?1:0);
      const keyZ=(keys.has('s')||keys.has('arrowdown')?1:0)-(keys.has('w')||keys.has('arrowup')?1:0);
      let delta={x:0,z:0};
      if(path.length){
        while(path.length&&Math.hypot(path[0].x-position.x,path[0].z-position.z)<.12)path.shift();
        if(path.length){
          const dx=path[0].x-position.x,dz=path[0].z-position.z,length=Math.hypot(dx,dz);
          const step=Math.min(length,3.35*dt);
          delta={x:dx/length*step,z:dz/length*step};
        }else target=null;
      }else{
        const dir=cameraRelativeMove({x:input.x+keyX,z:input.z+keyZ},yaw),speed=keys.has('shift')?5.3:3.2;
        velocity=approachVelocity(velocity,{x:dir.x*speed,z:dir.z*speed},dt);
        delta={x:velocity.x*dt,z:velocity.z*dt};
      }
      const next=moveWithCollisions(position,delta,bounds,obstacles);
      walking=Math.hypot(next.x-position.x,next.z-position.z)>.0001;
      if(walking){
        heading=Math.atan2(position.x-next.x,position.z-next.z);
        position=next;
      }else if(path.length){path=[];target=null;}
    }
    if(!paused)tick+=dt;
    const t=reducedMotion?.matches?1:1-Math.exp(-dt*10);
    camera.x+=(position.x-camera.x)*t;
    camera.z+=(position.z-camera.z)*t;
    updateNear();draw();emit();
  }
  function localPoint(e){const r=canvas.getBoundingClientRect();return {x:e.clientX-r.left,y:e.clientY-r.top};}
  listen(canvas,'pointerdown',e=>{if(paused||e.button!==0)return;canvas.focus({preventScroll:true});canvas.setPointerCapture?.(e.pointerId);const p=localPoint(e);pointers.set(e.pointerId,p);if(pointers.size===1)drag={id:e.pointerId,...p,moved:false};if(pointers.size===2){const a=[...pointers.values()];pinch=Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y);if(drag)drag.moved=true;}});
  listen(canvas,'pointermove',e=>{if(!pointers.has(e.pointerId))return;const p=localPoint(e),prior=pointers.get(e.pointerId);pointers.set(e.pointerId,p);if(pointers.size===2){const a=[...pointers.values()],distance=Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y);if(pinch>0)zoom=clamp(zoom*distance/pinch,.45,2);pinch=distance;}else if(drag){if(Math.hypot(p.x-drag.x,p.y-drag.y)>5)drag.moved=true;if(drag.moved)yaw=angleDelta(0,yaw-(p.x-prior.x)*.005);}});
  const release=e=>{const p=localPoint(e);if(drag?.id===e.pointerId&&!drag.moved&&!paused&&!hasDialog()){const hit=labelRects.find(r=>p.x>=r.x&&p.x<=r.x+r.w&&p.y>=r.y&&p.y<=r.y+r.h);onManual();if(hit){if(near?.id===hit.s.id)interact();else goToStation(hit.s.id);}else{const floor=unproject(p.x,p.y);if(isWalkable(floor.x,floor.z,bounds,obstacles)){path=findPath(position,floor,bounds,obstacles);target=path.length?floor:null;}}}pointers.delete(e.pointerId);if(!pointers.size)drag=null;pinch=0;};
  listen(canvas,'pointerup',release);const cancelPointer=e=>{pointers.delete(e.pointerId);drag=null;pinch=0;};listen(canvas,'pointercancel',cancelPointer);listen(canvas,'lostpointercapture',cancelPointer);listen(canvas,'wheel',e=>{if(paused)return;e.preventDefault();zoom=clamp(zoom*Math.exp(-clamp(e.deltaY,-100,100)*.002),.45,2);},{passive:false});
  listen(document,'keydown',e=>{if(paused||hasDialog()||e.ctrlKey||e.metaKey||e.altKey)return;const k=e.key.toLowerCase();if(['w','a','s','d','arrowup','arrowdown','arrowleft','arrowright','shift'].includes(k)){keys.add(k);path=[];target=null;onManual();e.preventDefault();}else if(k==='e'){e.preventDefault();interact();}else if(k==='2')setView('close');else if(k==='3')setView('follow');else if(k==='4')setView('overview');});
  listen(document,'keyup',e=>keys.delete(e.key.toLowerCase()));listen(window,'blur',clearMovement);listen(document,'visibilitychange',()=>{if(document.hidden)clearMovement();});listen(window,'resize',resize);
  function dispose(){disposed=true;cancelAnimationFrame(frameId);for(const remove of removers)remove();canvas.remove();}
  setConfig(config);resize();frameId=requestAnimationFrame(animate);
  return {setConfig,setCompleted,setView,setMove,goToStation,interact,resize,dispose,getState,setPaused,setLanguage,setPosition,resetPosition,setObjective,recenter,look,stop:clearMovement};
}
