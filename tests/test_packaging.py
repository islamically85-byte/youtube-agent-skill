#!/usr/bin/env python3
"""Unit tests to validate release packaging and zip archive integrity."""

import os
import subprocess
import sys
import unittest
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestPackaging(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Execute release packaging script
        script_path = os.path.join(REPO_ROOT, "scripts", "build-releases.py")
        subprocess.check_call([sys.executable, script_path], cwd=REPO_ROOT)

    def test_release_archives_exist(self):
        release_dir = os.path.join(REPO_ROOT, "release")
        expected_zips = [
            "youtube-agent-claude.zip",
            "youtube-agent-chatgpt-skill.zip",
            "youtube-agent-chatgpt-plugin.zip",
        ]
        for name in expected_zips:
            zip_path = os.path.join(release_dir, name)
            self.assertTrue(os.path.exists(zip_path), f"Missing release archive: {name}")
            self.assertGreater(os.path.getsize(zip_path), 5000, f"Zip file {name} is unusually small")

            # Verify zip archive integrity
            with zipfile.ZipFile(zip_path, "r") as zf:
                bad_file = zf.testzip()
                self.assertIsNone(bad_file, f"Corrupted zip entry found in {name}: {bad_file}")


if __name__ == "__main__":
    unittest.main()
