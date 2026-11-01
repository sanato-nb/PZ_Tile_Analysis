#!/usr/bin/env python3
"""Rosewood manual batch 10: Source-verified 31 real Decocraft Blockbench .bbmodel
assets vs PZ original complete furniture images, NOT actual Minecraft game footage.
"""
import runpy
from pathlib import Path
p=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
env=runpy.run_path(str(p),run_name="batch10_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/10_091_100/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
  [
    "tv_old",
    "Television",
    "Antique"
  ],
  [
    "crt_tv",
    "Television",
    "Antique"
  ],
  [
    "tv_small",
    "Television",
    "Antique"
  ],
  [
    "bottom_cabinet_1_birch",
    "Counter",
    "Generic Shop"
  ],
  [
    "bottom_cabinet_1_oak",
    "Counter",
    "Generic Shop"
  ],
  [
    "diner_counter_yellow",
    "Counter",
    "Generic Shop"
  ],
  [
    "single_bed_black_white",
    "Bed",
    "Fancy"
  ],
  [
    "single_bed_birch_white",
    "Bed",
    "Fancy"
  ],
  [
    "single_bed_spruce_white",
    "Bed",
    "Fancy"
  ],
  [
    "single_bed_black_light_gray",
    "Bed",
    "Fancy"
  ],
  [
    "bamboo_coffee_table_round_yellow",
    "Light Round Table",
    ""
  ],
  [
    "diner_table_round_yellow",
    "Light Round Table",
    ""
  ],
  [
    "diner_table_round_black",
    "Light Round Table",
    ""
  ],
  [
    "vanity_center_birch",
    "Drawers",
    "Mirror And"
  ],
  [
    "vanity_left_birch",
    "Drawers",
    "Mirror And"
  ],
  [
    "vanity_right_birch",
    "Drawers",
    "Mirror And"
  ],
  [
    "closet_3_birch",
    "Drawers",
    "Mirror And"
  ],
  [
    "standing_mirror_birch",
    "Drawers",
    "Mirror And"
  ],
  [
    "cottage_coffee_table",
    "Low Table",
    "White"
  ],
  [
    "wooden_table_white",
    "Low Table",
    "White"
  ],
  [
    "bamboo_coffee_table_square_yellow",
    "Low Table",
    "White"
  ],
  [
    "toaster_silver",
    "Toaster",
    "Small Chrome"
  ],
  [
    "toaster_cream",
    "Toaster",
    "Small Chrome"
  ],
  [
    "toaster_black",
    "Toaster",
    "Small Chrome"
  ],
  [
    "chair_1_cherry",
    "Chair",
    "Pile o' Crepe"
  ],
  [
    "chair_1_palm",
    "Chair",
    "Pile o' Crepe"
  ],
  [
    "chair_2_cherry",
    "Chair",
    "Pile o' Crepe"
  ],
  [
    "school_chair_orange",
    "Chair",
    "Pile o' Crepe"
  ],
  [
    "diner_chair_orange",
    "Chair",
    "Pile o' Crepe"
  ],
  [
    "picnic_table",
    "Table",
    "Picknic"
  ],
  [
    "picnic_basket",
    "Table",
    "Picknic"
  ]
]
if __name__=="__main__":env["main"]()
