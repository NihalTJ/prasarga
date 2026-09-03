"""
Platform Recommender — analyzes a video's content, topic, and characteristics
to recommend the best platform(s) for posting.

Based on 2026 research on platform algorithms, audience behavior, and monetization:
  - Facebook: highest interaction rate, best for experimental/satisfying content
  - YouTube: best for educational content, only platform that pays AI creators reliably
  - Instagram: best for aesthetic/visual content, high save rate
  - X: best for conversation-starting content, high share rate

Sources: Computers in Human Behavior (2026), PLOS One science communication study,
Facebook/YouTube algorithm research, creator economy data.
"""

# Platform scoring weights per content type
# Each content type is scored 0-10 for each platform based on research
CONTENT_PLATFORM_SCORES = {
    "experimental": {
        "facebook": 10,     # Highest engagement for experiment videos
        "instagram": 8,   # Dynamic experimental videos = highest engagement on IG
        "youtube": 7,     # Good for educational experiments
        "x": 5,           # Moderate — can spark discussion
    },
    "satisfying_asmr": {
        "facebook": 10,     # #1 format on Facebook, highest completion rate
        "instagram": 9,   # High save rate for aesthetic satisfying content
        "youtube": 7,     # ASMR channels growing fast
        "x": 4,           # Low — not conversation-driven
    },
    "educational_science": {
        "youtube": 10,    # Best for educational content, highest RPM
        "facebook": 7,      # Good reach but lower monetization for AI
        "instagram": 6,   # Moderate — needs visual appeal
        "x": 7,           # Good for science discussions
    },
    "nature_cinematic": {
        "youtube": 9,     # High watch time, good RPM
        "instagram": 10,  # #1 for aesthetic nature content
        "facebook": 7,      # Good for short clips
        "x": 6,           # Moderate shares
    },
    "geography_scale": {
        "youtube": 10,    # Best for scale/journey content
        "facebook": 7,      # Good for split series
        "x": 8,           # Conversation starter
        "instagram": 7,   # Good for carousel/split
    },
    "engineering": {
        "youtube": 10,    # Best for technical explanations
        "x": 8,           # Tech community engagement
        "facebook": 6,      # Moderate
        "instagram": 5,   # Lower for technical content
    },
    "trending_format": {
        "facebook": 10,     # Trending content lives on Facebook
        "instagram": 8,   # Good for trending
        "youtube": 7,     # Moderate
        "x": 7,           # Can amplify trending topics
    },
    "conversation_starter": {
        "x": 10,          # Best for driving discussion
        "facebook": 7,      # Comments are secondary signal
        "youtube": 6,     # Comments exist but less central
        "instagram": 5,   # Comments less prominent
    },
}

# Monetization ranking by platform (for AI creators)
MONETIZATION_RANK = {
    "youtube": 1,    # Only reliable direct pay for AI content (45% rev share)
    "instagram": 3,  # Brand deals (no direct payment)
    "facebook": 3,     # AI excluded from Creator Rewards (negligible direct pay)
    "x": 4,          # Minimal direct, but traffic referral value
}

# Platform display info
PLATFORM_INFO = {
    "youtube": {
        "name": "YouTube Shorts",
        "icon": "▶️",
        "best_for": "Educational content, highest monetization",
        "monetization": "45% ad revenue share (need 1K subs + 10M views/90 days)",
        "ai_friendly": True,
        "posting_frequency": "1x/day",
        "disclosure": "MANDATORY: Label as 'Altered content'",
    },
    "facebook": {
        "name": "Facebook",
        "icon": "🎵",
        "best_for": "Viral reach, experimental & satisfying content",
        "monetization": "AI content excluded from Creator Rewards. Use for AUDIENCE GROWTH.",
        "ai_friendly": False,  # Not for monetization, but fine for reach
        "posting_frequency": "1-3x/day",
        "disclosure": "MANDATORY: Enable AI content label",
    },
    "instagram": {
        "name": "Instagram Reels",
        "icon": "📸",
        "best_for": "Aesthetic/visual content, brand deals",
        "monetization": "No direct payment. Brand deals at 10K+ followers.",
        "ai_friendly": True,
        "posting_frequency": "5-7x/week",
        "disclosure": "RECOMMENDED: Use AI-generated label",
    },
    "x": {
        "name": "X (Twitter)",
        "icon": "🐦",
        "best_for": "Conversation starters, tech/science engagement",
        "monetization": "Ad revenue share if Premium eligible. High referral value.",
        "ai_friendly": True,
        "posting_frequency": "2-3x/day",
        "disclosure": "RECOMMENDED: Add #AIgenerated hashtag",
    },
}


def classify_content(prompt: str, category: str = "", tags: list = None) -> str:
    """
    Classify a prompt into a content type for platform scoring.
    """
    text = f"{prompt} {category} {' '.join(tags or [])}".lower()

    if any(w in text for w in ["experiment", "chemistry", "reaction", "explosion",
                                "eruption", "foam", "glow", "demonstration"]):
        return "experimental"
    if any(w in text for w in ["asmr", "satisfying", "cutting", "slicing", "crushing",
                                "kinetic sand", "glass fruit", "soap", "slime"]):
        return "satisfying_asmr"
    if any(w in text for w in ["physics", "science", "wave", "resonance", "magnetic",
                                "fluid", "quantum", "explain", "how does"]):
        return "educational_science"
    if any(w in text for w in ["nature", "aurora", "ocean", "volcano", "bioluminescence",
                                "lightning", "landscape", "wildlife", "sunset", "forest"]):
        return "nature_cinematic"
    if any(w in text for w in ["scale", "universe", "depth", "trench", "planet",
                                "galaxy", "size", "zoom", "descent", "journey"]):
        return "geography_scale"
    if any(w in text for w in ["engine", "mechanism", "machine", "how things work",
                                "engineering", "turbine", "gear", "transmission"]):
        return "engineering"
    if any(w in text for w in ["trending", "viral", "meme", "challenge", "trend"]):
        return "trending_format"
    if any(w in text for w in ["what if", "imagine", "debate", "controversial",
                                "question", "opinion"]):
        return "conversation_starter"

    # Default based on category
    if category.lower() in ("physics", "chemistry"):
        return "educational_science"
    if category.lower() == "nature":
        return "nature_cinematic"
    if category.lower() == "satisfying":
        return "satisfying_asmr"
    if category.lower() == "geography":
        return "geography_scale"
    if category.lower() == "engineering":
        return "engineering"

    return "educational_science"  # safe default


def recommend_platforms(
    prompt: str = "",
    category: str = "",
    tags: list = None,
    top_n: int = 4,
) -> dict:
    """
    Analyze content and recommend the best platform(s) for maximum performance.

    Returns:
        {
            "content_type": str,
            "rankings": [
                {
                    "platform": str,
                    "rank": int,
                    "score": int (0-10),
                    "reasoning": str,
                    "monetization_rank": int,
                    "platform_info": dict,
                }
            ],
            "primary_recommendation": str,
            "cross_post_strategy": str,
        }
    """
    content_type = classify_content(prompt, category, tags)
    scores = CONTENT_PLATFORM_SCORES.get(content_type, CONTENT_PLATFORM_SCORES["educational_science"])

    # Build rankings
    rankings = []
    for platform, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        reasoning = _get_reasoning(platform, content_type, score)
        rankings.append({
            "platform": platform,
            "rank": len(rankings) + 1,
            "score": score,
            "reasoning": reasoning,
            "monetization_rank": MONETIZATION_RANK.get(platform, 4),
            "platform_info": PLATFORM_INFO.get(platform, {}),
        })

    primary = rankings[0]["platform"]
    cross_post = _get_cross_post_strategy(content_type, rankings)

    return {
        "content_type": content_type.replace("_", " ").title(),
        "rankings": rankings[:top_n],
        "primary_recommendation": primary,
        "primary_reason": rankings[0]["reasoning"],
        "cross_post_strategy": cross_post,
    }


def _get_reasoning(platform: str, content_type: str, score: int) -> str:
    """Generate human-readable reasoning for a platform recommendation."""
    reasons = {
        ("facebook", "experimental"): "Facebook generates highest engagement for experimental science content. "
                                     "Experiment videos get the most views and comments on this platform.",
        ("facebook", "satisfying_asmr"): "Facebook is the #1 platform for ASMR/satisfying content with billions of views. "
                                       "Highest completion rate format — perfect for loops.",
        ("facebook", "educational_science"): "Facebook generates the most interactions for science content, but AI content "
                                            "isn't eligible for direct monetization. Use for audience growth.",
        ("facebook", "nature_cinematic"): "Facebook can amplify dramatic nature clips, especially with trending audio.",
        ("facebook", "geography_scale"): "Split into series for Facebook. Each scale level = one video.",
        ("facebook", "trending_format"): "Facebook is where trends start. Post within 48 hours of trend peak.",
        ("youtube", "experimental"): "YouTube rewards educational experiment content with high watch time and RPM. "
                                     "Only platform that directly pays AI creators (45% revenue share).",
        ("youtube", "satisfying_asmr"): "ASMR channels are among YouTube's fastest-growing. Good watch time for "
                                        "satisfying content. Revenue share available.",
        ("youtube", "educational_science"): "YouTube is the #1 platform for educational science. Highest RPM, "
                                             "long content lifespan, search-driven discovery.",
        ("youtube", "nature_cinematic"): "Cinematic nature content gets high watch time on YouTube. "
                                          "Documentary style performs well and earns reliably.",
        ("youtube", "geography_scale"): "Long-form scale/journey content gets maximum watch time. "
                                        "Educational content with high RPM.",
        ("youtube", "engineering"): "Engineering explained content has a loyal audience on YouTube. "
                                    "High RPM in tech niche.",
        ("instagram", "experimental"): "Dynamic experimental videos generate highest engagement on Instagram. "
                                        "High share rate for visual experiments.",
        ("instagram", "satisfying_asmr"): "Instagram's visual-first audience loves satisfying content. "
                                           "Extremely high save rate. Aesthetic quality matters most here.",
        ("instagram", "nature_cinematic"): "Instagram is the #1 platform for aesthetic nature content. "
                                            "Maximum saves and shares. Build a visually cohesive feed.",
        ("instagram", "educational_science"): "Instagram works for science if visuals are striking. "
                                               "Use carousel format for deeper engagement.",
        ("x", "conversation_starter"): "X is the best platform for starting conversations. "
                                       "Questions and surprising content drive replies and quote tweets.",
        ("x", "geography_scale"): "'How deep is the ocean really?' type content drives massive engagement "
                                  "through replies and shares on X.",
        ("x", "engineering"): "Tech and engineering communities are active on X. "
                              "Good for professional audience engagement.",
    }

    key = (platform, content_type)
    if key in reasons:
        return reasons[key]

    # Generic reasoning
    info = PLATFORM_INFO.get(platform, {})
    return f"{info.get('name', platform)} scores {score}/10 for this content type. {info.get('best_for', '')}"


def _get_cross_post_strategy(content_type: str, rankings: list) -> str:
    """Generate a cross-posting strategy recommendation."""
    top_platforms = [r["platform"] for r in rankings[:3]]
    strategy = (
        f"Post to ALL of these platforms — each one compounds your reach. "
        f"Priority: {' → '.join(top_platforms)}. "
    )

    if "youtube" in top_platforms and "facebook" in top_platforms:
        strategy += (
            "Post to Facebook first for initial reach, then YouTube Shorts for monetization. "
            "Facebook is your audience builder; YouTube is your income source."
        )
    elif "instagram" in top_platforms and "facebook" in top_platforms:
        strategy += (
            "Post to Facebook and Instagram simultaneously — same video, platform-specific caption. "
            "Add YouTube Shorts for monetization."
        )
    elif "youtube" in top_platforms:
        strategy += "YouTube is your primary monetization platform. Post there first, then cross-post."

    return strategy


def get_platform_info(platform: str = "") -> dict:
    """Return info about a specific platform, or all platforms."""
    if platform:
        return PLATFORM_INFO.get(platform, {})
    return PLATFORM_INFO
