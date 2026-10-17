# Changelog — YouTube Agent Studio

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-10-17

### Added
- **Free-First Stock Footage Documentary Production**:
  - Expanded toolkit from script/SEO ideation into real, playable video production using permissive stock footage (Pexels, Pixabay, Mixkit, CC0).
  - Added seven new production skills across both Claude and ChatGPT:
    * `yt-studio`: Master documentary production orchestrator.
    * `yt-stock-producer`: Permissive stock video curation and licensing provenance tracking.
    * `yt-voice-urdu`: Fluent Pakistani Urdu voiceover guidance, 130 WPM cadence, and audio mastering.
    * `yt-video-editor`: Timeline planning and multi-track assembly via FFmpeg.
    * `yt-motion-graphics`: RTL Urdu typography, safe margins, and subtitles.
    * `yt-production-qa`: Automated technical QA probing via `qa_media.py`.
    * `yt-credit-guard`: Third-party quota protection and zero-credit budget enforcement.
- **Four Production Python Tools**:
  - `shared/scripts/validate_manifest.py`: Validates `project-manifest.json` against licensing classes and timeline rules.
  - `shared/scripts/credit_guard.py`: Enforces zero-credit baseline and prevents accidental depletion of third-party balances (e.g. vidIQ).
  - `shared/scripts/render_free.py`: Multi-track FFmpeg engine combining stock clips, -14.0 LUFS dialogue, -24.0 dB ducked music, and cross-platform path escaping.
  - `shared/scripts/qa_media.py`: Technical prober evaluating black frames, EBU R128 loudness, and emitting `TECHNICALLY_VALID_PENDING_REVIEW`.
- **JSON Schemas**:
  - `shared/schemas/project-manifest.schema.json`
  - `shared/schemas/qa-report.schema.json`
- **Research Note**: Added `docs/RESEARCH-NOTE-FREE-PRODUCTION.md` analyzing stock licensing classes, vidIQ credit depletion, Pakistani Urdu TTS landscape, and zero-credit production routes.
- **Test Suite Expansion**: Added 16 new unit tests, bringing the automated test suite to 72 passing tests.

### Maintained By
- Extended, architected, and maintained by **ABDUL MUEED LASHARY**. Upstream MIT copyright and attribution strictly preserved for original author Jake Schincariol.

---

## [2.0.0] - 2026-10-16

### Added
- **Dual Platform Support**: Built dedicated, independently maintainable editions for both **Anthropic Claude** and **OpenAI ChatGPT**.
- **Master ChatGPT Orchestrator (`yt-studio`)**: Higher-level conversational workflow that interprets creator goals, dispatches specialized skills, and maintains shared context across scripts, storyboards, and packaging.
- **Six Advanced Workflows**:
  - `yt-storyboard`: Shot-by-shot visual blocking, camera moves, and character continuity sheets.
  - `yt-produce`: AI video generation prompt coordination with positive and negative constraints.
  - `yt-localize`: Multilingual adaptation featuring native Pakistani Urdu script (`اردو`), ~130 WPM pacing, and RTL considerations.
  - `yt-factcheck`: Script claim verification, source auditing, and zero-hallucination protections.
  - `yt-upload-prep`: Complete pre-flight publication dossier with compliance and synthetic media disclosures.
  - `yt-experiment`: Controlled A/B hypothesis design for YouTube Studio's "Test & Compare" feature.
- **Universal Transcript Engine (`transcript.py`)**: Zero-dependency parser supporting SRT, WebVTT (with cue settings/tags), Whisper JSON, WhisperX, and YouTube TimedText JSON with full Unicode/RTL support.
- **Automated Test Suite**: 56 unit and behavioral evaluation tests covering all Python helpers, skill frontmatter, manifest schemas, and edge cases.
- **Release Automation (`build-releases.py`)**: Automated packaging generating validated ZIP archives:
  - `youtube-agent-claude.zip`
  - `youtube-agent-chatgpt-skill.zip`
  - `youtube-agent-chatgpt-plugin.zip`
- **Channel Profile Specifications**: Portable YAML/JSON channel profile schemas with a complete sample for a Pakistani Urdu psychological awareness channel.
- **Comprehensive Documentation Suite**: Added `AUDIT-REPORT.md`, `INSTALL-CLAUDE.md`, `INSTALL-CHATGPT.md`, `COMPATIBILITY.md`, `ARCHITECTURE.md`, `SECURITY.md`, and `CONTRIBUTING.md`.
- **GitHub Actions CI**: Automated test discovery and packaging verification workflow across Python 3.10–3.13.

### Changed
- **Self-Contained Skill Packaging**: Fixed broken cross-directory relative imports in `yt-chapters`, `yt-retention`, and `yt-viral`. Every skill directory is now 100% self-contained.
- **Fortified Python Utilities**:
  - Rewrote manual `sys.argv` indexing to standard `argparse` CLI interfaces.
  - Added structured `--json` output across all six tools.
  - Added safe decimal and percentage string parsing in `retention.py` and handled Shorts rewatch loops (>100% retention).
  - Fixed falsy zero bugs in retention analysis.
  - Handled formatted strings (e.g. "45.5K", "1.2M") safely in `swipe.py` and flagged small channel sample sizes (<4 uploads).
- **Upgraded 11 Original Workflows**: Enhanced long-form, Shorts, educational, talking-head, and faceless guidance in `yt-script`, `yt-package`, `yt-edit`, `yt-comment`, `yt-plan`, `yt-viral`, `yt-retention`, `yt-shorts`, `yt-seo`, `yt-chapters`, and `yt-audit`.
- **Manifest Updates**: Updated `.claude-plugin/plugin.json` and `marketplace.json` to v2.0.0 and added `chatgpt/plugin.json`.

---

## [1.0.0] - 2026-09-16
- Initial release by Jake Schincariol with 11 Claude skills and 6 Python utilities.
