import requests
import json
import os

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# App IDs and names
apps = {
    '6478002011': {
        'name': 'Tap & Tell Fun',
        'filename': 'tap-tell-fun',
        'description': 'A fun and interactive game that challenges your memory and reflexes.'
    },
    '6478002011': {
        'name': 'Phase 10 Score',
        'filename': 'phase-10-score',
        'description': 'Keep track of your Phase 10 game scores with this easy-to-use scoreboard.'
    },
    '6478002011': {
        'name': 'Sky Jo Score Board',
        'filename': 'sky-jo-score',
        'description': 'The perfect companion for your Sky Jo card game sessions.'
    },
    '6478002011': {
        'name': '500 Rummy Score Board',
        'filename': '500-rummy-score',
        'description': 'Track your 500 Rummy game scores with this intuitive scoreboard app.'
    },
    '6478002011': {
        'name': 'Zing Txt',
        'filename': 'zing-txt',
        'description': 'A fun and engaging text-based game that challenges your creativity and quick thinking.'
    }
}

def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'images/{filename}.png', 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")

def get_app_info(app_id):
    url = f'https://itunes.apple.com/lookup?id={app_id}'
    response = requests.get(url)
    data = json.loads(response.text)
    
    if data['resultCount'] > 0:
        app = data['results'][0]
        return {
            'icon_url': app['artworkUrl512'],
            'app_url': app['trackViewUrl'],
            'description': app['description'],
            'version': app['version'],
            'rating': app['averageUserRating'],
            'rating_count': app['userRatingCount']
        }
    return None

# Download images and get app info for each app
for app_id, app_data in apps.items():
    print(f"\nFetching info for {app_data['name']}...")
    app_info = get_app_info(app_id)
    
    if app_info:
        print(f"Found app info:")
        print(f"Version: {app_info['version']}")
        print(f"Rating: {app_info['rating']} ({app_info['rating_count']} ratings)")
        print(f"Description: {app_info['description'][:100]}...")
        
        # Download the app icon
        download_image(app_info['icon_url'], app_data['filename'])
    else:
        print(f"App {app_data['name']} not found")

print("\nAll downloads completed!") 