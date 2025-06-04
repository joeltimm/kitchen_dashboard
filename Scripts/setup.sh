#!/bin/bash

# setup.sh - Script to set up the Kitchen Dashboard development environment
# This script is intended for setting up a local development environment.
# For Docker-based deployment, the Dockerfile will manage the container's environment.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Starting Kitchen Dashboard Setup ---"

# Define project root relative to the script location (one level up from 'scripts')
SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "${SCRIPTS_DIR}/.." &> /dev/null && pwd )"

echo "Project Root: ${PROJECT_ROOT}"
echo "Scripts Directory: ${SCRIPTS_DIR}"

# --- 1. Create Python Virtual Environment ---
VENV_DIR="${PROJECT_ROOT}/venv"
if [ ! -d "${VENV_DIR}" ]; then
    echo "Creating Python virtual environment in ${VENV_DIR}..."
    python3 -m venv "${VENV_DIR}"
    echo "Virtual environment created."
else
    echo "Virtual environment already exists at ${VENV_DIR}."
fi

# --- 2. Activate Virtual Environment and Install Dependencies ---
source "${VENV_DIR}/bin/activate"
echo "Activated virtual environment."

REQUIREMENTS_FILE="${PROJECT_ROOT}/requirements.txt"
if [ ! -f "${REQUIREMENTS_FILE}" ]; then
    echo "Creating initial requirements.txt with specified dependencies..."
    cat << EOF > "${REQUIREMENTS_FILE}"
Flask
python-dotenv
google-api-python-client
google-auth
google-auth-oauthlib
google-auth-httplib2
requests
schedule
APScheduler
msal
cryptography
gunicorn
EOF
    echo "Initial requirements.txt created at ${REQUIREMENTS_FILE}."
else
    echo "requirements.txt already exists at ${REQUIREMENTS_FILE}. Using existing file."
fi

echo "Installing/updating dependencies from ${REQUIREMENTS_FILE}..."
pip install -r "${REQUIREMENTS_FILE}"
echo "Dependencies installed."

deactivate
echo "Deactivated virtual environment for script context."

# --- 3. Ensure Essential Directories Exist ---
AUTH_DIR_ROOT="${PROJECT_ROOT}/auth"
SECRETS_DIR="${AUTH_DIR_ROOT}/secrets"

LOGS_DIR="${PROJECT_ROOT}/logs"
DATA_DIR="${PROJECT_ROOT}/data"
UTILS_DIR="${PROJECT_ROOT}/utils"

BACKEND_DIR="${PROJECT_ROOT}/backend"
FRONTEND_DIR="${PROJECT_ROOT}/frontend" # Frontend root
STATIC_DIR="${FRONTEND_DIR}/static"     # Static files in frontend/
TEMPLATES_DIR="${FRONTEND_DIR}/templates" # Templates in frontend/


echo "Creating essential directories..."
mkdir -p "${SECRETS_DIR}"
mkdir -p "${LOGS_DIR}"
mkdir -p "${DATA_DIR}"
mkdir -p "${BACKEND_DIR}"
mkdir -p "${FRONTEND_DIR}" # Ensure frontend directory exists
mkdir -p "${STATIC_DIR}"
mkdir -p "${TEMPLATES_DIR}"
mkdir -p "${UTILS_DIR}"
mkdir -p "${SCRIPTS_DIR}"

echo "Directory structure ensured/updated:"
echo "  ${SECRETS_DIR} (for sensitive credential/token files)"
echo "  ${LOGS_DIR}"
echo "  ${DATA_DIR}"
echo "  ${BACKEND_DIR}"
echo "  ${FRONTEND_DIR}"
echo "  ${STATIC_DIR} (in frontend/)"
echo "  ${TEMPLATES_DIR} (in frontend/)"
echo "  ${UTILS_DIR}"
echo "  ${SCRIPTS_DIR}"


# --- 4. Create/Update .gitignore ---
GITIGNORE_FILE="${PROJECT_ROOT}/.gitignore"
echo "Ensuring .gitignore is up to date..."
# (Content of .gitignore remains the same as previously provided - it's general)
cat << EOF > "${GITIGNORE_FILE}"
# Python virtual environment
venv/
__pycache__/
*.pyc
*.pyo
*.pyd

# IDE specific files
.idea/
.vscode/
*.swp
*.swo

# Secrets and sensitive data
auth/secrets/
# You might want to be more specific, e.g.:
# auth/secrets/*.json
# auth/secrets/token*.json
# auth/secrets/*_credentials.json
# auth/secrets/.env.encrypted # If you place an encrypted env here

# Unencrypted .env file (should always be ignored)
.env
*.env

# Log files
*.log
logs/

# Data files (if they contain sensitive or user-specific info)
# data/*.json # Decide if user-specific data should be ignored
# !data/default_layout.json # Allow a default if you create one
# !data/default_settings.json # Allow a default if you create one

# OS generated files
.DS_Store
Thumbs.db

# Build artifacts
dist/
build/
*.egg-info/
EOF
echo ".gitignore created/updated at ${GITIGNORE_FILE}."
echo "IMPORTANT: Manually review .gitignore to ensure it covers all your needs, especially for 'auth/secrets/' and 'data/'."


# --- 5. Create .env file if it doesn't exist ---
ENV_FILE="${PROJECT_ROOT}/.env"
if [ ! -f "${ENV_FILE}" ]; then
    echo "Creating .env file with example configurations at ${ENV_FILE}..."
    # (Content of .env remains largely the same, paths are generally relative to project root or absolute)
    cat << EOF > "${ENV_FILE}"
# --- General Settings (Flask app is in backend/app.py) ---
FLASK_APP=backend/app.py
FLASK_ENV=development
DEBUG=True # Set to False in production

# --- API Keys & Paths ---
# WEATHER_API_KEY=your_weather_api_key_here

# --- Paths to credential/token files (these will be used by your Python code) ---
# These paths are relative to the project root.
GOOGLE_CREDENTIALS_PATH=auth/secrets/google_client_secret.json
CALENDAR_TOKEN_PATH=auth/secrets/token_calendar.json
PHOTOS_TOKEN_PATH=auth/secrets/token_photos.json # Example
ONEDRIVE_TOKEN_PATH=auth/secrets/token_onedrive.json # Example
GMAIL_CREDENTIALS_PATH=auth/secrets/gmail_credentials.json # For emailer
GMAIL_TOKEN_PATH=auth/secrets/token_gmail.json # For emailer

# --- Paths for application data & logs (relative to project root) ---
LAYOUT_CONFIG_FILE=data/layout.json
SETTINGS_CONFIG_FILE=data/settings.json
LOG_FILE=logs/app.log

# --- Encrypted Environment File Loader (if used) ---
# ENCRYPTED_DOTENV_PATH=auth/secrets/.env.encrypted
# DOTENV_ENCRYPTION_KEY=your_secret_encryption_key_here # THIS SHOULD NOT BE IN .env, but passed as an actual ENV VAR
EOF
    echo ".env file created. Please review and add your configurations."
    echo "REMINDER: Do NOT commit .env if it contains sensitive data. Ensure it's in .gitignore."
else
    echo ".env file already exists at ${ENV_FILE}. Please ensure it's configured."
fi

# --- 6. Instructions for Credentials ---
# (Instructions remain the same as previously provided, emphasizing auth/secrets/)
echo ""
echo "--- Important Next Steps ---"
echo "1. Activate the virtual environment to work on the project:"
echo "   source ${VENV_DIR}/bin/activate"
echo ""
echo "2. Place your necessary credential JSON files in the '${SECRETS_DIR}' directory."
# ... (rest of instructions same as before) ...
echo ""
echo "--- Kitchen Dashboard Setup Complete ---"