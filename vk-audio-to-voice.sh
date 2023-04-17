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

# Parse command-line arguments
if [ $# -eq 0 ]
then
    echo "Usage: $0 [--token <VK API token>] [--user <VK user ID or screen name>] <file>"
    exit 1
fi

while [ $# -gt 0 ]
do
    case "$1" in
        --token)
            TOKEN="$2"
            shift
            shift
            ;;
        --user)
            USER="$2"
            shift
            shift
            ;;
        *)
            FILE="$1"
            shift
            ;;
    esac
done

# Check if the file exists
if [ ! -f "$FILE" ]
then
    echo "The specified file '$FILE' does not exist."
    exit 1
fi

# Execute the Python script with the command-line arguments
python3 /usr/local/bin/vk-audio-to-voice.py --token "$TOKEN" --user "$USER" "$FILE"
