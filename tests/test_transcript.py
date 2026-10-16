#!/usr/bin/env python3
"""Unit tests for transcript parser and timing utilities."""

import os
import unittest
import sys

# Ensure shared scripts are on path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "shared", "scripts"))

from transcript import (
    parse_timestamp,
    format_timestamp,
    count_words,
    estimate_speech_duration,
    load_transcript,
    normalize_tokens,
)


class TestTranscriptParser(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.join(REPO_ROOT, "shared", "fixtures")
        self.srt_path = os.path.join(self.fixtures_dir, "sample_transcript.srt")
        self.vtt_path = os.path.join(self.fixtures_dir, "sample_transcript.vtt")
        self.whisper_path = os.path.join(self.fixtures_dir, "sample_whisper.json")
        self.urdu_path = os.path.join(self.fixtures_dir, "urdu_transcript.srt")

    def test_parse_timestamps(self):
        self.assertAlmostEqual(parse_timestamp("00:01:23.456"), 83.456)
        self.assertAlmostEqual(parse_timestamp("00:01:23,456"), 83.456)
        self.assertAlmostEqual(parse_timestamp("01:23.500"), 83.5)
        self.assertAlmostEqual(parse_timestamp("45.2"), 45.2)
        self.assertAlmostEqual(parse_timestamp("00:00:00.000 line:0% position:50%"), 0.0)
        self.assertEqual(parse_timestamp("invalid"), 0.0)

    def test_format_timestamps(self):
        self.assertEqual(format_timestamp(83.456, fmt="mmss"), "1:23")
        self.assertEqual(format_timestamp(3683.0, fmt="mmss"), "1:01:23")
        self.assertEqual(format_timestamp(83.456, fmt="srt"), "00:01:23,456")
        self.assertEqual(format_timestamp(83.456, fmt="vtt"), "00:01:23.456")

    def test_load_srt(self):
        cues = load_transcript(self.srt_path)
        self.assertEqual(len(cues), 6)
        self.assertEqual(cues[0][0], 0.0)
        self.assertEqual(cues[0][1], 3.5)
        self.assertIn("97% of creators", cues[0][2])

    def test_load_vtt_with_tags(self):
        cues = load_transcript(self.vtt_path)
        self.assertGreaterEqual(len(cues), 3)
        # Verify voice tag <v Host> was stripped
        self.assertFalse("<v" in cues[0][2])
        self.assertIn("Your first 30 seconds", cues[0][2])

    def test_load_whisper_json(self):
        cues = load_transcript(self.whisper_path)
        self.assertEqual(len(cues), 4)
        self.assertAlmostEqual(cues[0][0], 0.0)
        self.assertAlmostEqual(cues[0][1], 3.8)

    def test_unicode_urdu_support(self):
        cues = load_transcript(self.urdu_path)
        self.assertEqual(len(cues), 4)
        # Ensure Urdu characters are preserved without corruption
        self.assertIn("جذبات", cues[0][2])
        tokens = normalize_tokens(cues[0][2])
        self.assertGreater(len(tokens), 5)
        # Speech duration estimate for Urdu (~130 WPM)
        duration_est = estimate_speech_duration(cues[0][2], language="ur")
        self.assertGreater(duration_est, 2.0)

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_transcript("non_existent_file.srt")


if __name__ == "__main__":
    unittest.main()
