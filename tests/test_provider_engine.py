#!/usr/bin/env python3
"""Unit tests for provider_engine.py (Hybrid Studio v3.0)."""

import unittest
from shared.scripts.provider_engine import ProviderEngine, ProviderState


class TestProviderEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ProviderEngine(credit_budget=0)

    def test_default_credit_budget_is_zero(self):
        self.assertEqual(self.engine.credit_budget, 0)
        self.assertEqual(self.engine.credits_spent, 0)

    def test_unsupported_language_falls_back_to_piper(self):
        # Even if a provider was available, if it lacks Urdu support, voiceover falls back to piper or human
        plan = self.engine.resolve_pipeline_plan(language="ur", duration_target_sec=390.0)
        self.assertIn(plan["voiceover_provider"].lower(), ["piper_urdu", "human_voice"])
        self.assertIn("ffmpeg", plan["render_engine"].lower())

    def test_credit_deduction_fails_when_budget_exceeded(self):
        success = self.engine.spend_credits("paid_ai_api", 5)
        self.assertFalse(success)
        self.assertEqual(self.engine.credits_spent, 0)

    def test_credit_deduction_succeeds_when_budget_authorized(self):
        engine_funded = ProviderEngine(credit_budget=20)
        success = engine_funded.spend_credits("paid_ai_api", 5)
        self.assertTrue(success)
        self.assertEqual(engine_funded.credits_spent, 5)
        self.assertEqual(engine_funded.remaining_credits(), 15)

    def test_decision_ledger_records_routing(self):
        self.engine.resolve_pipeline_plan(language="ur", duration_target_sec=390.0)
        ledger = self.engine.get_decision_ledger()
        self.assertGreaterEqual(len(ledger), 5)
        task_types = [entry["task"] for entry in ledger]
        self.assertIn("scriptwriting", task_types)
        self.assertIn("voiceover", task_types)
        self.assertIn("video_rendering", task_types)


if __name__ == "__main__":
    unittest.main()
