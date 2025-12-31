#!/usr/bin/env python3
"""
Copy files from assets/cubes/ to assets/images/cubes/ where le.load expects them
"""
import shutil
from pathlib import Path

BASE_DIR = Path(".")

# Files to copy - le.load("cubes/bg.png") looks for assets/images/cubes/bg.png
files_to_copy = {
    "assets/cubes/bg.png": "assets/images/cubes/bg.png",
    "assets/cubes/advect.png": "assets/images/cubes/advect.png",
    "assets/cubes_env.exr": "assets/images/cubes_env.exr",
}

print("Copying files to correct locations...\n")

for source_str, target_str in files_to_copy.items():
    source = BASE_DIR / source_str
    target = BASE_DIR / target_str
    target.parent.mkdir(parents=True, exist_ok=True)
    
    if source.exists():
        try:
            # Check if source is valid (not HTML)
            with open(source, 'rb') as f:
                header = f.read(30)
                if header.startswith((b'<!doctype', b'<html', b'<HTML', b'<!DOCTYPE')):
                    print(f"✗ {source_str} - is HTML, skipping")
                    continue
                elif target_str.endswith('.png') and header[:8] != b'\x89PNG\r\n\x1a\n':
                    print(f"✗ {source_str} - invalid PNG, skipping")
                    continue
            
            # Copy file
            shutil.copy2(source, target)
            size = target.stat().st_size
            print(f"✓ Copied {source_str} → {target_str} ({size:,} bytes)")
        except Exception as e:
            print(f"✗ Error copying {source_str}: {e}")
    else:
        print(f"✗ Source not found: {source_str}")

print("\n✅ Done! Files should now be in the correct locations.")
print("Refresh browser (Cmd+R) and check if the 3D content loads.")

