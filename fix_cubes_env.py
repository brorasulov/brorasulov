#!/usr/bin/env python3
import re
import os
import subprocess

# Read the file
with open('igloo_app3d.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find all le.load calls that might reference cubes_env.exr
# The error says it's looking for "cubes_env.exr" (relative path)
# Let's search for any reference to it
patterns = [
    r'le\.load\(["\']([^"\']*cubes_env[^"\']*)["\']',
    r'load\(["\']([^"\']*cubes_env[^"\']*)["\']',
    r'["\']([^"\']*cubes_env\.exr[^"\']*)["\']',
]

found = False
for pattern in patterns:
    matches = re.findall(pattern, content)
    if matches:
        print(f"Found references to cubes_env:")
        for match in matches:
            print(f"  {match}")
            found = True

if not found:
    print("No direct reference found in code, but error suggests it's loaded.")
    print("Trying to find where environment maps are created...")
    
    # Look for environment map creation
    env_patterns = [
        r'fromEquirectangular',
        r'environment',
        r'envmap',
        r'envMap',
    ]
    
    for pattern in env_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"\nFound {len(matches)} references to: {pattern}")
            # Get context around one match
            for match in re.finditer(pattern, content, re.IGNORECASE):
                start = max(0, match.start() - 200)
                end = min(len(content), match.end() + 200)
                context = content[start:end]
                # Look for le.load in this context
                if 'le.load' in context:
                    # Extract the le.load call
                    load_match = re.search(r'le\.load\(["\']([^"\']+)["\']', context)
                    if load_match:
                        print(f"  Found le.load: {load_match.group(1)}")
                    break

# Also check if the file exists
if os.path.exists('assets/images/cubes_env.exr'):
    size = os.path.getsize('assets/images/cubes_env.exr')
    print(f"\n✓ File exists: assets/images/cubes_env.exr ({size} bytes)")
    
    # Copy to assets/ root if needed
    if not os.path.exists('assets/cubes_env.exr'):
        import shutil
        shutil.copy2('assets/images/cubes_env.exr', 'assets/cubes_env.exr')
        print(f"  ✓ Copied to assets/cubes_env.exr")
else:
    print("\n✗ File not found: assets/images/cubes_env.exr")
    print("  Trying to download...")
    
    BASE_URL = "https://www.igloo.inc"
    for path in ['assets/images/cubes_env.exr', 'assets/cubes_env.exr']:
        url = f"{BASE_URL}/{path}"
        result = subprocess.run(['curl', '-s', '-f', '-L', url, '-o', path], 
                              capture_output=True, timeout=10)
        if result.returncode == 0 and os.path.exists(path):
            size = os.path.getsize(path)
            if size > 10000:  # EXR files should be larger
                print(f"  ✓ Downloaded {path} ({size} bytes)")
                break
            else:
                os.remove(path)
                print(f"  ✗ {path} too small ({size} bytes)")

