#!/usr/bin/env python3
"""Unit tests for hook scoring and formula classification."""

import os
import unittest
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "shared", "scripts"))

from hookscore import score, band, classify, PROPS, FIX


class TestHookscore(unittest.TestCase):
    def test_strong_hook(self):
        hook = "If you start a YouTube channel, 97% quit before video 30. Here is how you survive."
        parts, verdict, name, hits = score(hook)
        self.assertGreaterEqual(verdict, 65)
        self.assertEqual(band(verdict), "STRONG")
        self.assertEqual(name, "The Statistic")
        self.assertGreaterEqual(hits, 1)

    def test_weak_vague_hook(self):
        hook = "Hey guys, welcome back to my channel! In this video today I have an amazing insane secret."
        parts, verdict, name, hits = score(hook)
        self.assertLess(verdict, 55)
        self.assertEqual(band(verdict), "WEAK")
        # Should flag brevity or curiosity or specificity
        self.assertLessEqual(parts["SPECIFICITY"], 40)

    def test_editorial_heuristic_bounds(self):
        # All property scores must strictly stay between 0 and 100
        test_cases = [
            "",
            "a",
            "Super incredible awesome massive secret mindblowing trick!",
            "Why does everyone in tech fail to learn Python in 30 days?",
        ]
        for t in test_cases:
            parts, verdict, _, _ = score(t)
            for k, v in parts.items():
                self.assertGreaterEqual(v, 0, f"{k} negative for '{t}'")
                self.assertLessEqual(v, 100, f"{k} > 100 for '{t}'")
            self.assertGreaterEqual(verdict, 0)
            self.assertLessEqual(verdict, 100)

    def test_weakest_property_fix(self):
        hook = "You are going to lose everything because of this."
        parts, verdict, _, _ = score(hook)
        weakest = min(parts, key=parts.get)
        self.assertIn(weakest, FIX)


if __name__ == "__main__":
    unittest.main()
