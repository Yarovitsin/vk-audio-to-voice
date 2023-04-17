#!/bin/bash

# Change to the directory where your Python script is located
cd /usr/local/bin/

# Check if the Python executable is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3 before running this script."
    exit 1
fi

# Check if the required Python packages are installed
if ! python3 -c "import vk_api, requests" &> /dev/null
then
    echo "The required Python packages are not installed. Please install them by running 'pip install vk_api requests'."
    exit 1
fi

# Execute the Python script with the command-line arguments
python3 /usr/local/bin/vk-audio-to-voice.py --token "$TOKEN" --user "$USER" "$FILE"
