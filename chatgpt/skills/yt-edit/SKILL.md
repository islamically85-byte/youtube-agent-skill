---
name: yt-edit
description: >-
  Generate precise Edit Decision Lists (EDL) from timestamped transcripts (.srt, .vtt, Whisper .json).
  Detects dead-air gaps, filler cues, restarted takes, and pacing drag while preserving natural speech cadence.
---

# yt-edit — Transcript Edit Decision List (EDL)

Turn raw video and audio transcripts into an actionable Edit Decision List. Eliminates dead time, verbal filler, and retakes before you touch your video editor timeline.

## Tools Available
Run the self-contained deadair tool in this directory:
```bash
python3 deadair.py transcript.srt
python3 deadair.py transcript.vtt --floor 0.35
python3 deadair.py whisper_transcript.json --json
```

## What it Detects & Flags
1. **DEAD AIR**: Pauses exceeding the floor threshold (default 0.45s).
   - *Cadence Preservation*: Trims from the center of the gap, maintaining breath room at boundary edges so the speaker does not sound breathless.
2. **FILLER CUES**: Subtitle cues consisting purely of verbal tics ("um", "uh", "you know", "basically", "so yeah", Urdu "matlab/yani").
3. **RESTARTS & RETAKES**: Repeated sentence openings where the creator stumbled, paused, and restarted the line.
   - Compares current cues against prior substantive speech cues across filler gaps.
4. **STRUCTURAL DRAG**: Identifies long rambling intros, repetitive restatements of known premises, and sections ripe for b-roll cutaways.

## EDL Output Contract
Each proposed cut includes:
- **Cut Type**: `DEAD`, `FILLER`, `REPEAT`, or `PACING`
- **Timecode In / Out**: Exact start and end timestamps in `HH:MM:SS.mmm` and seconds
- **Duration Removed**: Exact seconds saved
- **Rationale & Transcript Excerpt**: Context of what was cut
- **Confidence Rating**: `High` (safe to ripple cut automatically), `Medium` (review recommended to preserve intentional comedic/dramatic pauses)

## Optional Local FFmpeg Helper
If you have `ffmpeg` installed locally, you can preview or assemble the cuts without touching an NLE:
```bash
# Example FFmpeg select filter generation for high-confidence cuts
# (Provided for creator convenience; ffmpeg execution is entirely optional)
ffmpeg -i raw_recording.mp4 -vf "select='not(between(t, 7.5, 9.8) + between(t, 10.6, 13.9))',setpts=N/FRAME_RATE/TB" -af "aselect='not(between(t, 7.5, 9.8) + between(t, 10.6, 13.9))',asetpts=N/SR/TB" tightened_preview.mp4
```

## What to Hand Back
1. Total initial runtime vs. estimated tightened runtime (% reduction).
2. Ranked list of recommended cuts with timestamps and context snippets.
3. Summary of potential false starts and retakes to confirm with the creator.
4. Ready-to-apply EDL table for Premiere Pro, DaVinci Resolve, or Final Cut Pro.
5. Final question: **Ship it, or change it?**
