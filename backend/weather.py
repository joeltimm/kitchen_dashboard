import os
import json
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from auth.credentials import load_master_credentials
import config
config.LOG_PATH
config.log_error("Something went wrong")

# Google Weather API or Maps API (using weather)
API_URL = 'https://maps.googleapis.com/maps/api/weather/data'  # Replace with actual API endpoint

# Scopes required by the Google API
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def get_weather(CITY):
    """
    Fetch weather data using Google API.
    """
    creds = load_master_credentials()
    headers = {
        'Authorization': f'Bearer {creds.token}'
    }

    # You can replace this with actual weather API endpoint logic, e.g., OpenWeather or Google Weather
    params = {'q': city, 'appid': 'YOUR_API_KEY'}  # Example for OpenWeather
    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return {
            'temperature': weather_data['main']['temp'],
            'condition': weather_data['weather'][0]['description']
        }
    else:
        return {"error": "Failed to retrieve weather data."}
