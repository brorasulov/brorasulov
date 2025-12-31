#!/bin/bash

echo "📦 Final push - ALL files to GitHub..."
echo ""

cd /Users/xoji/Documents/comment

# Barcha fayllarni qo'shish (hatto ignore qilinganlar ham)
echo "📝 Adding ALL files (force add)..."
git add -f .
git add -f assets/
git add -f assets/libs/
git add -f assets/fonts/
git add -f assets/geometries/
git add -f assets/images/
git add -f assets/audio/
git add -A

# Status
echo ""
echo "📊 Files to commit:"
git status --short | head -30
echo "..."

# Commit
echo ""
echo "💾 Committing..."
git commit -m "Complete deployment - all assets" || echo "No changes to commit"

# Push
echo ""
echo "⬆️  Pushing to GitHub (force)..."
git remote set-url origin "https://brorasulov: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@github.com/brorasulov/brorasulov.git"
git push origin main --force
git remote set-url origin "https://github.com/brorasulov/brorasulov.git"

echo ""
echo "✅ Done! All files pushed."
echo ""
echo "⏱️  Wait 2-3 minutes for GitHub Pages to update"
echo "🌐 Then check: https://brorasulov.github.io/brorasulov/"

