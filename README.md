# YouTube Agent Studio v3.0 — Motion-First Hybrid Production Suite

> **A professional, motion-first hybrid video production studio for YouTube — engineered natively for both Anthropic Claude and OpenAI ChatGPT.**  
> **Extension Maintainer:** ABDUL MUEED LASHARY | **Upstream Author:** Jake Schincariol

[![Test & Build](https://github.com/islamically85-byte/youtube-agent-skill/actions/workflows/test.yml/badge.svg)](https://github.com/islamically85-byte/youtube-agent-skill/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](#python-utilities)
[![Platform: Claude & ChatGPT](https://img.shields.io/badge/Platform-Claude%20%7C%20ChatGPT-purple.svg)](#platform-editions)
[![Motion: Chrome & Blender](https://img.shields.io/badge/Motion-Chrome%20%2B%20Blender-orange.svg)](#motion-first-visual-production)
[![Audio: Spotify Pedalboard](https://img.shields.io/badge/Audio-Spotify%20Pedalboard-green.svg)](#broadcast-audio-engineering)
[![Interchange: OpenTimelineIO](https://img.shields.io/badge/Interchange-OpenTimelineIO-blueviolet.svg)](#opentimelineio-nle-interchange)

---

## What is YouTube Agent Studio v3.0?

YouTube Agent Studio v3.0 upgrades our production toolkit into a **motion-first, broadcast-grade hybrid video production studio**. It transitions from static documentary slides to **deterministic browser motion graphics** (HTML/CSS/SVG/Canvas), **procedural 3D land parcel flyovers** (Blender LTS `bpy`), **studio-grade vocal DSP** (Spotify Pedalboard + FFmpeg Loudnorm), and **NLE interchange** (OpenTimelineIO for DaVinci Resolve, Premiere Pro, and Final Cut Pro).

---

## The Three Creator Production Options

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       YOUTUBE AGENT STUDIO v3.0                             │
│                      Choose Your Production Mode                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  [A] FREE STUDIO (Zero Budget / 100% Offline Local Engine)                  │
│      • Cost: $0.00 | API Keys: None required | Internet: Not required      │
│      • Browser Motion: Deterministic HTML5/SVG/Canvas via Headless Chrome   │
│      • 3D Visualization: Procedural 3D parcels & flyovers via Blender LTS   │
│      • Voiceover: Offline Piper Urdu neural TTS or human microphone WAV     │
│      • Audio DSP: Spotify Pedalboard + FFmpeg Broadcast Loudnorm (-14 LUFS) │
│      • NLE Export: OpenTimelineIO (.otio, .edl) for DaVinci / Premiere      │
│                                                                             │
│  [B] HYBRID VALUE (Pennies / Low-Cost High-Fidelity APIs)                   │
│      • Cost: < $0.05 per documentary | Checked quotas & price-guard         │
│      • Voiceover: Gemini Voice / Cloud TTS for ultra-natural Urdu inflection│
│      • Rendering: Free local browser motion & Blender 3D engine             │
│      • Fallback: Gracefully falls back to Option A if quota exhausted       │
│                                                                             │
│  [C] vidIQ / PREMIUM (Credit-Guarded Commercial Provider)                   │
│      • Cost: Verified vidIQ balance deducted with explicit authorization   │
│      • Balance Check: Credit Guard audits available tokens before any call  │
│      • Auto-Protection: Falls back to Option A/B if balance insufficient    │
└─────────────────────────────────────────────────────────────────────────────┘
```

> [!NOTE]
> The three options above are presented **only** when entering video or audio production workflows, never interrupting pure ideation, scriptwriting, title linting, or SEO prompts.

---

## Dual Platform Architecture

YouTube Agent Studio provides two dedicated, independently installable distributions:

| Feature | Claude Edition (`skills/`) | ChatGPT Edition (`chatgpt/`) |
| :--- | :--- | :--- |
| **Invocation** | Slash commands (`/yt-studio`, `/yt-browser-motion`, etc.) | Natural conversation & Master Orchestrator (`yt-studio`) |
| **Skill Count** | **34 Dedicated Skills** | **34 Dedicated Skills** |
| **Python Execution** | Local shell execution in Claude Code | Code Interpreter / local Python execution |
| **Package Asset** | `release/youtube-agent-claude.zip` | `release/youtube-agent-chatgpt-skill.zip`<br>`release/youtube-agent-chatgpt-plugin.zip` |
| **Installation** | [docs/INSTALL-CLAUDE.md](docs/INSTALL-CLAUDE.md) | [docs/INSTALL-CHATGPT.md](docs/INSTALL-CHATGPT.md) |
| **Windows Setup** | [docs/INSTALL-WINDOWS.md](docs/INSTALL-WINDOWS.md) | [docs/INSTALL-WINDOWS.md](docs/INSTALL-WINDOWS.md) |

---

## The 34-Workflow Studio Catalog

### 1. Motion-First Visual & Audio Engines (New in v3.0)
- **`yt-browser-motion`**: Deterministic HTML5/SVG/Canvas frame capture via headless Chrome/Edge and FFmpeg (`browser_motion.py`).
- **`yt-blender-3d`**: Procedural 3D land parcels, boundary grids, and structural file stacks via Blender LTS (`blender_parcel_render.py`).
- **`yt-sound-design`**: Spotify Pedalboard voice mastering (Highpass, Gate, Compressor, Limiter) and -24 dB ducking (`pedalboard_master.py`).
- **`yt-timeline-otio`**: Multi-track OpenTimelineIO NLE interchange generator (`otio_export.py`).

### 2. Hybrid Studio & Production Engines
- **`yt-studio`**: Master 12-step hybrid documentary conductor with 3-Option Creator Choice Gate.
- **`yt-hybrid-production`**: Hybrid provider resolver & credit budget guard (`provider_engine.py`).
- **`yt-voice`**: Pakistani Urdu TTS selector, pronunciation benchmark, and number normalizer (`urdu_voice_engine.py`).
- **`yt-assets`**: Semantic story-to-shot director generating 70-95 cuts from verified manifests (`stock_director.py`).
- **`yt-audio`**: Broadcast audio mastering engine (-14 LUFS, -24 dB ducking, YouTube chapters) (`audio_manager.py`).
- **`yt-render`**: High-definition video assembler with Ken Burns motion and cue-synchronized ASS subtitles (`render_free.py`).
- **`yt-render-qc`**: Strict technical QA prober enforcing 360-420s duration bounds and EBU R128 compliance (`qa_media.py`).

### 3. Free Stock Footage & Documentary Workflows
- **`yt-stock-producer`**: Manifest licensing validation (`validate_manifest.py`).
- **`yt-voice-urdu`**: Native Pakistani Urdu voiceover production in Nastaliq script.
- **`yt-video-editor`**: Multi-track timeline assembly.
- **`yt-motion-graphics`**: Subtitle styling and mobile safe margins.
- **`yt-production-qa`**: Deterministic ffprobe quality check and human sign-off gate.
- **`yt-credit-guard`**: Third-party API protection and zero-credit enforcement (`credit_guard.py`).

### 4. Core Channel & Editorial Workflows (11)
- **`yt-script`**: Scriptwriting engine with 21 scored hook formulas (`hookscore.py`).
- **`yt-package`**: Title and thumbnail packaging linter (`title.py`).
- **`yt-edit`**: Edit decision lists from transcripts (`deadair.py`, `transcript.py`).
- **`yt-comment`**: 5-tier comment triage and authentic community engagement.
- **`yt-plan`**: Workload-calibrated content calendars.
- **`yt-viral`**: Competitor outlier ranking over median views (`swipe.py`).
- **`yt-retention`**: Audience retention diagnostic curves (`retention.py`).
- **`yt-shorts`**: 9:16 vertical extraction with rewritten hooks.
- **`yt-seo`**: Search-intent descriptions, value summaries, and tags.
- **`yt-chapters`**: YouTube 4-rule platform chapter validator (`chapters.py`).
- **`yt-audit`**: 5-pillar holistic channel diagnostic.

### 5. Advanced Studio Systems (6)
- **`yt-storyboard`**: Scene blocking, camera moves, and continuity bibles.
- **`yt-produce`**: Capability-aware AI video prompts.
- **`yt-localize`**: Multilingual adaptation for Pakistani Urdu audiences.
- **`yt-factcheck`**: Rigorous claim verification classifying evidence into `[VERIFIED]`, `[DISPUTED]`, `[UNSUPPORTED]`.
- **`yt-upload-prep`**: Pre-flight publication dossiers.
- **`yt-experiment`**: Controlled A/B testing scopes for YouTube Studio "Test & Compare".

---

## Python Utilities Suite

All 20 tools run on standard Python 3.10+ without mandatory paid dependencies:

```bash
# 1. Check system readiness (Chrome, Blender, FFmpeg, Pedalboard, OTIO)
python3 shared/scripts/browser_motion.py check
python3 shared/scripts/blender_parcel_render.py check
python3 shared/scripts/pedalboard_master.py check
python3 shared/scripts/otio_export.py check

# 2. Render 15-second browser motion graphics demo (42,000 files vs 6,000 plots)
python3 shared/scripts/browser_motion.py render \
  --html templates/motion/discrepancy_counter.html \
  --out output/demo_motion_15s.mp4 \
  --duration 15.0 --fps 30

# 3. Render 3D procedural land parcel visualization via Blender LTS
python3 shared/scripts/blender_parcel_render.py render \
  --out output/blender_parcel_3d.png \
  --frames 60 --fps 30

# 4. Master voiceover and apply -24 dB sidechain ducking
python3 shared/scripts/pedalboard_master.py master \
  --voice assets/voice/raw_urdu_narration.wav \
  --out output/mastered_voice.wav

python3 shared/scripts/pedalboard_master.py mix \
  --voice output/mastered_voice.wav \
  --music assets/audio/documentary_bed.mp3 \
  --out output/full_audio_mix.wav

# 5. Export multi-track timeline for NLE editing (.otio, .edl)
python3 shared/scripts/otio_export.py export \
  --manifest Stock_Footage_Manifest_22.csv \
  --motion output/demo_motion_15s.mp4 \
  --blender output/blender_parcel_3d.png \
  --voice output/mastered_voice.wav \
  --music output/full_audio_mix.wav \
  --out output/documentary_timeline.otio

# 6. Strict technical QA probing
python3 shared/scripts/qa_media.py \
  --media output/demo_motion_15s.mp4 \
  --min-duration 10.0 --max-duration 30.0
```

---

## Automated Quality Assurance

YouTube Agent Studio includes an automated test suite containing **109 unit, integration, and behavioral tests**:

```bash
# Run the complete test suite (100% passing)
python3 -m unittest discover -s tests -t . -v

# Build and validate all 3 release archives
python3 scripts/build-releases.py
```

---

## Open-Source Motion Skills & Third-Party Integration

- Integration instructions for `JakeB-5/motion-graphic-skill` and `haidrrrry/claude-remotion-skill` via official skills CLI are available in [docs/MOTION-SKILLS-INTEGRATION.md](docs/MOTION-SKILLS-INTEGRATION.md).
- Upstream unconfirmed-license skills (`abhimahamkali/claude-motion-skill`) are maintained as optional external links and not bundled into our core MIT release.

---

## Upstream Attribution, Maintainer & License

- **Original Upstream Author:** [Jake Schincariol](https://github.com/Jakeschincariol/youtube-agent-skill) ([`Jakeschincariol/youtube-agent-skill`](https://github.com/Jakeschincariol/youtube-agent-skill)).
- **Extension Architecture & Maintenance:** **ABDUL MUEED LASHARY** ([`islamically85-byte/youtube-agent-skill`](https://github.com/islamically85-byte/youtube-agent-skill)).
- **License:** Open-source under the **[MIT License](LICENSE)**.
- *Notice:* This repository is an independent open-source toolkit and is not officially affiliated with, sponsored by, or endorsed by Anthropic, OpenAI, Google, Blender Foundation, Spotify, or vidIQ.
