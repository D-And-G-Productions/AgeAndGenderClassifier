#!/bin/bash
set -e # Exit immediately if a command fails

# --- Step 1: Dependency Validation ---
echo "--- Step 1: Checking for required dependencies... ---"

# Check for Docker
if ! command -v docker &> /dev/null
then
    echo "❌ Error: Docker is not installed or not in your PATH."
    echo "   Please install Docker before running this script."
    exit 1
fi

# Check for pip
if ! command -v pip &> /dev/null
then
    echo "❌ Error: pip is not installed or not in your PATH."
    echo "   pip is required to run 'pip install gdown' in the download script."
    echo "   Please install pip for Python 3 to continue."
    exit 1
fi

echo "✅ All dependencies are installed."

# --- Step 2: Prepare Models ---
echo "--- Step 2: Preparing models... ---"
sh ./download_models.sh

# --- Step 3: Build and Run Application ---
echo "--- Step 3: Building and running application... ---"
docker-compose up --build -d

echo "--- Done. Application is running. ---"