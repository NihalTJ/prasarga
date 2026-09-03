"""
Runway Gen-4.5 — Best for brand/marketing content with advanced editing.
4K, up to 16s, Motion Brush, character consistency (Acts), style transfer.

Get API key: https://runwayml.com/api/
Docs: https://docs.dev.runwayml.com/
"""

import time
import requests

from .base import VideoProvider
from config.settings import RUNWAY_API_KEY


class RunwayProvider(VideoProvider):
    name = "runway"
    display_name = "Runway Gen-4.5"
    description = "Best for branded content, advanced editing controls, character consistency"
    best_for = "Marketing content, brand videos, VFX, product demos"
    max_duration = 16
    supports_native_audio = False
    max_resolution = "4K"
    cost_per_clip = "$1.15"
    cost_per_second = 0.12

    BASE_URL = "https://api.runwayml.com/v1"

    def __init__(self):
        self.api_key = RUNWAY_API_KEY

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Runway-Version": "2024-11-06",
        }

    def generate(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: str = "9:16",
        resolution: str = "720p",
        image_url: str | None = None,
    ) -> dict:
        if not self.is_configured():
            raise RuntimeError("Runway API key not set. Add RUNWAY_API_KEY to .env")

        payload = {
            "promptText": prompt,
            "model": "gen4_turbo",
            "duration": min(duration, self.max_duration),
            "ratio": aspect_ratio.replace(":", "x"),
        }
        if image_url:
            payload["promptImage"] = image_url

        endpoint = "image_to_video" if image_url else "text_to_video"

        resp = requests.post(
            f"{self.BASE_URL}/{endpoint}",
            headers=self._headers(),
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        task = resp.json()
        task_id = task["id"]

        return self._poll(task_id)

    def check_status(self, task_id: str) -> dict:
        if not self.is_configured():
            raise RuntimeError("Runway API key not set")

        resp = requests.get(
            f"{self.BASE_URL}/tasks/{task_id}",
            headers=self._headers(),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        status = data.get("status", "unknown")
        output = data.get("output", [])

        return {
            "status": "completed" if status == "SUCCEEDED" else
                      "failed" if status == "FAILED" else "pending",
            "video_url": output[0] if output else None,
            "raw_response": data,
        }

    def _poll(self, task_id: str, max_wait: int = 300, interval: int = 10) -> dict:
        elapsed = 0
        while elapsed < max_wait:
            result = self.check_status(task_id)
            if result["status"] == "completed":
                return {
                    "video_url": result["video_url"],
                    "provider": self.name,
                    "task_id": task_id,
                    "raw_response": result["raw_response"],
                }
            if result["status"] == "failed":
                raise RuntimeError(f"Runway generation failed: {result['raw_response']}")
            time.sleep(interval)
            elapsed += interval

        raise TimeoutError(f"Runway task {task_id} did not complete in {max_wait}s")
