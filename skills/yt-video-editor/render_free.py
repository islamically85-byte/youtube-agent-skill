#!/usr/bin/env python3
"""render_free.py - Multi-track FFmpeg assembly engine for free-first YouTube production.

Features:
- Assembles stock video clips according to project-manifest.json.
- Normalizes footage to canvas resolution (16:9 1080p, 9:16 Shorts, or 1:1) with uniform framerate.
- Multi-track audio mix:
    * Narration normalized to -14.0 LUFS via FFmpeg loudnorm.
    * Ducked background music (-24 dB / volume adjustment).
- Subtitle rendering:
    * Supports burned-in subtitles when libass is compiled into FFmpeg.
    * Automatically falls back to muxed standard subtitle tracks (mov_text) with language tags (e.g. Urdu 'urd').
- Procedural generation mode:
    * Generates synthetic visual/audio assets when running offline tests or demos without external dependencies.
- Dry-run mode:
    * Generates and validates the full FFmpeg command without executing.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    from validate_manifest import validate_manifest_data
except ImportError:
    try:
        from shared.scripts.validate_manifest import validate_manifest_data
    except ImportError:
        def validate_manifest_data(data: Dict[str, Any], check_files: bool = False, base_dir: Optional[str] = None):
            return True, [], []


def escape_ffmpeg_filter_path(path: str) -> str:
    """Escapes file paths for use inside FFmpeg filtergraph arguments."""
    norm = os.path.normpath(path).replace("\\", "/")
    norm = norm.replace(":", r"\:")
    norm = norm.replace("'", r"\'")
    norm = norm.replace("[", r"\[").replace("]", r"\]")
    return norm


def find_ffmpeg() -> Optional[str]:
    """Locate ffmpeg binary in PATH or standard locations."""
    return shutil.which("ffmpeg")


def find_ffprobe() -> Optional[str]:
    """Locate ffprobe binary in PATH or standard locations."""
    return shutil.which("ffprobe")


def check_filter_supported(filter_name: str) -> bool:
    """Check if a specific filter is compiled into FFmpeg."""
    ffmpeg_bin = find_ffmpeg()
    if not ffmpeg_bin:
        return False
    try:
        proc = subprocess.run([ffmpeg_bin, "-filters"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        for line in proc.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[1] == filter_name:
                return True
        return False
    except Exception:
        return False


def generate_synthetic_assets(output_dir: str, duration_sec: float = 4.0) -> Dict[str, str]:
    """Generate synthetic video clips, narration tone, and music for testing/smoke runs."""
    ffmpeg_bin = find_ffmpeg()
    if not ffmpeg_bin:
        raise RuntimeError("ffmpeg binary required to generate synthetic assets.")

    os.makedirs(output_dir, exist_ok=True)
    clip1 = os.path.join(output_dir, "clip_1_stock.mp4")
    clip2 = os.path.join(output_dir, "clip_2_stock.mp4")
    narr = os.path.join(output_dir, "narration_ur.wav")
    bgm = os.path.join(output_dir, "bg_music.wav")
    subs = os.path.join(output_dir, "subtitles.srt")

    half_dur = max(1.0, duration_sec / 2.0)

    # Generate clip 1: 1920x1080 SMPTE color bars
    if not os.path.exists(clip1):
        cmd = [
            ffmpeg_bin, "-y", "-f", "lavfi",
            "-i", f"smptebars=duration={half_dur:.1f}:size=1920x1080:rate=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", clip1
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Generate clip 2: 1920x1080 test pattern
    if not os.path.exists(clip2):
        cmd = [
            ffmpeg_bin, "-y", "-f", "lavfi",
            "-i", f"testsrc=duration={half_dur:.1f}:size=1920x1080:rate=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", clip2
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Generate synthetic voiceover tone (simulating speech track)
    if not os.path.exists(narr):
        cmd = [
            ffmpeg_bin, "-y", "-f", "lavfi",
            "-i", f"sine=frequency=440:duration={duration_sec:.1f}",
            "-af", "volume=0.5",
            narr
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Generate synthetic background music tone (simulating gentle drone)
    if not os.path.exists(bgm):
        cmd = [
            ffmpeg_bin, "-y", "-f", "lavfi",
            "-i", f"sine=frequency=220:duration={duration_sec + 1.0:.1f}",
            "-af", "volume=0.1",
            bgm
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Generate synthetic Urdu subtitle file (UTF-8)
    if not os.path.exists(subs):
        with open(subs, "w", encoding="utf-8") as f:
            f.write(
                "1\n00:00:00,000 --> 00:00:02,000\nیہ ایک مکمل اور معیاری ویڈیو ٹیسٹ ہے\n\n"
                "2\n00:00:02,000 --> 00:00:04,000\nیوٹیوب ایجنٹ اسٹوڈیو ورژن ۲\n"
            )

    return {
        "clip1": clip1,
        "clip2": clip2,
        "narration": narr,
        "music": bgm,
        "subtitles": subs
    }


def build_ffmpeg_command(
    manifest: Dict[str, Any],
    manifest_dir: str,
    output_override: Optional[str] = None,
    burn_subtitles: bool = False
) -> Tuple[List[str], str]:
    """Construct deterministic FFmpeg command and filter_complex from manifest."""
    ffmpeg_bin = find_ffmpeg() or "ffmpeg"
    
    render_target = manifest.get("render_target", {})
    output_path = output_override or render_target.get("output_path", "output.mp4")
    if not os.path.isabs(output_path):
        output_path = os.path.join(manifest_dir, output_path)

    res_str = render_target.get("resolution", "1920x1080")
    try:
        width_str, height_str = res_str.lower().split("x")
        canvas_w, canvas_h = int(width_str), int(height_str)
    except Exception:
        canvas_w, canvas_h = 1920, 1080

    fps = int(render_target.get("fps", 30))
    video_codec = render_target.get("video_codec", "libx264")
    audio_codec = render_target.get("audio_codec", "aac")

    clips = manifest.get("footage_clips", [])
    if not clips:
        raise ValueError("Manifest has no footage_clips.")

    inputs: List[str] = []
    filter_chains: List[str] = []
    clip_output_labels: List[str] = []

    # 1. Add video clip inputs
    for idx, clip in enumerate(clips):
        c_path = clip.get("source_url_or_path", "")
        if not os.path.isabs(c_path):
            c_path = os.path.join(manifest_dir, c_path)
        inputs.extend(["-i", c_path])

        t_in = float(clip.get("timeline_in_sec", 0.0))
        t_out = float(clip.get("timeline_out_sec", 1.0))
        dur = max(0.1, t_out - t_in)

        label = f"v{idx}"
        chain = (
            f"[{idx}:v]trim=start=0:duration={dur:.3f},setpts=PTS-STARTPTS,"
            f"scale={canvas_w}:{canvas_h}:force_original_aspect_ratio=decrease,"
            f"pad={canvas_w}:{canvas_h}:(ow-iw)/2:(oh-ih)/2,"
            f"setsar=1,fps={fps}[{label}]"
        )
        filter_chains.append(chain)
        clip_output_labels.append(f"[{label}]")

    # 2. Concat video clips
    concat_inputs = "".join(clip_output_labels)
    concat_filter = f"{concat_inputs}concat=n={len(clips)}:v=1:a=0[v_concatenated]"
    filter_chains.append(concat_filter)

    # 3. Subtitles handling
    last_v_label = "v_concatenated"
    graphics = manifest.get("graphics_and_subtitles", {})
    sub_file = graphics.get("subtitles_file")
    has_sub_filter = check_filter_supported("subtitles")
    use_burned_subs = False
    use_muxed_subs = False
    sub_input_idx = None

    if sub_file:
        if not os.path.isabs(sub_file):
            sub_file = os.path.join(manifest_dir, sub_file)
        if os.path.exists(sub_file):
            if burn_subtitles and has_sub_filter:
                esc_path = escape_ffmpeg_filter_path(sub_file)
                sub_filter = f"[{last_v_label}]subtitles='{esc_path}':force_style='FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3'[v_subtitled]"
                filter_chains.append(sub_filter)
                last_v_label = "v_subtitled"
                use_burned_subs = True
            else:
                use_muxed_subs = True

    # 4. Audio tracks
    audio = manifest.get("audio", {})
    narration_info = audio.get("narration", {})
    narr_path = narration_info.get("file_path", "")
    if not os.path.isabs(narr_path):
        narr_path = os.path.join(manifest_dir, narr_path)

    narr_input_idx = len(clips)
    inputs.extend(["-i", narr_path])

    target_lufs = float(narration_info.get("target_lufs", -14.0))
    filter_chains.append(
        f"[{narr_input_idx}:a]loudnorm=I={target_lufs:.1f}:TP=-1.5:LRA=11[a_narr_norm]"
    )

    bg_music = audio.get("background_music")
    if bg_music and bg_music.get("file_path"):
        bg_path = bg_music["file_path"]
        if not os.path.isabs(bg_path):
            bg_path = os.path.join(manifest_dir, bg_path)
        bg_input_idx = len(clips) + 1
        inputs.extend(["-i", bg_path])

        duck_db = float(bg_music.get("ducking_level_db", -24.0))
        volume_factor = max(0.01, min(1.0, 10 ** (duck_db / 20.0)))
        filter_chains.append(f"[{bg_input_idx}:a]volume={volume_factor:.4f}[a_bg_ducked]")
        filter_chains.append(
            f"[a_narr_norm][a_bg_ducked]amix=inputs=2:duration=first:dropout_transition=2[a_mixed]"
        )
        last_a_label = "a_mixed"
    else:
        last_a_label = "a_narr_norm"

    # If muxing subtitles
    extra_maps: List[str] = []
    if use_muxed_subs and sub_file:
        sub_input_idx = len(inputs) // 2
        inputs.extend(["-i", sub_file])
        extra_maps = [
            "-map", f"{sub_input_idx}:s",
            "-c:s", "mov_text",
            "-metadata:s:s:0", f"language={narration_info.get('language', 'urd')}"
        ]

    full_filtergraph = ";\n".join(filter_chains)

    target_dur = float(manifest.get("target_duration_sec", 1.0))
    cmd = [
        ffmpeg_bin, "-y",
        *inputs,
        "-filter_complex", full_filtergraph,
        "-map", f"[{last_v_label}]",
        "-map", f"[{last_a_label}]",
        *extra_maps,
        "-c:v", video_codec,
        "-preset", "medium",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", audio_codec,
        "-b:a", "192k",
        "-t", f"{target_dur:.3f}",
        "-movflags", "+faststart",
        output_path
    ]

    return cmd, output_path


def render_project(
    manifest_path: str,
    output_override: Optional[str] = None,
    burn_subtitles: bool = False,
    dry_run: bool = False
) -> int:
    """Execute rendering pipeline for the given project manifest."""
    manifest_abs = os.path.abspath(manifest_path)
    if not os.path.exists(manifest_abs):
        print(f"ERROR: Manifest not found: {manifest_abs}", file=sys.stderr)
        return 1

    manifest_dir = os.path.dirname(manifest_abs)
    with open(manifest_abs, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    is_valid, errors, warnings = validate_manifest_data(manifest, check_files=(not dry_run), base_dir=manifest_dir)
    if not is_valid:
        print("❌ Manifest validation failed before render:", file=sys.stderr)
        for err in errors:
            print(f"   - {err}", file=sys.stderr)
        return 1

    if warnings:
        print("⚠️ Manifest warnings:")
        for w in warnings:
            print(f"   - {w}")

    cmd, out_path = build_ffmpeg_command(
        manifest,
        manifest_dir=manifest_dir,
        output_override=output_override,
        burn_subtitles=burn_subtitles
    )

    if dry_run:
        print("🔍 [DRY RUN] FFmpeg Command:")
        print(" ".join(f'"{arg}"' if " " in arg or "\n" in arg else arg for arg in cmd))
        print(f"\nTarget Output: {out_path}")
        return 0

    ffmpeg_bin = find_ffmpeg()
    if not ffmpeg_bin:
        print("ERROR: ffmpeg executable not found in PATH. Install ffmpeg to render video.", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    print(f"🎬 Starting video render for project '{manifest.get('project_id')}'...")
    print(f"   Resolution: {manifest.get('render_target', {}).get('resolution', '1920x1080')}")
    print(f"   Clips: {len(manifest.get('footage_clips', []))}")
    print(f"   Target: {out_path}")

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        print(f"❌ FFmpeg rendering failed with exit code {proc.returncode}:", file=sys.stderr)
        err_lines = proc.stderr.strip().splitlines()
        for line in err_lines[-15:]:
            print(f"   {line}", file=sys.stderr)
        return proc.returncode

    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        size_mb = os.path.getsize(out_path) / (1024 * 1024)
        print(f"✅ Render complete: {out_path} ({size_mb:.2f} MB)")
        return 0
    else:
        print(f"❌ Output file missing or zero bytes after render: {out_path}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-track FFmpeg assembly engine for YouTube Agent Studio.")
    parser.add_argument("--manifest", "-m", help="Path to project manifest JSON.")
    parser.add_argument("--output", "-o", help="Override output MP4 file path.")
    parser.add_argument("--burn-subtitles", action="store_true", help="Burn subtitles directly into video frames.")
    parser.add_argument("--dry-run", action="store_true", help="Print FFmpeg command without executing.")
    parser.add_argument("--synthetic", action="store_true", help="Generate synthetic fixtures and render demo.")
    parser.add_argument("--synthetic-dir", default="shared/fixtures/synthetic_demo", help="Directory for synthetic assets.")
    args = parser.parse_args()

    if args.synthetic:
        syn_dir = os.path.abspath(args.synthetic_dir)
        print(f"🧪 Generating synthetic assets in {syn_dir}...")
        assets = generate_synthetic_assets(syn_dir, duration_sec=4.0)

        demo_manifest = {
            "project_id": "synthetic_smoke_test_001",
            "title": "Synthetic Stock Footage Documentary Smoke Test",
            "target_duration_sec": 4.0,
            "aspect_ratio": "16:9",
            "credit_budget": 0,
            "footage_clips": [
                {
                    "id": "clip_1",
                    "source_type": "procedural_test",
                    "source_url_or_path": assets["clip1"],
                    "license_class": "MIT Procedural Test",
                    "license_verified_date": "2026-10-16",
                    "clip_duration_sec": 2.0,
                    "timeline_in_sec": 0.0,
                    "timeline_out_sec": 2.0
                },
                {
                    "id": "clip_2",
                    "source_type": "procedural_test",
                    "source_url_or_path": assets["clip2"],
                    "license_class": "MIT Procedural Test",
                    "license_verified_date": "2026-10-16",
                    "clip_duration_sec": 2.0,
                    "timeline_in_sec": 2.0,
                    "timeline_out_sec": 4.0
                }
            ],
            "audio": {
                "narration": {
                    "file_path": assets["narration"],
                    "language": "ur",
                    "script_format": "urdu_nastaliq",
                    "target_lufs": -14.0,
                    "voice_provenance": "procedural_test"
                },
                "background_music": {
                    "file_path": assets["music"],
                    "license_class": "MIT Procedural Test",
                    "ducking_level_db": -24.0
                }
            },
            "graphics_and_subtitles": {
                "subtitles_file": assets["subtitles"],
                "rtl_layout": True
            },
            "render_target": {
                "output_path": os.path.join(syn_dir, "synthetic_rendered_demo.mp4"),
                "resolution": "1920x1080",
                "fps": 30,
                "video_codec": "libx264",
                "audio_codec": "aac"
            }
        }

        demo_manifest_path = os.path.join(syn_dir, "demo_manifest.json")
        with open(demo_manifest_path, "w", encoding="utf-8") as f:
            json.dump(demo_manifest, f, indent=2)

        print(f"📝 Created demo manifest: {demo_manifest_path}")
        return render_project(
            demo_manifest_path,
            output_override=args.output,
            burn_subtitles=args.burn_subtitles,
            dry_run=args.dry_run
        )

    if not args.manifest:
        parser.print_help()
        return 1

    return render_project(
        args.manifest,
        output_override=args.output,
        burn_subtitles=args.burn_subtitles,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    sys.exit(main())
