from peer_investigation_writer import record
D={
'b210':'''8+5-4-.6|8.4|1e-10|Closed seasonal volume budget includes explicitly defined net loss; km3 remains a volume, not discharge.
500*1e6*1.8/1e9|.90|1e-10|Area-depth conversion checked; evaporation volume differs from actual stage change with other inflows and changing area.
40/(10/(100*1e-7)+20/(100*1e-5))|.0000392157|5e-11|Equal-area steady one-dimensional series Darcy resistance; bypasses and nonlinearity excluded in mechanism.
2100/1.12|1875|1e-9|Water content is water mass divided by dry solids; wet density is not compaction evidence alone.
.32-.20|.12|1e-10|Same-datum relative settlement is a displacement difference, not a predicted crack opening.
9.81*180*55*.9/1000|87.4071|1e-8|Net head and overall efficiency explicitly assumed; MW conversion and gravity checked.
1200000/1.3|923077|.5|Dry mass divided by dry bulk deposit density includes voids; rounded cubic metres checked.
60/.75|80|1e-9|Defined delivered-to-release efficiency; losses can remain in basin rather than being consumptive.
.4+.7+.3|1.4|1e-10|Cumulative deficit assumes no intervening refill; not inferred from mean annual inflow alone.
14-9|5|1e-9|State-matched baseline residual is not a failure diagnosis without sensor and model uncertainty.''',
'b211':'''20*18*2*8|5760|1e-9|Loose transported volume per productive day; not compacted accepted volume or unconstrained linear fleet scaling.
1e-4*2000*(60/400)|.030|1e-10|Equivalent-area Darcy path is idealized; blanket defects and edge bypass are separately discussed.
(.001+.00001)/2|.000505|1e-10|Arithmetic conductivity average valid for equal-thickness layers parallel to flow, not perpendicular series flow.
(2.65-1)/1.65|1|1e-10|Uniform cohesionless upward heave gradient, not general internal-erosion threshold.
4.5/9|.50|1e-10|Mean level-rise rate only; shallow equilibration does not establish deep pore-pressure equilibrium.
2500*120|300000|1e-9|Prescribed average depositional section times advance gives prism volume; distance alone is not volume.
300-292|8|1e-9|Common elevation datum and local bed required; reservoir-wide mean elevation cannot establish intake clearance.
.35*81/19.62|1.44495|.000005|Assumed local loss coefficient times velocity head; adequate diameter does not remove transition loss.
450*6|2700|1e-9|Actual delivered power times generating duration yields MWh; nameplate is not guaranteed annual energy.
9.81*150*70/1000|103.005|1e-8|Hydraulic dissipation power scale excludes structural load distribution; comparisons require matched conditions.''',
'b212':'''0.6*100/15|4|1e-10|Ideal thin circular ring membrane compression only; arch-cantilever action and abutment boundary excluded.
9.81*80*80/2|31392|1e-8|Vertical projected unit-width hydrostatic resultant grows quadratically with water depth.
9.81*200*60/1000|117.72|1e-9|Bulk hydraulic power is not local plunge-pool pressure or its fluctuation distribution.
900/45|20|1e-10|Prescribed resultant divided by effective area gives mean pressure, not all local pulses.
(90-60)*2|60|1e-10|Net differential pressure over stated block area; rock discontinuities can govern despite intact strength.
75-68|7|1e-10|Horizontal approach of scour edge relative to a fixed reference differs from maximum scour depth.
(.20-.12)*600/800|.060|1e-10|Constant net pump balance and basin area; groundwater and cofferdam stability require separate checks.
18-4-5|9|1e-10|Opposing intrusions subtract from total clearance; one gate position does not prove full travel clearance.
250*20|5000|1e-9|Specified mean differential pressure times area, not a hydrostatic pressure inferred from an unrelated depth.
(30-24)/30*100|20|1e-10|RMS pressure reduction requires matched hydraulics and instrumentation; not arbitrary before-after subtraction.''',
'b213':'''40*.004|.16|1e-10|Prescribed uniform wetting strain gives settlement; not proof that all postimpoundment settlement is construction compaction.
500-350|150|1e-9|Scalar normal effective stress illustrates saturated-core pressure margin; not full hydraulic-fracture prediction.
.8/.25|3.2|1e-10|Dimensionless transition-size screening ratio, not universal acceptance independent of soil class and placement.
120+100+80|300|1e-9|Total discharge sums distinct bays; equal total flow does not imply equal downstream distribution.
.98*.95|.931|1e-10|Independent series gate-and-hoist availability; shared-cause failures must be modeled separately.
9.81*200*60*.9/1000|105.948|1e-9|Net-head hydraulic power times stated efficiency; nameplate capacity differs from available output.
1e9*.20/1e6|200|1e-9|Locally constant mean area converts stage change to million cubic metres, not a global stage-storage curve.
102-99-.3-1.2|1.5|1e-10|Prescribed setup and runup deducted from still-water freeboard; no wave-overtopping guarantee.
(220-100)/30|4|1e-10|Discharge ramp in m3/s per minute, not volume or downstream stage rise.
4200/(1000*8760/1000)|.479452|.0000005|GWh and MW-hour conversion; capacity factor reflects availability and hydrology, not turbine efficiency alone.''',
'b214':'''12*20*86400/1e6|20.736|1e-9|Constant synthetic collection flow over twenty days gives million cubic metres before losses and use allocation.
.5*9.81*180**2|158922|1e-8|Unit projected width hydrostatic force; published structural height is not operating water depth.
12000*2400*9.81/1000|282528|1e-8|Concrete density is mass density; gravity converts to kN weight for one-metre width.
9.81*(100+20)*80/2|47088|1e-8|Linear base-head distribution integrated across the full base; one drain reading cannot represent uplift.
60/6-8|2|1e-10|Middle-third kern applies rectangular full contact and no-tension interpretation; being somewhere inside base is insufficient.
(90000-20000)*.7|49000|1e-8|Coulomb friction uses effective normal force after uplift; excludes cohesion and other loads.
25e9*10e-6*12/1e6|3|1e-10|Uniaxial fully restrained elastic cooling with lateral freedom; creep, cracking and multiaxial restraint are separate.
(20-5)/20*100|75|1e-10|Matched pressure water-take reduction is observed flow change, not guaranteed curtain continuity or grout-volume success.
18-13|5|1e-9|Temperature-stage matched relative plumb-line residual; not absolute geodetic displacement.
9.81*25*900*.92/1000|203.067|1e-9|Synthetic system net head differs from dam height; hydraulic efficiency and MW conversion checked.'''
}
M={
'b210':'Owner indexed primary page independently corroborates rockfill description, 111 m riverbed-relative height and 15 January 1971 inauguration. Length conflicts explicitly excluded. Later dates are guide publications. Hypothetical facts and source limitations are clear; two distinct information institutions, null securities and approximate Egypt map point are appropriate.',
'b211':'Independently searched World Bank 2020 factsheet confirms 1976 completion and March 2012 fourth-extension approval, kept distinct from commissioning. WAPDA height is scoped above riverbed; 1986 audit is historical context. Lesson examples are synthetic, no invented contractor assignment, publication versus construction dates are separated.',
'b212':'River-authority history and rehabilitation pages distinguish 1956–1959 construction, 1958 impoundment monitoring and 2015 financing. Six gates corroborated by authority context; outdated forecasts explicitly excluded from completion claims. Arch, scour and gate examples remain hypothetical; roles describe information providers and no securities are invented.',
'b213':'Independently searched VRA primary plant page corroborates 1961–1965 original construction, 1020 MW and twelve gates across two spillways. Conflicting heights/lengths excluded rather than resolved by guessing. Hypothetical numerical parameters are clear; publication date 2011 is identified as filter-guide context. Institution roles and map context are appropriate.',
'b214':'Owner engineering and scheme-history pages distinguish Grande Dixence 285 m, 1951–1961 construction and commissioning from 1961 from Cleuson 1947–1951 and earlier Dixence. Structural height is explicitly separate from scheme net head. Guide provenance and source-access limits are stated, and organizations are educational references without invented contracts.'}
if __name__=='__main__':record(D,M)
