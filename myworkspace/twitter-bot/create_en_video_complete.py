#!/usr/bin/env python3
"""
Create English video with:
- 7s thumb at start and end
- Talking head at bottom right during main section
- @kfromkmedia text below talking head
- Voiceover sped up 15% and pitched down 2 semitones
"""
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont

# Paths
thumb = "/Users/kaizhen/myworkspace/twitter-bot/avartar/thumb-en.png"
talking_head = "/Users/kaizhen/myworkspace/twitter-bot/avartar/image4-removed.png"
voiceover = "/Users/kaizhen/myworkspace/twitter-bot/scripts/2026-02-01/voiceover-en.m4a"
output_dir = "/Users/kaizhen/myworkspace/twitter-bot/scripts/2026-02-01"
final_output = f"{output_dir}/video-en-final.mp4"

print("=" * 60)
print("CREATING ENGLISH VIDEO")
print("=" * 60)

# Step 1: Adjust voiceover
adjusted_vo = f"{output_dir}/voiceover-en-final.m4a"
print("\n[1/6] Adjusting voiceover (speed +15%, pitch -2)...")
subprocess.run([
    "ffmpeg", "-i", voiceover,
    "-filter:a", "atempo=1.15,asetrate=44100*0.887",
    adjusted_vo, "-y"
], check=True, capture_output=True)

result = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", adjusted_vo],
    capture_output=True, text=True, check=True
)
vo_duration = float(result.stdout.strip())
main_duration = vo_duration - 14
print(f"      Duration: {vo_duration:.1f}s (7s intro + {main_duration:.1f}s main + 7s outro)")

# Step 2: Create text overlay
print("\n[2/6] Creating @kfromkmedia text overlay...")
text_overlay = "/tmp/kfromkmedia_text.png"
img = Image.new('RGBA', (300, 50), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
except:
    font = ImageFont.load_default()
draw.text((10, 10), "@kfromkmedia", fill=(255, 255, 255, 255), font=font)
img.save(text_overlay)
print("      ✓ Text overlay created")

# Step 3: Create start segment
start_seg = f"{output_dir}/seg_start.mp4"
print("\n[3/6] Creating intro (7s thumb)...")
subprocess.run([
    "ffmpeg", "-loop", "1", "-t", "7", "-i", thumb,
    "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    start_seg, "-y"
], check=True, capture_output=True)
print("      ✓ Intro created")

# Step 4: Create middle segment
middle_seg = f"{output_dir}/seg_middle.mp4"
print(f"\n[4/6] Creating main section ({main_duration:.1f}s with talking head + text)...")
subprocess.run([
    "ffmpeg",
    "-loop", "1", "-t", str(main_duration), "-i", thumb,
    "-loop", "1", "-t", str(main_duration), "-i", talking_head,
    "-loop", "1", "-t", str(main_duration), "-i", text_overlay,
    "-filter_complex",
    "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[bg];"
    "[1:v]scale=300:-1[head];"
    "[2:v]scale=300:-1[text];"
    "[bg][head]overlay=W-w-20:H-h-70[tmp];"
    "[tmp][text]overlay=W-w-20:H-h-20",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    middle_seg, "-y"
], check=True, capture_output=True)
print("      ✓ Main section created")

# Step 5: Create end segment
end_seg = f"{output_dir}/seg_end.mp4"
print("\n[5/6] Creating outro (7s thumb)...")
subprocess.run([
    "ffmpeg", "-loop", "1", "-t", "7", "-i", thumb,
    "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    end_seg, "-y"
], check=True, capture_output=True)
print("      ✓ Outro created")

# Step 6: Concatenate and add audio
print("\n[6/6] Combining segments and adding audio...")
concat_list = f"{output_dir}/concat_list.txt"
with open(concat_list, 'w') as f:
    f.write(f"file '{start_seg}'\n")
    f.write(f"file '{middle_seg}'\n")
    f.write(f"file '{end_seg}'\n")

subprocess.run([
    "ffmpeg",
    "-f", "concat", "-safe", "0", "-i", concat_list,
    "-i", adjusted_vo,
    "-c:v", "copy", "-c:a", "aac", "-shortest",
    final_output, "-y"
], check=True, capture_output=True)

# Cleanup
os.remove(start_seg)
os.remove(middle_seg)
os.remove(end_seg)
os.remove(concat_list)

file_size = os.path.getsize(final_output) / (1024 * 1024)
print(f"      ✓ Final video assembled")

print("\n" + "=" * 60)
print(f"✓ VIDEO CREATED: {final_output}")
print(f"  Size: {file_size:.1f} MB")
print(f"  Duration: {vo_duration:.1f}s")
print("=" * 60)
