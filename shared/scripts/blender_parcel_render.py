#!/usr/bin/env python3
"""
blender_parcel_render.py — 3D Land Parcel & Architectural Visualization Engine
Part of YouTube Agent Studio v3.0

Generates procedural 3D land parcels, boundary grids, and structural representations
of the 6,000 physical plots vs 42,000 issued files using headless Blender (bpy).
Supports animated camera flyovers, PBR material workflows, and MP4/PNG sequence output.

Author: ABDUL MUEED LASHARY
Upstream: Jake Schincariol (MIT License)
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def find_blender() -> Optional[str]:
    """Locate Blender executable across macOS, Windows, and Linux."""
    custom = os.environ.get("BLENDER_PATH")
    if custom and os.path.exists(custom):
        return custom

    # Priority 2: PATH
    path_bin = shutil.which("blender")
    if path_bin:
        return path_bin

    # Priority 3: Standard OS paths
    system = platform.system().lower()
    if system == "darwin":
        candidates = [
            "/Applications/Blender.app/Contents/MacOS/Blender",
            os.path.expanduser("~/Applications/Blender.app/Contents/MacOS/Blender"),
        ]
    elif system == "windows":
        prog_files = os.environ.get("PROGRAMFILES", r"C:\Program Files")
        candidates = [
            os.path.join(prog_files, r"Blender Foundation\Blender 5.2\blender.exe"),
            os.path.join(prog_files, r"Blender Foundation\Blender 5.0\blender.exe"),
            os.path.join(prog_files, r"Blender Foundation\Blender 4.2\blender.exe"),
            os.path.join(prog_files, r"Blender Foundation\Blender 4.0\blender.exe"),
            os.path.join(prog_files, r"Blender Foundation\Blender\blender.exe"),
        ]
    else:
        candidates = [
            "/usr/bin/blender",
            "/snap/bin/blender",
            "/usr/local/bin/blender",
        ]

    for p in candidates:
        if p and os.path.exists(p):
            return p
    return None


def run_blender_scene(
    output_path: str,
    frames: int = 120,
    fps: int = 30,
    width: int = 1920,
    height: int = 1080,
    plots_count: int = 6000,
    files_count: int = 42000,
    blender_bin: Optional[str] = None,
) -> Dict[str, any]:
    """
    Execute Blender in headless background mode to generate and render the 3D scene.
    """
    blender = blender_bin or find_blender()
    if not blender:
        raise RuntimeError(
            "Blender executable not found! Please install Blender LTS.\n"
            "  macOS:   brew install --cask blender\n"
            "  Windows: winget install BlenderFoundation.Blender\n"
            "  Linux:   sudo apt-get install blender"
        )

    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # In-memory Blender python script passed via temporary file
    blender_py_code = f"""
import bpy
import math
import os

# Set render settings
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = {width}
scene.render.resolution_y = {height}
scene.render.fps = {fps}
scene.frame_start = 1
scene.frame_end = {frames}

# Clear default objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create World & Environment
world = bpy.data.worlds.new("DocumentaryWorld")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0.02, 0.03, 0.05, 1.0)
    bg.inputs['Strength'].default_value = 0.5

# 1. Procedural Ground Plane (Master Site)
bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "GroundSite"
mat_ground = bpy.data.materials.new(name="Mat_Ground")
mat_ground.use_nodes = True
bsdf = mat_ground.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.05, 0.07, 0.09, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.85
ground.data.materials.append(mat_ground)

# 2. Road Network Grid & Survey Sectors
for r in range(-4, 5):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(r * 15, 0, 0.05))
    road_x = bpy.context.active_object
    road_x.scale = (0.8, 80, 0.02)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, r * 15, 0.05))
    road_y = bpy.context.active_object
    road_y.scale = (80, 0.8, 0.02)

# 3. The 6,000 Allotted Land Plots (Organized physical residential pads)
# Create a visually realistic sample array representing the approved 6,000 plots
plot_mat = bpy.data.materials.new(name="Mat_Plots")
plot_mat.use_nodes = True
p_bsdf = plot_mat.node_tree.nodes.get("Principled BSDF")
if p_bsdf:
    p_bsdf.inputs['Base Color'].default_value = (0.06, 0.45, 0.25, 1.0) # Emerald zoning
    p_bsdf.inputs['Roughness'].default_value = 0.5

for i in range(-5, 6):
    for j in range(-5, 6):
        if (i, j) == (0, 0): continue
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 4.5, j * 4.5, 0.2))
        plot = bpy.context.active_object
        plot.scale = (3.2, 3.2, 0.3)
        plot.data.materials.append(plot_mat)

# 4. The 42,000 Issued Files (Towering Monolith / Staggering Paper Stack)
# Visually demonstrating the 7:1 ratio towering 45m above the ground plots
stack_mat = bpy.data.materials.new(name="Mat_FileStack")
stack_mat.use_nodes = True
s_bsdf = stack_mat.node_tree.nodes.get("Principled BSDF")
if s_bsdf:
    s_bsdf.inputs['Base Color'].default_value = (0.85, 0.15, 0.15, 1.0) # Crimson tension
    s_bsdf.inputs['Roughness'].default_value = 0.2
    if 'Transmission Weight' in s_bsdf.inputs:
        s_bsdf.inputs['Transmission Weight'].default_value = 0.25

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 22.5))
tower = bpy.context.active_object
tower.name = "Tower_42000_Files"
tower.scale = (6.0, 6.0, 45.0) # 700% height disparity
tower.data.materials.append(stack_mat)

# 5. Sun Light and Warm Rim Accent
bpy.ops.object.light_add(type='SUN', location=(30, -40, 50))
sun = bpy.context.active_object
sun.data.energy = 3.5
sun.data.color = (1.0, 0.95, 0.88)
sun.rotation_euler = (math.radians(50), math.radians(15), math.radians(35))

bpy.ops.object.light_add(type='POINT', location=(-15, 15, 25))
rim = bpy.context.active_object
rim.data.energy = 500
rim.data.color = (0.2, 0.6, 1.0)

# 6. Cinematic Motivated Camera Flyover
bpy.ops.object.camera_add(location=(45, -55, 30))
cam = bpy.context.active_object
scene.camera = cam
cam.data.lens = 35 # Wide documentary focal length

# Track To Constraint pointing at the 42,000 file tower center
track = cam.constraints.new(type='TRACK_TO')
track.target = tower
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

# Animate Camera Orbit
cam.keyframe_insert(data_path="location", frame=1)
cam.location = (40, -50, 18)
cam.keyframe_insert(data_path="location", frame=1)

cam.location = (15, -45, 38)
cam.keyframe_insert(data_path="location", frame={frames})

# Render Configuration
scene.render.filepath = "{str(out_file)}"
if "{out_file.suffix.lower()}" == ".mp4":
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    bpy.ops.render.render(animation=True)
else:
    scene.render.image_settings.file_format = 'PNG'
    scene.frame_set(min(60, {frames}))
    bpy.ops.render.render(write_still=True)

print("[BLENDER-RENDER] Completed scene generation successfully.")
"""

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(blender_py_code)
        script_path = f.name

    t0 = time.time()
    cmd = [blender, "--background", "--python", script_path]
    print(f"[BLENDER-3D] Launching Blender headless: {blender}")
    print(f"[BLENDER-3D] Resolution: {width}x{height} | Frames: {frames} | Target: {out_file.name}")

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        os.unlink(script_path)
        raise RuntimeError(f"Blender rendering failed:\n{e.stderr}\n{e.stdout}")
    finally:
        if os.path.exists(script_path):
            os.unlink(script_path)

    elapsed = time.time() - t0
    size_mb = out_file.stat().st_size / (1024 * 1024) if out_file.exists() else 0.0

    print(f"[BLENDER-3D] Render completed in {elapsed:.2f}s! Output size: {size_mb:.2f} MB")

    return {
        "status": "success",
        "output_path": str(out_file),
        "file_size_mb": round(size_mb, 2),
        "frames": frames,
        "fps": fps,
        "resolution": f"{width}x{height}",
        "render_time_sec": round(elapsed, 2),
        "maintainer": "ABDUL MUEED LASHARY",
        "license": "MIT",
    }


def main():
    parser = argparse.ArgumentParser(description="Blender 3D Land Parcel Visualization Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_p = subparsers.add_parser("check", help="Check Blender installation and environment")

    render_p = subparsers.add_parser("render", help="Render 3D land parcel visualization")
    render_p.add_argument("--out", required=True, help="Output file (.mp4 or .png)")
    render_p.add_argument("--frames", type=int, default=120, help="Total frames (default: 120)")
    render_p.add_argument("--fps", type=int, default=30, help="Frames per second (default: 30)")
    render_p.add_argument("--width", type=int, default=1920, help="Frame width (default: 1920)")
    render_p.add_argument("--height", type=int, default=1080, help="Frame height (default: 1080)")
    render_p.add_argument("--json", action="store_true", help="Output JSON result")

    args = parser.parse_args()

    if args.command == "check":
        b_path = find_blender()
        status = {
            "blender_found": bool(b_path),
            "blender_path": b_path,
            "os": platform.system(),
            "ready": bool(b_path),
        }
        print(json.dumps(status, indent=2))
        sys.exit(0 if status["ready"] else 1)

    elif args.command == "render":
        try:
            res = run_blender_scene(
                output_path=args.out,
                frames=args.frames,
                fps=args.fps,
                width=args.width,
                height=args.height,
            )
            if args.json:
                print(json.dumps(res, indent=2))
            else:
                print(f"[SUCCESS] 3D Parcel Scene rendered to: {res['output_path']} ({res['file_size_mb']} MB)")
        except Exception as e:
            print(f"[ERROR] 3D render failed: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
