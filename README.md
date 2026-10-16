# YouTube Agent Studio v2.0

> **A professional, open-source production toolkit for YouTube creators — engineered natively for both Anthropic Claude and OpenAI ChatGPT.**

[![Test & Build](https://github.com/islamically85-byte/youtube-agent-skill/actions/workflows/test.yml/badge.svg)](https://github.com/islamically85-byte/youtube-agent-skill/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](#python-utilities)
[![Platform: Claude & ChatGPT](https://img.shields.io/badge/Platform-Claude%20%7C%20ChatGPT-purple.svg)](#platform-editions)

---

## What is YouTube Agent Studio?

YouTube Agent Studio transforms AI into a rigorous pair-programmer for YouTube creators. Rather than generating generic summaries or formulaic fluff, it provides **17 specialized production workflows** backed by **seven zero-dependency Python utilities**.

### Core Guarantees:
- **100% Free & Offline-First**: No paid APIs, subscriptions, YouTube account logins, or API keys are required for core functionality.
- **Never Fabricates Metrics**: Does not invent analytics, competitor statistics, scientific studies, or publication outcomes.
- **You Remain in Control**: Every workflow concludes with an actionable artifact and the question: **Ship it, or change it?** Nothing is published automatically.

---

## Dual Platform Editions

YouTube Agent Studio provides two dedicated, independently maintainable distributions in the same repository:

| Feature | Claude Edition (`skills/`) | ChatGPT Edition (`chatgpt/`) |
|---|---|---|
| **Invocation** | Slash commands (`/yt-script`, `/yt-package`, etc.) | Natural conversation & Master Orchestrator (`yt-studio`) |
| **Skill Count** | 17 Dedicated Skills | 18 Workflows (17 Specialized + `yt-studio` Orchestrator) |
| **Python Execution** | Local shell execution in Claude Code | Code Interpreter / local Python execution |
| **Package Asset** | `release/youtube-agent-claude.zip` | `release/youtube-agent-chatgpt-skill.zip`<br>`release/youtube-agent-chatgpt-plugin.zip` |
| **Installation Guide** | [docs/INSTALL-CLAUDE.md](docs/INSTALL-CLAUDE.md) | [docs/INSTALL-CHATGPT.md](docs/INSTALL-CHATGPT.md) |

---

## The Workflow Catalog

### Upgraded Core Workflows (11)
1. **`yt-script`**: Scriptwriting engine across long-form, Shorts, educational, faceless, and talking-head formats. Evaluates hooks against 21 creator formulas with language-aware speech rates.
2. **`yt-package`**: Lints title and thumbnail as a single click surface. Checks mobile (40 char) and desktop (60 char) truncation, shouting, buzzwords, and keyword repetition.
3. **`yt-edit`**: Generates Edit Decision Lists (EDL) from SRT, VTT, or Whisper JSON transcripts. Pinpoints dead-air pauses, verbal fillers, and repeated restart takes.
4. **`yt-comment`**: 5-tier comment triage (questions, feedback, appreciation, moderation, noise) and authentic voice replies.
5. **`yt-plan`**: Capacity-calibrated content calendars distinguishing anchor tentpole videos from low-friction Shorts.
6. **`yt-viral`**: Ethical competitor intelligence ranking uploads by multiple over each channel's own median view count.
7. **`yt-retention`**: Diagnoses hook leaks (first 30s), steep drop cliff moments, and pacing slides from YouTube Studio CSV exports.
8. **`yt-shorts`**: Extracts standalone 9:16 vertical clips from long transcripts with rewritten spoken hooks and loop engineering.
9. **`yt-seo`**: Search-intent descriptions, above-the-fold value summaries, verified timestamps, and secondary tags.
10. **`yt-chapters`**: Validates YouTube's platform chapter constraints (starts at 00:00, >= 3 chapters, min 10s per chapter).
11. **`yt-audit`**: 5-pillar holistic channel diagnostic delivering exactly **ONE highest-impact fix**.

### Advanced Studio Workflows (6 New)
12. **`yt-storyboard`**: Converts scripts into shot-by-shot visual storyboards with camera angles, subject blocking, lighting, and continuity bibles.
13. **`yt-produce`**: Capability-aware AI video prompt generation for realistic live-action, 3D animation, and explainers with positive and negative constraints.
14. **`yt-localize`**: Professional multilingual localization with native Pakistani Urdu script (`اردو`), ~130 WPM cadence adjustments, and RTL formatting.
15. **`yt-factcheck`**: Rigorous claim verification classifying evidence into `[VERIFIED]`, `[DISPUTED]`, `[UNSUPPORTED]`, or `[REQUIRES CITATION]` with zero-hallucination rules.
16. **`yt-upload-prep`**: Complete publication dossier with COPPA audience classification, synthetic-media disclosures, and audio LUFS pre-flight checklists.
17. **`yt-experiment`**: Controlled A/B hypothesis design calibrated for YouTube Studio's native "Test & Compare" thumbnail tool.

### Master Orchestration (ChatGPT)
18. **`yt-studio`**: Central conductor that interprets conversational creator requests, sequences skills, verifies cross-asset consistency, and delivers consolidated production packages.

---

## Quickstart Installation

### Claude Code Installation
```bash
# Direct marketplace installation
/plugin marketplace add islamically85-byte/youtube-agent-skill
/plugin install youtube-agent

# Or clone and copy into user skills folder
git clone https://github.com/islamically85-byte/youtube-agent-skill.git
cp -r youtube-agent-skill/skills/yt-* ~/.claude/skills/
```

### ChatGPT Installation
1. Download `release/youtube-agent-chatgpt-skill.zip` (or `youtube-agent-chatgpt-plugin.zip`).
2. In ChatGPT, upload the skill archive into your Custom GPT configuration.
3. Enable **Code Interpreter** to execute the Python tools.
4. See [docs/INSTALL-CHATGPT.md](docs/INSTALL-CHATGPT.md) for step-by-step instructions.

---

## Python Utilities (Zero External Dependencies)

All tools run on standard Python 3.10+ without `pip install`:

```bash
# Universal transcript parsing (SRT, VTT, Whisper JSON)
python3 shared/scripts/transcript.py transcript.srt --language ur

# Score a hook against 21 creator formulas
python3 shared/scripts/hookscore.py --hook "97% of creators quit before video 30"

# Lint title & thumbnail pairing
python3 shared/scripts/title.py --title "Why 97% of Creators Quit" --thumb "STOP QUITTING"

# Generate Edit Decision List (EDL) from transcript
python3 shared/scripts/deadair.py transcript.srt --floor 0.35 --json

# Validate YouTube platform chapters
python3 shared/scripts/chapters.py transcript.srt --target 8

# Diagnose audience retention leaks
python3 shared/scripts/retention.py retention.csv --transcript transcript.srt

# Rank competitor outliers against channel median
python3 shared/scripts/swipe.py competitor_videos.json --min 2.0
```

---

## Example ChatGPT Orchestration

You can prompt ChatGPT conversationally without remembering commands:

> **"Create a complete YouTube production package about emotional abuse, in Pakistani Urdu, with four realistic 10-second video scenes, a thumbnail concept, video metadata and an upload checklist."**

`yt-studio` will automatically:
1. Verify clinical psychological claims via `yt-factcheck`.
2. Lint non-overlapping packaging via `yt-package`.
3. Draft a spoken script in authentic Pakistani Urdu script (`اردو`) via `yt-script` & `yt-localize`.
4. Generate 4 modular 10-second realistic video generation prompts with negative constraints via `yt-produce`.
5. Assemble description, validated chapters, and compliance disclosures via `yt-upload-prep`.

---

## Automated Quality Assurance

YouTube Agent Studio includes an automated test suite with **56 unit, integration, and behavioral tests**:

```bash
# Run the complete test suite
python3 -m unittest discover -s tests -t . -v

# Build and validate release archives
python3 scripts/build-releases.py
```

---

## Documentation Directory
- [Audit Findings & Remediation](docs/AUDIT-REPORT.md)
- [Claude Installation Guide](docs/INSTALL-CLAUDE.md)
- [ChatGPT Installation Guide](docs/INSTALL-CHATGPT.md)
- [Compatibility & Comparison Matrix](docs/COMPATIBILITY.md)
- [Repository Architecture](docs/ARCHITECTURE.md)
- [Security & Integrity Policy](docs/SECURITY.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

---

## Upstream Attribution & License

- Original project by [Jake Schincariol](https://github.com/Jakeschincariol/youtube-agent-skill).
- Extended, architected, and maintained by **ABDUL MUEED LASHARY**.
- Released under the open-source **[MIT License](LICENSE)**.
