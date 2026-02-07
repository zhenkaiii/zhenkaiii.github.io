import requests
from datetime import datetime
import feedparser
import os

class NewsAggregator:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.rss_feeds = {
            'Economist': 'https://www.economist.com/china/rss.xml',
            'Reuters': 'https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best',
            'AP News': 'https://rsshub.app/apnews/topics/apf-topnews',
        }
        self.economist_session = None
        self.economist_email = os.getenv('ECONOMIST_EMAIL')
        self.economist_password = os.getenv('ECONOMIST_PASSWORD')
    
    def login_economist(self):
        """Login to The Economist to access full articles"""
        if self.economist_session:
            return self.economist_session
        
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            
            # The Economist uses a complex auth flow, for now just use authenticated headers
            # This is a simplified version - full implementation would need OAuth flow
            self.economist_session = session
            return session
        except Exception as e:
            print(f"Economist login failed: {e}")
            return None
    
    def fetch_article_content(self, url):
        """Fetch article content from URL with authentication"""
        try:
            # Use authenticated session for Economist
            if 'economist.com' in url and self.economist_email:
                session = self.login_economist()
            else:
                session = requests.Session()
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = session.get(url, headers=headers, timeout=15)
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try multiple methods to extract content
            content = []
            
            # Method 1: Economist-specific selectors
            if 'economist.com' in url:
                # Try article body
                article_body = soup.find('div', {'class': ['article__body-text', 'ds-layout-grid']})
                if article_body:
                    for p in article_body.find_all('p'):
                        text = p.get_text(strip=True)
                        if len(text) > 50:
                            content.append(text)
                        if len(content) >= 8:  # Get more paragraphs
                            break
            
            # Method 2: Generic paragraph extraction
            if not content:
                for p in soup.find_all('p'):
                    text = p.get_text(strip=True)
                    if len(text) > 50:
                        content.append(text)
                    if len(content) >= 8:
                        break
            
            if content:
                full_text = ' '.join(content)
                print(f"  Extracted {len(full_text)} chars from {url[:50]}...")
                return full_text[:3000]  # Increased to 3000 chars with larger context
            
            return None
        except Exception as e:
            print(f"  Error fetching article: {e}")
            return None
    
    def fetch_headlines(self):
        """Fetch headlines from RSS feeds with article content"""
        all_headlines = []
        
        # Check if local articles exist
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        articles_dir = f'scripts/{today}/articles'
        
        if os.path.exists(articles_dir):
            print(f"Using local articles from {articles_dir}")
            # Load local articles (geopolitics)
            for i in range(1, 6):
                article_file = f'{articles_dir}/article_{i}.txt'
                if os.path.exists(article_file):
                    with open(article_file, 'r') as f:
                        lines = f.readlines()
                        title = lines[0].replace('Title: ', '').strip()
                        source = lines[1].replace('Source: ', '').strip()
                        url = lines[2].replace('URL: ', '').strip()
                        
                        # Get content after the separator
                        content_start = False
                        content = []
                        for line in lines:
                            if 'PASTE ARTICLE CONTENT BELOW:' in line:
                                content_start = True
                                continue
                            if content_start and line.strip():
                                content.append(line.strip())
                        
                        if content:
                            # Clean up navigation and junk text
                            full_text = ' '.join(content)
                            
                            # Extract content between "Listen to this story" and "■"
                            if 'Listen to this story' in full_text and '■' in full_text:
                                start = full_text.find('Listen to this story')
                                end = full_text.find('■', start)
                                if start != -1 and end != -1:
                                    full_text = full_text[start:end]
                            
                            # Remove common navigation patterns
                            junk_patterns = [
                                'The Economist', 'Insider', 'For you', 'Menu', 'Skip to content',
                                'Weekly edition', 'World in brief', 'United States', 'Business',
                                'Finance & economics', 'Europe', 'Middle East', 'Americas',
                                'Artificial intelligence', 'Culture', 'Cartoons & games',
                                'Save', 'Share', 'Summary', 'Listen to this story', 'AI Narrat',
                                'Photograph:', 'Illustration:', 'Getty Images', 'min read',
                                'Subscribe', 'Sign in', 'Search', 'Topics', 'Current edition'
                            ]
                            
                            # Split into sentences and filter
                            sentences = full_text.split('. ')
                            clean_sentences = []
                            for sent in sentences:
                                # Skip if it's mostly navigation junk
                                if len(sent) < 30:  # Too short
                                    continue
                                if any(junk in sent for junk in junk_patterns):
                                    continue
                                if sent.count('●') > 0 or sent.count('|') > 2:  # Navigation markers
                                    continue
                                clean_sentences.append(sent)
                            
                            clean_text = '. '.join(clean_sentences)
                            
                            if len(clean_text) > 500:  # Only use if we got substantial content
                                all_headlines.append({
                                    'source': source,
                                    'title': title,
                                    'link': url,
                                    'content': clean_text[:3000]
                                })
                                print(f"  Article {i}: {len(clean_text)} chars after cleaning")
            
            # Load economy/markets article
            economy_file = f'{articles_dir}/article_economy.txt'
            if os.path.exists(economy_file):
                with open(economy_file, 'r') as f:
                    lines = f.readlines()
                    title = lines[0].replace('Title: ', '').strip()
                    source = lines[1].replace('Source: ', '').strip()
                    url = lines[2].replace('URL: ', '').strip()
                    
                    content_start = False
                    content = []
                    for line in lines:
                        if 'PASTE ARTICLE CONTENT BELOW:' in line:
                            content_start = True
                            continue
                        if content_start and line.strip():
                            content.append(line.strip())
                    
                    if content:
                        full_text = ' '.join(content)
                        
                        # Extract content between "Listen to this story" and "■"
                        if 'Listen to this story' in full_text and '■' in full_text:
                            start = full_text.find('Listen to this story')
                            end = full_text.find('■', start)
                            if start != -1 and end != -1:
                                full_text = full_text[start:end]
                        
                        # Remove navigation junk
                        junk_patterns = [
                            'The Economist', 'Insider', 'For you', 'Menu', 'Skip to content',
                            'Weekly edition', 'World in brief', 'United States', 'Business',
                            'Finance & economics', 'Europe', 'Middle East', 'Americas',
                            'Artificial intelligence', 'Culture', 'Cartoons & games',
                            'Save', 'Share', 'Summary', 'Listen to this story', 'AI Narrat',
                            'Photograph:', 'Illustration:', 'Getty Images', 'min read',
                            'Subscribe', 'Sign in', 'Search', 'Topics', 'Current edition'
                        ]
                        
                        sentences = full_text.split('. ')
                        clean_sentences = []
                        for sent in sentences:
                            if len(sent) < 30:
                                continue
                            if any(junk in sent for junk in junk_patterns):
                                continue
                            if sent.count('●') > 0 or sent.count('|') > 2:
                                continue
                            clean_sentences.append(sent)
                        
                        clean_text = '. '.join(clean_sentences)
                        
                        if len(clean_text) > 500:
                            all_headlines.append({
                                'source': source,
                                'title': title,
                                'link': url,
                                'content': clean_text[:3000],
                                'category': 'economy'
                            })
                            print(f"  Economy article: {len(clean_text)} chars after cleaning")
            
            if all_headlines:
                print(f"Loaded {len(all_headlines)} local articles")
                return all_headlines  # Return all articles including economy
        
        # Fallback to RSS if no local articles
        print("No local articles found, using RSS feeds")
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
                        
                        # If content extraction failed (paywall), use RSS summary
                        if not content or len(content) < 200:
                            summary = entry.get('summary', '')
                            # Enhance with description if available
                            description = entry.get('description', '')
                            content = f"{summary} {description}".strip()[:1000]
                        
                        all_headlines.append({
                            'source': source,
                            'title': title,
                            'link': link,
                            'content': content if content else title
                        })
                        
                        if len(all_headlines) >= 5:
                            break
            except Exception as e:
                print(f"Error fetching {source}: {e}")
        
        return all_headlines[:5]
    
    def generate_script(self, headlines):
        """Generate YouTube video script from headlines"""
        stories_text = ""
        economy_story = None
        geopolitics_stories = []
        
        for h in headlines:
            if h.get('category') == 'economy':
                economy_story = h
            else:
                geopolitics_stories.append(h)
        
        # Add geopolitics stories
        for i, h in enumerate(geopolitics_stories, 1):
            stories_text += f"\nGeopolitics Story {i} - [{h['source']}] {h['title']}\n"
            stories_text += f"Content: {h['content'][:2000]}\n"
        
        # Add economy story separately
        if economy_story:
            stories_text += f"\n**ECONOMY STORY (MANDATORY)** - [{economy_story['source']}] {economy_story['title']}\n"
            stories_text += f"Content: {economy_story['content'][:2000]}\n"
        
        prompt = f"""You are a geopolitical analyst creating a YouTube video script about China-US-Europe news AND economy/markets.

Today's stories:
{stories_text}

Your job: Pick 2-3 GEOPOLITICS stories + ALWAYS include the ECONOMY story marked as MANDATORY above.

Create a script with this structure:

**INTRO**
Hello. Regarding China-US-Europe geopolitics and global markets, today we have [X] news stories to share.

**STORY 1** (Geopolitics)
[Write 3-4 sentences with key facts: numbers, dates, names, locations. Keep factual and concise - aim for 50-70 words.]

Our take: [150-200 words of OPINIONATED analysis. Quote relevant phrases from the article. Connect dots. Make bold predictions. Challenge conventional wisdom. Be specific about implications.]

**STORY 2** (Geopolitics)
[Same structure - concise facts]

Our take: [150-200 words of bold, opinionated analysis with quotes]

**STORY 3** (Geopolitics - if relevant)
[Same structure]

Our take: [150-200 words of analysis]

**STORY 4** (Economy/Markets - MANDATORY if available)
[Write 3-4 sentences about the economy/stock/investment story with key facts and numbers - 50-70 words.]

Our take: [150-200 words of OPINIONATED analysis about market implications, investment opportunities/risks, economic trends. Connect to geopolitical stories if relevant.]

**CLOSING**
Thank you for watching.

CRITICAL RULES:
- ALWAYS include the economy story if available (marked with category: 'economy')
- Geopolitics stories: 2-3 stories based on importance
- News summary: 50-70 words, just the facts
- "Our take": 150-200 words, OPINIONATED and analytical
- Quote relevant phrases from articles to support arguments
- Make connections between stories and broader trends
- Be bold - challenge assumptions, make predictions
- Total script: 600-1000 words (4-6 minutes)
- End with "Thank you for watching" - nothing else"""
        
        try:
            response = requests.post(self.ollama_url, json={
                "model": "llama3.1:8b-large",
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
        prompt = f"""You are translating a YouTube video script to Chinese (Simplified). 

CRITICAL RULES - MUST FOLLOW:
1. Output ONLY Chinese characters - absolutely NO English words
2. Translate ALL stage directions: "Intro music plays" → "开场音乐响起"
3. Translate ALL technical terms: "purge" → "清洗", "shake-up" → "大洗牌", "aircraft carrier" → "航空母舰"
4. Use natural, fluent Chinese - short and crisp sentences
5. No sensational or baity language - keep it factual and plain

Script to translate:
{text}

Remember: Your output must be 100% Chinese. No English words allowed."""
        
        try:
            response = requests.post(self.ollama_url, json={
                "model": "llama3.1:8b-large",
                "prompt": prompt,
                "stream": False
            })
            result = response.json()['response']
            
            # Post-processing: Remove common English phrases the LLM adds
            import re
            result = re.sub(r'Here is the translated script:?\s*', '', result, flags=re.IGNORECASE)
            result = re.sub(r'Here is the translation:?\s*', '', result, flags=re.IGNORECASE)
            
            # Replace common English words that slip through
            replacements = {
                'beneath': '在表面之下',
                'shake-up': '大洗牌',
                'purged': '清洗',
                'purge': '清洗',
                'geopolitics': '地缘政治',
                'geopolitical': '地缘政治'
            }
            for eng, chi in replacements.items():
                result = re.sub(eng, chi, result, flags=re.IGNORECASE)
            
            return result
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
                "model": "llama3.1:8b-large",
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
