#!/usr/bin/env python3
"""Unit tests for audio_manager.py (Hybrid Studio v3.0)."""

import unittest
from shared.scripts.audio_manager import (
    generate_youtube_chapters, create_audio_metadata,
    DEFAULT_TARGET_LUFS, DEFAULT_DUCKING_DB
)


class TestAudioManager(unittest.TestCase):
    def test_default_constants(self):
        self.assertEqual(DEFAULT_TARGET_LUFS, -14.0)
        self.assertEqual(DEFAULT_DUCKING_DB, -24.0)

    def test_generate_youtube_chapters_timestamps(self):
        chapters = generate_youtube_chapters(total_duration_sec=390.0)
        self.assertEqual(len(chapters), 7)
        self.assertEqual(chapters[0]["time"], "00:00")
        self.assertIn("الزامات", chapters[0]["title"])
        self.assertIn("سی ڈی اے", chapters[3]["title"])
        self.assertIn("چار نکاتی", chapters[4]["title"])

    def test_metadata_records_missing_music_warning(self):
        meta = create_audio_metadata(
            total_duration_sec=390.0,
            music_present=False
        )
        self.assertFalse(meta["music_present"])
        self.assertEqual(meta["missing_music_warning"], "MISSING_MUSIC_WARNING")
        self.assertEqual(meta["voice_lufs"], -14.0)
        self.assertEqual(meta["music_attenuation_db"], -24.0)

    def test_metadata_when_music_present(self):
        meta = create_audio_metadata(
            total_duration_sec=390.0,
            music_present=True
        )
        self.assertTrue(meta["music_present"])
        self.assertIsNone(meta["missing_music_warning"])


if __name__ == "__main__":
    unittest.main()
