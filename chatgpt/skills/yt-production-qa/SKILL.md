---
name: yt-production-qa
description: Inspect rendered documentary media files using ffprobe/ffmpeg, enforce technical standards, and output TECHNICALLY_VALID_PENDING_REVIEW with human sign-off checklists.
---

# yt-production-qa — Automated Technical Media QA & Human Review Gate

`yt-production-qa` provides objective, deterministic verification of rendered video files. It runs automated probes using `ffprobe` and `ffmpeg` via `qa_media.py`, guaranteeing that media meets YouTube technical specifications before human editorial sign-off.

## The Quality Gate Philosophy

> [!IMPORTANT]
> **No video is approved by automated tools alone.**
> Passing automated checks earns the status **`TECHNICALLY_VALID_PENDING_REVIEW`**.
> Human ears and eyes must sign off on linguistic inflection, editorial tone, and visual storytelling before publication.

## Automated Inspection Suite

1. **Stream & Geometry Verification**:
   - Probes resolution (`1920x1080` for 16:9, `1080x1920` for 9:16 Shorts).
   - Verifies framerate consistency (e.g. 30 fps or 24 fps).
   - Verifies valid container format and industry codecs (`libx264` video, `aac` audio).

2. **Black Frame & Drop Detection**:
   - Executes FFmpeg `blackdetect=d=0.5:pic_th=0.98`.
   - Flags any accidental missing frames, dropped visual clips, or rendering glitches exceeding 0.5 seconds.

3. **EBU R128 Loudness Compliance**:
   - Executes FFmpeg `ebur128=peak=true` filter.
   - Measures integrated loudness against YouTube's **-14.0 LUFS** target.
   - Measures true peak against **-1.5 dBFS** limit to prevent digital clipping.

4. **Licensing Provenance Verification**:
   - Inspects the accompanying `project-manifest.json`.
   - Confirms that every clip has a verified commercial license class and zero unverified assets.

## The 5 Mandatory Human Review Items

Every QA report requires manual sign-off on the following 5 editorial criteria:
- [ ] **Urdu Pronunciation & Cadence**: Voiceover has correct pronunciations, natural inflection, and appropriate 130 WPM pacing.
- [ ] **Visual Relevance**: Stock footage metaphorically and emotionally supports the spoken narrative without literal clichés.
- [ ] **Subtitle Typography & Safe Zones**: Urdu RTL subtitles render properly without clipping in mobile safe margins.
- [ ] **Audio Balance & Ducking**: Atmospheric music remains audible while ducked at -24 dB, never obscuring speech intelligibility.
- [ ] **Commercial Clearances**: Recognizable persons, private buildings, or trademarks have proper releases or editorial justifications.

## CLI Usage

```bash
python3 scripts/qa_media.py --media exports/master_video.mp4 --manifest project-manifest.json
```
