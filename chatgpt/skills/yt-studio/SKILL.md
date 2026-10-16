---
name: yt-studio
description: >-
  Master orchestration skill for YouTube Agent Studio in ChatGPT. Coordinates multi-step YouTube
  projects across ideation, scripting, packaging, storyboards, Pakistani Urdu voiceover, stock
  footage documentary curation, multi-track FFmpeg rendering, and automated media QA.
---

# yt-studio — Master Production Orchestrator

`yt-studio` is the central orchestration brain of YouTube Agent Studio for ChatGPT. It interprets high-level creator requests, determines project scope, selects the precise specialized skills needed, coordinates shared context, and delivers a coherent end-to-end production package.

## Conversational Intent Recognition
In ChatGPT, creators do not need to type slash commands. `yt-studio` activates automatically upon detecting YouTube creator intentions, such as:
- *"I want to make a documentary video about X..."*
- *"Create a complete YouTube production package for an essay on emotional abuse in Pakistani Urdu..."*
- *"Help me script, curate stock footage, and package my next video..."*
- *"Review my transcript, cut dead air, and extract 3 Shorts..."*
- *"Audit my channel packaging and tell me what to fix..."*
- *"Render a zero-credit stock footage documentary with Urdu subtitles..."*

## The 10 Orchestration Principles
1. **Interpret Goal, Language, Audience & Format**:
   - Detect explicit parameters (e.g., Pakistani Urdu, 10-minute long-form, 16:9 widescreen, beginner audience).
   - Infer missing parameters from `channel-profile.yaml` or standard conventions without interrogating the creator.
2. **Dynamic Skill Dispatch (Select ONLY What is Needed)**:
   - Script request -> Dispatches `yt-script`
   - Title + Thumbnail request -> Dispatches `yt-package`
   - Pakistani Urdu Voiceover -> Dispatches `yt-voice-urdu`
   - Stock Video Curation -> Dispatches `yt-stock-producer`
   - Video Assembly & Rendering -> Dispatches `yt-video-editor`
   - Subtitle & Motion Graphics -> Dispatches `yt-motion-graphics`
   - Technical Media QA -> Dispatches `yt-production-qa`
   - Budget & Paid API Protection -> Dispatches `yt-credit-guard`
   - Full Production Package -> Sequences: `yt-factcheck` -> `yt-script` -> `yt-voice-urdu` -> `yt-stock-producer` -> `yt-video-editor` -> `yt-motion-graphics` -> `yt-production-qa` -> `yt-package` -> `yt-upload-prep`
3. **Evidence & Claim Grounding**:
   - For health, psychology, science, or religious content, trigger claim verification (`yt-factcheck`).
   - Ground claims using verified facts and flag uncertainties. Never invent studies or citations.
4. **Free-First & Zero-Credit Baseline**:
   - Production operations default to a **0-credit budget**.
   - No paid third-party tools (vidIQ, ElevenLabs, OpenAI DALL-E) are invoked without explicit creator authorization.
5. **Authentic Pakistani Urdu Voiceover**:
   - Native Urdu script (`اردو`), avoiding Roman Urdu.
   - Speech cadence targets ~130 words per minute for natural documentary weight.
   - Prioritizes well-recorded human voice over unverified neural TTS.
6. **Real Footage Over Synthetic Slides**:
   - Source authentic, high-definition stock footage from permissive repositories (Pexels, Pixabay, Mixkit, CC0).
   - Reject robotic slide shows, AI 3D morphing, or low-effort image pans.
7. **Multi-Track Audio Standards**:
   - Spoken narration normalized to **-14.0 LUFS** via FFmpeg `loudnorm`.
   - Atmospheric background music ducked to **-24.0 dB** beneath speech.
8. **Defensive Manifest & Provenance Tracking**:
   - Every asset is registered in `project-manifest.json` with source URL, license class, and verification date.
   - Run `validate_manifest.py` before touching the render pipeline.
9. **Rigorous Quality Gate (`TECHNICALLY_VALID_PENDING_REVIEW`)**:
   - Rendered media is probed via `qa_media.py` for duration, black frames, resolution, and audio loudness.
   - Automated tools report technical compliance but **never** bypass human editorial sign-off.
10. **Actionable Closure**:
    - Conclude every studio milestone with a single clear decision point: *"Proceed to rendering, or refine the script hook?"*

## Specialized Skill Directory (Dispatched as Needed)
- `yt-script`: Long-form, Shorts, voiceover, and narrative scripts with 21 hook formulas.
- `yt-package`: Title and thumbnail pairing linter with mobile truncation checks.
- `yt-edit`: Edit decision lists (EDL) detecting dead air, filler, and retakes.
- `yt-comment`: Triage comments into 5 piles and draft authentic voice replies.
- `yt-plan`: Capacity-calibrated weekly/monthly publishing calendars.
- `yt-viral`: Ethical competitor intelligence scored by channel median multiples.
- `yt-retention`: Diagnosis of hook leaks, cliff moments, and pacing slides.
- `yt-shorts`: Standalone 9:16 vertical clip extraction with rewritten hooks.
- `yt-seo`: Search intent descriptions, validated chapters, and secondary tags.
- `yt-chapters`: Enforce YouTube's 4 platform timestamp rules.
- `yt-audit`: Channel health diagnostic delivering exactly ONE highest-impact fix.
- `yt-storyboard`: Scene-by-scene blocking, shot types, camera moves, and audio cues.
- `yt-produce`: Model-neutral and capability-aware AI video prompt sequences.
- `yt-localize`: Authentic multilingual adaptation (including native Pakistani Urdu script).
- `yt-factcheck`: Claim extraction, source verification, and script corrections.
- `yt-upload-prep`: Complete pre-flight publication dossier with compliance checks.
- `yt-experiment`: Controlled A/B hypotheses and YouTube Test & Compare scopes.
- `yt-stock-producer`: Permissive stock video discovery, curation, and manifest registration.
- `yt-voice-urdu`: Fluent Pakistani Urdu voiceover guidance, timing, and audio mastering.
- `yt-video-editor`: Documentary pacing, multi-track FFmpeg timeline assembly, and audio ducking.
- `yt-motion-graphics`: Urdu typography, RTL subtitles, lower-thirds, and mobile safe zones.
- `yt-production-qa`: Automated probing via `qa_media.py` and human sign-off checklist.
- `yt-credit-guard`: Zero-credit budget enforcement and third-party quota protection.
