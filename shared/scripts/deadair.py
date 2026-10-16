#!/usr/bin/env python3
"""deadair.py - Generate an Edit Decision List (EDL) from a timestamped transcript.

Analyzes SRT, VTT, or Whisper JSON transcripts to detect:
- DEAD AIR: Silent gaps between spoken cues exceeding a configurable floor (default 0.45s).
            Pads edges to preserve natural breath boundaries.
- FILLER: Cues consisting purely of filler words ("um", "uh", "you know", "basically", etc.).
- REPEAT: False starts, restarted sentences, or second takes where speech was repeated.

DOES NOT modify media files directly. Produces an EDL and summary metrics for your video editor.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

# Try importing transcript loader from shared module, fallback to local implementation
try:
    from transcript import format_timestamp, load_transcript, normalize_tokens, parse_timestamp
except ImportError:
    try:
        from shared.scripts.transcript import format_timestamp, load_transcript, normalize_tokens, parse_timestamp
    except ImportError:
        def parse_timestamp(s: Any) -> float:
            if isinstance(s, (int, float)):
                return float(s)
            s = str(s).strip().replace(",", ".").split()[0]
            p = s.split(":")
            if len(p) == 3:
                return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2])
            elif len(p) == 2:
                return int(p[0]) * 60 + float(p[1])
            return float(p[0]) if p and p[0] else 0.0

        def format_timestamp(sec: float, fmt: str = "mmss") -> str:
            sec = max(0.0, float(sec))
            t = int(sec)
            ms = int(round((sec - t) * 1000))
            if ms >= 1000:
                t += 1
                ms = 0
            h, m, s = t // 3600, (t % 3600) // 60, t % 60
            if fmt == "srt":
                return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
            return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

        def normalize_tokens(t: str) -> List[str]:
            return re.findall(r"[\w']+", t.lower(), re.UNICODE)

        def load_transcript(path: str) -> List[Tuple[float, float, str]]:
            with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
                raw = f.read()
            if path.endswith(".json"):
                d = json.loads(raw)
                segs = d.get("segments", d if isinstance(d, list) else [])
                return [(float(s.get("start", 0)), float(s.get("end", 0)), (s.get("text") or "").strip()) for s in segs]
            cues = []
            cur = None
            for line in raw.splitlines():
                m = re.search(r"(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)", line)
                if m:
                    if cur:
                        cues.append(cur)
                    cur = [parse_timestamp(m.group(1)), parse_timestamp(m.group(2)), []]
                elif cur is not None and line.strip() and not line.strip().isdigit():
                    cur[2].append(line.strip())
            if cur:
                cues.append(cur)
            return [(a, b, " ".join(t)) for a, b, t in cues if t]


FILLER_REGEX = re.compile(
    r"^[\s,.-]*((um+|uh+|er+|ah+|so|okay|ok|right|yeah|like|anyway|basically|actually|"
    r"you know|i mean|let me see|hold on|matlab|yani|مطلب|یعنی)[\s,.-]*)+$",
    re.I | re.UNICODE
)


def is_filler_cue(text: str) -> bool:
    tokens = normalize_tokens(text)
    if not tokens:
        return True
    if FILLER_REGEX.match(text):
        return True
    filler_set = {"um", "uh", "er", "ah", "like", "basically", "actually", "matlab", "yani", "مطلب", "یعنی"}
    return len(tokens) <= 3 and all(t in filler_set for t in tokens)


def generate_edl(
    cues: List[Tuple[float, float, str]],
    floor: float = 0.45,
    min_cut_duration: float = 0.2
) -> List[Dict[str, Any]]:
    cuts: List[Dict[str, Any]] = []

    for i, (s, e, t) in enumerate(cues):
        # 1. Pure filler cue
        if is_filler_cue(t):
            cuts.append({
                "kind": "FILLER",
                "start": round(s, 3),
                "end": round(e, 3),
                "duration": round(e - s, 3),
                "reason": f"Filler cue: \"{t.strip()[:48]}\"",
                "confidence": "high",
            })

        # 2. Dead air gaps
        if i > 0:
            prev_end = cues[i - 1][1]
            gap = s - prev_end
            if gap > floor:
                # Keep margin at boundaries so breath sounds are not clipped unnaturally
                margin = min(0.12, floor / 3.0)
                cut_start = round(prev_end + margin, 3)
                cut_end = round(s - margin, 3)
                if cut_end - cut_start >= min_cut_duration:
                    cuts.append({
                        "kind": "DEAD",
                        "start": cut_start,
                        "end": cut_end,
                        "duration": round(cut_end - cut_start, 3),
                        "reason": f"Dead air pause ({gap:.2f}s gap)",
                        "confidence": "high",
                    })

        # 3. Restarts / retakes
        if t.strip() and not is_filler_cue(t):
            # Scan backwards to last substantive speech cue
            j = i - 1
            while j >= 0 and (is_filler_cue(cues[j][2]) or not cues[j][2].strip()):
                j -= 1
            if j >= 0:
                prev_tokens = normalize_tokens(cues[j][2])[:6]
                curr_tokens = normalize_tokens(t)[:6]
                if len(curr_tokens) >= 3 and prev_tokens[:3] == curr_tokens[:3]:
                    cuts.append({
                        "kind": "REPEAT",
                        "start": round(cues[j][0], 3),
                        "end": round(cues[j][1], 3),
                        "duration": round(cues[j][1] - cues[j][0], 3),
                        "reason": f"Sentence restart of \"{' '.join(curr_tokens[:4])}\"",
                        "confidence": "medium",
                    })

    # Filter out invalid or zero-duration cuts
    valid_cuts = [c for c in cuts if c["end"] > c["start"]]
    valid_cuts.sort(key=lambda c: c["start"])

    # Merge overlapping cuts
    merged_cuts: List[Dict[str, Any]] = []
    for c in valid_cuts:
        if not merged_cuts:
            merged_cuts.append(c)
            continue
        prev = merged_cuts[-1]
        if c["start"] <= prev["end"]:
            prev["end"] = max(prev["end"], c["end"])
            prev["duration"] = round(prev["end"] - prev["start"], 3)
            prev["reason"] = f"{prev['reason']} + {c['reason']}"
        else:
            merged_cuts.append(c)

    return merged_cuts


def main():
    parser = argparse.ArgumentParser(description="Create Edit Decision List from transcript.")
    parser.add_argument("file", help="Path to transcript (.srt, .vtt, .json)")
    parser.add_argument("--floor", type=float, default=0.45, help="Dead air threshold in seconds (default: 0.45)")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON EDL")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    try:
        cues = load_transcript(args.file)
    except Exception as e:
        print(f"Error loading transcript: {e}", file=sys.stderr)
        sys.exit(1)

    if not cues:
        print("No speech cues found in file.", file=sys.stderr)
        sys.exit(1)

    total_duration = cues[-1][1]
    cuts = generate_edl(cues, floor=args.floor)
    total_removed = sum(c["duration"] for c in cuts)
    output_duration = max(0.0, total_duration - total_removed)
    percent_removed = (total_removed / total_duration * 100) if total_duration > 0 else 0.0

    result = {
        "source": args.file,
        "input_duration_sec": round(total_duration, 2),
        "input_duration_fmt": format_timestamp(total_duration),
        "output_duration_sec": round(output_duration, 2),
        "output_duration_fmt": format_timestamp(output_duration),
        "total_cuts": len(cuts),
        "seconds_removed": round(total_removed, 2),
        "percent_trimmed": round(percent_removed, 1),
        "cuts": cuts,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print(f"\n  {args.file}")
    print(f"  Duration: {format_timestamp(total_duration)} ({total_duration:.2f}s) | Cues: {len(cues)} | Dead-air floor: {args.floor}s\n")
    for c in cuts:
        print(f"    {c['kind']:<7} {format_timestamp(c['start']):>8} -> {format_timestamp(c['end']):>8} ({c['duration']:5.2f}s)  {c['reason']}")
    print(f"\n  Summary: {len(cuts)} cuts, {total_removed:.2f}s removed -> {format_timestamp(output_duration)} out ({percent_removed:.1f}% tighter)\n")


if __name__ == "__main__":
    main()
