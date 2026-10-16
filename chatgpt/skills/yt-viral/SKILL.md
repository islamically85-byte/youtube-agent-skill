---
name: yt-viral
description: >-
  Conduct ethical niche and competitor research by ranking videos against each channel's own median
  performance, identifying genuine narrative outliers, and classifying winning packaging patterns.
---

# yt-viral — Ethical Outlier & Competitor Intelligence

Raw view counts reflect channel subscriber size, not idea quality. A 500K video on a 5M-subscriber channel is an average Tuesday; a 500K video on a channel whose median upload receives 20K views represents a genuine **outlier multiple (25x)** that resonated beyond its subscriber base.

## Tools Available
Run the outlier detection script in this directory:
```bash
python3 swipe.py collected.json --min 2.0
python3 swipe.py competitor_batch.json --json
```

## Collecting Verified Data
Input is a JSON array of videos from public creator listings:
```json
[
  {"channel": "Creator A", "title": "...", "views": 185000, "url": "...", "duration": 620},
  {"channel": "Creator A", "title": "...", "views": 12000, "url": "...", "duration": 480}
]
```
> **ETHICAL INTEGRITY RULES**:
> 1. **Never invent metrics or view counts**: If a number is unknown, collect it or omit it.
> 2. **Sample Size Caveat**: Requires at least **4 videos per channel** to compute a meaningful median. Thin channels are flagged and skipped.
> 3. **Hypothesis vs. Fact**: Classifying a title formula describes the visible phrasing; it is an analytical hypothesis, never an absolute explanation of YouTube recommendation mechanics.

## Analytical Methodology

1. **Calculate Channel Baseline**: Find the statistical median views across each creator's recent comparable uploads.
2. **Compute Outlier Multiples**: Score each video by `Views / Channel Median`.
   - Normal: 0.8x – 1.3x
   - Strong: 1.5x – 2.9x
   - Breakout Outlier: >= 3.0x
3. **Classify Hook & Packaging Patterns**: Check which of the 21 proven hook formulas appeared in the outlier titles (e.g., The Statistic, The Contrarian Warning, Someone Else's Result).
4. **Isolate Structural Elements**:
   - What curiosity gap was opened in the title?
   - What emotional stake or urgency was introduced?
   - Did the video capitalize on a major trend or evergreen search intent?

## What to Hand Back
1. Ranked leaderboard of verified outliers with their respective channel median multiples.
2. Breakdown of recurring title formulas and thumbnail visual patterns among the outliers.
3. Identified content gaps: topics that over-performed in the niche but were left unexplained.
4. Actionable hypotheses for your own channel: **Which concept should we adapt into `/yt-package`?**
