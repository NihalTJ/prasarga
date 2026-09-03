"""
Base class for all social media posting platforms.
Each platform implements the same interface so posting is uniform.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class SocialPlatform(ABC):
    """Abstract base for social media video posting."""

    name: str = "base"

    @abstractmethod
    def post_video(
        self,
        video_path: str | Path,
        title: str,
        description: str = "",
        tags: list[str] | None = None,
        privacy: str = "public",
    ) -> dict:
        """
        Post a video to this platform.

        Args:
            video_path: Path or URL to the video file.
            title: Video title / caption.
            description: Longer description.
            tags: List of hashtags or tags.
            privacy: "public", "unlisted", or "private".

        Returns:
            {
                "success": bool,
                "platform": str,
                "post_url": str | None,   # URL to the published post
                "post_id": str | None,
                "message": str,
            }
        """
        ...

    @abstractmethod
    def is_configured(self) -> bool:
        """Return True if this platform has the required credentials."""
        ...
