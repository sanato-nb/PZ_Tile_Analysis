#!/usr/bin/env python3
"""v194: revisit 160..319, the second-added source A batch, from PNG itself
before surrounding TMX B/C. Correct over-specific A-only identifications without
rewriting the earlier provisional observations or claiming any final ID.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import csv,hashlib,json,math
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v194_Afirst_second160_319'
SHEETS=OUT/'sheets';SHEETS.mkdir(parents=True,exist_ok=True)
def csvrows(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(data):return hashlib.sha256(data).hexdigest()
def filesha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for piece in iter(lambda:f.read(4*1024*1024),b''):h.update(piece)
 return h.hexdigest()
def bbox(s):
 a=tuple(int(x) for x in s.strip('[]').split(','))
 assert len(a)==4 and 0<=a[0]<a[2] and 0<=a[1]<a[3]
 return a
@lru_cache(maxsize=32)
def png(path):
 with Image.open(R/path) as im:return im.convert('RGBA')
source=csvrows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
assert len(source)==4633
parent=csvrows(R/'review/v123_ABCD_next160/ABCD_160_319.csv')
assert len(parent)==160 and [int(x['index']) for x in parent]==list(range(160,320))
previous125=csvrows(R/'review/v125_AI_ABCD_20/AI_VISUAL_SPOTCHECK_20.csv')
prior134=json.loads((R/'review/v134_visual_180_319/MANUAL_VISUAL_NOTES.json').read_text())
assert len(previous125)==20 and len(prior134['notes'])==140
previous134=csvrows(R/'review/v134_visual_180_319/VISUAL_REVIEW.csv')
previous134promoted={int(x['index']) for x in previous134}
assert len(previous134promoted)==129
flags=json.loads((OUT/'MANUAL_A_REASSESSMENT_FLAGS.json').read_text())
risk={int(x['index']):x for x in flags['flags']}
assert len(risk)==25 and all(160<=i<320 for i in risk)
assert flags['official_mapping_verified']==flags['final_identity_certified']==0
review=[]
for index in range(160,320):
 a=source[index];p=parent[index-160]
 assert int(p['index'])==index and (p['tile_set_name'],int(p['local_id']))==(a['tile_set_name'],int(a['local_id']))
 assert a['selection_status']=='selected_provisional'
 assert a['source_image_path'] and a['selected_crop_xyxy'] and a['source_png_sha256'] and a['selected_rgba_pixel_sha256']
 path=R/a['source_image_path'];assert path.is_file()
 assert filesha(path)==a['source_png_sha256'],('PNG_modified',index)
 im=png(a['source_image_path']).crop(bbox(a['selected_crop_xyxy']))
 assert sha(im.tobytes())==a['selected_rgba_pixel_sha256'],('RGBA_source_mismatch',index)
 assert im.getchannel('A').getbbox() is not None
 if index<180:
  prior=previous125[index-160]
  assert int(prior['index'])==index
  assert (prior['tile_set_name'],int(prior['local_id']))==(a['tile_set_name'],int(a['local_id']))
  oldname=prior['identity_candidate'];oldparts=prior['part_role'];oldfeatures=prior['observed_features']
  oldstatus=prior['review_status']
 else:
  prior=prior134['notes'][str(index)]
  oldname=prior['candidate'];oldparts=prior['part'];oldfeatures=prior['features']
  oldstatus='provisional_candidate' if index in previous134promoted else 'held'
 if index in risk:
  f=risk[index]
  status='A_specificity_downgrade_requested'
  A_new=f['A_observation']
  caution=f['reason']
 else:
  status='A_sha_verified_no_independent_specificity_decision'
  A_new=''
  caution='Original A source pixel verified and A-only contact sheet provided; previous label still provisional and not newly independently confirmed.'
 review.append(dict(index=index,tile_set_name=a['tile_set_name'],local_id=int(a['local_id']),source_PNG=a['source_image_path'],
  A_RGBA_sha256=a['selected_rgba_pixel_sha256'],A_PNG_sha256=a['source_png_sha256'],
  A_source_verified=1,previous_candidate=oldname,previous_part=oldparts,previous_A_or_B_observation=oldfeatures,
  previous_status=oldstatus,original_B_C_changed_pixels=int(p['b_c_changed_pixels']),
  A_first_reaudit_status=status,
  corrected_A_only_shape=A_new,
  needs_caution=caution,
  risk_type=risk[index]['risk'] if index in risk else '',
  wiki_name_class_reference_only='https://pzwiki.net/wiki/PZwiki:Tile_list',
  wiki_matches_exact_tile_id=0,official_PNG_LocalID_mapping_verified=0,final_identity_certified=0))
assert len(review)==160 and len({(x['tile_set_name'],x['local_id']) for x in review})==160
assert all(x['A_source_verified']==1 for x in review)
assert sum(x['A_first_reaudit_status']=='A_specificity_downgrade_requested' for x in review)==25
assert sum(x['A_first_reaudit_status']=='A_sha_verified_no_independent_specificity_decision' for x in review)==135
# Compact original-A-only contact sheets. No B/C scene is placed in the card.
# Danger is visually indicated, but no identity scores are inflated.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
tiny=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
from PIL import ImageFont
font_kr=None
for loc in ['/usr/share/fonts/truetype/nanum/NanumGothic.ttf','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc']:
 if Path(loc).is_file():
  font_kr=ImageFont.truetype(loc,14);break
font_kr=font_kr or font
for batch in range(4):
 items=review[batch*40:(batch+1)*40]
 board=Image.new('RGB',(2600,2400),(236,240,245));d=ImageDraw.Draw(board)
 for i,r in enumerate(items):
  x=(i%5)*520;y=(i//5)*300
  marked=r['A_first_reaudit_status']=='A_specificity_downgrade_requested'
  d.rectangle((x+3,y+3,x+516,y+296),fill=(255,242,230) if marked else (253,253,253),outline=(220,118,78) if marked else (165,176,190),width=2)
  title=f'{r["index"]} {r["tile_set_name"][:28]} / {r["local_id"]}'
  d.text((x+11,y+9),title,font=font,fill=(28,49,75))
  d.text((x+11,y+30),('RECHECK A ROLE' if marked else 'A source verified (role not recertified)'),font=tiny,fill=(160,48,38) if marked else (58,104,71))
  tile=png(r['source_PNG']).crop(bbox(source[r['index']]['selected_crop_xyxy']))
  tile.thumbnail((230,201),Image.Resampling.NEAREST)
  check=Image.new('RGBA',(245,208),(240,244,250,255))
  b=ImageDraw.Draw(check)
  for yy in range(0,208,20):
   for xx in range(0,245,20):
    if ((xx//20)+(yy//20))%2==0:b.rectangle((xx,yy,xx+19,yy+19),fill=(214,221,229,255))
  check.alpha_composite(tile,((245-tile.width)//2,(208-tile.height)//2))
  board.paste(check.convert('RGB'),(x+9,y+53))
  d.text((x+268,y+58),'PREVIOUS candidate:',font=tiny,fill=(74,77,87))
  # Limit long mixed-language text to avoid tiny text clipping; full notes in CSV.
  old=r['previous_candidate'][:16] or '(held)'
  d.text((x+268,y+81),old,font=font_kr,fill=(57,64,79))
  d.text((x+268,y+131),'A-only shape review:',font=tiny,fill=(82,76,83))
  if marked:
   def cut(s,n):return [s[j:j+n] for j in range(0,min(len(s),n*4),n)]
   for k,part in enumerate(cut(r['corrected_A_only_shape'],17)):
    d.text((x+268,y+152+k*21),part,font=font_kr,fill=(164,65,45))
  else:d.text((x+268,y+152),'No independent role',font=tiny,fill=(97,107,116))
  d.text((x+10,y+269),'SOURCE A RGBA verified / identity NOT certified',font=tiny,fill=(69,102,113))
 board.save(SHEETS/f'A_ONLY_BATCH_{batch:02}.jpg',quality=88,optimize=True)
with (OUT/'A_FIRST_REAUDIT_160_319.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(review[0].keys()));w.writeheader();w.writerows(review)
counter=Counter(x['risk_type'] for x in review if x['risk_type'])
manifest=dict(version='v194',phase='second_added_batch_160_to_319_A_original_independent_qa',
 total_source_160_319=160,exact_original_PNG_sha_verified=160,exact_original_A_RGBA_sha_verified=160,
 previous_provisional_observed=sum(x['previous_status']=='provisional_candidate' for x in review),
 previously_held=sum(x['previous_status']=='held' for x in review),
 A_specificity_flags=25,unchallenged_not_independently_confirmed=135,
 flagged_previous_provisional=sum(x['previous_status']=='provisional_candidate' and x['risk_type']!='' for x in review),
 flagged_previous_held=sum(x['previous_status']=='held' and x['risk_type']!='' for x in review),
 flags_by_risk=dict(counter),
 new_observed=0,automatic_identity_changes=0,new_official_mapping=0,new_final_certified=0,
 source_wiki='https://pzwiki.net/wiki/PZwiki:Tile_list',
 wiki_scope='Moveables_EN and script-derived movable categories; not a complete atlas source/official local_id map',
 source_sheets=['review/v119_selected_A_new4633/sheets/SELECTED_A_002.jpg','review/v119_selected_A_new4633/sheets/SELECTED_A_003.jpg'],
 new_A_only_sheets=[f'A_ONLY_BATCH_{i:02}.jpg' for i in range(4)],
 original_A_CSV_path='review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv',
 original_review_tables=['review/v125_AI_ABCD_20/AI_VISUAL_SPOTCHECK_20.csv','review/v134_visual_180_319/MANUAL_VISUAL_NOTES.json'],
 csv_sha256=filesha(OUT/'A_FIRST_REAUDIT_160_319.csv'),
 flags_sha256=filesha(OUT/'MANUAL_A_REASSESSMENT_FLAGS.json'),
 source_image_identity_certification=0)
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v194 초기 두 번째 추가 배치 160..319 원본 A 우선 독립 재감사\n\n'
 '사용자 지적: 두 번째 추가 배치부터 타일 원본 A가 아니라 주변 B/C 장면만 보고 사물 이름을 붙였을 위험을 감사했습니다. '
 '첫 단계로 160~319 총 160개 정확한 원본 PNG 바이트 SHA256 및 해당 크롭 RGBA 픽셀 SHA256를 독립 검증하고 A만 담은 네 장의 새 접촉시트를 작성했습니다. '
 '이전 후보/부분역할과 원본 A에서 독립으로 보이는 실제 형상을 분리했습니다.\n\n'
 '- **25종**은 B의 조립된 주변 사물이나 용도까지 개별 A에 귀속했을 가능성이 보여, 원본 A의 형상 한정으로 후보 구체성을 낮춰 재검토하도록 표시. '
 '대표적으로 180-182 장작더미 조각, 187-192 캠핑 바닥/매트와 침낭 추측, 196/197/201/202 텐트 단일 평판, 305-312 흰 가지형 조각을 장식물로 단정한 사례입니다.\n'
 '- 나머지 **135종**은 이번에는 A 출처·이미지 무결성만 확인했고, 모든 실물 정체를 독립 재인증했다고 주장하지 않습니다. '
 '기존 A/B/C 관찰 기록과 SQLite/PROJECT_STATE를 변경하지 않았고, 이번 QA에서 추가 관찰/공식 매핑/최종 인증은 0입니다.\n'
 '- PZwiki:Tile list는 두 목록(Moveables_EN, script-derived)에서 물체의 일반 명칭을 참고할 수 있으나, '
 '모든 원본 타일의 PNG 크롭/Local ID/모든 건축 부품 대응표는 아니어서 공식 맵핑 증거로 사용하지 않았습니다.\n'
 '- 후속 범위는 idx320 이후 전체 기존 관찰 기록을 버전별로 원본 A 시트에 기반해 재확인하는 것. '
 '현재 상태 v192의 10,007/10,042(99.65%)는 *역사적 잠정 기록률*이며, 이번 원본 A 독립 재감사까지 모두 통과한 비율이 아닙니다.\n',encoding='utf-8')
print('PASS v194 A-FIRST ORIGINAL IMAGE 160',json.dumps(manifest,ensure_ascii=False),flush=True)
