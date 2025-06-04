# kitchen_dashboard/utils/google_utils.py

import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# --- Configuration ---
# Resolve project root: If this file is kitchen_dashboard/utils/google_utils.py
# then parent is 'utils', and parent.parent is 'kitchen_dashboard'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CLIENT_SECRETS_FILENAME = "google_client_secret.json" # General client secrets
SECRETS_DIR = PROJECT_ROOT / "auth" / "secrets"

# Ensure the secrets directory exists (though setup.sh should also do this)
SECRETS_DIR.mkdir(parents=True, exist_ok=True)

def _get_credentials_path(filename_in_secrets_dir):
    """Constructs the full path to a file in the auth/secrets directory."""
    return SECRETS_DIR / filename_in_secrets_dir

def load_google_creds(token_filename: str, client_secrets_filename: str, scopes: list):
    """
    Loads Google API credentials.
    Handles token refresh and initiates OAuth flow if needed.

    Args:
        token_filename (str): The name of the token file (e.g., "token_calendar.json").
        client_secrets_filename (str): The name of the client secrets JSON file
                                       (e.g., "google_client_secret.json").
        scopes (list): A list of strings representing the required OAuth scopes.

    Returns:
        google.oauth2.credentials.Credentials: Authenticated credentials object, or None.
    """
    creds = None
    token_path = _get_credentials_path(token_filename)
    client_secrets_path = _get_credentials_path(client_secrets_filename)

    if not client_secrets_path.exists():
        print(f"🔴 ERROR: Client secrets file not found at {client_secrets_path}")
        print("Please download your OAuth 2.0 client credentials from Google Cloud Console")
        print(f"and place it as '{client_secrets_filename}' in the '{SECRETS_DIR}' directory.")
        return None

    # Load existing token if available
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), scopes)
        except Exception as e:
            print(f"⚠️ Warning: Could not load token from {token_path}. Error: {e}")
            creds = None # Ensure creds is None if loading fails

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print(f"🔄 Refreshing token: {token_filename}")
                creds.refresh(Request())
            except Exception as e:
                print(f"🔴 ERROR: Failed to refresh token for {token_filename}. Error: {e}")
                # Fall through to re-authenticate if refresh fails
                creds = None # Force re-authentication
        else:
            # Initiate OAuth flow
            print(f"🚀 Initiating new OAuth flow for {token_filename} with scopes: {scopes}")
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets_path), scopes)
            # Try to run with a specific port to avoid conflicts if generating multiple tokens
            # You might need to adjust port numbers if running multiple flows simultaneously
            # For a dashboard usually run on a server, this might be done once manually.
            try:
                creds = flow.run_local_server(port=0) # port=0 finds a free port
            except OSError as e:
                if e.errno == 98: # Address already in use
                     print(f"🔴 ERROR: Port for OAuth flow is already in use. Try closing other apps or try again shortly.")
                     print(f"If running generate_google_tokens.py, ensure ports are unique per service.")
                else:
                     print(f"🔴 ERROR: Could not start local server for OAuth flow. {e}")
                return None
            except Exception as e:
                print(f"🔴 ERROR: An unexpected error occurred during the OAuth flow: {e}")
                return None


        # Save the credentials for the next run
        if creds:
            try:
                with open(token_path, "w") as token_file:
                    token_file.write(creds.to_json())
                print(f"✅ Token saved to {token_path}")
            except Exception as e:
                print(f"🔴 ERROR: Could not save token to {token_path}. Error: {e}")
        else:
            print(f"🔴 ERROR: Failed to obtain credentials for {token_filename}.")
            return None # Explicitly return None if creds are not obtained

    return creds

def build_google_service(api_name: str, api_version: str, scopes: list,
                         token_filename: str,
                         client_secrets_filename: str = DEFAULT_CLIENT_SECRETS_FILENAME):
    """
    Builds and returns an authenticated Google API service client.

    Args:
        api_name (str): Name of the API (e.g., "calendar", "gmail", "photoslibrary").
        api_version (str): Version of the API (e.g., "v3" for Calendar).
        scopes (list): List of OAuth scopes required by the API.
        token_filename (str): Filename for storing/retrieving the OAuth token
                              (e.g., "token_calendar.json").
        client_secrets_filename (str, optional): Filename of the client secrets JSON.
                                                 Defaults to DEFAULT_CLIENT_SECRETS_FILENAME.

    Returns:
        googleapiclient.discovery.Resource: Authenticated API service client, or None.
    """
    print(f"🛠️ Building Google service: {api_name} {api_version} using token '{token_filename}'")
    creds = load_google_creds(token_filename, client_secrets_filename, scopes)
    if not creds:
        print(f"🔴 ERROR: Could not get credentials for service {api_name} using token {token_filename}.")
        return None
    try:
        service = build(api_name, api_version, credentials=creds, static_discovery=False)
        print(f"✅ Successfully built service: {api_name} {api_version}")
        return service
    except Exception as e:
        print(f"🔴 ERROR: Failed to build service {api_name} {api_version}. Error: {e}")
        return None

# --- Example Usage (for testing this module directly) ---
if __name__ == "__main__":
    # Example: Building the Calendar service
    CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    CALENDAR_TOKEN_FILE = 'token_calendar_test.json' # Use a test token file
    # Assumes 'google_client_secret.json' is in 'auth/secrets/'

    print(f"Attempting to build Google Calendar service...")
    print(f"Make sure '{DEFAULT_CLIENT_SECRETS_FILENAME}' is in '{SECRETS_DIR}'")
    print(f"Token will be stored as '{CALENDAR_TOKEN_FILE}' in '{SECRETS_DIR}'")

    calendar_service = build_google_service(
        api_name='calendar',
        api_version='v3',
        scopes=CALENDAR_SCOPES,
        token_filename=CALENDAR_TOKEN_FILE
        # client_secrets_filename can be specified if different from default
    )

    if calendar_service:
        print("\nCalendar service built successfully. Now fetching calendar list...")
        try:
            calendar_list = calendar_service.calendarList().list().execute()
            print("Available calendars:")
            for calendar_list_entry in calendar_list.get('items', []):
                print(f"  - {calendar_list_entry.get('summary')} ({calendar_list_entry.get('id')})")
        except Exception as e:
            print(f"🔴 ERROR fetching calendar list: {e}")
    else:
        print("\nFailed to build Calendar service.")

    # You could add similar tests for Photos or other services here