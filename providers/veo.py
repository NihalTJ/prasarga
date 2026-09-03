"""
Google Veo 3.1 — Best overall cinematic quality with synced audio.
Up to 60s, 1080p native (4K upscale), native synced audio.

Access via Google AI Studio or Vertex AI.
Get API key: https://aistudio.google.com/apikey
Docs: https://ai.google.dev/gemini-api/docs/video
"""

import time
import requests

from .base import VideoProvider
from config.settings import VEO_API_KEY


class VeoProvider(VideoProvider):
    name = "veo"
    display_name = "Google Veo 3.1"
    description = "Best cinematic quality, synced audio, 60s clips"
    best_for = "Hero shots, cinematic scenes, premium content, audio-led videos"
    max_duration = 60
    supports_native_audio = True
    max_resolution = "1080p"
    cost_per_clip = "$1.50"
    cost_per_second = 0.15

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    def __init__(self):
        self.api_key = VEO_API_KEY

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def generate(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: str = "9:16",
        resolution: str = "720p",
        image_url: str | None = None,
    ) -> dict:
        if not self.is_configured():
            raise RuntimeError("Veo API key not set. Add VEO_API_KEY to .env")

        payload = {
            "instances": [{
                "prompt": prompt,
                "image": {"bytesBase64Encoded": None} if image_url else None,
            }],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": aspect_ratio,
                "resolution": resolution,
                "durationSeconds": min(duration, self.max_duration),
                "generateAudio": True,
            },
        }
        if image_url:
            payload["instances"][0]["image"] = {"gcsUri": image_url}

        # Use the Veo model endpoint
        resp = requests.post(
            f"{self.BASE_URL}/models/veo-3.1:predictLongRunning?key={self.api_key}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        operation_name = data.get("name")

        if not operation_name:
            raise RuntimeError(f"Veo did not return an operation name: {data}")

        return self._poll(operation_name)

    def check_status(self, task_id: str) -> dict:
        if not self.is_configured():
            raise RuntimeError("Veo API key not set")

        resp = requests.get(
            f"{self.BASE_URL}/{task_id}?key={self.api_key}",
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        done = data.get("done", False)
        if done:
            videos = data.get("response", {}).get("generatedSamples", [])
            video_url = videos[0].get("video", {}).get("uri") if videos else None
            if video_url and not video_url.startswith("http"):
                video_url = f"https://generativelanguage.googleapis.com{video_url}&key={self.api_key}"
            return {
                "status": "completed",
                "video_url": video_url,
                "raw_response": data,
            }

        error = data.get("error")
        if error:
            return {
                "status": "failed",
                "video_url": None,
                "raw_response": data,
            }

        return {
            "status": "pending",
            "video_url": None,
            "raw_response": data,
        }

    def _poll(self, task_id: str, max_wait: int = 600, interval: int = 15) -> dict:
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
                raise RuntimeError(f"Veo generation failed: {result['raw_response']}")
            time.sleep(interval)
            elapsed += interval

        raise TimeoutError(f"Veo task {task_id} did not complete in {max_wait}s")
