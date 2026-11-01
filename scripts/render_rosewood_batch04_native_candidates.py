#!/usr/bin/env python3
"""Batch 04: execute the proven real Blockbench model renderer with new test IDs."""
import runpy
from pathlib import Path
p=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
env=runpy.run_path(str(p),run_name="batch04_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/04_031_040/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
("bottom_cabinet_1_ebony","Counter","Wooden"),
("bottom_cabinet_1_spruce","Counter","Wooden"),
("coffee_grinder","X-press","Coffee"),
("kitchen_sink_silver","Sink","Chrome"),
("square_sink_silver","Sink","Chrome"),
("chair_1_ebony","Chair","Fancy Wooden"),
("chair_1_cherry","Chair","Fancy Wooden"),
("chair_1_white","Chair","White Wooden"),
("chair_2_white","Chair","White Wooden"),
("china_cabinet_open_white","Shelves","White Fancy"),
("bedside_table_open_1_oak","Drawers","Bedroom"),
("bedside_table_open_2_oak","Drawers","Bedroom"),
("bedside_table_open_1_birch","Drawers","Bedroom"),
("wooden_table_oak","Table","Small"),
("wooden_table_cherry","Table","Small"),
("decobench","Bench","Oakwood"),
("piano_bench_spruce","Bench","Oakwood"),
("modular_desk_storage_white","Shelves","White Fancy"),
]
if __name__=="__main__":env["main"]()
