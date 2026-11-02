#!/usr/bin/env python3
"""Second pass: use official Blockbench, same verified source BBMODEL, wider camera.
Does not modify original native proof or any global data.
"""
from pathlib import Path
import runpy
original=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
wrapper=Path(__file__).with_name("render_rosewood_batch24_native_candidates.py")
prev=runpy.run_path(str(wrapper),run_name="batch24_camera_test")
tests=prev["env"]["main"].__globals__["TESTS"]
source=original.read_text("utf8")
old="const distance=Math.max(28,span*1.65);"
new="const distance=Math.max(110,span*6);"
assert source.count(old)==1
source=source.replace(old,new)
env={"__file__":str(original),"__name__":"batch24_wide_camera"}
exec(compile(source,str(original),"exec"),env)
env["TESTS"]=tests
env["O"]=env["D"]/"ten_batch_review/24_231_240/extra_decocraft_render_full_frame"
env["main"]()
