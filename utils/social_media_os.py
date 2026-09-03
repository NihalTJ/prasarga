"""
Social Media OS Connector

This module connects the AI Video Studio to the Social Media OS platform.
It allows the Video Studio to push finished videos to Social Media OS
for automated scheduling, cross-platform posting, and engagement management.

Integration flow:
    1. Video Studio generates a video and prepares the caption
    2. Video Studio calls POST /api/content/ingest on Social Media OS
    3. Social Media OS adapts the caption per platform, schedules, and posts
    4. Performance data flows back into the Social Media OS dashboard
"""

import json
import logging
import urllib.request
import urllib.error
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)


def build_ingest_payload(
    video_url: str,
    topic: str,
    platforms: list[str],
    caption: str,
    *,
    idea_id: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[list[str]] = None,
    viral_score: Optional[int] = None,
    monetization_niche: Optional[str] = None,
    physics_principles: Optional[list[str]] = None,
    series_potential: Optional[str] = None,
    source: str = "prasarga",
) -> dict:
    """
    Build the payload for the Social Media OS ingest endpoint.

    This matches the /api/content/ingest contract described in the Social Media OS
    master document: video URL, topic, platforms, and suggested caption — enriched
    with metadata from the Video Studio so Social Media OS can make smarter decisions.
    """
    return {
        "source": source,
        "type": "video",
        "content": {
            "video_url": video_url,
            "topic": topic,
            "caption": caption,
            "category": category,
            "tags": tags or [],
            "metadata": {
                "idea_id": idea_id,
                "viral_score": viral_score,
                "monetization_niche": monetization_niche,
                "physics_principles": physics_principles or [],
                "series_potential": series_potential,
            },
        },
        "platforms": platforms,
    }


def send_to_social_os(
    video_url: str,
    topic: str,
    platforms: list[str],
    caption: str,
    **kwargs,
) -> dict:
    """
    Send a finished video to Social Media OS for scheduling and posting.

    Args:
        video_url: URL of the generated video file
        topic: Video topic / title
        platforms: List of platforms to post to (youtube, instagram, x, facebook)
        caption: Suggested caption (Social Media OS will adapt per platform)
        **kwargs: Additional metadata (idea_id, category, tags, viral_score, etc.)

    Returns:
        dict with keys:
            - success (bool)
            - status (str): "sent" | "disabled" | "error"
            - message (str): human-readable status
            - response (dict|None): response from Social Media OS if successful
            - payload (dict): the payload that was sent (for debugging)
    """
    payload = build_ingest_payload(
        video_url=video_url,
        topic=topic,
        platforms=platforms,
        caption=caption,
        **kwargs,
    )

    # Check if Social OS integration is configured
    if not settings.SOCIAL_OS_ENABLED:
        return {
            "success": False,
            "status": "disabled",
            "message": (
                "Social Media OS integration is not enabled. "
                "Set SOCIAL_OS_ENABLED=true and configure SOCIAL_OS_URL "
                "and SOCIAL_OS_API_KEY in your .env file."
            ),
            "response": None,
            "payload": payload,
        }

    if not settings.SOCIAL_OS_URL:
        return {
            "success": False,
            "status": "error",
            "message": "SOCIAL_OS_URL is not set. Configure it in your .env file.",
            "response": None,
            "payload": payload,
        }

    if not settings.SOCIAL_OS_API_KEY:
        return {
            "success": False,
            "status": "error",
            "message": "SOCIAL_OS_API_KEY is not set. Configure it in your .env file.",
            "response": None,
            "payload": payload,
        }

    # Build the full URL
    url = settings.SOCIAL_OS_URL.rstrip("/") + settings.SOCIAL_OS_INGEST_ENDPOINT

    # Prepare the request
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.SOCIAL_OS_API_KEY}",
            "X-Source": "prasarga",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            try:
                response_data = json.loads(response_body)
            except json.JSONDecodeError:
                response_data = {"raw": response_body}

            return {
                "success": True,
                "status": "sent",
                "message": f"Video sent to Social Media OS successfully. "
                           f"Social Media OS will schedule and post to: {', '.join(platforms)}",
                "response": response_data,
                "payload": payload,
            }

    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode("utf-8")
        except Exception:
            pass
        logger.error(f"Social OS returned HTTP {e.code}: {error_body}")
        return {
            "success": False,
            "status": "error",
            "message": f"Social Media OS returned error {e.code}: {error_body or e.reason}",
            "response": {"status_code": e.code, "error": error_body or e.reason},
            "payload": payload,
        }

    except urllib.error.URLError as e:
        logger.error(f"Cannot reach Social OS at {url}: {e.reason}")
        return {
            "success": False,
            "status": "error",
            "message": f"Cannot reach Social Media OS at {url}. "
                       f"Make sure it is running and the URL is correct. Error: {e.reason}",
            "response": None,
            "payload": payload,
        }

    except Exception as e:
        logger.error(f"Unexpected error sending to Social OS: {e}")
        return {
            "success": False,
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
            "response": None,
            "payload": payload,
        }


def generate_caption(topic: str, category: str, platforms: list[str],
                     description: str = "", tags: list[str] = None) -> dict:
    """
    Generate a platform-aware caption for the video.
    Social Media OS will further adapt this per platform, but we provide
    a strong starting point.

    Returns a dict with:
        - base_caption: the main caption
        - platform_variants: per-platform tweaked versions
    """
    base = f"{topic}"
    if description:
        base += f"\n\n{description}"
    if tags:
        base += "\n\n" + " ".join(f"#{t.replace(' ', '')}" for t in tags[:8])

    variants = {}
    for platform in platforms:
        if platform == "youtube":
            variants[platform] = base + "\n\nSubscribe for more physics-accurate AI videos!"
        elif platform == "instagram":
            # Instagram captions can be longer
            variants[platform] = base + "\n\n.\n.\n.\n" + " ".join(
                f"#{t.replace(' ', '')}" for t in (tags or [])[:15]
            )
        elif platform == "x":
            # X has character limits — keep it punchy
            short = topic
            if tags:
                short += " " + " ".join(f"#{t.replace(' ', '')}" for t in tags[:4])
            variants[platform] = short
        elif platform == "facebook":
            variants[platform] = base
        else:
            variants[platform] = base

    return {
        "base_caption": base,
        "platform_variants": variants,
    }


def check_connection() -> dict:
    """
    Check if the Social Media OS is reachable and properly configured.
    Useful for the settings page connection test.
    """
    if not settings.SOCIAL_OS_ENABLED:
        return {
            "configured": False,
            "reachable": False,
            "message": "Social Media OS integration is not enabled.",
        }

    if not settings.SOCIAL_OS_URL or not settings.SOCIAL_OS_API_KEY:
        return {
            "configured": False,
            "reachable": False,
            "message": "SOCIAL_OS_URL and SOCIAL_OS_API_KEY must be set.",
        }

    # Try a simple GET to the base URL to check reachability
    try:
        url = settings.SOCIAL_OS_URL.rstrip("/") + "/api/health"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {settings.SOCIAL_OS_API_KEY}",
                "X-Source": "prasarga",
            },
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return {
                "configured": True,
                "reachable": True,
                "message": f"Social Media OS is reachable at {settings.SOCIAL_OS_URL}",
                "status_code": response.status,
            }
    except urllib.error.HTTPError as e:
        # 404 might mean the health endpoint doesn't exist yet, but the server is running
        if e.code == 404:
            return {
                "configured": True,
                "reachable": True,
                "message": f"Social Media OS is running at {settings.SOCIAL_OS_URL} "
                           f"(health endpoint not found, but server responds)",
                "status_code": 404,
            }
        return {
            "configured": True,
            "reachable": False,
            "message": f"Social Media OS returned HTTP {e.code}: {e.reason}",
        }
    except urllib.error.URLError as e:
        return {
            "configured": True,
            "reachable": False,
            "message": f"Cannot reach Social Media OS: {e.reason}",
        }
    except Exception as e:
        return {
            "configured": True,
            "reachable": False,
            "message": f"Unexpected error: {str(e)}",
        }
