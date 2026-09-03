# 🎬 Prasarga — AI Video Studio

Create realistic AI videos, optimize them for virality, post to social media, and earn money.

## What This App Does

A complete web app that helps you:

1. **Generate realistic AI videos** from text prompts using the best 2026 models
2. **Enhance prompts** with realism boosters, viral hook formulas, and platform-specific optimization
3. **Score viral potential** before generating — see your hook strength, emotional triggers, trend alignment
4. **Calculate earnings** — projected monthly income across all platforms based on your niche and views
5. **Post to social media** — YouTube Shorts, Instagram Reels, Facebook, X (Twitter) from one interface
6. **Track history** — see all generated videos and posting status

## Quick Start

```bash
cd ai-video-studio
pip install -r requirements.txt
cp .env.example .env    # fill in your API keys
python app.py           # open http://localhost:5000
```

For X (Twitter) posting, also run: `pip install requests-oauthlib`

## App Tabs

### 🔍 Discover (NEW)
The app's "brain" — decides what to create so you don't have to guess. Contains a curated library of 16 viral-worthy video ideas across 6 categories:
- **Physics**: Prince Rupert's Drop, Non-Newtonian Fluid, Chladni Plate sound patterns
- **Chemistry**: Elephant Toothpaste, Chemiluminescence, Bismuth Crystals
- **Nature**: Bioluminescent Waves, Volcanic Lightning, Frost Flowers
- **Satisfying**: Glass Fruit Cutting, Ferrofluid, Kinetic Sand
- **Geography**: Mariana Trench Descent, Scale of the Universe
- **Engineering**: V8 Engine Cutaway

Each idea includes:
- A ready-to-use prompt enhanced with physics accuracy constraints
- Physics principles list (gravity, fluid dynamics, thermodynamics, etc.)
- Platform ranking with reasoning (which platform this content performs best on and why)
- Viral score breakdown (hook, emotion, novelty, trend, retention)
- Recommended AI provider for maximum realism
- Earning potential (niche + estimated RPM)
- Series potential (can this become a recurring format?)

Buttons: "Surprise Me" (random idea), "Trending Now", "Best Earning Potential", filter by category. One-click "Generate This Video" sends the enhanced prompt straight to generation with the recommended provider.

### 🎨 Create
Generate AI videos from text prompts. Choose from 6 providers, set duration/aspect/resolution. Auto-enhances your prompt and checks viral score. Preview the video, add title/caption/tags, and post to multiple social platforms at once.

### ⚡ Enhance & Score
- **Prompt Enhancer**: Transforms basic ideas into optimized prompts with realism keywords, hook formulas, and niche-specific boosters
- **Viral Score Estimator**: Analyzes your prompt on 5 dimensions (hook strength, emotional trigger, visual novelty, trend alignment, retention design) and gives a 0-100 score with actionable recommendations

### 💰 Earnings
- **Monetization Calculator**: Enter your expected views and followers to see projected earnings across YouTube, Facebook, Instagram, and X — including additional revenue streams (affiliate, brand deals, merch, website ads, stock video)
- **Niche RPM Comparison**: See which niches pay the most per 1,000 views

### 📋 Strategy
Complete 2026 content strategy guide: key principles, niche rankings with content ideas, posting frequency and timing, batch production workflow, platform-specific tips, and AI content disclosure rules for each platform.

## Video Providers (2026 Best Models)

| Provider | Best For | Max Duration | Resolution | Native Audio | Cost/Clip | Realism |
|----------|----------|-------------|------------|-------------|-----------|---------|
| **MiniMax Hailuo 02** | Social media at scale (Facebook/Reels/Shorts) | 10s | 720p | No | ~$0.15 | Good |
| **Kling 3.0** | Realistic human motion, multi-shot | 15s | 4K | Yes | ~$0.45 | Excellent |
| **Google Veo 3.1** | Cinematic quality + synced audio | 60s | 1080p | Yes | ~$1.50 | Outstanding |
| **Runway Gen-4.5** | Brand/marketing content | 16s | 4K | No | ~$1.15 | Excellent |
| **Pika 2.0** | Creative effects, trending content | 10s | 1080p | No | ~$0.30 | Good |
| **Replicate** | Multi-model fallback | 10s | 720p | No | ~$0.50 | Good |

### Provider Recommendations

- **Most realistic**: Kling 3.0 (best human motion) or Veo 3.1 (best cinematic)
- **Social media at scale**: MiniMax Hailuo 02 (fastest + cheapest)
- **Brand/professional**: Runway Gen-4.5
- **Budget-friendly**: MiniMax or Pika

## Getting API Keys

### Video Generation

| Provider | Where to Get Key |
|----------|----------------|
| MiniMax | https://hailuoai.video |
| Kling | https://klingai.com |
| Veo (Google) | https://aistudio.google.com/apikey |
| Runway | https://runwayml.com/api/ |
| Pika | https://pika.art |
| Replicate | https://replicate.com/account/api-tokens |

### Social Media

| Platform | Where to Get Credentials |
|----------|------------------------|
| YouTube | Google Cloud Console → enable YouTube Data API v3 → OAuth 2.0 credentials |
| Instagram | Facebook Developer → Instagram Graph API |
| Facebook | https://developers.facebook.com/ |
| X (Twitter) | https://developer.x.com/ |

## Monetization Reality (2026)

### Which Platforms Pay AI Creators?

| Platform | AI Content? | RPM (per 1K views) | Direct Pay? |
|----------|------------|-------------------|-------------|
| **YouTube Shorts** | Yes (with disclosure + human input) | $0.02-$0.13 | Yes — 45% revenue share |
| **Facebook** | Excluded from Creator Rewards | ~$0.005-$0.02 | Negligible for AI |
| **Instagram** | Allowed (with disclosure) | $0 (brand deals only) | No direct payment |
| **X** | Allowed | ~$0.001 | Minimal |

### Key Insight
YouTube Shorts is the **only platform** that reliably pays AI creators directly. Facebook explicitly penalizes AI content (~$15/million views vs $200-600 for non-AI). Instagram has no direct payment program. The real money comes from:

1. **YouTube ad revenue** (primary direct income)
2. **Brand sponsorship deals** ($500-15K/month at 10K-100K followers)
3. **Affiliate marketing** ($200-3K/month, especially tech/finance)
4. **Website ad revenue** ($200-1.5K/month at 60K pageviews)
5. **Merchandise** ($100-2K/month with a series/character)
6. **Stock video sales** ($100-1K/month passive)

### YouTube Monetization Requirements
- 1,000 subscribers
- 10 million Shorts views in 90 days (OR 4,000 watch hours in 12 months)
- Must disclose AI content as "Altered content"
- Must show human creativity (100% AI with no human input = demonetized)

## Virality Strategy (2026)

### The 3-Second Hook Formula
65% of viral success is determined by the first 3 seconds. The app's Prompt Enhancer automatically adds:
- **Pattern interrupt**: Visually striking opening frame
- **Curiosity gap**: Makes viewer want to see what happens
- **Emotional trigger**: Wonder, humor, shock, or awe

### Best Practices
1. **Post daily** — AI lets you maintain 1-3x/day (traditional creators can't)
2. **Cross-post everywhere** — same video, slight edits per platform = 2x total reach
3. **Series format** — "Day X of..." or "AI vs Real" builds return viewers
4. **Batch produce** — 2-3 hours twice per week generates 6-8 videos
5. **Always disclose AI** — transparency keeps you monetizable
6. **Add human creativity** — commentary, editing, narrative = stays monetizable
7. **Niche matters** — finance/tech earn 5-10x more per view than entertainment
8. **Let data decide** — after 20-30 posts, find what gets 3x engagement and double down

## Project Structure

```
ai-video-studio/
├── app.py                    # Flask app — main entry point
├── requirements.txt
├── .env.example
├── config/settings.py        # All configuration & API key loading
├── providers/                # Video generation providers
│   ├── base.py
│   ├── kling.py              # Kling 3.0
│   ├── veo.py               # Google Veo 3.1
│   ├── minimax.py           # MiniMax Hailuo 02
│   ├── runway.py            # Runway Gen-4.5
│   ├── pika.py              # Pika 2.0
│   ├── replicate.py         # Replicate (multi-model)
│   └── factory.py           # Provider factory
├── social/                   # Social media posting modules
│   ├── base.py
│   ├── youtube.py
│   ├── instagram.py
│   ├── facebook.py
│   ├── x_twitter.py
│   └── factory.py
├── utils/
│   ├── helpers.py            # Video download, history
│   ├── prompt_enhancer.py   # Prompt optimization + hook formulas
│   ├── viral_scorer.py       # Viral potential estimator
│   ├── monetization.py      # Earnings calculator
│   └── strategy.py           # Content strategy guide
├── templates/index.html      # Web UI (4 tabs)
├── static/css/style.css
└── static/js/app.js
```

## Adding New Providers or Platforms

### New Video Provider
1. Create `providers/myprovider.py` implementing `VideoProvider` (must have `generate()`, `check_status()`, `is_configured()`, `get_info()`)
2. Register in `providers/factory.py` in `_PROVIDERS`

### New Social Platform
1. Create `social/myplatform.py` implementing `SocialPlatform` (must have `post_video()`, `is_configured()`)
2. Register in `social/factory.py` in `_PLATFORMS`

## Notes

- **Instagram & Facebook** require a **public video URL** for posting (they can't upload local files). Works best when your video provider returns a hosted URL.
- **YouTube** supports direct file upload from your local machine.
- Video generation costs money on all providers. MiniMax is cheapest (~$0.15/clip), Veo is most expensive (~$1.50/clip).
- The app polls APIs for completion — long generations (15s+) may take 2-5 minutes.
- Sora 2's API is shutting down September 2026 — not included in this app.

## License

MIT — use it however you like.
