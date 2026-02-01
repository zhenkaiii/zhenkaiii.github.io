#!/bin/bash
# Complete daily video creation workflow

cd /Users/kaizhen/myworkspace/twitter-bot

echo "🎬 DAILY VIDEO CREATION STARTING..."
echo ""

# Step 1: Generate script
echo "📝 Step 1: Generating script from news..."
python3 news_aggregator.py
echo ""

# Step 1.5: Generate voiceover script file
echo "📄 Step 1.5: Preparing voiceover script..."
python3 video_generator.py
echo ""

# Step 2: Download images and generate voiceover
echo "🖼️  Step 2: Downloading images and generating voiceover..."
python3 video_creator.py
echo ""

# Step 3: Create video
echo "🎥 Step 3: Creating final video..."
python3 video_creator.py --create-video
echo ""

# Summary
DATE=$(date +%Y-%m-%d)
echo "✅ COMPLETE!"
echo ""
echo "Your files are in: scripts/$DATE/"
echo ""
echo "📹 Video: scripts/$DATE/final_video.mp4"
echo "🐦 Twitter text: scripts/$DATE/3_twitter_preview.txt"
echo ""
echo "Next steps:"
echo "1. Upload video to YouTube"
echo "2. Post Twitter preview with YouTube link"
echo ""
