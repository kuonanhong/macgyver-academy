# V12 光學與精密儀器 101 門逐步課程 — 作者簡報 / Authoring brief

You are writing the authored inputs for **step-by-step engineering courses** in the
MacGyver Engineering Academy (馬蓋先工程學院). Each input file becomes a 32-step
bilingual course (4 stages × 8 steps). A Python generator turns each of your 8
"units" into 4 steps — (1) mechanism analysis, (2) quantitative model,
(3) measurement/verification, (4) failure diagnosis — plus knowledge points,
quizzes, a worked example, a history, a map point, vendor cards with stock
lookup and an architecture diagram. Because every field of a unit becomes its
own step, each field must stand on its own and be concrete. **Your text is the substance
of the course — write like a senior engineer teaching a capable apprentice.**

## Files

* Targets (ids, exact titles, discipline, family): `tools/optics-v12/targets.json`
* Gold example (copy its depth and tone): `tools/optics-v12/inputs/a402.json`
* Validator (must print `OK`): `python3 -I tools/optics-v12/validate_input.py tools/optics-v12/inputs/<id>.json`
* Write each course to `tools/optics-v12/inputs/<id>.json` (UTF-8, pretty JSON).

## Bilingual convention

Every bilingual field is ONE string: `中文內容~English content` (exactly one `~`).
Traditional Chinese (台灣用語) first, English second. Do not mix languages inside
a half. Keep technical symbols, units and formulas in both halves.

## Field rules (validator enforces minimum depth)

| field | content |
|---|---|
| `id`, `title`, `discipline` | copy exactly from `targets.json` (`title` = `title~titleEn`) |
| `family` | copy from targets (schematic family) |
| `focus` | one line: the engineering focus of this course |
| `summary` | 1–2 sentences that are **specific to this instrument/facility** |
| `units` (exactly 8) | the technical backbone; ordered to follow the 4 stages below |
| `example` | an ORIGINAL worked numeric example with formula, numbers, units, result (state that numbers are teaching assumptions) |
| `history` | 2–3 sentences of public engineering context (who/when/why; no proprietary claims) |
| `place` | a representative public institution/site with approximate lat/lng and a Google-Maps query |
| `sources` (2–4) | **real, existing** public pages: official vendor/institution/lab/standards pages, university course notes, NIST/NASA/ESO/CERN etc. ≥2 must be `primary`. Wikipedia allowed only as `secondary`. |
| `vendors` (2–4) | real companies/institutions relevant to the course with business description; `security` = `{symbol, exchange, currency}` for **listed** companies (only if you are sure), otherwise `null` |
| `related` | 2 other ids from the optics set (a401–a500 or `asml`) |
| `architectureNodes` 4–6, `architectureEdges` | functional blocks of the instrument and their connections (for the original schematic) |

### The 8 units map to 4 stages (2 units per stage)

1. **系統邊界與物理原理 / System boundaries and physical principles** – units 1–2
2. **元件、材料與製造 / Components, materials and fabrication** – units 3–4
3. **量測、校正與誤差預算 / Measurement, calibration and error budgets** – units 5–6
4. **系統整合、驗證與工程交接 / Integration, validation and engineering handoff** – units 7–8

Each unit needs:

* `anchor` – the concrete component/signal the step points at (short)
* `title` – unit title
* `mechanism` – 2–4 sentences explaining the physics/engineering mechanism (≥80 CJK chars / ≥50 English words)
* `model` – a quantitative relation, design rule or estimate **with numbers and units** (e.g. a formula evaluated once)
* `verify` – how an engineer measures/validates this unit (instrument, procedure, what to compare)
* `failure` – a realistic failure mode, its symptom and consequence
* `misconception` – one plausible-sounding wrong belief (used as a quiz distractor)

## Quality bar

* Accuracy first. Use well-known public physics and engineering (Bragg, Rayleigh,
  Abbe, Sagnac, Maréchal, Stoney, Allan deviation, shot noise, etc.). Numbers
  must be self-consistent — compute them. Mark assumed values as assumptions.
* Be specific to the named instrument or facility (e.g. for "ESO ELT" talk about the 39 m segmented primary, 798 segments, M4 adaptive mirror; for "LIGO" talk about 4 km arms, Fabry–Pérot arm cavities, 1064 nm, quadruple pendulums).
* No proprietary recipes, no weapon content, no operating instructions for hazardous equipment — this is educational modelling.
* Verify every URL with WebSearch (the result list must show the URL/title). Prefer official pages. Do not invent URLs. If a page cannot be confirmed, choose another.
* Vendors: use real companies (ZEISS, Thorlabs, Edmund Optics, Hamamatsu, Nikon, Canon, Keyence, Zygo/AMETEK, Renishaw, Hexagon, Bruker, Thermo Fisher, Horiba, Shimadzu, Coherent, IPG, Lumentum, Jenoptik, Oxford Instruments, Bluefors, Pfeiffer Vacuum, Edwards, Agilent, Leybold, Teledyne, Andor/Oxford, Excelitas, Hamamatsu, Honeywell, Safran, Northrop Grumman, Exail/iXblue, Menlo Systems, Toptica, NKT Photonics, Microchip, Largan, Asia Optical, Young Optics, Chroma ATE, Gudeng, etc.). Give listed securities only when certain: e.g. ASML→NASDAQ:ASML USD, Nikon→TSE:7731 JPY, Canon→TSE:7751 JPY, Hamamatsu→TSE:6965 JPY, Keyence→TSE:6861 JPY, Renishaw→LSE:RSW GBP, Hexagon→STO:HEXA-B SEK, AMETEK→NYSE:AME USD, Bruker→NASDAQ:BRKR USD, Thermo Fisher→NYSE:TMO USD, Horiba→TSE:6856 JPY, Shimadzu→TSE:7701 JPY, Coherent→NYSE:COHR USD, IPG→NASDAQ:IPGP USD, Lumentum→NASDAQ:LITE USD, Jenoptik→XETRA:JEN EUR, Oxford Instruments→LSE:OXIG GBP, Pfeiffer Vacuum→XETRA:PFV EUR, Agilent→NYSE:A USD, Teledyne→NYSE:TDY USD, Honeywell→NASDAQ:HON USD, Safran→EURONEXT:SAF EUR, Northrop Grumman→NYSE:NOC USD, Microchip→NASDAQ:MCHP USD, Largan 大立光→TWSE:3008 TWD, Asia Optical 亞洲光學→TWSE:3019 TWD, Young Optics 揚明光→TWSE:3504 TWD, Chroma 致茂→TWSE:2360 TWD, Gudeng 家登→TPEx:3680 TWD, Lasertec→TSE:6920 JPY, Tokyo Electron→TSE:8035 JPY, Hoya→TSE:7741 JPY, AGC→TSE:5201 JPY, Corning→NYSE:GLW USD, Sony→TSE:6758 JPY, Olympus→TSE:7733 JPY, Evident(private), Carl Zeiss Meditec→XETRA:AFX EUR, KLA→NASDAQ:KLAC USD, Onto→NYSE:ONTO USD, Nova→NASDAQ:NVMI USD, Camtek→NASDAQ:CAMT USD, Applied Materials→NASDAQ:AMAT USD, Lam→NASDAQ:LRCX USD, Trimble→NASDAQ:TRMB USD, FARO→NASDAQ:FARO USD, Cognex→NASDAQ:CGNX USD, Basler→XETRA:BSL EUR, Ushio→TSE:6925 JPY, Topcon→TSE:7732 JPY, Fujifilm→TSE:4901 JPY, Seiko Epson→TSE:6724 JPY, Sumitomo Electric→TSE:5802 JPY, Fujikura→TSE:5803 JPY, Prysmian→BIT:PRY EUR, Ciena→NYSE:CIEN USD, Garmin→NYSE:GRMN USD, Leonardo DRS→NASDAQ:DRS USD, L3Harris→NYSE:LHX USD, RTX→NYSE:RTX USD, Lockheed Martin→NYSE:LMT USD, BAE Systems→LSE:BA GBP, Mitsubishi Electric→TSE:6503 JPY, Hitachi→TSE:6501 JPY, JEOL→TSE:6951 JPY, Toshiba(private 2023), Rigaku→TSE:268A JPY, Halma→LSE:HLMA GBP, Spectris→LSE:SXS GBP, Sartorius→XETRA:SRT EUR, Danaher→NYSE:DHR USD, Waters→NYSE:WAT USD, Mettler-Toledo→NYSE:MTD USD, Zygo = part of AMETEK, Leica Microsystems = part of Danaher, Andor = part of Oxford Instruments, Bluefors(private), Thorlabs(private), Edmund Optics(private), Zeiss(private foundation), Trumpf(private), Schott(private), Menlo(private), Toptica(private), Exail(private), Gooch & Housego→LSE:GHH GBP, Lumibird→EURONEXT:LBIRD EUR, nLight→NASDAQ:LASR USD, MKS→NASDAQ:MKSI USD, Novanta→NASDAQ:NOVT USD, II-VI = Coherent, Veeco→NASDAQ:VECO USD, Excelitas(private), Hamamatsu as above, Axcelis→NASDAQ:ACLS USD, Comet→SIX:COTN CHF, Oerlikon→SIX:OERL CHF, Bühler(private), Samsung Electronics→KRX:005930 KRW, LG Innotek→KRX:011070 KRW, Sunny Optical→HKEX:2382 HKD. Institutions (ESO, CERN, NASA, NIST, PTB, KEK, RIKEN, NSRRC 國家同步輻射研究中心, ITRI 工研院, LIGO Lab) are valid "vendors" with `security: null` and `entityType` implied.

## Tone

Confident, precise, educational. Avoid marketing language. Every sentence must
carry engineering content. Each course should read as **different** from the
others — do not reuse paragraphs between courses.

## Done criteria for your batch

1. All assigned files exist in `tools/optics-v12/inputs/`.
2. `python3 -I tools/optics-v12/validate_input.py <your files>` prints OK for each.
3. Report: list of files written, the sources you verified (URL + how), and any
   uncertainty (e.g. a ticker you were not sure about → set `security: null`).


## Extending an existing guided course (`asml`, `a405`)

`targets.json` marks these with `"mode": "extend-existing"` and lists their
current steps in `existingSteps`. Existing steps and IDs are kept unchanged; your
8 units become 32 NEW steps appended after them. Therefore your units must go
deeper than, and not repeat, the existing step topics (e.g. for `asml`: pellicles,
reticle-stage dynamics, EUV collector lifetime, high-NA anamorphic optics, dose
and focus metrology, wafer-table thermal control, field-to-field overlay
modelling, throughput/availability; for `a405`: apochromat/triplet extension,
partial dispersion, cemented vs air-spaced doublets, thermal defocus,
MTF-based acceptance, interferometric test, stray light, production centring).
