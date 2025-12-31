#!/usr/bin/env python3
"""
Download and fix ALL missing files - final solution
"""
import urllib.request
import ssl
import shutil
from pathlib import Path

ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://www.igloo.inc"
BASE_DIR = Path(".")

# All files that need to exist
# le.load("cubes/bg.png") looks for assets/images/cubes/bg.png
# le.load("cubes_env.exr") looks for assets/images/cubes_env.exr

files_to_fix = {
    "assets/images/cubes/bg.png": "https://www.igloo.inc/assets/images/cubes/bg.png",
    "assets/images/cubes/advect.png": "https://www.igloo.inc/assets/images/cubes/advect.png",
    "assets/images/cubes_env.exr": "https://www.igloo.inc/assets/images/cubes_env.exr",
}

print("Downloading and fixing all missing files...\n")

for file_path, url in files_to_fix.items():
    target = BASE_DIR / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove if exists and is HTML
    if target.exists():
        try:
            with open(target, 'rb') as f:
                header = f.read(10)
                if header.startswith((b'<!doctype', b'<html', b'<HTML')):
                    target.unlink()
                    print(f"Removed HTML: {file_path}")
        except:
            if target.exists():
                target.unlink()
    
    # Check if valid
    if target.exists():
        try:
            with open(target, 'rb') as f:
                header = f.read(8)
                if file_path.endswith('.png') and header[:8] == b'\x89PNG\r\n\x1a\n':
                    size = target.stat().st_size
                    if size > 1000:
                        print(f"✓ {file_path} already valid ({size:,} bytes)")
                        continue
        except:
            pass
    
    # Download
    print(f"Downloading {file_path}...", end=' ', flush=True)
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://www.igloo.inc/',
            'Accept': 'image/png,image/*,*/*;q=0.8' if file_path.endswith('.png') else '*/*'
        })
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            
            # Check if HTML
            if data[:10].startswith((b'<!doctype', b'<html', b'<HTML')):
                print("✗ (got HTML)")
                continue
            
            # Check PNG
            if file_path.endswith('.png') and data[:8] != b'\x89PNG\r\n\x1a\n':
                print("✗ (not PNG)")
                continue
            
            # Write
            with open(target, 'wb') as f:
                f.write(data)
            
            size = target.stat().st_size
            if size > 1000:
                print(f"✓ ({size:,} bytes)")
            else:
                print(f"✗ (too small: {size} bytes)")
                target.unlink()
                
    except Exception as e:
        print(f"✗ Error: {e}")

print("\nFinal verification:")
all_good = True
for file_path in files_to_fix.keys():
    target = BASE_DIR / file_path
    if target.exists():
        size = target.stat().st_size
        try:
            with open(target, 'rb') as f:
                header = f.read(8)
                if file_path.endswith('.png') and header[:8] == b'\x89PNG\r\n\x1a\n':
                    print(f"✓ {file_path} - valid PNG ({size:,} bytes)")
                elif file_path.endswith('.exr'):
                    print(f"✓ {file_path} - EXR ({size:,} bytes)")
                else:
                    print(f"✗ {file_path} - invalid format")
                    all_good = False
        except:
            print(f"✗ {file_path} - could not verify")
            all_good = False
    else:
        print(f"✗ {file_path} - NOT FOUND")
        all_good = False

if all_good:
    print("\n✅ All files are valid! Refresh browser (Cmd+R).")
else:
    print("\n⚠️  Some files are missing or invalid. Check the errors above.")

