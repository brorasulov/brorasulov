#!/bin/bash

echo "🔑 GitHub Personal Access Token kerak!"
echo ""
echo "Token yaratish:"
echo "1. https://github.com/settings/tokens ga kiring"
echo "2. 'Generate new token (classic)' ni bosing"
echo "3. 'repo' permission'ni belgilang"
echo "4. Token'ni nusxalab oling"
echo ""
read -p "Token'ni kiriting: " TOKEN

if [ -z "$TOKEN" ]; then
    echo "❌ Token kiritilmadi!"
    exit 1
fi

cd /Users/xoji/Documents/comment

# Remote'ni token bilan sozlash
git remote set-url origin https://brorasulov:$TOKEN@github.com/brorasulov/brorasulov.git

# Push qilish
echo ""
echo "⬆️  Pushing to GitHub..."
git push -u origin main

# Remote'ni tozalash (xavfsizlik uchun)
git remote set-url origin https://github.com/brorasulov/brorasulov.git

echo ""
echo "✅ Done!"
echo ""
echo "📋 Next: Enable GitHub Pages at:"
echo "   https://github.com/brorasulov/brorasulov/settings/pages"

