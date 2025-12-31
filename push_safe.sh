#!/bin/bash

echo "📦 Safe push - ALL files to GitHub..."
echo ""

cd /Users/xoji/Documents/comment

# Barcha fayllarni qo'shish
echo "📝 Adding ALL files..."
git add -f .
git add -f assets/
git add -A

# Commit
echo ""
echo "💾 Committing..."
git commit -m "Complete deployment - all assets" || echo "No changes to commit"

# Push (token bilan, lekin skriptda emas)
echo ""
echo "⬆️  Pushing to GitHub..."
echo ""
echo "⚠️  Using token from environment or credential helper"
echo ""

# Token'ni environment variable'dan olish yoki credential helper ishlatish
if [ -n "$GITHUB_TOKEN" ]; then
    git remote set-url origin "https://brorasulov:${GITHUB_TOKEN}@github.com/brorasulov/brorasulov.git"
    git push origin main --force
    git remote set-url origin "https://github.com/brorasulov/brorasulov.git"
else
    echo "❌ GITHUB_TOKEN environment variable not set"
    echo ""
    echo "Run this command:"
    echo "  export GITHUB_TOKEN='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'"
    echo "  ./push_safe.sh"
    echo ""
    echo "Or push manually:"
    echo "  git push origin main --force"
    exit 1
fi

echo ""
echo "✅ Done! All files pushed."
echo ""
echo "⏱️  Wait 2-3 minutes for GitHub Pages to update"
echo "🌐 Then check: https://brorasulov.github.io/brorasulov/"

