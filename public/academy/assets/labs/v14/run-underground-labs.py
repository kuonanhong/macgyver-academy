#!/usr/bin/env python3
"""Six synthetic underground-engineering labs; Python 3.10+ standard library only."""
import argparse, hashlib, json, math
from pathlib import Path


def finite(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or (positive and value <= 0):
        raise ValueError(f'{name}: finite {"positive " if positive else ""}number required')
    return value


def settlement(v):
    """Numerical cross-section integration of a Gaussian greenfield trough."""
    D=finite(v['diameter_m'],'diameter',True); width=finite(v['trough_width_m'],'width',True)
    loss=finite(v['volume_loss_percent'],'loss')/100
    if not 0<=loss<=.1: raise ValueError('Synthetic loss domain: 0–10%')
    area=loss*math.pi*D*D/4
    peak=area/(math.sqrt(2*math.pi)*width)
    # Simpson integral over ±6 widths; even interval count and exact SI units.
    n=1200; lo=-6*width; dx=12*width/n
    values=[peak*math.exp(-((lo+j*dx)/width)**2/2) for j in range(n+1)]
    integral=dx/3*(values[0]+values[-1]+sum((4 if j%2 else 2)*values[j] for j in range(1,n)))
    return {'peak_settlement_mm':1000*peak,'lost_area_m2':area,'integrated_trough_area_m2':integral,'relative_balance_error':abs(integral-area)/max(area,1e-20)}


def tbm(v):
    """Calendar budget: cutting shifts are explicit; availability is not applied twice."""
    pen=finite(v['penetration_mm_per_rev'],'penetration',True); rpm=finite(v['rpm'],'rpm',True)
    hours=v['cutting_hours_per_day']; values=[]
    if not hours: raise ValueError('At least one day required')
    for h in hours:
        finite(h,'hours')
        if not 0<=h<=24: raise ValueError('Cutting hours must be between 0 and 24')
        values.append(pen*rpm*60*h/1000)
    ring=finite(v['ring_width_m'],'ring width',True)
    return {'daily_advance_m':values,'total_advance_m':sum(values),'complete_rings':math.floor((sum(values)+1e-10)/ring),'mean_calendar_advance_m_per_day':sum(values)/len(values)}


def drainage(v):
    """Parallel one-dimensional Darcy paths sharing boundary head difference."""
    head=finite(v['head_difference_m'],'head')
    if head<0: raise ValueError('Use nonnegative head magnitude')
    paths=v['paths']; flows=[]
    if not paths: raise ValueError('At least one flow path required')
    for p in paths:
        k=finite(p['conductivity_m_per_s'],'conductivity',True)
        a=finite(p['area_m2'],'area',True); length=finite(p['length_m'],'length',True)
        flows.append(k*a*head/length)
    total=sum(flows)
    return {'path_flows_m3_per_h':[x*3600 for x in flows],'total_flow_m3_per_h':3600*total,'mass_flow_kg_per_s':1000*total,'flow_shares':[x/total if total else 0 for x in flows]}


def ventilation(v):
    """Fan curve a-bQ² intersects system curve RQ²; solve by bracketed bisection."""
    a=finite(v['fan_shutoff_pa'],'fan shutoff',True); b=finite(v['fan_curve_coefficient'],'fan coefficient',True)
    R=finite(v['system_resistance'],'resistance',True); eta=finite(v['efficiency'],'efficiency',True)
    if eta>1: raise ValueError('Efficiency must not exceed one')
    lo=0; hi=math.sqrt(a/b)
    for _ in range(80):
        q=(lo+hi)/2
        if a-b*q*q-R*q*q>0:lo=q
        else:hi=q
    q=(lo+hi)/2; pressure=R*q*q
    return {'operating_flow_m3_per_s':q,'system_pressure_pa':pressure,'shaft_power_kw':pressure*q/eta/1000,'curve_residual_pa':a-b*q*q-pressure}


def convergence(v):
    """Fit u(t)=U[1-exp(-t/tau)] by bounded grid search and analytic least squares U."""
    obs=v['observations']; times=[finite(row[0],'time',True) for row in obs]
    values=[finite(row[1],'closure') for row in obs]
    if len(obs)<3 or len(set(times))<3: raise ValueError('Need three distinct positive times')
    if any(x<0 for x in values): raise ValueError('This synthetic closure model requires nonnegative values')
    candidates=[]
    for j in range(10,301):
        tau=j/10; x=[-math.expm1(-t/tau) for t in times]; U=sum(a*b for a,b in zip(x,values))/sum(a*a for a in x)
        mse=sum((U*a-b)**2 for a,b in zip(x,values))/len(x); candidates.append((mse,tau,U))
    mse,tau,U=min(candidates)
    return {'fitted_limit_mm':U,'fitted_tau_days':tau,'rmse_mm':math.sqrt(mse),'forecast_day30_mm':U*(-math.expm1(-30/tau)),'at_search_boundary':tau in (1,30)}


def consolidation(v):
    """Average degree of 1-D consolidation, uniform initial excess pressure."""
    cv=finite(v['cv_m2_per_day'],'cv',True); H=finite(v['drainage_path_m'],'drainage path',True)
    rows=[]
    for t in v['times_days']:
        finite(t,'time')
        if t<0:raise ValueError('Time must be nonnegative')
        T=cv*t/(H*H)
        # Short-time asymptote avoids finite-series truncation near t=0.
        U=2*math.sqrt(T/math.pi) if T<.001 else 1-sum(8/(math.pi**2*(2*j+1)**2)*math.exp(-(2*j+1)**2*math.pi**2*T/4) for j in range(2000))
        rows.append({'time_days':t,'time_factor':T,'average_degree_percent':100*U})
    return {'t90_days':.848*H*H/cv,'history':rows}

LABS={'settlement':settlement,'tbm':tbm,'drainage':drainage,'ventilation':ventilation,'convergence':convergence,'consolidation':consolidation}
ASSUMPTIONS={
 'settlement':'Greenfield Gaussian trough; no building interaction or groundwater settlement. Synthetic geometry; not a project prediction.',
 'tbm':'Constant active penetration and speed. Input cutting hours already exclude downtime. No logistics simulation or schedule guarantee.',
 'drainage':'Homogeneous independent saturated paths, steady laminar flow, equal head difference. No fracture turbulence or 3-D excavation inflow.',
 'ventilation':'Synthetic fixed-speed fan and fixed incompressible system; no smoke-control, exposure or emergency design.',
 'convergence':'Synthetic exponential curve, grid tau 1–30 days. Extrapolation cannot diagnose stability or authorize excavation.',
 'consolidation':'Terzaghi 1-D, uniform initial excess pore pressure, constant cv, maximum drainage path H. No secondary compression.'}


def check():
    # Independent exact values, conservation and physical scaling relationships.
    s=settlement({'diameter_m':6,'trough_width_m':10,'volume_loss_percent':1}); assert abs(s['peak_settlement_mm']-11.2798272358395)<1e-8; assert s['relative_balance_error']<3e-9
    t=tbm({'penetration_mm_per_rev':5,'rpm':2,'cutting_hours_per_day':[10,0,5],'ring_width_m':1.5}); assert t['total_advance_m']==9 and t['complete_rings']==6
    d=drainage({'head_difference_m':10,'paths':[{'conductivity_m_per_s':.0001,'area_m2':20,'length_m':20},{'conductivity_m_per_s':.0001,'area_m2':20,'length_m':20}]}); assert abs(d['total_flow_m3_per_h']-7.2)<1e-12;assert d['flow_shares']==[.5,.5]
    v=ventilation({'fan_shutoff_pa':1000,'fan_curve_coefficient':.2,'system_resistance':.2,'efficiency':.8});assert abs(v['operating_flow_m3_per_s']-50)<1e-10;assert abs(v['shaft_power_kw']-31.25)<1e-10;assert abs(v['curve_residual_pa'])<1e-9
    fit=convergence({'observations':[[t,20*(-math.expm1(-t/5))] for t in [1,2,5,10,20]]});assert fit['fitted_tau_days']==5;assert abs(fit['fitted_limit_mm']-20)<1e-10
    c=consolidation({'cv_m2_per_day':.01,'drainage_path_m':5,'times_days':[0,2120]});assert abs(c['t90_days']-2120)<1e-9;assert abs(c['history'][1]['average_degree_percent']-90)<.01
    tiny=consolidation({'cv_m2_per_day':1,'drainage_path_m':1,'times_days':[0,1e-14]});assert tiny['history'][0]['average_degree_percent']==0;assert abs(tiny['history'][1]['average_degree_percent']-1.1283791670955126e-5)<1e-16
    half=consolidation({'cv_m2_per_day':.01,'drainage_path_m':2.5,'times_days':[]});assert abs(half['t90_days']-530)<1e-9
    try:ventilation({'fan_shutoff_pa':1000,'fan_curve_coefficient':.2,'system_resistance':.2,'efficiency':1.1})
    except ValueError:pass
    else:raise AssertionError('Invalid efficiency accepted')
    return 'PASS: six labs; exact values, mass/volume balance, scale relationships and domain check.'


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');parser.add_argument('--cases',type=Path,default=Path(__file__).with_name('synthetic-cases.json'));parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.check:print(check());return
    cases=json.loads(args.cases.read_text('utf-8')); result={}
    if set(cases)!=set(LABS):raise ValueError('Exactly six named cases required')
    for key,fn in LABS.items():
        raw=json.dumps(cases[key],sort_keys=True,separators=(',',':')).encode();result[key]={'input_sha256':hashlib.sha256(raw).hexdigest(),'synthetic':True,'assumptions':ASSUMPTIONS[key],'inputs':cases[key],'results':fn(cases[key])}
    output=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    if args.output:args.output.write_text(output,'utf-8')
    else:print(output,end='')

if __name__=='__main__':main()
