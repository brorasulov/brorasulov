#!/usr/bin/env python3
"""
Download missing cube geometry and texture files
"""
import urllib.request
import ssl
from pathlib import Path

ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://www.igloo.inc"
BASE_DIR = Path(".")

# Missing geometry files
geometry_files = [
    "assets/geometries/cubes/cube1.drc",
    "assets/geometries/cubes/cube2.drc",
    "assets/geometries/cubes/cube3.drc",
]

# Missing texture files
texture_files = [
    "assets/images/cubes/cube1_roughness.ktx2",
    "assets/images/cubes/cube1_normal.ktx2",
    "assets/images/cubes/cube2_roughness.ktx2",
    "assets/images/cubes/cube2_normal.ktx2",
    "assets/images/cubes/cube3_roughness.ktx2",
    "assets/images/cubes/cube3_normal.ktx2",
    "assets/images/cubes/overpass_logo_color.ktx2",
    "assets/images/cubes/abstractlogo_color.ktx2",
    "assets/images/cubes/pudgy_color.ktx2",
]

all_files = geometry_files + texture_files

print("Downloading missing cube files...\n")

downloaded = 0
failed = 0

for file_path in all_files:
    url = f"{BASE_URL}/{file_path}"
    target = BASE_DIR / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    if target.exists():
        size = target.stat().st_size
        print(f"✓ {file_path} already exists ({size:,} bytes)")
        downloaded += 1
        continue
    
    print(f"Downloading {file_path}...", end=' ', flush=True)
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://www.igloo.inc/',
            'Accept': '*/*',
        })
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            
            # Check if HTML
            if data[:20].startswith((b'<!doctype', b'<html', b'<HTML', b'<!DOCTYPE')):
                print("✗ (got HTML)")
                failed += 1
                continue
            
            # Check size
            if len(data) < 100:
                print("✗ (too small)")
                failed += 1
                continue
            
            # Write
            with open(target, 'wb') as f:
                f.write(data)
            
            size = target.stat().st_size
            print(f"✓ ({size:,} bytes)")
            downloaded += 1
                
    except Exception as e:
        print(f"✗ Error: {e}")
        failed += 1

print(f"\n✅ Downloaded: {downloaded}")
print(f"❌ Failed: {failed}")
print(f"📊 Total: {len(all_files)}")
print("\nRefresh browser (Cmd+R) and check if errors are gone!")
