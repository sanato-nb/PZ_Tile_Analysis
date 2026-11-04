#!/usr/bin/env python3
"""Stage the generated v14 original-source sprite contact sheets as reviewable text."""
import base64,zipfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
zpath=r/"analysis/furniture_full_b42/2026-11-04/source_first_v14/B42_FURNITURE_SOURCE_FIRST_V14.zip"
out=r/"analysis/furniture_full_b42/2026-11-04/visual_review_v15"
out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 for i in (2,3,4):
  p=f"V14_SOURCE_ONLY_ORIGINAL_CONTACT_{i:02d}.png"
  data=z.read(p)
  (out/f"STAGED_ORIGINAL_CONTACT_{i:02d}_BASE64.txt").write_text(base64.b64encode(data).decode("ascii"),encoding="ascii")
  print("STAGED_ORIGINAL_IMAGE",i,len(data))
