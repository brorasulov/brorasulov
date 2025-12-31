#!/bin/bash

cd /Users/xoji/Documents/comment

echo "🔗 Setting remote with token..."
echo "⚠️  Note: Use your GitHub token manually or set GITHUB_TOKEN env variable"
# git remote set-url origin "https://brorasulov:YOUR_TOKEN@github.com/brorasulov/brorasulov.git"

echo "⬆️  Pushing to GitHub..."
git push -u origin main

echo "🧹 Cleaning remote URL..."
git remote set-url origin "https://github.com/brorasulov/brorasulov.git"

echo ""
echo "✅ Done!"
echo ""
echo "📋 Next: Enable GitHub Pages at:"
echo "   https://github.com/brorasulov/brorasulov/settings/pages"
echo ""
echo "🌐 Site will be at:"
echo "   https://brorasulov.github.io/brorasulov/"

