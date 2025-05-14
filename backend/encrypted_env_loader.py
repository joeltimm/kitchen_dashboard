# backend/encrypted_env_loader.py
import os
from pathlib import Path
from cryptography.fernet import Fernet

def load_encrypted_env():
    key = os.getenv("DOTENV_ENCRYPTION_KEY")
    if not key:
        raise RuntimeError("DOTENV_ENCRYPTION_KEY not set")
    #Find the file in the project root folder
    ROOT_DIR = Path(__file__).resolve().parent.parent
    encrypted_path = ROOT_DIR / ".env.encrypted"

    if not encrypted_path.exists():
        raise FileNotFoundError(f"No .env.encrypted found at {encrypted_path}")

    decrypted = Fernet(key.encode()).decrypt(encrypted_path.read_bytes()).decode()

    for line in decrypted.splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k, v = line.strip().split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

