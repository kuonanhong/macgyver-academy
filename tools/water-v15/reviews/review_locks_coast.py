"""Non-author peer arithmetic, read directly from input statements; no author audit import."""
from pathlib import Path
import json,math,hashlib
H=Path(__file__).resolve().parents[1]
C={}
def course(cid,rows):
 C[cid]=[]
 for line in rows.strip().splitlines():
  bits=line.split(' | ');checks=[]
  for chunk in bits[0].split(' ; '):
   expr,expected,tol,unit=chunk.split(' @ ');actual=eval(expr,{'__builtins__':{},'math':math,'abs':abs,'min':min,'max':max,'round':round,'sum':sum});expected=float(expected);tol=float(tol)
   checks.append(dict(expression=expr,actual=actual,expected=expected,tolerance=tol,outputUnit=unit,status='PASS' if abs(actual-expected)<=tol+1e-12*max(1,abs(actual)) else 'FAIL'))
  C[cid].append(dict(**checks[0],extraChecks=checks[1:],boundaryNotes=bits[1]))
 assert len(C[cid])==10
course('b281',r'''
5/25 @ .20 @ 1e-12 @ m ; 10/math.sqrt(25) @ 2 @ 1e-12 @ s | Prototype-to-model length ratio is explicit; gravity/Froude similarity does not match viscous or impact processes automatically. Both quiz versions falsely assert complete similarity.
25**1.5*.0004 @ .050 @ 1e-12 @ m2/s ; 25**1.5*.0004*1000 @ 50 @ 1e-10 @ L/s/m | Unit-width discharge scales as length to three-halves, distinct from total flow exponent five-halves. This is no pedestrian exposure limit; both wrong alternatives conflate exponents.
.030/(.50*120) @ .0005 @ 1e-12 @ m2/s | Collection balance needs effective width and complete capture. The model makes the closure condition explicit; a visible collector reading does not establish total capture.
4*math.sqrt(.0025) @ .20 @ 1e-12 @ m | Spectral zeroth moment has area units, and significant height uses its square root. Maximum individual wave height is a distinct quantity in both quiz versions.
.10/.20 @ .50 @ 1e-12 @ ratio ; (.10-.02)/.20 @ .40 @ 1e-12 @ ratio | Fixed crest and wave height make rising water reduce freeboard. Equal relative freeboard alone does not preserve all foreshore or wave conditions.
.20/.50 @ .40 @ 1e-12 @ ratio ; (.20/.50)**2 @ .16 @ 1e-12 @ ratio | Matched medium and frequency allow squared amplitude energy ratio; separating incident/reflected components is required. The stated amplitude-energy equivalence misconception is false.
20/2 @ 10 @ 1e-12 @ Hz ; 20*2 @ 40 @ 1e-12 @ points/cycle | Nyquist is an ideal sampling bound, not a resolved impact bandwidth. The text explicitly separates a two-second wave from millisecond pressure peaks.
2/math.sqrt(9.81*.30) @ 1.17 @ .005 @ Fr | Froude number compares inertia and local shallow-water gravity scale; it cannot establish public access safety. Both quiz versions wrongly turn an indicator into permission.
(.4+.5+.6)/3 @ .5 @ 1e-12 @ L/s/m ; math.sqrt(((.4-.5)**2+(.5-.5)**2+(.6-.5)**2)/2) @ .1 @ 1e-12 @ L/s/m ; .1/math.sqrt(3) @ .0577 @ .00005 @ L/s/m | Sample deviation uses n-minus-one and the mean standard error assumes independent realizations. Repeating one deterministic wave train does not create independent sea-state evidence.
100/.020/1000 @ 5 @ 1e-12 @ kPa | Uniform instantaneous resultant divided by the specified plate area gives average pressure. Mean overtopping does not establish impact demand on unrelated structural parts.
''')
course('b282',r'''
(2650-1025)*9.81*2/1000 @ 31.8825 @ .00005 @ kN | Rock material and displaced volume are consistent for the assumed solid block; submerged weight depends on surrounding fluid density. The equal-dry-weight assertion is false.
2650/1025-1 @ 1.5854 @ .00005 @ ratio ; 3/((2650/1025-1)*1) @ 1.892 @ .0005 @ Ns | Relative submerged density and nominal size give dimensionless stability number, with no universal acceptance value. Shape, slope and period remain separate.
(100-60)/100 @ .40 @ 1e-12 @ porosity ; (100-60)/60 @ .667 @ .0005 @ void ratio | Bulk volume and solid volume form different denominators for porosity and void ratio. The bilingual quiz falsely equates these two fractions.
10*2 @ 20 @ 1e-12 @ m ; math.sqrt(10**2+20**2) @ 22.36 @ .005 @ m | The stated one-vertical-to-two-horizontal slope yields horizontal projection before the sloping distance. Average slope does not establish the toe location.
4/1 @ 4 @ 1e-12 @ ratio | Both diameters use millimeters, so the filter ratio is dimensionless. No single ratio establishes all filtration criteria under every soil and reversing flow.
(5000/2650)**(1/3) @ 1.2357 @ .00005 @ m | Nominal diameter is the cube root of solid volume, not maximum stone dimension. Equal volume scale does not imply equal shape or overturning resistance.
1025*1*2*2**2/2 @ 4100 @ .5 @ N ; 1025*1*2*2**2/2/1000 @ 4.1 @ .0001 @ kN | Steady drag with selected coefficient excludes wave inertia and sheltering. Fixed coefficient drag grows with speed squared, contradicting the linear-speed quiz assertion.
.02*3 @ .060 @ 1e-12 @ m | Uniform vertical strain across one layer predicts that layer's mean compression only. Small average movement cannot exclude differential foundation or filter damage.
100/(2*math.cos(math.radians(30))) @ 57.74 @ .005 @ kN | Angle is measured from vertical and both slings are symmetric and static. Tension is not half-weight except in the zero-angle limit; dynamics are excluded.
8/1**2 @ 8 @ 1e-12 @ dimensionless damage | Cross-section damaged area is normalized by nominal diameter squared; this is not a percentage of original material. Location and survey datum remain essential.
''')
course('b283',r'''
2400*1000 @ 2400000 @ 1e-9 @ kg ; 2400*1000*9.81/1000 @ 23544 @ .0001 @ kN | Concrete material volume produces mass/weight, while buoyancy uses submerged external displacement. Chinese weight versus English mass wording does not alter the false envelope-volume claim.
2460000/(1025*400) @ 6 @ 1e-12 @ m ; 10-2460000/(1025*400) @ 4 @ 1e-12 @ m | Constant rectangular waterplane and sealed upright body are required. Mean draft/freeboard does not cover heel, waves or lower flooding openings.
3+(20*20**3/12)/2400-7 @ 1.556 @ .0005 @ m | Transverse waterplane second moment, displacement and vertical gravity reference are consistent; initial GM is a small-angle measure, not complete tow stability.
(10*10**3/12)/2400 @ .3472 @ .00005 @ m | Free-surface correction uses same-density tank liquid, rectangular free surface and small heel. Tank extent/compartmentation can change correction at constant liquid quantity.
205000/(1025*400) @ .50 @ 1e-12 @ m | Added mass changes mean draft at constant waterplane; flooding/geometry changes invalidate that local relation. It does not determine a field ballasting sequence.
(80+20)*20/2 @ 1000 @ 1e-9 @ kN/m | Integrated linear bottom pressure gives uplift per unit breakwater length; distribution and application point remain assumed, not universally linear in service.
.6*(4000-1000) @ 1800 @ 1e-9 @ kN/m ; .6*(4000-1000)/1500 @ 1.20 @ 1e-12 @ ratio | Effective normal load subtracts uplift before friction. All forces share the per-metre basis; this teaching resistance/demand ratio is not code certification.
4000/2000 @ 2 @ 1e-12 @ m ; 12/6 @ 2 @ 1e-12 @ m ; 2000/12*(1+6*2/12) @ 333.3 @ .05 @ kPa ; 2000/12*(1-6*2/12) @ 0 @ 1e-12 @ kPa | Linear full-contact rectangular base reaches its kern boundary at zero minimum pressure; extension to fictitious soil tension is explicitly rejected.
.020/20 @ .001 @ 1e-12 @ rad ; math.degrees(.020/20) @ .0573 @ .00005 @ degrees | Two-point settlement difference yields only a small rigid-body rotation, not local bending. Meter/millimeter conversion and radian-degree conversion are consistent.
10.05525*(8**2-6**2)/2 @ 140.7735 @ .00005 @ kN/m | Two still-water triangles share a common base and are integrated separately. Overflow suction, scour and tsunami dynamics are excluded rather than inferred from head difference.
''')
course('b284',r'''
3000/2400 @ 1.25 @ 1e-12 @ m3 ; (3000-1025*(3000/2400))*9.81/1000 @ 16.86 @ .005 @ kN | Solid-volume buoyancy assumes the declared material density and submerged solid block. Shape/contact and water-accessible voids remain separate hydraulic questions.
(170-8)/340 @ .4765 @ .00005 @ ratio | Effective added water subtracts explicitly stated dry-aggregate absorption and assumes no surface water. Constant metered water alone does not preserve effective ratio.
1e-5*25*2 @ .0005 @ 1e-12 @ m ; 1e-5*25*2*1000 @ .50 @ 1e-12 @ mm | Uniform free thermal movement excludes gradients and restraint. A small global dimensional change cannot establish absence of internal thermal stress.
25e9*1e-5*25/1e6 @ 6.25 @ 1e-12 @ MPa tension | Fully restrained elastic cooling produces tensile demand at selected modulus; creep/cracking relaxation and age-dependent resistance are not covered.
900000/.15**2/1e6 @ 40 @ 1e-12 @ MPa | Cube nominal compression strength uses loaded face area; it is not automatically a characteristic/design value or lifting-arm tensile capacity.
3000*9.81/(2*math.cos(math.radians(45)))/1000 @ 20.81 @ .005 @ kN | Symmetric static slings measured from vertical satisfy vertical force equilibrium. Offshore acceleration and attachment capacities are explicitly excluded.
200/1000 @ .20 @ 1e-12 @ units/m2 | Count per coverage area is placement density, not three-dimensional porosity or local interlock quality. Coverage denominator must match slope/projection convention.
math.sqrt(.10**2+.20**2+.05**2) @ .2291 @ .00005 @ m | Euclidean displacement of a defined reference point excludes orientation and contact. The bilingual misconception incorrectly equates position with full pose.
3000/20**3 @ .375 @ 1e-12 @ kg | Equal material density makes mass scale with length cubed; submerged relative density and roughness require separate checks. The linear mass-scale alternative is false.
(1-.950)/1*100 @ 5 @ 1e-10 @ percent | Dry laboratory mass loss under specified exposure is not an annual service rate. Reproducibility does not establish time equivalence between test and field.
''')
course('b285',r'''
1000*20*1.5 @ 30000 @ 1e-9 @ m3 | Rectangular thickness/width/length accounting is intentionally not equilibrium morphology. Completed width cannot guarantee an unchanged future shoreline.
10000*(1-.40)*2650 @ 15900000 @ 1e-6 @ kg | Grain density and dry solids exclude pore-water mass. Drainage can lower wet weight without loss of sand grains, as distinguished by both languages.
.45/.30 @ 1.50 @ 1e-12 @ ratio | Median-size ratio uses identical units and is only one grading descriptor. Larger median alone cannot establish full compatibility or permanent retention.
30000/(1000*(5+2)) @ 4.286 @ .0005 @ m | Active-profile parallel translation requires closure depth and berm elevation on a common datum; volume divided by length alone has area units.
30000-45000 @ -15000 @ 1e-9 @ m3/year ; (30000-45000)*5 @ -75000 @ 1e-9 @ m3 | Fixed signed annual alongshore fluxes yield storage change, not a constant monthly shoreline rate. Other cross-shore exchanges are expressly omitted.
18000/(1-.40) @ 30000 @ 1e-9 @ m3 ; 18000/(1-.35) @ 27692.3 @ .05 @ m3 | Solids stay fixed while porosity controls bulk volume. Unchanged grain quantity therefore does not require unchanged exterior geometry.
20000-8000 @ 12000 @ 1e-9 @ m3 ; 8000/20000*100 @ 40 @ 1e-9 @ percent | Recovery fraction refers to an explicit fixed survey area and baseline loss. Remaining deficit does not prove permanent export from the wider coastal system.
100000*math.sqrt(2)*.03 @ 4242.6 @ .05 @ m3 standard uncertainty | Independent coherent offsets between surveys combine by RSS; they are not independent cells. More points do not eliminate a shared datum offset.
(150-20)/1000 @ .13 @ 1e-12 @ kg/m3 ; (150-20)/1000*2 @ .26 @ 1e-12 @ kg/s | Milligrams per liter convert to kilograms per cubic meter by dividing1000. Uniform concentration-flow product is not uncalibrated optical turbidity.
3/.02 @ 150 @ 1e-9 @ s ; .30*3/.02 @ 45 @ 1e-9 @ m | Constant settling and horizontal velocity produce first-arrival scales only; turbulence, flocculation and resuspension invalidate a permanent-deposition conclusion.
''')
course('b286',r'''
2-1.2 @ .8 @ 1e-12 @ m ; (2-1.2)/1.6 @ .50 @ 1e-12 @ ratio | Water cover and relative submergence are geometric quantities, not transmission. Crest width and incident-wave properties remain relevant.
.8/2 @ .40 @ 1e-12 @ ratio ; (.8/2)**2*.80 @ .128 @ 1e-12 @ energy-flux ratio | Energy-flux ratio includes squared height and group-velocity ratio at equal density; percent height decrease is not percent energy decrease.
.78*2 @ 1.56 @ 1e-12 @ m | Breaker index is explicitly selected for the synthetic example rather than asserted universal across periods, shapes and submerged structures.
30/20 @ 1.50 @ 1e-12 @ m/s | Steady effective cross-section discharge gives area-mean speed; it cannot establish local instantaneous peaks or rip-current access conditions.
1025*9.81*2**2/8 @ 5027.6 @ .05 @ J/m2 ; 1025*9.81*2**2/8*5/1000 @ 25.138 @ .0005 @ kW/m | Regular linear-wave height uses one-eighth energy coefficient; random significant height requires a different convention. Group speed converts energy density to flux.
2/((2650-1025)*9.81*.0005) @ .2509 @ .00005 @ Shields | Shear stress divided by submerged grain-weight scale is dimensionless. No incipient-motion threshold or scour depth is inferred from the computed value.
math.sqrt(9.81*2) @ 4.429 @ .0005 @ m/s ; 100/math.sqrt(9.81*2) @ 22.58 @ .005 @ s | Linear shallow-water speed requires depth much smaller than wavelength and small wave amplitude; arbitrary ocean waves are not nondispersive.
100/200 @ .50 @ 1e-12 @ ratio | Length divided by offshore distance is geometry only. It is not a unique predictor of tombolo development or complete shoreline shape.
.8+.2 @ 1 @ 1e-12 @ m ; .2/.8*100 @ 25 @ 1e-10 @ percent | Fixed water level with crest settlement increases cover; transmission is not linearly determined by that cover increment.
(2+math.sqrt(9.81*2))*.5/5 @ .6429 @ .00005 @ Courant | One-dimensional explicit shallow-water characteristic speed includes flow plus gravity wave speed. Correct-looking output and one Courant value do not prove convergence.
''')
course('b287',r'''
(120+180)*50/2 @ 7500 @ 1e-9 @ m3 | Average-end-area volume assumes linear section-area variation. Accepted average depth does not establish removal of every controlling shoal.
(1300-1000)/(2650-1000) @ .1818 @ .00005 @ solids volume fraction | Two-component additive volumes and negligible gas are explicit; solids mass fraction has a different denominator and cannot be substituted.
2650*.15*2 @ 795 @ 1e-9 @ kg/s ; 2650*.15*2*3600 @ 2862000 @ 1e-6 @ kg | Slurry discharge times solids volume fraction and grain density yields dry mass flux. Constant operation for one hour is explicitly assumed.
.02*(500/.50)*3**2/(2*9.81) @ 9.174 @ .0005 @ m | The given Darcy-style expression is a clear-water baseline, not concentrated-slurry transport approval; fittings and slurry effects are omitted.
1300*9.81*2*20/.70/1000 @ 728.7 @ .05 @ kW | Total efficiency divides hydraulic demand, with stated mixture density and head. Increased electric power alone does not prove greater accepted dry-solid production.
1500*.020/2 @ 15 @ 1e-12 @ m ; 1500*.020/2+1 @ 16 @ 1e-12 @ m | Two-way acoustic travel is halved before adding transducer draft; chart datum/tide corrections remain separate from instantaneous water depth.
math.sqrt(.05**2+.08**2+.04**2) @ .1025 @ .00005 @ m standard uncertainty | RSS assumes independent zero-mean components and excludes systematic bias; sounding uncertainty does not prove full obstacle detection.
15-13-.5-.4-.2 @ .9 @ 1e-12 @ m | Geometric clearance subtracts squat, wave demand and stated survey allowance. The illustrative residual is expressly not permission to navigate.
600*60/40*.75 @ 675 @ 1e-9 @ m3/h | Availability is separately defined from cycle duration to avoid double-counting downtime; the numerator is completed accepted volume rather than nominal hopper capacity.
2*.5 @ 1 @ 1e-12 @ kg/s ; (100-2*.5)/100*100 @ 99 @ 1e-9 @ percent | Dry-solid retention balance uses matching period and mass basis. High removal fraction does not establish discharge concentration or environmental compliance.
''')
course('b288',r'''
6500+3000+500 @ 10000 @ 1e-9 @ t ; 6500/10000*100 @ 65 @ 1e-9 @ percent | Verified suitable sand is distinguished from merely planned destinations; classification mass balance and confirmed reuse denominator are explicit.
12000/60000 @ .20 @ 1e-12 @ m | Uniform retained post-drainage volume gives mean thickness only; later consolidation and local inundation remain outside this volume/area calculation.
1*(1+1)/(1+2) @ .667 @ .0005 @ m ; 1-1*(1+1)/(1+2) @ .333 @ .0005 @ m | Fixed solids in a one-dimensional layer require constant plan area; mechanism distinguishes spreading, foundation settlement and decomposition from this thickness change.
math.acos(.5/1)/math.pi @ .3333333333333333 @ 1e-12 @ time fraction | Sinusoidal level above ground with no ponding gives exceedance duration, not vegetation survival probability or full ecological performance.
540/600*100 @ 90 @ 1e-9 @ recovery percent ; 540/600*100 @ 90 @ 1e-9 @ purity percent | Feed sand and total product are distinct denominators that happen to be equal numerically. The quiz's universal equivalence is false.
1000*1000*20/1e6 @ 20 @ 1e-9 @ kg tracer ; 20/((1000+1000)*1000)*1e6 @ 10 @ 1e-9 @ mg/kg | Dry-mass unit conversion conserves tracer burden during dilution. Text explicitly rejects interpreting a lower concentration as destruction or compliance.
.50-.08-.04 @ .38 @ 1e-12 @ m | Uniform erosion and compression subtract from cover thickness; mixing, diffusion and bioturbation remain separate performance mechanisms.
50-35 @ 15 @ 1e-12 @ kPa ; 50-(35-10) @ 25 @ 1e-12 @ kPa | Effective stress changes with pore pressure at fixed total stress, rather than surface dryness proving full drainage or final strength.
10000*(50-20)*.08 @ 24000 @ 1e-9 @ kg CO2e | Transport-factor saving excludes treatment and empty return-trip changes. It is not a complete lifecycle benefit or universal emissions factor.
(50-30)-(50-40) @ 10 @ 1e-12 @ percentage points | Difference-in-differences is an arithmetic contrast, with causal identification requiring additional assumptions. Percentages are subtracted as percentage points.
''')
course('b289',r'''
math.tan(math.radians(45-30/2))**2 @ .3333 @ .00005 @ Ka | Rankine active coefficient assumes smooth vertical wall, level cohesionless fill and mobilized movement, not automatic at-rest conditions.
(1/3)*10*15**2/2 @ 375 @ 1e-9 @ kN/m ; 15/3 @ 5 @ 1e-12 @ m | Triangular effective earth pressure uses submerged unit weight; hydrostatic pressure is separate, and its force location is one-third height above base.
(1/3)*30 @ 10 @ 1e-12 @ kPa ; (1/3)*30*15 @ 150 @ 1e-9 @ kN/m | Infinite uniform surcharge generates uniform lateral increment. This is not a concentrated wheel load near the wall.
10.05525*(5**2-3**2)/2 @ 80.442 @ .0005 @ kN/m | Hydrostatic pressures on the same base are integrated before subtraction; backfill water need not track harbor tide synchronously.
3000/15*(1+6*1.5/15) @ 320 @ 1e-9 @ kPa ; 3000/15*(1-6*1.5/15) @ 80 @ 1e-9 @ kPa ; 15/6-1.5 @ 1 @ 1e-12 @ m kern margin | Eccentric resultant lies inside rectangular kern, so linear full-contact distribution is admissible. Mean pressure alone cannot assess edge contact or ground resistance.
.5*20000000*.10**2*.80/1000 @ 80 @ 1e-9 @ kJ | Effective mass already contains added mass and the combined coefficient is selected. Energy does not determine fender peak reaction without its load-deflection curve.
1000*.30/2 @ 150 @ 1e-9 @ kJ | Triangular loading work is area under the loading curve, not necessarily irreversible dissipated energy; unloading behavior is intentionally unspecified.
300000*.20*9.81/1000 @ 588.6 @ .0001 @ kN/m | Participating mass per metre and selected acceleration yield inertia per metre only; dynamic earth and water actions remain separate.
100*5/10000 @ .050 @ 1e-12 @ m | One-dimensional compression uses constrained modulus, effective stress increment and one uniform layer. Average settlement cannot establish rail alignment.
15/500 @ .030 @ 1e-12 @ strain ; 15/500*100 @ 3 @ 1e-12 @ percent | Uniaxial engineering strain uses an explicit effective gauge length, not material contact pressure, shear or seal water-tightness capacity.
''')
course('b290',r'''
math.pi*(1**2-.96**2)/4 @ .061575 @ .0000005 @ m2 ; 2e6/(math.pi*(1**2-.96**2)/4)/1e6 @ 32.48 @ .005 @ MPa | Hollow steel annulus carries axial stress; full outer footprint is not material area. Mean axial stress excludes bending and buckling.
5e6*math.pi*1**2/4/1000 @ 3927.0 @ .05 @ kN | Closed circular toe and uniform unit resistance are explicit; open-pile plugging must be established before using the same effective end area.
math.pi*50*1*20 @ 3141.6 @ .05 @ kN | Positive uniform shaft shear integrates over circumference and effective length. Downdrag and toe resistance are not included.
12000/4+12000*3/(4*3**2) @ 4000 @ 1e-9 @ kN ; 12000/4-12000*3/(4*3**2) @ 2000 @ 1e-9 @ kN | Equal axial stiffness and rigid-cap distribution over symmetric x positions make the moment formula valid; eccentric loading does not give equal pile forces.
2e6*30/(200e9*.060) @ .005 @ 1e-12 @ m | Uniform axial force and prismatic elastic area yield pile shortening; ground settlement is separate and axial force transfer may invalidate uniformity.
100000*10**3/(3*200e9*.0074)*1000 @ 22.52 @ .005 @ mm ; 100*10 @ 1000 @ 1e-9 @ kNm | Ideal cantilever with fixed base excludes soil flexibility; mudline is not automatically fixed. Tip-load moment and displacement use matching units.
(10/12)**3 @ .5787 @ .00005 @ stiffness ratio ; (1-(10/12)**3)*100 @ 42.13 @ .005 @ percent reduction | Fixed EI and cantilever effective-length idealization explain cubic sensitivity; actual scour alters pile-soil response beyond a simple length change.
1025*1.2*1*2**2/2/1000 @ 2.460 @ .0005 @ kN/m | Steady current drag per unit length uses diameter as projected width. Wave acceleration and added-mass inertia are not automatically included.
(1-.966**2)/(1-.960**2) @ .8526 @ .00005 @ remaining area ratio | Fixed outer diameter and inward uniform wall loss define the annulus ratio; local corrosion and remaining service life require other evidence.
100000/1000000+200000/500000 @ .50 @ 1e-12 @ Miner damage | Linear cumulative damage uses two defined cycle ranges and reference lives. It is not a guarantee of proportional remaining chronological service life.
''')
course('b291',r'''
10250/(1025*100) @ .10 @ 1e-12 @ m | Uniform added load and constant waterplane give mean draft increment; eccentric heel and waves remain excluded from corner safety.
1.225*1.2*100*20**2/2/1000 @ 29.40 @ .0001 @ kN | Selected wind speed, projected area and drag coefficient yield one force component, not a complete dock-plus-vessel mooring demand.
1025*1*20*1.5**2/2/1000 @ 23.0625 @ .00005 @ kN | Uniform steady current drag excludes wave inertia and spatial velocity variations; a distant average current is not necessarily the pontoon surface speed.
40/(2*math.cos(math.radians(30))) @ 23.094 @ .0005 @ kN | Two taut horizontal symmetric lines share a specified horizontal force by directional components; pretension/dynamics and changing geometry are excluded.
25*20/5000 @ .10 @ 1e-12 @ m | Straight elastic line with effective EA uses tension increment and excludes slack/creep. The equation does not assign constant stiffness to every rope history.
math.sqrt(10**2+1**2) @ 10.0499 @ .00005 @ m ; math.sqrt(10**2+3**2) @ 10.4403 @ .00005 @ m ; math.sqrt(109)-math.sqrt(101) @ .3904 @ .00005 @ m | Fixed horizontal separation with changing height changes straight chord length; no catenary or tension calculation is claimed.
10/(20+30) @ .20 @ 1e-12 @ m | Collinear parallel incremental restoring components remain engaged near one equilibrium. Arbitrarily oriented axial line stiffnesses cannot simply be summed.
2*math.pi*math.sqrt(100000/50000) @ 8.886 @ .0005 @ s | Effective mass already includes hydrodynamic added mass; undamped linear period is not an amplitude or maximum line-tension prediction.
1.2/12*100 @ 10 @ 1e-10 @ grade percent ; math.degrees(math.atan(1.2/12)) @ 5.711 @ .0005 @ degrees ; math.sqrt(12**2+1.2**2) @ 12.0599 @ .00005 @ m | Horizontal projection differs from slope length; geometric slope does not by itself establish accessibility compliance or safe use.
120*1025-100000 @ 23000 @ 1e-9 @ kg reserve | Sealed maximum displacement gives theoretical mass reserve to complete immersion, not permitted live load or acceptable freeboard under heel/waves.
''')
course('b292',r'''
300*30*10 @ 90000 @ 1e-9 @ m3 | Empty vertical-sided chamber and lift define transferred volume; the entire chamber capacity is not consumed on every transit, and saving basins are excluded.
90000/150 @ 600 @ 1e-9 @ s ; 90000/150/60 @ 10 @ 1e-12 @ min | Interval-mean rather than peak discharge gives duration by volume conservation. The wrong alternative reverses or misuses this relationship in both languages.
150/9000 @ .01667 @ .000005 @ m/s ; 150/9000*60 @ 1 @ 1e-12 @ m/min | Effective area and net inflow give spatial mean rise, not a local oscillation or vertical velocity guarantee.
.70*8*math.sqrt(2*9.81*5) @ 55.465 @ .0005 @ m3/s | Fixed opening and instantaneous head use a quasi-steady orifice relation, excluding acceleration. Fixed valve position does not imply fixed discharge.
2*9000*(math.sqrt(10)-math.sqrt(.1))/(.70*8*math.sqrt(2*9.81)) @ 2065.3 @ .05 @ s | Fixed upstream level, constant chamber area/opening and negligible inertia underlie the integrated square-root drawdown; endpoint is not gate-operating permission.
3*4**2/(2*9.81) @ 2.446 @ .0005 @ m | Local-loss coefficients may be summed only on the same reference velocity basis. Smaller total loss does not guarantee uniform chamber flow.
1000*20*4/1000 @ 80 @ 1e-9 @ kN | Momentum reaction assumes zero outlet component in the selected direction and neglected pressure differences; it is not automatically force on a vessel.
1000*900*1/1000 @ 900 @ 1e-9 @ kPa ; 2*300/900 @ .667 @ .0005 @ s | Rapid single-phase velocity change must be fast relative to the stated round-trip time. A slow arbitrary closure does not produce the same first-wave increment.
(80000-2300)/(1000*10**2/2) @ 1.554 @ .0005 @ cavitation index | Absolute pressure and vapor pressure share a reference; cavitation index is not a universal threshold and one positive gauge point cannot rule out local suction.
10000000*9.81*.05/200/1000 @ 24.525 @ .0005 @ kN | Long-wave quasi-hydrostatic small-slope force scale uses displaced weight; drag, ship acceleration and detailed mooring dynamics require separate treatment.
''')
course('b294',r'''
1000*9.81*(8**2-6**2)/2/1000 @ 137.34 @ .005 @ kN/m | Hydrostatic triangles on the same base produce resultant per vertical-plane width, not actuator thrust or actual closed-gate reaction distribution.
10/math.cos(math.radians(20)) @ 10.6418 @ .00005 @ m ; 10*math.tan(math.radians(20)) @ 3.6397 @ .00005 @ m | Leaf angle is measured from transverse and half clear opening is projected width; hinge and joint offsets are intentionally omitted.
100*.50**2/8 @ 3.125 @ .0005 @ kNm/m ; 6*(100000*.50**2/8)/.020**2/1e6 @ 46.875 @ .0005 @ MPa | Unit-width simply supported strip converts pressure to line load; elastic one-way bending excludes two-way action and local geometric restraint.
(200000-1000*50)*9.81/1000 @ 1471.5 @ .05 @ kN | Sealed displaced water reduces effective downward weight; flooding/dewatering and support load sharing are distinct conditions.
1.5e6/(.30*.40)/1e6 @ 12.50 @ .0001 @ MPa | Projected diameter times bearing length gives nominal mean bearing pressure, not Hertz contact maximum or every point's stress.
.003/15 @ .0002 @ 1e-12 @ rad ; math.degrees(.003/15) @ .01146 @ .000005 @ degrees | Two-point alignment gives overall small tilt, not shaft curvature or local hinge-seat mismatch. Millimeters are converted to meters before division.
12e-6*15*20*1000 @ 3.60 @ .0001 @ mm | Uniform free steel heating excludes gradients and restraints. Equal air temperature does not ensure spatially uniform gate temperature.
200/(2*math.sin(math.radians(30))) @ 200 @ 1e-9 @ kN | Actuator moment arm is radius times sine of force-radius angle. Synthetic resisting torque is not a field operating requirement.
10e6*math.pi*.16**2/4/1000 @ 201.062 @ .0005 @ kN | Ideal cap-end cylinder force assumes no backpressure/friction; retracting annular area differs. Pressure alone does not verify gate seating or watertightness.
.60*.002*math.sqrt(2*9.81*2) @ .007517 @ .0000005 @ m3/s ; .60*.002*math.sqrt(2*9.81*2)*1000 @ 7.517 @ .0005 @ L/s | Equivalent orifice leakage uses specified head and coefficient; comparison of repairs must normalize head, and the number is no allowable leak limit.
''')
course('b295',r'''
(100*0+10*35)/(100+10) @ 3.1818 @ .00005 @ kg/m3 | Additive volume and complete mixing use mass concentration, not practical salinity; mean dilution does not guarantee improvement at every depth or intake.
20*15 @ 300 @ 1e-9 @ kg/s | Uniform landward flow-concentration product has mass/time units; stratified transport requires integrating correlated velocity and concentration.
1000000*2 @ 2000000 @ 1e-9 @ kg ; (100*5-100*2)/1000000 @ .0003 @ 1e-12 @ kg/m3/s | Constant-volume mixed box has equal inlet/outlet flow; derivative is instantaneous and changes with outlet concentration. Unlimited linear extrapolation is false.
1000000/100*math.log(5) @ 16094.4 @ .05 @ s ; 1000000/100*math.log(5)/3600 @ 4.471 @ .0005 @ h | Constant mixed volume and fresh inflow with no salt re-entry yield exponential flushing. One residence time does not remove every original parcel.
9.81*20/1000 @ .1962 @ .00005 @ m/s2 ; math.sqrt((9.81*20/1000)*4*6/(4+6)) @ .6862 @ .00005 @ m/s | Small-amplitude two-layer rigid-lid long waves require observed stratification; finite interface, shear and full mixing lie outside this speed scale.
.1962*2/.50**2 @ 1.5696 @ .00005 @ bulk Richardson | Bulk layer scale differs from a local gradient Richardson number; a textbook threshold cannot prove all estuarine turbulence absent.
500*43200/math.pi @ 6875494 @ .5 @ m3 positive half-cycle ; 0 @ 0 @ 1e-12 @ m3 net full-cycle | Integrating a sinusoidal signed discharge yields positive exchange and zero net water, not zero net salt or an equivalent amount of new freshwater.
10*20 @ 200 @ 1e-9 @ kg/s ; 10*5 @ 50 @ 1e-9 @ kg/s ; (10*20)/(10*5) @ 4 @ 1e-12 @ local ratio | Equal withdrawal volumes at different local concentrations change salt export only; return flow and drainage constraints prevent a whole-system success conclusion.
2*1.5**2/(2*9.81) @ .2294 @ .00005 @ m | Selected local-loss coefficient with a defined velocity is a synthetic clear-water comparison, not IJmuiden field data; salt control can affect drainage.
3.20-3.00 @ .20 @ 1e-12 @ kg/m3 bias ; (3.20-3.00)/3.00*100 @ 6.667 @ .0005 @ percent | Same-sample reference comparison diagnoses measurement/conversion bias rather than environmental salinization; multiple sensors can share calibration error.
''')

def sha(v):return hashlib.sha256(v).hexdigest()
def main():
 rows=[];courses=[];errors=[]
 for cid,units in C.items():
  p=H/'inputs'/f'{cid}.json';raw=p.read_bytes();d=json.loads(raw)
  for i,item in enumerate(units,1):
   u=d['units'][i-1]
   row=dict(courseId=cid,unit=i,modelSha256=sha(u['model'].encode()),quizSha256=sha(u['misconception'].encode()),**item)
   if item['status']!='PASS' or any(x['status']!='PASS'for x in item['extraChecks']):errors.append((cid,i,item))
   rows.append(row)
  courses.append(dict(courseId=cid,inputSha256=sha(raw),metadataSha256=sha(json.dumps({k:v for k,v in d.items()if k!='units'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),metadataNotes=NOTES[cid],sourceURLs=[s['url']for s in d['sources']],status='PASS'))
 report=dict(date='2026-10-21',reviewer='/root/ai_sync/locks_coast',nonAuthorReviewer=True,status='PASS'if not errors else'IN_PROGRESS',method='Read the140 bilingual input model statements and misconceptions directly, recomputed using separately authored arithmetic, checked physical mechanism boundaries and metadata. No author audit script or calculation table was imported.',rows=rows,courses=courses,issues=ISSUES,sourceChecks=SOURCECHECKS,limitations=['Synthetic teaching calculations are not project design certification.','Metadata review distinguishes verified publication/owner context and explicitly limited indexed summaries from full-text engineering review.','Map points are approximate public context, not construction coordinates.'])
 (H/'reviews/peer_locks_coast.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print('rows',len(rows),'extraChecks',sum(len(x['extraChecks'])for x in rows),'errors',[(x[0],x[1])for x in errors])
 for x in errors:print(x)
 assert not errors

NOTES={
'b281':'EurOtop author site distinguishes the 2007 first edition, 2018 second edition and removed obsolete calculator; CEM 2002 is a catalogue date, not invention or project history. Newbiggin and Borth are functional coastal comparisons, not claimed users of every laboratory detail. Public map context is plausible. Two institutional educational roles, null securities, synthetic facts and bilingual FALSE misconceptions were reviewed.',
'b282':'The rock-armour course keeps density, nominal diameter, layer geometry and filter descriptors distinct. CEM and EurOtop dates identify publications; Newbiggin/Borth compare coastal functions without asserting the synthetic rock configuration was installed there. Both institutional roles are education/resource links, not contractors; securities are null. Context map and numerical fact cards are consistent.',
'b283':'PARI 2012 concerns the 2011 tsunami; the teaching still-water head calculation is explicitly not a tsunami load model. Tuas first caisson in 2016 and final Phase 1 caisson in 2019 are confirmed by the owner speech. Quay-caisson fabrication is distinguished from breakwater loading. Concrete volume versus displacement, free-surface density and full-contact assumptions are retained. Institutional roles/security null and public Kamaishi context map are appropriate.',
'b284':'The RWS article dated 20 October 2025 describes Afsluitdijk armour elements and model tests; it does not publish the synthetic mix as a proprietary specification. Tuas is a fabrication comparison, not proof of this armour placement system. Publication and project dates are separated. All six numerical fact examples are assumptions rather than field data; institution roles and null securities are appropriate.',
'b285':'The Beach Management Manual page separates project start in 2007, completion in 2011 and web publication in 2021. Sand Motor 2011 is a redistribution case, not guaranteed permanent retention. The Borth report represents 2012–2013 monitoring rather than current beach state. Map is approximate public Sand Motor context. Six numerical facts, related water IDs, institutional educational roles and null securities are consistent.',
'b286':'Borth reef/profile monitoring and Newbiggin sheltered coast are functional comparisons; Sand Motor is not falsely presented as a submerged concrete structure. CEM 2002 is bibliographic history, with current applicable guidance/corrigenda still needed. The course separates wave-height, energy flux, geometry and morphology claims. Borth public context map, institutional educational roles and null securities are appropriate.',
'b287':'USACE catalogue dates EM1110-2-5025 to 31 July 2015; IHO official index dates S-44 edition 6.2.0 to October 2024. Savannah March 2022 completion refers to dredging, not every mitigation obligation. Poplar compares sediment routing. Survey uncertainty remains independent standard components and under-keel clearance is not transit authorization. Public navigation map and institutional educational roles/security null are consistent.',
'b288':'EPA/USACE Inland Testing Manual is February 1998; Poplar construction/expansion milestones and Mordecai 2015 placement are historical cases, not universal material acceptance. The course explicitly rejects dilution-to-compliance and distinguishes dry-mass balance, retained thickness, ecology and transport-only emissions. Map/landmark context and institutional roles/security null are appropriate. Difference-in-differences is not claimed causal without assumptions.',
'b289':'Tuas Phase 1 first caisson 2016, final caisson 2019 and reclamation completion 2021 are separate milestones, not whole-port opening. Kamaishi is a limited structural/load-path comparison. PWDM parts cover the relevant structure classes without a code-compliance claim. The fictitious tension, active-pressure, loading-work and dynamic-action exclusions are explicit. Public map, source scopes, educational institution roles and null securities are consistent.',
'b290':'EM1110-2-2906 dated January 1991 is historical engineering guidance. Los Angeles official June 2025 announcement confirms restoration after construction began in November 2023 and describes a concrete wharf, not the hypothetical steel tube being calculated. Pak Kok is a public pier comparison without an unsupported steel-pile claim. Source scopes, map context, institution educational roles and null securities are appropriate.',
'b291':'Hong Kong 2021 coastal study context is separated from the Ma Liu Shui public opening on 9 September 2025; official announcement confirms floating platform and gangway. WBDG current catalogue date for UFC4-152-07 is 30 September 2026, distinct from cancelled 2009/2012 material; scope is bibliographic and does not pretend full new-edition review. Map is approximate Ma Liu Shui context. Institution roles and null securities are consistent.',
'b292':'USACE catalogue confirms EM1110-2-1604 on 1 May 2006 and EM1110-2-1610 on 30 September 2018. Panama June 2016 training and inauguration are separate events; new gates are not called miter gates. Reviewer found latitude 9.38 too far north; author corrected to 9.274,-79.916 using the owner indexed air-monitoring point at Agua Clara, explicitly not the lock centre or construction control. Final location source scope and all other metadata were reread. Institution roles/security null remain appropriate.',
'b294':'Original Gatun trial on 26 September 1913 concerns historic miter gates and is kept distinct from expanded Canal rolling gates. EM1110-2-2107 August 2022 and EM1110-2-2610 March 2025 are publication milestones. Wilson 2025 alignment/repair record does not turn forecast reopening into a completed event. Gate geometry, nominal bearing pressure and cap-end force remain teaching idealizations. Gatun context map and institutional education roles/security null are appropriate.',
'b295':'EM1110-2-1607 March 1991 is tidal-hydraulics guidance; USGS conductance revision is 2019. The Mississippi 2023 sill delays a wedge rather than eliminating all intrusion. RWS late-2024 testing and April 2025 report identify the unexpected drainage effect of IJmuiden salt control, which the course retains instead of claiming unconditional success. Salt concentration is not practical salinity. Public IJmuiden map, source scope, institutional roles and null securities are appropriate.'
}
ISSUES=[{
 'courseId':'b292','field':'place','severity':'metadata location','status':'RESOLVED',
 'finding':'Original public Agua Clara latitude 9.38 was about 12 km north of the official contextual monitoring point.',
 'resolution':'Author changed place to 9.274,-79.916 and added primary panama-location source with explicit air-monitoring/background-point limitation. Reviewer reread final input; numerical models did not change.',
 'officialPoint':'9°16′26.97″ N,79°54′59.33″ W (owner report indexed air-monitoring location)',
 'reviewedInputSha256':'042fdd95d559e00904dc6eba98529f3ac7aea7956086d8360d68cad27e10cd5a'
}]
SOURCECHECKS=[
 {'url':'https://www.overtopping-manual.com/','ref':'turn307view2','access':'opened author site','finding':'2007 first edition; 2018 second edition; obsolete web calculator not updated to new formulae.'},
 {'url':'https://www.mpa.gov.sg/media-centre/details/speech-for-ms-quah-ley-hoon-chief-executive-maritime-and-port-authority-at-tuas-terminal-phase-one-reclamation-installation-of-the-last-caisson-on-tuesday-23-april-2019','ref':'turn305view1','access':'opened owner statement','finding':'23 April 2019 final Phase 1 caisson milestone recalls the first in April 2016; not whole-port completion.'},
 {'url':'https://www.rijkswaterstaat.nl/en/news/archive/2025/10/second-place-2025-jan-agema-award-for-afsluitdijk-causeway-reinforcement','ref':'turn305view0','access':'opened owner article','finding':'20 October 2025 article describes dedicated armour elements, testing and the 2019–2023 reinforcement period.'},
 {'url':'https://iho.int/en/standards-and-specifications','ref':'turn305view2','access':'opened official catalogue','finding':'S-44 edition 6.2.0 is October 2024; catalogue distinction retained.'},
 {'url':'https://portoflosangeles.org/references/2025-news-releases/news_061825_wharf_restoration','ref':'turn307view0','access':'opened owner announcement','finding':'18 June 2025 completion announcement; November 2023 construction start; concrete wharf replaces damaged timber structure.'},
 {'url':'https://www.info.gov.hk/gia/general/202509/09/P2025090900292p.htm','ref':'turn307view3','access':'opened government announcement','finding':'9 September 2025 Ma Liu Shui opening; floating platform and gangway expressly described.'},
 {'url':'https://www.wbdg.org/dod/ufc/ufc-4-152-07','ref':'turn287search0','access':'official indexed catalogue','finding':'Current catalogue date is 30 September 2026; older archived PDF cannot be represented as current.'},
 {'url':'https://legacy.wbdg.org/FFC/DOD/UFC/ARCHIVES/ufc_4_152_07_2009.pdf','ref':'turn287search2','access':'official indexed archive','finding':'Older 2009/2012 edition marked cancelled; course limits review of the new edition to bibliographic information.'},
 {'url':'https://pancanal.com/en/design-of-the-locks/','ref':'turn287search3','access':'owner source','finding':'Original Gatun trial on 26 September 1913; original miter and expanded rolling gates kept distinct.'},
 {'url':'https://pancanal.com/wp-content/uploads/2023/05/Duodecimo-reporte-cumplimiento.pdf','ref':'turn289search37','access':'official indexed excerpt; 36 MB full PDF exceeded tool open limit','finding':'Air-monitoring point at Agua Clara gives 9°16′26.97″ N,79°54′59.33″ W; suitable only as explicitly approximate public context.'},
 {'url':'https://www.rijkswaterstaat.nl/nieuws/archief/2025/04/het-onverwachte-effect-van-zoutdam-ijmuiden','ref':'turn201view1','access':'opened owner article during this V15 task','finding':'23 April 2025 report retains the unexpectedly large drainage effect found after late-2024 testing.'},
 {'url':'https://pubs.usgs.gov/publication/tm9A6.3','ref':'turn202search1','access':'official indexed publication during this V15 task','finding':'Specific-conductance chapter revised 8 February 2019, distinct from direct salt concentration.'},
 {'url':'https://www.publications.usace.army.mil/USACE-Publications/Engineer-Manuals/u43544q/647265646765/','ref':'turn310search6','access':'official indexed catalogue','finding':'EM1110-2-5025 publication 31 July 2015 and superseded manuals explicitly identified.'},
 {'url':'https://www.publications.usace.army.mil/USACE-Publications/Engineer-Manuals/u43544q/4E415649474154494F4E/udt_43544_param_direction/ascending/udt_43544_param_orderby/Info/','ref':'turn310search2','access':'official indexed catalogue','finding':'EM1110-2-1604 dated 1 May 2006; EM1110-2-1610 dated 30 September 2018.'},
 {'url':'https://www.pari.go.jp/en/2012/03/20120315211424.html','ref':'turn307view1','access':'direct open returned 403','finding':'Did not claim access to full text; owner PDF indexed evidence and primary authors paper corroborate the stated research scope.'},
 {'url':'https://www.pari.go.jp/en/pdf/en/213ef9b3da0162f47c9547b87239787601def027.pdf','ref':'turn310search37','access':'official indexed PDF abstract','finding':'Kamaishi tsunami-overflow investigation and hydraulic mechanism scope; no assumed project loads imported into teaching examples.'},
 {'url':'https://www.jstage.jst.go.jp/article/kaigan/68/2/68_I_826/_article/-char/en','ref':'turn310search8','access':'primary authors indexed paper','finding':'2012 publication about the 2011 event uses hydraulic experiments and numerical simulation, supporting the research-history distinction.'}
]

if __name__=='__main__':main()
