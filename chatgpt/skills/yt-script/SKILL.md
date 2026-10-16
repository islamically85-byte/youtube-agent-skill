---
name: yt-script
description: >-
  Write professional YouTube video scripts from a raw idea across long-form, Shorts,
  documentaries, educational, storytelling, faceless, talking-head, and psychological-awareness formats.
  Generates scored hook candidates, visual cues, retention beats, and language-aware runtime estimates.
---

# yt-script — Video Scriptwriting Engine

One idea into a compelling, finished script designed for viewer retention and narrative payoff.

## Supported Production Formats
- **Long-form Video Essays & Documentaries** (Deep research, narrative arcs, multi-chapter pacing)
- **Shorts & Vertical Video** (0:15–0:60 rapid hook, constant visual movement, seamless loop points)
- **Educational & Psychological-Awareness** (Empathetic tone, responsible mental health framing, evidence-backed claims)
- **Talking-Head & Creator Commentary** (Spoken cadence, personal anecdotes, conversational transitions)
- **Faceless & Voiceover-Driven** (Explicit visual instructions, B-roll timing, kinetic text callouts)
- **Product Reviews & Sponsorship Integrations** (Authentic disclosures, feature-benefit demonstrations)

## Tools Available
This skill includes a deterministic 5-property hook panel (`hookscore.py`) based on 21 creator formulas:
```bash
python3 hookscore.py --hook "97% of creators quit before their 30th video"
python3 hookscore.py hooks.txt --json
```

> **CRITICAL EDITORIAL PRINCIPLE**: Hook scores are editorial heuristics, **NEVER** guaranteed predictors of algorithm distribution or virality. Use scores to eliminate weak, vague openings; never promise view counts.

## Step 1: Channel Profile & Voice Grounding
1. Check for `~/.claude/youtube/voice.md`, `channel-profile.yaml`, or creator-provided guidelines.
2. Ground vocabulary, target audience, cadence, and forbidden buzzwords before drafting.
3. If no voice profile exists, inquire about the audience persona, format preference, and target language.
4. **Never invent sources, data, or credentials.** If a factual claim, scientific study, or statistic would strengthen the script, ask the creator or clearly flag `[VERIFICATION NEEDED]`.

## Step 2: Hook Engineering (First 15 Seconds)
Write **FIVE distinct hook options** exploring different psychological entry angles:
- Candidate A (The Statistic / Concrete Metric)
- Candidate B (The Contrarian Claim / Curiosity Gap)
- Candidate C (Direct Mistake / Stake Confrontation)
- Candidate D (Visual Mystery / Story In Media Res)
- Candidate E (The Identity / Transformation Promise)

Score candidates with `hookscore.py`. Present the top two scoring candidates with their diagnostic breakdown (Specificity, Address, Stakes, Curiosity, BreVITY).

## Step 3: Script Architecture & Retention Beats
Deliver the chosen script formatted with dual columns / clear markers for production:

1. **The Hook (0:00–0:15)**: Confirms title promise, establishes the stakes, avoids self-introductions or subscribe pitches.
2. **The Turn (0:15–0:45)**: Explicit single-sentence road map of what the video delivers, opening the primary narrative loop.
3. **The Body (Segmented by Topic Beats)**:
   - Mark every beat with `[ON SCREEN: ...]` specifying B-roll, camera focal length (Wide/Tight), graphics, or text overlays.
   - Insert micro-resets every 45–60 seconds (shift in visual pace, sound cue, change of angle, counter-argument).
4. **The Payoff**: Explicitly deliver on the hook's central curiosity gap before asking for engagement.
5. **The Call-to-Action (CTA)**: Exactly ONE relevant next step (e.g., specific follow-up video, download, comment prompt).

## Step 4: Language-Aware Speech Duration
Calculate estimated duration using language-appropriate spoken word rates:
- **English**: ~150 words per minute (2.5 words/sec)
- **Urdu / Hindi**: ~130 words per minute (2.16 words/sec)
- **Spanish / Romance**: ~160 words per minute (2.67 words/sec)
- **Arabic**: ~125 words per minute (2.08 words/sec)

Report: Total word count, estimated runtime range, and pacing recommendations.

## What to Hand Back
1. The 5 candidate hooks with the top 2 scored hook panels.
2. Complete spoken script with timestamps, `[ON SCREEN]` visual cues, and audio cues.
3. Production runtime estimate.
4. Next actionable step: **Ship it, or change it?**
