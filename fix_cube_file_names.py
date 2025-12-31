#!/usr/bin/env python3
import urllib.request
import ssl
import shutil
from pathlib import Path

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = Path(".")

# Files to fix
files_to_fix = {
    "assets/images/cubes/bg.png": [
        "assets/images/cubes/bg.pngsrgb",  # Try existing wrong name first
        "assets/cubes/bg.png",  # Alternative location
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

print("Fixing cube file names and downloading missing files...\n")

for target_path, source_paths in files_to_fix.items():
    target = BASE_DIR / target_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if target already exists and is valid
    if target.exists():
        size = target.stat().st_size
        if size > 1000:
            print(f"✓ {target_path} already exists ({size:,} bytes)")
            continue
    
    # Try to copy from existing wrong-named files
    found = False
    for source_path in source_paths:
        source = BASE_DIR / source_path
        if source.exists():
            size = source.stat().st_size
            if size > 1000:
                shutil.copy2(source, target)
                print(f"✓ Copied {source_path} → {target_path} ({size:,} bytes)")
                found = True
                break
    
    # If not found, download
    if not found:
        url = f"https://www.igloo.inc/{target_path}"
        print(f"⬇️  Downloading {target_path}...", end=' ', flush=True)
        try:
            urllib.request.urlretrieve(url, str(target))
            if target.exists():
                size = target.stat().st_size
                if size > 1000:
                    print(f"✓ ({size:,} bytes)")
                else:
                    print(f"✗ (too small: {size} bytes)")
                    target.unlink()
            else:
                print("✗ (failed)")
        except Exception as e:
            print(f"✗ Error: {e}")

print("\nVerifying files...")
for target_path in files_to_fix.keys():
    target = BASE_DIR / target_path
    if target.exists():
        size = target.stat().st_size
        print(f"✓ {target_path} - {size:,} bytes")
    else:
        print(f"✗ {target_path} - NOT FOUND")

print("\n✅ Done!")

