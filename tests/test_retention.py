#!/usr/bin/env python3
"""Unit tests for audience retention analysis."""

import os
import unittest
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "shared", "scripts"))

from retention import load_retention_csv, analyze_retention


class TestRetention(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.join(REPO_ROOT, "shared", "fixtures")
        self.std_csv = os.path.join(self.fixtures_dir, "retention_standard.csv")
        self.pct_csv = os.path.join(self.fixtures_dir, "retention_percentages.csv")
        self.loop_csv = os.path.join(self.fixtures_dir, "retention_shorts_loop.csv")
        self.srt_path = os.path.join(self.fixtures_dir, "sample_transcript.srt")

    def test_standard_retention_analysis(self):
        rows = load_retention_csv(self.std_csv)
        self.assertGreaterEqual(len(rows), 10)
        res = analyze_retention(rows, duration=240.0, transcript_path=self.srt_path)
        self.assertEqual(res["start_retention"], 100.0)
        self.assertGreater(res["hook_leak"], 0.0)
        self.assertGreaterEqual(len(res["cliffs"]), 1)
        self.assertFalse(res["has_loops_or_rewatches"])

    def test_percentage_string_parsing(self):
        rows = load_retention_csv(self.pct_csv)
        self.assertEqual(len(rows), 11)
        # All values should be clean floats between 0 and 100
        for x, y in rows:
            self.assertIsInstance(x, float)
            self.assertIsInstance(y, float)
            self.assertGreaterEqual(y, 0.0)

    def test_shorts_loop_detection(self):
        rows = load_retention_csv(self.loop_csv)
        res = analyze_retention(rows)
        # Check that retention over 100% was detected as rewatch/loop
        self.assertTrue(res["has_loops_or_rewatches"])
        max_ret = max(y for _, y in rows)
        self.assertGreater(max_ret, 100.0)

    def test_insufficient_data_error(self):
        with self.assertRaises(ValueError):
            analyze_retention([(0.0, 100.0), (1.0, 90.0)])


if __name__ == "__main__":
    unittest.main()
