---
name: yt-package
description: >-
  Develop and lint YouTube title and thumbnail pairings as a unified click surface.
  Audits mobile/desktop truncation, word duplication, visual hierarchy, curiosity gaps,
  and delivers prompt-ready thumbnail generation briefs.
---

# yt-package — Title & Thumbnail Pairing Engine

The title and thumbnail are **one unified click surface**. Writing them in isolation wastes half your opportunity: the thumbnail repeats the title, creating redundancy rather than curiosity.

## Tools Available
Run the automated packaging linter in this directory:
```bash
python3 title.py --title "Why 97% of Creators Quit Before Video 30" --thumb "STOP QUITTING"
python3 title.py titles.txt --thumb "DON'T QUIT" --json
```

## Platform Rules Enforced
- **Desktop Search Truncation (~60 chars)**: Longer titles lose their conclusion in search results.
- **Mobile Feed Truncation (~40 chars)**: On smartphone feeds, titles cut early. The primary subject must survive in the first 40 characters.
- **Hard Limit (100 chars)**: YouTube's maximum allowed character limit.
- **No Vocabulary Duplication**: Thumbnail text must NOT repeat keywords already present in the title.
- **Thumbnail Word Economy (<= 3–4 words)**: At mobile feed scale, long text degrades into unreadable visual clutter.
- **Specifics Over Buzzwords**: Concrete metrics, dates, and named entities outperform generic hype adjectives ("insane", "shocking").

## Workflow Steps

### 1. Generate 5 Distinct Title/Thumbnail Strategic Pairings
Provide five complementary pairings targeting different audience motivations:
- **Pairing 1: The Curiosity Gap** (Title poses the paradox; Thumbnail reveals an unexpected visual clue)
- **Pairing 2: The Direct Warning** (Title states the consequence; Thumbnail highlights the trigger item)
- **Pairing 3: The Proof / Metric** (Title provides verified numbers; Thumbnail displays the before/after contrast)
- **Pairing 4: The Contrarian Stance** (Title challenges popular wisdom; Thumbnail shows immediate reaction)
- **Pairing 5: The Relatable Struggle** (Title identifies the exact pain point; Thumbnail dramatizes the emotional frustration)

### 2. Lint and Audit Each Pairing
Run each candidate through `title.py`. Report character length, mobile survival, shouting flags, and duplicate word detection.

### 3. Detailed Visual Brief for the Winning Concept
For the highest-scoring packaging concept, provide a complete production specification:
- **Focal Subject & Framing**: Camera distance (Extreme Close-Up / Medium), rule of thirds positioning, facial expression.
- **Background & Depth**: Low-distraction environment, depth-of-field separation, color grading contrast.
- **Color Palette & Lighting**: Complementary colors (e.g., warm foreground subject against cool dark background).
- **Text Placement & Typography**: High-contrast, sans-serif, positioned away from YouTube's lower-right duration badge.
- **Thumbnail Generation Prompt**: A structured text-to-image prompt (for Midjourney, DALL-E, or Stable Diffusion).

> **HONESTY CONSTRAINT**: Never claim a text prompt or markdown layout is a rendered image file. Only generate an image if an authorized image generation tool is actively connected and explicitly requested by the user.

## What to Hand Back
1. 5 complete title + thumbnail text pairings with audit scores.
2. The recommended top choice with rationale.
3. Production-ready visual thumbnail brief and copy-ready AI image prompt.
4. Final checkpoint: **Ship it, or change it?**
