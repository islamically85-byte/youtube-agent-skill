#!/usr/bin/env python3
"""Unit tests to validate plugin manifests and JSON schemas."""

import json
import os
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestManifests(unittest.TestCase):
    def test_claude_plugin_json(self):
        path = os.path.join(REPO_ROOT, ".claude-plugin", "plugin.json")
        self.assertTrue(os.path.exists(path))
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data.get("name"), "youtube-agent")
        self.assertEqual(data.get("version"), "2.0.0")
        self.assertIn("islamically85-byte", data.get("homepage", ""))
        self.assertIn("Jake Schincariol", data.get("author", {}).get("name", ""))

    def test_claude_marketplace_json(self):
        path = os.path.join(REPO_ROOT, ".claude-plugin", "marketplace.json")
        self.assertTrue(os.path.exists(path))
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data.get("name"), "youtube-agent-skill")
        self.assertGreaterEqual(len(data.get("plugins", [])), 1)

    def test_chatgpt_plugin_json(self):
        for subpath in ["plugin.json", os.path.join(".codex-plugin", "plugin.json")]:
            path = os.path.join(REPO_ROOT, "chatgpt", subpath)
            self.assertTrue(os.path.exists(path), f"Missing {path}")
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data.get("schema_version"), "v1")
            self.assertEqual(data.get("name_for_model"), "youtube_agent_studio")
            self.assertEqual(data.get("auth", {}).get("type"), "none")

    def test_json_schemas(self):
        schemas_dir = os.path.join(REPO_ROOT, "shared", "schemas")
        for f in os.listdir(schemas_dir):
            if f.endswith(".json"):
                full_path = os.path.join(schemas_dir, f)
                with open(full_path, "r", encoding="utf-8") as sf:
                    schema = json.load(sf)
                self.assertIn("$schema", schema)
                self.assertIn("properties", schema)


if __name__ == "__main__":
    unittest.main()
