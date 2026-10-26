#!/usr/bin/env python3
"""Generate v100 per-tile TSV from 216 directly inspected visual note rows and original TMX/PNG manifest."""
import csv,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cp=ROOT/'checkpoints/v100'
m=json.loads((ROOT/'checkpoints/v100_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
with (ROOT/'checkpoints/v99/observations.tsv').open(encoding='utf8',newline='') as f: fields=next(csv.reader(f,delimiter='\t'))
notes={}
for start in (0,36,72,108,144,180):
 p=cp/f'review_notes_{start:03d}_{start+35:03d}.psv'
 for row in p.read_text('utf8').splitlines()[1:]:
  f=row.split('|')
  assert len(f)==4 and int(f[0]) not in notes
  notes[int(f[0])]=dict(visual=f[1],candidate=f[2],confidence=f[3])
assert len(notes)==len(m['results'])==216
def role(name):
 for pattern,value in (
  ('지붕|처마|박공|기와','지붕 경사면·박공·처마·이음부'),
  ('벽|창|문|몰딩|기둥','내외벽 패널·개구부·모서리 이음'),
  ('가구|수납|소파|카운터|탁자|의자','실내 가구 및 보관 설비'),
  ('바닥|러그|토양|흙|연석|주차선','바닥·도로·연석·장식 무늬'),
  ('간판|글자|표지|전단|안내','벽 부착 표시 또는 공공·상업 안내'),
  ('잎|바위|덩굴|풀|나무|쓰레기','식생·자연물 또는 지면 파편'),
  ('등|신호|그릴|기기|장비|금속','조명·시설 설비 및 관련 부품')):
  if re.search(pattern,name):return value
 return '개별 사물 또는 관련 부품'
rows=[];candidates=held=real_d=single=0
for i,e in enumerate(m['results']):
 n=notes[i]
 tile,id=e['key'];p=e['primary_placement'];q=e['other_placement']
 delta=e['visible_pixel_delta'];d=e['other_placement_available']
 status='candidate' if n['candidate'] and delta>=500 else 'held'
 if status=='candidate':candidates+=1
 else:held+=1
 real_d+=int(d);single+=int(e['uses']==1)
 png=f'Tiles/2x/{tile}.png'
 assert m['sha256'][png] and m['sha256'][p['tmx']]
 b=f'checkpoints/v100_preview/{tile}__{id:03d}'
 identity=n['candidate'] if status=='candidate' else ''
 record=dict(tile_set_locator=tile,local_id=id,review_status=status,
  observed_features=f"A 실제 원본에서 {n['visual']}. B는 TMX 같은 층 주변 5×5 근사 조립, C는 동일 레이어 단일 배치 제거. B-C 변화 {delta}픽셀. D는 "+('다른 실제 근접 위치, 독립 현장 아님.' if d else '다른 위치 없어 안내판 표시.'),
  identity_candidate=identity,part_role=role(identity),confidence='low' if status=='candidate' else 'none',
  source_tmx=p['tmx'],level=p['level'],layer_name=p['layer'],x=p['x'],y=p['y'],
  other_tmx=q['tmx'] if d else '',other_level=q['level'] if d else -1,other_x=q['x'] if d else -1,other_y=q['y'] if d else -1,
  visible_pixel_delta=delta,missing_png_neighbors=e['missing_png_neighbors_B'],png_height_mismatch=int(e['atlas_status']=='height_mismatch'),
  mapping_verified=0,tilezed_verified=0,final_certified=0,
  evidence_A=b+'_A.jpg',evidence_B=b+'_B.jpg',evidence_C=b+'_C.jpg',evidence_D=b+'_D.jpg',evidence_board=b+'_ABCD.jpg',
  raw_gid=p['gid'],other_raw_gid=q['gid'] if d else 0,
  source_tmx_sha256=m['sha256'][p['tmx']],source_png_sha256=m['sha256'][png],atlas_status=e['atlas_status'],
  review_notes=f"v100 36개 접촉 검수판 직접 시각 관찰과 review_notes PSV 6개 기록. 실제 TMX 사용 {e['uses']}회. 근접 D={d}, 독립 D={e['D_independent_5_cells_or_other_map']}, B 주변 누락={e['missing_png_neighbors_B']}. "+('원본 및 배치 기여 충분치 않아 후보 보류.' if status=='held' else '원본 외형으로 잠정 후보 제시, 독립 D 없어 신뢰도 low.')+' 공식 Local ID·PNG 높이·TileZed 미검증.')
 assert set(record)==set(fields),(i,set(fields)-set(record),set(record)-set(fields))
 rows.append(record)
assert real_d==23 and single==193 and held+candidates==216 and sum(x['D_independent_5_cells_or_other_map'] for x in m['results'])==0
with (cp/'observations.tsv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
 w.writeheader();w.writerows(rows)
(cp/'review_summary.json').write_text(json.dumps(dict(version='v100',observed=216,candidate=candidates,held=held,D_near=real_d,D_none=single,independent_D=0),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS v100 source notes to 180 TSV:',candidates,'candidate',held,'held')
