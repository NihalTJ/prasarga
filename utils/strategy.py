"""
Content Strategy Guide — provides actionable 2026 social media strategy for AI video creators.

Covers: niche selection, posting cadence, optimal timing, disclosure rules,
batch workflow, and platform-specific optimization tips.
"""

# Optimal posting times (in target timezone)
POSTING_TIMES = {
    "facebook": ["9-11 AM", "1-3 PM", "7-9 PM"],
    "youtube": ["2-4 PM weekdays", "9-11 AM weekends"],
    "instagram": ["6-9 AM", "12-2 PM", "5-7 PM"],
    "x": ["12-1 PM", "5-6 PM"],
}

# Posting frequency recommendations
POSTING_FREQUENCY = {
    "facebook": {"min": "1x/day", "ideal": "1-2x/day", "max": "2x/day"},
    "youtube": {"min": "3x/week", "ideal": "1x/day", "max": "2x/day"},
    "instagram": {"min": "3x/week", "ideal": "5-7x/week", "max": "2x/day"},
    "x": {"min": "1x/day", "ideal": "2-3x/day", "max": "5x/day"},
}

# Niche profitability ranking
NICHE_RANKINGS = [
    {
        "niche": "Finance",
        "yt_rpm": 0.13,
        "difficulty": "Medium",
        "audience": "Business professionals, investors",
        "content_ideas": [
            "AI visualization of market trends",
            "Luxury lifestyle B-roll with financial tips overlay",
            "Animated infographics about money/wealth",
            "Cinematic shots of financial districts",
        ],
        "best_provider": "Runway Gen-4.5 (professional polish)",
    },
    {
        "niche": "Tech",
        "yt_rpm": 0.10,
        "difficulty": "Medium",
        "audience": "Tech enthusiasts, developers, early adopters",
        "content_ideas": [
            "Macro shots of futuristic tech gadgets",
            "AI labs and clean minimalist environments",
            "Product demos with cinematic B-roll",
            "Futuristic UI/animations",
        ],
        "best_provider": "Veo 3.1 (cinematic quality) or Runway (brand content)",
    },
    {
        "niche": "Education",
        "yt_rpm": 0.08,
        "difficulty": "Easy",
        "audience": "Students, lifelong learners, curious minds",
        "content_ideas": [
            "Historical events recreated with AI",
            "Scientific concepts visualized",
            "How things work — animated explanations",
            "AI recreation of famous moments in history",
        ],
        "best_provider": "Kling 3.0 (multi-shot storytelling)",
    },
    {
        "niche": "Travel",
        "yt_rpm": 0.04,
        "difficulty": "Easy",
        "audience": "Travel enthusiasts, dreamers",
        "content_ideas": [
            "Breathtaking drone shots of destinations",
            "Hidden gems and secret locations",
            "Cultural moments and local experiences",
            "Before/after transformations of real places",
        ],
        "best_provider": "Veo 3.1 (cinematic landscapes)",
    },
    {
        "niche": "Food",
        "yt_rpm": 0.05,
        "difficulty": "Easy",
        "audience": "Foodies, home cooks",
        "content_ideas": [
            "Macro food photography in motion",
            "Slow-motion cooking processes",
            "Restaurant-quality plating close-ups",
            "Satisfying food transformations",
        ],
        "best_provider": "MiniMax (fast, cheap for high-volume posting)",
    },
    {
        "niche": "Nature",
        "yt_rpm": 0.03,
        "difficulty": "Easy",
        "audience": "Nature lovers, relaxation seekers",
        "content_ideas": [
            "Wildlife close-ups documentary style",
            "Dramatic weather and landscapes",
            "Time-lapse nature transformations",
            "Hidden natural phenomena",
        ],
        "best_provider": "Veo 3.1 (best for natural scenes)",
    },
    {
        "niche": "Lifestyle",
        "yt_rpm": 0.04,
        "difficulty": "Medium",
        "audience": "Young adults, aesthetic-focused",
        "content_ideas": [
            "Aesthetic morning/evening routines",
            "Cozy interior shots with natural light",
            "Self-care and wellness visual content",
            "Minimalist lifestyle B-roll",
        ],
        "best_provider": "MiniMax (fast for daily posting)",
    },
    {
        "niche": "Entertainment",
        "yt_rpm": 0.02,
        "difficulty": "Hard",
        "audience": "General audience",
        "content_ideas": [
            "Surreal/impossible scenarios",
            "Anthropomorphic animals doing human things",
            "Comedy sketches with AI characters",
            "Trending meme formats",
        ],
        "best_provider": "Pika (creative effects) or MiniMax (volume)",
    },
]

# Disclosure requirements by platform
DISCLOSURE_RULES = {
    "youtube": {
        "requirement": "MANDATORY: Label realistic AI content as 'Altered content' in YouTube Studio.",
        "how_to": "When uploading, check 'Altered content' in the upload flow. "
                  "Required for content that could be mistaken for real footage.",
        "penalty": "Failure to disclose = demonetization or channel removal.",
    },
    "facebook": {
        "requirement": "MANDATORY: Label AI-generated content using Facebook's AI content label.",
        "how_to": "Enable 'AI-generated content' toggle before posting. "
                  "Facebook also auto-detects AI content with ~90% accuracy.",
        "penalty": "Unlabeled AI content is removed. AI content is excluded from Creator Rewards.",
    },
    "instagram": {
        "requirement": "RECOMMENDED: Use Meta's 'AI-generated' label.",
        "how_to": "Toggle 'AI-generated' label before posting. Meta is rolling out auto-labeling.",
        "penalty": "No direct penalty yet, but builds trust and transparency.",
    },
    "x": {
        "requirement": "RECOMMENDED: Add '#AIgenerated' or '#AIvideo' to your post.",
        "how_to": "Include disclosure in your tweet text. X may add auto-labels in future.",
        "penalty": "No penalty, but transparency builds audience trust.",
    },
}

# Batch production workflow
BATCH_WORKFLOW = {
    "name": "Weekly Batch Production (2-3 hours, twice per week)",
    "steps": [
        "1. Write 10-15 prompts in advance (use the Prompt Enhancer)",
        "2. Generate all videos in one session (parallel if possible)",
        "3. Review and reject weak outputs — keep only the best 6-8",
        "4. Add text overlays and captions to each video",
        "5. Write platform-specific titles/captions/tags for each",
        "6. Schedule posts across the week using platform native scheduling",
        "7. Monitor performance after 48 hours — identify top performers",
        "8. Generate 5 more variations of your best-performing format",
    ],
    "time_breakdown": {
        "prompt_writing": "20 min",
        "generation": "30-60 min (mostly waiting)",
        "editing_captions": "30 min",
        "scheduling": "15 min",
    },
    "total_weekly_time": "3-5 hours",
    "output": "6-8 high-quality videos per week across 4 platforms",
}


def get_strategy_guide(niche: str = "") -> dict:
    """
    Return a comprehensive content strategy guide.
    If a niche is specified, returns niche-specific recommendations.
    """
    niche_info = None
    if niche:
        niche_info = next((n for n in NICHE_RANKINGS if n["niche"].lower() == niche.lower()), None)

    return {
        "posting_times": POSTING_TIMES,
        "posting_frequency": POSTING_FREQUENCY,
        "niche_rankings": NICHE_RANKINGS,
        "selected_niche": niche_info,
        "disclosure_rules": DISCLOSURE_RULES,
        "batch_workflow": BATCH_WORKFLOW,
        "key_principles": [
            "The 3-second hook determines 65% of viral success. Engineer your opening frame explicitly.",
            "Series formats beat random posting. Create a recognizable format viewers return for.",
            "Post daily — AI lets you maintain 3x/day, which traditional creators physically can't.",
            "Cross-post to ALL platforms. Same video, slight edits per platform = 2x total reach.",
            "Let data drive decisions after 20-30 posts. Find what gets 3x average engagement, "
            "then produce 10 more variations of that specific format.",
            "Always disclose AI content. Transparency builds trust and keeps you monetizable.",
            "Add human creativity: original commentary, editing decisions, or narrative development. "
            "Pure 100% AI content is being demonetized across platforms.",
            "Batch produce 2x per week (2-3 hours each). This enables daily posting at quality.",
        ],
    }


def get_platform_tips(platform: str = "") -> dict:
    """
    Return platform-specific optimization tips.
    """
    all_tips = {
        "youtube": {
            "format": "Vertical 9:16, 15-60 seconds",
            "hook": "Strong visual hook in first frame + text overlay with bold claim",
            "description": "Front-load hook in first line. Add 3-5 niche hashtags at the end.",
            "best_content": "Cinematic B-roll, educational content, storytelling series",
            "monetization": "45% ad revenue share. Need 1K subs + 10M views/90 days. "
                          "Highest direct pay for AI creators.",
            "tips": [
                "Use YouTube's built-in A/B thumbnail testing",
                "Pin a comment linking to your best related Short",
                "Upload a horizontal version as a regular video for extra reach",
                "Post at 2-4 PM on weekdays for algorithm boost",
            ],
        },
        "facebook": {
            "format": "Vertical 9:16, 15-60 seconds (1+ min for Creator Rewards, but AI excluded)",
            "hook": "Pattern interrupt in first second. Bold visual + on-screen text.",
            "description": "Short caption + 3-5 relevant hashtags. Use trending sounds.",
            "best_content": "Trending formats, comedy, satisfying content, 'AI vs Real'",
            "monetization": "AI content excluded from Creator Rewards. "
                          "Use Facebook for AUDIENCE GROWTH, not direct income. "
                          "Monetize via Facebook Shop affiliate + brand deals.",
            "tips": [
                "Post 1-2x per day on Facebook Reels",
                "Use trending sounds within 48 hours of peak",
                "Engage with comments in first hour for algorithm boost",
                "Create a series — 'Day X of...' builds return viewers",
            ],
        },
        "instagram": {
            "format": "Vertical 9:16, 15-30 seconds",
            "hook": "Aesthetic + emotional. Beautiful first frame that stops the scroll.",
            "description": "Aspirational caption + 5-7 hashtags. Save-worthy content performs best.",
            "best_content": "Aesthetic, aspirational, travel, food, lifestyle, transformations",
            "monetization": "No direct payment. Monetize via brand deals (need 10K+ followers). "
                          "Average: $200-2000/post at 50K-100K followers.",
            "tips": [
                "Post 5-7x per week consistently",
                "Save-to-collection is a key signal — make content worth saving",
                "Use carousel posts for deeper engagement",
                "Post at 6-9 AM or 5-7 PM when audience is active",
            ],
        },
        "x": {
            "format": "Native video upload, 15-45 seconds",
            "hook": "Conversation-starting. Bold claim or comparison that drives replies.",
            "description": "Provocative one-liner + question. 'What do you think?' drives engagement.",
            "best_content": "Tech demos, AI vs traditional comparisons, behind-the-scenes",
            "monetization": "Ad revenue share if Premium eligible. Great for driving traffic "
                          "to YouTube/website. High share rate amplifies reach.",
            "tips": [
                "Upload natively — never link Facebook/YouTube",
                "Ask a question in every post to drive replies",
                "Thread your videos for more engagement",
                "Post at 12-1 PM or 5-6 PM",
            ],
        },
    }

    if platform:
        return all_tips.get(platform.lower(), {})
    return all_tips
