#!/usr/bin/env python3
import csv,base64,hashlib,html,json,zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
CP=ROOT/'checkpoints/v84'
PRE=ROOT/'checkpoints/v84_preview'
with (CP/'observations.tsv').open(encoding='utf8',newline='') as f:
 rows=list(csv.DictReader(f,delimiter='\t'))
with (CP/'observations.csv').open('w',encoding='utf-8-sig',newline='') as csv_out:
 writer=csv.DictWriter(csv_out,fieldnames=list(rows[0]))
 writer.writeheader()
 writer.writerows(rows)
manifest=json.loads((PRE/'EVIDENCE_MANIFEST.json').read_text('utf8'))
assert len(rows)==len(manifest['results'])==92
images=[]
cards=[]
for r in rows:
 one=[]
 for k in ['A','B','C','D','board']:
  p=ROOT/r['evidence_'+k]
  with Image.open(p) as im: im.verify()
  images.append(p)
  b64=base64.b64encode(p.read_bytes()).decode('ascii')
  one.append('<figure><figcaption>'+k+'</figcaption><img loading="lazy" src="data:image/jpeg;base64,'+b64+'"></figure>')
 cards.append('<article><h2>'+html.escape(r['tile_set_locator']+'/'+r['local_id'])+'</h2><p>'+html.escape(r['observed_features'])+'</p><p>잠정 정체: '+html.escape(r['identity_candidate'] or '보류')+'</p><p>부품 역할: '+html.escape(r['part_role'])+'</p><p>신뢰도: '+html.escape(r['confidence'])+'</p>'+''.join(one)+'</article>')
assert len(images)==len(set(images))==460
page='<!doctype html><html lang="ko"><meta charset="utf-8"><title>v84 B42 타일 92종 직접 검수</title><style>body{font:16px system-ui;background:#f3f4f6;color:#172b38;max-width:1250px;margin:2rem auto}article{background:white;padding:1rem;margin:1rem;border-radius:10px}img{max-width:100%;height:auto}figure{margin:1rem 0}figcaption{font-weight:bold}</style><h1>v84 타일 이미지 검수 92종 · 잠정 74 · 보류 18</h1><p>PNG 원본 A, TMX 조립 B, 한 배치 제거 C, 다른 사용 위치 D, 비교판. 최종 인증 0.</p>'+''.join(cards)+'</html>'
assert page.count('data:image/jpeg;base64,')==460
out=CP/'v84_이미지내장_검수.html'
out.write_text(page,encoding='utf8')
zp=CP/'v84_증거_92종_A_B_C_D.zip'
files=[CP/'observations.csv',CP/'observations.tsv',out,PRE/'EVIDENCE_MANIFEST.json',*images]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files: z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None and len(z.namelist())==len(files)==464
report={'version':'v84','zip_sha256':hashlib.sha256(zp.read_bytes()).hexdigest(),'zip_size_bytes':zp.stat().st_size,'zip_files':len(files),'zip_crc':'PASS','image_count':460,'image_load':'PASS','embedded_html_images':460,'html_size_bytes':out.stat().st_size,'observations':92,'provisional':74,'held':18,'certified':0}
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=0)+'\n',encoding='utf8')
print('PASS v84 HTML/JPEG/ZIP CRC',report)

# v84 rerun after concurrent artifact push conflict; preserve corrected candidate/held counts.
