#!/bin/bash

echo "📦 Force pushing ALL files to GitHub..."
echo ""

cd /Users/xoji/Documents/comment

# .gitignore'ni tekshirish
echo "📋 Checking .gitignore..."
if grep -q "assets\|\.ktx2\|\.drc" .gitignore 2>/dev/null; then
    echo "⚠️  .gitignore may be blocking files!"
fi

# Barcha fayllarni qo'shish (hatto ignore qilinganlar ham)
echo "📝 Adding ALL files (including ignored)..."
git add -f assets/
git add -f *.html
git add -f *.js
git add -A

# Status
echo ""
echo "📊 Files to commit:"
git status --short | wc -l
echo ""

# Commit
echo "💾 Committing..."
git commit -m "Add all missing assets - complete deployment" || echo "No changes to commit"

# Push
echo "⬆️  Pushing to GitHub..."
echo "⚠️  Note: You may need to authenticate with your GitHub token"
git push origin main --force

echo ""
echo "✅ Done! All files pushed."
echo ""
echo "⏱️  Wait 2-3 minutes for GitHub Pages to update"
echo "🌐 Check: https://brorasulov.github.io/brorasulov/"

