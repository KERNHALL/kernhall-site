#!/usr/bin/env python3
"""Create mobile-friendly WebP copies of existing KERNHALL cover PNGs.

Does not run automatically, change published files,
overwrite source artwork, or modify HTML references.
Usage: python -m pip install Pillow
       python scripts/optimize_covers.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "covers"
DEST = SOURCE / "webp"
DEST.mkdir(parents=True, exist_ok=True)

for original in sorted(SOURCE.glob("*.png")):
    target = DEST / (original.stem + ".webp")
    with Image.open(original) as image:
        image = image.convert("RGB")
        if max(image.size) > 1600:
            image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        image.save(target, "WEBP", quality=90, method=6)
    old_kb = original.stat().st_size / 1024
    new_kb = target.stat().st_size / 1024
    print(f"{original.name}: {old_kb:.0f} KB -> {new_kb:.0f} KB "
          f"({100 * (1 - new_kb / old_kb):.1f}% reduction)")
print("Original PNGs unchanged. Review quality before switching website paths.")
