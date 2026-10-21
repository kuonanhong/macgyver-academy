# V14 support, water and construction-method courses

Reviewed 2026-10-21. Authored inputs: **b151–b175, 25 courses, 250 bilingual units**. Each unit retains mechanism, dimensional model, measurable verification, failure diagnosis, misconception and practice fields. The integrator expands these to 1000 new steps; this author did not edit public/generated data or deployment files.

All 25 inputs pass the unchanged V13-depth validator. The author source consists of `build_support.py` and five `support_rows_*.py` files. It rebuilds only assigned inputs and `research_support.json`. Exact catalog titles and underground disciplines/families are retained.

## Numerical and physical review

`audit_support.py` contains 250 separately expressed primary-output calculations, one per unit. All agree with displayed rounding. This is explicitly an **author self-check**, not a third-party certificate; secondary formula results were also reread manually. `audit_support.json` records every check and SHA256 for the 25 reviewed inputs. Independent peer reviews are separate files maintained by their reviewers.

Specific boundaries maintained:

- Bolt, rib and membrane examples separate nominal area from effective contact. Early strength, thickness averages and test coverage are not blanket acceptance criteria.
- Rockburst serial-component minimum is a static force comparison, not minimum energy. Remaining energy absorption uses a calibrated force and remaining travel, not subtraction of event energy from a product rating.
- Grout pressure includes elevation and line loss; pressure above groundwater is not an allowed injection pressure. Water-head direction and effective-stress effects are explicit.
- Immersed-tube tonnes denote mass. Displacement, free-surface correction, trim/attitude, foundation contact and longitudinal support transitions use different models. No rectangular immersed element is modeled as a circular ring.
- Seal pressure times span is transverse force per length, not membrane tension. Geometric compression does not establish reaction or tightness. Primary/secondary barriers can share common failures.
- Pipe-jacking forces include reaction paths, contact eccentricity and sectional load transfer. Slurry density does not automatically count all recirculated solids as fresh excavation.
- HDD heading, toolface and measured path differ. Utility clearance deducts uncertainty before pipe radii; endpoint closure does not bound all intermediate errors.
- Caisson imbalance does not predict sinking velocity. Upward seepage reduces effective stress; weight/uplift ratios are not code safety factors. Stage changes require separately established support and sealing boundaries.

All numerical examples are original assumptions, not project measurements or approved operating settings. Explicit units were added to density, annulus, pressure, ring volume, hydraulic and uncertainty formulas that previously abbreviated inputs.

## Sources and project boundaries

18 primary-source entries were actually retrieved or verified through official indexed content in this rebuild; each course includes 3–5 relevant entries. `research_support.json` records URLs and access limitations. FHWA, CEDD, EFNARC, material manufacturers, PJA, Network Rail, Crossrail and Tideway support principles and public context, not the invented numeric inputs.

Direct retrieval limitations are disclosed for the D-bolt DOI and MassDOT page; no full-text review is claimed. The Paddington project-team indexed text supports permanent slabs bracing diaphragm walls. Fehmarn owner context and Gina/Omega manufacturer roles are separated from hypothetical seal dimensions or ratings. No product suitability, partnership, contract or security listing is invented.

Werrington is a documented curved-box-jacking comparison. Heathwall is expressly a **2013 proposed caisson/underpinning method, not as-built evidence**. Cremorne is expressly **piles plus sprayed lining, a non-caisson comparison**. Generic utility corridors and receiving shafts are labelled hypothetical. Map points are public educational references, not surveyed construction coordinates.

# Independent peer review of landmark courses

The same reviewer separately checked **hsuehshan and b102–b125: all 250 models**, reading their kind/context allocation, dimensions and physical boundary statements. `audit_landmarks_support_peer.py` uses label-keyed physical equations without importing the author generator or author audit. It recalculates all **250 base results and 250 single-parameter +10% sensitivity results**, and checks all 250 bilingual model displays. All pass at numerical tolerance 1e-11; the report includes final input SHA256 hashes.

Two observations were resolved by the landmark author and the rebuilt files were reread:

1. The uniaxial circular-hole formula now states **maximum tangential compression**, vertical remote loading, zero horizontal remote stress and the sidewall location. It is not an all-position stress value.
2. Jurong's explicitly hypothetical cover was changed from 1220 m to a context-appropriate 120 m, giving 9.36 MPa and a +10% sensitivity result of 10.296 MPa. This remains a teaching assumption.

Seven project boundaries were independently re-browsed against official owner/contractor sources: Marmaray 1387 m immersed section; Aqua-Line 15.1 km whole road; Brenner 55 km base tunnel versus 64 km connected route; New Wujie 6.5 km TBM drive within 16.5 km conveyance scope; HZMB rounded 7 km tunnel section; Outer Underground Discharge Channel 6300 m waterway; Jurong 1.47 million m3 storage. None was silently converted into a different project boundary.

The peer review does not certify construction design or revalidate every historical source. Remaining history and metadata are covered by the separate metadata review. The three immersed-box courses contain no thin-ring formula; water-route/storage courses do not use vehicle travel-time models; Jurong hydraulic containment uses one datum and positive external-minus-internal pressure for a local inward gradient.

## Support peer-review clarifications (final rebuild)

Ground-course reviewer independently read all 250 models and requested the following scope/definition corrections. The author updated both reproducible rows and generated inputs; numerical results remain unchanged. The unchanged validator passes 25/25, and `audit_support.py` again passes 250/250 and records the new input hashes.

- b151 unit 2: explicit MPa for demand and early strength.
- b155 unit 9: one-gauge displacement difference is apparent chord rotation; joint rotation requires both side slopes with common rigid-body rotation removed.
- b158 unit 3: fourth-power span scaling holds uniform line load q, EI and simple-support conditions fixed, rather than fixed total force.
- b161 unit 6: 80 mm is compatible circumferential shortening, not diametral convergence.
- b163 unit 2: the 10 m pressure correction explicitly assumes conveyed-fluid density 1000 kg/m3; other grout density requires recalculation.
- b164 unit 7: Manning diameter scaling assumes similar circular effective passages flowing full with unchanged n and energy slope, not arbitrary bottom deposits.
- b166 unit 8 and b171 unit 9: the displayed difference/span is mean settlement slope before removal of rigid-body tilt, not automatically distortion or track twist.
- b166 unit 10: RSS combines independent standard uncertainties; it is not a measured survey-closure residual.
- b169 unit 4 and b170 unit 6: the joint interpretation expressly assumes a rigid element beside a horizontal neighbor; otherwise use the difference of adjacent slopes.
- b174 unit 6: the 34.9 mm value projects the final heading error over the whole length and is not a time-integrated path-error prediction.
