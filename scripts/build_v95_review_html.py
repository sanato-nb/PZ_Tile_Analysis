#!/usr/bin/env python3
"""v95 12종 CSV·JPEG 내장 HTML 한 파일·ZIP 1개(매 CRC 검증)."""
from pathlib import Path
from PIL import Image
import csv,json,hashlib,base64,html,zipfile
ROOT=Path(__file__).resolve().parents[1]
CP=ROOT/'checkpoints/v95';PRE=ROOT/'checkpoints/v95_preview'
with (CP/'observations.tsv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==12 and sum(r['review_status']=='candidate' for r in rows)==7
with (CP/'observations.csv').open('w',encoding='utf-8-sig',newline='') as out:
 writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
m=json.loads((PRE/'EVIDENCE_MANIFEST.json').read_text('utf8'))
assert len(m['results'])==12 and len(m['review_sheets'])==2
reports=[];all_images=[]
for batch in range(1):
 group=rows
 cards=[];images=[]
 for r in group:
  sections=[]
  for kind in ('A','B','C','D','board'):
   p=ROOT/r['evidence_'+kind]
   with Image.open(p) as im:im.verify()
   images.append(p);all_images.append(p)
   sections.append('<figure><figcaption>'+kind+(' — 실제 다른 TMX 좌표(근접, 비독립)' if kind=='D' else '')+'</figcaption><img loading="lazy" src="data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode('ascii')+'"></figure>')
  cards.append('<article><h2>'+html.escape(r['tile_set_locator']+'/'+r['local_id'])+'</h2><p>'+html.escape(r['observed_features'])+'</p><p>잠정 후보: '+html.escape(r['identity_candidate'] or '보류')+'</p><p>'+html.escape(r['review_notes'])+'</p>'+''.join(sections)+'</article>')
 assert len(images)==60
 page='<!doctype html><html lang="ko"><meta charset="utf-8"><title>v95 A/B/C/D 시각 검수</title><style>body{font:16px system-ui;background:#f1f3f5;color:#172b38;max-width:1250px;margin:2rem auto}article{background:white;padding:1rem;margin:1rem;border-radius:10px}img{max-width:100%;height:auto}figure{margin:1rem 0}figcaption{font-weight:bold}</style><h1>v95 신규 12종 실제 이미지 검수</h1><p>A 원본 PNG, B 동일 층 5×5 근사 조립, C 선택 배치 하나 제거, D 다른 실제 TMX 사용 위치. D는 전부 1~3칸 이내 근접 사용 위치로 독립 검증이 아니며 공식 Local ID/TileZed 정합 미검증. 후보 7, 보류 5, 최종 인증 0.</p>'+''.join(cards)+'</html>'
 assert page.count('data:image/jpeg;base64,')==60
 hp=CP/f'v95_이미지내장_검수_{batch+1:02d}.html'
 hp.write_text(page,encoding='utf8')
 sheets=[ROOT/x for x in m['review_sheets']]
 for p in sheets:
  with Image.open(p) as im:im.verify()
 zip_path=CP/f'v95_증거_12종_{batch+1:02d}.zip'
 paths=[CP/'observations.tsv',CP/'observations.csv',hp,PRE/'EVIDENCE_MANIFEST.json',*images,*sheets]
 with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in paths:z.write(p,p.relative_to(ROOT).as_posix())
 with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None and len(z.namelist())==66
 assert hp.stat().st_size<95000000 and zip_path.stat().st_size<95000000
 reports.append({'batch':batch+1,'zip_file':str(zip_path.relative_to(ROOT)),'zip_size_bytes':zip_path.stat().st_size,'zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'zip_files':66,'zip_crc':'PASS','html_file':str(hp.relative_to(ROOT)),'html_size_bytes':hp.stat().st_size,'html_embedded_images':60,'review_sheets':2})
assert len(all_images)==len(set(all_images))==60
report={'version':'v95','batch_reports':reports,'zip_crc':'PASS','zip_files_total':66,'image_count':60,'image_load':'PASS','embedded_html_images':60,'observations':12,'provisional':7,'held':5,'certified':0,'review_sheets':2,'actual_nearby_D':12,'independent_D':0}
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS v95 CSV HTML JPEG ZIP CRC',report)
