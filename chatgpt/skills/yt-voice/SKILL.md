---
name: yt-voice
description: Voiceover quality selector and Pakistani Urdu pronunciation engine. Benchmarks audio cadence, normalizes numerals and acronyms, and enforces human listening review.
---

# yt-voice — Pakistani Urdu Narration & Audio Cadence Engine v3.0

`yt-voice` handles voiceover synthesis, script phonetic normalization, and timing alignment for YouTube documentaries. It enforces strict Pakistani Urdu pronunciation rules for numerals, regulatory acronyms, and geographic names, benchmarking audio tracks against an empirical 20–40s standard passage.

## Core Capabilities

1. **Pronunciation & Normalization**:
   - Numerals are converted to native Urdu phonetic words (e.g. `42,000` -> `بیالیس ہزار`, `6,000` -> `چھ ہزار`, `36,000` -> `چھتیس ہزار`, `16` -> `سولہ`, `7` -> `سات`).
   - Regulatory and administrative acronyms are expanded into Urdu phonetic equivalents (e.g. `CDA` -> `سی ڈی اے`, `NOC` -> `این او سی`, `SECP` -> `ایس ای سی پی`, `NAB` -> `نیب`).
2. **Breath-Level Chunking**:
   - Sentences are divided at native punctuation (`۔`, `؟`, `!`, `،`) to prevent unnatural rushes and robotic delivery.
3. **Pacing Benchmark**:
   - Enforces ~130 words per minute cadence suitable for serious investigative journalism.
4. **Mandatory Human Listening Review**:
   - Automated scripts never certify pronunciation quality in isolation; human sign-off is flagged for retroflex consonants (`ٹ`, `ڈ`, `ڑ`) and tone.

## CLI Usage

Run the 20–40s benchmark test passage:

```bash
python3 scripts/urdu_voice_engine.py --test-passage
```

Analyze a full documentary screenplay:

```bash
python3 scripts/urdu_voice_engine.py --script templates/documentaries/pakistan_property_screenplay.txt --normalize
```

Export structured timing metrics:

```bash
python3 scripts/urdu_voice_engine.py --script templates/documentaries/pakistan_property_screenplay.txt --normalize --json
```

## Mandatory Human Review Checkpoints

- [ ] Confirm retroflex consonant clarity (`ٹ`, `ڈ`, `ڑ`) in words like `پلاٹ` and `کوآپریٹو`.
- [ ] Verify deliberate, unhurried cadence on investigative numbers: `42,000` and `6,000`.
- [ ] Listen for natural breath pauses between clauses to preserve documentary weight.
