#!/bin/bash

cd /Users/xoji/Documents/comment

echo "📦 Manual push - ALL files to GitHub..."
echo ""

# 1. Barcha fayllarni qo'shish
echo "📝 Adding ALL files..."
git add -f .
git add -f assets/
git add -A

# 2. Commit
echo ""
echo "💾 Committing..."
git commit -m "Complete deployment - all assets" || echo "No changes"

# 3. Push instructions
echo ""
echo "⬆️  To push, run these commands:"
echo ""
echo "   git remote set-url origin 'https://brorasulov:YOUR_TOKEN@github.com/brorasulov/brorasulov.git'"
echo "   git push origin main --force"
echo "   git remote set-url origin 'https://github.com/brorasulov/brorasulov.git'"
echo ""
echo "   Replace YOUR_TOKEN with your actual GitHub token"
echo ""

