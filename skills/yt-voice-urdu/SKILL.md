---
name: yt-voice-urdu
description: Write, pace, and master authentic Pakistani Urdu narration in native Urdu script, optimized for 130 WPM documentary pacing and -14 LUFS loudness.
---

# yt-voice-urdu — Pakistani Urdu Narration & Audio Mastering

`yt-voice-urdu` guides the creation, phrasing, speech timing, and audio mastering of authentic Pakistani Urdu voiceover for high-retention YouTube documentaries and essays.

## 1. Linguistic & Script Rules

1. **Native Urdu Script (`اردو`)**:
   - Write all spoken narration in native Nastaliq/Naskh Perso-Arabic script.
   - **Never use Roman Urdu** (`Aap kaisay hain`) unless explicitly requested by the user. Roman Urdu degrades editorial authority and prevents proper subtitle rendering.

2. **Natural Pakistani Spoken Register**:
   - Use standard Pakistani conversational documentary Urdu (as spoken on serious news magazines and quality documentaries).
   - Balance clarity and dignity: avoid archaic Persianized vocabulary that alienates youth, and avoid overly casual street slang.
   - Example:
     * ❌ *Too archaic*: "یہ سانحہ قلوب و اذہان پر گراں بار نقوش ثبت کر گیا"
     * ❌ *Too slangy*: "سین یہ ہے کہ بندہ بالکل ڈپریس ہو کے بیٹھ جاتا ہے"
     * ✅ *Ideal Pakistani Urdu*: "یہ کیفیت انسان کے اندر خاموشی سے جنم لیتی ہے اور رفتہ رفتہ اس کے اعصاب کو کھوکھلا کر دیتی ہے"

3. **Pacing & Cadence (The 130 WPM Rule)**:
   - Target **120 to 140 words per minute** (approx. 2 to 2.3 words per second).
   - Urdu compound verbs and honorifics require breathing room. Rushing narration above 160 WPM destroys emotional resonance.
   - Insert explicit pause markers `[...]` or paragraph breaks to indicate 0.5s–1.0s reflective pauses between scenes.

## 2. Voiceover Provenance & Monetization Safety

| Voice Source | Commercial Clearance | Quality Assessment | Recommendation |
| :--- | :--- | :--- | :--- |
| **Human Voiceover** (Creator / Voice Actor) | **100% Cleared** | Gold standard; natural inflection, breath, and emotion | **Primary recommendation** for monetized YouTube channels |
| **ElevenLabs** | Commercial tier cleared | High quality, but requires paid credits (blocks under 0-credit budget) | Requires explicit user consent |
| **Meta MMS Urdu** | **CC-BY-NC (Non-Commercial)** | Unsuitable for monetized channels; robotic | **Do not use** for commercial YouTube content |
| **Piper / Coqui TTS** | Open source / varies | Unstable Urdu phoneme mapping; pronunciation errors | Requires manual audition before use |

## 3. Audio Mastering Specifications

- **Integrated Loudness**: **-14.0 LUFS** (YouTube playback standard).
- **True Peak**: Maximum **-1.5 dBFS** (prevents inter-sample clipping during AAC transcoding).
- **Sample Rate**: **48,000 Hz** (or 44,100 Hz), 16-bit or 24-bit PCM WAV.
- **FFmpeg Mastering Filter**:
  ```bash
  ffmpeg -i raw_voiceover.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 narration_norm.wav
  ```

## 4. Script Delivery Template

```markdown
### سین ۱: تعارف اور تجسس (0:00 - 0:15)
[نرم، سنجیدہ لب و لہجہ — رفتار ۱۲۵ الفاظ فی منٹ]
کیا آپ نے کبھی غور کیا کہ جب انسان مسلسل دباؤ میں رہتا ہے تو اس کے اندر کی آواز کیسے بدل جاتی ہے؟ [...] 
ہم اکثر خاموشی کو سکون سمجھ لیتے ہیں، مگر بعض اوقات یہ خاموشی کسی بڑے طوفان کا پیش خیمہ ہوتی ہے۔

*تکنیکی تفصیلات:*
- دورانیہ: ۱۵ سیکنڈ
- الفاظ کی تعداد: ۳۲ الفاظ
- بصری کٹ تجویز: مدہم روشنی، کھڑکی سے باہر بارش کا منظر
```
