# YouTube Agent Studio Architecture & Data Contracts

**Extension Maintainer:** ABDUL MUEED LASHARY  
**Upstream Author & MIT Attribution:** Jake Schincariol  
**Version:** 2.1.0  
**License:** MIT  

---

## Directory Layout

```
youtube-agent-skill/
├── .claude-plugin/              # Claude Code Plugin metadata
│   ├── plugin.json              # Version 2.0.0 Claude manifest
│   └── marketplace.json         # Marketplace distribution schema
│
├── skills/                      # 24 Upgraded Claude Skills (Self-Contained)
│   ├── yt-studio/               # Master Documentary Production Studio
│   ├── yt-stock-producer/       # Stock footage curation & licensing (validate_manifest.py)
│   ├── yt-voice-urdu/           # Pakistani Urdu voiceover & audio mastering
│   ├── yt-video-editor/         # FFmpeg multi-track video assembly (render_free.py)
│   ├── yt-motion-graphics/      # RTL Urdu typography, safe margins, subtitles
│   ├── yt-production-qa/        # Automated media QA & human gate (qa_media.py)
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
│   ├── skills/                  # 24 Specialized workflows matching Claude
│   ├── templates/               # Portable channel profiles
│   ├── references/              # Guides (Urdu, Factcheck, Chapters, Packaging)
│   ├── scripts/                 # 11 standalone Python tools for Code Interpreter
│   ├── schemas/                 # Project manifest & QA report schemas
│   └── README.md                # Dedicated ChatGPT documentation
│
├── shared/                      # Core Shared Assets & Schemas
│   ├── scripts/                 # Canonical Python standard library tools
│   ├── schemas/                 # JSON Schemas (project-manifest, qa-report, etc.)
│   └── fixtures/                # Real-world test fixtures & synthetic demo assets
│
├── templates/                   # Channel profiles and voice configurations
│   ├── voice.md                 # Spoken voice and forbidden words
│   ├── channel-profile-template.yaml
│   └── channel-profiles/
│       └── pakistani-urdu-awareness.yaml
│
├── docs/                        # Complete Engineering Documentation
│   ├── RESEARCH-NOTE-FREE-PRODUCTION.md # Stock licensing, vidIQ audit, Urdu TTS benchmark
│   ├── AUDIT-REPORT.md          # Baseline audit findings and remediation
│   ├── INSTALL-CLAUDE.md        # Claude installation guide
│   ├── INSTALL-CHATGPT.md       # ChatGPT installation guide
│   ├── COMPATIBILITY.md         # Claude vs. ChatGPT comparison matrix
│   ├── ARCHITECTURE.md          # Architecture & data contract specs
│   ├── SECURITY.md              # Security, privacy, and integrity model
│   └── CONTRIBUTING.md          # Open-source contribution guidelines
│
├── tests/                       # Automated Test Suite (72 Tests, 100% Passing)
│   ├── test_validate_manifest.py # Manifest & license provenance tests
│   ├── test_credit_guard.py     # Quota budget & balance protection tests
│   ├── test_render_free.py      # FFmpeg command builder & path escaping tests
│   ├── test_qa_media.py         # Media prober & EBU R128 loudness tests
│   ├── test_transcript.py       # Universal transcript loader tests
│   ├── test_hookscore.py        # 5-property panel tests
│   ├── test_title.py            # Packaging linter tests
│   ├── test_deadair.py          # EDL generator tests
│   ├── test_chapters.py         # YouTube chapter constraint tests
│   ├── test_retention.py        # CSV retention analysis tests
│   ├── test_swipe.py            # Outlier multiple tests
│   ├── test_skills_structure.py # Skill frontmatter validator (all 24 skills)
│   ├── test_manifests.py        # Claude & ChatGPT manifest tests
│   ├── test_packaging.py        # Zip archive verification tests
│   └── evals/                   # 20 Behavioral evaluation scenarios
│       └── test_behavioral_evals.py
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
│   └── test.yml                 # Matrix testing on Python 3.10-3.13
│
├── README.md                    # Main Repository README
├── CHANGELOG.md                 # Version History
└── LICENSE                      # MIT Open Source License
```

---

## Data Contracts & Output Schemas

All core tools return structured JSON whenever `--json` is passed:

1. **`validate_manifest.py`**:
   - Validates `project-manifest.json` against `project-manifest.schema.json`.
   - Returns `{ "valid": bool, "manifest_path": str, "errors": list, "warnings": list, "clip_count": int, "credit_budget": int }`.

2. **`credit_guard.py`**:
   - Enforces zero-credit baseline and pre-flight balance checks.
   - Returns `{ "authorized": bool, "message": str, "details": { "tool": str, "action": str, "requested_cost_credits": int, "credit_budget": int, "available_balance": int|null, "free_alternative": str } }`.

3. **`render_free.py`**:
   - Constructs deterministic FFmpeg multi-track command combining stock video, normalized narration (-14 LUFS), and ducked music (-24 dB).
   - Generates playable 1080p/Shorts MP4 with cross-platform filter path escaping.

4. **`qa_media.py`**:
   - Probes media file with `ffprobe` and `ffmpeg` (blackdetect, ebur128).
   - Returns `{ "project_id": str, "media_path": str, "status": "TECHNICALLY_VALID_PENDING_REVIEW"|"FAILED_CRITICAL_CHECKS", "probed_metrics": dict, "automated_checks": dict, "mandatory_human_review_items": list, "verdict_summary": str }`.

5. **`transcript.py`**: Universal transcript parser (SRT, WebVTT, Whisper JSON).
6. **`hookscore.py`**: 5-property panel score (0-100) and weakest property fix.
7. **`title.py`**: Character counts, mobile/desktop issues, and vocabulary overlap.
8. **`deadair.py`**: Edit decision list (EDL) with cut reasons, timecodes, and total trimmed runtime.
9. **`chapters.py`**: Validated YouTube chapter list adhering to platform rules.
10. **`retention.py`**: Hook leak percentage, cliff drop moments, and middle slide attrition.
11. **`swipe.py`**: Outlier multiple leaderboard and hook formula classification.
