# Automated YouTube News Video Generator

An automated system that generates daily 2-minute YouTube videos about China-US-Europe geopolitical news with Chinese narration.

## What It Does

Automatically creates daily videos with:
- Latest news from The Economist (China/US/Europe focus)
- Chinese script translation
- Relevant stock images
- Video slideshow
- Twitter preview text for promotion

## Features

✅ Fetches real-time news headlines and article content
✅ Generates 2-3 minute video script with specific facts and details
✅ Translates to Chinese
✅ Downloads 8-10 relevant images from Pixabay (free stock photos)
✅ Creates Twitter preview text in Chinese
✅ Generates video slideshow (images + your voiceover)
✅ Organizes everything in daily folders

## Setup

### Prerequisites
- Python 3
- ffmpeg: `brew install ffmpeg`
- Pixabay API key (free): https://pixabay.com/api/docs/

### Installation

```bash
cd /Users/kaizhen/myworkspace/twitter-bot
pip3 install tweepy requests beautifulsoup4 feedparser newspaper3k
```

### Configuration

API keys are already configured in the scripts:
- Pixabay API key: In `video_creator.py`
- Twitter API keys: In `.env` file (for future use)

## Daily Workflow

### Automated Script Generation (2 minutes)

```bash
cd /Users/kaizhen/myworkspace/twitter-bot
./generate_daily_script.sh
```

This creates a folder: `scripts/YYYY-MM-DD/` with:
- `1_english_script.txt` - Full English script with sources
- `2_chinese_script.txt` - Chinese translation
- `3_twitter_preview.txt` - Twitter promotion text
- `4_scene_breakdown.txt` - Scene-by-scene guide
- `5_voiceover_only.txt` - Clean narration text (read this!)
- `6_video_workflow.txt` - Instructions
- `7_image_keywords.txt` - Image keywords used
- `images/` - Downloaded stock photos
- `voiceover.mp3` - (you create this)
- `final_video.mp4` - Final video (created after voiceover)

### Record Your Voiceover (5 minutes)

1. Open `scripts/YYYY-MM-DD/5_voiceover_only.txt`
2. Record yourself reading it (use phone/mic)
3. Save as: `scripts/YYYY-MM-DD/voiceover.mp3`

### Create Final Video (30 seconds)

```bash
cd /Users/kaizhen/myworkspace/twitter-bot
python3 video_creator.py --create-video
```

This creates: `scripts/YYYY-MM-DD/final_video.mp4`

### Publish (3 minutes)

1. Upload `final_video.mp4` to YouTube
2. Copy text from `3_twitter_preview.txt`
3. Post to Twitter with YouTube link

## Total Time Per Day: ~10 minutes

- Script generation: 2 min (automated)
- Record voiceover: 5 min (manual)
- Create video: 30 sec (automated)
- Upload & post: 3 min (manual)

## Cost: $0/month

Everything uses free tiers:
- Pixabay API: Free
- The Economist RSS: Free
- Ollama (local LLM): Free
- Stock images: Free

## File Structure

```
twitter-bot/
├── generate_daily_script.sh    # Main workflow script
├── news_aggregator.py          # Fetches news and generates script
├── video_generator.py          # Extracts voiceover text
├── video_creator.py            # Downloads images and creates video
├── bot.py                      # Twitter bot (for future use)
├── config.py                   # Configuration
├── .env                        # API keys
└── scripts/
    └── YYYY-MM-DD/
        ├── 1_english_script.txt
        ├── 2_chinese_script.txt
        ├── 3_twitter_preview.txt
        ├── 5_voiceover_only.txt
        ├── voiceover.mp3        # You create this
        ├── final_video.mp4      # Final output
        └── images/              # Stock photos
```

## How It Works

### 1. News Aggregation
- Fetches headlines from The Economist RSS feed
- Filters for China/US/Europe keywords
- Extracts article content (not just headlines)
- Gets specific facts, numbers, quotes

### 2. Script Generation
- Uses Ollama (local LLM - llama3.2) to generate script
- Creates 2-3 minute structure: Hook → Main Stories → Closing
- Includes specific details from articles
- Translates to Chinese

### 3. Image Download
- Extracts keywords from Chinese script
- Searches Pixabay for relevant images
- Downloads 8-10 high-quality stock photos
- All images are free for commercial use

### 4. Video Creation
- Combines images into slideshow
- Syncs with voiceover duration
- Each image displays for equal time
- Outputs 720p MP4 video

## Customization

### Change News Sources

Edit `news_aggregator.py`:
```python
self.rss_feeds = {
    'Economist': 'https://www.economist.com/china/rss.xml',
    'Reuters': 'https://www.reutersagency.com/feed/...',
    # Add more feeds
}
```

### Change Video Duration

The video automatically matches your voiceover length. Longer voiceover = longer video.

### Change Image Count

Edit `video_creator.py` line ~200:
```python
return all_headlines[:10]  # Change 10 to desired number
```

## Troubleshooting

### "No images found"
- Check Pixabay API key is correct
- Check internet connection
- Keywords might be too specific

### "Voiceover not found"
- Make sure you saved it as `voiceover.mp3` (not `voice.mp3`)
- Check it's in the correct date folder

### Video is too short/long
- Video duration matches voiceover duration
- Record longer/shorter voiceover to adjust

### Script quality is poor
- The LLM (llama3.2) generates the script
- Quality depends on source articles
- You can manually edit the Chinese script before recording

## Future Enhancements

- [ ] Automatic YouTube upload
- [ ] Automatic Twitter posting
- [ ] Multiple language support
- [ ] Custom thumbnails
- [ ] Background music
- [ ] Subtitle generation

## Credits

Built using:
- Ollama (llama3.2) for script generation
- Pixabay for stock images
- FFmpeg for video creation
- The Economist for news content

## License

For personal use only. Respect source attribution and licensing.

---

**Created:** January 31, 2026
**Last Updated:** January 31, 2026
