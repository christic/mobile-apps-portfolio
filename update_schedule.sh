#!/bin/bash

# Function to update app data
update_apps() {
    echo "Updating app data..."
    python3 update_apps.py
}

# Initial update
update_apps

# Schedule updates every 6 hours
while true; do
    sleep 21600  # 6 hours in seconds
    update_apps
done 