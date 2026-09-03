"""
Social platform factory — returns the right platform by name.
"""

from .base import SocialPlatform
from .youtube import YouTubePlatform
from .instagram import InstagramPlatform
from .facebook import FacebookPlatform
from .x_twitter import XPlatform

_PLATFORMS = {
    "youtube": YouTubePlatform,
    "instagram": InstagramPlatform,
    "facebook": FacebookPlatform,
    "x": XPlatform,
}


def get_platform(name: str) -> SocialPlatform:
    """Get a social platform instance by name."""
    cls = _PLATFORMS.get(name)
    if not cls:
        raise ValueError(f"Unknown platform '{name}'. Available: {list(_PLATFORMS.keys())}")
    return cls()


def list_platforms() -> list[dict]:
    """Return all platforms with their configuration status."""
    results = []
    for name, cls in _PLATFORMS.items():
        instance = cls()
        results.append({
            "name": name,
            "configured": instance.is_configured(),
        })
    return results
