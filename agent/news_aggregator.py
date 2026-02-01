import requests
from datetime import datetime
import feedparser

class NewsAggregator:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.rss_feeds = {
            'Economist': 'https://www.economist.com/china/rss.xml',
            'Reuters': 'https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best',
            'FT': 'https://www.ft.com/?format=rss',
        }
    
    def fetch_article_content(self, url):
        """Fetch article content from URL"""
        try:
            from newspaper import Article
            article = Article(url)
            article.download()
            article.parse()
            return article.text[:2000]  # First 2000 chars
        except:
            return None
    
    def fetch_headlines(self):
        """Fetch headlines from RSS feeds with article content"""
        all_headlines = []
        
        keywords = ['china', 'us', 'america', 'euro', 'europe', 'trade', 'economy', 'gdp', 'inflation', 'tariff', 'xi', 'trump', 'biden']
        
        for source, url in self.rss_feeds.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:20]:
                    title = entry.get('title', '')
                    link = entry.get('link', '')
                    
                    if len(title) > 30 and any(keyword in title.lower() for keyword in keywords):
                        # Try to get article content
                        content = self.fetch_article_content(link)
                        summary = entry.get('summary', '')[:500] if not content else content
                        
                        all_headlines.append({
                            'source': source,
                            'title': title,
                            'link': link,
                            'content': summary
                        })
                        
                        if len(all_headlines) >= 5:
                            break
            except Exception as e:
                print(f"Error fetching {source}: {e}")
        
        return all_headlines[:5]
    
    def generate_script(self, headlines):
        """Generate YouTube video script from headlines"""
        stories_text = ""
        for i, h in enumerate(headlines, 1):
            stories_text += f"\nStory {i} - [{h['source']}] {h['title']}\n"
            stories_text += f"Content: {h['content'][:800]}\n"
        
        prompt = f"""You are a geopolitical analyst creating a YouTube video script about today's China-US-Europe news.

Today's stories with actual content:
{stories_text}

Create a 2-3 minute video script. Structure:
1. Hook (10 seconds) - Start with the most important/surprising development
2. Main stories (2 minutes) - Cover 3-4 stories with SPECIFIC details from the articles (numbers, quotes, facts)
3. Closing (20 seconds) - Connect the stories and their implications

Style: Clear, factual, insightful. Use SPECIFIC information from the articles, not generic commentary."""
        
        try:
            response = requests.post(self.ollama_url, json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            })
            result = response.json()
            return result['response']
        except Exception as e:
            print(f"Error generating script: {e}")
            return None
    
    def translate_to_chinese(self, text):
        """Translate script to Chinese"""
        prompt = f"""Translate this YouTube video script to Chinese (Simplified). Keep the structure and formatting:

{text}"""
        
        try:
            response = requests.post(self.ollama_url, json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            })
            result = response.json()
            return result['response']
        except Exception as e:
            print(f"Error translating: {e}")
            return None
    
    def generate_twitter_preview(self, chinese_script):
        """Generate short Twitter preview from Chinese script"""
        prompt = f"""From this Chinese video script, extract the most compelling highlight for a Twitter post.
Write it in Chinese. Make it 200-250 characters, engaging, and make people want to watch the full video.
End with: 完整视频链接在评论👇

Script:
{chinese_script}"""
        
        try:
            response = requests.post(self.ollama_url, json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            })
            result = response.json()
            preview = result['response'].strip().strip('"')[:260]
            return preview
        except Exception as e:
            print(f"Error generating preview: {e}")
            return None
    
    def save_script(self, script, headlines):
        """Save script to organized folder structure"""
        import os
        
        timestamp = datetime.now().strftime('%Y-%m-%d')
        
        # Create folder structure
        base_dir = "scripts"
        day_dir = os.path.join(base_dir, timestamp)
        os.makedirs(day_dir, exist_ok=True)
        
        # File 1: English script
        english_file = os.path.join(day_dir, "1_english_script.txt")
        with open(english_file, 'w', encoding='utf-8') as f:
            f.write(f"VIDEO SCRIPT - {timestamp}\n")
            f.write("="*60 + "\n\n")
            f.write("SOURCES:\n")
            for h in headlines:
                f.write(f"- [{h['source']}] {h['title']}\n")
            f.write("\n" + "="*60 + "\n\n")
            f.write("SCRIPT:\n\n")
            f.write(script)
        
        print(f"✓ English script saved")
        
        # File 2: Chinese translation
        print("Translating to Chinese...")
        chinese_script = self.translate_to_chinese(script)
        if chinese_script:
            chinese_file = os.path.join(day_dir, "2_chinese_script.txt")
            with open(chinese_file, 'w', encoding='utf-8') as f:
                f.write(f"视频脚本 - {timestamp}\n")
                f.write("="*60 + "\n\n")
                f.write(chinese_script)
            print(f"✓ Chinese script saved")
        
        # File 3: Twitter preview
        print("Generating Twitter preview...")
        twitter_preview = self.generate_twitter_preview(chinese_script if chinese_script else script)
        if twitter_preview:
            preview_file = os.path.join(day_dir, "3_twitter_preview.txt")
            with open(preview_file, 'w', encoding='utf-8') as f:
                f.write(f"TWITTER PREVIEW - {timestamp}\n")
                f.write("="*60 + "\n\n")
                f.write(twitter_preview)
                f.write(f"\n\n{'='*60}\n")
                f.write(f"Characters: {len(twitter_preview)}/280\n")
            print(f"✓ Twitter preview saved")
            
            print(f"\n{'='*60}")
            print("TWITTER PREVIEW:")
            print(f"{'='*60}")
            print(twitter_preview)
            print(f"{'='*60}\n")
        
        print(f"\n✓ All files saved to: {day_dir}/")
        return day_dir
    
    def run(self):
        """Main execution"""
        print("Fetching headlines...")
        headlines = self.fetch_headlines()
        
        if not headlines:
            print("No headlines found")
            return
        
        print(f"Found {len(headlines)} relevant headlines")
        
        print("\nGenerating script...")
        script = self.generate_script(headlines)
        
        if script:
            self.save_script(script, headlines)

if __name__ == "__main__":
    aggregator = NewsAggregator()
    aggregator.run()
