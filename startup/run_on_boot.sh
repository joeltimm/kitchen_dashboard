#!/bin/bash
cd /joel/kitchen_dashboard
source venv/bin/activate
python3 backend/app.py &

# Wait for server
sleep 10

# Launch Chromium in kiosk
chromium-browser --noerrdialogs --kiosk http://localhost:5050
