#!/usr/bin/env python3
"""Render authored railway system relationships as bilingual original SVGs."""
import html, json, math, textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'public/academy/data'
OUT=ROOT/'public/academy/assets/diagrams'
def esc(v): return html.escape(str(v),quote=True)
def lines(text,width):
    return textwrap.wrap(text,width=width,break_long_words=True,break_on_hyphens=False) or ['']
def draw(course,en):
    arch=course.get('v16Architecture') or course
    nodes=arch['architectureNodes']; edges=arch['architectureEdges']
    n=len(nodes); columns=3; rows=math.ceil(n/columns); height=240+rows*150
    positions=[(164+(i%columns)*270,200+(i//columns)*150) for i in range(n)]
    title=course['titleEn' if en else 'title']
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 {height}" role="img" aria-labelledby="t d"><title id="t">{esc(title)}</title><desc id="d">{esc("Original teaching map of authored system relationships; not to scale." if en else "原創教學系統關係圖；非比例尺與施工圖。")}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#457e91"/></marker></defs><rect width="870" height="{height}" rx="22" fill="#f1f6f2"/><text x="42" y="40" fill="#517364" font-family="sans-serif" font-size="13" letter-spacing="2">MACGYVER · RAIL &amp; TRANSPORT · V16</text>']
    for j,line in enumerate(lines(title,58 if en else 30)[:2]): parts.append(f'<text x="42" y="{78+j*27}" font-size="23" font-weight="700" font-family="sans-serif" fill="#173c35">{esc(line)}</text>')
    for a,b in edges:
        if not (0<=a<n and 0<=b<n and a!=b):raise ValueError('Invalid authored edge')
        x1,y1=positions[a];x2,y2=positions[b];dx,dy=x2-x1,y2-y1
        scale=max(abs(dx)/112,abs(dy)/49); ex=x2-dx/scale;ey=y2-dy/scale
        parts.append(f'<path d="M{x1} {y1}L{ex:.2f} {ey:.2f}" stroke="#457e91" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>')
    colors=['#d3eadb','#d2e8ef','#f4e0b9','#e0dbf0','#d9eccc','#f0d6d3']
    for i,(x,y) in enumerate(positions):
        node=nodes[i]; label=node[1 if en else 0] if isinstance(node,list) else node.get('labelEn' if en else 'label',node.get('title',''))
        parts.append(f'<rect x="{x-112}" y="{y-49}" width="224" height="98" rx="15" fill="{colors[i%len(colors)]}" stroke="#86a69a"/><text x="{x-96}" y="{y-28}" fill="#356c5b" font-family="sans-serif" font-size="12">{i+1:02}</text>')
        wrapped=lines(label,25 if en else 13)
        if len(wrapped)>3: raise ValueError(f'Label too long: {course["id"]} {label}')
        for j,line in enumerate(wrapped):parts.append(f'<text x="{x}" y="{y+1+(j-(len(wrapped)-1)/2)*20}" text-anchor="middle" font-size="16" font-family="sans-serif" fill="#1f4036">{esc(line)}</text>')
    foot='Arrows reproduce the authored course relationships. Consult the linked references for context.' if en else '箭頭依教材列出的系統關係繪製；適用邊界與驗證方法請配合課程來源閱讀。'
    parts.append(f'<text x="42" y="{height-39}" font-family="sans-serif" font-size="13" fill="#4d6a5e">{esc(foot)}</text></svg>')
    return ''.join(parts)+'\n'
def main():
    featured=json.loads((DATA/'featured.json').read_text());catalog=json.loads((DATA/'catalog.json').read_text())
    targets={f'b{i}' for i in range(301,401)}; courses=[c for c in featured if c['id'] in targets]
    assert len(courses)==100,'Integrate all 100 rail courses first.'
    OUT.mkdir(parents=True,exist_ok=True)
    for c in courses:
        for en in [False,True]:
            path=f'assets/diagrams/v16-{c["id"]}-'+('en' if en else 'zh')+'.svg'
            (ROOT/'public/academy'/path).write_text(draw(c,en),encoding='utf-8')
            c['flowDiagramEn' if en else 'flowDiagram']=path
    by={c['id']:c for c in courses}
    for c in catalog:
        if c['id'] in by:
            for k in ['flowDiagram','flowDiagramEn']:c[k]=by[c['id']][k]
    for name,value in [('featured',featured),('catalog',catalog)]:
        (DATA/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,separators=(',',':'))+'\n')
    print(json.dumps({'railCourses':100,'originalDiagramSvgFiles':200}))
if __name__=='__main__':main()
