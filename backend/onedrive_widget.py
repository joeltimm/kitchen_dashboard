# kitchen_dashboard/backend/onedrive_widget.py

import os
import time
import random
import json
import logging
from pathlib import Path
from flask import jsonify

from common.auth.onedrive_credentials import get_onedrive_token

import requests

logger = logging.getLogger(__name__)

# Cache path
CACHE_PATH = Path(__file__).resolve().parent / "../static_data/onedrive_images/image_cache.json"

# Folder ID or name on OneDrive
ONEDRIVE_FOLDER_NAME = "DashboardPhotos"

GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0/me/drive/root:/{}:/children"


def fetch_onedrive_images():
    """
    Retrieves image file metadata from the OneDrive folder and caches them.
    """
    token = get_onedrive_token()
    headers = {"Authorization": f"Bearer {token}"}
    folder_url = GRAPH_API_ENDPOINT.format(ONEDRIVE_FOLDER_NAME)

    response = requests.get(folder_url, headers=headers)
    if response.status_code != 200:
        logger.error(f"❌ OneDrive API failed: {response.text}")
        return []

    items = response.json().get("value", [])
    image_links = []

    for item in items:
        if "image" in item.get("file", {}):  # Ensures it's an image
            image_links.append(item["@microsoft.graph.downloadUrl"])

    # Cache it
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(image_links, f)

    return image_links


def load_cached_images():
    if not CACHE_PATH.exists():
        return fetch_onedrive_images()

    with open(CACHE_PATH) as f:
        return json.load(f)


_last_served = 0

def get_next_image():
    """
    Returns a random image from the cached list.
    """
    images = load_cached_images()
    if not images:
        return jsonify({"error": "No images found"}), 404

    return jsonify({"image_url": random.choice(images)})