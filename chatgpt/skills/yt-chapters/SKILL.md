---
name: yt-chapters
description: >-
  Generate and validate YouTube chapter timestamps from transcripts, strictly enforcing YouTube's
  three platform formatting rules so chapters render correctly on web and mobile players.
---

# yt-chapters — YouTube Platform Chapter Validation

Chapters break long-form videos into scannable segments, boosting average viewer duration and enabling Google Search "Key Moments" indexing. If a chapter block violates YouTube's rules by even one character, YouTube silently ignores the entire block.

## Tools Available
Run the self-contained chapters utility in this directory:
```bash
# Generate chapters from a transcript
python3 chapters.py transcript.srt --target 8
python3 chapters.py transcript.vtt --json

# Validate an existing description chapter block
python3 chapters.py --validate "0:00 Intro\n1:15 Step 1\n3:45 Step 2"
```

## The Non-Negotiable YouTube Chapter Rules
1. **Rule 1: Must Start at 00:00 (or 0:00)**: If the first timestamp is 00:05 or missing, chapters fail to activate.
2. **Rule 2: Minimum of Three Chapters**: A list with only two timestamps will not render on the scrubber bar.
3. **Rule 3: Minimum 10 Seconds per Chapter**: Any chapter shorter than 10 seconds causes the entire block to be discarded.
4. **Rule 4: Strict Chronological Order**: Timestamps must progress forward in time without overlapping ranges.

## Writing Engaging Chapter Titles
Raw transcripts often suggest dry technical tags ("Section 1", "Database"). Convert topic words into **benefit-driven, curiosity-inducing titles**:
- Dry: `02:15 Memory Leak Fix`
- Engaging: `02:15 The Hidden Memory Leak Slowing Down Your App`

## What to Hand Back
1. Formatted chapter block ready to paste directly into your video description.
2. Validation status confirming compliance with YouTube's 4 rules.
3. Total chapter count and average section duration.
4. Final check: **Ship it into the description, or retitle sections?**
