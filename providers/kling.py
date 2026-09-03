"""
Kling 3.0 — Best for realistic human motion, facial expressions, multi-shot.
Native 4K @ 60fps, up to 15s, multi-shot with character consistency, native audio.

Get API key: https://klingai.com (API access) or via fal.ai / replicate
Docs: https://docs.kuaishou.com/kling-api
"""

import time
import requests

from .base import VideoProvider
from config.settings import KLING_API_KEY


class KlingProvider(VideoProvider):
    name = "kling"
    display_name = "Kling 3.0"
    description = "Best realistic human motion, 4K, multi-shot, native audio"
    best_for = "Talking heads, human subjects, cinematic B-roll, storytelling"
    max_duration = 15
    supports_native_audio = True
    max_resolution = "4K"
    cost_per_clip = "$0.45"
    cost_per_second = 0.09

    BASE_URL = "https://api.klingai.com/v1"

    def __init__(self):
        self.api_key = KLING_API_KEY

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
            raise RuntimeError("Kling API key not set. Add KLING_API_KEY to .env")

        payload = {
            "prompt": prompt,
            "duration": min(duration, self.max_duration),
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "cfg_scale": 0.5,
            "callback_url": None,
            "external_task_id": None,
        }
        if image_url:
            payload["image"] = image_url

        resp = requests.post(
            f"{self.BASE_URL}/videos/text2video",
            headers=self._headers(),
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        task_id = data.get("data", {}).get("task_id") or data.get("task_id")

        if not task_id:
            raise RuntimeError(f"Kling did not return a task_id: {data}")

        return self._poll(task_id)

    def check_status(self, task_id: str) -> dict:
        if not self.is_configured():
            raise RuntimeError("Kling API key not set")

        resp = requests.get(
            f"{self.BASE_URL}/videos/text2video/{task_id}",
            headers=self._headers(),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        status = data.get("data", {}).get("task_status", "unknown")
        videos = data.get("data", {}).get("task_result", {}).get("videos", [])
        video_url = videos[0].get("url") if videos else None

        return {
            "status": "completed" if status in ("succeed", "succeeded") else
                      "failed" if status == "failed" else "pending",
            "video_url": video_url,
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
                raise RuntimeError(f"Kling generation failed: {result['raw_response']}")
            time.sleep(interval)
            elapsed += interval

        raise TimeoutError(f"Kling task {task_id} did not complete in {max_wait}s")
