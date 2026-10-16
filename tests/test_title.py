#!/usr/bin/env python3
"""Unit tests for title and thumbnail linter."""

import os
import unittest
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "shared", "scripts"))

from title import check_pairing


class TestTitleLinter(unittest.TestCase):
    def test_optimal_pairing(self):
        title = "Why 97% of Creators Quit Before Video 30"
        thumb = "STOP QUITTING"
        res = check_pairing(title, thumb)
        self.assertGreaterEqual(res["score"], 80)
        self.assertLessEqual(res["chars"], 60)
        # Verify no duplicate words detected
        duplicate_issues = [m for k, m in res["issues"] if k == "duplicate"]
        self.assertEqual(len(duplicate_issues), 0)

    def test_duplicate_words_detection(self):
        title = "The Best Camera for YouTube Videos"
        thumb = "BEST CAMERA YOUTUBE"
        res = check_pairing(title, thumb)
        issue_keys = [k for k, _ in res["issues"]]
        self.assertIn("duplicate", issue_keys)

    def test_mobile_and_desktop_truncation(self):
        # 45 chars: Safe for desktop (<=60), flags mobile (>40)
        res_45 = check_pairing("The Secret Technique to Double Your Coding Speed")
        issue_keys_45 = [k for k, _ in res_45["issues"]]
        self.assertIn("mobile", issue_keys_45)
        self.assertNotIn("length", issue_keys_45)

        # 75 chars: Flags desktop and mobile
        res_75 = check_pairing("The Complete In-Depth Guide on How to Master Artificial Intelligence and Python")
        issue_keys_75 = [k for k, _ in res_75["issues"]]
        self.assertIn("length", issue_keys_75)

    def test_shouting_all_caps(self):
        res = check_pairing("DO NOT MAKE THIS HUGE CRITICAL MISTAKE EVER")
        issue_keys = [k for k, _ in res["issues"]]
        self.assertIn("shouting", issue_keys)


if __name__ == "__main__":
    unittest.main()
