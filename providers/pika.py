"""
Pika 2.0 — Fast iteration, creative effects, good for trending content.
Up to 10s, 1080p, good for social-first viral effects.

Get API key: https://pika.art
Docs: https://docs.pika.art/
"""

import time
import requests

from .base import VideoProvider
from config.settings import PIKA_API_KEY


class PikaProvider(VideoProvider):
    name = "pika"
    display_name = "Pika 2.0"
    description = "Fast iteration, creative effects, social-first viral content"
    best_for = "Trending effects, quick experiments, social media viral content"
    max_duration = 10
    supports_native_audio = False
    max_resolution = "1080p"
    cost_per_clip = "$0.30"
    cost_per_second = 0.05

    BASE_URL = "https://api.pika.art/v1"

    def __init__(self):
        self.api_key = PIKA_API_KEY

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
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
            raise RuntimeError("Pika API key not set. Add PIKA_API_KEY to .env")

        payload = {
            "promptText": prompt,
            "options": {
                "aspectRatio": aspect_ratio,
                "resolution": resolution,
                "duration": min(duration, self.max_duration),
            },
        }
        if image_url:
            payload["image"] = image_url

        resp = requests.post(
            f"{self.BASE_URL}/generate",
            headers=self._headers(),
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        task = resp.json()
        task_id = task.get("id") or task.get("task_id")

        if task.get("videoUrl") or task.get("video_url"):
            return {
                "video_url": task.get("videoUrl") or task.get("video_url"),
                "provider": self.name,
                "task_id": task_id,
                "raw_response": task,
            }

        return self._poll(task_id)

    def check_status(self, task_id: str) -> dict:
        if not self.is_configured():
            raise RuntimeError("Pika API key not set")

        resp = requests.get(
            f"{self.BASE_URL}/tasks/{task_id}",
            headers=self._headers(),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        status = data.get("status", "unknown").lower()
        video_url = data.get("videoUrl") or data.get("video_url")

        return {
            "status": "completed" if status == "completed" else
                      "failed" if status == "failed" else "pending",
            "video_url": video_url,
            "raw_response": data,
        }

    def _poll(self, task_id: str, max_wait: int = 300, interval: int = 8) -> dict:
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
                raise RuntimeError(f"Pika generation failed: {result['raw_response']}")
            time.sleep(interval)
            elapsed += interval

        raise TimeoutError(f"Pika task {task_id} did not complete in {max_wait}s")
