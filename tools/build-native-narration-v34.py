#!/usr/bin/env python3
"""Build bounded, normalized narration with voices already available to macOS say.

No API, network service, voice/model download, or movie modification is used.
Requires macOS say, Node.js with Intl.Segmenter, and FFmpeg/ffprobe. Output is separate WAV/M4A narration.
Default: first interposer chapter, in Traditional Chinese and English, 30 s each.
--full produces the entire source timeline: 300 s for the existing overviews.
--script accepts {id,durationSeconds,cues:[{start,end,text:{language:text}}]}
for authored timelines, including a separate 900 s / 30-chapter process film,
semantically aligned multilingual subtitle cues instead of existing chapters.
Each original Intl.Segmenter sentence is synthesized separately. Sentence times
come from measured PCM samples after a common chapter pace adjustment, not text
length estimates. Silent gaps remain gaps in the emitted VTT/JSON.
Every unit is measured and fitted without cutting a spoken ending. Excessively
dense scripts fail rather than being silently truncated or sped up without limit.
"""
from __future__ import annotations
import argparse
import hashlib
import fcntl
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import struct
import wave

ROOT=Path(__file__).resolve().parents[1]
VOICES={'zh-TW':'Meijia','zh-CN':'Tingting','en':'Samantha','ja':'Kyoko','ko':'Yuna'}
RATE=48000
LEAD=.35
TAIL=.50
GAP=.18
ALIGNMENT="measured-sentence-pcm-v2"
TARGET_LUFS=-16


def run(args):
    return subprocess.run([str(a) for a in args],check=True,capture_output=True,text=True)


def duration(file):
    file=Path(file)
    if file.suffix=='.wav':
        with wave.open(str(file)) as f:return f.getnframes()/f.getframerate()
    if file.suffix=='.aiff':
        # AIFF COMM carries exact frame count and IEEE 80-bit sample rate.
        # Reading this avoids launching ffprobe for every synthesized sentence.
        with file.open('rb') as f:
            head=f.read(12)
            if head[:4]!=b'FORM' or head[8:] not in (b'AIFF',b'AIFC'):raise ValueError('Invalid native AIFF file.')
            while True:
                h=f.read(8)
                if len(h)!=8:break
                tag,size=struct.unpack('>4sI',h)
                if tag==b'COMM':
                    data=f.read(size)
                    if len(data)<18:raise ValueError('Incomplete AIFF COMM.')
                    frames=struct.unpack('>I',data[2:6])[0]
                    exponent=struct.unpack('>H',data[8:10])[0]
                    mantissa=struct.unpack('>Q',data[10:18])[0]
                    hz=mantissa*2.0**((exponent&0x7fff)-16383-63)
                    if exponent&0x8000 or not 8000<=hz<=192000 or frames<=0:raise ValueError('Invalid native AIFF timing.')
                    return frames/hz
                f.seek(size+(size%2),1)
        raise ValueError('AIFF has no timing metadata.')
    return float(json.loads(run(['ffprobe','-v','error','-show_format','-of','json',file]).stdout)['format']['duration'])


def digest(file):
    h=hashlib.sha256()
    with file.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def loudness(file):
    log=run(['ffmpeg','-hide_banner','-i',file,'-af',f'loudnorm=I={TARGET_LUFS}:TP=-1.5:LRA=7:print_format=json','-f','null','-']).stderr
    data=json.loads(log[log.rfind('{'):log.rfind('}')+1])
    if not math.isfinite(float(data['input_i'])):raise ValueError('No measurable speech: '+str(file))
    return data


def final_meter(file):
    # EBU R128 analysis measures the decoded waveform without running an
    # unnecessary second normalization on the complete audio timeline.
    log=run(['ffmpeg','-hide_banner','-i',file,'-af','ebur128=peak=true:framelog=verbose','-f','null','-']).stderr
    summary=log.rsplit('Summary:',1)[-1]
    def field(pattern):
        found=re.search(pattern,summary)
        if not found or not math.isfinite(float(found[1])):raise ValueError('Missing finite EBU R128 meter.')
        return found[1]
    return {'input_i':field(r'\bI:\s+(-?[0-9.]+)'),
            'input_tp':field(r'Peak:\s+(-?[0-9.]+)')}


def read_units(tour,language,script=None):
    if script:
        d=json.loads(script.read_text('utf-8'))
        units=[{'start':c['start'],'end':c['end'],'title':c.get('id',''),'text':c['text'][language]} for c in d['cues']]
        identity=d.get('id','authored-script')
    else:
        file=ROOT/'public/academy/assets/packaging-tour-v33/transcripts'/f'{tour}.{language}.json'
        d=json.loads(file.read_text('utf-8'));units=d['chapters'];identity=tour
    previous=0
    for i,c in enumerate(units):
        if any(type(c[k]) not in (int,float) or not math.isfinite(c[k]) for k in ('start','end')):
            raise ValueError('Narration cue timestamps must be finite numbers.')
        if abs(c['start']-previous)>1e-6 or not c['end']>c['start']:
            raise ValueError('Narration cue windows must be contiguous, beginning at zero.')
        if not isinstance(c['text'],str) or not c['text'].strip():raise ValueError('Missing narration text.')
        previous=c['end']
    if not units or not re.fullmatch(r'[A-Za-z0-9_.-]+',identity):raise ValueError('Invalid script identity or empty cue list.')
    declared=d.get('durationSeconds' if script else 'duration',previous)
    if type(declared) not in (int,float) or not math.isfinite(declared) or declared<=0 or abs(declared-previous)>1e-6:
        raise ValueError('Declared duration must match the complete contiguous source timeline.')
    code="""const fs=require('fs');const x=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(x.units.map(c=>[...new Intl.Segmenter(x.language,{granularity:'sentence'}).segment(c.text)].map(s=>s.segment.trim()).filter(Boolean))));"""
    pieces=json.loads(subprocess.run(['node','-e',code],input=json.dumps({'units':units,'language':language}),check=True,capture_output=True,text=True).stdout)
    for unit,sentences in zip(units,pieces):
        if re.sub(r'\s+','',''.join(sentences))!=re.sub(r'\s+','',unit['text']):raise ValueError('Sentence splitting changed the source text.')
        unit['sentences']=sentences
    return identity,units


def pcm_frames(file):
    with wave.open(str(file)) as f:
        if (f.getframerate(),f.getnchannels(),f.getsampwidth())!=(RATE,1,2):raise ValueError('Unexpected PCM format.')
        return f.getnframes()


def build_unit(text,sentences,voice,seconds,folder,index):
    if seconds<=LEAD+TAIL+1:raise ValueError('Cue window is too short for paced narration.')
    folder.mkdir(parents=True,exist_ok=True)
    cached=folder/f'{index:03d}.sentence-unit.json'
    output=folder/f'{index:03d}.sentence-timed.wav'
    if cached.is_file():
        old=json.loads(cached.read_text('utf-8'))
        if old.get('alignmentMode')==ALIGNMENT and old.get('textSha256')==hashlib.sha256(text.encode()).hexdigest() and old.get('voice')==voice and old.get('windowSeconds')==seconds and output.is_file() and digest(output)==old.get('timedWavSha256'):
            return output,old
    def speak(rate):
        files=[]
        for j,sentence in enumerate(sentences,1):
            source=folder/f'{index:03d}-{j:02d}.txt';source.write_text(sentence+'\n','utf-8')
            raw=folder/f'{index:03d}-{j:02d}-r{rate}.aiff'
            side=raw.with_suffix('.source.sha256')
            identity=hashlib.sha256((voice+'\n'+sentence).encode()).hexdigest()
            if not raw.is_file() or not side.is_file() or side.read_text()!=identity:
                run(['say','-v',voice,'-r',rate,'-f',source,'-o',raw])
                side.write_text(identity)
            files.append(raw)
        return files,sum(duration(f) for f in files)
    # These two installed compact voices consistently reached the calm lower
    # rate bound in the measured pilot; start there to avoid needless resynthesis.
    rate=110 if voice in ('Samantha','Yuna') else 150
    first_rate=rate
    raw,initial=speak(rate)
    target=min(seconds-LEAD-TAIL,seconds*.88)-GAP*(len(sentences)-1)
    if target<=1:raise ValueError('Too many sentences for the chapter window.')
    adjusted=max(110,min(220,round(rate*initial/target)))
    if abs(adjusted-rate)>=2:rate=adjusted;raw,natural=speak(rate)
    else:natural=initial
    available=seconds-LEAD-TAIL-GAP*(len(sentences)-1)
    # Preserve every utterance. A shared tempo keeps a chapter's pace consistent.
    tempo=max(1,natural/available)
    if tempo>1.15:raise ValueError(f'Chapter {index} does not fit at bounded speech speed; no utterance was cut.')
    gap_samples=round(GAP*RATE);lead_samples=round(LEAD*RATE)
    speech_files=[];sentence_reports=[];cursor=lead_samples
    fitted_files=[folder/f'{index:03d}-{j:02d}.speech.wav' for j in range(1,len(raw)+1)]
    # One FFmpeg process fits independent sentences and writes separate WAVs;
    # this preserves exact per-sentence sample counts without process churn.
    args=['ffmpeg','-hide_banner','-loglevel','error','-y']
    for source in raw:args+=['-i',source]
    args+=['-filter_complex',';'.join(f'[{j}:a]atempo={tempo:.9f},aresample={RATE}[s{j}]' for j in range(len(raw)))]
    for j,fitted in enumerate(fitted_files):args+=['-map',f'[s{j}]','-ac','1','-ar',RATE,'-c:a','pcm_s16le',fitted]
    run(args)
    for j,(fitted,sentence) in enumerate(zip(fitted_files,sentences),1):
        n=pcm_frames(fitted)
        sentence_reports.append({'sentenceIndex':j-1,'startSample':cursor,'endSample':cursor+n,
                                 'start':cursor/RATE,'end':(cursor+n)/RATE,'text':sentence,'speechTruncated':False})
        cursor+=n+gap_samples;speech_files.append(fitted)
    end_sample=cursor-gap_samples
    samples=round(seconds*RATE)
    if end_sample>samples-round(TAIL*RATE):raise ValueError('Measured complete sentences overflow chapter; refusing to trim.')
    assembled=folder/f'{index:03d}.sentence-assembled.wav'
    with wave.open(str(assembled),'wb') as f:
        f.setparams((1,2,RATE,0,'NONE','not compressed'));f.writeframes(b'\0'*(2*lead_samples))
        for j,part in enumerate(speech_files):
            with wave.open(str(part)) as q:f.writeframes(q.readframes(q.getnframes()))
            if j+1<len(speech_files):f.writeframes(b'\0'*(2*gap_samples))
        f.writeframes(b'\0'*(2*(samples-end_sample)))
    if pcm_frames(assembled)!=samples:raise ValueError('Assembled chapter sample count mismatch.')
    meter=loudness(assembled)
    normalize=(f'loudnorm=I={TARGET_LUFS}:TP=-1.5:LRA=7:measured_I={meter["input_i"]}:'
               f'measured_TP={meter["input_tp"]}:measured_LRA={meter["input_lra"]}:'
               f'measured_thresh={meter["input_thresh"]}:offset={meter["target_offset"]}:linear=true')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',assembled,'-af',normalize+f',aresample={RATE}',
         '-ac','1','-ar',RATE,'-c:a','pcm_s16le',output])
    if pcm_frames(output)!=samples:raise ValueError('Normalization changed the exact PCM timeline.')
    report={'index':index,'voice':voice,'windowSeconds':seconds,'firstPassSeconds':initial,'firstPassRate':first_rate,'nativeRate':rate,
            'nativeSpeechSeconds':natural,'tempo':tempo,'fittedSpeechSeconds':sum((c['endSample']-c['startSample'])/RATE for c in sentence_reports),
            'leadSeconds':LEAD,'sentenceGapSeconds':GAP,'trailingSpaceSeconds':seconds-end_sample/RATE,
            'textSha256':hashlib.sha256(text.encode()).hexdigest(),'samples':samples,'speechTruncated':False,
            'alignmentMode':ALIGNMENT,'sentences':sentence_reports,'timedWavSha256':digest(output)}
    cached.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    return output,report


def timestamp(seconds):
    ms=round(seconds*1000)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d}.{ms%1000:03d}'


def write_cues(key,language,units,out):
    cues=[]
    origin=units[0]['scriptStart']
    for i,unit in enumerate(units):
        offset=unit['scriptStart']-origin
        for sentence in unit['sentences']:
            cues.append({'start':round(offset+sentence['start'],6),'end':round(offset+sentence['end'],6),
                         'text':sentence['text'],'chapterIndex':i,'sentenceIndex':sentence['sentenceIndex']})
    last=0
    for cue in cues:
        if cue['start']<last or cue['end']<=cue['start']:raise ValueError('Measured sentence cue order is invalid.')
        last=cue['end']
    file=out/(key+'.cues.json')
    file.write_text(json.dumps({'language':language,'alignmentMode':ALIGNMENT,'cues':cues},ensure_ascii=False,indent=2)+'\n','utf-8')
    vtt=out/(key+'.vtt')
    vtt.write_text('WEBVTT\n\n'+'\n'.join(f'{i}\n{timestamp(c["start"])} --> {timestamp(c["end"])}\n{c["text"].replace("-->","→")}\n' for i,c in enumerate(cues,1)),'utf-8')
    return file,vtt,cues


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tour',default='interposer')
    p.add_argument('--languages',nargs='+',choices=VOICES,default=['zh-TW','en'])
    p.add_argument('--full',action='store_true')
    p.add_argument('--chapter',type=int,default=1,help='One-based chapter/cue when --full is absent.')
    p.add_argument('--script',type=Path,help='Optional authored multilingual cue JSON.')
    p.add_argument('--out',type=Path,default=ROOT.parent/'delivery/narration-prototype')
    p.add_argument('--bitrate',choices=['32k','40k','48k','96k'],default='40k',help='AAC mono delivery rate; 40k is the production default.')
    p.add_argument('--discard-wav',action='store_true',help='Keep verified M4A and report, discard the large final PCM WAV.')
    p.add_argument('--keep-work',action='store_true',help='Keep AIFF and temporary chapter WAVs after a successful track.')
    p.add_argument('--force',action='store_true',help='Regenerate even if a verified track matches the unchanged script.')
    a=p.parse_args()
    for name in ('say','ffmpeg','ffprobe','node'):
        if not shutil.which(name):raise ValueError('Missing local tool: '+name)
    if not re.fullmatch(r'[A-Za-z0-9_-]+',a.tour):raise ValueError('Invalid tour ID.')
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
    available=run(['say','-v','?']).stdout
    (out/'voice-inventory.txt').write_text(available,'utf-8')
    result_path=out/'NARRATION_PROTOTYPE_VALIDATION.json'
    prior=json.loads(result_path.read_text()) if result_path.exists() else {'results':[]}
    results={r['id']:r for r in prior['results']}
    for lang in a.languages:
        voice=VOICES[lang]
        if not any(line.startswith(voice+' ') for line in available.splitlines()):raise ValueError('Requested installed voice unavailable: '+voice)
        identity,all_units=read_units(a.tour,lang,a.script)
        if not 1<=a.chapter<=len(all_units):raise ValueError('Chapter outside source script.')
        chosen=all_units if a.full else all_units[a.chapter-1:a.chapter]
        key=f'{identity}.full.{lang}' if a.full else f'{identity}.ch{a.chapter:02d}.{lang}'
        previous=results.get(key)
        if not a.force and previous and previous.get('status')=='PASS' and previous.get('aacBitrate')==a.bitrate and previous.get('voice')==voice and previous.get('alignmentMode')==ALIGNMENT:
            candidate=Path(previous['m4a'])
            unchanged=len(previous.get('units',[]))==len(chosen) and all(
                old.get('textSha256')==hashlib.sha256(c['text'].encode()).hexdigest() and
                old.get('scriptStart')==c['start'] and old.get('scriptEnd')==c['end']
                for old,c in zip(previous['units'],chosen))
            if unchanged and candidate.is_file() and digest(candidate)==previous.get('m4aSha256'):
                # Restore deterministic sentence files if a user removed them.
                write_cues(key,lang,previous['units'],out)
                print(json.dumps({'track':key,'status':'REUSED_VERIFIED','seconds':previous['seconds']}),flush=True)
                continue
        folder=out/'work'/key
        chunks=[];unit_reports=[]
        for i,c in enumerate(chosen,1):
            chunk,report=build_unit(c['text'],c['sentences'],voice,c['end']-c['start'],folder,i)
            report.update({'scriptStart':c['start'],'scriptEnd':c['end']})
            chunks.append(chunk);unit_reports.append(report)
            print(json.dumps({'track':key,'cue':i,'seconds':report['windowSeconds'],'spoken':report['fittedSpeechSeconds']},ensure_ascii=False),flush=True)
        listing=folder/'concat.txt'
        listing.write_text(''.join("file '"+str(x).replace("'","'\\''")+"'\n" for x in chunks),'utf-8')
        wav=out/(key+'.wav')
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',listing,'-c:a','copy',wav])
        total=sum(c['end']-c['start'] for c in chosen)
        with wave.open(str(wav)) as f:
            count=f.getnframes()
            if count!=round(total*RATE):raise ValueError('Full-track sample timeline mismatch.')
        m4a=out/(key+'.m4a')
        # Low-rate AAC can reconstruct peaks above the PCM ceiling. Reserve
        # headroom with a latency-compensated look-ahead limiter, then measure
        # the decoded AAC itself rather than claiming the PCM measurement.
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',wav,'-af','alimiter=limit=0.63:level=false:latency=true:attack=5:release=50',
             '-c:a','aac','-b:a',a.bitrate,'-movflags','+faststart',m4a])
        measured=final_meter(wav)
        if abs(float(measured['input_i'])-TARGET_LUFS)>.6 or float(measured['input_tp'])>-.8:
            raise ValueError('Final narration loudness/true peak outside limits.')
        encoded_meter=final_meter(m4a)
        if abs(float(encoded_meter['input_i'])-TARGET_LUFS)>.8 or float(encoded_meter['input_tp'])>-.5:
            raise ValueError('Encoded AAC loudness/true peak outside limits: '+json.dumps(encoded_meter))
        encoded_seconds=duration(m4a)
        if abs(encoded_seconds-total)>.001:raise ValueError('M4A presentation duration does not match the film timeline.')
        cues_file,vtt_file,cues=write_cues(key,lang,unit_reports,out)
        entry={'alignmentMode':ALIGNMENT,'cuesFile':str(cues_file),'subtitleFile':str(vtt_file),'cues':cues,'id':key,'status':'PASS','language':lang,'voice':voice,'seconds':total,'sampleRate':RATE,'samples':count,
               'channels':1,'wav':None if a.discard_wav else str(wav),'m4a':str(m4a),'m4aSeconds':encoded_seconds,
               'aacBitrate':a.bitrate,'m4aBytes':m4a.stat().st_size,
               'finalLoudnessMeasurement':'EBU R128 with true-peak analysis of decoded waveform',
               'aacHeadroomLimiter':{'limit':.63,'automaticMakeupGain':False,'latencyCompensated':True},
               'integratedLUFS':float(measured['input_i']),'truePeakDBTP':float(measured['input_tp']),
               'aacIntegratedLUFS':float(encoded_meter['input_i']),'aacTruePeakDBTP':float(encoded_meter['input_tp']),
               'wavSha256':digest(wav),'m4aSha256':digest(m4a),'units':unit_reports,
               'qualityReview':'Native synthetic voice; no claim of human narration or native-engineer pronunciation review.'}
        # Independent languages may render concurrently; merge under a file lock.
        with (out/'.validation.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            latest=json.loads(result_path.read_text()) if result_path.exists() else {'results':[]}
            results={r['id']:r for r in latest['results']};results[key]=entry
            temporary=result_path.with_suffix('.tmp')
            temporary.write_text(json.dumps({'status':'PASS','provider':'Installed macOS say voices','networkOrPaidApiUsed':False,
                                              'moviesModified':False,'normalizationTargetLUFS':TARGET_LUFS,'results':list(results.values())},ensure_ascii=False,indent=2)+'\n','utf-8')
            temporary.replace(result_path)
        if a.discard_wav:wav.unlink()
        if not a.keep_work:shutil.rmtree(folder)
        print(json.dumps({'track':key,'status':'PASS','seconds':total,'LUFS':entry['integratedLUFS'],'truePeak':entry['truePeakDBTP']},ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
