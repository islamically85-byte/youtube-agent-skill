#!/usr/bin/env python3
"""hookscore.py - Score a YouTube hook before you waste a take on it.

Five properties (0-100 each), and a verdict that is 60% the mean and 40% the weakest property:
- SPECIFICITY: Concrete numbers, metrics, proper nouns vs. vague adjectives and filler words
- ADDRESS: Direct viewer address ('you', 'your') in opening words
- STAKES: Real cost, risk, loss, or consequence of inaction
- CURIOSITY: Unresolved knowledge gap or contrarian question without premature resolution
- BREVITY: Word count calibrated for spoken delivery inside 10 seconds (~9-24 words)

IMPORTANT NOTE:
Editorial heuristic, NOT a predictor of views. It separates deliberately weak hooks from
focused ones, but cannot guarantee algorithm distribution or viral performance.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))

# Candidate paths for hooks.json
CANDIDATE_PATHS = [
    os.path.join(HERE, "hooks.json"),
    os.path.join(HERE, "..", "shared", "scripts", "hooks.json"),
    os.path.join(HERE, "..", "yt-script", "hooks.json"),
    os.path.join(HERE, "..", "..", "shared", "scripts", "hooks.json"),
    os.path.join(HERE, "..", "..", "skills", "yt-script", "hooks.json"),
]

DEFAULT_FORMULAS = [
    {
        "id": "the-statistic",
        "name": "The Statistic",
        "shape": "A concrete number or metric, stated flat, then the consequence.",
        "match": [r"\b\d+(\.\d+)?\s?%", r"\b\d+ (out of|in) \d+\b", r"\b\d{2,}(,\d{3})+\b"]
    },
    {
        "id": "someone-elses-result",
        "name": "Someone Else's Result",
        "shape": "A named person's outcome, then the mechanism.",
        "match": [r"\bthis (channel|creator|person|team|business)\b", r"\bwent from .* to\b"]
    },
    {
        "id": "the-mistake",
        "name": "The Mistake",
        "shape": "Name the specific error the viewer is probably making.",
        "match": [r"\bthe (reason|mistake|error|trap|lie)\b", r"\byou're doing .* wrong\b"]
    },
    {
        "id": "the-curiosity-gap",
        "name": "The Curiosity Gap",
        "shape": "A paradox or contradiction that cannot be closed without watching.",
        "match": [r"\bwhy (nobody|everyone|almost)\b", r"\bwhat happens when\b", r"\bthe real reason\b"]
    }
]


def load_formulas() -> List[Dict[str, Any]]:
    for path in CANDIDATE_PATHS:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f).get("hooks", DEFAULT_FORMULAS)
            except Exception:
                pass
    return DEFAULT_FORMULAS


FORMULAS = load_formulas()

FILLER = {
    "basically", "actually", "literally", "just", "really", "very", "so", "kind", "sort", "like",
    "guys", "hey", "welcome", "today", "video", "subscribe", "channel", "bro", "look"
}
VAGUE = {
    "amazing", "incredible", "insane", "crazy", "huge", "massive", "game", "changer", "secret",
    "powerful", "ultimate", "best", "revolutionary", "mind", "blowing", "unbelievable", "awesome",
    "epic", "shocking", "magic"
}

CONCRETE = re.compile(
    r"\b(\d[\d,.]*\s?(%|k|m|x|s|m|h)?|\$\d[\d,.]*|\d+\s?(second|minute|hour|day|week|month|year)s?)\b",
    re.I
)
YOU = re.compile(r"\b(you|your|you're|youre|yourself)\b", re.I)
STAKE = re.compile(
    r"\b(lose|lost|wasting|waste|quit|fail|broke|cost|risk|before|stop|never|die|dying|dead|ruin|destroy|harm)\b",
    re.I
)
CURIOSITY = re.compile(
    r"\b(why|how|what|which|until|before|but|nobody|almost|except|reason|actually|secret|hidden)\b",
    re.I
)


def words(t: str) -> List[str]:
    return re.findall(r"[\w'%$.]+", t.lower(), re.UNICODE)


def specificity(t: str) -> int:
    w = words(t)
    if not w:
        return 0
    nums = len(CONCRETE.findall(t))
    vague = sum(1 for x in w if x in VAGUE)
    filler = sum(1 for x in w if x in FILLER)
    s = 34 + nums * 22 - vague * 16 - filler * 5
    # Proper nouns / capitalized words not at sentence start
    tokens = t.split()
    if len(tokens) > 1:
        proper = sum(1 for x in tokens[1:] if x[:1].isupper() and x.isalpha())
        s += min(18, 6 * proper)
    return max(0, min(100, s))


def address(t: str) -> int:
    n = len(YOU.findall(t))
    first = 30 if YOU.search(" ".join(t.split()[:6])) else 0
    return max(0, min(100, 26 + n * 20 + first))


def stakes(t: str) -> int:
    n = len(STAKE.findall(t))
    has_concrete = 14 if CONCRETE.search(t) else 0
    return max(0, min(100, 22 + n * 26 + has_concrete))


def curiosity(t: str) -> int:
    n = len(CURIOSITY.findall(t))
    q = 18 if t.strip().endswith("?") else 0
    closed = -18 if re.search(r"\b(because|so that|which means|in this video)\b", t, re.I) else 0
    return max(0, min(100, 24 + n * 17 + q + closed))


def brevity(t: str) -> int:
    n = len(words(t))
    if n == 0:
        return 0
    # 9-24 words is optimal for 10-second delivery (~150 wpm)
    if 9 <= n <= 24:
        return 100
    if n < 9:
        return max(30, 100 - (9 - n) * 11)
    return max(10, 100 - (n - 24) * 7)


PROPS = [
    ("SPECIFICITY", specificity),
    ("ADDRESS", address),
    ("STAKES", stakes),
    ("CURIOSITY", curiosity),
    ("BREVITY", brevity),
]

FIX = {
    "SPECIFICITY": "Swap an adjective for a concrete number, named person, or metric.",
    "ADDRESS": "Use direct address ('you', 'your') within the first 6 words.",
    "STAKES": "Name the specific cost, risk, or loss of continuing the current way.",
    "CURIOSITY": "Cut the second half of the sentence if it prematurely answers itself.",
    "BREVITY": "Target 9 to 24 words (~10 spoken seconds). Read aloud in one breath.",
}


def classify(t: str) -> Tuple[str, int]:
    best, hits = None, 0
    for f in FORMULAS:
        n = sum(1 for p in f.get("match", []) if re.search(p, t, re.I))
        if n > hits:
            best, hits = f, n
    return (best["name"] if best else "Unclassified"), hits


def score(t: str) -> Tuple[Dict[str, int], int, str, int]:
    parts = {name: fn(t) for name, fn in PROPS}
    vals = list(parts.values())
    verdict = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals)) if vals else 0
    formula_name, hits = classify(t)
    return parts, verdict, formula_name, hits


def band(v: int) -> str:
    return "STRONG" if v >= 72 else "WORKABLE" if v >= 55 else "WEAK"


def report(t: str, parts: Dict[str, int], verdict: int, name: str, hits: int):
    t_clean = t.strip()
    print(f"\n  {t_clean}")
    print(f"  {'-' * min(72, max(20, len(t_clean)))}")
    for k, v in parts.items():
        bar = "#" * (v // 5)
        print(f"    {k:<12} {v:3d}  {bar}")
    print(f"    {'VERDICT':<12} {verdict:3d}  [{band(verdict)}]")
    matched_str = f"({hits} pattern{'s' if hits != 1 else ''} matched)" if hits else "(no formula matched - often a summary, not a hook)"
    print(f"    formula      {name}  {matched_str}")
    low = min(parts, key=parts.get)
    print(f"    weakest      {low} - {FIX[low]}")


def main():
    parser = argparse.ArgumentParser(description="Score YouTube hooks with the 5-property panel.")
    parser.add_argument("file", nargs="?", help="File containing hook options (one per line)")
    parser.add_argument("--hook", help="Score a single hook string")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    lines: List[str] = []
    if args.hook:
        lines = [args.hook]
    elif args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            lines = [line.strip() for line in f if line.strip()]
    else:
        parser.print_help()
        sys.exit(0)

    out = []
    for line in lines:
        parts, verdict, name, hits = score(line)
        weakest = min(parts, key=parts.get)
        out.append({
            "hook": line.strip(),
            "properties": parts,
            "verdict": verdict,
            "band": band(verdict),
            "formula": name,
            "matched_patterns": hits,
            "weakest_property": weakest,
            "fix_suggestion": FIX[weakest],
        })

    out.sort(key=lambda r: -r["verdict"])

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    for r in out:
        report(r["hook"], r["properties"], r["verdict"], r["formula"], r["matched_patterns"])

    if len(out) > 1:
        winner = out[0]
        print(f"\n  WINNER: \"{winner['hook']}\" ({winner['verdict']}/100, {winner['band']})\n")


if __name__ == "__main__":
    main()
