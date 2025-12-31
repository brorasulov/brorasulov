#!/bin/bash

cd /Users/xoji/Documents/comment

echo "📦 Final push - ALL files to GitHub..."
echo ""

# 1. Barcha fayllarni qo'shish
echo "📝 Adding ALL files..."
git add -f .
git add -f assets/
git add -A

# 2. Commit
echo ""
echo "💾 Committing..."
git commit -m "Complete deployment - all assets (no tokens in scripts)" || echo "No changes"

# 3. Push (token bilan)
echo ""
echo "⬆️  Pushing to GitHub..."
git remote set-url origin 'https://brorasulov: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@github.com/brorasulov/brorasulov.git'
git push origin main --force
git remote set-url origin 'https://github.com/brorasulov/brorasulov.git'

echo ""
echo "✅ Done!"
echo ""
echo "⏱️  Wait 2-3 minutes for GitHub Pages to update"
echo "🌐 Then check: https://brorasulov.github.io/brorasulov/"

