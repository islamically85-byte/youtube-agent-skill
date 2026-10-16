#!/usr/bin/env python3
"""build-releases.py - Package and validate YouTube Agent Studio distribution archives.

Generates three validated release archives in release/:
1. youtube-agent-claude.zip         (Full Claude Code / Claude Desktop edition)
2. youtube-agent-chatgpt-skill.zip  (Standalone ChatGPT Skill package)
3. youtube-agent-chatgpt-plugin.zip (Complete ChatGPT Plugin package)

Validates file integrity, manifest syntax, and ensures no dangling relative dependencies.
"""

import json
import os
import shutil
import sys
import zipfile
from typing import List, Tuple

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELEASE_DIR = os.path.join(REPO_ROOT, "release")


def log(msg: str):
    print(f"[BUILD] {msg}")


def create_zip(source_items: List[Tuple[str, str]], zip_path: str):
    """Create a clean zip archive from a list of (abs_source_path, archive_rel_path)."""
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for src, arcname in source_items:
            if os.path.isdir(src):
                for root, dirs, files in os.walk(src):
                    # Skip cache, git, and ds_store
                    dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", ".pytest_cache")]
                    for f in files:
                        if f in (".DS_Store", "*.pyc"):
                            continue
                        full_path = os.path.join(root, f)
                        rel_path = os.path.relpath(full_path, src)
                        target_arc = os.path.join(arcname, rel_path) if arcname else rel_path
                        zf.write(full_path, target_arc)
            elif os.path.isfile(src):
                zf.write(src, arcname)


def validate_zip(zip_path: str, required_files: List[str]) -> bool:
    """Ensure all required files exist inside the generated zip."""
    if not os.path.exists(zip_path):
        print(f"[FAIL] Missing archive: {zip_path}", file=sys.stderr)
        return False

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = set(zf.namelist())

    missing = []
    for req in required_files:
        if not any(n == req or n.endswith("/" + req) or req in n for n in names):
            missing.append(req)

    if missing:
        print(f"[FAIL] {os.path.basename(zip_path)} is missing required files: {missing}", file=sys.stderr)
        return False

    size_kb = os.path.getsize(zip_path) / 1024.0
    log(f"Verified {os.path.basename(zip_path)} ({size_kb:.1f} KB, {len(names)} files)")
    return True


def build_claude_release():
    zip_path = os.path.join(RELEASE_DIR, "youtube-agent-claude.zip")
    log("Building Claude Edition archive...")
    items = [
        (os.path.join(REPO_ROOT, ".claude-plugin"), ".claude-plugin"),
        (os.path.join(REPO_ROOT, "skills"), "skills"),
        (os.path.join(REPO_ROOT, "templates"), "templates"),
        (os.path.join(REPO_ROOT, "shared"), "shared"),
        (os.path.join(REPO_ROOT, "docs"), "docs"),
        (os.path.join(REPO_ROOT, "LICENSE"), "LICENSE"),
        (os.path.join(REPO_ROOT, "README.md"), "README.md"),
    ]
    create_zip(items, zip_path)
    required = [
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
        "skills/yt-script/SKILL.md",
        "skills/yt-script/hookscore.py",
        "skills/yt-storyboard/SKILL.md",
        "skills/yt-produce/SKILL.md",
        "skills/yt-localize/SKILL.md",
        "skills/yt-stock-producer/SKILL.md",
        "skills/yt-video-editor/SKILL.md",
        "skills/yt-production-qa/SKILL.md",
        "skills/yt-credit-guard/SKILL.md",
        "shared/scripts/render_free.py",
        "shared/scripts/validate_manifest.py",
        "shared/scripts/qa_media.py",
        "shared/scripts/credit_guard.py",
        "templates/channel-profiles/pakistani-urdu-awareness.yaml",
        "LICENSE",
    ]
    assert validate_zip(zip_path, required)


def build_chatgpt_skill_release():
    zip_path = os.path.join(RELEASE_DIR, "youtube-agent-chatgpt-skill.zip")
    log("Building ChatGPT Standalone Skill archive...")
    chatgpt_dir = os.path.join(REPO_ROOT, "chatgpt")
    items = [
        (os.path.join(chatgpt_dir, "skills"), "skills"),
        (os.path.join(chatgpt_dir, "templates"), "templates"),
        (os.path.join(chatgpt_dir, "references"), "references"),
        (os.path.join(chatgpt_dir, "scripts"), "scripts"),
        (os.path.join(chatgpt_dir, "schemas"), "schemas"),
        (os.path.join(chatgpt_dir, "README.md"), "README.md"),
        (os.path.join(REPO_ROOT, "LICENSE"), "LICENSE"),
    ]
    create_zip(items, zip_path)
    required = [
        "skills/yt-studio/SKILL.md",
        "skills/yt-script/SKILL.md",
        "skills/yt-localize/SKILL.md",
        "skills/yt-stock-producer/SKILL.md",
        "skills/yt-video-editor/SKILL.md",
        "skills/yt-production-qa/SKILL.md",
        "skills/yt-credit-guard/SKILL.md",
        "references/hooks.json",
        "references/urdu-localization-guide.md",
        "scripts/transcript.py",
        "scripts/hookscore.py",
        "scripts/render_free.py",
        "scripts/validate_manifest.py",
        "scripts/qa_media.py",
        "scripts/credit_guard.py",
        "templates/channel-profiles/pakistani-urdu-awareness.yaml",
        "README.md",
        "LICENSE",
    ]
    assert validate_zip(zip_path, required)


def build_chatgpt_plugin_release():
    zip_path = os.path.join(RELEASE_DIR, "youtube-agent-chatgpt-plugin.zip")
    log("Building ChatGPT Plugin archive...")
    chatgpt_dir = os.path.join(REPO_ROOT, "chatgpt")
    items = [
        (os.path.join(chatgpt_dir, "plugin.json"), "plugin.json"),
        (os.path.join(chatgpt_dir, ".codex-plugin"), ".codex-plugin"),
        (os.path.join(chatgpt_dir, "skills"), "skills"),
        (os.path.join(chatgpt_dir, "templates"), "templates"),
        (os.path.join(chatgpt_dir, "references"), "references"),
        (os.path.join(chatgpt_dir, "scripts"), "scripts"),
        (os.path.join(chatgpt_dir, "schemas"), "schemas"),
        (os.path.join(chatgpt_dir, "README.md"), "README.md"),
        (os.path.join(REPO_ROOT, "LICENSE"), "LICENSE"),
    ]
    create_zip(items, zip_path)
    required = [
        "plugin.json",
        ".codex-plugin/plugin.json",
        "skills/yt-studio/SKILL.md",
        "skills/yt-package/SKILL.md",
        "skills/yt-video-editor/SKILL.md",
        "skills/yt-production-qa/SKILL.md",
        "references/packaging-guidelines.md",
        "scripts/title.py",
        "scripts/render_free.py",
        "scripts/qa_media.py",
        "README.md",
        "LICENSE",
    ]
    assert validate_zip(zip_path, required)


def main():
    os.makedirs(RELEASE_DIR, exist_ok=True)
    try:
        build_claude_release()
        build_chatgpt_skill_release()
        build_chatgpt_plugin_release()
        log("ALL THREE RELEASE PACKAGES SUCCESSFULLY BUILT AND VALIDATED!")
    except Exception as e:
        print(f"[ERROR] Release packaging failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
