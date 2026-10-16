# Repository Audit Report — YouTube Agent Studio

## Executive Summary

- **Repository**: `https://github.com/islamically85-byte/youtube-agent-skill`
- **Upstream Origin**: `https://github.com/Jakeschincariol/youtube-agent-skill`
- **Auditor**: Senior AI Agent Engineer & Open-Source Maintainer
- **Baseline Git Commit**: `d79580c3232ec282a3fe9dce78071a0506b58884`
- **Development Branch**: `feature/v2-youtube-agent-studio`
- **Target Upgrade**: YouTube Agent Studio v2.0 (Dual Claude + ChatGPT Edition)

---

## 1. Inventory of Existing Workflows & Tools

### Existing Workflows (Claude Edition)
1. `yt-script` — One idea into a 5-beat script with scored hook options.
2. `yt-package` — Title and thumbnail linted as a single click surface.
3. `yt-edit` — Edit decision list (EDL) from timestamped transcripts.
4. `yt-comment` — Comment triage and replies reflecting creator voice.
5. `yt-plan` — Capacity-aware weekly/monthly content scheduling.
6. `yt-viral` — Outlier ranking by multiple over channel's own median.
7. `yt-retention` — Audience retention leak identification (hook leak, cliffs, slide).
8. `yt-shorts` — Extracting self-contained vertical video clips from long-form.
9. `yt-seo` — Search intent descriptions and secondary tag recommendations.
10. `yt-chapters` — YouTube timestamp/chapter generator adhering to platform constraints.
11. `yt-audit` — End-to-end channel diagnostic targeting one high-impact fix.

### Existing Python Utilities
1. `skills/yt-script/hookscore.py`
2. `skills/yt-package/title.py`
3. `skills/yt-edit/deadair.py`
4. `skills/yt-chapters/chapters.py`
5. `skills/yt-retention/retention.py`
6. `skills/yt-viral/swipe.py`

---

## 2. Identified Bugs, Fragilities, and Architectural Issues

### A. Broken Packaging & Unresolved Cross-Skill Relative Imports
- **`skills/yt-chapters/chapters.py`** executes:
  ```python
  sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "yt-edit"))
  from deadair import load, parse_ts
  ```
  If `yt-chapters` is installed individually or packaged in isolation, this import raises `ImportError: cannot import name 'load' from 'deadair'`.
- **`skills/yt-retention/retention.py`** executes:
  ```python
  sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "yt-edit"))
  from deadair import load as load_cues
  ```
  Same failure occurs when `yt-retention` is moved or packaged independently.
- **`skills/yt-viral/swipe.py`** loads:
  ```python
  FORMULAS = json.load(open(os.path.join(HERE, "..", "yt-script", "hooks.json")))["hooks"]
  ```
  Fails with `FileNotFoundError` if installed without `yt-script/hooks.json` in the relative parent directory.

### B. Transcript Parsing & Encoding Fragilities
- **Non-ASCII & Multilingual Destruction**: `deadair.py` normalizes text with:
  ```python
  def norm(t): return re.sub(r"[^a-z ]", "", t.lower()).split()
  ```
  This strips all non-Latin characters. For Urdu, Arabic, Hindi, Japanese, Cyrillic, and accented Latin scripts, `norm(t)` returns an empty list, completely breaking repeat/restart detection.
- **Strict VTT Assumptions**: `deadair.py` uses `r"\s*(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)"`, but does not handle WebVTT cue settings, metadata headers, or inline `<c>` voice tags.
- **Whisper JSON Schema Variations**: Only checks `segments` or top-level list, failing on WhisperX or raw word-level JSON timestamp formats.

### C. CSV Parsing & Retention Calculation Inconsistencies
- **Malformed & Header Inconsistencies**: `retention.py` assumes numeric columns are always at indices 0 and 1, skipping rows without checking semantic column headers (e.g. `Timestamp, Video time, Audience retention %`).
- **Falsy Zero Bug**: `start = ys[0] or 100.0`. If retention starts at `0.0`, Python evaluates `0.0 or 100.0` to `100.0`.
- **Retention Over 100%**: Shorts loops and rewatches frequently produce retention rates > 100% (e.g., 140%). The existing logic does not recognize loops and flags false hook leaks.
- **Zero-Division / Index Crashes**: Empty CSVs or files with fewer than 8 rows crash with exit code 1 instead of returning structured error diagnostics.

### D. Outlier Calculation & Small Sample Caveats
- **Invalid Views Values**: In `swipe.py`, `float(v.get("views", 0) or 0)` crashes on formatted strings like `"45.2K"` or `"12,000"`.
- **Sample Size Reliability**: Ignores statistical variance and does not output caveats on channel age or sample disparity.

### E. CLI Interface & Portability
- Scripts lack standard `argparse` implementations, relying on fragile manual `sys.argv` indexing (e.g. `a[a.index("--floor") + 1]`), which crashes with `ValueError` or `IndexError` on invalid flags.
- No `--help` flag documentation in several tools.
- Windows console encoding (`cp1252`) causes unhandled `UnicodeEncodeError` when non-ASCII characters are printed without UTF-8 stream handling.

### F. Duplicated Workflow Instructions & Platform Lock-In
- All 11 existing `SKILL.md` files repeat identical instructions referring to `~/.claude/youtube/voice.md`.
- No modular channel profile specification exists (no structured schema for niche, language, target persona, production limits).
- Completely lacks ChatGPT support: no ChatGPT manifest, no conversational orchestration, and no OpenAPI/plugin schemas.

---

## 3. Corrective Architecture Plan

1. **Shared Foundation (`shared/scripts/`)**:
   - Universal transcript parser (`transcript.py`) supporting SRT, VTT, Whisper, YouTube JSON, with full Unicode/Urdu support.
   - Refactored `hookscore.py`, `title.py`, `deadair.py`, `chapters.py`, `retention.py`, `swipe.py` with standard `argparse`, structured JSON output, and defensive type conversion.
   - Embedded hook formula fallbacks to avoid broken relative dependencies.
2. **Self-Contained Claude Edition (`skills/`)**:
   - Keep all 11 existing command names and directories backward-compatible.
   - Bundle self-contained helper scripts into each skill so they can be copied or zipped without external path dependencies.
   - Add the 6 new advanced workflows (`yt-storyboard`, `yt-produce`, `yt-localize`, `yt-factcheck`, `yt-upload-prep`, `yt-experiment`).
3. **Dedicated ChatGPT Edition (`chatgpt/`)**:
   - `yt-studio` master orchestration workflow with conversational triggers.
   - 17 specialized skills tailored for ChatGPT execution and OpenAI packaging guidelines.
   - Separate manifests for ChatGPT Skills (ZIP) and ChatGPT Plugins (`plugin.json`).
4. **Channel Personalization (`templates/channel-profiles/`)**:
   - Structured YAML/JSON channel profiles with sample for Pakistani Urdu educational content.
5. **Quality Assurance (`tests/`)**:
   - Automated pytest suite with test fixtures.
   - 20 behavioral evaluation scenarios verifying real prompt behavior.
   - Packaging validation script (`scripts/build-releases.py`).
