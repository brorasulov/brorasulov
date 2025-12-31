#!/usr/bin/env python3
"""
Fix missing cube files - download directly
"""
import urllib.request
import ssl
from pathlib import Path

ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://www.igloo.inc"
BASE_DIR = Path(".")

# Critical missing files
CRITICAL_FILES = {
    "assets/images/cubes/bg.png": "https://www.igloo.inc/assets/images/cubes/bg.png",
    "assets/images/cubes/advect.png": "https://www.igloo.inc/assets/images/cubes/advect.png",
    "assets/images/cubes_env.exr": "https://www.igloo.inc/assets/images/cubes_env.exr",
}

print("Fixing critical missing files...\n")

for file_path, url in CRITICAL_FILES.items():
    target = BASE_DIR / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing if invalid
    if target.exists():
        try:
            with open(target, 'rb') as f:
                header = f.read(10)
                if header.startswith((b'<!doctype', b'<html', b'<HTML')):
                    print(f"Removing invalid HTML: {file_path}")
                    target.unlink()
                elif file_path.endswith('.png') and header[:8] != b'\x89PNG\r\n\x1a\n':
                    print(f"Removing invalid PNG: {file_path}")
                    target.unlink()
        except:
            target.unlink()
    
    # Download
    print(f"Downloading {file_path}...", end=' ', flush=True)
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        req.add_header('Referer', 'https://www.igloo.inc/')
        req.add_header('Accept', 'image/png,image/*,*/*;q=0.8' if file_path.endswith('.png') else '*/*')
        
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

print("\nVerifying files...")
for file_path in CRITICAL_FILES.keys():
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
        except:
            print(f"✗ {file_path} - could not verify")
    else:
        print(f"✗ {file_path} - NOT FOUND")

print("\n✅ Done! Refresh browser (Cmd+R).")

