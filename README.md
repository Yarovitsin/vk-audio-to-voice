## VK Audio Message Sender

This script allows you to send an audio file as a voice message to a VKontakte user or group.

### Installation

To install the script, first make sure you have Python 3.8 or higher installed on your system. Then, clone this repository and run the installation script:

```bash
git clone https://github.com/Yarovitsin/vk-audio-message-sender.git
cd vk-audio-to-voice
./install.sh
```

### Usage
1. Obtain a VK API access token from the VK API documentation.
2. Store the access token in a file named `token.txt` in the root directory of the repository or with the `--token` argument.
3. Run the script using the following command:
    
    ```bash
   python vk_voice_message_sender.py USER_ID_OR_SCREEN_NAME AUDIO_FILE
    ```
    
   Replace USER_ID_OR_SCREEN_NAME with the VK user ID or screen name of the recipient, and AUDIO_FILE with the path to the audio file you want to send.

    For example:
        
    ```bash
    python vk_voice_message_sender.py john_doe audio.ogg
    ```
4. The script will upload the audio file to VK's document storage, create a VK document from the file, and send a message with the document attached to the specified user.

Note: If you already have a VK API access token, you can store it in the token.txt file and skip step 1.
