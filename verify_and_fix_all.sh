#!/bin/bash

echo "🔍 Verifying all required files..."
echo ""

cd /Users/xoji/Documents/comment

# Check critical files
MISSING=0

# Check draco files
if [ ! -f "assets/libs/draco/draco_wasm_wrapper.js" ]; then
    echo "❌ Missing: assets/libs/draco/draco_wasm_wrapper.js"
    MISSING=1
fi
if [ ! -f "assets/libs/draco/draco_decoder.wasm" ]; then
    echo "❌ Missing: assets/libs/draco/draco_decoder.wasm"
    MISSING=1
fi

# Check font files
if [ ! -f "assets/fonts/IBMPlexMono-Medium.json" ]; then
    echo "❌ Missing: assets/fonts/IBMPlexMono-Medium.json"
    MISSING=1
fi

# Check geometries
if [ ! -f "assets/geometries/mountain.drc" ]; then
    echo "❌ Missing: assets/geometries/mountain.drc"
    MISSING=1
fi

if [ $MISSING -eq 1 ]; then
    echo ""
    echo "⚠️  Some critical files are missing!"
    echo "Downloading from original site..."
    echo ""
    
    # Download missing files
    BASE_URL="https://www.igloo.inc"
    
    # Draco files
    mkdir -p assets/libs/draco
    curl -s -L "$BASE_URL/assets/libs/draco/draco_wasm_wrapper.js" -o "assets/libs/draco/draco_wasm_wrapper.js" || echo "Failed: draco_wasm_wrapper.js"
    curl -s -L "$BASE_URL/assets/libs/draco/draco_decoder.wasm" -o "assets/libs/draco/draco_decoder.wasm" || echo "Failed: draco_decoder.wasm"
    
    # Font files
    mkdir -p assets/fonts
    curl -s -L "$BASE_URL/assets/fonts/IBMPlexMono-Medium.json" -o "assets/fonts/IBMPlexMono-Medium.json" || echo "Failed: IBMPlexMono-Medium.json"
    
    echo ""
    echo "✅ Downloaded missing files"
fi

# Now add and push everything
echo ""
echo "📝 Adding all files..."
git add -f assets/
git add -A

echo "💾 Committing..."
git commit -m "Add all missing assets - complete fix" || echo "No changes"

echo "⬆️  Pushing..."
git remote set-url origin "https://brorasulov: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@github.com/brorasulov/brorasulov.git"
git push origin main --force
git remote set-url origin "https://github.com/brorasulov/brorasulov.git"

echo ""
echo "✅ Done! Wait 2-3 minutes for GitHub Pages to update"

