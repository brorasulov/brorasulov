#!/usr/bin/env python3
import re
import os
import subprocess

# Read App3D file
with open('igloo_app3d.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find all load() calls
patterns = [
    r"le\.load\(['\"]([^'\"]+)['\"]",
    r"zt\.load\(['\"]([^'\"]+)['\"]",
    r"load\(['\"]([^'\"]+\.(?:ktx2|drc|png|jpg|jpeg|exr|gltf|glb|mp3|wav))['\"]",
]

all_paths = set()
for pattern in patterns:
    matches = re.findall(pattern, content)
    all_paths.update(matches)

# Filter valid file paths
valid_paths = []
skip_types = {'data', 'srgb', 'linear', 'repeat', 'colordata', 'datatexture', '3d-data', 'luttetrahedral', 'nearest'}

for path in all_paths:
    # Skip type identifiers
    if path in skip_types:
        continue
    # Skip template strings
    if '${' in path or '`' in path:
        continue
    # Must have file extension
    if '.' in path and not path.startswith('data'):
        # Clean path (remove type suffixes)
        clean_path = path.split('srgb')[0].split('linear')[0].split('repeat')[0].split('data')[0].split('colordata')[0].split('datatexture')[0].split('3d-data')[0].split('luttetrahedral')[0].split('nearest')[0]
        if clean_path and clean_path != path:
            valid_paths.append(clean_path.rstrip('-'))
        else:
            valid_paths.append(path)

# Get unique paths
unique_paths = sorted(set(valid_paths))

print(f"Found {len(unique_paths)} asset paths")
print("\nDownloading...\n")

BASE_URL = "https://www.igloo.inc"
downloaded = 0
failed = 0

for path in unique_paths:
    # Construct full path
    if path.startswith('../'):
        full_path = path[3:]  # Remove ../
    elif path.startswith('assets/'):
        full_path = path
    else:
        full_path = f"assets/{path}"
    
    # Create directory
    dir_path = os.path.dirname(full_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    # Check if exists
    if os.path.exists(full_path):
        print(f"  ✓ Exists: {full_path}")
        downloaded += 1
        continue
    
    # Download
    url = f"{BASE_URL}/{full_path}"
    result = subprocess.run(['curl', '-s', '-f', '-L', url, '-o', full_path], 
                          capture_output=True)
    
    if result.returncode == 0 and os.path.exists(full_path):
        print(f"  ✓ Downloaded: {full_path}")
        downloaded += 1
    else:
        print(f"  ✗ Failed: {url}")
        failed += 1

print(f"\n✅ Downloaded: {downloaded}")
print(f"❌ Failed: {failed}")

