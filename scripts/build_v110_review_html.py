#!/usr/bin/env python3
"""Build shareable HTML and ZIP for v110 diagnostic evidence; no identity claims."""
from pathlib import Path
import base64,csv,hashlib,html,json,zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; CP=ROOT/'checkpoints/v110'
m=json.loads((ROOT/'checkpoints/v110_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
with (CP/'unresolved_51.csv').open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
assert len(rows)==51
cards=[];images=[]
for i,r in enumerate(m['results']):
    k=r['key'];figs=[]
    for a in ('A','B','C','D','board'):
        path=ROOT/'checkpoints/v110_preview'/r[a]
        with Image.open(path) as im:im.verify()
        images.append(path)
        figs.append('<figure><figcaption>'+a+'</figcaption><img loading="lazy" src="data:image/jpeg;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')+'"></figure>')
    cards.append('<article><h2>'+html.escape(str(k[0])+'/'+str(k[1]))+'</h2><p>판독 보류: A 원본 가시 형상 없음. B-C 제거 변화 0. 정체 미확정.</p><div class="figs">'+''.join(figs)+'</div></article>')
assert len(images)==45
page='<!doctype html><html lang="ko"><meta charset="utf-8"><title>v110 미해결 원본 검수</title><style>body{font:16px system-ui;margin:2em auto;max-width:1300px;background:#f4f6f8;color:#172635}article{background:#fff;padding:1em;margin:1em 0;border-radius:10px}.figs{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1em}img{width:100%;height:auto}figure{margin:0}figcaption{font-weight:bold}</style><h1>v110 51종 미해결 원본 점검</h1><p>9종은 크롭 가능하지만 A가 가시적으로 비어 있고 B-C 픽셀 변화가 0입니다. 42종은 PNG 누락 5, Local ID PNG 범위 밖 37입니다. 새 관찰·후보·인증 증가 0. v109 누적 관찰 5,358/5,409 유지.</p><p>미해결 전체 51종의 원인과 키는 unresolved_51.csv에 기록했습니다. 아래는 9종의 A/B/C/D 증거 이미지 45장입니다.</p>'+''.join(cards)+'</html>'
assert page.count('data:image/jpeg;base64,')==45
html_path=CP/'v110_이미지내장_미해결검수.html'
html_path.write_text(page,encoding='utf8')
zip_path=CP/'v110_미해결51종_증거.zip'
files=images+[ROOT/s for s in m['review_sheets']]+[
    CP/'unresolved_51.csv',CP/'review_notes_000_008.psv',
    ROOT/'checkpoints/v110_preview/EVIDENCE_MANIFEST.json']
assert len(files)==50
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for path in files:z.write(path,arcname=str(path.relative_to(ROOT)))
with zipfile.ZipFile(zip_path) as z:
    assert len(z.namelist())==50 and z.testzip() is None
report={'version':'v110','mode':'source_gap_diagnostic','new_observed':0,
 'unresolved_total':51,'visual_blank':9,'missing_png':5,'local_id_out_of_png':37,
 'candidate_added':0,'certified_added':0,'images_loaded':45,'embedded_images':45,
 'review_sheets':2,'zip_files':50,'zip_crc':'PASS','zip_size_bytes':zip_path.stat().st_size,
 'zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'html_file':str(html_path.relative_to(ROOT)),
 'html_embedded_images':45}
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS v110 HTML 45 embedded images, ZIP 50 items CRC, 51 unresolved; no observation increase')