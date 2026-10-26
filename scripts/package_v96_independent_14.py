#!/usr/bin/env python3
"""Package independent v96 14-tile visual audit without changing official progress."""
from pathlib import Path
from PIL import Image
from xml.etree import ElementTree as ET
import base64,csv,hashlib,html,json,sqlite3,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'checkpoints/v96'
PREVIEW=ROOT/'checkpoints/v96_preview'
OUT=AUDIT/'independent_14'
OUT.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((AUDIT/'INDEPENDENT_AUDIT_14_REAL_D_20261026.csv').open(encoding='utf-8-sig',newline='')))
manifest=json.loads((PREVIEW/'EVIDENCE_MANIFEST.json').read_text('utf-8'))
source={(r['key'][0],int(r['key'][1])):r for r in manifest['results'] if r['status']=='evidence_only_unreviewed'}
assert len(rows)==14 and len(source)==120
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(keys)==14
assert sum(r['review_status']=='candidate' for r in rows)==12
assert sum(r['review_status']=='held' for r in rows)==2
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
assert all(r['D_independent']=='0' and r['other_placement_available']=='1' for r in rows)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Restore the v95 official database and verify all fourteen keys are unobserved.
base=Path('/tmp/pz_v95_independent14.sqlite')
subprocess.run([sys.executable,str(ROOT/'scripts/restore_unified_v95.py'),str(base)],check=True)
with sqlite3.connect(base) as c:
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    for key in keys:
        assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',key).fetchone()==(0,),key
    assert c.execute('SELECT COUNT(*) FROM analysis_queue').fetchone()[0]==1083
# Original asset SHA, TMX placement identity and A/B/C/D/board image load verification.
tmx_cache={}
image_sha={}
source_checks=[]
for r in rows:
    key=(r['tile_set_locator'],int(r['local_id']))
    e=source[key]
    a,b=e['primary_placement'],e['other_placement']
    assert e['other_placement_available'] and not e['D_independent_5_cells_or_other_map']
    assert int(r['visible_pixel_delta'])==e['visible_pixel_delta']
    assert int(r['missing_png_neighbors_B'])==e['missing_png_neighbors_B']
    assert (r['source_tmx'],int(r['level']),int(r['x']),int(r['y']),int(r['raw_gid']))==(a['tmx'],a['level'],a['x'],a['y'],a['gid'])
    assert (r['other_tmx'],int(r['other_level']),int(r['other_x']),int(r['other_y']),int(r['other_raw_gid']))==(b['tmx'],b['level'],b['x'],b['y'],b['gid'])
    assert (a['tmx'],a['level'],a['layer_index'],a['x'],a['y'])!=(b['tmx'],b['level'],b['layer_index'],b['x'],b['y'])
    png=ROOT/'Tiles/2x'/(key[0]+'.png')
    assert png.exists() and sha(png)==r['source_png_sha256']==manifest['sha256']['Tiles/2x/'+key[0]+'.png']
    with Image.open(png) as im: im.verify()
    for placement in (a,b):
        tmx=ROOT/'B4220.3_MapExport_256/tmx'/placement['tmx']
        assert sha(tmx)==manifest['sha256'][placement['tmx']]
        if placement['tmx'] not in tmx_cache:
            root=ET.parse(tmx).getroot()
            tmx_cache[placement['tmx']]=root.findall('layer')
        layer=tmx_cache[placement['tmx']][placement['layer_index']]
        assert layer.attrib['name']==placement['layer']
        assert int(layer.attrib.get('level',0))==placement['level']
        values=[int(x.strip()) for x in layer.find('data').text.split(',') if x.strip()]
        assert values[placement['y']*256+placement['x']]==placement['gid'],(key,placement)
    for k in ('A','B','C','D','board'):
        path=ROOT/r['evidence_'+k]
        assert path.exists()
        with Image.open(path) as im:im.verify()
        with Image.open(path) as im:im.load()
        image_sha[str(path.relative_to(ROOT))]=sha(path)
    source_checks.append({'key':list(key),'primary':a,'other':b,'delta_pixels_from_generation':e['visible_pixel_delta'],
        'D_independent':False,'source_png_sha256':r['source_png_sha256'],
        'source_tmx_sha256':r['source_tmx_sha256']})
# Supplemental evidence-only SQLite; not a replacement for the official integrated database.
db=OUT/'v96_independent_14_audit.sqlite'
if db.exists():db.unlink()
with sqlite3.connect(db) as c:
    c.execute('CREATE TABLE audit_rows(tile_set_locator TEXT NOT NULL,local_id INTEGER NOT NULL,review_status TEXT NOT NULL,observed_features TEXT NOT NULL,identity_candidate TEXT,part_role TEXT,confidence TEXT,record_json TEXT NOT NULL,PRIMARY KEY(tile_set_locator,local_id))')
    for r in rows:
        c.execute('INSERT INTO audit_rows VALUES (?,?,?,?,?,?,?,?)',(r['tile_set_locator'],int(r['local_id']),r['review_status'],r['observed_features'],r['identity_candidate'],r['part_role'],r['confidence'],json.dumps(r,ensure_ascii=False)))
    c.commit()
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert c.execute('SELECT COUNT(*) FROM audit_rows').fetchone()[0]==14
# Standalone image-embedded HTML, with actual source filenames and D nonindependence caveat.
parts=['<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>v96 독립 14종 검수</title><style>body{font-family:system-ui,sans-serif;background:#edf1f5;color:#18232c;max-width:1200px;margin:25px auto}article{background:white;padding:18px;margin:18px 0;border-radius:12px}img{max-width:100%;height:auto;border:1px solid #d1d8df}p{line-height:1.6}small{color:#555}</style></head><body><h1>v96 독립 A/B/C/D 시각 판독 14종</h1><p>후보 12종 · 보류 2종 · 최종 인증 0종. D는 다른 실제 배치지만 모두 근접 또는 다른 층으로 독립 현장 아님. 공식 v95 누적 수치 미변경.</p>']
for r in rows:
    parts.append('<article><h2>'+html.escape(r['tile_set_locator']+'/'+r['local_id'])+' · '+html.escape(r['review_status'])+'</h2><p><b>관찰:</b> '+html.escape(r['observed_features'])+'<br><b>잠정:</b> '+html.escape(r['identity_candidate'] or '보류')+'<br><b>역할:</b> '+html.escape(r['part_role'])+'<br><b>근거:</b> '+html.escape(r['review_notes'])+'</p>')
    for k in ('A','B','C','D','board'):
        path=ROOT/r['evidence_'+k]
        parts.append('<h3>'+k+'</h3><img alt="'+k+'" src="data:image/jpeg;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')+'">')
    parts.append('</article>')
parts.append('</body></html>')
htmlpath=OUT/'v96_independent_14_images_embedded.html'
htmlpath.write_text('\n'.join(parts),encoding='utf-8')
assert htmlpath.read_text('utf-8').count('data:image/jpeg;base64,')==70
checks={'base_version':'v95','source_v95_sha256':sha(base),'base_queue_remaining':1083,
    'audit_keys':14,'candidate':12,'held':2,'independent_D_sites':0,'other_actual_D_placements':14,
    'source_checks':source_checks,'evidence_jpeg_sha256':image_sha,'supplemental_sqlite_sha256':sha(db),
    'html_sha256':sha(htmlpath),'html_embedded_jpegs':70,'db_integrity':'ok','source_png_tmx_hash_match':True,'tmx_raw_gid_placements_verified':28,'jpeg_loaded':70}
validation=OUT/'validation.json'
validation.write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
zipfile_path=OUT/'v96_independent_14_A_B_C_D.zip'
with zipfile.ZipFile(zipfile_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for r in rows:
        for k in ('A','B','C','D','board'):
            p=ROOT/r['evidence_'+k]
            z.write(p,str(p.relative_to(ROOT)))
    for p in [AUDIT/'INDEPENDENT_AUDIT_14_REAL_D_20261026.csv',AUDIT/'INDEPENDENT_AUDIT_14_REAL_D_20261026.md',db,htmlpath,validation]:
        z.write(p,str(p.relative_to(ROOT)))
with zipfile.ZipFile(zipfile_path) as z:
    assert z.testzip() is None
    count=len(z.namelist())
    assert count==75,count
report={'zip_crc':'PASS','zip_entries':count,'zip_sha256':sha(zipfile_path),
    'sqlite_sha256':sha(db),'sqlite_integrity':'ok','html_sha256':sha(htmlpath),
    'image_sha256_verified':len(image_sha),'source_tmx_sha256_verified':True,'source_png_sha256_verified':True,
    'D_second_actual_placements':14,'D_independent_sites':0,'final_certified':0,
    'official_v95_progress_unchanged':True}
(OUT/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS v96 independent 14 packaging',report)
