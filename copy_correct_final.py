#!/usr/bin/env python3
"""Copy files with correct names"""
import shutil
from pathlib import Path

BASE_DIR = Path(".")

# Copy files with correct names
copies = [
    ("assets/images/cubes/bg.pngsrgb", "assets/images/cubes/bg.png"),
    ("assets/images/cubes/advect.pngcolordata-repeat", "assets/images/cubes/advect.png"),
    ("assets/cubes_env.exr", "assets/images/cubes_env.exr"),
]

print("Copying files with correct names...\n")

for source_str, target_str in copies:
    source = BASE_DIR / source_str
    target = BASE_DIR / target_str
    target.parent.mkdir(parents=True, exist_ok=True)
    
    if source.exists():
        # Check if source is HTML
        try:
            with open(source, 'rb') as f:
                header = f.read(10)
                if header.startswith((b'<!doctype', b'<html', b'<HTML')):
                    print(f"✗ {source_str} is HTML, skipping")
                    continue
        except:
            pass
        
        size = source.stat().st_size
        if size > 1000:
            shutil.copy2(source, target)
            print(f"✓ Copied {source_str} → {target_str} ({size:,} bytes)")
        else:
            print(f"✗ {source_str} too small ({size} bytes)")
    else:
        print(f"✗ {source_str} not found")

print("\nVerifying...")
for _, target_str in copies:
    target = BASE_DIR / target_str
    if target.exists():
        size = target.stat().st_size
        try:
            with open(target, 'rb') as f:
                header = f.read(8)
                if target_str.endswith('.png') and header[:8] == b'\x89PNG\r\n\x1a\n':
                    print(f"✓ {target_str} - valid PNG ({size:,} bytes)")
                elif target_str.endswith('.exr'):
                    print(f"✓ {target_str} - EXR ({size:,} bytes)")
                else:
                    print(f"✗ {target_str} - invalid format")
        except:
            print(f"✗ {target_str} - could not verify")
    else:
        print(f"✗ {target_str} - NOT FOUND")

print("\n✅ Done! Refresh browser (Cmd+R).")

