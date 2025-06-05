import datetime
import threading
import time
import os
from googleapiclient.discovery import build

from calendar_cache import save_cached_events, load_cached_events
from config import LOG_PATH, log_error
from auth.credentials import load_master_credentials

# --- Configuration for Calendar API ---
# These could also come from environment variables via os.getenv() if preferred
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_TOKEN_FILENAME = 'token_calendar.json' # Will be stored in auth/secrets/
# Assumes 'google_client_secret.json' is used by default by build_google_service
# Global variable for the service to cache it, or initialize it on first call
calendar_service_instance = None

CACHE_FILE = os.path.join(LOG_PATH, 'calendar_cache.json')
POLL_INTERVAL = 300  # seconds

def get_calendar_service():
    try:
        creds = load_master_credentials_joeltimm()
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        log_error(f"Calendar service init failed: {e}")
        return None

def fetch_events():
    """Fetches upcoming events from the primary Google Calendar."""
    service = get_calendar_service()
    if not service:
        return {"error": "Failed to connect to Google Calendar service."}

    try:
        now_utc = datetime.now(timezone.utc)
        time_min = now_utc.isoformat()
        # Fetch events for the next 7 days, for example
        time_max = (now_utc + timedelta(days=7)).isoformat()

        print(f"Fetching events from {time_min} to {time_max}")
        events_result = service.events().list(
            calendarId='primary',  # Use 'primary' for the user's main calendar
            timeMin=time_min,
            timeMax=time_max,
            maxResults=10,        # Adjust as needed
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        formatted_events = []
        if not events:
            print("No upcoming events found.")
            return {"events": [], "message": "No upcoming events."}

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            formatted_events.append({
                'summary': event.get('summary', 'No Title'),
                'start': start,
                'end': event['end'].get('dateTime', event['end'].get('date')),
                'id': event['id']
            })
        print(f"Fetched {len(formatted_events)} events.")
        return {"events": formatted_events}

    except Exception as e:
        print(f"🔴 An error occurred fetching calendar events: {e}")
        # Consider more specific error handling or re-raising
        return {"error": f"An error occurred: {str(e)}"}

def start_polling():
    # TODO: Implement actual background polling using APScheduler if needed
    # For now, this is called once at startup in your app.py
    print("Calendar polling placeholder initiated. (Actual polling not yet implemented here)")
    # You might want to fetch initial events here if not relying on an immediate API call
    # fetch_events() # Or call this from app.py after starting

if __name__ == '__main__':
    # Test fetching events directly (requires auth setup)
    print("Testing calendar_widget.py directly...")
    # Ensure google_client_secret.json is in ../auth/secrets/ from this file's perspective
    # Or adjust paths if running this directly and paths in google_utils assume project root
    
    # For direct testing, you might need to adjust how PROJECT_ROOT is found
    # or temporarily add backend to sys.path if utils is not found
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent)) # Add project root
    
    test_events = fetch_events()
    print("\nTest fetch_events result:")
    import json
    print(json.dumps(test_events, indent=2))
