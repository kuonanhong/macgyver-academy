# V15 hydraulics and transferred dam author handoff

Owned inputs: **b210–b214 and b241–b255**. These are 20 complete bilingual courses with exactly 10 distinct units each (200 units; the root generator supplies four steps per unit). The author does not own b256–b260.

## Verification

- `validate_input.py`: all 20 owned inputs pass unchanged V14 depth thresholds and V15 catalog title/discipline checks.
- `audit_hydraulics.py`: all 200 primary formulas recomputed from stated teaching inputs. Unrounded expected results use relative tolerance 1e-9; every printed result is additionally checked against its displayed decimal precision. The JSON records the exact SHA-256 of each reviewed input.
- `audit_hydraulics_sensitivity.py`: 25 arithmetic checks cover the extended sensitivity example in each of the 20 courses.
- All author Python files compile. Every misconception is phrased as an intentionally false belief, as required by the generated quiz distractor.
- Rounded hand calculations corrected during author review include b243 slope ratio, b244 conjugate depth, b245 flight time, b247 long-weir discharge, b248 orifice flow, b251 gate discharge and b253 Shields number. The final inputs and audit hashes contain the corrections.

These are author numerical recomputations, not an independent peer certification or a field design approval. Assumptions and physical boundaries remain in each mechanism and model. Main examples use hypothetical dimensions, loads, concentrations and efficiencies; a publicly reported dam height is never silently substituted as net operating head.

## Source and claim limits

Every course includes 3–5 primary sources with per-source scope. `research_hydraulics.json` maps each course to sources and includes claims/URLs. Official source catalogs or indexed passages are explicitly identified when PDF size limits, HTTP 403, timeouts or EPFL 429 responses prevented full retrieval. Full-text access is not claimed for those sources.

The five named dams have separate case histories, map reference points, publication/project timelines and public facts:

- Aswan: ministry-indexed rockfill type, 111 m above riverbed and 15 January 1971 inauguration. Conflicting official length descriptions are omitted.
- Tarbela: owner-reported 143 m above riverbed; owner/World Bank 1976 original completion, 1986 original project audit and 2012 fourth-extension approval are distinct. Inconsistent early unit-count arithmetic in the factsheet is excluded.
- Kariba: 1956–1959 construction, 1958 impoundment monitoring and 2015 rehabilitation financing are distinguished. Old prospective completion dates are not current completion claims.
- Akosombo: rockfill type, 1961–1965 construction and owner-listed 1,020 MW are retained. Conflicting heights (111/141 m) and crest lengths (640/660 m) are excluded.
- Grande Dixence: owner-reported 285 m gravity dam, 1951–1961 construction and commissioning from 1961; Cleuson and later scheme phases are kept separate.

Technique-course landmarks are explicit comparisons. Millsite suction dredging is a **proposed** application, Muddy Creek is an RSEM scenario, and Rudbar-Lorestan is a venting-model investigation. None is asserted to be a completed construction contract. Vendors are relevant public institutions or the waterstop manufacturer Sika, with no contractor attribution. All security fields remain null because listings were not verified.

## Rebuild

```bash
python3 tools/water-v15/build_hydraulics.py
python3 tools/water-v15/validate_input.py tools/water-v15/inputs/b21[0-4].json tools/water-v15/inputs/b24[1-9].json tools/water-v15/inputs/b25[0-5].json
python3 tools/water-v15/audit_hydraulics.py
python3 tools/water-v15/audit_hydraulics_sensitivity.py
```

The helper only writes the 20 IDs present in its authored row files. It does not modify the app, public generated data, external services or deployment state.
