#!/usr/bin/env python3
"""Attach all five subtitle tracks, verify duration, and create real film stills."""
from pathlib import Path
import argparse,json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'public/academy/assets/packaging-tour-v33'
IDS=['interposer','fanout','hybrid','bridge','chiplet','thermal']
LANGS=[('zh-TW','zho','繁體中文'),('en','eng','English'),('ja','jpn','日本語'),('ko','kor','한국어'),('zh-CN','zho','简体中文')]
def run(argv):return subprocess.run(argv,check=True,capture_output=True,text=True).stdout
def main():
 p=argparse.ArgumentParser();p.add_argument('--recordings',type=Path,default=ROOT.parent/'MacGyver_Packaging_Tour_Experiment/recordings');p.add_argument('--tour',choices=IDS,action='append');p.add_argument('--compact',action='store_true',help='Re-encode at 720p/24fps with a 650 kbit/s ceiling for the shared Pages budget');a=p.parse_args()
 (ASSETS/'videos').mkdir(exist_ok=True);(ASSETS/'stills').mkdir(exist_ok=True)
 reports=[]
 for id in a.tour or IDS:
  src=a.recordings/(id+'.mp4');dst=ASSETS/'videos'/(id+'.mp4')
  if not src.is_file():raise FileNotFoundError(src)
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src)]
  for lang,_,_ in LANGS:cmd+=['-i',str(ASSETS/'subtitles'/f'{id}.{lang}.vtt')]
  cmd+=['-f','ffmetadata','-i',str(ASSETS/'transcripts'/f'{id}.ffmetadata'),'-map','0:v:0']
  for i in range(1,6):cmd+=['-map',f'{i}:s:0']
  cmd+=(['-c:v','libx264','-preset','veryfast','-crf','22','-maxrate','650k','-bufsize','1300k','-threads','2','-pix_fmt','yuv420p'] if a.compact else ['-c:v','copy'])
  cmd+=['-c:s','mov_text','-map_chapters','6','-movflags','+faststart']
  for i,(_,lang,title) in enumerate(LANGS):cmd +=[f'-metadata:s:s:{i}',f'language={lang}',f'-metadata:s:s:{i}',f'title={title}',f'-metadata:s:s:{i}',f'handler_name={title}',f'-disposition:s:{i}','default' if i==0 else '0']
  cmd+=[str(dst)];run(cmd)
  meta=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-show_chapters','-of','json',str(dst)]))
  video=[s for s in meta['streams'] if s['codec_type']=='video'];subs=[s for s in meta['streams'] if s['codec_type']=='subtitle']
  assert len(video)==1 and video[0]['codec_name']=='h264' and video[0]['width']==1280 and video[0]['height']==720
  assert abs(float(video[0]['duration'])-300)<.05 and int(video[0]['nb_frames'])==7200
  assert len(subs)==5 and len(meta['chapters'])==10
  for second in [15,135,225]:
   run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(second),'-i',str(dst),'-frames:v','1','-q:v','2',str(ASSETS/'stills'/f'{id}-{second}.jpg')])
  entry={'id':id,'duration':float(video[0]['duration']),'width':1280,'height':720,'fps':'24/1','frames':int(video[0]['nb_frames']),'subtitleLanguages':[l[0] for l in LANGS],'chapters':10,'bytes':dst.stat().st_size,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()};reports.append(entry);print(json.dumps(entry),flush=True)
 (ASSETS/'videos'/'manifest.json').write_text(json.dumps({'version':'33.0.1','date':'2026-11-23','status':'PASS','silent':True,'teachingReconstruction':True,'encoding':'H.264 720p 24fps, CRF 22 with 650 kbit/s ceiling' if a.compact else 'Original browser H.264','videos':reports},ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
