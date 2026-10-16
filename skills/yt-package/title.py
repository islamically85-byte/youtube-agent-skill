#!/usr/bin/env python3
"""title.py - Lint a YouTube title and thumbnail pairing as a unified system.

The title and thumbnail form a single click surface. Repeating words across them wastes
valuable real estate.

Key checks:
- Length: Truncation warnings at 40 chars (mobile feed) and 60 chars (desktop search). Hard limit 100.
- Shouting: Flags more than two ALL-CAPS words.
- Specificity: Checks for numbers, metrics, or proper nouns; flags vague buzzwords.
- Front-loading: Checks if the primary subject appears early.
- Thumbnail pairing: Flags duplicate vocabulary between thumbnail and title.
- Thumbnail length: Checks for <= 3 words on thumbnail for readability at mobile sizes.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

DESKTOP_MAX = 60
MOBILE_MAX = 40
HARD_MAX = 100

VAGUE_WORDS = {
    "amazing", "incredible", "insane", "crazy", "huge", "massive", "ultimate", "best", "powerful",
    "secret", "revolutionary", "mindblowing", "epic", "perfect", "complete", "everything",
    "unbelievable", "shocking", "gamechanger", "game-changer"
}

STOP_WORDS = {
    "the", "a", "an", "of", "for", "to", "in", "on", "and", "or", "is", "are", "with", "your",
    "you", "my", "i", "this", "that", "it", "how", "what", "why", "at", "by", "from", "as"
}


def words(t: str) -> List[str]:
    return re.findall(r"[\w']+", t.lower(), re.UNICODE)


def check_pairing(title: str, thumb: Optional[str] = None) -> Dict[str, Any]:
    t = title.strip()
    n = len(t)
    issues: List[Tuple[str, str]] = []
    good: List[str] = []

    # Length constraints
    if n > HARD_MAX:
        issues.append(("length", f"{n} characters exceeds YouTube's hard 100-character limit."))
    elif n > DESKTOP_MAX:
        issues.append(("length", f"{n} characters. Desktop search truncates around {DESKTOP_MAX} characters."))
    else:
        good.append(f"{n} characters, safe for desktop search cutoffs.")

    if n > MOBILE_MAX:
        head = t[:MOBILE_MAX].rsplit(" ", 1)[0]
        issues.append(("mobile", f"Mobile home feed cuts near {MOBILE_MAX} chars ('{head}...'). Verify subject visibility."))
    else:
        good.append(f"Inside {MOBILE_MAX} characters: fully visible on mobile feeds without truncation.")

    # Capitalization
    caps_words = [w for w in t.split() if len(w) > 2 and w.isupper() and w.isalpha()]
    if len(caps_words) > 2:
        issues.append(("shouting", f"{len(caps_words)} ALL-CAPS words. Maximum recommended is 2 before triggering spam filters."))
    elif caps_words:
        good.append(f"{len(caps_words)} emphasized uppercase word(s).")

    # Specificity & Buzzwords
    t_words = words(t)
    vague_found = [w for w in t_words if w in VAGUE_WORDS]
    if vague_found:
        issues.append(("vague", f"Vague buzzwords detected: {', '.join(sorted(set(vague_found)))}. Swap for metrics or names."))

    nums = re.findall(r"\b\d[\d,.]*%?\b", t)
    if nums:
        good.append(f"Carries concrete figure: {', '.join(nums[:3])}")
    else:
        issues.append(("no-number", "No concrete number, metric, or named entity found."))

    if t.endswith("?"):
        good.append("Open question structure creates curiosity.")

    # Front-loading
    front_tokens = [w for w in t_words[:3] if w not in STOP_WORDS]
    if not front_tokens:
        issues.append(("front-load", "First three words are common stopwords. Move core subject earlier."))
    else:
        good.append("Subject is front-loaded in opening words.")

    # Thumbnail integration
    if thumb:
        thumb_clean = thumb.strip()
        t_set = set(t_words) - STOP_WORDS
        th_words = words(thumb_clean)
        th_set = set(th_words) - STOP_WORDS
        shared = t_set & th_set
        if shared:
            issues.append(("duplicate", f"Thumbnail repeats title word(s): {', '.join(sorted(shared))}. Use thumbnail for complementary visual hook."))
        else:
            good.append("Thumbnail and title use complementary, non-overlapping vocabulary.")

        if len(th_words) > 4:
            issues.append(("thumb-length", f"{len(th_words)} words on thumbnail. 3-4 words is the legibility ceiling on mobile."))
        else:
            good.append(f"Thumbnail text is punchy ({len(th_words)} words).")

    score = max(0, min(100, 100 - (15 * len(issues)) + (4 * len(good))))

    return {
        "title": t,
        "thumbnail_text": thumb.strip() if thumb else None,
        "chars": n,
        "score": score,
        "issues": issues,
        "good": good,
    }


def show_report(r: Dict[str, Any]):
    print(f"\n  Title: \"{r['title']}\"")
    if r.get("thumbnail_text"):
        print(f"  Thumbnail: \"{r['thumbnail_text']}\"")
    print(f"  Length: {r['chars']} chars | Score: {r['score']}/100")
    for k, m in r["issues"]:
        print(f"    [X] {k:<12} {m}")
    for m in r["good"]:
        print(f"    [OK]            {m}")


def main():
    parser = argparse.ArgumentParser(description="Lint YouTube title and thumbnail pairing.")
    parser.add_argument("file", nargs="?", help="File with titles (one per line)")
    parser.add_argument("--title", help="Evaluate a single title")
    parser.add_argument("--thumb", help="Thumbnail overlay text")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    rows = []
    if args.title:
        rows = [check_pairing(args.title, args.thumb)]
    elif args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            titles = [l.strip() for l in f if l.strip()]
        rows = [check_pairing(t, args.thumb) for t in titles]
    else:
        parser.print_help()
        sys.exit(0)

    rows.sort(key=lambda r: -r["score"])

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return

    for r in rows:
        show_report(r)
    print()


if __name__ == "__main__":
    main()
