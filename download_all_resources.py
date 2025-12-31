#!/usr/bin/env python3
import re
import os
import urllib.request
import urllib.parse
from pathlib import Path

base_url = "https://www.igloo.inc"
base_dir = Path(".")

def extract_urls_from_file(filepath):
    """Extract all URLs from a file"""
    urls = set()
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Find all URLs
            patterns = [
                r'https://www\.igloo\.inc/[^\s"\'\)]+',
                r'["\']([^"\']*\.(?:js|css|woff|woff2|png|jpg|jpeg|gif|svg|ktx2|drc|mp3|wav|gltf|glb|json))["\']',
                r'load\(["\']([^"\']+)["\']',
                r'src=["\']([^"\']+)["\']',
                r'href=["\']([^"\']+)["\']',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match else ''
                    if match and (match.startswith('http') or match.startswith('/') or match.startswith('./')):
                        if match.startswith('http'):
                            urls.add(match)
                        elif match.startswith('/'):
                            urls.add(base_url + match)
                        elif match.startswith('./'):
                            # Relative path - might need base URL
                            pass
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return urls

def download_file(url, local_path):
    """Download a file from URL to local path"""
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        if os.path.exists(local_path):
            print(f"  ✓ Already exists: {local_path}")
            return True
        
        print(f"  ↓ Downloading: {url}")
        urllib.request.urlretrieve(url, local_path)
        print(f"  ✓ Downloaded: {local_path}")
        return True
    except Exception as e:
        print(f"  ✗ Error downloading {url}: {e}")
        return False

def main():
    print("🔍 Extracting URLs from files...")
    
    # Extract URLs from all JS files
    all_urls = set()
    for js_file in ['igloo_main.js', 'igloo_app3d.js', 'igloo_index.html']:
        if os.path.exists(js_file):
            print(f"📄 Scanning {js_file}...")
            urls = extract_urls_from_file(js_file)
            all_urls.update(urls)
            print(f"  Found {len(urls)} URLs")
    
    # Also add known asset paths
    asset_paths = [
        '/assets/favicon32-af94112f.png',
        '/assets/favicon16-9e4401be.png',
        '/assets/images/social.jpg',
        '/assets/audioworker-036a09db.js',
        '/assets/bitmapworker-046527f8.js',
        '/assets/exrworker-41cbee65.js',
        '/assets/msdfworker-ac346fa7.js',
    ]
    
    for path in asset_paths:
        all_urls.add(base_url + path)
    
    print(f"\n📦 Total unique URLs found: {len(all_urls)}")
    print("\n⬇️  Downloading files...\n")
    
    downloaded = 0
    failed = 0
    
    for url in sorted(all_urls):
        if not url.startswith(base_url):
            continue
        
        # Convert URL to local path
        path = url.replace(base_url, '').lstrip('/')
        local_path = base_dir / path
        
        if download_file(url, local_path):
            downloaded += 1
        else:
            failed += 1
    
    print(f"\n✅ Downloaded: {downloaded}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(all_urls)}")

if __name__ == "__main__":
    main()

