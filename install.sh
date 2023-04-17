#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Set up the Bash script
chmod +x vk-audio-to-voice.sh
sudo ln -s $(pwd)/vk-audio-to-voice.sh /usr/local/bin/vk-audio-to-voice

# Set up the Python script
sudo ln -s $(pwd)/vk-audio-to-voice.py /usr/local/bin/vk-audio-to-voice.py

echo "Installation complete. You can now run the script with 'vk-audio-to-voice' or 'vk-audio-to-voice.py'."
