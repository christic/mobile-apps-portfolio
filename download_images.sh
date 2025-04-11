#!/bin/bash

# Create images directory if it doesn't exist
mkdir -p images

# Download app screenshots
curl -o images/tap-tell-fun.png "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/8a/8b/8a/8a8b8a8a-8a8b-8a8b-8a8b-8a8b8a8b8a8b/AppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/1200x630wa.png"
curl -o images/phase-10-score.png "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/8a/8b/8a/8a8b8a8a-8a8b-8a8b-8a8b-8a8b8a8b8a8b/AppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/1200x630wa.png"
curl -o images/sky-jo-score.png "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/8a/8b/8a/8a8b8a8a-8a8b-8a8b-8a8b-8a8b8a8b8a8b/AppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/1200x630wa.png"
curl -o images/500-rummy-score.png "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/8a/8b/8a/8a8b8a8a-8a8b-8a8b-8a8b-8a8b8a8b8a8b/AppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/1200x630wa.png"
curl -o images/zing-txt.png "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/8a/8b/8a/8a8b8a8a-8a8b-8a8b-8a8b-8a8b8a8b8a8b/AppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/1200x630wa.png"

echo "Images downloaded successfully!" 