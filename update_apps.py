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
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading app data: {str(e)}")
    return {"apps": []}

def save_app_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving app data: {str(e)}")
        raise

def download_image(url, filename):
    try:
        # Ensure images directory exists
        os.makedirs(IMAGES_DIR, exist_ok=True)
        
        # Clean the URL
        url = url.replace('&amp;', '&')
        
        response = requests.get(url)
        if response.status_code == 200:
            image_path = os.path.join(IMAGES_DIR, f'{filename}.png')
            with open(image_path, 'wb') as f:
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
                'last_updated': datetime.datetime.now().isoformat(),
                # Additional App Store information
                'release_date': app.get('releaseDate'),
                'size': app.get('fileSizeBytes'),
                'minimum_os_version': app.get('minimumOsVersion'),
                'supported_devices': app.get('supportedDevices', []),
                'genres': app.get('genres', []),
                'price': app.get('price', 0),
                'currency': app.get('currency'),
                'seller_name': app.get('sellerName'),
                'bundle_id': app.get('bundleId'),
                'primary_genre': app.get('primaryGenreName'),
                'content_rating': app.get('contentAdvisoryRating'),
                'languages': app.get('languageCodesISO2A', []),
                'current_version_release_date': app.get('currentVersionReleaseDate'),
                'release_notes': app.get('releaseNotes'),
                'app_store_url': app.get('trackViewUrl')
            }
    except Exception as e:
        print(f"Error fetching app info for ID {app_id}: {str(e)}")
    return None

def update_app_data():
    try:
        data = load_app_data()
        updated = False
        
        # Download App Store badge
        app_store_badge_url = "https://tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-us?size=250x83&releaseDate=1276560000&h=7e7b68fad197e508f92cb1ecd82d8d23"
        if download_image(app_store_badge_url, 'app-store-badge'):
            print("Downloaded App Store badge")
        
        # App IDs from App Store
        apps_info = {
            '6741855207': {  # Zing Txt
                'name': 'Zing Txt',
                'filename': 'zing-txt'
            }
        }
        
        # Remove any duplicate entries
        seen_ids = set()
        data['apps'] = [app for app in data['apps'] if not (app['id'] in seen_ids or seen_ids.add(app['id']))]
        
        # Update or add apps
        for app_id, app_data in apps_info.items():
            print(f"\nUpdating {app_data['name']}...")
            app_info = get_app_info(app_id)
            
            if app_info:
                # Find existing app or create new one
                existing_app = next((app for app in data['apps'] if app['id'] == app_id), None)
                if existing_app:
                    app = existing_app
                else:
                    app = {
                        'id': app_id,
                        'name': app_data['name'],
                        'filename': app_data['filename']
                    }
                    data['apps'].append(app)
                
                # Update app information
                app.update(app_info)
                
                # Download new icon if needed
                if download_image(app_info['icon_url'], app['filename']):
                    print(f"Downloaded new icon for {app['name']}")
                
                updated = True
                print(f"Successfully updated {app['name']}")
            else:
                print(f"Failed to update {app_data['name']}")
        
        if updated:
            save_app_data(data)
            print("\nApp data updated successfully!")
        else:
            print("\nNo updates were made.")
    except Exception as e:
        print(f"Error in update_app_data: {str(e)}")
        raise

if __name__ == "__main__":
    update_app_data() 