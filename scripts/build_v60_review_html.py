#!/usr/bin/env python3
"""v60 육안 검수용 이미지 내장 HTML/독립 ZIP/CRC 검증. 기존 원본 변경 없음."""
import csv,base64,hashlib,html,json,zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
CP=ROOT/'checkpoints/v60'
PRE=ROOT/'checkpoints/v60_preview'
with (CP/'observations.tsv').open(encoding='utf-8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
manifest=json.loads((PRE/'EVIDENCE_MANIFEST.json').read_text(encoding='utf-8'))
assert len(rows)==12 and len(manifest['results'])==12
img_paths=[]
for row in rows:
    for kind in ['A','B','C','D','board']:
        p=ROOT/row['evidence_'+kind]
        assert p.is_file(),p
        with Image.open(p) as im:
            im.verify()
        img_paths.append(p)
assert len(img_paths)==len(set(img_paths))==60
def embedded(path):
    return 'data:image/jpeg;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
cards=[]
for idx,r in enumerate(rows,1):
    key=r['tile_set_locator']+' / '+r['local_id']
    status='잠정 후보' if r['review_status']=='candidate' else '보류'
    images=''.join(f'<figure><img loading="lazy" src="{embedded(ROOT/r["evidence_"+k])}" alt="{k}"><figcaption>{k} — '+('원본 크롭' if k=='A' else '장면 조립' if k=='B' else '한 배치만 제거' if k=='C' else '두 번째 사용 위치')+'</figcaption></figure>' for k in ['A','B','C','D'])
    board=embedded(ROOT/r['evidence_board'])
    cards.append(f"""<article data-status="{r['review_status']}"><header><b>{idx:02d}. {html.escape(key)}</b><span>{status}</span></header>
<p><strong>이미지에서 직접 확인한 특징:</strong> {html.escape(r['observed_features'])}</p>
<p><strong>잠정 정체:</strong> {html.escape(r['identity_candidate']) if r['identity_candidate'] else '정체 보류'}</p>
<p><strong>부품 역할:</strong> {html.escape(r['part_role'])} · 신뢰도 {html.escape(r['confidence'])}</p>
<p class="meta">TMX: {html.escape(r['source_tmx'])} / Level {r['level']} / ({r['x']},{r['y']}) / B-C 변화 {r['visible_pixel_delta']}px / 누락 주변 {r['missing_png_neighbors']}개 / 공식 대응 미인증</p>
<details open><summary>A/B/C/D 비교판</summary><img class="board" loading="lazy" src="{board}" alt="A/B/C/D 비교판"></details>
<details><summary>A 원본 · B 조립 · C 제거 · D 다른 위치 개별 이미지</summary><div class="quad">{images}</div></details></article>""")
css="""body{font:14px/1.6 system-ui,'Malgun Gothic',sans-serif;color:#213243;background:#f3f5f7;margin:0}
main{max-width:1450px;margin:auto;padding:22px}h1{margin:0}header.top{background:#142738;color:#fff;padding:20px 5%}
small{color:#ced8e3}article{background:#fff;border:1px solid #d9e2ea;border-radius:12px;padding:16px;margin:18px 0}
article header{display:flex;gap:15px;align-items:center;justify-content:space-between;font-size:17px}
article header span{font-size:12px;color:#667b8c}article p{margin:7px 0}.meta{color:#647789;font-size:12px}
.board{width:100%;height:auto;border-radius:6px;background:#eff2f5}.quad{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
figure{margin:0}figure img{width:100%;height:auto}figcaption{font-size:12px;color:#738290}
details{margin-top:10px}summary{cursor:pointer;font-weight:600}
select{padding:8px;border-radius:6px;margin:12px 0}@media(max-width:700px){.quad{grid-template-columns:1fr}}"""
html_text='<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>v60 타일 이미지 판독 증거 12종</title><style>'+css+'</style></head><body>'
html_text+='<header class="top"><h1>좀보이드 B42 v60 · 신규 시각 검수 12종</h1><small>잠정 후보 9, 보류 3 · v59 이후 신규 · 공식 Local ID/TileZed 인증 0</small></header>'
html_text+='<main><p>원본 PNG 크롭과 동일 층 주변 5×5 근사 아이소메트릭 B/C/D를 실제 이미지로 판독했습니다. PNG 높이 불일치 및 정합 미검증을 고려하여 정체를 최종 확정하지 않습니다.</p>'
html_text+='<label>표시 상태 <select id="filter" onchange="document.querySelectorAll(\'article\').forEach(e=>e.hidden=this.value!==\'all\'&&e.dataset.status!==this.value)"><option value="all">전체 12종</option><option value="candidate">잠정 후보 9종</option><option value="held">보류 3종</option></select></label>'
html_text+=''.join(cards)+'</main></body></html>'
html_file=CP/'v60_이미지내장_검수.html'
html_file.write_text(html_text,encoding='utf-8')
assert html_text.count('data:image/jpeg;base64,')==60
pack=CP/'v60_증거_12종_A_B_C_D.zip'
sources=[CP/'observations.csv',CP/'observations.tsv',html_file,PRE/'EVIDENCE_MANIFEST.json',*img_paths]
with zipfile.ZipFile(pack,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sources:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(pack) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(sources)
    for info in z.infolist():
        assert info.CRC>=0
report={'version':'v60','zip_sha256':hashlib.sha256(pack.read_bytes()).hexdigest(),
    'zip_size_bytes':pack.stat().st_size,'zip_files':len(sources),
    'zip_crc':'PASS','image_count':60,'image_load':'PASS',
    'embedded_html_images':60,'html_size_bytes':html_file.stat().st_size,
    'observations':12,'provisional':9,'held':3,'certified':0}
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS v60 HTML/PNG-derivative JPEG loading/ZIP CRC',report)
