#!/usr/bin/env python3
"""Build v254 one-file offline reviewer: embed EXACT source A PNG and verified original B/C.
Source: v119 lossless ZIP; v251 real single-TMX B/C; v253 user fields, no guesses.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import io,csv,json,hashlib,zipfile,re,base64,sys,collections
R=Path(__file__).resolve().parents[1]
V119=R/"review/v119_selected_A_new4633"
V251=R/"review/v251_held188_single_location_Afirst_2026-10-30"
V253=R/"review/v253_user_manual68_reviewkit_2026-10-30"
OUT=R/"review/v254_manual68_embedded_original_images_2026-10-30"
OUT.mkdir(parents=True,exist_ok=True)
def readcsv(path):
 with path.open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def sha(x):return hashlib.sha256(x).hexdigest()
base_html=(V253/"PZ_USER_MANUAL_REVIEW_68.html").read_text(encoding="utf-8")
pat=re.compile(r'const DATA=(\[.*?\]);\s*\nconst repo=',re.S)
m=pat.search(base_html)
assert m,"v253 68 key source JSON anchor changed"
users=json.loads(m.group(1))
assert len(users)==68 and len({r["source_key"] for r in users})==68
assert sum(r["review_group"].startswith("정체불명") for r in users)==3
assert sum(r["review_group"].startswith("재검수") for r in users)==65
ledgerfile=V119/"REPRESENTATIVE_A_4633.csv"
manifest=json.loads((V119/"MANIFEST.json").read_text(encoding="utf-8"))
assert sha(ledgerfile.read_bytes())==manifest["selected_ledger_sha256"]
ledger=readcsv(ledgerfile)
archives={Path(r["path"]).name:r["sha256"] for r in manifest["png_archive_shards"]}
zip_paths=sorted({str(V119.relative_to(R)/ledger[int(r["source_index"])]["selected_shard"]) for r in users})
for p in zip_paths:assert Path(p).name in archives
def paths():
 return sorted({r["true_TMX_B_C_evidence_path"] for r in users}|set(zip_paths))
if "--list-images" in sys.argv:
 for p in paths():print(p)
 sys.exit(0)
zips={}
for p in zip_paths:
 raw=(R/p).read_bytes()
 assert sha(raw)==archives[Path(p).name],("source archive SHA failed",p)
 zips[p]=zipfile.ZipFile(io.BytesIO(raw))
# Render only diagnostic alpha-bbox zoom. The original PNG bytes are also embedded unchanged.
def zoom_original(A):
 box=A.getchannel("A").getbbox()
 assert box
 margin=4
 part=A.crop((max(0,box[0]-margin),max(0,box[1]-margin),min(A.width,box[2]+margin),min(A.height,box[3]+margin)))
 width,height=540,340
 panel=Image.new("RGB",(width,height),"#eff4f8")
 dr=ImageDraw.Draw(panel)
 for y in range(0,height,18):
  for x in range(0,width,18):
   if (x//18+y//18)%2==0:dr.rectangle((x,y,min(width,x+17),min(height,y+17)),fill="#dce5ec")
 fac=min((width-12)/part.width,(height-12)/part.height,10)
 part=part.resize((max(1,round(part.width*fac)),max(1,round(part.height*fac))),Image.Resampling.NEAREST)
 panel.paste(part,((width-part.width)//2,(height-part.height)//2),part)
 stream=io.BytesIO()
 panel.save(stream,format="PNG",optimize=True)
 return stream.getvalue(),box
b64=lambda b:base64.b64encode(b).decode("ascii")
embed={}
audit=[]
total_original_panel_bytes=0
for j,r in enumerate(users):
 idx=int(r["source_index"]);tile=ledger[idx]
 assert tile["tile_set_name"]+"/"+str(int(tile["local_id"]))==r["source_key"]
 archive=str(V119.relative_to(R)/tile["selected_shard"])
 A_png=zips[archive].read(tile["selected_zip_entry"])
 assert sha(A_png)==tile["selected_png_file_sha256"],("A PNG hash failure",r["source_key"])
 with Image.open(io.BytesIO(A_png)) as source:A=source.convert("RGBA")
 assert sha(A.tobytes())==tile["selected_rgba_pixel_sha256"],("A RGBA hash failure",r["source_key"])
 assert sha(A.tobytes())==r["original_A_RGBA_SHA256"],("v253 CSV A mismatch",r["source_key"])
 alpha=sum(A.getchannel("A").histogram()[1:])
 assert alpha==int(r["original_A_alpha_pixels"]) and alpha>0
 png_zoom,bbox=zoom_original(A)
 proof_path=R/r["true_TMX_B_C_evidence_path"]
 evidence_png=proof_path.read_bytes()
 with Image.open(io.BytesIO(evidence_png)) as im:
  assert im.format=="PNG",r["source_key"]
  pw,ph=im.size
 assert pw>=1500 and ph>=500,(r["source_key"],pw,ph)
 total_original_panel_bytes+=len(evidence_png)
 embed[r["source_key"]]=dict(a_raw="data:image/png;base64,"+b64(A_png),
  a_zoom="data:image/png;base64,"+b64(png_zoom),
  bc="data:image/png;base64,"+b64(evidence_png))
 audit.append(dict(source_index=idx,source_key=r["source_key"],
  source_PNG_original_sha256=sha(A_png),source_original_RGBA_sha256=sha(A.tobytes()),
  source_original_nontransparent_alpha=alpha,
  source_sprite_bbox=str(bbox),
  source_original_A_archive=archive,source_original_A_zip_entry=tile["selected_zip_entry"],
  original_B_C_source_path=r["true_TMX_B_C_evidence_path"],
  original_B_C_png_sha256=sha(evidence_png),original_B_C_original_width=pw,original_B_C_original_height=ph,
  original_A_lossless_bytes_embedded=1,original_BC_lossless_bytes_embedded=1,
  A_alpha_bbox_zoom_is_diagnostic_only=1,
  user_manual_decision_embedded=0,certified=0))
 print("EMBED",j+1,"/",len(users),r["source_key"],len(A_png),len(evidence_png),flush=True)
# Patch v253 with embedded images; preserve exact same 68 data, user fields and storage key.
js_assets="const IMAGE_ASSETS="+json.dumps(embed,ensure_ascii=True,separators=(",",":"))+";\n"
assert "const repo=" in base_html and base_html.count("const repo=")==1
html=base_html.replace("const repo=",js_assets+"const repo=",1)
old='  let imgs=sources.map(([name,path])=>{let f=fileFor(path);if(!f)return"";const uri=URL.createObjectURL(f);previewUrls.push(uri);return \'<div style="max-width:47%"><div class="small">\'+h(name)+\'</div><img src="\'+uri+\'" alt="\'+h(name)+\'"/></div>\'}).join("");'
assert old in html,"original v253 lazy images code not found"
new=r'''  const asset=IMAGE_ASSETS[x.source_key];
  let imgs="";
  if(asset){
   imgs='<section class="fullimage-proof" aria-label="원본 A/B/C 직접 표시">'
     +'<div class="source-images">'
     +'<figure><figcaption>A 원본 크롭 (투명 영역·앵커 그대로)</figcaption><div class="checker"><img loading="lazy" src="'+asset.a_raw+'" alt="검증된 원본 A PNG"/></div></figure>'
     +'<figure><figcaption>A 원본 알파 영역 확대 (판독용)</figcaption><img loading="lazy" class="zoom-a" src="'+asset.a_zoom+'" alt="원본 A 비투명 영역을 확대 표시"/></figure>'
     +'</div>'
     +'<figure class="wide-proof"><figcaption>실제 TMX 원본 A / B / 목표 GID 제거 C / B−C 차이 (전체 증거)</figcaption><img loading="lazy" src="'+asset.bc+'" alt="원본 TMX B 및 C 비교, 원본 PNG 무손실 내장"/></figure>'
     +'<div class="note">이미지는 파일 안에 직접 포함되어 있습니다. 별도 폴더 선택이나 GitHub 로그인이 필요 없습니다. 알파 영역 확대는 판독용이며 원본 PNG 크롭은 왼쪽에 그대로 있습니다.</div>'
     +'</section>';
  }else{
   imgs=sources.map(([name,path])=>{let f=fileFor(path);if(!f)return"";const uri=URL.createObjectURL(f);previewUrls.push(uri);return '<div style="max-width:47%"><div class="small">'+h(name)+'</div><img src="'+uri+'" alt="'+h(name)+'"/></div>'}).join("");
  }'''
html=html.replace(old,new,1)
old_notice="GitHub 비공개 저장소 이미지가 브라우저에 직접 표시되지 않으면 링크를 클릭해 확인하세요. 로컬 폴더의 같은 이름 PNG를 선택하면 카드에 미리보기가 생깁니다."
assert old_notice in html
html=html.replace(old_notice,"v254에서는 모든 68종의 원본 A와 실제 B/C 증거가 HTML에 직접 포함되어 있어 폴더 선택이 필요 없습니다.",1)
folderrow='<div class="row" style="margin-top:9px"><label>로컬 증거 이미지 폴더 (선택사항)<input id="files" type="file" multiple webkitdirectory></label><span class="small">v254에서는 모든 68종의 원본 A와 실제 B/C 증거가 HTML에 직접 포함되어 있어 폴더 선택이 필요 없습니다.</span></div>'
assert folderrow in html
html=html.replace(folderrow,'<div class="row" style="margin-top:9px"><span style="color:#126b57;font-weight:700">✓ 원본 A 이미지와 실제 B/C 전체 68종 자동 표시 — 파일 선택 불필요</span><input id="files" type="file" multiple webkitdirectory hidden></div>',1)
old_warning="임시 판정은 현재 브라우저에 저장을 시도하지만, 브라우저/로컬 파일 제한으로 보장되지 않습니다."
assert old_warning in html
html=html.replace(old_warning,"원본 A와 실제 B/C 이미지가 전부 이 HTML 안에 포함돼 있습니다. 별도 이미지 폴더를 선택하지 않아도 아래에 표시됩니다. 판정값은 현재 브라우저에 임시 저장을 시도하지만, 브라우저/로컬 파일 제한으로 보장되지 않습니다.",1)
html=html.replace("보류 68종 v253</title>","보류 68종 v254 (원본 이미지 내장)</title>",1)
assert "</style>" in html
css=r"""
.fullimage-proof{display:block;width:100%;max-width:100%;margin-top:9px}
.fullimage-proof figure{min-width:0;margin:0 0 10px;overflow:hidden;border:1px solid #d6e0e7;border-radius:8px;padding:8px;background:#f9fbfd}
.fullimage-proof figcaption{font-size:12px;font-weight:700;color:#2b5369;margin:0 0 8px}
.fullimage-proof .source-images{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.fullimage-proof .source-images img{width:100%;height:245px;max-height:245px;object-fit:contain;image-rendering:pixelated}
.fullimage-proof .source-images .checker{background:repeating-conic-gradient(#dbe4ea 0% 25%,#fff 0% 50%) 0 / 20px 20px}
.fullimage-proof .wide-proof img{width:100%;height:auto;max-height:none;object-fit:contain;image-rendering:auto}
.fullimage-proof .zoom-a{image-rendering:pixelated}
.previews:has(.fullimage-proof){display:block;max-width:100%}
@media(max-width:760px){.fullimage-proof .source-images{grid-template-columns:1fr}}
"""
html=html.replace("</style>",css+"</style>",1)
# Original v253 CSS max-height for previews img must be overridden by explicit v254 rules.
# The browser selectors above have higher specificity than .previews img.
output=OUT/"PZ_USER_MANUAL_REVIEW_68_IMAGES_INCLUDED.html"
output.write_text(html,encoding="utf-8")
assert output.stat().st_size<85*1024*1024,("GitHub oversized single-file HTML",output.stat().st_size)
with (OUT/"EMBEDDED_68_ORIGINAL_A_AND_REAL_BC_SHA.csv").open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(audit[0]));w.writeheader();w.writerows(audit)
summary=dict(version="v254",date="2026-10-30",scope_exact_68=68,
 source_medium65=65,source_unknown3=3,
 original_source_PNG_lossless_SHA256_checked=68,
 original_source_RGBA_byte_SHA256_checked=68,
 original_source_zip_shard_SHA256_checked=len(zips),
 original_B_C_source_PNG_lossless_embedded=68,
 original_B_C_original_source_SHA256_recorded=68,
 full_original_A_png_embedded_unchanged=68,
 zoomed_alpha_bbox_diagnostic_previews=68,
 original_B_C_image_pixels_not_changed=True,
 source_BC_png_total_bytes=total_original_panel_bytes,
 offline_HTML_file_bytes=output.stat().st_size,
 internet_or_GitHub_login_required_to_see_embedded_images=False,
 source_BC_reuses_v251_renders_not_newly_rendered=True,
 old_user_decisions_loaded_by_same_localstorage_key_when_browser_allows=True,
 user_CSV_and_JSON_export_and_import_retained=True,
 user_manual_decisions_received=0,auto_certification_or_db_activation=0,
 source_v251_v252_v253_files_modified=False,
 artifact="PZ_USER_MANUAL_REVIEW_68_IMAGES_INCLUDED.html")
(OUT/"MANIFEST.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("DONE",json.dumps(summary,ensure_ascii=False),flush=True)
