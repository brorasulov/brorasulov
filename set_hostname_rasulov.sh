#!/bin/bash

echo "Setting hostname to 'rasulov'..."

# Set ComputerName
sudo scutil --set ComputerName rasulov

# Set LocalHostName (used for Bonjour)
sudo scutil --set LocalHostName rasulov

# Set HostName
sudo scutil --set HostName rasulov

echo ""
echo "✅ Hostname changed to 'rasulov'"
echo ""
echo "Verifying changes:"
echo "ComputerName: $(scutil --get ComputerName)"
echo "LocalHostName: $(scutil --get LocalHostName)"
echo "HostName: $(scutil --get HostName)"
echo ""
echo "Now you can access the site at:"
echo "  - http://rasulov:8000"
echo "  - http://rasulov.local:8000"
echo ""
echo "Note: You may need to restart your computer for changes to take full effect."

