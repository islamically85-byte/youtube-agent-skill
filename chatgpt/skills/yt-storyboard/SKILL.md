---
name: yt-storyboard
description: >-
  Convert video scripts into comprehensive production storyboards with scene durations,
  camera angles, subject blocking, lighting setups, continuity sheets, and audio design.
---

# yt-storyboard — Video Production Storyboarding & Shot Design

Transform a written script into an actionable, visual production storyboard. Designed for creators, directors, animators, and generative AI video workflows who need shot-by-shot continuity and visual clarity before recording or rendering.

## Supported Aspect Ratios
- **16:9 Standard Widescreen**: Traditional long-form YouTube essays, tutorials, and documentaries.
- **9:16 Vertical Framing**: YouTube Shorts, Instagram Reels, and TikTok vertical productions.

## Storyboard Specification Elements
Each scene block must detail:
1. **Scene Number & Target Duration** (e.g., `Scene 01 [0:00–0:05] (5.0s)`).
2. **Shot Type & Camera Framing**:
   - Shot size: Extreme Wide Shot (EWS), Wide Shot (WS), Medium Shot (MS), Medium Close-Up (MCU), Close-Up (CU), Extreme Close-Up (ECU).
   - Camera movement: Static, Slow Push-In, Pan, Tilt, Dolly tracking, Orbit, Handheld natural jitter.
3. **Subject Blocking & Action**: Precise character movement, posture, facial expression, and interaction with props.
4. **Environment & Setting**: Location architecture, background clutter, depth of field (shallow/deep).
5. **Lighting & Color Palette**: Lighting key (high-key soft, dramatic low-key, golden hour rim light), dominant color tones.
6. **Audio Design**: Spoken dialogue/voiceover lines, background ambience, sound effects (SFX), and music pacing.
7. **Transitions**: Hard cut, J-cut, L-cut, whip pan, match cut, or dip to black.
8. **Continuity Markers**: Wardrobe, prop state, character facial features, and hair positioning to maintain visual coherence across scenes.

## The Continuity & Character Bible
Before generating multi-scene storyboards with recurring characters or environments:
- **Character Consistency Tokens**: Name, gender, age, ethnicity, specific clothing (colors, fabric, accessories), distinct features.
- **Environment Sheet**: Room dimensions, window light direction, signature wall art, furniture placement.

## Sample Storyboard Format
```markdown
### Scene 01 | The Hook [0:00–0:04] (4.0s)
- **Aspect Ratio**: 16:9
- **Shot Type**: Medium Close-Up (MCU), 50mm lens perspective, shallow depth of field
- **Camera Movement**: Slow, continuous push-in towards the subject
- **Subject Action**: Subject sitting at a minimalist wooden desk, staring intently into camera, leaning forward at 0:02
- **Lighting**: Soft diffused key light from left (45 deg), subtle blue edge/rim light from behind
- **Voiceover / Spoken**: "97% of creators quit before video 30."
- **Audio / SFX**: Ambient low drone, subtle sub-bass hit on "97%"
- **Transition**: Fast whip-pan to Scene 02
- **Continuity Check**: Subject wearing navy crewneck sweater, dark background
```

## What to Hand Back
1. Complete Scene-by-Scene Storyboard table or detailed shot cards.
2. Character and Environment Continuity Sheet.
3. B-Roll and Asset Checklist (props, overlays, sound effects).
4. Shot list ordered by setup location to optimize filming efficiency.
5. Next step: **Confirm shot list or proceed to `/yt-produce`?**
