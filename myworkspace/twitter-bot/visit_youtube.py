#!/usr/bin/env python3
"""
Visit YouTube URL with browser automation at random intervals (2-5 minutes)
Usage: python3 visit_youtube.py
Press Ctrl+C to stop

Requirements:
    pip install selenium
    brew install chromedriver
"""

import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.youtube.com/watch?v=etnNpFTEd6Q"

def create_driver():
    """Create Chrome driver with options"""
    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")  # Mute audio
    chrome_options.add_argument("--window-size=1280,720")
    # Remove headless mode so video actually plays
    # chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def visit_video(driver):
    """Visit YouTube video and let it play for 30 seconds"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Opening video...")
        
        driver.get(URL)
        
        # Wait for video player to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "movie_player"))
        )
        
        # Wait a bit for video to start
        time.sleep(3)
        
        # Try to click play if paused
        try:
            driver.execute_script("""
                var video = document.querySelector('video');
                if (video && video.paused) {
                    video.play();
                }
            """)
        except:
            pass
        
        # Let video play for 30 seconds
        print(f"[{timestamp}] Playing video for 30 seconds...")
        time.sleep(30)
        
        print(f"[{timestamp}] ✓ Visit complete")
        return True
        
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Error: {e}")
        return False

def main():
    print(f"Starting periodic YouTube visits: {URL}")
    print("Press Ctrl+C to stop\n")
    
    driver = create_driver()
    
    try:
        while True:
            visit_video(driver)
            
            # Random interval between 2-5 minutes (120-300 seconds)
            interval = random.randint(120, 300)
            next_visit = datetime.now().timestamp() + interval
            next_visit_time = datetime.fromtimestamp(next_visit).strftime("%H:%M:%S")
            
            print(f"Next visit in {interval//60} min {interval%60} sec (at {next_visit_time})\n")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    finally:
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    main()
