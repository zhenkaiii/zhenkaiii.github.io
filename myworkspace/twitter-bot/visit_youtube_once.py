#!/usr/bin/env python3
"""
Single YouTube visit with browser automation
Run this via GitHub Actions or cron
"""

import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.youtube.com/watch?v=etnNpFTEd6Q"

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Use system chromedriver if available
    chromedriver_path = os.environ.get('CHROMEDRIVER_PATH', '/usr/bin/chromedriver')
    if os.path.exists(chromedriver_path):
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        driver = webdriver.Chrome(options=chrome_options)
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Opening video: {URL}")
        
        driver.get(URL)
        
        # Wait for video player
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "movie_player"))
        )
        
        print(f"[{timestamp}] Video loaded, waiting 3 seconds...")
        time.sleep(3)
        
        # Try to play video
        try:
            driver.execute_script("""
                var video = document.querySelector('video');
                if (video) {
                    video.play();
                    console.log('Video playing');
                }
            """)
        except Exception as e:
            print(f"Could not start video: {e}")
        
        # Let video play for 30 seconds
        print(f"[{timestamp}] Playing video for 30 seconds...")
        time.sleep(30)
        
        print(f"[{timestamp}] ✓ Visit complete")
        return True
        
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ✗ Error: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
