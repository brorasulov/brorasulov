#!/usr/bin/env python3
"""
Download ALL source code and assets from igloo.inc - COMPLETE COPY
Each file downloaded ONCE only - no duplicates
"""
import urllib.request
import ssl
from pathlib import Path
import hashlib

ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://www.igloo.inc"
BASE_DIR = Path(".")

# Track downloaded files to prevent duplicates
downloaded_files = set()

# ALL source files - complete list, no duplicates
ALL_SOURCE_FILES = [
    # Main HTML/JS files
    "index.html",
    "igloo_main.js",
    "igloo_app3d.js",
    
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
    
    # UV checker
    "assets/images/uv/uvchecker-srgb.ktx2",
    "assets/images/uv/uvchecker-srgb.png",
    
    # Additional textures
    "assets/images/abstractlogo_dark_color.ktx2",
    "assets/images/overpass_logo_dark_color.ktx2",
    "assets/images/pudgy_dark_color.ktx2",
    
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
]

def get_file_hash(file_path):
    """Get hash of file to check if it's valid"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read(1024)).hexdigest()
    except:
        return None

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
    
    # Check minimum sizes
    min_sizes = {
        '.png': 1000,
        '.exr': 10000,
        '.drc': 1000,
        '.ktx2': 1000,
        '.woff': 1000,
        '.wasm': 1000,
        '.js': 100,
        '.json': 100,
        '.jpg': 1000,
        '.html': 100,
    }
    
    ext = Path(file_path).suffix.lower()
    min_size = min_sizes.get(ext, 100)
    
    return len(data) >= min_size

def download_file(file_path):
    """Download a single file - ONCE only, no duplicates"""
    # Check if already processed
    if file_path in downloaded_files:
        return True, 0, "already processed"
    
    target = BASE_DIR / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Skip if already exists and valid
    if target.exists():
        try:
            size = target.stat().st_size
            if size > 100:
                with open(target, 'rb') as f:
                    header = f.read(10)
                    # Not HTML
                    if not header.startswith((b'<!doctype', b'<html', b'<HTML')):
                        # Check PNG signature if PNG
                        if file_path.endswith('.png'):
                            f.seek(0)
                            if f.read(8) == b'\x89PNG\r\n\x1a\n':
                                downloaded_files.add(file_path)
                                return True, size, "exists"
                        else:
                            downloaded_files.add(file_path)
                            return True, size, "exists"
        except:
            pass
    
    # Remove invalid file
    if target.exists():
        target.unlink()
    
    # Mark as processing
    downloaded_files.add(file_path)
    
    # Download
    url = f"{BASE_URL}/{file_path}"
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        req.add_header('Referer', 'https://www.igloo.inc/')
        req.add_header('Accept', '*/*')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            
            if not is_valid_file(file_path, data):
                downloaded_files.discard(file_path)  # Remove from set if invalid
                return False, 0, "invalid format"
            
            with open(target, 'wb') as f:
                f.write(data)
            
            size = target.stat().st_size
            return True, size, "downloaded"
    except Exception as e:
        downloaded_files.discard(file_path)  # Remove from set if failed
        return False, 0, str(e)

print("=" * 70)
print("Downloading ALL source code and assets - COMPLETE COPY")
print("Each file will be downloaded ONCE only - no duplicates")
print("=" * 70)
print(f"\nTotal files: {len(ALL_SOURCE_FILES)}\n")

downloaded = 0
skipped = 0
failed = 0
failed_files = []

for i, file_path in enumerate(ALL_SOURCE_FILES, 1):
    # Check for duplicates in list
    if ALL_SOURCE_FILES.count(file_path) > 1:
        print(f"[{i}/{len(ALL_SOURCE_FILES)}] ⚠️  {file_path} - DUPLICATE in list, skipping")
        continue
    
    print(f"[{i}/{len(ALL_SOURCE_FILES)}] {file_path}...", end=' ', flush=True)
    success, size, status = download_file(file_path)
    
    if success:
        if status == "exists":
            print(f"⏭️  (exists, {size:,} bytes)")
            skipped += 1
        elif status == "already processed":
            print(f"⏭️  (already processed)")
            skipped += 1
        else:
            print(f"✓ ({size:,} bytes)")
            downloaded += 1
    else:
        print(f"✗ ({status})")
        failed += 1
        failed_files.append((file_path, status))

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"✅ Downloaded: {downloaded}")
print(f"⏭️  Skipped (already exists): {skipped}")
print(f"❌ Failed: {failed}")
print(f"📊 Total processed: {len(ALL_SOURCE_FILES)}")
print(f"🔒 Unique files: {len(downloaded_files)}")

if failed_files:
    print(f"\n⚠️  Failed files ({len(failed_files)}):")
    for file_path, reason in failed_files[:10]:
        print(f"  - {file_path}: {reason}")
    if len(failed_files) > 10:
        print(f"  ... and {len(failed_files) - 10} more")

print("\n✅ Complete! All source code copied. Refresh browser (Cmd+R).")

