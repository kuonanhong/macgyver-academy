# V12 UI translation — delta pass (68 new interface strings)

Same rules as `tools/i18n-v12/TRANSLATION_BRIEF.md` (read it first: glossary, placeholders, brand names, register).

* Source keys: `/home/claude/work/v12/tools/i18n-v12/delta/keys.json` (68 English strings; the list is the key set).
* Output per language: `/home/claude/work/v12/tools/i18n-v12/delta/<code>.json`
  ```json
  {"lang": "<code>", "version": 12, "strings": {"<English key>": "<translation>", ...}}
  ```
* Validate: `cd /home/claude/work/v12 && python3 -I tools/i18n-v12/validate_delta.py <code>` must print OK.
* For consistency, look up how the main dictionary `/home/claude/work/v12/public/academy/i18n/<code>.json`
  (if it exists) already translates related terms: "learning pass", "guided course", "mentor", "sign in", "subdiscipline", "learning map".
* Keys ending with ":" must keep a colon (or the language's colon) at the end; the value is followed by a name/date.
* ALL-CAPS keys are small eyebrow labels (keep upper case where the script has case). "·" separators stay.
* Do NOT edit any other file. Use your own scratch folder (given in your task) for helper scripts.
* Work efficiently: one short python3 script per language writing a dict literal and json.dump(ensure_ascii=False, indent=1).
