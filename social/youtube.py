"""
YouTube Shorts posting via the YouTube Data API v3.

Prerequisites:
  1. Google Cloud project with YouTube Data API v3 enabled.
  2. OAuth 2.0 credentials (client ID + secret).
  3. Obtain access + refresh tokens via the OAuth flow.

Docs: https://developers.google.com/youtube/v3/docs/videos/insert
"""

import os
import requests

from .base import SocialPlatform
from config.settings import (
    YOUTUBE_ACCESS_TOKEN,
    YOUTUBE_CLIENT_ID,
    YOUTUBE_CLIENT_SECRET,
    YOUTUBE_REFRESH_TOKEN,
)


class YouTubePlatform(SocialPlatform):
    name = "youtube"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"

    def is_configured(self) -> bool:
        return bool(YOUTUBE_ACCESS_TOKEN)

    def _refresh_access_token(self) -> str:
        """Refresh the OAuth access token using the refresh token."""
        if not YOUTUBE_REFRESH_TOKEN or not YOUTUBE_CLIENT_ID:
            raise RuntimeError("YouTube refresh token or client ID not set")

        resp = requests.post(self.TOKEN_URL, data={
            "client_id": YOUTUBE_CLIENT_ID,
            "client_secret": YOUTUBE_CLIENT_SECRET,
            "refresh_token": YOUTUBE_REFRESH_TOKEN,
            "grant_type": "refresh_token",
        }, timeout=30)
        resp.raise_for_status()
        return resp.json()["access_token"]

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
                "message": "YouTube not configured. Set YOUTUBE_ACCESS_TOKEN in .env",
            }

        try:
            token = YOUTUBE_ACCESS_TOKEN
            # Try to refresh if we have a refresh token
            if YOUTUBE_REFRESH_TOKEN:
                try:
                    token = self._refresh_access_token()
                except Exception:
                    pass  # fall back to the stored access token

            # Build metadata
            import json
            tags = tags or []
            metadata = {
                "snippet": {
                    "title": title[:100],
                    "description": description[:5000],
                    "tags": tags,
                    "categoryId": "22",  # People & Blogs
                },
                "status": {
                    "privacyStatus": privacy,
                    "selfDeclaredMadeForKids": False,
                },
            }

            # Read video file (supports both local paths and URLs)
            if isinstance(video_path, str) and video_path.startswith("http"):
                video_data = requests.get(video_path, timeout=120).content
            else:
                with open(video_path, "rb") as f:
                    video_data = f.read()

            resp = requests.post(
                f"{self.UPLOAD_URL}?uploadType=multipart&part=snippet,status",
                headers={"Authorization": f"Bearer {token}"},
                files={
                    "metadata": ("metadata.json", json.dumps(metadata), "application/json"),
                    "video": ("video.mp4", video_data, "video/mp4"),
                },
                timeout=300,
            )
            resp.raise_for_status()
            data = resp.json()

            video_id = data.get("id")
            return {
                "success": True,
                "platform": self.name,
                "post_url": f"https://www.youtube.com/watch?v={video_id}",
                "post_id": video_id,
                "message": "Video uploaded to YouTube successfully",
            }
        except Exception as e:
            return {
                "success": False,
                "platform": self.name,
                "post_url": None,
                "post_id": None,
                "message": f"YouTube upload failed: {e}",
            }
