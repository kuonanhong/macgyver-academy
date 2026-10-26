/* CPU spherical projection for verified 2:1 panoramas. No synthesized views.
 * Rendering uses a bounded 320 x 180 sampling surface; the original photograph
 * is resampled, never inferred. The scene's requestAnimationFrame owns updates.
 */
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
export function panoramaDirectionUV(x,y,aspect,yaw=0,pitch=0,zoom=1){
 const k=Math.tan((75/clamp(zoom,.5,2))*Math.PI/360),dx=x*aspect*k,dy=y*k,dz=-1,cp=Math.cos(pitch),sp=Math.sin(pitch);
 const ry=dy*cp-dz*sp,rz=dy*sp+dz*cp,cy=Math.cos(yaw),sy=Math.sin(yaw),rx=dx*cy-rz*sy,zz=dx*sy+rz*cy,len=Math.hypot(rx,ry,zz);
 return {u:((Math.atan2(rx,-zz)/(2*Math.PI)+.5)%1+1)%1,v:Math.acos(clamp(ry/len,-1,1))/Math.PI};
}
export function panoramaHotspotPoint(yaw,pitch,viewYaw,viewPitch,zoom,width,height){
 const wx=Math.sin(yaw)*Math.cos(pitch),wy=Math.sin(pitch),wz=-Math.cos(yaw)*Math.cos(pitch),cy=Math.cos(viewYaw),sy=Math.sin(viewYaw),cp=Math.cos(viewPitch),sp=Math.sin(viewPitch);
 const dx=wx*cy+wz*sy,rz=-wx*sy+wz*cy,dy=wy*cp+rz*sp,dz=-wy*sp+rz*cp;
 if(dz>=-.01)return null;
 const k=Math.tan((75/clamp(zoom,.5,2))*Math.PI/360),x=width/2*(1+dx/(-dz)/(width/height*k)),y=height/2*(1-dy/(-dz)/k);
 return x>=0&&x<=width&&y>=0&&y<=height?{x,y}:null;
}
export function createCpuPanorama(canvas,{maxWidth=320,maxHeight=180}={}){
 let ctx;try{ctx=canvas.getContext('2d',{alpha:false});}catch{}if(!ctx)return null;
 const sample=document.createElement('canvas'),sampleContext=sample.getContext('2d',{willReadFrequently:true});
 const frame=document.createElement('canvas'),frameContext=frame.getContext('2d',{alpha:false});
 if(!sampleContext||!frameContext)return null;
 let pixels=null,imageWidth=0,imageHeight=0,destroyed=false,last='',lastAt=0;
 return {mode:'cpu',setImage(image){
  try{imageWidth=Math.min(2048,image.naturalWidth||image.width);imageHeight=Math.round(imageWidth/2);sample.width=imageWidth;sample.height=imageHeight;sampleContext.drawImage(image,0,0,imageWidth,imageHeight);pixels=sampleContext.getImageData(0,0,imageWidth,imageHeight).data;last='';return true;}catch{pixels=null;return false;}
 },draw(yaw,pitch,zoom){
  if(destroyed||!pixels||!canvas.width||!canvas.height)return;
  const width=Math.min(maxWidth,canvas.width),height=Math.max(1,Math.min(maxHeight,Math.round(width*canvas.height/canvas.width))),stamp=[yaw,pitch,zoom,canvas.width,canvas.height].join(':');if(stamp===last)return;
  // One bounded render per requested scene frame. Low-power devices avoid DPR
  // multiplication; pixel resolution is independent of display resolution.
  frame.width=width;frame.height=height;const data=frameContext.createImageData(width,height),out=data.data,aspect=canvas.width/canvas.height;
  const k=Math.tan((75/clamp(zoom,.5,2))*Math.PI/360),cp=Math.cos(pitch),sp=Math.sin(pitch),cy=Math.cos(yaw),sy=Math.sin(yaw);
  for(let py=0;py<height;py++){const dy=(1-2*(py+.5)/height)*k,ry=dy*cp+sp,rz=dy*sp-cp;
   for(let px=0;px<width;px++){const dx=(2*(px+.5)/width-1)*aspect*k,rx=dx*cy-rz*sy,zz=dx*sy+rz*cy,len=Math.hypot(rx,ry,zz),u=((Math.atan2(rx,-zz)/(2*Math.PI)+.5)%1+1)%1,v=Math.acos(clamp(ry/len,-1,1))/Math.PI,source=(Math.min(imageHeight-1,Math.floor(v*imageHeight))*imageWidth+Math.min(imageWidth-1,Math.floor(u*imageWidth)))*4,target=(py*width+px)*4;out[target]=pixels[source];out[target+1]=pixels[source+1];out[target+2]=pixels[source+2];out[target+3]=255;}
  }
  frameContext.putImageData(data,0,0);ctx.imageSmoothingEnabled=true;ctx.drawImage(frame,0,0,canvas.width,canvas.height);last=stamp;lastAt=Date.now();
 },dispose(){destroyed=true;pixels=null;sample.width=sample.height=frame.width=frame.height=1;},get modeDetails(){return {mode:'cpu',maxWidth,maxHeight,lastAt};}};
}
