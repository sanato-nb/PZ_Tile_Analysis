#!/usr/bin/env python3
"""Rosewood manual batch 14: render 33 original Decocraft Forge 1.20.1 source BBMODEL
and PNG variant assets inside Blockbench 5.2.2; source hashes and images only.
No standalone model asset is treated as a game-installed 1:1 certified replacement.
"""
import runpy
from pathlib import Path
p=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
env=runpy.run_path(str(p),run_name="batch14_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/14_131_140/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
  [
    "fridge_small_cream",
    "Freezer",
    "Chest"
  ],
  [
    "fridge_small_silver",
    "Freezer",
    "Chest"
  ],
  [
    "fridge_large",
    "Freezer",
    "Chest"
  ],
  [
    "fridge_small_open_bottom_cream",
    "Fridge",
    "Build-in Trailer"
  ],
  [
    "fridge_small_open_top_silver",
    "Fridge",
    "Build-in Trailer"
  ],
  [
    "armchair_black",
    "Chair",
    "Black Fancy"
  ],
  [
    "armchair_dark_gray",
    "Chair",
    "Black Fancy"
  ],
  [
    "armchair_leather_black",
    "Chair",
    "Black Fancy"
  ],
  [
    "armchair_leather_brown",
    "Chair",
    "Black Fancy"
  ],
  [
    "stove",
    "Oven",
    "Green"
  ],
  [
    "toilet_mint",
    "Oven",
    "Green"
  ],
  [
    "single_bed_oak_white",
    "Bed",
    "Simple"
  ],
  [
    "single_bed_spruce_white",
    "Bed",
    "Simple"
  ],
  [
    "single_bed_birch_white",
    "Bed",
    "Simple"
  ],
  [
    "piano_bench_spruce",
    "Bench",
    "Birchwood"
  ],
  [
    "piano_bench_white",
    "Bench",
    "Birchwood"
  ],
  [
    "picnic_table",
    "Bench",
    "Birchwood"
  ],
  [
    "armchair_cream",
    "Chair",
    "White Lazy"
  ],
  [
    "armchair_white",
    "Chair",
    "White Lazy"
  ],
  [
    "cottage_armchair",
    "Chair",
    "White Lazy"
  ],
  [
    "toilet_white",
    "Toilet",
    "Low"
  ],
  [
    "toilet_aqua",
    "Toilet",
    "Low"
  ],
  [
    "top_cabinet_1_oak",
    "Counter",
    "Floating Trailer"
  ],
  [
    "top_cabinet_2_oak",
    "Counter",
    "Floating Trailer"
  ],
  [
    "top_cabinet_3_oak",
    "Counter",
    "Floating Trailer"
  ],
  [
    "top_cabinet_4_oak",
    "Counter",
    "Floating Trailer"
  ],
  [
    "bottom_cabinet_1_oak",
    "Counter",
    "Floating Trailer"
  ],
  [
    "couch_left_ocean_blue",
    "Couch",
    "Blue Comfy"
  ],
  [
    "couch_right_ocean_blue",
    "Couch",
    "Blue Comfy"
  ],
  [
    "couch_left_cyan",
    "Couch",
    "Blue Comfy"
  ],
  [
    "couch_right_cyan",
    "Couch",
    "Blue Comfy"
  ],
  [
    "couch_left_light_blue",
    "Couch",
    "Blue Comfy"
  ],
  [
    "couch_right_light_blue",
    "Couch",
    "Blue Comfy"
  ]
]
if __name__=="__main__":env["main"]()
