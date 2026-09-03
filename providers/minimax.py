"""
MiniMax Hailuo 02 — Fastest & cheapest, best for social media content at scale.
Good prompt adherence, smooth output, ideal for Facebook Reels/YouTube Shorts.

Get API key: https://hailuoai.video (API access) or via replicate/fal.ai
Docs: https://docs.hailuoai.com/api
"""

import time
import requests

from .base import VideoProvider
from config.settings import MINIMAX_API_KEY


class MiniMaxProvider(VideoProvider):
    name = "minimax"
    display_name = "MiniMax Hailuo 02"
    description = "Fastest & cheapest, best for social media at scale"
    best_for = "Short-form vertical content, Facebook Reels/YouTube Shorts, high-volume posting"
    max_duration = 10
    supports_native_audio = False
    max_resolution = "720p"
    cost_per_clip = "$0.15"
    cost_per_second = 0.02

    BASE_URL = "https://api.hailuoai.com/v1"

    def __init__(self):
        self.api_key = MINIMAX_API_KEY

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
            raise RuntimeError("MiniMax API key not set. Add MINIMAX_API_KEY to .env")

        payload = {
            "model": "hailuo-02-standard",
            "prompt": prompt,
            "duration": min(duration, self.max_duration),
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        }
        if image_url:
            payload["image"] = image_url

        resp = requests.post(
            f"{self.BASE_URL}/video/generation",
            headers=self._headers(),
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        task_id = data.get("task_id") or data.get("id")

        if not task_id:
            raise RuntimeError(f"MiniMax did not return a task_id: {data}")

        return self._poll(task_id)

    def check_status(self, task_id: str) -> dict:
        if not self.is_configured():
            raise RuntimeError("MiniMax API key not set")

        resp = requests.get(
            f"{self.BASE_URL}/video/generation/{task_id}",
            headers=self._headers(),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        status = data.get("status", "unknown").lower()
        video_url = data.get("video_url") or data.get("url")

        return {
            "status": "completed" if status == "succeeded" else
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
                raise RuntimeError(f"MiniMax generation failed: {result['raw_response']}")
            time.sleep(interval)
            elapsed += interval

        raise TimeoutError(f"MiniMax task {task_id} did not complete in {max_wait}s")
