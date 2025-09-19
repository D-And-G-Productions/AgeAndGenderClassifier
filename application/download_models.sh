#!/bin/bash
# Exit script if any command fails
set -e

# --- Configuration ---
GDRIVE_LINK="https://drive.google.com/drive/folders/1v7tpyxxz8V6LyBE1-17CF6Zu01PxAZS2?usp=sharing"
OUTPUT_FILENAME="models.zip"
DESTINATION_FOLDER="."
# ---------------------

# Check if the destination folder exists and is not empty
if [ ! -d "$DESTINATION_FOLDER" ] || [ -z "$(ls -A "$DESTINATION_FOLDER")" ]; then
    echo "🟡 Destination folder not found or is empty. Downloading assets..."

    # Install dependencies
    pip install gdown
    apt-get update && apt-get install -y unzip --no-install-recommends && rm -rf /var/lib/apt/lists/*

    # Download the file from Google Drive
    gdown --output $OUTPUT_FILENAME "$GDRIVE_LINK"

    # Create destination folder and unzip
    mkdir -p $DESTINATION_FOLDER
    unzip $OUTPUT_FILENAME -d $DESTINATION_FOLDER

    # Clean up the downloaded zip file
    rm $OUTPUT_FILENAME

    echo "✅ Assets downloaded and extracted successfully."
else
    echo "✅ Assets already exist in '$DESTINATION_FOLDER'. Skipping download."
fi