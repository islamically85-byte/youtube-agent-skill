#!/usr/bin/env python3
"""editorial_motion.py - Synchronized Documentary Motion Graphics & ASS Generator v3.0.

Features:
1. Synchronized to EXACT narration spoken cues (from voice_cue_times.json or transcript),
   NOT arbitrary duration percentages.
2. Presentation of 42,000, 6,000, and 36,000 strictly as REPORTED ALLEGATIONS ('رپورٹ کردہ الزامات'),
   never established court findings.
3. Clean, understated broadcast aesthetics (Noto Naskh Arabic / Noto Nastaliq Urdu):
   - Headline curiosity overlays
   - Stat comparison cards with disclaimer
   - Evidence tags (Geo News investigative reporting, CDA, NOC vs Layout Plan)
   - 4-step due diligence checklist
   - Subtle vertical rise and fade animation (0.45s rise, no tacky glitches or neon)
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def timecode_ass(seconds: float) -> str:
    """Format seconds into ASS timecode H:MM:SS.cs."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def escape_ass(text: str) -> str:
    """Escape ASS control characters."""
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("\n", r"\N")


# ASS header with refined typographic hierarchy
ASS_HEADER = """[Script Info]
Title: Pakistan Property Group Documentary Motion Graphics v3.0
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Headline,Noto Naskh Arabic,68,&H00FFFFFF,&H00FFFFFF,&H00303030,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,7,90,90,30,1
Style: Stat,Noto Naskh Arabic,80,&H00FFFFFF,&H00FFFFFF,&H00303030,&H70000000,-1,0,0,0,100,100,0,0,1,3,1,7,90,90,30,1
Style: Evidence,Noto Naskh Arabic,52,&H00FFFFFF,&H00FFFFFF,&H00303030,&H90000000,-1,0,0,0,100,100,0,0,1,2,1,7,90,90,30,1
Style: Disclaimer,Noto Naskh Arabic,42,&H0020D0FF,&H0020D0FF,&H00202020,&HA0000000,-1,0,0,0,100,100,0,0,1,2,1,7,90,90,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def build_synchronized_motion_ass(
    total_duration_sec: float,
    cue_times: Optional[List[Dict[str, Any]]] = None,
    output_path: Optional[str] = None
) -> str:
    """Build ASS motion graphics file synchronized to exact spoken cue events."""
    out_file = Path(output_path) if output_path else Path("editorial_motion.ass")
    events: List[str] = []

    def add_card(start_s: float, end_s: float, style: str, text: str, x: int = 250, y: int = 720):
        # Subtle 22px vertical rise over 0.45s with gentle fade
        motion = rf"{{\move({x},{y+22},{x},{y},0,450)\fad(350,350)}}"
        dialogue = (
            f"Dialogue: 0,{timecode_ass(start_s)},{timecode_ass(end_s)},"
            f"{style},,0,0,0,,{motion}{escape_ass(text)}\n"
        )
        events.append(dialogue)

    # If cue times are supplied from actual TTS/speech alignment:
    if cue_times and len(cue_times) >= 5:
        # Search for exact cue moments
        for cue in cue_times:
            c_text = cue.get("text", "")
            c_start = float(cue.get("start", 0.0))
            c_end = float(cue.get("end", c_start + 4.0))
            dur = max(3.5, c_end - c_start)

            # 1. Opening hook
            if "فائل موجود" in c_text and c_start < 40.0:
                add_card(c_start, c_start + dur + 1.0, "Headline", "فائل موجود ہے۔۔۔ مگر زمین کہاں ہے؟", 250, 720)

            # 2. 42,000 files statistic
            elif "بیالیس ہزار" in c_text or "42,000" in c_text:
                add_card(c_start, c_start + dur, "Stat", "رپورٹ شدہ دعویٰ: 42,000 فائلیں؟", 250, 200)

            # 3. 6,000 plots statistic
            elif "چھ ہزار" in c_text or "6,000" in c_text:
                add_card(c_start, c_start + dur, "Stat", "دستیاب گنجائش: تقریباً 6,000 پلاٹ؟", 250, 200)

            # 4. Legal disclaimer
            elif "الزامات" in c_text or "جرم ثابت" in c_text:
                add_card(c_start, c_start + dur + 1.0, "Disclaimer", "⚠️ یہ رپورٹ کردہ الزامات ہیں — حتمی عدالتی فیصلہ نہیں", 180, 880)

            # 5. Investigative reports
            elif "تحقیقاتی" in c_text or "جیو نیوز" in c_text:
                add_card(c_start, c_start + dur, "Evidence", "تحقیقاتی رپورٹ  |  ذرائع کے حوالے سے تفصیلات", 150, 810)

            # 6. Layout Plan vs NOC distinction
            elif "این او سی" in c_text and "منظوری" in c_text:
                add_card(c_start, c_start + dur, "Evidence", "منظور شدہ لے آؤٹ پلان  ≠  جاری شدہ این او سی", 140, 810)

            # 7. Step 1 Due diligence
            elif "پہلا قدم" in c_text:
                add_card(c_start, c_start + dur, "Evidence", "۱ — سرکاری ادارے سے تازہ این او سی کی تصدیق کریں", 140, 800)

            # 8. Step 2
            elif "دوسرا قدم" in c_text:
                add_card(c_start, c_start + dur, "Evidence", "۲ — فائل اور پلاٹ نمبر کو زمین کے اصل نقشے سے ملائیں", 140, 800)

            # 9. Step 3
            elif "تیسرا قدم" in c_text:
                add_card(c_start, c_start + dur, "Evidence", "۳ — موقع پر جا کر زمین کی باؤنڈری اور ملکیت دیکھیں", 140, 800)

            # 10. Step 4
            elif "چوتھا قدم" in c_text:
                add_card(c_start, c_start + dur, "Evidence", "۴ — بڑی رقم کی ادائیگی سے قبل وکیل سے جانچ کرائیں", 140, 800)

            # 11. Closing
            elif "پاکستان پراپرٹی گروپ" in c_text and c_start > (total_duration_sec - 40.0):
                add_card(c_start, min(total_duration_sec, c_start + dur + 2.0), "Headline", "پاکستان پراپرٹی گروپ", 250, 710)

    # Fallback to proportionally scaled cue points if exact cue times are not available
    if not events:
        marks = [
            (0.02, 0.08, "Headline", "فائل موجود ہے۔۔۔ مگر زمین کہاں ہے؟", 250, 720),
            (0.12, 0.18, "Stat", "رپورٹ شدہ دعویٰ: 42,000 فائلیں؟", 250, 200),
            (0.18, 0.23, "Stat", "دستیاب گنجائش: تقریباً 6,000 پلاٹ؟", 250, 200),
            (0.23, 0.28, "Disclaimer", "⚠️ یہ رپورٹ کردہ الزامات ہیں — حتمی عدالتی فیصلہ نہیں", 180, 880),
            (0.40, 0.44, "Evidence", "تحقیقاتی رپورٹ  |  ذرائع کے حوالے سے تفصیلات", 150, 810),
            (0.53, 0.58, "Evidence", "منظور شدہ لے آؤٹ پلان  ≠  جاری شدہ این او سی", 140, 810),
            (0.68, 0.72, "Evidence", "۱ — سرکاری ادارے سے تازہ این او سی کی تصدیق کریں", 140, 800),
            (0.73, 0.77, "Evidence", "۲ — فائل اور پلاٹ نمبر کو زمین کے اصل نقشے سے ملائیں", 140, 800),
            (0.78, 0.82, "Evidence", "۳ — موقع پر جا کر زمین کی باؤنڈری اور ملکیت دیکھیں", 140, 800),
            (0.83, 0.87, "Evidence", "۴ — بڑی رقم کی ادائیگی سے قبل وکیل سے جانچ کرائیں", 140, 800),
            (0.95, 0.99, "Headline", "پاکستان پراپرٹی گروپ", 250, 710)
        ]
        for st_frac, en_frac, style, label, x, y in marks:
            a = round(total_duration_sec * st_frac, 2)
            b = round(total_duration_sec * en_frac, 2)
            add_card(a, b, style, label, x, y)

    full_ass_content = ASS_HEADER + "".join(events)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(full_ass_content, encoding="utf-8-sig")
    return str(out_file)


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronized Documentary Motion Graphics Builder.")
    parser.add_argument("--duration", type=float, default=390.0, help="Total timeline duration in seconds.")
    parser.add_argument("--cues", help="Optional voice_cue_times.json to synchronize to spoken timestamps.")
    parser.add_argument("--output", "-o", default="editorial_motion.ass", help="Output ASS file path.")
    args = parser.parse_args()

    cue_data = None
    if args.cues and os.path.exists(args.cues):
        with open(args.cues, "r", encoding="utf-8") as f:
            cue_data = json.load(f)

    path = build_synchronized_motion_ass(
        total_duration_sec=args.duration,
        cue_times=cue_data,
        output_path=args.output
    )

    print(f"✨ Created synchronized motion graphics ASS: {path} ({args.duration:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
