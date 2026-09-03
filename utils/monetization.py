"""
Monetization Calculator — estimates earnings based on platform, niche, and views.
Uses 2026 real-world RPM data from creator reports and platform policies.

Key insight: YouTube Shorts is the ONLY platform that reliably pays AI creators.
Facebook penalizes AI content to ~$15/million views. Instagram has no direct payment.
The real money is in cross-posting + brand deals + affiliate revenue.
"""

# RPM data: revenue per 1,000 views (in USD)
# Sources: YouTube monetization policies, Facebook Creator Rewards data, creator reports 2026

# YouTube Shorts RPM by niche (AI content — 45% revenue share)
YOUTUBE_SHORTS_RPM = {
    "finance": 0.13,        # Highest: finance/business content
    "tech": 0.10,           # Technology, gadgets, tutorials
    "education": 0.08,      # Educational content
    "food": 0.05,           # Food/cooking
    "travel": 0.04,        # Travel content
    "nature": 0.03,         # Nature/wildlife
    "lifestyle": 0.04,     # Lifestyle/aesthetic
    "entertainment": 0.02,  # Lowest: general entertainment
}

# Facebook Reels RPM — in-stream ads available in India
FACEBOOK_RPM = {
    "finance": 0.020,   # ~$20 per million views (vs $400-1000 for non-AI)
    "tech": 0.018,
    "education": 0.015,
    "food": 0.010,
    "travel": 0.010,
    "nature": 0.008,
    "lifestyle": 0.010,
    "entertainment": 0.005,
}

# Instagram Reels — no direct payment program (since Aug 2025)
# Revenue comes from brand deals only
INSTAGRAM_BRAND_DEAL_RANGE = {
    "10k_followers": (50, 200),
    "50k_followers": (200, 800),
    "100k_followers": (500, 2000),
    "500k_followers": (2000, 8000),
    "1M_followers": (5000, 20000),
}

# X (Twitter) — no direct monetization, but great for driving traffic
# Revenue from creator subscriptions + tips + ad revenue share (if eligible)
X_RPM = 0.001  # negligible direct, but high referral value

# Additional revenue streams
ADDITIONAL_REVENUE = {
    "affiliate_marketing": {
        "description": "Promote products related to your niche",
        "typical_monthly": (200, 3000),
        "notes": "Tech and finance niches earn the most. Include affiliate links in bio.",
    },
    "brand_sponsorships": {
        "description": "Paid brand deals once you have 10K+ followers",
        "typical_monthly": (500, 15000),
        "notes": "Brands pay for AI video skills. Rate: $100-500 per 10K followers.",
    },
    "merchandise": {
        "description": "Sell merch related to your content series",
        "typical_monthly": (100, 2000),
        "notes": "Works best with a recurring character or series format.",
    },
    "website_ads": {
        "description": "Drive traffic to your own site with display ads",
        "typical_monthly": (200, 1500),
        "notes": "Mediavine/Ezoic ads. 60K monthly pageviews = $900-1500/month.",
    },
    "stock_video": {
        "description": "Sell AI clips on stock video platforms",
        "typical_monthly": (100, 1000),
        "notes": "Pond5, Shutterstock accept AI content with disclosure.",
    },
}

# Monetization thresholds by platform
MONETIZATION_THRESHOLDS = {
    "youtube": {
        "followers": 1000,
        "views_90_days": 10_000_000,  # 10M Shorts views in 90 days
        "watch_hours_alt": 4000,  # OR 4,000 watch hours in 12 months
        "revenue_share": "45% of pooled ad revenue",
        "ai_policy": "Allowed with disclosure. Must show human creativity. "
                     "100% AI with no human input = demonetized.",
    },
    "facebook": {
        "followers": 10000,
        "views_30_days": None,
        "revenue_share": "In-stream ads (55% revenue share like YouTube)",
        "ai_policy": "AI content allowed with disclosure. "
                     "In-stream ads available in India for Reels. "
                     "Better direct monetization than Instagram for AI creators.",
    },
    "instagram": {
        "followers": 10000,
        "views_90_days": None,  # No set threshold
        "revenue_share": "No direct payment (Reels Play Bonus discontinued Aug 2025)",
        "ai_policy": "AI content allowed with disclosure. "
                     "Monetize via brand deals and affiliate links.",
    },
    "x": {
        "followers": 500,
        "views_90_days": None,
        "revenue_share": "Ad revenue share (if eligible for Premium)",
        "ai_policy": "AI content allowed. Great for driving engagement and traffic.",
    },
}


def calculate_earnings(
    niche: str = "entertainment",
    monthly_views_youtube: int = 100000,
    monthly_views_facebook: int = 500000,
    monthly_views_instagram: int = 100000,
    monthly_views_x: int = 50000,
    followers: int = 0,
    include_additional: bool = True,
) -> dict:
    """
    Calculate projected monthly earnings across all platforms.

    Returns detailed breakdown with platform-specific earnings, thresholds,
    and additional revenue stream estimates.
    """
    niche = niche.lower() if niche.lower() in YOUTUBE_SHORTS_RPM else "entertainment"

    # YouTube Shorts
    yt_rpm = YOUTUBE_SHORTS_RPM.get(niche, 0.02)
    yt_earnings = (monthly_views_youtube / 1000) * yt_rpm
    yt_threshold_met = followers >= 1000

    # Facebook (AI content penalty applies)
    fb_rpm = FACEBOOK_RPM.get(niche, 0.005)
    fb_earnings = (monthly_views_facebook / 1000) * fb_rpm
    fb_threshold_met = followers >= 10000

    # Instagram (brand deals only)
    ig_earnings = 0
    ig_brand_range = (0, 0)
    for threshold, range_tuple in sorted(INSTAGRAM_BRAND_DEAL_RANGE.items()):
        threshold_num = int(threshold.replace("k_followers", "").replace("M_followers", "000"))
        if followers >= threshold_num:
            ig_brand_range = range_tuple
    if ig_brand_range != (0, 0):
        ig_earnings = (ig_brand_range[0] + ig_brand_range[1]) / 2 / 30  # monthly avg per deal

    # X
    x_earnings = (monthly_views_x / 1000) * X_RPM

    # Additional revenue
    additional = {}
    total_additional_mid = 0
    if include_additional:
        for stream, info in ADDITIONAL_REVENUE.items():
            mid = (info["typical_monthly"][0] + info["typical_monthly"][1]) / 2
            # Scale by follower count
            if followers < 10000:
                mid *= 0.1
            elif followers < 50000:
                mid *= 0.3
            elif followers < 100000:
                mid *= 0.5
            elif followers < 500000:
                mid *= 0.7
            additional[stream] = {
                "description": info["description"],
                "estimated_monthly": round(mid, 2),
                "range": info["typical_monthly"],
                "notes": info["notes"],
            }
            total_additional_mid += mid

    platform_earnings = yt_earnings + fb_earnings + ig_earnings + x_earnings
    total_monthly = platform_earnings + total_additional_mid
    total_annual = total_monthly * 12

    # Strategy recommendation
    strategy = _generate_strategy(niche, followers, monthly_views_youtube, yt_threshold_met)

    return {
        "niche": niche,
        "platforms": {
            "youtube": {
                "views": monthly_views_youtube,
                "rpm": yt_rpm,
                "earnings": round(yt_earnings, 2),
                "threshold_met": yt_threshold_met,
                "threshold_info": MONETIZATION_THRESHOLDS["youtube"],
            },
            "facebook": {
                "views": monthly_views_facebook,
                "rpm": fb_rpm,
                "earnings": round(fb_earnings, 2),
                "threshold_met": fb_threshold_met,
                "threshold_info": MONETIZATION_THRESHOLDS["facebook"],
                "warning": "Facebook penalizes AI content — you earn ~97% less than non-AI creators"
            },
            "instagram": {
                "views": monthly_views_instagram,
                "earnings": round(ig_earnings, 2),
                "threshold_info": MONETIZATION_THRESHOLDS["instagram"],
            },
            "x": {
                "views": monthly_views_x,
                "earnings": round(x_earnings, 2),
                "threshold_info": MONETIZATION_THRESHOLDS["x"],
            },
        },
        "platform_total": round(platform_earnings, 2),
        "additional_revenue": additional,
        "additional_total": round(total_additional_mid, 2),
        "total_monthly": round(total_monthly, 2),
        "total_annual": round(total_annual, 2),
        "strategy": strategy,
    }


def _generate_strategy(niche: str, followers: int, yt_views: int, yt_threshold: bool) -> list[str]:
    """Generate personalized monetization strategy recommendations."""
    tips = []

    if followers < 1000:
        tips.append("GOAL: Reach 1,000 YouTube subscribers + 10M Shorts views in 90 days for monetization.")
        tips.append("Post 1-3 Shorts daily. AI lets you maintain this pace — traditional creators can't.")
        tips.append(f"Focus on {niche} niche — it has higher RPM than general entertainment.")
    elif followers < 10000:
        tips.append("You're monetized on YouTube! Focus on increasing views and watch time.")
        tips.append("Start building Facebook presence for audience growth (don't expect much direct pay).")
        tips.append("Begin affiliate marketing in your niche for additional income.")
    elif followers < 100000:
        tips.append("Great progress! Start pursuing brand sponsorship deals ($500-2000/post).")
        tips.append("Cross-post to ALL platforms — each one compounds your total reach.")
        tips.append("Consider merchandise if you have a recognizable series/character.")
    else:
        tips.append("You're at scale! Diversify: brand deals, merch, courses, affiliate.")
        tips.append("Consider a website with display ads (Mediavine at 50K+ monthly visits).")
        tips.append("Sell AI video clips on stock platforms for passive income.")

    # Niche-specific tips
    if niche == "finance":
        tips.append("Finance is the highest-RPM niche. Even small view counts can earn well.")
    elif niche == "tech":
        tips.append("Tech content pairs perfectly with affiliate marketing (gadgets, software).")
    elif niche == "entertainment":
        tips.append("Entertainment has the lowest RPM. Consider pivoting to a more profitable niche "
                    "or rely on volume + brand deals.")

    return tips


def get_niche_rpm_comparison() -> list[dict]:
    """Return RPM comparison across niches for the UI."""
    results = []
    for niche in YOUTUBE_SHORTS_RPM:
        results.append({
            "niche": niche,
            "youtube_rpm": YOUTUBE_SHORTS_RPM[niche],
            "facebook_ai_rpm": FACEBOOK_RPM.get(niche, 0.005),
            "youtube_per_million": round(YOUTUBE_SHORTS_RPM[niche] * 1000, 2),
            "facebook_per_million": round(FACEBOOK_RPM.get(niche, 0.005) * 1000, 2),
        })
    return sorted(results, key=lambda x: x["youtube_rpm"], reverse=True)
