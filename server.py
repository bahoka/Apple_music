# server.py
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MATTERMOST_API = "https://your-mattermost-url/api/v4/users/me/status"
MM_TOKEN = os.environ.get("MM_TOKEN")  # Сохранишь в Railway

@app.route("/update-status", methods=["POST"])
def update_status():
    data = request.get_json()
    track = data.get("track", "🎵 Ничего не играет")

    headers = {
        "Authorization": f"Bearer {MM_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "status": "online",
        "custom_status": {
            "emoji": "🎵",
            "text": track[:64]  # ограничение в Mattermost
        }
    }

    resp = requests.put(MATTERMOST_API, headers=headers, json=payload)
    return jsonify({"ok": True, "mattermost_response": resp.status_code})
