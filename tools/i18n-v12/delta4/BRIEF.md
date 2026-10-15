# V13 UI translation — delta4 (36 new interface strings: Bridges & Buildings collection, pricing note)

Same rules as `tools/i18n-v12/TRANSLATION_BRIEF.md` (read it first: glossary, placeholders, brand names, register).

* Source keys: `tools/i18n-v12/delta4/keys.json` (the list is the key set).
* Output per language: `tools/i18n-v12/delta4/<code>.json`
  ```json
  {"lang": "<code>", "version": 13, "strings": {"<English key>": "<translation>", ...}}
  ```
* Validate: `python3 -I tools/i18n-v12/validate_delta.py --set delta4 <code>` must print OK.
* Reuse the main dictionary's terminology (`public/academy/i18n/<code>.json` + earlier `tools/i18n-v12/delta*/<code>.json`):
  "guided course", "subdiscipline", "learning map", "learning pass", "stage/section", "verification".
* Civil-engineering terms must be the normal professional words of the language: suspension bridge, cable-stayed bridge,
  stay cable, main cable, viaduct, sea crossing, bearing, expansion joint, outrigger, diagrid, damper, differential
  shortening, long-span roof, curtain wall / façade, precast, base isolation, code (= design code / building standard).
* Keep proper names as the language normally writes them (Akashi Kaikyō Bridge, Millau Viaduct, Taipei 101, Burj Khalifa,
  Sydney Opera House, Shanghai Tower). Keep "TWD" and the numbers (5, 40, 100, {n}) unchanged.
* "BRIDGES × BUILDINGS" is an ALL-CAPS eyebrow label: keep upper case where the script has case, keep "×".
* Do NOT edit any other file.
