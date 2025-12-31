#!/usr/bin/env python3
"""
Barcha muammolarni hal qilish va GitHub'ga push qilish
"""
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path("/Users/xoji/Documents/comment")
BASE_URL = "https://www.igloo.inc"

# Yetishmayotgan kritik fayllar ro'yxati
CRITICAL_FILES = [
    # Draco
    ("assets/libs/draco/draco_wasm_wrapper.js", "assets/libs/draco/draco_wasm_wrapper.js"),
    ("assets/libs/draco/draco_decoder.wasm", "assets/libs/draco/draco_decoder.wasm"),
    
    # Fonts
    ("assets/fonts/IBMPlexMono-Medium.json", "assets/fonts/IBMPlexMono-Medium.json"),
    
    # Worker files
    ("assets/audioworker-036a09db.js", "assets/audioworker-036a09db.js"),
    ("assets/bitmapworker-046527f8.js", "assets/bitmapworker-046527f8.js"),
    ("assets/exrworker-41cbee65.js", "assets/exrworker-41cbee65.js"),
    ("assets/msdfworker-ac346fa7.js", "assets/msdfworker-ac346fa7.js"),
    
    # Geometries
    ("assets/geometries/mountain.drc", "assets/geometries/mountain.drc"),
    ("assets/geometries/igloo.drc", "assets/geometries/igloo.drc"),
    ("assets/geometries/ground.drc", "assets/geometries/ground.drc"),
    ("assets/geometries/igloo/igloo_cage.drc", "assets/geometries/igloo/igloo_cage.drc"),
    ("assets/geometries/igloo/igloo_outline.drc", "assets/geometries/igloo/igloo_outline.drc"),
    ("assets/geometries/igloo/patch.drc", "assets/geometries/igloo/patch.drc"),
    ("assets/geometries/intro_particles.drc", "assets/geometries/intro_particles.drc"),
    ("assets/geometries/floor.drc", "assets/geometries/floor.drc"),
    ("assets/geometries/smoke_trail.drc", "assets/geometries/smoke_trail.drc"),
    ("assets/geometries/shattered_ring2.drc", "assets/geometries/shattered_ring2.drc"),
    ("assets/geometries/blurrytext_cylinder.drc", "assets/geometries/blurrytext_cylinder.drc"),
    ("assets/geometries/background_shapes.drc", "assets/geometries/cubes/background_shapes.drc"),
    ("assets/geometries/pudgy.drc", "assets/geometries/pudgy.drc"),
    ("assets/geometries/blurrytext.drc", "assets/geometries/blurrytext.drc"),
    ("assets/geometries/overpass_logo.drc", "assets/geometries/overpass_logo.drc"),
    ("assets/geometries/abstractlogo.drc", "assets/geometries/abstractlogo.drc"),
    ("assets/geometries/shattered_ring_smoke.drc", "assets/geometries/shattered_ring_smoke.drc"),
    ("assets/geometries/ceilingsmoke.drc", "assets/geometries/ceilingsmoke.drc"),
    ("assets/geometries/shattered_ring.drc", "assets/geometries/shattered_ring.drc"),
]

def download_file(url_path, local_path):
    """Faylni yuklab olish"""
    local_file = BASE_DIR / local_path
    local_file.parent.mkdir(parents=True, exist_ok=True)
    
    url = f"{BASE_URL}/{url_path}"
    
    if local_file.exists() and local_file.stat().st_size > 100:
        print(f"  ✅ {local_path} (mavjud)")
        return True
    
    try:
        print(f"  📥 {local_path}")
        result = subprocess.run(
            ["curl", "-s", "-L", "-H", "User-Agent: Mozilla/5.0", 
             "-H", "Referer: https://www.igloo.inc/", url, "-o", str(local_file)],
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0 and local_file.exists() and local_file.stat().st_size > 100:
            print(f"     ✅ Yuklandi")
            return True
        else:
            print(f"     ❌ Xato")
            return False
    except Exception as e:
        print(f"     ❌ Xato: {e}")
        return False

def main():
    print("🔧 Saytni to'liq sozlash...")
    print("")
    
    # 1. Kritik fayllarni yuklab olish
    print("📥 Step 1: Kritik fayllarni yuklab olish...")
    print("")
    for url_path, local_path in CRITICAL_FILES:
        download_file(url_path, local_path)
    
    # 2. Barcha fayllarni qo'shish
    print("")
    print("📝 Step 2: Barcha fayllarni git'ga qo'shish...")
    subprocess.run(["git", "add", "-f", "."], cwd=BASE_DIR, check=False)
    subprocess.run(["git", "add", "-f", "assets/"], cwd=BASE_DIR, check=False)
    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=False)
    
    # 3. Commit
    print("")
    print("💾 Step 3: Commit...")
    result = subprocess.run(
        ["git", "commit", "-m", "Complete fix - all assets and files"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ Committed")
    else:
        print("ℹ️  No changes or already committed")
    
    # 4. Push instructions
    print("")
    print("⬆️  Step 4: Push qilish...")
    print("")
    print("Terminalda quyidagi buyruqlarni bajaring:")
    print("")
    print("  git remote set-url origin 'https://brorasulov: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@github.com/brorasulov/brorasulov.git'")
    print("  git push origin main --force")
    print("  git remote set-url origin 'https://github.com/brorasulov/brorasulov.git'")
    print("")
    print("✅ Done!")
    print("")
    print("⏱️  Push'dan keyin 2-3 daqiqa kutib, saytni qayta yuklang:")
    print("🌐 https://brorasulov.github.io/brorasulov/")

if __name__ == "__main__":
    main()

