#!/usr/bin/env python3
"""Unit tests for YouTube chapter rules validation and generation."""

import os
import unittest
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "shared", "scripts"))

from chapters import validate_chapter_list, parse_raw_chapter_text, generate_chapters


class TestChapters(unittest.TestCase):
    def test_valid_youtube_chapters(self):
        valid_text = (
            "00:00 Introduction\n"
            "01:30 The Problem\n"
            "04:15 The System\n"
            "08:00 Conclusion"
        )
        chapters = parse_raw_chapter_text(valid_text)
        is_valid, errors = validate_chapter_list(chapters)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(chapters), 4)

    def test_invalid_first_timestamp_nonzero(self):
        invalid_text = (
            "00:15 Introduction\n"
            "01:30 The Problem\n"
            "04:15 The System"
        )
        chapters = parse_raw_chapter_text(invalid_text)
        is_valid, errors = validate_chapter_list(chapters)
        self.assertFalse(is_valid)
        self.assertTrue(any("start at 00:00" in e for e in errors))

    def test_invalid_fewer_than_three_chapters(self):
        invalid_text = (
            "00:00 Part 1\n"
            "05:00 Part 2"
        )
        chapters = parse_raw_chapter_text(invalid_text)
        is_valid, errors = validate_chapter_list(chapters)
        self.assertFalse(is_valid)
        self.assertTrue(any("at least 3 chapters" in e for e in errors))

    def test_invalid_chapter_shorter_than_ten_seconds(self):
        invalid_text = (
            "00:00 Intro\n"
            "00:05 Hook\n"
            "02:00 Main Topic"
        )
        chapters = parse_raw_chapter_text(invalid_text)
        is_valid, errors = validate_chapter_list(chapters)
        self.assertFalse(is_valid)
        self.assertTrue(any("10-second minimum" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
