#!/bin/bash

echo "🚀 Deploying to GitHub..."
echo "Repository: https://github.com/abdulazizproject/comment.git"
echo ""

cd /Users/xoji/Documents/comment

# Initialize git if not already
if [ ! -d ".git" ]; then
    echo "📦 Initializing git..."
    git init
fi

# Add remote
echo "🔗 Setting up remote..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/abdulazizproject/comment.git

# Add all files
echo "📝 Adding files..."
git add .

# Commit
echo "💾 Committing..."
git commit -m "Deploy igloo.inc website to GitHub Pages" || echo "No changes to commit"

# Push
echo "⬆️  Pushing to GitHub..."
git branch -M main
git push -u origin main --force

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "📋 Next steps:"
echo "1. Go to: https://github.com/abdulazizproject/comment"
echo "2. Click: Settings"
echo "3. Click: Pages (left menu)"
echo "4. Under 'Source':"
echo "   - Select: Deploy from a branch"
echo "   - Branch: main"
echo "   - Folder: / (root)"
echo "5. Click: Save"
echo ""
echo "🌐 Your site will be available at:"
echo "   https://abdulazizproject.github.io/comment/"
echo ""
echo "⏱️  Wait 1-2 minutes for deployment"

