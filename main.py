import os
import subprocess
import requests
from time import sleep
from dotenv import load_dotenv

load_dotenv()

def get_current_song():
    try:
        output = subprocess.check_output([
            "osascript",
            "-e",
            'tell application "Music" to get name of current track & " – " & artist of current track'
        ])
        return output.decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return None

def update_mattermost_status(song):
    import json
    url = os.getenv("MM_URL") + "/api/v4/users/me/status/custom"
    token = os.getenv("MM_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "custom_status": {
            "emoji": "🎵",
            "text": f"Now Playing: {song}",
            "duration": "dont_clear"  # или "today", "one_hour", "thirty_minutes"
        }
    }

    # DEBUG: покажем, что отправляем
    print("[DEBUG] Payload:", json.dumps(payload, indent=2))

    r = requests.put(url, json=payload, headers=headers)
    print(f"[Status] {r.status_code} - {r.text}")

def main_loop():
    last_song = ""
    while True:
        song = get_current_song()
        if song and song != last_song:
            print(f"[Now Playing] {song}")
            update_mattermost_status(song)  # <--- исправлено
            last_song = song
        sleep(60)

if __name__ == "__main__":
    main_loop()
