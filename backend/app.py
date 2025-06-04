import os, sys
from encrypted_env_loader import load_encrypted_env
load_encrypted_env()

from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
from flask import Flask, jsonify
from calendar_widget import fetch_events, start_polling
from weather import get_weather
from onedrive_widget import get_next_image
from widget_profiles import widget_api
from flask import render_template

app = Flask(__name__)
app.register_blueprint(widget_api)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent # This is kitchen_dashboard/

# Define explicit paths for frontend folders
STATIC_FOLDER_PATH = PROJECT_ROOT / 'frontend' / 'static'
TEMPLATE_FOLDER_PATH = PROJECT_ROOT / 'frontend' / 'templates'

app = Flask(__name__,
            static_folder=str(STATIC_FOLDER_PATH),
            template_folder=str(TEMPLATE_FOLDER_PATH),
            static_url_path='/static') # This is the URL path for static files, usually '/static'

@app.route('/')
def home():
    return render_template('index.html') # Will look for index.html in frontend/templates/
    return 'Welcome to the Kitchen Dashboard!'

@app.route("/api/calendar")
def get_calendar():
    events = fetch_events()
    return jsonify(events)

@app.route('/api/weather')
def api_weather():
    weather_data = get_weather()  # Fetch local weather info
    return jsonify(weather_data)

@app.route("/api/onedrive/photo")
def serve_onedrive_photo():
    return get_next_image()

if __name__ == "__main__":
    start_polling()
    app.run(debug=True, host="0.0.0.0", port=5050)
