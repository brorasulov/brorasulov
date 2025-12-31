#!/bin/bash

BASE_URL="https://www.igloo.inc"

echo "Fixing missing files..."

# Ensure directories exist
mkdir -p assets/cubes assets/images/cubes 2>/dev/null

# Files that need to be in assets/cubes/ (relative to assets/)
files=(
    "cubes/bg.png"
    "cubes/advect.png"
    "cubes_env.exr"
)

for file in "${files[@]}"; do
    target="assets/$file"
    target_dir=$(dirname "$target")
    
    # Create directory
    mkdir -p "$target_dir" 2>/dev/null
    
    # Check if file exists in images/
    source="assets/images/$file"
    if [ -f "$source" ]; then
        size=$(stat -f%z "$source" 2>/dev/null || echo 0)
        if [ "$size" -gt 5000 ]; then
            cp "$source" "$target" 2>/dev/null && echo "✓ Copied $source → $target"
        fi
    fi
    
    # If still missing, try to download
    if [ ! -f "$target" ] || [ "$(stat -f%z "$target" 2>/dev/null || echo 0)" -lt 5000 ]; then
        # Try different URL paths
        for url_path in "assets/images/$file" "assets/$file"; do
            url="$BASE_URL/$url_path"
            if curl -s -f -L "$url" -o "$target" 2>/dev/null; then
                size=$(stat -f%z "$target" 2>/dev/null || echo 0)
                if [ "$size" -gt 5000 ]; then
                    echo "✓ Downloaded $target from $url_path ($size bytes)"
                    break
                else
                    rm -f "$target"
                fi
            fi
        done
    fi
done

echo "✅ Done!"

