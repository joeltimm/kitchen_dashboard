from flask import Flask, jsonify
from calendar_widget import fetch_events, start_polling
from weather import get_weather
from onedrive_widget import get_next_image
from widget_profiles import widget_api
app.register_blueprint(widget_api)


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

@app.route("/api/onedrive/photo")
def serve_onedrive_photo():
    return get_next_image()

if __name__ == "__main__":
    start_polling()
    app.run(debug=True, host="0.0.0.0", port=5050)
