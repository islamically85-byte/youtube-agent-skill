# YouTube Agent Studio v2.0 — Free-First Documentary Production Edition

> **A professional, open-source production toolkit for YouTube creators — engineered natively for both Anthropic Claude and OpenAI ChatGPT.**
> **Extension Maintainer:** ABDUL MUEED LASHARY | **Upstream Author:** Jake Schincariol

[![Test & Build](https://github.com/islamically85-byte/youtube-agent-skill/actions/workflows/test.yml/badge.svg)](https://github.com/islamically85-byte/youtube-agent-skill/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](#python-utilities)
[![Platform: Claude & ChatGPT](https://img.shields.io/badge/Platform-Claude%20%7C%20ChatGPT-purple.svg)](#platform-editions)
[![FFmpeg Verified](https://img.shields.io/badge/FFmpeg-Multi--Track%20Assembly-red.svg)](#multi-track-video-assembly)

---

## What is YouTube Agent Studio?

YouTube Agent Studio transforms AI into a rigorous pair-programmer and production lead for YouTube creators. Rather than generating generic summaries or formulaic fluff, it provides **24 specialized production workflows** backed by **11 zero-dependency Python utilities** and a deterministic **FFmpeg multi-track video assembly engine**.

### Core Guarantees:
- **100% Free & Offline-First (Default Budget = 0 Credits)**: Core functionality requires no paid APIs, no subscriptions, no YouTube account logins, and no API keys.
- **Third-Party Quota Guarding**: Protects depleting third-party quotas (such as vidIQ) from accidental drain and blocks metered charges without explicit user authorization.
- **Documentary-Grade Real Footage**: Replaces AI slide shows and synthetic 3D gimmicks with authentic, permissively licensed stock video (Pexels, Pixabay, Mixkit, CC0).
- **Authentic Pakistani Urdu Narration**: Spoken scripts and subtitles authored strictly in native Perso-Arabic Urdu script (`اردو`) at ~130 WPM documentary pacing.
- **Objective Quality Gate (`TECHNICALLY_VALID_PENDING_REVIEW`)**: Probes media for black frames, loudness compliance (-14 LUFS), and licensing provenance without ever replacing mandatory human review.
- **Never Fabricates Metrics**: Does not invent analytics, competitor statistics, scientific citations, or publication outcomes.

---

## Dual Platform Architecture

YouTube Agent Studio provides two dedicated, independently maintainable distributions in the same repository:

| Feature | Claude Edition (`skills/`) | ChatGPT Edition (`chatgpt/`) |
|---|---|---|
| **Invocation** | Slash commands (`/yt-studio`, `/yt-script`, etc.) | Natural conversation & Master Orchestrator (`yt-studio`) |
| **Skill Count** | **24 Dedicated Skills** | **24 Dedicated Skills** |
| **Python Execution** | Local shell execution in Claude Code | Code Interpreter / local Python execution |
| **Package Asset** | `release/youtube-agent-claude.zip` | `release/youtube-agent-chatgpt-skill.zip`<br>`release/youtube-agent-chatgpt-plugin.zip` |
| **Installation Guide** | [docs/INSTALL-CLAUDE.md](docs/INSTALL-CLAUDE.md) | [docs/INSTALL-CHATGPT.md](docs/INSTALL-CHATGPT.md) |

---

## The 24-Workflow Studio Catalog

### 1. Studio Orchestration
- **`yt-studio`**: Master documentary conductor coordinating concept &rarr; research &rarr; script &rarr; Urdu narration &rarr; stock curation &rarr; FFmpeg assembly &rarr; QA &rarr; packaging.

### 2. Free Stock Footage & Documentary Production (New in v2.0)
- **`yt-stock-producer`**: Curates and registers permissive stock footage (Pexels, Pixabay, Mixkit, CC0) into a deterministic `project-manifest.json` with commercial licensing verification.
- **`yt-voice-urdu`**: Guides authentic Pakistani Urdu voiceover production in native script (`اردو`), ~130 WPM speech cadence, and broadcast audio mastering.
- **`yt-video-editor`**: Documentary timeline assembly via `render_free.py` (clip trimming, canvas scaling to 1080p, -24 dB audio ducking).
- **`yt-motion-graphics`**: Typographic design for Urdu RTL subtitles, clean lower-thirds, and 10% mobile safe-zone enforcement.
- **`yt-production-qa`**: Automated `ffprobe`/`ffmpeg` technical media prober via `qa_media.py`, awarding `TECHNICALLY_VALID_PENDING_REVIEW`.
- **`yt-credit-guard`**: Budget controller via `credit_guard.py` blocking unapproved third-party API deductions (e.g. vidIQ, ElevenLabs).

### 3. Core Channel & Editorial Workflows (11)
- **`yt-script`**: Scriptwriting engine across long-form, Shorts, and documentaries with 21 scored hook formulas.
- **`yt-package`**: Lints title and thumbnail as a single click surface with mobile (40 char) truncation checks.
- **`yt-edit`**: Generates Edit Decision Lists (EDL) from SRT, VTT, or Whisper JSON transcripts (dead air & filler cuts).
- **`yt-comment`**: 5-tier comment triage and authentic creator voice replies.
- **`yt-plan`**: Capacity-calibrated content calendars distinguishing anchor tentpole videos from low-friction Shorts.
- **`yt-viral`**: Ethical competitor intelligence ranking uploads by multiple over each channel's median views.
- **`yt-retention`**: Diagnoses hook leaks (first 30s), steep drop cliff moments, and pacing slides from CSV exports.
- **`yt-shorts`**: Extracts standalone 9:16 vertical clips from long transcripts with rewritten spoken hooks.
- **`yt-seo`**: Search-intent descriptions, above-the-fold value summaries, verified timestamps, and secondary tags.
- **`yt-chapters`**: Validates YouTube platform chapter constraints (starts at 00:00, >= 3 chapters, min 10s per chapter).
- **`yt-audit`**: 5-pillar holistic channel diagnostic delivering exactly **ONE highest-impact fix**.

### 4. Advanced Studio Systems (6)
- **`yt-storyboard`**: Converts scripts into shot-by-shot visual storyboards with camera angles and continuity bibles.
- **`yt-produce`**: Capability-aware AI video prompt generation for realistic live-action and explainers.
- **`yt-localize`**: Multilingual adaptation with native Pakistani Urdu script and culturally fluent phrasing.
- **`yt-factcheck`**: Rigorous claim verification classifying evidence into `[VERIFIED]`, `[DISPUTED]`, `[UNSUPPORTED]`, or `[REQUIRES CITATION]`.
- **`yt-upload-prep`**: Complete publication dossier with COPPA classification, synthetic disclosures, and audio checks.
- **`yt-experiment`**: Controlled A/B hypothesis design calibrated for YouTube Studio's "Test & Compare" tool.

---

## Python Utilities Suite

All tools run on standard Python 3.10+ without required external dependencies:

```bash
# 1. Validate project manifest & licensing provenance
python3 shared/scripts/validate_manifest.py --manifest project-manifest.json --strict

# 2. Check third-party credit budget & protect live balances
python3 shared/scripts/credit_guard.py --tool vidiq --action competitor_research

# 3. Render multi-track documentary video with ducked music & subtitles
python3 shared/scripts/render_free.py --manifest project-manifest.json --output master.mp4

# 4. Probe rendered media for technical QA compliance
python3 shared/scripts/qa_media.py --media master.mp4 --manifest project-manifest.json

# 5. Universal transcript parser (SRT, VTT, Whisper JSON)
python3 shared/scripts/transcript.py transcript.srt --language ur

# 6. Score hook against 21 creator formulas
python3 shared/scripts/hookscore.py --hook "97% of creators quit before video 30"

# 7. Lint title & thumbnail pairing
python3 shared/scripts/title.py --title "Why 97% of Creators Quit" --thumb "STOP QUITTING"

# 8. Generate Edit Decision List (EDL) from pauses
python3 shared/scripts/deadair.py transcript.srt --floor 0.35 --json

# 9. Validate YouTube platform chapters
python3 shared/scripts/chapters.py transcript.srt --target 8

# 10. Diagnose audience retention leaks
python3 shared/scripts/retention.py retention.csv --transcript transcript.srt

# 11. Rank competitor outliers against channel median
python3 shared/scripts/swipe.py competitor_videos.json --min 2.0
```

---

## Automated Quality Assurance

YouTube Agent Studio includes an automated test suite containing **72 unit, integration, and behavioral tests**:

```bash
# Run the complete test suite
python3 -m unittest discover -s tests -t . -v

# Run synthetic video render demo
python3 shared/scripts/render_free.py --synthetic

# Build and validate release archives
python3 scripts/build-releases.py
```

---

## Upstream Attribution, Maintainer & License

- **Original Project & MIT Attribution:** [Jake Schincariol](https://github.com/Jakeschincariol/youtube-agent-skill) ([`Jakeschincariol/youtube-agent-skill`](https://github.com/Jakeschincariol/youtube-agent-skill)).
- **Extension Architecture & Maintenance:** **ABDUL MUEED LASHARY** ([`islamically85-byte/youtube-agent-skill`](https://github.com/islamically85-byte/youtube-agent-skill)).
- **License:** Open-source under the **[MIT License](LICENSE)**.
- *Notice:* This repository is an independent open-source toolkit and is not officially affiliated with, sponsored by, or endorsed by Anthropic, OpenAI, Google, or vidIQ.
