#!/usr/bin/env python3
"""Unit tests for qa_media.py."""

import os
import unittest

from shared.scripts.qa_media import parse_framerate, run_qa

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYNTHETIC_DEMO_MP4 = os.path.join(REPO_ROOT, "shared", "fixtures", "synthetic_demo", "synthetic_rendered_demo.mp4")
DEMO_MANIFEST = os.path.join(REPO_ROOT, "shared", "fixtures", "synthetic_demo", "demo_manifest.json")


class TestQAMedia(unittest.TestCase):
    def test_parse_framerate(self):
        self.assertEqual(parse_framerate("30/1"), 30.0)
        self.assertAlmostEqual(parse_framerate("24000/1001"), 23.976, places=2)
        self.assertEqual(parse_framerate("60"), 60.0)

    def test_missing_file_returns_failed_critical(self):
        report = run_qa("/non_existent_media_xyz.mp4")
        self.assertEqual(report["status"], "FAILED_CRITICAL_CHECKS")
        self.assertEqual(len(report["mandatory_human_review_items"]), 5)

    def test_synthetic_demo_video_qa(self):
        if not os.path.exists(SYNTHETIC_DEMO_MP4):
            self.skipTest("Synthetic demo MP4 not present")

        report = run_qa(SYNTHETIC_DEMO_MP4, manifest_path=DEMO_MANIFEST)
        self.assertEqual(report["status"], "TECHNICALLY_VALID_PENDING_REVIEW")
        metrics = report["probed_metrics"]
        self.assertEqual(metrics["resolution"], "1920x1080")
        self.assertEqual(metrics["aspect_ratio"], "16:9")
        self.assertEqual(metrics["duration_sec"], 4.0)
        self.assertEqual(metrics["video_codec"], "h264")
        self.assertEqual(metrics["audio_codec"], "aac")

        checks = report["automated_checks"]
        self.assertTrue(checks["black_frames"]["passed"])
        self.assertTrue(checks["audio_loudness"]["passed"])
        self.assertTrue(checks["license_compliance"]["passed"])
        self.assertEqual(len(report["mandatory_human_review_items"]), 5)


if __name__ == "__main__":
    unittest.main()
