#!/usr/bin/env python3
"""Unit tests for OpenTimelineIO multi-track NLE timeline generator."""

import os
import unittest
from pathlib import Path
from shared.scripts.otio_export import (
    HAS_OTIO,
    build_otio_timeline,
    load_manifest_clips,
)

ROOT_DIR = Path(__file__).resolve().parent.parent


class TestOtioExport(unittest.TestCase):
    def test_otio_availability(self):
        self.assertIn(HAS_OTIO, [True, False])

    @unittest.skipUnless(HAS_OTIO, "OpenTimelineIO library not installed")
    def test_build_multi_track_timeline(self):
        out_dir = ROOT_DIR / "output" / "test_otio"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_otio = out_dir / "test_documentary.otio"

        sample_clips = [
            {"clip_name": "Shot_01_Aerial", "duration_sec": 4.5, "file_path": "/media/shot1.mp4", "intent": "aerial"},
            {"clip_name": "Shot_02_Documents", "duration_sec": 3.0, "file_path": "/media/shot2.mp4", "intent": "investigation"},
        ]
        sample_motion = [{"name": "Motion_Overlay", "path": "/media/motion.mp4", "duration_sec": 7.5}]
        sample_blender = [{"name": "Blender_3D", "path": "/media/blender.mp4", "duration_sec": 4.0}]

        tl = build_otio_timeline(
            name="Test Documentary Timeline",
            fps=30,
            clips=sample_clips,
            motion_overlays=sample_motion,
            blender_3d_clips=sample_blender,
            voice_track_path="/media/voice.wav",
            music_track_path="/media/music.wav",
            output_path=str(out_otio),
        )

        self.assertIsNotNone(tl)
        self.assertEqual(len(tl.tracks), 5, "Timeline should contain 5 tracks (3 video, 2 audio)")
        self.assertTrue(out_otio.exists(), "Exported .otio file must exist on disk")
        self.assertGreater(out_otio.stat().st_size, 100)

    @unittest.skipUnless(HAS_OTIO, "OpenTimelineIO library not installed")
    def test_export_edl_fallback(self):
        out_dir = ROOT_DIR / "output" / "test_otio"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_edl = out_dir / "test_documentary.edl"

        sample_clips = [
            {"clip_name": "Shot_01", "duration_sec": 5.0, "file_path": "/media/shot1.mp4"},
            {"clip_name": "Shot_02", "duration_sec": 5.0, "file_path": "/media/shot2.mp4"},
        ]

        tl = build_otio_timeline(
            name="EDL Test Timeline",
            fps=30,
            clips=sample_clips,
            output_path=str(out_edl),
        )

        self.assertTrue(out_edl.exists(), "Exported .edl file must exist on disk")
        content = out_edl.read_text(encoding="utf-8")
        self.assertIn("TITLE: EDL Test Timeline", content)
        self.assertIn("FCM: NON-DROP FRAME", content)


if __name__ == "__main__":
    unittest.main()
