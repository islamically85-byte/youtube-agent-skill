# Research Note: Free-First Documentary Production Architecture

**Project:** YouTube Agent Studio V2  
**Extension Maintainer:** ABDUL MUEED LASHARY  
**Upstream Author & Original MIT Attribution:** Jake Schincariol ([`Jakeschincariol/youtube-agent-skill`](https://github.com/Jakeschincariol/youtube-agent-skill))  
**Date:** October 2026  
**License:** MIT  

---

## 1. Executive Summary

YouTube Agent Studio V2 expands beyond scriptwriting and SEO analytics into an end-to-end, free-first documentary video production engine. Rather than relying on paid cloud services, proprietary subscriptions, or synthetic slide-show animations, V2 establishes an offline-capable, zero-credit workflow powered by:

1. **Permissive stock footage curation** (Pexels, Pixabay, Mixkit, CC0) with auditable commercial provenance.
2. **Authentic Pakistani Urdu narration** in native Perso-Arabic script (`اردو`) at ~130 WPM documentary pacing.
3. **Deterministic multi-track FFmpeg timeline rendering** with automatic -14.0 LUFS speech normalization and -24.0 dB music ducking.
4. **Strict third-party quota guarding** (default credit budget = 0), preventing accidental deductions from depleted accounts (such as vidIQ).
5. **Automated media QA probing** that enforces the `TECHNICALLY_VALID_PENDING_REVIEW` quality gate alongside a 5-point mandatory human editorial checklist.

---

## 2. Third-Party Metered Quota Audit & Credit Guard

### 2.1 The vidIQ Quota Baseline Finding
During technical environment auditing on **2026-10-16**, the connected vidIQ account was found to have:
- **Remaining Balance:** 2 credits out of 150 monthly credits.
- **Quota Renewal Date:** 2026-11-16.
- **Operation Unit Costs:**
  - Competitor research / keyword expansion: **5 credits**
  - Daily ideas generation: **5 credits**
  - AI title generator: **5 credits**
  - AI thumbnail generation: **15 credits**

### 2.2 Quota Depletion Risk & Mitigation
Calling a 5-credit or 15-credit vidIQ endpoint with a live balance of only 2 credits results in immediate HTTP 402/429 errors, failed pipelines, and wasted execution time. Furthermore, unmetered AI tools can silently incur unexpected charges.

**Implemented Defense (`credit_guard.py` & `yt-credit-guard`):**
1. **Default Credit Budget = 0:** No external paid API call is ever attempted unless the user explicitly grants consent (`--consent yes`) and specifies a non-zero budget.
2. **Pre-Flight Balance Check:** If a known live balance is provided and is less than the requested cost (e.g. 2 balance vs 5 cost), `credit_guard.py` proactively aborts with an `EXHAUSTED` warning before any network call is dispatched.
3. **Free-First Fallbacks:** Every guarded tool maps to an offline local alternative:
   - vidIQ competitor research &rarr; Local `yt-viral` (median multiple outlier calculation), `yt-seo`, and YouTube autocomplete.
   - vidIQ AI thumbnails &rarr; Permissive stock stills (Pexels/Pixabay) + `yt-package` pairing linter.
   - ElevenLabs TTS &rarr; Human creator voiceover recording (gold standard) or permissive offline speech benchmark.

---

## 3. Free Stock Footage Licensing & Provenance Register

### 3.1 Legal & Commercial Taxonomy

Documentary production on YouTube requires unambiguous commercial monetization clearance. The table below details verified free stock platforms:

| Repository | Primary License Class | YouTube Monetization | Model / Property Release Rules |
| :--- | :--- | :--- | :--- |
| **Pexels** | `Pexels License` | Fully permitted without attribution | Scenic/b-roll safe; recognizable faces require release for commercial ads; editorial OK |
| **Pixabay** | `Pixabay License` | Fully permitted without attribution | Commercial use allowed; do not depict recognizable trademarks, logos, or brands |
| **Mixkit** | `Mixkit Free License` | Permitted on YouTube videos | Check specific asset tier (Free vs Restricted); music may require platform attribution |
| **Creative Commons CC0** | `Creative Commons CC0` | Worldwide public domain dedication | Completely unrestricted worldwide; no attribution required |
| **Creator-Owned** | `Creator Owned` | Full creator copyright | Self-cleared footage shot by creator |

### 3.2 The Project Manifest (`project-manifest.json`)
Every stock clip used in a video edit must be logged in `project-manifest.json` conforming to `shared/schemas/project-manifest.schema.json`. The manifest records:
- Source URL or local path
- License class and verification timestamp
- Model/property release status (`released`, `not_required_scenic`, `editorial_only`)
- Exact in/out timeline offsets

The manifest is verified before rendering by `validate_manifest.py`:
```bash
python3 shared/scripts/validate_manifest.py --manifest project-manifest.json --strict
```

---

## 4. Pakistani Urdu Narration & Audio Mastering

### 4.1 Linguistic Register & Script Purity
- **Native Script (`اردو`):** All voiceover scripts and subtitle files are authored strictly in Perso-Arabic Urdu script. **Roman Urdu is prohibited** unless explicitly requested, as Roman Urdu lacks orthographic standardization, obscures authentic pronunciation, and looks unprofessional on screen.
- **Cadence & Speech Rate:** Spoken Pakistani Urdu documentary narration targets **~130 words per minute** (approx. 2.1 words per second). This delivers natural gravitas, allows compound verbs (`کر دیا گیا ہے`) to breathe, and provides space for visual absorption.

### 4.2 Urdu TTS vs. Human Voiceover Benchmark
A systematic review of current free, offline neural TTS solutions reveals:
- **Meta MMS Urdu:** Bound by a strict **CC-BY-NC (Non-Commercial)** license. Using Meta MMS audio on monetized YouTube channels constitutes a direct license violation.
- **Piper / Coqui XTTS:** While open-source, current Urdu model checkpoints suffer from erratic phoneme-to-grapheme mapping, misplaced stresses on retroflex consonants (`ٹ`, `ڈ`, `ڑ`), and unnatural robotic flatlines on long sentences.
- **ElevenLabs:** Produces convincing Urdu inflection, but requires paid cloud tokens and violates zero-credit defaults without explicit user approval.

> [!IMPORTANT]
> **Gold Standard:** A well-recorded human voiceover (recorded on a USB/XLR microphone at 24-bit 48kHz WAV with a pop filter) remains the single highest-retention, 100% commercially cleared voice solution for Pakistani Urdu documentaries.

### 4.3 Multi-Track Audio Engineering
The audio pipeline in `render_free.py` enforces broadcast-standard audio levels:
- **Narration Dialogue:** Normalized to **-14.0 LUFS** with a maximum true peak of **-1.5 dBFS** using FFmpeg `loudnorm=I=-14:TP=-1.5:LRA=11`.
- **Atmospheric Background Music:** Ducked by **-24.0 dB** beneath spoken dialogue (`volume=0.0631`) using `amix=inputs=2:duration=first:dropout_transition=2`. Spoken words remain 100% intelligible.

---

## 5. Timeline Assembly & Cross-Platform FFmpeg Engine

### 5.1 Architecture of `render_free.py`
The assembly engine constructs a deterministic FFmpeg `filter_complex` graph that:
1. Trims each stock clip to its scheduled in/out timeline markers.
2. Centers and normalizes varied footage to canvas resolution (16:9 `1920x1080` for long-form; 9:16 `1080x1920` for Shorts) with uniform 30 fps framerate.
3. Concatenates video streams seamlessly.
4. Escapes filter paths defensively across macOS, Linux, and Windows:
   - Replaces Windows backslashes `\` with `/`.
   - Escapes colons in drive letters (`C\:`) and single quotes (`\'`).
5. Handles subtitles flexibly:
   - Burns subtitles directly into video frames if `libass` is compiled into FFmpeg.
   - Gracefully falls back to muxing standard UTF-8 timed text tracks (`-c:s mov_text -metadata:s:s:0 language=urd`) inside the MP4 container when subtitle burning filters are unavailable.

---

## 6. Technical Media QA & The Human Review Gate

### 6.1 The Probing Engine (`qa_media.py`)
Rendered MP4 files are probed using `ffprobe` and `ffmpeg`:
- **Geometry & Codecs:** Confirms canvas dimensions, aspect ratio, H.264 video codec, and AAC audio codec.
- **Black Frame Drops:** Scans for unintentional black frames or dropped clips exceeding 0.5 seconds via FFmpeg `blackdetect`.
- **EBU R128 Loudness:** Scans the audio stream via FFmpeg `ebur128=peak=true` and validates integrated LUFS.
- **Licensing Audit:** Cross-references clips against `project-manifest.json` for missing or unverified licenses.

### 6.2 The Status Contract: `TECHNICALLY_VALID_PENDING_REVIEW`
If all automated technical checks pass, `qa_media.py` awards the status:
```
TECHNICALLY_VALID_PENDING_REVIEW
```
Automated tools can measure loudness and detect black frames, but they **cannot** judge whether an Urdu phrase is pronounced with correct cultural inflection, whether a cut feels jarring, or whether a stock image carries unintentional editorial bias.

### 6.3 The 5 Mandatory Human Review Checklist Items
Every automated QA report mandates human sign-off on:
1. **Urdu Pronunciation & Cadence:** Confirm correct pronunciations, natural inflection, and 130 WPM speech cadence.
2. **Visual Relevance:** Confirm stock footage cuts visually support the spoken narrative without literal clichés.
3. **Subtitle Typography & Safe Zones:** Confirm Urdu RTL subtitles render without corruption or clipping in mobile safe margins.
4. **Audio Balance & Ducking:** Confirm background music remains audible while ducked at -24 dB, never obscuring voiceover intelligibility.
5. **Commercial Clearances:** Confirm that recognizable individuals or private properties have appropriate releases or editorial justifications.
