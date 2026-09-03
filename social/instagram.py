"""
Instagram Reels posting via the Instagram Graph API.

Prerequisites:
  1. A Facebook Business account linked to an Instagram Business/Creator account.
  2. A Facebook app with Instagram Graph API permissions.
  3. A long-lived access token with instagram_content_publish permission.

Docs: https://developers.facebook.com/docs/instagram-api/guides/video-uploads
"""

import requests

from .base import SocialPlatform
from config.settings import INSTAGRAM_ACCESS_TOKEN


class InstagramPlatform(SocialPlatform):
    name = "instagram"
    BASE_URL = "https://graph.facebook.com/v21.0"

    def is_configured(self) -> bool:
        return bool(INSTAGRAM_ACCESS_TOKEN)

    def _get_ig_user_id(self) -> str:
        """Fetch the Instagram user ID from the access token."""
        resp = requests.get(
            f"{self.BASE_URL}/me",
            params={"fields": "id", "access_token": INSTAGRAM_ACCESS_TOKEN},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["id"]

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
                "message": "Instagram not configured. Set INSTAGRAM_ACCESS_TOKEN in .env",
            }

        # Instagram requires a public video URL — cannot upload local files directly
        if isinstance(video_path, str) and not video_path.startswith("http"):
            return {
                "success": False,
                "platform": self.name,
                "post_url": None,
                "post_id": None,
                "message": "Instagram requires a public video URL. "
                           "Upload your video to a public host first.",
            }

        try:
            ig_user_id = self._get_ig_user_id()
            caption = title
            if description:
                caption += f"\n\n{description}"
            if tags:
                caption += "\n" + " ".join(f"#{t.lstrip('#')}" for t in tags)

            # Step 1: Create media container
            resp = requests.post(
                f"{self.BASE_URL}/{ig_user_id}/media",
                data={
                    "media_type": "REELS",
                    "video_url": video_path,
                    "caption": caption[:2200],
                    "access_token": INSTAGRAM_ACCESS_TOKEN,
                },
                timeout=60,
            )
            resp.raise_for_status()
            container_id = resp.json()["id"]

            # Step 2: Publish the container
            resp = requests.post(
                f"{self.BASE_URL}/{ig_user_id}/media_publish",
                data={
                    "creation_id": container_id,
                    "access_token": INSTAGRAM_ACCESS_TOKEN,
                },
                timeout=60,
            )
            resp.raise_for_status()
            media_id = resp.json()["id"]

            return {
                "success": True,
                "platform": self.name,
                "post_url": f"https://www.instagram.com/reel/{media_id}",
                "post_id": media_id,
                "message": "Reel published to Instagram successfully",
            }
        except Exception as e:
            return {
                "success": False,
                "platform": self.name,
                "post_url": None,
                "post_id": None,
                "message": f"Instagram upload failed: {e}",
            }
