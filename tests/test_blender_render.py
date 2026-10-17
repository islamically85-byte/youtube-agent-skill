#!/usr/bin/env python3
"""Unit tests for Blender 3D land parcel visualization engine."""

import os
import unittest
from pathlib import Path
from shared.scripts.blender_parcel_render import find_blender, run_blender_scene

ROOT_DIR = Path(__file__).resolve().parent.parent


class TestBlenderRender(unittest.TestCase):
    def test_find_blender(self):
        blender = find_blender()
        if blender:
            self.assertTrue(os.path.exists(blender), f"Blender path does not exist: {blender}")
        else:
            self.assertIsNone(blender, "When Blender is absent, find_blender returns None")

    @unittest.skipUnless(find_blender(), "Blender LTS not installed in environment")
    def test_render_blender_parcel_still(self):
        """Test rendering a single frame of the 3D procedural parcel scene."""
        out_dir = ROOT_DIR / "output" / "test_blender"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_png = out_dir / "test_parcel_still.png"

        res = run_blender_scene(
            output_path=str(out_png),
            frames=10,
            fps=30,
            width=640,
            height=360,
        )

        self.assertEqual(res["status"], "success")
        self.assertTrue(out_png.exists(), "Rendered PNG still must exist")
        self.assertGreater(out_png.stat().st_size, 5000, "Rendered PNG file should have non-trivial size")
        self.assertEqual(res["maintainer"], "ABDUL MUEED LASHARY")


if __name__ == "__main__":
    unittest.main()
