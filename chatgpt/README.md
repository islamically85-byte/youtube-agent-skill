# YouTube Agent Studio — ChatGPT Edition

A specialized, conversational YouTube creator studio engineered for ChatGPT. Powered by **18 modular workflows** coordinated by the central **`yt-studio`** orchestrator.

---

## Architecture Overview

Unlike command-line or slash-command interfaces, the ChatGPT edition operates on **natural language intent recognition**. You describe what you want to achieve, and `yt-studio` selects, sequences, and executes the appropriate specialized skills while maintaining shared context across titles, scripts, storyboards, and metadata.

```
chatgpt/
  plugin.json                   # ChatGPT Plugin manifest (OpenAI v1 schema)
  .codex-plugin/plugin.json     # ChatGPT Codex environment manifest
  skills/
    yt-studio/                  # Master Orchestrator (Intent parser & skill sequencer)
    yt-script/                  # 21-formula scriptwriting & scored hooks
    yt-package/                 # Title + thumbnail click surface linter
    yt-edit/                    # EDL generation (dead air, filler, restarts)
    yt-comment/                 # 5-tier comment triage & authentic voice replies
    yt-plan/                    # Capacity-calibrated publishing calendars
    yt-viral/                   # Ethical niche outlier ranking (channel median multiples)
    yt-retention/               # Hook leak, cliff moment & pacing diagnostics
    yt-shorts/                  # 9:16 vertical clip extraction with rewritten hooks
    yt-seo/                     # Semantic search descriptions & platform tags
    yt-chapters/                # YouTube 4-rule platform chapter validation
    yt-audit/                   # 5-pillar channel diagnostic targeting #1 fix
    yt-storyboard/              # Shot-by-shot blocking & continuity sheets
    yt-produce/                 # Model-neutral & adapter-specific AI video prompts
    yt-localize/                # Multilingual translation (Native Pakistani Urdu)
    yt-factcheck/               # Factual claim verification & citation audits
    yt-upload-prep/             # Publication dossier & Studio pre-flight checklist
    yt-experiment/              # Controlled A/B hypothesis & Test & Compare scopes
  templates/
    channel-profile-template.yaml
    channel-profiles/pakistani-urdu-awareness.yaml
    voice.md
  references/
    hooks.json                  # 21 creator hook formulas
    urdu-localization-guide.md  # Authentic Pakistani Urdu guidelines
    fact-checking-rules.md      # Zero-hallucination verification rules
    packaging-guidelines.md     # Single click surface rules
    youtube-chapter-rules.md    # Platform chapter constraints
  scripts/                      # Standalone zero-dependency Python utilities
```

---

## Installation & Distribution Modes

### Distribution 1: Standalone ChatGPT Skill (ZIP)
For environments supporting uploadable Skills archives:
1. Locate the packaged release asset `release/youtube-agent-chatgpt-skill.zip`.
2. In ChatGPT, navigate to **Settings** -> **Personalization / Custom GPTs** -> **Upload Skill**.
3. Select `youtube-agent-chatgpt-skill.zip`.
4. ChatGPT will index `yt-studio`, all references, and Python helpers.

### Distribution 2: ChatGPT Plugin
For developers and organizations running local or registered developer plugins:
1. Ensure the manifest is served from your local or hosted domain (`/.well-known/ai-plugin.json` or through local developer mode).
2. Point ChatGPT to `chatgpt/plugin.json`.
3. The plugin declares authentication type `none` and runs offline-capable core utilities.

---

## Example Orchestration Prompt

You can prompt ChatGPT conversationally without memorizing slash commands:

> **"Create a complete YouTube production package about emotional abuse, in Pakistani Urdu, with four realistic 10-second video scenes, a thumbnail concept, video metadata and an upload checklist."**

### How `yt-studio` Processes This Request:
1. **Fact-Checking (`yt-factcheck`)**: Validates psychological consensus on emotional boundary violations and enforces clinical disclaimers.
2. **Packaging (`yt-package`)**: Formulates a punchy, non-overlapping title and thumbnail pairing (under 40 characters for mobile display).
3. **Pakistani Urdu Script (`yt-script` + `yt-localize`)**: Writes a 4-beat spoken narrative script in authentic Urdu script (`اردو`), avoiding Roman Urdu.
4. **Multi-Scene Prompts (`yt-produce` + `yt-storyboard`)**: Builds a character and setting continuity sheet and generates 4 modular 10-second realistic video prompts with explicit positive and negative constraints.
5. **Metadata & Pre-Flight (`yt-upload-prep` + `yt-chapters`)**: Assembles formatted description, validated chapters starting at `00:00`, timed `.srt` subtitle cues, and a pre-publish compliance checklist.

---

## Core Guarantees & Non-Negotiables
- **100% Free & Offline-First**: Requires no paid third-party API keys or YouTube account credentials for core operations.
- **Never Fabricates Metrics**: Does not invent subscriber growth, view counts, or CTR statistics.
- **Never Claims to Upload**: Generates complete, verified production dossiers for you to review and publish in YouTube Studio.
- **Preserves Attribution**: Open-source under the MIT License; upstream attribution preserved to Jake Schincariol. Maintained by ABDUL MUEED LASHARY.
