#!/usr/bin/env python3
"""Independently verify original Decocraft models for PZ 221–230 using actual Blockbench 5.2.2.
Never approve game placement or 1:1 equivalence from screenshots alone."""
from pathlib import Path
import runpy
env=runpy.run_path(str(Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")),run_name="batch23_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/23_221_230/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
 ["diner_counter_corner_green","Counter","Green Corner"],
 ["dish_rack_white","Shelves","White Wall"],
 ["diner_table_black","Table","Black Low Modern"],
 ["bunk_bed_birch_black","Beds","Twin"]
]
if __name__=="__main__":env["main"]()
