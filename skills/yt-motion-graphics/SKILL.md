---
name: yt-motion-graphics
description: Design documentary-grade Urdu typography, RTL subtitles, lower thirds, and mobile-safe graphic overlays.
---

# yt-motion-graphics — Urdu Typography & Documentary Motion Graphics

`yt-motion-graphics` establishes design and typographic rules for subtitles, lower-thirds, chapter cards, and data overlays in Pakistani Urdu and bilingual documentaries.

## 1. Urdu Typographic Hierarchy

1. **Font Selection**:
   - **Documentary Narration & Subtitles**: Clean Naskh or optimized digital Nastaliq (`Noto Nastaliq Urdu`, `Jameel Noori Nastaleeq`).
   - For fast-reading subtitles, prefer legible digital Naskh/Nastaliq variants over overly complex cursive calligraphic styles that slow down reading.

2. **RTL Direction & Punctuation Integrity**:
   - All Urdu text must render Right-to-Left (RTL).
   - Use native Urdu punctuation:
     * Full stop: `۔` (Urdu khatma), never English period `.`
     * Question mark: `؟` (RTL question mark), never English `?`
     * Comma: `،` (RTL comma), never English `,`
   - In `.srt` files, ensure UTF-8 encoding without BOM to prevent glyph corruption.

3. **Color & Legibility**:
   - Text color: Pure white (`#FFFFFF`) with 2px dark outline (`#000000`) or 50% black translucent bounding box.
   - Size: Minimum 24pt for 1080p desktop; 32pt for vertical 9:16 mobile Shorts.

## 2. Mobile Safe Zones & Screen Geometry

```
+-------------------------------------------------------+
|  10% Top Margin (Avoid YouTube Title / Share icons)   |
|                                                       |
|                     SAFE ACTION AREA                  |
|                                                       |
|                                                       |
|                                                       |
|  [ Lower Third: ڈاکٹر احمد خان — ماہر نفسیات ]       |
|                                                       |
|  [ Subtitle: "یہ کیفیت انسان کے اعصاب کو متاثر کرتی ہے" ]|
|  10% Bottom Margin (Avoid Seek Bar & Time Display)    |
+-------------------------------------------------------+
```

- **Top Safe Margin**: Keep clear top 10% of screen (avoids YouTube channel overlay, card icons, and back button).
- **Bottom Safe Margin**: Keep clear bottom 15% on 16:9 (avoids scrubber bar and player controls), and bottom 25% on 9:16 Shorts (avoids creator handle, caption, and music title).
- **Right Safe Margin (Shorts)**: Keep clear right 20% on 9:16 Shorts (avoids like, dislike, comment, and share vertical action pills).

## 3. Subtitle Generation Pattern (SRT)

```srt
1
00:00:00,000 --> 00:00:02,500
کیا آپ نے کبھی اس اندرونی خاموشی پر غور کیا ہے؟

2
00:00:02,800 --> 00:00:05,200
یہ خاموشی اکثر کسی بڑے طوفان کا پیش خیمہ ہوتی ہے۔
```

## 4. Minimalist Lower-Thirds Contract
- **Duration**: Display for 3.5 to 5.0 seconds upon speaker introduction.
- **Animation**: 0.3s gentle opacity fade-in, stationary hold, 0.3s gentle fade-out.
- **Content**: Name + verifiable credential (e.g., `ڈاکٹر عاصم رؤف — ماہر امراض قلب`).
