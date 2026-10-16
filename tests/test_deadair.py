#!/usr/bin/env python3
"""Unit tests for deadair and EDL generator."""

import os
import unittest
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "shared", "scripts"))

from deadair import generate_edl, is_filler_cue
from transcript import load_transcript


class TestDeadAir(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.join(REPO_ROOT, "shared", "fixtures")
        self.srt_path = os.path.join(self.fixtures_dir, "sample_transcript.srt")

    def test_filler_cue_detection(self):
        self.assertTrue(is_filler_cue("um, basically..."))
        self.assertTrue(is_filler_cue("uh yeah"))
        self.assertTrue(is_filler_cue("you know, like"))
        self.assertTrue(is_filler_cue("مطلب، یعنی..."))  # Urdu filler
        self.assertFalse(is_filler_cue("97% of creators quit before video 30"))

    def test_generate_edl(self):
        cues = load_transcript(self.srt_path)
        cuts = generate_edl(cues, floor=0.45)
        self.assertGreaterEqual(len(cuts), 2)

        cut_types = [c["kind"] for c in cuts]
        self.assertIn("FILLER", cut_types)
        self.assertIn("DEAD", cut_types)
        self.assertIn("REPEAT", cut_types)

        # Check repeat cut detection of sentence restart
        repeat_cuts = [c for c in cuts if c["kind"] == "REPEAT"]
        self.assertGreaterEqual(len(repeat_cuts), 1)
        self.assertIn("restart", repeat_cuts[0]["reason"].lower())


if __name__ == "__main__":
    unittest.main()
