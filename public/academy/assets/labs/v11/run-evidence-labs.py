#!/usr/bin/env python3
"""Original synthetic evidence labs. Python 3.10+, standard library only.
No network, subprocesses, device access, models or real personal data.
"""
import argparse,hashlib,json,math
from pathlib import Path

def validate_case(name,v):
    def number(key,lo,hi,integer=False):
        value=v[key]
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not lo<=value<=hi or (integer and value!=int(value)):raise ValueError('Invalid bounded input: '+key)
    ranges={
      'pipeline':[('base_cpi',.1,10),('branch_fraction',0,1),('misprediction_rate',0,1),('penalty_cycles',0,1000)],
      'roofline':[('peak_tflops',.01,10000),('bandwidth_gbs',.01,100000),('intensity_flop_byte',0,10000)],
      'dns':[('ttl_s',0,86400),('arrival_per_s',.001,1000000)],
      'queue':[('arrival_per_s',0,1000000),('service_per_s',.001,1000000)],
      'privacy':[('sensitivity',0,1000000),('epsilon',.001,1000)],
      'hydro':[('flow_m3s',0,10000),('net_head_m',0,2000),('efficiency',0,1)],
      'gold':[('dry_ore_t',0,1000000),('grade_gt',0,100),('recovery',0,1)],
      'facility':[('it_mw',0,1000),('pue',1,10)]}
    for row in ranges.get(name,[]):number(*row)
    if name=='quorum':
        number('voters',1,101,True);parts=v['partitions']
        if not isinstance(parts,list) or not 1<=len(parts)<=101 or any(isinstance(p,bool) or not isinstance(p,int) or p<1 for p in parts) or sum(parts)!=v['voters']:raise ValueError('Partitions must cover distinct voters exactly.')
    if name=='alerts':
        counts=v['confusion']
        if not isinstance(counts,dict) or any(isinstance(counts[k],bool) or not isinstance(counts[k],int) or not 0<=counts[k]<=1000000 for k in ['tp','fp','fn','tn']):raise ValueError('Use bounded synthetic confusion counts.')
        if counts['tp']+counts['fp']==0 or counts['tp']+counts['fn']==0 or counts['fp']+counts['tn']==0:raise ValueError('Metric denominator is zero.')
    if name=='privacy':
        eps=v['sequential_epsilons']
        if not isinstance(eps,list) or not 1<=len(eps)<=100 or any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not 0<x<=1000 for x in eps):raise ValueError('Use 1–100 positive finite privacy budgets.')
    if name=='attention':
        q,k,values=v['query'],v['keys'],v['values']
        if not isinstance(q,list) or not 1<=len(q)<=16 or not isinstance(k,list) or not 1<=len(k)<=32 or not isinstance(values,list) or len(values)!=len(k) or not isinstance(values[0],list) or not 1<=len(values[0])<=16:raise ValueError('Invalid attention dimensions.')
        if any(not isinstance(row,list) or len(row)!=len(q) for row in k) or any(not isinstance(row,list) or len(row)!=len(values[0]) for row in values):raise ValueError('Attention matrix dimensions differ.')
        if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or abs(x)>100 for row in [q]+k+values for x in row):raise ValueError('Attention inputs exceed finite model bounds.')
    if name=='neuron':
        number('learning_rate',.001,1);number('epochs',1,2000,True)
        for key in ['train','validation']:
            rows=v[key]
            if not isinstance(rows,list) or not 2<=len(rows)<=256 or any(not isinstance(row,list) or len(row)!=2 or isinstance(row[0],bool) or not isinstance(row[0],(int,float)) or not math.isfinite(row[0]) or abs(row[0])>10 or row[1] not in (0,1) for row in rows):raise ValueError('Use bounded synthetic one-dimensional labeled rows.')

def run_case(name,inputs):
    validate_case(name,inputs)
    if name=='pipeline':
        v=inputs;return {'cpi':v['base_cpi']+v['branch_fraction']*v['misprediction_rate']*v['penalty_cycles'],'units':'cycles/instruction','limit':'No overlapping stalls, cache misses or superscalar effects.'}
    if name=='roofline':
        v=inputs;memory=v['bandwidth_gbs']*v['intensity_flop_byte']/1000
        return {'ceiling_tflops':min(v['peak_tflops'],memory),'memory_ceiling_tflops':memory,'bound':'memory' if memory<v['peak_tflops'] else 'compute','limit':'Ideal bound; not a benchmark or actual GPU throughput.'}
    if name=='quorum':
        voters=inputs['voters'];majority=voters//2+1
        return {'majority':majority,'partition_sizes':inputs['partitions'],'partitions_with_majority':[i for i,p in enumerate(inputs['partitions']) if p>=majority],'max_lost_voters':voters-majority,'limit':'Fixed voters, crash faults, no Byzantine or membership-change model.'}
    if name=='alerts':
        rows=inputs['confusion'];tp,fp,fn,tn=[rows[k] for k in ['tp','fp','fn','tn']]
        return {'precision':tp/(tp+fp),'recall':tp/(tp+fn),'false_positive_rate':fp/(fp+tn),'counts':rows,'limit':'Synthetic labeled alerts. Thresholds and costs are not optimized for production.'}
    if name=='dns':
        ttl=inputs['ttl_s'];rate=inputs['arrival_per_s'];interval=ttl+1/rate
        return {'mean_refresh_interval_s':interval,'refreshes_per_minute':60/interval,'limit':'One cache/key, Poisson requests, fixed TTL, no prefetch or serve-stale.'}
    if name=='queue':
        arrival=inputs['arrival_per_s'];service=inputs['service_per_s'];rho=arrival/service
        if not 0<=rho<1:raise ValueError('M/M/1 requires arrival < service.')
        return {'utilization':rho,'mean_response_s':1/(service-arrival),'p99_response_s':math.log(100)/(service-arrival),'limit':'Stationary M/M/1, exponential independent service, infinite queue, no retries.'}
    if name=='privacy':
        b=inputs['sensitivity']/inputs['epsilon']
        return {'laplace_scale':b,'sum_epsilon_sequential':sum(inputs['sequential_epsilons']),'limit':'Pure-DP Laplace scale and basic sequential composition; no real records or random releases.'}
    if name=='attention':
        q,k,values=inputs['query'],inputs['keys'],inputs['values'];scores=[sum(a*b for a,b in zip(q,row))/math.sqrt(len(q)) for row in k]
        shifted=[math.exp(s-max(scores)) for s in scores];weights=[v/sum(shifted) for v in shifted]
        output=[sum(weights[i]*values[i][j] for i in range(len(values))) for j in range(len(values[0]))]
        return {'scores':scores,'attention_weights':weights,'weighted_value':output,'limit':'One query/head with supplied vectors; no causal mask, positions, projection training or full Transformer.'}
    if name=='neuron':
        train=inputs['train'];w=b=0.;lr=inputs['learning_rate'];history=[]
        def sigmoid(z):return 1/(1+math.exp(-max(-50,min(50,z))))
        def loss(rows):return sum(-(y*math.log(max(1e-12,sigmoid(w*x+b)))+(1-y)*math.log(max(1e-12,1-sigmoid(w*x+b)))) for x,y in rows)/len(rows)
        for epoch in range(inputs['epochs']+1):
            if epoch%20==0:history.append({'epoch':epoch,'train_cross_entropy':loss(train)})
            if epoch==inputs['epochs']:break
            residuals=[(x,sigmoid(w*x+b)-y) for x,y in train];dw=sum(x*r for x,r in residuals)/len(train);db=sum(r for x,r in residuals)/len(train);w-=lr*dw;b-=lr*db
        return {'weight':w,'bias':b,'history':history,'validation_cross_entropy':loss(inputs['validation']),'predictions':[{'x':x,'p_class_1':sigmoid(w*x+b),'label':y} for x,y in inputs['validation']],'limit':'One sigmoid neuron trained on synthetic 1D data. It cannot solve XOR and is not a trained engineering model.'}
    if name=='hydro':
        v=inputs;return {'power_mw':1000*9.81*v['flow_m3s']*v['net_head_m']*v['efficiency']/1e6,'limit':'Steady water balance, constant density/efficiency; no hydraulic transients or operating prescription.'}
    if name=='gold':
        v=inputs;return {'recovered_kg':v['dry_ore_t']*v['grade_gt']*v['recovery']/1000,'limit':'Synthetic dry-ore mass balance; no chemical extraction or mineral-resource estimate.'}
    if name=='facility':
        v=inputs;return {'total_mw':v['it_mw']*v['pue'],'non_it_mw':v['it_mw']*(v['pue']-1),'limit':'Steady PUE accounting, not useful-compute efficiency, carbon or water performance.'}
    raise ValueError('Unknown synthetic case.')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case',default='all');parser.add_argument('--inputs',type=Path,default=Path(__file__).with_name('synthetic-cases.json'));parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.inputs.stat().st_size>256*1024:raise ValueError('Educational input exceeds 256 KiB.')
    raw=args.inputs.read_bytes();data=json.loads(raw);assert data.get('synthetic') is True,'Use explicitly synthetic inputs.'
    cases=data['cases'];selected=cases if args.case=='all' else {args.case:cases[args.case]};outputs={}
    for name,entry in selected.items():
        result=run_case(name,entry['inputs']);outputs[name]=result
        if args.check:
            for key,expected in entry['checks'].items():
                actual=result[key]
                if isinstance(expected,(float,int)):assert math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-9),(name,key,actual,expected)
                else:assert actual==expected,(name,key)
            if name=='neuron':assert result['history'][-1]['train_cross_entropy']<result['history'][0]['train_cross_entropy'] and result['validation_cross_entropy']<.25
    print(json.dumps({'edition':11,'synthetic':True,'input_sha256':hashlib.sha256(raw).hexdigest(),'checked':args.check,'results':outputs},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
