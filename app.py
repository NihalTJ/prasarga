"""
Flask application — Prasarga (AI Video Studio).
Main entry point. Run with: python app.py

Features:
  - AI video generation (Kling, Veo, MiniMax, Runway, Pika, Replicate)
  - Prompt enhancer with realism boosters and viral hook formulas
  - Viral score estimator
  - Monetization calculator
  - Content strategy guide
  - Social media posting (YouTube, Instagram, Facebook, X)
  - Batch generation mode
"""

import os
import sys
import uuid
from datetime import datetime

from flask import Flask, render_template, request, jsonify, send_from_directory
from config.settings import SECRET_KEY, DEBUG, PORT, STORAGE_DIR, get_config_summary
from providers.factory import get_provider, list_providers, get_recommendations
from social.factory import get_platform, list_platforms
from utils.helpers import download_video, save_to_history, get_history, clear_history
from utils.prompt_enhancer import (
    enhance_prompt, get_hook_formulas, get_niches as get_prompt_niches,
)
from utils.viral_scorer import score_viral_potential
from utils.monetization import calculate_earnings, get_niche_rpm_comparison
from utils.strategy import get_strategy_guide, get_platform_tips
from utils.idea_generator import (
    get_ideas, get_idea, get_idea_with_analysis, get_random_idea,
    get_categories, get_trending_ideas, get_best_earning_ideas,
)
from utils.platform_recommender import recommend_platforms, get_platform_info as get_platform_rec_info
from utils.physics_realism import enhance_physics_realism, get_physics_directives
from utils.idea_expander import (
    generate_idea, generate_ideas_batch, get_ncert_topics,
    generate_from_ncert_chapter,
)
from utils.social_media_os import (
    send_to_social_os, generate_caption, check_connection as check_social_os,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


# ─── Pages ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ─── API: Status ─────────────────────────────────────────────────────────────

@app.route("/api/status")
def api_status():
    return jsonify({
        "video_providers": list_providers(),
        "social_platforms": list_platforms(),
        "config": get_config_summary(),
        "recommendations": get_recommendations(),
    })


# ─── API: Generate Video ─────────────────────────────────────────────────────

@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.json
    prompt = data.get("prompt", "").strip()
    provider_name = data.get("provider")
    duration = int(data.get("duration", 5))
    aspect_ratio = data.get("aspect_ratio", "9:16")
    resolution = data.get("resolution", "720p")
    image_url = data.get("image_url")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        provider = get_provider(provider_name)
        if not provider.is_configured():
            return jsonify({
                "error": f"Provider '{provider.name}' is not configured. "
                         f"Add the API key to your .env file."
            }), 400

        result = provider.generate(
            prompt=prompt,
            duration=duration,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            image_url=image_url,
        )

        video_url = result["video_url"]

        local_path = None
        if video_url and video_url.startswith("http"):
            try:
                local_path = download_video(video_url)
            except Exception as e:
                print(f"Warning: could not download video locally: {e}")

        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "provider": result["provider"],
            "video_url": video_url,
            "local_path": local_path,
            "title": "",
            "description": "",
            "tags": [],
            "posted_to": [],
        }
        save_to_history(entry)

        return jsonify({
            "success": True,
            "video_url": video_url,
            "local_path": local_path,
            "id": entry["id"],
            "provider": result["provider"],
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── API: Post to Social Media ──────────────────────────────────────────────

@app.route("/api/post", methods=["POST"])
def api_post():
    data = request.json
    video_url = data.get("video_url")
    local_path = data.get("local_path")
    platforms = data.get("platforms", [])
    title = data.get("title", "AI Generated Video")
    description = data.get("description", "")
    tags = data.get("tags", [])
    privacy = data.get("privacy", "public")

    if not platforms:
        return jsonify({"error": "Select at least one platform"}), 400

    video_source = local_path or video_url
    if not video_source:
        return jsonify({"error": "No video available to post"}), 400

    results = []
    for platform_name in platforms:
        try:
            platform = get_platform(platform_name)
            if not platform.is_configured():
                results.append({
                    "platform": platform_name,
                    "success": False,
                    "message": f"{platform_name} is not configured. Set credentials in .env",
                })
                continue

            result = platform.post_video(
                video_path=video_source,
                title=title,
                description=description,
                tags=tags,
                privacy=privacy,
            )
            results.append(result)

        except Exception as e:
            results.append({
                "success": False,
                "platform": platform_name,
                "message": f"Error: {e}",
            })

    return jsonify({"results": results})


# ─── API: Prompt Enhancer ───────────────────────────────────────────────────

@app.route("/api/enhance-prompt", methods=["POST"])
def api_enhance_prompt():
    data = request.json
    result = enhance_prompt(
        raw_prompt=data.get("prompt", ""),
        niche=data.get("niche", ""),
        hook_style=data.get("hook_style", ""),
        target_platform=data.get("platform", ""),
        realism_level=data.get("realism_level", "high"),
    )
    return jsonify(result)


@app.route("/api/hook-formulas")
def api_hook_formulas():
    return jsonify({"formulas": get_hook_formulas()})


@app.route("/api/niches")
def api_niches():
    return jsonify({"niches": get_prompt_niches()})


# ─── API: Viral Score ────────────────────────────────────────────────────────

@app.route("/api/viral-score", methods=["POST"])
def api_viral_score():
    data = request.json
    result = score_viral_potential(
        prompt=data.get("prompt", ""),
        caption=data.get("caption", ""),
        niche=data.get("niche", ""),
    )
    return jsonify(result)


# ─── API: Monetization Calculator ───────────────────────────────────────────

@app.route("/api/monetization", methods=["POST"])
def api_monetization():
    data = request.json
    result = calculate_earnings(
        niche=data.get("niche", "entertainment"),
        monthly_views_youtube=int(data.get("yt_views", 100000)),
        monthly_views_facebook=int(data.get("fb_views", 500000)),
        monthly_views_instagram=int(data.get("ig_views", 100000)),
        monthly_views_x=int(data.get("x_views", 50000)),
        followers=int(data.get("followers", 0)),
        include_additional=data.get("include_additional", True),
    )
    return jsonify(result)


@app.route("/api/niche-rpm")
def api_niche_rpm():
    return jsonify({"niches": get_niche_rpm_comparison()})


# ─── API: Strategy Guide ────────────────────────────────────────────────────

@app.route("/api/strategy")
def api_strategy():
    niche = request.args.get("niche", "")
    return jsonify(get_strategy_guide(niche))


@app.route("/api/platform-tips")
def api_platform_tips():
    platform = request.args.get("platform", "")
    return jsonify(get_platform_tips(platform))


@app.route("/api/platform-tips-all")
def api_platform_tips_all():
    return jsonify(get_platform_tips())


# ─── API: History ────────────────────────────────────────────────────────────

@app.route("/api/history")
def api_history():
    return jsonify(get_history())


@app.route("/api/history", methods=["DELETE"])
def api_history_clear():
    clear_history()
    return jsonify({"success": True})


# ─── API: Serve local video files ───────────────────────────────────────────

@app.route("/storage/<path:filename>")
def serve_storage(filename):
    return send_from_directory(str(STORAGE_DIR), filename)


# ─── API: Content Ideas / Discover ──────────────────────────────────────────

@app.route("/api/ideas")
def api_ideas():
    category = request.args.get("category", "")
    trending = request.args.get("trending", "false").lower() == "true"
    limit = int(request.args.get("limit", 20))
    return jsonify({"ideas": get_ideas(category=category, trending_only=trending, limit=limit)})


@app.route("/api/ideas/<idea_id>")
def api_idea_detail(idea_id):
    result = get_idea_with_analysis(idea_id)
    if not result:
        return jsonify({"error": "Idea not found"}), 404
    return jsonify(result)


@app.route("/api/ideas/random")
def api_idea_random():
    return jsonify(get_random_idea())


@app.route("/api/ideas/trending")
def api_ideas_trending():
    limit = int(request.args.get("limit", 10))
    return jsonify({"ideas": get_trending_ideas(limit)})


@app.route("/api/ideas/best-earning")
def api_ideas_best_earning():
    limit = int(request.args.get("limit", 10))
    return jsonify({"ideas": get_best_earning_ideas(limit)})


@app.route("/api/categories")
def api_categories():
    return jsonify({"categories": get_categories()})


# ─── API: Platform Recommender ──────────────────────────────────────────────

@app.route("/api/recommend-platforms", methods=["POST"])
def api_recommend_platforms():
    data = request.json or {}
    result = recommend_platforms(
        prompt=data.get("prompt", ""),
        category=data.get("category", ""),
        tags=data.get("tags", []),
    )
    return jsonify(result)


# ─── API: Physics Realism ───────────────────────────────────────────────────

@app.route("/api/enhance-physics", methods=["POST"])
def api_enhance_physics():
    data = request.json or {}
    result = enhance_physics_realism(
        prompt=data.get("prompt", ""),
        physics_principles=data.get("physics_principles", []),
        maximize_realism=data.get("maximize_realism", True),
    )
    return jsonify(result)


@app.route("/api/physics-directives")
def api_physics_directives():
    return jsonify({"directives": get_physics_directives()})


# ─── API: Dynamic Idea Expander ────────────────────────────────────────────

@app.route("/api/generate-idea", methods=["POST"])
def api_generate_idea():
    """Generate a video idea dynamically from any topic."""
    data = request.json or {}
    topic = data.get("topic", "").strip()
    category = data.get("category", "")
    if not topic:
        return jsonify({"error": "Topic is required"}), 400
    idea = generate_idea(topic, category)
    # Enhance with physics realism and viral score
    enhanced = enhance_physics_realism(idea["prompt"], idea.get("physics_principles", []))
    score = score_viral_potential(idea["prompt"])
    idea["prompt"] = enhanced["enhanced_prompt"]
    idea["physics_notes"] = enhanced["physics_notes"]
    idea["viral_score_detail"] = score
    return jsonify(idea)


@app.route("/api/generate-ideas-batch", methods=["POST"])
def api_generate_ideas_batch():
    """Generate multiple ideas from a list of topics."""
    data = request.json or {}
    topics = data.get("topics", [])
    category = data.get("category", "")
    if not topics:
        return jsonify({"error": "At least one topic is required"}), 400
    ideas = generate_ideas_batch(topics, category)
    return jsonify({"ideas": ideas})


@app.route("/api/ncert-topics")
def api_ncert_topics():
    """Return all NCERT chapter topics for physics and chemistry."""
    subject = request.args.get("subject", "")
    return jsonify(get_ncert_topics(subject))


@app.route("/api/ncert-generate", methods=["POST"])
def api_ncert_generate():
    """Generate a video idea for a specific NCERT chapter."""
    data = request.json or {}
    chapter = data.get("chapter", "").strip()
    subject = data.get("subject", "physics")
    if not chapter:
        return jsonify({"error": "Chapter name is required"}), 400
    idea = generate_from_ncert_chapter(chapter, subject)
    enhanced = enhance_physics_realism(idea["prompt"], idea.get("physics_principles", []))
    score = score_viral_potential(idea["prompt"])
    idea["prompt"] = enhanced["enhanced_prompt"]
    idea["physics_notes"] = enhanced["physics_notes"]
    idea["viral_score_detail"] = score
    return jsonify(idea)


# ─── Social Media OS Integration ──────────────────────────────────────────────

@app.route("/api/social-os/status")
def social_os_status():
    """Check if Social Media OS is configured and reachable."""
    result = check_social_os()
    return jsonify(result)


@app.route("/api/social-os/send", methods=["POST"])
def social_os_send():
    """
    Send a finished video to Social Media OS for scheduling and posting.

    Expected JSON body:
        video_url: URL of the generated video
        topic: Video topic / title
        platforms: List of platforms to post to (youtube, instagram, x, facebook)
        caption: Suggested caption (optional — will be generated if omitted)
        idea_id: Idea ID for tracking (optional)
        category: Content category (optional)
        tags: List of tags (optional)
        viral_score: Viral score from the idea (optional)
        monetization_niche: Monetization niche (optional)
        physics_principles: List of physics principles (optional)
        series_potential: Series potential description (optional)
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    video_url = data.get("video_url", "").strip()
    topic = data.get("topic", "").strip()
    platforms = data.get("platforms", [])

    if not video_url:
        return jsonify({"error": "video_url is required"}), 400
    if not topic:
        return jsonify({"error": "topic is required"}), 400
    if not platforms:
        return jsonify({"error": "At least one platform is required"}), 400

    # Generate caption if not provided
    caption = data.get("caption", "").strip()
    if not caption:
        caption_data = generate_caption(
            topic=topic,
            category=data.get("category", ""),
            platforms=platforms,
            description=data.get("description", ""),
            tags=data.get("tags", []),
        )
        caption = caption_data["base_caption"]

    # Send to Social Media OS
    result = send_to_social_os(
        video_url=video_url,
        topic=topic,
        platforms=platforms,
        caption=caption,
        idea_id=data.get("idea_id"),
        category=data.get("category"),
        tags=data.get("tags"),
        viral_score=data.get("viral_score"),
        monetization_niche=data.get("monetization_niche"),
        physics_principles=data.get("physics_principles"),
        series_potential=data.get("series_potential"),
    )

    status_code = 200 if result["success"] else 400
    return jsonify(result), status_code


@app.route("/api/social-os/caption", methods=["POST"])
def social_os_caption():
    """
    Generate a platform-aware caption for a video.
    Useful for previewing captions before sending.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    topic = data.get("topic", "").strip()
    platforms = data.get("platforms", [])
    if not topic or not platforms:
        return jsonify({"error": "topic and platforms are required"}), 400

    caption_data = generate_caption(
        topic=topic,
        category=data.get("category", ""),
        platforms=platforms,
        description=data.get("description", ""),
        tags=data.get("tags", []),
    )
    return jsonify(caption_data)


# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  🎬 PRASARGA — AI Video Studio")
    print("=" * 60)
    print(f"  → http://localhost:{PORT}")
    print(f"  → Storage: {STORAGE_DIR}")
    print(f"  → Providers: Kling, Veo, MiniMax, Runway, Pika, Replicate")
    print(f"  → Social: YouTube, Instagram, Facebook, X")
    print(f"  → Features: Prompt Enhancer, Viral Score, Monetization Calc")
    print("=" * 60 + "\n")
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
