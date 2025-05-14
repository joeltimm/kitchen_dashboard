import os
from cryptography.fernet import Fernet

key = os.getenv("DOTENV_ENCRYPTION_KEY")
if not key:
    raise RuntimeError("DOTENV_ENCRYPTION_KEY environment variable is not set")

fernet = Fernet(key.encode())

with open(".env", "rb") as f:
    encrypted = fernet.encrypt(f.read())

with open(".env.encrypted", "wb") as f:
    f.write(encrypted)

print("✅ .env encrypted and saved to .env.encrypted")
