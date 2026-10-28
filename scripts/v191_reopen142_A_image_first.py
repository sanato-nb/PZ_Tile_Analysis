#!/usr/bin/env python3
"""v191 image-first 142-key reopened review. Actual selected original PNG A
and pixel-zoom view shown, with no observed, certified, or DB changes.
Original 9 keys do not have verified PNG/localID crop mapping and remain labeled.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import csv,hashlib,json,math
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v191_reopen142_A_first'
SHEETS=OUT/'sheets'
for p in [OUT,SHEETS]:p.mkdir(parents=True,exist_ok=True)
def csvrows(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(b):return hashlib.sha256(b).hexdigest()
def file_sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(4*1024*1024),b''):h.update(c)
 return h.hexdigest()
def box(s):
 x=tuple(map(int,s.strip('[]').split(',')))
 assert len(x)==4 and 0<=x[0]<x[2] and 0<=x[1]<x[3]
 return x
@lru_cache(maxsize=40)
def rgba(path):
 with Image.open(path) as im:return im.convert('RGBA')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
tiny=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
source=csvrows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
excluded=csvrows(R/'review/v188_active_review_exclusions/EXCLUDED_FROM_ACTIVE_REVIEW_142.csv')
assert len(source)==4633 and len(excluded)==142
assert len({(r['tile_set_name'],int(r['local_id'])) for r in excluded})==142
old=json.loads((R/'review/v175_remaining381_evidence_audit/OLD_NINE_UNOBSERVED.json').read_text())
assert len(old)==9
oldkeys={(r['tile_set_name'],int(r['local_id'])) for r in old}
assert { (r['tile_set_name'],int(r['local_id'])) for r in excluded if r['origin']=='original_5409' }==oldkeys
items=[]
for e in excluded:
 key=(e['tile_set_name'],int(e['local_id']))
 record=dict(tile_set_name=key[0],local_id=key[1],origin=e['origin'],
  source_A_index=e['source_A_index'],prior_category=e['source_blocker_category'],
  previous_user_action=e['previous_user_action'],original_exclusion=e['disposition'],
  review_reopened_by_user=1,source_A_pixel_sha_verified=0,source_png_sha_verified=0,
  source_A_transparent_nonzero_bbox='',actual_A_bbox='',zoom_is_original_A_nearest_neighbor=1,
  source_PNG='',source_crop='',source_status='',
  A_visible=0,A_visual_identity_observed=0,B_C_re_reviewed_this_stage=0,
  provisional_candidate=0,mapping_verified=0,tilezed_verified=0,certified=0,
  note='A original image must be directly inspected before identity assignment.')
 if e['origin']=='new_4633':
  idx=int(e['source_A_index'])
  s=source[idx]
  assert (s['tile_set_name'],int(s['local_id']))==key
  record['source_A_index']=idx;record['source_status']=s['selection_status']
  record['source_PNG']=s['source_image_path']
  record['source_crop']=s['selected_crop_xyxy']
  if s['selection_status']=='selected_provisional' and s['source_image_path'] and s['selected_crop_xyxy']:
   p=R/s['source_image_path']
   assert p.is_file(),('missing_original_png',key,str(p))
   assert file_sha(p)==s['source_png_sha256'],('original_PNG_SHA',key)
   tile=rgba(str(p)).crop(box(s['selected_crop_xyxy']))
   assert sha(tile.tobytes())==s['selected_rgba_pixel_sha256'],('original_A_RGBA_SHA',key)
   nontransparent=tile.getchannel('A').getbbox()
   assert nontransparent,('fully_transparent_A_requires_exception',key)
   record['actual_A_bbox']=list(tile.size)
   record['source_A_transparent_nonzero_bbox']=nontransparent
   record['source_A_pixel_sha_verified']=1
   record['source_png_sha_verified']=1
   record['A_visible']=1
   record['note']='Original individual sprite A confirmed by PNG bytes and full cropped RGBA pixel hash. No identity, source atlas LocalID, TileZed or certification inferred.'
 else:
  assert e['origin']=='original_5409'
  record['source_status']='historical_catalog_only_no_verified_A_crop'
  record['note']='Older tile catalog key has no verified source A crop and no official LocalID correspondence in v119 selected new atlas. Do not substitute an adjacent atlas cell as image evidence.'
 items.append(record)
assert len(items)==142
assert sum(r['origin']=='new_4633' for r in items)==133
assert sum(r['origin']=='original_5409' for r in items)==9
assert sum(r['source_A_pixel_sha_verified'] for r in items)>=131
cats=Counter(r['prior_category'] for r in items)
# A-only contact sheets in exclusion ledger order, 16 keys per sheet, no neighborhood context masking.
PW,PH=445,350
checker=Image.new('RGBA',(205,218),(245,247,250,255))
cd=ImageDraw.Draw(checker)
for yy in range(0,218,20):
 for xx in range(0,205,20):
  if ((xx//20)+(yy//20))%2==0:cd.rectangle((xx,yy,xx+19,yy+19),fill=(219,226,234,255))
def fit(im,w,h,nearest=False):
 t=im.copy()
 t.thumbnail((w,h),resample=Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS)
 return t
for i in range(math.ceil(len(items)/16)):
 sheet=Image.new('RGB',(PW*4,PH*4),(235,240,246))
 d=ImageDraw.Draw(sheet)
 for z,record in enumerate(items[i*16:i*16+16]):
  x=(z%4)*PW;y=(z//4)*PH
  d.rectangle((x+2,y+2,x+PW-3,y+PH-3),fill='white',outline=(158,173,190),width=2)
  idx=record['source_A_index']
  label=(f"IDX {idx}" if idx!='' else 'OLD / NO VERIFIED A')
  title=f"{label}   {record['tile_set_name'][:35]} / {record['local_id']}"
  d.text((x+9,y+8),title,font=small,fill=(31,52,72))
  d.text((x+9,y+29),f"prior hold: {record['prior_category'][:53]}",font=tiny,fill=(103,61,48))
  d.text((x+13,y+51),'A ORIGINAL (complete sprite)',font=tiny,fill=(54,72,96))
  d.text((x+229,y+51),'A PIXEL ZOOM (not new sprite)',font=tiny,fill=(54,72,96))
  if record['source_A_pixel_sha_verified']:
   tile=rgba(str(R/record['source_PNG'])).crop(box(record['source_crop']))
   base=checker.copy()
   full=fit(tile,200,208)
   base.alpha_composite(full,((205-full.width)//2,(218-full.height)//2))
   sheet.paste(base.convert('RGB'),(x+9,y+69))
   cropped=tile.crop(record['source_A_transparent_nonzero_bbox'])
   zoom=fit(cropped,200,208,nearest=True)
   zoomcanvas=checker.copy()
   zoomcanvas.alpha_composite(zoom,((205-zoom.width)//2,(218-zoom.height)//2))
   sheet.paste(zoomcanvas.convert('RGB'),(x+226,y+69))
   d.text((x+9,y+293),f"A png pixel SHA256: {str(record['source_A_pixel_sha_verified'])}   tile bbox {tile.size}",font=tiny,fill=(48,104,67))
  else:
   d.rectangle((x+9,y+69,x+431,y+288),fill=(245,230,221))
   d.text((x+28,y+140),'Original A source unavailable / unverified',font=small,fill=(140,45,36))
   d.text((x+28,y+170),'Do not infer any tile identity.',font=small,fill=(140,45,36))
  d.text((x+9,y+317),'IMAGE REVIEW PENDING   /   ID certification 0',font=tiny,fill=(113,40,50))
 sheet.save(SHEETS/f'A_ORIGINAL_{i:02}.jpg',quality=90,optimize=True)
fieldnames=list(items[0])
with (OUT/'REOPEN_142_A_SOURCE_AUDIT.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fieldnames);w.writeheader()
 for r in items:
  rr={k:(json.dumps(v) if isinstance(v,(tuple,list)) else v) for k,v in r.items()}
  w.writerow(rr)
ledger=dict(version='v191',kind='explicitly_reopen_142_image_first_png_pixel_audit',
 input_v188_excluded_keys=142,new_atlas_keys=133,old_catalog_keys=9,
 original_A_png_sha_verified=sum(r['source_png_sha_verified'] for r in items),
 original_A_rgba_sha_verified=sum(r['source_A_pixel_sha_verified'] for r in items),
 source_A_unavailable_or_not_verified=sum(1 for r in items if not r['source_A_pixel_sha_verified']),
 prior_reason_distribution=dict(cats),
 original_A_contact_sheets=[p.name for p in sorted(SHEETS.glob('A_ORIGINAL_*.jpg'))],
 A_sheets_direct_visual_review_finished=0,manual_identity_records_added=0,
 observed_checkpoint_before=9898,observed_checkpoint_after=9898,
 active_review_reopened_user_instruction=True,previous_v188_history_preserved=True,
 official_mapping_verified=0,tilezed_verified=0,certified=0)
(OUT/'MANIFEST.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v191 명시적으로 다시 열린 142종 — 원본 이미지 A 우선 판독용 실제 시트\n\n'
 '사용자가 제외됐던 142종을 다시 검수하라고 지시하여, 원래 v188 제외 기록을 보존한 상태로 신규 133개와 오래된 9개 키를 모두 검수 대상으로 재개합니다.\n'
 '원본 PNG 바이트 SHA256와 A RGBA 픽셀 SHA256 검사를 통과한 원본 스프라이트를 왼쪽에 전체 표시하고, 오른쪽에는 **같은 A 픽셀의 비투명 영역만 확대** 표시합니다. '
 '오른쪽 확대는 새로운 이미지나 다른 타일이 아닙니다. 사물 정체와 연결을 알려면 반드시 이 이미지 시트를 사람이 직접 시각적으로 보고 B/C/배치 근거와 나중에 함께 검수해야 합니다.\n'
 '오래된 원본9개는 공식 원본 A의 정확한 크롭/LocalID 대응이 아직 검증되지 않았으므로 아무 임의 이미지도 대신 사용하지 않습니다.\n'
 '이번 단계는 근거 시트 제작과 원본 이미지 무결성 감사이며, 시트가 생성되었다는 사실만으로 관찰 완료하거나 100%로 표시하지 않습니다. '
 '원본 DB, 사용자 과거 제외 지시, D/JUMBO 보류, 공식 매핑/TileZed/최종 인증은 변경하지 않습니다.\n',encoding='utf-8')
print('PASS v191 SOURCE A 142',json.dumps(ledger,ensure_ascii=False),flush=True)
