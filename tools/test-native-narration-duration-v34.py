#!/usr/bin/env python3
"""Test 900-second narration assembly using a frozen, reviewed audio fixture.

Requires the already verified interposer English track/report, macOS voice
inventory, Node.js, FFmpeg and Python 3. No new TTS is synthesized. A previously
reviewed 30-second chapter is repeated only inside an automatically deleted
temporary timing fixture; it is never presented as a new teaching film.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]

def load(name,file):
    spec=importlib.util.spec_from_file_location(name,file);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def run(args):return subprocess.run([str(x) for x in args],check=True,capture_output=True,text=True)

def digest(file):
    h=hashlib.sha256()
    with file.open('rb') as f:
        for data in iter(lambda:f.read(1048576),b''):h.update(data)
    return h.hexdigest()

def check(value,message):
    if not value:raise AssertionError(message)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference',type=Path,default=ROOT.parent/'delivery/narration-v34/interposer/NARRATION_PROTOTYPE_VALIDATION.json')
    parser.add_argument('--report',type=Path,default=ROOT.parent/'delivery/narration-audit-v34/DURATION_900_TEST.json')
    a=parser.parse_args()
    native=load('native_narration',ROOT/'tools/build-native-narration-v34.py')
    collector=load('narration_collector',ROOT/'tools/collect-packaging-narration-v34.py')
    ref=next(r for r in json.loads(a.reference.read_text())['results'] if r['id']=='interposer.full.en' and r['status']=='PASS')
    media=Path(ref['m4a']);check(digest(media)==ref['m4aSha256'],'The frozen reference audio changed.')
    transcript=json.loads((ROOT/'public/academy/assets/packaging-tour-v33/transcripts/interposer.en.json').read_text())
    original_text=transcript['chapters'][0]['text'];unit=ref['units'][0]
    check(hashlib.sha256(original_text.encode()).hexdigest()==unit['textSha256'],'Reference wording changed.')
    source_files=[a.reference,media,Path(ref['cuesFile']),Path(ref['subtitleFile'])]
    before={str(p):digest(p) for p in source_files}
    checks=[]
    with tempfile.TemporaryDirectory(prefix='native-duration-test-') as temporary:
        temp=Path(temporary);identity='duration-test-not-a-film';delivery=temp/'delivery';out=delivery/identity
        script={'id':identity,'version':'test-fixture-only','durationSeconds':900,'languages':['en'],
                'cues':[{'id':str(i+1),'start':i*30,'end':(i+1)*30,'text':{'en':original_text}} for i in range(30)]}
        script_file=temp/'fixture.json';script_file.write_text(json.dumps(script),'utf-8')
        _,units=native.read_units(identity,'en',script_file)
        seconds,chapters=collector.expected_timeline(script)
        check(seconds==900 and len(units)==len(chapters)==30 and units[-1]['end']==900,'900-second source timeline was not accepted.')
        checks.append('900-second source with 30 chapters accepted')
        for label,change in [
            ('declared duration does not match chapters',lambda d:d.update(durationSeconds=300)),
            ('gap in chapter timeline',lambda d:d['cues'][12].update(start=361)),
            ('non-finite declared duration',lambda d:d.update(durationSeconds=float('nan'))),
        ]:
            bad=copy.deepcopy(script);change(bad);bad_file=temp/'bad.json';bad_file.write_text(json.dumps(bad),'utf-8')
            for name,action in [('builder',lambda:native.read_units(identity,'en',bad_file)),('collector',lambda:collector.expected_timeline(bad))]:
                try:action()
                except ValueError:pass
                else:raise AssertionError(name+' accepted '+label)
            checks.append('Rejected '+label)
        # Decode one complete reviewed chapter. Its final utterance ends before
        # 29.5 seconds, so this exact 30-second chapter extraction cuts no speech.
        check(unit['sentences'][-1]['end']<=29.5,'Reference chapter lacks a safe tail.')
        base=temp/'reviewed-chapter.wav'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',media,'-t','30','-ar','48000','-ac','1','-c:a','pcm_s16le',base])
        check(native.pcm_frames(base)==1_440_000,'Reference chapter extraction sample count differs.')
        work=out/'work'/f'{identity}.full.en';work.mkdir(parents=True)
        for i in range(1,31):
            cached=copy.deepcopy(unit);cached['index']=i;cached['timedWavSha256']=digest(base)
            target=work/f'{i:03d}.sentence-timed.wav';os.link(base,target)
            (work/f'{i:03d}.sentence-unit.json').write_text(json.dumps(cached),'utf-8')
        native_run=native.run
        def forbid_new_synthesis(args):
            if Path(str(args[0])).name=='say' and list(args[1:])!=['-v','?']:
                raise AssertionError('The timing test must not synthesize unreviewed narration.')
            return native_run(args)
        native.run=forbid_new_synthesis
        saved_argv=sys.argv
        try:
            sys.argv=['build-native-narration-v34.py','--script',str(script_file),'--tour',identity,'--languages','en','--full','--discard-wav','--out',str(out)]
            native.main()
        finally:sys.argv=saved_argv
        result=json.loads((out/'NARRATION_PROTOTYPE_VALIDATION.json').read_text())['results'][0]
        check(result['seconds']==900 and result['samples']==43_200_000 and len(result['units'])==30,'Actual builder output was clipped or kept a five-minute limit.')
        encoded=Path(result['m4a'])
        packets=json.loads(run(['ffprobe','-v','error','-show_packets','-show_entries','packet=pts_time,duration_time','-of','json',encoded]).stdout)['packets']
        final_end=float(packets[-1]['pts_time'])+float(packets[-1]['duration_time'])
        check(abs(final_end-900)<.000003,'AAC packet presentation does not end at 900 seconds.')
        check(native.timestamp(900)=='00:15:00.000','15-minute subtitle formatting failed.')
        check(len(result['cues'])==30*len(unit['sentences']) and result['cues'][-1]['chapterIndex']==29 and result['cues'][-1]['end']>870,'Late-film sentence cues were dropped.')
        checked=run([sys.executable,ROOT/'tools/collect-packaging-narration-v34.py','--delivery',delivery,'--process-script',script_file,'--check-only'])
        summary=json.loads(checked.stdout.strip().splitlines()[-1])
        check(summary['status']=='PASS' and summary['durationSeconds']==900 and summary['chapterCount']==30 and not summary['manifestWritten'],'Generic read-only collector failed the real 900-second fixture.')
        check(not (delivery/f'AUDIO_MANIFEST_{identity}.json').exists(),'--check-only wrote a manifest.')
        checks+=['Actual 900-second AAC presentation and 43,200,000 PCM samples','All 30 chapter groups retained beyond minute five','Dynamic collector accepted 900 seconds without writing a manifest','No new TTS synthesis; only a temporary frozen-audio timing fixture']
        audio_summary={'durationSeconds':900,'chapters':30,'samples':43_200_000,'packetPresentationEndSeconds':final_end,'sentenceCues':len(result['cues']),
                       'aacIntegratedLUFS':result['aacIntegratedLUFS'],'aacTruePeakDBTP':result['aacTruePeakDBTP']}
    check(all(digest(Path(p))==h for p,h in before.items()),'A frozen reference artifact changed during testing.')
    report={'status':'PASS','fixtureOnly':True,'fixtureRemoved':True,'newC01LongNarrationGenerated':False,'newTtsSynthesisCalls':0,
            'frozenReferenceFilesUnchanged':True,'checks':checks,'audioTimingFixture':audio_summary}
    a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({'status':'PASS','tests':len(checks),'durationSeconds':900,'report':str(a.report)},ensure_ascii=False))

if __name__=='__main__':main()
