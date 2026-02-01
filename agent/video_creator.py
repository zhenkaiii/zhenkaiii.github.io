import os
import requests
from datetime import datetime
import time

class AutoVideoCreator:
    def __init__(self, script_dir):
        self.script_dir = script_dir
        self.ollama_url = "http://localhost:11434/api/generate"
        self.elevenlabs_api_key = "sk_39e4c7f214e464e3375e98b5b550d2f250d39682ea07ba5c"
    
    def extract_keywords(self, script_file):
        """Extract visual keywords from Chinese script"""
        with open(script_file, 'r', encoding='utf-8') as f:
            script = f.read()
        
        prompt = f"""From this Chinese video script, extract 8-10 keywords for finding images.
Return ONLY the keywords in English, one per line, no numbering.
Focus on: people, places, objects, concepts that can be visualized.

Script:
{script}

Example output:
Xi Jinping
aircraft carrier
rural China
military officers
"""
        
        try:
            response = requests.post(self.ollama_url, json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            })
            result = response.json()
            keywords = [k.strip() for k in result['response'].strip().split('\n') if k.strip() and not k.strip().startswith('#')]
            return keywords[:10]
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []
    
    def generate_voiceover_elevenlabs(self, text, output_file):
        """Generate Chinese voiceover using ElevenLabs API"""
        # Use a Chinese voice - Rachel (multilingual) or get voice ID from ElevenLabs
        voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel - supports Chinese
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            print("Generating voiceover with ElevenLabs...")
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                print(f"✓ Voiceover generated: {output_file}")
                return True
            else:
                print(f"✗ ElevenLabs API error: {response.status_code}")
                print(response.text)
                return False
        except Exception as e:
            print(f"✗ Error generating voiceover: {e}")
            return False
    
    def download_images_pixabay(self, keywords, output_dir):
        """Download images from Pixabay"""
        API_KEY = '54462194-5a128b709c181be934624389c'
        
        os.makedirs(output_dir, exist_ok=True)
        downloaded = []
        
        for i, keyword in enumerate(keywords):
            try:
                url = f"https://pixabay.com/api/?key={API_KEY}&q={keyword}&image_type=photo&per_page=3"
                print(f"Searching: {keyword}...")
                
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('hits'):
                        # Get the first image
                        img_url = data['hits'][0]['largeImageURL']
                        
                        # Download
                        img_response = requests.get(img_url, timeout=10)
                        if img_response.status_code == 200:
                            filename = os.path.join(output_dir, f"{i+1:02d}_{keyword.replace(' ', '_')}.jpg")
                            with open(filename, 'wb') as f:
                                f.write(img_response.content)
                            downloaded.append(filename)
                            print(f"✓ Downloaded: {keyword}")
                        else:
                            print(f"✗ Failed to download image for: {keyword}")
                    else:
                        print(f"✗ No images found for: {keyword}")
                else:
                    print(f"✗ API error for: {keyword}")
                
                time.sleep(1)
            except Exception as e:
                print(f"✗ Error: {keyword} - {e}")
        
        return downloaded
    
    def create_slideshow_video(self, images_dir, voiceover_file, output_video):
        """Create slideshow video using ffmpeg"""
        import glob
        import subprocess
        
        images = sorted(glob.glob(os.path.join(images_dir, "*.jpg")))
        
        if not images:
            print("No images found")
            return False
        
        # Get voiceover duration
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
             '-of', 'default=noprint_wrappers=1:nokey=1', voiceover_file],
            capture_output=True, text=True
        )
        vo_duration = float(result.stdout.strip())
        
        # Calculate duration per image to match voiceover
        duration_per_image = vo_duration / len(images)
        
        print(f"Voiceover: {vo_duration:.1f}s, Images: {len(images)}, Duration per image: {duration_per_image:.1f}s")
        
        # Create file list for ffmpeg with absolute paths
        list_file = os.path.join(images_dir, "images.txt")
        with open(list_file, 'w') as f:
            for img in images[:-1]:  # All but last
                abs_path = os.path.abspath(img)
                f.write(f"file '{abs_path}'\n")
                f.write(f"duration {duration_per_image}\n")
            # Last image (no duration needed)
            abs_path = os.path.abspath(images[-1])
            f.write(f"file '{abs_path}'\n")
        
        # FFmpeg command to create slideshow with voiceover
        abs_list = os.path.abspath(list_file)
        abs_vo = os.path.abspath(voiceover_file)
        abs_out = os.path.abspath(output_video)
        
        cmd = f'ffmpeg -f concat -safe 0 -i "{abs_list}" -i "{abs_vo}" -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest "{abs_out}" -y'
        
        print("\nCreating video...")
        result = os.system(cmd)
        
        if result == 0 and os.path.exists(output_video):
            print(f"\n✓ Video created: {output_video}")
            file_size = os.path.getsize(output_video) / (1024*1024)
            print(f"  Size: {file_size:.1f} MB")
            return True
        else:
            print("\n✗ Video creation failed")
            return False
    
    def run(self):
        """Main execution"""
        timestamp = datetime.now().strftime('%Y-%m-%d')
        day_dir = os.path.join(self.script_dir, timestamp)
        
        if not os.path.exists(day_dir):
            print(f"No script found for {timestamp}")
            return
        
        chinese_script = os.path.join(day_dir, "2_chinese_script.txt")
        
        # Extract keywords
        print("Extracting keywords from script...")
        keywords = self.extract_keywords(chinese_script)
        
        if not keywords:
            print("No keywords extracted")
            return
        
        print(f"\nKeywords found: {', '.join(keywords)}")
        
        # Save keywords
        keywords_file = os.path.join(day_dir, "7_image_keywords.txt")
        with open(keywords_file, 'w') as f:
            f.write("IMAGE KEYWORDS\n")
            f.write("="*60 + "\n\n")
            for i, kw in enumerate(keywords, 1):
                f.write(f"{i}. {kw}\n")
        print(f"✓ Keywords saved")
        
        # Download images automatically
        images_dir = os.path.join(day_dir, "images")
        print(f"\nDownloading images from Pixabay...\n")
        
        downloaded = self.download_images_pixabay(keywords, images_dir)
        
        print(f"\n✓ Downloaded {len(downloaded)} images")
        
        # Generate voiceover automatically
        voiceover_script = os.path.join(day_dir, "5_voiceover_only.txt")
        voiceover_file = os.path.join(day_dir, "voiceover.mp3")
        
        if os.path.exists(voiceover_script):
            with open(voiceover_script, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract just the narration text
                lines = content.split('\n')
                text = '\n'.join([l for l in lines if l and not l.startswith('=') and 'VOICEOVER' not in l and 'Character count' not in l])
            
            print("\n" + "="*60)
            self.generate_voiceover_elevenlabs(text, voiceover_file)
        
        print(f"\n{'='*60}")
        print("NEXT STEP:")
        print(f"{'='*60}")
        print("\nCreate video (1 min):")
        print("   - Install ffmpeg: brew install ffmpeg")
        print("   - Run: python3 video_creator.py --create-video")
        print(f"\n{'='*60}")

if __name__ == "__main__":
    import sys
    creator = AutoVideoCreator("scripts")
    
    if "--create-video" in sys.argv:
        # Create video from existing images and voiceover
        timestamp = datetime.now().strftime('%Y-%m-%d')
        day_dir = os.path.join("scripts", timestamp)
        images_dir = os.path.join(day_dir, "images")
        voiceover = os.path.join(day_dir, "voiceover.mp3")
        output = os.path.join(day_dir, "final_video.mp4")
        
        if os.path.exists(voiceover):
            creator.create_slideshow_video(images_dir, voiceover, output)
        else:
            print(f"Voiceover not found: {voiceover}")
    else:
        creator.run()
