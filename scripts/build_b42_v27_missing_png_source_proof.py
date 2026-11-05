#!/usr/bin/env python3
"""v27 part 1: preserve v26 SQLite, prove 23 exact absent original PNG atlases (89 source tile keys).
Missing a provided source file is not evidence that the game sprite does not exist.
"""
from pathlib import Path
from collections import Counter
import csv,sqlite3,json,zipfile,shutil,subprocess,hashlib
R=Path(__file__).resolve().parents[1]
BASE=R/"analysis/furniture_full_b42/2026-11-05/all_multitile_visual_v26/B42_FURNITURE_SOURCE_GRID_VISUAL_V26.zip"
O=R/"analysis/furniture_full_b42/2026-11-05/missing_atlas_warning_v27"
DB=O/"B42_FURNITURE_SOURCE_AUDIT_V27.sqlite"
def select(c,q):return [dict(r) for r in c.execute(q)]
def put(c,t,row):
 cols=list(row);c.execute("INSERT INTO "+t+"("+",".join(cols)+") VALUES("+",".join("?" for _ in cols)+")",list(row.values()))
def dump(n,data):
 with (O/n).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
def J(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def main():
 assert BASE.exists() and not DB.exists()
 O.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(BASE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_SOURCE_GRID_VISUAL_V26.sqlite") as i,DB.open("wb") as o:shutil.copyfileobj(i,o)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for t,n in {"source_attributes":195265,"source_slots":73644,"furniture_tile":8219,
  "registry_entry":2231,"v13_warning_case":474,"v14_source_only_ledger":963,
  "v20_23_original_atlas_filename_audit":23,
  "v26_all_820_source_direction_grid_visual_evidence":820}.items():
  assert c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]==n,t
 git=subprocess.run(["git","ls-tree","-r","--name-only","HEAD","Tiles/2x"],cwd=R,text=True,capture_output=True,check=True).stdout
 paths={line.strip() for line in git.splitlines() if line.strip().endswith(".png")}
 assert len(paths)>350
 source={x["source_key"]:x for x in select(c,"SELECT source_key,group_id,SpriteGridPos FROM furniture_tile")}
 ledger={x["entry_id"]:x for x in select(c,"SELECT * FROM v14_source_only_ledger")}
 missing=select(c,"SELECT * FROM v20_23_original_atlas_filename_audit ORDER BY entry_id")
 assert len(missing)==23
 c.executescript("""
 CREATE TABLE v27_missing_atlas_group(
  entry_id TEXT PRIMARY KEY,group_id TEXT,original_name TEXT,source_tileset TEXT,
  expected_png_path TEXT,source_tile_keys_json TEXT,source_part_count INTEGER,
  exact_png_present_in_git_source_tree INTEGER,prior_indexed_sprite_cells INTEGER,
  nearest_neighbor_png_name_hints_NOT_equivalent_json TEXT,blocker_class TEXT,
  original_png_mapping_resolved INTEGER DEFAULT 0,game_object_identity_certified INTEGER DEFAULT 0);
 CREATE TABLE v27_missing_atlas_source_key(
  entry_id TEXT,group_id TEXT,source_key TEXT,local_id INTEGER,raw_grid TEXT,
  missing_exact_atlas_path TEXT,raw_tiledef_verified INTEGER DEFAULT 1,
  exact_original_png_pixel_recovered INTEGER DEFAULT 0,PRIMARY KEY(entry_id,source_key));
 CREATE TABLE v27_three_absent_atlas_filenames(
  filename TEXT PRIMARY KEY,source_groups INTEGER,source_tile_keys INTEGER,
  exact_git_png_present INTEGER DEFAULT 0,
  substitute_asset_equivalence_proven INTEGER DEFAULT 0);
 """)
 counts=Counter();keycounts=Counter();items=[];tileitems=[]
 for m in missing:
  ident=m["entry_id"];s=ledger[ident]
  assert s["group_id"]==m["source_group_id"]
  assert int(s["image_mapping_present"])==0
  sets=json.loads(m["original_tilesets_json"])
  assert len(sets)==1
  t=sets[0]
  assert t in ("crafted_03","lighting_indoor_01_on","e_newsnow_ground_1"),t
  expected="Tiles/2x/"+t+".png"
  assert expected not in paths
  assert json.loads(m["expected_png_filenames_json"])==[t+".png"]
  assert json.loads(m["exact_expected_png_assets_in_current_repo_json"])==[]
  assert int(m["source_image_cell_matches_in_prior_db"])==0
  ks=json.loads(s["original_tile_ids_json"])
  assert len(ks)==int(s["original_tile_count"]) and ks
  assert all(k.startswith(t+"/") and k in source and source[k]["group_id"]==s["group_id"] for k in ks)
  category={"crafted_03":"MISSING_CRAFTED_ATLAS",
   "lighting_indoor_01_on":"MISSING_LAMP_ON_STATE_ATLAS",
   "e_newsnow_ground_1":"MISSING_SNOW_GROUND_ATLAS_POSSIBLE_NONFURNITURE"}[t]
  rec=dict(entry_id=ident,group_id=s["group_id"],original_name=m["original_name"],
   source_tileset=t,expected_png_path=expected,source_tile_keys_json=J(ks),
   source_part_count=len(ks),exact_png_present_in_git_source_tree=0,
   prior_indexed_sprite_cells=0,
   nearest_neighbor_png_name_hints_NOT_equivalent_json=m["possible_neighbor_or_state_alias_assets_json"],
   blocker_class=category)
  put(c,"v27_missing_atlas_group",rec);items.append(rec);counts[t]+=1;keycounts[t]+=len(ks)
  for key in ks:
   rr=dict(entry_id=ident,group_id=s["group_id"],source_key=key,
    local_id=int(key.rsplit("/",1)[-1]),raw_grid=source[key]["SpriteGridPos"] or "",
    missing_exact_atlas_path=expected)
   put(c,"v27_missing_atlas_source_key",rr);tileitems.append(rr)
 assert len(items)==23 and len(tileitems)==89
 assert dict(counts)=={"crafted_03":17,"lighting_indoor_01_on":5,"e_newsnow_ground_1":1}
 assert dict(keycounts)=={"crafted_03":17,"lighting_indoor_01_on":24,"e_newsnow_ground_1":48}
 types=[]
 for t in sorted(counts):
  rr=dict(filename=t+".png",source_groups=counts[t],source_tile_keys=keycounts[t])
  put(c,"v27_three_absent_atlas_filenames",rr);types.append(rr)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 c.close()
 dump("V27_23_MISSING_PNG_GROUPS_EXACT_EVIDENCE.csv",items)
 dump("V27_89_SOURCE_TILE_KEYS_WITH_ABSENT_ATLAS.csv",tileitems)
 dump("V27_3_ABSENT_ATLAS_FILENAMES.csv",types)
 manifest=dict(original_v26_zip_sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
  exact_github_git_tiles2x_png_entries=len(paths),source_group_count=23,
  original_missing_source_tile_keys=89,distinct_missing_exact_atlas_filenames=3,
  groups_by_atlas=dict(counts),tile_keys_by_atlas=dict(keycounts),
  exact_game_sprite_pixels_recovered=0,
  original_missing_source_groups_resolved=0,
  user_connected_google_drive_2x_inventory_also_lacks_three_exact_names=True,
  drive_check_is_external_metadata_evidence_not_ci_verified=True)
 (O/"V27_PNG_STAGE_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 print("V27_PNG_SOURCE_23_GROUPS_89_KEYS_3_EXACT_ATLASES_ABSENT",J(manifest))
if __name__=="__main__":main()
