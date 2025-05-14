import os
from pathlib import Path
from datetime import datetime

# Paths
APP_ROOT = Path(__file__).resolve().parent.parent
AUTH_PATH = APP_ROOT / 'auth'
LOG_PATH = APP_ROOT / 'backend' / 'logs'

# Load env vars
REQUIRED_VARS = ['TZ', 'FLASK_ENV', 'CITY']
missing = [var for var in REQUIRED_VARS if os.getenv(var) is None]
if missing:
    raise RuntimeError(f"Missing required env vars: {missing}")

# Error logger
def log_error(msg):
    os.makedirs(LOG_PATH, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_PATH / 'error.log', 'a') as f:
        f.write(f"[{timestamp}] [ERROR] {msg}\n")
