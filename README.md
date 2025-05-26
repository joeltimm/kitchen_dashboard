# Kitchen Dashboard

## Project Description

The Kitchen Dashboard is a web-based interface designed to run on a dedicated display in a kitchen environment, such as a Raspberry Pi connected to a monitor. It provides a centralized view of useful information like calendar events, weather updates, and potentially photos. The dashboard is highly customizable, allowing users to drag, resize, and arrange widgets to suit their preferences. It is built with a Flask backend for data handling and a frontend utilizing standard web technologies with a drag-and-resize library.

## Features

*   **Customizable Layout:** Drag-and-resize widgets using GridStack.js or Interact.js.
*   **Calendar Integration:** Displays upcoming events from Google Calendar (with caching).
*   **Weather Information:** Shows current weather data.
*   **Photo Display (Planned):** Integration with OneDrive for displaying photos.
*   **Settings Management:** Configure calendar view, timezone, display schedule, and widget layout.
*   **Automated Operation:** Designed to launch automatically on boot and manage display on/off times.
*   **Daily Status Emails:** Sends a summary email with status and error information.
*   **Secure Credential Handling:** Credentials and secrets are stored in a dedicated, external directory.

## Technologies Used

*   **Backend:** Flask (Python)
*   **Frontend:** HTML, CSS, JavaScript
*   **Widget Interaction:** GridStack.js or Interact.js
*   **Data Storage:** SQLite or JSON (for layout and settings)
*   **APIs:** Google Calendar API, Weather APIs, OneDrive API (planned)
*   **System Integration:** systemd or .desktop files (for Raspberry Pi)
*   **Email:** smtplib and email (Python)

## Setup Instructions (Linux Server)

These instructions are for setting up the project on a Linux server for development.

1.  **Clone the Repository:**
```
bash
    git clone <repository_url> kitchen_dashboard
    cd kitchen_dashboard
    
```
2.  **Install Dependencies:**
    It's highly recommended to use a Python virtual environment.
```
bash
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv git
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
```
3.  **Set up Credentials:**
    Create the directory for credentials outside the main project directory (for security).
```
bash
    mkdir -p common/auth
    
```
Place your credential files (`google_token.json`, `onedrive_token.json`, `gmail_credentials.json`, `config.env`) inside the `kitchen_dashboard/common/auth` directory. The `config.env` file should contain necessary API keys, timezones, and other configuration details.

4.  **Run the Application:**
    You can run the Flask development server for testing.
```
bash
    source venv/bin/activate
    export FLASK_APP=backend/app.py
    flask run
    
```
The frontend will be accessible in your web browser at the address provided by the Flask development server (usually `http://127.0.0.1:5000`).

## Future Plans

*   **Migration to Raspberry Pi:** Transition the developed application from the Linux server to the target Raspberry Pi hardware. This will involve configuring auto-launch on boot using systemd or a `.desktop` file and setting up display control.
*   **Dockerization:** Containerize the application using Docker for easier deployment and management. This will involve creating a Dockerfile and potentially using Docker Compose.
*   **Refine Features:** Continue developing and refining the planned features, such as the photo display integration and advanced settings options.
*   **Improve UI/UX:** Enhance the user interface and user experience of the dashboard and settings pages.
*   **Add More Widgets:** Explore adding new types of widgets (e.g., news feeds, to-do lists).