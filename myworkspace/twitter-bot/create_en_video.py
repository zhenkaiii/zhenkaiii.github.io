#!/usr/bin/env python3
import subprocess
import os

# Paths
thumb = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/avartar/thumb-en.png"
talking_head = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/avartar/image4-removed.png"
voiceover = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/scripts/2026-02-01/voiceover-en.m4a"
output_dir = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/scripts/2026-02-01"
output = f"{output_dir}/video-en.mp4"

# Step 1: Adjust voiceover (speed up 15%, pitch down 2 semitones)
adjusted_vo = f"{output_dir}/voiceover-en-final.m4a"
print("Step 1: Adjusting voiceover...")
subprocess.run([
    "ffmpeg", "-i", voiceover,
    "-filter:a", "atempo=1.15,asetrate=44100*0.887",
    adjusted_vo, "-y"
], check=True)

# Get voiceover duration
result = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", adjusted_vo],
    capture_output=True, text=True, check=True
)
vo_duration = float(result.stdout.strip())
main_duration = vo_duration - 14  # 7s start + 7s end

print(f"  Voiceover: {vo_duration:.2f}s, Main: {main_duration:.2f}s")

# Step 2: Create start segment (7s thumb)
start_seg = f"{output_dir}/seg_start.mp4"
print("\nStep 2: Creating start segment (7s)...")
subprocess.run([
    "ffmpeg", "-loop", "1", "-t", "7", "-i", thumb,
    "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    start_seg, "-y"
], check=True)

# Step 3: Create middle segment (thumb + talking head overlay)
middle_seg = f"{output_dir}/seg_middle.mp4"
print(f"\nStep 3: Creating middle segment ({main_duration:.2f}s)...")
subprocess.run([
    "ffmpeg",
    "-loop", "1", "-t", str(main_duration), "-i", thumb,
    "-loop", "1", "-t", str(main_duration), "-i", talking_head,
    "-filter_complex",
    "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[bg];"
    "[1:v]scale=300:-1[head];"
    "[bg][head]overlay=W-w-20:H-h-20",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    middle_seg, "-y"
], check=True)

# Step 4: Create end segment (7s thumb)
end_seg = f"{output_dir}/seg_end.mp4"
print("\nStep 4: Creating end segment (7s)...")
subprocess.run([
    "ffmpeg", "-loop", "1", "-t", "7", "-i", thumb,
    "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    end_seg, "-y"
], check=True)

# Step 5: Concatenate segments and add audio
print("\nStep 5: Concatenating segments and adding audio...")
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
    output, "-y"
], check=True)

# Cleanup
os.remove(start_seg)
os.remove(middle_seg)
os.remove(end_seg)
os.remove(concat_list)

print(f"\n✓ Video created: {output}")
print("\nNote: Add '@kfromkmedia' text below talking head in video editor")
