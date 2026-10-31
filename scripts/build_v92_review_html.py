#!/usr/bin/env python3
"""v92 신규 12종 실제 A/B/C/D 시각 근거: 이미지 내장 HTML, CSV, ZIP CRC."""
from pathlib import Path
from PIL import Image
import csv,base64,hashlib,html,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
CP=ROOT/'checkpoints/v92'
with (CP/'observations.tsv').open(encoding='utf8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==12
assert sum(r['review_status']=='candidate' for r in rows)==9
assert sum(r['review_status']=='held' for r in rows)==3
with (CP/'observations.csv').open('w',encoding='utf-8-sig',newline='') as out:
    writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
manifest=ROOT/'checkpoints/v92_preview/EVIDENCE_MANIFEST.json'
m=json.loads(manifest.read_text('utf8'))
assert m['base']=='v91' and len(m['results'])==12
sheets=[ROOT/p for p in m['review_sheets']]
assert len(sheets)==2
cards=[];images=[]
for r in rows:
    sections=[]
    for key in ('A','B','C','D','board'):
        p=ROOT/r['evidence_'+key]
        with Image.open(p) as im:im.verify()
        images.append(p)
        b64=base64.b64encode(p.read_bytes()).decode('ascii')
        sections.append('<figure><figcaption>'+key+'</figcaption><img loading="lazy" src="data:image/jpeg;base64,'+b64+'"></figure>')
    cards.append('<article><h2>'+html.escape(r['tile_set_locator']+'/'+r['local_id'])+'</h2><p>'+html.escape(r['observed_features'])+'</p><p>잠정 정체: '+html.escape(r['identity_candidate'] or '보류')+'</p><p>부품 역할: '+html.escape(r['part_role'])+'</p><p>검수 신뢰도: '+html.escape(r['confidence'])+'</p>'+''.join(sections)+'</article>')
assert len(images)==len(set(images))==60
page='<!doctype html><html lang="ko"><meta charset="utf-8"><title>v92 신규 12종 시각 검수</title><style>body{font:16px system-ui;background:#f3f4f6;color:#172b38;max-width:1250px;margin:2rem auto}article{background:white;padding:1rem;margin:1rem;border-radius:10px}img{max-width:100%;height:auto}figure{margin:1rem 0}figcaption{font-weight:bold}</style><h1>v92 신규 타일 12종 이미지 검수</h1><p>A 원본 PNG, B 같은 층 TMX 5×5, C 단일 배치 제거, D 다른 위치. 잠정 후보 9, 보류 3, 공식 인증 0.</p>'+''.join(cards)+'</html>'
assert page.count('data:image/jpeg;base64,')==60
htmlpath=CP/'v92_이미지내장_검수.html'
htmlpath.write_text(page,encoding='utf8')
for p in sheets:
    with Image.open(p) as im:im.verify()
zp=CP/'v92_증거_12종_A_B_C_D.zip'
paths=[CP/'observations.tsv',CP/'observations.csv',manifest,htmlpath,CP/'INDEPENDENT_VISUAL_AUDIT.md',*images,*sheets]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in paths:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None and len(z.namelist())==len(paths)==67
report={'version':'v92','zip_file':str(zp.relative_to(ROOT)),'zip_size_bytes':zp.stat().st_size,'zip_sha256':hashlib.sha256(zp.read_bytes()).hexdigest(),'zip_files':len(paths),'zip_crc':'PASS','html_file':str(htmlpath.relative_to(ROOT)),'html_size_bytes':htmlpath.stat().st_size,'embedded_images':60,'image_count':60,'image_load':'PASS','observations':12,'provisional':9,'held':3,'certified':0,'review_sheets':2}
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS v92 HTML/CSV/ZIP CRC',report)
