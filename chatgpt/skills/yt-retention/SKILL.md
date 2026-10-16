---
name: yt-retention
description: >-
  Diagnose audience drop-off from YouTube Studio retention CSV exports, pinpointing hook leaks,
  specific cliff moments, and middle pacing slides with aligned transcript dialogue.
---

# yt-retention — Audience Retention Diagnostic Engine

Audience retention data is YouTube's most unfiltered creator feedback. This skill diagnoses exactly where viewers abandon your videos and provides a single, high-leverage corrective action.

## Tools Available
Run the retention analyzer in this directory:
```bash
python3 retention.py retention.csv --duration 600
python3 retention.py retention.csv --transcript transcript.srt
python3 retention.py retention.csv --json
```

Export path in YouTube Studio: `Analytics` -> Select Video -> `Engagement` -> `Audience retention chart` -> `Export (CSV)`.

## Three Distinct Diagnostic Phenomena

### 1. The Hook Leak (First 30 Seconds)
- **Healthy**: Under 25% drop. (Viewer expectation matched the title/thumbnail promise).
- **Leaking**: 25%–40% drop. (Viewer experienced friction: fluff intro, slow start, mismatched topic).
- **Severe**: > 40% drop. (Viewer felt misled by the click packaging or bored by channel branding).
- *Correction*: Never re-edit the body. Rewrite the first 15 seconds using `/yt-script`.

### 2. Cliffs (Steep Local Drops > 0.8%)
- Abrupt drops indicate a specific moment of friction:
  - Boring tangents or over-explained details.
  - Jarring audio/visual transitions or unannounced sponsor breaks.
  - Discarded premises or premature answers to the central curiosity question.
- *Correction*: With `--transcript`, the tool highlights the exact words spoken when viewers left.

### 3. The Slide (Pacing Bleed Across the Body)
- A steady downward slope across the middle section indicates pacing exhaustion, not content failure.
- *Correction*: Tighten runtime with `/yt-edit`. Cut redundant examples; do not rewrite the entire topic.

### 4. Rewatch Spikes & Retention > 100%
- Common on Shorts or high-density tutorial timestamps. The tool detects these loop points and flags them as high-interest visual anchors.

## What to Hand Back
1. Retention Curve Summary: Start %, 30s Drop %, End % with health band.
2. The Top 3 Cliff Moments: Exact timestamp, percentage lost, and spoken dialogue at that moment.
3. **The Single Highest-Impact Fix**: One clear priority action (e.g., "Eliminate the 45-second backstory at 02:15").
4. Secondary observations (optional technical pacing notes).
5. Final step: **Ready to apply this fix to the next video outline?**
