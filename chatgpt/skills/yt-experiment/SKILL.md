---
name: yt-experiment
description: >-
  Design controlled packaging and content optimization experiments, structuring valid title/thumbnail
  A/B hypotheses, sample size requirements, measurement windows, and statistical interpretations.
---

# yt-experiment — Controlled A/B Testing & Content Experiments

Scientific experimentation separates amateur guessing from consistent channel growth. This workflow formats rigorous, hypothesis-driven split tests for thumbnails, titles, opening hooks, and content formats.

## YouTube Native Experiment Capabilities
> **STUDIO "TEST & COMPARE" DOCUMENTED SCOPE**:
> YouTube Studio provides native A/B/C testing for **thumbnails only** (up to 3 thumbnails per video). It rotates thumbnails across viewers and reports "Watch Time Share" rather than raw CTR. YouTube **DOES NOT** currently offer native automated title rotation on standard creator accounts. Structure title experiments as phased sequential tests or manual split tests.

## Experiment Integrity Principles
1. **Never Invent Statistical Significance**: Never promise "a 42% guaranteed CTR jump" or fabricate simulated test winners.
2. **One Variable at a Time**: An experiment testing two titles AND two thumbnails simultaneously cannot identify which variable drove the outcome.
3. **Sample Size & Time Horizons**: Evaluating a test after 30 impressions is statistically meaningless. Define minimum threshold impressions (typically 1,000+ per variation) and a 7–14 day measurement window.

## Supported Experiment Modalities

### 1. Native Thumbnail "Test & Compare" (3-Way Split)
- **Hypothesis Formulation**:
  - *Variant A (Baseline)*: Creator face expressing surprise, high-contrast text.
  - *Variant B (Curiosity Clue)*: Extreme close-up on the central object/tool without face.
  - *Variant C (Minimalist Contrast)*: Stark black/yellow split, 2-word punchy statement.
- **Metric**: Watch time share (%) over 14 days.

### 2. Phased Title Split Testing (Sequential)
- Test Phase 1 (Days 1–7): Descriptive search-oriented title.
- Test Phase 2 (Days 8–14): Curiosity-gap or question-oriented title.
- Control for upload day decay by measuring browse impressions vs. search conversions.

### 3. Hook & Retention Variations (For Future Uploads)
- Test two different introductory pacing models across two similar topical uploads:
  - Video A: Direct Statistic hook (first 10 seconds).
  - Video B: In-Media-Res story opening (first 10 seconds).
- Compare 30-second retention loss via `/yt-retention`.

## Experiment Specification Template
```markdown
### Experiment: "Why Python Developers Quit" Thumbnail Test
- **Target Video**: "Why 97% of Developers Quit Python"
- **Variable Under Test**: Facial Expression vs. Code Error Screenshot
- **Hypothesis**: Showing a relatable syntax error screenshot will outperform a generic shocked face among experienced programmers because it triggers immediate technical recognition.
- **Variation A (Control)**: Host looking frustrated at desk. Overlay: "I GAVE UP"
- **Variation B (Treatment)**: Red terminal error message "RecursionError: maximum depth exceeded". Overlay: "FATAL ERROR"
- **Platform Tool**: YouTube Studio "Test & Compare"
- **Evaluation Window**: 14 days or until YouTube declares a statistically confident winner.
- **Decision Rule**: If Variation B achieves > 55% watch time share, adopt error-code styling for future technical tutorials.
```

## What to Hand Back
1. Formal Hypothesis Document with single-variable isolation.
2. Production specifications for Control (A) and Treatment (B/C) variations.
3. Defined measurement window, metric targets, and decision threshold.
4. Next step: **Generate creative assets via `/yt-package` or launch test?**
