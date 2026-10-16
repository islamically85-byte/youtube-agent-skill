---
name: yt-assets
description: Stock footage and music asset curator. Performs semantic story-to-shot mapping (70-95 shots for 6-7 min), verifies permissive licenses, and ensures asset integrity.
---

# yt-assets — Stock Footage & Music Asset Curator v3.0

`yt-assets` directs visual asset acquisition, licensing validation, and editorial shot planning for documentary videos. It replaces random category rotation with semantic story-to-shot mapping, generating an Edit Decision List (EDL) of 70–95 distinct cuts for a full 6–7 minute timeline.

## Core Capabilities

1. **Semantic Story-to-Shot Mapping**:
   - Matches visual scenes strictly to narration topics (e.g., Margalla Hills/Islamabad for opening drone shots; blueprints/construction for file trading; courthouses for inquiries).
2. **Accurate Manifest Validation**:
   - Replaces nominal count mismatches (e.g. naming files `_47.csv` when only 22 rows exist) with verified, deterministic row counting and SHA-256 verification.
3. **Licensing Provenance**:
   - Audits every media URL and classifies licenses into permissive categories (`free_commercial_with_attribution`, `cc0_public_domain`, `pexels_license`, `pixabay_license`).
4. **EDL Generation**:
   - Generates 70–95 shot sequences with dynamic 3.5s – 6.0s durations and non-repetitive clip cycling.

## CLI Usage

Generate a 70–95 shot Edit Decision List from an asset manifest:

```bash
# Generate EDL for a 390-second (6.5 minute) documentary
python3 scripts/stock_director.py --manifest Stock_Footage_Manifest_22.csv --duration 390.0 --out edit_decisions.json
```

Validate manifest licensing and asset integrity:

```bash
python3 scripts/validate_manifest.py project-manifest.json
```

## Manifest JSON Schema

```json
{
  "project_id": "pakistan_property_doc_v3",
  "footage_clips": [
    {
      "clip_id": "S01",
      "filename": "islamabad_drone_aerial.mp4",
      "source_url": "https://www.pexels.com/video/...",
      "license_class": "pexels_license",
      "duration_sec": 12.5,
      "sha256": "..."
    }
  ]
}
```
