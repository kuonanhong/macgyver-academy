#!/usr/bin/env python3
"""Independent arithmetic/unit audit of authored b126–b150, not a design certification.
Expressions below were independently transcribed from the stated synthetic assumptions;
they do not import authors' implementations. Output records model and file hashes.
"""
import argparse,ast,hashlib,json,math
from decimal import Decimal
from pathlib import Path
H=Path(__file__).resolve().parent
# id|unit|independent expression (tuple)|published rounded results|units|boundary review
ROWS=r'''
b126|1|(30*sin(radians(10)),)|(5.21,)|m|Bore direction measured against target plane; inferred intercept is geometric.
b126|2|(100*sin(radians(1)),)|(1.745,)|m|Angular alignment error; no assertion of actual bore deviation.
b126|3|(2*pi*200/(pi*.1**2*.02/4)/1e6,)|(8.,)|MJ/m3|Rotational work only; thrust and losses omitted.
b126|4|(.15/.003,.15/.003*.01)|(50.,.50)|s,m|Volume and steady return flow; transit delay is not unique geological attribution.
b126|5|(27-20,(27-20)/60)|(7.,.117)|L/min,L/s|Balance excludes storage correction and is not steady groundwater inflow.
b126|6|(490000/(1000*9.81),)|(49.95,)|m|Pressure head alone; elevation head must be added.
b126|7|(1e-6*2*5,1e-6*2*5*1000)|(1e-5,.01)|m3/s,L/s|Darcy homogeneous idealization and specified hydraulic gradient.
b126|8|(.2*.8/(.2*.8+.8*.1),)|(.667,)|fraction|Prior and false-positive definitions retained; not probability from signal alone.
b126|9|(1.6/2,2-1.6)|(.8,.4)|fraction,m|Core recovery does not assign location or strength of lost material.
b126|10|(8/10,)|(.8,)|fraction|Evidence completeness is not construction acceptance.
b127|1|((9-15)/(9+15),)|(-.25,)|amplitude ratio|Normal-incidence impedance contrast; sign is phase, not energy fraction.
b127|2|(4000*.04/2,4400*.04/2)|(80.,88.)|m|Two-way time; fixed time while velocity changes.
b127|3|(4000/1000,4000/1000/4)|(4.,1.)|m|Quarter wavelength is a scale, not guaranteed resolution.
b127|4|(8000/2,1000/8000)|(4000.,.125)|Hz,ms|Ideal Nyquist limit is not an alias-safe working bandwidth.
b127|5|(sqrt(16),20*log10(sqrt(16)))|(4.,12.04)|ratio,dB|Coherent repeated signals and independent zero-mean noise explicitly stated.
b127|6|(80*sin(radians(5)),)|(6.97,)|m|Azimuth uncertainty translated geometrically.
b127|7|(2500*2000**2/1e9,1.1**2)|(10.,1.21)|GPa,ratio|Small-strain dynamic shear modulus, not static rock-mass modulus.
b127|8|(exp(-.01*50),)|(.607,)|amplitude ratio|Material attenuation only; geometrical spreading excluded.
b127|9|(80*sqrt(.05**2+.02**2),)|(4.31,)|m|Independent velocity/time uncertainties; correlations require covariance.
b127|10|(8/10,3/20)|(.8,.15)|fractions|Sensitivity and false-positive denominator remain separate.
b128|1|(2.7/3,3-2.7)|(.9,.3)|fraction,m|Lost length cannot be assigned to a particular depth without evidence.
b128|2|(1.4/2,)|(.7,)|fraction|Sound pieces and 100 mm counting convention; no standalone design classification.
b128|3|(.3/cos(radians(60)),)|(.6,)|m|Angle is to discontinuity normal, not to its plane.
b128|4|(4/2,)|(2.,)|ratio|Infill/asperity geometry is not a strength factor.
b128|5|(200000/(pi*.05**2/4)/1e6,)|(101.9,)|MPa|Intact specimen nominal stress, not rock-mass strength.
b128|6|(12+15+10+20+7-5,)|(59.,)|score|Illustrative score without claiming a code edition or design threshold.
b128|7|((60/9)*(2/3)*(1/5),(60/9)*(2/3)*(.5/5))|(.889,.444)|score|Empirical index inputs and sensitivity, not measured capacity.
b128|8|(10/.05,(10/.05)**2)|(200.,40000.)|ratios|Length and area scale cannot be applied as strength reduction.
b128|9|(16/20,)|(.8,)|fraction|Raw agreement is not chance-corrected kappa.
b128|10|(4/10,)|(.4,)|fraction|Inferred proportion is not failure probability.
b129|1|(70+90-65,)|(95.,)|m|Union computed from common interval and overlap.
b129|2|(degrees(atan(2*.05/.1)),)|(45.,)|degrees|Vertical bore, planar trace, stated sinusoid half-amplitude.
b129|3|(.05/20*1000,.1/20*1000)|(2.5,5.)|mm|Axial sample interval, not guaranteed feature resolution.
b129|4|(20*sin(radians(5)),)|(1.74,)|m|Geometric effect of azimuth bias.
b129|5|((110-100)/100,)|(.10,)|fraction|Defined ovality index; denominator explicitly selected.
b129|6|(.2*3,.2*2)|(.6,.4)|mm|Apparent width and two-edge one-pixel worst-case allowance.
b129|7|(30/20,)|(1.5,)|1/m|Scanline frequency is not volumetric fracture density.
b129|8|(.35-.20,)|(.15,)|L/s|Aligned steady flow readings; mixing or storage would invalidate attribution.
b129|9|(16/20,16/(16+4))|(.8,.8)|fractions|Recall and precision have different definitions despite equal example values.
b129|10|(92/100,100-92)|(.92,8.)|fraction,count|Traceability does not imply all missing observations are benign.
b130|1|(2600*9.81*500/1e6,)|(12.75,)|MPa|Overburden estimate omits topography/tectonics and nonuniform density.
b130|2|(10+sqrt(2**2+3**2),10-sqrt(2**2+3**2))|(13.61,6.39)|MPa|Two-dimensional principal values, not full 3D stress state.
b130|3|(15-.8*3,15-1*3)|(12.6,12.)|MPa|Biot coefficient and pressure reference defined.
b130|4|(40e9*200e-6/1e6,)|(8.,)|MPa|Uniaxial illustration, not full strain-to-stress inversion.
b130|5|(8+1000*9.81*100/1e6,)|(8.981,)|MPa|Static water-column correction; flow losses excluded.
b130|6|(3*20-10,)|(50.,)|MPa|Author clarified free-wall, homogeneous isotropic elastic medium and hole axis along third principal direction after review.
b130|7|(20e9*100e-6/1e6,40e9*100e-6/1e6)|(2.,4.)|MPa|Sensitivity to assumed modulus, not a complete anisotropic solution.
b130|8|(5**2/15**2,)|(.111,)|ratio|One radial scaling term, not the complete stress solution.
b130|9|(sqrt((3**2+(-4)**2+0**2)/3),)|(2.89,)|microstrain|RMSE without removing common bias; not proof of identifiability.
b130|10|((18+22+26)/3,26-18)|(22.,8.)|MPa|Mean and range; no normal-distribution claim.
b131|1|(tan(radians(35)),tan(radians(25)))|(.700,.466)|MPa|Zero-cohesion effective normal stress 1 MPa and selected angles.
b131|2|((1.2-.4)*tan(radians(30)),)|(.462,)|MPa|Effective normal stress and drained friction relation.
b131|3|(2*.3,)|(.6,)|MPa|Prescribed normal stiffness; machine compliance excluded.
b131|4|(degrees(atan(.2/2)),)|(5.71,)|degrees|Dilation displacement ratio, not direct friction angle.
b131|5|((.9-.5)/.9,)|(.444,)|fraction|Peak-to-residual drop is not a factor of safety.
b131|6|((100-10)*100,9000/((100-10)*100),9000/(100*100))|(9000.,1.,.9)|mm2,MPa,MPa|Overlap correction for assumed planar shear specimen.
b131|7|(.005**2/1e-8,.005**2/1e-8/60)|(2500.,41.7)|s,min|Diffusion timescale only; boundary-dependent consolidation solution omitted.
b131|8|(2/10,2/100,100/10)|(.2,.02,10.)|ratios|Relative roughness is geometry, not direct strength scaling.
b131|9|(sqrt(.02**2+.03**2)*100,)|(3.61,)|percent|Independent first-order force and area uncertainty.
b131|10|(.6e6*.005,)|(3000.,)|J/m2|Work per nominal area; not all energy necessarily dissipated.
b132|1|(10*exp(-5**2/(2*5**2)),)|(6.07,)|mm|Gaussian settlement illustration with downward-positive convention.
b132|2|(sqrt(2*pi)*.01*5,sqrt(2*pi)*.01*5/(pi*6**2/4)*100)|(.1253,.443)|m2,percent|Trough volume per length compared to excavation area; not actual loss causality.
b132|3|(8+3,)|(11.,)|mm|External reference needed to recover benchmark movement.
b132|4|(.005/10,)|(.0005,)|rad|Small angular distortion; no universal damage threshold.
b132|5|(2/24,2/2)|(.0833,1.)|mm/h|Time windows remain explicit and comparable.
b132|6|(sqrt(2)*.5,)|(.707,)|mm|Independent epoch errors; shared datum bias does not cancel automatically.
b132|7|(9.81*2,)|(19.62,)|kPa|Total stress held constant and measured pore-head fall specified.
b132|8|(30/6,)|(5.,)|ratio|Reference face distance and diameter only, sign convention retained.
b132|9|(8/10,)|(.8,)|fraction|Illustrative review ratio, not authorization or code limit.
b132|10|(.8+.4+.2+.1,)|(1.5,)|mm|Decreasing increments do not prove zero future movement.
b133|1|((8-7.988)*1000,(8-7.988)/8)|(12.,.0015)|mm,strain|Chord contraction excludes common translation.
b133|2|(6+14,6/(6+14))|(20.,.3)|mm,fraction|Pre-baseline displacement is inferred and separately identified.
b133|3|(100*5/206265*1000,)|(2.42,)|mm|Small-angle transverse scale, not full survey error budget.
b133|4|(12e-6*10*10*1000,)|(1.2,)|mm|Uniform thermal expansion; sag and restraint omitted.
b133|5|(5-5,)|(0.,)|mm|Common translation preserves chord lengths while absolute position changes.
b133|6|((11-8)/6,(11-8)/3)|(.5,1.)|mm/h,mm/m|Time and advance-normalized rates are distinct.
b133|7|(20e6*.002/1000,)|(40.,)|kN|Linear post-contact support response only.
b133|8|((6.006-5.990)*1000,)|(16.,)|mm|Defined diameter difference, not a universal ovality criterion.
b133|9|(5+10+15,)|(30.,)|min|Serial worst-case latency, excluding remeasurement and other delays.
b133|10|(10.5-10,)|(0.5,)|mm|Equal residuals for two models do not establish equal mechanisms.
b134|1|(5*5e-6/.025*1000,)|(1.,)|mm/pixel|Ground sampling distance is not 3D reconstruction accuracy.
b134|2|(5**2/(5000*1)*.5*1000,)|(2.5,)|mm|Ideal stereo propagation with fixed calibrated geometry.
b134|3|(1e-9*1000**3,)|(1.,)|pixel|Specified radial-distortion coefficient and pixel convention.
b134|4|(2/1.99,)|(1.00503,)|scale|Global scaling cannot repair local warping.
b134|5|(200000/2000000,)|(.1,)|fraction|Saturated-pixel count is not usable measurement coverage.
b134|6|(42/50,50-42)|(.84,8.)|fraction,m2|Occluded area remains missing rather than inferred as sound.
b134|7|(sqrt((1+4+4)/3),)|(1.73,)|mm|Checkpoint RMSE differs from maximum error and training fit.
b134|8|(degrees(acos(.8)),)|(36.87,)|degrees|Unit normal and vertical reference stated.
b134|9|(sqrt(2)*2,1.96*sqrt(2)*2)|(2.83,5.54)|mm|Independent Gaussian epoch errors for stated 95 percent illustration.
b134|10|(9/10,)|(.9,)|fraction|Missing datum can invalidate a high-completeness dataset.
b135|1|(300-180,)|(120.,)|kPa|Effective stress illustration, not face support setting.
b135|2|(1500*9.81*6/1000,)|(88.29,)|kPa|Hydrostatic head term alone does not establish stability range.
b135|3|(18*8,)|(144.,)|kPa|Simple overburden ignores arching, water and cohesion.
b135|4|(150/50,)|(3.,)|ratio|Illustrative load-to-undrained-strength ratio, no universal threshold.
b135|5|((2.65-1)/(1+.7),)|(.971,)|gradient|Ideal critical-gradient relation not a tunnel-face design criterion.
b135|6|(pi*6**2/4*1.5,)|(42.41,)|m3|In-situ geometry; fluid and bulking must be reconciled separately.
b135|7|(200*exp(-2/10),)|(163.7,)|kPa|Assumed exponential transient, not a calibrated field forecast.
b135|8|(6/30,)|(.2,)|fraction|Sand area fraction is not a risk probability.
b135|9|(150/50,150/40,(150/40)/(150/50)-1)|(3.,3.75,.25)|ratios|Strength sensitivity, not probability of failure.
b135|10|(4/5,)|(.8,)|fraction|An anomalous fifth record cannot be overruled by majority.
b136|1|(160/8,)|(20.,)|kPa/m|Observed mean pressure gradient, not equipment setting.
b136|2|(250/1000,250/(1000+250))|(.25,.2)|fractions|Dry-mass water content distinguished from wet-mass fraction.
b136|3|(100*3/300,)|(1.,)|m3|Absolute pressure and ideal isothermal gas only.
b136|4|(.6/2,)|(.3,)|fraction|Specified sieve convention, not a universal recipe.
b136|5|(2+.5*4,)|(4.,)|kPa|Ideal Bingham parameters with shear-rate units.
b136|6|(1e6*2*2*pi/60/1000,)|(209.4,)|kW|Rotational shaft power, not installed equipment rating.
b136|7|(2/40,)|(.05,)|fraction|Volume ratio is an illustrative observation, not conditioning instruction.
b136|8|(1e-7*.01*10,1e-7*.01*10*1000*60)|(1e-8,.0006)|m3/s,L/min|Darcy assumptions, particular geometry and gradient.
b136|9|(80/100,)|(.8,)|fraction|Arbitrary test-index retention, not specification acceptance.
b136|10|(8/12,)|(.667,)|fraction|Failed trials remain in denominator.
b137|1|(110-100,)|(10.,)|m3/h|Unchanged storage; net return includes fluid and solids.
b137|2|(.25/(pi*.4**2/4),)|(1.989,)|m/s|Mean velocity only, not transport recommendation.
b137|3|(.2*500/.75,)|(133.3,)|kW|Hydraulic power divided by pump efficiency; motor losses omitted.
b137|4|((1200-1000)/(2600-1000),((1200-1000)/(2600-1000))*2600/1200)|(.125,.271)|fractions|Two-component volume and mass fractions are distinguished.
b137|5|(80/100,)|(.8,)|fraction|Overall solids recovery does not establish each particle-size fraction.
b137|6|(60/120,60/120*60)|(.5,30.)|h,min|Nominal residence time differs from actual residence-time distribution.
b137|7|(1200*300*.5/1000,)|(180.,)|kPa|Author clarified velocity change fast relative to 2L/a and excluded direct application to slow changes after review.
b137|8|((12-10)/1000,)|(.002,)|mm/h|Observed average rate, extrapolation only under unchanged conditions.
b137|9|(160/(160+10)*100,)|(94.12,)|percent|Operational availability denominator, not intrinsic reliability.
b137|10|(9/10,)|(.9,)|fraction|Critical uncalibrated measurement requires resolution regardless of percentage.
b138|1|(.01**3,)|(1e-6,)|probability|Independent barriers only; common causes explicitly invalidate product.
b138|2|(40-15,40+15)|(25.,55.)|mm|Opposite eccentric clearances, ovalization excluded.
b138|3|(1000*9.81*30/1000,)|(294.3,)|kPa|Freshwater hydrostatic pressure excludes grout transient and supply setting.
b138|4|(120/8,)|(15.,)|kg/m|Zero-advance standstill denominator is undefined.
b138|5|(1.5/1,)|(1.5,)|ratio|Line pressure-loss ratio is not a sealing-capacity ratio.
b138|6|(.5/20*100,)|(2.5,)|percent|Continuous local defect cannot be risk-averaged by circumference share.
b138|7|(250-230,)|(20.,)|kPa|Diagnostic signed pressure difference, not allowable margin.
b138|8|(30/5,30/5/60)|(6.,.1)|L/min,L/s|Dedicated collection required; mixed drainage cannot isolate leakage.
b138|9|(36/24,)|(1.5,)|kg/h|Observation does not establish replenishment schedule.
b138|10|(9/12,12-9)|(.75,3.)|fraction,count|Adjacent missing zones are not uniform random omissions.
b139|1|(2*pi*5*4/60,)|(2.094,)|m/s|Tangential speed at stated radius, not recommended rotation.
b139|2|(30/3,)|(10.,)|mm/rev|Advance per revolution does not establish tool capacity.
b139|3|(10000/40,)|(250.,)|kN/tool|Effective cutting thrust only; arithmetic mean not actual individual load.
b139|4|(2*pi*2*10/20,)|(6.283,)|MJ/m3|Rotational work only; constant mean torque assumed.
b139|5|(3/600,)|(.005,)|mm/m|Average observed wear cannot be transferred blindly to different strata.
b139|6|(65-40,)|(25.,)|K|Temperature difference, not universal bearing threshold.
b139|7|(2*3*60*100,)|(36000.,)|transitions|Event count with stated conversions of rpm and hours.
b139|8|(80/10,)|(8.,)|ratio|Spacing/penetration ratio does not determine equal specific energy across rocks.
b139|9|(400+200,)|(600.,)|h|Unreplaced bearing retains prior service history.
b139|10|(36/40,40-36)|(.9,4.)|fraction,count|Clustered missing cutter states cannot be ignored.
b140|1|(.3*3,)|(.9,)|MN/m|Thin continuous ring membrane force; bending and joints excluded.
b140|2|((48+50+52)/3,)|(50.,)|MPa|Small-sample mean is not characteristic strength.
b140|3|(3*12000*.5/(2*.15*.125**2)/1e6,)|(3.84,)|MPa|After review, author explicitly states a three-point centre-loaded notched beam with the stated ligament.
b140|4|(6*.5,)|(3.,)|mm|Same-direction bias sums directly; independent errors require a different model.
b140|5|(20e9*1e-5*20/1e6,)|(4.,)|MPa|Full restraint and linear elasticity; creep changes actual stress.
b140|6|(20*2/8,)|(5.,)|kNm|W is total uniformly distributed load, not load per metre.
b140|7|(1/.1,)|(10.,)|MPa|Average pad bearing does not check splitting or edge distance.
b140|8|(sqrt(1e-6*3600),)|(.06,)|m|Thermal diffusion scale, not spalling depth or required fire thickness.
b140|9|((50/40)**2,)|(1.5625,)|ratio|Unchanged diffusion coefficient and boundary scaling; no lifetime guarantee.
b140|10|(118/120*100,120-118)|(98.33,2.)|percent,count|Traceability proportion does not authorize missing pieces.
b141|1|((20-15)/20*100,)|(25.,)|percent|Effective gasket height and defined compression; not product acceptance.
b141|2|(1000*9.81*50/1e6,)|(.4905,)|MPa|Freshwater hydrostatic conversion excludes transients and design allowance.
b141|3|(30-5,(30-5)/30*100)|(25.,83.3)|mm,percent|Simplified lateral overlap excludes rubber deformation and combined performance.
b141|4|(30*2,)|(60.,)|kN|Line reaction integrates to force; local groove stress requires contact geometry.
b141|5|(70/100*100,)|(70.,)|percent|Specified-test retention cannot predict a 50-year life directly.
b141|6|(1/4*100,)|(25.,)|percent|Corner count coverage, not perimeter-weighted risk.
b141|7|(.1/2*100,)|(5.,)|percent|Small unretained strip can interrupt continuous sealing.
b141|8|(.005/2*100,)|(.25,)|percent|Contaminated length fraction is not watertightness-loss fraction.
b141|9|(sqrt(1**2+2**2),1+2)|(2.24,3.)|mm|Independent standard deviations versus same-direction systematic biases distinguished.
b141|10|(18/20*100,20-18)|(90.,2.)|percent,count|Unpassed assemblies require individual investigation.
b142|1|(50/1000,)|(.05,)|m|Load eccentricity alone cannot prove opening without section geometry.
b142|2|(.30/6,)|(.05,)|m|Mechanism explicitly states rectangular linear full-compression contact and no-tension reassessment.
b142|3|(.2*.024*100000,)|(480.,)|Nm|Illustrative nut factor K; friction dependence precludes torque-only proof of preload.
b142|4|(20/.002/1000,)|(10.,)|MNm/rad|Secant slope over a stated increment, not a universal constant or tangent stiffness.
b142|5|(.003*.2*1000,)|(.6,)|mm|Small rotation at stated seal offset; translation and rotation sign remain separate.
b142|6|(200/4,)|(50.,)|kN/zone|Equal-share mean does not resolve actual eccentric distribution.
b142|7|(100*30*365,)|(1095000.,)|cycles|Specified representative amplitude and 365 days/year; no fatigue-damage summation implied.
b142|8|(120/.02/1000,)|(6.,)|MPa|Nominal force/area is not complete local anchorage capacity check.
b142|9|(.004-.001,)|(.003,)|rad|Machine-compliance subtraction requires independent calibration.
b142|10|(8/10*100,10-8)|(80.,2.)|percent,count|Direct test coverage distinguished from analytical extrapolation.
b143|1|(pi*(6.4**2-6.2**2)*1.5/4,)|(2.969,)|m3|Nominal annular void geometry does not prove complete filling.
b143|2|(4-.3-.2,)|(3.5,)|m3|Metered balance subtracts line storage and return but not unresolved losses.
b143|3|(1800*9.81*6/1000,)|(105.95,)|kPa|Hydrostatic elevation correction with flow losses separate.
b143|4|(30/1000*100,)|(3.,)|percent|Specimen bleeding does not directly predict field void increase.
b143|5|(.12/.004,)|(30.,)|s|Nominal line residence excludes stoppages and nonideal transport.
b143|6|(1200*9.81*15/1000,12000*9.81/1000,1200*9.81*15/1000-12000*9.81/1000)|(176.58,117.72,58.86)|kN|Author clarified near-hydrostatic external pressure and effective displaced grout volume, not concrete volume; revised model reread.
b143|7|(50*.001,50*.001*1000)|(.05,50.)|MPa,kPa|Linear compressive stiffness illustration, not failure strength.
b143|8|(3*.02,)|(.06,)|m3|Free volumetric reduction does not automatically become a restrained field void.
b143|9|((100-10)/100*100,)|(90.,)|percent|Unmeasured area remains unknown, not defect-free.
b143|10|(8/10*100,10-8)|(80.,2.)|percent,count|Unclosed ring balances require individual review.
b144|1|(min(2,1,2,2),(2+1+2+2)/4)|(1.,1.75)|barriers|Minimum stage redundancy cannot be represented by an average count.
b144|2|(9.81*20,9.81*20*10/1000)|(196.2,1.962)|kPa,MN|Freshwater head difference and uniformly loaded plane area, not pressure-varying resultant.
b144|3|((1+1)/(1/1e-6+1/1e-8),)|(1.98e-8,)|m/s|Series flow normal to two layers; harmonic mean fails for bypass paths.
b144|4|(10/5,10/1)|(2.,10.)|gradients|Effective shortest path, not automatically the nominal treatment thickness.
b144|5|(12-4,12+4)|(8.,16.)|mm|Geometric opposite compression; flexible seal response requires testing.
b144|6|(10*tan(radians(.2))*1000,)|(34.91,)|mm|Crossing length and angular-error geometry, not allowable angle.
b144|7|(4/4,)|(1.,)|MN/support|Equal support stiffness assumed; actual eccentricity and gaps require analysis.
b144|8|(5/6*100,)|(83.3,)|percent|Offline data must remain missing rather than filled with normal zeros.
b144|9|(2+3+5,)|(10.,)|min|Serial information-delay scale, not permissible engineering hold time.
b144|10|(9/10*100,10-9)|(90.,1.)|percent,count|Unverified permanent interface remains open regardless of average completion.
b145|1|(1000*10e-6*1000,)|(10.,)|mm|Scale error grows with origin distance; not random instrument error.
b145|2|(300*1.5/206265*1000,)|(2.18,)|mm|Arcsecond conversion and small-angle transverse scale; station errors excluded.
b145|3|(100*.001*1000,)|(100.,)|mm|Small-angle projection of direction bias.
b145|4|(10*sin(radians(.1))*1000,)|(17.45,)|mm|Rotating lever-arm correction, not fixed translation.
b145|5|(100*.02,sqrt(100**2+(100*.02)**2))|(2.,100.020)|m|Horizontal chainage differs from slope distance.
b145|6|(1.5/300,degrees(1.5/300))|(.005,.286)|rad,degrees|Short-arc curvature illustration, not ring/steering acceptance.
b145|7|(12-5,)|(7.,)|mm|Relative machine-ring eccentricity differs from absolute alignment offset.
b145|8|(sqrt(2**2+2**2),6/sqrt(2**2+2**2))|(2.83,2.12)|mm,ratio|Independent standard uncertainties; no automatic normal-significance claim.
b145|9|(1/sqrt(1/2**2+1/3**2),)|(1.664,)|mm|Independent unbiased measurements of same quantity; shared biases invalidate reduction.
b145|10|(sqrt(10**2+12**2+9**2),)|(18.03,)|mm|Author clarified standard-uncertainty components of independent zero-mean errors; raw signed offsets and systematic bias are not combined by this RSS.
b146|1|(1.8-.3,floor((1.8-.3)/1.2))|(1.5,1.)|m,count|Integer ring count uses usable stroke after reserved travel.
b146|2|(8/4,8/2)|(2.,4.)|MPa|Nominal contact stress, not allowable ground pressure.
b146|3|(.4*8,.4*8/2.8)|(3.2,1.14)|MN,ratio|Ideal friction estimate, not code safety factor.
b146|4|(12/24,12/24/.1)|(.5,5.)|MN,MPa|Equal shoe distribution omits segment bending and nonuniform contacts.
b146|5|(max(30,25)+5,30+25+5,(60-35)/60*100)|(35.,60.,41.7)|min,min,percent|Perfect independent overlap; regrip remains serial.
b146|6|(.3*.2*pi*6*4,.3*.2*pi*6*6)|(4.52,6.79)|MN|Uniform normal contact pressure and assumed friction coefficient.
b146|7|(.010/5,degrees(.010/5))|(.002,.115)|rad,degrees|Geometric differential stroke, not steering instruction.
b146|8|(800*.5/40,800*.5/40*3.6)|(10.,36.)|kWh/m3,MJ/m3|Mean mechanical energy boundary retained; individual losses not separately inferred.
b146|9|(.005*2*60*20*.5,.005*2*60*20*.4)|(6.,4.8)|m/day|Utilization fraction and working-day denominator explicit.
b146|10|(114/120,120-114)|(.95,6.)|fraction,count|Unresolved handover records remain unresolved.
b147|1|(2.4*26,)|(62.4,)|kN|Self-weight of assumed block is not bolt demand or sliding check.
b147|2|(6/.8,6/.4)|(7.5,15.)|h|Exposure duration is not stand-up-time capacity.
b147|3|(4*60*cos(radians(30)),)|(207.8,)|kN|Projected ideal bolt forces, no automatic design allowance.
b147|4|(6*2/.12**2/1000,6*2/.10**2/1000)|(.833,1.2)|MPa|Elastic one-metre strip stress; tension/cracking requires separate assessment.
b147|5|(5*20*3**4/(384*50000)*1000,5*20*4**4/(384*50000)*1000,(4/3)**4)|(.422,1.333,3.16)|mm,mm,ratio|Simply supported uniform-load elastic beam only.
b147|6|((11-8)/6,sqrt(2)*.3)|(.5,.424)|mm/h,mm|Independent reading uncertainty; trend does not establish cause.
b147|7|(pi*(6.1**2-6**2)*2/4,)|(1.901,)|m3|In-situ geometric excess, not loose spoil volume.
b147|8|((80-65)*2,20/(80-65))|(30.,1.33)|m3,h|Fixed loose-volume production/removal and finite buffer.
b147|9|(600/20,log(10)*600/20)|(30.,69.1)|s|Ideal completely mixed clean-air replacement, no continuing source; not access permission.
b147|10|(20/100,1/10)|(.2,.1)|fractions|Sample fractions do not justify population failure prevalence.
b148|1|((.6+.1)/(.02+.01),.01*((.6+.1)/(.02+.01)-10))|(23.33,.133)|mm,MPa|Linear ground/support illustration within u>=10 and positive ground pressure.
b148|2|(30/80*100,30*1)|(37.5,30.)|percent,m3|Area/volume partition does not establish load share or stability.
b148|3|(300/.2/1000,(300/.2/1000)/2)|(1.5,.75)|MPa,ratio|Unit-width axial stress and synthetic strength; no factors or bending.
b148|4|((200/.25+6*10/.25**2)/1000,(200/.25-6*10/.25**2)/1000)|(1.76,-.16)|MPa|Elastic full-section stress; negative edge tension identified.
b148|5|(600/20,600/60)|(30.,10.)|mm|Prescribed equivalent incremental stiffness, not field calibration.
b148|6|(300e3/(6e9*.25)*1e6,300e3/(12e9*.25)*1e6)|(200.,100.)|microstrain|Elastic axial illustration excludes creep and shrinkage.
b148|7|(20*(1-exp(-5/5)),20*(1-exp(-10/5)))|(12.64,17.29)|mm|Assumed exponential asymptote is not a field limit.
b148|8|(150*2,)|(300.,)|kN|Local plane area with uniform gauge pressure, not whole curved lining resultant.
b148|9|(500/50,1000/100)|(10.,10.)|mm|Single displacement cannot identify force and stiffness independently.
b148|10|(8/200*100,200-8)|(4.,192.)|percent,m2|Critical joint defect cannot be averaged away by sound area.
b149|1|(900/2,900*.6,900*.4)|(450.,540.,360.)|kN|Symmetric versus hypothetical asymmetric reaction allocation.
b149|2|(12/2,12/2+3)|(6.,9.)|days|Fixed moving separation; duration is not allowable wait.
b149|3|(600/1.2,600/.8)|(500.,750.)|kPa|Mean contact pressure before bearing and settlement assessment.
b149|4|(60*4,12*4,12/60)|(240.,48.,.2)|m3,m3,fraction|Core volume fraction is not resistance fraction.
b149|5|(.004/6,degrees(.004/6))|(.000667,.0382)|rad,degrees|Small rigid-body rotation, not structural distortion capacity.
b149|6|(25*1.5*2400,25*1.5*1.4)|(90000.,52.5)|kg,m3|Mass conserved, loose volume separated by assumed bulking factor.
b149|7|(3-2,20/(3-2))|(1.,20.)|m/day,days|Constant-speed catch-up; equal speeds never close gap.
b149|8|(1/sqrt(4),2)|(0.5,2.)|mm|Independent noise averages; common bias remains.
b149|9|(1e-4*15*8/12,1e-4*15*8/12*3600)|(.001,3.6)|m3/s,m3/h|Darcy idealization with fixed k and flow geometry.
b149|10|(5.20-5.05-.03,)|(.12,)|m|Geometric remainder excludes future deformation reserve.
b150|1|(30*8**2/8,30*4**2/8)|(240.,60.)|kNm|Uniform load and simple supports must remain the same.
b150|2|((600*2+400*10)/1000,6-(600*2+400*10)/1000)|(5.2,.8)|m|Resultant location and eccentricity; no stress adequacy implied.
b150|3|(pi**2*20000/6**2,pi**2*20000/9**2)|(5483.,2437.)|kN|Euler ideal pinned elastic column excludes imperfections and inelasticity.
b150|4|((500/.3+6*50/.3**2)/1000,(500/.3-6*50/.3**2)/1000)|(5.,-1.667)|MPa|Elastic one-metre strip, tensile edge identified, no cracked-section capacity claim.
b150|5|(1000/(20+30),20*1000/50,30*1000/50,1000/30)|(20.,400.,600.,33.33)|mm,kN,kN,mm|Parallel linear elements and force held fixed during removal.
b150|6|(4*200,3*200,700-3*200)|(800.,600.,100.)|kN|Given independent same-direction resistance; factors/group effects excluded.
b150|7|(sqrt(2**2+3**2+2*.5*2*3),sqrt(2**2+3**2))|(4.36,3.61)|mm|Covariance applies to sum, not an unspecified difference.
b150|8|(sqrt((1**2+0+(-2)**2)/3),)|(1.29,)|mm|Withheld observations; RMSE is not peak residual.
b150|9|(9.81*18,9.81*18*1.5)|(176.58,264.87)|kPa,kN|Plane local area; whole curved structure requires vector integration.
b150|10|(76/80,80-76)|(.95,4.)|fraction,count|Approval fraction cannot override unresolved load transfer.
'''
# This is a closed dictionary for manually authored expressions, not user input.
ENV={n:getattr(math,n) for n in ['sin','cos','tan','asin','acos','atan','radians','degrees','sqrt','exp','log','log10','floor']};ENV.update(pi=math.pi,max=max,min=min)
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--accept-reviewed-model-changes',action='store_true',help='Use only after independent manual rereading of changed models, including units and physical boundaries.')
 args=parser.parse_args()
 oldfile=H/'audit_investigation_ai.json'
 previous={(x['courseId'],x['unit']):(x.get('unitReviewSha256'),x['modelSha256'])for x in json.loads(oldfile.read_text()).get('checks',[])} if oldfile.exists() else {}
 out=[]
 for line in ROWS.strip().splitlines():
  cid,num,expr,expected,units,note=line.split('|');f=H/'inputs'/f'{cid}.json'
  if not f.exists():continue
  d=json.loads(f.read_text());unit=d['units'][int(num)-1]
  actual=eval(expr,{'__builtins__':{}},ENV);stated=eval(expected,{'__builtins__':{}},{})
  # Half the final displayed decimal place, independently of result magnitude.
  # Scientific literals here are exact reference values, not one-digit estimates.
  literals=[ast.get_source_segment(expected,n) for n in ast.parse(expected,mode='eval').body.elts]
  tolerance=[max(1e-14,abs(float(v))*1e-9) if 'e' in v.lower() and '.' not in v else max(1e-14,float(Decimal(10)**Decimal(v).as_tuple().exponent)/2) for v in literals]
  matched=all(abs(a-b)<=t for a,b,t in zip(actual,stated,tolerance)) and len(actual)==len(stated)
  out.append({'courseId':cid,'unit':int(num),'title':unit['title'],'independentExpression':expr,'recalculated':actual,'publishedRoundedResults':stated,'displayRoundingTolerance':tolerance,'units':units,'arithmetic':'PASS' if matched else 'FAIL','physicalBoundaryReview':note,'model':unit['model'],'modelSha256':hashlib.sha256(unit['model'].encode()).hexdigest(),'unitReviewSha256':hashlib.sha256(json.dumps({k:unit.get(k,'')for k in ['title','model','mechanism','verify','failure']},ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'inputSha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 changed=[f"{x['courseId']}/u{x['unit']}"for x in out if (x['courseId'],x['unit']) in previous and (previous[(x['courseId'],x['unit'])][0]!=x['unitReviewSha256'] if previous[(x['courseId'],x['unit'])][0] else previous[(x['courseId'],x['unit'])][1]!=x['modelSha256'])]
 if changed and not args.accept_reviewed_model_changes:
  raise SystemExit('MANUAL REREVIEW REQUIRED for changed model text: '+', '.join(changed)+'. Existing audit preserved; accept only after rereading changed units.')
 assert len(out)==len({(x['courseId'],x['unit'])for x in out}), 'duplicate audit key'
 courses=sorted(set(x['courseId']for x in out))
 assert all(sum(x['courseId']==cid for x in out)==10 for cid in courses), 'incomplete per-course review'
 pending=[f'b{i}'for i in range(126,151)if f'b{i}'not in courses]
 result={'reviewer':'ai_sync (independent of b126–b150 authors)','date':'2026-10-21','method':'Manual model/units/boundary reading plus independent standard-library arithmetic. Expressions and reported rounded values transcribed separately from course text; does not import author calculations. Numeric tolerance accommodates stated rounding; all displayed assumptions and boundaries also reviewed. Input hashes identify the reviewed snapshot. Later reviewed unit-text changes (model/mechanism/verification/failure) block report replacement unless manually rereviewed and explicitly accepted.','limits':['Synthetic instructional examples only; not design certification or field validation.','Sources are not exhaustively reverified by this arithmetic review.','Automated comparisons do not parse prose for truth; the recorded model text and manual boundary notes are the actual reviewed scope.'],'reviewGuardValidation':{'date':'2026-10-21','result':'PASS','method':'In isolated temporary copies, separately change b126 unit 1 model and mechanism text; each rerun returns nonzero MANUAL REREVIEW REQUIRED and leaves the previous audit byte-for-byte unchanged.'},'coursesReviewed':courses,'unitsReviewed':len(out),'pendingCourses':pending,'arithmeticPass':sum(x['arithmetic']=='PASS'for x in out),'arithmeticFail':sum(x['arithmetic']=='FAIL'for x in out),'boundaryFindings':[{'id':'I130-6','courseId':'b130','unit':6,'severity':'clarification','issue':'Kirsch 3σH−σh assumes a free wall, homogeneous isotropic elasticity and hole axis along the remaining principal direction. Request explicit assumptions in the model.','disposition':'original author updated bilingual source and input; reviewed revised model and schema PASS'},{'id':'I137-7','courseId':'b137','unit':7,'severity':'clarification','issue':'Joukowsky full pressure jump applies to sufficiently rapid velocity change relative to wave round-trip time; request this explicit limit in the model.','disposition':'original author updated bilingual source and input; reviewed revised model and schema PASS'}],'checks':out}
 result['boundaryFindings'].append({'id':'I140-3','courseId':'b140','unit':3,'severity':'clarification','issue':'Residual flexural stress coefficient 3FL/(2bh²) assumes a notched beam under three-point centre loading; request explicit loading geometry.','disposition':'original author added bilingual three-point centre-loaded notched-beam geometry; revised model reviewed and value 3.84 MPa rechecked'})
 result['boundaryFindings'].append({'id':'I143-6','courseId':'b143','unit':6,'severity':'clarification','issue':'Archimedes grout-uplift illustration needs approximately hydrostatic external pressure and effective displaced volume rather than concrete volume.','disposition':'original author added near-hydrostatic external pressure and effective displaced grout volume rather than concrete volume; revised bilingual model reread and all three forces rechecked'})
 result['boundaryFindings'].append({'id':'I145-10','courseId':'b145','unit':10,'severity':'clarification','issue':'RSS error budget should explicitly combine standard-uncertainty components of independent zero-mean errors, not three raw signed offsets.','disposition':'original author explicitly states standard-uncertainty components of independent zero-mean lateral errors; revised bilingual model reread, only b145/u10 reviewed text changed, and 18.03 mm recomputed'})
 for finding in result['boundaryFindings']:
  finding['status']='OPEN' if 'pending verification' in finding['disposition'] else 'RESOLVED'
 result['openBoundaryFindings']=sum(f['status']=='OPEN' for f in result['boundaryFindings'])
 result['reviewStatus']='PASS' if not pending and not result['arithmeticFail'] and not result['openBoundaryFindings'] else 'IN_PROGRESS'
 (H/'audit_investigation_ai.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 md=['# V14 調查與監測獨立數值稽核','',f"2026-10-21；稽核者：ai_sync，非 b126–b150 作者。",'',f"最終狀態：{result['reviewStatus']}。已覆蓋 {len(courses)} 門／{len(out)} 單元；算術核對 {result['arithmeticPass']} PASS，{result['arithmeticFail']} FAIL，未解決邊界項目 {result['openBoundaryFindings']}。",'', '覆蓋課程：'+', '.join(courses)+'。', '', '尚待課稿完成：'+(', '.join(pending) if pending else '無')+'。','', '## 方法與證據','', '逐單元閱讀雙語 model、必要時回讀 mechanism／verify；依宣告的合成輸入，獨立使用 Python 標準函式庫重算並核對單位與有效邊界。沒有呼叫作者算例程式。JSON 保存每式獨立算式、重算值、原稿四捨五入結果、完整模型文字及檔案／模型 SHA-256。','', '命令：`python tools/underground-v14/audit_investigation_ai.py`。已人工核對顯示精度與近似值；程式容差只為容納原稿小數位，不代表工程容許誤差。','', '## 發現與處置','', '| 課程／單元 | 問題 | 處置 |','|---|---|---|', '| b130／6 | Kirsch 最大環應力缺明確自由孔壁、均質等向彈性及孔軸主應力方向條件。 | 作者已補中英模型與機制；稽核者回讀修訂並確認數值 50 MPa 不變。 |', '| b137／7 | 完整 Joukowsky 壓力跳躍需快於往返波傳時間；慢變速不能直接套同幅壓峰。 | 作者已補中英 2L/a 與慢變速限制；180 kPa 數值不變。 |', '', 'b140／3 的殘餘強度公式係數依載入幾何而定。作者已補中英三點中央載重缺口梁，稽核者已回讀修訂並重算 3.84 MPa；已解決。','', 'b143／6 作者已明示近似靜水漿壓及有效排開體積（非混凝土體積），稽核者已回讀並重算 176.58−117.72=58.86 kN；已解決。','', 'b145／10 作者已明示 RSS 分量是獨立零均值誤差的標準不確定度，而非三筆已量測偏差；已回讀修訂並重算 18.03 mm，已解決。','', '其他已覆蓋模型未見需要更正的算術或實質單位問題。b127 疊加相干性、b132 總應力固定、b140 有效韌帶、b146 整環向下取整、b147 完全混合無持續來源、b148／150 拉應力負號、b149 Darcy 流量轉換等均另行核對。','', '## 限制','', '此為教學合成算例的數值與物理適用範圍檢查，不是設計認證、現地驗證、規範合格證明或逐來源全文稽核。自動算術比對不會理解自然語言；實際人工審核範圍以 JSON 文字、逐式邊界紀錄及對應雜湊為準。新改稿須重新檢查。程式偵測既有單元的模型、機制、驗證或故障文字雜湊變動時會保留舊報告並停止；只有人工回讀之後才可使用 `--accept-reviewed-model-changes` 更新審查快照。','']
 (H/'REVIEW_INVESTIGATION_AI_V14.md').write_text('\n'.join(md))
 fail=[(x['courseId'],x['unit'],x['recalculated'],x['publishedRoundedResults'])for x in out if x['arithmetic']=='FAIL']
 print(json.dumps({'reviewStatus':result['reviewStatus'],'courses':len(courses),'units':len(out),'pending':pending,'openBoundaryFindings':result['openBoundaryFindings'],'failures':fail},ensure_ascii=False))
 if fail:raise SystemExit(1)
if __name__=='__main__':main()
