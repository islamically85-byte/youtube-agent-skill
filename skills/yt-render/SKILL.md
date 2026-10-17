---
name: yt-render
description: Documentary video renderer. Assembles stock footage cuts, Ken Burns motion, and cue-synchronized ASS subtitles into high-definition 16:9 or 9:16 MP4 video.
---

# yt-render — Documentary Video Rendering & Motion Engine v3.0

`yt-render` executes high-definition video assembly using FFmpeg. It takes the semantic Edit Decision List (EDL) from `yt-assets`, the master audio mix from `yt-audio`, and cue-synchronized ASS motion subtitles from `editorial_motion.py`, rendering a broadcast-grade 1080p MP4 documentary.

## Core Capabilities

1. **Deterministic Multi-Shot Assembly**:
   - Stitches 70–95 stock footage cuts smoothly with subtle cross-fades and Ken Burns motion.
2. **Aspect Ratio Flexibility**:
   - Supports 16:9 standard documentary widescreen (`1920x1080`) and 9:16 vertical shorts (`1080x1920`).
3. **Cue-Synchronized Subtitles & Allegations Disclaimers**:
   - Synchronizes ASS subtitles to exact audio cue timestamps (`voice_cue_times.json`).
   - Displays investigative figures (e.g. 42,000 files, 6,000 plots, 36,000 excess, Rs 16B inquiry) strictly with the label **REPORTED ALLEGATIONS** (`رپورٹ کردہ الزامات`).
4. **Broadcast Encoding Specs**:
   - Codec: H.264 High Profile (`yuv420p`), AAC Audio (`48kHz, 192kbps`), Keyframe Interval: 2.0s (`-g 60` at 30fps).

## CLI Usage

Render the full documentary master video:

```bash
# Render master video with EDL, master audio, and ASS subtitles
python3 shared/scripts/render_free.py \
  --manifest project-manifest.json \
  --audio master_audio.m4a \
  --subtitles documentary_motion.ass \
  --output exports/master_documentary.mp4
```

Generate cue-synchronized ASS motion graphics subtitles:

```bash
python3 shared/scripts/editorial_motion.py \
  --cues voice_cue_times.json \
  --output documentary_motion.ass
```

## Production Verification

Never mark a rendering task complete or claim a video is finished unless the output MP4 actually exists on disk and is playable. Run `yt-render-qc` immediately after rendering.
