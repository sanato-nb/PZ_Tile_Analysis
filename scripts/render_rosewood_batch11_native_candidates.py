#!/usr/bin/env python3
"""Batch 11 — original Decocraft BBMODEL / variant texture provenance and native desktop renderer.
This is independent of 12th and 13th groups; never touch source data.
"""
import runpy
from pathlib import Path
p=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
env=runpy.run_path(str(p),run_name="batch11_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/11_101_110/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[["closet_5_ebony","Wardrobe","Fancy Oak"],["closet_5_oak","Wardrobe","Fancy Oak"],["closet_6_oak","Wardrobe","Fancy Oak"],["closet_6_ebony","Wardrobe","Fancy Oak"],["filing_cabinet_white","Cabinet","Grey File"],["filing_cabinet_black","Cabinet","Grey File"],["display_counter_bottom_oak","Counter","Shop Display"],["display_counter_bottom_spruce","Counter","Shop Display"],["display_counter_bottom_white","Counter","Shop Display"],["couch_left_leather_brown","Couch","Brown Lazy"],["couch_right_leather_brown","Couch","Brown Lazy"],["couch_middle_leather_brown","Couch","Brown Lazy"],["cottage_couch_left","Couch","Brown Lazy"],["cottage_couch_right","Couch","Brown Lazy"],["wooden_table_white","Table","Large Plastic"],["kitchen_table_white","Table","Large Plastic"],["diner_table_light_gray","Table","Large Plastic"],["trash_can","Public Garbage Bin",""],["trash_can_open","Public Garbage Bin",""],["waste_basket_black","Public Garbage Bin",""],["armchair_leather_brown","Chair","Brown Lazy"],["cottage_armchair","Chair","Brown Lazy"],["microwave","Microwave","White"],["piano_upright_spruce","Piano","Western"],["piano_spruce","Piano","Western"],["piano_upright_black","Piano","Western"]]
if __name__=="__main__":env["main"]()
