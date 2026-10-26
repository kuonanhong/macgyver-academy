/* Exact 2D coordinate transform for manually marked, normalized photo points.
 * The browser image uses object-fit: contain/cover, centered transform origin,
 * translate(px,px) scale(zoom). No new views or object recognition are inferred.
 */
export function validFlatPhotoPoint(point){return !!point&&Number.isFinite(point.x)&&Number.isFinite(point.y)&&point.x>=0&&point.x<=1&&point.y>=0&&point.y<=1;}
export function flatPhotoRect(imageWidth,imageHeight,width,height,{fit='contain',zoom=1,panX=0,panY=0}={}){
 if(![imageWidth,imageHeight,width,height,zoom].every(v=>Number.isFinite(v)&&v>0)||![panX,panY].every(Number.isFinite)||!['contain','cover'].includes(fit))return null;
 const scale=(fit==='cover'?Math.max:Math.min)(width/imageWidth,height/imageHeight)*zoom,w=imageWidth*scale,h=imageHeight*scale;
 return {left:(width-w)/2+panX,top:(height-h)/2+panY,width:w,height:h};
}
export function flatPhotoHotspotPoint(point,imageWidth,imageHeight,width,height,options={}){
 if(!validFlatPhotoPoint(point))return null;const rect=flatPhotoRect(imageWidth,imageHeight,width,height,options);if(!rect)return null;
 const x=rect.left+point.x*rect.width,y=rect.top+point.y*rect.height;
 return x>=0&&x<=width&&y>=0&&y<=height?{x,y}:null;
}
