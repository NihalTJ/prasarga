"""
Facebook Reels posting via the Facebook Graph API.

Facebook Reels are available in India and can be monetized through
Facebook's in-stream ads and Stars program.

Prerequisites:
  1. A Facebook Page (not personal profile).
  2. A Facebook app with Pages permissions.
  3. A Page Access Token with pages_manage_posts and pages_read_engagement.

Docs: https://developers.facebook.com/docs/video-api/guides/reels
"""

import requests

from .base import SocialPlatform
from config.settings import FACEBOOK_ACCESS_TOKEN, FACEBOOK_PAGE_ID


class FacebookPlatform(SocialPlatform):
    name = "facebook"
    BASE_URL = "https://graph.facebook.com/v21.0"

    def is_configured(self) -> bool:
        return bool(FACEBOOK_ACCESS_TOKEN and FACEBOOK_PAGE_ID)

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
                "message": "Facebook not configured. Set FACEBOOK_ACCESS_TOKEN and FACEBOOK_PAGE_ID in .env",
            }

        # Facebook Reels requires a public video URL
        if isinstance(video_path, str) and not video_path.startswith("http"):
            return {
                "success": False,
                "platform": self.name,
                "post_url": None,
                "post_id": None,
                "message": "Facebook requires a public video URL. "
                           "Upload your video to a public host first.",
            }

        try:
            caption = title
            if description:
                caption += f"\n\n{description}"
            if tags:
                caption += "\n" + " ".join(f"#{t.lstrip('#')}" for t in tags)

            # Step 1: Create reel container
            resp = requests.post(
                f"{self.BASE_URL}/{FACEBOOK_PAGE_ID}/video_reels",
                data={
                    "video_url": video_path,
                    "title": title[:100],
                    "description": caption[:5000],
                    "access_token": FACEBOOK_ACCESS_TOKEN,
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            container_id = data.get("id")

            if not container_id:
                return {
                    "success": False,
                    "platform": self.name,
                    "post_url": None,
                    "post_id": None,
                    "message": f"Facebook did not return a container ID: {data}",
                }

            return {
                "success": True,
                "platform": self.name,
                "post_url": f"https://www.facebook.com/reel/{container_id}",
                "post_id": container_id,
                "message": "Reel published to Facebook successfully",
            }
        except Exception as e:
            return {
                "success": False,
                "platform": self.name,
                "post_url": None,
                "post_id": None,
                "message": f"Facebook upload failed: {e}",
            }
