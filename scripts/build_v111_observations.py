#!/usr/bin/env python3
"""Compile v111 direct 16 visual reviews: 12 real B-C differences, 4 no-change holds, 5 PNG-missing."""
from pathlib import Path
import csv,json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'checkpoints/v111_singleuse_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
assert m['base']=='v110' and len(m['results'])==16 and len(m['source_unrenderable'])==5
notes={}
for line in (R/'checkpoints/v111/review_notes_000_015.psv').read_text('utf8').splitlines()[1:]:
    a=line.split('|')
    assert len(a)==4 and int(a[0]) not in notes
    notes[int(a[0])]=a
assert len(notes)==16
with (R/'checkpoints/v110/observations.tsv').open(encoding='utf8',newline='') as f:
    fields=next(csv.reader(f,delimiter='\t'))
rows=[];held=[]
for i,e in enumerate(m['results']):
    _,visual,candidate,confidence=notes[i]
    tile,lid=e['key'];k=(tile,int(lid));p=e['primary_placement']
    assert e['uses']==1 and not e['other_placement_available'] and e['atlas_status']=='tiledef_grid_provisional'
    assert m['sha256']['Tiles/2x/'+tile+'.png'] and m['sha256'][p['tmx']]
    delta=e['visible_pixel_delta']
    if not candidate or delta<500:
        assert not candidate and delta==0
        held.append({'tile_set_locator':tile,'local_id':int(lid),'status':'held_no_BC_change',
                     'reason':'PNG A may contain visual pixels but this TMX placement causes no B-C change; 1 use, D unavailable',
                     'observed_features':visual})
        continue
    assert confidence=='low' and delta>=500
    prefix=f'checkpoints/v111_singleuse_preview/{tile}__{lid:03d}'
    role=('벽 균열·선형 오버레이' if tile.startswith('d_wallcracks_') else '풀·작은 나무·관목 등 지면 식생')
    row=dict(tile_set_locator=tile,local_id=lid,review_status='candidate',
      observed_features=f"A 실제 원본에서 {visual}. B TMX 동일 층 5×5 조립, C 대상 배치 하나 제거. B-C 변화 {delta}픽셀. D는 다른 사용 위치가 없어 안내판. TileZed 텍스트 격자 사용, 공식 Local ID 미검증.",
      identity_candidate=candidate,part_role=role,confidence='low',
      source_tmx=p['tmx'],level=p['level'],layer_name=p['layer'],x=p['x'],y=p['y'],
      other_tmx='',other_level=-1,other_x=-1,other_y=-1,
      visible_pixel_delta=delta,missing_png_neighbors=e['missing_png_neighbors_B'],png_height_mismatch=1,
      mapping_verified=0,tilezed_verified=0,final_certified=0,
      evidence_A=prefix+'_A.jpg',evidence_B=prefix+'_B.jpg',evidence_C=prefix+'_C.jpg',
      evidence_D=prefix+'_D.jpg',evidence_board=prefix+'_ABCD.jpg',
      raw_gid=p['gid'],other_raw_gid=0,
      source_tmx_sha256=m['sha256'][p['tmx']],source_png_sha256=m['sha256']['Tiles/2x/'+tile+'.png'],
      atlas_status='tiledef_grid_provisional',
      review_notes='v111 접촉판 3장 직접 판독. 1회 배치로 D 미확보. TileZed 정의 격자 잠정 크롭, 공식 PNG-TMX Local ID 및 TileZed 렌더 미검증. low 신뢰도.')
    assert set(row)==set(fields),(set(fields)-set(row),set(row)-set(fields))
    rows.append(row)
for e in m['source_unrenderable']:
    assert e['reason']=='missing'
    held.append({'tile_set_locator':e['key'][0],'local_id':int(e['key'][1]),
                 'status':'held_missing_PNG','reason':'PNG source missing; cannot independently crop or identify',
                 'observed_features':'해당 이름의 원본 PNG 미확보'})
assert len(rows)==12 and len(held)==9 and len({(r['tile_set_locator'],int(r['local_id'])) for r in rows+held})==21
cp=R/'checkpoints/v111';cp.mkdir(exist_ok=True,parents=True)
with (cp/'observations.tsv').open('w',newline='',encoding='utf8') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
with (cp/'unresolved_9.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(held[0]));w.writeheader();w.writerows(held)
(cp/'review_summary.json').write_text(json.dumps({'version':'v111','new_observed':12,'candidate':12,'held_not_observed':4,'missing_png_not_observed':5,'D_available':0,'final':0},ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS v111: 12 observed provisional + 4 zero-delta + 5 source missing, original PNG/TMX evidence')