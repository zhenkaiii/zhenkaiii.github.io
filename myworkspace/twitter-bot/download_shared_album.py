#!/usr/bin/env python3
import requests
import re
import os
from urllib.parse import unquote

def download_from_shared_album(url, output_dir):
    """Download images from Google Photos shared album"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the album page
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to access album: {response.status_code}")
        return
    
    # Extract image URLs from the page
    content = response.text
    pattern = r'https://lh3\.googleusercontent\.com/[^"\'>\s]+'
    urls = re.findall(pattern, content)
    
    # Remove duplicates and filter
    urls = list(set(urls))
    image_urls = [u for u in urls if '=w' in u or '=h' in u]
    
    print(f"Found {len(image_urls)} images")
    
    for i, img_url in enumerate(image_urls, 1):
        # Modify URL to get full resolution
        img_url = re.sub(r'=w\d+-h\d+', '=w2000-h2000', img_url)
        
        try:
            img_response = requests.get(img_url, timeout=30)
            if img_response.status_code == 200:
                filename = f"image_{i:03d}.jpg"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                print(f"✓ Downloaded: {filename}")
            else:
                print(f"✗ Failed {i}: {img_response.status_code}")
        except Exception as e:
            print(f"✗ Error {i}: {e}")

if __name__ == "__main__":
    url = "https://photos.app.goo.gl/W3Lwr9WuYvUEmQ9m8"
    output_dir = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/images_asset"
    download_from_shared_album(url, output_dir)
