---
name: yt-render-qc
description: Strict technical quality assurance prober. Enforces 360-420s duration bounds, probes EBU R128 loudness, detects black frames, verifies licensing, and flags human gate sign-off.
---

# yt-render-qc — Strict Technical Quality Assurance Prober v3.0

`yt-render-qc` performs deterministic technical quality control on rendered documentary video files. It replaces permissive warnings with strict verification gates, enforcing duration constraints (e.g. rejecting outputs below 360 seconds for a 6–7 minute documentary), black frame detection, EBU R128 loudness compliance, and license integrity.

## Strict QC Gates

| Check | Passing Standard | Failure Action |
|---|---|---|
| **Duration Bounds** | 360.0s – 420.0s (for 6–7 min documentary) | Rejects render with `FAILED_CRITICAL_CHECKS` |
| **Black Frames** | 0 black frames exceeding 0.5s duration | Fails QA, reports exact drop intervals |
| **Audio Loudness** | Integrated -14.0 LUFS (±6 LUFS tolerance), Peak ≤ -1.5 dBFS | Fails QA, requires remixing |
| **Background Music** | Music track present without `MISSING_MUSIC_WARNING` | Warns or fails when `--require-music` enabled |
| **Asset Licensing** | 100% of clips have verified permissive licenses | Fails QA, flags unverified assets |
| **Review Status** | Automated checks pass: `TECHNICALLY_VALID_PENDING_REVIEW` | Enforces mandatory 5-point human sign-off |

## CLI Usage

Run strict technical QA with duration and music verification:

```bash
# Verify 6-7 minute documentary duration (360-420s) and require music
python3 scripts/qa_media.py \
  --media exports/master_documentary.mp4 \
  --manifest project-manifest.json \
  --min-duration 360.0 \
  --max-duration 420.0 \
  --require-music
```

Emit JSON report for CI/CD pipelines:

```bash
python3 scripts/qa_media.py \
  --media exports/master_documentary.mp4 \
  --manifest project-manifest.json \
  --min-duration 360.0 \
  --max-duration 420.0 \
  --json
```

## Mandatory Human Review Checkpoints

Even when all automated checks pass, `qa_media.py` awards `TECHNICALLY_VALID_PENDING_REVIEW`, requiring human completion of:
1. Urdu pronunciation, inflection, and cadence in voiceover track.
2. Visual relevance and editorial pacing of stock footage cuts relative to spoken narration.
3. Urdu subtitle typography, RTL line-wrapping, and safe-margin clearance on mobile screens.
4. Background music ducking remains audible without competing with narrative intelligibility.
5. Verification that recognizable persons or private property have appropriate editorial/commercial clearance.
