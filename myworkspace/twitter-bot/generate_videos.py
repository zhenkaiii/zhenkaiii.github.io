#!/usr/bin/env python3
"""
Automated video generation script for Twitter bot
Usage: python3 generate_videos.py YYYY-MM-DD
"""

import sys
import os
import subprocess

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 generate_videos.py YYYY-MM-DD")
        sys.exit(1)
    
    date = sys.argv[1]
    base_dir = "/Users/kaizhen/myworkspace/twitter-bot"
    scripts_dir = f"{base_dir}/scripts/{date}"
    
    # Check prerequisites
    if not os.path.exists(f"{scripts_dir}/voiceover-en.m4a"):
        print(f"Error: {scripts_dir}/voiceover-en.m4a not found")
        sys.exit(1)
    if not os.path.exists(f"{scripts_dir}/voiceover-cn.m4a"):
        print(f"Error: {scripts_dir}/voiceover-cn.m4a not found")
        sys.exit(1)
    
    os.chdir(scripts_dir)
    
    # Step 1: Adjust voiceovers
    print("Step 1: Adjusting voiceovers...")
    subprocess.run([
        "ffmpeg", "-i", "voiceover-en.m4a",
        "-filter:a", "atempo=1.20,asetrate=44100*0.887,atempo=1.127",
        "voiceover-en-adjusted.m4a", "-y"
    ], check=True)
    
    subprocess.run([
        "ffmpeg", "-i", "voiceover-cn.m4a",
        "-filter:a", "atempo=1.20,asetrate=44100*0.887,atempo=1.127",
        "voiceover-cn-adjusted.m4a", "-y"
    ], check=True)
    
    # Step 2: Generate lip-synced talking heads
    print("Step 2: Generating lip-synced talking heads (this takes ~5 minutes)...")
    os.chdir(f"{base_dir}/Wav2Lip")
    
    subprocess.run([
        "python3", "inference.py",
        "--checkpoint_path", "checkpoints/wav2lip_gan.pth",
        "--face", "../avartar/image4-removed.png",
        "--audio", f"../scripts/{date}/voiceover-en-adjusted.m4a",
        "--outfile", f"../scripts/{date}/talking_head_en_adjusted.mp4"
    ], check=True)
    
    subprocess.run([
        "python3", "inference.py",
        "--checkpoint_path", "checkpoints/wav2lip_gan.pth",
        "--face", "../avartar/image4-removed.png",
        "--audio", f"../scripts/{date}/voiceover-cn-adjusted.m4a",
        "--outfile", f"../scripts/{date}/talking_head_cn_adjusted.mp4"
    ], check=True)
    
    # Step 3 & 4: Create backgrounds and compose final videos
    print("Step 3: Creating backgrounds and composing final videos...")
    os.chdir(base_dir)
    
    # Create text overlay if it doesn't exist
    if not os.path.exists(f"{scripts_dir}/text_overlay.png"):
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGBA', (150, 30), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        except:
            font = ImageFont.load_default()
        draw.text((5, 5), "@kfromkmedia", fill=(255, 255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0, 255))
        img.save(f"{scripts_dir}/text_overlay.png")
    
    # Process EN video
    process_video("en", date, base_dir, scripts_dir)
    
    # Process CN video
    process_video("cn", date, base_dir, scripts_dir)
    
    print(f"\n✓ Videos generated successfully!")
    print(f"  EN: {scripts_dir}/final_video_en_complete.mp4")
    print(f"  CN: {scripts_dir}/final_video_cn_complete.mp4")

def process_video(lang, date, base_dir, scripts_dir):
    """Process a single video (EN or CN)"""
    print(f"\nProcessing {lang.upper()} video...")
    
    # Get audio duration
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        f"{scripts_dir}/voiceover-{lang}-adjusted.m4a"
    ], capture_output=True, text=True, check=True)
    audio_dur = float(result.stdout.strip())
    
    # Create thumbnail video
    thumb_file = f"{scripts_dir}/thumb_{lang}_7s.mp4"
    if not os.path.exists(thumb_file):
        subprocess.run([
            "ffmpeg", "-loop", "1", "-t", "7",
            "-i", f"{base_dir}/avartar/thumb-{lang}.png",
            "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=25",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            thumb_file, "-y"
        ], check=True, capture_output=True)
    
    # Create trimmed slideshow
    slideshow_dur = audio_dur - 14
    slideshow_file = f"{scripts_dir}/slideshow_{lang}_trimmed.mp4"
    
    # Use existing slideshow or create new one
    if os.path.exists(f"{scripts_dir}/final_video_en.mp4"):
        source_slideshow = f"{scripts_dir}/final_video_en.mp4"
    else:
        # Create slideshow from images_asset
        print(f"  Creating slideshow from images...")
        # This would need the slideshow creation logic
        source_slideshow = f"{scripts_dir}/final_video_en.mp4"
    
    subprocess.run([
        "ffmpeg", "-i", source_slideshow,
        "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=25",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-t", str(slideshow_dur),
        slideshow_file, "-y"
    ], check=True, capture_output=True)
    
    # Create concat file
    concat_file = f"{scripts_dir}/concat_{lang}.txt"
    with open(concat_file, 'w') as f:
        f.write(f"file 'thumb_{lang}_7s.mp4'\n")
        f.write(f"file 'slideshow_{lang}_trimmed.mp4'\n")
        f.write(f"file 'thumb_{lang}_7s.mp4'\n")
    
    # Concatenate background
    bg_file = f"{scripts_dir}/bg_final_{lang}.mp4"
    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-c", "copy", bg_file, "-y"
    ], check=True, capture_output=True)
    
    # Compose final video
    subprocess.run([
        "ffmpeg",
        "-stream_loop", "-1", "-i", f"{scripts_dir}/talking_head_{lang}_adjusted.mp4",
        "-i", bg_file,
        "-loop", "1", "-i", f"{scripts_dir}/text_overlay.png",
        "-i", f"{scripts_dir}/voiceover-{lang}-adjusted.m4a",
        "-filter_complex",
        "[1:v]fps=25[bg];"
        "[0:v]scale=115:-1,fps=25[face];"
        "[bg][face]overlay=W-w-10:H-h-60[v1];"
        "[v1][2:v]overlay=W-160:H-25[v]",
        "-map", "[v]", "-map", "3:a",
        "-c:v", "libx264", "-c:a", "copy",
        "-shortest",
        f"{scripts_dir}/final_video_{lang}_complete.mp4", "-y"
    ], check=True, capture_output=True)
    
    # Get file size
    size = os.path.getsize(f"{scripts_dir}/final_video_{lang}_complete.mp4") / (1024*1024)
    print(f"  ✓ {lang.upper()} video complete: {size:.1f} MB, {audio_dur/60:.1f} min")

if __name__ == "__main__":
    main()
