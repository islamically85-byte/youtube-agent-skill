---
name: yt-timeline-otio
description: OpenTimelineIO multi-track NLE interchange generator (.otio, .edl) for DaVinci Resolve, Premiere Pro, and Final Cut Pro in YouTube Agent Studio v3.0 (ChatGPT Edition).
---

# yt-timeline-otio — OpenTimelineIO NLE Multi-Track Interchange

`yt-timeline-otio` bridges AI agent media generation with professional Non-Linear Editors (NLEs). It compiles stock B-roll, 3D Blender renders, browser motion graphics overlays, and mastered audio stems into industry-standard interchange formats (`.otio`, `.edl`).

Maintained by **ABDUL MUEED LASHARY** as part of YouTube Agent Studio v3.0 (ChatGPT Edition).

---

## Multi-Track Timeline Architecture

```
Track Layout in Generated Timeline:
─────────────────────────────────────────────────────────────────────────────
[V3] Motion Graphics    : Lower-thirds, animated counters, legal disclaimers
[V2] Blender 3D Parcels : 3D master plans, structural file pillars, flyovers
[V1] Base Stock B-roll  : Curated licensed documentary footage (Pexels, CC0)
─────────────────────────────────────────────────────────────────────────────
[A1] Spoken Voiceover   : Mastered native Pakistani Urdu narration (-14 LUFS)
[A2] Atmospheric Music  : Scored background music (-24 dB sidechain ducking)
─────────────────────────────────────────────────────────────────────────────
```

---

## NLE Compatibility

- **Blackmagic DaVinci Resolve**: File -> Import -> Timeline -> Select `.otio` or `.edl`.
- **Adobe Premiere Pro**: File -> Import -> Select `.otio` (via OTIO plugin) or CMX 3600 `.edl`.
- **Apple Final Cut Pro**: File -> Import -> XML / EDL.

---

## Command Reference

```bash
# Check OpenTimelineIO library and adapter availability
python3 scripts/otio_export.py check

# Export complete 5-track documentary timeline (.otio)
python3 scripts/otio_export.py export \
  --name "Pakistan Property Group Documentary" \
  --manifest Stock_Footage_Manifest_22.csv \
  --motion output/demo_motion_15s.mp4 \
  --blender output/blender_parcel_3d.png \
  --voice output/urdu_mastered.wav \
  --music output/full_audio_mix.wav \
  --out output/documentary_timeline.otio

# Export standard CMX 3600 Edit Decision List (.edl)
python3 scripts/otio_export.py export \
  --name "Pakistan Property Group Documentary" \
  --motion output/demo_motion_15s.mp4 \
  --out output/documentary_timeline.edl
```
