#!/usr/bin/env python3
"""
otio_export.py — OpenTimelineIO NLE Timeline Generator & Interchange Engine
Part of YouTube Agent Studio v3.0

Generates multi-track NLE timelines (.otio, .edl, .xml) linking B-roll footage,
3D Blender parcels, browser motion graphics overlays, and mastered broadcast audio stems.
Compatible with DaVinci Resolve, Adobe Premiere Pro, and Final Cut Pro.

Author: ABDUL MUEED LASHARY
Upstream: Jake Schincariol (MIT License)
"""

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Check for OpenTimelineIO availability
HAS_OTIO = False
try:
    import opentimelineio as otio
    HAS_OTIO = True
except ImportError:
    HAS_OTIO = False


def build_otio_timeline(
    name: str = "Pakistan Property Group Documentary",
    fps: int = 30,
    clips: Optional[List[Dict[str, Any]]] = None,
    motion_overlays: Optional[List[Dict[str, Any]]] = None,
    blender_3d_clips: Optional[List[Dict[str, Any]]] = None,
    voice_track_path: Optional[str] = None,
    music_track_path: Optional[str] = None,
    output_path: Optional[str] = None,
) -> Any:
    """
    Construct a full multi-track documentary timeline using OpenTimelineIO.
    """
    if not HAS_OTIO:
        raise RuntimeError("opentimelineio package is not installed. Run 'pip install opentimelineio'.")

    timeline = otio.schema.Timeline(name=name)
    timeline.global_start_time = otio.opentime.RationalTime(0, fps)

    # 1. Base Video Track (B-roll Stock Footage)
    video_track = otio.schema.Track(name="V1_Base_Footage", kind=otio.schema.TrackKind.Video)
    timeline.tracks.append(video_track)

    # 2. 3D Architectural / Blender Track
    blender_track = otio.schema.Track(name="V2_Blender_3D", kind=otio.schema.TrackKind.Video)
    timeline.tracks.append(blender_track)

    # 3. Motion Graphics Overlay Track
    motion_track = otio.schema.Track(name="V3_Motion_Graphics", kind=otio.schema.TrackKind.Video)
    timeline.tracks.append(motion_track)

    # 4. Audio Track 1: Mastered Urdu Voiceover (-14 LUFS)
    audio_voice_track = otio.schema.Track(name="A1_Urdu_Voiceover", kind=otio.schema.TrackKind.Audio)
    timeline.tracks.append(audio_voice_track)

    # 5. Audio Track 2: Ducked Atmospheric Music (-24 dB)
    audio_music_track = otio.schema.Track(name="A2_Atmospheric_BGM", kind=otio.schema.TrackKind.Audio)
    timeline.tracks.append(audio_music_track)

    # Populate Base Footage Clips
    if clips:
        for idx, item in enumerate(clips):
            clip_name = item.get("clip_name", f"Clip_{idx+1:03d}")
            duration_sec = float(item.get("duration_sec", item.get("duration", 4.0)))
            frames_count = int(round(duration_sec * fps))
            target_url = item.get("file_path", item.get("url", f"/media/stock/{clip_name}.mp4"))

            media_ref = otio.schema.ExternalReference(target_url=str(target_url))
            clip = otio.schema.Clip(
                name=clip_name,
                media_reference=media_ref,
                source_range=otio.opentime.TimeRange(
                    start_time=otio.opentime.RationalTime(0, fps),
                    duration=otio.opentime.RationalTime(frames_count, fps),
                ),
            )
            # Add metadata tags
            clip.metadata["intent"] = item.get("intent", "b_roll")
            clip.metadata["license"] = item.get("license", "CC0")
            video_track.append(clip)
    else:
        # Placeholder 15s clip
        clip = otio.schema.Clip(
            name="Establishing_Aerial_Site",
            media_reference=otio.schema.ExternalReference(target_url="assets/stock/aerial_site.mp4"),
            source_range=otio.opentime.TimeRange(
                start_time=otio.opentime.RationalTime(0, fps),
                duration=otio.opentime.RationalTime(15 * fps, fps),
            ),
        )
        video_track.append(clip)

    # Populate 3D Blender Clips
    if blender_3d_clips:
        for b_item in blender_3d_clips:
            dur_sec = float(b_item.get("duration_sec", 4.0))
            b_clip = otio.schema.Clip(
                name=b_item.get("name", "Blender_Parcel_3D"),
                media_reference=otio.schema.ExternalReference(target_url=b_item.get("path", "output/blender_parcel_3d.mp4")),
                source_range=otio.opentime.TimeRange(
                    start_time=otio.opentime.RationalTime(0, fps),
                    duration=otio.opentime.RationalTime(int(round(dur_sec * fps)), fps),
                ),
            )
            blender_track.append(b_clip)

    # Populate Motion Graphics Overlays
    if motion_overlays:
        for m_item in motion_overlays:
            dur_sec = float(m_item.get("duration_sec", 15.0))
            m_clip = otio.schema.Clip(
                name=m_item.get("name", "Motion_Discrepancy_Counter"),
                media_reference=otio.schema.ExternalReference(target_url=m_item.get("path", "output/demo_motion_15s.mp4")),
                source_range=otio.opentime.TimeRange(
                    start_time=otio.opentime.RationalTime(0, fps),
                    duration=otio.opentime.RationalTime(int(round(dur_sec * fps)), fps),
                ),
            )
            # Add disclaimer marker
            marker = otio.schema.Marker(
                name="Mandatory Legal Disclaimer",
                marked_range=otio.opentime.TimeRange(
                    start_time=otio.opentime.RationalTime(int(round(1.0 * fps)), fps),
                    duration=otio.opentime.RationalTime(int(round(14.0 * fps)), fps),
                ),
                color=otio.schema.MarkerColor.RED,
            )
            m_clip.markers.append(marker)
            motion_track.append(m_clip)

    # Add Voice Audio Track
    if voice_track_path:
        voice_clip = otio.schema.Clip(
            name="Urdu_Voiceover_Mastered",
            media_reference=otio.schema.ExternalReference(target_url=str(voice_track_path)),
            source_range=otio.opentime.TimeRange(
                start_time=otio.opentime.RationalTime(0, fps),
                duration=timeline.duration(),
            ),
        )
        audio_voice_track.append(voice_clip)

    # Add Music Audio Track
    if music_track_path:
        music_clip = otio.schema.Clip(
            name="Atmospheric_BGM_Ducked",
            media_reference=otio.schema.ExternalReference(target_url=str(music_track_path)),
            source_range=otio.opentime.TimeRange(
                start_time=otio.opentime.RationalTime(0, fps),
                duration=timeline.duration(),
            ),
        )
        audio_music_track.append(music_clip)

    # Save to file if output_path specified
    if output_path:
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)
        suffix = out_p.suffix.lower()

        if suffix in [".otio", ".otiod", ".otioz", ".json"]:
            otio.adapters.write_to_file(timeline, str(out_p))
        elif suffix == ".edl":
            # Attempt adapter, fallback to native CMX 3600 generator
            try:
                otio.adapters.write_to_file(timeline, str(out_p), adapter_name="cmx_3600")
            except Exception:
                edl_lines = [f"TITLE: {timeline.name}", "FCM: NON-DROP FRAME", ""]
                rec_in = 0
                for idx, clip in enumerate(video_track):
                    dur_frames = clip.source_range.duration.value
                    src_out_tc = f"{int(dur_frames//(30*60)):02d}:{int((dur_frames//30)%60):02d}:{int(dur_frames%30):02d}:00"
                    rec_out = rec_in + dur_frames
                    rec_in_tc = f"{int(rec_in//(30*60)):02d}:{int((rec_in//30)%60):02d}:{int(rec_in%30):02d}:00"
                    rec_out_tc = f"{int(rec_out//(30*60)):02d}:{int((rec_out//30)%60):02d}:{int(rec_out%30):02d}:00"
                    edl_lines.append(f"{idx+1:03d}  AX       V     C        00:00:00:00 {src_out_tc} {rec_in_tc} {rec_out_tc}")
                    edl_lines.append(f"* FROM CLIP NAME: {clip.name}")
                    rec_in = rec_out
                out_p.write_text("\n".join(edl_lines) + "\n", encoding="utf-8")
        else:
            otio.adapters.write_to_file(timeline, str(out_p))

    return timeline


def load_manifest_clips(manifest_csv_path: str) -> List[Dict[str, Any]]:
    """Parse stock footage CSV manifest into structured clips list."""
    path = Path(manifest_csv_path)
    if not path.exists():
        return []

    clips = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dur = 4.0
            for key in ["Duration (s)", "Duration", "duration_sec", "duration"]:
                if key in row and row[key]:
                    try:
                        dur = float(row[key])
                        break
                    except ValueError:
                        pass
            name = row.get("File Name", row.get("Clip Name", row.get("name", "Clip")))
            clips.append({
                "clip_name": name,
                "duration_sec": dur,
                "file_path": row.get("Local File Path", row.get("url", f"assets/stock/{name}")),
                "intent": row.get("Editorial Intent", "b_roll"),
                "license": row.get("License Class", "CC0"),
            })
    return clips


def main():
    parser = argparse.ArgumentParser(description="OpenTimelineIO NLE Timeline Generator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_p = subparsers.add_parser("check", help="Check OpenTimelineIO environment availability")

    export_p = subparsers.add_parser("export", help="Export an NLE timeline (.otio, .edl, .xml)")
    export_p.add_argument("--name", default="Pakistan Property Group Documentary", help="Timeline name")
    export_p.add_argument("--manifest", help="Optional stock footage CSV manifest")
    export_p.add_argument("--motion", help="Path to motion graphics MP4/MOV")
    export_p.add_argument("--blender", help="Path to Blender 3D render")
    export_p.add_argument("--voice", help="Path to mastered Urdu voiceover (.wav)")
    export_p.add_argument("--music", help="Path to ducked background music (.wav)")
    export_p.add_argument("--out", required=True, help="Output timeline path (.otio, .edl, .xml)")
    export_p.add_argument("--fps", type=int, default=30, help="Timeline frame rate (default: 30)")
    export_p.add_argument("--json", action="store_true", help="Output JSON result")

    args = parser.parse_args()

    if args.command == "check":
        status = {
            "opentimelineio_available": HAS_OTIO,
            "version": otio.__version__ if HAS_OTIO else None,
            "supported_adapters": [
                "otio_json", "cmx_3600_edl", "fcp_xml", "rv_session"
            ] if HAS_OTIO else [],
            "ready": HAS_OTIO,
        }
        print(json.dumps(status, indent=2))
        sys.exit(0 if HAS_OTIO else 1)

    elif args.command == "export":
        clips = load_manifest_clips(args.manifest) if args.manifest else None
        motion_overlays = [{"name": "Motion_Overlay", "path": args.motion, "duration_sec": 15.0}] if args.motion else None
        blender_clips = [{"name": "Blender_3D_Parcel", "path": args.blender, "duration_sec": 5.0}] if args.blender else None

        try:
            tl = build_otio_timeline(
                name=args.name,
                fps=args.fps,
                clips=clips,
                motion_overlays=motion_overlays,
                blender_3d_clips=blender_clips,
                voice_track_path=args.voice,
                music_track_path=args.music,
                output_path=args.out,
            )
            dur_sec = tl.duration().to_seconds()
            track_count = len(tl.tracks)
            res = {
                "status": "success",
                "timeline_name": tl.name,
                "output_path": str(Path(args.out).resolve()),
                "duration_seconds": round(dur_sec, 2),
                "fps": args.fps,
                "tracks_count": track_count,
                "maintainer": "ABDUL MUEED LASHARY",
                "license": "MIT",
            }
            if args.json:
                print(json.dumps(res, indent=2))
            else:
                print(f"[SUCCESS] Timeline exported to {res['output_path']}")
                print(f"  Duration: {res['duration_seconds']}s across {res['tracks_count']} tracks ({res['fps']} FPS)")
        except Exception as e:
            print(f"[ERROR] OTIO export failed: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
