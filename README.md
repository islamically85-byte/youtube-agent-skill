# YouTube Agent Studio v3.0 — Hybrid Video Production Edition

> **A professional, production-capable hybrid creator studio for YouTube — engineered natively for both Anthropic Claude and OpenAI ChatGPT.**  
> **Extension Maintainer:** ABDUL MUEED LASHARY | **Upstream Author:** Jake Schincariol

[![Test & Build](https://github.com/islamically85-byte/youtube-agent-skill/actions/workflows/test.yml/badge.svg)](https://github.com/islamically85-byte/youtube-agent-skill/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](#python-utilities)
[![Platform: Claude & ChatGPT](https://img.shields.io/badge/Platform-Claude%20%7C%20ChatGPT-purple.svg)](#platform-editions)
[![FFmpeg Verified](https://img.shields.io/badge/FFmpeg-Broadcast%20Rendering-red.svg)](#multi-track-video-assembly)

---

## What is YouTube Agent Studio v3.0?

YouTube Agent Studio v3.0 upgrades our production toolkit into a **production-capable hybrid creator studio**. It leverages premium third-party APIs (ElevenLabs, Azure, Runway, vidIQ) when connected, authorized, and credited — while guaranteeing a completely supported, zero-budget fallback to local open-source tools (FFmpeg, Piper Urdu, Python stdlib) with no loss in documentary rigor.

### Core Guarantees:
- **Hybrid Provider Resolution (Default Budget = 0 Credits)**: Core functionality never charges any paid account without prior explicit user confirmation and cost estimation.
- **Strict Quality Control & Duration Bounds**: Enforces exact documentary runtime constraints (360.0s – 420.0s for 6–7 minute documentaries); short narration tracks are rejected by QA rather than exported with warnings.
- **Documentary-Grade Real Stock Footage**: Generates 70–95 semantic cuts per 6.5-minute timeline from verified permissive stock (Pexels, Pixabay, Mixkit, CC0) without slide-show gimmicks or fake AI morphs.
- **Authentic Pakistani Urdu Narration**: Screenplays and subtitles written in native Perso-Arabic Urdu script (`اردو`), benchmarked against an empirical 20–40s test passage covering key numerals and regulatory bodies (`سی ڈی اے`, `این او سی`, `ایس ای سی پی`, `نیب`).
- **Broadcast Audio Standards**: Voiceover mastered to **-14.0 LUFS** with automatic **-24.0 dB** background score ducking and explicit `MISSING_MUSIC_WARNING` detection.
- **Reported Allegations Compliance**: All investigative figures (such as 42,000 files vs 6,000 plots, Rs 16B inquiry, 7 arrests) are strictly badged as **REPORTED ALLEGATIONS** (`رپورٹ کردہ الزامات`) with explicit presumption-of-innocence disclaimers.

---

## Dual Platform Architecture

YouTube Agent Studio provides two dedicated, independently maintainable distributions in the same repository:

| Feature | Claude Edition (`skills/`) | ChatGPT Edition (`chatgpt/`) |
|---|---|---|
| **Invocation** | Slash commands (`/yt-studio`, `/yt-script`, etc.) | Natural conversation & Master Orchestrator (`yt-studio`) |
| **Skill Count** | **30 Dedicated Skills** | **30 Dedicated Skills** |
| **Python Execution** | Local shell execution in Claude Code | Code Interpreter / local Python execution |
| **Package Asset** | `release/youtube-agent-claude.zip` | `release/youtube-agent-chatgpt-skill.zip`<br>`release/youtube-agent-chatgpt-plugin.zip` |
| **Installation Guide** | [docs/INSTALL-CLAUDE.md](docs/INSTALL-CLAUDE.md) | [docs/INSTALL-CHATGPT.md](docs/INSTALL-CHATGPT.md) |

---

## The 30-Workflow Studio Catalog

### 1. Hybrid Studio & Production Engines (New in v3.0)
- **`yt-studio`**: Master 12-step hybrid documentary conductor coordinating provider resolution, fact-checking, narration, stock editing, audio mastering, rendering, and QA.
- **`yt-hybrid-production`**: Hybrid provider resolver & credit budget guard (`provider_engine.py`).
- **`yt-voice`**: Pakistani Urdu TTS selector, 20-40s pronunciation benchmark, and number/acronym normalizer (`urdu_voice_engine.py`).
- **`yt-assets`**: Semantic story-to-shot director generating 70-95 cuts from verified manifests (`stock_director.py`).
- **`yt-audio`**: Broadcast audio mastering engine (-14 LUFS, -24 dB ducking, YouTube chapters) (`audio_manager.py`).
- **`yt-render`**: High-definition video assembler with Ken Burns motion and cue-synchronized ASS subtitles (`render_free.py`, `editorial_motion.py`).
- **`yt-render-qc`**: Strict technical QA prober enforcing 360-420s duration bounds and EBU R128 compliance (`qa_media.py`).

### 2. Free Stock Footage & Documentary Workflows
- **`yt-stock-producer`**: Manifest licensing validation (`validate_manifest.py`).
- **`yt-voice-urdu`**: Native Pakistani Urdu voiceover production in Nastaliq script.
- **`yt-video-editor`**: Multi-track timeline assembly.
- **`yt-motion-graphics`**: Subtitle styling and mobile safe margins.
- **`yt-production-qa`**: Deterministic ffprobe quality check and human sign-off gate.
- **`yt-credit-guard`**: Third-party API protection and zero-credit enforcement (`credit_guard.py`).

### 3. Core Channel & Editorial Workflows (11)
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

### 4. Advanced Studio Systems (6)
- **`yt-storyboard`**: Scene blocking, camera moves, and continuity bibles.
- **`yt-produce`**: Capability-aware AI video prompts.
- **`yt-localize`**: Multilingual adaptation for Pakistani Urdu audiences.
- **`yt-factcheck`**: Rigorous claim verification classifying evidence into `[VERIFIED]`, `[DISPUTED]`, `[UNSUPPORTED]`.
- **`yt-upload-prep`**: Pre-flight publication dossiers.
- **`yt-experiment`**: Controlled A/B testing scopes for YouTube Studio "Test & Compare".

---

## Python Utilities Suite

All 16 tools run on standard Python 3.10+ without mandatory paid dependencies:

```bash
# 1. Inspect hybrid provider status & credit budget ledger
python3 shared/scripts/provider_engine.py --status --json

# 2. Evaluate Pakistani Urdu pronunciation benchmark (20-40s standard passage)
python3 shared/scripts/urdu_voice_engine.py --test-passage

# 3. Analyze & normalize 6-7 minute Urdu documentary screenplay
python3 shared/scripts/urdu_voice_engine.py --script templates/documentaries/pakistan_property_screenplay.txt --normalize

# 4. Generate 70-95 shot EDL from licensed stock manifest
python3 shared/scripts/stock_director.py --manifest Stock_Footage_Manifest_22.csv --duration 390.0 --out edit_decisions.json

# 5. Master broadcast audio (-14 LUFS voice, -24 dB ducked music, YouTube chapters)
python3 shared/scripts/audio_manager.py --voice voice.wav --music score.mp3 --duration 390.0 --out master_audio.m4a --meta audio_mix.json

# 6. Generate cue-synchronized ASS motion subtitles with allegations disclaimers
python3 shared/scripts/editorial_motion.py --output documentary_motion.ass

# 7. Render master 1080p MP4 documentary
python3 shared/scripts/render_free.py --manifest project-manifest.json --audio master_audio.m4a --subtitles documentary_motion.ass --output exports/master.mp4

# 8. Strict technical QA probing (rejecting durations < 360s)
python3 shared/scripts/qa_media.py --media exports/master.mp4 --manifest audio_mix.json --min-duration 360.0 --max-duration 420.0 --require-music
```

---

## Automated Quality Assurance

YouTube Agent Studio includes an automated test suite containing **95 unit, integration, and behavioral tests**:

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
