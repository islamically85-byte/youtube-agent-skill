#!/usr/bin/env python3
"""Unit tests for validate_manifest.py."""

import copy
import json
import os
import tempfile
import unittest

from shared.scripts.validate_manifest import validate_manifest_data

SAMPLE_VALID_MANIFEST = {
    "project_id": "test_proj_001",
    "title": "Documentary Test Project",
    "target_duration_sec": 10.0,
    "aspect_ratio": "16:9",
    "credit_budget": 0,
    "footage_clips": [
        {
            "id": "clip_1",
            "source_type": "pexels",
            "source_url_or_path": "https://www.pexels.com/video/12345",
            "license_class": "Pexels License",
            "license_verified_date": "2026-10-16",
            "clip_duration_sec": 5.0,
            "timeline_in_sec": 0.0,
            "timeline_out_sec": 5.0
        },
        {
            "id": "clip_2",
            "source_type": "pixabay",
            "source_url_or_path": "https://pixabay.com/videos/67890",
            "license_class": "Pixabay License",
            "license_verified_date": "2026-10-16",
            "clip_duration_sec": 5.0,
            "timeline_in_sec": 5.0,
            "timeline_out_sec": 10.0
        }
    ],
    "audio": {
        "narration": {
            "file_path": "audio/narration.wav",
            "language": "ur",
            "script_format": "urdu_nastaliq",
            "target_lufs": -14.0
        }
    },
    "render_target": {
        "output_path": "exports/test.mp4",
        "resolution": "1920x1080",
        "fps": 30
    }
}


class TestValidateManifest(unittest.TestCase):
    def test_valid_manifest(self):
        valid, errors, warnings = validate_manifest_data(SAMPLE_VALID_MANIFEST, check_files=False)
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)

    def test_missing_required_fields(self):
        bad = copy.deepcopy(SAMPLE_VALID_MANIFEST)
        del bad["project_id"]
        del bad["footage_clips"]
        valid, errors, _ = validate_manifest_data(bad, check_files=False)
        self.assertFalse(valid)
        self.assertTrue(any("project_id" in e for e in errors))
        self.assertTrue(any("footage_clips" in e for e in errors))

    def test_credit_budget_violation(self):
        bad = copy.deepcopy(SAMPLE_VALID_MANIFEST)
        bad["credit_budget"] = 25  # Free-first violation
        valid, errors, _ = validate_manifest_data(bad, check_files=False)
        self.assertFalse(valid)
        self.assertTrue(any("Credit budget violation" in e for e in errors))

    def test_invalid_license_class(self):
        bad = copy.deepcopy(SAMPLE_VALID_MANIFEST)
        bad["footage_clips"][0]["license_class"] = "Pirated / Unlicensed Web Rip"
        valid, errors, _ = validate_manifest_data(bad, check_files=False)
        self.assertFalse(valid)
        self.assertTrue(any("unrecognized license_class" in e for e in errors))

    def test_invalid_timeline_order(self):
        bad = copy.deepcopy(SAMPLE_VALID_MANIFEST)
        bad["footage_clips"][0]["timeline_in_sec"] = 8.0
        bad["footage_clips"][0]["timeline_out_sec"] = 4.0
        valid, errors, _ = validate_manifest_data(bad, check_files=False)
        self.assertFalse(valid)
        self.assertTrue(any("must be greater than timeline_in_sec" in e for e in errors))

    def test_check_files_fails_when_missing(self):
        manifest = copy.deepcopy(SAMPLE_VALID_MANIFEST)
        manifest["footage_clips"][0]["source_type"] = "local"
        manifest["footage_clips"][0]["source_url_or_path"] = "non_existent_file_xyz_123.mp4"
        valid, errors, _ = validate_manifest_data(manifest, check_files=True)
        self.assertFalse(valid)
        self.assertTrue(any("file not found" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
