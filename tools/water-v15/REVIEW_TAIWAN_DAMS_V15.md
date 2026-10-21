# V15 six dam cases: numeric and content review

Author: `/root/courses_landmarks/taiwan_dams`. Date: 2026-10-21. This is an author audit using separately entered Python literal expressions, not independent external peer review.

## Coverage

- Six courses b215–b220, exactly ten distinct units each; 60 models recomputed.
- Every model explicitly labels assumptions, inputs with units and applicable limitations. All project dimensions and historical dates remain separate from teaching scenarios.
- All 60 misconception fields manually read as plausible FALSE propositions for quiz distractors. Correct cautions were inverted in the first 20 authored entries; later entries were authored as false propositions.
- Mechanisms contain distinct physics discussion; no mechanism is built by copying its entire failure paragraph.

## Corrections found by recomputation

- b216 unit 8 conjugate hydraulic-jump depth corrected from 3.146774 to 3.146630 m.
- b217 unit 7 orifice discharge corrected from 10.09064 to 10.090393 m3/s.
- b219 unit 4 gated underflow corrected from 27.639874 to 27.639749 m3/s.
- b219 unit 8 Manning discharge corrected from 4.174848 to 4.173697 m3/s.
- b218 metadata efficiency sensitivity corrected to 40.6134 MW.
- b215 unit 2 uses a 10 m thickness and 120 m radius (ratio 0.0833), giving 9.6 MPa ideal membrane compression; a 20% thickness increase gives 8 MPa. Explicitly a reduced ideal strip, not a complete arch stress solution.

## Source boundaries

- Owner/authority sources support Kurobe 186 m/1963; Feitsui 122.5 m/1987; Shihmen 133.1 m/1964; Deji 180 m and distinct 1973 impoundment/1974 completion; Tsengwen current 134 m/400 m/1973; Nanhua 87.5 m and distinct 1993 impoundment/1994 completion and supply.
- Tsengwen uses current owner 134 m; an older 133 m value was deliberately not mixed in.
- Reclamation guides were checked at official index scope, including 2014 seepage and 2022 appurtenant chapter dates; linked full documents are not claimed as fully reviewed.
- USACE 1994 arch title/date were confirmed by official indexed catalogue/cover excerpts; direct catalogue and PDF retrieval returned 403, recorded explicitly.
- Institutions are data or method-reference providers; no invented construction contract, participation, financial listing or security identifier.
- No current reservoir capacity, operating schedule, design criterion, flow permission or site safety conclusion is inferred from historical webpages.

## All arithmetic checks

| Course | Unit | Literal recomputation | Result | Unit |
|---|---:|---|---:|---|
| b215 | 1 | `(20-12)*21600` | 172800 | m3 |
| b215 | 2 | `0.8*120/10` | 9.6 | MPa |
| b215 | 3 | `90/18000` | 0.005 | m |
| b215 | 4 | `30000*0.00001*12` | 3.6 | MPa |
| b215 | 5 | `0.018*(1600/3)*4**2/(2*9.81)` | 7.828746177 | m |
| b215 | 6 | `1000*9.81*18*420*0.9/1e6` | 66.74724 | MW |
| b215 | 7 | `1000*900*1.5/1e6` | 1.35 | MPa |
| b215 | 8 | `1000*9.81*0.25*35/0.7/1000` | 122.625 | kW |
| b215 | 9 | `1.6-(0.12*15+0.25*(-4))` | 0.8 | mm |
| b215 | 10 | `(24-16)*1800` | 14400 | m3 |
| b216 | 1 | `20000000/4/86400` | 57.87037037 | day |
| b216 | 2 | `1000*9.81*10*40**2/2/1e6` | 78.48 | MN |
| b216 | 3 | `50*3000/(3000+2000)` | 30 | MN |
| b216 | 4 | `(80-0.3*100)*math.tan(math.radians(30))` | 28.86751346 | MN |
| b216 | 5 | `0.00001*24*15*1000` | 3.6 | mm |
| b216 | 6 | `0.2/math.sqrt(9.81*2*8/1000)` | 0.5048187773 | dimensionless |
| b216 | 7 | `140*10800/8000000` | 0.189 | m |
| b216 | 8 | `(math.sqrt(1+8*8**2/9.81)-1)/2` | 3.146629992 | m |
| b216 | 9 | `12*0.35*7200` | 30240 | kg |
| b216 | 10 | `(3*20+2*50)/(3+2)` | 32 | mg/L |
| b217 | 1 | `1000*30/(10/1e-7+10/5e-8)` | 0.0001 | m3/s |
| b217 | 2 | `0.7/0.25` | 2.8 | dimensionless |
| b217 | 3 | `2100/(1+0.12)` | 1875 | kg/m3 |
| b217 | 4 | `900-45*12` | 360 | kN |
| b217 | 5 | `0.15*24000` | 3600 | kN |
| b217 | 6 | `(1800000-600000)/1200` | 1000 | m3 |
| b217 | 7 | `0.62*1.5*math.sqrt(2*9.81*6)` | 10.09039286 | m3/s |
| b217 | 8 | `9*8*2400/1000` | 172.8 | tonne |
| b217 | 9 | `(18-11)*2700` | 18900 | m3 |
| b217 | 10 | `0.004/20` | 0.0002 | m2/s |
| b218 | 1 | `1000*9.81*15*(200*0.9+120*0.88)/1e6` | 42.02604 | MW |
| b218 | 2 | `1000*9.81*140/1e6` | 1.3734 | MPa |
| b218 | 3 | `(5-1)/1000/200` | 2e-05 | dimensionless |
| b218 | 4 | `math.sqrt(9.81*4*3/1000)` | 0.3431034829 | m/s |
| b218 | 5 | `900000+250000-1000000-30000` | 120000 | m3/day |
| b218 | 6 | `(80000-2500)/(0.5*1000*18**2)` | 0.4783950617 | dimensionless |
| b218 | 7 | `2*1.2/0.02` | 120 | MPa |
| b218 | 8 | `2*1200/800` | 3 | s |
| b218 | 9 | `200/2` | 100 | Hz |
| b218 | 10 | `36*5` | 180 | MWh |
| b219 | 1 | `1200000-700000-100000-50000` | 350000 | m3/day |
| b219 | 2 | `420-170` | 250 | kPa |
| b219 | 3 | `0.006*12/(0.003*24)` | 1 | m |
| b219 | 4 | `0.65*4*0.8*math.sqrt(2*9.81*9)` | 27.63974877 | m3/s |
| b219 | 5 | `1000*9.81*35*18/140/1000` | 44.145 | kW/m2 |
| b219 | 6 | `6*15*3600/1000` | 324 | tonne |
| b219 | 7 | `1000*9.81*8*60*0.86/1e6` | 4.049568 | MW |
| b219 | 8 | `6*(6/7.4)**(2/3)*math.sqrt(0.0004)/0.025` | 4.17369707 | m3/s |
| b219 | 9 | `(21-12)/180` | 0.05 | mm/day |
| b219 | 10 | `0.6*2000000/0.75` | 1600000 | m3 |
| b220 | 1 | `500000+300000-600000-40000` | 160000 | m3/day |
| b220 | 2 | `(4000000+5000000)*2/2` | 9000000 | m3 |
| b220 | 3 | `(2*18+1*42)/(2+1)` | 26 | mg/L |
| b220 | 4 | `1000*9.81*1.8*(45+12)/0.78/1000` | 1290.392308 | kW |
| b220 | 5 | `0.02+(1-0.02)*0.05*0.04` | 0.02196 | probability |
| b220 | 6 | `108-103-1.2-0.3-0.4` | 3.1 | m |
| b220 | 7 | `0.12*40000000*0.45` | 2160000 | m3 |
| b220 | 8 | `30000000/600000` | 50 | year |
| b220 | 9 | `12000000/(500000*(1-0.15))` | 28.23529412 | day |
| b220 | 10 | `(1.8-1.74)/math.sqrt(0.02**2+0.018**2)` | 2.229882439 | dimensionless |

## Final artifacts

`research_taiwan_dams.json` preserves access evidence and scoped claims. `reviews/numeric_taiwan_author.json` preserves each final model hash, misconception hash, input hash and recomputation. All six input JSONs pass the unchanged strict validator.
