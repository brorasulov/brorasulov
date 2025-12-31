#!/usr/bin/env python3
"""
Barcha asset fayllarni tekshirish va yetishmayotganlarini yuklab olish
"""
import os
import subprocess
import re
from pathlib import Path

BASE_DIR = Path("/Users/xoji/Documents/comment")
BASE_URL = "https://www.igloo.inc"

def extract_asset_paths():
    """igloo_app3d.js dan barcha asset path'larni chiqarish"""
    app3d_file = BASE_DIR / "igloo_app3d.js"
    if not app3d_file.exists():
        print("❌ igloo_app3d.js topilmadi!")
        return []
    
    with open(app3d_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern'lar
    patterns = [
        r'["\']([^"\']+\.(?:drc|ktx2|json|wasm|js))["\']',
        r'load\(["\']([^"\']+)["\']',
        r'["\']assets/([^"\']+)["\']',
        r'["\']([^"\']+\.(?:png|jpg|exr|mp3|wav|ogg))["\']',
    ]
    
    assets = set()
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if match and not match.startswith('http'):
                assets.add(match)
    
    return sorted(assets)

def check_file_exists(asset_path):
    """Fayl mavjudligini tekshirish"""
    # Turli path variantlarini tekshirish
    possible_paths = [
        BASE_DIR / asset_path,
        BASE_DIR / "assets" / asset_path,
        BASE_DIR / "assets" / "images" / asset_path,
        BASE_DIR / "assets" / "geometries" / asset_path,
        BASE_DIR / "assets" / "fonts" / asset_path,
        BASE_DIR / "assets" / "libs" / asset_path,
    ]
    
    for path in possible_paths:
        if path.exists() and path.is_file():
            return True, path
    return False, None

def download_file(asset_path):
    """Faylni yuklab olish"""
    # To'g'ri path'ni aniqlash
    if asset_path.startswith('assets/'):
        asset_path = asset_path[7:]
    
    # Papka strukturasini aniqlash
    if asset_path.startswith('libs/'):
        local_path = BASE_DIR / "assets" / asset_path
    elif asset_path.startswith('fonts/'):
        local_path = BASE_DIR / "assets" / asset_path
    elif asset_path.startswith('geometries/'):
        local_path = BASE_DIR / "assets" / asset_path
    elif asset_path.startswith('images/'):
        local_path = BASE_DIR / "assets" / asset_path
    elif asset_path.startswith('audio/'):
        local_path = BASE_DIR / "assets" / asset_path
    elif asset_path.endswith('.drc'):
        # Geometry fayllar
        if '/' in asset_path:
            local_path = BASE_DIR / "assets" / "geometries" / asset_path
        else:
            local_path = BASE_DIR / "assets" / "geometries" / asset_path
    elif asset_path.endswith('.ktx2'):
        # Texture fayllar
        if '/' in asset_path:
            local_path = BASE_DIR / "assets" / "images" / asset_path
        else:
            local_path = BASE_DIR / "assets" / "images" / asset_path
    elif asset_path.endswith('.json'):
        # Font fayllar
        if '/' in asset_path:
            local_path = BASE_DIR / "assets" / "fonts" / asset_path
        else:
            local_path = BASE_DIR / "assets" / "fonts" / asset_path
    else:
        local_path = BASE_DIR / "assets" / asset_path
    
    # Papkani yaratish
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    # URL
    url = f"{BASE_URL}/assets/{asset_path}" if not asset_path.startswith('assets/') else f"{BASE_URL}/{asset_path}"
    
    # Yuklab olish
    try:
        print(f"  📥 Downloading: {asset_path}")
        result = subprocess.run(
            ["curl", "-s", "-L", "-H", "User-Agent: Mozilla/5.0", "-H", "Referer: https://www.igloo.inc/", 
             url, "-o", str(local_path)],
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0 and local_path.exists() and local_path.stat().st_size > 100:
            return True
        else:
            print(f"    ❌ Failed or too small")
            return False
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return False

def main():
    print("🔍 Barcha asset fayllarni tekshirish...")
    print("")
    
    assets = extract_asset_paths()
    print(f"📋 Topildi: {len(assets)} ta asset")
    print("")
    
    missing = []
    existing = []
    
    for asset in assets[:100]:  # Birinchi 100 tasini tekshirish
        exists, path = check_file_exists(asset)
        if exists:
            existing.append(asset)
            print(f"✅ {asset}")
        else:
            missing.append(asset)
            print(f"❌ {asset} - yetishmayapti")
            download_file(asset)
    
    print("")
    print(f"✅ Mavjud: {len(existing)}")
    print(f"❌ Yetishmayotgan: {len(missing)}")
    print("")
    print("📝 Barcha fayllarni qo'shish...")
    
    # Git'ga qo'shish
    subprocess.run(["git", "add", "-f", "assets/"], cwd=BASE_DIR)
    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
    
    print("✅ Done!")

if __name__ == "__main__":
    main()

