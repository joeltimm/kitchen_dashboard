import os
import requests
import unittest
from unittest.mock import patch, MagicMock
import json
from pathlib import Path
from backend import onedrive_widget
from onedrive_widget.py import fetch_onedrive_images, get_next_image, CACHE_PATH
from auth.credentials import load_onedrive_credentials
from config import LOG_PATH, log_error

class OneDriveWidgetTest(unittest.TestCase):

    @patch("onedrive_widget.get_onedrive_token")
    @patch("requests.get")
    def test_fetch_onedrive_images_success(self, mock_get, mock_get_onedrive_token):
        # Mock the token retrieval
        mock_get_onedrive_token.return_value = "test_token"

        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "value": [
                {"name": "image1.jpg", "file": {"mimeType": "image/jpeg", "hashes": {"quickXorHash": "test_hash"}}, "@microsoft.graph.downloadUrl": "http://example.com/image1.jpg"},
                {"name": "image2.png", "file": {"mimeType": "image/png", "hashes": {"quickXorHash": "test_hash"}}, "@microsoft.graph.downloadUrl": "http://example.com/image2.png"},
            ]
        }
        mock_get.return_value = mock_response

        # Call the function
        image_links = fetch_onedrive_images()

        # Assertions
        self.assertEqual(len(image_links), 2)
        self.assertIn("http://example.com/image1.jpg", image_links)
        self.assertIn("http://example.com/image2.png", image_links)
        mock_get_onedrive_token.assert_called_once()
        mock_get.assert_called_once()

        # Clean up the cache file
        if CACHE_PATH.exists():
            CACHE_PATH.unlink()

    @patch("onedrive_widget.get_onedrive_token")
    @patch("requests.get")
    def test_fetch_onedrive_images_api_failure(self, mock_get, mock_get_onedrive_token):
        # Mock the token retrieval
        mock_get_onedrive_token.return_value = "test_token"

        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "API Error"
        mock_get.return_value = mock_response

        # Call the function
        image_links = fetch_onedrive_images()

        # Assertions
        self.assertEqual(len(image_links), 0)
        mock_get_onedrive_token.assert_called_once()
        mock_get.assert_called_once()

        # Clean up the cache file
        if CACHE_PATH.exists():
            CACHE_PATH.unlink()

    @patch("onedrive_widget.load_cached_images")
    def test_get_next_image_success(self, mock_load_cached_images):
        # Mock the cached images
        mock_load_cached_images.return_value = ["http://example.com/image1.jpg", "http://example.com/image2.png"]

        # Call the function
        response, status_code = get_next_image()
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertIn("image_url", data)
        self.assertIn(data["image_url"], ["http://example.com/image1.jpg", "http://example.com/image2.png"])
        mock_load_cached_images.assert_called_once()

        # Clean up the cache file
        if CACHE_PATH.exists():
            CACHE_PATH.unlink()

    @patch("onedrive_widget.load_cached_images")
    def test_get_next_image_no_images(self, mock_load_cached_images):
        # Mock the cached images
        mock_load_cached_images.return_value = []

        # Call the function
        response, status_code = get_next_image()
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(status_code, 404)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "No images found")
        mock_load_cached_images.assert_called_once()

        # Clean up the cache file
        if CACHE_PATH.exists():
            CACHE_PATH.unlink()

if __name__ == '__main__':
    unittest.main()