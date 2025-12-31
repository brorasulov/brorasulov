#!/usr/bin/env python3
"""
Download audio files for igloo.inc
"""
import urllib.request
import ssl
from pathlib import Path

ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://www.igloo.inc"
BASE_DIR = Path(".")

# Audio files needed
audio_files = {
    "assets/audio/music-highq.ogg": "https://www.igloo.inc/assets/audio/music-highq.ogg",
}

print("Downloading audio files...\n")

for file_path, url in audio_files.items():
    target = BASE_DIR / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    if target.exists():
        size = target.stat().st_size
        print(f"✓ {file_path} already exists ({size:,} bytes)")
        continue
    
    print(f"Downloading {file_path}...", end=' ', flush=True)
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://www.igloo.inc/',
            'Accept': 'audio/ogg,audio/*,*/*;q=0.8',
        })
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            
            # Check if HTML
            if data[:20].startswith((b'<!doctype', b'<html', b'<HTML', b'<!DOCTYPE')):
                print("✗ (got HTML)")
                continue
            
            # Write
            with open(target, 'wb') as f:
                f.write(data)
            
            size = target.stat().st_size
            print(f"✓ ({size:,} bytes)")
                
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n✅ Audio download complete!")
print("Refresh browser (Cmd+R) and check if sound works.")

