import os
import json
import logging
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
import msal

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

AUTH_DIR = Path(__file__).parent
TOKEN_PATH = AUTH_DIR / "onedrive_token.json"
ENCRYPTION_KEY = os.getenv("ONEDRIVE_TOKEN_ENCRYPTION_KEY")
CLIENT_SECRET_ENV = os.getenv("ONEDRIVE_CREDENTIALS_JSON")

def _get_fernet():
    if not ENCRYPTION_KEY:
        raise ValueError("Missing ONEDRIVE_TOKEN_ENCRYPTION_KEY environment variable.")
    return Fernet(ENCRYPTION_KEY.encode())

def _decrypt_token(data):
    return json.loads(_get_fernet().decrypt(data).decode())

def _encrypt_token(data):
    return _get_fernet().encrypt(json.dumps(data).encode())

def load_onedrive_credentials():
    if not CLIENT_SECRET_ENV:
        raise ValueError("Missing ONEDRIVE_CREDENTIALS_JSON environment variable.")

    creds = json.loads(CLIENT_SECRET_ENV)
    client_id = creds["client_id"]
    tenant_id = creds["tenant_id"]
    client_secret = creds["client_secret"]
    scopes = creds.get("scopes", ["https://graph.microsoft.com/.default"])
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    # Try decrypting existing token first
    if TOKEN_PATH.exists():
        try:
            token_data = _decrypt_token(TOKEN_PATH.read_bytes())
            if "access_token" in token_data:
                logger.info("🔐 Loaded OneDrive token from encrypted file.")
                return token_data["access_token"]
        except InvalidToken:
            logger.warning("⚠️ Token decryption failed — reauth required.")

    # Request new token with client credentials
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority
    )

    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" not in result:
        raise Exception(f"Failed to get OneDrive token: {result.get('error_description')}")

    TOKEN_PATH.write_bytes(_encrypt_token(result))
    logger.info("✅ New OneDrive token saved and encrypted.")
    return result["access_token"]
