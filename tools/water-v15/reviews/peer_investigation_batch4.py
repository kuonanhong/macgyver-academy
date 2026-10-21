from peer_investigation_writer import record
D={
'b251':'''9.81*6*25/2|735.75|1e-9|One-sided hydrostatic resultant; downstream water pressure must be subtracted for a net force.
6*2/3|4|1e-10|Triangular pressure resultant is two-thirds depth below free surface, not geometric middepth.
6020-6008|12|1e-9|Total transverse clearance only; distributed guide alignment and moving-assembly dimensions remain necessary.
600*.015|9|1e-10|Equivalent rolling-resistance coefficient under prescribed wheel normal force; movement alone does not prove all wheels roll.
300-40+25+60|345|1e-9|Specified upward lifting demand subtracts buoyancy and adds downward seal/downpull loads, excluding acceleration.
400*(.5+.5/8)|225|1e-9|Rigid two-pick static load split with defined eccentricity; higher reaction differs from half total load.
200000*20/(.001*80e9)|.050|1e-10|Equivalent elastic rope modulus model; unequal extension or seating invalidates equality inferred from drum rotation.
.6*.0005*math.sqrt(8*9.81)|.00265767|.000000005|Assumed defect orifice area and coefficient, not a guarantee of continuous seal contact.
.08*.5+.08**2/(2*.16)|.060|1e-10|Constant braking deceleration after signal delay; not instantaneous stop at limit-switch actuation.
.65*4*.5*math.sqrt(6*9.81)|9.97364|.000005|Assumed free underflow with specified head and coefficient; submerged flow and alternate heads need different treatment.''',
'b252':'''35*9.81|343.35|1e-9|Hydrostatic pressure from a defined head difference; nearby depth is not necessarily local differential pressure.
6/80|.075|1e-10|Straight active stretch length assumed; profile folds and bulbs change effective deformation length.
20*10e-6*15|.003|1e-10|Free thermal contraction, not actual restrained field joint opening.
1800/120|15|1e-10|N/mm2 equals MPa for nominal coupon tensile stress; appearance alone does not establish full fusion.
150-25|125|1e-9|Placement error reduces embedment geometrically; fresh concrete can subsequently displace the waterstop.
.8*.04*.03|.00096|1e-10|Illustrative rectangular void volume; an intact strip cannot prevent a surrounding concrete bypass.
.1*(.0002**3)*1000/(12*.001*1)|.0000000666667|5e-14|Smooth parallel-plate laminar cubic flow with dynamic viscosity; rough joints and opening deformation are excluded.
(160-100)/100*100|60|1e-10|Free volumetric swelling percentage cannot determine constrained contact pressure without constitutive response.
18/120|.15|1e-10|Localized timed leakage in L/s; diversion to another path may leave a repaired point dry.
.002*15|.030|1e-10|Calibrated isothermal small-change compliance gives volume change; temperature, trapped gas and system deformation must be separated from leakage.''',
'b253':'''40/100|.40|1e-10|Water-discharge diversion fraction need not equal diversion of each sediment size class.
40*3|120|1e-9|Representative cross-section suspended concentration times bypass flow gives kg/s; excludes unmeasured bed load.
21000/30000*100|70|1e-10|Same-event cumulative bypass mass over incoming mass defines event efficiency, distinct from peak instantaneous ratio.
40/(4*1.25)|8|1e-10|Actual rectangular wetted area rather than excavation area determines section mean velocity.
.01*1200/8|1.50|1e-10|Prescribed travel-time settling distance is still-water screening, not turbulent tunnel deposit thickness.
20/(1650*9.81*.010)|.123560|.0000005|Shields stress normalized by submerged grain-weight scale; threshold depends on slope, gradation and exposure.
12/300|.040|1e-10|Historical average abrasion per operating hour; changing sediment and hydraulics preclude guaranteed future linear loss.
(40*3+60*.2)/(40+60)|1.32|1e-10|Fully mixed conservative concentration is discharge weighted; excludes near-field gradients and deposition.
(120*1800+50*1800)/1000|306|1e-9|Time-integrated mass flux converted from kg to tonnes; discharge and concentration peaks need not coincide.
1000-650-100-230|20|1e-9|Closed dry-mass budget residual includes measurement/coverage error, not uniquely unmeasured erosion.''',
'b254':'''1000*.99+2650*.01|1016.5|1e-9|Volume-weighted dilute mixture density with specified water density; ambient temperature/salinity can change density contrast.
9.81*16.5/1000|.161865|1e-10|Reduced gravity uses ambient reference density explicitly; mixing and settling alter it downstream.
.5/math.sqrt(.16*2)|.883883|.0000005|Densimetric Froude based on current-layer thickness and prescribed reduced gravity, not full reservoir depth.
6000/.4/3600|4.16667|.000005|Mean front-speed travel scale, not exact arrival or gate timing under changing current conditions.
3/.002/60|25|1e-10|Still-water settling through a prescribed three-metre layer; turbulence and particle-size distribution are separate.
100/30|3.33333|.000005|Clear-water entrainment dilution conserves suspended mass when no deposition or resuspension is assumed.
15*4|60|1e-9|Measured outlet concentration and discharge yield exported mass rate; outlet size alone does not fix concentration.
540/900*100|60|1e-10|Same-event denominator is arriving-current mass, not all reservoir inflow sediment; comparison requires consistent definitions.
(10*2+30*8)/40|6.5|1e-10|No-reaction fully mixed dissolved-oxygen balance; local plumes and biochemical consumption are excluded.
1200-650-100|450|1e-9|Net storage mass from incoming minus two exports; sediment location cannot be inferred from scalar closure.''',
'b255':'''12000*1.8|21600|1e-8|Survey area times mean required cut gives in-situ volume; denser grids do not remove common datum bias.
1000*1300/1000|1300|1e-9|Dry bulk density converts in-situ deposit volume to dry solids tonnes, not pumped slurry volume.
.85*1000+.15*2650|1247.5|1e-9|Volume-fraction mixture density; solids mass fraction is a different quantity.
.25*.15*3600|135|1e-9|Slurry flow times solids volume fraction gives dry-particle volume per hour, excluding water and in-situ deposit voids.
.25/(math.pi*.3**2/4)|3.53678|.000005|Mean pipe velocity from circular full-flow area; transport/deposition threshold needs particle and slurry information.
1250*9.81*.25*30/.7/1000|131.384|.0005|Specified slurry density and pump efficiency convert hydraulic power to shaft kW; clear-water curves need slurry correction.
.20/500|.00040|1e-10|Surface hydraulic loading in m/s for ideal sedimentation screening; short circuits and fines prevent guaranteed complete removal.
100/.60|166.667|.0005|Cake solids fraction by mass converts dry tonnes to wet tonnes; retained water remains in the total.
.20*.10*3600|72|1e-9|100 mg/L equals 0.10 kg/m3; integrating return concentration and flow gives dry kg load.
22000-2500|19500|1e-8|In-situ excavation minus measured redeposition gives stated geometric storage gain; hauled bulk volume is not identical.'''
}
M={
'b251':'USACE official program portal lists the vertical-lift gate manual and hydraulic-steel guidance; course separates dry erection, wet loading and acceptance evidence. Literature dates are not installation dates. Hoover/Glen Canyon are system comparisons, synthetic gate dimensions are not attributed, and institutional roles have no unsupported contractor or security details.',
'b252':'USBR joint-waterstop research pages 3191 and 7688 independently read during this session distinguish deterioration and laboratory repair investigation from field guarantees. Sika manufacturer page supplies material/profile context without claiming project supply. Waterstop sizes and stresses remain hypothetical; dates and comparison landmarks are clearly scoped.',
'b253':'ETH original completed-research catalog supports Solis bypass modeling and Palagnedra abrasion context; PWRI/MLIT are official sediment and Miwa bypass sources. Course distinguishes bypass from flushing and assumes all lesson transport quantities. Named comparisons, publication chronology, Denver reference and information-only roles do not invent operating performance.',
'b254':'EPFL repository sources are explicitly limited to visible abstracts/bibliography where retrieval was restricted. Rudbar-Lorestan is a venting-model comparison and Miwa a distinct bypass-path comparison. No current construction or performance assertion is inferred. Two-layer synthetic calculations and information-provider institutions are clearly separated from project facts.',
'b255':'USACE Millsite source is a permit-application notice, and text correctly labels the project proposed rather than approved/completed. USBR RSEM Muddy Creek is an economic-model scenario, not measured dredging performance. Primary sediment-strategy note and source limitations are appropriate; synthetic dredging accounting, literature dates and two agency roles are clear.'}
if __name__=='__main__':record(D,M)
