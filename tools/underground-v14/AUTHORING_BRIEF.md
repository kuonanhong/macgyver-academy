# V14 隧道與地下工程 100 門逐步課程 — 作者簡報 / Authoring brief

You are writing authored inputs for **step-by-step engineering courses** in the
MacGyver Engineering Academy (馬蓋先工程學院), collection **"Tunnels & Underground Works"
(隧道與地下工程)**. Each input file becomes a bilingual course of **5 stages × 8 steps =
40 steps**. A Python generator turns each of your **10 units** into 4 steps —
(1) mechanism & load path, (2) quantitative model, (3) testing / measurement /
verification, (4) failure diagnosis — plus knowledge points, quizzes, a worked
example, a fact sheet, a timeline, codes, landmark comparisons, a map point,
vendor cards with stock lookup and an original architecture diagram.
Every field of a unit becomes its own step, so each field must stand on its own
and be concrete. **Your text is the substance of the course — write like a
senior underground / geotechnical engineer teaching a capable apprentice.**

## Files

* Targets (ids, exact titles, discipline, family, existing steps): `tools/underground-v14/targets.json`
* **Gold example — copy its depth, tone and format:** `tools/underground-v14/inputs/hsuehshan.json`
* Validator (must print `OK`): `python3 -I tools/underground-v14/validate_input.py tools/underground-v14/inputs/<id>.json`
* Write each course to `tools/underground-v14/inputs/<id>.json` (UTF-8, pretty JSON, 2-space indent).

## Bilingual convention

Every bilingual field is ONE string: `中文內容~English content` (exactly one `~`).
Traditional Chinese (台灣用語, e.g. 混凝土、鋼筋、預力、支承、伸縮縫、帷幕牆、斜張橋、懸索橋)
first, English second. Never put CJK characters in the English half. Keep symbols,
units and formulas in both halves. Do not use the `~` character anywhere else
(write "approximately" / 「約」 instead of a tilde).

## Course-level fields

| field | content |
|---|---|
| `id`, `title`, `discipline`, `family` | copy exactly from `targets.json` (`title` = `title~titleEn`) |
| `focus` | one line: the engineering focus of this course |
| `summary` | 2–3 sentences specific to this tunnel / underground facility / technique |
| `units` | **exactly 10**, ordered to follow the 5 stages below |
| `example` | an ORIGINAL worked numeric example (formula → numbers → units → result → what changes if one input changes); say the numbers are teaching assumptions |
| `history` | 3–4 sentences of public engineering context: who / when / why / what was new; end by saying the course reconstructs public principles only |
| `facts` | 6–10 key facts, each `中文~English` **with a number** (length, depth, water head, opening year, section, concrete strength, lining thickness, deformation or permeability…). For a technique course use explicitly labelled numerical teaching assumptions and results, or verified values from named projects. List real numbers and units, not just numbered disclaimers. Use only verified project facts; write 「約」/"about" when rounded |
| `timeline` | 3–6 `{ "year": "1998", "event": "中文~English" }` milestones (design, construction start, key erection step, opening, retrofit, record…). For a technique: invention, first major use, codification, landmark uses |
| `codes` | 2–4 real codes / standards / guidelines relevant to the topic, e.g. AASHTO LRFD Bridge Design Specifications, Eurocode 1/2/3/8 (EN 1991/1992/1993/1998), ACI 318, AISC 360/341, ASCE 7, ASCE 41, fib Model Code, PTI/fib grouting guides, ISO 10137, ISO 4354, AWS D1.1/D1.5, RCSC bolt specification, EN 1090, ASTM E330/E331/E283, AAMA 501, NFPA, EN 81-20, Japanese Specifications for Highway Bridges (道路橋示方書), 中華民國公路橋梁設計規範、公路橋梁耐震設計規範、建築物耐震設計規範及解說、建築物耐風設計規範及解說、建築技術規則 |
| `landmarks` | 2–4 named real projects (`中文~English`). For a named project: comparable projects to contrast with; for a technique: projects where it was used |
| `place` | a representative public site with approximate `lat`/`lng` and a Google-Maps `query`. Named projects: the structure itself. Techniques: a public landmark where the technique is visible, or a public research lab (e.g. NCREE 國家地震工程研究中心, Lehigh ATLSS, PEER, BRI Tsukuba) |
| `sources` (3–5) | **real, existing** public pages; ≥ 2 must be `primary` (owner/operator, government agency, designer, contractor, standards body, university lab, CTBUH Skyscraper Center, FHWA, NIST…). Wikipedia allowed only as `secondary` |
| `vendors` (2–4) | real companies/institutions relevant to the course; `security` = `{symbol, exchange, currency}` only for **listed** companies you are sure of, else `null` |
| `related` | 2 other ids from this underground set (see `targets.json`), the closest comparisons |
| `architectureNodes` 4–6, `architectureEdges` | functional blocks of the structure/system and their load or information connections |

### The 10 units map to 5 stages (2 units per stage)

1. **工程背景、荷載與結構系統 / Context, loads and structural system** – units 1–2 (site, demand, load cases, load path, structural form, dynamic behaviour)
2. **材料、構件與接合細部 / Materials, members and connection details** – units 3–4 (steel/concrete/cable/foundation materials, member sizing, connection and detailing)
3. **施工方法與施工階段控制 / Construction methods and stage control** – units 5–6 (erection method, temporary works, geometry/stress control during construction, closure)
4. **試驗、量測與監測驗證 / Testing, measurement and monitoring** – units 7–8 (wind-tunnel, load test, survey, sensors, NDT, acceptance)
5. **耐久、維護與工程交接 / Durability, maintenance and engineering handoff** – units 9–10 (corrosion, fatigue, inspection, retrofit, lifecycle records, handover)

Adapt the stage themes to the topic (e.g. for BIM: stage 3 = coordination workflow during construction), but keep the order.

Each unit needs (see the gold example):

* `anchor` – the concrete component / quantity the step points at (short, unique in the course)
* `title` – unit title (unique in the course)
* `mechanism` – 3–5 sentences explaining the structural mechanism / load path / behaviour (100–460 CJK chars; 60–260 English words)
* `model` – a quantitative relation **evaluated once with numbers and units** (catenary/sag H = wL²/8f, Euler buckling, Strouhal, pendulum, thermal ΔL = αLΔT, creep/shrinkage, hydration ΔT, bolt preload, S–N fatigue, scour depth, Den Hartog, stiffness k = EA/L, prestress losses, ...). Compute it — numbers must be self-consistent.
* `verify` – how an engineer measures / tests / accepts it (instrument, procedure, what is compared, acceptance criterion)
* `failure` – a realistic failure mode, symptom and consequence (real historical failures are welcome when accurately stated, e.g. Tacoma Narrows 1940, Quebec Bridge 1907, Silver Bridge 1967, Hyatt Regency walkway 1981, Sampoong 1995, I-35W 2007, Morandi 2018, Nanfang'ao 南方澳 2019, Citicorp 1978 wind issue, Millennium Bridge 2000 lateral sway)
* `misconception` – one plausible-sounding wrong belief (used as a quiz distractor)
* `practice` – a site / design-office practice note: a detailing rule, hold point, specification clause idea, inspection habit or coordination rule a chief engineer would insist on

## Quality bar

* **Accuracy first.** For named tunnels and underground works, check key numbers (total/bored length, maximum overburden, section, opening year, geology, excavation method and lining system) against official/authoritative pages with WebSearch/WebFetch. If two sources disagree, use the owner/operator value and say 「約」/"about". Never invent numbers about a real project; when unsure, move the number into the clearly labelled teaching-assumption calculation instead.
* Be **specific to the named tunnel or technique**: distinguish rail and road facilities, bore length and route length, sea depth and cover, geological risks, excavation method, lining action and operation. Do not import facts from another project or imply that a synthetic model reproduces the as-built design.
* Units of the same course must NOT repeat each other; courses must not reuse paragraphs from other courses. Every sentence must carry engineering content.
* Technique courses (craft topics) must anchor on at least two named real projects (in `landmarks`, `facts` or `history`).
* No proprietary recipes, no fabricated test data presented as real, no step-by-step instructions for hazardous field operations (rigging, hot work, tensioning) presented as authorisation — the course teaches reasoning, checks and hold points, not operating permits. Safety-relevant topics end in "who must approve / which hold point".
* Verify every URL with WebSearch or WebFetch (the result must show that exact page). Prefer official pages. Do not invent URLs. If a page cannot be confirmed, choose another.
* **Tone:** confident, precise, educational. No marketing language.

### Vendors and listed securities

Give `security` only when certain (else `null`). Known-good examples — still double-check anything you are unsure about:
Vinci→EURONEXT:DG EUR · Bouygues→EURONEXT:EN EUR · Eiffage→EURONEXT:FGR EUR · Saint-Gobain→EURONEXT:SGO EUR ·
Skanska→STO:SKA-B SEK · Hexagon→STO:HEXA-B SEK · Trelleborg→STO:TREL-B SEK · Hochtief→XETRA:HOT EUR ·
Heidelberg Materials→XETRA:HEI EUR · Nemetschek→XETRA:NEM EUR · ACS→BME:ACS EUR · Ferrovial→BME:FER EUR ·
Webuild→BIT:WBD EUR · Strabag→VIE:STR EUR · Implenia→SIX:IMPN CHF · Schindler→SIX:SCHP CHF · Sika→SIX:SIKA CHF ·
Holcim→SIX:HOLN CHF · KONE→HEL:KNEBV EUR · AECOM→NYSE:ACM USD · Jacobs→NYSE:J USD · Fluor→NYSE:FLR USD ·
Otis→NYSE:OTIS USD · Cemex→NYSE:CX USD · CRH→NYSE:CRH USD · Nucor→NYSE:NUE USD · Manitowoc→NYSE:MTW USD ·
Terex→NYSE:TEX USD · Taylor Devices→NASDAQ:TAYD USD · Trimble→NASDAQ:TRMB USD · Autodesk→NASDAQ:ADSK USD ·
Bentley Systems→NASDAQ:BSY USD · Procore→NYSE:PCOR USD · WSP Global→TSX:WSP CAD · Stantec→TSX:STN CAD ·
Kajima→TSE:1812 JPY · Obayashi→TSE:1802 JPY · Taisei→TSE:1801 JPY · Shimizu→TSE:1803 JPY ·
Sumitomo Mitsui Construction→TSE:1821 JPY · IHI→TSE:7013 JPY · Kawasaki Heavy Industries→TSE:7012 JPY ·
Nippon Steel→TSE:5401 JPY · JFE Holdings→TSE:5411 JPY · Kobe Steel→TSE:5406 JPY · Tokyo Rope→TSE:5981 JPY ·
Bridgestone→TSE:5108 JPY · Mitsubishi Electric→TSE:6503 JPY · Hitachi→TSE:6501 JPY · Fujitec→TSE:6406 JPY ·
AGC→TSE:5201 JPY · Topcon→TSE:7732 JPY · Samsung C&T→KRX:028260 KRW · Hyundai E&C→KRX:000720 KRW ·
China State Construction Engineering→SSE:601668 CNY · China Communications Construction→SSE:601800 CNY ·
China Railway Group→SSE:601390 CNY · China Railway Construction→SSE:601186 CNY · Sany Heavy Industry→SSE:600031 CNY ·
China Steel 中鋼→TWSE:2002 TWD · Taiwan Cement 台泥→TWSE:1101 TWD · Asia Cement 亞泥→TWSE:1102 TWD ·
CTCI 中鼎→TWSE:9933 TWD · ArcelorMittal→AMS:MT EUR · Bekaert→EBR:BEKB EUR · Emaar Properties→DFM:EMAAR AED.
Taiwanese contractors (大陸工程、中華工程、潤弘精密、根基營造 …): verify the ticker by WebSearch before using it, otherwise `null`.
Private firms / subsidiaries → `security: null` (Arup, SOM, Thornton Tomasetti, COWI, Ramboll, Leonhardt Andrä und Partner,
Mott MacDonald, Buro Happold, RWDI, Freyssinet (Vinci), VSL (Bouygues), DYWIDAG, mageba, MAURER, FIP, Liebherr, Mammoet,
Sarens, Doka, PERI, Hilti, Permasteelisa, Schüco, Josef Gartner, Takenaka, Bechtel, TK Elevator).
Owners and institutions are valid "vendors" with `security: null` (交通部公路局, 本州四國連絡高速道路 JB Honshi,
Golden Gate Bridge Highway and Transportation District, Øresundsbro Konsortiet, Sund & Bælt, Transport Scotland,
Highways England/National Highways, FHWA, NIST, NCREE 國家地震工程研究中心, CTBUH).
Do not list a company merely because it is famous — `role` must say what the course learner can study from it.

## Extending an existing guided course (`danjiang`, `b003`, `b015`, `b021`)

`targets.json` marks these with `"mode": "extend-existing"` and lists their current
steps in `existingSteps`. Existing steps and IDs are kept unchanged; your 10 units
become 40 NEW steps appended after them. Your units must therefore go **deeper**
than, and not repeat, the existing step topics — e.g. quantitative cable/stay force
models, deck aerodynamic derivatives and flutter speed, fatigue detail categories,
foundation settlement and scour numbers, construction-stage camber, wind-tunnel and
monitoring data interpretation, retrofit and hanger/stay replacement engineering.

## Done criteria for your batch

1. All assigned files exist in `tools/underground-v14/inputs/`.
2. `python3 -I tools/underground-v14/validate_input.py <your files>` prints OK for each.
3. Final report (short): files written; for each course the source URLs you verified;
   any fact or ticker you were unsure of and how you handled it (`null`, 「約」, moved into assumptions).
