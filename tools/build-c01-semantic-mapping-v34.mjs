#!/usr/bin/env node
/** C01 authored clause mapping. English captions follow the selected language's
 * measured speech, never the English audio clock. --require-all is fail-closed.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const delivery=path.resolve(root,'../delivery/process-v34/C01');
const scriptFile=path.join(root,'docs/packaging-process-scripts-v34/C01.json');
const scriptBytes=fs.readFileSync(scriptFile),D=JSON.parse(scriptBytes);
const sha=value=>crypto.createHash('sha256').update(value).digest('hex');
const segments=Object.fromEntries(D.languages.map(lang=>[lang,D.cues.map(c=>[...new Intl.Segmenter(lang,{granularity:'sentence'}).segment(c.text[lang])].map(s=>s.segment.trim()).filter(Boolean))]));
const en=segments.en;
const E=(chapter,...indices)=>indices.map(i=>en[chapter-1][i-1]).join(' ');
const thermalIntro='Start thermal planning with explicit assumptions.';
const thermalValues='Assume two hundred fifty watts sustained, an effective resistance of zero point one eight kelvin per watt for the complete cooling system, and thirty-five degrees ambient.';
const evidenceAndThroughput=E(9,4)+' Then check sustained throughput.';
const throttle='Any performance reduction from thermal throttling belongs in the verification result.';
const parallel=(chapter)=>[...en[chapter-1]];
const chinese=[
  parallel(1),[E(2,1,2),E(2,3),E(2,4),E(2,5,6)],parallel(3),
  [E(4,1,2),E(4,3),E(4,4,5)],
  [thermalIntro,thermalValues,E(5,2),E(5,3),E(5,4)],
  [E(6,1),E(6,2),E(6,3),E(6,4,5)],parallel(7),
  [E(8,1),E(8,2,3),E(8,4),E(8,5),E(8,6)],
  [E(9,1,2),E(9,3),evidenceAndThroughput,throttle],parallel(10)
];
const japaneseKorean=[
  parallel(1),parallel(2),parallel(3),
  ['Consider this teaching example.','Sixty-four lanes in one direction, each carrying sixteen gigabits per second.',E(4,2),E(4,3),'This is not a standards guarantee.',E(4,5)],
  [thermalIntro,thermalValues,E(5,2),E(5,3),E(5,4)],parallel(6),parallel(7),parallel(8),
  [E(9,1),E(9,2),E(9,3),evidenceAndThroughput,throttle],
  [E(10,1),E(10,2),E(10,3),'Next comes functional and die partitioning.','Turn requirements into candidate system compositions.',E(10,5)]
];
const japanese=japaneseKorean.map(a=>[...a]);
japanese[7]=[E(8,1),E(8,2),E(8,3),E(8,4),'Compare useful bandwidth, power, dimensions, test access, supply conditions, and total cost; identify the evidence needed to distinguish candidates.'];
const authored={'zh-TW':chinese,'zh-CN':chinese,en:en,ja:japanese,ko:japaneseKorean};
const tracks=[];
for(const language of D.languages){
  const cueFile=path.join(delivery,`C01.full.${language}.cues.json`);
  let measured=null,cueSha=null;
  if(fs.existsSync(cueFile)){const bytes=fs.readFileSync(cueFile);cueSha=sha(bytes);const parsed=JSON.parse(bytes);if(parsed.alignmentMode!=='measured-sentence-pcm-v2')throw Error(`Unexpected timing basis for ${language}`);measured=parsed.cues;}
  else if(process.argv.includes('--require-all'))throw Error(`Measured cues are not complete: ${language}`);
  const sentences=[];
  for(let c=0;c<10;c++){
    const source=segments[language][c],translations=authored[language][c];
    if(source.length!==translations.length)throw Error(`Authored clause count mismatch ${language}/${c+1}: ${source.length}/${translations.length}`);
    source.forEach((sourceText,s)=>{
      let cue=null;if(measured){cue=measured.find(r=>r.chapterIndex===c&&r.sentenceIndex===s);if(!cue||cue.text!==sourceText)throw Error(`Source differs from measured narration: ${language}/${c+1}/${s+1}`);if(!(cue.start>=c*30&&cue.end<=c*30+30&&cue.end>cue.start))throw Error('Invalid measured interval');}
      sentences.push({chapter:c+1,sentence:s+1,sourceText,sourceTextSha256:sha(sourceText),englishText:translations[s],alignment:'authored-semantic',measuredCueVerified:!!cue,...(cue?{speechStart:cue.start,speechEnd:cue.end}:{})});
    });
  }
  if(measured&&sentences.length!==measured.length)throw Error(`Unmapped measured sentences in ${language}`);
  tracks.push({tourId:'C01',language,timingBindingStatus:measured?'PASS':'AWAITING_MEASURED_CUES',measuredCueFile:measured?path.relative(delivery,cueFile):null,measuredCueSha256:cueSha,sentences});
}
const result={schemaVersion:1,processId:'C01',scriptSha256:sha(scriptBytes),basis:'Authored chapter-local meaning alignment, reviewed against all five complete scripts; exact source text is checked against measured PCM sentence cues when available.',timingPolicy:'Selected-language measured speech defines the subtitle interval. English second line translates that spoken sentence or clause, not English audio timestamps.',reviewType:'AI authored semantic mapping; not native-speaker engineering certification',status:tracks.every(t=>t.timingBindingStatus==='PASS')?'PASS':'SEMANTICS_READY_AWAITING_REMAINING_MEASURED_CUES',tracks};
fs.mkdirSync(delivery,{recursive:true});const out=path.join(delivery,'SEMANTIC_MAPPING_C01.json');fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({file:out,status:result.status,sentenceRows:tracks.reduce((n,t)=>n+t.sentences.length,0),measuredLanguages:tracks.filter(t=>t.timingBindingStatus==='PASS').map(t=>t.language)},null,2));
