#!/usr/bin/env python3
"""
Final fix - download cubes files correctly
"""
import urllib.request
import ssl
import shutil
from pathlib import Path

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = Path(".")

# Files that must exist
files_to_fix = {
    "assets/images/cubes/bg.png": "https://www.igloo.inc/assets/images/cubes/bg.png",
    "assets/images/cubes/advect.png": "https://www.igloo.inc/assets/images/cubes/advect.png",
    "assets/images/cubes_env.exr": "https://www.igloo.inc/assets/images/cubes_env.exr",
}

print("Removing HTML files and downloading correct files...\n")

for file_path, url in files_to_fix.items():
    target = BASE_DIR / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove if exists (might be HTML)
    if target.exists():
        try:
            with open(target, 'rb') as f:
                header = f.read(20)
                if header.startswith((b'<!doctype', b'<html', b'<HTML')):
                    print(f"Removing HTML file: {file_path}")
                    target.unlink()
                elif file_path.endswith('.png') and header[:8] != b'\x89PNG\r\n\x1a\n':
                    print(f"Removing invalid PNG: {file_path}")
                    target.unlink()
                else:
                    print(f"Keeping valid file: {file_path}")
                    continue
        except:
            target.unlink()
    
    # Download with proper headers
    print(f"Downloading {file_path}...", end=' ', flush=True)
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.igloo.inc/',
            'Accept': 'image/png,image/*,*/*;q=0.8' if file_path.endswith('.png') else '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
        })
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            
            # Check if HTML
            if data[:20].startswith((b'<!doctype', b'<html', b'<HTML', b'<!DOCTYPE')):
                print("✗ (got HTML)")
                # Try alternative URL
                alt_url = url.replace('/assets/images/', '/assets/')
                print(f"  Trying alternative: {alt_url}...", end=' ', flush=True)
                try:
                    req2 = urllib.request.Request(alt_url, headers=req.headers)
                    with urllib.request.urlopen(req2, timeout=30) as r2:
                        data2 = r2.read()
                        if not data2[:20].startswith((b'<!doctype', b'<html', b'<HTML', b'<!DOCTYPE')):
                            with open(target, 'wb') as f:
                                f.write(data2)
                            print(f"✓ ({len(data2):,} bytes)")
                        else:
                            print("✗ (still HTML)")
                except:
                    print("✗ (failed)")
                continue
            
            # Check PNG signature
            if file_path.endswith('.png') and data[:8] != b'\x89PNG\r\n\x1a\n':
                print("✗ (not PNG)")
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
                header = f.read(20)
                if file_path.endswith('.png'):
                    if header[:8] == b'\x89PNG\r\n\x1a\n':
                        print(f"✓ {file_path} - valid PNG ({size:,} bytes)")
                    else:
                        print(f"✗ {file_path} - invalid PNG")
                        all_ok = False
                elif file_path.endswith('.exr'):
                    # EXR files start with specific bytes
                    if not header.startswith((b'<!doctype', b'<html', b'<HTML', b'<!DOCTYPE')):
                        print(f"✓ {file_path} - EXR ({size:,} bytes)")
                    else:
                        print(f"✗ {file_path} - is HTML")
                        all_ok = False
                else:
                    if not header.startswith((b'<!doctype', b'<html', b'<HTML', b'<!DOCTYPE')):
                        print(f"✓ {file_path} - valid ({size:,} bytes)")
                    else:
                        print(f"✗ {file_path} - is HTML")
                        all_ok = False
        except Exception as e:
            print(f"✗ {file_path} - error: {e}")
            all_ok = False
    else:
        print(f"✗ {file_path} - NOT FOUND")
        all_ok = False

if all_ok:
    print("\n✅ All files are valid!")
    print("\nNow:")
    print("1. Make sure HTTP server is running: python3 -m http.server 8000")
    print("2. Open browser: http://localhost:8000")
    print("3. Refresh page (Cmd+R)")
else:
    print("\n⚠️  Some files are still missing or invalid.")
    print("Try running this script again or check the URLs manually.")

