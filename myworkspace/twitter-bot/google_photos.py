"""
Google Photos integration for downloading images
"""
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import requests

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

class GooglePhotosDownloader:
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Photos API"""
        creds = None
        token_file = 'token.pickle'
        
        # Load existing credentials
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    print("\n❌ ERROR: credentials.json not found!")
                    print("\nPlease follow these steps:")
                    print("1. Go to https://console.cloud.google.com/")
                    print("2. Enable Google Photos Library API")
                    print("3. Create OAuth credentials (Desktop app)")
                    print("4. Download and save as 'credentials.json'")
                    return None
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
        print("✓ Authenticated with Google Photos")
    
    def search_photos(self, keywords, max_results=10):
        """Search photos by keywords"""
        if not self.service:
            return []
        
        results = []
        for keyword in keywords:
            try:
                # Search in media items
                response = self.service.mediaItems().search(
                    body={
                        "pageSize": max_results,
                        "filters": {
                            "contentFilter": {
                                "includedContentCategories": ["LANDSCAPES", "CITYSCAPES", "LANDMARKS"]
                            }
                        }
                    }
                ).execute()
                
                items = response.get('mediaItems', [])
                if items:
                    results.extend(items[:max_results])
                    print(f"✓ Found {len(items)} photos for: {keyword}")
                else:
                    print(f"✗ No photos found for: {keyword}")
            
            except Exception as e:
                print(f"✗ Error searching for {keyword}: {e}")
        
        return results[:max_results]
    
    def download_photo(self, media_item, output_path):
        """Download a photo from Google Photos"""
        try:
            # Get download URL
            base_url = media_item['baseUrl']
            download_url = f"{base_url}=d"  # =d for download
            
            # Download image
            response = requests.get(download_url)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"✗ Failed to download: {response.status_code}")
                return False
        
        except Exception as e:
            print(f"✗ Error downloading: {e}")
            return False
