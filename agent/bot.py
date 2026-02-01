import tweepy
import time
import sqlite3
import json
import requests
from datetime import datetime, timedelta
from config import *

class TwitterBot:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.twitter = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET,
            bearer_token=TWITTER_BEARER_TOKEN
        )
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database to track posted content"""
        conn = sqlite3.connect('bot_history.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS posts
                     (id INTEGER PRIMARY KEY, tweet TEXT, topics TEXT, timestamp TEXT)''')
        conn.commit()
        conn.close()
    
    def get_trends(self):
        """Fetch trending topics from The Economist"""
        import requests
        from bs4 import BeautifulSoup
        try:
            response = requests.get('https://www.economist.com/', headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            
            trends = []
            # Get article headlines
            for article in soup.find_all(['h2', 'h3'], limit=20):
                title = article.get_text(strip=True)
                if title and len(title) > 20:
                    trends.append(title)
                if len(trends) >= 5:
                    break
            
            return trends if trends else ["Global economic trends", "Market developments", "Policy changes"]
        except Exception as e:
            print(f"Error fetching trends: {e}")
            return ["Global economic trends", "Market developments", "Policy changes"]
    
    def generate_tweet(self, trends):
        """Generate original commentary using Ollama"""
        trend_context = "\n".join([f"- {t[:100]}" for t in trends])
        
        prompt = f"""You are a balanced economic commentator. 

Current headlines:
{trend_context}

Write ONE short observation or insight about these topics.
Be neutral and factual. Max 200 characters. No hashtags."""
        
        try:
            response = requests.post(self.ollama_url, json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            })
            result = response.json()
            return result['response'].strip().strip('"')[:280]
        except Exception as e:
            print(f"Error generating tweet: {e}")
            return None
    
    def review_tweet(self, tweet):
        """Self-review before posting"""
        try:
            response = requests.post(self.ollama_url, json={
                "model": "llama3.1:8b",
                "prompt": f"""Review this tweet: "{tweet}"

Check: 1) Is it thoughtful commentary (not spam)? 2) Appropriate tone? 3) Under 280 chars?
Reply: APPROVE or REJECT with brief reason.""",
                "stream": False
            })
            result = response.json()
            review_text = result['response']
            return "APPROVE" in review_text.upper(), review_text
        except Exception as e:
            print(f"Error reviewing tweet: {e}")
            return False, str(e)
    
    def post_tweet(self, content, topics):
        """Display tweet for manual posting"""
        print("\n" + "="*60)
        print("📝 TWEET READY TO POST:")
        print("="*60)
        print(content)
        print("="*60)
        print(f"Characters: {len(content)}/280")
        print("\nCopy and paste this to Twitter manually.")
        print("="*60 + "\n")
        
        # Log to database
        conn = sqlite3.connect('bot_history.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (tweet, topics, timestamp) VALUES (?, ?, ?)",
                 (content, topics, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        return True
    
    def run_cycle(self):
        """Run one complete cycle"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting cycle...")
        
        # Get trends
        trends = self.get_trends()
        if not trends:
            print("No trends found, skipping cycle")
            return
        
        print(f"Found {len(trends)} trending topics")
        
        # Generate tweet
        tweet = self.generate_tweet(trends)
        if not tweet:
            print("Failed to generate tweet")
            return
        
        print(f"Generated: {tweet}")
        
        # Review
        approved, review = self.review_tweet(tweet)
        print(f"Review: {review}")
        
        if approved:
            # Post
            topics = "economics"
            self.post_tweet(tweet, topics)
        else:
            print("Tweet rejected by review")
    
    def start(self):
        """Start the bot loop"""
        print("🤖 Twitter Bot Started")
        print(f"Domain: {', '.join(DOMAIN_KEYWORDS)}")
        print(f"Interval: Every {POST_INTERVAL_HOURS} hours\n")
        
        while True:
            try:
                self.run_cycle()
            except Exception as e:
                print(f"Error in cycle: {e}")
            
            print(f"Sleeping for {POST_INTERVAL_HOURS} hours...")
            time.sleep(POST_INTERVAL_HOURS * 3600)

if __name__ == "__main__":
    bot = TwitterBot()
    bot.start()
