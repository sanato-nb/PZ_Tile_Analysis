#!/usr/bin/env python3
"""v91 132종 기존 12+추가 120 실제 근거로 CSV, 2분할 내장 HTML, ZIP CRC 보고."""
from pathlib import Path
from PIL import Image
import csv,base64,hashlib,html,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
CP=ROOT/'checkpoints/v91'
with (CP/'observations_combined.tsv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==132
assert sum(r['review_status']=='candidate' for r in rows)==102
assert sum(r['review_status']=='held' for r in rows)==30
with (CP/'observations_combined.csv').open('w',encoding='utf-8-sig',newline='') as out:
 writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
m1=json.loads((ROOT/'checkpoints/v91_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
m2=json.loads((ROOT/'checkpoints/v91_extra_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
assert len(m1['results'])==12 and len(m2['results'])==120 and len(m2['review_sheets'])==20
first_sheets=[ROOT/p for p in m1['review_sheets']]+[ROOT/p for p in m2['review_sheets'][:9]]
second_sheets=[ROOT/p for p in m2['review_sheets'][9:]]
assert len(first_sheets)==len(second_sheets)==11
reports=[];all_images=[]
for batch in range(2):
 group=rows[batch*66:(batch+1)*66]
 cards=[];images=[]
 for r in group:
  sections=[]
  for key in ('A','B','C','D','board'):
   p=ROOT/r['evidence_'+key]
   with Image.open(p) as im: im.verify()
   images.append(p);all_images.append(p)
   b64=base64.b64encode(p.read_bytes()).decode('ascii')
   sections.append('<figure><figcaption>'+key+'</figcaption><img loading="lazy" src="data:image/jpeg;base64,'+b64+'"></figure>')
  cards.append('<article><h2>'+html.escape(r['tile_set_locator']+'/'+r['local_id'])+'</h2><p>'+html.escape(r['observed_features'])+'</p><p>잠정 정체: '+html.escape(r['identity_candidate'] or '보류')+'</p><p>부품 역할: '+html.escape(r['part_role'])+'</p><p>검수 신뢰도: '+html.escape(r['confidence'])+'</p>'+''.join(sections)+'</article>')
 assert len(images)==330
 page='<!doctype html><html lang="ko"><meta charset="utf-8"><title>v91 타일 132종 검수 '+str(batch+1)+'</title><style>body{font:16px system-ui;background:#f3f4f6;color:#172b38;max-width:1250px;margin:2rem auto}article{background:white;padding:1rem;margin:1rem;border-radius:10px}img{max-width:100%;height:auto}figure{margin:1rem 0}figcaption{font-weight:bold}</style><h1>v91 이미지 검수 '+str(batch*66+1)+'~'+str((batch+1)*66)+'/132</h1><p>기존 독립 판독 12종+신규 120종. A PNG, B TMX 5×5, C 배치 제거, D 대체 위치. 최종 인증 0.</p>'+''.join(cards)+'</html>'
 assert page.count('data:image/jpeg;base64,')==330
 htmlpath=CP/f'v91_이미지내장_검수_{batch+1:02d}.html'
 htmlpath.write_text(page,encoding='utf8')
 sheets=first_sheets if batch==0 else second_sheets
 for p in sheets:
  with Image.open(p) as im:im.verify()
 zp=CP/f'v91_증거_66종_{batch+1:02d}.zip'
 paths=[CP/'observations_combined.tsv',CP/'observations_combined.csv',ROOT/'checkpoints/v91_preview/EVIDENCE_MANIFEST.json',ROOT/'checkpoints/v91_extra_preview/EVIDENCE_MANIFEST.json',htmlpath,*images,*sheets]
 with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in paths:z.write(p,p.relative_to(ROOT).as_posix())
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None and len(z.namelist())==len(paths)==346
 assert htmlpath.stat().st_size<95000000 and zp.stat().st_size<95000000
 reports.append({'batch':batch+1,'zip_file':str(zp.relative_to(ROOT)),'zip_size_bytes':zp.stat().st_size,'zip_sha256':hashlib.sha256(zp.read_bytes()).hexdigest(),'zip_files':len(paths),'zip_crc':'PASS','html_file':str(htmlpath.relative_to(ROOT)),'html_size_bytes':htmlpath.stat().st_size,'embedded_images':330,'review_sheets':len(sheets)})
assert len(all_images)==len(set(all_images))==660
report={'version':'v91','batch_reports':reports,'zip_crc':'PASS','zip_files_total':692,'image_count':660,'image_load':'PASS','embedded_html_images':660,'observations':132,'provisional':102,'held':30,'certified':0,'review_sheets':22}
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS v91 HTML/CSV/ZIP CRC',report)
