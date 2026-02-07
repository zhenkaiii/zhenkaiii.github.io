#!/usr/bin/env python3
import subprocess
import os
import glob

# Paths
thumb = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/avartar/thumb-en.png"
talking_head_img = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/avartar/image4-removed.png"
voiceover = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/scripts/2026-02-01/voiceover-en.m4a"
images_dir = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/images_asset"
output_dir = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/scripts/2026-02-01"
final_output = f"{output_dir}/video-en-final.mp4"

print("=" * 60)
print("CREATING ENGLISH VIDEO WITH WAV2LIP")
print("=" * 60)

# Step 1: Adjust voiceover
adjusted_vo = f"{output_dir}/voiceover-en-final.m4a"
print("\n[1/7] Adjusting voiceover (speed +15%, pitch -2)...")
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
print(f"      Duration: {vo_duration:.1f}s")

# Step 2: Create talking head with Wav2Lip
talking_head_video = f"{output_dir}/talking_head.mp4"
print("\n[2/7] Creating lip-synced talking head with Wav2Lip...")
wav2lip_dir = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/Wav2Lip"
subprocess.run([
    "python3", "inference.py",
    "--checkpoint_path", "checkpoints/wav2lip_gan.pth",
    "--face", talking_head_img,
    "--audio", adjusted_vo,
    "--outfile", talking_head_video,
    "--static", "True",
    "--fps", "30"
], cwd=wav2lip_dir, check=True)
print("      ✓ Talking head created")

# Step 3: Add @kfromkmedia text to talking head
print("\n[3/7] Adding @kfromkmedia text to talking head...")
from PIL import Image, ImageDraw, ImageFont
import cv2

# Create text overlay PNG
text_overlay = "/tmp/kfromkmedia_text.png"
img = Image.new('RGBA', (300, 50), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
except:
    font = ImageFont.load_default()
draw.text((10, 10), "@kfromkmedia", fill=(255, 255, 255, 255), font=font)
img.save(text_overlay)

# Overlay text on talking head and resize to 300px
talking_head_final = f"{output_dir}/talking_head_final.mp4"
subprocess.run([
    "ffmpeg", "-i", talking_head_video, "-i", text_overlay,
    "-filter_complex",
    "[0:v]scale=300:-1[head];"
    "[1:v]scale=300:-1[text];"
    "[head][text]overlay=0:H-h",
    "-c:v", "libx264", "-c:a", "copy",
    talking_head_final, "-y"
], check=True, capture_output=True)
print("      ✓ Text added and resized")

# Step 4: Create intro (7s thumb)
start_seg = f"{output_dir}/seg_start.mp4"
print("\n[4/7] Creating intro (7s)...")
subprocess.run([
    "ffmpeg", "-loop", "1", "-t", "7", "-i", thumb,
    "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    start_seg, "-y"
], check=True, capture_output=True)
print("      ✓ Intro created")

# Step 5: Create main section with images slideshow + talking head overlay
print(f"\n[5/7] Creating main section ({main_duration:.1f}s)...")
images = sorted(glob.glob(f"{images_dir}/*.jpg"))
duration_per_image = main_duration / len(images)

# Create slideshow
slideshow = f"{output_dir}/slideshow.mp4"
list_file = f"{output_dir}/images_list.txt"
with open(list_file, 'w') as f:
    for img in images[:-1]:
        f.write(f"file '{os.path.abspath(img)}'\n")
        f.write(f"duration {duration_per_image}\n")
    f.write(f"file '{os.path.abspath(images[-1])}'\n")

subprocess.run([
    "ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file,
    "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-t", str(main_duration),
    slideshow, "-y"
], check=True, capture_output=True)

# Overlay talking head (already has lip sync and text)
middle_seg = f"{output_dir}/seg_middle.mp4"
subprocess.run([
    "ffmpeg", "-i", slideshow, "-i", talking_head_final,
    "-filter_complex", "[0:v][1:v]overlay=W-w-20:H-h-20",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-t", str(main_duration),
    middle_seg, "-y"
], check=True, capture_output=True)
os.remove(slideshow)
os.remove(list_file)
print("      ✓ Main section created")

# Step 6: Create outro (7s thumb)
end_seg = f"{output_dir}/seg_end.mp4"
print("\n[6/7] Creating outro (7s)...")
subprocess.run([
    "ffmpeg", "-loop", "1", "-t", "7", "-i", thumb,
    "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    end_seg, "-y"
], check=True, capture_output=True)
print("      ✓ Outro created")

# Step 7: Concatenate all segments
print("\n[7/7] Combining segments and adding audio...")
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
