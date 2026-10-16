#!/usr/bin/env python3
"""validate_manifest.py - Validate YouTube project manifest and licensing provenance.

Ensures that all video/audio assets comply with free-first production rules:
1. Zero-credit quota compliance (credit_budget <= 0).
2. Permissive licensing provenance (Pexels, Pixabay, Mixkit, CC0, Creator-owned, or procedural test).
3. Non-empty required metadata, valid aspect ratio, and proper timeline ranges.
4. Optional filesystem existence check for all referenced local files (--check-files or --strict).
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

VALID_SOURCE_TYPES = {"local", "pexels", "pixabay", "mixkit", "creator_owned", "procedural_test"}
VALID_LICENSE_CLASSES = {
    "Pexels License",
    "Pixabay License",
    "Mixkit Free License",
    "Creative Commons CC0",
    "Creator Owned",
    "MIT Procedural Test"
}
VALID_ASPECT_RATIOS = {"16:9", "9:16", "1:1"}
VALID_LANGUAGES = {"ur", "en", "hi", "other"}


def validate_manifest_data(
    data: Dict[str, Any],
    check_files: bool = False,
    base_dir: Optional[str] = None
) -> Tuple[bool, List[str], List[str]]:
    """Validate manifest dictionary against schema rules.
    
    Returns (is_valid, errors, warnings).
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(data, dict):
        return False, ["Manifest root must be a JSON object."], []

    # Required top-level fields
    for field in ["project_id", "title", "target_duration_sec", "footage_clips", "audio", "render_target"]:
        if field not in data:
            errors.append(f"Missing mandatory top-level field: '{field}'")

    project_id = data.get("project_id", "")
    if not isinstance(project_id, str) or not project_id.strip():
        errors.append("Field 'project_id' must be a non-empty string.")

    target_duration = data.get("target_duration_sec")
    if not isinstance(target_duration, (int, float)) or target_duration <= 0:
        errors.append("Field 'target_duration_sec' must be a positive number.")

    aspect_ratio = data.get("aspect_ratio", "16:9")
    if aspect_ratio not in VALID_ASPECT_RATIOS:
        errors.append(f"Field 'aspect_ratio' '{aspect_ratio}' is invalid. Allowed: {sorted(VALID_ASPECT_RATIOS)}")

    # Credit budget rule: default and maximum must be <= 0 for free-first production
    credit_budget = data.get("credit_budget", 0)
    if not isinstance(credit_budget, (int, float)):
        errors.append("Field 'credit_budget' must be a numeric value.")
    elif credit_budget > 0:
        errors.append(
            f"Credit budget violation: credit_budget is {credit_budget}, but free-first policy requires <= 0. "
            "Paid credits (e.g. vidIQ / paid APIs) cannot be budgeted automatically."
        )

    # Validate footage_clips
    clips = data.get("footage_clips")
    total_clip_timeline_duration = 0.0
    if not isinstance(clips, list) or len(clips) == 0:
        errors.append("Field 'footage_clips' must be a non-empty list of clip objects.")
    else:
        for idx, clip in enumerate(clips):
            c_label = f"footage_clips[{idx}]"
            if not isinstance(clip, dict):
                errors.append(f"{c_label} must be an object.")
                continue

            for req in ["id", "source_type", "source_url_or_path", "license_class", "license_verified_date", "clip_duration_sec", "timeline_in_sec", "timeline_out_sec"]:
                if req not in clip:
                    errors.append(f"{c_label} missing required field '{req}'")

            source_type = clip.get("source_type")
            if source_type not in VALID_SOURCE_TYPES:
                errors.append(f"{c_label} invalid source_type '{source_type}'. Allowed: {sorted(VALID_SOURCE_TYPES)}")

            license_class = clip.get("license_class")
            if license_class not in VALID_LICENSE_CLASSES:
                errors.append(f"{c_label} unrecognized license_class '{license_class}'. Allowed: {sorted(VALID_LICENSE_CLASSES)}")

            t_in = clip.get("timeline_in_sec", 0.0)
            t_out = clip.get("timeline_out_sec", 0.0)
            clip_dur = clip.get("clip_duration_sec", 0.0)

            if isinstance(t_in, (int, float)) and isinstance(t_out, (int, float)):
                if t_out <= t_in:
                    errors.append(f"{c_label} timeline_out_sec ({t_out}) must be greater than timeline_in_sec ({t_in}).")
                else:
                    duration_on_timeline = t_out - t_in
                    total_clip_timeline_duration += duration_on_timeline
                    if isinstance(clip_dur, (int, float)) and clip_dur < duration_on_timeline and source_type != "procedural_test":
                        warnings.append(
                            f"{c_label} clip_duration_sec ({clip_dur}s) is shorter than timeline duration ({duration_on_timeline}s)."
                        )

            # Check file existence if requested and source is local
            src = clip.get("source_url_or_path", "")
            if check_files and (source_type in {"local", "creator_owned"} or os.path.exists(src)):
                check_path = os.path.join(base_dir, src) if base_dir and not os.path.isabs(src) else src
                if not os.path.exists(check_path):
                    errors.append(f"{c_label} file not found at '{check_path}'.")

    # Check total footage coverage against target_duration_sec
    if isinstance(target_duration, (int, float)) and total_clip_timeline_duration > 0:
        if abs(total_clip_timeline_duration - target_duration) > 0.5:
            warnings.append(
                f"Footage timeline sum ({total_clip_timeline_duration:.1f}s) differs from target_duration_sec ({target_duration:.1f}s)."
            )

    # Validate audio
    audio = data.get("audio")
    if not isinstance(audio, dict):
        errors.append("Field 'audio' must be an object.")
    else:
        narration = audio.get("narration")
        if not isinstance(narration, dict):
            errors.append("Field 'audio.narration' must be an object.")
        else:
            narr_path = narration.get("file_path", "")
            if not isinstance(narr_path, str) or not narr_path.strip():
                errors.append("Field 'audio.narration.file_path' must be specified.")
            elif check_files:
                check_path = os.path.join(base_dir, narr_path) if base_dir and not os.path.isabs(narr_path) else narr_path
                if not os.path.exists(check_path):
                    errors.append(f"Narration audio file not found: '{check_path}'")

            lang = narration.get("language")
            if lang not in VALID_LANGUAGES:
                errors.append(f"Field 'audio.narration.language' '{lang}' is invalid. Allowed: {sorted(VALID_LANGUAGES)}")

        bg_music = audio.get("background_music")
        if isinstance(bg_music, dict):
            bg_path = bg_music.get("file_path", "")
            if bg_path and check_files:
                check_path = os.path.join(base_dir, bg_path) if base_dir and not os.path.isabs(bg_path) else bg_path
                if not os.path.exists(check_path):
                    errors.append(f"Background music file not found: '{check_path}'")

    # Validate graphics and subtitles (optional)
    graphics = data.get("graphics_and_subtitles")
    if isinstance(graphics, dict):
        sub_file = graphics.get("subtitles_file")
        if sub_file and check_files:
            check_path = os.path.join(base_dir, sub_file) if base_dir and not os.path.isabs(sub_file) else sub_file
            if not os.path.exists(check_path):
                errors.append(f"Subtitles file not found: '{check_path}'")

    # Validate render_target
    render = data.get("render_target")
    if not isinstance(render, dict):
        errors.append("Field 'render_target' must be an object.")
    else:
        out_path = render.get("output_path", "")
        if not isinstance(out_path, str) or not out_path.strip():
            errors.append("Field 'render_target.output_path' must be a non-empty string.")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate YouTube Project Manifest & Licensing Provenance.")
    parser.add_argument("--manifest", "-m", required=True, help="Path to project manifest JSON file.")
    parser.add_argument("--check-files", action="store_true", help="Verify referenced local files exist on disk.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors and enable file checking.")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")
    args = parser.parse_args()

    manifest_path = os.path.abspath(args.manifest)
    if not os.path.exists(manifest_path):
        err_msg = f"Manifest file not found: {manifest_path}"
        if args.json:
            print(json.dumps({"valid": False, "errors": [err_msg], "warnings": []}))
        else:
            print(f"ERROR: {err_msg}", file=sys.stderr)
        return 1

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        err_msg = f"Failed to parse manifest JSON: {e}"
        if args.json:
            print(json.dumps({"valid": False, "errors": [err_msg], "warnings": []}))
        else:
            print(f"ERROR: {err_msg}", file=sys.stderr)
        return 1

    base_dir = os.path.dirname(manifest_path)
    check_files = args.check_files or args.strict
    is_valid, errors, warnings = validate_manifest_data(data, check_files=check_files, base_dir=base_dir)

    if args.strict and warnings:
        is_valid = False
        errors.extend([f"Strict mode failure: {w}" for w in warnings])

    result = {
        "valid": is_valid,
        "manifest_path": manifest_path,
        "errors": errors,
        "warnings": warnings,
        "clip_count": len(data.get("footage_clips", [])) if isinstance(data, dict) else 0,
        "credit_budget": data.get("credit_budget", 0) if isinstance(data, dict) else 0
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if is_valid:
            print(f"✅ Manifest '{os.path.basename(manifest_path)}' is VALID.")
            print(f"   Clips: {result['clip_count']}, Credit budget: {result['credit_budget']}")
            if warnings:
                print("   Warnings:")
                for w in warnings:
                    print(f"     ⚠️ {w}")
        else:
            print(f"❌ Manifest '{os.path.basename(manifest_path)}' is INVALID.", file=sys.stderr)
            for err in errors:
                print(f"   - {err}", file=sys.stderr)
            if warnings:
                for w in warnings:
                    print(f"   ⚠️ {w}", file=sys.stderr)

    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
