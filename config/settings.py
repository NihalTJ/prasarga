"""
Central configuration for AI Video Studio.
All API keys are read from environment variables — never hardcode them.
Copy .env.example to .env and fill in your keys.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

# ─── Flask ────────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
PORT = int(os.getenv("PORT", 5000))

# ─── Video Generation API Keys (2026 best models) ───────────────────────────
# Kling 3.0 — best realistic human motion, 4K, multi-shot, native audio
KLING_API_KEY = os.getenv("KLING_API_KEY", "")

# Google Veo 3.1 — best overall cinematic quality with synced audio
VEO_API_KEY = os.getenv("VEO_API_KEY", "")

# MiniMax Hailuo 02 — fastest & cheapest, best for social media at scale
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")

# Runway Gen-4.5 — best for brand/marketing content, advanced editing controls
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY", "")

# Pika 2.0 — fast iteration, creative effects, good for trending content
PIKA_API_KEY = os.getenv("PIKA_API_KEY", "")

# Replicate — fallback, hosts multiple open models
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY", "")

# Default provider — MiniMax is recommended for social media creators
# Options: kling, veo, minimax, runway, pika, replicate
DEFAULT_VIDEO_PROVIDER = os.getenv("DEFAULT_VIDEO_PROVIDER", "minimax")

# ─── Social Media API Keys ───────────────────────────────────────────────────
# YouTube (PRIMARY monetization platform for AI creators)
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_ACCESS_TOKEN = os.getenv("YOUTUBE_ACCESS_TOKEN", "")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")

# Instagram
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")

# Facebook Reels (good for reach in India, Meta Ads monetization)
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN", "")

# X (Twitter) — great for AI content virality & engagement
X_API_KEY = os.getenv("X_API_KEY", "")
X_API_SECRET = os.getenv("X_API_SECRET", "")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN", "")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET", "")

# ─── Social Media OS Integration ─────────────────────────────────────────────
# Connects to your separate Social Media OS platform (built on Claude)
# This allows the Video Studio to push finished videos to Social Media OS
# for automated scheduling, cross-platform posting, and engagement management.
#
# How it works:
#   1. Video Studio generates a video and prepares the caption
#   2. Video Studio calls POST /api/content/ingest on Social Media OS
#   3. Social Media OS adapts the caption per platform, schedules, and posts
#   4. Performance data flows back into the Social Media OS dashboard
#
# Set these in your .env file once your Social Media OS is deployed
SOCIAL_OS_ENABLED = os.getenv("SOCIAL_OS_ENABLED", "false").lower() == "true"
SOCIAL_OS_URL = os.getenv("SOCIAL_OS_URL", "")  # e.g. https://your-social-os.up.railway.app
SOCIAL_OS_API_KEY = os.getenv("SOCIAL_OS_API_KEY", "")  # shared secret for auth
SOCIAL_OS_INGEST_ENDPOINT = os.getenv("SOCIAL_OS_INGEST_ENDPOINT", "/api/content/ingest")

# ─── Video defaults optimized for social media ──────────────────────────────
DEFAULT_DURATION = 5        # seconds — ideal for Shorts/Reels/Facebook
DEFAULT_RESOLUTION = "720p"  # 720p balances quality vs API cost
DEFAULT_ASPECT_RATIO = "9:16"  # vertical for shorts/reels


def get_config_summary():
    """Return a dict showing which services are configured (without exposing keys)."""
    return {
        "video_providers": {
            "kling": bool(KLING_API_KEY),
            "veo": bool(VEO_API_KEY),
            "minimax": bool(MINIMAX_API_KEY),
            "runway": bool(RUNWAY_API_KEY),
            "pika": bool(PIKA_API_KEY),
            "replicate": bool(REPLICATE_API_KEY),
        },
        "social_platforms": {
            "youtube": bool(YOUTUBE_ACCESS_TOKEN),
            "instagram": bool(INSTAGRAM_ACCESS_TOKEN),
            "facebook": bool(FACEBOOK_ACCESS_TOKEN),
            "x": bool(X_ACCESS_TOKEN),
        },
        "default_provider": DEFAULT_VIDEO_PROVIDER,
        "social_os": {
            "enabled": SOCIAL_OS_ENABLED,
            "url": SOCIAL_OS_URL[:40] + "..." if len(SOCIAL_OS_URL) > 40 else SOCIAL_OS_URL,
            "connected": bool(SOCIAL_OS_URL and SOCIAL_OS_API_KEY),
        },
    }
