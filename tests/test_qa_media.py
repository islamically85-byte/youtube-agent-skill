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
        import shutil
        if not os.path.exists(SYNTHETIC_DEMO_MP4):
            self.skipTest("Synthetic demo MP4 not present")
        if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
            self.skipTest("ffmpeg/ffprobe not installed in environment")

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

    def test_duration_bounds_failure_when_below_min(self):
        import shutil
        if not os.path.exists(SYNTHETIC_DEMO_MP4) or not shutil.which("ffprobe"):
            self.skipTest("Synthetic demo or ffprobe missing")

        # Demo is 4.0s. Requiring min 360.0s (e.g. 6-7 min documentary) MUST fail!
        report = run_qa(SYNTHETIC_DEMO_MP4, min_duration=360.0, max_duration=420.0)
        self.assertEqual(report["status"], "FAILED_CRITICAL_CHECKS")
        self.assertFalse(report["automated_checks"]["duration_bounds"]["passed"])
        self.assertIn("below minimum requirement", report["verdict_summary"])

    def test_duration_bounds_success_when_within_range(self):
        import shutil
        if not os.path.exists(SYNTHETIC_DEMO_MP4) or not shutil.which("ffprobe"):
            self.skipTest("Synthetic demo or ffprobe missing")

        report = run_qa(SYNTHETIC_DEMO_MP4, min_duration=2.0, max_duration=10.0)
        self.assertEqual(report["status"], "TECHNICALLY_VALID_PENDING_REVIEW")
        self.assertTrue(report["automated_checks"]["duration_bounds"]["passed"])

    def test_require_music_check_with_warning(self):
        import shutil
        if not os.path.exists(SYNTHETIC_DEMO_MP4) or not shutil.which("ffprobe"):
            self.skipTest("Synthetic demo or ffprobe missing")

        # Create temporary manifest with missing music warning
        import tempfile, json
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
            json.dump({"project_id": "test", "warnings": ["MISSING_MUSIC_WARNING"], "music_present": False}, tf)
            t_path = tf.name

        try:
            report = run_qa(SYNTHETIC_DEMO_MP4, manifest_path=t_path, require_music=True)
            self.assertEqual(report["status"], "FAILED_CRITICAL_CHECKS")
            self.assertIn("music", report["verdict_summary"].lower())
        finally:
            if os.path.exists(t_path):
                os.remove(t_path)


if __name__ == "__main__":
    unittest.main()
