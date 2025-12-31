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

# 3. Push (token bilan - manual)
echo ""
echo "⬆️  Pushing to GitHub..."
echo "⚠️  Note: You need to authenticate manually"
echo ""
echo "Run this command:"
echo "  git remote set-url origin 'https://brorasulov:YOUR_TOKEN@github.com/brorasulov/brorasulov.git'"
echo "  git push origin main --force"
echo "  git remote set-url origin 'https://github.com/brorasulov/brorasulov.git'"

echo ""
echo "✅ Done!"
echo ""
echo "⏱️  Wait 2-3 minutes for GitHub Pages to update"
echo "🌐 Then check: https://brorasulov.github.io/brorasulov/"

