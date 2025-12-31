#!/bin/bash

cd /Users/xoji/Documents/comment

echo "🔧 Saytni to'liq sozlash va push qilish..."
echo ""

# 1. Barcha asset fayllarni tekshirish
echo "📋 Step 1: Asset fayllarni tekshirish..."
python3 verify_all_assets.py

# 2. Barcha fayllarni qo'shish
echo ""
echo "📝 Step 2: Barcha fayllarni qo'shish..."
git add -f .
git add -f assets/
git add -f assets/libs/
git add -f assets/fonts/
git add -f assets/geometries/
git add -f assets/images/
git add -f assets/audio/
git add -A

# 3. Status
echo ""
echo "📊 Step 3: Status..."
git status --short | head -20
echo "..."

# 4. Commit
echo ""
echo "💾 Step 4: Commit..."
git commit -m "Complete deployment - all assets fixed" || echo "No changes"

# 5. Push
echo ""
echo "⬆️  Step 5: Push qilish..."
echo ""
echo "Token bilan push qiling:"
echo ""
echo "  git remote set-url origin 'https://brorasulov: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@github.com/brorasulov/brorasulov.git'"
echo "  git push origin main --force"
echo "  git remote set-url origin 'https://github.com/brorasulov/brorasulov.git'"
echo ""

