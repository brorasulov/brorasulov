#!/bin/bash

echo "🚀 Deploying to GitHub Pages..."
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo ""
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo "⚠️  No GitHub repository found!"
    echo ""
    echo "Please create a GitHub repository first:"
    echo "1. Go to: https://github.com/new"
    echo "2. Create a new repository (name: comment or igloo-site)"
    echo "3. Don't initialize with README"
    echo "4. Copy the repository URL"
    echo ""
    read -p "Enter your GitHub repository URL (or press Enter to skip): " REPO_URL
    
    if [ ! -z "$REPO_URL" ]; then
        git remote add origin "$REPO_URL"
        echo "✅ Remote added: $REPO_URL"
    else
        echo "⚠️  Skipping remote setup. You can add it later with:"
        echo "   git remote add origin YOUR_REPO_URL"
        exit 1
    fi
    echo ""
fi

# Add all files
echo "📝 Adding files..."
git add .

# Commit
echo "💾 Committing changes..."
git commit -m "Deploy igloo.inc website to GitHub Pages" || echo "No changes to commit"

# Push to main branch
echo "⬆️  Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Pushed to GitHub!"
echo ""
echo "📋 Next steps:"
echo "1. Go to your GitHub repository"
echo "2. Settings > Pages"
echo "3. Source: Deploy from a branch"
echo "4. Branch: main, folder: / (root)"
echo "5. Save"
echo ""
echo "🌐 Your site will be available at:"
echo "   https://YOUR_USERNAME.github.io/REPO_NAME/"
echo ""
echo "⏱️  It may take 1-2 minutes to deploy"

