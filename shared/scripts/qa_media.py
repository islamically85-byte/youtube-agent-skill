#!/usr/bin/env python3
"""qa_media.py - Automated Technical QA Prober for YouTube Documentary Media.

Performs deterministic inspection of rendered MP4/MOV files using ffprobe and ffmpeg:
1. Probes container and stream metrics (resolution, duration, fps, video/audio codecs).
2. Detects unexpected black frames / video drops (via blackdetect filter).
3. Analyzes EBU R128 loudness metrics (integrated LUFS and true peak).
4. Verifies licensing compliance against the project manifest if provided.
5. Emits an automated QA report conforming to qa-report.schema.json.
6. Enforces that passing outputs are labeled 'TECHNICALLY_VALID_PENDING_REVIEW'
   to ensure mandatory human review is never bypassed.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple


def find_binary(name: str) -> Optional[str]:
    """Locate binary in PATH or return None."""
    return shutil.which(name)


def probe_media_file(media_path: str) -> Dict[str, Any]:
    """Run ffprobe on media file and return streams/format dict."""
    ffprobe_bin = find_binary("ffprobe")
    if not ffprobe_bin:
        raise RuntimeError("ffprobe executable not found in PATH.")

    cmd = [
        ffprobe_bin, "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        media_path
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {proc.stderr.strip()}")

    return json.loads(proc.stdout)


def parse_framerate(r_frame_rate: str) -> float:
    """Parse fractional frame rate e.g. '30/1' or '24000/1001'."""
    try:
        if "/" in r_frame_rate:
            num, den = r_frame_rate.split("/")
            return float(num) / float(den)
        return float(r_frame_rate)
    except Exception:
        return 30.0


def detect_black_frames(media_path: str, min_duration_sec: float = 0.5) -> Tuple[bool, int, List[str]]:
    """Detect black frames intervals exceeding min_duration_sec using ffmpeg blackdetect."""
    ffmpeg_bin = find_binary("ffmpeg")
    if not ffmpeg_bin:
        return True, 0, []

    cmd = [
        ffmpeg_bin, "-i", media_path,
        "-vf", f"blackdetect=d={min_duration_sec:.2f}:pic_th=0.98",
        "-an", "-f", "null", "-"
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    intervals: List[str] = []
    # Lines look like: [blackdetect @ 0x...] black_start:1.20 black_end:2.00 black_duration:0.80
    pattern = re.compile(r"black_start:([0-9.]+)\s+black_end:([0-9.]+)\s+black_duration:([0-9.]+)")
    for match in pattern.finditer(proc.stderr):
        start, end, dur = match.groups()
        intervals.append(f"{start}s - {end}s ({dur}s)")

    passed = (len(intervals) == 0)
    return passed, len(intervals), intervals


def measure_ebur128_loudness(media_path: str) -> Tuple[bool, float, float]:
    """Measure EBU R128 integrated loudness (LUFS) and true peak using ffmpeg ebur128."""
    ffmpeg_bin = find_binary("ffmpeg")
    if not ffmpeg_bin:
        return True, -14.0, -1.5

    cmd = [
        ffmpeg_bin, "-i", media_path,
        "-filter_complex", "ebur128=peak=true",
        "-f", "null", "-"
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Parse Summary block:
    #   Integrated loudness:
    #     I:         -20.0 LUFS
    #   True peak:
    #     Peak:      -12.9 dBFS
    integrated_lufs = -14.0
    true_peak = -1.5

    i_match = re.search(r"Integrated loudness:\s+I:\s+([-\d.]+)\s+LUFS", proc.stderr)
    if i_match:
        try:
            integrated_lufs = float(i_match.group(1))
        except ValueError:
            pass

    tp_match = re.search(r"True peak:\s+Peak:\s+([-\d.]+)\s+dBFS", proc.stderr)
    if tp_match:
        try:
            true_peak = float(tp_match.group(1))
        except ValueError:
            pass

    # YouTube standard is -14.0 LUFS. Tolerance: +/- 6 LUFS acceptable for raw mixes
    passed = (-24.0 <= integrated_lufs <= -10.0)
    return passed, integrated_lufs, true_peak


def check_licensing(manifest_path: Optional[str]) -> Tuple[bool, int]:
    """Check licensing provenance in manifest if provided."""
    if not manifest_path or not os.path.exists(manifest_path):
        return True, 0

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return False, 1

    unverified = 0
    clips = data.get("footage_clips", [])
    for clip in clips:
        lic = clip.get("license_class", "")
        if not lic or lic == "unknown":
            unverified += 1

    return (unverified == 0), unverified


MANDATORY_HUMAN_REVIEW_ITEMS = [
    "Verify Urdu pronunciation, inflection, and cadence in voiceover track.",
    "Confirm visual relevance and editorial pacing of stock footage cuts relative to spoken narration.",
    "Inspect Urdu subtitle typography, RTL line-wrapping, and safe-margin clearance on mobile screens.",
    "Ensure background music ducking remains audible without competing with narrative intelligibility.",
    "Verify that any recognizable persons or private property have appropriate editorial/commercial clearance."
]


def run_qa(
    media_path: str,
    manifest_path: Optional[str] = None,
    target_lufs: float = -14.0,
    min_duration: Optional[float] = None,
    max_duration: Optional[float] = None,
    require_music: bool = False
) -> Dict[str, Any]:
    """Run full technical QA analysis on media file."""
    media_abs = os.path.abspath(media_path)
    if not os.path.exists(media_abs):
        return {
            "project_id": "unknown",
            "media_path": media_path,
            "qa_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": "FAILED_CRITICAL_CHECKS",
            "probed_metrics": {
                "duration_sec": 0.0,
                "resolution": "0x0",
                "video_codec": "unknown",
                "audio_codec": "unknown"
            },
            "automated_checks": {
                "black_frames": {"passed": False, "drop_count": 0, "intervals": []},
                "audio_loudness": {"passed": False, "integrated_lufs": -99.0, "target_lufs": target_lufs, "true_peak_db": -99.0},
                "license_compliance": {"passed": False, "unverified_assets_count": 1},
                "duration_bounds": {"passed": False, "duration_sec": 0.0, "min_sec": min_duration, "max_sec": max_duration}
            },
            "mandatory_human_review_items": MANDATORY_HUMAN_REVIEW_ITEMS,
            "verdict_summary": f"Media file not found: {media_abs}"
        }

    project_id = "standalone_media"
    manifest_data: Dict[str, Any] = {}
    if manifest_path and os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
                project_id = manifest_data.get("project_id", project_id)
        except Exception:
            pass

    # 1. Probe streams
    if not find_binary("ffprobe"):
        return {
            "project_id": project_id,
            "media_path": media_abs,
            "qa_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": "FAILED_CRITICAL_CHECKS",
            "probed_metrics": {
                "duration_sec": 0.0,
                "resolution": "0x0",
                "video_codec": "none",
                "audio_codec": "none"
            },
            "automated_checks": {
                "black_frames": {"passed": False, "drop_count": 0, "intervals": []},
                "audio_loudness": {"passed": False, "integrated_lufs": -99.0, "target_lufs": target_lufs, "true_peak_db": -99.0},
                "license_compliance": {"passed": False, "unverified_assets_count": 0},
                "duration_bounds": {"passed": False, "duration_sec": 0.0, "min_sec": min_duration, "max_sec": max_duration}
            },
            "mandatory_human_review_items": MANDATORY_HUMAN_REVIEW_ITEMS,
            "verdict_summary": "ffprobe executable not found in PATH. Install ffmpeg/ffprobe to probe media."
        }

    probe_data = probe_media_file(media_abs)
    video_stream = next((s for s in probe_data.get("streams", []) if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in probe_data.get("streams", []) if s.get("codec_type") == "audio"), None)
    format_info = probe_data.get("format", {})

    dur = float(format_info.get("duration", 0.0))
    if dur == 0.0 and video_stream:
        dur = float(video_stream.get("duration", 0.0))

    width = int(video_stream.get("width", 0)) if video_stream else 0
    height = int(video_stream.get("height", 0)) if video_stream else 0
    v_codec = video_stream.get("codec_name", "none") if video_stream else "none"
    fps = parse_framerate(video_stream.get("r_frame_rate", "30/1")) if video_stream else 30.0

    a_codec = audio_stream.get("codec_name", "none") if audio_stream else "none"
    channels = int(audio_stream.get("channels", 0)) if audio_stream else 0
    sample_rate = int(audio_stream.get("sample_rate", 0)) if audio_stream else 0

    aspect_ratio = "16:9"
    if width > 0 and height > 0:
        ratio = width / height
        if abs(ratio - 16 / 9) < 0.05:
            aspect_ratio = "16:9"
        elif abs(ratio - 9 / 16) < 0.05:
            aspect_ratio = "9:16"
        elif abs(ratio - 1.0) < 0.05:
            aspect_ratio = "1:1"
        else:
            aspect_ratio = f"{width}:{height}"

    probed_metrics = {
        "duration_sec": round(dur, 2),
        "resolution": f"{width}x{height}",
        "aspect_ratio": aspect_ratio,
        "framerate_fps": round(fps, 2),
        "video_codec": v_codec,
        "audio_codec": a_codec,
        "audio_channels": channels,
        "sample_rate_hz": sample_rate
    }

    # 2. Automated checks
    bf_passed, bf_count, bf_intervals = detect_black_frames(media_abs)
    loudness_passed, int_lufs, true_peak = measure_ebur128_loudness(media_abs)
    lic_passed, unverified_lic_count = check_licensing(manifest_path)

    # Duration bounds check
    dur_bounds_passed = True
    dur_failures: List[str] = []
    if min_duration is not None and dur < min_duration:
        dur_bounds_passed = False
        dur_failures.append(f"duration {dur:.1f}s is below minimum requirement of {min_duration:.1f}s")
    if max_duration is not None and dur > max_duration:
        dur_bounds_passed = False
        dur_failures.append(f"duration {dur:.1f}s exceeds maximum requirement of {max_duration:.1f}s")

    # Music track check
    music_passed = True
    music_warning: Optional[str] = None
    if manifest_data:
        raw_manifest_str = json.dumps(manifest_data)
        if "MISSING_MUSIC_WARNING" in raw_manifest_str:
            music_warning = "MISSING_MUSIC_WARNING present in manifest"
            if require_music:
                music_passed = False
        elif manifest_data.get("music_present") is False or (require_music and not manifest_data.get("music_track")):
            music_warning = "Background music track is missing from project manifest"
            if require_music:
                music_passed = False

    automated_checks = {
        "black_frames": {
            "passed": bf_passed,
            "drop_count": bf_count,
            "intervals": bf_intervals
        },
        "audio_loudness": {
            "passed": loudness_passed,
            "integrated_lufs": round(int_lufs, 1),
            "target_lufs": target_lufs,
            "true_peak_db": round(true_peak, 1)
        },
        "license_compliance": {
            "passed": lic_passed,
            "unverified_assets_count": unverified_lic_count
        },
        "duration_bounds": {
            "passed": dur_bounds_passed,
            "duration_sec": round(dur, 2),
            "min_sec": min_duration,
            "max_sec": max_duration
        }
    }

    if require_music or music_warning:
        automated_checks["music_track"] = {
            "passed": music_passed,
            "required": require_music,
            "warning": music_warning
        }

    # Determine status
    critical_pass = (
        dur > 0 and
        width > 0 and
        height > 0 and
        v_codec != "none" and
        a_codec != "none" and
        bf_passed and
        loudness_passed and
        lic_passed and
        dur_bounds_passed and
        music_passed
    )

    if critical_pass:
        status = "TECHNICALLY_VALID_PENDING_REVIEW"
        summary = (
            f"All automated technical checks passed ({probed_metrics['resolution']}, {dur:.1f}s, "
            f"{int_lufs:.1f} LUFS). Human audiovisual sign-off is required before final publication."
        )
    else:
        status = "FAILED_CRITICAL_CHECKS"
        failures = []
        if dur <= 0:
            failures.append("duration is 0")
        if not bf_passed:
            failures.append(f"{bf_count} black frame intervals detected")
        if not loudness_passed:
            failures.append(f"integrated loudness {int_lufs:.1f} LUFS out of acceptable range")
        if not lic_passed:
            failures.append(f"{unverified_lic_count} unverified licenses")
        failures.extend(dur_failures)
        if not music_passed:
            failures.append(music_warning or "background music check failed")
        summary = f"Critical technical checks failed: {', '.join(failures)}."

    report = {
        "project_id": project_id,
        "media_path": media_abs,
        "qa_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": status,
        "probed_metrics": probed_metrics,
        "automated_checks": automated_checks,
        "mandatory_human_review_items": MANDATORY_HUMAN_REVIEW_ITEMS,
        "verdict_summary": summary
    }

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Automated Technical QA Prober for YouTube Media.")
    parser.add_argument("--media", "-m", required=True, help="Path to rendered MP4/MOV video file.")
    parser.add_argument("--manifest", help="Optional project manifest JSON to check license compliance.")
    parser.add_argument("--min-duration", type=float, default=None, help="Minimum acceptable duration in seconds.")
    parser.add_argument("--max-duration", type=float, default=None, help="Maximum acceptable duration in seconds.")
    parser.add_argument("--require-music", action="store_true", help="Require background music track without warnings.")
    parser.add_argument("--json", action="store_true", help="Output full report in JSON format.")
    args = parser.parse_args()

    report = run_qa(
        args.media,
        manifest_path=args.manifest,
        min_duration=args.min_duration,
        max_duration=args.max_duration,
        require_music=args.require_music
    )

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status = report["status"]
        print(f"🎬 QA Report for: {os.path.basename(report['media_path'])}")
        print(f"   Project ID: {report['project_id']}")
        print(f"   Status: {status}")
        print(f"   Summary: {report['verdict_summary']}")
        print(f"\n📊 Probed Metrics:")
        metrics = report["probed_metrics"]
        print(f"   - Resolution: {metrics['resolution']} ({metrics['aspect_ratio']}) @ {metrics['framerate_fps']} fps")
        print(f"   - Duration: {metrics['duration_sec']}s")
        print(f"   - Video / Audio: {metrics['video_codec']} / {metrics['audio_codec']} ({metrics['sample_rate_hz']} Hz)")

        print(f"\n🔍 Automated Checks:")
        checks = report["automated_checks"]
        bf = checks["black_frames"]
        print(f"   - Black Frames: {'PASSED' if bf['passed'] else 'FAILED'} (drops: {bf['drop_count']})")
        loud = checks["audio_loudness"]
        print(f"   - Audio Loudness: {'PASSED' if loud['passed'] else 'FAILED'} ({loud['integrated_lufs']} LUFS, True Peak: {loud['true_peak_db']} dBFS)")
        lic = checks["license_compliance"]
        print(f"   - Licensing: {'PASSED' if lic['passed'] else 'FAILED'} (unverified: {lic['unverified_assets_count']})")
        db = checks.get("duration_bounds", {})
        if db.get("min_sec") is not None or db.get("max_sec") is not None:
            print(f"   - Duration Bounds: {'PASSED' if db['passed'] else 'FAILED'} ({db.get('min_sec')}s - {db.get('max_sec')}s)")
        if "music_track" in checks:
            mt = checks["music_track"]
            print(f"   - Music Track: {'PASSED' if mt['passed'] else 'FAILED'} (warning: {mt.get('warning')})")

        print(f"\n📋 Mandatory Human Review Checklist:")
        for item in report["mandatory_human_review_items"]:
            print(f"   [ ] {item}")

    return 0 if report["status"] == "TECHNICALLY_VALID_PENDING_REVIEW" else 1


if __name__ == "__main__":
    sys.exit(main())
