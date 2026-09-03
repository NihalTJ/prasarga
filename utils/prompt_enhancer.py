"""
Prompt Enhancer — transforms basic prompts into optimized, realistic video generation
prompts with hook formulas, realism keywords, and platform-specific optimization.

Based on 2026 best practices for AI video virality.
"""

# Realism keywords that significantly improve photorealistic output
REALISM_KEYWORDS = {
    "cinematic": ["cinematic lighting", "shot on ARRI Alexa", "cinematic color grading",
                  "film grain", "anamorphic lens", "shallow depth of field", "cinematic framing"],
    "photorealistic": ["photorealistic", "8K resolution", "hyper-detailed", "natural lighting",
                       "documentary footage", "real camera", "no CGI", "lifelike textures"],
    "human_motion": ["natural movement", "realistic gestures", "fluid motion",
                     "lifelike expressions", "natural gait", "realistic skin texture"],
    "camera": ["handheld camera", "steady cam", "drone shot", "tracking shot",
               "dolly in", "close-up", "wide angle", "POV shot"],
    "lighting": ["golden hour lighting", "soft natural light", "volumetric lighting",
                 "rim lighting", "backlit", "diffused light", "atmospheric haze"],
    "quality": ["ultra-detailed", "high production value", "professional footage",
                "sharp focus", "HDR", "color accurate"],
}

# Hook formulas that drive 50%+ hook rate (viewers past 3 seconds)
HOOK_FORMULAS = [
    {
        "name": "Pattern Interrupt",
        "template": "{unexpected_visual}. {subject} does {surprising_action} in {setting}.",
        "example": "A businessman in a suit walks into the ocean. He keeps walking until fully submerged.",
        "best_for": "Facebook, Reels",
    },
    {
        "name": "Curiosity Gap",
        "template": "Something impossible happens: {impossible_event}. {subject} reacts.",
        "example": "A city begins floating into the sky. People look up in disbelief.",
        "best_for": "YouTube Shorts, Facebook",
    },
    {
        "name": "Before-After Reveal",
        "template": "{subject} in {ordinary_state}. Then transforms into {extraordinary_state}.",
        "example": "A dusty old bookshop. The books begin flying off shelves, rearranging into a tornado of pages.",
        "best_for": "Instagram Reels, Facebook",
    },
    {
        "name": "Scale Disruption",
        "template": "Tiny {subject} in {giant_world}. Or giant {subject} in {tiny_world}.",
        "example": "A tiny 2-inch tall chef cooking in a full-scale kitchen, climbing on utensils.",
        "best_for": "All platforms",
    },
    {
        "name": "Emotional Cinematic",
        "template": "{subject} experiences {emotion} as {dramatic_event} unfolds in {setting}.",
        "example": "An old man watches a sunset alone on a cliff. Tears roll down his face as the sky turns gold.",
        "best_for": "YouTube Shorts, Instagram",
    },
    {
        "name": "Comedy/Satire",
        "template": "Absurd {subject} in {mundane_situation}, {comedic_twist}.",
        "example": "A cat in a business suit sits at a desk, reviewing stock charts and looking increasingly stressed.",
        "best_for": "Facebook, X",
    },
]

# Platform-specific prompt suffixes
PLATFORM_SUFFIXES = {
    "youtube": "Optimized for YouTube Shorts. Fast-paced, visually striking, hook in first frame.",
    "facebook": "Optimized for Facebook. Bold visual hook, trend-ready, emotional payoff.",
    "instagram": "Optimized for Instagram Reels. Aesthetic, aspirational, high visual quality.",
    "x": "Optimized for X. Conversation-starting, shareable, visually surprising.",
}

# Niches with highest monetization potential
NICHE_PROMPTS = {
    "finance": {
        "boosters": ["luxury lifestyle", "financial district", "wealth visualization",
                     "success story", "money flowing", "stock market"],
        "example": "Aerial shot of Manhattan financial district at golden hour, "
                   "traders walking confidently, cinematic, photorealistic",
    },
    "tech": {
        "boosters": ["futuristic technology", "clean minimalist", "product close-up",
                     "innovation showcase", "tech laboratory"],
        "example": "Macro shot of a futuristic chip glowing with blue light, "
                   "clean laboratory background, cinematic, ultra-detailed",
    },
    "travel": {
        "boosters": ["breathtaking landscape", "aerial drone shot", "hidden paradise",
                     "local culture", "golden hour", "travel destination"],
        "example": "Drone shot of a hidden tropical beach in the Philippines, "
                   "crystal clear water, golden hour lighting, cinematic",
    },
    "food": {
        "boosters": ["macro food shot", "steam rising", "slow motion pour",
                     "restaurant quality plating", "appetizing close-up"],
        "example": "Macro shot of chocolate slowly melting over a warm dessert, "
                   "golden lighting, shallow depth of field, photorealistic",
    },
    "nature": {
        "boosters": ["wildlife close-up", "national geographic style", "natural habitat",
                     "dramatic weather", "untouched wilderness"],
        "example": "Close-up of a snow leopard in the Himalayas, snow falling, "
                   "documentary footage style, photorealistic",
    },
    "lifestyle": {
        "boosters": ["aesthetic morning routine", "cozy interior", "self-care",
                     "minimalist lifestyle", "aspirational living"],
        "example": "Morning sunlight streaming through curtains into a cozy bedroom, "
                   "slow camera pan, cinematic, warm tones",
    },
}


def enhance_prompt(
    raw_prompt: str,
    niche: str = "",
    hook_style: str = "",
    target_platform: str = "",
    realism_level: str = "high",
) -> dict:
    """
    Transform a basic prompt into an optimized, realism-boosted, virality-focused prompt.

    Args:
        raw_prompt: The user's basic prompt idea.
        niche: Target niche for monetization optimization.
        hook_style: Desired hook formula name.
        target_platform: Target platform for optimization.
        realism_level: "low", "medium", "high", "maximum"

    Returns:
        {
            "enhanced_prompt": str,
            "hook_formula": dict,
            "niche": str,
            "suggestions": list[str],
        }
    """
    enhanced = raw_prompt.strip()
    suggestions = []

    # 1. Add realism keywords
    realism_tags = []
    if realism_level in ("high", "maximum"):
        realism_tags.extend(REALISM_KEYWORDS["photorealistic"][:2])
        realism_tags.extend(REALISM_KEYWORDS["cinematic"][:2])
        realism_tags.extend(REALISM_KEYWORDS["quality"][:1])
        if realism_level == "maximum":
            realism_tags.extend(REALISM_KEYWORDS["lighting"][:2])
            realism_tags.extend(REALISM_KEYWORDS["camera"][:1])

    # 2. Add niche-specific boosters
    niche_boosters = []
    if niche and niche in NICHE_PROMPTS:
        niche_boosters = NICHE_PROMPTS[niche]["boosters"][:3]
        suggestions.append(
            f"Niche '{niche}' detected. Added boosters: {', '.join(niche_boosters[:2])}"
        )

    # 3. Select hook formula
    selected_hook = None
    if hook_style:
        selected_hook = next((h for h in HOOK_FORMULAS if h["name"] == hook_style), None)
    elif target_platform == "facebook":
        selected_hook = HOOK_FORMULAS[0]  # Pattern Interrupt
    elif target_platform == "youtube":
        selected_hook = HOOK_FORMULAS[1]  # Curiosity Gap
    elif target_platform == "instagram":
        selected_hook = HOOK_FORMULAS[2]  # Before-After Reveal
    else:
        selected_hook = HOOK_FORMULAS[0]

    suggestions.append(f"Hook formula: {selected_hook['name']} — best for {selected_hook['best_for']}")

    # 4. Add opening frame direction
    opening_frame = "OPENING FRAME: visually striking composition that stops the scroll. "
    enhanced = f"{opening_frame}{enhanced}"

    # 5. Add camera direction if not present
    if not any(word in enhanced.lower() for word in ["camera", "shot", "angle", "drone", "close-up"]):
        enhanced += ". Slow cinematic camera movement, tracking shot"

    # 6. Append realism and niche keywords
    all_tags = realism_tags + niche_boosters
    if all_tags:
        enhanced += f". {', '.join(all_tags[:6])}"

    # 7. Add platform-specific suffix
    if target_platform and target_platform in PLATFORM_SUFFIXES:
        enhanced += f". {PLATFORM_SUFFIXES[target_platform]}"

    # 8. Suggest best provider for this prompt
    if niche in ("finance", "tech", "brand"):
        suggestions.append("Recommended provider: Runway Gen-4.5 (best for branded/professional content)")
    elif target_platform in ("facebook", "instagram"):
        suggestions.append("Recommended provider: MiniMax Hailuo 02 (fastest & cheapest for social media)")
    elif "human" in raw_prompt.lower() or "person" in raw_prompt.lower() or "face" in raw_prompt.lower():
        suggestions.append("Recommended provider: Kling 3.0 (best for realistic human motion)")
    else:
        suggestions.append("Recommended provider: Veo 3.1 (best overall cinematic quality)")

    return {
        "enhanced_prompt": enhanced,
        "hook_formula": selected_hook,
        "niche": niche,
        "suggestions": suggestions,
    }


def get_hook_formulas() -> list[dict]:
    """Return all available hook formulas."""
    return HOOK_FORMULAS


def get_niches() -> list[str]:
    """Return all available niche categories."""
    return list(NICHE_PROMPTS.keys())


def get_niche_info(niche: str) -> dict:
    """Return info about a specific niche."""
    return NICHE_PROMPTS.get(niche, {})
