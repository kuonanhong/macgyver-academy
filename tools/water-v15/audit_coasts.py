#!/usr/bin/env python3
"""Author recomputation of declared synthetic coastal models; not independent design approval."""
import ast,hashlib,json,math
from pathlib import Path
from decimal import Decimal
H=Path(__file__).resolve().parent
ROWS=r'''
b281|1|(5/25,10/math.sqrt(25))|(.20,2.)|m,s|Gravity similarity only; Reynolds/Weber and air effects need separate review.
b281|2|(25**1.5*.0004,25**1.5*.0004*1000)|(.050,50.)|m2/s,L/s/m|Unit-width discharge scales as length^1.5, not total flow length^2.5.
b281|3|(.03/(.5*120),)|(.0005,)|m2/s|Closed collection balance and effective width/time.
b281|4|(4*math.sqrt(.0025),)|(.20,)|m|Spectral significant height, not maximum individual height.
b281|5|(.10/.20,(.10-.02)/.20)|(.50,.40)|ratios|Fixed crest and incident-height assumption; depth changes also need recalibration.
b281|6|(.20/.50,(.20/.50)**2)|(.40,.16)|ratios|Separated amplitudes and matched propagation conditions for energy square.
b281|7|(20/2,20*2)|(10.,40.)|Hz,points|Ideal Nyquist is not usable bandwidth or proof of impact resolution.
b281|8|(2/math.sqrt(9.81*.3),)|(1.17,)|Froude|Local flow regime, not access safety.
b281|9|((.4+.5+.6)/3,math.sqrt((.1**2+.1**2)/2),.1/math.sqrt(3))|(.5,.1,.0577)|L/s/m|Sample deviation with n-1; independent realizations only.
b281|10|(100/.020/1000,)|(5.,)|kPa|Uniform instantaneous area-average, not a local pressure spike.
b282|1|((2650-1025)*9.81*2/1000,)|(31.8825,)|kN|Individual displaced volume, not loose bulk stockpile volume.
b282|2|(2650/1025-1,3/(2650/1025-1))|(1.5854,1.892)|ratios|Indicator has no universal acceptance threshold.
b282|3|((100-60)/100,(100-60)/60)|(.40,.667)|fractions|Porosity differs from void ratio; connectivity separate.
b282|4|(10*2,math.sqrt(10**2+20**2))|(20.,22.36)|m|Horizontal run differs from slope length.
b282|5|(4/1,)|(4.,)|ratio|Grading ratio alone does not satisfy every filter criterion.
b282|6|((5000/2650)**(1/3),)|(1.2357,)|m|Cube-root volume nominal diameter, not longest axis.
b282|7|(.5*1025*1*2*2**2,.5*1025*1*2*2**2/1000)|(4100.,4.1)|N,kN|Steady drag only; inertia, turbulent peaks and changing exposure excluded.
b282|8|(.02*3,)|(.060,)|m|Uniform layer strain only; differential/other-layer settlement excluded.
b282|9|(100/(2*math.cos(math.radians(30))),)|(57.74,)|kN|Symmetric static slings with angle from vertical; no field lifting setting.
b282|10|(8/1**2,)|(8.,)|dimensionless|Damage area normalized by Dn² is not a percentage.
b283|1|(2400*1000,2400*1000*9.81/1000)|(2400000.,23544.)|kg,kN|Concrete volume is not buoyant envelope volume.
b283|2|(2460000/(1025*400),10-2460000/(1025*400))|(6.,4.)|m|Sealed rectangular waterplane and calm-water draft/freeboard.
b283|3|(3+(20*20**3/12)/2400-7,)|(1.556,)|m|Small-angle GM, not complete righting-arm stability.
b283|4|((10*10**3/12)/2400,)|(.3472,)|m|Part-filled connected free surface; tank liquid matches surrounding density.
b283|5|(205000/(1025*400),)|(.50,)|m|Fixed waterplane and sealed body; mean draft only.
b283|6|((80+20)*20/2,)|(1000.,)|kN/m|Assumed linear static base pressure; time and intermediate peaks excluded.
b283|7|(.6*(4000-1000),.6*(4000-1000)/1500)|(1800.,1.20)|kN,ratio|Effective normal load and assumed friction; not code safety factor.
b283|8|(4000/2000,12/6,2000/12*(1+6*2/12),2000/12*(1-6*2/12))|(2.,2.,333.3,0.)|m,m,kPa,kPa|Rectangular linear full-contact boundary; ground tension not allowed.
b283|9|(.020/20,math.degrees(.020/20))|(.001,.0573)|rad,degrees|Small rigid-body rotation only.
b283|10|(1025*9.81/1000,(1025*9.81/1000)*(8**2-6**2)/2)|(10.05525,140.7735)|kN/m3,kN/m|Two static pressure triangles on same base; no tsunami/suction/scour claim.
b284|1|(3000/2400,(2400-1025)*9.81*(3000/2400)/1000)|(1.25,16.86)|m3,kN|Material volume and submerged weight; no proprietary product specification.
b284|2|((170-8)/340,)|(.4765,)|ratio|Absorbed water removed from effective water, no surface water assumed.
b284|3|(1e-5*25*2,1e-5*25*2*1000)|(.0005,.50)|m,mm|Uniform free thermal movement, no restraint or gradient stress.
b284|4|(25e9*1e-5*25/1e6,)|(6.25,)|MPa|Fully restrained linear elastic cooling; creep and cracking excluded.
b284|5|(900000/.15**2/1e6,)|(40.,)|MPa|Cube nominal compressive strength, not characteristic/design strength.
b284|6|(3000*9.81/(2*math.cos(math.radians(45)))/1000,)|(20.81,)|kN|Symmetric static slings45degrees from vertical; no dynamic/attachment approval.
b284|7|(200/1000,)|(.20,)|units/m2|Placement density is not porosity or complete interlocking evidence.
b284|8|(math.sqrt(.10**2+.20**2+.05**2),)|(.2291,)|m|Position-vector magnitude, not orientation error.
b284|9|(3000/20**3,)|(.375,)|kg|Equal material density with geometric length ratio20; contact/roughness separate.
b284|10|((1-.95)/1*100,)|(5.,)|percent|Specified abrasion test, not annual service-life rate.
b285|1|(1000*20*1.5,)|(30000.,)|m3|Rectangular geometry, not an equilibrium-profile design.
b285|2|(10000*(1-.4)*2650,)|(15900000.,)|kg|Dry grain mass excludes pore water.
b285|3|(.45/.30,)|(1.50,)|ratio|Median ratio does not prove full grading compatibility.
b285|4|(30000/(1000*(5+2)),)|(4.286,)|m|Assumed parallel translation across fixed active-profile height.
b285|5|(30000-45000,(30000-45000)*5)|(-15000.,-75000.)|m3/year,m3|Stationary alongshore-only budget.
b285|6|(18000/(1-.4),18000/(1-.35))|(30000.,27692.3)|m3|Fixed solid volume, changing porosity, no export implied.
b285|7|(20000-8000,8000/20000*100)|(12000.,40.)|m3,percent|Fixed survey limits, no proof of permanent export.
b285|8|(100000*math.sqrt(2)*.03,)|(4242.6,)|m3|Independent coherent offsets between epochs, not independent cells.
b285|9|((150-20)/1000,(150-20)/1000*2)|(.13,.26)|kg/m3,kg/s|Uniform background-corrected section concentration, not permit criterion.
b285|10|(3/.02,.3*3/.02)|(150.,45.)|s,m|Constant velocity and settling, no turbulence or resuspension.
b286|1|(2-1.2,(2-1.2)/1.6)|(.8,.50)|m,ratio|Common datum and fixed height; not transmission coefficient.
b286|2|(.8/2,(.8/2)**2*.8)|(.40,.128)|ratios|Equal density, energy ratio includes group-speed ratio.
b286|3|(.78*2,)|(1.56,)|m|Selected breaker index, not universal acceptance limit.
b286|4|(30/20,)|(1.50,)|m/s|Section average, not local peak.
b286|5|(1025*9.81*2**2/8,1025*9.81*2**2/8*5/1000)|(5027.6,25.138)|J/m2,kW/m|Regular linear wave, spectral significant height requires different coefficient.
b286|6|(2/((2650-1025)*9.81*.0005),)|(.2509,)|Shields|Noncohesive grain forcing, not scour depth or prescribed threshold.
b286|7|(math.sqrt(9.81*2),100/math.sqrt(9.81*2))|(4.429,22.58)|m/s,s|Linear shallow-water long wave only.
b286|8|(100/200,)|(.50,)|ratio|Geometry alone does not predict tombolo formation.
b286|9|(.8+.2,.2/.8*100)|(1.,25.)|m,percent|Fixed water level, not a proportional transmission change.
b286|10|((2+math.sqrt(9.81*2))*.5/5,)|(.6429,)|Courant|Selected explicit1D shallow-water illustration, not stability guarantee.
b287|1|((120+180)*50/2,)|(7500.,)|m3|Trapezoidal integration assumes linear section-area change.
b287|2|((1300-1000)/(2650-1000),)|(.1818,)|volume fraction|Two additive phases, excludes gas and variable density.
b287|3|(2650*.15*2,2650*.15*2*3600)|(795.,2862000.)|kg/s,kg|Uniform synchronized concentration and flow for one operating hour.
b287|4|(.02*(500/.5)*3**2/(2*9.81),)|(9.174,)|m|Clear-water Darcy baseline, slurry and fittings excluded.
b287|5|(1300*9.81*2*20/.7/1000,)|(728.7,)|kW|Total illustrative efficiency, matched operating point.
b287|6|(1500*.020/2,1500*.020/2+1)|(15.,16.)|m|Vertical beam uniform sound speed; range plus transducer draft, before chart datum.
b287|7|(math.sqrt(.05**2+.08**2+.04**2),)|(.1025,)|m|Independent zero-mean standard components, systematic/coverage separate.
b287|8|(15-13-.5-.4-.2,)|(.9,)|m|Synthetic clearance budget, never navigation authorization.
b287|9|(600*60/40*.75,)|(675.,)|m3/h|Availability separately defined, accepted volume not hopper capacity.
b287|10|(2*.5,(100-2*.5)/100*100)|(1.,99.)|kg/s,percent|Period retention, not environmental compliance.
b288|1|(6500+3000+500,6500/10000*100)|(10000.,65.)|t,percent|Common dry-mass basis and only verified sand counted reused.
b288|2|(12000/60000,)|(.20,)|m|Uniform retained post-drainage layer, consolidation excluded.
b288|3|(1*(1+1)/(1+2),1-1*(1+1)/(1+2))|(.667,.333)|m|One-dimensional fixed solids, no foundation/lateral/organic loss.
b288|4|(math.acos(.5/1)/math.pi,)|(0.3333333333333333,)|fraction|Sinusoidal tide and no ponding, not survival probability.
b288|5|(540/600*100,540/600*100)|(90.,90.)|percent|Recovery feed-sand denominator versus purity product-total denominator happen to match.
b288|6|(1000*1000*20/1e6,20*1e6/(2000*1000))|(20.,10.)|kg,mg/kg|Tracer conserved, not dilution-to-compliance method.
b288|7|(.5-.08-.04,)|(.38,)|m|Uniform geometric accounting, no chemical isolation guarantee.
b288|8|(50-35,50-(35-10))|(15.,25.)|kPa|Fixed total stress for second state; not shear strength.
b288|9|(10000*(50-20)*.08,)|(24000.,)|kgCO2e|Synthetic transport factor, excludes full life cycle and return effects.
b288|10|((50-30)-(50-40),)|(10.,)|percentage points|Difference-in-differences requires comparable controls and parallel trends.
b289|1|(math.tan(math.radians(45-30/2))**2,)|(.3333,)|Ka|Level cohesionless fill, smooth vertical wall, mobilized active state.
b289|2|((1/3)*10*15**2/2,15/3)|(375.,5.)|kN/m,m|Effective soil triangle, pore-water pressure separate.
b289|3|((1/3)*30,(1/3)*30*15)|(10.,150.)|kPa,kN/m|Infinite uniform surcharge only, not wheel load.
b289|4|(10.05525*(5**2-3**2)/2,)|(80.442,)|kN/m|Two hydrostatic triangles share same base; no transient seepage.
b289|5|(3000/15*(1+6*1.5/15),3000/15*(1-6*1.5/15))|(320.,80.)|kPa|Rectangular linear full contact; effective force excludes uplift.
b289|6|(.5*20000000*.1**2*.8/1000,)|(80.,)|kJ|Mass already includes added mass, normal velocity, selected synthetic factor.
b289|7|(.5*1000*.3,)|(150.,)|kJ|Linear loading work, unloading dissipation not given.
b289|8|(300000*.2*9.81/1000,)|(588.6,)|kN/m|Participating mass per metre only, soil-water dynamics separate.
b289|9|(100*5/10000,)|(.050,)|m|Uniform1D constrained-modulus layer, not whole site.
b289|10|(15/500,15/500*100)|(.030,3.)|strain,percent|Actual seal gauge length and uniaxial movement; no waterproofing qualification.
b290|1|(math.pi*(1**2-.96**2)/4,2000000/(math.pi*(1-.96**2)/4)/1e6)|(.061575,32.48)|m2,MPa|Annular steel area, mean axial stress only.
b290|2|(5e6*math.pi*1**2/4/1000,)|(3927.0,)|kN|Closed toe with assumed uniform pressure, unverified open pile plug excluded.
b290|3|(math.pi*50*1*20,)|(3141.6,)|kN|Uniform positive shaft shear, no downdrag or toe resistance.
b290|4|(12000/4+12000*3/(4*3**2),12000/4-12000*3/(4*3**2))|(4000.,2000.)|kN|Rigid cap, four equal axial stiffnesses, two piles each side.
b290|5|(2e6*30/(200e9*.060),2e6*30/(200e9*.060)*1000)|(.005,5.)|m,mm|Uniform axial-force rod, actual shaft transfer requires integration.
b290|6|(100e3*10**3/(3*200e9*.0074)*1000,100*10)|(22.52,1000.)|mm,kNm|Ideal fixed cantilever, not a real mudline fixity.
b290|7|((10/12)**3,(1-(10/12)**3)*100)|(.5787,42.13)|ratio,percent|ConstantEI effective cantilever comparison, not full pile-soil model.
b290|8|(.5*1025*1.2*1*2**2/1000,)|(2.460,)|kN/m|Steady drag only, phase-resolved inertia excluded.
b290|9|((1-.966**2)/(1-.960**2),)|(.8526,)|area ratio|Fixed outside diameter and inner-face loss, not service-life fraction.
b290|10|(100000/1000000+200000/500000,)|(.50,)|Miner fraction|Linear damage with selected curves, no remaining-life guarantee.
b291|1|(10250/(1025*100),)|(.10,)|m|Constant waterplane uniform added load, no heel or waves.
b291|2|(.5*1.225*1.2*100*20**2/1000,)|(29.40,)|kN|Selected wind definition and coefficient, not operational limit.
b291|3|(.5*1025*1*20*1.5**2/1000,)|(23.0625,)|kN|Uniform steady current, no wave inertia.
b291|4|(40/(2*math.cos(math.radians(30))),)|(23.094,)|kN|Two taut horizontal symmetric lines, no pretension/dynamics.
b291|5|(25*20/5000,)|(.10,)|m|Straight elastic incremental line response, no slack or creep.
b291|6|(math.sqrt(10**2+1**2),math.sqrt(10**2+3**2),math.sqrt(109)-math.sqrt(101))|(10.0499,10.4403,.3904)|m|Chord geometry only, not catenary tension.
b291|7|(10/(20+30),)|(.20,)|m|Collinear engaged parallel small-increment stiffnesses.
b291|8|(2*math.pi*math.sqrt(100000/50000),)|(8.886,)|s|Effective mass includes added mass; undamped linear1DOF period only.
b291|9|(1.2/12*100,math.degrees(math.atan(1.2/12)),math.sqrt(12**2+1.2**2))|(10.,5.711,12.0599)|percent,degrees,m|Horizontal run distinct from span; no accessibility compliance claim.
b291|10|(120*1025-100000,)|(23000.,)|kg|Theoretical reserve to full immersion, not allowable added load.
b292|1|(300*30*10,)|(90000.,)|m3|Empty rectangular chamber, no savings basin/vessel geometry.
b292|2|(90000/150,90000/150/60)|(600.,10.)|s,min|Interval mean discharge, not constant instantaneous flow.
b292|3|(150/9000,150/9000*60)|(.01667,1.)|m/s,m/min|Spatial mean rise, not local uniformity.
b292|4|(.7*8*math.sqrt(2*9.81*5),)|(55.465,)|m3/s|Fixed orifice quasi-steady relation excludes acceleration.
b292|5|(2*9000*(math.sqrt(10)-math.sqrt(.1))/(.7*8*math.sqrt(2*9.81)),)|(2065.3,)|s|Fixed upper reservoir/opening and no inertia; residual head not gate instruction.
b292|6|(3*4**2/(2*9.81),)|(2.446,)|m|All coefficients share reference velocity.
b292|7|(1000*20*4/1000,)|(80.,)|kN|Complete stopping of chosen component, pressure forces neglected, not vessel force.
b292|8|(1000*900*1/1000,2*300/900)|(900.,.667)|kPa,s|Velocity change rapid relative to round-trip wave time.
b292|9|((80000-2300)/(.5*1000*10**2),)|(1.554,)|cavitation index|Absolute pressure; no universal threshold claimed.
b292|10|(10000000*9.81*(.05/200)/1000,)|(24.525,)|kN|Long-wave small hydrostatic gradient, drag/acceleration excluded.
b294|1|(1000*9.81*(8**2-6**2)/2/1000,)|(137.34,)|kN/m|Same-base hydrostatic triangles, not actuator thrust.
b294|2|(10/math.cos(math.radians(20)),10*math.tan(math.radians(20)))|(10.6418,3.6397)|m|Leaf angle measured from transverse; hinge details excluded.
b294|3|(100*.5**2/8,6*3125/.020**2/1e6)|(3.125,46.875)|kNm/m,MPa|Unit-width simply supported strip; two-way plate effects excluded.
b294|4|((200000-1000*50)*9.81/1000,)|(1471.5,)|kN|Sealed displaced envelope volume, vertical resultant not bearing distribution.
b294|5|(1.5e6/(.3*.4)/1e6,)|(12.50,)|MPa|Projected bearing pressure, not Hertz contact peak.
b294|6|(.003/15,math.degrees(.003/15))|(.0002,.01146)|rad,degrees|Two-point mean inclination; bowing cannot be inferred.
b294|7|(12e-6*15*20*1000,)|(3.60,)|mm|Uniform free temperature change, no restraint or gradients.
b294|8|(200/(2*math.sin(math.radians(30))),)|(200.,)|kN|Selected torque geometry, not an operating setting.
b294|9|(10e6*math.pi*.16**2/4/1000,)|(201.062,)|kN|Cap-end force without backpressure or friction; rod area differs on retraction.
b294|10|(.6*.002*math.sqrt(2*9.81*2)*1000,)|(7.517,)|L/s|Synthetic equivalent orifice, not allowable leakage.
b295|1|(10*35/(100+10),)|(3.1818,)|kg/m3|Additive volumetric fully mixed streams, not PSU or conductance.
b295|2|(20*15,)|(300.,)|kg/s|Uniform synchronized section concentration; otherwise integrate uC.
b295|3|(1e6*2,100*(5-2)/1e6)|(2000000.,.0003)|kg,kg/m3/s|Fixed box with equal inflow/outflow, derivative only instantaneous.
b295|4|(1e6/100*math.log(5),1e6/100*math.log(5)/3600)|(16094.4,4.471)|s,h|Well-mixed fixed box, fresh replacement and no salt reentry.
b295|5|(9.81*20/1000,math.sqrt((9.81*20/1000)*4*6/(4+6)))|(.1962,.6862)|m/s2,m/s|Two-layer rigid-lid small-amplitude long wave with stratification observed.
b295|6|(.1962*2/.5**2,)|(1.5696,)|bulkRi|Bulk parameter not a local gradient stability threshold.
b295|7|(500*43200/math.pi,)|(6875494.,)|m3|Positive half-cycle sinusoidal prism, full-cycle net zero not renewal.
b295|8|(10*20,10*5,(10*20)/(10*5))|(200.,50.,4.)|kg/s,kg/s,ratio|Equal volume discharges, local export not whole-system success.
b295|9|(2*1.5**2/(2*9.81),)|(.2294,)|m|Chosen clear-water local-loss coefficient, not IJmuiden field value.
b295|10|(3.20-3.00,(3.20-3.00)/3.00*100)|(.20,6.667)|kg/m3,percent|Same-sample bias against traceable reference; not environmental trend.
'''
SENSITIVITIES={'b281':('(10/math.sqrt(27.5),(10/math.sqrt(27.5)/2-1)*100)','(1.9069,-4.65)','s,percent'),'b282':('((2650-1025)*9.81*2.2/1000,)','(35.07075,)','kN')}
SENSITIVITIES['b283']=('(2400*1100*9.81/1000,)','(25898.4,)','kN')
SENSITIVITIES['b284']=('(3300/2400,(2400-1025)*9.81*(3300/2400)/1000)','(1.375,18.54703)','m3,kN')
SENSITIVITIES['b285']=('(1000*22*1.5,)','(33000.,)','m3')
SENSITIVITIES['b286']=('(2.2-1.2,(2.2-1.2)/1.6,((2.2-1.2)/.8-1)*100)','(1.,.625,25.)','m,ratio,percent')
SENSITIVITIES['b287']=('((120+198)*50/2,((120+198)/(120+180)-1)*100)','(7950.,6.)','m3,percent')
SENSITIVITIES['b288']=('(7150+3000+500,7150/(7150+3000+500)*100)','(10650.,67.14)','t,percent')
SENSITIVITIES['b289']=('(math.tan(math.radians(45-33/2))**2,(1-math.tan(math.radians(45-33/2))**2/(1/3))*100)','(.2948,11.56)','Ka,percent')
SENSITIVITIES['b290']=('(math.pi*(1.1**2-1.06**2)/4,2000000/(math.pi*(1.1**2-1.06**2)/4)/1e6)','(.067858,29.47)','m2,MPa')
SENSITIVITIES['b291']=('(11275/(1025*100),)','(.11,)','m')
SENSITIVITIES['b292']=('(300*30*11,300*30*11/150)','(99000.,660.)','m3,s')
SENSITIVITIES['b294']=('(1000*9.81*(8.8**2-6**2)/2/1000,((8.8**2-6**2)/(8**2-6**2)-1)*100)','(203.2632,48.)','kN/m,percent')
SENSITIVITIES['b295']=('(10*35/(110+10),(1-(10*35/(110+10))/(10*35/(100+10)))*100)','(2.9167,8.333)','kg/m3,percent')
def run():
 checks=[]
 for row in ROWS.strip().splitlines():
  cid,n,expr,published,units,boundary=row.split('|');f=H/'inputs'/f'{cid}.json';d=json.loads(f.read_text());u=d['units'][int(n)-1]
  actual=eval(expr,{'__builtins__':{},'math':math});expected=ast.literal_eval(published)
  literals=[ast.get_source_segment(published,x)for x in ast.parse(published,mode='eval').body.elts]
  tolerance=[max(1e-12,float(Decimal(10)**Decimal(x).as_tuple().exponent)/2)for x in literals]
  ok=len(actual)==len(expected) and all(abs(a-b)<=t for a,b,t in zip(actual,expected,tolerance))
  checks.append(dict(courseId=cid,unit=int(n),expression=expr,recomputed=actual,published=expected,units=units,tolerance=tolerance,status='PASS'if ok else'FAIL',boundary=boundary,model=u['model'],modelSha256=hashlib.sha256(u['model'].encode()).hexdigest(),inputSha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 sens=[]
 for cid,(expr,pub,units)in SENSITIVITIES.items():
  a=eval(expr,{'__builtins__':{},'math':math});b=ast.literal_eval(pub)
  assert all(abs(x-y)<=max(.0001,abs(y)*.001)for x,y in zip(a,b)),cid
  sens.append(dict(courseId=cid,expression=expr,recomputed=a,published=b,units=units,status='PASS'))
 result=dict(date='2026-10-21',method='Author recomputation from declared synthetic inputs with standard-library mathematics; not independent project verification.',units=len(checks),passes=sum(x['status']=='PASS'for x in checks),failures=[x for x in checks if x['status']=='FAIL'],checks=checks,sensitivity=sens)
 (H/'calculation_coasts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:result[k]for k in ['units','passes','failures']},ensure_ascii=False))
 assert not result['failures']
if __name__=='__main__':run()
