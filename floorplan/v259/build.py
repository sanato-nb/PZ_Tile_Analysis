"""Build the standalone v259 plan from a restored v258 database."""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUTPUT = ROOT / "floorplan/current/v259_floorplan.html"


def pack(raw):
    return base64.b64encode(gzip.compress(raw, compresslevel=9, mtime=0)).decode("ascii")


def read_data(db):
    db.row_factory = sqlite3.Row
    labels = dict(custom_name="원본 이름", group_name="원본 그룹", facing="방향",
                  sprite_grid_pos="다칸 부품 위치", material="재질", material_type="재질 분류",
                  container_type="원본 저장소 유형", container_capacity="원본 저장 용량", solid="Solid")
    definitions = {r["source_key"]: {k:r[k] for k in labels if r[k] not in ("",None)}
                   for r in db.execute("SELECT * FROM v257_v255_join")}
    candidates = {r["candidate_id"]: dict(r) | {"keys":[]} for r in db.execute(
        "SELECT candidate_id,category,display_name,registered_name,evidence,name_status,storage_status FROM v258_furniture")}
    tiles = {}
    for candidate, key in db.execute("SELECT candidate_id,tile_id FROM v258_furniture_tile ORDER BY candidate_id,tile_id"):
        tiles.setdefault(key, []).append(candidate)
        candidates[candidate]["keys"].append(key)
    storage = {}
    for candidate,key,evidence,kind,capacity in db.execute("SELECT * FROM v258_storage_evidence"):
        storage.setdefault(key,{})[candidate] = [evidence,kind,capacity]
    assert len(definitions)==10042 and len(candidates)==2197 and len(tiles)==8130
    return dict(defs=definitions,candidates=candidates,tiles=tiles,storage=storage,labels=labels)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path)
    parser.add_argument("--sample", type=Path, default=ROOT/"B4220.3_MapExport_256/tmx/31_46.tmx")
    args = parser.parse_args()
    manifest = json.loads((ROOT/"analysis/current/v258/MANIFEST.json").read_text())
    if hashlib.sha256(args.database.read_bytes()).hexdigest() != manifest["sqlite_sha256"]:
        raise ValueError("Expected the published v258 SQLite")
    with sqlite3.connect(args.database.resolve().as_uri()+"?mode=ro",uri=True) as db:
        payload = read_data(db)
    html = (ROOT/"floorplan/current/v256_floorplan_unified_10042.html").read_text(encoding="utf8")
    def replace(old,new):
        nonlocal html
        if html.count(old)!=1:
            raise ValueError("Expected one template marker: "+old)
        html = html.replace(old,new)
    replace("v256 최신 통합 10,042종 평면도","v259 · 가구 통합 평면도")
    replace(">v256</span>",">v259</span>")
    replace("v256 최신 통합 타일 검색","타일 ID · 사물명 검색")
    replace('id="files" type','id="files" disabled type')
    replace('<div class="status" id="status">','<button class="smallbtn" disabled id="sampleMap">실제 맵 31_46 열기</button><div class="status" id="status">')
    replace('<div class="section"><h3>타일 ID', (HERE/"panel.html").read_text(encoding="utf8")+'<div class="section"><h3>타일 ID')
    replace('</style>', '''.f-filters{display:grid;gap:5px;margin-bottom:7px}.f-filters input,.f-filters select{width:100%;padding:7px;border:1px solid #bbccd7;border-radius:6px;background:white}
#fResults{display:grid;gap:4px;max-height:155px;overflow:auto;margin:5px 0}#fSelection{white-space:pre-line;margin:8px 0}#fResults [aria-pressed=true]{border-color:#945f19;background:#fff1c8}#sampleMap{margin-top:8px}</style>''')
    replace('v240 우선 10,042종 / 활성 9,587종','v258 통합 타일 10,042종 / 가구 후보 2,197개')
    replace("v256 · 최신 통합 10,042 · 사용자 68 우선 · 공식 인증 0","v258 타일 10,042 · 가구 후보 2,197")
    replace("status('v256 통합 정체 로드 완료", "await loadFurniture(); status('v258 정의·가구 로드 완료")
    replace('v243Inspect(items);v256Inspect(items);','v243Inspect(items);v256Inspect(items);inspectFurniture(items);')
    replace('v256MarkHeld(visible,show,v);','markFurniture(visible,show,v);v256MarkHeld(visible,show,v);')
    replace("function getLevel(el,path){const pp=properties(el);", """function getLevel(el,path){
      for (let node=el; node && node.nodeName!=='map'; node=node.parentElement) {
        const explicit=node.getAttribute('level') ?? node.getAttribute('z') ?? properties(node).Level ?? properties(node).level;
        if (explicit != null && /^-?[0-9]+$/.test(String(explicit))) return Number(explicit);
      }
      const pp=properties(el);""")
    replace('options.objects&&obj)drawObject(obj,c.x,c.y,v);','options.objects&&obj)drawObject(obj,c.x,c.y,v);if(options.objects)drawFurnitureSymbol(c,show,v);')
    replace('function v256MapStats(){','function v256MapStats(){\n if (indexedModel !== model) indexFurniture();')
    replace('"A_shape","user_choice","evidence_source"]','"A_shape","user_choice","evidence_source","v258_tile_properties","v258_furniture_and_storage"]')
    replace('r?.latest_visual_source||""].map','r?.latest_visual_source||"",...furnitureCsv(v256ItemKey(a))].map')
    replace('+"_v256.csv"','+"_v259.csv"')
    replace("disabledLayers.clear();selectFloor", "disabledLayers.clear();for (const layer of model.layers) if (!layer.visible) disabledLayers.add(layer.id);selectFloor")
    replace("!disabledLayers.has(a.layer.id)&&a.layer.visible", "!disabledLayers.has(a.layer.id)")
    replace('sizeCanvas();loadCatalog();', 'const FURNITURE_B64="'+pack(json.dumps(payload,ensure_ascii=False,separators=(",",":")).encode())+'";\nconst SAMPLE_B64="'+pack(args.sample.read_bytes())+'";\n'+(HERE/'furniture.js').read_text(encoding="utf8")+'\nsizeCanvas();loadCatalog();')
    OUTPUT.write_text(html,encoding="utf8")


if __name__=="__main__":
    main()
