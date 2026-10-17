#!/usr/bin/env python3
"""Unit tests for render_free.py."""

import json
import os
import unittest

from shared.scripts.render_free import (
    build_ffmpeg_command,
    escape_ffmpeg_filter_path,
    find_ffmpeg
)


class TestRenderFree(unittest.TestCase):
    def test_escape_ffmpeg_filter_path(self):
        # Test backslash and colon escaping (Windows drive compatibility)
        p = r"C:\Users\Creator\Assets\subtitle:file's.srt"
        esc = escape_ffmpeg_filter_path(p)
        self.assertNotIn("\\U", esc)
        self.assertIn(r"\:", esc)
        self.assertIn(r"\'", esc)

    def test_build_ffmpeg_command(self):
        manifest = {
            "project_id": "test_cmd_01",
            "title": "Command Test",
            "target_duration_sec": 6.0,
            "footage_clips": [
                {
                    "id": "c1",
                    "source_url_or_path": "clip1.mp4",
                    "timeline_in_sec": 0.0,
                    "timeline_out_sec": 3.0
                },
                {
                    "id": "c2",
                    "source_url_or_path": "clip2.mp4",
                    "timeline_in_sec": 3.0,
                    "timeline_out_sec": 6.0
                }
            ],
            "audio": {
                "narration": {
                    "file_path": "narration.wav",
                    "target_lufs": -14.0
                },
                "background_music": {
                    "file_path": "music.mp3",
                    "ducking_level_db": -24.0
                }
            },
            "render_target": {
                "output_path": "output.mp4",
                "resolution": "1920x1080",
                "fps": 30,
                "video_codec": "libx264",
                "audio_codec": "aac"
            }
        }

        cmd, out_path = build_ffmpeg_command(manifest, manifest_dir="/tmp")
        cmd_str = " ".join(cmd)

        self.assertIn("-filter_complex", cmd)
        self.assertIn("loudnorm", cmd_str)
        self.assertIn("amix", cmd_str)
        self.assertIn("concat", cmd_str)
        self.assertIn("-c:v", cmd)
        self.assertIn("libx264", cmd)
        self.assertIn("aac", cmd)
        self.assertTrue(out_path.endswith("output.mp4"))


if __name__ == "__main__":
    unittest.main()
