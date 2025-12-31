#!/usr/bin/env python3
import os
import urllib.request
import subprocess

BASE_URL = "https://www.igloo.inc"
BASE_DIR = "assets"

# Files that need to be in assets/ root (relative paths)
relative_path_files = [
    "cubes/bg.png",
    "cubes/advect.png", 
    "cubes_env.exr",
    "perlin-datatexture.png"
]

# Try different source paths
source_paths = [
    "assets/images/cubes/bg.png",
    "assets/cubes/bg.png",
    "assets/images/cubes/advect.png",
    "assets/cubes/advect.png",
    "assets/images/cubes_env.exr",
    "assets/cubes_env.exr",
    "assets/images/perlin-datatexture.png",
    "assets/perlin-datatexture.png"
]

print("Downloading missing files...\n")

for target_file in relative_path_files:
    local_path = f"{BASE_DIR}/{target_file}"
    dir_path = os.path.dirname(local_path)
    
    # Create directory
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    # Check if file exists and is valid size
    if os.path.exists(local_path):
        size = os.path.getsize(local_path)
        if size > 5000:
            print(f"  ✓ {target_file} exists ({size} bytes)")
            continue
        else:
            print(f"  ⚠ {target_file} too small ({size} bytes), re-downloading...")
    
    # Try to download from different paths
    downloaded = False
    for source_path in source_paths:
        if target_file in source_path:
            url = f"{BASE_URL}/{source_path}"
            try:
                result = subprocess.run(
                    ['curl', '-s', '-f', '-L', url, '-o', local_path],
                    capture_output=True,
                    timeout=10
                )
                if result.returncode == 0 and os.path.exists(local_path):
                    size = os.path.getsize(local_path)
                    if size > 5000:
                        print(f"  ✓ Downloaded {target_file} from {source_path} ({size} bytes)")
                        downloaded = True
                        break
            except:
                continue
    
    if not downloaded:
        print(f"  ✗ Could not download {target_file}")

print("\n✅ Done!")

