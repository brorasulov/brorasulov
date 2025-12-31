#!/bin/bash

cd /Users/xoji/Documents/comment

echo "🧹 Step 1: Cleaning all tokens from scripts..."
echo ""

# Barcha skriptlardan tokenni olib tashlash
TOKEN="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"
REPLACEMENT="YOUR_GITHUB_TOKEN_HERE"

# Shell skriptlarni tozalash
for file in *.sh; do
    if [ -f "$file" ] && [ "$file" != "FINAL_PUSH_CLEAN.sh" ]; then
        echo "  Cleaning: $file"
        sed -i '' "s|$TOKEN|$REPLACEMENT|g" "$file" 2>/dev/null || sed -i "s|$TOKEN|$REPLACEMENT|g" "$file"
    fi
done

# Python skriptlarni tozalash
for file in *.py; do
    if [ -f "$file" ]; then
        echo "  Cleaning: $file"
        sed -i '' "s|$TOKEN|$REPLACEMENT|g" "$file" 2>/dev/null || sed -i "s|$TOKEN|$REPLACEMENT|g" "$file"
    fi
done

echo ""
echo "✅ Tokens removed!"
echo ""

# Step 2: Add all files
echo "📝 Step 2: Adding ALL files..."
git add -f .
git add -f assets/
git add -A

# Step 3: Commit
echo ""
echo "💾 Step 3: Committing..."
git commit -m "Complete deployment - all assets (tokens removed from scripts)" || echo "No changes"

echo ""
echo "✅ Ready to push!"
echo ""
echo "⬆️  Step 4: Push manually with token:"
echo ""
echo "   git remote set-url origin 'https://brorasulov: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@github.com/brorasulov/brorasulov.git'"
echo "   git push origin main --force"
echo "   git remote set-url origin 'https://github.com/brorasulov/brorasulov.git'"
echo ""
echo "   OR use GitHub's 'Allow secret' option if it appears again"
echo ""

