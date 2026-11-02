#!/usr/bin/env python3
"""Lane A 221-230: inspect ten original Decocraft source BBMODEL variants in native Blockbench.
No geometry is invented and no in-game 1:1 approval is implied."""
from pathlib import Path
import runpy
env=runpy.run_path(str(Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")),run_name="batch22_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/22_221_230/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
 ["beach_chair_purple","Chair","Purple Rattan"],
 ["beach_chair_red","Chair","Red Comfy"],
 ["couch_corner_purple","Couch","Purple Rattan"],
 ["bamboo_couch_left_yellow","Couch","Yellow Modern"],
 ["diner_counter_corner_green","Counter","Green Corner"],
 ["bottom_cabinet_2_oak","Counter","Hardwood Floating"],
 ["dish_rack_white","Shelves","White Wall"],
 ["diner_table_black","Table","Black Low Modern"],
 ["bunk_bed_birch_black","Beds","Twin"],
 ["school_chair_blue","Chair","Darkblue Modern"]
]
if __name__=="__main__":env["main"]()
