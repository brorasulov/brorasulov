#!/bin/bash

cd /Users/xoji/Documents/comment

echo "📦 Push without tokens in scripts..."
echo ""

# 1. Barcha fayllarni qo'shish
echo "📝 Adding ALL files..."
git add -f .
git add -f assets/
git add -A

# 2. Commit
echo ""
echo "💾 Committing..."
git commit -m "Complete deployment - all assets (no tokens in code)" || echo "No changes"

# 3. Push instructions
echo ""
echo "⬆️  To push, use your token manually:"
echo ""
echo "   export GITHUB_TOKEN='your_token_here'"
echo "   git remote set-url origin \"https://brorasulov:\${GITHUB_TOKEN}@github.com/brorasulov/brorasulov.git\""
echo "   git push origin main --force"
echo "   git remote set-url origin 'https://github.com/brorasulov/brorasulov.git'"
echo ""
echo "   Or use GitHub CLI:"
echo "   gh auth login"
echo "   git push origin main --force"
echo ""

