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
        ("assets/images/cubes/bg.pngsrgb", "copy"),
        ("https://www.igloo.inc/assets/images/cubes/bg.png", "download"),
    ],
    "assets/images/cubes/advect.png": [
        ("assets/images/cubes/advect.pngcolordata-repeat", "copy"),
        ("https://www.igloo.inc/assets/images/cubes/advect.png", "download"),
    ],
    "assets/images/cubes_env.exr": [
        ("assets/cubes_env.exr", "copy"),
        ("https://www.igloo.inc/assets/images/cubes_env.exr", "download"),
    ],
}

print("Fixing cube files...\n")

for target_path, sources in files_to_fix.items():
    target = BASE_DIR / target_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing target if it exists and is invalid (HTML)
    if target.exists():
        try:
            with open(target, 'rb') as f:
                header = f.read(10)
                # Check if it's HTML (starts with <!doctype or <html)
                if header.startswith(b'<!doctype') or header.startswith(b'<html') or header.startswith(b'<HTML'):
                    target.unlink()
                    print(f"Removed invalid HTML file: {target_path}")
        except:
            pass
    
    # Check if target already exists and is valid
    if target.exists():
        try:
            with open(target, 'rb') as f:
                header = f.read(4)
                if target_path.endswith('.png') and header[:4] == b'\x89PNG':
                    size = target.stat().st_size
                    if size > 1000:
                        print(f"✓ {target_path} already valid ({size:,} bytes)")
                        continue
                elif target_path.endswith('.exr'):
                    size = target.stat().st_size
                    if size > 10000:  # EXR files are larger
                        print(f"✓ {target_path} already valid ({size:,} bytes)")
                        continue
        except:
            pass
    
    # Try to fix
    fixed = False
    for source, method in sources:
        try:
            if method == "copy":
                source_path = BASE_DIR / source
                if source_path.exists():
                    size = source_path.stat().st_size
                    # Check if source is valid
                    with open(source_path, 'rb') as f:
                        header = f.read(10)
                        if header.startswith(b'<!doctype') or header.startswith(b'<html'):
                            print(f"  ⚠ {source} is HTML, skipping copy")
                            continue
                    
                    if size > 1000:
                        shutil.copy2(source_path, target)
                        print(f"✓ Copied {source} → {target_path} ({size:,} bytes)")
                        fixed = True
                        break
            elif method == "download":
                print(f"  ⬇️  Downloading {target_path}...", end=' ', flush=True)
                req = urllib.request.Request(source)
                req.add_header('User-Agent', 'Mozilla/5.0')
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = response.read()
                    # Check if it's HTML
                    if data[:10].startswith(b'<!doctype') or data[:10].startswith(b'<html'):
                        print("✗ (got HTML instead of file)")
                        continue
                    with open(target, 'wb') as f:
                        f.write(data)
                
                if target.exists():
                    size = target.stat().st_size
                    if size > 1000:
                        print(f"✓ ({size:,} bytes)")
                        fixed = True
                        break
                    else:
                        target.unlink()
                        print("✗ (too small)")
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    if not fixed:
        print(f"✗ Could not fix {target_path}")

print("\nVerifying...")
for target_path in files_to_fix.keys():
    target = BASE_DIR / target_path
    if target.exists():
        size = target.stat().st_size
        try:
            with open(target, 'rb') as f:
                header = f.read(4)
                if target_path.endswith('.png') and header[:4] == b'\x89PNG':
                    print(f"✓ {target_path} - {size:,} bytes (valid PNG)")
                elif target_path.endswith('.exr'):
                    print(f"✓ {target_path} - {size:,} bytes (EXR)")
                else:
                    print(f"✗ {target_path} - {size:,} bytes (INVALID format)")
        except:
            print(f"✗ {target_path} - could not verify")
    else:
        print(f"✗ {target_path} - NOT FOUND")

print("\n✅ Done!")

