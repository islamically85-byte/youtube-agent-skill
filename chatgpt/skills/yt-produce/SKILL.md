---
name: yt-produce
description: >-
  Coordinate cinematic and AI-assisted video production with capability-aware prompting,
  character consistency sheets, scene-to-scene visual continuity, and negative constraints.
---

# yt-produce — Video Production & Multi-Scene Prompt Coordination

Coordinate the physical filming or AI-assisted video generation of multi-scene YouTube productions. Translates scripts and storyboards into **model-neutral or adapter-specific prompt sequences** designed for visual coherence, character consistency, and cinematic pacing.

## Honesty & Tool Integrity Constraints
> **MANDATORY PRODUCTION DISTINCTION**:
> 1. **Never Confuse Static Art with Rendered Video**: A markdown table, image prompt, or storyboard illustration is **NOT** a rendered 3D animated or live-action video file.
> 2. **Render Only with Real Connected Tools**: Only trigger rendering if an authorized video/image generation tool or local script is genuinely connected. Otherwise, deliver copy-ready, production-calibrated prompt packages.
> 3. **Model Capabilities Awareness**: AI video models (Runway Gen-3, Luma Dream Machine, Kling, Sora, Pika, etc.) typically operate in 5–10 second clip intervals. Break longer scripts into modular, independently renderable scene prompts.

## Visual Styles Supported
- **Realistic Cinematic Live-Action** (Natural skin texture, realistic camera optics, 35mm/50mm focal depth, natural lighting)
- **Cinematic 3D Animation & Stylized CGI** (Stylized keyframes, Pixar/DreamWorks aesthetic, global illumination)
- **Animated Technical Explainers** (Clean isometric vector visuals, kinetic typography, screen simulations)
- **Product Advertisements & Commercials** (Macro studio lighting, product turntable, dynamic depth-of-field)
- **Documentary B-Roll & Historical Reconstruction** (Archival grade, vintage film grain, authentic period wardrobe)

## Multi-Scene Continuity Architecture
To maintain character, setting, and prop consistency across short generated clips:

### 1. The Persistent Character & Environment Bible
Define shared anchor tokens reused in every prompt:
- `[CHARACTER]`: "A 28-year-old South Asian man with short black hair, neat stubble, wearing a plain charcoal-gray crewneck cotton t-shirt."
- `[SETTING]`: "Modern minimalist home office studio in Lahore, warm walnut wooden desk, soft warm LED desk lamp, blurred bookshelf in deep background."
- `[LIGHTING & OPTICS]`: "Cinematic lighting, 50mm f/1.8 lens, 4K UHD, photorealistic color grading."

### 2. Segmenting into 10-Second Generation Blocks
For each scene, structure two distinct prompt blocks:
- **Positive Prompt**: Action verbs, camera trajectory, subject emotion, lighting, and environmental physics.
- **Negative Prompt / Negative Constraints**: Artifact elimination (e.g. `blurry, deformed hands, extra limbs, warped face, unrealistic motion, morphing objects, text watermarks, plastic skin, jitter`).

## Sample Scene Generation Block
```markdown
### Scene 02 | The Revelation [0:10–0:20] (10.0s)
- **Target Style**: Realistic Live-Action / Cinematic Documentary
- **Aspect Ratio**: 16:9
- **Camera Movement**: Subtle crane movement lowering from high angle to eye level
- **Subject**: [CHARACTER] looking up from his laptop screen with a sudden realization, eyes widening subtly
- **Environment**: [SETTING], rain pattering softly against window glass in the background
- **Positive Prompt**:
  "Cinematic medium shot of [CHARACTER] sitting at walnut desk, looking up from laptop with an expression of sudden clarity. Soft daylight from window mixed with warm lamp key light, 50mm lens, shallow depth of field, natural skin texture, realistic cloth folds, subtle head movement, high fidelity, 4k resolution --ar 16:9"
- **Negative Constraints**:
  "deformed anatomy, morphing fingers, duplicate faces, cartoon shader, exaggerated eye movement, oversaturated colors, jittery frame interpolation"
- **Audio & Dialogue**:
  - Dialogue: "That was the exact moment I realized the algorithm wasn't punishing me. I was punishing myself."
  - Audio: Ambient room tone, soft rain against window, keyboard keystrokes
```

## Quality Review & Post-Generation Checklist
- **Temporal Consistency**: Does the character's clothing and hairstyle remain identical to Scene 01?
- **Lip-Sync & Audio Alignment**: Is the spoken line duration shorter than the clip's physical duration?
- **Motion Naturalness**: Are camera zooms smooth without object warping or physics breaking?

## What to Hand Back
1. Character and Environment Continuity Anchor Sheet.
2. Complete sequence of modular scene generation prompts with explicit positive and negative constraints.
3. Audio/dialogue sync schedule for video editing.
4. Production readiness sign-off: **Ready to render or adjust scene pacing?**
