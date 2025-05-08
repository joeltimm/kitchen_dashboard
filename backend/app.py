from flask import Flask, jsonify
from calendar_widget import fetch_events, start_polling
from weather import get_weather
# STILL NEED TO BUILD from backend.photos import fetch_photos

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the Kitchen Dashboard!'

@app.route("/api/calendar")
def get_calendar():
    events = fetch_events()
    return jsonify(events)

@app.route('/api/weather')
def api_weather():
    weather_data = get_weather()  # Fetch local weather info
    return jsonify(weather_data)

##@app.route('/api/photos')
##NEEDS BUILDINGdef api_photos():
    ##photos = fetch_photos()  # Fetch photos from OneDrive
    ##return jsonify(photos)

if __name__ == "__main__":
    start_polling()
    app.run(debug=True, host="0.0.0.0", port=5050)
