/** Read a large UTF-8 JSON array without creating one unbounded V8 string.
 * Each bounded item is still validated by JSON.parse; this scanner only finds
 * item boundaries and validates the outer array grammar. No eval is used.
 */
import fs from 'node:fs';
import {TextDecoder} from 'node:util';

const whitespace=character=>character===' '||character==='\n'||character==='\r'||character==='\t';

export function* iterateJsonArray(file,{chunkSize=65536,maxItemChars=16*1024*1024}={}){
  if(!Number.isSafeInteger(chunkSize)||chunkSize<1||chunkSize>16*1024*1024)throw new RangeError('Invalid JSON chunk size');
  if(!Number.isSafeInteger(maxItemChars)||maxItemChars<1||maxItemChars>64*1024*1024)throw new RangeError('Invalid JSON item size limit');
  const descriptor=fs.openSync(file,'r'),buffer=Buffer.allocUnsafe(chunkSize),decoder=new TextDecoder('utf-8',{fatal:true,ignoreBOM:true});
  let state='start',allowEnd=true,kind='',inString=false,escaped=false,stack=[],parts=[],length=0,item=0;
  const fail=message=>{throw new SyntaxError(`${String(file)}: JSON array item ${item+1}: ${message}`);};
  const append=value=>{length+=value.length;if(length>maxItemChars)throw new RangeError(`${String(file)}: JSON array item ${item+1} exceeds ${maxItemChars} characters`);if(value)parts.push(value);};
  const finish=()=>{let result;try{result=JSON.parse(parts.join(''));}catch(error){fail(error.message);}parts=[];length=0;item++;state='after';return result;};
  function* scan(text){
    let mark=state==='token'?0:-1;
    for(let i=0;i<text.length;i++){
      const c=text[i];
      if(state==='token'){
        if(kind==='primitive'){
          if(whitespace(c)||c===','||c===']'){append(text.slice(mark,i));mark=-1;yield finish();i--;}
          continue;
        }
        if(inString){
          if(escaped){escaped=false;continue;}
          if(c==='\\'){escaped=true;continue;}
          if(c==='"'){
            inString=false;
            if(kind==='string'){append(text.slice(mark,i+1));mark=-1;yield finish();}
          }
          continue;
        }
        if(c==='"'){inString=true;continue;}
        if(c==='{'||c==='['){stack.push(c);continue;}
        if(c==='}'||c===']'){
          if(stack.pop()!==(c==='}'?'{':'['))fail('Mismatched nested container');
          if(!stack.length){append(text.slice(mark,i+1));mark=-1;yield finish();}
        }
        continue;
      }
      if(whitespace(c))continue;
      if(state==='start'){
        if(c!=='[')fail('Expected a top-level array');
        state='value';continue;
      }
      if(state==='done')fail('Unexpected data after the array');
      if(state==='after'){
        if(c===','){state='value';allowEnd=false;continue;}
        if(c===']'){state='done';continue;}
        fail('Expected a comma or closing bracket');
      }
      if(c===']'){
        if(!allowEnd)fail('Trailing comma');
        state='done';continue;
      }
      if(!'{["-0123456789tfn'.includes(c))fail('Expected a JSON value');
      kind=c==='"'?'string':c==='{'||c==='['?'container':'primitive';
      state='token';stack=[];inString=false;escaped=false;mark=i;i--;
    }
    if(mark>=0)append(text.slice(mark));
  }
  try{
    for(;;){
      const count=fs.readSync(descriptor,buffer,0,buffer.length,null);
      if(!count)break;
      let decoded;try{decoded=decoder.decode(buffer.subarray(0,count),{stream:true});}catch{fail('Invalid UTF-8');}
      yield* scan(decoded);
    }
    let tail;try{tail=decoder.decode();}catch{fail('Incomplete UTF-8');}
    yield* scan(tail);
    if(state!=='done')fail('Unexpected end of input');
  }finally{fs.closeSync(descriptor);}
}

export const readJsonArray=(file,options)=>Array.from(iterateJsonArray(file,options));
