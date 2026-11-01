#!/usr/bin/env python3
"""Batch 10: 29 original Decocraft 1.20.1 Forge BBMODEL + source PNG renders with
pinned desktop Blockbench 5.2.2, before 091-100 independent PZ visual matching.
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
    "tv_small",
    "Television",
    "Antique"
  ],
  [
    "tv_large",
    "Television",
    "Antique"
  ],
  [
    "diner_counter_light_gray",
    "Counter",
    "Generic Shop"
  ],
  [
    "diner_counter_yellow",
    "Counter",
    "Generic Shop"
  ],
  [
    "bottom_cabinet_1_birch",
    "Counter",
    "Generic Shop"
  ],
  [
    "single_bed_black_white",
    "Bed",
    "Fancy"
  ],
  [
    "single_bed_black_light_gray",
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
    "diner_table_round_yellow",
    "Light Round Table",
    ""
  ],
  [
    "bamboo_coffee_table_round_yellow",
    "Light Round Table",
    ""
  ],
  [
    "diner_table_round_gray",
    "Round Table",
    ""
  ],
  [
    "vanity_center_oak",
    "Drawers",
    "Mirror And"
  ],
  [
    "vanity_center_birch",
    "Drawers",
    "Mirror And"
  ],
  [
    "vanity_left_oak",
    "Drawers",
    "Mirror And"
  ],
  [
    "vanity_right_oak",
    "Drawers",
    "Mirror And"
  ],
  [
    "bedside_table_oak",
    "Drawers",
    "Mirror And"
  ],
  [
    "cottage_coffee_table",
    "Low Table",
    "White"
  ],
  [
    "bedside_table_white",
    "Low Table",
    "White"
  ],
  [
    "wooden_table_white",
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
    "chair_2_cherry",
    "Chair",
    "Pile o' Crepe"
  ],
  [
    "chair_1_oak",
    "Chair",
    "Pile o' Crepe"
  ],
  [
    "chair_2_oak",
    "Chair",
    "Pile o' Crepe"
  ],
  [
    "picnic_table",
    "Table",
    "Picnic"
  ]
]
if __name__=="__main__":env["main"]()
