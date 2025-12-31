#!/bin/bash

echo "🔧 Starting server on free port..."
echo ""

# Kill any process on port 8000
PID=$(lsof -ti:8000)
if [ ! -z "$PID" ]; then
    echo "Stopping process on port 8000 (PID: $PID)..."
    kill -9 $PID 2>/dev/null
    sleep 1
fi

# Find free port
PORT=8000
while lsof -ti:$PORT > /dev/null 2>&1; do
    PORT=$((PORT + 1))
done

echo "✅ Starting server on port $PORT"
echo ""
echo "📍 Local access: http://localhost:$PORT"
echo "📍 Network access: http://172.20.10.4:$PORT"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd /Users/xoji/Documents/comment
python3 -m http.server $PORT --bind 0.0.0.0

