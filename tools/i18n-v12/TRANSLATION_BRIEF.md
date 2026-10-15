# V12 UI translation brief

You translate the **interface strings** of 馬蓋先 MacGyver Engineering Academy, an
engineering-education website (apprentices learn from a "mentor" through guided,
step-by-step courses with an interactive workbench, quizzes, maps, sources,
memberships and stock information about related companies).

* Source strings: `tools/optics-v12/../i18n-v12/ui_keys.json` → i.e. `/home/claude/work/v12/tools/i18n-v12/ui_keys.json` (824 English strings; the list is the key set).
* Output per language: `/home/claude/work/v12/public/academy/i18n/<code>.json`
  ```json
  {"lang": "<code>", "name": "<language name in that language>", "version": 12, "strings": {"<English key>": "<translation>", ...}}
  ```
* Validate: `cd /home/claude/work/v12 && python3 -I tools/i18n-v12/validate_i18n.py <code>` must print OK.

## Rules
1. Translate every key; keep the English key exactly as given (it is the lookup key).
2. `{n}` is a number placeholder — keep it exactly (same count). Keep symbols such as `×`, `→`, `/`, `·`, `%`, `+`, `↓`, `✳`, emoji and keyboard names (Space, Shift, Esc, WASD, I/K, J/L, PageUp) unchanged.
3. Keep product / brand / standard names untranslated: MacGyver, Google Maps, TradingView, PayPal, ECPay, Supabase, GitHub, YouTube, Holo Artisan, CPU, GPU, TPU, HVDC, PCB, MEMS, EUV, SPC, JSON, CSV, AI (you may use the local abbreviation for AI if standard).
4. ALL-CAPS English labels (e.g. `STACK`, `MEMBERS`, `TU / UNDERGROUND`) are small eyebrow labels: translate them; use upper case only where the script has case.
5. Consistent glossary — choose natural, professional terms and use them consistently:
   mentor (師傅, the teaching master), apprentice (學徒), guided course, step, stage / section / phase, workbench / workshop, knowledge check, evidence, learning pass (paid membership period), learning map, engineering atlas, sources, sign in, register, username, password, mobile number, checkout.
6. Tone: concise, professional, friendly; formal register where the language distinguishes (e.g. Sie in German, vous in French, 您 is not needed for zh-CN — use 你 consistently).
7. Do not add explanations, quotes or markup. Output valid UTF-8 JSON.
8. Work efficiently: generate the JSON with a short python3 script per language (write the translations as a Python dict literal in 2–4 chunks if large, merge, then json.dump with ensure_ascii=False). Never leave English text in place except for rule 3 names and codes.
