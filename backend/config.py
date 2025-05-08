import os
from dotenv import load_dotenv

# Set paths
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
AUTH_PATH = os.path.join(APP_ROOT, 'common', 'auth')
LOG_PATH = os.path.join(os.path.dirname(__file__), 'logs')

# Load from kitchen_dashboard/.env
load_dotenv(os.path.join(APP_ROOT, '.env'))

def log_error(msg):
    os.makedirs(LOG_PATH, exist_ok=True)
    with open(os.path.join(LOG_PATH, 'error.log'), 'a') as f:
        f.write(f"[ERROR] {msg}\n")
