from peer_investigation_writer import record
D={
'b246':'''(16/9.81)**(1/3)|1.17711|.000005|Critical rectangular depth from unit discharge; not actual depth over every step in nonuniform aerated flow.
1.2/.6|2|1e-10|Relative critical depth to step rise is only one regime parameter; slope and geometry also matter.
math.degrees(math.atan(.5))|26.5651|.00005|Rise/run defines mean geometric angle; individual offsets and tolerances require inspection.
400*3*5/1000|6|1e-10|Prescribed interfacial shear times area and relative speed gives kW transfer scale, not independent linear dissipation per step.
18/60|.30|1e-10|Measured inception distance fraction; visible surface aeration differs from near-bed air concentration.
.80/.75|1.06667|.000005|Uniform mixture bulk depth assumes prescribed mean void fraction and equivalent liquid volume; not stratified profile reconstruction.
(80000-2300)/(500*18**2)|.479630|.0000005|Both pressures absolute and in Pa; index is not a universal cavitation damage threshold.
1.1+64/19.62|4.36198|.000005|Specific energy assumes kinetic-energy coefficient one and defined section datum; terminal losses still need checking.
1.5*12*9.81|176.58|1e-9|Net underside head times slab area gives kN uplift independent of surface energy dissipation efficacy.
20**1.5|89.4427|.00005|Froude scaling gives velocity square-root length; same viscosity gives Reynolds ratio L to power 1.5.''',
'b247':'''2*40|80|1e-9|Uniform lateral inflow per unit length integrated along side channel; flow varies spatially.
1.7*30*1.2**1.5|67.0412|.00005|Assumed dimensional weir coefficient at fixed head; downstream conveyance may control total capacity.
80*4|320|1e-9|Outgoing axial momentum flux is kN after water-density conversion; lateral input has zero prescribed axial component.
90/(8*3)|3.75|1e-10|Section continuity yields mean speed only; momentum and boundary conditions determine profile.
(100/9.81)**(1/3)|2.16825|.000005|Rectangular outlet critical depth for q=10 m2/s; upstream spatial profile responds to control.
16*6/(9.81*30)|.326198|.0000005|Approximate transverse centrifugal level difference for stated curvature and velocity; not universal horizontal cross-section surface.
5-3.6-.8|.60|1e-10|Prescribed wave crest subtracted from mean-depth clearance, not a full probabilistic overtopping criterion.
(108-105)*9.81|29.43|1e-9|Common-datum total heads give net pressure in kPa; drains do not guarantee zero underslab pressure.
(40-10)/40|.75|1e-10|Fixed-head, fixed-coefficient crest reduction only; real blockage pattern can alter coefficient and local flow.
(100-98)/100*100|2|1e-10|Steady mass-balance residual is a necessary consistency check, not validation of local three-dimensional flow.''',
'b248':'''1.7*math.pi*10|53.4071|.00005|Free circular crest rating with prescribed coefficient/head; transitions to throat or conduit control require different relations.
.75*12*math.sqrt(2*9.81*8)|112.755|.0005|Orifice control scales with square-root effective head and discharge coefficient, not the free-weir exponent.
math.pi*(25-9)/4|12.5664|.00005|Annulus uses diameters squared divided by four; an air core removes liquid area.
15/12|1.25|1e-10|Air volume at local pressure/temperature divided by velocity gives section, excluding compressible line losses.
20/(4*math.pi)|1.59155|.000005|Ideal free-vortex circulation relation applies away from the singular core; low mean approach velocity cannot exclude rotation.
math.sqrt(2)*60*10|848.528|.0005|Orthogonal equal-speed momentum-vector change; pressure, weight and unsteady bend loads remain additional.
.018*75*64/19.62|4.40367|.000005|Full-pipe Darcy friction with stated diameter/length; not Fanning factor or partly full flow.
40*600/2000000|.012|1e-10|Constant-area short-step storage balance; complete routing requires stage-dependent outflow and time history.
14/20|.70|1e-10|Geometric open-area fraction, not directly the discharge fraction under changed head and contraction.
2*8|16|1e-10|Nyquist theoretical boundary is not a practical acquisition recommendation; text explicitly requires margin and peak fidelity checks.''',
'b249':'''90-35|55|1e-10|Atmospheric plus gauge gives absolute pressure; negative gauge is not automatically vaporization.
(100000-2300)/(500*20**2)|.4885|1e-10|Absolute pressure margin normalized by dynamic pressure, not a direct damage-rate law.
.004/.80|.005|1e-10|Relative offset scale is dimensionless; orientation and flow separation remain independent factors.
70-3*15|25|1e-10|Statistical mean-minus-three-SD illustrative level, explicitly not a hard physical minimum or guarantee against transients.
6/(6+54)|.10|1e-10|Common-condition volumetric air fraction; total supply cannot establish local wall protection.
3*.5*1.2*20**2|720|1e-9|Low-Mach air pressure loss in Pa from prescribed K, not compressible high-speed ventilation sizing.
15*math.sqrt(.4/9.81)|3.02891|.000005|Horizontal ballistic trajectory over a 0.20-m drop; water-level and air-supply conditions can drown the cavity.
12*.025|.30|1e-10|Damage volume is surveyed area times mean depth at one epoch; no annual linear loss rate follows.
9000/.003/1e6|3|1e-10|Pull-off force converted from kN to N and Pa to MPa; localized test does not prove full-area bond.
2.5+1+3.5|7|1e-10|Exposure durations add, but no equal damage-per-hour or linear cumulative erosion law is asserted.''',
'b250':'''9.81*8*36/2|1412.64|1e-8|Horizontal resultant uses vertical rectangular projection from free surface, not curved-skin area.
45*9.81|441.45|1e-9|Magnitude from a specified imaginary fluid volume; vertical direction requires the explicit free-body convention.
3/10000|.000300|1e-10|Small-angle elevation mismatch over span is one alignment component, not full three-dimensional coaxiality.
1800*.08*.20|28.8|1e-10|Prescribed bearing friction coefficient and effective radius determine moment; coefficient can change with condition.
400/(2*math.sin(math.pi/3))|230.940|.0005|Symmetric slings with angles measured above horizontal; half-weight tension only for vertical legs.
50*1.2**2/8|9|1e-10|Unit-width simply supported strip idealization; local span controls bending, not total skin area.
math.pi**2*200e9*.00008/36/1000|4386.49|.005|Ideal pinned Euler load with SI modulus and inertia; imperfections, yielding and connection stiffness preclude direct field capacity.
800/8|100|1e-9|Centered force and equal anchor stiffness give average tension only; eccentricity and prying change maxima.
(30-24)/30*100|20|1e-10|Geometric seal compression fraction; more compression increases friction and may damage the seal.
6/12000|.0005|1e-10|Small-angle travel skew indicator with common geometry; equal displacement does not establish equal forces.'''
}
M={
'b246':'Stepped-spillway guide HL-2015-06 is primary USBR research and the Upper Stillwater research catalog supports the named model comparison. Generic historical years are explicitly publication dates. Glen Canyon is a smooth-chute comparison. Examples do not transplant guide design parameters; USBR/USACE roles and null securities are appropriate.',
'b247':'Fontenelle HYD-486 is an original 1962 hydraulic model study of double side channels, chute and basin, independently searchable at USBR. Course uses model-validation comparison without assigning synthetic geometry to Fontenelle. General publication chronology, Denver reference, technical guides and information-provider roles remain clear.',
'b248':'USBR Monticello owner page independently confirms the morning-glory form and 1957 completion; course formulas explicitly separate free-weir, orifice and full-pipe regimes. Glen Canyon is a tunnel-spillway comparison rather than a shaft-geometry source. Historical years are literature milestones; no invented vendors or securities.',
'b249':'Official EM42/SpillwayPro source distinguishes 1990 cavitation monograph from 2021 smooth/stepped software development. Catalog aeration studies provide technical context, not current operating performance claims. Hoover/Glen Canyon are named interface comparisons. Original examples and pressure reference conventions are kept separate from public project facts.',
'b250':'USBR original radial-gate risk chapter and USACE hydraulic steel manual match geometry, load-path and failure-context scope. Simplified lifting and component calculations are expressly not installation acceptance plans. Publication chronology and broad dam comparisons make no unsupported gate supply or construction claim; two distinct institutions and null securities are appropriate.'}
if __name__=='__main__':record(D,M)
