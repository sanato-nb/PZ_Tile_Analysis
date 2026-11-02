#!/usr/bin/env python3
"""Native Decocraft 3.0.4 Forge 1.20.1 candidates for Rosewood manual review 161-170.
Use verified official Blockbench 5.2.2 screenshots. Models are not automatically approved.
"""
from pathlib import Path
import runpy
env=runpy.run_path(str(Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")),run_name="batch17_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/17_161_170/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
 ["treadmill","Hamster Wheel","Human"],
 ["locker_blue","Locker","Blue Wall"],
 ["gym_bench","Bench","Sturdy"],
 ["modular_desk_drawers_oak","Desk","Lightwood"],
 ["kitchen_sink_silver","Sink","Large Industrial"],
 ["piano_bench_spruce","Stool","Piano"],
 ["piano_bench_white","Stool","Piano"],
 ["single_bed_birch_blue","Bed","Blue"],
 ["fridge_small_cream","Fridge","Green"]
]
if __name__=="__main__":env["main"]()
