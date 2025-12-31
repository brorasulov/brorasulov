#!/bin/bash

echo "🌐 Setting up public access to your website..."
echo ""

# Check if ngrok is installed
if command -v ngrok &> /dev/null; then
    echo "✅ ngrok is installed"
    echo ""
    echo "Starting ngrok tunnel..."
    echo "This will create a public URL like: https://xxxxx.ngrok.io"
    echo ""
    echo "Press Ctrl+C to stop"
    echo ""
    ngrok http 8000
else
    echo "❌ ngrok is not installed"
    echo ""
    echo "Installing ngrok..."
    echo ""
    
    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        echo "Installing ngrok via Homebrew..."
        brew install ngrok/ngrok/ngrok
        echo ""
        echo "✅ ngrok installed!"
        echo ""
        echo "Now run this script again to start the tunnel"
    else
        echo "⚠️  Homebrew is not installed"
        echo ""
        echo "Please install ngrok manually:"
        echo "1. Visit: https://ngrok.com/download"
        echo "2. Download for macOS"
        echo "3. Extract and move to /usr/local/bin/"
        echo ""
        echo "Or install Homebrew first:"
        echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        echo ""
        echo "Then install ngrok:"
        echo "brew install ngrok/ngrok/ngrok"
    fi
fi

