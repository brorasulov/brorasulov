#!/bin/bash

cd /Users/xoji/Documents/comment

echo "🧹 Removing all tokens from scripts..."
echo ""

# Barcha skriptlardan tokenni olib tashlash
TOKEN="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"
REPLACEMENT="YOUR_GITHUB_TOKEN_HERE"

# Shell skriptlarni tozalash
for file in *.sh; do
    if [ -f "$file" ]; then
        echo "Cleaning: $file"
        sed -i '' "s|$TOKEN|$REPLACEMENT|g" "$file" 2>/dev/null || sed -i "s|$TOKEN|$REPLACEMENT|g" "$file"
    fi
done

# Python skriptlarni tozalash
for file in *.py; do
    if [ -f "$file" ]; then
        echo "Cleaning: $file"
        sed -i '' "s|$TOKEN|$REPLACEMENT|g" "$file" 2>/dev/null || sed -i "s|$TOKEN|$REPLACEMENT|g" "$file"
    fi
done

echo ""
echo "✅ All tokens removed from scripts!"
echo ""
echo "📝 Now commit and push:"
echo "   git add -A"
echo "   git commit -m 'Remove tokens from scripts'"
echo "   git push origin main --force"
echo ""

