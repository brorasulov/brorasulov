#!/bin/bash

echo "🔍 Checking all files..."
echo ""

cd /Users/xoji/Documents/comment

# Count files
TOTAL_FILES=$(find assets -type f 2>/dev/null | wc -l | tr -d ' ')
TRACKED_FILES=$(git ls-files 2>/dev/null | wc -l | tr -d ' ')

echo "📊 Files found:"
echo "   Total files in assets/: $TOTAL_FILES"
echo "   Files tracked by git: $TRACKED_FILES"
echo ""

if [ "$TOTAL_FILES" -gt "$TRACKED_FILES" ]; then
    echo "⚠️  Some files are not tracked!"
    echo ""
    echo "📝 Adding all files..."
    git add -A
    
    echo "💾 Committing..."
    git commit -m "Add all missing assets" || echo "No changes to commit"
    
    echo "⬆️  Pushing to GitHub..."
    git remote set-url origin "https://brorasulov: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@github.com/brorasulov/brorasulov.git"
    git push origin main
    git remote set-url origin "https://github.com/brorasulov/brorasulov.git"
    
    echo ""
    echo "✅ Done! All files pushed."
else
    echo "✅ All files are tracked!"
fi

echo ""
echo "🌐 Check your site: https://brorasulov.github.io/brorasulov/"

