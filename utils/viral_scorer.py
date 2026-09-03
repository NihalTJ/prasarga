"""
Viral Score Estimator — analyzes a prompt and caption to predict viral potential.
Scores on: hook strength, emotional trigger, visual novelty, trend alignment,
retention design, and engagement triggers.

Based on 2026 viral content analysis from Facebook, YouTube Shorts, and Instagram Reels.
"""

# Emotional triggers and their viral impact weights
EMOTIONAL_TRIGGERS = {
    "wonder": {"weight": 9, "keywords": ["impossible", "magical", "unbelievable", "incredible",
                "stunning", "breathtaking", "mesmerizing", "surreal", "impossible"]},
    "humor": {"weight": 8, "keywords": ["funny", "absurd", "ridiculous", "hilarious",
               "comedy", "satire", "parody", "silly", "weird"]},
    "curiosity": {"weight": 8, "keywords": ["secret", "mystery", "what happens", "hidden",
                  "unknown", "discover", "revealed", "nobody knows", "never seen"]},
    "fear": {"weight": 7, "keywords": ["scary", "terrifying", "dangerous", "creepy",
              "horror", "nightmare", "dread", "unsettling"]},
    "awe": {"weight": 9, "keywords": ["epic", "massive", "giant", "huge", "enormous",
             "spectacular", "magnificent", "grand", "colossal"]},
    "nostalgia": {"weight": 7, "keywords": ["retro", "vintage", "childhood", "old",
                   "classic", "memory", "remember", "throwback"]},
    "inspiration": {"weight": 7, "keywords": ["success", "triumph", "overcome", "journey",
                    "transformation", "achievement", "dream", "goal"]},
    "shock": {"weight": 9, "keywords": ["unexpected", "sudden", "never before", "shocking",
               "surprising", "plot twist", "mind-blowing", "wait for it"]},
}

# Pattern interrupt indicators
PATTERN_INTERRUPTS = [
    "contrast", "unexpected", "suddenly", "but then", "however",
    "twist", "reverse", "flip", "break", "shatter", "explode",
    "transform", "morph", "change", "switch",
]

# Retention design elements
RETENTION_ELEMENTS = {
    "fast_pace": ["fast", "quick", "rapid", "quick cuts", "fast-paced"],
    "visual_variety": ["transition", "multiple angles", "close-up", "wide shot", "drone"],
    "cliffhanger": ["wait", "until", "at the end", "finally", "last second"],
    "loop": ["loop", "endless", "repeating", "cycle", "infinite"],
    "reveal": ["reveal", "shows", "exposes", "uncovers", "transforms into"],
}

# Trend-aligned content formats
TRENDING_FORMATS = [
    {"name": "AI vs Real", "keywords": ["ai vs real", "real or ai", "can you tell"],
     "score_boost": 8},
    {"name": "Before/After", "keywords": ["before", "after", "transformation", "then vs now"],
     "score_boost": 7},
    {"name": "What If", "keywords": ["what if", "imagine if", "alternate reality"],
     "score_boost": 8},
    {"name": "POV", "keywords": ["pov", "point of view", "first person"],
     "score_boost": 6},
    {"name": "Satisfying", "keywords": ["satisfying", "asmr", "mesmerizing", "oddly satisfying"],
     "score_boost": 9},
    {"name": "Storytelling", "keywords": ["story", "journey", "day in", "behind the scenes"],
     "score_boost": 6},
    {"name": "Educational", "keywords": ["how to", "learn", "did you know", "fact"],
     "score_boost": 5},
    {"name": "Challenge", "keywords": ["challenge", "try", "attempt", "can i"],
     "score_boost": 6},
]


def score_viral_potential(prompt: str, caption: str = "", niche: str = "") -> dict:
    """
    Analyze a prompt + caption to estimate viral potential.
    Returns a 0-100 score with breakdown and recommendations.

    Scoring dimensions (each 0-100, weighted):
    - Hook strength (25%): First-frame visual impact
    - Emotional trigger (20%): Emotional engagement potential
    - Visual novelty (20%): How unique/unexpected the content is
    - Trend alignment (15%): Matches trending formats
    - Retention design (20%): Elements that keep viewers watching
    """
    text = f"{prompt} {caption}".lower()

    # 1. Hook strength
    hook_score = 30  # base
    if any(kw in text for kw in PATTERN_INTERRUPTS):
        hook_score += 25
    if "opening frame" in text or "first frame" in text:
        hook_score += 15
    if any(kw in text for kw in ["close-up", "macro", "extreme close"]):
        hook_score += 10
    if any(kw in text for kw in ["bold", "striking", "dramatic", "extreme"]):
        hook_score += 10
    if any(kw in text for kw in ["slow motion", "freeze frame"]):
        hook_score += 10
    hook_score = min(hook_score, 100)

    # 2. Emotional trigger
    emotion_score = 20  # base
    emotions_detected = []
    for emotion, data in EMOTIONAL_TRIGGERS.items():
        if any(kw in text for kw in data["keywords"]):
            emotions_detected.append(emotion)
            emotion_score = max(emotion_score, data["weight"] * 10)
    if not emotions_detected:
        emotion_score = 25  # no emotional trigger detected
    emotion_score = min(emotion_score, 100)

    # 3. Visual novelty
    novelty_score = 30  # base
    novelty_keywords = ["impossible", "never seen", "surreal", "impossible",
                        "floating", "gravity", "giant", "tiny", "miniature",
                        "underwater", "space", "abstract", "dreamlike"]
    for kw in novelty_keywords:
        if kw in text:
            novelty_score += 12
    if any(kw in text for kw in ["ai generated", "ai video", "ai art"]):
        novelty_score += 5  # AI content is still novel to general audiences
    novelty_score = min(novelity_score if 'novelty_score' in dir() else 30, 100) if False else min(novelty_score, 100)

    # 4. Trend alignment
    trend_score = 20  # base
    trends_matched = []
    for trend in TRENDING_FORMATS:
        if any(kw in text for kw in trend["keywords"]):
            trends_matched.append(trend["name"])
            trend_score = max(trend_score, trend["score_boost"] * 10)
    trend_score = min(trend_score, 100)

    # 5. Retention design
    retention_score = 25  # base
    retention_elements_found = []
    for element, keywords in RETENTION_ELEMENTS.items():
        if any(kw in text for kw in keywords):
            retention_score += 15
            retention_elements_found.append(element)
    # Short content naturally retains better
    retention_score = min(retention_score, 100)

    # Weighted total
    total_score = (
        hook_score * 0.25 +
        emotion_score * 0.20 +
        novelty_score * 0.20 +
        trend_score * 0.15 +
        retention_score * 0.20
    )
    total_score = round(total_score)

    # Generate recommendations
    recommendations = _generate_recommendations(
        hook_score, emotion_score, novelty_score, trend_score, retention_score,
        emotions_detected, trends_matched, retention_elements_found, niche
    )

    return {
        "total_score": total_score,
        "grade": _score_to_grade(total_score),
        "breakdown": {
            "hook_strength": hook_score,
            "emotional_trigger": emotion_score,
            "visual_novelty": novelty_score,
            "trend_alignment": trend_score,
            "retention_design": retention_score,
        },
        "emotions_detected": emotions_detected,
        "trends_matched": trends_matched,
        "retention_elements": retention_elements_found,
        "recommendations": recommendations,
    }


def _score_to_grade(score: int) -> str:
    if score >= 80:
        return "A — High viral potential"
    elif score >= 65:
        return "B — Good potential, minor improvements needed"
    elif score >= 50:
        return "C — Average, needs stronger hook or emotional trigger"
    elif score >= 35:
        return "D — Below average, rethink your hook and add emotional triggers"
    else:
        return "F — Low viral potential. Start over with a stronger concept"


def _generate_recommendations(
    hook, emotion, novelty, trend, retention,
    emotions, trends, retention_elements, niche
) -> list[str]:
    recs = []

    if hook < 60:
        recs.append("HOOK: Add a pattern interrupt — start with something unexpected or visually "
                   "striking. Use 'OPENING FRAME:' in your prompt to control the first frame.")
    if emotion < 60:
        if not emotions:
            recs.append("EMOTION: No emotional trigger detected. Add wonder, humor, or shock "
                       "elements. Emotional content gets 3x more shares.")
        else:
            recs.append(f"EMOTION: {', '.join(emotions)} detected. Amplify it further with "
                       "more dramatic language in your prompt.")
    if novelty < 60:
        recs.append("NOVELTY: Make it more unique. Add impossible physics, surreal elements, "
                   "or scale disruption (tiny subject in giant world or vice versa).")
    if trend < 60:
        recs.append("TREND: Align with trending formats. Try 'AI vs Real', 'What If', "
                   "or 'Satisfying' formats — they're performing well in 2026.")
    if retention < 60:
        recs.append("RETENTION: Add fast cuts, visual transitions, or a cliffhanger ending. "
                   "Design for rewatch value — loops and reveals work best.")

    if not recs:
        recs.append("Excellent! Your prompt has strong viral elements. Focus on execution quality "
                   "and post at peak times for your audience.")

    # Niche-specific
    if niche == "finance":
        recs.append("Finance tip: Show wealth visually — luxury settings, success imagery. "
                   "Finance content has the highest RPM ($0.13/1K views on YouTube).")
    elif niche == "tech":
        recs.append("Tech tip: Use macro shots of products and clean minimalist backgrounds. "
                   "Tech pairs well with affiliate marketing income.")
    elif niche == "entertainment":
        recs.append("Entertainment has the lowest monetization. Consider adding educational or "
                   "aspirational elements to boost RPM and engagement.")

    return recs
