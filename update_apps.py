import requests
import json
import os
import datetime
from pathlib import Path
from urllib.parse import urlparse

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
    """Download an image from a URL and save it to the images directory."""
    try:
        # Clean the URL
        url = url.strip()
        if not url:
            print(f'Empty URL for {filename}')
            return False

        # Create images directory if it doesn't exist
        os.makedirs(IMAGES_DIR, exist_ok=True)

        # Check if image already exists and is valid
        filepath = os.path.join(IMAGES_DIR, filename)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:  # Check if file exists and is not empty
            print(f'Using existing image for {filename}')
            return True

        # Download the image
        print(f'Downloading {filename}...')
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Save the image
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Successfully downloaded {filename}')
        return True
    except Exception as e:
        print(f'Error downloading {filename}: {str(e)}')
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
    """Update the app data file with the latest information."""
    try:
        # Read existing data
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = {"apps": []}

        # Download App Store badge
        app_store_badge_url = "https://tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-us?size=250x83&amp;releaseDate=1276560000&h=7e6b68fad15e08c33384f7bbcc0e429c"
        download_image(app_store_badge_url, "app-store-badge.png")

        # Update Zing Txt
        zing_txt_info = get_app_info("6741855207")
        if zing_txt_info:
            zing_txt = {
                "id": "6741855207",
                "name": "Zing Txt",
                "filename": "zing-txt",
                **zing_txt_info
            }
            # Update or add Zing Txt
            existing_apps = [app for app in data["apps"] if app["id"] == zing_txt["id"]]
            if existing_apps:
                data["apps"][data["apps"].index(existing_apps[0])] = zing_txt
            else:
                data["apps"].append(zing_txt)

        # Update scoring apps
        scoring_app_ids = ["6478002012", "6478002013", "6478002014"]
        for app_id in scoring_app_ids:
            app_info = get_app_info(app_id)
            if app_info:
                app = {
                    "id": app_id,
                    "name": app_info["name"],
                    "filename": app_info["name"].lower().replace(" ", "-"),
                    **app_info
                }
                # Update or add app
                existing_apps = [a for a in data["apps"] if a["id"] == app["id"]]
                if existing_apps:
                    data["apps"][data["apps"].index(existing_apps[0])] = app
                else:
                    data["apps"].append(app)

        # Save updated data
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print("App data updated successfully!")

    except Exception as e:
        print(f"Error updating app data: {str(e)}")

if __name__ == "__main__":
    update_app_data() 