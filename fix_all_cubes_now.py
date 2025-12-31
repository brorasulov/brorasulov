#!/usr/bin/env python3
"""
Fix all cubes files - remove HTML and download correctly
"""
import urllib.request
import ssl
import shutil
from pathlib import Path

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = Path(".")

# Files that must exist - le.load("cubes/bg.png") looks for assets/images/cubes/bg.png
files_to_fix = {
    "assets/images/cubes/bg.png": "https://www.igloo.inc/assets/images/cubes/bg.png",
    "assets/images/cubes/advect.png": "https://www.igloo.inc/assets/images/cubes/advect.png",
    "assets/images/cubes_env.exr": "https://www.igloo.inc/assets/images/cubes_env.exr",
}

print("Checking and fixing cubes files...\n")

for file_path, url in files_to_fix.items():
    target = BASE_DIR / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Checking {file_path}...")
    
    # Check if exists and is valid
    should_download = False
    if target.exists():
        try:
            with open(target, 'rb') as f:
                header = f.read(30)
                # Check if HTML
                if header.startswith((b'<!doctype', b'<html', b'<HTML', b'<!DOCTYPE')):
                    print(f"  ✗ Is HTML - removing")
                    target.unlink()
                    should_download = True
                # Check PNG signature
                elif file_path.endswith('.png') and header[:8] != b'\x89PNG\r\n\x1a\n':
                    print(f"  ✗ Invalid PNG signature - removing")
                    target.unlink()
                    should_download = True
                # Check if too small (likely HTML or corrupted)
                elif target.stat().st_size < 100:
                    print(f"  ✗ Too small ({target.stat().st_size} bytes) - removing")
                    target.unlink()
                    should_download = True
                else:
                    size = target.stat().st_size
                    print(f"  ✓ Valid file ({size:,} bytes)")
                    continue
        except Exception as e:
            print(f"  ✗ Error checking: {e} - removing")
            target.unlink()
            should_download = True
    else:
        should_download = True
    
    if should_download:
        # Download with proper headers
        print(f"  Downloading...", end=' ', flush=True)
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.igloo.inc/',
                'Accept': 'image/png,image/*,*/*;q=0.8' if file_path.endswith('.png') else '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
            })
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                
                # Check if HTML
                if data[:30].startswith((b'<!doctype', b'<html', b'<HTML', b'<!DOCTYPE')):
                    print("✗ (got HTML)")
                    continue
                
                # Check PNG signature
                if file_path.endswith('.png') and data[:8] != b'\x89PNG\r\n\x1a\n':
                    print("✗ (not PNG)")
                    continue
                
                # Check size
                if len(data) < 100:
                    print("✗ (too small)")
                    continue
                
                # Write
                with open(target, 'wb') as f:
                    f.write(data)
                
                size = target.stat().st_size
                print(f"✓ ({size:,} bytes)")
                    
        except Exception as e:
            print(f"✗ Error: {e}")

print("\n" + "="*60)
print("Final verification:")
print("="*60)

all_ok = True
for file_path in files_to_fix.keys():
    target = BASE_DIR / file_path
    if target.exists():
        size = target.stat().st_size
        try:
            with open(target, 'rb') as f:
                header = f.read(30)
                if file_path.endswith('.png'):
                    if header[:8] == b'\x89PNG\r\n\x1a\n' and size > 100:
                        print(f"✓ {file_path} - valid PNG ({size:,} bytes)")
                    else:
                        print(f"✗ {file_path} - invalid PNG")
                        all_ok = False
                elif file_path.endswith('.exr'):
                    if not header.startswith((b'<!doctype', b'<html', b'<HTML', b'<!DOCTYPE')) and size > 100:
                        print(f"✓ {file_path} - EXR ({size:,} bytes)")
                    else:
                        print(f"✗ {file_path} - is HTML or too small")
                        all_ok = False
        except Exception as e:
            print(f"✗ {file_path} - error: {e}")
            all_ok = False
    else:
        print(f"✗ {file_path} - NOT FOUND")
        all_ok = False

if all_ok:
    print("\n✅ All files are valid!")
    print("\nNow check:")
    print("1. HTTP server is running: python3 -m http.server 8000")
    print("2. Open browser: http://localhost:8000")
    print("3. Refresh page (Cmd+R)")
else:
    print("\n⚠️  Some files are still missing or invalid.")
    print("Check the files manually or try running this script again.")

