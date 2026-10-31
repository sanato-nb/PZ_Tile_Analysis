#!/usr/bin/env python3
"""v110 CSV + 150 original PNG/TMX JPEG embedded HTML + evidence ZIP CRC."""
from pathlib import Path
from PIL import Image
import csv,json,hashlib,base64,html,zipfile
ROOT=Path(__file__).resolve().parents[1]
CP=ROOT/'checkpoints/v110';PRE=ROOT/'checkpoints/v110_tiledef_preview'
with (CP/'observations.tsv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==30 and sum(r['review_status']=='candidate' for r in rows)==25
with (CP/'observations.csv').open('w',encoding='utf-8-sig',newline='') as out:
 writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
m=json.loads((PRE/'EVIDENCE_MANIFEST.json').read_text('utf8'))
assert len(m['results'])==30 and len(m['review_sheets'])==5
cards=[];images=[]
for r in rows:
 sections=[]
 for kind in ('A','B','C','D','board'):
  p=ROOT/r['evidence_'+kind]
  with Image.open(p) as im:im.verify()
  images.append(p)
  sections.append('<figure><figcaption>'+kind+(' — 다른 실제 TMX 배치' if kind=='D' else '')+'</figcaption><img loading="lazy" src="data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode('ascii')+'"></figure>')
 cards.append('<article><h2>'+html.escape(r['tile_set_locator']+'/'+r['local_id'])+'</h2><p>'+html.escape(r['observed_features'])+'</p><p>잠정 후보: '+html.escape(r['identity_candidate'] or '보류')+'</p><p>'+html.escape(r['review_notes'])+'</p>'+''.join(sections)+'</article>')
assert len(images)==len(set(images))==150
page='<!doctype html><html lang="ko"><meta charset="utf-8"><title>v110 타일 30종</title><style>body{font:16px system-ui;background:#f1f3f5;color:#172b38;max-width:1250px;margin:2rem auto}article{background:white;padding:1rem;margin:1rem;border-radius:10px}img{max-width:100%;height:auto}figure{margin:1rem 0}figcaption{font-weight:bold}</style><h1>v110 신규 30종 A/B/C/D 시각 검수</h1><p>모든 30종 실제 다른 TMX D 존재(28종 원거리). PNG 크롭은 TileZed 타일정의 텍스트 격자에 따른 잠정 대응으로 공식 Local ID·TileZed 검증 미완료. 후보 25, 보류 5, 최종 인증 0.</p>'+''.join(cards)+'</html>'
assert page.count('data:image/jpeg;base64,')==150
hp=CP/'v110_이미지내장_검수_01.html';hp.write_text(page,'utf8')
sheets=[ROOT/x for x in m['review_sheets']]
for p in sheets:
 with Image.open(p) as im:im.verify()
zip_path=CP/'v110_증거_30종_01.zip'
paths=[CP/'observations.tsv',CP/'observations.csv',hp,PRE/'EVIDENCE_MANIFEST.json',*images,*sheets]
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in paths:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None and len(z.namelist())==159
assert hp.stat().st_size<95000000 and zip_path.stat().st_size<95000000
report={'version':'v110','zip_file':str(zip_path.relative_to(ROOT)),'zip_size_bytes':zip_path.stat().st_size,
 'zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'zip_files':159,'zip_crc':'PASS',
 'html_file':str(hp.relative_to(ROOT)),'html_embedded_images':150,
 'observations':30,'provisional':25,'held':5,'certified':0,'review_sheets':5,
 'actual_D':30,'independent_D':28,'mapping_verified':0,'tilezed_verified':0}
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+chr(10),'utf8')
print('PASS v110 CSV HTML ZIP CRC',report)
