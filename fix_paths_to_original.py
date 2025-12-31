#!/usr/bin/env python3
"""
Fix paths to match original website - change from assets/images/ to relative paths
Original website uses relative paths like "cubes/bg.png" not "assets/images/cubes/bg.png"
"""
import re
from pathlib import Path

BASE_DIR = Path(".")

# Read the file
with open('igloo_app3d.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Original paths that should be changed
# Original website uses: le.load("cubes/bg.png") not le.load("assets/images/cubes/bg.png")
# Original website uses: le.load("cubes_env.exr") not le.load("assets/images/cubes_env.exr")

changes = [
    # Change from assets/images/cubes/bg.png to cubes/bg.png
    ('le.load("assets/images/cubes/bg.png"', 'le.load("cubes/bg.png"'),
    # Change from assets/images/cubes/advect.png to cubes/advect.png
    ('le.load("assets/images/cubes/advect.png"', 'le.load("cubes/advect.png"'),
    # Change from assets/images/cubes_env.exr to cubes_env.exr
    ('le.load("assets/images/cubes_env.exr"', 'le.load("cubes_env.exr"'),
]

print("Fixing paths to match original website...\n")

for old_path, new_path in changes:
    if old_path in content:
        content = content.replace(old_path, new_path)
        print(f"✓ Changed: {old_path} → {new_path}")
    else:
        print(f"⚠ Not found: {old_path}")

# Write back
with open('igloo_app3d.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Paths fixed! Now files should be in:")
print("  - assets/cubes/bg.png (or assets/images/cubes/bg.png)")
print("  - assets/cubes/advect.png (or assets/images/cubes/advect.png)")
print("  - assets/cubes_env.exr (or assets/images/cubes_env.exr)")
print("\nCopy files to match the new paths:")

# Now copy files to the expected locations
import shutil

file_moves = [
    ("assets/images/cubes/bg.png", "assets/cubes/bg.png"),
    ("assets/images/cubes/advect.png", "assets/cubes/advect.png"),
    ("assets/images/cubes_env.exr", "assets/cubes_env.exr"),
]

print("\nCopying files to new locations...")
for source, target in file_moves:
    source_path = BASE_DIR / source
    target_path = BASE_DIR / target
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    if source_path.exists():
        try:
            with open(source_path, 'rb') as f:
                header = f.read(10)
                if not header.startswith((b'<!doctype', b'<html', b'<HTML')):
                    shutil.copy2(source_path, target_path)
                    print(f"✓ Copied {source} → {target}")
        except:
            pass
    elif target_path.exists():
        print(f"✓ {target} already exists")

print("\n✅ Done! Refresh browser (Cmd+R).")

