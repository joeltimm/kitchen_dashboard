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
# 'auth/' at root, then 'auth/secrets/'
AUTH_DIR_ROOT="${PROJECT_ROOT}/auth"
SECRETS_DIR="${AUTH_DIR_ROOT}/secrets" # New path for secrets

LOGS_DIR="${PROJECT_ROOT}/logs"
DATA_DIR="${PROJECT_ROOT}/data"
STATIC_DIR="${PROJECT_ROOT}/backend/static" # Standard for Flask if app is in backend/
TEMPLATES_DIR="${PROJECT_ROOT}/backend/templates" # Standard for Flask if app is in backend/
UTILS_DIR="${PROJECT_ROOT}/utils" # User will create this, but good to ensure

# Also ensure the 'backend' directory exists, as app.py is there
BACKEND_DIR="${PROJECT_ROOT}/backend"

echo "Creating essential directories..."
mkdir -p "${SECRETS_DIR}" # Creates auth/ and auth/secrets/
mkdir -p "${LOGS_DIR}"
mkdir -p "${DATA_DIR}"
mkdir -p "${BACKEND_DIR}" # Ensure backend directory exists
mkdir -p "${STATIC_DIR}" # Static files for Flask app in backend/
mkdir -p "${TEMPLATES_DIR}" # Templates for Flask app in backend/
mkdir -p "${UTILS_DIR}" # utils directory at project root
mkdir -p "${SCRIPTS_DIR}" # Ensure scripts dir in project root is acknowledged

echo "Directory structure ensured/updated:"
echo "  ${SECRETS_DIR} (for sensitive credential/token files)"
echo "  ${LOGS_DIR}"
echo "  ${DATA_DIR}"
echo "  ${BACKEND_DIR}"
echo "  ${STATIC_DIR}"
echo "  ${TEMPLATES_DIR}"
echo "  ${UTILS_DIR}"
echo "  ${SCRIPTS_DIR}"


# --- 4. Create/Update .gitignore ---
GITIGNORE_FILE="${PROJECT_ROOT}/.gitignore"
echo "Ensuring .gitignore is up to date..."

# Basic structure
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
ENV_FILE="${PROJECT_ROOT}/.env" # Main .env file for non-sensitive or dev-specific config
if [ ! -f "${ENV_FILE}" ]; then
    echo "Creating .env file with example configurations at ${ENV_FILE}..."
    cat << EOF > "${ENV_FILE}"
# --- General Settings (Flask app is in backend/app.py) ---
FLASK_APP=backend/app.py
FLASK_ENV=development
DEBUG=True # Set to False in production

# --- API Keys & Paths ---
# Option 1: Store actual keys/sensitive values in an encrypted file loaded by encrypted_env_loader.py
#           and point to credential files if needed.
# Option 2: For local development, you might temporarily put non-critical keys here.
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
# If encrypted_env_loader.py loads a specific encrypted .env file, specify its path here or in code.
# ENCRYPTED_DOTENV_PATH=auth/secrets/.env.encrypted
# DOTENV_ENCRYPTION_KEY=your_secret_encryption_key_here # THIS SHOULD NOT BE IN .env, but passed as an actual ENV VAR

EOF
    echo ".env file created. Please review and add your configurations."
    echo "REMINDER: Do NOT commit .env if it contains sensitive data. Ensure it's in .gitignore."
else
    echo ".env file already exists at ${ENV_FILE}. Please ensure it's configured according to the new auth/secrets/ path."
fi

# --- 6. Instructions for Credentials ---
echo ""
echo "--- Important Next Steps ---"
echo "1. Activate the virtual environment to work on the project:"
echo "   source ${VENV_DIR}/bin/activate"
echo ""
echo "2. Place your necessary credential JSON files in the '${SECRETS_DIR}' directory."
echo "   For example:"
echo "   - For Google services: Place your OAuth client secret JSON (e.g., 'google_client_secret.json' or 'calendar_credentials.json') in '${SECRETS_DIR}'."
echo "     Generated tokens (e.g., 'token_calendar.json') will also be stored here by your app."
echo "   - For Microsoft services (MSAL/OneDrive): Place necessary configuration/secret files in '${SECRETS_DIR}'."
echo "   - For Weather API Key: This can be stored in the .env file (if less sensitive and .env is gitignored) or managed via your encrypted_env_loader."
echo "   Ensure these files are NOT committed to Git (verify '.gitignore' has 'auth/secrets/')."
echo ""
echo "3. Review and update '${REQUIREMENTS_FILE}' if you have other specific package versions in mind."
echo "4. Review and update '${ENV_FILE}' with your specific configurations, API keys, and correct paths pointing to '${SECRETS_DIR}'."
echo "   If using 'encrypted_env_loader.py', ensure it's configured to load your encrypted secrets, and the actual encryption key is passed as an environment variable at runtime, not stored in version control."
echo ""
echo "--- Kitchen Dashboard Setup Complete ---"