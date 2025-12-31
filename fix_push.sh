#!/bin/bash

echo "🔄 Syncing with GitHub..."
echo ""

cd /Users/xoji/Documents/comment

# Pull remote changes
echo "📥 Pulling remote changes..."
git pull origin main --allow-unrelated-histories

# If there are conflicts, we'll handle them
if [ $? -ne 0 ]; then
    echo "⚠️  There might be conflicts. Resolving..."
    git add .
    git commit -m "Merge remote changes"
fi

# Push
echo "⬆️  Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Done!"

