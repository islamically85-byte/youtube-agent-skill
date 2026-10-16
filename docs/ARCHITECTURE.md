# YouTube Agent Studio Architecture & Data Contracts

**Extension Maintainer:** ABDUL MUEED LASHARY  
**Upstream Author & MIT Attribution:** Jake Schincariol  
**Version:** 3.0.0  
**License:** MIT  

---

## Directory Layout

```
youtube-agent-skill/
├── .claude-plugin/              # Claude Code Plugin metadata
│   ├── plugin.json              # Version 3.0.0 Claude manifest
│   └── marketplace.json         # Marketplace distribution schema
│
├── skills/                      # 30 Upgraded Claude Skills (Self-Contained)
│   ├── yt-studio/               # Master 12-Step Hybrid Production Studio
│   ├── yt-hybrid-production/    # Provider resolution & credit budget verification (provider_engine.py)
│   ├── yt-voice/                # Pakistani Urdu TTS benchmark & phonetic normalizer (urdu_voice_engine.py)
│   ├── yt-assets/               # Stock footage director & semantic shot planner (stock_director.py)
│   ├── yt-audio/                # Broadcast audio mastering & ducking engine (audio_manager.py)
│   ├── yt-render/               # Multi-track FFmpeg renderer & ASS motion subtitles (render_free.py)
│   ├── yt-render-qc/            # Strict duration & technical QA gate (qa_media.py)
│   ├── yt-stock-producer/       # Stock footage curation & licensing (validate_manifest.py)
│   ├── yt-voice-urdu/           # Pakistani Urdu voiceover & audio mastering
│   ├── yt-video-editor/         # FFmpeg multi-track video assembly
│   ├── yt-motion-graphics/      # RTL Urdu typography, safe margins, subtitles
│   ├── yt-production-qa/        # Automated media QA & human gate
│   ├── yt-credit-guard/         # Quota protection & zero-credit budget (credit_guard.py)
│   ├── yt-script/               # Scripts, 21 hook formulas, hookscore.py
│   ├── yt-package/              # Title & thumbnail linter (title.py)
│   ├── yt-edit/                 # EDL generator (deadair.py, transcript.py)
│   ├── yt-comment/              # 5-tier comment triage
│   ├── yt-plan/                 # Content calendar & workload sizing
│   ├── yt-viral/                # Competitor outlier ranking (swipe.py)
│   ├── yt-retention/            # Retention curve diagnostic (retention.py)
│   ├── yt-shorts/               # 9:16 vertical clip extraction
│   ├── yt-seo/                  # Semantic search descriptions & tags
│   ├── yt-chapters/             # YouTube 4-rule chapter validator (chapters.py)
│   ├── yt-audit/                # 5-pillar channel diagnostic
│   ├── yt-storyboard/           # Scene blocking, camera moves, continuity
│   ├── yt-produce/              # Capability-aware AI video prompts
│   ├── yt-localize/             # Multilingual adaptation (Pakistani Urdu)
│   ├── yt-factcheck/            # Claim verification & citation audit
│   ├── yt-upload-prep/          # Pre-flight upload dossier
│   └── yt-experiment/           # A/B testing & Test & Compare scopes
│
├── chatgpt/                     # Dedicated ChatGPT Edition
│   ├── plugin.json              # OpenAI Plugin v1 manifest
│   ├── .codex-plugin/           # Codex developer environment manifest
│   ├── skills/                  # 30 Specialized workflows matching Claude
│   ├── templates/               # Portable channel profiles & screenplays
│   ├── references/              # Guides (Urdu, Factcheck, Chapters, Packaging)
│   ├── scripts/                 # 16 standalone Python tools for Code Interpreter
│   ├── schemas/                 # Project manifest & QA report schemas
│   └── README.md                # Dedicated ChatGPT documentation
│
├── shared/                      # Core Shared Assets & Schemas
│   ├── scripts/                 # Canonical Python standard library tools
│   │   ├── provider_engine.py   # Hybrid provider router & credit guard
│   │   ├── urdu_voice_engine.py # Pakistani Urdu pronunciation & 20-40s benchmark
│   │   ├── stock_director.py    # Semantic story-to-shot director (70-95 shots)
│   │   ├── editorial_motion.py  # Cue-synchronized ASS subtitles with allegations disclaimers
│   │   ├── audio_manager.py     # Broadcast audio mastering (-14 LUFS, -24 dB ducking)
│   │   ├── render_free.py       # FFmpeg video timeline renderer
│   │   ├── qa_media.py          # Technical QA prober with strict duration bounds
│   │   ├── validate_manifest.py # Manifest schema and license checker
│   │   └── credit_guard.py      # Zero-budget credit balance protector
│   ├── schemas/                 # JSON Schemas (project-manifest, qa-report, etc.)
│   └── fixtures/                # Real-world test fixtures & synthetic demo assets
│
├── templates/                   # Channel profiles and production screenplays
│   ├── channel-profiles/
│   │   └── pakistani-urdu-awareness.yaml
│   └── documentaries/
│       └── pakistan_property_screenplay.txt # 6-7 minute Urdu investigative screenplay
│
├── tests/                       # Automated Test Suite (95 Tests, 100% Passing)
│   ├── test_provider_engine.py  # Provider state, fallback, and ledger tests
│   ├── test_urdu_voice_engine.py# Benchmark passage, numerals, and chunking tests
│   ├── test_stock_director.py   # EDL generation, 70-95 shots, and manifest row tests
│   ├── test_audio_manager.py    # Loudness, ducking, chapters, and missing music tests
│   ├── test_editorial_motion.py # Synchronized ASS generation & disclaimer tests
│   ├── test_qa_media.py         # Strict duration bounds & loudness QA tests
│   ├── test_skills_structure.py # Skill frontmatter validator (all 30 skills)
│   └── ...                      # Comprehensive creators suite tests
│
├── scripts/
│   └── build-releases.py        # Packaging and validation script
│
├── release/                     # Validated Release Assets
│   ├── youtube-agent-claude.zip
│   ├── youtube-agent-chatgpt-skill.zip
│   └── youtube-agent-chatgpt-plugin.zip
│
├── .github/workflows/           # CI/CD Workflows
│   ├── test.yml                 # Matrix testing on Python 3.10-3.13
│   └── render-urdu-stock-documentary.yml # End-to-end cloud rendering pipeline
│
├── README.md                    # Main Repository README
├── CHANGELOG.md                 # Version History
└── LICENSE                      # MIT Open Source License
```

---

## Data Contracts & Output Schemas

All core tools return structured JSON whenever `--json` is passed:

1. **`provider_engine.py`**:
   - Resolves provider state across `AVAILABLE`, `NO_CREDITS`, `NOT_CONNECTED`, `UNSUPPORTED_LANGUAGE`, `RATE_LIMITED`.
   - Records all choices in an auditable ledger: `{ "resolved_provider": str, "provider_tier": str, "state": str, "ledger": dict }`.

2. **`urdu_voice_engine.py`**:
   - Evaluates audio against empirical 20-40s benchmark passage with required keywords.
   - Normalizes numbers and acronyms: `{ "benchmark_passed": bool, "word_count": int, "measured_duration_sec": float, "calculated_wpm": float, "requires_human_listening_review": true }`.

3. **`stock_director.py`**:
   - Generates 70–95 shot EDL mapping narration acts to verified footage with intelligent reuse spacing.
   - Returns `{ "manifest_rows_count": int, "total_edl_shots": int, "target_duration_sec": float, "avg_shot_duration_sec": float }`.

4. **`audio_manager.py`**:
   - Broadcast audio mixing: -14.0 LUFS dialogue, -24.0 dB ducking, missing music warning detection.
   - Generates YouTube chapters: `{ "voice_lufs": float, "music_attenuation_db": float, "music_present": bool, "missing_music_warning": str|null, "youtube_chapters": list }`.

5. **`qa_media.py`**:
   - Probes media file with `ffprobe` and `ffmpeg` (blackdetect, ebur128).
   - Enforces strict duration bounds (360.0s – 420.0s for 6–7 min documentary).
   - Returns `{ "status": "TECHNICALLY_VALID_PENDING_REVIEW"|"FAILED_CRITICAL_CHECKS", "probed_metrics": dict, "automated_checks": dict, "mandatory_human_review_items": list }`.
