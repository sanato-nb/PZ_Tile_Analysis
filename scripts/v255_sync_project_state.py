#!/usr/bin/env python3
"""Update central state after v255 artifacts verified; retain all historical entries unchanged."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
statep=R/"PROJECT_STATE.json"
j=json.loads(statep.read_text("utf-8"))
v255=json.loads((R/"review/v255_latest_integrated_10042_2026-10-30/MANIFEST.json").read_text("utf-8"))
db=json.loads((R/"analysis/current/v255/MANIFEST.json").read_text("utf-8"))
floor=json.loads((R/"floorplan/current/MANIFEST_V255.json").read_text("utf-8"))
assert (v255["total_keys"],v255["active_unchanged"],v255["excluded_unchanged"])==(10042,9587,455)
assert (db["table_count"],db["parent_table_count"],db["integrity_check"])==(260,258,"ok")
assert (floor["held_latest_visual_candidates"],floor["latest_user_choices"])==(439,68)
assert j["latest_checkpoint"]["version"]=="v240" and j["unified_database"]["version"]=="v240"
j["previous_checkpoint_v240"]=j["latest_checkpoint"]
j["previous_unified_database_v240"]=j["unified_database"]
j["previous_next_actions_v240"]=j["next_actions"]
j["latest_checkpoint"]=dict(version="v255",date="2026-10-30",
 kind="latest visual candidate integration of held439 and user68, source statuses unchanged",
 expanded_84_tmx_unique_total=10042,
 expanded_unique_observed=10007,expanded_unique_unobserved=35,
 expanded_observation_percent=10007/10042*100,
 integrated_source_keys=10042,
 active_source_keys=9587,inactive_source_keys=455,
 held_439=439,latest_439_visual_notes=439,
 user68_explicit_identified=4,user68_explicit_part_only=12,
 user68_implicit_agreement=52,user68_newly_official_certified=0,
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 evidence_repo_path=v255["new_preferred_master"],
 evidence_manifest="review/v255_latest_integrated_10042_2026-10-30/MANIFEST.json",
 physical_db_manifest="analysis/current/v255/MANIFEST.json",
 floorplan_html=floor["output_html"],
 note="v255 changes visual/provisional metadata only; historically observed10007/10042 and archive455 remain unchanged, no world conversion/official ID")
j["unified_database"]=dict(version="v255",status="VERIFIED",
 repo_manifest="analysis/current/v255/MANIFEST.json",
 restore_script="scripts/restore_v255_master.py",
 sqlite_sha256=db["new_sqlite_sha256"],
 compressed_sha256=db["zlib_sha256"],
 sqlite_bytes=db["new_sqlite_bytes"],
 table_count=260,original_v240_table_count=258,
 combined_unique=10042,active_unique=9587,inactive_unique=455,
 held_visual_overlay_count=439,user_manual_priority_count=68,
 certified=0,mapping_verified=0,tilezed_verified=0,
 original_source_preserved=True,
 integrity_check="ok",parent_tables_row_counts_equal=True,
 verification_provenance="CI source bytes original v240 SHA, sqlite backup parent tables, 439+68 overlay rows, full 10042 master")
j["latest_v255_integrated_results"]=dict(
 source_versions=["v240","v248","v249","v250","v251","v252","v254"],
 all_master=v255["new_preferred_master"],
 held439="review/v255_latest_integrated_10042_2026-10-30/HELD439_LATEST_VISUAL_USER_PRIORITY.csv",
 user68="review/v255_latest_integrated_10042_2026-10-30/USER68_EFFECTIVE_ROWS.csv",
 physical_sqlite_parts_manifest="analysis/current/v255/MANIFEST.json",
 latest_floorplan=floor["output_html"],
 latest_floorplan_manifest="floorplan/current/MANIFEST_V255.json",
 user_priority="explicit user choice > user approved earlier provisional for empty choice > v252 > v251 > v250/v249/v248; held flag unchanged",
 latest_A_BC_provisional_not_official=True,
 external_world_export_completed=False,
 official_tile_local_id_certifications=0)
j["next_actions"]=[
 "Use v255 10042 preferred master and the v255 floorplan HTML as current; v243 kept for provenance.",
 "Keep historical inactive439+manual16 archived until explicit separately authorized state promotion; latest names can be read in inspector but do not create final Minecraft blocks.",
 "Differentiate v254 user 16 explicit choices / 52 implicit agreement; original user CSV and prior AI A/B evidence unchanged.",
 "Verify official B42 tile identity and exact orientation/connected multi-sprite objects and Minecraft full block-width wall conversion separately; final identity certifications 0.",
 "Preserve all previous 258 v240 tables, 84 TMX, Tiles PNG, earlier manual reviews, v240 CSV and all prior commits."
]
statep.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
again=json.loads(statep.read_text("utf-8"))
assert again["previous_checkpoint_v240"]["version"]=="v240"
assert again["latest_v240_physical_master"]==j["latest_v240_physical_master"]
assert again["latest_checkpoint"]["version"]=="v255"
print("PASS project state synced v255, all original history entries retained, sqlite260/439+68/10042; filesize",statep.stat().st_size)
