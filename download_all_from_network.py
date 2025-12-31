#!/usr/bin/env python3
"""
Download ALL files from igloo.inc website - one time only, no duplicates
Based on Network tab analysis
"""
import urllib.request
import ssl
import json
from pathlib import Path
from urllib.parse import urlparse

ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://www.igloo.inc"
BASE_DIR = Path(".")

# ALL files from Network tab - complete list, no duplicates
ALL_FILES = [
    # Main JS files
    "igloo_main.js",
    "igloo_app3d.js",
    "index.html",
    
    # Worker files
    "assets/audioworker-036a09db.js",
    "assets/bitmapworker-046527f8.js",
    "assets/exrworker-41cbee65.js",
    "assets/msdfworker-ac346fa7.js",
    
    # Favicons
    "assets/favicon32-af94112f.png",
    "assets/favicon16-9e4401be.png",
    "assets/images/social.jpg",
    
    # Fonts
    "assets/fonts/IBMPlexMono-Medium.json",
    "assets/fonts/IBMPlexMono-Medium-datatexture.ktx2",
    "assets/fonts/IBMPlexMono-Regular-datatexture.ktx2",
    "assets/IBMPlexMono-Medium-1e253194.woff",
    "assets/IBMPlexMono-Regular-419d45f6.woff",
    
    # Libraries
    "assets/libs/draco/draco_wasm_wrapper.js",
    "assets/libs/draco/draco_decoder.wasm",
    "assets/libs/basis/basis_transcoder.js",
    "assets/libs/basis/basis_transcoder.wasm",
    
    # Cubes textures
    "assets/images/cubes/bg.png",
    "assets/images/cubes/advect.png",
    "assets/images/cubes/blurrytext_atlas.ktx2",
    "assets/images/cubes/cube_scene.ktx2",
    "assets/images/cubes/dot_pattern.ktx2",
    "assets/images/cubes_env.exr",
    
    # Igloo textures
    "assets/images/igloo/ground_color.ktx2",
    "assets/images/igloo/ground_glow.ktx2",
    "assets/images/igloo/ground_sansigloo_color.ktx2",
    "assets/images/igloo/igloo_color.ktx2",
    "assets/images/igloo/igloo_exploded_color.ktx2",
    "assets/images/igloo/igloo_scene.ktx2",
    "assets/images/igloo/mountain_color.ktx2",
    "assets/images/igloo/numbers.ktx2",
    "assets/images/igloo/triangles_tiling.ktx2",
    
    # Other textures
    "assets/images/bokeh.ktx2",
    "assets/images/caustics.ktx2",
    "assets/images/clouds_noise.ktx2",
    "assets/images/floor_color.ktx2",
    "assets/images/frost-datatexture.ktx2",
    "assets/images/mosaic.ktx2",
    "assets/images/noises/blue-8-128-rgb.ktx2",
    "assets/images/numbers-datatexture.ktx2",
    "assets/images/perlin-datatexture.ktx2",
    "assets/images/perlin-datatexture.png",
    "assets/images/scroll-datatexture.ktx2",
    "assets/images/shapes_blurred.ktx2",
    "assets/images/wind_noise.ktx2",
    "assets/images/shattered_ring_ao.ktx2",
    "assets/images/shattered_ring_color.ktx2",
    "assets/images/shattered_ring2_ao.ktx2",
    "assets/images/shattered_ring2_color.ktx2",
    
    # UI textures
    "assets/images/ui/arrow-datatexture.ktx2",
    "assets/images/ui/close-datatexture.ktx2",
    "assets/images/ui/logo-datatexture.ktx2",
    "assets/images/ui/sound-datatexture.ktx2",
    "assets/images/ui/visit-datatexture.ktx2",
    
    # Volumes
    "assets/images/volumes/medium_32.ktx2",
    "assets/images/volumes/peachesbody_64.ktx2",
    "assets/images/volumes/x_64.ktx2",
    
    # Geometries - Cubes
    "assets/geometries/cubes/background_shapes.drc",
    
    # Geometries - Igloo
    "assets/geometries/igloo/igloo_cage.drc",
    "assets/geometries/igloo/igloo_outline.drc",
    "assets/geometries/igloo/patch.drc",
    
    # Geometries - Main
    "assets/geometries/blurrytext.drc",
    "assets/geometries/blurrytext_cylinder.drc",
    "assets/geometries/ceilingsmoke.drc",
    "assets/geometries/floor.drc",
    "assets/geometries/ground.drc",
    "assets/geometries/intro_particles.drc",
    "assets/geometries/mountain.drc",
    "assets/geometries/shattered_ring.drc",
    "assets/geometries/shattered_ring2.drc",
    "assets/geometries/shattered_ring_smoke.drc",
    "assets/geometries/smoke_trail.drc",
    "assets/geometries/abstractlogo.drc",
    "assets/geometries/overpass_logo.drc",
    "assets/geometries/pudgy.drc",
    
    # Additional textures
    "assets/images/abstractlogo_dark_color.ktx2",
    "assets/images/overpass_logo_dark_color.ktx2",
    "assets/images/pudgy_dark_color.ktx2",
    "assets/images/uv/uvchecker-srgb.ktx2",
    "assets/images/uv/uvchecker-srgb.png",
]

def is_valid_file(file_path, data):
    """Check if downloaded file is valid (not HTML)"""
    if len(data) < 10:
        return False
    
    # Check if HTML
    if data[:10].startswith((b'<!doctype', b'<html', b'<HTML')):
        return False
    
    # Check PNG
    if file_path.endswith('.png') and data[:8] != b'\x89PNG\r\n\x1a\n':
        return False
    
    # Check minimum size
    if file_path.endswith('.png') and len(data) < 1000:
        return False
    if file_path.endswith('.exr') and len(data) < 10000:
        return False
    if file_path.endswith('.drc') and len(data) < 1000:
        return False
    if file_path.endswith('.ktx2') and len(data) < 1000:
        return False
    if file_path.endswith('.woff') and len(data) < 1000:
        return False
    if file_path.endswith('.wasm') and len(data) < 1000:
        return False
    if file_path.endswith('.js') and len(data) < 100:
        return False
    
    return True

def download_file(file_path):
    """Download a single file"""
    target = BASE_DIR / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Skip if already exists and valid
    if target.exists():
        try:
            size = target.stat().st_size
            if size > 100:
                with open(target, 'rb') as f:
                    header = f.read(10)
                    if not header.startswith((b'<!doctype', b'<html', b'<HTML')):
                        return True, size, "exists"
        except:
            pass
    
    # Download
    url = f"{BASE_URL}/{file_path}"
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        req.add_header('Referer', 'https://www.igloo.inc/')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            
            if not is_valid_file(file_path, data):
                return False, 0, "invalid"
            
            with open(target, 'wb') as f:
                f.write(data)
            
            size = target.stat().st_size
            return True, size, "downloaded"
    except Exception as e:
        return False, 0, str(e)

print(f"Downloading {len(ALL_FILES)} files from Network tab...\n")
print("Each file will be downloaded ONCE only.\n")

downloaded = 0
skipped = 0
failed = 0

for file_path in ALL_FILES:
    success, size, status = download_file(file_path)
    
    if success:
        if status == "exists":
            print(f"⏭️  {file_path} (already exists, {size:,} bytes)")
            skipped += 1
        else:
            print(f"✓ {file_path} ({size:,} bytes)")
            downloaded += 1
    else:
        print(f"✗ {file_path} - {status}")
        failed += 1

print(f"\n✅ Downloaded: {downloaded}")
print(f"⏭️  Skipped: {skipped}")
print(f"❌ Failed: {failed}")
print(f"📊 Total: {len(ALL_FILES)}")
print("\n✅ All files processed! Refresh browser (Cmd+R).")

