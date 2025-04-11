import requests
import json
import os
import datetime
from pathlib import Path

# Configuration
DATA_FILE = 'app_data.json'
IMAGES_DIR = 'images'
os.makedirs(IMAGES_DIR, exist_ok=True)

def load_app_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"apps": []}

def save_app_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'{IMAGES_DIR}/{filename}.png', 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading image for {filename}: {str(e)}")
    return False

def get_app_info(app_id):
    url = f'https://itunes.apple.com/lookup?id={app_id}'
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['resultCount'] > 0:
            app = data['results'][0]
            return {
                'name': app['trackName'],
                'version': app['version'],
                'description': app['description'],
                'rating': app.get('averageUserRating', 0),
                'rating_count': app.get('userRatingCount', 0),
                'icon_url': app['artworkUrl512'],
                'screenshots': app.get('screenshotUrls', []),
                'last_updated': datetime.datetime.now().isoformat()
            }
    except Exception as e:
        print(f"Error fetching app info for ID {app_id}: {str(e)}")
    return None

def update_app_data():
    data = load_app_data()
    updated = False
    
    for app in data['apps']:
        print(f"\nUpdating {app['name']}...")
        app_info = get_app_info(app['id'])
        
        if app_info:
            # Update app information
            app['version'] = app_info['version']
            app['description'] = app_info['description']
            app['rating'] = app_info['rating']
            app['rating_count'] = app_info['rating_count']
            app['last_updated'] = app_info['last_updated']
            app['screenshots'] = app_info['screenshots']
            
            # Download new icon if needed
            if download_image(app_info['icon_url'], app['filename']):
                print(f"Downloaded new icon for {app['name']}")
            
            updated = True
            print(f"Successfully updated {app['name']}")
        else:
            print(f"Failed to update {app['name']}")
    
    if updated:
        save_app_data(data)
        print("\nApp data updated successfully!")
    else:
        print("\nNo updates were made.")

if __name__ == "__main__":
    update_app_data() 