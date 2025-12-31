#!/bin/bash

echo "🌐 Starting public tunnel for igloo.inc..."
echo ""

# Method 1: Try ngrok
if command -v ngrok &> /dev/null; then
    echo "✅ Using ngrok..."
    echo ""
    echo "Starting ngrok tunnel on port 8000..."
    echo "You'll get a public URL like: https://xxxxx.ngrok-free.app"
    echo ""
    echo "⚠️  Make sure your local server is running first!"
    echo "   Run: python3 -m http.server 8000 --bind 0.0.0.0"
    echo ""
    echo "Press Ctrl+C to stop ngrok"
    echo ""
    ngrok http 8000
    exit 0
fi

# Method 2: Try localtunnel (npm)
if command -v lt &> /dev/null; then
    echo "✅ Using localtunnel..."
    echo ""
    echo "Starting localtunnel on port 8000..."
    echo ""
    lt --port 8000
    exit 0
fi

# Method 3: Try cloudflared
if command -v cloudflared &> /dev/null; then
    echo "✅ Using Cloudflare Tunnel..."
    echo ""
    echo "Starting Cloudflare tunnel on port 8000..."
    echo ""
    cloudflared tunnel --url http://localhost:8000
    exit 0
fi

# If nothing is installed
echo "❌ No tunnel tool found"
echo ""
echo "Please install one of these:"
echo ""
echo "1. ngrok (Recommended - easiest):"
echo "   brew install ngrok/ngrok/ngrok"
echo ""
echo "2. localtunnel (via npm):"
echo "   npm install -g localtunnel"
echo ""
echo "3. Cloudflare Tunnel:"
echo "   brew install cloudflared"
echo ""
echo "After installing, run this script again"

