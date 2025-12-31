#!/usr/bin/env python3
"""
Comprehensive script to download ALL assets, graphics, code, and resources from igloo.inc
"""
import re
import os
import subprocess
import json
from pathlib import Path
from urllib.parse import urlparse

BASE_URL = "https://www.igloo.inc"
BASE_DIR = Path(".")

def extract_all_urls_from_content(content, file_path=""):
    """Extract all possible URLs and asset paths from content"""
    urls = set()
    
    # Pattern 1: Full URLs
    patterns = [
        r'https://www\.igloo\.inc[^\s"\'\)]+',
        r'["\']https://www\.igloo\.inc[^"\']+["\']',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            # Clean up quotes
            match = match.strip('"\'')
            if match.startswith('http'):
                urls.add(match)
    
    # Pattern 2: le.load() calls
    le_load_pattern = r'le\.load\(["\']([^"\']+)["\']'
    matches = re.findall(le_load_pattern, content)
    for match in matches:
        # Skip type identifiers
        if match in ['data', 'srgb', 'linear', 'repeat', 'colordata', 'datatexture', '3d-data', 'luttetrahedral', 'nearest']:
            continue
        # Clean path
        clean_path = match.split('srgb')[0].split('linear')[0].split('repeat')[0].split('data')[0].split('colordata')[0].split('datatexture')[0].split('3d-data')[0].split('luttetrahedral')[0].split('nearest')[0].rstrip('-')
        if clean_path and '.' in clean_path:
            # Construct full path
            if clean_path.startswith('assets/'):
                urls.add(f"{BASE_URL}/{clean_path}")
            elif clean_path.startswith('../'):
                # Relative path like ../fonts/...
                clean_path = clean_path[3:]  # Remove ../
                urls.add(f"{BASE_URL}/assets/{clean_path}")
            else:
                # Assume assets/images/ for textures, assets/geometries/ for .drc
                if clean_path.endswith('.drc'):
                    urls.add(f"{BASE_URL}/assets/geometries/{clean_path}")
                elif clean_path.endswith(('.ktx2', '.png', '.jpg', '.jpeg', '.exr')):
                    urls.add(f"{BASE_URL}/assets/images/{clean_path}")
                else:
                    urls.add(f"{BASE_URL}/assets/{clean_path}")
    
    # Pattern 3: zt.load() calls (geometry loader)
    zt_load_pattern = r'zt\.load\(["\']([^"\']+)["\']'
    matches = re.findall(zt_load_pattern, content)
    for match in matches:
        if match and '.' in match:
            if match.startswith('assets/'):
                urls.add(f"{BASE_URL}/{match}")
            else:
                urls.add(f"{BASE_URL}/assets/geometries/{match}")
    
    # Pattern 4: Worker files
    worker_patterns = [
        r'worker["\']?\s*:\s*["\']([^"\']+worker[^"\']+)["\']',
        r'new Worker\(["\']([^"\']+)["\']',
        r'Worker\(["\']([^"\']+)["\']',
    ]
    for pattern in worker_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if 'worker' in match.lower():
                if match.startswith('http'):
                    urls.add(match)
                elif match.startswith('/'):
                    urls.add(f"{BASE_URL}{match}")
                else:
                    urls.add(f"{BASE_URL}/assets/{match}")
    
    # Pattern 5: Font files
    font_patterns = [
        r'["\']([^"\']*\.(?:woff|woff2|ttf|otf))["\']',
        r'url\(["\']?([^"\']*\.(?:woff|woff2|ttf|otf))["\']?\)',
    ]
    for pattern in font_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if match.startswith('http'):
                urls.add(match)
            elif match.startswith('/'):
                urls.add(f"{BASE_URL}{match}")
            else:
                urls.add(f"{BASE_URL}/assets/fonts/{match}")
    
    # Pattern 6: JSON files (font metadata, configs, etc.)
    json_pattern = r'["\']([^"\']*\.json)["\']'
    matches = re.findall(json_pattern, content)
    for match in matches:
        if match.startswith('http'):
            urls.add(match)
        elif match.startswith('/'):
            urls.add(f"{BASE_URL}{match}")
        else:
            urls.add(f"{BASE_URL}/assets/{match}")
    
    # Pattern 7: Audio files
    audio_pattern = r'["\']([^"\']*\.(?:mp3|wav|ogg|m4a))["\']'
    matches = re.findall(audio_pattern, content)
    for match in matches:
        if match.startswith('http'):
            urls.add(match)
        elif match.startswith('/'):
            urls.add(f"{BASE_URL}{match}")
        else:
            urls.add(f"{BASE_URL}/assets/audio/{match}")
    
    # Pattern 8: GLTF/GLB files
    gltf_pattern = r'["\']([^"\']*\.(?:gltf|glb))["\']'
    matches = re.findall(gltf_pattern, content)
    for match in matches:
        if match.startswith('http'):
            urls.add(match)
        elif match.startswith('/'):
            urls.add(f"{BASE_URL}{match}")
        else:
            urls.add(f"{BASE_URL}/assets/gltf/{match}")
    
    return urls

def download_file(url, local_path):
    """Download a file from URL to local path"""
    try:
        # Create directory if needed
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Skip if file exists and is reasonable size
        if local_path.exists():
            size = local_path.stat().st_size
            if size > 100:  # At least 100 bytes
                return True
        
        # Download using curl
        result = subprocess.run(
            ['curl', '-s', '-f', '-L', '--max-time', '30', url, '-o', str(local_path)],
            capture_output=True,
            timeout=35
        )
        
        if result.returncode == 0 and local_path.exists():
            size = local_path.stat().st_size
            if size > 100:
                return True
            else:
                local_path.unlink()  # Remove too small file
                return False
        return False
    except Exception as e:
        print(f"    Error downloading {url}: {e}")
        return False

def main():
    print("🔍 Scanning all files for assets, graphics, and code...\n")
    
    all_urls = set()
    
    # Files to scan
    files_to_scan = [
        'index.html',
        'igloo_main.js',
        'igloo_app3d.js',
    ]
    
    for file_path in files_to_scan:
        file_path_obj = Path(file_path)
        if file_path_obj.exists():
            print(f"📄 Scanning {file_path}...")
            try:
                with open(file_path_obj, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                urls = extract_all_urls_from_content(content, file_path)
                all_urls.update(urls)
                print(f"  Found {len(urls)} URLs")
            except Exception as e:
                print(f"  Error reading {file_path}: {e}")
    
    # Add known worker files
    known_workers = [
        'audioworker-036a09db.js',
        'bitmapworker-046527f8.js',
        'exrworker-41cbee65.js',
        'msdfworker-ac346fa7.js',
    ]
    for worker in known_workers:
        all_urls.add(f"{BASE_URL}/assets/{worker}")
    
    # Add known asset files
    known_assets = [
        'favicon32-af94112f.png',
        'favicon16-9e4401be.png',
        'images/social.jpg',
    ]
    for asset in known_assets:
        all_urls.add(f"{BASE_URL}/assets/{asset}")
    
    print(f"\n📦 Total unique URLs found: {len(all_urls)}")
    print("\n⬇️  Downloading all files...\n")
    
    downloaded = 0
    failed = 0
    skipped = 0
    
    # Sort URLs for consistent output
    sorted_urls = sorted(all_urls)
    
    for url in sorted_urls:
        if not url.startswith(BASE_URL):
            continue
        
        # Convert URL to local path
        path = url.replace(BASE_URL, '').lstrip('/')
        local_path = BASE_DIR / path
        
        # Check if already exists
        if local_path.exists():
            size = local_path.stat().st_size
            if size > 100:
                print(f"  ✓ Exists: {path} ({size:,} bytes)")
                skipped += 1
                continue
        
        # Download
        print(f"  ⬇️  Downloading: {path}...", end=' ', flush=True)
        if download_file(url, local_path):
            size = local_path.stat().st_size
            print(f"✓ ({size:,} bytes)")
            downloaded += 1
        else:
            print("✗")
            failed += 1
    
    print(f"\n✅ Downloaded: {downloaded}")
    print(f"⏭️  Skipped (already exists): {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(sorted_urls)}")
    
    print("\n✅ Download complete!")
    print(f"\n📁 Files are in: {BASE_DIR.absolute()}")

if __name__ == "__main__":
    main()

