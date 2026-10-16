#!/usr/bin/env python3
"""chapters.py - Generate and validate YouTube chapters from timestamped transcripts or text blocks.

Enforces YouTube's platform chapter rules:
1. First chapter must begin at 00:00 (or 0:00).
2. Must contain at least 3 chapters.
3. Each chapter must be at least 10 seconds long.
4. Timestamps must be in ascending chronological order.

Can:
- Generate draft chapters from an SRT, VTT, or Whisper JSON file.
- Validate an existing chapter text block copied from a YouTube description.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

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
            h, m, s = t // 3600, (t % 3600) // 60, t % 60
            return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

        def normalize_tokens(t: str) -> List[str]:
            return re.findall(r"[\w']+", t.lower(), re.UNICODE)

        def load_transcript(path: str) -> List[Tuple[float, float, str]]:
            with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
                raw = f.read()
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


STOP_WORDS = set(
    "the a an of for to in on and or is are was were be been with this that it as at by from "
    "you your i my we our they them he she but so if then than there here what which who how "
    "when where why not no yes do does did just really very like about into over out up down "
    "can could will would should have has had get got make made go going went one two also".split()
)


def extract_keywords(text: str) -> List[str]:
    tokens = normalize_tokens(text)
    return [w for w in tokens if len(w) >= 4 and w not in STOP_WORDS]


def validate_chapter_list(chapters: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Validate chapters against YouTube platform constraints."""
    errors = []
    if not chapters:
        return False, ["Chapter list is empty."]

    # Rule 1: Starts at 00:00
    if chapters[0]["seconds"] != 0.0:
        errors.append(f"First chapter must start at 00:00 (starts at {chapters[0].get('timestamp', chapters[0]['seconds'])}).")

    # Rule 2: Minimum 3 chapters
    if len(chapters) < 3:
        errors.append(f"YouTube requires at least 3 chapters (found {len(chapters)}).")

    # Rule 3 & 4: Chronological and >= 10 seconds each
    for i in range(len(chapters)):
        sec = chapters[i]["seconds"]
        if i > 0 and sec <= chapters[i - 1]["seconds"]:
            errors.append(f"Chapter '{chapters[i]['title']}' timestamp ({chapters[i].get('timestamp')}) is not strictly after previous chapter.")

        dur = chapters[i].get("duration")
        if dur is not None and dur < 10.0:
            errors.append(f"Chapter '{chapters[i]['title']}' duration ({dur:.1f}s) is shorter than YouTube's 10-second minimum.")

    return len(errors) == 0, errors


def parse_raw_chapter_text(text: str) -> List[Dict[str, Any]]:
    """Parse pasted YouTube chapter text (e.g., '01:23 Introduction')."""
    lines = text.strip().splitlines()
    parsed = []
    ts_pattern = re.compile(r"(\d{1,2}:)?\d{1,2}:\d{2}")

    for line in lines:
        line_clean = line.strip()
        m = ts_pattern.search(line_clean)
        if m:
            ts_str = m.group(0)
            sec = parse_timestamp(ts_str)
            title = line_clean.replace(ts_str, "").strip(" -:–|")
            parsed.append({
                "timestamp": ts_str,
                "seconds": round(sec, 2),
                "title": title or "Untitled Section",
            })

    parsed.sort(key=lambda c: c["seconds"])
    for i in range(len(parsed)):
        if i + 1 < len(parsed):
            parsed[i]["duration"] = round(parsed[i + 1]["seconds"] - parsed[i]["seconds"], 2)
        else:
            parsed[i]["duration"] = None

    return parsed


def generate_chapters(cues: List[Tuple[float, float, str]], target: int = 7) -> List[Dict[str, Any]]:
    if not cues:
        return []
    total_dur = cues[-1][1]
    if len(cues) < 6 or total_dur < 30.0:
        return [
            {"seconds": 0.0, "timestamp": "0:00", "title": "Introduction", "duration": round(total_dur, 2)}
        ]

    # Score boundaries by pause duration and vocabulary shift
    candidates = []
    for i in range(1, len(cues)):
        gap = cues[i][0] - cues[i - 1][1]
        before_text = " ".join(c[2] for c in cues[max(0, i - 12):i])
        after_text = " ".join(c[2] for c in cues[i:min(len(cues), i + 12)])
        kb = set(extract_keywords(before_text))
        ka = set(extract_keywords(after_text))
        shift = 1.0 - (len(kb & ka) / len(kb | ka)) if (kb | ka) else 0.0
        score = (gap * 1.5) + (shift * 3.0)
        candidates.append((score, cues[i][0], i))

    candidates.sort(reverse=True, key=lambda x: x[0])

    picked = [0.0]
    min_dist = 12.0  # Safe minimum spacing between chapters

    for _, t, _ in candidates:
        if len(picked) >= target:
            break
        if all(abs(t - p) >= min_dist for p in picked) and (total_dur - t) >= min_dist:
            picked.append(t)

    picked.sort()

    chapters = []
    for n, t in enumerate(picked):
        end_t = picked[n + 1] if n + 1 < len(picked) else total_dur
        span_text = " ".join(c[2] for c in cues if c[0] >= t and c[1] <= end_t)
        kw = extract_keywords(span_text)
        kw_freq: Dict[str, int] = {}
        for w in kw:
            kw_freq[w] = kw_freq.get(w, 0) + 1
        sorted_kw = sorted(kw_freq.items(), key=lambda x: -x[1])
        top_words = [w.capitalize() for w, _ in sorted_kw[:3]]

        title = " ".join(top_words) if top_words else (f"Part {n + 1}" if n > 0 else "Introduction")
        chapters.append({
            "seconds": round(t, 2),
            "timestamp": format_timestamp(t),
            "title": title,
            "duration": round(end_t - t, 2),
        })

    return chapters


def main():
    parser = argparse.ArgumentParser(description="Generate and validate YouTube chapters.")
    parser.add_argument("file", nargs="?", help="Transcript file (.srt, .vtt, .json) or text file with chapters")
    parser.add_argument("--validate", help="Validate pasted chapter text directly")
    parser.add_argument("--target", type=int, default=7, help="Target number of chapters (default: 7)")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    if args.validate:
        chapters = parse_raw_chapter_text(args.validate)
        is_valid, errors = validate_chapter_list(chapters)
        res = {"valid": is_valid, "errors": errors, "chapters": chapters}
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print("\n  Chapter Validation:")
            print(f"  Valid: {is_valid}")
            for c in chapters:
                dur_str = f"({c['duration']:.1f}s)" if c.get("duration") else ""
                print(f"    {c['timestamp']} {c['title']} {dur_str}")
            if errors:
                print("\n  Errors detected:")
                for e in errors:
                    print(f"    - {e}")
            print()
        sys.exit(0 if is_valid else 1)

    if not args.file or not os.path.exists(args.file):
        parser.print_help()
        sys.exit(1)

    # Check if input is transcript or raw text list
    if args.file.endswith((".srt", ".vtt", ".json")):
        cues = load_transcript(args.file)
        chapters = generate_chapters(cues, target=args.target)
    else:
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        chapters = parse_raw_chapter_text(content)

    is_valid, errors = validate_chapter_list(chapters)
    result = {
        "source": args.file,
        "valid": is_valid,
        "chapter_count": len(chapters),
        "errors": errors,
        "chapters": chapters,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print("\n  YouTube Chapters:\n")
    for c in chapters:
        print(f"  {c['timestamp']} {c['title']}")

    print(f"\n  Total chapters: {len(chapters)}")
    if is_valid:
        print("  [OK] Valid for YouTube video description.")
    else:
        print("  [INVALID] Chapter block breaks YouTube rules:")
        for err in errors:
            print(f"    - {err}")
    print("  Note: Retitle topic keywords into audience-facing chapter titles before publishing.\n")


if __name__ == "__main__":
    main()
