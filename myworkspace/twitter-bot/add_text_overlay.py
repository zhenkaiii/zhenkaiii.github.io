#!/usr/bin/env python3
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Create transparent PNG with @kfromkmedia text
img = Image.new('RGBA', (300, 50), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Use default font
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
except:
    font = ImageFont.load_default()

# Draw text
draw.text((10, 10), "@kfromkmedia", fill=(255, 255, 255, 255), font=font)

# Save
text_overlay = "/tmp/kfromkmedia_text.png"
img.save(text_overlay)

# Add text overlay to video
input_video = "/Users/kaizhen/myworkspace/twitter-bot/scripts/2026-02-01/video-en.mp4"
output_video = "/Users/kaizhen/myworkspace/twitter-bot/scripts/2026-02-01/video-en-final.mp4"

print("Adding @kfromkmedia text overlay...")
subprocess.run([
    "ffmpeg", "-i", input_video, "-i", text_overlay,
    "-filter_complex",
    "[1:v]scale=300:-1[text];"
    "[0:v][text]overlay=W-w-20:H-h-20:enable='between(t,7,429.54)'",
    "-c:a", "copy", "-c:v", "libx264", "-pix_fmt", "yuv420p",
    output_video, "-y"
], check=True)

print(f"✓ Final video with text: {output_video}")
