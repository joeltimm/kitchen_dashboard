import json
import os
from config import LOG_PATH

CACHE_FILE = os.path.join(LOG_PATH, 'calendar_cache.json')

def save_cached_events(events):
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(events, f)
    except Exception as e:
        print(f"Cache write failed: {e}")

def load_cached_events():
    if not os.path.exists(CACHE_FILE):
        return []
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Cache read failed: {e}")
        return []
