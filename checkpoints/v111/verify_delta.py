#!/usr/bin/env python3
"""Verify v111 original PNG/TMX, 12 candidates, 9 unchanged/missing holds, no fake D."""
from pathlib import Path
from PIL import Image
import csv,json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'checkpoints/v111'
m=json.loads((R/'checkpoints/v111_singleuse_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
with (P/'observations.tsv').open(encoding='utf8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
with (P/'unresolved_9.csv').open(encoding='utf-8-sig',newline='') as f: held=list(csv.DictReader(f))
assert len(rows)==12 and len(held)==9 and len(m['results'])==16 and len(m['source_unrenderable'])==5
keys={(x['tile_set_locator'],int(x['local_id'])) for x in rows+held}
assert len(keys)==21 and keys=={(x['key'][0],int(x['key'][1])) for x in m['results']+m['source_unrenderable']}
assert len(m['review_sheets'])==3 and m['base']=='v110' and m['observed_count_added']==0
assert all(x['review_status']=='candidate' and x['confidence']=='low' and int(x['visible_pixel_delta'])>=500 for x in rows)
assert all(x['mapping_verified']==x['tilezed_verified']==x['final_certified']=='0' for x in rows)
assert sum(x['visible_pixel_delta']==0 for x in m['results'])==4
for e in m['results']:
    tile,lid=e['key'];p=e['primary_placement']
    assert e['uses']==1 and not e['other_placement_available'] and e['atlas_status']=='tiledef_grid_provisional'
    for name,path in [(p['tmx'],R/'B4220.3_MapExport_256/tmx'/p['tmx']),('Tiles/2x/'+tile+'.png',R/'Tiles/2x'/(tile+'.png'))]:
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==m['sha256'][name]
    for k in ('A','B','C','D','board'):
        q=R/'checkpoints/v111_singleuse_preview'/e[k]
        assert q.is_file() and q.stat().st_size>1000
        with Image.open(q) as im:im.verify()
for x in m['review_sheets']:
    with Image.open(R/x) as im:im.verify()
print('PASS v111: 21 unique, 12 B-C positive, 4 B-C zero, 5 PNG missing; 80 JPEG and 3 sheets; 0 mapping certificates')