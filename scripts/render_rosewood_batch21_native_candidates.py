#!/usr/bin/env python3
"""Independent lane B 201-210: native Blockbench renders of actual Decocraft source assets.
Never approve based on a partial or failed viewport. Source mod JAR is SHA-512 verified."""
from pathlib import Path
import runpy
env=runpy.run_path(str(Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")),run_name="batch21_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/21_201_210/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
 ["pizza_oven","Oven","Large Modern"],
 ["diner_table_black","Table","Large Dark"],
 ["wooden_table_oak","Table","Large Dark"],
 ["school_chair_gray","Chair","Makeshift"],
 ["kitchen_table_oak","Table","Lightwood Trailer"],
 ["grill_black","Barbecue","Jorge Foreguy"],
 ["bamboo_chair_yellow","Chair","Yellow Modern"],
 ["diner_counter_corner_black","Counter","Dark Corner"]
]
if __name__=="__main__":env["main"]()
