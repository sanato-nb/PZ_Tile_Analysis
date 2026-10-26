#!/usr/bin/env python3
"""v102 12종 CSV·JPEG 내장 HTML 한 파일·ZIP 한 개(매 CRC 검증)."""
from pathlib import Path
from PIL import Image
import csv,json,hashlib,base64,html,zipfile
ROOT=Path(__file__).resolve().parents[1]
CP=ROOT/'checkpoints/v102';PRE=ROOT/'checkpoints/v102_preview'
with (CP/'observations.tsv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==12 and sum(r['review_status']=='candidate' for r in rows)==10
with (CP/'observations.csv').open('w',encoding='utf-8-sig',newline='') as out:
 writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
m=json.loads((PRE/'EVIDENCE_MANIFEST.json').read_text('utf8'))
assert len(m['results'])==12 and len(m['review_sheets'])==2
reports=[];all_images=[]
for batch in range(1):
 group=rows[batch*12:(batch+1)*12]
 cards=[];images=[]
 for r in group:
  sections=[]
  for kind in ('A','B','C','D','board'):
   p=ROOT/r['evidence_'+kind]
   with Image.open(p) as im:im.verify()
   images.append(p);all_images.append(p)
   sections.append('<figure><figcaption>'+kind+(' — 실제 근접 D 또는 미확보 (개별 기록 확인)' if kind=='D' else '')+'</figcaption><img loading="lazy" src="data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode('ascii')+'"></figure>')
  cards.append('<article><h2>'+html.escape(r['tile_set_locator']+'/'+r['local_id'])+'</h2><p>'+html.escape(r['observed_features'])+'</p><p>잠정 후보: '+html.escape(r['identity_candidate'] or '보류')+'</p><p>'+html.escape(r['review_notes'])+'</p>'+''.join(sections)+'</article>')
 assert len(images)==60
 page='<!doctype html><html lang="ko"><meta charset="utf-8"><title>v102 검수 타일 '+str(batch+1)+'</title><style>body{font:16px system-ui;background:#f1f3f5;color:#172b38;max-width:1250px;margin:2rem auto}article{background:white;padding:1rem;margin:1rem;border-radius:10px}img{max-width:100%;height:auto}figure{margin:1rem 0}figcaption{font-weight:bold}</style><h1>v102 새 검수 타일 '+str(batch*12+1)+'~'+str((batch+1)*12)+' /12</h1><p>A 원본 PNG, B 실제 TMX 5×5 근사 조립, C 배치 제거. D는 다른 실제 TMX 근접 배치 12종 또는 대체 사용 위치 없음 0종. 독립된 원거리 검증 D는 0종입니다. 모든 후보 잠정, 최종 인증 0.</p>'+''.join(cards)+'</html>'
 assert page.count('data:image/jpeg;base64,')==60
 hp=CP/f'v102_이미지내장_검수_{batch+1:02d}.html'
 hp.write_text(page,encoding='utf8')
 sheets=[ROOT/x for x in m['review_sheets'][batch*2:(batch+1)*2]]
 for p in sheets:
  with Image.open(p) as im:im.verify()
 obsolete_zip=CP/f'v102_증거_72종_{batch+1:02d}.zip'
 if obsolete_zip.exists(): obsolete_zip.unlink()
 zip_path=CP/f'v102_증거_12종_{batch+1:02d}.zip'
 paths=[CP/'observations.tsv',CP/'observations.csv',hp,PRE/'EVIDENCE_MANIFEST.json',*images,*sheets]
 with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in paths:z.write(p,p.relative_to(ROOT).as_posix())
 with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None and len(z.namelist())==66
 assert hp.stat().st_size<95000000 and zip_path.stat().st_size<95000000
 reports.append({'batch':batch+1,'zip_file':str(zip_path.relative_to(ROOT)),'zip_size_bytes':zip_path.stat().st_size,'zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'zip_files':66,'zip_crc':'PASS','html_file':str(hp.relative_to(ROOT)),'html_size_bytes':hp.stat().st_size,'html_embedded_images':60,'review_sheets':2})
assert len(all_images)==len(set(all_images))==60
report={'version':'v102','batch_reports':reports,'zip_crc':'PASS','zip_files_total':66,'image_count':60,'image_load':'PASS','embedded_html_images':60,'observations':12,'provisional':10,'held':2,'certified':0,'review_sheets':2,'single_use_without_D':0,'actual_nearby_D':12,'independent_D':0}
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS v102 CSV HTML JPEG ZIP CRC',report)
