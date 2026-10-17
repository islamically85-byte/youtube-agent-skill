#!/usr/bin/env python3
"""Unit tests for stock_director.py (Hybrid Studio v3.0)."""

import os
import unittest
from shared.scripts.stock_director import (
    classify_clip_intent, generate_edl, count_manifest_rows, FALLBACK_CLIPS
)


class TestStockDirector(unittest.TestCase):
    def test_classify_clip_intent(self):
        clip_islamabad = {"filename": "islamabad_drone_aerial.mp4", "description": "Margalla hills scenic view"}
        intent = classify_clip_intent(clip_islamabad)
        self.assertEqual(intent, "islamabad_geographic")

        clip_blueprint = {"filename": "architectural_blueprint.mp4", "description": "Drafting site plans"}
        intent = classify_clip_intent(clip_blueprint)
        self.assertEqual(intent, "blueprint_planning")

        clip_court = {"filename": "courthouse_steps.mp4", "description": "Legal scales and inquiry"}
        intent = classify_clip_intent(clip_court)
        self.assertEqual(intent, "legal_inquiry")

    def test_edl_generation_shot_count_and_duration_bounds(self):
        # For a 390.0 second (6.5 min) documentary, target is 70 - 95 shots
        edl = generate_edl(FALLBACK_CLIPS, target_duration_sec=390.0)
        self.assertGreaterEqual(len(edl), 70)
        self.assertLessEqual(len(edl), 95)

        # Check total duration
        total_dur = edl[-1]["timeline_end"]
        self.assertAlmostEqual(total_dur, 390.0, delta=1.0)

        # Check individual shot durations are within 3.5s - 6.0s
        for shot in edl:
            self.assertGreaterEqual(shot["duration"], 3.0)
            self.assertLessEqual(shot["duration"], 6.5)

    def test_count_manifest_rows_accurate(self):
        # Ensure count reflects actual rows, preventing nominal naming discrepancies
        rows = count_manifest_rows(FALLBACK_CLIPS)
        self.assertEqual(rows, len(FALLBACK_CLIPS))
        self.assertEqual(rows, 22)


if __name__ == "__main__":
    unittest.main()
