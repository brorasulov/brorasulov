#!/bin/bash

echo "🚀 Pushing to brorasulov repository..."
echo ""

cd /Users/xoji/Documents/comment

# Remote'ni to'g'ri sozlash
echo "🔗 Setting up remote..."
git remote remove origin 2>/dev/null
git remote add origin https://brorasulov@github.com/brorasulov/brorasulov.git

# Status tekshirish
echo "📊 Checking status..."
git status

# Add va commit
echo "📝 Adding and committing..."
git add .
git commit -m "Deploy igloo.inc website" 2>/dev/null || echo "Already committed"

# Branch
echo "🌿 Setting branch to main..."
git branch -M main

# Push
echo "⬆️  Pushing to GitHub..."
echo ""
echo "⚠️  You'll be asked for credentials:"
echo "   Username: brorasulov"
echo "   Password: Your GitHub password or Personal Access Token"
echo ""
git push -u origin main

echo ""
echo "✅ Done!"
echo ""
echo "📋 Next: Enable GitHub Pages at:"
echo "   https://github.com/brorasulov/brorasulov/settings/pages"
echo ""
echo "🌐 Site will be at:"
echo "   https://brorasulov.github.io/brorasulov/"

