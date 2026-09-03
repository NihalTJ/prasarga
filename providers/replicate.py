"""
Replicate video generation provider.
Supports multiple models hosted on Replicate (e.g., stable-video-diffusion, wan-video).

Docs: https://replicate.com/docs
Get your API token: https://replicate.com/account/api-tokens
"""

import os
import time
import requests

from .base import VideoProvider
from config.settings import REPLICATE_API_KEY


class ReplicateProvider(VideoProvider):
    name = "replicate"
    BASE_URL = "https://api.replicate.com/v1"

    # Popular video models on Replicate
    MODELS = {
        "wan": "cjwbw/wan:latest",
        "stable-video": "stability-ai/stable-video-diffusion:latest",
        "kling": "kuaishou/kling-v1:latest",
    }

    def __init__(self, model_key: str = "wan"):
        self.api_key = REPLICATE_API_KEY
        self.model = self.MODELS.get(model_key, self.MODELS["wan"])

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Prefer": "wait",  # try synchronous response
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
            raise RuntimeError("Replicate API key not set. Add REPLICATE_API_KEY to .env")

        input_data = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
        }
        if image_url:
            input_data["image"] = image_url

        # Create prediction
        resp = requests.post(
            f"{self.BASE_URL}/predictions",
            headers=self._headers(),
            json={"version": self.model, "input": input_data},
            timeout=120,
        )
        resp.raise_for_status()
        prediction = resp.json()

        # If synchronous (Prefer: wait), we may already have output
        if prediction.get("status") == "succeeded" and prediction.get("output"):
            return {
                "video_url": prediction["output"][0]
                    if isinstance(prediction["output"], list)
                    else prediction["output"],
                "provider": self.name,
                "task_id": prediction["id"],
                "raw_response": prediction,
            }

        # Otherwise poll
        task_id = prediction["id"]
        return self._poll(task_id)

    def check_status(self, task_id: str) -> dict:
        if not self.is_configured():
            raise RuntimeError("Replicate API key not set")

        resp = requests.get(
            f"{self.BASE_URL}/predictions/{task_id}",
            headers=self._headers(),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        status = data.get("status", "unknown")
        output = data.get("output")

        return {
            "status": "completed" if status == "succeeded" else
                      "failed" if status == "failed" else "pending",
            "video_url": output[0] if isinstance(output, list) else output,
            "raw_response": data,
        }

    def _poll(self, task_id: str, max_wait: int = 300, interval: int = 10) -> dict:
        """Poll Replicate for completion."""
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
                raise RuntimeError(f"Replicate generation failed: {result['raw_response']}")
            time.sleep(interval)
            elapsed += interval

        raise TimeoutError(f"Replicate task {task_id} did not complete in {max_wait}s")
