from peer_investigation_writer import record
D={
'b241':'''142+196.2/9.81|162|1e-9|Gauge pressure head plus elevation gives total piezometric head; compared values need one datum and negligible velocity head.
2e-5*500*12/50|.0024|1e-10|Saturated steady Darcy scale; discharge alone cannot distinguish hydraulic forcing from erosion.
1.4*.1**2.5|.00442719|.000000005|Specified calibrated free-flow V-notch rating; tailwater submergence invalidates it.
18-5-2|11|1e-9|Steady sump has no storage change; independently identified rainfall and maintenance flows are deducted.
4*(1-math.exp(-2))|3.45866|.000005|First-order instrument response after step, not a proof that ground pressure itself changes slowly.
8*1.3/1.0|10.4|1e-10|Same geometry/head with viscosity-dependent laminar conductivity; seasonal viscosity change does not imply larger pores.
.012*(80/1000)*3600|3.456|1e-10|80 mg/L equals 0.080 kg/m3; concentration requires sampling calibration, not raw turbidity substitution.
.009/30|.000300|1e-10|Bulk conductance unit m2/s differs from material hydraulic conductivity m/s.
30/2+5|20|1e-10|Persistent event and uniformly distributed phase give half-interval mean delay, not worst-case latency.
math.hypot(.3,.4)|.50|1e-10|Independent standard uncertainties combine by RSS; alert evidence is not an engineering acceptance limit.''',
'b242':'''0.60/0.20|3|1e-10|Dimensionless illustrative retention ratio; soil classification and test procedures remain necessary.
.60/.030|20|1e-10|Permeability screening ratio is distinct from retention and cannot alone approve a coarse filter.
(18-12)/12|.50|1e-10|H is percentage-point increase between d and 4d; ratio illustrates internal-gradation screening rather than universal approval.
.80-.12-.08|.60|1e-10|Encroachments from both sides reduce placed thickness; design drawing does not establish local continuity.
(60*8+40*2)/100|5.6|1e-10|Dry mass-weighted fines average; local segregation remains invisible in aggregate average.
(120-9)/120*100|92.5|1e-10|Dry-solids yield conserves material; wash-water quantity is not direct cleanliness evidence.
.003*30/(.01*6)|1.50|1e-10|Steady Darcy head requirement in stated drain section; outlet resistance remains a separate boundary.
math.pi*(1.8**2-.6**2)|9.04779|.000005|Annular area uses radii rather than diameters; volume and under-conduit placement need additional dimensions/evidence.
.004*.5*.3|.00060|1e-10|Prescribed opening and measured mean velocity give discharge; no crack-law or erosion-rate prediction is inferred.
.045/.75|.060|1e-10|Average simple shear strain is geometric screening, not a claim of continuity at arbitrary deformation.''',
'b243':'''(150-60)*math.tan(math.pi/6)|51.9615|.00005|Frictional component from prescribed normal effective stress; pore pressure may lag reservoir fall.
math.tan(math.radians(32))/math.tan(math.radians(24))|1.40348|.000005|Dry cohesionless infinite-slope illustration; no complex-slope design approval implied.
20**2/.002/86400|2.31481|.000005|Diffusive characteristic time L squared over diffusivity, not a failure countdown or exact transient solution.
10*.5*math.sin(math.radians(.2))|.0174533|.00000005|Identical segment rotation increments integrated along assumed fixed reference; deep toe stability is not automatic.
18-11|7|1e-9|Common axis and epoch relative displacement can hide rigid translation of both points.
12/math.cos(math.pi/6)|13.8564|.00005|Known direction relative to LOS permits projection inversion; without direction only LOS motion is measured.
(5-2)/3|1|1e-10|Change of daily velocity divided by three days gives mm/day2; extrapolation does not determine failure time.
6-2|4|1e-10|Difference of exterior and internal head drops quantifies lag; not equivalent to uniform drainage rate.
18000*12|216000|1e-8|Prismatic volume with assumed mean thickness; impulse waves need velocity, geometry and entry conditions.
math.hypot(2,2)|2.82843|.000005|Independent epoch standard uncertainties propagated for difference; correlations and reference movement are separate.''',
'b244':'''240/(20*1)|12|1e-10|Rectangular section mean velocity differs from local extremes.
12/math.sqrt(9.81)|3.83131|.000005|Froude number describes gravity-inertia balance, not similarity of every local pressure or turbulence feature.
(math.sqrt(1+8*144/9.81)-1)/2|4.94130|.000005|Horizontal rectangular classical jump uses momentum and hydrostatic end sections, not energy conservation across the jump.
(5-1)**3/(4*1*5)|3.20|1e-10|Given conjugate-depth loss formula dissipates mechanical head; no electrical recovery is implied.
5.4-5.0|.40|1e-10|Tailwater margin at one discharge does not establish jump location for every partial-flow condition.
9.81*2*30|588.6|1e-9|Net head across slab converted to kN; transient pressure and drainage lag remain separate.
8*7|56|1e-10|Captured water momentum removal gives mean kN force; does not allocate force equally to baffles.
math.sqrt((36+36)/3)|4.89898|.000005|RMS of stated zero-mean pressure samples, not the peak or full design load combination.
18-11-2|5|1e-10|Sediment mass retained after outlet and cleaning terms; through-going solids can still abrade surfaces.
500/(25**2.5)|.160|1e-10|Froude geometric scaling gives Q ratio L to power 2.5; Reynolds, aeration and cavitation similarity are not guaranteed.''',
'b245':'''400*math.sin(math.pi/3)/9.81|35.3119|.00005|Ballistic free-jet centerline with equal launch/landing elevations and neglected air drag; footprint is broader.
(10+math.sqrt(100+2*9.81*8))/9.81|2.65341|.000005|Positive root for downward landing drop eight metres; equal-elevation range equation is inapplicable.
1000*22**2*.8/18/1000|21.5111|.00005|Curvature pressure scale for prescribed speed, depth and radius; Pa-to-kPa conversion now explicit; not total hydrostatic-plus-dynamic pressure.
24**2/(2*9.81)|29.3578|.00005|Velocity head remains mechanical energy after bucket exit, pending jet breakup and impact.
9.81*80*40/1000|31.392|1e-9|Total hydraulic power is a scale; pool depth requires jet and rock response, not power alone.
40/(.8*20)|2.50|1e-10|Homogeneous mixture with equal phase velocity; air fraction expands visible jet area without extra liquid discharge.
30*18|540|1e-9|Water momentum change in vertical component yields mean kN; direction matters independently of speed magnitude.
600/24|25|1e-10|Mean impact force over assumed area, not local pressure peaks capable of rock-block uplift.
(2650-1000)*9.81*2/1000|32.373|1e-9|Submerged weight subtracts displaced water mass; joint uplift and anchorage are separate from intact rock strength.
1000*4*.020/.072|1111.11|.005|Weber ratio uses model jet thickness as length scale; gravity-scaled trajectories do not assure surface-tension breakup similarity.'''
}
M={
'b241':'History explicitly uses 1978/1980/1987 publication milestones rather than a fabricated monitoring installation chronology. USBR catalog and FEMA P-1032 topic independently verified; monitoring chapter and institutional Fontenelle/Teton history are scoped. Denver is a reference point, cases are comparisons, distinct USBR/FEMA roles have no construction or security claim.',
'b242':'Filter calculations are expressly screens, not universal criteria. Official 2011 protective-filter chapter and FEMA seepage guide match retention, permeability and erosion scope. Historical dates are publications; Fontenelle/Teton are comparison cases without invented use of every technique. Institution roles, map and synthetic facts are appropriately separated.',
'b243':'USGS primary Guobu study independently corroborates reservoir/rainfall response context, and USBR 2011 static stability chapter is verified. Guobu/Laxiwa and Barry Arm are monitoring comparisons, not source parameters. Publication dates do not pretend to be project milestones. USBR and USGS are correctly information sources with null securities.',
'b244':'USBR official catalog confirms revised 1978 dissipator and 1980 laboratory references; 1987 small-dam publication is distinct from any structure commissioning. USACE spillway manual is scoped to official index because full retrieval was restricted. Hoover/Glen Canyon are explicitly system comparisons; no synthetic stilling-basin dimensions are attributed to them.',
'b245':'Ballistic and momentum lessons retain assumptions and distinguish hydraulic power from scour design. Shared primary manuals are relevant general references, while Hoover/Glen Canyon are explicitly interface comparisons rather than claims that these specific synthetic buckets exist there. Dates are publication milestones; vendor roles and null securities avoid invented commercial relationships.'}
if __name__=='__main__':record(D,M)
