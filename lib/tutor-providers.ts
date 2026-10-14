// Provider keys and URLs come only from server configuration, never the client.
type Config = { AI_BASE_URL?:string; AI_API_KEY?:string; AI_MODEL?:string; GEMINI_API_KEY?:string; GEMINI_MODEL?:string };
export type TutorImage = {mimeType:string; data:string};
export function hostedRoutes(config:Config) {
  const routes = [];
  if(config.AI_BASE_URL && config.AI_API_KEY && config.AI_MODEL) routes.push({id:'default', label:'Configured AI service', model:config.AI_MODEL, supportsImages:false, cloud:true, destination:'Administrator-configured AI provider'});
  if(config.GEMINI_API_KEY) routes.push({id:'gemini',label:'Gemini · text + image',model:config.GEMINI_MODEL || 'gemini-3.5-flash-lite',supportsImages:true,cloud:true,destination:'Google Gemini API'});
  return routes;
}
export function validateTutorImage(value:unknown):TutorImage|undefined {
  if(value===undefined || value===null) return undefined;
  if(typeof value!=='object' || Array.isArray(value)) throw new Error('Invalid image.');
  const {mimeType,data}=value as TutorImage;
  if(!['image/png','image/jpeg','image/webp'].includes(mimeType) || typeof data!=='string' || !data || data.length>5592408 || data.length%4 || /[^A-Za-z0-9+/=]/.test(data) || data.slice(0,-2).includes('=') || (data.at(-2)==='=' && data.at(-1)!=='=')) throw new Error('Use a PNG, JPEG or WebP image up to 4 MiB.');
  const raw=atob(data);
  if(raw.length>4194304 || btoa(raw)!==data) throw new Error('Invalid image encoding or size.');
  const u=(i:number)=>raw.charCodeAt(i), be16=(i:number)=>(u(i)<<8)|u(i+1), be32=(i:number)=>u(i)*16777216+(u(i+1)<<16)+(u(i+2)<<8)+u(i+3), le24=(i:number)=>u(i)+(u(i+1)<<8)+(u(i+2)<<16);
  let width=0,height=0;
  if(mimeType==='image/png' && raw.startsWith('\x89PNG\r\n\x1a\n') && raw.slice(12,16)==='IHDR' && raw.length>=33 && be32(8)===13) {width=be32(16);height=be32(20);}
  else if(mimeType==='image/jpeg' && raw.startsWith('\xff\xd8\xff') && raw.endsWith('\xff\xd9')) {
    let i=2;
    while(i+4<raw.length) {
      if(u(i++)!==255) break;
      while(u(i)===255)i++;
      const tag=u(i++);
      if(tag===217 || tag===218) break;
      if(tag===1 || (tag>=208 && tag<=215)) continue;
      const length=be16(i); if(length<2 || i+length>raw.length) break;
      if([192,193,194,195,197,198,199,201,202,203,205,206,207].includes(tag) && length>=8) {height=be16(i+3);width=be16(i+5);break;}
      i+=length;
    }
  } else if(mimeType==='image/webp' && raw.startsWith('RIFF') && raw.slice(8,12)==='WEBP' && raw.length>=30 && u(4)+(u(5)<<8)+(u(6)<<16)+u(7)*16777216===raw.length-8) {
    if(raw.slice(12,16)==='VP8X') {width=le24(24)+1;height=le24(27)+1;}
    else if(raw.slice(12,16)==='VP8 ' && raw.slice(23,26)==='\x9d\x01\x2a') {width=(u(26)+(u(27)<<8))&16383;height=(u(28)+(u(29)<<8))&16383;}
    else if(raw.slice(12,16)==='VP8L' && u(20)===47) {width=1+u(21)+((u(22)&63)<<8);height=1+(u(22)>>6)+(u(23)<<2)+((u(24)&15)<<10);}
  }
  if(!width || !height || width>8192 || height>8192 || width*height>32000000) throw new Error('Invalid image format or dimensions (maximum 8192 per edge / 32 megapixels).');
  return {mimeType,data};
}
export function tutorHistory(value:unknown) {
  if(value===undefined) return [];
  if(!Array.isArray(value) || value.length>6) throw new Error('Invalid conversation history.');
  const result=value.map((v:unknown)=>{
    if(!v || typeof v!=='object')throw new Error('Invalid conversation history.');
    const {role,content}=v as {role:unknown;content:unknown};
    if(!['user','assistant'].includes(String(role)) || typeof content!=='string' || content.length>3000)throw new Error('Invalid conversation history.');
    return {role,content};
  });
  if(result.reduce((n,v)=>n+v.content.length,0)>6000)throw new Error('Conversation history is too long.');
  return result;
}
export async function geminiCompletion(config:Config, system:string, prompt:string, image?:TutorImage, jsonOutput=false) {
  const model=config.GEMINI_MODEL || 'gemini-3.5-flash-lite';
  if(!config.GEMINI_API_KEY || !/^[a-zA-Z0-9._-]{1,100}$/.test(model)) throw new Error('Gemini is not configured.');
  const response=await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,{
    method:'POST',redirect:'error',signal:AbortSignal.timeout(35000),
    headers:{'Content-Type':'application/json','x-goog-api-key':config.GEMINI_API_KEY},
    body:JSON.stringify({systemInstruction:{parts:[{text:system}]},contents:[{role:'user',parts:[{text:prompt},...(image?[{inlineData:image}]:[])]}],generationConfig:{temperature:0.2,maxOutputTokens:jsonOutput?8192:3000,...(jsonOutput?{responseMimeType:'application/json'}:{})}})
  });
  if(!response.ok)throw new Error('Gemini rejected the request.');
  const result=await response.json() as {candidates?:{content?:{parts?:{text?:string;thought?:boolean}[]}}[]};
  const answer=result.candidates?.[0]?.content?.parts?.filter(p=>typeof p.text==='string' && !p.thought).map(p=>p.text).join('') || '';
  if(!answer.trim() || answer.length>100000)throw new Error('Gemini returned an invalid response.');
  return {answer:jsonOutput?answer:answer.slice(0,24000),model};
}
