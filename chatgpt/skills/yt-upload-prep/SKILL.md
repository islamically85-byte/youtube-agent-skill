---
name: yt-upload-prep
description: >-
  Assemble publication-ready YouTube metadata packages, including titles, descriptions,
  chapters, thumbnail specifications, synthetic-media disclosures, and pre-publish QA checklists.
---

# yt-upload-prep — Publication Packaging & Studio Pre-Flight

Assemble complete, copy-ready YouTube publication packages before uploading. Consolidates packaging, SEO metadata, platform compliance declarations, and audio/video quality checklists into a single verified pre-flight dossier.

## Publication Transparency
> **IMPORTANT PLATFORM NOTICE**:
> This workflow **DOES NOT** pretend to upload or publish videos autonomously. It prepares all human-readable and machine-readable assets. You review, approve, and upload via YouTube Studio. Never commit private OAuth tokens, API secrets, or passwords to a public repository.

## The Complete Upload Dossier

### 1. Core Metadata
- **Final Video Title**: Under 60 characters for desktop/mobile safety.
- **Title Character Count**: Verified against YouTube's hard 100-character ceiling.
- **Thumbnail Specifications**: File dimensions (1280x720 minimum, 16:9), format (.PNG or .JPG < 2MB), visual contrast check, overlay text check.

### 2. Formatted Description Block
- **Above-the-Fold Hook**: First 2–3 lines conveying immediate viewer value.
- **Topic Outline & Timestamps**: Complete chapter list starting at `00:00`.
- **Primary Links & Resources**: Lead magnets, tools, affiliate links with legal disclosures.
- **Community & Social Handles**: Links to community Discord, Twitter/X, newsletter.
- **Hashtags**: 3–5 targeted hashtags.

### 3. Compliance & Regulatory Settings
- **Audience Classification (COPPA)**: Declare explicitly whether content is "Made for Kids" or "Not Made for Kids".
- **Altered or Synthetic Content Disclosure**: Declare whether the video contains realistic AI-generated people, voices, or synthetic events as required by YouTube's 2024+ synthetic media policies.
- **Age Restriction & Content Warnings**: Check if graphic discussions, swearing, or sensitive topics require appropriate tagging.
- **Paid Promotion Checkbox**: If sponsored or containing product placements, mark required studio toggle.

### 4. Technical Audio/Video Pre-Flight
- **Loudness Normalization**: Audio mixed to YouTube's target (-14 LUFS integrated, -1.0 dB true peak).
- **Color Space & Encoding**: H.264/H.265 (MP4/MOV), Rec.709 color matrix, native resolution (1080p / 4K).
- **Aspect Ratio**: 16:9 widescreen or 9:16 vertical for Shorts.
- **End Screen & Card Timestamps**: Designate the final 20 seconds for end-screen video cards and subscribe badges.

### 5. Scheduling Strategy
- Optimal day-of-week and time-of-day recommendation based on channel audience geography.
- Set upload visibility initially to **Unlisted** for 2–4 hours prior to release to allow YouTube to process high-definition encodes (HD/4K) and complete automated copyright/Content ID checks.

## Exportable Machine-Readable Package
Provides JSON metadata block compatible with the `shared/schemas/upload-package.schema.json` specification:
```json
{
  "title": "Why 97% of Creators Quit Before Video 30",
  "description": "Discover the 3 critical systems separating top YouTube channels...",
  "primary_keywords": ["youtube growth", "creator burnout", "retention strategy"],
  "hashtags": ["#YouTubeTips", "#CreatorEconomy", "#VideoProduction"],
  "compliance": {
    "made_for_kids": false,
    "contains_synthetic_media": false,
    "synthetic_media_disclosure_required": false
  }
}
```

## What to Hand Back
1. Complete Studio-ready description and metadata dossier.
2. Verified chapter timestamp block.
3. Pre-flight technical checklist (Audio LUFS, aspect ratio, encoding).
4. Scheduling and Unlisted processing recommendation.
5. Final pre-upload confirmation: **Ready to copy into YouTube Studio?**
