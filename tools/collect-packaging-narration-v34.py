#!/usr/bin/env python3
"""Verify and collect the measured native narration deliverables.

Default requires all six tours and all five languages. --partial writes only
currently verified sentence-timed tracks with an explicit PARTIAL status.
--publish-assets also copies those tracks and their cue index into the static
academy, but does not change the existing video or video manifest.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
TOURS=('interposer','fanout','hybrid','bridge','chiplet','thermal')
LANGUAGES=('zh-TW','en','zh-CN','ja','ko')
ALIGNMENT='measured-sentence-pcm-v2'


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for part in iter(lambda:f.read(1024*1024),b''):h.update(part)
    return h.hexdigest()


def check(value,message):
    if not value:raise ValueError(message)


def vtt_texts(file):
    blocks=re.split(r'\n\s*\n',file.read_text('utf-8').strip())
    return ['\n'.join(b.splitlines()[2:]) for b in blocks if '-->' in b]


def expected_timeline(custom=None):
    if not custom:return 300,[{'start':i*30,'end':(i+1)*30} for i in range(10)]
    seconds=custom.get('durationSeconds')
    check(type(seconds) in (int,float) and math.isfinite(seconds) and seconds>0,'An authored process needs a positive finite durationSeconds.')
    chapters=custom.get('cues',[]);check(bool(chapters),'An authored process needs chapter cues.')
    previous=0
    for chapter in chapters:
        check(all(type(chapter.get(k)) in (int,float) and math.isfinite(chapter[k]) for k in ('start','end')),'Chapter timestamps must be finite numbers.')
        check(abs(chapter['start']-previous)<1e-6 and chapter['end']>chapter['start'],'Chapter windows must be contiguous from zero.')
        previous=chapter['end']
    check(abs(previous-seconds)<1e-6,'Declared process duration differs from its chapter timeline.')
    return seconds,chapters


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--delivery',type=Path,default=ROOT.parent/'delivery/narration-v34')
    p.add_argument('--partial',action='store_true')
    p.add_argument('--process-script',type=Path,help='Collect a separate authored process timeline (for example C01 at 300 s or C01-long at 900 s); requires its parent --delivery directory.')
    p.add_argument('--publish-assets',action='store_true')
    p.add_argument('--check-only',action='store_true',help='Verify sources without writing a manifest, audio, or public index.')
    a=p.parse_args();out=a.delivery.resolve();tracks=[];missing=[]
    check(not (a.check_only and a.publish_assets),'--check-only cannot publish assets.')
    custom=json.loads(a.process_script.read_text('utf-8')) if a.process_script else None
    seconds,chapters=expected_timeline(custom);sample_count=round(seconds*48000)
    if custom:
        check(not a.publish_assets,'A separate process must not overwrite the V33 overview narration index.')
        check(re.fullmatch(r'[A-Za-z0-9_-]+',custom['id']),'Unsafe process ID.')
        tours=(custom['id'],);declared=custom.get('languages',list(LANGUAGES));languages=tuple(l for l in LANGUAGES if l in declared)
        check(set(languages)==set(declared) and all(l in c['text'] for c in custom['cues'] for l in languages),'The process has missing or unsupported language text.')
        check(bool(languages),'The process must have complete language scripts.')
        js="const fs=require('fs');const d=JSON.parse(fs.readFileSync(0,'utf8'));const o={};for(const l of d.languages)o[l]=d.cues.flatMap(c=>[...new Intl.Segmenter(l,{granularity:'sentence'}).segment(c.text[l])].map(s=>s.segment.trim()).filter(Boolean));process.stdout.write(JSON.stringify(o));"
        expected=json.loads(subprocess.run(['node','-e',js],input=json.dumps({'languages':languages,'cues':custom['cues']}),check=True,capture_output=True,text=True).stdout)
    else:tours=TOURS;languages=LANGUAGES
    for tour in tours:
        report=out/tour/'NARRATION_PROTOTYPE_VALIDATION.json'
        entries=json.loads(report.read_text())['results'] if report.exists() else []
        for lang in languages:
            key=f'{tour}.full.{lang}'
            r=next((x for x in entries if x['id']==key and x.get('alignmentMode')==ALIGNMENT and x.get('status')=='PASS'),None)
            if not r:missing.append(key);continue
            media=Path(r['m4a']);vtt=Path(r['subtitleFile']);cuefile=Path(r['cuesFile'])
            check(media.is_file() and media.stat().st_size==r['m4aBytes'] and digest(media)==r['m4aSha256'],key+': audio identity mismatch')
            check(r['seconds']==seconds and r['samples']==sample_count and r['sampleRate']==48000,key+': PCM timing mismatch')
            check(abs(r['aacIntegratedLUFS']+16)<=.8 and r['aacTruePeakDBTP']<=-.5,key+': decoded AAC meter exceeds limits')
            probe=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(media)],check=True,capture_output=True,text=True).stdout)
            streams=probe['streams'];check(len(streams)==1 and streams[0]['codec_name']=='aac' and streams[0]['channels']==1 and streams[0]['sample_rate']=='48000',key+': encoded format mismatch')
            check(abs(float(probe['format']['duration'])-seconds)<=.001,key+': encoded duration mismatch')
            cues=json.loads(cuefile.read_text('utf-8'))['cues'];check(cues==r['cues'],key+': cue report differs')
            if custom:
                original=expected[lang]
                check(all(u['textSha256']==hashlib.sha256(c['text'][lang].encode()).hexdigest() for u,c in zip(r['units'],custom['cues'])),key+': authored script changed')
            else:
                old=ROOT/'public/academy/assets/packaging-tour-v33/subtitles'/f'{tour}.{lang}.vtt';original=vtt_texts(old)
            check([c['text'] for c in cues]==original,key+': original subtitle sentence text changed')
            check([c['text'] for c in cues]==vtt_texts(vtt),key+': measured VTT sentence text mismatch')
            check(len(r['units'])==len(chapters),key+': chapter count mismatch')
            last=0;assigned=0
            for ci,chapter in enumerate(chapters):
                unit=r['units'][ci];group=[c for c in cues if c['chapterIndex']==ci]
                check(group and unit['scriptStart']==chapter['start'] and unit['scriptEnd']==chapter['end'],key+': chapter mismatch')
                assigned+=len(group)
                check([c['sentenceIndex'] for c in group]==list(range(len(group))),key+': sentence identity mismatch')
                check(not unit['speechTruncated'] and 110<=unit['nativeRate']<=220 and 1<=unit['tempo']<=1.15,key+': bounded pacing mismatch')
                for c in group:
                    check(c['start']>=last and chapter['start']+.3499<=c['start']<c['end']<=chapter['end']-.4999,key+': measured cue outside chapter')
                    last=c['end']
            check(assigned==len(cues),key+': sentence cue has an unknown chapter')
            coverage=sum(c['end']-c['start'] for c in cues)
            tracks.append({'tourId':tour,'language':lang,'file':str(media.relative_to(out)),'sha256':r['m4aSha256'],'bytes':r['m4aBytes'],
                           'subtitleFile':str(vtt.relative_to(out)),'subtitleSha256':digest(vtt),'cuesFile':str(cuefile.relative_to(out)),
                           'cuesSha256':digest(cuefile),'cues':cues,'seconds':seconds,'samples':sample_count,'sampleRate':48000,'channels':1,
                           'aacBitrate':r['aacBitrate'],'aacTargetBitrate':r['aacBitrate'],'encodedAverageBitrate':int(streams[0].get('bit_rate',0)),'voice':r['voice'],'voiceQuality':'installed macOS compact voice',
                           'integratedLUFS':r['aacIntegratedLUFS'],'truePeakDBTP':r['aacTruePeakDBTP'],'alignmentMode':ALIGNMENT,
                           'subtitleSpeechWindowSeconds':round(coverage,6),'subtitleSilentGapSeconds':round(seconds-coverage,6),'status':'PASS'})
    check(a.partial or not missing,'Incomplete narration: '+', '.join(missing))
    manifest={'version':'33.0.3','status':'PARTIAL' if missing else 'PASS','date':'2026-11-24','alignmentMode':ALIGNMENT,
              'durationSeconds':seconds,'chapterCount':len(chapters),'trackCount':len(tracks),'expectedTrackCount':len(tours)*len(languages),'missing':missing,
              'provider':'Installed macOS compact voices via say; no paid API or downloaded voice model',
              'sentenceTiming':'Measured complete sentence PCM at 48000 Hz after common chapter pace adjustment; silence gaps preserved',
              'speechTruncated':False,'moviesModified':False,
              'qualityLimit':'Synthetic compact speech; professional native-language pronunciation review has not been completed.',
              'tracks':tracks}
    if custom:manifest.update({'processId':custom['id'],'sourceScript':a.process_script.name,'sourceScriptVersion':custom.get('version'),'sourceScriptSha256':digest(a.process_script)})
    target=out/(f'AUDIO_MANIFEST_{custom["id"]}.json' if custom else 'AUDIO_MANIFEST_V34.json')
    if not a.check_only:
        temporary=target.with_suffix('.tmp');temporary.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8');temporary.replace(target)
    if a.publish_assets:
        academy=ROOT/'public/academy';audio=academy/'assets/packaging-tour-v33/audio';audio.mkdir(parents=True,exist_ok=True)
        data={'version':'33.0.3','tours':{}}
        for track in tracks:
            name=f'{track["tourId"]}.{track["language"]}.m4a';dest=audio/name
            if not dest.exists() or digest(dest)!=track['sha256']:
                staging=dest.with_suffix('.m4a.tmp');shutil.copyfile(out/track['file'],staging);staging.replace(dest)
            check(digest(dest)==track['sha256'],'Public audio copy changed')
            data['tours'].setdefault(track['tourId'],{})[track['language']]={'file':'assets/packaging-tour-v33/audio/'+name,'sha256':track['sha256'],'cues':track['cues']}
        index=academy/'packaging-narration-v33.js'
        staged=index.with_suffix('.js.tmp');staged.write_text('/* Verified synthetic narration and measured sentence timing. */\nwindow.MACGYVER_PACKAGING_NARRATION='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n','utf-8');staged.replace(index)
    print(json.dumps({'status':manifest['status'],'trackCount':len(tracks),'bytes':sum(x['bytes'] for x in tracks),'missingCount':len(missing),'manifest':str(target),'manifestWritten':not a.check_only,'durationSeconds':seconds,'chapterCount':len(chapters),'publishedAssets':a.publish_assets},ensure_ascii=False))


if __name__=='__main__':main()
