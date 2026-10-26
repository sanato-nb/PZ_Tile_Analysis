#!/usr/bin/env python3
"""v111 all sixteen A/B/C/D screenshot files and nine missing/blank held proofs."""
from pathlib import Path
from PIL import Image
import csv,json,base64,html,hashlib,zipfile
R=Path(__file__).resolve().parents[1];CP=R/'checkpoints/v111';P=R/'checkpoints/v111_singleuse_preview'
with (CP/'observations.tsv').open(encoding='utf8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
with (CP/'observations.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (CP/'unresolved_9.csv').open(encoding='utf-8-sig',newline='') as f:held=list(csv.DictReader(f))
assert len(rows)==12 and len(held)==9
m=json.loads((P/'EVIDENCE_MANIFEST.json').read_text('utf8'))
assert len(m['results'])==16 and len(m['review_sheets'])==3
cards=[];all_imgs=[]
ids={(x['tile_set_locator'],int(x['local_id'])) for x in rows}
for e in m['results']:
    key=(e['key'][0],int(e['key'][1])); candidate=key in ids
    figs=[]
    for kind in ('A','B','C','D','board'):
        path=P/e[kind]
        with Image.open(path) as im:im.verify()
        all_imgs.append(path)
        figs.append('<figure><figcaption>'+kind+'</figcaption><img loading="lazy" src="data:image/jpeg;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')+'"></figure>')
    cards.append('<article><h2>'+html.escape(key[0]+'/'+str(key[1]))+'</h2><p>'+('잠정 후보 (low), 공식 정합 미검증' if candidate else '보류: B-C 변화 0')+'</p><p>이미지 제거차: '+str(e['visible_pixel_delta'])+', 단일 TMX 사용, D 별도 위치 없음.</p>'+''.join(figs)+'</article>')
assert len(all_imgs)==len(set(all_imgs))==80
page='<!doctype html><html lang="ko"><meta charset="utf-8"><title>v111 단일 배치 PNG/TMX 시각 판독</title><style>body{font:16px system-ui;background:#f1f3f5;color:#172b38;max-width:1280px;margin:2rem auto}article{background:#fff;padding:1rem;margin:1rem 0;border-radius:10px}img{max-width:100%;height:auto}figure{margin:1rem 0}figcaption{font-weight:bold}</style><h1>v111 신규 시각 검수 — 12 잠정 후보, 9종 미관찰 유지</h1><p>TileZed 타일 정의 텍스트 격자로 잠정 크롭, 공식 Local ID/TileZed 인증 0. 16장 A/B/C/D 비교판 중 12는 B-C 차이 있고, 4는 차이 0. 별도 PNG 누락 5종은 CSV에 수록. D는 모두 실제 다른 위치 없음.</p>'+''.join(cards)+'</html>'
assert page.count('data:image/jpeg;base64,')==80
hp=CP/'v111_이미지내장_검수.html';hp.write_text(page,encoding='utf8')
sheets=[R/x for x in m['review_sheets']]
for x in sheets:
    with Image.open(x) as im:im.verify()
zip_file=CP/'v111_단일배치21종_증거.zip'
files=[CP/'observations.tsv',CP/'observations.csv',CP/'unresolved_9.csv',CP/'review_notes_000_015.psv',hp,P/'EVIDENCE_MANIFEST.json',*all_imgs,*sheets]
assert len(files)==89
with zipfile.ZipFile(zip_file,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in files:z.write(f,arcname=f.relative_to(R).as_posix())
with zipfile.ZipFile(zip_file) as z:
    assert len(z.namelist())==89 and z.testzip() is None
report={'version':'v111','zip_crc':'PASS','zip_items':89,'zip_size_bytes':zip_file.stat().st_size,
'zip_sha256':hashlib.sha256(zip_file.read_bytes()).hexdigest(),'observed_new':12,'candidates_new':12,
'held_not_observed':4,'png_missing':5,'remaining_unobserved':9,'images_loaded':80,'html_embedded_images':80,
'review_sheets':3,'mapping_verified':0,'tilezed_verified':0,'final_certified':0}
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS v111 HTML 80 images, ZIP 89 entries CRC, 12 observed and 9 source issues',report)