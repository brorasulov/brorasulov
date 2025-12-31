#!/bin/bash

cd /Users/xoji/Documents/comment

echo "🔗 Setting remote with token..."
git remote set-url origin "https://brorasulov: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@github.com/brorasulov/brorasulov.git"

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

