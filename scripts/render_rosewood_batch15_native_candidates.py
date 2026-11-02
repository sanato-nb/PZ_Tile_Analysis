#!/usr/bin/env python3
"""Native Blockbench candidates for 141-150; no approval from a screenshot alone."""
from pathlib import Path
import runpy
env=runpy.run_path(str(Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")),run_name="batch15_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/15_141_150/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
 ["couch_left_light_blue","Couch","White Lazy"],
 ["couch_right_light_blue","Couch","White Lazy"],
 ["bottom_cabinet_1_oak","Counter","Green"],
 ["dumpster","Dumpster","Blue"],
 ["fridge_small_cream","Fridge","Plain"],
 ["bathroom_counter_left_white","Counter","Low Motel"],
 ["cottage_armchair","Chair","Blue Comfy"],
 ["couch_left_ocean_blue","Couch","Green Comfy"],
 ["couch_right_ocean_blue","Couch","Green Comfy"],
 ["piano_bench_spruce","Low Table","Long"],
 ["top_cabinet_3_oak","Shelves","Lightwood Wall"],
 ["bottom_cabinet_2_white","Wardrobe","Fancy White"]
]
if __name__=="__main__":env["main"]()
