---
name: yt-localize
description: >-
  Professional multilingual YouTube localization and translation for subtitles, voiceover narration,
  on-screen graphics, and metadata, featuring native Pakistani Urdu script handling and cultural adaptation.
---

# yt-localize — Multilingual YouTube Localization & Adaptation

Expand your YouTube audience through authentic, culturally resonant localization. Translation is not mere word substitution; it requires adapting idioms, preserving conversational cadence, re-timing voiceover durations, and respecting linguistic nuances.

## Pakistani Urdu Localization Standard
When localizing into Urdu for Pakistani audiences:
1. **Urdu Script (اُردو رسم الخط) by Default**:
   - Write standard Pakistani Urdu in authentic Arabic/Perso-Arabic script (Nastaliq/Naskh Unicode).
   - **DO NOT** use Roman Urdu (Urdu written in English letters) unless explicitly requested by the creator.
2. **Culturally Authentic Vocabulary (پاکستانی بول چال)**:
   - Avoid mechanical, robotic machine-translations that sound like formal legal treaties.
   - Avoid Hindi-dominant Sanskrit loanwords (e.g., use `کوشش` instead of `پریاس`, `شکریہ` instead of `دھنیہ واد`, `مسئلہ` instead of `سمسیا`).
   - Retain naturally assimilated technical terms in conversational Urdu (e.g. `یوٹیوب چینل`, `ویڈیو`, `ایڈیٹنگ`, `ایلگورتھم`) rather than inventing archaic translations.
3. **Right-to-Left (RTL) Layout Considerations**:
   - Ensure on-screen graphics, lower-thirds, and text overlays account for RTL orientation and do not truncate against UI borders.
4. **Spoken Cadence & Duration Adjustment**:
   - Spoken Urdu typically flows at **~130 words per minute**, whereas conversational English averages **~150 words per minute**.
   - Expand or condense phrases so translated voiceover fits within the existing video visual cut timing.

## Multi-Layered Localization Deliverables
Localization must provide four coordinated outputs:

### 1. Spoken Voiceover Narration Script
- Formatted beat-by-beat with estimated spoken timestamps.
- Pronunciation cues for technical or foreign names.

### 2. Timecoded Subtitle Track (.SRT / .VTT Format)
- Subtitles segmented into digestible reading chunks (max 35–42 characters per line, max 2 lines per subtitle cue).
- Timed to match spoken cadence.

### 3. On-Screen Graphics & Lower-Thirds Translations
- Translated titles for diagrams, bullet points, and key takeaway banners.

### 4. Translated Packaging & SEO Metadata
- Culturally resonant YouTube title (under 60 characters).
- Localized description with relevant native search queries.
- Translated chapter titles for the description.

## Sample Urdu Localization Block
```markdown
### Hook Narration [0:00–0:05]
- **Original English**: "97% of creators quit before their 30th video."
- **Urdu Translation (اردو)**: "ستانوے فیصد یوٹیوبرز اپنی تیسویں ویڈیو بنانے سے پہلے ہی ہمت ہار جاتے ہیں۔"
- **On-Screen Text**: ۹۷٪ کری ایٹرز چھوڑ جاتے ہیں
- **Timing Check**: 12 words at 130 WPM ≈ 5.5s (Fits within 5-6s opening visual cut).

### The Turn [0:05–0:12]
- **Original English**: "Here is what the other 3% do differently every single week."
- **Urdu Translation (اردو)**: "آج ہم بات کریں گے کہ باقی تین فیصد لوگ ہر ہفتے ایسا کیا مختلف کرتے ہیں جو انہیں کامیاب بناتا ہے۔"
```

## Preservation of Caveats & Health Claims
> **INTEGRITY RULE**: When localizing psychological, medical, religious, or financial content, never alter caveats, qualifications, or legal disclaimers. Factual accuracy must remain identical across all languages.

## What to Hand Back
1. Complete localized spoken narration script in target language and native script.
2. Formatted subtitle cues ready for `.srt` export.
3. Localized YouTube title, description, and chapter timestamps.
4. Spoken duration timing comparison table (Original vs. Localized).
5. Next step: **Confirm translation tone or prepare `.srt` file?**
