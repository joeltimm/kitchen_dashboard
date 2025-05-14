import datetime
import threading
import time
import os
from googleapiclient.discovery import build

from calendar_cache import save_cached_events, load_cached_events
from config import LOG_PATH, log_error
from auth.credentials import load_master_credentials

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
    try:
        service = get_calendar_service()
        if not service:
            return load_cached_events()

        now = datetime.datetime.utcnow().isoformat() + 'Z'
        result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=20,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = result.get('items', [])
        save_cached_events(events)
        return events
    except Exception as e:
        log_error(f"Calendar fetch error: {e}")
        return load_cached_events()

def start_polling():
    def poll_loop():
        while True:
            fetch_events()
            time.sleep(POLL_INTERVAL)
    threading.Thread(target=poll_loop, daemon=True).start()
