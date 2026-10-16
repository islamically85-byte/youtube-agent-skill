---
name: yt-stock-producer
description: Curate, verify, and register permissive free stock footage (Pexels, Pixabay, Mixkit, CC0) into a deterministic project manifest with commercial licensing provenance.
---

# yt-stock-producer — Free Stock Footage Curator & Licensing Registrar

`yt-stock-producer` provides editorial curation and rigorous licensing verification for free stock footage, producing a valid `project-manifest.json` ready for multi-track video assembly.

## Permissive Stock Video Repositories

| Repository | Primary License Class | Commercial YouTube Monetization | Model/Property Release Rule |
| :--- | :--- | :--- | :--- |
| **Pexels** | `Pexels License` | Allowed without attribution | Required for recognizable faces; scenic safe |
| **Pixabay** | `Pixabay License` | Allowed without attribution | Avoid recognizable logos, brands, or private property |
| **Mixkit** | `Mixkit Free License` | Allowed for YouTube video | Check specific item tier (Free vs Restricted) |
| **Creative Commons CC0** | `Creative Commons CC0` | Public domain dedication | Completely unrestricted worldwide |
| **Creator-Owned** | `Creator Owned` | Full creator copyright | Self-cleared |

## The 6 Curation Rules

1. **Documentary Visual Metaphor**:
   - Stock footage must visualize the emotional or factual essence of the spoken line, not literal clichés.
   - Example: For "اندرونی تنہائی اور گھٹن" (internal loneliness and suffocation), use a slow-motion shot of rain hitting a windowpane in twilight, not a person holding their head.

2. **Pacing & Shot Variety**:
   - Long-form documentary cuts should breathe (3.0 to 6.0 seconds per clip).
   - Fast-paced Shorts require cuts every 1.5 to 2.5 seconds.
   - Alternate between wide establishing shots, intimate close-ups, and atmospheric macro textures.

3. **Strict Model & Trademark Avoidance**:
   - Scenic, nature, macro, and architectural footage require no model releases.
   - For shots with identifiable people in commercial videos, verify whether model releases exist or use silhouette/over-the-shoulder angles.
   - Reject clips displaying prominent commercial logos (Apple, Nike, Coca-Cola).

4. **Zero-Credit Quota Compliance**:
   - Never use paid stock platforms (Shutterstock, Getty, Envato Elements) or AI image generation tokens without explicit consent.
   - Enforce `credit_budget: 0` in all generated manifests.

5. **Deterministic Manifest Output**:
   - Every clip must be registered in `project-manifest.json` with:
     * `id`: Unique identifier (e.g., `clip_01_window_rain`)
     * `source_type`: `pexels`, `pixabay`, `mixkit`, `creator_owned`, or `local`
     * `source_url_or_path`: Web URL or local file path
     * `license_class`: Exact license tier
     * `license_verified_date`: YYYY-MM-DD
     * `clip_duration_sec`: Total duration of clip
     * `timeline_in_sec` & `timeline_out_sec`: Placement on the final master edit timeline

6. **Pre-Flight Manifest Validation**:
   - Validate the manifest using `validate_manifest.py`:
     ```bash
     python3 scripts/validate_manifest.py --manifest project-manifest.json --strict
     ```
