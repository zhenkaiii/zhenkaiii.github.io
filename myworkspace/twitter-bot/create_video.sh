#!/bin/bash
# Simple video creation workflow

SCRIPT_DIR="scripts/$(date +%Y-%m-%d)"

if [ ! -d "$SCRIPT_DIR" ]; then
    echo "No script found for today. Run ./generate_daily_script.sh first"
    exit 1
fi

echo "📋 Creating video for: $SCRIPT_DIR"
echo ""

# Step 1: Extract keywords
echo "Step 1: Extracting image keywords..."
python3 video_creator.py

# Step 2: Instructions
echo ""
echo "============================================================"
echo "SIMPLE VIDEO WORKFLOW (10 minutes)"
echo "============================================================"
echo ""
echo "1. DOWNLOAD IMAGES (5 min):"
echo "   Open: $SCRIPT_DIR/7_image_keywords.txt"
echo "   For each keyword:"
echo "     - Search on pexels.com or unsplash.com"
echo "     - Download 1 image"
echo "     - Save to: $SCRIPT_DIR/images/"
echo "     - Name: 01_china.jpg, 02_aircraft.jpg, etc."
echo ""
echo "2. GENERATE VOICEOVER (2 min):"
echo "   - Go to: https://elevenlabs.io (free account)"
echo "   - Copy text from: $SCRIPT_DIR/5_voiceover_only.txt"
echo "   - Select Chinese voice"
echo "   - Generate and download"
echo "   - Save as: $SCRIPT_DIR/voiceover.mp3"
echo ""
echo "3. CREATE VIDEO (1 min):"
echo "   - Run: python3 video_creator.py --create-video"
echo ""
echo "4. UPLOAD:"
echo "   - Video: $SCRIPT_DIR/final_video.mp4"
echo "   - Twitter text: $SCRIPT_DIR/3_twitter_preview.txt"
echo ""
echo "============================================================"
echo ""
echo "OR use online tool (even simpler):"
echo "  1. Go to: https://www.kapwing.com/tools/slideshow-video-maker"
echo "  2. Upload images from: $SCRIPT_DIR/images/"
echo "  3. Upload voiceover: $SCRIPT_DIR/voiceover.mp3"
echo "  4. Set each image to 2.5 seconds"
echo "  5. Export video"
echo "============================================================"
