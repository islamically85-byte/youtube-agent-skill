#!/usr/bin/env python3
"""Unit tests for deterministic browser motion engine."""

import os
import unittest
from pathlib import Path
from shared.scripts.browser_motion import (
    find_system_browser,
    find_ffmpeg,
    get_aspect_dimensions,
    render_html_motion,
)

ROOT_DIR = Path(__file__).resolve().parent.parent


class TestBrowserMotion(unittest.TestCase):
    def test_get_aspect_dimensions(self):
        w, h = get_aspect_dimensions("16:9")
        self.assertEqual((w, h), (1920, 1080))

        w, h = get_aspect_dimensions("9:16")
        self.assertEqual((w, h), (1080, 1920))

        w, h = get_aspect_dimensions("1:1")
        self.assertEqual((w, h), (1080, 1080))

        w, h = get_aspect_dimensions("custom", 1280, 720)
        self.assertEqual((w, h), (1280, 720))

    def test_find_system_browser(self):
        browser = find_system_browser()
        self.assertIsNotNone(browser, "Headless browser should be detected in test environment")
        self.assertTrue(os.path.exists(browser), f"Browser path does not exist: {browser}")

    def test_find_ffmpeg(self):
        ffmpeg = find_ffmpeg()
        self.assertIsNotNone(ffmpeg, "FFmpeg should be detected in test environment")
        self.assertTrue(os.path.exists(ffmpeg), f"FFmpeg path does not exist: {ffmpeg}")

    def test_discrepancy_counter_template_exists(self):
        template = ROOT_DIR / "templates" / "motion" / "discrepancy_counter.html"
        self.assertTrue(template.exists(), "discrepancy_counter.html template must exist")
        content = template.read_text(encoding="utf-8")
        self.assertIn("renderFrame", content)
        self.assertIn("42,000", content)
        self.assertIn("6,000", content)
        self.assertIn("حتمی عدالتی فیصلہ نہیں", content)

    def test_quick_render_motion_clip(self):
        """Render a 0.5s (15 frames) motion clip to test the complete pipeline."""
        out_dir = ROOT_DIR / "output" / "test_motion"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_mp4 = out_dir / "quick_test_15f.mp4"

        template = ROOT_DIR / "templates" / "motion" / "discrepancy_counter.html"
        res = render_html_motion(
            html_path=str(template),
            output_path=str(out_mp4),
            duration=0.5,
            fps=30,
            generate_contact_sheet=False,
            generate_previews=False,
        )

        self.assertEqual(res["status"], "success")
        self.assertTrue(out_mp4.exists(), "Rendered MP4 file must exist on disk")
        self.assertGreater(out_mp4.stat().st_size, 1000, "Rendered MP4 file should have non-trivial size")
        self.assertEqual(res["total_frames"], 15)
        self.assertEqual(res["maintainer"], "ABDUL MUEED LASHARY")


if __name__ == "__main__":
    unittest.main()
