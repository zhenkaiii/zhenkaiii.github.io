import os
from datetime import datetime

class VideoGenerator:
    """Generate video assets for manual assembly"""
    
    def __init__(self, script_dir):
        self.script_dir = script_dir
        self.ollama_url = "http://localhost:11434/api/generate"
    
    def generate_scene_breakdown(self, script_file):
        """Break script into scenes with visual suggestions"""
        with open(script_file, 'r', encoding='utf-8') as f:
            script = f.read()
        
        import requests
        prompt = f"""Break this Chinese video script into scenes for video editing.
For each scene, specify:
1. Timestamp
2. What to show (stock footage keywords)
3. Text overlay (if any)

Script:
{script}

Format as:
Scene 1 (0:00-0:10)
Visual: [keywords for stock footage]
Text: [text to show on screen]
Narration: [what's being said]
"""
        
        try:
            response = requests.post(self.ollama_url, json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            })
            result = response.json()
            return result['response']
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def generate_voiceover_script(self, script_file):
        """Extract clean narration for voiceover - robust extraction"""
        with open(script_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try multiple extraction methods
        narration = []
        
        # Method 1: Look for common narrator markers
        markers = ['Host:', 'Narrator:', 'narrators:', '主持人：', '主持人:', 'Host :', 'Narrator :']
        for line in content.split('\n'):
            for marker in markers:
                if marker.lower() in line.lower():
                    # Extract text after the marker
                    parts = line.split(marker, 1) if marker in line else line.lower().split(marker.lower(), 1)
                    if len(parts) > 1:
                        text = parts[1].strip().strip('"').strip('"').strip('"').strip('\"\"').strip()
                        if text and len(text) > 15:  # Only substantial text
                            narration.append(text)
                    break
        
        # If no narration found, extract all Chinese text (fallback)
        if not narration:
            import re
            chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
            for line in content.split('\n'):
                if chinese_pattern.search(line) and len(line.strip()) > 20:
                    # Skip headers and formatting
                    if not any(skip in line for skip in ['===', '**', 'SCRIPT', '视频脚本', 'Here is']):
                        clean = line.strip().strip('"').strip()
                        if clean:
                            narration.append(clean)
        
        result = '\n\n'.join(narration)
        return result if result else ""
    
    def save_video_assets(self):
        """Generate all assets needed for video creation"""
        timestamp = datetime.now().strftime('%Y-%m-%d')
        day_dir = os.path.join(self.script_dir, timestamp)
        
        if not os.path.exists(day_dir):
            print(f"No script found for {timestamp}")
            return
        
        chinese_script = os.path.join(day_dir, "2_chinese_script.txt")
        
        # Generate scene breakdown
        print("Generating scene breakdown...")
        scenes = self.generate_scene_breakdown(chinese_script)
        if scenes:
            scenes_file = os.path.join(day_dir, "4_scene_breakdown.txt")
            with open(scenes_file, 'w', encoding='utf-8') as f:
                f.write("VIDEO SCENE BREAKDOWN\n")
                f.write("="*60 + "\n\n")
                f.write(scenes)
            print(f"✓ Scene breakdown saved")
        
        # Generate clean voiceover script
        print("Generating voiceover script...")
        voiceover = self.generate_voiceover_script(chinese_script)
        if voiceover:
            vo_file = os.path.join(day_dir, "5_voiceover_only.txt")
            with open(vo_file, 'w', encoding='utf-8') as f:
                f.write("VOICEOVER SCRIPT (Clean narration only)\n")
                f.write("="*60 + "\n\n")
                f.write(voiceover)
                f.write(f"\n\n{'='*60}\n")
                f.write(f"Character count: {len(voiceover)}\n")
            print(f"✓ Voiceover script saved")
        
        # Generate instructions
        instructions = f"""
VIDEO CREATION WORKFLOW (FREE)
{'='*60}

STEP 1: Generate AI Voiceover (FREE)
- Go to: https://elevenlabs.io (free tier: 10k chars/month)
- Copy text from: 5_voiceover_only.txt
- Select Chinese voice
- Generate and download MP3

STEP 2: Get Stock Footage (FREE)
- Use keywords from: 4_scene_breakdown.txt
- Download from:
  * Pexels.com (free, no attribution)
  * Pixabay.com (free, no attribution)
  * Unsplash.com (free photos)

STEP 3: Edit Video (FREE - CapCut)
- Download CapCut: https://www.capcut.com
- Import voiceover MP3
- Add stock footage matching scenes
- Add text overlays (from scene breakdown)
- Export 1080p

STEP 4: Post to YouTube
- Upload video
- Copy description from: 1_english_script.txt (sources)

STEP 5: Promote on Twitter
- Copy text from: 3_twitter_preview.txt
- Add YouTube link

{'='*60}
Estimated time: 30-45 minutes per video
"""
        
        instructions_file = os.path.join(day_dir, "6_video_workflow.txt")
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        print(f"✓ Workflow instructions saved")
        
        print(f"\n✅ All video assets ready in: {day_dir}/")
        print("\nFiles created:")
        print("  1_english_script.txt - Original script with sources")
        print("  2_chinese_script.txt - Chinese translation")
        print("  3_twitter_preview.txt - Twitter promotion text")
        print("  4_scene_breakdown.txt - Scene-by-scene visual guide")
        print("  5_voiceover_only.txt - Clean narration for AI voice")
        print("  6_video_workflow.txt - Step-by-step instructions")

if __name__ == "__main__":
    generator = VideoGenerator("scripts")
    generator.save_video_assets()
