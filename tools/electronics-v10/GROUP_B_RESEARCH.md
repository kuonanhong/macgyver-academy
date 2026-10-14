# V10 electronics group B: a236–a268

33 original bilingual courses, each with 4 stages, 24 steps, 12 distinct technical units paired with model construction and counter-evidence review. All 792 step titles are unique. Each step has 3 knowledge items and a 3-option quiz. This is an educational decomposition and offline engineering interpretation, not 792 validated factory or field operations.

Rebuild from this directory or repository root:

```sh
python tools/electronics-v10/build_group_b.py
```

The builder reads its authored `group_b_specs.py`, `group_b_metadata.py` and two immutable title-only snapshots. It never reads mutable course counters, the current featured dataset or learner progress. Output is `group_b.json`. Integration is the root agent’s responsibility.

## Evidence and authorship

- Primary references were searched/read on 2026-10-14: NREL/DTU reference turbines and collection research; DOE/Sandia storage chapters; EMEC site/history; TI BMS, current sensing, observers, motor control, LLC, PSFB, DAB and PFC; ABB wind/shore/electrolysis/motors; Eaton UPS/supercapacitors; Renishaw encoders; SKF magnetic bearings; Microchip SR motors; Kollmorgen linear motors; Voith pumped hydro; Sumitomo flow batteries; Orbital tidal technology.
- All prose, teaching calculations, comparison tasks and diagram labels are original. References provide technical context; no vendor images, figures, transcripts or large passages are copied by this group.
- Worked examples use explicit hypothetical assumptions and stated units/model boundaries. They are not manufacturer settings, real measurements or unrestricted design claims.
- Site coordinates are approximate campus/area context, clearly labeled as such. Public addresses and two bilingual historical/context entries are included for every course. Locations are not claims that each technology was invented/manufactured there.
- Vendor hints identify specific engineering roles and official product/document URLs, not endorsement. Optional ticker identifiers are identifiers only; no quote, return or freshness claim is made here.
- Some vendor portals may require login for particular downloads. Link-only source reuse grants no image republication rights.
- Old nrel.gov PDFs were replaced with functioning official NLR research landing pages when direct PDF retrieval failed, preserving report identity instead of guessing download paths.

## Review results

Independent technical review checked all 33 courses and their numerical examples. Corrections applied: explicit voltage-aligned d-axis for unity-PF q≈0, positive flywheel rundown loss `P_loss = −Jω dω/dt`, and safe `abs(Id)` DSL notation. DAB quantities are referred to the primary and phase is in radians; LLC and SRM approximations state limits; motor dq power/current conventions are explicit.

Local verification checked exact 33-course range, 792 unique step IDs, 792 unique bilingual step titles, 2,376 knowledge items, bilingual required fields, 3-option quizzes, source ID resolution, 33 locations and 66 related-course links with 3 bilingual practice items each. Rebuilding twice produced identical JSON bytes. No deployment, git commit, public-data mutation or merchant action was performed by this group.
