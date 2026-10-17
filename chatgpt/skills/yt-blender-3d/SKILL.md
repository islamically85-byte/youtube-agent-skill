---
name: yt-blender-3d
description: Headless Blender 3D procedural land parcel and architectural visualization engine for YouTube Agent Studio v3.0 (ChatGPT Edition).
---

# yt-blender-3d — 3D Land Parcel & Architectural Visualization

`yt-blender-3d` renders physical 3D procedural master plans, boundary grids, and structural representations of land records using headless Blender LTS (`bpy`).

Maintained by **ABDUL MUEED LASHARY** as part of YouTube Agent Studio v3.0 (ChatGPT Edition).

---

## Capabilities & Architecture

1. **Procedural Site & Master Plan Reconstruction**:
   - Replaces artificial flat cards with realistic 3D spatial models.
   - Generates terrain ground slabs with PBR material shaders (roughness, specular, micro-details).
   - Generates road network grids, sector boundaries, and surveyor markings.

2. **The 6,000 Plots vs 42,000 Files Disparity**:
   - **Ground Capacity (6,000 Plots)**: Modeled as organized physical residential boundary pads with emerald zoning demarcations representing actual land capacity.
   - **Issued Files (42,000 Files)**: Modeled as a massive 45-meter towering monolith / structural stack soaring into the sky, physically displaying the catastrophic 7:1 over-allocation ratio in true 3D space.

3. **Cinematic Motivated Camera**:
   - Wide documentary focal length (35mm).
   - Smooth orbital camera tracking using constraint solvers (`TRACK_TO`).
   - Sunlight key lighting, sky fill, and cool rim accent lights.

4. **Headless Execution & Zero GUI Requirement**:
   - Runs purely in background CLI mode via `scripts/blender_parcel_render.py`.
   - Exports high-resolution stills (`.png`) or rendered MP4 animation flyovers.

---

## Command Reference

```bash
# Check Blender LTS availability
python3 scripts/blender_parcel_render.py check

# Render 3D land parcel still frame (1080p Full HD)
python3 scripts/blender_parcel_render.py render \
  --out output/blender_parcel_3d.png \
  --frames 60 --fps 30

# Render 4-second animated camera flyover (120 frames @ 30 FPS)
python3 scripts/blender_parcel_render.py render \
  --out output/blender_parcel_flyover.mp4 \
  --frames 120 --fps 30
```
