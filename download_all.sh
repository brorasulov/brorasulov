#!/bin/bash

BASE_URL="https://www.igloo.inc"
BASE_DIR="."

# Create directories
mkdir -p assets/{fonts,images,gltf,geometries,libs/{draco,basis},audio} 2>/dev/null

# Extract all URLs from files
echo "🔍 Extracting URLs..."

# Get all URLs from JS files
grep -roh 'https://www\.igloo\.inc[^"'\'' )]*' igloo_main.js igloo_app3d.js igloo_index.html | sort -u > all_urls.txt

# Get asset paths from le.load() calls
grep -o 'le\.load([^)]*' igloo_app3d.js | grep -o '"[^"]*"' | sed 's/"//g' | while read path; do
    if [[ $path == assets/* ]]; then
        echo "$BASE_URL/$path" >> all_urls.txt
    fi
done

# Add known worker files
echo "$BASE_URL/assets/audioworker-036a09db.js" >> all_urls.txt
echo "$BASE_URL/assets/bitmapworker-046527f8.js" >> all_urls.txt
echo "$BASE_URL/assets/exrworker-41cbee65.js" >> all_urls.txt
echo "$BASE_URL/assets/msdfworker-ac346fa7.js" >> all_urls.txt

# Sort and get unique URLs
sort -u all_urls.txt > unique_urls.txt

echo "📦 Found $(wc -l < unique_urls.txt) unique URLs"
echo ""
echo "⬇️  Downloading files..."
echo ""

downloaded=0
failed=0

while IFS= read -r url; do
    # Convert URL to local path
    local_path="${url#$BASE_URL/}"
    local_path="${local_path#/}"
    
    # Create directory if needed
    dir=$(dirname "$local_path")
    if [ "$dir" != "." ]; then
        mkdir -p "$dir" 2>/dev/null
    fi
    
    # Check if file already exists
    if [ -f "$local_path" ]; then
        echo "  ✓ Already exists: $local_path"
        ((downloaded++))
        continue
    fi
    
    # Download file
    if curl -s -f -L "$url" -o "$local_path" 2>/dev/null; then
        echo "  ✓ Downloaded: $local_path"
        ((downloaded++))
    else
        echo "  ✗ Failed: $url"
        ((failed++))
    fi
done < unique_urls.txt

echo ""
echo "✅ Downloaded: $downloaded"
echo "❌ Failed: $failed"
echo "📊 Total: $(wc -l < unique_urls.txt)"

