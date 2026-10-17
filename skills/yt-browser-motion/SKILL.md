---
name: yt-browser-motion
description: Deterministic browser-based motion graphics engine using HTML5, Canvas, SVG, CSS, headless Chrome/Edge, and FFmpeg for YouTube Agent Studio v3.0.
---

# yt-browser-motion — Deterministic Browser-Based Motion Graphics

`yt-browser-motion` produces broadcast-quality motion graphics overlays, title cards, animated evidence counters, and documentary data charts using standard web technologies (HTML, CSS, SVG, Canvas) and headless browser rendering.

Maintained by **ABDUL MUEED LASHARY** as part of YouTube Agent Studio v3.0.

---

## Capabilities & Architecture

1. **Deterministic Frame Capture**:
   - Instead of real-time screen recording (which drops frames under load), captures every frame sequentially and deterministically via `shared/scripts/browser_motion.py`.
   - Native support for 25 and 30 FPS across 16:9 (1920x1080), 9:16 (1080x1920 Shorts/Reels), and 1:1 (1080x1080 square).

2. **Professional Motion Design Principles**:
   - **Anticipation & Overshoot**: Counters pull back slightly before accelerating into smooth cubic eases (`easeOutBack`, `easeInOutCubic`).
   - **Visual Hierarchy & Depth**: Restrained slate gradients, soft vignette glows, technical coordinate grids, and subtle motivated camera drift (1.00 -> 1.035 scale).
   - **Typography**: Native Perso-Arabic Urdu script (`Noto Naskh Arabic`, `Geeza Pro`) alongside editorial Latin headings.
   - **Mandatory Legal Disclaimers**: Prominently burns documentary disclaimers (*"یہ رپورٹ کردہ الزامات اور تحقیقاتی اعداد و شمار ہیں، حتمی عدالتی فیصلہ نہیں"*).

3. **Alpha Transparency & Multi-Track Compositing**:
   - Renders with alpha channel to Apple ProRes 4444 (`.mov`) or VP9 (`.webm`) for direct non-linear overlay over B-roll footage.

4. **Automated Contact Sheets & Thumbnails**:
   - Generates multi-frame contact sheets (`_contact_sheet.png`) and review thumbnails (`previews/`) across the timeline duration.

---

## Command Reference

```bash
# Check system browser (Chrome/Edge/Chromium) and FFmpeg readiness
python3 shared/scripts/browser_motion.py check

# List available motion templates
python3 shared/scripts/browser_motion.py templates

# Render 15-second discrepancy counter (42,000 files vs 6,000 plots)
python3 shared/scripts/browser_motion.py render \
  --html templates/motion/discrepancy_counter.html \
  --out output/demo_motion_15s.mp4 \
  --duration 15.0 --fps 30 --aspect 16:9

# Render 9:16 Shorts vertical motion graphic
python3 shared/scripts/browser_motion.py render \
  --html templates/motion/discrepancy_counter.html \
  --out output/demo_motion_shorts.mp4 \
  --duration 12.0 --fps 30 --aspect 9:16

# Render transparent alpha overlay for NLE editing
python3 shared/scripts/browser_motion.py render \
  --html templates/motion/discrepancy_counter.html \
  --out output/motion_overlay.mov \
  --duration 10.0 --fps 30 --transparent
```
