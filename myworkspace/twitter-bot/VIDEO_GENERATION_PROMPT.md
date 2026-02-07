# Twitter Bot Video Generation Workflow

## Manual Tasks (You Must Do)

### 1. Paste Articles
- Paste full article content for the day's news
- This is used to generate image keywords and context

### 2. Record Voiceovers
- Record English voiceover → save as `scripts/YYYY-MM-DD/voiceover-en.m4a`
- Record Chinese voiceover → save as `scripts/YYYY-MM-DD/voiceover-cn.m4a`

### 3. Download Background Images
- Download ~16 images from Google Photos shared album
- Save to `/Users/kaizhen/myworkspace/twitter-bot/images_asset/`
- Images should be named: `image_001.jpg`, `image_002.jpg`, etc.

### 4. Create/Update Thumbnail Images
- Create English thumbnail → save as `avartar/thumb-en.png`
- Create Chinese thumbnail → save as `avartar/thumb-cn.png`
- Recommended size: 1536x1024 (will be scaled to fit 1280x720)

## Automated Tasks (AI Will Do)

### 1. Generate Image Keywords
- Extract keywords from articles for image search

### 2. Create Slideshow
- Generate slideshow from images in `images_asset/`
- Scale and crop to 1280x720

### 3. Adjust Voiceovers
- Speed up by 20%
- Lower pitch by 2 semitones

### 4. Generate Lip-Synced Talking Heads
- Use Wav2Lip to sync avatar with adjusted audio
- Takes ~3-5 minutes per video

### 5. Compose Final Videos
- Add thumbnails at start/end (7 seconds each)
- Overlay talking head (115px, bottom-right)
- Add @kfromkmedia text throughout
- Combine all elements into final videos

## Tools & Libraries Required

### System Requirements
- **macOS** (tested on macOS)
- **Python 3.9+**
- **FFmpeg 8.0.1+** (with libx264, libmp3lame, libopus support)

### Python Libraries
```bash
# Core video processing
pip install opencv-python
pip install numpy
pip install scipy

# Wav2Lip (lip-sync generation)
pip install librosa
pip install torch torchvision torchaudio
pip install face-alignment
pip install batch-face

# Image processing
pip install Pillow

# Audio transcription (optional)
pip install openai-whisper
```

### External Tools
1. **Wav2Lip** - AI lip-sync generation
   - Location: `/Users/kaizhen/myworkspace/twitter-bot/Wav2Lip/`
   - Model: `checkpoints/wav2lip_gan.pth` (416MB)
   - GitHub: https://github.com/Rudrabha/Wav2Lip

2. **FFmpeg** - Video/audio processing
   - Install: `brew install ffmpeg`
   - Used for: video composition, audio adjustment, format conversion

3. **Google Photos API** (optional)
   - For downloading images from shared albums
   - Requires OAuth credentials

### How These Tools Chain Together

```
1. Article Text
   ↓
2. [You] Record Voiceovers → voiceover-en.m4a, voiceover-cn.m4a
   ↓
3. [FFmpeg] Adjust Audio → Speed +20%, Pitch -2 semitones
   ↓
4. [Wav2Lip + PyTorch] Generate Lip-Sync → talking_head_en/cn_adjusted.mp4
   ↓
5. [FFmpeg] Create Slideshow → Background video from images_asset/
   ↓
6. [FFmpeg] Add Thumbnails → 7s at start + slideshow + 7s at end
   ↓
7. [Pillow] Create Text Overlay → @kfromkmedia PNG
   ↓
8. [FFmpeg] Compose Final Video → Combine all layers
   ↓
9. Final Output: final_video_en/cn_complete.mp4
```

### Installation Commands

```bash
# Install FFmpeg
brew install ffmpeg

# Install Python dependencies
pip install opencv-python numpy scipy librosa torch torchvision torchaudio face-alignment batch-face Pillow

# Clone and setup Wav2Lip
cd /Users/kaizhen/myworkspace/twitter-bot
git clone https://github.com/Rudrabha/Wav2Lip.git
cd Wav2Lip

# Download Wav2Lip model (416MB)
mkdir -p checkpoints
cd checkpoints
wget https://github.com/Rudrabha/Wav2Lip/releases/download/models/wav2lip_gan.pth
```

## Prerequisites Checklist
Before starting automation, ensure you have:
- [x] All tools and libraries installed (see above)
- [x] Voiceover files in `scripts/YYYY-MM-DD/`:
  - `voiceover-en.m4a` (English voiceover)
  - `voiceover-cn.m4a` (Chinese voiceover)
- [x] Thumbnail images in `avartar/`:
  - `thumb-en.png` (English thumbnail)
  - `thumb-cn.png` (Chinese thumbnail)
- [x] Avatar image: `avartar/image4-removed.png` (background removed)
- [x] Background images in `images_asset/` directory (~16 images)

## Prompt to Copy-Paste

```
Generate English and Chinese videos for Twitter bot with these specifications:

**Directory:** /Users/kaizhen/myworkspace/twitter-bot/scripts/YYYY-MM-DD/
(Replace YYYY-MM-DD with today's date)

**Video Requirements:**
1. **Thumbnails:** 
   - EN: Use `/Users/kaizhen/myworkspace/twitter-bot/avartar/thumb-en.png` at start and end (7 seconds each)
   - CN: Use `/Users/kaizhen/myworkspace/twitter-bot/avartar/thumb-cn.png` at start and end (7 seconds each)
   - Scale to fit 1280x720 without cropping (pad with black bars if needed)

2. **Voiceover:**
   - EN: Use `voiceover-en.m4a` from scripts directory
   - CN: Use `voiceover-cn.m4a` from scripts directory
   - Speed up by 20% (atempo=1.20)
   - Lower pitch by 2 semitones (asetrate=44100*0.887,atempo=1.127)

3. **Talking Head:**
   - Use `/Users/kaizhen/myworkspace/twitter-bot/avartar/image4-removed.png`
   - Generate lip-synced video with Wav2Lip using adjusted audio
   - Size: 115px width
   - Position: Bottom-right corner (10px from right, 60px from bottom)
   - Loop to match full video duration

4. **Text Overlay:**
   - Text: "@kfromkmedia"
   - Position: Far right, 25px from bottom (W-160:H-25)
   - Display throughout entire video (including thumbnails)

5. **Background:**
   - Create slideshow from images in `/Users/kaizhen/myworkspace/twitter-bot/images_asset/`
   - Scale to 1280:720 and crop to remove black bars
   - Duration: Total video length minus 14 seconds (for thumbnails)

**Output Files:**
- `/Users/kaizhen/myworkspace/twitter-bot/scripts/YYYY-MM-DD/final_video_en_complete.mp4`
- `/Users/kaizhen/myworkspace/twitter-bot/scripts/YYYY-MM-DD/final_video_cn_complete.mp4`

**Workflow Steps:**
1. Adjust voiceovers (speed +20%, pitch -2 semitones)
2. Generate lip-synced talking heads with Wav2Lip
3. Create background videos with thumbnails at start/end
4. Compose final videos with talking head and text overlay

Please execute this workflow.
```

## Manual Steps (if needed)

If you need to run steps manually:

### 1. Adjust Voiceovers
```bash
cd /Users/kaizhen/myworkspace/twitter-bot/scripts/YYYY-MM-DD

# English
ffmpeg -i voiceover-en.m4a -filter:a "atempo=1.20,asetrate=44100*0.887,atempo=1.127" voiceover-en-adjusted.m4a -y

# Chinese
ffmpeg -i voiceover-cn.m4a -filter:a "atempo=1.20,asetrate=44100*0.887,atempo=1.127" voiceover-cn-adjusted.m4a -y
```

### 2. Generate Lip-Synced Talking Heads
```bash
cd /Users/kaizhen/myworkspace/twitter-bot/Wav2Lip

# English
python3 inference.py --checkpoint_path checkpoints/wav2lip_gan.pth \
  --face ../avartar/image4-removed.png \
  --audio ../scripts/YYYY-MM-DD/voiceover-en-adjusted.m4a \
  --outfile ../scripts/YYYY-MM-DD/talking_head_en_adjusted.mp4

# Chinese
python3 inference.py --checkpoint_path checkpoints/wav2lip_gan.pth \
  --face ../avartar/image4-removed.png \
  --audio ../scripts/YYYY-MM-DD/voiceover-cn-adjusted.m4a \
  --outfile ../scripts/YYYY-MM-DD/talking_head_cn_adjusted.mp4
```

### 3. Create Background Videos
See `create_video_backgrounds.py` script

### 4. Compose Final Videos
See `compose_final_videos.py` script

## Notes
- Wav2Lip processing takes ~3-5 minutes per video
- Final video sizes: ~10MB for 6-minute videos
- All videos are 1280x720 @ 25fps
- Audio bitrate: 70 kb/s (AAC)
- Video codec: H.264
