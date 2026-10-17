# YouTube Agent Studio — ChatGPT Edition v3.0

A specialized, conversational YouTube creator studio engineered for ChatGPT. Powered by **34 modular workflows** coordinated by the central **`yt-studio`** orchestrator with **Motion-First Hybrid Production**.

Maintainer: **ABDUL MUEED LASHARY** | Upstream: **Jake Schincariol** (MIT License)

---

## Architecture Overview

Unlike command-line or slash-command interfaces, the ChatGPT edition operates on **natural language intent recognition**. You describe what you want to achieve, and `yt-studio` selects, sequences, and executes the appropriate specialized skills while maintaining shared context across titles, scripts, storyboards, motion graphics, and audio mixdown.

```
chatgpt/
  plugin.json                   # ChatGPT Plugin manifest (OpenAI v1 schema)
  .codex-plugin/plugin.json     # ChatGPT Codex environment manifest
  skills/                       # 34 specialized production workflows
    yt-studio/                  # Master Orchestrator (Intent parser, 3 Creator Options)
    yt-browser-motion/          # Headless browser HTML/Canvas/SVG motion graphics
    yt-blender-3d/              # Headless Blender LTS 3D land parcel visualization
    yt-sound-design/            # Spotify Pedalboard voice mastering & -24 dB ducking
    yt-timeline-otio/           # OpenTimelineIO multi-track NLE interchange (.otio, .edl)
    yt-hybrid-production/       # Hybrid provider router & credit budget guard
    yt-voice/                   # Pakistani Urdu voice benchmark & normalization
    yt-assets/                  # Semantic stock director (70-95 cuts per timeline)
    yt-audio/                   # Broadcast loudness & YouTube chapter validation
    yt-render/                  # Multi-track FFmpeg renderer with ASS subtitles
    yt-render-qc/               # Strict duration bounds & technical QA prober
    ...                         # 23 additional creator & editorial skills
  templates/
    motion/discrepancy_counter.html  # Editable 15s evidence comparison motion template
    channel-profiles/                # Regional & cultural awareness profiles
  references/
    hooks.json                  # 21 creator hook formulas
    urdu-localization-guide.md  # Authentic Pakistani Urdu guidelines
    fact-checking-rules.md      # Zero-hallucination verification rules
    packaging-guidelines.md     # Single click surface rules
  scripts/                      # 20 standalone zero-dependency Python utilities
```

---

## The Three Creator Options in ChatGPT

When requesting video, motion, or audio generation in conversation, `yt-studio` prompts the creator to choose:
- **[A] FREE STUDIO**: 100% offline local engine (Browser Motion + Blender 3D + FFmpeg + Piper Urdu; $0 cost).
- **[B] HYBRID VALUE**: Free local visuals + optional low-cost Gemini Urdu Voiceover (pennies per documentary).
- **[C] vidIQ / PREMIUM**: Commercial provider with explicit credit authorization and automatic fallback.

---

## Installation & Distribution Modes

### Distribution 1: Standalone ChatGPT Skill (ZIP)
1. Locate the release package `release/youtube-agent-chatgpt-skill.zip`.
2. In ChatGPT, navigate to **Settings** -> **Personalization / Custom GPTs** -> **Upload Skill**.
3. Select `youtube-agent-chatgpt-skill.zip`.
4. ChatGPT indexes `yt-studio`, all 34 workflows, and Python helpers.

### Distribution 2: ChatGPT Plugin
1. Register `chatgpt/plugin.json` or `.codex-plugin/plugin.json` in ChatGPT developer mode.
2. Full API schemas in `chatgpt/schemas/` connect endpoints directly to ChatGPT actions.
