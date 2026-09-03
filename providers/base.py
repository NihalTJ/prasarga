"""
Base class for all video generation providers.
Every provider implements the same interface so the app can swap them freely.
"""

from abc import ABC, abstractmethod
from typing import Optional


class VideoProvider(ABC):
    """Abstract base for AI video generation."""

    name: str = "base"
    display_name: str = "Base"
    description: str = ""
    best_for: str = ""
    max_duration: int = 10
    supports_native_audio: bool = False
    max_resolution: str = "1080p"
    cost_per_clip: str = "$0.50"
    cost_per_second: float = 0.05

    @abstractmethod
    def generate(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: str = "9:16",
        resolution: str = "720p",
        image_url: Optional[str] = None,
    ) -> dict:
        """
        Generate a video from a text prompt (and optionally an image).

        Returns:
            {
                "video_url": str,
                "provider": str,
                "task_id": str | None,
                "raw_response": dict,
            }
        """
        ...

    @abstractmethod
    def check_status(self, task_id: str) -> dict:
        """
        Poll the status of an async generation task.
        Returns {"status": "pending|completed|failed", "video_url": str|None}
        """
        ...

    def is_configured(self) -> bool:
        """Return True if this provider has the required API key set."""
        raise NotImplementedError

    def get_info(self) -> dict:
        """Return metadata about this provider for the UI."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "best_for": self.best_for,
            "max_duration": self.max_duration,
            "supports_native_audio": self.supports_native_audio,
            "max_resolution": self.max_resolution,
            "cost_per_clip": self.cost_per_clip,
            "cost_per_second": self.cost_per_second,
            "configured": self.is_configured(),
        }
