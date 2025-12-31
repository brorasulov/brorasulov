#!/bin/bash

cd /Users/xoji/Documents/comment

echo "🧹 Cleaning git history from tokens..."
echo ""

# Avvalgi commit'larni o'chirish va yangi bitta commit yaratish
echo "📝 Creating fresh commit without tokens..."

# Barcha fayllarni saqlab qolish
echo "💾 Stashing all changes..."
git stash

# Main branch'ni remote'dan yangilash
echo "🔄 Resetting to remote..."
git fetch origin main
git reset --hard origin/main

# Stash'dan qaytarish
echo "📦 Restoring files..."
git stash pop

# Barcha fayllarni qo'shish
echo "📝 Adding all files..."
git add -f .
git add -f assets/
git add -A

# Yangi commit
echo "💾 Creating new commit..."
git commit -m "Complete deployment - all assets (clean)"

echo ""
echo "✅ Git history cleaned!"
echo ""
echo "⬆️  Now push manually:"
echo "   git remote set-url origin 'https://brorasulov:YOUR_TOKEN@github.com/brorasulov/brorasulov.git'"
echo "   git push origin main --force"
echo "   git remote set-url origin 'https://github.com/brorasulov/brorasulov.git'"
echo ""

