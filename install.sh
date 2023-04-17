#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Set up the Bash script
chmod +x script.sh
sudo ln -s $(pwd)/vk-audio-to-voice.sh /usr/local/bin/vk-audio-to-voice

# Set up the Python script
sudo ln -s $(pwd)/vk-audio-to-voice.py /usr/local/bin/vk-audio-to-voice.py

echo "Installation complete. You can now run the script with 'script' or 'python3 script.py'."
