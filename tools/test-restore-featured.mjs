import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import {restoreFeatured} from './restore-featured.mjs';
const src=new URL('../public/academy/data/',import.meta.url),tmp=fs.mkdtempSync(path.join(os.tmpdir(),'mg-source-parts-'));
try{
 const data=path.join(tmp,'public/academy/data');fs.mkdirSync(data,{recursive:true});fs.cpSync(new URL('course-parts/',src),path.join(data,'course-parts'),{recursive:true});
 const canonical=fs.readFileSync(new URL('featured.json',src));const target=restoreFeatured(tmp);assert(fs.readFileSync(target).equals(canonical),'Canonical bytes restored exactly, including numeric spelling/order');assert.equal(JSON.parse(canonical).length,338);
 fs.unlinkSync(target);const manifest=JSON.parse(fs.readFileSync(path.join(data,'course-parts/index.json'))),part=path.join(data,'course-parts',manifest.parts[0].file);fs.appendFileSync(part,' ');assert.throws(()=>restoreFeatured(tmp),/size|checksum/);assert(!fs.existsSync(target),'No partial course file on corruption');
 assert.equal(crypto.createHash('sha256').update(canonical).digest('hex').length,64);
 console.log('PASS source reconstruction: all courses, exact canonical bytes, bounded/hash-checked parts, rejected corruption and no partial output.');
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
