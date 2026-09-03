"""
Utility functions: download videos, manage local storage, history.
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
from config.settings import STORAGE_DIR

HISTORY_FILE = STORAGE_DIR / "history.json"


def download_video(url: str, filename: str | None = None) -> str:
    """Download a video from a URL to local storage. Returns local path."""
    if not filename:
        filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

    path = STORAGE_DIR / filename
    resp = requests.get(url, stream=True, timeout=300)
    resp.raise_for_status()
    with open(path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return str(path)


def save_to_history(entry: dict):
    """Append an entry to the history JSON file."""
    history = []
    if HISTORY_FILE.exists():
        try:
            history = json.loads(HISTORY_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            history = []
    history.insert(0, entry)
    # Keep last 100 entries
    history = history[:100]
    HISTORY_FILE.write_text(json.dumps(history, indent=2, default=str))


def get_history() -> list[dict]:
    """Return the history list."""
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text())
    except (json.JSONDecodeError, IOError):
        return []


def clear_history():
    """Delete the history file."""
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
