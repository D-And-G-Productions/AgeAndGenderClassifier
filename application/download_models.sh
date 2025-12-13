#!/bin/bash
set -e

# --- Configuration ---
# Ensure this link points to a correctly zipped, non-empty file
GDRIVE_LINK="https://drive.google.com/uc?export=download&id=1Zm8nVGKZ2cSF6LiX045LGyjuI0muyJWk"
OUTPUT_FILENAME="models.zip"
DESTINATION_FOLDER="."
# ---------------------

EXPECTED_FILE="$DESTINATION_FOLDER/models/custom_model/2/fingerprint.pb"

if [ ! -e "$EXPECTED_FILE" ]; then
    echo "🟡 Expected file not found. Downloading assets..."

    # Use gdown, as it's designed to handle Google Drive's download flow
    pip install --upgrade gdown
    apt-get update && apt-get install -y unzip --no-install-recommends && rm -rf /var/lib/apt/lists/*

    # gdown will correctly handle the download confirmation
    gdown "$GDRIVE_LINK" -O "$OUTPUT_FILENAME"
    
    unzip $OUTPUT_FILENAME -d $DESTINATION_FOLDER
    rm $OUTPUT_FILENAME

    echo "✅ Assets downloaded and extracted successfully."
else
    echo "✅ Assets already exist. Skipping download."
fi