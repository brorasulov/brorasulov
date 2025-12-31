#!/usr/bin/env python3
import urllib.request
import ssl
from pathlib import Path

ssl._create_default_https_context = ssl._create_unverified_context

files = {
    "assets/images/cubes/bg.png": "https://www.igloo.inc/assets/images/cubes/bg.png",
    "assets/images/cubes/advect.png": "https://www.igloo.inc/assets/images/cubes/advect.png",
    "assets/images/cubes_env.exr": "https://www.igloo.inc/assets/images/cubes_env.exr",
}

for f, url in files.items():
    p = Path(f)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        p.unlink()
    print(f"Downloading {f}...", end=' ')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.igloo.inc/'})
        data = urllib.request.urlopen(req, timeout=30).read()
        if not data.startswith(b'<!doctype') and (not f.endswith('.png') or data[:8] == b'\x89PNG\r\n\x1a\n'):
            open(f, 'wb').write(data)
            print(f"✓ ({len(data):,} bytes)")
        else:
            print("✗ (HTML or invalid)")
    except Exception as e:
        print(f"✗ ({e})")

print("\nDone!")

