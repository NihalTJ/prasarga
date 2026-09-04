"""
Content Pack Generator — creates viral titles, hashtags, and captions for each platform.

When a video is generated (or an idea is selected), this module produces:
- 3 viral title options (hook-driven, curiosity-driven, benefit-driven)
- Platform-specific captions (YouTube, Instagram, X, Facebook)
- Hashtag sets (trending + niche + broad)
- Hook variations for the first 3 seconds

Based on 2026 viral content research across YouTube Shorts, Instagram Reels,
Facebook Reels, and X.
"""

import random

# ═══ Hook Formulas (proven viral openers) ═════════════════════════════

HOOK_FORMULAS = [
    "You won't believe what happens when...",
    "This {thing} breaks everything we know about...",
    "Watch what {thing} does when...",
    "Nobody told you this about...",
    "The crazy thing about {thing} is...",
    "This is what {thing} actually looks like...",
    "{thing} but with REAL physics",
    "What if {thing} followed actual science?",
    "POV: You discover that {thing}...",
    "Science says {thing} should be impossible...",
]

# ═══ Title Templates by Category ════════════════════════════════════

TITLE_TEMPLATES = {
    "curiosity": [
        "{topic} — {hook_clause}",
        "What happens when {topic}? (You won't expect this)",
        "This is what {topic} really looks like",
        "{topic} but it's REAL — no CGI",
        "The truth about {topic} that nobody shows you",
    ],
    "benefit": [
        "Understand {topic} in 10 seconds",
        "Master {topic} with this visual",
        "{topic} explained like never before",
        "Learn {topic} the easy way",
        "{topic} — finally makes sense",
    ],
    "viral": [
        "{topic} 🤯 #science #viral",
        "This {topic} video is breaking the internet",
        "POV: You just discovered {topic}",
        "{topic} but it's physics-accurate 👀",
        "Wait for it... {topic} 😱",
    ],
}

# ═══ Hashtag Banks ═══════════════════════════════════════════════════

TRENDING_HASHTAGS = [
    "#viral", "#fyp", "#foryou", "#shorts", "#reels",
    "#trending", "#viralvideo", "#explore", "#science", "#physics",
]

NICHE_HASHTAGS = {
    "Physics": ["#physics", "#science", "#physicsfun", "#sciencelover", "#experiment"],
    "Chemistry": ["#chemistry", "#science", "#chemicalreaction", "#chemfun", "#scienceiscool"],
    "Nature": ["#nature", "#science", "#naturalphenomenon", "#amazingnature", "#earth"],
    "Satisfying": ["#satisfying", "#oddlysatisfying", "#asmr", "#calming", "#mesmerizing"],
    "Geography": ["#geography", "#science", "#earth", "#geology", "#nature"],
    "Engineering": ["#engineering", "#science", "#howitworks", "#mechanical", "#tech"],
    "History": ["#history", "#science", "#historical", "#didyouknow", "#interesting"],
    "NCERT Physics": ["#ncert", "#physics", "#cbse", "#class11", "#class12", "#jee", "#neet"],
    "NCERT Chemistry": ["#ncert", "#chemistry", "#cbse", "#class11", "#class12", "#jee", "#neet"],
    "NCERT Maths": ["#ncert", "#maths", "#cbse", "#class11", "#class12", "#mathtricks"],
    "NCERT Biology": ["#ncert", "#biology", "#cbse", "#class11", "#class12", "#neet", "#biology"],
    "Anime & Silly": ["#anime", "#physics", "#whatif", "#animephysics", "#funny"],
}

BROAD_HASHTAGS = [
    "#ai", "#aivideo", "#artificialintelligence", "#aitechnology",
    "#didyouknow", "#learning", "#education", "#interesting",
]

# ═══ Platform-Specific Caption Templates ═════════════════════════════

YOUTUBE_CTA = [
    "Subscribe for more physics-accurate AI videos!",
    "Follow for daily science visualizations 🔬",
    "New videos every week — subscribe to not miss out!",
    "Which phenomenon should I visualize next? Comment below 👇",
]

INSTAGRAM_CTA = [
    "Save this for later 🔖",
    "Share with someone who needs to see this!",
    "Follow for more science that makes you go 🤯",
    "Double tap if this blew your mind ❤️",
]

X_CTA = [
    "RT if this amazed you 🔁",
    "Follow @ChaosAndContext for more science content",
    "What's your take on this? Reply below 👇",
    "This is your daily reminder that science is wild",
]

FACEBOOK_CTA = [
    "Like and follow for more amazing science content!",
    "Share this with a science lover!",
    "Comment your thoughts below!",
    "Follow the page for daily science videos!",
]


def generate_content_pack(
    topic: str,
    category: str = "",
    description: str = "",
    tags: list = None,
    platforms: list = None,
    viral_score: int = None,
) -> dict:
    """
    Generate a complete content pack for a video.

    Returns:
        {
            "titles": [3 viral title options],
            "hashtags": {
                "trending": [...],
                "niche": [...],
                "broad": [...],
                "all": [...],
            },
            "captions": {
                "youtube": "...",
                "instagram": "...",
                "x": "...",
                "facebook": "...",
            },
            "hooks": [3 hook variations for first 3 seconds],
            "best_title": "recommended title",
            "best_hashtag_set": "recommended hashtags as string",
        }
    """
    tags = tags or []
    platforms = platforms or ["youtube", "instagram", "x", "facebook"]
    niche_key = category if category in NICHE_HASHTAGS else "Physics"
    niche_tags = NICHE_HASHTAGS.get(niche_key, NICHE_HASHTAGS["Physics"])

    # Generate 3 title options (one from each style)
    titles = []
    for style in ["curiosity", "benefit", "viral"]:
        template = random.choice(TITLE_TEMPLATES[style])
        title = template.format(topic=topic, hook_clause=description[:60] + "..." if len(description) > 60 else description)
        titles.append(title)

    # Pick best title (curiosity-driven usually performs best)
    best_title = titles[0]

    # Generate hashtag sets
    trending = random.sample(TRENDING_HASHTAGS, min(5, len(TRENDING_HASHTAGS)))
    niche = niche_tags[:5]
    broad = random.sample(BROAD_HASHTAGS, min(3, len(BROAD_HASHTAGS)))
    all_tags = trending + niche + broad

    # Generate hook variations
    hooks = []
    for formula in random.sample(HOOK_FORMULAS, min(3, len(HOOK_FORMULAS))):
        hook = formula.replace("{thing}", topic.lower())
        hooks.append(hook)

    # Generate platform-specific captions
    base_caption = f"{topic}"
    if description:
        base_caption += f"\n\n{description}"

    captions = {}

    # YouTube caption
    yt_hashtags = " ".join(all_tags[:8])
    yt_cta = random.choice(YOUTUBE_CTA)
    captions["youtube"] = f"{best_title}\n\n{base_caption}\n\n{yt_hashtags}\n\n{yt_cta}"

    # Instagram caption (longer, more hashtags, emoji-heavy)
    ig_hashtags = " ".join(all_tags[:15])
    ig_cta = random.choice(INSTAGRAM_CTA)
    captions["instagram"] = f"{best_title} 🎬\n\n{base_caption}\n\n.\n.\n.\n\n{ig_hashtags}\n\n{ig_cta}"

    # X caption (short, punchy, fewer hashtags)
    x_hashtags = " ".join(all_tags[:4])
    x_cta = random.choice(X_CTA)
    x_text = best_title if len(best_title) < 100 else topic
    captions["x"] = f"{x_text} {x_hashtags}\n\n{x_cta}"

    # Facebook caption
    fb_hashtags = " ".join(all_tags[:6])
    fb_cta = random.choice(FACEBOOK_CTA)
    captions["facebook"] = f"{best_title}\n\n{base_caption}\n\n{fb_hashtags}\n\n{fb_cta}"

    return {
        "titles": titles,
        "best_title": best_title,
        "hashtags": {
            "trending": trending,
            "niche": niche,
            "broad": broad,
            "all": all_tags,
            "copy_paste": " ".join(all_tags),
        },
        "captions": captions,
        "hooks": hooks,
        "score_note": f"Viral score: {viral_score}/100" if viral_score else None,
    }
