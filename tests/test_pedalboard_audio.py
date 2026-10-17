#!/usr/bin/env python3
"""Unit tests for broadcast voice mastering and sidechain ducking engine."""

import os
import subprocess
import unittest
from pathlib import Path
from shared.scripts.pedalboard_master import (
    HAS_PEDALBOARD,
    master_voice_track,
    mix_voice_and_music_with_ducking,
    process_voice_ffmpeg_fallback,
)

ROOT_DIR = Path(__file__).resolve().parent.parent


class TestPedalboardAudio(unittest.TestCase):
    def setUp(self):
        self.test_dir = ROOT_DIR / "output" / "test_audio"
        self.test_dir.mkdir(parents=True, exist_ok=True)

        self.voice_raw = self.test_dir / "raw_voice.wav"
        self.music_raw = self.test_dir / "raw_music.wav"

        # Generate 2 seconds of 440Hz test sine tone
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "sine=frequency=440:duration=2",
            "-ar", "48000", str(self.voice_raw)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Generate 3 seconds of 220Hz test sine tone
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "sine=frequency=220:duration=3",
            "-ar", "48000", str(self.music_raw)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    def test_pedalboard_availability(self):
        self.assertIn(HAS_PEDALBOARD, [True, False])

    @unittest.skipUnless(HAS_PEDALBOARD, "Spotify Pedalboard library not installed")
    def test_master_voice_hybrid_pedalboard(self):
        out_master = self.test_dir / "voice_mastered.wav"
        res = master_voice_track(str(self.voice_raw), str(out_master), target_lufs=-14.0, peak_ceiling_db=-1.5)

        self.assertEqual(res["status"], "success")
        self.assertTrue(out_master.exists())
        self.assertGreater(out_master.stat().st_size, 1000)
        self.assertEqual(res["voice_lufs"], -14.0)
        self.assertEqual(res["maintainer"], "ABDUL MUEED LASHARY")

    def test_master_voice_ffmpeg_fallback(self):
        out_master = self.test_dir / "voice_mastered_ffmpeg.wav"
        res = master_voice_track(str(self.voice_raw), str(out_master), target_lufs=-14.0, force_ffmpeg=True)

        self.assertEqual(res["status"], "success")
        self.assertTrue(out_master.exists())
        self.assertEqual(res["engine"], "ffmpeg_filter_chain")

    def test_sidechain_ducking_mix(self):
        out_mix = self.test_dir / "ducked_mix.wav"
        res = mix_voice_and_music_with_ducking(
            voice_audio=str(self.voice_raw),
            music_audio=str(self.music_raw),
            output_audio=str(out_mix),
            ducking_db=-24.0,
            target_lufs=-14.0,
        )

        self.assertEqual(res["status"], "success")
        self.assertTrue(out_mix.exists())
        self.assertEqual(res["ducking_db"], -24.0)
        self.assertEqual(res["maintainer"], "ABDUL MUEED LASHARY")


if __name__ == "__main__":
    unittest.main()
