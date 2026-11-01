#!/usr/bin/env python3
"""Batch 12 (111-120): source-authentic Decocraft 3.0.4 Forge 1.20.1 BBMODEL+texture
in desktop Blockbench 5.2.2. The results are comparison evidence, not in-game approval.
"""
import runpy
from pathlib import Path
p=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
env=runpy.run_path(str(p),run_name="batch12_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/12_111_120/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[["double_bed_black_white","Bed","Large Fancy"],["double_bed_black_light_gray","Bed","Large Fancy"],["double_bed_black_gray","Bed","Large Fancy"],["double_bed_birch_white","Bed","Large Fancy"],["fridge_small_black","Fridge","Mini"],["fridge_small_silver","Fridge","Mini"],["fridge_small_cream","Fridge","Mini"],["laundry_basket_rattan","Bin","Washing"],["rolling_bin_yellow","Bin","Washing"],["rolling_bin_blue","Bin","Washing"],["bedside_table_black","Drawers","Dark Fancy"],["bedside_table_ebony","Drawers","Dark Fancy"],["modular_desk_drawers_black","Drawers","Dark Fancy"],["modular_desk_drawers_ebony","Drawers","Dark Fancy"],["wooden_table_ebony","Table","Large Dark Oak"],["wooden_table_spruce","Table","Large Dark Oak"],["kitchen_table_ebony","Table","Large Dark Oak"],["wooden_table_cherry","Table","Large Dark Oak"],["fridge_large","Fridge","Industrial"],["fridge_large_open_full","Fridge","Industrial"],["vending_machine_soda","Fridge","Industrial"],["fridge_small_open_top_silver","Fridge","White Industrial"],["fridge_small_open_bottom_silver","Fridge","White Industrial"],["crt_tv","Television","Premium Technologies"],["tv_small","Television","Premium Technologies"],["tv_wall_small","Television","Premium Technologies"],["tv_large","Television","Premium Technologies"],["tv_wall_large","Television","Premium Technologies"],["bottom_cabinet_corner_inner_oak","Counter","Modern Corner"],["bottom_cabinet_corner_inner_ebony","Counter","Modern Corner"],["bottom_cabinet_corner_outer_1_oak","Counter","Modern Corner"],["bottom_cabinet_corner_outer_1_ebony","Counter","Modern Corner"],["bottom_cabinet_corner_outer_2_oak","Counter","Modern Corner"]]
if __name__=="__main__":env["main"]()
