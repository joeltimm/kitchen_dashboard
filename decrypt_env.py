##To use it - copy my back back into the projet - command from kitchen_dashboard: "cp ~/secrets/.env.encrypted.bak .env.encrypted"
##Then run this script - command: "python3 decrypt_env.py"
## .env will be restored to the current folder 

import os
from cryptography.fernet import Fernet

key = os.getenv("DOTENV_ENCRYPTION_KEY")
if not key:
    raise RuntimeError("DOTENV_ENCRYPTION_KEY environment variable is not set")

fernet = Fernet(key.encode())

with open(".env.encrypted", "rb") as f:
    decrypted = fernet.decrypt(f.read())

with open(".env", "wb") as f:
    f.write(decrypted)

print("✅ .env successfully decrypted.")

os.remove("/home/joel/kitchen_dashboard/.env")
print("🧹 Cleaned up decrypted .env file.")