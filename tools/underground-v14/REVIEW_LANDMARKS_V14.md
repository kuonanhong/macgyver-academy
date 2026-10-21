# V14 landmark authoring and numerical review

Reviewed 2026-10-21. Scope: hsuehshan and b102–b125, 25 courses, 250 bilingual units; root expands each unit into four steps (1000 new steps). The three existing courses are to be appended by the integrator, not overwritten.

## Numerical review

- `audit_landmarks.py` independently reads emitted traces and uses separately expressed equations and SI conversions; it does not import or execute author-model functions.
- All 250 base calculations and 250 single-input +10% sensitivity recalculations agree within relative/absolute tolerance 1e-11. All 250 displayed bilingual models contain their recorded inputs, base result and sensitivity result.
- Each dimensionless gradient, coefficient, ratio and efficiency is labelled. Numerical scenarios are hypothetical; no teaching result is represented as a project measurement or acceptance criterion.
- Facts now contain two scoped project facts and four named calculations selected from that same course. No course-count filler or common three-example block remains.

| Independent sample | Result | Scope |
|---|---:|---|
| Lotschberg single-direction occupancy | 3.52941176 trains/h | excludes opposing conflicts |
| Fehmarn still-water buoyancy reserve | 3378.564 kN | not transverse stability |
| Eurasia roadway strip | 45.36 kN·m | not full deck/frame design |
| New Wujie full-pipe friction | 1.83486239 m | no transients or local loss |
| Outer channel material advection | 26.1111111 min | not flood-wave celerity |
| Outer channel rectangular-hydrograph storage | 87600 m³ | time step, not whole flood routing |
| Drop-shaft energy flux | 5886 kW | not shaft wall pressure or pump output |
| Jurong common-datum pressure difference | 176.2 kPa | local gradient, not complete containment |
| Jurong available hypothetical inventory | 27600 m³ | same-temperature inventory, not operation limit |

## Physics and source corrections

- Independent cross-author review clarified the elastic Kirsch scale: `3γH` is `σθ,max`, the sidewall maximum under vertical uniaxial remote compression and zero horizontal remote stress, not an arbitrary wall value. Jurong hypothetical cover is 120 m to keep the exercise near a cavern setting; it remains distinct from the published facility depth.

- Replaced mismatched annulus-grout exercises in Seikan and Ryfylke fracture sealing with equal-head before/after inflow reduction. Annular backfill remains only in shield-lining contexts.
- Rectangular Fehmarn, Marmaray and HZMB boxes use frame/strip bending; no thin circular-ring model appears in those three courses.
- New Wujie and the flood channel use water advection and hydraulic loss; Jurong uses land/inventory/containment. None uses a vehicle travel-time formula.
- Guanyin duct partition is explicitly distinguished from a traffic-bearing double-deck roadway.
- Geometric gasket reserve is not contact pressure; diffusion length is not corrosion-initiation life; advection is not flood-wave celerity; roof bending does not establish flotation.
- Ryfylke 292 m is geometric depth, not automatically local piezometric head. Jurong pressure uses one elevation and includes product head and gas gauge pressure.

## Primary project context checked

Every course also includes the FHWA official 2009 manual landing page and PIARC public road-tunnel manual. They support comparative principles, not project-specific inputs; road guidance is not asserted to govern rail, water or storage facilities. Map coordinates are approximate educational reference points, not entrances. Vendors are explicitly source institutions or publicly documented organisations, with no academy partnership or invented contract.

| ID | Public dimension and event | Project sources |
|---|---|---|
| hsuehshan | The public scale is about 12.9 km; retain the measurement boundary in the cited source. 2006 event: Hsuehshan Tunnel opens to small vehicles before a later staged opening to coaches. | https://www.freeway.gov.tw/Publish.aspx?cnid=610&p=126 |
| b102 | The public scale is about 50 km; retain the measurement boundary in the cited source. 1994 event: The Channel Tunnel opens as a fixed railway connection across the Channel. | https://press.getlinkgroup.com/news/1994-2024-the-channel-tunnel-30-years-of-unique-history-d776-0791e.html |
| b103 | The public scale is about 57 km; retain the measurement boundary in the cited source. 2016 event: Gotthard Base Tunnel enters service as a core of the Swiss low-gradient transalpine railway. | https://www.uvek.admin.ch/en/nrla |
| b104 | The public scale is about approximately 35 km; retain the measurement boundary in the cited source. 2007 event: Lotschberg Base Tunnel enters service with portions of the second bore awaiting expansion. | https://www.bls.ch/en/unternehmen/projekte-und-hintergruende/neat |
| b105 | The public scale is about 15.4 km; retain the measurement boundary in the cited source. 2020 event: Ceneri Base Tunnel is completed and enters full operation at year end. | https://www.uvek.admin.ch/en/nrla |
| b106 | The public scale is about 53.85 km; retain the measurement boundary in the cited source. 1988 event: Seikan Tunnel begins commercial operation on 13 March. | https://www.jrhokkaido.co.jp/network/seikan/01.html |
| b107 | The public scale is about 18 km; retain the measurement boundary in the cited source. 2020 event: Fehmarnbelt tunnel construction begins; this is not an opening date. | https://femern.com/ |
| b108 | The public scale is about 1387 m immersed section; retain the measurement boundary in the cited source. 2013 event: Marmaray cross-strait railway tunnel enters service. | https://holding.gama.com.tr/tr/proje/10273/<br>https://www.gov-online.go.jp/eng/publicity/book/hlj/html/201311/201311_00_en.html |
| b109 | The public scale is about 5.4 km tunnel and connection section; retain the measurement boundary in the cited source. 2016 event: Eurasia Tunnel is completed and launched for service. | https://www.avrasyatuneli.com/en/corporate/what/about<br>https://www.avrasyatuneli.com/en/corporate/what/chronology |
| b110 | The public scale is about 15.1 km whole road corridor; retain the measurement boundary in the cited source. 1997 event: The documented Aqua-Line tunnel construction contract is completed in December. | https://www.obayashi.co.jp/chronicle/works/d055.html |
| b111 | The public scale is about 24.5 km; retain the measurement boundary in the cited source. 2000 event: Laerdal road tunnel formally opens to traffic in November. | https://www.vegvesen.no/en/road-projects/project/e16lardalstunnelen/ |
| b112 | The public scale is about 16.9 km second-tube alignment; retain the measurement boundary in the cited source. 1980 event: The original Gotthard Road Tunnel begins highway operation. | https://gotthardtunnel.ch/en/the-second-tube/project-details-aim-purpose |
| b113 | The public scale is about 5798 m; retain the measurement boundary in the cited source. 1964 event: The Great St Bernard road tunnel officially opens in March. | https://letunnel.com/en/il-tunnel/le-strutture-del-tunnel/<br>https://letunnel.com/en/il-tunnel/ |
| b114 | The public scale is about 11.6 km; retain the measurement boundary in the cited source. 1965 event: Mont Blanc cross-border road tunnel opens to traffic in July. | https://www.atmb.com/connaitre-atmb/qui-est-atmb/le-tunnel-du-mont-blanc-ouvrage-exceptionnel-innovant-et-securise/<br>https://www.atmb.com/connaitre-atmb/histoire-datmb-les-dates-cles-de-la40-la-rn205-et-le-tunnel-du-mont-blanc/histoire/histoire-du-tunnel-du-mont-blanc/ |
| b115 | The public scale is about 12.87 km original tunnel; retain the measurement boundary in the cited source. 1980 event: The original Frejus Road Tunnel enters service. | https://www.ecologie.gouv.fr/presse/inauguration-philippe-tabarot-du-second-tube-du-tunnel-du-frejus-lundi-28-juillet-2025 |
| b116 | The public scale is about 55 km base tunnel; 64 km linked route; retain the measurement boundary in the cited source. 2014 event: Work starts on the Tulfes–Pfons lot; this is not whole-project opening. | https://www.bbt-se.com/en/brenner-base-tunnel/project-overview/<br>https://www.bbt-se.com/en/brenner-base-tunnel/bbt-history/ |
| b117 | The public scale is about 6.5 km TBM middle section within 16.5 km conveyance scope; retain the measurement boundary in the cited source. 2002 event: The documented middle-section TBM drive achieves breakthrough in June. | https://service.taipower.com.tw/Collection/2009/2025/8709/ |
| b118 | The public scale is about approximately 7.9 km; retain the measurement boundary in the cited source. 2016 event: The highway authority records a Guanyin Tunnel breakthrough milestone. | https://www.thb.gov.tw/News_Content.aspx?Create=1&n=87&s=51127<br>https://tra.hccp.gov.tw/blogs/1930 |
| b119 | The public scale is about approximately 7 km tunnel section; retain the measurement boundary in the cited source. 2018 event: The Hong Kong–Zhuhai–Macao crossing enters service. | https://www.hzmb.gov.hk/en/main-bridge.html<br>https://www.cso.gov.hk/eng/blog/blog20181111.htm |
| b120 | The public scale is about 10.8 km; retain the measurement boundary in the cited source. 2011 event: Shiziyang Tunnel opens for service in December. | https://source.nra.gov.cn/ztzl/hy/kjcx/kjxm/201802/t20180212_198473.shtml |
| b121 | The public scale is about 32.645 km; retain the measurement boundary in the cited source. 2014 event: Both main bores of New Guanjiao Tunnel achieve breakthrough in April. | https://www.gov.cn/xinwen/2014-04/15/content_2659690.htm |
| b122 | The public scale is about 18.02 km single-bore route; retain the measurement boundary in the cited source. 2007 event: Qinling Zhongnanshan Highway Tunnel opens on 20 January. | https://jtyst.shaanxi.gov.cn/static/home/nianjian/2018/13.pdf |
| b123 | The public scale is about 14.4 km; retain the measurement boundary in the cited source. 2019 event: Ryfylke Tunnel opens to traffic on 30 December. | https://www.vegvesen.no/om-oss/presse/aktuelt/nasjonalt/verdens-lengste-og-dypeste-veitunnel-er-apnet/ |
| b124 | The public scale is about 6.3 km underground waterway; retain the measurement boundary in the cited source. 2002 event: The 3.3 km reach from shaft 3 to the pumping station begins interim use in June. | https://www.ktr.mlit.go.jp/edogawa/study/sora/gaikaku/detail/zentai04.html<br>https://www.ktr.mlit.go.jp/edogawa/edogawa00147.html |
| b125 | The public scale is about 1.47 million m³ storage capacity; retain the measurement boundary in the cited source. 2014 event: Jurong Rock Caverns storage facility officially opens in September. | https://www.jtc.gov.sg/find-space/jurong-rock-caverns<br>https://www.pmo.gov.sg/newsroom/transcript-prime-minister-lee-hsien-loongs-speech-official-opening-jurong-rock-caverns/ |

## Deliberate limits and unresolved source differences

- Fehmarn current owner page gives 18 km; an older Sund & Baelt facts page gives 19 km. The latter length was excluded. Construction start 2020 is not opening, and no predicted opening date is stated.
- Lotschberg uses BLS approximately 35 km wording, without silently mixing a differently rounded 34 km NRLA description.
- Marmaray 1387 m is immersed section, not total railway length; Eurasia 5.4 km is tunnel-and-connections within a 14.6 km corridor; Aqua-Line 15.1 km is the whole road and the stated 1997 milestone is the documented contract completion.
- Gotthard Road 16.9 km is the second-tube alignment from FEDRO; the 1980 event refers to the original operational tunnel. The no-capacity-increase purpose remains explicit.
- Frejus source is a 2025 advance notice. The lesson states that a second-tube opening event was announced, rather than treating that notice as a post-event completion certificate. Its core historical event is the documented 1980 original opening.
- Brenner 55 km main works versus 64 km connected route are distinct; 2014 is only the Tulfes–Pfons lot excavation start.
- New Wujie uses Taipower archival scope: 16.5 km conveyance scope, 6.5 km TBM middle section, June 2002 breakthrough of that drive. It does not assert a full-project commissioning date.
- Guanyin 2016 breakthrough and 2020 corridor opening are separated; New Guanjiao April 2014 is breakthrough, not opening.
- HZMB uses the Hong Kong government rounded 7 km tunnel-section figure. It does not pretend this equals immersed-only length.
- Qinling Zhongnanshan: official Shaanxi yearbook search index supplied 18.02 km and 20 January 2007. Direct PDF retrieval failed; the course source scope explicitly limits review to that indexed extract. CREC English page gives conflicting 18.4 km and 2002 start; these values were excluded, and no start date was asserted.
- Outer channel June 2002 is interim operation of 3.3 km, not completion of all 6.3 km; the separate 1993–2006 construction span is documented.
- Jurong 2014 opening is supported by PMO, storage scale by JTC; hypothetical volume/height is not claimed as measured land saving.

## Reproducibility

`build_landmarks.py` reconstructs the 25 inputs from `landmarks_core.py`, `landmarks_dossiers.py` and `landmarks_models.py`. `calculation_landmarks.json` records full input labels and units. `audit_landmarks_numeric.json` contains all 250 independently calculated results. `research_landmarks.json` records scoped URLs, access limitations and hypothetical-scenario provenance. All 25 input validators pass without lowering depth thresholds.
