#!/usr/bin/env python3
import urllib.request
import ssl
from pathlib import Path

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = Path(".")

files = {
    "assets/images/cubes/bg.png": "https://www.igloo.inc/assets/images/cubes/bg.png",
    "assets/images/cubes/advect.png": "https://www.igloo.inc/assets/images/cubes/advect.png",
    "assets/images/cubes_env.exr": "https://www.igloo.inc/assets/images/cubes_env.exr",
}

print("Downloading cube files directly...\n")

for local_path_str, url in files.items():
    local_path = BASE_DIR / local_path_str
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing file
    if local_path.exists():
        local_path.unlink()
        print(f"Removed old {local_path_str}")
    
    # Download
    print(f"Downloading {local_path_str}...", end=' ', flush=True)
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(local_path, 'wb') as f:
                f.write(response.read())
        
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
        print(f"✗ Error: {e}")

print("\nVerifying...")
for local_path_str in files.keys():
    local_path = BASE_DIR / local_path_str
    if local_path.exists():
        size = local_path.stat().st_size
        # Check if it's actually a PNG/EXR (not HTML)
        with open(local_path, 'rb') as f:
            header = f.read(4)
            if local_path_str.endswith('.png') and header[:4] == b'\x89PNG':
                print(f"✓ {local_path_str} - {size:,} bytes (valid PNG)")
            elif local_path_str.endswith('.exr') and header[:4] in [b'\x76\x2f\x31\x01', b'EXR ']:
                print(f"✓ {local_path_str} - {size:,} bytes (valid EXR)")
            else:
                print(f"✗ {local_path_str} - {size:,} bytes (INVALID - looks like HTML)")
    else:
        print(f"✗ {local_path_str} - NOT FOUND")

print("\n✅ Done!")

