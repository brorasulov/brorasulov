#!/bin/bash
cd /Users/xoji/Documents/comment
mkdir -p assets/images/cubes

echo "Downloading cube files..."

# Download bg.png
curl -s -f -L "https://www.igloo.inc/assets/images/cubes/bg.png" -o "assets/images/cubes/bg.png" && echo "✓ bg.png" || echo "✗ bg.png"

# Download advect.png  
curl -s -f -L "https://www.igloo.inc/assets/images/cubes/advect.png" -o "assets/images/cubes/advect.png" && echo "✓ advect.png" || echo "✗ advect.png"

# Download cubes_env.exr
curl -s -f -L "https://www.igloo.inc/assets/images/cubes_env.exr" -o "assets/images/cubes_env.exr" && echo "✓ cubes_env.exr" || echo "✗ cubes_env.exr"

echo ""
echo "Checking file sizes..."
ls -lh assets/images/cubes/bg.png assets/images/cubes/advect.png assets/images/cubes_env.exr 2>/dev/null

echo "Done!"

