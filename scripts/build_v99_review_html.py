#!/usr/bin/env python3
"""v99 24 directly reviewed keys: CSV, 120 embedded images HTML, evidence ZIP CRC."""
from pathlib import Path
from PIL import Image
import csv,json,hashlib,base64,html,zipfile
ROOT=Path(__file__).resolve().parents[1]
CP=ROOT/'checkpoints/v99'; PRE=ROOT/'checkpoints/v99_preview'
with (CP/'observations.tsv').open(encoding='utf8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==24 and sum(r['review_status']=='candidate' for r in rows)==17
with (CP/'observations.csv').open('w',encoding='utf-8-sig',newline='') as out:
 w=csv.DictWriter(out,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
m=json.loads((PRE/'EVIDENCE_MANIFEST.json').read_text('utf8'))
assert len(m['results'])==24 and len(m['review_sheets'])==4
cards=[];images=[]
for r in rows:
 sections=[]
 for kind in ('A','B','C','D','board'):
  p=ROOT/r['evidence_'+kind]
  with Image.open(p) as im: im.verify()
  images.append(p)
  sections.append('<figure><figcaption>'+kind+'</figcaption><img loading="lazy" src="data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode('ascii')+'"></figure>')
 cards.append('<article><h2>'+html.escape(r['tile_set_locator']+'/'+r['local_id'])+'</h2><p>'+html.escape(r['observed_features'])+'</p><p>잠정 후보: '+html.escape(r['identity_candidate'] or '보류')+'</p><p>부품 역할: '+html.escape(r['part_role'])+'</p><p>'+html.escape(r['review_notes'])+'</p>'+''.join(sections)+'</article>')
assert len(images)==len(set(images))==120
page='<!doctype html><html lang="ko"><meta charset="utf-8"><title>v99 신규 24종 직접 이미지 검수</title><style>body{font:16px system-ui;background:#f1f3f5;color:#172b38;max-width:1250px;margin:2rem auto}article{background:white;padding:1rem;margin:1rem;border-radius:10px}img{max-width:100%;height:auto}figure{margin:1rem 0}figcaption{font-weight:bold}</style><h1>v99 신규 24종 A/B/C/D</h1><p>원본 PNG A, 실제 TMX 같은 층 5×5 근사 B, 한 배치 제거 C, 다른 근접 위치 D 6종 또는 미확보 안내 D 18종. 독립 원거리 D 0종. 후보 17, 보류 7, 최종 인증 0.</p>'+''.join(cards)+'</html>'
assert page.count('data:image/jpeg;base64,')==120
hp=CP/'v99_이미지내장_검수.html';hp.write_text(page,encoding='utf8')
sheets=[ROOT/x for x in m['review_sheets']]
for p in sheets:
 with Image.open(p) as im: im.verify()
zp=CP/'v99_증거_24종_A_B_C_D.zip'
paths=[CP/'observations.tsv',CP/'observations.csv',hp,PRE/'EVIDENCE_MANIFEST.json',*images,*sheets]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in paths:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(zp) as z:assert z.testzip() is None and len(z.namelist())==128
assert hp.stat().st_size<95000000 and zp.stat().st_size<95000000
report={'version':'v99','zip_file':str(zp.relative_to(ROOT)),'zip_size_bytes':zp.stat().st_size,'zip_sha256':hashlib.sha256(zp.read_bytes()).hexdigest(),'zip_files':128,'zip_crc':'PASS','html_file':str(hp.relative_to(ROOT)),'html_size_bytes':hp.stat().st_size,'html_embedded_images':120,'review_sheets':4,'image_load':'PASS','observations':24,'provisional':17,'held':7,'certified':0,'actual_nearby_D':6,'single_use_without_D':18,'independent_D':0}
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS v99 CSV HTML JPEG ZIP CRC',report)
