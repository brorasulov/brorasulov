#!/usr/bin/env python3
import os
import shutil
import subprocess

BASE_URL = "https://www.igloo.inc"

# Files that are expected in assets/ root (relative paths)
relative_files = {
    "cubes/bg.png": "assets/images/cubes/bg.png",
    "cubes/advect.png": "assets/images/cubes/advect.png", 
    "cubes_env.exr": "assets/images/cubes_env.exr",
    "perlin-datatexture.png": "assets/images/perlin-datatexture.png"
}

print("Fixing file paths...\n")

for target, source in relative_files.items():
    target_path = f"assets/{target}"
    target_dir = os.path.dirname(target_path)
    
    # Create directory
    if target_dir:
        os.makedirs(target_dir, exist_ok=True)
    
    # Check if source exists
    if os.path.exists(source):
        size = os.path.getsize(source)
        if size > 5000:
            # Copy to target location
            shutil.copy2(source, target_path)
            print(f"  ✓ Copied {source} → {target_path} ({size} bytes)")
        else:
            print(f"  ⚠ {source} too small ({size} bytes), trying to download...")
            # Try to download
            url = f"{BASE_URL}/{source}"
            result = subprocess.run(['curl', '-s', '-f', '-L', url, '-o', target_path], 
                                  capture_output=True, timeout=10)
            if result.returncode == 0 and os.path.exists(target_path):
                new_size = os.path.getsize(target_path)
                if new_size > 5000:
                    print(f"  ✓ Downloaded {target_path} ({new_size} bytes)")
                else:
                    print(f"  ✗ {target_path} still too small after download")
            else:
                print(f"  ✗ Could not download {target_path}")
    else:
        # Source doesn't exist, try to download directly
        print(f"  ⚠ {source} not found, downloading to {target_path}...")
        url = f"{BASE_URL}/assets/{target}"
        result = subprocess.run(['curl', '-s', '-f', '-L', url, '-o', target_path], 
                              capture_output=True, timeout=10)
        if result.returncode == 0 and os.path.exists(target_path):
            size = os.path.getsize(target_path)
            if size > 5000:
                print(f"  ✓ Downloaded {target_path} ({size} bytes)")
            else:
                print(f"  ✗ {target_path} too small ({size} bytes)")
        else:
            # Try alternative path
            alt_url = f"{BASE_URL}/assets/images/{target}"
            result = subprocess.run(['curl', '-s', '-f', '-L', alt_url, '-o', target_path], 
                                  capture_output=True, timeout=10)
            if result.returncode == 0 and os.path.exists(target_path):
                size = os.path.getsize(target_path)
                if size > 5000:
                    print(f"  ✓ Downloaded {target_path} from images/ ({size} bytes)")
                else:
                    print(f"  ✗ {target_path} still too small")
            else:
                print(f"  ✗ Could not download {target_path}")

print("\n✅ Done!")

