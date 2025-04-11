# Mobile Apps Portfolio Website

This is a professional website showcasing a collection of mobile apps available on the App Store.

## Features

- Modern, responsive design
- Individual sections for each app
- App Store download links
- Support section
- Mobile-friendly layout
- Automatic updates from App Store

## Setup Instructions

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

2. Install Python dependencies:
```bash
python3 -m pip install requests
```

3. Run the update script to fetch app data:
```bash
python3 update_apps.py
```

4. View the website locally:
   - Open `index.html` in a web browser

## Automatic Updates

The website automatically updates app information every 6 hours. To start the update process:

```bash
chmod +x update_schedule.sh
./update_schedule.sh
```

## GitHub Pages Deployment

This website is configured for GitHub Pages deployment. To deploy:

1. Push your changes to the main branch
2. GitHub Pages will automatically deploy your site
3. Your site will be available at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME`

## Customization

- Colors can be modified in `styles.css`
- Content can be updated in `index.html`
- Images can be replaced in the `images` directory

## Requirements

- Modern web browser
- Python 3.x
- App screenshots (recommended size: 300x600 pixels) 