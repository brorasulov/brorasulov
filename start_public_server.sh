#!/bin/bash

echo "🌐 Starting public server for igloo.inc..."
echo ""

# Get local IP address
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "192.168.1.100")

if [ -z "$LOCAL_IP" ] || [ "$LOCAL_IP" == "192.168.1.100" ]; then
    # Try alternative method
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
fi

echo "📍 Your local IP address: $LOCAL_IP"
echo ""
echo "🔗 Others can access the site at:"
echo "   http://$LOCAL_IP:8000"
echo ""
echo "📱 On the same WiFi network"
echo ""
echo "⚠️  Make sure your firewall allows connections on port 8000"
echo ""
echo "Starting server..."
echo "Press Ctrl+C to stop"
echo ""

cd /Users/xoji/Documents/comment
python3 -m http.server 8000 --bind 0.0.0.0

