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
            # Download app icon
            icon_url = zing_txt_info['icon_url']
            download_image(icon_url, "zing-txt.png")
            
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

        # Update scoring apps with manual data
        scoring_apps = [
            {
                "id": "6478002012",
                "name": "500 Rummy Score",
                "filename": "500-rummy-score",
                "version": "1.0",
                "description": "Keep track of your 500 Rummy card game scores with this simple and elegant scoring app. Perfect for family game nights and friendly competitions!\n\nFeatures:\n\u2022 Easy score tracking for multiple players\n\u2022 Running total calculation\n\u2022 Clean, intuitive interface\n\u2022 Save and resume games\n\u2022 Game history\n\u2022 No ads or in-app purchases",
                "rating": 5,
                "rating_count": 3,
                "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/fe/97/34/fe9734a0-4b9a-9575-e8ce-dbc636d62c54/AppIcon-0-0-1x_U007ephone-0-1-85-220.png/512x512bb.jpg",
                "screenshots": [],
                "last_updated": "2023-01-15T00:00:00Z",
                "release_date": "2023-01-15T00:00:00Z",
                "size": "2.5 MB",
                "minimum_os_version": "iOS 13.0",
                "price": 0,
                "currency": "USD",
                "seller_name": "Clarence Christ",
                "bundle_id": "com.christic.500RummyScore",
                "primary_genre": "Games",
                "content_rating": "4+",
                "languages": ["English"],
                "app_store_url": "https://apps.apple.com/app/500-rummy-score/id6478002012"
            },
            {
                "id": "6478002013",
                "name": "Phase 10 Score",
                "filename": "phase-10-score",
                "version": "1.1",
                "description": "The perfect companion app for Phase 10 card game enthusiasts! Keep track of phases completed and scores for all players with this user-friendly scoring app.\n\nFeatures:\n\u2022 Track phases completed for each player\n\u2022 Automatic score calculation\n\u2022 Support for multiple players\n\u2022 Phase reference guide included\n\u2022 Save games in progress\n\u2022 Dark mode support\n\u2022 No ads or in-app purchases",
                "rating": 4.8,
                "rating_count": 5,
                "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/fe/97/34/fe9734a0-4b9a-9575-e8ce-dbc636d62c54/AppIcon-0-0-1x_U007ephone-0-1-85-220.png/512x512bb.jpg",
                "screenshots": [],
                "last_updated": "2023-02-01T00:00:00Z",
                "release_date": "2023-02-01T00:00:00Z",
                "size": "2.8 MB",
                "minimum_os_version": "iOS 13.0",
                "price": 0,
                "currency": "USD",
                "seller_name": "Clarence Christ",
                "bundle_id": "com.christic.Phase10Score",
                "primary_genre": "Games",
                "content_rating": "4+",
                "languages": ["English"],
                "app_store_url": "https://apps.apple.com/app/phase-10-score/id6478002013"
            },
            {
                "id": "6478002014",
                "name": "Sky-Jo Score",
                "filename": "sky-jo-score",
                "version": "1.0",
                "description": "Keep score of your Sky-Jo card game matches with this clean and simple scoring app. Perfect for families and friends who love this exciting card game!\n\nFeatures:\n\u2022 Easy score input for multiple players\n\u2022 Automatic total calculation\n\u2022 Round-by-round scoring\n\u2022 Game history\n\u2022 Simple, intuitive interface\n\u2022 No ads or in-app purchases",
                "rating": 5,
                "rating_count": 2,
                "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/fe/97/34/fe9734a0-4b9a-9575-e8ce-dbc636d62c54/AppIcon-0-0-1x_U007ephone-0-1-85-220.png/512x512bb.jpg",
                "screenshots": [],
                "last_updated": "2023-03-15T00:00:00Z",
                "release_date": "2023-03-15T00:00:00Z",
                "size": "2.6 MB",
                "minimum_os_version": "iOS 13.0",
                "price": 0,
                "currency": "USD",
                "seller_name": "Clarence Christ",
                "bundle_id": "com.christic.SkyJoScore",
                "primary_genre": "Games",
                "content_rating": "4+",
                "languages": ["English"],
                "app_store_url": "https://apps.apple.com/app/sky-jo-score/id6478002014"
            }
        ]

        # Update or add scoring apps
        for app in scoring_apps:
            # Download app icon
            icon_url = app['icon_url']
            filename = f"{app['filename']}.png"
            download_image(icon_url, filename)
            
            # Update icon_url to use local path
            app['icon_url'] = f"images/{filename}"
            
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