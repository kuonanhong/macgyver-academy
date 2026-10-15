#!/usr/bin/env python3
"""Build the V12 optics & precision-instrument curricula from authored inputs.

Each authored input (tools/optics-v12/inputs/<id>.json) holds eight technical
"units". Every unit becomes four learning steps, so a course has 4 stages x 8
steps = 32 steps:

  A. mechanism and system boundary   (unit.mechanism + unit.misconception)
  B. quantitative estimate           (unit.model)
  C. measurement and verification    (unit.verify)
  D. failure diagnosis               (unit.failure)

`asml` and `a405` are existing guided courses: their old stages/steps/IDs stay
untouched and the 32 new steps are appended as four new stages.

Output: tools/optics-v12/optics.json (courses, sources, places, related,
vendor companies and course associations). Run tools/integrate-optics-v12.py
afterwards to merge it into public/academy/data.

Usage: python3 -I tools/optics-v12/build_optics.py
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
OUT = HERE / 'optics.json'

STAGES = [
    ('系統邊界與物理原理', 'System boundaries and physical principles'),
    ('元件、材料與製造', 'Components, materials and fabrication'),
    ('量測、校正與誤差預算', 'Measurement, calibration and error budgets'),
    ('系統整合、驗證與工程交接', 'Integration, validation and engineering handoff'),
]

WRONG_METHOD = [
    ('只看單次讀值或外觀即可判定合格，不需要基準件或重複量測。',
     'A single reading or a visual impression is enough to accept the result; no reference artefact or repeat measurement is needed.'),
    ('沿用另一台設備或另一個案例的量測結果，就可視為本系統已完成驗證。',
     'Reusing results from another instrument or another case counts as verifying this system.'),
    ('量測時不必記錄溫度、振動與時間等條件，因為它們不會影響結果。',
     'Temperature, vibration and timing need not be recorded because they cannot affect the result.'),
    ('只要模擬結果看起來合理，就可以省略實體量測與校正。',
     'If the simulation looks reasonable, physical measurement and calibration can be skipped.'),
    ('允收準則可以等看到量測數據後再決定。',
     'Acceptance criteria can be decided after the measured data have been seen.'),
    ('不確定度太難估計，報告中只寫最佳值即可。',
     'Uncertainty is too hard to estimate, so the report may state only the best value.'),
]
WRONG_DIAG = [
    ('先更換最貴的零件；只要症狀消失，就代表已找到根因。',
     'Replace the most expensive part first; if the symptom disappears, the root cause has been found.'),
    ('異常只出現一次就可以忽略，不需要記錄或追蹤。',
     'An anomaly that appears only once can be ignored without logging or follow-up.'),
    ('調高增益或放寬允收值，就能解決大多數異常。',
     'Raising the gain or widening the acceptance limits solves most anomalies.'),
    ('所有異常都來自操作人員失誤，系統設計不需要檢討。',
     'Every anomaly is operator error, so the system design never needs review.'),
    ('只要重新開機或重設軟體，硬體失效也會一併排除。',
     'Restarting or resetting the software also clears hardware failures.'),
    ('症狀相同就代表原因相同，不必用量測區分。',
     'Identical symptoms always mean identical causes, so no discriminating measurement is needed.'),
]

COURSE_SCOPE = ('依公開物理原理與官方資料編寫的原創教學；步驟是可驗證的學習任務與假想算例，'
                '不是原廠配方、施工圖、設備操作許可或安全程序。數值均為教學假設，需依實際規格重算。')
COURSE_SCOPE_EN = ('Original teaching built from public physics and official sources. Steps are verifiable '
                   'learning tasks and hypothetical exercises, not vendor recipes, construction drawings, '
                   'operating authorisation or safety procedures. Numbers are teaching assumptions and must '
                   'be recalculated for real specifications.')
COORD_SCOPE = ('人工選定的公開機構、設施或城市之近似代表座標；非設備定位、施工入口或參訪許可。'
               '研究機構或公司園區可能被多門課共用。')
COORD_SCOPE_EN = ('Manually selected approximate public institution, facility or city reference; not equipment '
                  'coordinates, an access point or a visit permit. Institutions may be shared by several courses.')


def split(value: str) -> tuple[str, str]:
    zh, en = value.split('~', 1)
    return zh.strip(), en.strip()


ZH_SENT = re.compile(r'(?<=[。！？])')
EN_SENT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9(“"])')


def sentences_zh(text: str) -> list[str]:
    return [s.strip() for s in ZH_SENT.split(text) if s.strip()]


def sentences_en(text: str) -> list[str]:
    out, buf = [], ''
    for part in EN_SENT.split(text):
        part = part.strip()
        if not part:
            continue
        # Do not split after common abbreviations.
        if buf:
            buf = buf + ' ' + part
        else:
            buf = part
        if re.search(r'\b(e\.g|i\.e|vs|approx|Fig|No|Dr|St|Mt)\.$', buf):
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


def build_course(d: dict, target: dict, existing: dict | None, src_ids: list[str]) -> dict:
    cid = d['id']
    title_zh, title_en = split(d['title'])
    units = []
    for u in d['units']:
        units.append({k: split(u[k]) for k in ('anchor', 'title', 'mechanism', 'model', 'verify', 'failure', 'misconception')})
    mis = [u['misconception'] for u in units]
    steps_by_stage: list[list[dict]] = [[] for _ in STAGES]
    prefix = f'{cid}-v12'
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
        other = [mis[(i + k) % 8] for k in (1, 3, 5, 6)]

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

        # A — mechanism and boundary
        step(0,
             (f'{tz}：原理與系統邊界', f'{te}: mechanism and system boundary'),
             (f'說明「{az}」如何決定{title_zh}的關鍵性能，並畫出其輸入、輸出與邊界。',
              f'Explain how “{ae}” determines the key performance of “{title_en}”, and map its inputs, outputs and boundaries.'),
             (mz + ' 師傅任務：以方塊圖畫出能量或訊號通過「' + az + '」的路徑，標出哪些量由設計決定、哪些由環境或製造決定，再用三句話寫出機制摘要。',
              me + f' Mentor task: draw a block diagram of the energy or signal path through “{ae}”, mark which quantities are fixed by design and which by environment or fabrication, then summarise the mechanism in three sentences.'),
             ('量級提示：' + first(qz, True), 'Order-of-magnitude cue: ' + first(qe, False)),
             ('常見誤解：「' + xz + '」這個說法忽略了上述機制；請在方塊圖上指出它錯在哪一個環節。',
              f'Common misconception: "{xe}" It ignores the mechanism above; mark on your block diagram where it breaks down.'),
             (f'方塊圖標明「{az}」的輸入、輸出與邊界；三句摘要能解釋本步列出的誤解為何不成立。',
              f'The block diagram shows inputs, outputs and boundaries of “{ae}”; the three-sentence summary explains why the listed misconception fails.'),
             ((tz, te, lead(mz, True), lead(me, False)),
              ('誤解辨析', 'Misconception check', '誤解：' + xz + ' 正確的工程判斷必須回到機制與量級。',
               'Misconception: ' + xe + ' Sound engineering judgement goes back to mechanism and magnitude.')),
             quiz((clause(first(mz, True), True), clause(first(me, False), False)), [(xz, xe), other[0]], seq + 1,
                  (f'關於「{tz}」，下列哪一項敘述正確？', f'Which statement about "{te}" is correct?'),
                  (first(mz, True) + ' 其餘選項是常見誤解。', first(me, False) + ' The other options are common misconceptions.')),
             20)
        # B — quantitative estimate
        step(1,
             (f'{tz}：定量估算', f'{te}: quantitative estimate'),
             (f'以數值模型估算「{az}」的關鍵量，並判斷參數改變時結果的方向與幅度。',
              f'Estimate the key quantities of “{ae}” with a numerical model and judge the direction and size of changes when a parameter moves.'),
             ('依下列模型逐步重算：' + qz + ' 師傅任務：保留單位重算一次，再只改變一個輸入（例如增加 10%），預測並計算輸出的變化，說明它是線性、平方或更高次方的關係。',
              'Recalculate step by step: ' + qe + ' Mentor task: redo the calculation keeping units, then change one input (for example by +10%), predict and compute the output change, and state whether the dependence is linear, quadratic or steeper.'),
             ('如何核對：' + first(vz, True), 'How to cross-check: ' + first(ve, False)),
             ('計算陷阱：單位換算錯誤、把教學假設當成設備規格，或只看結果不檢查數量級，都會讓後續設計判斷失準。',
              'Calculation traps: unit conversion slips, treating teaching assumptions as equipment specifications, or accepting a result without checking its magnitude will mislead later design decisions.'),
             ('重現模型中的數值（取整誤差在 ±5% 內），並提交一個參數改變後的敏感度計算與物理解釋。',
              'Reproduce the model values (within ±5% rounding) and submit a sensitivity calculation for one changed parameter with a physical explanation.'),
             (('定量模型', 'Quantitative model', qz, qe),
              ('模型邊界', 'Model boundary', '本步數值為教學假設；套用到實際設備前，必須重新取得規格、操作條件與不確定度。',
               'These numbers are teaching assumptions; before applying them to real equipment, obtain the actual specifications, operating conditions and uncertainties.')),
             quiz((clause(first(qz, True), True), clause(first(qe, False), False)), [other[1], other[2]], seq + 1,
                  (f'依「{tz}」的定量模型，下列哪一項敘述成立？', f'According to the quantitative model for "{te}", which statement holds?'),
                  (first(qz, True) + ' 重算時請保留單位。', first(qe, False) + ' Keep units when recalculating.')),
             30)
        # C — measurement and verification
        step(2,
             (f'{tz}：量測與驗證', f'{te}: measurement and verification'),
             (f'設計一項可重複的量測，驗證「{az}」是否符合模型預期，並訂出允收準則。',
              f'Design a repeatable measurement that verifies whether “{ae}” meets the model expectation, and set acceptance criteria.'),
             (vz + ' 師傅任務：把上述方法寫成量測計畫，列出儀器、基準件或參考樣品、步驟、比較對象與允收準則，並估計三項主要不確定度來源。',
              ve + ' Mentor task: turn this into a measurement plan listing instruments, reference artefacts or samples, procedure, comparison baseline and acceptance criteria, and estimate the three largest uncertainty contributions.'),
             ('注意干擾：' + first(fz, True), 'Watch for interference: ' + first(fe, False)),
             ('驗證陷阱：只量一次、沒有可追溯的基準，或不記錄環境條件，就無法分辨真正的偏差與量測誤差。',
              'Verification traps: a single measurement, no traceable reference, or unrecorded environmental conditions make real deviations indistinguishable from measurement error.'),
             ('提交量測計畫：儀器、基準、步驟、允收準則與不確定度預算，並說明如何判定合格或不合格。',
              'Submit the measurement plan: instruments, reference, procedure, acceptance criteria and uncertainty budget, with the pass/fail decision rule.'),
             (('驗證方法', 'Verification method', vz, ve),
              ('允收與不確定度', 'Acceptance and uncertainty', '允收準則必須在量測前訂定，並與擴充不確定度一起陳述；比較基準需可追溯。',
               'Acceptance criteria are fixed before measuring and stated together with expanded uncertainty; the comparison reference must be traceable.')),
             quiz((clause(first(vz, True), True), clause(first(ve, False), False)), [WRONG_METHOD[(seq + i) % len(WRONG_METHOD)], other[3]], seq + 1,
                  (f'要驗證「{tz}」，下列哪一個做法最恰當？', f'Which approach best verifies "{te}"?'),
                  (first(vz, True) + ' 驗證需要基準、重複性與允收準則。', first(ve, False) + ' Verification needs a reference, repeatability and acceptance criteria.')),
             25)
        # D — failure diagnosis
        step(3,
             (f'{tz}：失效診斷', f'{te}: failure diagnosis'),
             (f'從症狀倒推「{az}」的失效原因，提出能區分原因的檢查與矯正措施。',
              f'Work back from symptoms to the failure causes of “{ae}” and propose discriminating checks and corrective actions.'),
             (fz + ' 師傅任務：建立失效樹——症狀、兩個以上可能原因、能區分它們的量測，以及矯正與預防措施；並說明此失效如何影響整個系統的性能、良率或安全。',
              fe + ' Mentor task: build a fault tree with the symptom, at least two candidate causes, a measurement that tells them apart, and corrective and preventive actions; explain how the failure affects whole-system performance, yield or safety.'),
             ('連結機制：' + last(mz, True), 'Link to the mechanism: ' + last(me, False)),
             ('誤判風險：若相信「' + xz + '」，上述症狀可能被錯誤處理而反覆出現。',
              f'Misdiagnosis risk: believing "{xe}" leads to mishandling the symptom so it keeps returning.'),
             ('完成失效樹與矯正措施，並指出哪一項量測能最快確認根因、如何防止再發。',
              'Complete the fault tree and corrective actions, name the measurement that confirms the root cause fastest, and state how recurrence is prevented.'),
             (('失效模式', 'Failure mode', fz, fe),
              ('根因確認', 'Root-cause confirmation', '根因必須以可區分的量測確認；只更換零件或放寬參數可能掩蓋問題。',
               'Confirm the root cause with a discriminating measurement; merely swapping parts or relaxing limits can mask the problem.')),
             quiz((clause(first(fz, True), True), clause(first(fe, False), False)), [WRONG_DIAG[(seq + i) % len(WRONG_DIAG)], other[0]], seq + 1,
                  (f'在「{tz}」出現異常時，下列哪一項判斷最合理？', f'When "{te}" misbehaves, which diagnosis is most reasonable?'),
                  (first(fz, True) + ' 需以量測區分可能原因。', first(fe, False) + ' Discriminate candidate causes by measurement.')),
             25)

    stages = []
    for si, (sz, se) in enumerate(STAGES):
        u1, u2 = units[si * 2], units[si * 2 + 1]
        stages.append({
            'id': f'{prefix}-s{si + 1}', 'title': sz, 'titleEn': se,
            'description': f'本階段聚焦「{u1["title"][0]}」與「{u2["title"][0]}」：先建立機制與定量模型，再設計驗證並診斷失效。',
            'descriptionEn': f'This stage covers "{u1["title"][1]}" and "{u2["title"][1]}": build the mechanism and quantitative model first, then design verification and diagnose failures.',
            'steps': steps_by_stage[si],
        })
    return {'stages': stages, 'units': units}


def main() -> int:
    targets = {t['id']: t for t in json.loads((HERE / 'targets.json').read_text('utf-8'))}
    inputs = load_inputs(targets)
    missing = sorted(set(targets) - set(inputs))
    if missing:
        print('Missing authored inputs:', ' '.join(missing))
        if '--allow-missing' not in sys.argv:
            return 1
    featured = {c['id']: c for c in json.loads((DATA / 'featured.json').read_text('utf-8'))}
    catalog = {c['id']: c for c in json.loads((DATA / 'catalog.json').read_text('utf-8'))}
    sources = json.loads((DATA / 'sources.json').read_text('utf-8'))
    by_url = {s['url'].rstrip('/'): s['id'] for s in sources}
    known_ids = {s['id'] for s in sources}

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
                sid = 'v12o-' + s['key']
                n = 2
                while sid in known_ids:
                    sid = f"v12o-{s['key']}-{n}"; n += 1
                known_ids.add(sid); by_url[url.rstrip('/')] = sid
                out_sources.append({
                    'id': sid, 'title': s['title'], 'titleEn': s['titleEn'], 'publisher': s['publisher'],
                    'url': url, 'sourceType': s['sourceType'], 'scope': s['scope'], 'scopeEn': s['scopeEn'],
                    'accessed': '2026-10-15', 'imageReuse': 'Link only. No source image or article reproduction.',
                })
            src_ids.append(sid)
        src_ids = list(dict.fromkeys(src_ids))
        existing = featured.get(cid) if target.get('mode') == 'extend-existing' else None
        if existing:  # ignore V12 stages from a previous integration run
            existing = {**existing, 'stages': [st for st in existing['stages'] if '-v12-' not in st['id']]}
        result = build_course(d, target, existing, src_ids)
        built[cid] = {'input': d, 'units': result['units'], 'sourceIds': src_ids}
        nodes = [list(n) for n in d['architectureNodes']]
        edges = [list(e) for e in d['architectureEdges']]
        sz, se = split(d['summary'])
        fz, fe = split(d['focus'])
        ez, ee = split(d['example'])
        course = {
            'id': cid, 'title': title_zh, 'titleEn': title_en, 'category': 'instruments',
            'kind': 'course', 'status': 'guided', 'contentStatus': 'reviewable-educational-curriculum',
            'summary': sz, 'summaryEn': se, 'focus': fz, 'focusEn': fe,
            'scope': COURSE_SCOPE, 'scopeEn': COURSE_SCOPE_EN,
            'subcategory': target['discipline'], 'subcategoryTitle': target['disciplineTitle'],
            'subcategoryTitleEn': target['disciplineTitleEn'],
            'learningTrack': 'optics', 'learningSubdiscipline': target['discipline'],
            'learningTags': ['optics', target['discipline'], d['family']],
            'architectureFamily': d['family'], 'architectureNodes': nodes, 'architectureEdges': edges,
            'diagram': {'type': d['family'], 'labels': [n[0] for n in nodes[:5]], 'labelsEn': [n[1] for n in nodes[:5]], 'original': True, 'notToScale': True},
            'workedExample': {
                'title': '原創假想算例與邊界', 'titleEn': 'Original hypothetical example and boundaries',
                'text': ez, 'textEn': ee,
                'assumptions': '數值是本課自行設定的教學假設，不代表實機量測、產品額定或操作參數；改變系統邊界後必須重算。',
                'assumptionsEn': 'Inputs are teaching assumptions, not measured hardware, product ratings or operating parameters; recalculate after changing the system boundary.',
                'sourceScope': '原創數值練習；來源支援公開原理與設施背景，不宣稱來源提供這組數據。',
                'sourceScopeEn': 'Original numerical exercise; sources support public principles and facility context, not these numbers.',
            },
            'depth': 4, 'languageCoverage': ['zh-TW', 'en'], 'simulationOnly': True,
            'educationEdition': 12, 'enrichmentVersion': 12,
        }
        if existing:
            course['extendsExisting'] = True
            course['existingStepCount'] = sum(len(st['steps']) for st in existing['stages'])
            course['newStages'] = result['stages']
            course['sourceIds'] = list(dict.fromkeys((existing.get('sourceIds') or []) + src_ids))
        else:
            course['stages'] = result['stages']
            course['sourceIds'] = src_ids
            course['curriculumVersion'] = 12
        out_courses.append(course)

        pz, pe = split(d['place']['name'])
        cz, ce = split(d['place']['country'])
        hz, he = split(d['history'])
        u = result['units']
        if not existing:
            out_places.append({
                'courseId': cid,
                'place': {'name': pz, 'nameEn': pe, 'city': pz, 'cityEn': pe, 'country': cz, 'countryEn': ce,
                          'lat': round(float(d['place']['lat']), 5), 'lng': round(float(d['place']['lng']), 5),
                          'address': d['place']['query'], 'addressEn': d['place']['query'], 'mapQuery': d['place']['query'],
                          'coordinateScope': COORD_SCOPE, 'coordinateScopeEn': COORD_SCOPE_EN},
                'summary': f'{title_zh}：{fz}。', 'summaryEn': f'{title_en}: {fe}.',
                'connection': f'從「{u[0]["anchor"][0]}」追到「{u[7]["anchor"][0]}」；地圖提供公開案例的地理脈絡。',
                'connectionEn': f'Trace the system from “{u[0]["anchor"][1]}” to “{u[7]["anchor"][1]}”; the map gives public geographic context.',
                'history': [
                    {'year': '公開工程脈絡 / Public engineering context', 'title': title_zh, 'titleEn': title_en,
                     'text': hz, 'textEn': he, 'sourceIds': src_ids},
                    {'year': '學習延伸 / Learning transfer', 'title': '從工程史到可驗證模型', 'titleEn': 'From engineering history to verifiable models',
                     'text': f'本課把「{u[0]["title"][0]}」到「{u[7]["title"][0]}」改寫為 32 個原創分析、量測與診斷任務；不複製來源圖片、影片逐字稿或現場程序。',
                     'textEn': f'The course turns "{u[0]["title"][1]}" through "{u[7]["title"][1]}" into 32 original analysis, measurement and diagnosis tasks without copying source images, video transcripts or field procedures.',
                     'sourceIds': src_ids},
                ],
                'references': [{'title': s['title'], 'titleEn': s['titleEn'], 'publisher': s['publisher'], 'url': s['url'],
                                'scope': s['scope'], 'scopeEn': s['scopeEn']} for s in d['sources']],
                'sourceIds': src_ids,
            })

        for v in d['vendors']:
            name_en = v['nameEn'].strip()
            vid = None
            for k, comp in companies.items():
                if comp['nameEn'].casefold() == name_en.casefold():
                    vid = k
            if not vid:
                vid = slug(name_en)
                base, n = vid, 2
                while vid in companies and companies[vid]['nameEn'].casefold() != name_en.casefold():
                    vid = f'{base}-{n}'; n += 1
                companies[vid] = {'id': vid, 'name': v['name'], 'nameEn': name_en, 'business': v['business'],
                                  'businessEn': v['businessEn'], 'url': v['url'], 'investorUrl': v.get('investorUrl') or '',
                                  'sourceUrl': v['url'], 'reviewed': '2026-10-15', 'security': v.get('security')}
            elif not companies[vid].get('security') and v.get('security'):
                companies[vid]['security'] = v['security']
            if len(v['business']) < len(companies[vid]['business']):
                companies[vid]['business'], companies[vid]['businessEn'] = v['business'], v['businessEn']
            associations.setdefault(cid, []).append({'companyId': vid, 'role': v['role'], 'roleEn': v['roleEn'],
                                                     'business': v['business'], 'businessEn': v['businessEn']})

    # Related comparisons (needs every course built first).
    for cid, b in built.items():
        d = b['input']
        if targets[cid].get('mode') == 'extend-existing':
            continue
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
                'transfer': f'可遷移「{u[0]["title"][0]}」與「{u[4]["title"][0]}」的建模、量測與誤差預算方法；{oz}的元件、尺度與允收條件需重新設定。',
                'transferEn': f'The modelling, measurement and error-budget methods of "{u[0]["title"][1]}" and "{u[4]["title"][1]}" transfer, while components, scales and acceptance conditions of {oe} must be respecified.',
                'difference': f'本課聚焦{fz}；{oz}則以{ofz}為重點，不能直接沿用參數或允收值。',
                'differenceEn': f'This course focuses on {lower_first(fe)}; {oe} centres on {lower_first(ofe)}, so parameters and acceptance values do not transfer unchanged.',
                'practice': [
                    f'比較系統邊界：列出「{u[0]["anchor"][0]}」與「{w[0]["anchor"][0]}」的輸入、輸出與主要干擾。',
                    f'把本課算例的一個假設移到{oz}，標出可沿用的方程與必須重設的參數。',
                    f'以「{w[5]["title"][0]}」為例，設計一項能區分兩種系統的驗證量測，並註明不確定度。',
                ],
                'practiceEn': [
                    f'Compare system boundaries: list the inputs, outputs and main disturbances of “{u[0]["anchor"][1]}” and “{w[0]["anchor"][1]}”.',
                    f'Move one assumption of this course\'s worked example to {oe}, separating reusable equations from parameters that must be respecified.',
                    f'Using "{w[5]["title"][1]}", design a verification measurement that distinguishes the two systems and state its uncertainty.',
                ],
                'referenceUrls': [s['url'] for s in other['input']['sources']],
            })
        out_related.append({
            'courseId': cid,
            'overview': '以可遷移的原理、量測與驗證比較相近儀器；關聯不表示同一廠商、世代或驗收規格。',
            'overviewEn': 'Compare neighbouring instruments through transferable principles, measurements and validation; a link does not imply the same vendor, generation or acceptance requirements.',
            'related': related,
            'references': list({s['url']: {'title': s['title'], 'titleEn': s['titleEn'], 'publisher': s['publisher'], 'url': s['url'], 'scope': s['scope'], 'scopeEn': s['scopeEn']}
                                for s in d['sources'] + [x for rid in d['related'] if rid in built for x in built[rid]['input']['sources']]}.values()),
        })

    result = {
        'version': 12, 'generated': '2026-10-15',
        'courses': out_courses, 'sources': out_sources, 'places': out_places, 'related': out_related,
        'companies': list(companies.values()), 'associations': associations,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    steps = sum(len(st['steps']) for c in out_courses for st in (c.get('stages') or c.get('newStages')))
    listed = sum(1 for c in companies.values() if c.get('security'))
    print(json.dumps({'courses': len(out_courses), 'newSteps': steps, 'sources': len(out_sources),
                      'companies': len(companies), 'listed': listed, 'places': len(out_places),
                      'related': len(out_related), 'missing': missing}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
