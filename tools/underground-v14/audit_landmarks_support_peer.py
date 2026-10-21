#!/usr/bin/env python3
"""Peer numerical/physics review by support-course author; read-only to course inputs.
Uses label-keyed physical formulas, not author generator or its audit implementation.
"""
from pathlib import Path
from math import pi,sqrt,isclose,radians
import json,hashlib
P=Path(__file__).resolve().parent
G=9.81

def recalc(k,d):
 if k=='time':return d['length']/d['speed']*60
 if k=='darcy':return d['conductivity']*d['flow area']*d['hydraulic gradient']
 if k=='head':return G*d['head']*d['water density']/1000
 if k=='stress':return 3* d['cover'] * d['rock unit weight']/1000
 if k=='spring':return d['movement']*d['local stiffness']
 if k=='ring':return d['radius']/d['thickness']*d['uniform external pressure']
 if k=='joint':return d['initial compression']-d['tolerance']-d['opening']
 if k=='advance':return d['active penetration']*d['utilisation']*24
 if k=='logistics':return d['payload']*d['vehicles']/(d['cycle']/60)
 if k=='angle':return radians(d['orientation error']/3600)*d['control length']
 if k=='friction':return d['Darcy factor']*d['duct length']/d['hydraulic diameter']*d['air density']*d['mean velocity']**2/2
 if k=='heat':return d['volume flow']*d['air density']*d['specific heat']*d['temperature rise']
 if k=='dynamic':return d['train speed']**2*d['air density']/2
 if k=='sump':return d['usable reserve']/60/d['net inflow']
 if k=='escape':return d['travel distance']/d['walking speed']+d['pre-movement time']
 if k=='reliability':return d['single-unit unavailability']**2
 if k=='coverage':return 100-100*d['missing records']/d['asset count']
 if k=='grade':return d['train mass']*G*d['grade']*d['speed']/1000
 if k=='headway':return 60/(d['occupation']+d['clearance'])
 if k=='thermal':return d['elastic modulus']*1000*d['temperature difference']*d['expansion coefficient']
 if k=='void':return (d['excavated diameter']-d['lining diameter'])*(d['excavated diameter']+d['lining diameter'])*pi/4*d['ring length']
 if k=='rate':return d['movement increment']/d['interval']
 if k=='beam':return d['line load']*d['span']**2/8
 if k=='float':return G*(d['water density']*d['displacement']-d['mass'])/1000
 if k=='settle':return d['differential settlement']/d['baseline']
 if k=='lighting':return d['reflectance']*d['illuminance']/pi
 if k=='diffusion':return sqrt(d['diffusivity']*d['exposure']*86400*365.25)*1000
 if k=='balance':return d['inflow']-d['outflow']-d['other loss']
 if k=='waterfriction':return d['Darcy factor']*d['length']/d['diameter']*d['velocity']**2/(2*G)
 if k=='storage':return (d['inflow']-d['outflow'])*d['interval']*60
 if k=='inventory':return d['gross volume']-d['existing stock']-d['reserve']
 if k=='lift':return d['lifted mass']*G*d['height']/d['time']/d['efficiency']/1000
 if k=='wedge':return d['block volume']*d['unit weight']/d['sharing anchors']
 if k=='advection':return d['reach length']/d['water velocity']/60
 if k=='footprint':return d['storage volume']/d['equivalent height']
 if k=='hydropower':return d['water density']*d['flow']*G*d['drop']/1000
 if k=='levelbias':return d['local plan area']*d['level zero offset']
 if k=='contain':return G*(d['external water density']*d['external head']-d['product density']*d['product head'])/1000-d['gas gauge pressure']
 if k=='flowreduction':return (d['flow before at equal pressure']-d['flow after at equal pressure'])/d['flow before at equal pressure']*100
 raise ValueError(k)

records=json.loads((P/'calculation_landmarks.json').read_text())
ids=['hsuehshan']+[f'b{i}' for i in range(102,126)]
assert len(records)==250 and set(r['courseId'] for r in records)==set(ids)
inputs={cid:json.loads((P/'inputs'/f'{cid}.json').read_text()) for cid in ids}
checks=[];errors=[]
for r in records:
 vals={v['label']:v['value'] for v in r['inputs']}
 base=recalc(r['model'],vals)
 changed=vals.copy();changed[r['inputs'][r['changedIndex']]['label']]*=1.1
 perturbed=recalc(r['model'],changed)
 for label,got,wanted in [('base',base,r['result']),('sensitivity',perturbed,r['changedResult'])]:
  if not isclose(got,wanted,rel_tol=1e-11,abs_tol=1e-11):errors.append([r['courseId'],r['unit'],label,got,wanted])
 u=inputs[r['courseId']]['units'][r['unit']-1]
 halves=u['model'].split('~')
 assert len(halves)==2
 for v in [base,perturbed]:
  assert all(format(v,'.6g') in h for h in halves),(r['courseId'],r['unit'],v)
 assert all('not project measurements or acceptance values' in h for h in halves[1:])
 checks.append(dict(courseId=r['courseId'],unit=r['unit'],kind=r['model'],base=base,sensitivity=perturbed,units=r['unitLabel'],numericResult='pass'))
for cid in ('b107','b108','b119'):
 assert not any('σθ=pr/t' in u['model'] for u in inputs[cid]['units'])
for cid in ('b117','b124','b125'):
 assert not any('t=60L/v' in u['model'] for u in inputs[cid]['units'])
for r in records:
 if r['model']=='contain':assert r['result']>0 and 'inward' in r['boundary']
assert not errors,errors
for r in records:
 if r['model']=='stress':
  text=inputs[r['courseId']]['units'][r['unit']-1]['model']
  assert 'σθ,max' in text and 'sidewall' in text and 'horizontal remote stress' in text
b125stress=next(r for r in records if r['courseId']=='b125' and r['model']=='stress')
assert b125stress['inputs'][0]['value']==120 and isclose(b125stress['result'],9.36)

issues=[dict(id='P1',severity='clarification',scope='all stress models',issue='3*gamma*H is maximum tangential compression for the specified vertical uniaxial remote load, not stress at every wall position.',disposition='Resolved: author rebuilt every stress model with sigma_theta,max, vertical loading, zero horizontal remote stress and sidewall maximum; peer rechecked final inputs.'),dict(id='P2',severity='pedagogical',scope='b125 unit 3',issue='Hypothetical cover of 1220 m is explicit but remote from JTC project depth; a 120 m exercise is more context appropriate.',disposition='Resolved: author changed hypothetical cover to 120 m and regenerated inputs/trace; peer recalculated 9.36 MPa maximum stress and +10 percent sensitivity 10.296 MPa.')]
report=dict(reviewed='2026-10-21',reviewer='courses_support independent peer',scope={'courseIds':ids,'models':250,'baseRecalculations':250,'sensitivityRecalculations':250,'displayComparisons':250,'physics':'All 39 implemented formula types read; all 250 kind/context allocations read; immersed-box, water-route, storage and head-direction mechanisms separately inspected.','limitations':'No source-project design acceptance certified. Public project-source scope rechecked for seven high-risk dimension boundaries; remaining historical metadata relies on separate metadata review.'},errors=errors,issues=issues,sourceBoundaryChecks=[{'course':'b108','claim':'1387 m immersed portion, not the 76.3 km rail corridor','url':'https://holding.gama.com.tr/tr/proje/10273/'},{'course':'b110','claim':'15.1 km whole Aqua-Line road; 1997-12 documented contract completion','url':'https://www.obayashi.co.jp/chronicle/works/d055.html'},{'course':'b116','claim':'55 km base tunnel; 64 km connected underground route','url':'https://www.bbt-se.com/en/brenner-base-tunnel/project-overview/'},{'course':'b117','claim':'6.5 km TBM middle drive within 16.5 km conveyance scope; June 2002 drive breakthrough','url':'https://service.taipower.com.tw/Collection/2009/2025/8709/'},{'course':'b119','claim':'7 km rounded tunnel section, not immersed-only assertion','url':'https://www.hzmb.gov.hk/en/main-bridge.html'},{'course':'b124','claim':'6300 m tunnel waterway','url':'https://www.ktr.mlit.go.jp/edogawa/study/sora/gaikaku/detail/zentai04.html'},{'course':'b125','claim':'1.47 million m3 storage; 150 m below ground is separate from teaching head/cover','url':'https://www.jtc.gov.sg/find-space/jurong-rock-caverns'}],checks=checks,inputSha256={cid:hashlib.sha256((P/'inputs'/f'{cid}.json').read_bytes()).hexdigest() for cid in ids})
(P/'audit_landmarks_support_peer.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Peer arithmetic: 250 base + 250 sensitivity pass; 250 model displays checked; hashes recorded.')
