#!/bin/bash

cd /Users/xoji/Documents/comment

# Remove HTML files
rm -f assets/images/cubes/bg.png assets/images/cubes/advect.png assets/images/cubes_env.exr

# Download with proper headers
echo "Downloading bg.png..."
curl -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
     -H "Referer: https://www.igloo.inc/" \
     -H "Accept: image/png,image/*,*/*;q=0.8" \
     -L "https://www.igloo.inc/assets/images/cubes/bg.png" \
     -o "assets/images/cubes/bg.png"

echo "Downloading advect.png..."
curl -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
     -H "Referer: https://www.igloo.inc/" \
     -H "Accept: image/png,image/*,*/*;q=0.8" \
     -L "https://www.igloo.inc/assets/images/cubes/advect.png" \
     -o "assets/images/cubes/advect.png"

echo "Downloading cubes_env.exr..."
curl -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
     -H "Referer: https://www.igloo.inc/" \
     -H "Accept: */*" \
     -L "https://www.igloo.inc/assets/images/cubes_env.exr" \
     -o "assets/images/cubes_env.exr"

# Verify
echo ""
echo "Verifying files..."
file assets/images/cubes/bg.png assets/images/cubes/advect.png assets/images/cubes_env.exr

