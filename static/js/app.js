// ═══ State ══════════════════════════════════════════════════════════
let currentVideo = { url: null, localPath: null, id: null };
let configStatus = { video_providers: [], social_platforms: [] };

// ═══ Init ═══════════════════════════════════════════════════════════
document.addEventListener("DOMContentLoaded", () => {
  loadStatus();
  loadHistory();
  loadStrategy();
  loadPlatformTips();
  loadRpmComparison();
  loadCategories();
  loadIdeas();
  loadSocialOSStatus();
  loadConfigSummary();

  // Tab navigation
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
    });
  });

  // Create tab
  document.getElementById("btn-generate").addEventListener("click", generateVideo);
  document.getElementById("btn-post").addEventListener("click", postToSocial);
  document.getElementById("btn-clear-history").addEventListener("click", clearHistory);

  // Enhance tab
  document.getElementById("btn-enhance").addEventListener("click", enhancePrompt);
  document.getElementById("btn-score").addEventListener("click", scoreViral);

  // Earnings tab
  document.getElementById("btn-calculate").addEventListener("click", calculateEarnings);

  // Discover tab
  document.getElementById("btn-random-idea").addEventListener("click", () => loadRandomIdea());
  document.getElementById("btn-trending-ideas").addEventListener("click", () => loadTrendingIdeas());
  document.getElementById("btn-best-earning").addEventListener("click", () => loadBestEarningIdeas());
  document.getElementById("discover-category").addEventListener("change", (e) => loadIdeas(e.target.value));
  document.getElementById("btn-close-detail").addEventListener("click", () => {
    document.getElementById("idea-detail-card").classList.add("hidden");
  });

  // Custom idea generator
  document.getElementById("btn-generate-custom").addEventListener("click", generateCustomIdea);
  document.getElementById("custom-topic").addEventListener("keypress", (e) => {
    if (e.key === "Enter") generateCustomIdea();
  });

  // NCERT topics
  document.getElementById("ncert-subject").addEventListener("change", () => loadNcertTopics());
  loadNcertTopics();

  // Social Media OS
  document.getElementById("btn-social-os").addEventListener("click", sendToSocialOS);
  document.getElementById("btn-test-social-os").addEventListener("click", testSocialOSConnection);
});

// ═══ Status ═════════════════════════════════════════════════════════
async function loadStatus() {
  try {
    const resp = await fetch("/api/status");
    const data = await resp.json();
    configStatus = data;

    // Render badges
    const badgesDiv = document.getElementById("status-badges");
    badgesDiv.innerHTML = "";
    data.video_providers.forEach(p => {
      badgesDiv.innerHTML += `<span class="badge ${p.configured ? 'ok' : 'off'}">${p.display_name} ${p.configured ? '✓' : '✗'}</span>`;
    });
    data.social_platforms.forEach(p => {
      badgesDiv.innerHTML += `<span class="badge ${p.configured ? 'ok' : 'off'}">${p.name} ${p.configured ? '✓' : '✗'}</span>`;
    });

    renderPlatformChecks();
    renderProviderInfo(data.video_providers);
  } catch (e) {
    console.error("Status load failed:", e);
  }
}

function renderPlatformChecks() {
  const container = document.getElementById("platform-checks");
  container.innerHTML = "";
  configStatus.social_platforms.forEach(p => {
    const label = document.createElement("label");
    label.className = "platform-check" + (p.configured ? "" : " disabled");
    label.innerHTML = `
      <input type="checkbox" value="${p.name}" ${p.configured ? '' : 'disabled'} />
      ${p.name} ${p.configured ? '' : '(not configured)'}
    `;
    container.appendChild(label);
  });
}

function renderProviderInfo(providers) {
  const container = document.getElementById("provider-info");
  if (!container) return;
  const select = document.getElementById("provider");
  const selected = select ? select.value : "";
  const provider = providers.find(p => p.name === selected);

  // Update dropdown options to show configured status + cost
  if (select) {
    providers.forEach(p => {
      for (let i = 0; i < select.options.length; i++) {
        if (select.options[i].value === p.name) {
          const status = p.configured ? '✅' : '❌';
          select.options[i].textContent = `${status} ${p.display_name} (~${p.cost_per_clip}/clip)`;
        }
      }
    });
  }

  if (provider) {
    const configStatus = provider.configured
      ? '<span style="color:var(--success);">● Configured</span>'
      : '<span style="color:var(--danger);">● API key needed</span>';
    container.innerHTML = `<strong>${provider.display_name}</strong> ${configStatus}<br>
      ${provider.description} |<br>
      Best for: ${provider.best_for} |<br>
      Cost: ~${provider.cost_per_clip}/clip | Max: ${provider.max_duration}s ${provider.max_resolution} | Audio: ${provider.supports_native_audio ? 'Yes' : 'No'}`;
  }
}

// Update provider info when selection changes
document.addEventListener("change", (e) => {
  if (e.target && e.target.id === "provider") {
    renderProviderInfo(configStatus.video_providers);
  }
});

// ═══ Generate Video ════════════════════════════════════════════════
async function generateVideo() {
  // Check if selected provider is configured
  const selectedProvider = document.getElementById("provider").value;
  const providerInfo = configStatus.video_providers.find(p => p.name === selectedProvider);
  if (providerInfo && !providerInfo.configured) {
    const status = document.getElementById("generate-status");
    status.className = "status-msg error";
    status.innerHTML = `❌ ${providerInfo.display_name} is not configured. Add the API key in the Settings tab or choose a configured provider. <a href="#" onclick="document.querySelector('.tab-btn[data-tab=\"settings\"]').click(); return false;">Go to Settings →</a>`;
    return;
  }
  let prompt = document.getElementById("prompt").value.trim();
  if (!prompt) {
    showMsg("generate-status", "Please enter a prompt.", "error");
    return;
  }

  // Auto-enhance if enabled
  const autoEnhance = document.getElementById("auto-enhance").checked;
  if (autoEnhance) {
    try {
      const enhResp = await fetch("/api/enhance-prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, realism_level: "high" }),
      });
      const enhData = await enhResp.json();
      if (enhData.enhanced_prompt) {
        prompt = enhData.enhanced_prompt;
        showMsg("generate-status", "Prompt auto-enhanced. Generating...", "loading");
      }
    } catch (e) {
      console.warn("Auto-enhance failed, using raw prompt");
    }
  }

  const btn = document.getElementById("btn-generate");
  const status = document.getElementById("generate-status");

  btn.disabled = true;
  status.className = "status-msg loading";
  status.innerHTML = '<span class="spinner"></span> Generating video... this can take 30-120 seconds.';

  try {
    const resp = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        provider: document.getElementById("provider").value,
        duration: parseInt(document.getElementById("duration").value),
        aspect_ratio: document.getElementById("aspect").value,
        resolution: document.getElementById("resolution").value,
        image_url: document.getElementById("image-url").value || null,
      }),
    });

    const data = await resp.json();
    if (!resp.ok) {
      status.className = "status-msg error";
      status.textContent = data.error || "Generation failed.";
      return;
    }

    currentVideo = { url: data.video_url, localPath: data.local_path, id: data.id };

    const previewCard = document.getElementById("preview-card");
    previewCard.classList.remove("hidden");

    const videoEl = document.getElementById("video-preview");
    if (data.local_path) {
      const filename = data.local_path.split("/").pop().split("\\").pop();
      videoEl.src = `/storage/${filename}`;
    } else {
      videoEl.src = data.video_url;
    }

    status.className = "status-msg success";
    status.textContent = "Video generated! Preview below and post to social media.";

    // Auto-score if enabled
    const autoScore = document.getElementById("auto-score").checked;
    if (autoScore) {
      try {
        const scoreResp = await fetch("/api/viral-score", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt }),
        });
        const scoreData = await scoreResp.json();
        if (scoreData.total_score !== undefined) {
          status.innerHTML += `<br>📊 Viral Score: ${scoreData.total_score}/100 — ${scoreData.grade}`;
        }
      } catch (e) { /* ignore score failure */ }
    }

    loadHistory();
  } catch (e) {
    status.className = "status-msg error";
    status.textContent = `Error: ${e.message}`;
  } finally {
    btn.disabled = false;
  }
}

// ═══ Post to Social Media ══════════════════════════════════════════
async function postToSocial() {
  const platforms = Array.from(document.querySelectorAll(".platform-check input:checked"))
    .map(cb => cb.value);
  if (!platforms.length) {
    showMsg("post-status", "Select at least one platform.", "error");
    return;
  }

  const btn = document.getElementById("btn-post");
  const status = document.getElementById("post-status");
  btn.disabled = true;
  status.className = "status-msg loading";
  status.innerHTML = '<span class="spinner"></span> Posting...';

  try {
    const resp = await fetch("/api/post", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        video_url: currentVideo.url,
        local_path: currentVideo.localPath,
        platforms,
        title: document.getElementById("post-title").value || "AI Generated Video",
        description: document.getElementById("post-desc").value,
        tags: document.getElementById("post-tags").value.split(",").map(t => t.trim()).filter(Boolean),
        privacy: document.getElementById("privacy").value,
      }),
    });

    const data = await resp.json();
    if (!resp.ok) {
      status.className = "status-msg error";
      status.textContent = data.error || "Posting failed.";
      return;
    }

    let html = "";
    data.results.forEach(r => {
      const cls = r.success ? "success" : "error";
      const icon = r.success ? "✅" : "❌";
      const link = r.post_url ? ` <a href="${r.post_url}" target="_blank" style="color:var(--accent)">View ↗</a>` : "";
      html += `<div class="${cls}">${icon} <strong>${r.platform}</strong>: ${r.message}${link}</div>`;
    });
    status.className = "status-msg";
    status.innerHTML = html;
    loadHistory();
  } catch (e) {
    status.className = "status-msg error";
    status.textContent = `Error: ${e.message}`;
  } finally {
    btn.disabled = false;
  }
}

// ═══ Prompt Enhancer ═══════════════════════════════════════════════
async function enhancePrompt() {
  const raw = document.getElementById("enhance-raw").value.trim();
  if (!raw) { alert("Enter a prompt to enhance"); return; }

  const resultDiv = document.getElementById("enhance-result");
  resultDiv.classList.remove("hidden");
  resultDiv.innerHTML = '<span class="spinner"></span> Enhancing...';

  try {
    const resp = await fetch("/api/enhance-prompt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt: raw,
        niche: document.getElementById("enhance-niche").value,
        target_platform: document.getElementById("enhance-platform").value,
        realism_level: document.getElementById("enhance-realism").value,
      }),
    });
    const data = await resp.json();

    let html = `<div class="hook-info">Hook formula: ${data.hook_formula.name} (best for ${data.hook_formula.best_for})</div>`;
    html += `<div class="enhanced-prompt">${escapeHtml(data.enhanced_prompt)}</div>`;
    html += `<ul class="suggestions">`;
    data.suggestions.forEach(s => html += `<li>${escapeHtml(s)}</li>`);
    html += `</ul>`;
    html += `<button class="btn btn-small btn-ghost" onclick="copyToClipboard('${escapeAttr(data.enhanced_prompt)}')">📋 Copy Enhanced Prompt</button>`;
    html += ` <button class="btn btn-small btn-ghost" onclick="useEnhancedPrompt('${escapeAttr(data.enhanced_prompt)}')">🎨 Use in Create Tab</button>`;

    resultDiv.innerHTML = html;
  } catch (e) {
    resultDiv.innerHTML = `<div class="error">Error: ${e.message}</div>`;
  }
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => alert("Prompt copied to clipboard!"));
}

function useEnhancedPrompt(text) {
  document.getElementById("prompt").value = text;
  document.querySelector('.tab-btn[data-tab="create"]').click();
}

// ═══ Viral Score ══════════════════════════════════════════════════
async function scoreViral() {
  const prompt = document.getElementById("score-prompt").value.trim();
  if (!prompt) { alert("Enter a prompt to score"); return; }

  const resultDiv = document.getElementById("score-result");
  resultDiv.classList.remove("hidden");
  resultDiv.innerHTML = '<span class="spinner"></span> Analyzing...';

  try {
    const resp = await fetch("/api/viral-score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        caption: document.getElementById("score-caption").value,
      }),
    });
    const data = await resp.json();

    const scoreClass = data.total_score >= 65 ? "high" : data.total_score >= 45 ? "mid" : "low";
    const dims = [
      { label: "Hook Strength", val: data.breakdown.hook_strength },
      { label: "Emotional Trigger", val: data.breakdown.emotional_trigger },
      { label: "Visual Novelty", val: data.breakdown.visual_novelty },
      { label: "Trend Alignment", val: data.breakdown.trend_alignment },
      { label: "Retention Design", val: data.breakdown.retention_design },
    ];

    let html = `
      <div class="score-circle ${scoreClass}">${data.total_score}</div>
      <div class="score-grade">${data.grade}</div>
      <div class="score-breakdown">
    `;
    dims.forEach(d => {
      const barColor = d.val >= 65 ? "var(--success)" : d.val >= 45 ? "var(--warn)" : "var(--error)";
      html += `
        <div class="score-bar-item">
          <div class="label">${d.label}</div>
          <div class="value">${d.val}</div>
          <div class="score-bar"><div class="score-bar-fill" style="width:${d.val}%; background:${barColor};"></div></div>
        </div>`;
    });
    html += `</div>`;

    if (data.emotions_detected.length) {
      html += `<p style="font-size:0.8rem;color:var(--text-dim);margin-bottom:8px;">
        Emotions: ${data.emotions_detected.join(", ")}</p>`;
    }
    if (data.trends_matched.length) {
      html += `<p style="font-size:0.8rem;color:var(--text-dim);margin-bottom:8px;">
        Trends matched: ${data.trends_matched.join(", ")}</p>`;
    }

    html += `<ul class="score-recs">`;
    data.recommendations.forEach(r => html += `<li>${escapeHtml(r)}</li>`);
    html += `</ul>`;

    resultDiv.innerHTML = html;
  } catch (e) {
    resultDiv.innerHTML = `<div class="error">Error: ${e.message}</div>`;
  }
}

// ═══ Earnings Calculator ═══════════════════════════════════════════
async function calculateEarnings() {
  const resultDiv = document.getElementById("earnings-result");
  resultDiv.classList.remove("hidden");
  resultDiv.innerHTML = '<span class="spinner"></span> Calculating...';

  try {
    const resp = await fetch("/api/monetization", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        niche: document.getElementById("calc-niche").value,
        followers: parseInt(document.getElementById("calc-followers").value) || 0,
        yt_views: parseInt(document.getElementById("calc-yt").value) || 0,
        fb_views: parseInt(document.getElementById("calc-tt").value) || 0,
        ig_views: parseInt(document.getElementById("calc-ig").value) || 0,
        x_views: parseInt(document.getElementById("calc-x").value) || 0,
      }),
    });
    const data = await resp.json();

    let html = `
      <div class="earnings-total">
        <div class="amount">$${data.total_monthly.toFixed(2)}</div>
        <div class="period">estimated monthly earnings</div>
        <div style="font-size:0.85rem;color:var(--text-dim);margin-top:4px;">
          ~$${data.total_annual.toFixed(0)}/year
        </div>
      </div>
      <div class="earnings-breakdown">
    `;

    const p = data.platforms;
    html += `<div class="earnings-row"><span>YouTube Shorts (${p.youtube.views.toLocaleString()} views)</span><span class="amount">$${p.youtube.earnings.toFixed(2)}</span></div>`;
    if (p.youtube.warning) {
      html += `<div class="earnings-row" style="font-size:0.75rem;color:var(--text-dim);"><span>⚠️ ${p.facebook.warning}</span><span></span></div>`;
    }
    html += `<div class="earnings-row"><span>Facebook (${p.facebook.views.toLocaleString()} views)</span><span class="amount">$${p.facebook.earnings.toFixed(2)}</span></div>`;
    if (p.facebook.warning) {
      html += `<div class="earnings-row warning" style="font-size:0.75rem;"><span>⚠️ ${p.facebook.warning}</span><span></span></div>`;
    }
    html += `<div class="earnings-row"><span>Instagram (brand deals)</span><span class="amount">$${p.instagram.earnings.toFixed(2)}</span></div>`;
    html += `<div class="earnings-row"><span>X (Twitter)</span><span class="amount">$${p.x.earnings.toFixed(2)}</span></div>`;
    html += `<div class="earnings-row" style="border-bottom:none;font-weight:600;"><span>Platform Subtotal</span><span class="amount">$${data.platform_total.toFixed(2)}</span></div>`;
    html += `</div>`;

    if (data.additional_revenue) {
      html += `<h3 style="color:var(--text-dim);font-size:0.9rem;margin:12px 0 8px;">Additional Revenue Streams</h3>`;
      Object.entries(data.additional_revenue).forEach(([key, val]) => {
        html += `<div class="earnings-row"><span>${val.description}</span><span class="amount">$${val.estimated_monthly.toFixed(2)}</span></div>`;
      });
      html += `<div class="earnings-row" style="border-bottom:none;font-weight:600;"><span>Additional Subtotal</span><span class="amount">$${data.additional_total.toFixed(2)}</span></div>`;
    }

    html += `<div class="earnings-strategy"><strong>Strategy:</strong><ul class="earnings-strategy">`;
    data.strategy.forEach(s => html += `<li>${escapeHtml(s)}</li>`);
    html += `</ul></div>`;

    resultDiv.innerHTML = html;
  } catch (e) {
    resultDiv.innerHTML = `<div class="error">Error: ${e.message}</div>`;
  }
}

// ═══ RPM Comparison ════════════════════════════════════════════════
async function loadRpmComparison() {
  try {
    const resp = await fetch("/api/niche-rpm");
    const data = await resp.json();
    const container = document.getElementById("rpm-comparison");
    if (!container) return;

    let html = `<table class="rpm-table"><thead><tr>
      <th>Niche</th><th>YouTube RPM</th><th>YouTube /1M views</th>
      <th>Facebook AI RPM</th><th>Facebook /1M views</th>
    </tr></thead><tbody>`;
    data.niches.forEach(n => {
      html += `<tr>
        <td class="niche-name">${n.niche}</td>
        <td>$${n.youtube_rpm.toFixed(3)}</td>
        <td>$${n.youtube_per_million.toFixed(2)}</td>
        <td>$${n.facebook_ai_rpm.toFixed(4)}</td>
        <td>$${n.facebook_per_million.toFixed(2)}</td>
      </tr>`;
    });
    html += `</tbody></table>`;
    container.innerHTML = html;
  } catch (e) {
    console.error("RPM load failed:", e);
  }
}

// ═══ Strategy Guide ════════════════════════════════════════════════
async function loadStrategy() {
  try {
    const resp = await fetch("/api/strategy");
    const data = await resp.json();
    const container = document.getElementById("strategy-content");
    if (!container) return;

    let html = "";

    // Key principles
    html += `<div class="strategy-section"><h3>Key Principles</h3><ul class="principles">`;
    data.key_principles.forEach(p => html += `<li>${escapeHtml(p)}</li>`);
    html += `</ul></div>`;

    // Niche rankings
    html += `<div class="strategy-section"><h3>Niche Rankings (by RPM)</h3>`;
    data.niche_rankings.forEach(n => {
      html += `<div class="niche-card">
        <div class="niche-title">${n.niche}</div>
        <div class="niche-meta">YouTube RPM: $${n.yt_rpm}/1K views | Difficulty: ${n.difficulty} | Audience: ${n.audience}</div>
        <div class="niche-ideas">Content ideas: ${n.content_ideas.join(" • ")}</div>
        <div class="niche-ideas">Best provider: ${n.best_provider}</div>
      </div>`;
    });
    html += `</div>`;

    // Posting frequency
    html += `<div class="strategy-section"><h3>Posting Frequency</h3>`;
    Object.entries(data.posting_frequency).forEach(([platform, freq]) => {
      html += `<div class="niche-card">
        <div class="niche-title">${platform}</div>
        <div class="niche-meta">Min: ${freq.min} | Ideal: ${freq.ideal} | Max: ${freq.max}</div>
      </div>`;
    });
    html += `</div>`;

    // Posting times
    html += `<div class="strategy-section"><h3>Best Posting Times</h3>`;
    Object.entries(data.posting_times).forEach(([platform, times]) => {
      html += `<div class="niche-card"><div class="niche-title">${platform}</div>
        <div class="niche-meta">Best times: ${times.join(", ")}</div></div>`;
    });
    html += `</div>`;

    // Batch workflow
    html += `<div class="strategy-section"><h3>${data.batch_workflow.name}</h3>
      <ul class="principles">`;
    data.batch_workflow.steps.forEach(s => html += `<li>${escapeHtml(s)}</li>`);
    html += `</ul>
      <div class="niche-meta" style="margin-top:8px;">
        Total weekly time: ${data.batch_workflow.total_weekly_time} |
        Output: ${data.batch_workflow.output}
      </div></div>`;

    container.innerHTML = html;
  } catch (e) {
    console.error("Strategy load failed:", e);
  }
}

// ═══ Platform Tips ═════════════════════════════════════════════════
async function loadPlatformTips() {
  try {
    const resp = await fetch("/api/platform-tips-all");
    const data = await resp.json();
    const container = document.getElementById("platform-tips-content");
    if (!container) return;

    let html = "";
    Object.entries(data).forEach(([platform, tips]) => {
      html += `<div class="platform-tip-card">
        <h4>${platform}</h4>
        <div class="tip-row"><span class="tip-label">Format:</span> ${tips.format}</div>
        <div class="tip-row"><span class="tip-label">Hook:</span> ${tips.hook}</div>
        <div class="tip-row"><span class="tip-label">Description:</span> ${tips.description}</div>
        <div class="tip-row"><span class="tip-label">Best content:</span> ${tips.best_content}</div>
        <div class="tip-row"><span class="tip-label">Monetization:</span> ${tips.monetization}</div>
        <div class="tip-row"><span class="tip-label">Pro tips:</span></div>
        <ul style="font-size:0.8rem;padding-left:20px;">`;
      tips.tips.forEach(t => html += `<li>${escapeHtml(t)}</li>`);
      html += `</ul></div>`;
    });
    container.innerHTML = html;
  } catch (e) {
    console.error("Platform tips load failed:", e);
  }
}

// ═══ History ═══════════════════════════════════════════════════════
async function loadHistory() {
  try {
    const resp = await fetch("/api/history");
    const items = await resp.json();
    const container = document.getElementById("history-list");
    if (!container) return;
    if (!items.length) {
      container.innerHTML = '<p class="placeholder">No videos generated yet.</p>';
      return;
    }
    container.innerHTML = items.map(item => {
      const date = new Date(item.timestamp).toLocaleString();
      const platforms = (item.posted_to || []).map(p => `<span class="tag">${p}</span>`).join("");
      const videoLink = item.local_path
        ? `/storage/${item.local_path.split("/").pop()}`
        : item.video_url;
      return `
        <div class="history-item">
          <div class="h-prompt">${escapeHtml(item.prompt.slice(0, 100))}${item.prompt.length > 100 ? '...' : ''}</div>
          <div class="h-meta">
            <span>📅 ${date}</span>
            <span>🎬 ${item.provider}</span>
            ${item.title ? `<span>📝 ${escapeHtml(item.title)}</span>` : ""}
            ${videoLink ? `<a href="${videoLink}" target="_blank" style="color:var(--accent)">▶ Watch</a>` : ""}
          </div>
          ${platforms ? `<div class="h-platforms">${platforms}</div>` : ""}
        </div>`;
    }).join("");
  } catch (e) {
    console.error("History load failed:", e);
  }
}

async function clearHistory() {
  if (!confirm("Clear all history?")) return;
  await fetch("/api/history", { method: "DELETE" });
  loadHistory();
}

// ═══ Discover Tab: Content Ideas ════════════════════════════════════
async function loadCategories() {
  try {
    const resp = await fetch("/api/categories");
    const data = await resp.json();
    const select = document.getElementById("discover-category");
    if (!select) return;
    Object.entries(data.categories).forEach(([key, val]) => {
      const opt = document.createElement("option");
      opt.value = key;
      opt.textContent = `${val.icon} ${key} — ${val.description}`;
      select.appendChild(opt);
    });
  } catch (e) { console.error("Categories load failed:", e); }
}

async function loadIdeas(category) {
  try {
    const url = category ? `/api/ideas?category=${encodeURIComponent(category)}` : "/api/ideas";
    const resp = await fetch(url);
    const data = await resp.json();
    renderIdeas(data.ideas);
  } catch (e) { console.error("Ideas load failed:", e); }
}

async function loadTrendingIdeas() {
  try {
    const resp = await fetch("/api/ideas/trending");
    const data = await resp.json();
    renderIdeas(data.ideas);
  } catch (e) { console.error("Trending ideas load failed:", e); }
}

async function loadBestEarningIdeas() {
  try {
    const resp = await fetch("/api/ideas/best-earning");
    const data = await resp.json();
    renderIdeas(data.ideas);
  } catch (e) { console.error("Best earning ideas load failed:", e); }
}

async function loadRandomIdea() {
  try {
    const resp = await fetch("/api/ideas/random");
    const data = await resp.json();
    showIdeaDetail(data);
  } catch (e) { console.error("Random idea load failed:", e); }
}

function renderIdeas(ideas) {
  const container = document.getElementById("discover-ideas");
  if (!container) return;
  if (!ideas || !ideas.length) {
    container.innerHTML = '<p class="placeholder">No ideas found.</p>';
    return;
  }
  container.innerHTML = ideas.map(idea => `
    <div class="idea-card" onclick="showIdeaById('${idea.id}')">
      <div class="idea-cat">${idea.category}${idea.trending ? ' 🔥' : ''}</div>
      <div class="idea-title">${escapeHtml(idea.title)}</div>
      <div class="idea-desc">${escapeHtml(idea.description.slice(0, 120))}${idea.description.length > 120 ? '...' : ''}</div>
      <div class="idea-meta">
        <span class="score">📊 ${idea.viral_score}/100</span>
        <span class="platforms">📍 ${idea.best_platforms.join(', ')}</span>
        <span class="niche">💰 ${idea.monetization_niche}</span>
      </div>
    </div>
  `).join("");
}

async function showIdeaById(ideaId) {
  try {
    const resp = await fetch(`/api/ideas/${ideaId}`);
    const data = await resp.json();
    showIdeaDetail(data);
  } catch (e) { console.error("Idea detail load failed:", e); }
}

function showIdeaDetail(data) {
  const card = document.getElementById("idea-detail-card");
  const content = document.getElementById("idea-detail-content");
  const title = document.getElementById("idea-detail-title");
  const idea = data.idea || data;
  title.textContent = idea.title || "Idea Details";

  let html = "";
  if (idea.description) {
    html += `<div class="idea-detail-section"><h3>What Happens</h3>
      <p style="font-size:0.88rem;">${escapeHtml(idea.description)}</p></div>`;
  }
  if (data.enhanced_prompt) {
    html += `<div class="idea-detail-section"><h3>Physics-Accurate Prompt (ready to generate)</h3>
      <div class="idea-prompt-box">${escapeHtml(data.enhanced_prompt)}</div></div>`;
  } else if (idea.prompt) {
    html += `<div class="idea-detail-section"><h3>Prompt (ready to generate)</h3>
      <div class="idea-prompt-box">${escapeHtml(idea.prompt)}</div></div>`;
  }
  if (data.physics_notes && data.physics_notes.length) {
    html += `<div class="idea-detail-section"><h3>Physics Constraints Applied</h3>
      <ul class="idea-physics-list">`;
    data.physics_notes.forEach(n => html += `<li>${escapeHtml(n)}</li>`);
    html += `</ul>`;
    if (idea.physics_principles) {
      html += `<p style="font-size:0.8rem;color:var(--text-dim);margin-top:8px;">
        Principles: ${idea.physics_principles.join(', ')}</p>`;
    }
    html += `</div>`;
  }
  if (data.viral_score) {
    const s = data.viral_score;
    html += `<div class="idea-detail-section"><h3>Viral Score: ${s.total_score}/100</h3>
      <div class="score-grade">${s.grade}</div>
      <div class="score-breakdown">
        <div class="score-bar-item"><div class="label">Hook</div><div class="value">${s.breakdown.hook_strength}</div>
          <div class="score-bar"><div class="score-bar-fill" style="width:${s.breakdown.hook_strength}%;background:var(--accent);"></div></div></div>
        <div class="score-bar-item"><div class="label">Emotion</div><div class="value">${s.breakdown.emotional_trigger}</div>
          <div class="score-bar"><div class="score-bar-fill" style="width:${s.breakdown.emotional_trigger}%;background:var(--accent);"></div></div></div>
        <div class="score-bar-item"><div class="label">Novelty</div><div class="value">${s.breakdown.visual_novelty}</div>
          <div class="score-bar"><div class="score-bar-fill" style="width:${s.breakdown.visual_novelty}%;background:var(--accent);"></div></div></div>
        <div class="score-bar-item"><div class="label">Trend</div><div class="value">${s.breakdown.trend_alignment}</div>
          <div class="score-bar"><div class="score-bar-fill" style="width:${s.breakdown.trend_alignment}%;background:var(--accent);"></div></div></div>
        <div class="score-bar-item"><div class="label">Retention</div><div class="value">${s.breakdown.retention_design}</div>
          <div class="score-bar"><div class="score-bar-fill" style="width:${s.breakdown.retention_design}%;background:var(--accent);"></div></div></div>
      </div></div>`;
  }
  if (data.platform_recommendations && data.platform_recommendations.length) {
    html += `<div class="idea-detail-section"><h3>Where to Post (ranked)</h3>`;
    data.platform_recommendations.forEach(rec => {
      const info = rec.platform_info || {};
      html += `<div class="platform-rec-card">
        <div class="rank-num">${rec.rank}</div>
        <div class="rec-info">
          <div class="rec-platform">${info.icon || ''} ${info.name || rec.platform}</div>
          <div class="rec-score">Score: ${rec.score}/10 | Monetization rank: #${rec.monetization_rank}</div>
          <div class="rec-reasoning">${escapeHtml(rec.reasoning)}</div>
          <div class="rec-monetization">${escapeHtml(info.monetization || '')}</div>
        </div></div>`;
    });
    html += `</div>`;
  } else if (idea.best_platforms) {
    html += `<div class="idea-detail-section"><h3>Where to Post</h3>
      <p style="font-size:0.85rem;color:var(--accent);">📍 ${idea.best_platforms.join(' → ')}</p>`;
    if (idea.platform_reasoning) {
      Object.entries(idea.platform_reasoning).forEach(([platform, reason]) => {
        html += `<p style="font-size:0.8rem;color:var(--text-dim);margin-top:4px;">
          <strong>${platform}:</strong> ${escapeHtml(reason)}</p>`;
      });
    }
    html += `</div>`;
  }
  if (idea.series_potential) {
    html += `<div class="idea-detail-section"><h3>Series Potential</h3>
      <p style="font-size:0.85rem;">${escapeHtml(idea.series_potential)}</p></div>`;
  }
  if (data.recommended_provider) {
    html += `<div class="idea-detail-section"><h3>Recommended AI Provider</h3>
      <p style="font-size:0.85rem;color:var(--accent);">🎬 ${data.recommended_provider}</p></div>`;
  }
  if (idea.estimated_rpm) {
    html += `<div class="idea-detail-section"><h3>Earning Potential</h3>
      <p style="font-size:0.85rem;">Niche: ${idea.monetization_niche} | Est. RPM: $${idea.estimated_rpm}/1K views on YouTube</p></div>`;
  }
  const promptToUse = data.enhanced_prompt || idea.prompt || "";
  const providerToUse = data.recommended_provider || "veo";
  const ideaTitle = idea.title || "";
  const ideaCategory = idea.category || "";
  const ideaDesc = idea.description || "";
  const ideaTags = (idea.tags || []).join(',');
  const ideaScore = data.viral_score ? data.viral_score.total_score : (idea.viral_score || null);
  html += `<button class="btn btn-secondary idea-content-pack-btn"
    onclick="loadContentPack('${escapeAttr(ideaTitle)}', '${escapeAttr(ideaCategory)}', '${escapeAttr(ideaDesc)}', '${escapeAttr(ideaTags)}', ${ideaScore || 'null'})"
    style="width:100%;margin-bottom:8px;">
    📝 Generate Title + Hashtags + Captions
  </button>
  <div id="content-pack-result" class="idea-detail-section"></div>`;
  html += `<button class="btn btn-primary idea-generate-btn"
    onclick="generateFromIdea('${escapeAttr(promptToUse)}', '${providerToUse}', '${escapeAttr(ideaTitle)}', '${escapeAttr(ideaTags)}')">
    🎨 Generate This Video →
  </button>`;
  content.innerHTML = html;
  card.classList.remove("hidden");
  card.scrollIntoView({ behavior: "smooth" });
}

async function loadContentPack(topic, category, description, tags, score) {
  const container = document.getElementById("content-pack-result");
  if (!container) return;
  container.innerHTML = '<span class="spinner"></span> Generating titles & hashtags...';
  try {
    const tagList = tags ? tags.split(',').filter(t => t.trim()) : [];
    const resp = await fetch("/api/content-pack", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        topic, category, description,
        tags: tagList,
        platforms: ["youtube", "instagram", "x", "facebook"],
        viral_score: score,
      }),
    });
    const pack = await resp.json();
    if (pack.error) {
      container.innerHTML = `<div class="error">${pack.error}</div>`;
      return;
    }
    let html = '<h3>📋 Content Pack</h3>';
    // Titles
    html += '<div class="content-pack-section"><strong>🎬 Viral Titles:</strong><ul>';
    pack.titles.forEach((t, i) => {
      html += `<li style="margin:4px 0;"><label><input type="radio" name="title-choice" value="${escapeAttr(t)}" ${i === 0 ? 'checked' : ''} onclick="document.getElementById('post-title').value='${escapeAttr(t)}'"> ${escapeHtml(t)}</label></li>`;
    });
    html += '</ul></div>';
    // Hashtags
    html += '<div class="content-pack-section"><strong>#️⃣ Hashtags (copy-paste):</strong>';
    html += `<div class="hashtag-box" style="background:var(--bg-card);padding:8px;border-radius:8px;margin:4px 0;font-size:0.8rem;word-break:break-all;">${escapeHtml(pack.hashtags.copy_paste)}</div>`;
    html += '</div>';
    // Platform writeups (rich content per platform)
    html += '<div class="content-pack-section"><strong>📝 Writeups by Platform:</strong>';
    if (pack.writeups) {
      Object.entries(pack.writeups).forEach(([platform, wu]) => {
        const icon = platform === 'youtube' ? '📺' : platform === 'instagram' ? '📷' : platform === 'x' ? '🐦' : '👍';
        const typeLabel = wu.type ? ` (${wu.type.replace(/_/g, ' ')})` : '';
        html += `<div style="margin:8px 0;">
          <div style="font-weight:bold;color:var(--accent);font-size:0.85rem;">${icon} ${platform.toUpperCase()}${typeLabel}</div>`;
        // X thread
        if (wu.thread) {
          wu.thread.forEach((tweet, i) => {
            html += `<div style="background:var(--bg-card);padding:6px 8px;border-radius:6px;margin:4px 0;font-size:0.8rem;white-space:pre-wrap;"><strong>${i+1}/${wu.thread.length}:</strong> ${escapeHtml(tweet)}</div>`;
          });
        }
        // YouTube chapters
        if (wu.chapters) {
          html += '<div style="font-size:0.8rem;margin:4px 0;">⏱️ Chapters:</div><ul style="font-size:0.8rem;">';
          wu.chapters.forEach(ch => { html += `<li>${escapeHtml(ch)}</li>`; });
          html += '</ul>';
        }
        // Instagram carousel
        if (wu.carousel_slides) {
          html += '<div style="font-size:0.8rem;margin:4px 0;">📷 Carousel slides:</div><ol style="font-size:0.8rem;">';
          wu.carousel_slides.forEach(s => { html += `<li>${escapeHtml(s)}</li>`; });
          html += '</ol>';
        }
        // Full text (always present)
        html += `<div style="background:var(--bg-card);padding:8px;border-radius:8px;font-size:0.8rem;white-space:pre-wrap;max-height:120px;overflow-y:auto;margin-top:4px;">${escapeHtml(wu.full_text)}</div>`;
        html += '</div>';
      });
    } else {
      Object.entries(pack.captions).forEach(([platform, caption]) => {
        const icon = platform === 'youtube' ? '📺' : platform === 'instagram' ? '📷' : platform === 'x' ? '🐦' : '👍';
        html += `<div style="margin:8px 0;">
          <div style="font-weight:bold;color:var(--accent);font-size:0.85rem;">${icon} ${platform.toUpperCase()}</div>
          <div style="background:var(--bg-card);padding:8px;border-radius:8px;font-size:0.8rem;white-space:pre-wrap;max-height:120px;overflow-y:auto;">${escapeHtml(caption)}</div>
        </div>`;
      });
    }
    html += '</div>';
    // Hooks
    if (pack.hooks && pack.hooks.length) {
      html += '<div class="content-pack-section"><strong>🎣 Hook Variations (first 3 sec):</strong><ul>';
      pack.hooks.forEach(h => {
        html += `<li style="margin:4px 0;font-size:0.85rem;">${escapeHtml(h)}</li>`;
      });
      html += '</ul></div>';
    }
    container.innerHTML = html;
  } catch (e) {
    container.innerHTML = `<div class="error">Error: ${e.message}</div>`;
  }
}

function generateFromIdea(prompt, provider, title, tags) {
  document.querySelector('.tab-btn[data-tab="create"]').click();
  document.getElementById("prompt").value = prompt;
  document.getElementById("provider").value = provider;
  document.getElementById("post-title").value = title;
  document.getElementById("post-tags").value = tags;
  document.getElementById("auto-enhance").checked = false;
  setTimeout(() => generateVideo(), 500);
}

// ═══ Custom Idea Generator & NCERT Topics ════════════════════════════
async function generateCustomIdea() {
  const topic = document.getElementById("custom-topic").value.trim();
  if (!topic) { alert("Enter a topic first"); return; }

  const category = document.getElementById("custom-category").value;
  const resultDiv = document.getElementById("custom-idea-result");
  resultDiv.classList.remove("hidden");
  resultDiv.innerHTML = '<span class="spinner"></span> Generating idea...';

  try {
    const resp = await fetch("/api/generate-idea", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, category }),
    });
    const data = await resp.json();

    if (data.error) {
      resultDiv.innerHTML = `<div class="error">${data.error}</div>`;
      return;
    }

    // Show the generated idea using the same detail view
    showIdeaDetail(data);
    resultDiv.innerHTML = `<div class="status-msg success">✅ Idea generated! See details above.</div>`;
  } catch (e) {
    resultDiv.innerHTML = `<div class="error">Error: ${e.message}</div>`;
  }
}

async function loadNcertTopics() {
  const subject = document.getElementById("ncert-subject").value;
  const container = document.getElementById("ncert-topics-list");
  if (!container) return;

  try {
    const resp = await fetch(`/api/ncert-topics?subject=${subject}`);
    const data = await resp.json();

    let html = "";
    Object.entries(data).forEach(([subjectKey, chapters]) => {
      html += `<h3 style="color:var(--text-dim);font-size:0.9rem;margin:8px 0;">${subjectKey} — ${chapters.length} chapters</h3>`;
      chapters.forEach((chapter, idx) => {
        html += `<div class="ncert-chapter-item" onclick="generateNcertIdea('${escapeAttr(chapter)}', '${subject}')">
          <span class="chapter-num">${idx + 1}</span>
          <span class="chapter-name">${escapeHtml(chapter)}</span>
          <span class="chapter-arrow">→</span>
        </div>`;
      });
    });
    container.innerHTML = html;
  } catch (e) {
    container.innerHTML = `<p class="placeholder">Error loading topics: ${e.message}</p>`;
  }
}

async function generateNcertIdea(chapter, subject) {
  // Show loading in the detail card
  const card = document.getElementById("idea-detail-card");
  const content = document.getElementById("idea-detail-content");
  const title = document.getElementById("idea-detail-title");
  title.textContent = "Generating idea...";
  content.innerHTML = '<span class="spinner"></span> Generating idea for: ' + escapeHtml(chapter);
  card.classList.remove("hidden");
  card.scrollIntoView({ behavior: "smooth" });

  try {
    const resp = await fetch("/api/ncert-generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chapter, subject }),
    });
    const data = await resp.json();

    if (data.error) {
      content.innerHTML = `<div class="error">${data.error}</div>`;
      return;
    }

    showIdeaDetail(data);
  } catch (e) {
    content.innerHTML = `<div class="error">Error: ${e.message}</div>`;
  }
}

// ═══ Helpers ═══════════════════════════════════════════════════════
function showMsg(elementId, msg, type) {
  const el = document.getElementById(elementId);
  if (!el) return;
  el.className = `status-msg ${type}`;
  el.textContent = msg;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text || "";
  return div.innerHTML;
}

function escapeAttr(text) {
  return (text || "").replace(/'/g, "\\'").replace(/\n/g, "\\n");
}

// ═══ Social Media OS Integration ═══════════════════════════════════════
async function sendToSocialOS() {
  if (!currentVideo) {
    showMsg("social-os-status", "Generate a video first.", "error");
    return;
  }

  const platforms = Array.from(document.querySelectorAll(".platform-check input:checked"))
    .map(cb => cb.value);
  if (!platforms.length) {
    showMsg("social-os-status", "Select at least one platform.", "error");
    return;
  }

  const btn = document.getElementById("btn-social-os");
  const status = document.getElementById("social-os-status");
  btn.disabled = true;
  status.className = "status-msg loading";
  status.innerHTML = '<span class="spinner"></span> Sending to Social Media OS...';

  const title = document.getElementById("post-title").value || "AI Generated Video";
  const description = document.getElementById("post-desc").value;
  const tags = document.getElementById("post-tags").value.split(",").map(t => t.trim()).filter(Boolean);

  try {
    const resp = await fetch("/api/social-os/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        video_url: currentVideo.url,
        topic: title,
        platforms,
        description,
        tags,
        caption: description || title,
      }),
    });

    const data = await resp.json();

    if (data.success) {
      status.className = "status-msg success";
      status.innerHTML = `✅ ${data.message}`;
    } else if (data.status === "disabled") {
      status.className = "status-msg error";
      status.innerHTML = `⚠️ ${data.message}<br><small>Go to Settings → Social Media OS to configure.</small>`;
    } else {
      status.className = "status-msg error";
      status.textContent = `❌ ${data.message}`;
    }
  } catch (e) {
    status.className = "status-msg error";
    status.textContent = `Error: ${e.message}`;
  } finally {
    btn.disabled = false;
  }
}

async function testSocialOSConnection() {
  const status = document.getElementById("social-os-test-result");
  const indicator = document.getElementById("social-os-indicator");
  status.className = "status-msg loading";
  status.innerHTML = '<span class="spinner"></span> Testing connection...';
  indicator.textContent = "🟡 Testing...";

  try {
    const resp = await fetch("/api/social-os/status");
    const data = await resp.json();

    if (data.reachable) {
      status.className = "status-msg success";
      status.textContent = `✅ ${data.message}`;
      indicator.innerHTML = "🟢 <strong>Connected</strong> — Social Media OS is reachable";
    } else if (!data.configured) {
      status.className = "status-msg error";
      status.textContent = `⚠️ ${data.message}`;
      indicator.innerHTML = "🔴 <strong>Not configured</strong> — Set SOCIAL_OS_URL and SOCIAL_OS_API_KEY in .env";
    } else {
      status.className = "status-msg error";
      status.textContent = `❌ ${data.message}`;
      indicator.innerHTML = "🟡 <strong>Configured but unreachable</strong>";
    }
  } catch (e) {
    status.className = "status-msg error";
    status.textContent = `Error: ${e.message}`;
    indicator.textContent = "❌ Error checking connection";
  }
}

async function loadSocialOSStatus() {
  const indicator = document.getElementById("social-os-indicator");
  if (!indicator) return;

  try {
    const resp = await fetch("/api/social-os/status");
    const data = await resp.json();

    if (data.reachable) {
      indicator.innerHTML = "🟢 <strong>Connected</strong> — Social Media OS is reachable";
    } else if (!data.configured) {
      indicator.innerHTML = "⚪ <strong>Not configured</strong> — Set env vars in .env file";
    } else {
      indicator.innerHTML = "🟡 <strong>Configured but unreachable</strong>";
    }
  } catch (e) {
    indicator.textContent = "⚪ Unable to check";
  }
}

async function loadConfigSummary() {
  const container = document.getElementById("config-summary");
  if (!container) return;

  try {
    const resp = await fetch("/api/status");
    const data = await resp.json();

    let html = '<div style="display:grid;gap:0.5rem;">';

    // Video providers
    html += '<h3 style="font-size:0.95rem;margin:0.5rem 0 0.25rem;">Video Providers</h3>';
    data.video_providers.forEach(p => {
      const icon = p.configured ? "✅" : "❌";
      html += `<div style="display:flex;justify-content:space-between;padding:0.3rem 0;border-bottom:1px solid rgba(255,255,255,0.05);">
        <span>${icon} ${p.name}</span>
        <span style="color:rgba(255,255,255,0.5);font-size:0.85rem;">${p.configured ? "Ready" : "Not configured"}</span>
      </div>`;
    });

    // Social platforms
    html += '<h3 style="font-size:0.95rem;margin:1rem 0 0.25rem;">Social Platforms</h3>';
    for (const [name, configured] of Object.entries(data.social_platforms)) {
      const icon = configured ? "✅" : "❌";
      html += `<div style="display:flex;justify-content:space-between;padding:0.3rem 0;border-bottom:1px solid rgba(255,255,255,0.05);">
        <span>${icon} ${name.charAt(0).toUpperCase() + name.slice(1)}</span>
        <span style="color:rgba(255,255,255,0.5);font-size:0.85rem;">${configured ? "Ready" : "Not configured"}</span>
      </div>`;
    }

    // Social OS
    if (data.social_os) {
      html += '<h3 style="font-size:0.95rem;margin:1rem 0 0.25rem;">Social Media OS</h3>';
      const osStatus = data.social_os.connected ? "🟢 Connected" : "⚪ Not configured";
      html += `<div style="display:flex;justify-content:space-between;padding:0.3rem 0;">
        <span>${osStatus}</span>
        <span style="color:rgba(255,255,255,0.5);font-size:0.85rem;">${data.social_os.enabled ? "Enabled" : "Disabled"}</span>
      </div>`;
    }

    html += '</div>';
    container.innerHTML = html;
  } catch (e) {
    container.innerHTML = `<div class="error">Error loading config: ${e.message}</div>`;
  }
}
