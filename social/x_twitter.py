"""
X (Twitter) posting via the X API v2.

Prerequisites:
  1. Register an app at https://developer.x.com/
  2. Get API key, API secret, access token, and access token secret.
  3. Enable media upload + tweet creation permissions.

Docs: https://docs.x.com/docs/x-api
"""

import requests
import tempfile
import os

from .base import SocialPlatform
from config.settings import (
    X_ACCESS_TOKEN,
    X_ACCESS_TOKEN_SECRET,
    X_API_KEY,
    X_API_SECRET,
)


class XPlatform(SocialPlatform):
    name = "x"
    UPLOAD_URL = "https://upload.x.com/i/media/upload.json"
    TWEET_URL = "https://api.x.com/2/tweets"

    def is_configured(self) -> bool:
        return bool(X_ACCESS_TOKEN)

    def post_video(
        self,
        video_path,
        title: str,
        description: str = "",
        tags: list[str] | None = None,
        privacy: str = "public",
    ) -> dict:
        if not self.is_configured():
            return {
                "success": False,
                "platform": self.name,
                "post_url": None,
                "post_id": None,
                "message": "X (Twitter) not configured. Set X_ACCESS_TOKEN in .env",
            }

        try:
            # For X API v2 with OAuth 1.0a, use requests-oauthlib
            try:
                from requests_oauthlib import OAuth1
            except ImportError:
                return {
                    "success": False,
                    "platform": self.name,
                    "post_url": None,
                    "post_id": None,
                    "message": "requests-oauthlib not installed. Run: pip install requests-oauthlib",
                }

            auth = OAuth1(
                X_API_KEY,
                X_API_SECRET,
                X_ACCESS_TOKEN,
                X_ACCESS_TOKEN_SECRET,
            )

            # Download video if it's a URL
            if isinstance(video_path, str) and video_path.startswith("http"):
                video_data = requests.get(video_path, timeout=120).content
                tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
                tmp.write(video_data)
                tmp.close()
                file_path = tmp.name
            else:
                file_path = str(video_path)

            # Step 1: INIT — register media upload
            import os as _os
            file_size = _os.path.getsize(file_path)

            resp = requests.post(
                self.UPLOAD_URL,
                params={"command": "INIT", "total_bytes": file_size, "media_type": "video/mp4"},
                auth=auth,
                timeout=30,
            )
            resp.raise_for_status()
            media_id = resp.json()["media_id_string"]

            # Step 2: APPEND — upload chunks (simplified: single chunk)
            with open(file_path, "rb") as f:
                resp = requests.post(
                    self.UPLOAD_URL,
                    params={"command": "APPEND", "media_id": media_id, "segment_index": 0},
                    files={"media": f},
                    auth=auth,
                    timeout=120,
                )
                resp.raise_for_status()

            # Step 3: FINALIZE
            resp = requests.post(
                self.UPLOAD_URL,
                params={"command": "FINALIZE", "media_id": media_id},
                auth=auth,
                timeout=30,
            )
            resp.raise_for_status()

            # Step 4: Create tweet with media
            text = title
            if tags:
                text += " " + " ".join(f"#{t.lstrip('#')}" for t in tags)

            resp = requests.post(
                self.TWEET_URL,
                auth=auth,
                json={
                    "text": text[:280],
                    "media": {"media_ids": [media_id]},
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            tweet_id = data["data"]["id"]

            return {
                "success": True,
                "platform": self.name,
                "post_url": f"https://x.com/i/web/status/{tweet_id}",
                "post_id": tweet_id,
                "message": "Video posted to X successfully",
            }
        except Exception as e:
            return {
                "success": False,
                "platform": self.name,
                "post_url": None,
                "post_id": None,
                "message": f"X upload failed: {e}",
            }
