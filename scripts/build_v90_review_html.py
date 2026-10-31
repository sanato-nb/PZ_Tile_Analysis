#!/usr/bin/env python3
"""v90 시각 판독 CSV·분할 이미지 내장 HTML·2개 증거 ZIP 생성과 CRC 무결성 검증."""
from pathlib import Path
from PIL import Image
import csv,base64,hashlib,html,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
CP=ROOT/'checkpoints/v90'
PRE=ROOT/'checkpoints/v90_preview'
with (CP/'observations.tsv').open(encoding='utf8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
with (CP/'observations.csv').open('w',encoding='utf-8-sig',newline='') as out:
    writer=csv.DictWriter(out,fieldnames=list(rows[0]))
    writer.writeheader();writer.writerows(rows)
m=json.loads((PRE/'EVIDENCE_MANIFEST.json').read_text('utf8'))
assert len(rows)==len(m['results'])==240
assert sum(r['review_status']=='candidate' for r in rows)==191
assert sum(r['review_status']=='held' for r in rows)==49
assert len(m['review_sheets'])==40
all_images=[];reports=[];zip_paths=[]
for batch in range(2):
    group=rows[batch*120:(batch+1)*120]
    cards=[];images=[]
    for r in group:
        sections=[]
        for k in ('A','B','C','D','board'):
            p=ROOT/r['evidence_'+k]
            with Image.open(p) as im:im.verify()
            images.append(p);all_images.append(p)
            b64=base64.b64encode(p.read_bytes()).decode('ascii')
            sections.append('<figure><figcaption>'+k+'</figcaption><img loading="lazy" src="data:image/jpeg;base64,'+b64+'"></figure>')
        cards.append('<article><h2>'+html.escape(r['tile_set_locator']+'/'+r['local_id'])+'</h2><p>'+html.escape(r['observed_features'])+'</p><p>잠정 정체: '+html.escape(r['identity_candidate'] or '보류')+'</p><p>부품 역할: '+html.escape(r['part_role'])+'</p><p>검수 신뢰도: '+html.escape(r['confidence'])+'</p>'+''.join(sections)+'</article>')
    assert len(images)==600
    page='<!doctype html><html lang="ko"><meta charset="utf-8"><title>v90 B42 타일 240종 직접 검수 '+str(batch+1)+'</title><style>body{font:16px system-ui;background:#f3f4f6;color:#172b38;max-width:1250px;margin:2rem auto}article{background:white;padding:1rem;margin:1rem;border-radius:10px}img{max-width:100%;height:auto}figure{margin:1rem 0}figcaption{font-weight:bold}</style><h1>v90 타일 이미지 검수 '+str(batch*120+1)+'~'+str((batch+1)*120)+' / 240</h1><p>A 원본 PNG, B TMX 조립, C 동일 배치 제거, D 다른 위치. 검증되지 않은 잠정 정체이며 최종 인증 0.</p>'+''.join(cards)+'</html>'
    assert page.count('data:image/jpeg;base64,')==600
    h=CP/f'v90_이미지내장_검수_{batch+1:02d}.html'
    h.write_text(page,encoding='utf8')
    sheets=[ROOT/p for p in m['review_sheets'][batch*20:(batch+1)*20]]
    for p in sheets:
        with Image.open(p) as im:im.verify()
    zp=CP/f'v90_증거_120종_{batch+1:02d}.zip'
    paths=[CP/'observations.csv',CP/'observations.tsv',h,PRE/'EVIDENCE_MANIFEST.json',*images,*sheets]
    with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in paths:z.write(p,p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None and len(z.namelist())==len(paths)==624
    assert h.stat().st_size<95000000 and zp.stat().st_size<95000000,(h.stat().st_size,zp.stat().st_size)
    reports.append({'batch':batch+1,'zip_file':str(zp.relative_to(ROOT)),'zip_size_bytes':zp.stat().st_size,'zip_sha256':hashlib.sha256(zp.read_bytes()).hexdigest(),'zip_files':len(paths),'zip_crc':'PASS','html_file':str(h.relative_to(ROOT)),'html_size_bytes':h.stat().st_size,'html_embedded_images':600,'review_sheets':len(sheets)})
assert len(all_images)==len(set(all_images))==1200
report={'version':'v90','batch_reports':reports,'zip_crc':'PASS','zip_files_total':1248,'image_count':1200,'image_load':'PASS','embedded_html_images':1200,'observations':240,'provisional':191,'held':49,'certified':0,'review_sheets':40}
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS v90 CSV/HTML/JPEG/ZIP CRC',report)
