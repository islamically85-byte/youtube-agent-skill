#!/usr/bin/env python3
"""swipe.py - Rank collected competitor videos by multiple over each channel's OWN median.

Raw view counts rank channel subscriber size, not idea potency. A 400K video on a 2M-subscriber
channel is an ordinary upload; a 400K video on a channel whose median is 25K represents a true
niche outlier worth studying.

Features:
- Robust number parsing (handles '45.2K', '1.2M', commas, strings, ints)
- Computes channel baseline median (requires >= 4 videos per channel to avoid noise)
- Identifies hook formula on the title using the 21 hook patterns
- Formats structured JSON or human-readable outlier leaderboard
"""

import argparse
import json
import os
import re
import statistics
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    from hookscore import FORMULAS
except ImportError:
    try:
        from shared.scripts.hookscore import FORMULAS
    except ImportError:
        FORMULAS = []


def parse_views_count(val: Any) -> float:
    """Robustly parse view strings like '45.2K', '1.2M', '150,000' or raw ints."""
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return max(0.0, float(val))

    s = str(val).strip().replace(",", "").upper()
    multiplier = 1.0
    if s.endswith("K"):
        multiplier = 1000.0
        s = s[:-1]
    elif s.endswith("M"):
        multiplier = 1000000.0
        s = s[:-1]
    elif s.endswith("B"):
        multiplier = 1000000000.0
        s = s[:-1]

    try:
        return max(0.0, float(s) * multiplier)
    except ValueError:
        return 0.0


def classify_title(title: str) -> str:
    if not FORMULAS:
        return "Unclassified"
    scored = []
    for f in FORMULAS:
        matches = sum(1 for p in f.get("match", []) if re.search(p, title, re.I))
        if matches:
            scored.append((matches, f.get("name", "Unclassified")))
    scored.sort(reverse=True)
    return scored[0][1] if scored else "Unclassified"


def analyze_outliers(
    videos: List[Dict[str, Any]],
    min_multiple: float = 1.5,
    min_channel_samples: int = 4
) -> Dict[str, Any]:
    channels: Dict[str, List[Dict[str, Any]]] = {}
    for v in videos:
        ch = v.get("channel") or v.get("channel_title") or "Unknown Channel"
        channels.setdefault(ch, []).append(v)

    outliers: List[Dict[str, Any]] = []
    thin_channels: List[Dict[str, Any]] = []

    for ch, vids in channels.items():
        views_list = [parse_views_count(v.get("views")) for v in vids]
        if len(vids) < min_channel_samples:
            thin_channels.append({
                "channel": ch,
                "samples": len(vids),
                "reason": f"Fewer than {min_channel_samples} videos collected; median is unreliable.",
            })
            continue

        median_views = statistics.median(views_list) if views_list else 0.0

        for v in vids:
            v_views = parse_views_count(v.get("views"))
            multiple = round(v_views / median_views, 2) if median_views > 0 else 0.0
            if multiple >= min_multiple:
                outliers.append({
                    "channel": ch,
                    "title": v.get("title", ""),
                    "views": int(v_views),
                    "channel_median": int(median_views),
                    "multiple": multiple,
                    "formula": classify_title(v.get("title", "")),
                    "url": v.get("url", ""),
                })

    outliers.sort(key=lambda x: -x["multiple"])

    # Tally formulas across outliers
    formula_counts: Dict[str, int] = {}
    for o in outliers:
        f = o["formula"]
        formula_counts[f] = formula_counts.get(f, 0) + 1

    return {
        "total_videos_analyzed": len(videos),
        "total_channels": len(channels),
        "threshold_multiple": min_multiple,
        "outlier_count": len(outliers),
        "outliers": outliers,
        "thin_channels_skipped": thin_channels,
        "formula_distribution": dict(sorted(formula_counts.items(), key=lambda x: -x[1])),
    }


def main():
    parser = argparse.ArgumentParser(description="Rank YouTube competitor videos by multiple over channel median.")
    parser.add_argument("file", help="Path to JSON file containing list of videos")
    parser.add_argument("--min", type=float, default=1.5, help="Minimum multiple over median (default: 1.5x)")
    parser.add_argument("--samples", type=int, default=4, help="Minimum videos required per channel (default: 4)")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        if isinstance(data, dict):
            videos = data.get("videos") or data.get("items") or []
        elif isinstance(data, list):
            videos = data
        else:
            videos = []
    except Exception as e:
        print(f"Error parsing JSON file: {e}", file=sys.stderr)
        sys.exit(1)

    res = analyze_outliers(videos, min_multiple=args.min, min_channel_samples=args.samples)

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    print(f"\n  Analyzed: {res['total_videos_analyzed']} videos across {res['total_channels']} channels")
    print(f"  Outliers meeting >= {res['threshold_multiple']}x channel median: {res['outlier_count']}\n")

    for r in res["outliers"][:25]:
        ch_str = r["channel"][:20]
        title_str = r["title"][:50]
        print(f"    {r['multiple']:5.2f}x  {r['views']:>10,} views (vs {r['channel_median']:>9,} median)  [{ch_str:<20}] {title_str}")
        print(f"            Formula: {r['formula']}")

    if not res["outliers"]:
        print("    No videos exceeded the outlier multiple threshold. Collect more videos or lower --min.")

    if res["thin_channels_skipped"]:
        print(f"\n  Note: Skipped {len(res['thin_channels_skipped'])} channel(s) with < {args.samples} videos:")
        for tc in res["thin_channels_skipped"][:5]:
            print(f"    - {tc['channel']} ({tc['samples']} uploads)")

    if res["formula_distribution"]:
        print("\n  Top Hook Formulas Among Outliers:")
        for form, count in res["formula_distribution"].items():
            print(f"    {count:2d}x  {form}")
    print()


if __name__ == "__main__":
    main()
