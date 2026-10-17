---
name: yt-sound-design
description: Studio-grade broadcast voice mastering and sidechain ducking engine using Spotify Pedalboard and FFmpeg for YouTube Agent Studio v3.0.
---

# yt-sound-design — Broadcast Voice Mastering & Sidechain Ducking

`yt-sound-design` delivers television broadcast-grade audio processing for Pakistani Urdu narration and atmospheric musical scoring. It uses Spotify's **Pedalboard DSP** library with seamless FFmpeg fallback.

Maintained by **ABDUL MUEED LASHARY** as part of YouTube Agent Studio v3.0.

---

## Mastering Pipeline Specifications

1. **Dialogue DSP Chain**:
   - **Highpass Filter**: 80.0 Hz cutoff removes microphone rumble, desk thumps, and AC proximity hum.
   - **Noise Gate**: -45.0 dB threshold (2.5:1 ratio, 1ms attack, 100ms release) eliminates room reflections and breath noise between sentences.
   - **Compressor**: -18.0 dB threshold (3:1 ratio, 10ms attack, 100ms release) evens out vocal dynamics for commanding, consistent delivery.
   - **Brickwall Peak Limiter**: -1.5 dBFS true peak ceiling prevents digital clipping across all mobile devices and DACs.

2. **Broadcast Loudness Normalization**:
   - Two-pass EBU R128 / ITU-R BS.1770-4 normalization.
   - Target: **-14.0 LUFS** integrated loudness, **-1.5 dBFS** true peak, **LRA 7.0**.

3. **Dynamic Sidechain Ducking**:
   - Background music is dynamically attenuated by **-24.0 dB** beneath spoken dialogue.
   - 250ms attack prevents audible popping; 750ms release gently restores musical presence during natural documentary pauses.

---

## Command Reference

```bash
# Check Pedalboard and FFmpeg audio readiness
python3 shared/scripts/pedalboard_master.py check

# Master a voice narration track (-14 LUFS, -1.5 dBFS ceiling)
python3 shared/scripts/pedalboard_master.py master \
  --voice assets/voice/raw_urdu_narration.wav \
  --out output/mastered_voice.wav

# Mix voice and background music with -24 dB sidechain ducking
python3 shared/scripts/pedalboard_master.py mix \
  --voice output/mastered_voice.wav \
  --music assets/audio/documentary_bed.mp3 \
  --out output/full_audio_mix.wav \
  --ducking-db -24.0
```
