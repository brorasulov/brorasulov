#!/usr/bin/env python3
"""
Final fix - ensure files exist in assets/images/ with correct names
le.load("cubes/bg.png") looks for assets/images/cubes/bg.png
"""
import urllib.request
import ssl
import shutil
from pathlib import Path

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = Path(".")

# Files needed - le.load("cubes/bg.png") expects assets/images/cubes/bg.png
files_needed = {
    "assets/images/cubes/bg.png": [
        "assets/images/cubes/bg.pngsrgb",
        "assets/cubes/bg.png",
        "https://www.igloo.inc/assets/images/cubes/bg.png",
    ],
    "assets/images/cubes/advect.png": [
        "assets/images/cubes/advect.pngcolordata-repeat",
        "assets/cubes/advect.png",
        "https://www.igloo.inc/assets/images/cubes/advect.png",
    ],
    "assets/images/cubes_env.exr": [
        "assets/cubes_env.exr",
        "assets/images/cubes_env.exr",
        "https://www.igloo.inc/assets/images/cubes_env.exr",
    ],
}

print("Ensuring files exist in correct locations...\n")

for target_str, sources in files_needed.items():
    target = BASE_DIR / target_str
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove if HTML
    if target.exists():
        try:
            with open(target, 'rb') as f:
                header = f.read(10)
                if header.startswith((b'<!doctype', b'<html', b'<HTML')):
                    target.unlink()
                    print(f"Removed HTML: {target_str}")
        except:
            pass
    
    # Check if valid
    if target.exists():
        try:
            with open(target, 'rb') as f:
                header = f.read(8)
                if target_str.endswith('.png') and header[:8] == b'\x89PNG\r\n\x1a\n':
                    size = target.stat().st_size
                    if size > 1000:
                        print(f"✓ {target_str} already valid ({size:,} bytes)")
                        continue
        except:
            pass
    
    # Try sources
    found = False
    for source in sources:
        if source.startswith('http'):
            # Download
            print(f"  Downloading {target_str}...", end=' ', flush=True)
            try:
                req = urllib.request.Request(source, headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Referer': 'https://www.igloo.inc/'
                })
                data = urllib.request.urlopen(req, timeout=30).read()
                if not data.startswith((b'<!doctype', b'<html')) and len(data) > 1000:
                    if target_str.endswith('.png') and data[:8] != b'\x89PNG\r\n\x1a\n':
                        print("✗ (not PNG)")
                        continue
                    with open(target, 'wb') as f:
                        f.write(data)
                    print(f"✓ ({len(data):,} bytes)")
                    found = True
                    break
            except Exception as e:
                print(f"✗ ({e})")
        else:
            # Copy from local
            source_path = BASE_DIR / source
            if source_path.exists():
                try:
                    with open(source_path, 'rb') as f:
                        header = f.read(10)
                        if header.startswith((b'<!doctype', b'<html')):
                            continue
                    size = source_path.stat().st_size
                    if size > 1000:
                        shutil.copy2(source_path, target)
                        print(f"✓ Copied {source} → {target_str} ({size:,} bytes)")
                        found = True
                        break
                except:
                    pass
    
    if not found:
        print(f"✗ {target_str} - could not get from any source")

print("\nVerifying...")
for target_str in files_needed.keys():
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
                    print(f"✗ {target_str} - invalid")
        except:
            print(f"✗ {target_str} - could not verify")
    else:
        print(f"✗ {target_str} - NOT FOUND")

print("\n✅ Done! Refresh browser (Cmd+R).")

