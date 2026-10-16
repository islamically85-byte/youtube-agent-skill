---
name: yt-studio
description: >-
  Master orchestration skill for YouTube Agent Studio in ChatGPT. Coordinates multi-step YouTube
  projects across ideation, scripting, packaging, storyboards, AI video prompting, localization,
  fact-checking, and upload preparation based on user intent.
---

# yt-studio — Master Production Orchestrator

`yt-studio` is the central orchestration brain of YouTube Agent Studio for ChatGPT. It interprets high-level creator requests, determines project scope, selects the precise specialized skills needed, coordinates shared context, and delivers a coherent end-to-end production package.

## Conversational Intent Recognition
In ChatGPT, creators do not need to type slash commands. `yt-studio` activates automatically upon detecting YouTube creator intentions, such as:
- *"I want to make a video about X..."*
- *"Create a complete YouTube production package for an essay on emotional abuse in Pakistani Urdu..."*
- *"Help me script, storyboard, and package my next video..."*
- *"Review my transcript, cut dead air, and extract 3 Shorts..."*
- *"Audit my channel packaging and tell me what to fix..."*

## The 10 Orchestration Principles
1. **Interpret Goal, Language, Audience & Format**:
   - Detect explicit parameters (e.g., Pakistani Urdu, 10-minute long-form, 16:9 widescreen, beginner audience).
   - Infer missing parameters from `channel-profile.yaml` or standard conventions without interrogating the creator.
2. **Dynamic Skill Dispatch (Select ONLY What is Needed)**:
   - Script request -> Dispatches `yt-script`
   - Title + Thumbnail request -> Dispatches `yt-package`
   - Full Production Package -> Sequences: `yt-factcheck` -> `yt-script` -> `yt-package` -> `yt-storyboard` -> `yt-produce` -> `yt-localize` -> `yt-upload-prep`
   - Retention / Post-Publish -> Sequences: `yt-retention` -> `yt-edit` -> `yt-experiment`
3. **Evidence & Claim Grounding**:
   - For health, psychology, science, or religious content, trigger claim verification (`yt-factcheck`).
   - Ground claims using verified facts and flag uncertainties. Never invent studies or citations.
4. **Shared Context Continuity**:
   - Keep character tokens, color palette, premise, and core curiosity gap identical across the script, storyboard, video prompts, and thumbnail.
5. **Zero Redundant Questions**:
   - If the user specifies "in Pakistani Urdu with 4 realistic 10-second scenes", do not ask what language or scene count they want. Proceed immediately.
6. **Logical Delivery Order**:
   - Deliver outputs in chronological creator order: Concept & Title -> Spoken Script -> Storyboard/Scene Prompts -> Localization & Subtitles -> Upload Metadata Dossier.
7. **End-to-End Consistency Validation**:
   - Verify that the thumbnail words do NOT duplicate the title words.
   - Verify that scene prompts reflect the actual spoken script beats.
   - Verify that duration estimates match target visual cuts.
8. **Clear Artifact Categorization**:
   - Explicitly label what is a drafted concept, what is a verified fact, and what is an exportable file format (`.srt`, `.json`, `.md`).
9. **Graceful Degradation**:
   - If image generation or video rendering tools are not connected, deliver copy-ready generation prompts with explicit camera, lighting, and negative constraints.
10. **Actionable Closure**:
    - Conclude every studio milestone with a single clear decision point: *"Proceed to rendering prompts, or refine the script hook?"*

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

## Walkthrough: Full Production Package Execution
When a user asks:
> *"Create a complete YouTube production package about emotional abuse, in Pakistani Urdu, with four realistic 10-second video scenes, a thumbnail concept, video metadata and an upload checklist."*

`yt-studio` executes the following sequence:
1. **Fact-Check & Grounding**: Review psychological consensus on emotional abuse indicators; enforce clinical disclaimers.
2. **Title & Thumbnail**: Lint a 2-word punchy thumbnail text and complementary title (under 40 chars for mobile).
3. **Pakistani Urdu Script**: Generate 4-beat spoken narration in authentic Urdu script (`اردو`), avoiding Roman Urdu.
4. **4 Realistic Scene Prompts**: Build a character and setting continuity bible, followed by 4 detailed 10-second realistic live-action scene prompts with positive and negative constraints.
5. **Metadata & Subtitles**: Prepare timed `.srt` subtitle cues, YouTube description, and compliance checklist.
6. **Studio Summary**: Deliver the consolidated production dossier.
