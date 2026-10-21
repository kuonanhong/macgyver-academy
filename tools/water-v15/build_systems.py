#!/usr/bin/env python3
"""Original bilingual water-systems authoring inputs b221–b240; root integrates them."""
import json,pathlib,importlib.util,re,math
H=pathlib.Path(__file__).resolve().parent
T={t['id']:t for t in json.loads((H/'targets.json').read_text())};S={};D={};M={};AUDIT=[]
def pair(z,e):return z+'~'+e
def halves(x):return x.split('~')
def source(k,z,e,p,url,sz,se):S[k]=dict(key=k,title=z,titleEn=e,publisher=p,url=url,sourceType='primary',scope=sz,scopeEn=se)
def meta(cid,**kw):M[cid]=kw
def calc(cid,n,expression,expected,unit,rtol=1e-5):
 value=eval(expression,{'__builtins__':{},'math':math,'max':max,'min':min,'abs':abs})
 assert math.isclose(value,expected,rel_tol=rtol,abs_tol=rtol),(cid,n,value,expected)
 AUDIT.append(dict(course=cid,unit=n,expression=expression,result=value,expected=expected,units=unit,status='PASS'))
def compact(cid,focus,keys,text):
 units=[]
 for line in text.strip().splitlines():
  if not line.strip():continue
  p=[q.strip() for q in line.split('||')];assert len(p)==6,(cid,p)
  title,cause,model,measure,risk,wrong=p
  assert all(q.count('~')==1 for q in p),(cid,title)
  zt,et=halves(title);zc,ec=halves(cause);zm,em=halves(model);zv,ev=halves(measure);zr,er=halves(risk)
  units.append(dict(anchor=title,title=title,mechanism=pair(zc+' '+zm+' '+zr,ec+' '+em+' '+er),model=pair('教學假設，非地標實測值或操作設定：'+zm,'Teaching assumptions, not landmark measurements or operating settings: '+em),verify=measure,failure=risk,misconception=wrong,practice=pair('以'+zt+'編製可交接的證據頁，註明資料時間、單位、模型適用範圍與審查者。'+zv,'Prepare a reviewable evidence sheet for '+et.lower()+', recording data time, units, model applicability and reviewer. '+ev)))
 assert len(units)==10,(cid,len(units));D[cid]=dict(focus=focus,keys=list(dict.fromkeys(keys+(['usace-steel','usace-mechanical'] if int(cid[1:])<=230 else [])))[:5],units=units)
def make(cid,d):
 t=T[cid];m=M[cid];u=d['units'];zf,ef=halves(d['focus']);z0,e0=halves(u[0]['model']);z1,e1=halves(u[1]['model'])
 summary=pair('本課以'+t['title']+'為入口，深入'+zf+'。十個單元各自對應不同的荷載路徑、能量交換或監測問題，從守恆式建立量化估算，再檢查量測配置是否能辨認真正失效原因。工程史實只採用列明範圍的公開一手資料；所有模型輸入另標為教學假設，成果是可追溯的工程判讀紀錄。','Using '+t['titleEn']+' as its entry point, this course examines '+ef.lower()+'. Ten units address different load paths, energy exchanges or monitoring questions, starting with conservation-based estimates and testing whether observations distinguish failure causes. Historical statements use scoped primary evidence. Numerical model inputs are separately identified as teaching assumptions, producing a traceable engineering interpretation record.')
 example=pair('本課原創比較練習分兩個相互獨立的物理模型。'+z0+z1+'先逐一圈出公式內的控制體、力方向或時間尺度，再把每項輸入的量綱換成一致單位。第二人只根據輸入重算結果，不抄第一人的中間數字。最後指出這兩個估算尚未包含的空間變化、非線性及量測誤差；若將結果用於另一座工程，必須重建其幾何、材料與邊界條件，不能挪用本練習的假設。','This original comparison exercise uses two independent physical models. '+e0+' '+e1+' First identify the control volume, force direction or time scale in each relation, then convert every input to consistent units. A second reviewer recalculates from the inputs without copying intermediate numbers. Finally identify spatial variability, nonlinear effects and measurement errors omitted by both estimates. Transfer to another structure requires rebuilding its geometry, material description and boundary conditions; the assumed classroom inputs are not transferable design or operating parameters.')
 if d.get('sensitivity'):
  ze,ee=halves(example);zs,es=halves(d['sensitivity']);example=pair(ze+' '+zs,ee+' '+es)
 vendors=[]
 vendor_keys=m.get('vendorKeys',[d['keys'][0],d['keys'][-1]])
 if S[vendor_keys[0]]['publisher']==S[vendor_keys[-1]]['publisher']:
  vendor_keys=[vendor_keys[0],next(k for k in d['keys'] if S[k]['publisher']!=S[vendor_keys[0]]['publisher'])]
 for key in vendor_keys:
  s=S[key];vendors.append(dict(name=s['publisher'],nameEn=s['publisher'],business='提供相關水工建設、設備或工程技術資料的機構。',businessEn='Organization providing relevant hydraulic infrastructure, equipment or engineering information.',url=s['url'],investorUrl='',security=None,role='本課引用其公開資料作工程教育參照；不據此推定其他地標的承包關係。',roleEn='Its public information is used for engineering education; no contractor relationship with other landmarks is inferred.'))
 return dict(id=cid,title=t['title']+'~'+t['titleEn'],discipline=t['discipline'],family='water',focus=d['focus'],summary=summary,example=example,history=m['history'],units=u,facts=m['facts'],timeline=m['timeline'],codes=m['codes'],landmarks=m['landmarks'],place=m['place'],sources=[S[k] for k in d['keys']],vendors=vendors,related=m.get('related',[f'b{int(cid[1:])-1}',f'b{int(cid[1:])+1}']),architectureNodes=[halves(u[i]['title']) for i in [0,2,4,6,9]],architectureEdges=[[0,1],[1,2],[2,3],[3,4],[4,1]])
def main():
 for p in sorted((H/'authoring_systems').glob('*.py')):
  sp=importlib.util.spec_from_file_location(p.stem,p);mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod);mod.author(compact,source,meta,calc)
 mp=H/'authoring_systems'/'80_misconceptions.py'
 sp=importlib.util.spec_from_file_location('explicit_misconceptions',mp);mm=importlib.util.module_from_spec(sp);sp.loader.exec_module(mm)
 for cid,items in mm.DATA.items():
  if cid in D:
   assert len(items)==10
   for u,wrong in zip(D[cid]['units'],items):u['misconception']=wrong
 vp=H/'authoring_systems'/'81_verification.py'
 sp=importlib.util.spec_from_file_location('verification_additions',vp);vm=importlib.util.module_from_spec(sp);sp.loader.exec_module(vm)
 for cid,items in vm.EXTRA.items():
  if cid in D:
   assert len(items)==10
   for u,extra in zip(D[cid]['units'],items):
    z,e=halves(u['verify']);ze,ee=halves(extra);u['verify']=pair(z+ze,e+' '+ee)
 xp=H/'authoring_systems'/'82_sensitivity.py'
 sp=importlib.util.spec_from_file_location('metadata_sensitivity',xp);xm=importlib.util.module_from_spec(sp);sp.loader.exec_module(xm)
 sensitivity_checks=[]
 for cid,item in xm.DATA.items():
  D[cid]['sensitivity']=item['text']
  results={}
  for label in ['baseline','changed']:
   value=eval(item[label+'Expression'],{'__builtins__':{},'math':math})
   assert abs(value-item[label])<=item['tolerance'],(cid,label,value,item[label])
   results[label+'Computed']=value
  sensitivity_checks.append(dict(courseId=cid,**item,**results,status='PASS'))
 (H/'sensitivity_systems.json').write_text(json.dumps(dict(scope='Metadata example only; one changed parameter with other assumptions held fixed.',checks=sensitivity_checks),ensure_ascii=False,indent=2)+'\n')
 for cid,d in sorted(D.items()):(H/'inputs'/f'{cid}.json').write_text(json.dumps(make(cid,d),ensure_ascii=False,indent=2)+'\n')
 (H/'research_systems.json').write_text(json.dumps(dict(accessed='2026-10-21',courses={cid:d['keys'] for cid,d in D.items()},sources=S,limitations=['Original numerical models use expressly assumed inputs; none is a field control setting.','Public project facts and source scope are kept separate from teaching calculations.','Map locations are approximate context points, not access permissions.','Source institutions are educational associations unless a cited source explicitly supports a role.','This manifest records primary pages retrieved through web search/open; no claim is made of reading unprovided paid documents.']),ensure_ascii=False,indent=2)+'\n')
 (H/'calculations_systems.json').write_text(json.dumps(dict(method='Python independent arithmetic recomputation from explicit original assumptions; physical boundaries also stated in each model.',checks=AUDIT),ensure_ascii=False,indent=2)+'\n')
 print('Written',len(D),'courses;',sum(len(d['units']) for d in D.values()),'units;',len(AUDIT),'calculations PASS')
if __name__=='__main__':main()
