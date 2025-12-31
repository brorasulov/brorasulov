#!/bin/bash

BASE_URL="https://www.igloo.inc"
BASE_DIR="."

echo "🔍 Scanning and downloading ALL assets, graphics, code, and resources..."
echo ""

# Create all necessary directories
mkdir -p assets/{fonts,images/{cubes,igloo,ui,volumes,noises,uv},geometries/{cubes,igloo},gltf,libs/{draco,basis},audio} 2>/dev/null

# Extract all URLs from JavaScript files
echo "📄 Extracting URLs from code files..."

# Get all full URLs
grep -roh 'https://www\.igloo\.inc[^"'\'' )]*' igloo_main.js igloo_app3d.js index.html 2>/dev/null | sort -u > all_extracted_urls.txt

# Extract le.load() paths
grep -o 'le\.load([^)]*' igloo_app3d.js 2>/dev/null | \
    sed "s/le\.load(//g" | \
    sed "s/[,\"']//g" | \
    grep -E '\.(ktx2|drc|png|jpg|jpeg|exr|json|woff|woff2)' | \
    sed 's/srgb.*$//' | \
    sed 's/linear.*$//' | \
    sed 's/repeat.*$//' | \
    sed 's/data.*$//' | \
    sed 's/colordata.*$//' | \
    sed 's/datatexture.*$//' | \
    sed 's/3d-data.*$//' | \
    sed 's/luttetrahedral.*$//' | \
    sed 's/nearest.*$//' | \
    sed 's/-$//' | \
    grep -v '^$' | \
    while read path; do
        if [[ $path == assets/* ]]; then
            echo "$BASE_URL/$path" >> all_extracted_urls.txt
        elif [[ $path == ../* ]]; then
            echo "$BASE_URL/assets/${path#../}" >> all_extracted_urls.txt
        elif [[ $path == *.drc ]]; then
            echo "$BASE_URL/assets/geometries/$path" >> all_extracted_urls.txt
        elif [[ $path == *.ktx2 ]] || [[ $path == *.png ]] || [[ $path == *.jpg ]] || [[ $path == *.exr ]]; then
            echo "$BASE_URL/assets/images/$path" >> all_extracted_urls.txt
        else
            echo "$BASE_URL/assets/$path" >> all_extracted_urls.txt
        fi
    done

# Extract zt.load() paths (geometries)
grep -o 'zt\.load([^)]*' igloo_app3d.js 2>/dev/null | \
    sed "s/zt\.load(//g" | \
    sed "s/[,\"']//g" | \
    grep -E '\.drc' | \
    while read path; do
        if [[ $path == assets/* ]]; then
            echo "$BASE_URL/$path" >> all_extracted_urls.txt
        else
            echo "$BASE_URL/assets/geometries/$path" >> all_extracted_urls.txt
        fi
    done

# Add known worker files
echo "$BASE_URL/assets/audioworker-036a09db.js" >> all_extracted_urls.txt
echo "$BASE_URL/assets/bitmapworker-046527f8.js" >> all_extracted_urls.txt
echo "$BASE_URL/assets/exrworker-41cbee65.js" >> all_extracted_urls.txt
echo "$BASE_URL/assets/msdfworker-ac346fa7.js" >> all_extracted_urls.txt

# Add known assets
echo "$BASE_URL/assets/favicon32-af94112f.png" >> all_extracted_urls.txt
echo "$BASE_URL/assets/favicon16-9e4401be.png" >> all_extracted_urls.txt
echo "$BASE_URL/assets/images/social.jpg" >> all_extracted_urls.txt

# Get unique URLs
sort -u all_extracted_urls.txt > unique_all_urls.txt

echo "📦 Found $(wc -l < unique_all_urls.txt | tr -d ' ') unique URLs"
echo ""
echo "⬇️  Downloading all files..."
echo ""

downloaded=0
failed=0
skipped=0

while IFS= read -r url; do
    # Convert URL to local path
    local_path="${url#$BASE_URL/}"
    local_path="${local_path#/}"
    
    # Skip if empty
    [[ -z "$local_path" ]] && continue
    
    # Create directory if needed
    dir=$(dirname "$local_path")
    if [[ "$dir" != "." ]]; then
        mkdir -p "$dir" 2>/dev/null
    fi
    
    # Check if file already exists
    if [[ -f "$local_path" ]]; then
        size=$(stat -f%z "$local_path" 2>/dev/null || echo 0)
        if [[ $size -gt 100 ]]; then
            echo "  ✓ Exists: $local_path ($(numfmt --to=iec-i --suffix=B $size 2>/dev/null || echo ${size}B))"
            ((skipped++))
            continue
        fi
    fi
    
    # Download file
    echo -n "  ⬇️  $local_path... "
    if curl -s -f -L --max-time 30 "$url" -o "$local_path" 2>/dev/null; then
        size=$(stat -f%z "$local_path" 2>/dev/null || echo 0)
        if [[ $size -gt 100 ]]; then
            echo "✓ ($(numfmt --to=iec-i --suffix=B $size 2>/dev/null || echo ${size}B))"
            ((downloaded++))
        else
            rm -f "$local_path" 2>/dev/null
            echo "✗ (too small)"
            ((failed++))
        fi
    else
        echo "✗"
        ((failed++))
    fi
done < unique_all_urls.txt

echo ""
echo "✅ Downloaded: $downloaded"
echo "⏭️  Skipped (already exists): $skipped"
echo "❌ Failed: $failed"
echo "📊 Total: $(wc -l < unique_all_urls.txt | tr -d ' ')"
echo ""
echo "🎉 Complete! All assets, graphics, and code have been downloaded."

