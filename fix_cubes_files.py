#!/usr/bin/env python3
import urllib.request
import os
from pathlib import Path

BASE_URL = "https://www.igloo.inc"
BASE_DIR = Path(".")

# Files that need to be downloaded
files_to_download = {
    "assets/images/cubes/bg.png": "https://www.igloo.inc/assets/images/cubes/bg.png",
    "assets/images/cubes/advect.png": "https://www.igloo.inc/assets/images/cubes/advect.png",
    "assets/images/cubes_env.exr": "https://www.igloo.inc/assets/images/cubes_env.exr",
}

print("Downloading missing cube files...\n")

for local_path_str, url in files_to_download.items():
    local_path = BASE_DIR / local_path_str
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if file exists and is valid
    if local_path.exists():
        size = local_path.stat().st_size
        if size > 1000:  # At least 1KB
            print(f"✓ {local_path_str} exists ({size:,} bytes)")
            continue
    
    # Download
    print(f"⬇️  Downloading {local_path_str}...", end=' ', flush=True)
    try:
        urllib.request.urlretrieve(url, str(local_path))
        if local_path.exists():
            size = local_path.stat().st_size
            if size > 1000:
                print(f"✓ ({size:,} bytes)")
            else:
                print(f"✗ (too small: {size} bytes)")
                local_path.unlink()
        else:
            print("✗ (failed)")
    except Exception as e:
        print(f"✗ ({e})")

print("\n✅ Done!")

