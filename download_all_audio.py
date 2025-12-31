#!/usr/bin/env python3
"""
Download ALL audio files for igloo.inc
"""
import urllib.request
import ssl
from pathlib import Path

ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://www.igloo.inc"
BASE_DIR = Path(".")

# All audio files from the code
audio_files = [
    "music-highq.ogg",
    "room.ogg",
    "wind.ogg",
    "igloo.ogg",
    "beeps.ogg",
    "beeps2.ogg",
    "beeps3.ogg",
    "click-project.ogg",
    "enter-project.ogg",
    "leave-project.ogg",
    "shard.ogg",
    "project-text.ogg",
    "circles.ogg",
    "particles.ogg",
    "logo.ogg",
    "ui-long.ogg",
    "ui-short.ogg",
    "manifesto.ogg",
]

print("Downloading all audio files...\n")

downloaded = 0
failed = 0

for audio_file in audio_files:
    file_path = f"assets/audio/{audio_file}"
    url = f"{BASE_URL}/{file_path}"
    target = BASE_DIR / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    if target.exists():
        size = target.stat().st_size
        print(f"✓ {file_path} already exists ({size:,} bytes)")
        downloaded += 1
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
                failed += 1
                continue
            
            # Check size (should be > 100 bytes for audio)
            if len(data) < 100:
                print("✗ (too small)")
                failed += 1
                continue
            
            # Write
            with open(target, 'wb') as f:
                f.write(data)
            
            size = target.stat().st_size
            print(f"✓ ({size:,} bytes)")
            downloaded += 1
                
    except Exception as e:
        print(f"✗ Error: {e}")
        failed += 1

print(f"\n✅ Downloaded: {downloaded}")
print(f"❌ Failed: {failed}")
print(f"📊 Total: {len(audio_files)}")
print("\nRefresh browser (Cmd+R) and check if sound works!")

