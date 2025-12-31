#!/usr/bin/env python3
"""Move files to match original website paths"""
import shutil
from pathlib import Path

BASE_DIR = Path(".")

# Files to move - original website uses relative paths
# le.load("cubes/bg.png") expects assets/images/cubes/bg.png
# le.load("cubes_env.exr") expects assets/images/cubes_env.exr

# But we need to check where le.load actually looks
# Based on other paths like le.load("igloo/ground_color.ktx2") which is assets/images/igloo/ground_color.ktx2
# So le.load("cubes/bg.png") should be assets/images/cubes/bg.png

# So the paths in code are correct, we just need to ensure files exist
files_to_ensure = [
    "assets/images/cubes/bg.png",
    "assets/images/cubes/advect.png",
    "assets/images/cubes_env.exr",
]

print("Ensuring files exist in correct locations...\n")

# Try to copy from alternative locations
alternative_sources = {
    "assets/images/cubes/bg.png": [
        "assets/images/cubes/bg.pngsrgb",
        "assets/cubes/bg.png",
    ],
    "assets/images/cubes/advect.png": [
        "assets/images/cubes/advect.pngcolordata-repeat",
        "assets/cubes/advect.png",
    ],
    "assets/images/cubes_env.exr": [
        "assets/cubes_env.exr",
        "assets/images/cubes_env.exr",
    ],
}

for target_str in files_to_ensure:
    target = BASE_DIR / target_str
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if already exists and valid
    if target.exists():
        try:
            with open(target, 'rb') as f:
                header = f.read(10)
                if not header.startswith((b'<!doctype', b'<html', b'<HTML')):
                    size = target.stat().st_size
                    if size > 1000:
                        print(f"✓ {target_str} already exists ({size:,} bytes)")
                        continue
        except:
            pass
    
    # Try alternative sources
    found = False
    for source_str in alternative_sources.get(target_str, []):
        source = BASE_DIR / source_str
        if source.exists():
            try:
                with open(source, 'rb') as f:
                    header = f.read(10)
                    if header.startswith((b'<!doctype', b'<html', b'<HTML')):
                        continue
                size = source.stat().st_size
                if size > 1000:
                    shutil.copy2(source, target)
                    print(f"✓ Copied {source_str} → {target_str} ({size:,} bytes)")
                    found = True
                    break
            except:
                pass
    
    if not found:
        print(f"✗ {target_str} - not found in alternative locations")

print("\n✅ Done! Files should now be in correct locations.")
print("Refresh browser (Cmd+R).")

