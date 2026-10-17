#!/usr/bin/env python3
"""Unit tests to validate skill structure and metadata integrity."""

import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPECTED_CLAUDE_SKILLS = [
    "yt-script", "yt-package", "yt-edit", "yt-comment", "yt-plan", "yt-viral",
    "yt-retention", "yt-shorts", "yt-seo", "yt-chapters", "yt-audit",
    "yt-storyboard", "yt-produce", "yt-localize", "yt-factcheck", "yt-upload-prep", "yt-experiment",
    "yt-studio", "yt-stock-producer", "yt-voice-urdu", "yt-video-editor",
    "yt-motion-graphics", "yt-production-qa", "yt-credit-guard",
    "yt-hybrid-production", "yt-voice", "yt-assets", "yt-audio", "yt-render", "yt-render-qc"
]

EXPECTED_CHATGPT_SKILLS = EXPECTED_CLAUDE_SKILLS


class TestSkillStructure(unittest.TestCase):
    def _validate_skill_file(self, skill_path: str, expected_name: str):
        self.assertTrue(os.path.exists(skill_path), f"Missing skill file: {skill_path}")
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check YAML frontmatter presence
        self.assertTrue(content.startswith("---"), f"{skill_path} missing frontmatter opening '---'")
        parts = content.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, f"{skill_path} malformed frontmatter delimiter")
        frontmatter = parts[1]
        body = parts[2].strip()

        # Check name and description in frontmatter
        name_match = re.search(r"name:\s*([a-zA-Z0-9_-]+)", frontmatter)
        self.assertIsNotNone(name_match, f"{skill_path} missing 'name:' in frontmatter")
        self.assertEqual(name_match.group(1), expected_name, f"Name mismatch in {skill_path}")

        desc_match = re.search(r"description:\s*(.*)", frontmatter)
        self.assertIsNotNone(desc_match, f"{skill_path} missing 'description:' in frontmatter")

        # Check body length
        self.assertGreater(len(body), 100, f"Body in {skill_path} is suspiciously short")

    def test_claude_skills(self):
        claude_skills_dir = os.path.join(REPO_ROOT, "skills")
        for skill_name in EXPECTED_CLAUDE_SKILLS:
            skill_md = os.path.join(claude_skills_dir, skill_name, "SKILL.md")
            self._validate_skill_file(skill_md, skill_name)

    def test_chatgpt_skills(self):
        chatgpt_skills_dir = os.path.join(REPO_ROOT, "chatgpt", "skills")
        for skill_name in EXPECTED_CHATGPT_SKILLS:
            skill_md = os.path.join(chatgpt_skills_dir, skill_name, "SKILL.md")
            self._validate_skill_file(skill_md, skill_name)


if __name__ == "__main__":
    unittest.main()
