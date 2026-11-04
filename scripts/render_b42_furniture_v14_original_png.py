#!/usr/bin/env python3
"""Render original sprite-cell PNG previews; no human visual identity certifications."""
import base64,csv,hashlib,json,sqlite3,zipfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"analysis/furniture_full_b42/2026-11-04/source_first_v14"
DB=OUT/"B42_FURNITURE_SOURCE_FIRST_V14.sqlite"
def main():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 rows=[dict(x) for x in c.execute("SELECT * FROM v14_original_png_crop ORDER BY crop_queue_number")]
 assert len(rows)==160
 opened={};rawhash={};crops=[];audits=[]
 for x in rows:
  path=x["png_path"];file=ROOT/path;sha="";pixelsha="";crop=None;status="ORIGINAL_PIXEL_CROP_OK"
  try:
   if not file.is_file():raise FileNotFoundError(path)
   if path not in opened:
    rawhash[path]=hashlib.sha256(file.read_bytes()).hexdigest()
    opened[path]=Image.open(file).convert("RGBA")
   sha=rawhash[path];img=opened[path]
   w,h=int(x["cell_width"]),int(x["cell_height"])
   px,py=int(x["column_index"])*w,int(x["row_index"])*h
   if w<=0 or h<=0 or px<0 or py<0 or px+w>img.width or py+h>img.height:
    raise ValueError("cell crop out of original atlas bounds")
   crop=img.crop((px,py,px+w,py+h))
   pixelsha=hashlib.sha256(crop.tobytes()).hexdigest()
   if crop.getbbox() is None:status="ORIGINAL_CELL_TRANSPARENT"
  except Exception as err:status="CROP_FAILED:"+str(err)[:150]
  c.execute("UPDATE v14_original_png_crop SET png_sha256=?,crop_pixel_sha256=?,crop_status=? WHERE crop_queue_number=?",
            (sha,pixelsha,status,x["crop_queue_number"]))
  audits.append(dict(crop_queue_number=x["crop_queue_number"],entry_id=x["entry_id"],
   source_key=x["source_key"],original_png_path=path,original_png_sha256=sha,
   original_crop_pixels_sha256=pixelsha,crop_status=status,
   visual_game_object_identity_reviewed="NO"))
  crops.append(crop)
 for v in opened.values():v.close()
 font=ImageFont.load_default()
 for start in range(0,len(rows),40):
  cardw,cardh=232,218
  board=Image.new("RGB",(5*cardw,8*cardh),(243,246,249))
  draw=ImageDraw.Draw(board)
  for n in range(40):
   i=start+n; r=audits[i];x0=n%5*cardw;y0=n//5*cardh
   draw.rectangle((x0+3,y0+3,x0+cardw-4,y0+cardh-4),outline=(180,194,205),width=2,fill=(255,255,255))
   crop=crops[i]
   if crop is not None:
    thumb=crop.copy();thumb.thumbnail((202,151),Image.Resampling.NEAREST)
    bg=Image.new("RGBA",thumb.size,(249,250,252,255));bg.alpha_composite(thumb)
    board.paste(bg.convert("RGB"),(x0+(cardw-thumb.width)//2,y0+7+(151-thumb.height)//2))
   name=r["source_key"].encode("ascii","replace").decode("ascii")[:33]
   draw.text((x0+7,y0+166),str(i+1)+". "+name,font=font,fill=(36,53,71))
   draw.text((x0+7,y0+185),r["crop_status"][:29],font=font,fill=(62,77,92))
   draw.text((x0+7,y0+203),r["original_png_path"].split("/")[-1][:34],font=font,fill=(78,90,106))
  f=OUT/("V14_SOURCE_ONLY_ORIGINAL_CONTACT_%02d.png"%(start//40+1))
  board.save(f,optimize=True)
  if start==0:
   (OUT/"V14_CONTACT_01_BASE64_FOR_IMAGE_INSPECTION.txt").write_text(
      base64.b64encode(f.read_bytes()).decode("ascii"),encoding="ascii")
 with (OUT/"V14_160_ORIGINAL_PNG_PIXEL_SHA.csv").open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(audits[0]));w.writeheader();w.writerows(audits)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for table,n in [("source_attributes",195265),("source_slots",73644),("v13_warning_case",474),
                 ("v14_source_only_ledger",963),("v14_wiki_reference_audit",1268),
                 ("v14_source_tile_wiki_coverage",8219),("v14_original_png_crop",160)]:
  assert c.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]==n,(table,n)
 assert c.execute("SELECT COUNT(*) FROM v14_original_png_crop WHERE image_visual_identity_reviewed!=0 OR game_object_certified!=0").fetchone()[0]==0
 c.close()
 m=json.loads((OUT/"MANIFEST.json").read_text(encoding="utf8"))
 m.update(original_png_crop_ok=sum(r["crop_status"]=="ORIGINAL_PIXEL_CROP_OK" for r in audits),
  original_png_crop_empty=sum(r["crop_status"]=="ORIGINAL_CELL_TRANSPARENT" for r in audits),
  original_png_crop_failed=sum(r["crop_status"].startswith("CROP_FAILED:") for r in audits),
  original_png_contact_sheets=4,original_png_image_identity_reviews=0,original_warnings_still_open=474,
  game_object_identifications_confirmed=0,zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
  "# B42 v14 — 위키는 최신·완전함이 검증되지 않은 참고 원본\n\n"
  "v13의 전체 SQLite를 복제하고 963개 TileDef 전용 가구 후보, 1,268개 위키 참고 항목 및 8,219개 원본 TileDef 타일을 대조했습니다.\n"
  "963개 후보는 위키 이미지 타일 ID 연결이 없는 원본 가구 후보로, 위키 페이지에 정말 없는지와 게임 내 독립 물체인지는 확인되지 않았습니다.\n"
  "원본 PNG 실제 픽셀 160개를 추출해 4개 접촉시트로 생성했습니다. 이는 각 타일 한 장의 자동 추출이며 전체 가구 조립이나 시각적 정체 인증이 아닙니다.\n"
  "위키에 수납 정보가 비어 있어도 원본 속성을 유지합니다. 원본 경고 474건·게임 물체 인증 0건은 그대로입니다.\n"
  "Lua loot / TMX 배치 / Minecraft 구현 결정을 하지 않았습니다.\n",encoding="utf8")
 zipfile_path=OUT/"B42_FURNITURE_SOURCE_FIRST_V14.zip"
 with zipfile.ZipFile(zipfile_path,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(OUT.iterdir()):
   if f.is_file() and f!=zipfile_path and not f.name.startswith("_") and not f.name.endswith("_FOR_IMAGE_INSPECTION.txt"):
    z.write(f,f.name)
 with zipfile.ZipFile(zipfile_path) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V14_SOURCE_FIRST_COMPLETE_ORIGINAL_PNG_AND_SQLITE_VERIFIED",json.dumps(m,ensure_ascii=False,sort_keys=True),flush=True)
if __name__=="__main__":main()
