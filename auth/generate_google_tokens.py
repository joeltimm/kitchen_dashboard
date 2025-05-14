import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.helpers import session_from_client_secrets_file
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.helpers import session_from_client_secrets_file

CREDENTIALS_FILE = Path(__file__).parent / "google_credentials_joeltimm.json"

SERVICES = {
    "gmail": {
        "scopes": ["https://www.googleapis.com/auth/gmail.send"],
        "token_file": Path(__file__).parent / "gmail_token.json"
    },
    "calendar": {
        "scopes": ["https://www.googleapis.com/auth/calendar"],
        "token_file": Path(__file__).parent / "calendar_token_joeltimm.json"
    },
    "weather": {
        "scopes": ["https://www.googleapis.com/auth/cloud-platform"],
        "token_file": Path(__file__).parent / "weather_token.json"
    }
}

def authorize(service_name, scopes, token_path):
    print(f"🔐 Authorizing token for {service_name}...")
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), scopes)

    # Use the **local server workaround** (safe on headless)
    creds = flow.run_local_server(
        port=0,
        authorization_prompt_message="🔑 Visit this URL to authorize:\n{url}\n",
        success_message="✅ Auth complete. You can close this window.",
        open_browser=False
    )

    # Save token
    with open(token_path, "w") as f:
        f.write(creds.to_json())
    print(f"✅ Saved token: {token_path.name}")

if __name__ == "__main__":
    for name, cfg in SERVICES.items():
        authorize(name, cfg["scopes"], cfg["token_file"])
