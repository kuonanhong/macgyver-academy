"""Independent review expressions transcribed from course inputs, not author audit code."""
import ast,hashlib,json,math
from decimal import Decimal
from pathlib import Path
H=Path(__file__).resolve().parents[1]
ROWS=r'''
b261|1|(.020*5000*2**2/(2*9.81),)|(20.39,)|Darcy friction, selected factor, local losses excluded.
b261|2|(math.sqrt(2.2e9/(1000*(1+2.2e9/(200e9*.010)))),)|(1023.5,)|Thin elastic wall; mechanism explicitly excludes Poisson and restraint corrections.
b261|3|(1000*1000*1/1e6,1000*1000/(1000*9.81))|(1.00,101.94)|Rapid single-phase wavefront increment; not full maximum envelope or absolute pressure.
b261|4|(2*5000/1000,3/(2*5000/1000))|(10.0,.30)|Uniform speed and simple round trip, reflection histories need boundary conditions.
b261|5|(2*5000/(9.81*30),)|(33.98,)|Slow reservoir-to-valve scale only; real valve curve and reflections explicitly required.
b261|6|(100*100**2/2/1000,(100*100**2/2)/100000)|(500.,5.0)|Energy/power comparison, not actual rundown with variable torque.
b261|7|(30-2.3,)|(27.7,)|Absolute pressure comparison at stated temperature.
b261|8|(300*(2/1.8)**1.2,)|(340.4,)|Gas volumes, absolute pressure, selected polytropic exponent.
b261|9|(1000*.020/20,1000*.010/20)|(1.0,.50)|Courant values do not independently guarantee accuracy.
b261|10|(.40*1/(2*.010),)|(20.0,)|Thin-wall nominal stress range; fatigue detail effects separate.
b262|1|(1000*9.81*50/1000,)|(490.5,)|Static connected surface and gauge reference.
b262|2|(2.5*3*100,)|(750.,)|In-situ prism, bulking and variable section excluded.
b262|3|(12/.60,)|(20.,)|Continuous effective-width contact average, not ring deformation check.
b262|4|(100/(2*math.cos(math.radians(30))),)|(57.74,)|Symmetric static sling forces with angle from vertical, not rigging rating.
b262|5|(1.50*1.20/(2*.012),)|(75.0,)|Thin-shell nominal hoop stress, not weld qualification.
b262|6|(math.pi*1.2**2/4,2*.80*(math.pi*1.2**2/4)*math.sin(math.radians(45)))|(1.131,1.280)|Hydrostatic bend pressure thrust only; resisting ground separate.
b262|7|(.020/12,1.2*.020/12*1000)|(.001667,2.0)|Small rotation; joint relative movement needs adjacent section orientation.
b262|8|(12e-6*100*25,12e-6*100*25*1000)|(.030,30.)|Free expansion, restraint stress not included.
b262|9|(100*1e6/2.2e9,100*1e6/2.2e9*1000)|(.04545,45.45)|Liquid-only compression, excludes pipe compliance and gas.
b262|10|(math.pi*1.2**2*1000/4,math.pi*1.2**2*1000/4/.1/3600)|(1131.0,3.142)|Theoretical volume and comparison flow, not commissioning approval.
b263|1|(.62*1e-5*math.sqrt(2*300000/1000)*1000,)|(.1519,)|Specified orifice and pressure, no loudness inversion.
b263|2|((200-1000*.040)/2,200-(200-1000*.040)/2)|(80.0,120.)|Known path length, uniform propagation and defined delay orientation.
b263|3|((200-2*60)/.080,)|(1000.,)|Calibration for one assumed uniform reach only.
b263|4|(-.040*100/2,1000*.001/2)|(-2.0,.50)|Signed speed sensitivity plus magnitude of separate timing bias.
b263|5|(1/2000,1000/(2*2000))|(.0005,.25)|Sample spacing is not guaranteed field resolution.
b263|6|(800/200,)|(4.0,)|Band-specific phase speed and wavelength, not leak resolution.
b263|7|(math.exp(-.010*100),20*math.log10(math.exp(-1)))|(.3679,-8.686)|Exponential amplitude attenuation and20log amplitude units.
b263|8|(3**2/(4*9),)|(.25,)|Compatible spectra, coherence not probability of leak.
b263|9|(.80*50,)|(40.0,)|Independently calibrated tool speed, not bulk flow.
b263|10|(8/(8+2)*100,8/(8+4)*100)|(80.,66.7)|Different precision and recall denominators.
b264|1|(1000-100-800-50,)|(50.,)|Synchronized balance includes storage, not necessarily physical leakage.
b264|2|(32+18-7,)|(43.,)|Signed boundary flows retained.
b264|3|((9800-10000)/10000*100,10000-9800)|(-2.0,200.)|Registration bias denominator is true volume.
b264|4|(((10+20)/2+(20+10)/2)*900,((10+20)/2+(20+10)/2)*900/1000)|(27000.,27.0)|Piecewise-linear trapezoids, litres converted to cubic metres.
b264|5|(5-1.2-.3,)|(3.5,)|Storage and authorized night use deducted; unexplained flow not proven leaks.
b264|6|(2.5*(40/50)**1.2,)|(1.913,)|Selected leakage exponent applies to leakage component only.
b264|7|(.20*5,)|(1.0,)|Window mismatch with selected constant interval flow.
b264|8|(300*.10,)|(30.,)|Constant tank area and common datum.
b264|9|(92/96*100,96-92)|(95.83,4.)|Completeness not detection sensitivity.
b264|10|(math.sqrt(10**2+8**2+3**2),)|(13.15,)|Independent standard components, not arbitrary correlated errors.
b265|1|(100-60-15,)|(25.,)|Supply head, node elevation and selected hydraulic loss.
b265|2|(20*math.sqrt((20-10)/(30-10)),)|(14.14,)|Specified pressure-dependent demand interpolation, not universal demand law.
b265|3|((30/40)**1.2,10*(30/40)**1.2)|(.7081,7.081)|Fixed empirical exponent for leakage component only.
b265|4|(200000*.020,200000*.020/1000)|(4000.,4.0)|Dissipated hydraulic power, not recovered electricity.
b265|5|(20/(20+30),)|(.40,)|Authority at a defined branch operating point, not all-flow stability.
b265|6|(-.020*180,)|(-3.60,)|Linear trend over selected data latency.
b265|7|(.40*5,)|(2.0,)|Percentage-point command increment, not relative percent or controller tuning.
b265|8|(45-20-18,45-20-18-15)|(7.,-8.)|Backup head margin under chosen losses, not availability proof.
b265|9|(1000*800*.20/1000,)|(160.,)|Rapid wavefront magnitude separate from starting pressure.
b265|10|(500/10,500/8)|(50.,62.5)|Volume/renewal-flow scale, not complete water-age distribution.
b266|1|(.5/.45,.5/.45-.5)|(1.111,.611)|Volumetric membrane recovery and concentrate continuity.
b266|2|(1.2/.12,)|(10.0,)|Effective normal flow area, not biological safety criterion.
b266|3|(20*.60*.75,1.20/(20*.60*.75))|(9.0,.1333)|Gross area adjusted for openings and blockage.
b266|4|(2*1.5**2/(2*9.81),)|(.2294,)|Same velocity reference for local loss coefficient.
b266|5|(10+3-.3-1.5,10+3-.3-1.5-8)|(11.2,3.2)|Available NPSH vs assumed required, excludes vortex/air conclusions.
b266|6|(5e-4*300*.10,)|(.0150,)|Darcy medium and selected hydraulic gradient.
b266|7|(.020*2/(1e-4*100),.020*2/(.5e-4*100))|(4.0,8.0)|Fixed flow and medium dimensions, no indefinite suction assumption.
b266|8|(10.055*math.pi*1.2**2/4-6,)|(5.372,)|Fully submerged empty-pipe displaced external area and selected unit weight.
b266|9|(2*1*600,)|(1200.,)|Potential organism entrainment count, mortality fraction not supplied.
b266|10|((1-.10)*35+.10*45,)|(36.0,)|Mass fraction and mass-based salinity, not unqualified volume mixing.
b267|1|(1000-400,1000*35/(1000-400))|(600.,58.33)|Mass balance, assumed salt-free product.
b267|2|(35+(60-35)/10,)|(37.5,)|Mass dilution of excess over ambient, not total salinity divided by10.
b267|3|(.4/8,(.4/8)/(math.pi*.15**2/4))|(.050,2.829)|Equal-port-flow assumption, blockage distribution separate.
b267|4|(9.81*(1040-1025)/1025,)|(.1436,)|Reduced gravity magnitude with explicit ambient reference density.
b267|5|(3/math.sqrt(.15*.20),)|(17.32,)|Densimetric Froude ratio, no final dilution prediction.
b267|6|(1040*.050*3,.050*3)|(156.,.150)|Density required for force; kinematic flux has m4/s2 units.
b267|7|(2/.20,2/.22)|(10.,9.09)|Geometric ratio alone does not preclude plume interaction.
b267|8|(.10*1800,)|(180.,)|Passive translation with uniform current, not dilution distance.
b267|9|((9000*35+1000*60)/(9000+1000),)|(37.5,)|Steady completely mixed mass-flow box.
b267|10|(math.sqrt(.10**2+.10**2),)|(.1414,)|Independent standard uncertainties, difference not ecological safety.
b268|1|(8/80,80-8)|(.10,72.)|Specified instantaneous streams, not low-flow allocation authorization.
b268|2|(2*.30*3600,)|(2160.,)|Constant synchronized concentration/flow over interval.
b268|3|((2650-1000)*9.81*(20e-6)**2/(18*.001),)|(.0003597,)|Stokes isolated small particles; mechanism requires low particle Reynolds number.
b268|4|(.20/100,)|(.0020,)|Ideal surface loading, short circuits and turbulence separate.
b268|5|(.05*(2650-1000)*9.81*.001,)|(.8093,)|Selected critical Shields parameter, entrainment not evacuation guarantee.
b268|6|(1000*9.81*.50*.001,)|(4.905,)|Mean approximately uniform-flow shear not every local bed point.
b268|7|(.5*math.sin(math.radians(20)),.5*math.cos(math.radians(20)))|(.1710,.4698)|Angle referenced to tangent, normal and sweeping projections distinct.
b268|8|(3*600,)|(1800.,)|Flushing water volume, no sediment-removal claim.
b268|9|(1200/1500,40/(1200/1500))|(.80,50.)|Dry bulk density and constant deposition, not guaranteed maintenance interval.
b268|10|(math.sqrt(1/25),(1/25)**2.5)|(.2,.00032)|Froude velocity and total discharge scaling, sediment similarity separate.
b269|1|(100+2.35,)|(102.35,)|Explicit vertical datum.
b269|2|(19620/(1000*9.81),)|(2.00,)|Gauge-pressure water column, temperature/density and sensor elevation separate.
b269|3|(3e8*40e-9/2,110-3e8*40e-9/2)|(6.00,104.)|Round-trip electromagnetic travel and surveyed antenna elevation.
b269|4|(.004*60/2,)|(.12,)|Rate bound and nearest regular sample, missing samples break bound.
b269|5|(.003*120,)|(.36,)|Selected constant rise over observation latency.
b269|6|(20*(2-.5)**1.6,)|(38.26,)|Rating coefficient units m1.4/s checked; changing control invalidates fixed curve.
b269|7|((2.22-2.10)/600,(2.22-2.10)/600*3600)|(.00020,.72)|Two-point interval average, not instantaneous derivative.
b269|8|(math.sqrt(.010**2+.020**2),)|(.02236,)|Independent standard sensor/datum components.
b269|9|(12*40*.5*.85/2,)|(102.,)|Energy budget with specified usable fraction and efficiency, ageing separate.
b269|10|(.02*.02,.02*.02*100)|(.0004,.04)|Same-period independent failures; common-cause failure excluded.
b270|1|((6-4)*300/600,)|(1.00,)|Fixed wet-well area and interval flows.
b270|2|(3+.20*4**2,)|(6.20,)|Loss coefficient s2/m5 produces head in metres.
b270|3|(2*math.sqrt(7/1.05),)|(5.164,)|Intersection of matched two-pump and system curves, not doubled single-pump operating flow.
b270|4|(1000*9.81*4*6/(.75*.95)/1000,)|(330.44,)|Separate pump and motor efficiencies applied to hydraulic power.
b270|5|(.9,.9**2,.9**3)|(.90,.81,.729)|Homologous affinity points, actual system operating point separate.
b270|6|(100*.6/.5+100*.6/(2-.5),3600/(100*.6/.5+100*.6/(2-.5)))|(160.,22.5)|Constant inflow and fixed pump flow, includes both fill and drain legs.
b270|7|(10.3+1.5-.25-1.2,)|(10.35,)|Atmospheric and vapor absolute-head terms, vortex analysis separate.
b270|8|(500/.8,)|(625.,)|Steady apparent power, startup requirements not implied.
b270|9|(9.81*2*(3**2-1**2)/2,)|(78.48,)|Two pressure triangles on same bottom datum, not square of head difference.
b270|10|(2*2,5-2*2)|(4.0,1.0)|Available unit flow explicitly assumed, one outage not all system failures.
b271|1|(.70*.050*200000,)|(7000.,)|Volume runoff coefficient and connected event area, not detention sizing by itself.
b271|2|((4+6-2-3)*300/2,)|(750.,)|Trapezoidal net storage balance, matched time interval.
b271|3|(1000*2+100*2**2,)|(2400.,)|Integral of variable area, h in metres and initial storage zero.
b271|4|(.62*.10*math.sqrt(2*9.81),)|(.2746,)|Differential head and selected discharge coefficient, tailwater retained.
b271|5|(1.70*2*.30**1.5,)|(.5587,)|Coefficient carries m0.5/s; free-weir relation not inundated control.
b271|6|(1000*.005*2,)|(10.0,)|Millimetres converted to metres, selected constant infiltration period.
b271|7|(2*1000*(math.sqrt(2)-math.sqrt(.20))/(.62*.10*math.sqrt(2*9.81)),)|(7042.,)|Constant basin area, free orifice drawdown and no inflow; finite terminal head.
b271|8|(8+2,3+7,8+7)|(10.,10.,15.)|Two sampled simultaneous totals differ from sum of separate peaks.
b271|9|(1000*.15,2400-1000*.15)|(150.,2250.)|Uniform retained deposit, outlet blockage still separate.
b271|10|(10000-7600-2350,(10000-7600-2350)/10000*100)|(50.,.50)|Balance residual fraction does not verify peak dynamics.
b276|1|(1000*9.81*.8*.003,)|(23.544,)|Mean quasi-uniform boundary stress, not local bank maximum or vegetation tolerance.
b276|2|(.5*1000*1.1*1.2*2**2,)|(2640.,)|Fixed frontal area and drag coefficient, bending/reconfiguration separate.
b276|3|(1600/.2/1000,)|(8.,)|Effective tension already includes mobilization/orientation, not raw root density.
b276|4|((1000-600)*9.81*.8,)|(3139.2,)|Fully submerged homogeneous log, net static uplift only.
b276|5|(1.2-.5,)|(.7,)|Remaining geometric embedment not stability proof.
b276|6|(180/240,)|(.75,)|Original cohort denominator excludes replacement plants and strength inference.
b276|7|((6*2-(6-1)*.2)*20,)|(220.,)|Six parallel strips with exactly five longitudinal overlaps.
b276|8|(9.81*2,)|(19.62,)|Same-elevation hydrostatic pressure difference, not transient bank stability.
b276|9|((.08*.12-.075*.07)*3600,)|(15.66,)|Integrated sediment mass storage, no lateral flux or permanent-removal claim.
b276|10|((70-35)-(55-40),)|(20.,)|Percentage-point difference in differences; parallel-trend and uncontaminated-control assumptions explicit.
b277|1|(.6/(.012-.004),)|(75.,)|Uniform-slope geometric spacing, not optimized or guaranteed equilibrium.
b277|2|(.8+2.4**2/(2*9.81*.8**2),)|(1.258716,)|Rectangular hydrostatic section, unit velocity correction and local datum.
b277|3|((2.4**2/9.81)**(1/3),)|(.837371,)|Rectangular critical depth, not general drowned-control discharge.
b277|4|(.5*.4*(math.sqrt(1+8*5**2/(9.81*.4))-1),)|(1.241782,)|Horizontal rectangular short jump without added resisting forces.
b277|5|(.5*(30+10)*4*6,)|(480.,)|Explicit net upward pressures prevent double-counting top-water load.
b277|6|(40/((2650-1000)*9.81*.05),)|(.0494239,)|Noncohesive Shields ratio, no universal entrainment threshold.
b277|7|(2/.5,)|(4.,)|Grading ratio only, no universal acceptance criterion.
b277|8|((.001-.0015)*86400/((1-.35)*12*80),)|(-.0692308,)|Solid-volume flux converted through porosity to mean bed lowering.
b277|9|((2650-1000)*9.81*math.pi*.6**3/6,)|(1830.650022,)|Ideal submerged sphere volume and density contrast, drag/lift excluded.
b277|10|((350-295)/5,)|(11.,)|Downstream chainage decrease gives upstream interval-average migration.
b272|1|(400-120,120/400*100)|(280.,30.)|Instantaneous channel split, bypass still needs downstream continuity.
b272|2|(1.7*10*1**1.5,)|(17.0,)|Chosen free-weir coefficient with proper dimensions, not lateral or drowned weir universally.
b272|3|((1/.030)*40*(40/24)**(2/3)*math.sqrt(.0004),)|(37.49,)|Rectangular uniform-flow Manning section with specified roughness and energy slope.
b272|4|((5**2/9.81)**(1/3),)|(1.366,)|Rectangular critical depth, distinct from normal depth.
b272|5|((3**2-1**2)/(2*9.81),)|(.4077,)|Velocity-head change distinct from irreversible local loss.
b272|6|((.001-.0005)/(1-.60**2),)|(.00078125,)|Gradually varied flow local relation, invalid at critical denominator.
b272|7|(5/3*1.5,5000/2.5)|(2.5,2000.)|Wide-channel Manning kinematic celerity in mechanism, not particle velocity or exact crest arrival.
b272|8|(102.5-101.7-.20,)|(.60,)|Geometric crest margin after allowance, not embankment reliability.
b272|9|((.020-.015)*3600/((1-.40)*20*1000),)|(.0015,)|Solid-volume flux and porosity conversion to mean deposited depth.
b272|10|(.8*50/(2+math.sqrt(9.81*2)),)|(6.221,)|Shallow-water characteristic scale for selected explicit step, not convergence proof.
b278|1|(math.sqrt(2*9.81*.15),)|(1.715517,)|Ideal local jet scale, not species swimming threshold or pool average.
b278|2|(.7*.2*.8*math.sqrt(2*9.81*.15),)|(.192138,)|Fully submerged opening and selected effective discharge coefficient.
b278|3|(1000*9.81*.25*.15/3.5,)|(105.107143,)|Assumes all selected head power dissipates in pool; average power density not local turbulence.
b278|4|(6/(1.2-.8),)|(15.,)|Fish speed relative to water minus downstream current, fixed sustainable speed.
b278|5|(.6/40,)|(.015,)|Instantaneous attraction-flow fraction, not fraction of fish attracted.
b278|6|(8/.4,)|(20.,)|Nominal turnover, not identical fish or parcel residence.
b278|7|(.9/(3*.6),)|(.5,)|Open-area normal velocity differs from gross-area superficial velocity.
b278|8|(.4/.2,)|(2.,)|Eddy dimensional timescale only, not complete spectrum or physiological response.
b278|9|((80/.8)/(100/.9),)|(.9,)|Known detection probabilities and same unique cohort, no recrossing or parameter uncertainty.
b278|10|(.9**5,)|(.59049,)|Equal conditional stage probabilities; marginal-product independence not assumed.
b279|1|(1800/1200,)|(1.5,)|Matched endpoints and centreline definition, not automatic ecological/flood benefit.
b279|2|(3/1800,)|(.001666667,)|Mean bed geometry, not local energy slope or sediment equilibrium.
b279|3|(24*1.2**(2/3)*math.sqrt(.0015)/.04,)|(26.241241,)|SI Manning near-uniform flow, independently specified energy slope.
b279|4|(60000*.35,)|(21000.,)|Added inundation at a specified stage, no pre-existing volume and no peak-flow reduction inference.
b279|5|(1.5**2*12/(9.81*60),)|(.045872,)|Modest-width curvature scale, secondary circulation and bank erosion not solved.
b279|6|(240*2.5*1.8,)|(1080.,)|Uniform in-place bank prism, not grain volume or instantaneous exported sediment.
b279|7|(.8*7200,)|(5760.,)|Gross inward volume, outward flow needed for net storage.
b279|8|(.00002*300*.4/20,)|(.00012,)|Saturated homogeneous1D steady Darcy discharge, not pore velocity.
b279|9|(1800/.6,)|(3000.,)|Uniform parcel advection time, not wave celerity or tracer distribution.
b279|10|(math.sqrt(.03**2+.04**2),)|(.05,)|Independent zero-mean random standard deviations, no systematic datum cancellation assumption.
b273|1|(2/(1+.15),(2/(1+.15))/1.85*100)|(1.739,94.01)|Dry/wet density and mass water-content bases retained, no seepage-resistance guarantee.
b273|2|(1000*(.15-.12),)|(30.,)|Retained added water relative to fixed dry mass, uniform mixing not assumed automatic.
b273|3|(2.7/1.8-1,.15*2.7/(2.7/1.8-1))|(.50,.81)|Consistent density units, soil phase relation and dry-mass water content.
b273|4|(.25*4*math.log10(150/100)/(1+.8),)|(.09783,)|Normally consolidated1D primary-compression model with effective stresses, not all settlement.
b273|5|(.848*2**2/1e-7,.848*2**2/1e-7/86400)|(33920000.,392.59)|Drainage length rather than full layer thickness; time seconds converted to days.
b273|6|(1e-6*5*100*3/30,)|(5e-5,)|Saturated1D Darcy geometry and hydraulic gradient, no bypass.
b273|7|((2.65-1)/(1+.65),((2.65-1)/(1+.65))/.4)|(1.00,2.50)|Ideal vertical heave, not backward erosion or universal piping safety factor.
b273|8|(3/(.6/(1e-9*10)+29.4/(1e-5*10)),)|(4.976e-8,)|Same area serial hydraulic resistance, no joint or tip bypass.
b273|9|(.60/.20,.60/.05)|(3.,12.)|Selected retention/permeability ratios, not complete filter acceptance.
b273|10|(12+29.43/9.81,)|(15.,)|Sensor elevation plus gauge-pressure head, same vertical datum.
'''
ROWS += r'''
b280|1|(8/20,)|(.4,)|Equally weighted empirical member fraction; true-event calibration is explicitly separate.
b280|2|(4*.9,140+.6*(160-140))|(3.6,152.)|Specified zero-based linear empirical quantile, no universal tail bound.
b280|3|((.2**2+(.7-1)**2+(.6-1)**2+.1**2)/4,)|(.075,)|Binary Brier score on four held-out cases, not full long-term validation.
b280|4|(((100+180)-(80+120))*3600/2,)|(144000.,)|Matched trapezoidal storage balance without omitted water terms.
b280|5|(120+80+60,)|(260.,)|Contributions already routed to same junction and instant; no instantaneous upstream addition.
b280|6|(300-90-70,)|(140.,)|Hypothetical synchronized downstream flow allowance, not an upstream release command.
b280|7|(1800000/50/3600,)|(10.,)|Specified additional net release relative to baseline, sustained feasibility assumed and ramp time excluded.
b280|8|(max(90,120)-min(140,100),)|(20.,)|Positive gap explicitly means incompatible simultaneous constraints, not permission to relax them.
b280|9|(3/50,)|(.06,)|Equal-scenario fraction, not calibrated probability or consequence-weighted risk.
b280|10|((12+8+20+4)/4,(20+15+25+12)/4,1-11/18)|(11.,18.,.388889)|Same four held-out cases and positive reference MAE, no inference of equal operational risk reduction.
b274|1|(9.81*3**2/2,3/3,9.81*3**3/6)|(44.145,1.,44.145)|Vertical face, dry rear and unit wall length; hydrostatic only, with force square and moment cube scaling.
b274|2|((30+10)*4/2,4*(30+2*10)/(3*(30+10)))|(80.,1.667)|Linear net uplift distribution on horizontal base, resultant measured from high-pressure edge.
b274|3|(.5*(200-80),.5*(200-80)/40)|(60.,1.50)|Friction based on effective compressive normal action, no unverified cohesion or passive resistance.
b274|4|(60/120,120/4*(1+6*.5/4),120/4*(1-6*.5/4))|(.50,52.5,7.5)|Net effective force and net central moment, rigid linear full contact; eccentricity below middle-third bound.
b274|5|(5.14*40,)|(205.6,)|Mechanism specifies surface strip footing, uniform undrained clay, level ground and centered vertical load; net ultimate only.
b274|6|(50*4*(1-.3**2)*1/20000,)|(.00910,)|Uniform elastic half-space with assigned influence factor, no consolidation/shape guarantee.
b274|7|(math.tan(math.radians(45+30/2))**2,)|(3.00,)|Smooth vertical interface and level dry cohesionless ground; coefficient alone is not mobilized force.
b274|8|(2e-6*10*4/20,2e-6*10*4/40)|(4e-6,2e-6)|Assigned constant-area1D saturated path, not cutoff depth substituted for actual multidimensional flow length.
b274|9|((20-8)/1000/6,)|(.002,)|Two-point average settlement slope, not local opening or waterstop pressure capacity.
b274|10|(9.81*(.5**2-1.5**2)/2,)|(-9.81,)|Hydrostatic faces share base datum; sign convention positive river-to-land, other loads excluded.
b275|1|(.5+1+1.5+3+.5,8-(.5+1+1.5+3+.5))|(6.5,1.5)|Sequential nonoverlapping stages and deadline before safe installation becomes impossible, not merely crest arrival.
b275|2|(max(2,3.5)+.5,)|(4.0,)|Independent simultaneous crews and shared final inspection after both finish; unlisted/shared resources excluded.
b275|3|(math.ceil(12000/3500),12000/3500)|(4.,3.43)|Payload-only trip count with distributable items; integer ceiling distinct from fractional quotient and vehicle timing.
b275|4|(9.81*1.2**2*2/2,9.81*1.2**2*2/2*1.2/3)|(14.1264,5.65056)|Interior equally spaced post tributary width and one-sided hydrostatic pressure; external load, not anchor rating.
b275|5|(.4*(30-5),.4*(30-5)/8)|(10.,1.25)|Coulomb scale with effective normal action, no anchors/passive force or approval inference.
b275|6|(12-9,(12-9)/12*100)|(3.,25.)|Pure uniform-seal geometry, no constitutive pressure or watertightness guarantee.
b275|7|((.012-.008)*1800/40,)|(.18,)|Fixed actual flows and storage area over stated interval, rainfall and varying head excluded.
b275|8|(min(102,101.7,101.9)-101.5,)|(.20,)|Common datum and minimum effective continuous crest, allowances and performance separate.
b275|9|(.98**4,.98**4*100)|(.92236816,92.2368)|Explicit independent necessary-stage success, excludes common cause and structural/flood exceedance.
b275|10|(1-.05**(1/30),(1-.05**(1/30))*100)|(.09503,9.503)|Exact one-sided95percent zero-failure frequentist binomial bound under independent identically distributed trials with fixed probability.
'''
COURSE_NOTES={
'b261':'Publication history1949 USBR and2020 EPANET kept separate from construction. Independently checked USBR official indexed first-issue statement, EPANET pressure-demand scope, NYC2025 renewed procurement and SFPUC planning status. EPANET expressly not a rapid transient solver. Institutions are source associations with null securities. Synthetic pressure/timing example recomputed.',
'b262':'Historical penstock reference and EPANET scope do not imply current code approval. Independent NYC/SFPUC checks support incomplete/planning wording.2021 mainlaying amendment identified specifically; named cases remain comparisons. Institutional roles do not assert contracting. Sling sensitivity73.2% independently recalculated with vertical angle convention.',
'b263':'Independently checked WSD Q-Leak July2021 opening and varied materials/training, and WIN district-flow/pressure purpose.2017 housing-estate guideline and2010 EPA guide identified as local/historical references. Training accuracy never generalized to city-wide performance. False distractors, signed delay sensitivity and institution-only roles reviewed.',
'b264':'EPANET official documentation confirms pressure-dependent demand and mass-balance scope; PUB primary announcement15April2021 is300000 meters planned for rollout, not a2021 completed installation. WSD WIN is district monitoring, customer meters a different scale. Balance facts and20% residual sensitivity checked; all security claims null.',
'b265':'Same verified EPA/WSD/PUB primary source set appropriately used for pressure-management context. History distinguishes2020 model capability from2021 metering announcement. No actual gains/pressure settings or blanket method adoption attributed to named projects. Both leakage exponents and sensitivity reductions recalculated; institutional roles verified.',
'b266':'Independent primary Water Corporation evidence confirms2006 Kwinana and2011 Binningup production. California page states May2015 amendment. Opened panel report via official link and read12May2025 response limiting2024 report to high-level guidance, not sole compliance procedure. Course accurately carries that limitation; synthetic flows not site settings.',
'b267':'EPA primary indexed manual confirms December2024 PLUMES2.0. Source scope properly requires negative-buoyancy and seabed submodel checks rather than claiming universal brine validation. Owner production dates independently confirmed;2015 California event is jurisdiction-specific. Mass dilution definitions and diameter sensitivity checked; no unsupported contractor/security claims.',
'b268':'USBR official record independently confirms substantial completion26September2012 and operations transfer28September, not the older research plant. EBMUD official page distinguishes2011 completion from2014 first drought use. Guides2006/2009 and HEC thresholds have explicit species/grain-scope limitations. Stokes sensitivity and Reynolds numbers independently checked.',
'b269':'USGS2010 stage report and2010 leveling publication independently verified. Historical Vicksburg record explicitly supports January1977 downstream I20 location and datum/slope caveat.2026 timeline is a curriculum source check, not station construction. Lees Ferry/NOAA roles are data/architecture examples; no invented field battery installation. Rating sensitivity independently checked.',
'b270':'Independent official USACE indexed release verifies first storm operation29August2012; DSD confirms Sheung Wan commissioning2009.2020 EM3105 source explicitly catalogue-only, not misidentified old PDF.2018 DSD manual is version-bounded. Pump curves and N-1 flows synthetic, source institutions not inferred contractors; operating-point sensitivity recalculated.',
'b271':'DSD primary pages independently confirm Tai Hang Tung September2004 and Happy Valley full commissioning16March2017. EPA2017 hydraulic reference supports storage/control scope, not exact equivalence of hand model to software. Orifice diameter/area and drawdown sensitivities verified. Institutions and actual synthetic fact units reviewed.',
'b272':'Manitoba primary page confirms original1962–1968 works; DSD independently confirms Yuen Long2003 start/2006 completion. History separates bypass function from assumed weir/roughness.2017 SWMM and2018 DSD scopes are method references. Fixed-geometry Manning sensitivity checked; no field operating instruction or unverified supplier role.',
'b273':'Official USBR catalogue independently confirms2011 protective filters,2012 embankment construction and2014 seepage chapters; large PDFs were not represented as fully read. USACE2013 South River Road release distinguishes cutoff completion, previous-year embankment and future follow-on work. Dam guidance transfer is bounded rather than claimed as levee criteria. Synthetic consolidation sensitivity checked; institution roles and null securities reviewed.',
'b274':'EA primary release independently confirms Bewdley north2004/south2006 completion and2020 seepage/joint maintenance. EA2025 Boston page separates primary gate December2020 completion, first protective operation2021 and future whole-scheme work. USACE2022 manual is explicitly catalogue-only; restricted text is not treated as verified criteria. Hydrostatic sensitivity recomputed; educational institutions and null securities checked.',
'b275':'Opened EA284-page guide and verified August2011 copyright, distinct from2010 landing-page label and2021 posting. EA12September2025 release explicitly distinguishes Beales operational completion from continuing landscaping. Operator StEB confirms Cologne fixed/mobile elements and stage-dependent coordination; no live trigger reused. Regional Rhine pin is public context, not a precise installation coordinate. All reliability confidence bounds and independent-stage sensitivity recomputed; source roles and null securities checked.',
'b276':'Independently opened NRCS2007 supplement and verified Winooski context;2020 national standard directory directs users to local criteria. EEA Regge1998 start is distinct from an old expected2025 completion. Loads remain synthetic and no claim of identical adopted methods is made. Explicit fixed-slope hydraulic-radius sensitivity now recomputed; institutional roles are publications, not contractors.',
'b277':'Opened NRCS2007 grade supplement; Blue Creek1997 and2002 are survey profiles, with construction discussed separately, and Mink Creek is Manitoba. National2020 directory is not local approval. HEC Shields page confirms formulation-dependent thresholds. Hypothetical spacing sensitivity independently recomputed, no unsupported procurement or securities claims.',
'b278':'NOAA official2023 directory scope is accurately limited and USBR2009 screening guide is not conflated with upstream passage. Official indexed USACE2014 record confirms McNary lamprey prototype rather than measured success rate. Bonneville is a counting reference only. Independently recalculated head-to-velocity sensitivity and species-specific limitations; source institutions and null securities checked.',
'b279':'Independent EEA page confirms Skjern1968 channelization and1999–2003 restoration, distinct from1992/2018 image dates. Regge1998 programme start retained without claiming projected2025 completion. Public regional pin is compatible with lower Skjern context. Second educational institution corrected to distinct NRCS. Sinuosity sensitivity checked and no hydraulic/ecological benefit inferred solely from that ratio.',
'b280':'Independently opened HEC network manual, NWS HEFS FAQ and CW3E Russian River page. They support network/routing distinctions, late2017 MARFC experiment and FIRO development since2014, respectively. Course does not conflate programmes, reuse obsolete service schedules or turn hypothetical releases into approved operations. Fixed-denominator exceedance sensitivity and all synthetic fact values checked; roles are source institutions with null securities.'
}
ISSUES=[{'courseIds':['b268'],'field':'example','status':'RESOLVED','finding':'Unrounded Stokes sensitivity gives Reynolds0.009575214; five-decimal display should0.00958 rather than0.00957. Author corrected both languages; final example independently reread and recomputed.'},{'courseIds':['b276','b277','b278','b279','b280'],'field':'example','status':'RESOLVED','finding':'Integrated examples initially compared baseline mechanisms without required changed-parameter sensitivity. Author added explicitly fixed-condition sensitivity in all five river-extension courses; independently recomputed all five final examples.'},{'courseIds':['b279'],'field':'vendors','status':'RESOLVED','finding':'Initial two institution cards were both EEA. Author selected already-cited NRCS as the distinct second educational source institution; final role statements and URLs checked.'}]
SENS=r"""
b261|(1000*1100/1e6,2*5000/1100)|(1.10,9.09)
b262|(100/(2*math.cos(math.radians(60))),(math.cos(math.radians(30))/math.cos(math.radians(60))-1)*100)|(100.,73.2)
b263|((200-1100*.040)/2,(200-1000*.041)/2)|(78.,79.5)
b264|(1010-100-800-50,((1010-100-800-50)/50-1)*100)|(60.,20.)
b265|(10*(30/40)**.5,10*(30/40)**1.2,(1-(30/40)**.5)*100,(1-(30/40)**1.2)*100)|(8.660,7.081,13.4,29.2)
b266|(.5/.4,(.45/.4-1)*100,(.5/.45)/10,(.5/.4)/10)|(1.250,12.5,.1111,.1250)
b267|(.05/(math.pi*.2**2/4),.05/(math.pi*.22**2/4),(1-(.2/.22)**2)*100,(.05/(math.pi*.2**2/4))/math.sqrt(.15*.2),(.05/(math.pi*.22**2/4))/math.sqrt(.15*.22),(1-(.2/.22)**2.5)*100)|(1.5915,1.3153,17.36,9.1888,7.2407,21.20)
b268|((2650-1000)*9.81*(22e-6)**2/(18*.001),(1.1**2-1)*100,1000*((2650-1000)*9.81*(20e-6)**2/(18*.001))*20e-6/.001,1000*((2650-1000)*9.81*(22e-6)**2/(18*.001))*22e-6/.001)|(.0004352,21.,.00719,.00958)
b269|(20*(2.1-.5)**1.6,((1.6/1.5)**1.6-1)*100)|(42.43,10.88)
b270|(2*math.sqrt((10-3.3)/1.05),(1-math.sqrt((10-3.3)/(10-3)))*100)|(5.052,2.17)
b271|(.62*.121*math.sqrt(2*9.81),1/(1.1**2)*100)|(.3323,82.64)
b272|((1/.036)*40*(40/24)**(2/3)*math.sqrt(.0004),(1-.030/.036)*100)|(31.24,16.67)
b273|(.848*2**2/1.1e-7/86400,(1-1/1.1)*100)|(356.90,9.09)
b274|(9.81*3.3**2/2,9.81*3.3**3/6,(1.1**2-1)*100,(1.1**3-1)*100)|(53.41545,58.7570,21.,33.1)
b275|(.99**4,(.99**4-.98**4)*100)|(.96059601,3.822785)
b276|(1000*9.81*.88*.003,(.88/.8-1)*100)|(25.8984,10.)
b277|(.66/(.012-.004),(.66/.6-1)*100)|(82.5,10.)
b278|(math.sqrt(2*9.81*.18),(math.sqrt(.18/.15)-1)*100)|(1.879255,9.54)
b279|(1980/1200,(1980/1800-1)*100)|(1.65,10.)
b280|(10/20,(10/20-8/20)*100)|(.5,10.)
"""

def run():
 rows=[]
 for text in ROWS.strip().splitlines():
  if not text.strip():continue
  cid,n,expr,expected,boundary=text.split('|');n=int(n)
  p=H/'inputs'/f'{cid}.json';d=json.loads(p.read_text());u=d['units'][n-1]
  actual=eval(expr,{'__builtins__':{},'math':math,'max':max,'min':min,'sum':sum,'abs':abs,'round':round});wanted=ast.literal_eval(expected)
  terms=ast.parse(expected,mode='eval').body.elts
  tol=[max(1e-11,.5*float(Decimal(10)**Decimal(ast.get_source_segment(expected,x)).as_tuple().exponent))for x in terms]
  passed=len(actual)==len(wanted) and all(abs(a-b)<=t for a,b,t in zip(actual,wanted,tol))
  rows.append({'courseId':cid,'unit':n,'modelSha256':hashlib.sha256(u['model'].encode()).hexdigest(),'quizSha256':hashlib.sha256(u['misconception'].encode()).hexdigest(),'expression':ast.get_source_segment(expr,ast.parse(expr,mode='eval').body.elts[0]),'actual':actual[0],'expected':wanted[0],'tolerance':tol[0],'extraChecks':[{'expression':ast.get_source_segment(expr,node),'actual':actual[j],'expected':wanted[j],'tolerance':tol[j],'status':'PASS'if abs(actual[j]-wanted[j])<=tol[j] else'FAIL'}for j,node in enumerate(ast.parse(expr,mode='eval').body.elts)if j>0],'boundaryNotes':boundary+' Misconception independently read and false in its stated general claim.','status':'PASS'if passed else'FAIL'})
 courses=[]
 for cid,notes in sorted(COURSE_NOTES.items()):
  p=H/'inputs'/f'{cid}.json';d=json.loads(p.read_text());meta={k:v for k,v in d.items()if k!='units'}
  courses.append({'courseId':cid,'inputSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'metadataSha256':hashlib.sha256(json.dumps(meta,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),'metadataNotes':notes,'sourceURLs':[x['url']for x in d['sources']],'status':'PASS'})
 sens=[]
 for line in SENS.strip().splitlines():
  cid,expr,wanted=line.split('|');actual=eval(expr,{'__builtins__':{},'math':math,'max':max,'min':min,'sum':sum,'abs':abs,'round':round});expected=ast.literal_eval(wanted)
  terms=ast.parse(wanted,mode='eval').body.elts
  tolerance=[max(1e-11,.5*float(Decimal(10)**Decimal(ast.get_source_segment(wanted,x)).as_tuple().exponent))for x in terms]
  sens.append(dict(courseId=cid,expression=expr,actual=actual,expected=expected,tolerance=tolerance,status='PASS'if all(abs(a-b)<=t for a,b,t in zip(actual,expected,tolerance))else'FAIL'))
 rows.sort(key=lambda x:(x['courseId'],x['unit']))
 reviewed_keys={(x['courseId'],x['unit'])for x in rows}
 expected_keys={(f'b{n}',i)for n in range(261,281)for i in range(1,11)}
 bad=[x for x in rows if x['status']!='PASS'];complete=len(rows)==200 and reviewed_keys==expected_keys and len(courses)==20 and len(sens)==20 and not bad and not any(x.get('status')=='OPEN'for x in ISSUES) and all(x['status']=='PASS'for x in sens)
 out={'date':'2026-10-21','reviewer':'/root/ai_sync','nonAuthorReviewer':True,'status':'PASS'if complete else'IN_PROGRESS','method':'Independent expressions manually transcribed from displayed input models; author audit scripts were not executed or copied. Rounded displayed quantities checked within half final digit. Misconceptions and physical bounds reviewed alongside models.','expectedCourses':[f'b{x}'for x in range(261,281)],'modelCount':len(rows),'passes':sum(x['status']=='PASS'for x in rows),'rows':rows,'courses':courses,'issues':ISSUES,'sensitivityChecks':sens}
 (H/'reviews'/'peer_ai_sync.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'models':len(rows),'failures':bad,'metadataCourses':len(courses),'sensitivityFailures':[x for x in sens if x['status']!='PASS']},ensure_ascii=False))
if __name__=='__main__':run()
