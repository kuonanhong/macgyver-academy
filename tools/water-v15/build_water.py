#!/usr/bin/env python3
"""Build the V15 water and coastal engineering (水利與海岸工程) curricula from authored inputs.

Each authored input (tools/water-v15/inputs/<id>.json) holds ten technical
"units". Every unit becomes four learning steps, so a course has 5 stages x 8
steps = 40 steps:

  A. mechanism and load path        (unit.mechanism + unit.misconception)
  B. quantitative estimate          (unit.model)
  C. testing and verification       (unit.verify + unit.practice)
  D. failure diagnosis              (unit.failure)

`three-gorges`, `b202` and `b226` are existing guided courses: their old
stages/steps/IDs stay untouched and the 40 new steps are appended as five new
stages. Course-level facts, timeline, codes and landmarks become an engineering
dossier guide and place-history milestones during integration.

Output: tools/water-v15/water.json. Run tools/integrate-water-v15.py
afterwards to merge it into public/academy/data.

Usage: python3 -I tools/water-v15/build_water.py [--allow-missing]
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = ROOT / 'public/academy/data'
INPUTS = HERE / 'inputs'
OUT = HERE / 'water.json'
EDITION = 15
TAG = f'-v{EDITION}-'
UNITS = 10
ACCESSED = '2026-10-21'

STAGES = [
    ('水文條件、邊界與工程系統', 'Hydrology, boundaries and engineering system'),
    ('水力機制、材料與定量模型', 'Hydraulics, materials and quantitative models'),
    ('施工方法與施工階段控制', 'Construction methods and stage control'),
    ('試驗、量測與監測驗證', 'Testing, measurement and monitoring'),
    ('耐久、維護與工程交接', 'Durability, maintenance and engineering handoff'),
]

WRONG_METHOD = [
    ('只看一次讀值或外觀即可判定合格，不需要基準點、參考試體或重複量測。',
     'A single reading or a visual impression is enough to accept the work; no datum, reference specimen or repeat measurement is needed.'),
    ('沿用另一處水工設施或流域的量測結果，就可視為本工程已完成驗證。',
     'Reusing results from another hydraulic structure or catchment counts as verifying this structure.'),
    ('量測時不必記錄溫度、水頭、水位歷程與施工荷重，因為它們不會影響結果。',
     'Temperature, water head, water-level history and construction loads need not be recorded because they cannot affect the result.'),
    ('只要結構分析模型看起來合理，就可以省略現場量測與試驗。',
     'If the structural model looks reasonable, site measurement and testing can be skipped.'),
    ('允收準則可以等看到量測數據後再決定。',
     'Acceptance criteria can be decided after the measured data have been seen.'),
    ('不確定度太難估計，報告中只寫最佳值即可。',
     'Uncertainty is too hard to estimate, so the report may state only the best value.'),
]
WRONG_DIAG = [
    ('先更換最貴的構件；只要症狀消失，就代表已找到根因。',
     'Replace the most expensive component first; if the symptom disappears, the root cause has been found.'),
    ('裂縫或異常只出現一次就可以忽略，不需要記錄或追蹤。',
     'A crack or anomaly that appears only once can be ignored without logging or follow-up.'),
    ('補一層塗料或放寬允收值，就能解決大多數劣化問題。',
     'Adding a coat of paint or widening the acceptance limits solves most deterioration problems.'),
    ('所有異常都來自施工人員失誤，設計與細部不需要檢討。',
     'Every anomaly is a workmanship error, so design and detailing never need review.'),
    ('只要結構還沒倒，就代表安全餘裕仍然足夠。',
     'As long as the structure is still standing, its safety margin must still be adequate.'),
    ('症狀相同就代表原因相同，不必用量測區分。',
     'Identical symptoms always mean identical causes, so no discriminating measurement is needed.'),
]

COURSE_SCOPE = ('依公開工程原理、官方資料與規範架構編寫的原創教學；步驟是可驗證的學習任務與假想算例，'
                '不是設計圖說、施工計畫、開挖、注漿或受限空間作業許可，也不是任何專案的設計文件。數值均為教學假設或公開資料，'
                '實際工程須由合格技師依規範與實測資料重新計算並簽證。')
COURSE_SCOPE_EN = ('Original teaching built from public engineering principles, official sources and code frameworks. '
                   'Steps are verifiable learning tasks and hypothetical exercises, not design drawings, method statements, '
                   'excavation, grouting or confined-space permits, or any project\'s design documents. Numbers are teaching assumptions or '
                   'public data; real work must be recalculated and certified by qualified engineers using codes and measured data.')
COORD_SCOPE = ('人工選定的公開地標、設施或研究機構之近似代表座標；非施工入口、構件位置或參訪許可。'
               '研究機構或地標可能被多門課共用。')
COORD_SCOPE_EN = ('Manually selected approximate public landmark, facility or research-institution reference; not a site '
                  'entrance, member location or visit permit. Institutions or landmarks may be shared by several courses.')


def split(value: str) -> tuple[str, str]:
    zh, en = value.split('~', 1)
    return zh.strip(), en.strip()


ZH_SENT = re.compile(r'(?<=[。！？])')
EN_SENT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9(“"‘])')


def sentences_zh(text: str) -> list[str]:
    return [s.strip() for s in ZH_SENT.split(text) if s.strip()]


def sentences_en(text: str) -> list[str]:
    out, buf = [], ''
    for part in EN_SENT.split(text):
        part = part.strip()
        if not part:
            continue
        buf = f'{buf} {part}' if buf else part
        if re.search(r'\b(e\.g|i\.e|vs|approx|Fig|No|Dr|St|Mt|Eq|ca)\.$', buf):
            continue
        out.append(buf)
        buf = ''
    if buf:
        out.append(buf)
    return out


def first(text: str, zh: bool) -> str:
    parts = sentences_zh(text) if zh else sentences_en(text)
    return parts[0] if parts else text


def last(text: str, zh: bool) -> str:
    parts = sentences_zh(text) if zh else sentences_en(text)
    return parts[-1] if parts else text


def lead(text: str, zh: bool, count: int = 2) -> str:
    parts = sentences_zh(text) if zh else sentences_en(text)
    return ('' if zh else ' ').join(parts[:count]) if parts else text


def lower_first(text: str) -> str:
    if not text or text[:2].isupper() or not text[:1].isalpha():
        return text
    word = re.match(r'[A-Za-z]+', text)
    if word and len(word.group(0)) > 1 and word.group(0)[1:].islower():
        return text[:1].lower() + text[1:]
    return text


def clause(text: str, zh: bool, limit: int = 80) -> str:
    """Shorten a quiz option to its first clause when the sentence is long."""
    sep = '；' if zh else '; '
    if len(text) > (limit if zh else limit * 2) and sep in text:
        head = text.split(sep, 1)[0].rstrip('，,:： ')
        return head + ('。' if zh and not head.endswith('。') else ('' if zh or head.endswith('.') else '.'))
    return text


def quiz(correct: tuple[str, str], wrong: list[tuple[str, str]], position: int,
         question: tuple[str, str], explanation: tuple[str, str]) -> dict:
    options = [w for w in wrong if w[0] != correct[0]][:2]
    assert len(options) == 2, question
    options.insert(position % 3, correct)
    zh = [o[0] for o in options]
    en = [o[1] for o in options]
    assert len(set(zh)) == 3 and len(set(en)) == 3, (question, zh)
    return {
        'question': question[0], 'questionEn': question[1],
        'options': zh, 'optionsEn': en, 'answer': position % 3,
        'explanation': explanation[0], 'explanationEn': explanation[1],
    }


def slug(text: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return s[:48] or hashlib.sha256(text.encode()).hexdigest()[:10]


def load_inputs(targets: dict) -> dict:
    found = {}
    for path in sorted(INPUTS.glob('*.json')):
        d = json.loads(path.read_text('utf-8'))
        if d.get('id') in targets:
            found[d['id']] = d
    return found


def build_course(d: dict, existing: dict | None, src_ids: list[str]) -> dict:
    cid = d['id']
    title_zh, title_en = split(d['title'])
    units = []
    for u in d['units']:
        units.append({k: split(u[k]) for k in ('anchor', 'title', 'mechanism', 'model', 'verify', 'failure', 'misconception', 'practice')})
    assert len(units) == UNITS, cid
    mis = [u['misconception'] for u in units]
    steps_by_stage: list[list[dict]] = [[] for _ in STAGES]
    prefix = f'{cid}-v{EDITION}'
    previous = None
    if existing:
        old = [s for st in existing['stages'] for s in st['steps']]
        previous = old[-1]['id'] if old else None
    seq = 0
    for i, u in enumerate(units):
        stage_index = i // 2
        tz, te = u['title']
        az, ae = u['anchor']
        mz, me = u['mechanism']
        qz, qe = u['model']
        vz, ve = u['verify']
        fz, fe = u['failure']
        xz, xe = u['misconception']
        pz, pe = u['practice']
        other = [mis[(i + k) % UNITS] for k in (1, 3, 5, 7)]

        def step(kind: int, title, objective, instruction, observation, failure, check, knowledge, q, minutes):
            nonlocal seq, previous
            seq += 1
            sid = f'{prefix}-{seq:02d}'
            k1, k2 = knowledge
            rec = {
                'id': sid, 'title': title[0], 'titleEn': title[1],
                'estimatedMinutes': minutes, 'simulationOnly': True,
                'sourceIds': src_ids, 'prerequisiteIds': [previous] if previous else [],
                'objective': objective[0], 'objectiveEn': objective[1],
                'instruction': instruction[0], 'instructionEn': instruction[1],
                'observation': observation[0], 'observationEn': observation[1],
                'failure': failure[0], 'failureEn': failure[1],
                'check': check[0], 'checkEn': check[1],
                'knowledge': [
                    {'id': f'{sid}-k1', 'title': k1[0], 'titleEn': k1[1], 'text': k1[2], 'textEn': k1[3], 'sourceIds': src_ids},
                    {'id': f'{sid}-k2', 'title': k2[0], 'titleEn': k2[1], 'text': k2[2], 'textEn': k2[3], 'sourceIds': src_ids},
                ],
                'quiz': q,
                'unit': i + 1, 'unitFacet': ['mechanism', 'model', 'verification', 'failure'][kind],
            }
            previous = sid
            steps_by_stage[stage_index].append(rec)

        # A — mechanism and load path
        step(0,
             (f'{tz}：機制與系統路徑', f'{te}: mechanism and system paths'),
             (f'說明「{az}」如何影響{title_zh}的受力、變形、水流或訊號表現，並畫出相關輸入、傳遞路徑與邊界。',
              f'Explain how “{ae}” governs forces, deformation, flow or signals in “{title_en}”, and map the relevant inputs, transfer paths and boundaries.'),
             (mz + ' 師傅任務：以自由體圖、流路圖或訊號圖畫出相關物理量如何經過「' + az + '」傳到系統邊界，標出哪些量由設計決定、哪些由材料、施工或環境決定，再用三句話寫出機制摘要。',
              me + f' Mentor task: draw a free-body, flow or signal diagram showing how relevant physical quantities pass through “{ae}” to the system boundary, mark which quantities are fixed by design and which by materials, construction or environment, then summarise the mechanism in three sentences.'),
             ('量級提示：' + first(qz, True), 'Order-of-magnitude cue: ' + first(qe, False)),
             ('常見誤解：「' + xz + '」這個說法忽略了上述機制；請在系統圖上指出它錯在哪一個環節。',
              f'Common misconception: "{xe}" It ignores the mechanism above; mark on your system diagram where it breaks down.'),
             (f'系統圖標明「{az}」的輸入、傳遞路徑與邊界；三句摘要能解釋本步列出的誤解為何不成立。',
              f'The system diagram shows inputs, transfer paths and boundaries for “{ae}”; the three-sentence summary explains why the listed misconception fails.'),
             ((tz, te, lead(mz, True), lead(me, False)),
              ('誤解辨析', 'Misconception check', '誤解：' + xz + ' 正確的工程判斷必須回到傳力機制與量級。',
               'Misconception: ' + xe + ' Sound engineering judgement goes back to the load path and magnitude.')),
             quiz((clause(first(mz, True), True), clause(first(me, False), False)), [(xz, xe), other[0]], seq + 1,
                  (f'關於「{tz}」，下列哪一項敘述正確？', f'Which statement about "{te}" is correct?'),
                  (first(mz, True) + ' 其餘選項是常見誤解。', first(me, False) + ' The other options are common misconceptions.')),
             20)
        # B — quantitative estimate
        step(1,
             (f'{tz}：定量估算', f'{te}: quantitative estimate'),
             (f'以數值模型估算「{az}」的關鍵量，並判斷幾何、水頭、荷載或材料參數改變時結果的方向與幅度。',
              f'Estimate the key quantities of “{ae}” with a numerical model and judge the direction and size of change when geometry, water head, load or material parameters move.'),
             ('依下列模型逐步重算：' + qz + ' 師傅任務：保留單位重算一次，再只改變一個輸入（例如增加 10%），預測並計算輸出的變化，說明它是線性、平方或更高次方的關係，並指出規範或設計上通常如何處理這個敏感度。',
              'Recalculate step by step: ' + qe + ' Mentor task: redo the calculation keeping units, then change one input (for example by +10%), predict and compute the output change, state whether the dependence is linear, quadratic or steeper, and note how codes or designers usually handle this sensitivity.'),
             ('如何核對：' + first(vz, True), 'How to cross-check: ' + first(ve, False)),
             ('計算陷阱：單位換算錯誤、把教學假設當成真實設計值、混淆標稱值與設計值（未乘載重或強度係數），或只看結果不檢查數量級，都會讓後續設計判斷失準。',
              'Calculation traps: unit slips, treating teaching assumptions as real design values, mixing nominal and factored values, or accepting a result without checking its magnitude will mislead later design decisions.'),
             ('依模型顯示精度重現數值，列出單位與取整方式，並提交一個參數改變後的敏感度計算與工程解釋。',
              'Reproduce the model values to their displayed precision, state units and rounding, and submit a sensitivity calculation for one changed parameter with an engineering explanation.'),
             (('定量模型', 'Quantitative model', qz, qe),
              ('模型邊界', 'Model boundary', '本步數值為教學假設或公開資料的簡化；套用到實際工程前，必須依規範荷載組合、材料試驗與現場量測重新計算並由技師簽證。',
               'These numbers are teaching assumptions or simplified public data; before applying them to a real structure, recalculate with code load combinations, material tests and site measurements, certified by a qualified engineer.')),
             quiz((clause(first(qz, True), True), clause(first(qe, False), False)), [other[1], other[2]], seq + 1,
                  (f'依「{tz}」的定量模型，下列哪一項敘述成立？', f'According to the quantitative model for "{te}", which statement holds?'),
                  (first(qz, True) + ' 重算時請保留單位。', first(qe, False) + ' Keep units when recalculating.')),
             30)
        # C — testing, measurement and verification
        step(2,
             (f'{tz}：試驗與驗證', f'{te}: testing and verification'),
             (f'設計一項可重複的試驗、量測或檢查，驗證「{az}」是否符合模型與規範預期，並在量測前訂出允收準則與停工點。',
              f'Design a repeatable test, measurement or inspection that verifies whether “{ae}” meets the model and code expectation, fixing acceptance criteria and hold points before measuring.'),
             (vz + ' 師傅任務：把上述方法寫成試驗或量測計畫，列出儀器與感測器、基準點或參考試體、步驟、比較對象、允收準則與停工點，並估計三項主要不確定度來源。',
              ve + ' Mentor task: turn this into a test or measurement plan listing instruments and sensors, datums or reference specimens, procedure, comparison baseline, acceptance criteria and hold points, and estimate the three largest uncertainty contributions.'),
             ('現場實務：' + pz, 'Site practice: ' + pe),
             ('注意干擾：' + first(fz, True) + ' 只量一次、沒有可追溯的基準，或不記錄溫度、水頭與施工荷重，就無法分辨真正的偏差與量測誤差。',
              'Watch for interference: ' + first(fe, False) + ' A single reading, no traceable datum, or unrecorded temperature, water head and construction loads make real deviations indistinguishable from measurement error.'),
             ('提交試驗或量測計畫：儀器、基準、步驟、允收準則、停工點與不確定度預算，並說明如何判定合格或不合格、由誰簽認。',
              'Submit the test or measurement plan: instruments, datums, procedure, acceptance criteria, hold points and uncertainty budget, with the pass/fail rule and who signs it off.'),
             (('驗證方法', 'Verification method', vz, ve),
              ('現場實務', 'Site practice', pz, pe)),
             quiz((clause(first(vz, True), True), clause(first(ve, False), False)), [WRONG_METHOD[(seq + i) % len(WRONG_METHOD)], other[3]], seq + 1,
                  (f'要驗證「{tz}」，下列哪一個做法最恰當？', f'Which approach best verifies "{te}"?'),
                  (first(vz, True) + ' 驗證需要基準、重複性與事先訂定的允收準則。', first(ve, False) + ' Verification needs a datum, repeatability and acceptance criteria fixed in advance.')),
             25)
        # D — failure diagnosis
        step(3,
             (f'{tz}：失效診斷', f'{te}: failure diagnosis'),
             (f'從症狀倒推「{az}」的失效或劣化原因，提出能區分原因的檢查、矯正與預防措施。',
              f'Work back from symptoms to the failure or deterioration causes of “{ae}” and propose discriminating checks, corrective actions and prevention.'),
             (fz + ' 師傅任務：建立失效樹——症狀、兩個以上可能原因、能區分它們的量測或檢測，以及矯正與預防措施；並說明此失效如何影響整體結構的安全、使用性、耐久或營運。',
              fe + ' Mentor task: build a fault tree with the symptom, at least two candidate causes, a measurement or inspection that tells them apart, and corrective and preventive actions; explain how the failure affects whole-structure safety, serviceability, durability or operation.'),
             ('連結機制：' + last(mz, True), 'Link to the mechanism: ' + last(me, False)),
             ('誤判風險：若相信「' + xz + '」，上述症狀可能被錯誤處理而反覆出現。',
              f'Misdiagnosis risk: believing "{xe}" leads to mishandling the symptom so it keeps returning.'),
             ('完成失效樹與矯正措施，指出哪一項量測或檢測能最快確認根因、需要哪些人簽認，以及如何防止再發。',
              'Complete the fault tree and corrective actions, name the measurement or inspection that confirms the root cause fastest, who must sign off, and how recurrence is prevented.'),
             (('失效模式', 'Failure mode', fz, fe),
              ('根因確認', 'Root-cause confirmation', '根因必須以可區分的量測或檢測確認；只補強外觀、更換構件或放寬允收值可能掩蓋問題。',
               'Confirm the root cause with a discriminating measurement or inspection; cosmetic repair, swapping components or relaxing limits can mask the problem.')),
             quiz((clause(first(fz, True), True), clause(first(fe, False), False)), [WRONG_DIAG[(seq + i) % len(WRONG_DIAG)], other[0]], seq + 1,
                  (f'在「{tz}」出現異常時，下列哪一項判斷最合理？', f'When "{te}" shows distress, which diagnosis is most reasonable?'),
                  (first(fz, True) + ' 需以量測區分可能原因。', first(fe, False) + ' Discriminate candidate causes by measurement.')),
             25)

    stages = []
    for si, (sz, se) in enumerate(STAGES):
        u1, u2 = units[si * 2], units[si * 2 + 1]
        stages.append({
            'id': f'{prefix}-s{si + 1}', 'title': sz, 'titleEn': se,
            'description': f'本階段聚焦「{u1["title"][0]}」與「{u2["title"][0]}」：先建立機制、系統路徑與定量模型，再設計試驗驗證並診斷失效。',
            'descriptionEn': f'This stage covers "{u1["title"][1]}" and "{u2["title"][1]}": establish the mechanism, system paths and quantitative model first, then design verification and diagnose failures.',
            'steps': steps_by_stage[si],
        })
    return {'stages': stages, 'units': units}


def dossier(d: dict) -> dict:
    """Bilingual fact sheet: facts, timeline, codes and landmark projects."""
    facts = [split(x) for x in d['facts']]
    codes = [split(x) for x in d['codes']]
    marks = [split(x) for x in d['landmarks']]
    timeline = [(m['year'].strip(), *split(m['event'])) for m in d['timeline']]
    return {
        'facts': [f[0] for f in facts], 'factsEn': [f[1] for f in facts],
        'timeline': [f'{y}　{z}' for y, z, _ in timeline], 'timelineEn': [f'{y} — {e}' for y, _, e in timeline],
        'codes': [c[0] for c in codes], 'codesEn': [c[1] for c in codes],
        'landmarks': [m[0] for m in marks], 'landmarksEn': [m[1] for m in marks],
        'milestones': [{'year': y, 'text': z, 'textEn': e} for y, z, e in timeline],
    }


def visual_family(cid: str) -> str:
    n = 201 if cid == 'three-gorges' else int(cid[1:])
    if n <= 220 or 231 <= n <= 240: return 'water-dam'
    if 226 <= n <= 229 or 292 <= n <= 294: return 'water-lock'
    if n <= 230: return 'water-gate'
    if n <= 260: return 'water-hydraulic'
    if n <= 268: return 'water-pipe'
    if n <= 280: return 'water-river'
    if n <= 288: return 'water-coast'
    if n <= 294: return 'water-port'
    return 'water-ecology'


def main() -> int:
    targets = {t['id']: t for t in json.loads((HERE / 'targets.json').read_text('utf-8'))}
    inputs = load_inputs(targets)
    missing = sorted(set(targets) - set(inputs))
    if missing:
        print('Missing authored inputs:', ' '.join(missing))
        if '--allow-missing' not in sys.argv:
            return 1
    featured = {c['id']: c for c in json.loads((DATA / 'featured.json').read_text('utf-8'))}
    sources = json.loads((DATA / 'sources.json').read_text('utf-8'))
    by_url = {s['url'].rstrip('/'): s['id'] for s in sources if not s['id'].startswith(f'v{EDITION}s-')}
    known_ids = {s['id'] for s in sources if not s['id'].startswith(f'v{EDITION}s-')}

    out_sources, out_courses, out_places, out_related = [], [], [], []
    companies: dict[str, dict] = {}
    associations: dict[str, list] = {}
    built: dict[str, dict] = {}

    for cid in [t for t in targets if t in inputs]:
        d, target = inputs[cid], targets[cid]
        title_zh, title_en = split(d['title'])
        assert (title_zh, title_en) == (target['title'], target['titleEn']), cid
        src_ids = []
        for s in d['sources']:
            url = s['url'].strip()
            sid = by_url.get(url.rstrip('/'))
            if not sid:
                sid = f'v{EDITION}s-' + s['key']
                n = 2
                while sid in known_ids:
                    sid = f"v{EDITION}s-{s['key']}-{n}"; n += 1
                known_ids.add(sid); by_url[url.rstrip('/')] = sid
                out_sources.append({
                    'id': sid, 'title': s['title'], 'titleEn': s['titleEn'], 'publisher': s['publisher'],
                    'url': url, 'sourceType': s['sourceType'], 'scope': s['scope'], 'scopeEn': s['scopeEn'],
                    'accessed': ACCESSED, 'imageReuse': 'Link only. No source image or article reproduction.',
                })
            src_ids.append(sid)
        src_ids = list(dict.fromkeys(src_ids))
        existing = featured.get(cid) if target.get('mode') == 'extend-existing' else None
        if existing:  # ignore V15 stages from a previous integration run
            existing = {**existing, 'stages': [st for st in existing['stages'] if TAG not in st['id']], 'sourceIds': [sid for sid in existing.get('sourceIds', []) if not sid.startswith(f'v{EDITION}s-') and sid not in src_ids]}
        result = build_course(d, existing, src_ids)
        book = dossier(d)
        built[cid] = {'input': d, 'units': result['units'], 'sourceIds': src_ids}
        nodes = [list(n) for n in d['architectureNodes']]
        edges = [list(e) for e in d['architectureEdges']]
        sz, se = split(d['summary'])
        fz, fe = split(d['focus'])
        ez, ee = split(d['example'])
        hz, he = split(d['history'])
        course = {
            'id': cid, 'title': title_zh, 'titleEn': title_en, 'category': 'water',
            'kind': 'course', 'status': 'guided', 'contentStatus': 'reviewable-educational-curriculum',
            'summary': sz, 'summaryEn': se, 'focus': fz, 'focusEn': fe,
            'scope': COURSE_SCOPE, 'scopeEn': COURSE_SCOPE_EN,
            'subcategory': target['discipline'], 'subcategoryTitle': target['disciplineTitle'],
            'subcategoryTitleEn': target['disciplineTitleEn'],
            'learningTrack': 'water', 'learningSubdiscipline': target['discipline'],
            'learningTags': ['water', target['discipline'], d['family']],
            'architectureFamily': visual_family(cid), 'architectureNodes': nodes, 'architectureEdges': edges,
            'diagram': {'type': visual_family(cid), 'labels': [n[0] for n in nodes[:5]], 'labelsEn': [n[1] for n in nodes[:5]], 'original': True, 'notToScale': True},
            'workedExample': {
                'title': '原創假想算例與邊界', 'titleEn': 'Original hypothetical example and boundaries',
                'text': ez, 'textEn': ee,
                'assumptions': '數值是本課自行設定的教學假設，不代表任何專案的設計值、量測值或規範允許值；改變系統邊界或荷載組合後必須重算。',
                'assumptionsEn': 'Inputs are teaching assumptions, not any project\'s design values, measurements or code allowances; recalculate after changing the system boundary or load combination.',
                'sourceScope': '原創數值練習；來源支援公開原理與工程背景，不宣稱來源提供這組數據。',
                'sourceScopeEn': 'Original numerical exercise; sources support public principles and project context, not these numbers.',
            },
            'dossier': {k: v for k, v in book.items() if k != 'milestones'},
            'depth': 5, 'languageCoverage': ['zh-TW', 'en'], 'simulationOnly': True,
            'educationEdition': EDITION, 'enrichmentVersion': EDITION,
        }
        if existing:
            course['extendsExisting'] = True
            course['existingStepCount'] = sum(len(st['steps']) for st in existing['stages'])
            course['newStages'] = result['stages']
            course['sourceIds'] = list(dict.fromkeys((existing.get('sourceIds') or []) + src_ids))
        else:
            course['stages'] = result['stages']
            course['sourceIds'] = src_ids
            course['curriculumVersion'] = EDITION
        out_courses.append(course)

        pz, pe = split(d['place']['name'])
        cz, ce = split(d['place']['country'])
        u = result['units']
        milestones = [{'year': m['year'], 'title': title_zh, 'titleEn': title_en, 'text': m['text'], 'textEn': m['textEn'],
                       'sourceIds': src_ids} for m in book['milestones']]
        out_places.append({
            'courseId': cid, 'extendsExisting': bool(existing),
            'place': {'name': pz, 'nameEn': pe, 'city': pz, 'cityEn': pe, 'country': cz, 'countryEn': ce,
                      'lat': round(float(d['place']['lat']), 5), 'lng': round(float(d['place']['lng']), 5),
                      'address': d['place']['query'], 'addressEn': d['place']['query'], 'mapQuery': d['place']['query'],
                      'coordinateScope': COORD_SCOPE, 'coordinateScopeEn': COORD_SCOPE_EN},
            'summary': f'{title_zh}：{fz}。', 'summaryEn': f'{title_en}: {fe}.',
            'connection': f'從「{u[0]["anchor"][0]}」追到「{u[-1]["anchor"][0]}」；地圖提供公開工程的地理脈絡。',
            'connectionEn': f'Trace the structure from “{u[0]["anchor"][1]}” to “{u[-1]["anchor"][1]}”; the map gives public geographic context.',
            'history': [
                {'year': '公開工程脈絡 / Public engineering context', 'title': title_zh, 'titleEn': title_en,
                 'text': hz, 'textEn': he, 'sourceIds': src_ids},
                *milestones,
                {'year': '學習延伸 / Learning transfer', 'title': '從工程史到可驗證模型', 'titleEn': 'From engineering history to verifiable models',
                 'text': f'本課把「{u[0]["title"][0]}」到「{u[-1]["title"][0]}」改寫為 40 個原創分析、試驗與診斷任務；不複製來源圖片、影片逐字稿、設計圖或現場程序。',
                 'textEn': f'The course turns "{u[0]["title"][1]}" through "{u[-1]["title"][1]}" into 40 original analysis, testing and diagnosis tasks without copying source images, video transcripts, drawings or field procedures.',
                 'sourceIds': src_ids},
            ],
            'references': [{'title': s['title'], 'titleEn': s['titleEn'], 'publisher': s['publisher'], 'url': s['url'],
                            'scope': s['scope'], 'scopeEn': s['scopeEn']} for s in d['sources']],
            'sourceIds': src_ids,
        })

        for v in d['vendors']:
            name_en = v['nameEn'].strip()
            sec = v.get('security') or None
            vid = None
            for k, comp in companies.items():
                same_listing = sec and comp.get('security') and (comp['security']['exchange'], comp['security']['symbol']) == (sec['exchange'], sec['symbol'])
                if comp['nameEn'].casefold() == name_en.casefold() or same_listing:
                    vid = k
            if not vid:
                vid = slug(name_en)
                base, n = vid, 2
                while vid in companies and companies[vid]['nameEn'].casefold() != name_en.casefold():
                    vid = f'{base}-{n}'; n += 1
                companies[vid] = {'id': vid, 'name': v['name'], 'nameEn': name_en, 'business': v['business'],
                                  'businessEn': v['businessEn'], 'url': v['url'], 'investorUrl': v.get('investorUrl') or '',
                                  'sourceUrl': v['url'], 'reviewed': ACCESSED, 'security': v.get('security')}
            elif not companies[vid].get('security') and v.get('security'):
                companies[vid]['security'] = v['security']
            if len(v['business']) < len(companies[vid]['business']):
                companies[vid]['business'], companies[vid]['businessEn'] = v['business'], v['businessEn']
            associations.setdefault(cid, []).append({'companyId': vid, 'role': v['role'], 'roleEn': v['roleEn'],
                                                     'business': v['business'], 'businessEn': v['businessEn']})

    # Related comparisons (needs every course built first).
    for cid, b in built.items():
        d = b['input']
        related = []
        for rid in d['related']:
            if rid not in built:
                continue
            other = built[rid]
            oz, oe = split(other['input']['title'])
            ofz, ofe = split(other['input']['focus'])
            fz, fe = split(d['focus'])
            u, w = b['units'], other['units']
            related.append({
                'id': rid, 'title': oz, 'titleEn': oe,
                'transfer': f'可遷移「{u[0]["title"][0]}」與「{u[6]["title"][0]}」的傳力分析、量測與驗證方法；{oz}的跨度、荷載、材料與允收條件需重新設定。',
                'transferEn': f'The load-path analysis, measurement and verification methods of "{u[0]["title"][1]}" and "{u[6]["title"][1]}" transfer, while hydraulic boundaries, loads, materials and acceptance conditions of {oe} must be respecified.',
                'difference': f'本課聚焦{fz}；{oz}則以{ofz}為重點，不能直接沿用參數或允收值。',
                'differenceEn': f'This course focuses on {lower_first(fe)}; {oe} centres on {lower_first(ofe)}, so parameters and acceptance values do not transfer unchanged.',
                'practice': [
                    f'比較系統邊界：列出「{u[0]["anchor"][0]}」與「{w[0]["anchor"][0]}」的荷載來源、傳力路徑與主要環境作用。',
                    f'把本課算例的一個假設移到{oz}，標出可沿用的方程與必須重設的參數。',
                    f'以「{w[6]["title"][0]}」為例，設計一項能區分兩種結構行為的試驗或量測，並註明不確定度與允收準則。',
                ],
                'practiceEn': [
                    f'Compare system boundaries: list the load sources, load paths and main environmental actions of “{u[0]["anchor"][1]}” and “{w[0]["anchor"][1]}”.',
                    f'Move one assumption of this course\'s worked example to {oe}, separating reusable equations from parameters that must be respecified.',
                    f'Using "{w[6]["title"][1]}", design a test or measurement that distinguishes the two structural behaviours and state its uncertainty and acceptance criterion.',
                ],
                'referenceUrls': [s['url'] for s in other['input']['sources']],
            })
        out_related.append({
            'courseId': cid, 'extendsExisting': targets[cid].get('mode') == 'extend-existing',
            'overview': '以可遷移的傳力原理、施工方法與驗證比較相近的水利與海岸設施；關聯不表示同一業主、設計者、年代或規範。',
            'overviewEn': 'Compare neighbouring water and coastal works through transferable load-path principles, construction methods and verification; a link does not imply the same owner, designer, era or code.',
            'related': related,
            'references': list({s['url']: {'title': s['title'], 'titleEn': s['titleEn'], 'publisher': s['publisher'], 'url': s['url'], 'scope': s['scope'], 'scopeEn': s['scopeEn']}
                                for s in d['sources'] + [x for rid in d['related'] if rid in built for x in built[rid]['input']['sources']]}.values()),
        })

    result = {
        'version': EDITION, 'generated': ACCESSED,
        'courses': out_courses, 'sources': out_sources, 'places': out_places, 'related': out_related,
        'companies': list(companies.values()), 'associations': associations,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    steps = sum(len(st['steps']) for c in out_courses for st in (c.get('stages') or c.get('newStages')))
    listed = sum(1 for c in companies.values() if c.get('security'))
    print(json.dumps({'courses': len(out_courses), 'newSteps': steps, 'sources': len(out_sources),
                      'companies': len(companies), 'listed': listed, 'places': len(out_places),
                      'related': len(out_related), 'missing': len(missing)}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
