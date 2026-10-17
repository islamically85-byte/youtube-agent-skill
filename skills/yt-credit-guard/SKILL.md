---
name: yt-credit-guard
description: Enforce zero-credit production budgets, protect depleting third-party quotas (such as vidIQ), and route to free-first offline workflows.
---

# yt-credit-guard — Zero-Credit Quota Guard & Paid-Service Protection

`yt-credit-guard` guarantees that YouTube Agent Studio operations remain 100% free-first. It blocks automated deductions against metered third-party services (vidIQ, ElevenLabs, OpenAI DALL-E) and routes creators to local, offline alternatives.

## The Zero-Credit Production Policy

1. **Default Budget = 0 Credits**:
   - The studio core operates without requiring paid subscriptions, YouTube API quotas, or metered third-party credits.
   - Any metered operation requires explicit creator consent (`--consent yes`).

2. **Connected Quota Depletion Protection**:
   - Live connected quotas are strictly guarded.
   - *Example Finding*: A connected vidIQ account had 2/150 credits remaining on 2026-10-16 (renewing 2026-11-16). Standard competitor research calls cost 5 credits.
   - Calling an API requiring 5 credits with only 2 credits remaining causes API failure and burns remaining quota. `credit_guard.py` blocks this before execution.

3. **Free-First Fallbacks**:

| Metered / Paid Tool | Standard Cost | Risk / Constraint | Free-First Zero-Credit Fallback |
| :--- | :--- | :--- | :--- |
| **vidIQ Competitor Research** | 5 credits | Depletes quota, requires live login | Offline `yt-viral`, `yt-seo`, manual YouTube autocomplete |
| **vidIQ AI Thumbnail** | 15 credits | High credit consumption | Permissive stock stills (Pexels, Pixabay) + `yt-package` pairing |
| **ElevenLabs Voiceover** | Metered tokens | Paid API subscription | Well-recorded human voiceover (preferred) or verified local TTS |
| **Paid Stock / DALL-E** | Paid credits | Commercial licensing ambiguities | Pexels, Pixabay, Mixkit, CC0 stock video |

## CLI Enforcement Guide

### Check If an Operation Is Authorized
```bash
python3 shared/scripts/credit_guard.py --tool vidiq --action competitor_research
```
*Output (Blocked by default):*
```
🚫 [CREDIT-GUARD BLOCKED] Operation 'competitor_research' on 'vidiq' requires 5 credits, but current budget is 0 credits and explicit user consent was not provided.
Free-first alternative: Use local offline yt-seo, yt-package, yt-audit, and manual YouTube search/autocomplete.
To proceed with paid credits, the user must explicitly approve with --consent yes.
```

### Checking Known Tool Balance
```bash
python3 shared/scripts/credit_guard.py --tool vidiq --action competitor_research --consent yes --budget 5 --balance 2
```
*Output (Insufficient Quota Prevention):*
```
❌ [CREDIT-GUARD EXHAUSTED] Quota insufficient for 'vidiq'. Requested: 5 credits, but current live balance is only 2 credits. Free-first alternative: Use local offline yt-seo, yt-package, yt-audit, and manual YouTube search/autocomplete.
```

### Structured Output for Automation
```bash
python3 shared/scripts/credit_guard.py --tool vidiq --action keyword_expansion --json
```
