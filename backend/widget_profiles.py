from flask import Blueprint, request, jsonify
from pathlib import Path
import json

widget_api = Blueprint("widget_profiles", __name__)
PROFILE_FILE = Path(__file__).parent / "static_data" / "widget_profiles.json"

if not PROFILE_FILE.exists():
    PROFILE_FILE.write_text(json.dumps({}))


@widget_api.route("/api/widgets/settings", methods=["GET"])
def get_widget_settings():
    profile = request.args.get("profile", "default")
    try:
        data = json.loads(PROFILE_FILE.read_text())
        return jsonify(data.get(profile, {}))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@widget_api.route("/api/widgets/settings", methods=["POST"])
def save_widget_settings():
    body = request.json
    profile = body.get("profile", "default")
    settings = body.get("settings", {})  # Dict of widget configs
    try:
        all_profiles = json.loads(PROFILE_FILE.read_text())
        all_profiles[profile] = settings
        PROFILE_FILE.write_text(json.dumps(all_profiles, indent=2))
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
