#!/usr/bin/env python3
"""30 actual A/B/C/D visual notes from provisional TileZed text grid, no official mapping certification."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cp=ROOT/'checkpoints/v110'
m=json.loads((ROOT/'checkpoints/v110_tiledef_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
with (ROOT/'checkpoints/v109/observations.tsv').open(encoding='utf8',newline='') as f:
 fields=next(csv.reader(f,delimiter='\t'))
lines=(cp/'review_notes_000_029.psv').read_text('utf8').splitlines()[1:]
notes={}
for line in lines:
 f=line.split('|')
 assert len(f)==4
 i=int(f[0]);assert i not in notes
 notes[i]=dict(visual=f[1],candidate=f[2],confidence=f[3])
assert len(notes)==len(m['results'])==30
rows=[];candidate=held=0
for i,e in enumerate(m['results']):
 n=notes[i];tile,lid=e['key'];p=e['primary_placement'];q=e['other_placement']
 assert e['other_placement_available'] and e['visible_pixel_delta']>0
 assert e['atlas_status']=='tiledef_grid_provisional'
 status='candidate' if n['candidate'] and e['visible_pixel_delta']>=500 else 'held'
 candidate+=int(status=='candidate');held+=int(status=='held')
 png=f'Tiles/2x/{tile}.png'
 assert m['sha256'][png] and m['sha256'][p['tmx']]
 prefix=f'checkpoints/v110_tiledef_preview/{tile}__{lid:03d}'
 record=dict(tile_set_locator=tile,local_id=lid,review_status=status,
  observed_features=f"A 원본 PNG에서 {n['visual']}. B 실제 TMX 같은 층 5×5 조립, C 동일 레이어 선택 배치 1개 제거. B-C 변화 {e['visible_pixel_delta']}픽셀. D 다른 실제 TMX 좌표 ({q['tmx']}, {q['level']}층, {q['x']},{q['y']}) 확인. PNG 크롭은 TileZed 타일정의 텍스트 격자에 따른 잠정 매핑.",
  identity_candidate=n['candidate'] if status=='candidate' else '',
  part_role='석재 벽면 균열·오염 오버레이' if tile.startswith('d_wallcracks') else '지면의 풀·잎·덤불 등 식생 조각',
  confidence='low' if status=='candidate' else 'none',
  source_tmx=p['tmx'],level=p['level'],layer_name=p['layer'],x=p['x'],y=p['y'],
  other_tmx=q['tmx'],other_level=q['level'],other_x=q['x'],other_y=q['y'],
  visible_pixel_delta=e['visible_pixel_delta'],missing_png_neighbors=e['missing_png_neighbors_B'],
  png_height_mismatch=1,mapping_verified=0,tilezed_verified=0,final_certified=0,
  evidence_A=prefix+'_A.jpg',evidence_B=prefix+'_B.jpg',evidence_C=prefix+'_C.jpg',
  evidence_D=prefix+'_D.jpg',evidence_board=prefix+'_ABCD.jpg',
  raw_gid=p['gid'],other_raw_gid=q['gid'],
  source_tmx_sha256=m['sha256'][p['tmx']],source_png_sha256=m['sha256'][png],
  atlas_status=e['atlas_status'],
  review_notes=f"v110 접촉판 5장 직접 시각 판독. 다른 실제 D 존재, 원거리/다른 지도 여부={e['D_independent_5_cells_or_other_map']}. 원본 TMX GID-타일정의 PNG 격자 대응은 공식 인증 전의 가설. 모든 후보 low; mapping_verified=tilezed_verified=final_certified=0.")
 assert set(record)==set(fields),(set(record)-set(fields),set(fields)-set(record))
 rows.append(record)
assert (candidate,held)==(25,5),(candidate,held)
assert len({(r['tile_set_locator'],r['local_id']) for r in rows})==30
with (cp/'observations.tsv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
 w.writeheader();w.writerows(rows)
(cp/'review_summary.json').write_text(json.dumps(dict(version='v110',observed=30,candidate=25,held=5,
  D_actual=30,D_independent=sum(bool(x['D_independent_5_cells_or_other_map']) for x in m['results']),
  official_mapping_verified=0,final_certified=0),ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS v110 observations',candidate,held)
