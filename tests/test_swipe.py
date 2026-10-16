#!/usr/bin/env python3
"""Unit tests for competitor outlier analysis."""

import os
import unittest
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "shared", "scripts"))

from swipe import parse_views_count, analyze_outliers


class TestSwipe(unittest.TestCase):
    def test_parse_views_variations(self):
        self.assertEqual(parse_views_count(45000), 45000.0)
        self.assertEqual(parse_views_count("45,000"), 45000.0)
        self.assertEqual(parse_views_count("45.5K"), 45500.0)
        self.assertEqual(parse_views_count("1.2M"), 1200000.0)
        self.assertEqual(parse_views_count("invalid"), 0.0)
        self.assertEqual(parse_views_count(None), 0.0)

    def test_outlier_multiple_calculation(self):
        videos = [
            {"channel": "TechTest", "title": "Outlier Video", "views": 200000},
            {"channel": "TechTest", "title": "Normal Video 1", "views": 20000},
            {"channel": "TechTest", "title": "Normal Video 2", "views": 22000},
            {"channel": "TechTest", "title": "Normal Video 3", "views": 21000},
        ]
        res = analyze_outliers(videos, min_multiple=2.0, min_channel_samples=4)
        self.assertEqual(res["outlier_count"], 1)
        outlier = res["outliers"][0]
        self.assertEqual(outlier["title"], "Outlier Video")
        self.assertGreaterEqual(outlier["multiple"], 9.0)

    def test_thin_channel_skipped(self):
        videos = [
            {"channel": "ThinChannel", "title": "Video 1", "views": 10000},
            {"channel": "ThinChannel", "title": "Video 2", "views": 50000},
        ]
        res = analyze_outliers(videos, min_channel_samples=4)
        self.assertEqual(len(res["thin_channels_skipped"]), 1)
        self.assertEqual(res["thin_channels_skipped"][0]["channel"], "ThinChannel")
        self.assertEqual(res["outlier_count"], 0)


if __name__ == "__main__":
    unittest.main()
