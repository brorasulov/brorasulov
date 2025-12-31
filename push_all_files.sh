#!/bin/bash

echo "📦 Pushing all files to GitHub..."
echo ""

cd /Users/xoji/Documents/comment

# Barcha fayllarni qo'shish (hatto .gitignore'dagi ham)
echo "📝 Adding all files..."
git add -A

# Status
echo "📊 Files to commit:"
git status --short | head -20
echo ""

# Commit
echo "💾 Committing..."
git commit -m "Add all missing assets and files" || echo "No changes to commit"

# Push
echo "⬆️  Pushing to GitHub..."
echo "⚠️  Note: You may need to authenticate with your GitHub token"
git push origin main

echo ""
echo "✅ Done! All files pushed."
echo ""
echo "⏱️  Wait 1-2 minutes for GitHub Pages to update"
echo "🌐 Check: https://brorasulov.github.io/brorasulov/"

