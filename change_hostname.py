#!/usr/bin/env python3
"""
Change localhost to rasulov in all files
"""
import re
from pathlib import Path

BASE_DIR = Path(".")

# Files to check
files_to_check = [
    "index.html",
    "igloo_main.js",
    "igloo_app3d.js",
]

print("Changing localhost to rasulov...\n")

for file_path in files_to_check:
    target = BASE_DIR / file_path
    if not target.exists():
        print(f"⚠ {file_path} not found, skipping")
        continue
    
    with open(target, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_content = content
    
    # Replace localhost:8000 with rasulov:8000
    content = re.sub(r'localhost:8000', 'rasulov:8000', content)
    content = re.sub(r'http://localhost', 'http://rasulov', content)
    content = re.sub(r'https://localhost', 'https://rasulov', content)
    content = re.sub(r'127\.0\.0\.1:8000', 'rasulov:8000', content)
    content = re.sub(r'127\.0\.0\.1', 'rasulov', content)
    
    if content != original_content:
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated {file_path}")
    else:
        print(f"  No changes needed in {file_path}")

print("\n✅ Done!")
print("\nNow you can access the site at: http://rasulov:8000")
print("Or if you want to use rasulov.local: http://rasulov.local:8000")

