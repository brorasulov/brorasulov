#!/usr/bin/env python3
import urllib.request
import ssl
from pathlib import Path

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = Path(".")

files = {
    "assets/images/cubes/bg.png": "https://www.igloo.inc/assets/images/cubes/bg.png",
    "assets/images/cubes/advect.png": "https://www.igloo.inc/assets/images/cubes/advect.png",
    "assets/images/cubes_env.exr": "https://www.igloo.inc/assets/images/cubes_env.exr",
}

print("Downloading files with proper headers...\n")

for file_path, url in files.items():
    target = BASE_DIR / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing
    if target.exists():
        target.unlink()
    
    print(f"Downloading {file_path}...", end=' ', flush=True)
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        req.add_header('Accept', 'image/png,image/*,*/*;q=0.8' if file_path.endswith('.png') else 'application/octet-stream,*/*;q=0.8')
        req.add_header('Referer', 'https://www.igloo.inc/')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            
            # Check if HTML
            if data[:10].startswith((b'<!doctype', b'<html', b'<HTML')):
                print("✗ (HTML response)")
                continue
            
            # Check PNG
            if file_path.endswith('.png') and data[:8] != b'\x89PNG\r\n\x1a\n':
                print("✗ (not PNG)")
                continue
            
            # Write
            with open(target, 'wb') as f:
                f.write(data)
            
            size = target.stat().st_size
            print(f"✓ {size:,} bytes")
            
    except Exception as e:
        print(f"✗ {e}")

print("\nVerifying...")
for file_path in files.keys():
    target = BASE_DIR / file_path
    if target.exists():
        size = target.stat().st_size
        with open(target, 'rb') as f:
            header = f.read(8)
            if file_path.endswith('.png') and header[:8] == b'\x89PNG\r\n\x1a\n':
                print(f"✓ {file_path} - valid PNG ({size:,} bytes)")
            elif file_path.endswith('.exr'):
                print(f"✓ {file_path} - EXR ({size:,} bytes)")
            else:
                print(f"✗ {file_path} - invalid")
    else:
        print(f"✗ {file_path} - not found")

print("\n✅ Done! Now refresh browser (Cmd+R)")

