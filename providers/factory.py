"""
Provider factory — returns the right video provider based on name.
"""

from .base import VideoProvider
from .kling import KlingProvider
from .veo import VeoProvider
from .minimax import MiniMaxProvider
from .runway import RunwayProvider
from .pika import PikaProvider
from .replicate import ReplicateProvider

_PROVIDERS = {
    "kling": KlingProvider,
    "veo": VeoProvider,
    "minimax": MiniMaxProvider,
    "runway": RunwayProvider,
    "pika": PikaProvider,
    "replicate": ReplicateProvider,
}

# Provider recommendations by use case
RECOMMENDATIONS = {
    "realistic": "kling",
    "cinematic": "veo",
    "social_media": "minimax",
    "brand": "runway",
    "trending": "pika",
    "budget": "minimax",
}


def get_provider(name: str = None) -> VideoProvider:
    """Get a video provider instance by name."""
    from config.settings import DEFAULT_VIDEO_PROVIDER

    name = name or DEFAULT_VIDEO_PROVIDER
    cls = _PROVIDERS.get(name)
    if not cls:
        raise ValueError(
            f"Unknown provider '{name}'. Available: {list(_PROVIDERS.keys())}"
        )
    return cls()


def list_providers() -> list[dict]:
    """Return all providers with their info and configuration status."""
    results = []
    for name, cls in _PROVIDERS.items():
        instance = cls()
        results.append(instance.get_info())
    return results


def get_recommendations() -> dict:
    """Return recommended providers for different use cases."""
    return RECOMMENDATIONS
