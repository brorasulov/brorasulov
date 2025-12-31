#!/usr/bin/env python3
import urllib.request
import os
from pathlib import Path

BASE_URL = "https://www.igloo.inc"
BASE_DIR = Path(".")

files = [
"assets/audioworker-036a09db.js",
"assets/bitmapworker-046527f8.js",
"assets/exrworker-41cbee65.js",
"assets/msdfworker-ac346fa7.js",
"assets/favicon32-af94112f.png",
"assets/favicon16-9e4401be.png",
"assets/images/social.jpg",
"assets/fonts/IBMPlexMono-Medium.json",
"assets/fonts/IBMPlexMono-Medium-datatexture.ktx2",
"assets/fonts/IBMPlexMono-Regular-datatexture.ktx2",
"assets/IBMPlexMono-Medium-1e253194.woff",
"assets/IBMPlexMono-Regular-419d45f6.woff",
"assets/libs/draco/draco_wasm_wrapper.js",
"assets/libs/draco/draco_decoder.wasm",
"assets/libs/basis/basis_transcoder.js",
"assets/libs/basis/basis_transcoder.wasm",
"assets/images/cubes/bg.png",
"assets/images/cubes/advect.png",
"assets/images/cubes/blurrytext_atlas.ktx2",
"assets/images/cubes/cube_scene.ktx2",
"assets/images/cubes/dot_pattern.ktx2",
"assets/images/cubes_env.exr",
"assets/images/igloo/ground_color.ktx2",
"assets/images/igloo/ground_glow.ktx2",
"assets/images/igloo/ground_sansigloo_color.ktx2",
"assets/images/igloo/igloo_color.ktx2",
"assets/images/igloo/igloo_exploded_color.ktx2",
"assets/images/igloo/igloo_scene.ktx2",
"assets/images/igloo/mountain_color.ktx2",
"assets/images/igloo/numbers.ktx2",
"assets/images/igloo/triangles_tiling.ktx2",
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
"assets/images/ui/arrow-datatexture.ktx2",
"assets/images/ui/close-datatexture.ktx2",
"assets/images/ui/logo-datatexture.ktx2",
"assets/images/ui/sound-datatexture.ktx2",
"assets/images/ui/visit-datatexture.ktx2",
"assets/images/volumes/medium_32.ktx2",
"assets/images/volumes/peachesbody_64.ktx2",
"assets/images/volumes/x_64.ktx2",
"assets/geometries/cubes/background_shapes.drc",
"assets/geometries/igloo/igloo_cage.drc",
"assets/geometries/igloo/igloo_outline.drc",
"assets/geometries/igloo/patch.drc",
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
"assets/images/abstractlogo_dark_color.ktx2",
"assets/images/overpass_logo_dark_color.ktx2",
"assets/images/pudgy_dark_color.ktx2",
"assets/images/uv/uvchecker-srgb.ktx2",
"assets/images/uv/uvchecker-srgb.png",
]

print(f"Downloading {len(files)} files...\n")
downloaded = 0
skipped = 0
failed = 0

for f in files:
    local_path = BASE_DIR / f
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    if local_path.exists() and local_path.stat().st_size > 100:
        print(f"✓ {f} (exists)")
        skipped += 1
        continue
    
    url = f"{BASE_URL}/{f}"
    try:
        urllib.request.urlretrieve(url, str(local_path))
        if local_path.exists() and local_path.stat().st_size > 100:
            size = local_path.stat().st_size
            print(f"✓ {f} ({size:,} bytes)")
            downloaded += 1
        else:
            print(f"✗ {f} (too small)")
            failed += 1
            if local_path.exists():
                local_path.unlink()
    except Exception as e:
        print(f"✗ {f} - {e}")
        failed += 1

print(f"\n✅ Downloaded: {downloaded}")
print(f"⏭️  Skipped: {skipped}")
print(f"❌ Failed: {failed}")
print(f"📊 Total: {len(files)}")

