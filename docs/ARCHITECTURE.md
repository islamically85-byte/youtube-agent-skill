# Target Repository Architecture

YouTube Agent Studio is structured to maintain clean separation between platform-specific manifests, self-contained skills, and shared testing infrastructure.

---

## Directory Layout

```
youtube-agent-skill/
├── .claude-plugin/              # Claude Code Plugin metadata
│   ├── plugin.json              # Version 2.0.0 Claude manifest
│   └── marketplace.json         # Marketplace distribution schema
│
├── skills/                      # 17 Upgraded Claude Skills (Self-Contained)
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
│   ├── skills/
│   │   ├── yt-studio/           # Master Orchestrator for ChatGPT
│   │   └── yt-*/                # 17 specialized workflows
│   ├── templates/               # Portable channel profiles
│   ├── references/              # Guides (Urdu, Factcheck, Chapters, Packaging)
│   ├── scripts/                 # Standalone Python tools for Code Interpreter
│   └── README.md                # Dedicated ChatGPT documentation
│
├── shared/                      # Core Shared Assets & Schemas
│   ├── scripts/                 # Canonical Python standard library tools
│   ├── schemas/                 # JSON Schemas (profiles, storyboards, upload)
│   └── fixtures/                # Real-world test fixtures (SRT, VTT, JSON, CSV)
│
├── templates/                   # Channel profiles and voice configurations
│   ├── voice.md                 # Spoken voice and forbidden words
│   ├── channel-profile-template.yaml
│   └── channel-profiles/
│       └── pakistani-urdu-awareness.yaml
│
├── docs/                        # Complete Engineering Documentation
│   ├── AUDIT-REPORT.md          # Baseline audit findings and remediation
│   ├── INSTALL-CLAUDE.md        # Claude installation guide
│   ├── INSTALL-CHATGPT.md       # ChatGPT installation guide
│   ├── COMPATIBILITY.md         # Claude vs. ChatGPT comparison matrix
│   ├── ARCHITECTURE.md          # Architecture & data contract specs
│   ├── SECURITY.md              # Security, privacy, and integrity model
│   └── CONTRIBUTING.md          # Open-source contribution guidelines
│
├── tests/                       # Automated Test Suite (100% Passing)
│   ├── test_transcript.py       # Universal transcript loader tests
│   ├── test_hookscore.py        # 5-property panel tests
│   ├── test_title.py            # Packaging linter tests
│   ├── test_deadair.py          # EDL generator tests
│   ├── test_chapters.py         # YouTube chapter constraint tests
│   ├── test_retention.py        # CSV retention analysis tests
│   ├── test_swipe.py            # Outlier multiple tests
│   ├── test_skills_structure.py # Skill frontmatter validator
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
1. `transcript.py` -> Returns parsed cues with seconds and formatted timestamps.
2. `hookscore.py` -> Returns 5 property scores, weakest property, and specific fix recommendation.
3. `title.py` -> Returns character count, mobile/desktop issues, and vocabulary overlap.
4. `deadair.py` -> Returns edit decision list (EDL) with cut reasons, timecodes, and total trimmed runtime.
5. `chapters.py` -> Returns validated YouTube chapter list with compliance check.
6. `retention.py` -> Returns hook leak percentage, cliff drop moments, and middle slide attrition.
7. `swipe.py` -> Returns outlier multiple leaderboard and hook formula classification.
