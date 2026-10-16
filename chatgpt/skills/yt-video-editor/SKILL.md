---
name: yt-video-editor
description: Assemble multi-track documentary video timelines using FFmpeg, combining stock clips, normalized Pakistani Urdu voiceover, and ducked atmospheric music.
---

# yt-video-editor — Multi-Track Documentary Timeline & Assembly

`yt-video-editor` translates narrative scripts and curated stock footage into a concrete multi-track timeline, executing deterministic assembly via the `render_free.py` FFmpeg engine.

## Documentary Editorial Principles

1. **Audio-Led Editing (The Voiceover Spine)**:
   - In documentary storytelling, the spoken voiceover is the master spine.
   - Video clips cut to sentence boundaries, breath pauses, and tonal shifts.
   - Use **J-cuts** (narration begins 0.5s before the new visual) and **L-cuts** (ambience trails past visual cuts) to eliminate choppy, abrupt edits.

2. **Resolution & Aspect Ratio Canvas**:
   - Long-form widescreen: `1920x1080` (16:9) @ 30 or 24 fps.
   - Shorts / TikTok / Reels: `1080x1920` (9:16) @ 30 or 60 fps.
   - Footage with mismatched aspect ratios is cleanly centered and letterboxed/pillarboxed using standard FFmpeg scaling:
     ```
     scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1
     ```

3. **Multi-Track Audio Ducking Standards**:
   - **Track 1 (Narration)**: Primary dialogue track normalized to **-14.0 LUFS** with maximum **-1.5 dBFS** true peak.
   - **Track 2 (Background Ambience / Music)**: Ducked by **-24.0 dB** beneath spoken dialogue (linear volume ~0.06 to 0.08) so the voice remains 100% intelligible.
   - Uses FFmpeg `amix=inputs=2:duration=first:dropout_transition=2`.

4. **Zero-Credit Local Rendering**:
   - Renders locally using FFmpeg without reliance on cloud rendering credits or paid subscriptions.

## CLI Execution Guide

### 1. Validate the Timeline Manifest
```bash
python3 scripts/validate_manifest.py --manifest project-manifest.json --strict
```

### 2. Dry-Run Inspection
```bash
python3 scripts/render_free.py --manifest project-manifest.json --dry-run
```

### 3. Full Production Render
```bash
python3 scripts/render_free.py --manifest project-manifest.json --output exports/master_video.mp4
```
