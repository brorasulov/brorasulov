#!/bin/bash

echo "🔍 Checking git status..."
echo ""

cd /Users/xoji/Documents/comment

# Git status
echo "📊 Git status:"
git status
echo ""

# Branch'lar
echo "🌿 Branches:"
git branch -a
echo ""

# Remote
echo "🔗 Remote:"
git remote -v
echo ""

# Agar commit yo'q bo'lsa
if [ -z "$(git log --oneline -1 2>/dev/null)" ]; then
    echo "⚠️  No commits found. Creating commit..."
    git add .
    git commit -m "Deploy igloo.inc website"
    echo "✅ Committed!"
    echo ""
fi

# Branch'ni tekshirish
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "none")

if [ "$CURRENT_BRANCH" == "none" ] || [ -z "$CURRENT_BRANCH" ]; then
    echo "⚠️  No branch found. Creating main branch..."
    git checkout -b main 2>/dev/null || git branch -M main
    echo "✅ Branch created!"
    echo ""
fi

# Push qilish
echo "⬆️  Pushing to GitHub..."
echo "⚠️  You'll need to enter credentials:"
echo "   Username: brorasulov"
echo "   Password: Your GitHub password or token"
echo ""
git push -u origin main

echo ""
echo "✅ Done! Now check GitHub Pages settings."

