---
name: yt-shorts
description: >-
  Extract and re-engineer high-retention vertical Shorts (9:16) from long-form video transcripts,
  providing rewritten hooks, framing instructions, caption styling, and clip manifests.
---

# yt-shorts — Long-Form to Vertical Shorts Extraction

A successful Short extracted from a long video is **not** merely a favorite highlight. It is a moment that **survives completely independently** without needing the preceding 10 minutes of context.

## Selection Criteria (The 3 Tests)
Examine the transcript to identify spans of 25–55 seconds that satisfy all three requirements:
1. **The Independent Entry**: The clip starts on a standalone thought. If understanding the first sentence requires prior context, it fails as a Short.
2. **The Turn / Contrast**: Contains an immediate friction point, surprising revelation, counter-intuitive insight, or emotional shift.
3. **The Punchy Resolution / Loop Point**: Concludes decisively or seamlessly loops back into the opening hook line.

> **FACTUAL INTEGRITY RULE**: Never distort, trim out caveats, or cherry-pick sentences in ways that misrepresent scientific, educational, medical, or religious facts for the sake of artificial viral shock.

## Re-Engineering for 9:16 Vertical Video
For each selected candidate clip:
- **Rewritten Spoken Hook (0:00–0:03)**: Often long-form speech enters a topic too leisurely. Provide an alternate punchy opening line if recorded pickup is possible, or specify exact audio in-point.
- **Vertical Framing & Aspect Ratio (9:16)**:
  - Subject framing: Center-weighted crop, split-screen (speaker top + visual demonstration bottom), or dynamic pan-and-scan.
  - Safe Margins: Avoid placing critical text near the right-side interaction icons (Like/Share/Comments) or bottom channel handle overlay.
- **Dynamic Captions & Pacing**: Identify key emphasis words (highlight in high-contrast yellow/green).
- **Loop Engineering**: Detail how the final sentence connects with the first sentence for continuous looping.

## Clip Manifest Output
Provide structured cutting parameters for each extracted Short:
```json
{
  "clip_id": "short_01",
  "title": "The 1 Habit Destroying Your Sleep",
  "source_in": "04:12.500",
  "source_out": "04:58.200",
  "duration_seconds": 45.7,
  "rewritten_hook_overlay": "Stop checking your phone at 11 PM.",
  "framing": "9:16 vertical crop, speaker centered at top 60%, B-roll lower 40%",
  "loop_point": "Final word connects directly to opening hook line"
}
```

## What to Hand Back
1. Ranked list of 3–5 viable Shorts candidates from the transcript.
2. Exact source in/out timestamps and spoken text.
3. Hook overlay text and vertical framing instructions for your editor.
4. Exportable JSON clip manifest.
5. Next step: **Confirm selected clip or request alternative moments?**
