#!/bin/bash

echo "🔧 Fixing port 8000 and setting up tunnel..."
echo ""

# Step 1: Kill process on port 8000
echo "1️⃣ Checking port 8000..."
PID=$(lsof -ti:8000)

if [ ! -z "$PID" ]; then
    echo "   Found process on port 8000 (PID: $PID)"
    echo "   Killing process..."
    kill -9 $PID 2>/dev/null
    sleep 1
    echo "   ✅ Port 8000 is now free"
else
    echo "   ✅ Port 8000 is free"
fi

echo ""

# Step 2: Try localtunnel (no auth needed)
if command -v lt &> /dev/null; then
    echo "2️⃣ Starting localtunnel (no auth needed)..."
    echo ""
    echo "   Starting server..."
    cd /Users/xoji/Documents/comment
    python3 -m http.server 8000 --bind 0.0.0.0 &
    SERVER_PID=$!
    sleep 2
    
    echo "   Starting tunnel..."
    echo "   You'll get a public URL in a moment..."
    echo ""
    lt --port 8000
    kill $SERVER_PID 2>/dev/null
    exit 0
fi

# Step 3: Try cloudflared (no auth needed)
if command -v cloudflared &> /dev/null; then
    echo "2️⃣ Starting Cloudflare Tunnel (no auth needed)..."
    echo ""
    echo "   Starting server..."
    cd /Users/xoji/Documents/comment
    python3 -m http.server 8000 --bind 0.0.0.0 &
    SERVER_PID=$!
    sleep 2
    
    echo "   Starting tunnel..."
    cloudflared tunnel --url http://localhost:8000
    kill $SERVER_PID 2>/dev/null
    exit 0
fi

# Step 4: Install localtunnel
echo "2️⃣ Installing localtunnel (no auth needed)..."
echo ""

if command -v npm &> /dev/null; then
    echo "   Installing localtunnel..."
    npm install -g localtunnel
    echo ""
    echo "   ✅ Installed! Now run this script again"
else
    echo "   ❌ npm is not installed"
    echo ""
    echo "   Please install Node.js first:"
    echo "   brew install node"
fi

