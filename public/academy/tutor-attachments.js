// Images stay in memory until the learner explicitly submits to a vision-capable route.
export const TUTOR_IMAGE_LIMIT = 4 * 1024 * 1024;
export const TUTOR_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
export function tutorImageMime(bytes) {
  if (bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) return 'image/jpeg';
  if ([137,80,78,71,13,10,26,10].every((v,i) => bytes[i] === v)) return 'image/png';
  if (String.fromCharCode(...bytes.slice(0,4)) === 'RIFF' && String.fromCharCode(...bytes.slice(8,12)) === 'WEBP') return 'image/webp';
  return '';
}
export function tutorImageDimensions(bytes, mimeType = tutorImageMime(bytes)) {
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const u24 = offset => bytes[offset] | (bytes[offset+1]<<8) | (bytes[offset+2]<<16);
  if (mimeType === 'image/png' && bytes.length >= 24 && String.fromCharCode(...bytes.slice(12,16)) === 'IHDR') return {width:view.getUint32(16),height:view.getUint32(20)};
  if (mimeType === 'image/jpeg') {
    let offset=2;
    while (offset+3 < bytes.length) {
      if (bytes[offset++] !== 255) return null;
      while (bytes[offset] === 255) offset++;
      const marker=bytes[offset++];
      if (marker === 217 || marker === 218) return null;
      if (marker === 1 || marker >= 208 && marker <= 216) continue;
      if (offset+2 > bytes.length) return null;
      const length=view.getUint16(offset);
      if (length < 2 || offset+length > bytes.length) return null;
      if ([192,193,194,195,197,198,199,201,202,203,205,206,207].includes(marker) && length >= 8) return {width:view.getUint16(offset+5),height:view.getUint16(offset+3)};
      offset+=length;
    }
  }
  if (mimeType === 'image/webp') {
    let offset=12;
    while (offset+8 <= bytes.length) {
      const chunk=String.fromCharCode(...bytes.slice(offset,offset+4)),length=view.getUint32(offset+4,true),start=offset+8;
      if (length > bytes.length-start) return null;
      if (chunk === 'VP8X' && length >= 10) return {width:u24(start+4)+1,height:u24(start+7)+1};
      if (chunk === 'VP8L' && length >= 5 && bytes[start] === 47) return {width:1+(bytes[start+1]|((bytes[start+2]&63)<<8)),height:1+((bytes[start+2]>>6)|(bytes[start+3]<<2)|((bytes[start+4]&15)<<10))};
      if (chunk === 'VP8 ' && length >= 10 && bytes[start+3] === 157 && bytes[start+4] === 1 && bytes[start+5] === 42) return {width:view.getUint16(start+6,true)&16383,height:view.getUint16(start+8,true)&16383};
      offset=start+length+(length%2);
    }
  }
  return null;
}
function validateDimensions(size) {
  if (!size?.width || !size?.height || size.width > 8192 || size.height > 8192 || size.width * size.height > 32000000) throw Error('IMAGE_DIMENSIONS');
}
export function validateTutorImageFile(file) {
  if (!file || !TUTOR_IMAGE_TYPES.includes(file.type)) throw Error('IMAGE_TYPE');
  if (!Number.isFinite(file.size) || file.size <= 0 || file.size > TUTOR_IMAGE_LIMIT) throw Error('IMAGE_SIZE');
}
export async function prepareTutorImage(file, env = globalThis) {
  validateTutorImageFile(file);
  const bytes = new Uint8Array(await file.arrayBuffer());
  if (bytes.byteLength !== file.size || tutorImageMime(bytes) !== file.type) throw Error('IMAGE_TYPE');
  const headerSize = tutorImageDimensions(bytes, file.type);
  if (!headerSize) throw Error('IMAGE_DECODE');
  validateDimensions(headerSize); // Reject oversized compressed images before browser decoding.
  let dimensions;
  if (typeof env.createImageBitmap === 'function') {
    const bitmap = await env.createImageBitmap(file);
    try { dimensions = {width:bitmap.width,height:bitmap.height}; } finally { bitmap.close?.(); }
  } else {
    dimensions = await new Promise((resolve,reject) => {
      const src = env.URL.createObjectURL(file), image = new env.Image();
      const done = () => env.URL.revokeObjectURL(src);
      image.onload = () => { const size={width:image.naturalWidth,height:image.naturalHeight};done();resolve(size); };
      image.onerror = () => {done();reject(Error('IMAGE_DECODE'));};
      image.src = src;
    });
  }
  validateDimensions(dimensions);
  let binary = '';
  for (let start=0;start<bytes.length;start+=0x8000) binary += String.fromCharCode(...bytes.subarray(start,start+0x8000));
  return {image:{mimeType:file.type,data:env.btoa(binary)},previewUrl:env.URL.createObjectURL(file),name:String(file.name||'image').slice(0,200),bytes:file.size,...dimensions};
}
export function releaseTutorImage(attachment, env = globalThis) {
  if (attachment?.previewUrl) env.URL.revokeObjectURL(attachment.previewUrl);
}
export function tutorServiceRoutes(routes, available = false) {
  const ids = new Set();
  const normalized = (Array.isArray(routes) ? routes : []).filter(r => r && typeof r.id === 'string' && /^[a-z][a-z0-9-]{0,63}$/.test(r.id) && !ids.has(r.id) && ids.add(r.id)).slice(0,12).map(r => ({id:r.id,label:String(r.label||r.id).slice(0,120),model:String(r.model||'').slice(0,120),supportsImages:r.supportsImages===true,cloud:r.cloud!==false,destination:String(r.destination||'').slice(0,200)}));
  // Older hosted endpoints do not declare a destination: treat them as cloud.
  return normalized.length ? normalized : available ? [{id:'default',label:'Configured AI',model:'',supportsImages:false,cloud:true,destination:''}] : [];
}
