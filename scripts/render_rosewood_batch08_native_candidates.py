#!/usr/bin/env python3
"""Batch 08: render twenty-seven original Decocraft 1.20.1 Forge .bbmodel alternatives
in pinned Blockbench 5.2.2. Native source/variant hashes and models, no fake screenshots.
"""
import runpy
from pathlib import Path
p=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
env=runpy.run_path(str(p),run_name="batch08_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/08_071_080/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
  [
    "diner_table_light_gray",
    "Table",
    "Light Wood Restaurant"
  ],
  [
    "diner_table_yellow",
    "Table",
    "Light Wood Restaurant"
  ],
  [
    "diner_table_round_black",
    "Table",
    "Light Wood Restaurant"
  ],
  [
    "diner_table_round_yellow",
    "Table",
    "Light Wood Restaurant"
  ],
  [
    "wooden_table_birch",
    "Table",
    "Light Wood Restaurant"
  ],
  [
    "chair_1_white",
    "Chair",
    "White Simple"
  ],
  [
    "chair_1_white_alt",
    "Chair",
    "White Simple"
  ],
  [
    "chair_2_white",
    "Chair",
    "White Simple"
  ],
  [
    "school_chair_white",
    "Chair",
    "White Simple"
  ],
  [
    "lunch_box_red",
    "Cabinet",
    "First Aid"
  ],
  [
    "pedal_trash_can",
    "Bin",
    "Grey Garbage"
  ],
  [
    "trash_can",
    "Bin",
    "Grey Garbage"
  ],
  [
    "trash_can_open",
    "Bin",
    "Grey Garbage"
  ],
  [
    "pedal_trash_can_open",
    "Bin",
    "Grey Garbage"
  ],
  [
    "dumpster",
    "Dumpster",
    "Orange"
  ],
  [
    "lunch_box_gray",
    "Chest",
    "Small"
  ],
  [
    "lunch_box_black",
    "Chest",
    "Small"
  ],
  [
    "lunch_box_light_gray",
    "Chest",
    "Small"
  ],
  [
    "microwave",
    "Microwave",
    "Chrome"
  ],
  [
    "bottom_cabinet_corner_inner_oak",
    "Counter",
    "Wooden Corner"
  ],
  [
    "bottom_cabinet_corner_outer_1_oak",
    "Counter",
    "Wooden Corner"
  ],
  [
    "bottom_cabinet_corner_outer_2_oak",
    "Counter",
    "Wooden Corner"
  ],
  [
    "bottom_cabinet_1_oak",
    "Counter",
    "Trailer"
  ],
  [
    "bottom_cabinet_1_birch",
    "Counter",
    "Trailer"
  ],
  [
    "bottom_cabinet_island_oak",
    "Counter",
    "Trailer"
  ],
  [
    "stove",
    "Oven",
    "Grey"
  ],
  [
    "pizza_oven",
    "Oven",
    "Grey"
  ]
]
if __name__=="__main__":env["main"]()
