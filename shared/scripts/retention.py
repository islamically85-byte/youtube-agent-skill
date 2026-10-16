#!/usr/bin/env python3
"""retention.py - Analyze YouTube Studio audience-retention exports to locate audience leaks.

Reports three distinct structural retention phenomena:
1. HOOK LEAK: Viewers lost during the opening 30 seconds (or first 10% on percent axes).
              Healthy: < 25% loss. Leaking: 25-40%. Severe: > 40%.
2. CLIFFS: Abrupt steep drops (> 0.8% drop across a single data step) representing
           specific moments viewers dropped off.
3. SLIDE: Steady audience attrition rate across the middle section (indicates pacing).

Supports:
- Varying CSV header names and column orders
- Percentages as strings ('78.5%'), floats (78.5), or decimal fractions (0.785)
- Retention > 100% (rewatches / loops on Shorts or detailed visual moments)
- Transcript cue alignment via `--transcript` to pinpoint spoken dialogue at drop moments
"""

import argparse
import csv
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    from transcript import format_timestamp, load_transcript
except ImportError:
    try:
        from shared.scripts.transcript import format_timestamp, load_transcript
    except ImportError:
        def format_timestamp(sec: float, fmt: str = "mmss") -> str:
            sec = max(0.0, float(sec))
            t = int(sec)
            h, m, s = t // 3600, (t % 3600) // 60, t % 60
            return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

        def load_transcript(path: str) -> List[Tuple[float, float, str]]:
            return []


def parse_cell_number(cell: str) -> Optional[float]:
    """Parse string cell into float, handling %, commas, and fractions."""
    clean = cell.strip().replace("%", "").replace(",", "")
    if not clean:
        return None
    try:
        val = float(clean)
        return val
    except ValueError:
        return None


def load_retention_csv(path: str) -> List[Tuple[float, float]]:
    """Robustly load retention CSV handling varied column layouts and encodings."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Retention file not found: {path}")

    raw_lines = []
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(path, newline="", encoding=enc) as fh:
                reader = csv.reader(fh)
                raw_lines = list(reader)
            break
        except UnicodeDecodeError:
            continue

    if not raw_lines:
        return []

    data_points: List[Tuple[float, float]] = []

    # Detect header and identify best columns
    time_col_idx = 0
    ret_col_idx = 1

    first_row = raw_lines[0]
    has_header = False
    for idx, col in enumerate(first_row):
        col_lower = col.lower()
        if any(k in col_lower for k in ("time", "position", "sec", "progress")):
            time_col_idx = idx
            has_header = True
        elif any(k in col_lower for k in ("retention", "watch", "percent", "viewers")):
            ret_col_idx = idx
            has_header = True

    start_idx = 1 if has_header else 0

    fraction_count = 0
    total_valid = 0

    for r in raw_lines[start_idx:]:
        if not r:
            continue
        # Extract numeric columns
        nums = [(i, parse_cell_number(c)) for i, c in enumerate(r) if parse_cell_number(c) is not None]
        if len(nums) < 2:
            continue

        # Use header indices if valid, else pick first two numeric columns
        val_time = None
        val_ret = None
        for i, val in nums:
            if i == time_col_idx and val_time is None:
                val_time = val
            elif i == ret_col_idx and val_ret is None:
                val_ret = val

        if val_time is None or val_ret is None:
            val_time = nums[0][1]
            val_ret = nums[1][1]

        if val_time is not None and val_ret is not None:
            if 0.0 < val_ret <= 1.0:
                fraction_count += 1
            total_valid += 1
            data_points.append((val_time, val_ret))

    # Normalize decimal fractions (0.85 -> 85.0) if whole column was decimal fractions
    if total_valid > 0 and (fraction_count / total_valid) > 0.8:
        data_points = [(t, r * 100.0) for t, r in data_points]

    data_points.sort(key=lambda p: p[0])
    return data_points


def analyze_retention(
    rows: List[Tuple[float, float]],
    duration: Optional[float] = None,
    transcript_path: Optional[str] = None
) -> Dict[str, Any]:
    if len(rows) < 4:
        raise ValueError(f"Insufficient retention data points ({len(rows)} points found, minimum 4 required).")

    xs = [r[0] for r in rows]
    ys = [r[1] for r in rows]

    is_percent_axis = max(xs) <= 100.5
    total_duration = duration if duration else (max(xs) if not is_percent_axis else None)

    def to_seconds(x: float) -> Optional[float]:
        if not is_percent_axis:
            return x
        if total_duration:
            return (x / 100.0) * total_duration
        return None

    start_val = ys[0]
    end_val = ys[-1]

    # Hook cutoff: first 30s or first 10%
    if is_percent_axis:
        hook_cutoff = (30.0 / total_duration * 100.0) if total_duration else 10.0
    else:
        hook_cutoff = 30.0

    hook_end_val = min((y for x, y in rows if x <= hook_cutoff), default=start_val)
    hook_leak = max(0.0, start_val - hook_end_val)

    # Detect cliffs (drops)
    drops = []
    for i in range(1, len(rows)):
        x_prev, y_prev = rows[i - 1]
        x_curr, y_curr = rows[i]
        span = abs(x_curr - x_prev)
        if span == 0.0:
            span = 1.0
        drop_val = y_prev - y_curr
        drops.append({
            "from_x": round(x_prev, 2),
            "to_x": round(x_curr, 2),
            "drop": round(drop_val, 2),
            "rate": round(drop_val / span, 3),
            "sec": round(to_seconds(x_prev), 1) if to_seconds(x_prev) is not None else None,
        })

    # Sort cliffs by steepest drop
    cliffs = [d for d in drops if d["drop"] >= 0.8]
    cliffs.sort(key=lambda d: -d["drop"])
    top_cliffs = cliffs[:5]

    # Calculate middle slide
    mid_drops = [d["drop"] for d in drops if d["from_x"] > hook_cutoff]
    slide_per_point = round(sum(mid_drops) / len(mid_drops), 3) if mid_drops else 0.0

    # Align with transcript if supplied
    spoken_dialogue = {}
    if transcript_path and os.path.exists(transcript_path):
        try:
            cues = load_transcript(transcript_path)
            for c in top_cliffs:
                t_sec = c["sec"]
                if t_sec is not None:
                    # Find cues within +/- 4 seconds
                    near = [q[2] for q in cues if q[0] <= t_sec + 4.0 and q[1] >= t_sec - 4.0]
                    spoken_dialogue[str(c["from_x"])] = " ".join(near)[:140]
        except Exception:
            pass

    verdict = "healthy" if hook_leak < 25.0 else ("leaking" if hook_leak < 40.0 else "severe")

    return {
        "data_points": len(rows),
        "axis_type": "percent" if is_percent_axis else "seconds",
        "video_duration_sec": total_duration,
        "start_retention": round(start_val, 1),
        "end_retention": round(end_val, 1),
        "hook_leak": round(hook_leak, 1),
        "hook_verdict": verdict,
        "slide_rate": slide_per_point,
        "cliffs": top_cliffs,
        "spoken_at_cliffs": spoken_dialogue,
        "has_loops_or_rewatches": any(y > 100.0 for y in ys),
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze YouTube audience-retention CSV export.")
    parser.add_argument("file", help="Path to audience retention CSV")
    parser.add_argument("--transcript", help="Path to transcript (.srt, .vtt) to identify dialogue at drops")
    parser.add_argument("--duration", type=float, help="Total video duration in seconds (if CSV axis is percentage)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    try:
        rows = load_retention_csv(args.file)
        res = analyze_retention(rows, duration=args.duration, transcript_path=args.transcript)
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error analyzing retention CSV: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    print(f"\n  Retention File: {args.file} ({res['data_points']} points)")
    print(f"  Retention Curve: {res['start_retention']}% -> {res['end_retention']}%")
    if res["has_loops_or_rewatches"]:
        print("  [NOTE] Curve exceeds 100% in sections (indicates viewer rewatches or loop repeats).")

    print(f"\n  HOOK LEAK: {res['hook_leak']}% lost in first 30s [{res['hook_verdict'].upper()}]")
    if res["hook_verdict"] == "healthy":
        print("             Under 25% drop is solid for standard videos.")
    else:
        print("             Primary fix: tighten the first 15 seconds before modifying downstream pacing.")

    print("\n  CLIFFS (Steepest drop moments):")
    if res["cliffs"]:
        for c in res["cliffs"]:
            at_str = f"{c['sec']:.1f}s" if c["sec"] is not None else f"{c['from_x']}%"
            dialogue = res["spoken_at_cliffs"].get(str(c["from_x"]), "")
            diag_str = f"  \"{dialogue}\"" if dialogue else ""
            print(f"    -{c['drop']:4.1f}% at {at_str:>8}{diag_str}")
    else:
        print("    None steeper than 0.8%. Loss is gradual pacing attrition rather than jarring cliffs.")

    print(f"\n  SLIDE RATE: {res['slide_rate']}% average drop per step in the body.")
    print("              Flat slide indicates pacing; edit out dead sections rather than rewriting topics.\n")


if __name__ == "__main__":
    main()
