#!/bin/bash

cd /Users/xoji/Documents/comment

echo "📦 Clean push - ALL files to GitHub..."
echo ""

# 1. Barcha fayllarni qo'shish
echo "📝 Adding ALL files..."
git add -f .
git add -f assets/
git add -A

# 2. Commit
echo ""
echo "💾 Committing..."
git commit -m "Complete deployment - all assets (clean, no tokens)" || echo "No changes"

# 3. Push (token bilan - manual)
echo ""
echo "⬆️  Pushing to GitHub..."
echo ""
echo "Run these commands manually:"
echo ""
echo "  git remote set-url origin 'https://brorasulov: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@github.com/brorasulov/brorasulov.git'"
echo "  git push origin main --force"
echo "  git remote set-url origin 'https://github.com/brorasulov/brorasulov.git'"
echo ""

