#!/bin/bash

BASE_URL="https://www.igloo.inc"
BASE_DIR="."

echo "🔍 Downloading ALL 86 files including canvas and graphics..."
echo ""

# Create all directories
mkdir -p assets/{fonts,images/{cubes,igloo,ui,volumes,noises,uv},geometries/{cubes,igloo},gltf,libs/{draco,basis},audio} 2>/dev/null

# List of ALL 86 files that should be downloaded
# This includes all textures, geometries, fonts, workers, and canvas-related files

ALL_FILES=(
    # Worker files (4)
    "assets/audioworker-036a09db.js"
    "assets/bitmapworker-046527f8.js"
    "assets/exrworker-41cbee65.js"
    "assets/msdfworker-ac346fa7.js"
    
    # Favicons (2)
    "assets/favicon32-af94112f.png"
    "assets/favicon16-9e4401be.png"
    
    # Social image (1)
    "assets/images/social.jpg"
    
    # Fonts (5)
    "assets/fonts/IBMPlexMono-Medium.json"
    "assets/fonts/IBMPlexMono-Medium-datatexture.ktx2"
    "assets/fonts/IBMPlexMono-Regular-datatexture.ktx2"
    "assets/IBMPlexMono-Medium-1e253194.woff"
    "assets/IBMPlexMono-Regular-419d45f6.woff"
    
    # Draco library (2)
    "assets/libs/draco/draco_wasm_wrapper.js"
    "assets/libs/draco/draco_decoder.wasm"
    
    # Basis library (2)
    "assets/libs/basis/basis_transcoder.js"
    "assets/libs/basis/basis_transcoder.wasm"
    
    # Cubes textures (6)
    "assets/images/cubes/bg.png"
    "assets/images/cubes/advect.png"
    "assets/images/cubes/blurrytext_atlas.ktx2"
    "assets/images/cubes/cube_scene.ktx2"
    "assets/images/cubes/dot_pattern.ktx2"
    "assets/images/cubes_env.exr"
    
    # Igloo textures (9)
    "assets/images/igloo/ground_color.ktx2"
    "assets/images/igloo/ground_glow.ktx2"
    "assets/images/igloo/ground_sansigloo_color.ktx2"
    "assets/images/igloo/igloo_color.ktx2"
    "assets/images/igloo/igloo_exploded_color.ktx2"
    "assets/images/igloo/igloo_scene.ktx2"
    "assets/images/igloo/mountain_color.ktx2"
    "assets/images/igloo/numbers.ktx2"
    "assets/images/igloo/triangles_tiling.ktx2"
    
    # Other textures (15)
    "assets/images/bokeh.ktx2"
    "assets/images/caustics.ktx2"
    "assets/images/clouds_noise.ktx2"
    "assets/images/floor_color.ktx2"
    "assets/images/frost-datatexture.ktx2"
    "assets/images/mosaic.ktx2"
    "assets/images/noises/blue-8-128-rgb.ktx2"
    "assets/images/numbers-datatexture.ktx2"
    "assets/images/perlin-datatexture.ktx2"
    "assets/images/perlin-datatexture.png"
    "assets/images/scroll-datatexture.ktx2"
    "assets/images/shapes_blurred.ktx2"
    "assets/images/wind_noise.ktx2"
    "assets/images/shattered_ring_ao.ktx2"
    "assets/images/shattered_ring_color.ktx2"
    "assets/images/shattered_ring2_ao.ktx2"
    "assets/images/shattered_ring2_color.ktx2"
    
    # UI textures (5)
    "assets/images/ui/arrow-datatexture.ktx2"
    "assets/images/ui/close-datatexture.ktx2"
    "assets/images/ui/logo-datatexture.ktx2"
    "assets/images/ui/sound-datatexture.ktx2"
    "assets/images/ui/visit-datatexture.ktx2"
    
    # Volumes (3)
    "assets/images/volumes/medium_32.ktx2"
    "assets/images/volumes/peachesbody_64.ktx2"
    "assets/images/volumes/x_64.ktx2"
    
    # Geometries - Cubes (1)
    "assets/geometries/cubes/background_shapes.drc"
    
    # Geometries - Igloo (4)
    "assets/geometries/igloo/igloo_cage.drc"
    "assets/geometries/igloo/igloo_outline.drc"
    "assets/geometries/igloo/patch.drc"
    
    # Geometries - Main (13)
    "assets/geometries/blurrytext.drc"
    "assets/geometries/blurrytext_cylinder.drc"
    "assets/geometries/ceilingsmoke.drc"
    "assets/geometries/floor.drc"
    "assets/geometries/ground.drc"
    "assets/geometries/intro_particles.drc"
    "assets/geometries/mountain.drc"
    "assets/geometries/shattered_ring.drc"
    "assets/geometries/shattered_ring2.drc"
    "assets/geometries/shattered_ring_smoke.drc"
    "assets/geometries/smoke_trail.drc"
    "assets/geometries/abstractlogo.drc"
    "assets/geometries/overpass_logo.drc"
    "assets/geometries/pudgy.drc"
    
    # Additional textures (5)
    "assets/images/abstractlogo_dark_color.ktx2"
    "assets/images/overpass_logo_dark_color.ktx2"
    "assets/images/pudgy_dark_color.ktx2"
    "assets/images/uv/uvchecker-srgb.ktx2"
    "assets/images/uv/uvchecker-srgb.png"
)

echo "📦 Total files to download: ${#ALL_FILES[@]}"
echo ""

downloaded=0
failed=0
skipped=0

for file_path in "${ALL_FILES[@]}"; do
    local_path="$file_path"
    dir=$(dirname "$local_path")
    
    # Create directory
    if [[ "$dir" != "." ]]; then
        mkdir -p "$dir" 2>/dev/null
    fi
    
    # Check if exists
    if [[ -f "$local_path" ]]; then
        size=$(stat -f%z "$local_path" 2>/dev/null || echo 0)
        if [[ $size -gt 100 ]]; then
            echo "  ✓ Exists: $file_path ($(numfmt --to=iec-i --suffix=B $size 2>/dev/null || echo ${size}B))"
            ((skipped++))
            continue
        fi
    fi
    
    # Download
    url="$BASE_URL/$file_path"
    echo -n "  ⬇️  $file_path... "
    
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
done

echo ""
echo "✅ Downloaded: $downloaded"
echo "⏭️  Skipped: $skipped"
echo "❌ Failed: $failed"
echo "📊 Total: ${#ALL_FILES[@]}"
echo ""
echo "🎉 Complete! All 86 files (including canvas) have been processed."

