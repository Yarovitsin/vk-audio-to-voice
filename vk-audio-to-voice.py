"""
    VK Audio Message Sender
    Copyright (C) 2023  Vanya Iarovitzine

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>."""

#!/usr/bin/env python3
import argparse
import os
import requests
import vk_api
from pathlib import Path
from typing import Tuple


TOKEN_FILE = 'token.txt'
UPLOAD_TYPE = 'audio_message'


def store_token(token: str) -> None:
    """Store the VK API token in a file."""
    mode = 'w' if Path(TOKEN_FILE).is_file() else 'x'
    with open(TOKEN_FILE, mode) as file:
        file.write(token)


def load_token() -> str:
    """Load the VK API token from a file."""
    if not Path(TOKEN_FILE).is_file():
        raise FileNotFoundError(f"Token file '{TOKEN_FILE}' not found")
    with open(TOKEN_FILE, 'r') as file:
        return file.read().strip()


def resolve_user_id(token: str, user_id: str) -> str:
    """Resolve a VK user ID from a screen name or handle."""
    if user_id.isdigit():
        return user_id

    if user_id.startswith('id') and user_id[2:].isdigit():
        return user_id[2:]

    if user_id.startswith('@'):
        user_id = user_id[1:]

    session = vk_api.VkApi(token=token)
    vk = session.get_api()
    try:
        user = vk.utils.resolveScreenName(screen_name=user_id)
        if not user:
            raise ValueError
        return user['object_id']
    except (vk_api.exceptions.ApiError, ValueError):
        raise argparse.ArgumentTypeError(f"User '{user_id}' not found")


def upload_file(token: str, file_path: str) -> dict:
    """Upload a file to VK's document storage."""
    with open(file_path, 'rb') as file:
        session = vk_api.VkApi(token=token)
        vk = session.get_api()
        upload_url = vk.docs.getUploadServer(type=UPLOAD_TYPE)
        upload_url = upload_url['upload_url'].replace('\\/', '/')  # fix VK's weird encoding
        response = requests.post(upload_url, files={"file": file})
        response.raise_for_status()
        return response.json()


def create_doc(token: str, file_path: str) -> Tuple[int, int]:
    """Create a VK document from a file."""
    upload_info = upload_file(token, file_path)
    if 'error' in upload_info:
        raise ValueError(f"Error uploading file: {upload_info['error']['error_msg']}")

    session = vk_api.VkApi(token=token)
    vk = session.get_api()
    try:
        doc = vk.docs.save(file=upload_info['file'], title=os.path.basename(file_path), tags=[UPLOAD_TYPE])
    except vk_api.exceptions.ApiError as e:
        raise ValueError(f"Error creating document: {e}")
    else:
        if not doc:
            raise ValueError("Error creating document: no document returned")
        return doc[0]['id'], doc[1]['owner_id']


def send_message(token: str, user_id: str, doc_id: Tuple[int, int]) -> None:
    """Send a VK message with a document attachment."""
    session = vk_api.VkApi(token=token)
    vk = session.get_api()
    try:
        vk.messages.send(user_id=user_id, attachment=f'doc{doc_id[1]}_{doc_id[0]}')
    except vk_api.exceptions.ApiError as e:
        raise ValueError(f"Error sending message: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='VK API token')
    parser.add_argument('user', help='User ID or screen name')
    parser.add_argument('file', help='Path to the file to send')
    args = parser.parse_args()

    if args.token:
        store_token(args.token)
    else:
        args.token = load_token()

    user_id = resolve_user_id(args.token, args.user)
    doc_id = create_doc(args.token, args.file)
    send_message(args.token, user_id, doc_id)
