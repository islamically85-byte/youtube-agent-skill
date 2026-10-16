#!/usr/bin/env python3
"""Unit tests for editorial_motion.py (Hybrid Studio v3.0)."""

import os
import tempfile
import unittest
from shared.scripts.editorial_motion import (
    timecode_ass, escape_ass, build_synchronized_motion_ass
)


class TestEditorialMotion(unittest.TestCase):
    def test_timecode_ass(self):
        self.assertEqual(timecode_ass(0.0), "0:00:00.00")
        self.assertEqual(timecode_ass(65.5), "0:01:05.50")
        self.assertEqual(timecode_ass(3600.25), "1:00:00.25")

    def test_escape_ass(self):
        self.assertEqual(escape_ass("Line1\nLine2"), r"Line1\NLine2")
        self.assertEqual(escape_ass("{curly}"), r"\{curly\}")

    def test_build_synchronized_motion_ass_contains_disclaimers(self):
        with tempfile.TemporaryDirectory() as td:
            out_ass = os.path.join(td, "motion.ass")
            res_path = build_synchronized_motion_ass(
                total_duration_sec=390.0,
                output_path=out_ass
            )
            self.assertTrue(os.path.exists(res_path))
            with open(res_path, "r", encoding="utf-8-sig") as f:
                content = f.read()
            self.assertIn("رپورٹ کردہ الزامات", content)
            self.assertIn("42,000", content)
            self.assertIn("6,000", content)
            self.assertIn("این او سی", content)
            self.assertIn("[Script Info]", content)
            self.assertIn("[V4+ Styles]", content)


if __name__ == "__main__":
    unittest.main()
