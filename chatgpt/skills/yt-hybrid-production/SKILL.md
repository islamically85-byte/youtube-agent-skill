---
name: yt-hybrid-production
description: Production orchestrator for hybrid provider resolution, credit budget verification, and automatic fallback from paid services to free local tools.
---

# yt-hybrid-production — Hybrid Provider Resolution & Credit Guard v3.0

`yt-hybrid-production` resolves the production tier for each YouTube video stage (scriptwriting, voiceover, stock footage, rendering, and QA). It enforces a strict **Zero-Credit Baseline** (`credit_budget = 0`), probes connected provider states, and switches seamlessly to local open-source tools when paid APIs are unconfigured or unfunded.

## Supported Provider States

| State | Definition | Fallback Action |
|---|---|---|
| `AVAILABLE` | Provider authenticated, sufficient credits/quota, language supported | Use provider if within authorized budget |
| `NO_CREDITS` | Balance = 0 or below required operation cost | Automatically fall back to free tier / local tool |
| `NOT_CONNECTED` | API key or integration absent | Use free baseline without raising errors |
| `UNSUPPORTED_LANGUAGE` | Service lacks native support (e.g. Urdu Nastaliq / audio) | Fall back to Piper Urdu or human recording |
| `RATE_LIMITED` | Quota exceeded or temporary throttling | Fall back to deterministic local processing |

## Core Principles

1. **Credit Budget Gate**: Never charge any third-party account without explicit, prior user confirmation with cost estimation.
2. **Deterministic Ledger**: Every routing decision is recorded in `provider_decisions.json`.
3. **Zero-Budget Guarantee**: Full 6-7 minute documentaries can be produced without external paid subscriptions.

## CLI Usage

Inspect and resolve provider status:

```bash
# Resolve production tier with default zero budget
python3 scripts/provider_engine.py --status

# Output auditable decision ledger in JSON format
python3 scripts/provider_engine.py --status --json
```

## Python Integration

```python
from scripts.provider_engine import ProviderEngine, ProviderState

engine = ProviderEngine(credit_budget=0)
plan = engine.resolve_pipeline_plan(language="ur", duration_target_sec=390.0)
print(plan["voiceover_provider"])  # "piper_urdu_local" or "human_recording_guide"
print(plan["render_engine"])       # "ffmpeg_local_free"
```
