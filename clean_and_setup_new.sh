#!/bin/bash

echo "🧹 Cleaning old git setup..."
echo ""

cd /Users/xoji/Documents/comment

# Remove old git
echo "🗑️  Removing old git repository..."
rm -rf .git

# Remove CNAME (we'll create new one)
echo "🗑️  Removing old CNAME..."
rm -f CNAME

# Initialize fresh git
echo "📦 Initializing fresh git repository..."
git init

echo ""
echo "✅ Cleaned! Ready for new repository"
echo ""
echo "📋 Next steps:"
echo "1. Create new repository on GitHub:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: comment (or any name)"
echo "   - Make it Public"
echo "   - Don't initialize with README"
echo ""
echo "2. Then run these commands:"
echo "   git remote add origin https://github.com/brorasulov/REPO_NAME.git"
echo "   git add ."
echo "   git commit -m 'Deploy igloo.inc website'"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Enable GitHub Pages:"
echo "   - Settings > Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main, Folder: / (root)"
echo ""
echo "🌐 Your site will be at:"
echo "   https://brorasulov.github.io/REPO_NAME/"

