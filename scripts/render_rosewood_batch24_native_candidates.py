#!/usr/bin/env python3
"""Lane B 231-240: open 10 real Decocraft source BBMODEL variants in official Blockbench.
No candidate is approved for in-game use from this renderer alone.
"""
from pathlib import Path
import runpy
env=runpy.run_path(str(Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")),run_name="batch24_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/24_231_240/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
 ["couch_corner_red","Couch","Red Comfy"],
 ["bathroom_counter_left_oak","Counter","Oak Floating"],
 ["lamp_cable_base_black_green","Lamp","Fancy Green"],
 ["sink_cabinet_white","Sink","Fancy Hanging"],
 ["kitchen_table_oak","Table","Long Oak"],
 ["bottom_cabinet_1_white","Counter","Pie Store"],
 ["double_bed_oak_white","Bed","Hospital"],
 ["gym_bench","Bench","Long Wooden"],
 ["beach_chair_gray","Chair","Rocking"],
 ["couch_corner_leather_brown","Couch","Victorian C5"]
]
if __name__=="__main__":env["main"]()
