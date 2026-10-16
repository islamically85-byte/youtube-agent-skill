#!/usr/bin/env python3
"""transcript.py - Universal, zero-dependency transcript parser and utility.

Supports:
- SRT (.srt)
- WebVTT (.vtt)
- Whisper JSON (.json with 'segments' or top-level list of cues)
- WhisperX / YouTube TimedText JSON
- Plain text with optional manual timestamps

Features:
- Full Unicode preservation (Urdu, Arabic, Hindi, CJK, Latin, etc.)
- Robust timestamp parsing and formatting (SRT, VTT, MM:SS, HH:MM:SS)
- Language-aware word count and speech-duration estimates
- Clean cue cleaning (stripping VTT formatting tags like <c.voice>, <b>, etc.)
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

SPEECH_RATES_WPM = {
    "en": 150.0,
    "ur": 130.0,  # Urdu spoken cadence
    "hi": 130.0,  # Hindi spoken cadence
    "es": 160.0,  # Spanish
    "fr": 150.0,  # French
    "ar": 125.0,  # Arabic
    "de": 135.0,  # German
    "default": 140.0,
}

TAG_CLEANER = re.compile(r"<[^>]+>")


def parse_timestamp(s: Any) -> float:
    """Convert string or numeric timestamp to float seconds."""
    if isinstance(s, (int, float)):
        return float(s)
    if not isinstance(s, str):
        return 0.0

    s = s.strip().replace(",", ".")
    # Remove any extra VTT positioning tokens (e.g. line:0% position:50%)
    s = s.split()[0]

    parts = s.split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 1 and parts[0]:
            return float(parts[0])
    except ValueError:
        pass
    return 0.0


def format_timestamp(seconds: float, fmt: str = "mmss") -> str:
    """Format seconds into HH:MM:SS, MM:SS, or SRT/VTT format."""
    seconds = max(0.0, float(seconds))
    total_sec = int(seconds)
    ms = int(round((seconds - total_sec) * 1000))
    if ms >= 1000:
        total_sec += 1
        ms = 0

    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    s = total_sec % 60

    if fmt == "srt":
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    elif fmt == "vtt":
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
    elif fmt == "hms":
        return f"{h:02d}:{m:02d}:{s:02d}"
    else:  # mmss
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m}:{s:02d}"


def normalize_tokens(text: str) -> List[str]:
    """Tokenize words preserving Unicode letters in any language (Urdu, Arabic, etc.)."""
    # \w in Python 3 re matches Unicode word characters (letters, numbers in any script)
    tokens = re.findall(r"[\w']+", text.lower(), re.UNICODE)
    return tokens


def count_words(text: str) -> int:
    """Count words in text accurately across multilingual inputs."""
    return len(normalize_tokens(text))


def estimate_speech_duration(text: str, language: str = "en") -> float:
    """Estimate spoken duration in seconds based on language cadence."""
    wpm = SPEECH_RATES_WPM.get(language.lower(), SPEECH_RATES_WPM["default"])
    words = count_words(text)
    if words == 0:
        return 0.0
    return round((words / wpm) * 60.0, 2)


def clean_text(text: str) -> str:
    """Clean subtitle tags and normalize spacing."""
    no_tags = TAG_CLEANER.sub("", text)
    return re.sub(r"\s+", " ", no_tags).strip()


def parse_srt_or_vtt(content: str) -> List[Tuple[float, float, str]]:
    """Parse SRT or WebVTT content into list of (start_sec, end_sec, text)."""
    lines = content.splitlines()
    cues: List[Tuple[float, float, str]] = []
    cur_start: Optional[float] = None
    cur_end: Optional[float] = None
    cur_text: List[str] = []

    time_pattern = re.compile(
        r"^\s*(\d{1,2}:)?\d{1,2}:\d{1,2}[.,]\d{1,3}\s*-->\s*(\d{1,2}:)?\d{1,2}:\d{1,2}[.,]\d{1,3}"
    )

    for line in lines:
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("WEBVTT") or line_clean.startswith("NOTE"):
            if cur_start is not None and cur_end is not None and cur_text:
                full_text = clean_text(" ".join(cur_text))
                if full_text:
                    cues.append((cur_start, cur_end, full_text))
                cur_start, cur_end, cur_text = None, None, []
            continue

        m = time_pattern.search(line_clean)
        if m:
            if cur_start is not None and cur_end is not None and cur_text:
                full_text = clean_text(" ".join(cur_text))
                if full_text:
                    cues.append((cur_start, cur_end, full_text))
            parts = line_clean.split("-->")
            cur_start = parse_timestamp(parts[0])
            cur_end = parse_timestamp(parts[1])
            cur_text = []
        elif cur_start is not None and not line_clean.isdigit():
            cur_text.append(line_clean)

    if cur_start is not None and cur_end is not None and cur_text:
        full_text = clean_text(" ".join(cur_text))
        if full_text:
            cues.append((cur_start, cur_end, full_text))

    return cues


def parse_json_transcript(data: Any) -> List[Tuple[float, float, str]]:
    """Parse Whisper or timed-text JSON into list of (start, end, text)."""
    cues: List[Tuple[float, float, str]] = []
    if isinstance(data, dict):
        segments = data.get("segments") or data.get("events") or data.get("items") or []
    elif isinstance(data, list):
        segments = data
    else:
        return []

    for seg in segments:
        if not isinstance(seg, dict):
            continue

        if "start" in seg:
            start = parse_timestamp(seg["start"])
        elif "tStartMs" in seg:
            start = parse_timestamp(seg["tStartMs"] / 1000.0)
        else:
            start = 0.0

        if "end" in seg:
            end = parse_timestamp(seg["end"])
        elif "dDurationMs" in seg:
            end = start + parse_timestamp(seg["dDurationMs"] / 1000.0)
        else:
            end = start
        
        # Whisper / standard text
        text = seg.get("text") or ""
        # YouTube timedtext events
        if not text and "segs" in seg:
            text = "".join(s.get("utf8", "") for s in seg["segs"] if isinstance(s, dict))
        
        text = clean_text(text)
        if text:
            cues.append((round(start, 3), round(end, 3), text))
            
    return cues


def load_transcript(path: str) -> List[Tuple[float, float, str]]:
    """Universal loader for subtitle and transcript files."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Transcript file not found: {path}")

    raw = ""
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                raw = f.read()
            break
        except UnicodeDecodeError:
            continue

    if path.endswith(".json"):
        try:
            parsed_json = json.loads(raw)
            return parse_json_transcript(parsed_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON transcript in {path}: {e}")

    # Fallback / try JSON if file contents start with { or [
    stripped = raw.strip()
    if (stripped.startswith("{") and stripped.endswith("}")) or (stripped.startswith("[") and stripped.endswith("]")):
        try:
            parsed_json = json.loads(raw)
            return parse_json_transcript(parsed_json)
        except Exception:
            pass

    return parse_srt_or_vtt(raw)


def extract_full_text(cues: List[Tuple[float, float, str]]) -> str:
    """Combine cues into a single text string."""
    return " ".join(c[2] for c in cues).strip()


def main():
    parser = argparse.ArgumentParser(description="Universal transcript parsing and timing utility.")
    parser.add_argument("file", help="Path to .srt, .vtt, or Whisper .json file")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    parser.add_argument("--language", default="en", help="Language code for timing estimates (en, ur, hi, etc.)")
    args = parser.parse_args()

    try:
        cues = load_transcript(args.file)
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error loading transcript: {e}", file=sys.stderr)
        sys.exit(1)

    total_duration = cues[-1][1] if cues else 0.0
    text = extract_full_text(cues)
    words = count_words(text)
    est_duration = estimate_speech_duration(text, args.language)

    result = {
        "source": args.file,
        "cue_count": len(cues),
        "duration_seconds": round(total_duration, 2),
        "duration_formatted": format_timestamp(total_duration),
        "word_count": words,
        "estimated_speech_duration_sec": est_duration,
        "cues": [{"start": c[0], "end": c[1], "start_fmt": format_timestamp(c[0]), "end_fmt": format_timestamp(c[1]), "text": c[2]} for c in cues],
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n  File: {args.file}")
        print(f"  Cues: {len(cues)} | Duration: {format_timestamp(total_duration)} ({total_duration:.2f}s)")
        print(f"  Words: {words} | Est. spoken duration ({args.language}): {format_timestamp(est_duration)}\n")
        for c in cues[:10]:
            print(f"    [{format_timestamp(c[0])} -> {format_timestamp(c[1])}] {c[2]}")
        if len(cues) > 10:
            print(f"    ... and {len(cues) - 10} more cues.")
        print()


if __name__ == "__main__":
    main()
