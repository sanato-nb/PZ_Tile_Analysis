#!/usr/bin/env python3
"""Rosewood 13th manual batch: render 32 actual Forge 1.20.1 Decocraft native
BBMODEL candidates for complete Project Zomboid furniture 121..130.
Only actual source-model screenshot evidence is stored, not inferred geometry.
"""
import runpy
from pathlib import Path
p=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
env=runpy.run_path(str(p),run_name="batch13_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/13_121_130/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
  [
    "fridge_small_silver",
    "Fridge",
    "Steel"
  ],
  [
    "fridge_large",
    "Fridge",
    "Steel"
  ],
  [
    "fridge_small_cream",
    "Fridge",
    "White"
  ],
  [
    "fridge_small_mint",
    "Fridge",
    "White"
  ],
  [
    "bottom_cabinet_1_oak",
    "Counter",
    "Bar"
  ],
  [
    "bottom_cabinet_1_spruce",
    "Counter",
    "Bar"
  ],
  [
    "diner_counter_yellow",
    "Counter",
    "Bar"
  ],
  [
    "armchair_cream",
    "Chair",
    "Fancy White"
  ],
  [
    "armchair_white",
    "Chair",
    "Fancy White"
  ],
  [
    "cottage_armchair",
    "Chair",
    "Fancy White"
  ],
  [
    "beach_chair_blue",
    "Chair",
    "Beach"
  ],
  [
    "beach_chair_light_blue",
    "Chair",
    "Beach"
  ],
  [
    "beach_chair_white",
    "Chair",
    "Beach"
  ],
  [
    "armchair_green",
    "Chair",
    "Green Comfy"
  ],
  [
    "armchair_lime",
    "Chair",
    "Green Comfy"
  ],
  [
    "armchair_gray",
    "Chair",
    "Green Comfy"
  ],
  [
    "bottom_cabinet_corner_outer_1_oak",
    "Counter",
    "Oak Corner"
  ],
  [
    "bottom_cabinet_corner_outer_2_oak",
    "Counter",
    "Oak Corner"
  ],
  [
    "bottom_cabinet_corner_inner_oak",
    "Counter",
    "Oak Corner"
  ],
  [
    "bottom_cabinet_corner_outer_1_white",
    "Counter",
    "White Corner"
  ],
  [
    "bottom_cabinet_corner_outer_2_white",
    "Counter",
    "White Corner"
  ],
  [
    "bottom_cabinet_corner_inner_white",
    "Counter",
    "White Corner"
  ],
  [
    "armchair_light_blue",
    "Chair",
    "Light Blue"
  ],
  [
    "armchair_ocean_blue",
    "Chair",
    "Light Blue"
  ],
  [
    "armchair_cyan",
    "Chair",
    "Light Blue"
  ],
  [
    "couch_left_light_blue",
    "Couch",
    "Light Blue"
  ],
  [
    "couch_middle_light_blue",
    "Couch",
    "Light Blue"
  ],
  [
    "couch_right_light_blue",
    "Couch",
    "Light Blue"
  ],
  [
    "couch_left_cream",
    "Couch",
    "Light Blue"
  ],
  [
    "couch_right_cream",
    "Couch",
    "Light Blue"
  ],
  [
    "couch_left_gray",
    "Couch",
    "Light Blue"
  ]
]
if __name__=="__main__":env["main"]()
