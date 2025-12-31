#!/usr/bin/env python3
"""
Download ALL 86 files including canvas and all graphics from igloo.inc
"""
import re
import os
import subprocess
from pathlib import Path

BASE_URL = "https://www.igloo.inc"
BASE_DIR = Path(".")

def extract_all_asset_paths():
    """Extract ALL asset paths from code files"""
    all_paths = set()
    
    # Read all JS files
    files_to_scan = ['igloo_main.js', 'igloo_app3d.js', 'index.html']
    
    for file_path in files_to_scan:
        file_obj = Path(file_path)
        if not file_obj.exists():
            continue
            
        with open(file_obj, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Pattern 1: le.load() calls
        le_matches = re.findall(r'le\.load\(["\']([^"\']+)["\']', content)
        for match in le_matches:
            # Skip type identifiers
            if match in ['data', 'srgb', 'linear', 'repeat', 'colordata', 'datatexture', '3d-data', 'luttetrahedral', 'nearest']:
                continue
            # Clean path
            clean = match.split('srgb')[0].split('linear')[0].split('repeat')[0].split('data')[0].split('colordata')[0].split('datatexture')[0].split('3d-data')[0].split('luttetrahedral')[0].split('nearest')[0].rstrip('-')
            if clean and '.' in clean:
                all_paths.add(clean)
        
        # Pattern 2: zt.load() calls
        zt_matches = re.findall(r'zt\.load\(["\']([^"\']+)["\']', content)
        for match in zt_matches:
            if match and '.' in match:
                all_paths.add(match)
        
        # Pattern 3: Full URLs
        url_matches = re.findall(r'https://www\.igloo\.inc[^\s"\'\)]+', content)
        for match in url_matches:
            path = match.replace(BASE_URL, '').lstrip('/')
            if path:
                all_paths.add(path)
    
    return all_paths

def construct_url(path):
    """Construct full URL from path"""
    if path.startswith('assets/'):
        return f"{BASE_URL}/{path}"
    elif path.startswith('../'):
        return f"{BASE_URL}/assets/{path[3:]}"
    elif path.endswith('.drc'):
        return f"{BASE_URL}/assets/geometries/{path}"
    elif path.endswith(('.ktx2', '.png', '.jpg', '.jpeg', '.exr')):
        # Try images/ first
        return f"{BASE_URL}/assets/images/{path}"
    elif path.endswith(('.woff', '.woff2', '.ttf', '.otf')):
        return f"{BASE_URL}/assets/fonts/{path}"
    elif path.endswith('.json'):
        return f"{BASE_URL}/assets/{path}"
    else:
        return f"{BASE_URL}/assets/{path}"

def download_file(url, local_path):
    """Download a file"""
    try:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        if local_path.exists():
            size = local_path.stat().st_size
            if size > 100:
                return True, size
        
        result = subprocess.run(
            ['curl', '-s', '-f', '-L', '--max-time', '30', url, '-o', str(local_path)],
            capture_output=True,
            timeout=35
        )
        
        if result.returncode == 0 and local_path.exists():
            size = local_path.stat().st_size
            if size > 100:
                return True, size
            else:
                local_path.unlink()
                return False, 0
        return False, 0
    except:
        return False, 0

def main():
    print("🔍 Extracting ALL asset paths (target: 86 files)...\n")
    
    # Extract all paths
    all_paths = extract_all_asset_paths()
    
    # Add known files
    known_files = [
        'audioworker-036a09db.js',
        'bitmapworker-046527f8.js',
        'exrworker-41cbee65.js',
        'msdfworker-ac346fa7.js',
        'favicon32-af94112f.png',
        'favicon16-9e4401be.png',
        'images/social.jpg',
        # Canvas and WebGL related
        'libs/draco/draco_wasm_wrapper.js',
        'libs/draco/draco_decoder.wasm',
        'libs/basis/basis_transcoder.js',
        'libs/basis/basis_transcoder.wasm',
    ]
    
    for file in known_files:
        all_paths.add(file)
    
    print(f"📦 Found {len(all_paths)} unique asset paths")
    print("\n⬇️  Downloading all files...\n")
    
    downloaded = 0
    failed = 0
    skipped = 0
    failed_urls = []
    
    # Sort for consistent output
    sorted_paths = sorted(all_paths)
    
    for path in sorted_paths:
        # Construct URL
        url = construct_url(path)
        
        # Determine local path
        if path.startswith('assets/'):
            local_path = BASE_DIR / path
        elif path.startswith('../'):
            local_path = BASE_DIR / 'assets' / path[3:]
        else:
            # Try to determine from extension
            if path.endswith('.drc'):
                local_path = BASE_DIR / 'assets' / 'geometries' / path
            elif path.endswith(('.ktx2', '.png', '.jpg', '.jpeg', '.exr')):
                local_path = BASE_DIR / 'assets' / 'images' / path
            elif path.endswith(('.woff', '.woff2', '.ttf', '.otf')):
                local_path = BASE_DIR / 'assets' / 'fonts' / path
            else:
                local_path = BASE_DIR / 'assets' / path
        
        # Check if exists
        if local_path.exists():
            size = local_path.stat().st_size
            if size > 100:
                print(f"  ✓ Exists: {local_path} ({size:,} bytes)")
                skipped += 1
                continue
        
        # Try to download
        print(f"  ⬇️  {path}...", end=' ', flush=True)
        success, size = download_file(url, local_path)
        
        if success:
            print(f"✓ ({size:,} bytes)")
            downloaded += 1
        else:
            # Try alternative paths
            alt_urls = []
            if path.endswith(('.ktx2', '.png', '.jpg', '.jpeg', '.exr')):
                alt_urls = [
                    f"{BASE_URL}/assets/{path}",
                    f"{BASE_URL}/assets/images/{path}",
                ]
            elif path.endswith('.drc'):
                alt_urls = [
                    f"{BASE_URL}/assets/{path}",
                    f"{BASE_URL}/assets/geometries/{path}",
                ]
            
            found = False
            for alt_url in alt_urls:
                if alt_url != url:
                    success, size = download_file(alt_url, local_path)
                    if success:
                        print(f"✓ ({size:,} bytes) [alt path]")
                        downloaded += 1
                        found = True
                        break
            
            if not found:
                print("✗")
                failed += 1
                failed_urls.append((path, url))
    
    print(f"\n✅ Downloaded: {downloaded}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total processed: {len(sorted_paths)}")
    print(f"🎯 Target: 86 files")
    
    if failed_urls:
        print(f"\n⚠️  Failed URLs:")
        for path, url in failed_urls[:10]:  # Show first 10
            print(f"  - {path} ({url})")
        if len(failed_urls) > 10:
            print(f"  ... and {len(failed_urls) - 10} more")
    
    # Count actual files
    asset_files = list(BASE_DIR.glob('assets/**/*'))
    asset_files = [f for f in asset_files if f.is_file()]
    print(f"\n📁 Total files in assets/: {len(asset_files)}")
    
    print("\n✅ Complete!")

if __name__ == "__main__":
    main()

