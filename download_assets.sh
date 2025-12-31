#!/bin/bash

BASE_URL="https://www.igloo.inc"
BASE_DIR="."

echo "🔍 Finding all asset paths from App3D file..."

# Extract all le.load() paths
grep -o 'le\.load([^)]*' igloo_app3d.js | \
    sed "s/le\.load(//g" | \
    sed "s/[,\"']//g" | \
    grep -v '^$' | \
    sort -u > asset_paths.txt

# Also extract zt.load() paths (geometry loader)
grep -o 'zt\.load([^)]*' igloo_app3d.js | \
    sed "s/zt\.load(//g" | \
    sed "s/[,\"']//g" | \
    grep -v '^$' | \
    sort -u >> asset_paths.txt

# Extract paths from load() calls
grep -o 'load([^)]*' igloo_app3d.js | \
    sed "s/load(//g" | \
    sed "s/[,\"']//g" | \
    grep -E '\.(ktx2|drc|png|jpg|jpeg|gltf|glb|exr|mp3|wav|json)' | \
    sort -u >> asset_paths.txt

# Get unique paths
sort -u asset_paths.txt > unique_paths.txt

echo "📦 Found $(wc -l < unique_paths.txt) asset paths"
echo ""

# Download each asset
downloaded=0
failed=0

while IFS= read -r path; do
    # Skip if path is empty or just a type
    if [[ -z "$path" ]] || [[ "$path" =~ ^(data|srgb|linear|repeat|colordata|datatexture)$ ]]; then
        continue
    fi
    
    # Construct full path
    if [[ "$path" == assets/* ]]; then
        full_path="$path"
    elif [[ "$path" == ../* ]]; then
        # Relative path like ../fonts/...
        full_path="${path#../}"
    else
        # Assume it's in assets/
        full_path="assets/$path"
    fi
    
    # Create directory
    dir=$(dirname "$full_path")
    if [ "$dir" != "." ]; then
        mkdir -p "$dir" 2>/dev/null
    fi
    
    # Construct URL
    url="$BASE_URL/$full_path"
    
    # Check if file exists
    if [ -f "$full_path" ]; then
        echo "  ✓ Exists: $full_path"
        ((downloaded++))
        continue
    fi
    
    # Download
    if curl -s -f -L "$url" -o "$full_path" 2>/dev/null; then
        echo "  ✓ Downloaded: $full_path"
        ((downloaded++))
    else
        echo "  ✗ Failed: $url"
        ((failed++))
    fi
done < unique_paths.txt

echo ""
echo "✅ Downloaded: $downloaded"
echo "❌ Failed: $failed"

