#!/usr/bin/env python3
"""
Ensure all required cube files exist with correct names and content
"""
import urllib.request
import ssl
import shutil
from pathlib import Path

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = Path(".")

# Required files
required_files = {
    "assets/images/cubes/bg.png": "https://www.igloo.inc/assets/images/cubes/bg.png",
    "assets/images/cubes/advect.png": "https://www.igloo.inc/assets/images/cubes/advect.png",
    "assets/images/cubes_env.exr": "https://www.igloo.inc/assets/images/cubes_env.exr",
}

print("Ensuring all cube files exist...\n")

for file_path, url in required_files.items():
    target = BASE_DIR / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if file exists and is valid
    is_valid = False
    if target.exists():
        try:
            with open(target, 'rb') as f:
                header = f.read(10)
                # Check if it's HTML (invalid)
                if header.startswith(b'<!doctype') or header.startswith(b'<html') or header.startswith(b'<HTML'):
                    print(f"✗ {file_path} is HTML (invalid), removing...")
                    target.unlink()
                else:
                    # Check PNG signature
                    if file_path.endswith('.png'):
                        f.seek(0)
                        png_header = f.read(8)
                        if png_header[:8] == b'\x89PNG\r\n\x1a\n':
                            size = target.stat().st_size
                            if size > 1000:
                                print(f"✓ {file_path} exists and is valid PNG ({size:,} bytes)")
                                is_valid = True
                    # Check EXR signature
                    elif file_path.endswith('.exr'):
                        f.seek(0)
                        exr_header = f.read(4)
                        if exr_header in [b'\x76\x2f\x31\x01', b'EXR ']:
                            size = target.stat().st_size
                            if size > 10000:
                                print(f"✓ {file_path} exists and is valid EXR ({size:,} bytes)")
                                is_valid = True
        except Exception as e:
            print(f"✗ Error checking {file_path}: {e}")
            target.unlink()
    
    # Download if not valid
    if not is_valid:
        print(f"⬇️  Downloading {file_path}...", end=' ', flush=True)
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            req.add_header('Accept', 'image/png,image/*,*/*;q=0.8' if file_path.endswith('.png') else '*/*')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                
                # Verify it's not HTML
                if data[:10].startswith(b'<!doctype') or data[:10].startswith(b'<html'):
                    print("✗ (got HTML, not a valid file)")
                    continue
                
                # Verify PNG
                if file_path.endswith('.png') and data[:8] != b'\x89PNG\r\n\x1a\n':
                    print("✗ (not a valid PNG file)")
                    continue
                
                # Write file
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
for file_path in required_files.keys():
    target = BASE_DIR / file_path
    if target.exists():
        size = target.stat().st_size
        try:
            with open(target, 'rb') as f:
                header = f.read(8)
                if file_path.endswith('.png') and header[:8] == b'\x89PNG\r\n\x1a\n':
                    print(f"✓ {file_path} - {size:,} bytes (valid PNG)")
                elif file_path.endswith('.exr'):
                    print(f"✓ {file_path} - {size:,} bytes (EXR)")
                else:
                    print(f"✗ {file_path} - {size:,} bytes (INVALID)")
        except:
            print(f"✗ {file_path} - could not verify")
    else:
        print(f"✗ {file_path} - NOT FOUND")

print("\n✅ Done! If files are valid, refresh your browser (Cmd+R).")

