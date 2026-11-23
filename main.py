"""make.fun news-image-20261122 entry: copy the finished image to /output.

The image (entry.png, drawn at build time by draw_image.py) is shipped in
this repository; this program only copies it, so both graded runs write
exactly the same bytes. Standard library only, no network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT, "entry.png")
shutil.copyfile(src, dst)
assert os.path.getsize(src) == os.path.getsize(dst), "copy size mismatch"
print("wrote", dst, os.path.getsize(dst), "bytes")
