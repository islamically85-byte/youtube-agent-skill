#!/usr/bin/env python3
"""Unit tests for urdu_voice_engine.py (Hybrid Studio v3.0)."""

import unittest
from shared.scripts.urdu_voice_engine import (
    evaluate_test_passage, normalize_urdu_text, chunk_narration_sentences,
    format_srt_timestamp, REQUIRED_BENCHMARK_KEYWORDS
)


class TestUrduVoiceEngine(unittest.TestCase):
    def test_test_passage_benchmark_passes(self):
        result = evaluate_test_passage()
        self.assertTrue(result["benchmark_passed"])
        self.assertEqual(len(result["missing_keywords"]), 0)
        self.assertTrue(result["requires_human_listening_review"])
        self.assertGreaterEqual(result["word_count"], 30)
        self.assertLessEqual(result["word_count"], 65)
        self.assertGreaterEqual(result["measured_duration_sec"], 20.0)
        self.assertLessEqual(result["measured_duration_sec"], 40.0)

    def test_required_benchmark_keywords_coverage(self):
        for kw in [
            "بیالیس ہزار فائلیں",
            "چھ ہزار پلاٹ",
            "چھتیس ہزار",
            "اسلام آباد",
            "کوآپریٹو ہاؤسنگ سوسائٹی",
            "سی ڈی اے",
            "این او سی"
        ]:
            self.assertIn(kw, REQUIRED_BENCHMARK_KEYWORDS)

    def test_numeral_and_acronym_normalization(self):
        sample = "CDA and SECP investigated 42,000 files vs 6,000 plots and 36,000 victims without NOC."
        normalized = normalize_urdu_text(sample)
        self.assertIn("سی ڈی اے", normalized)
        self.assertIn("ایس ای سی پی", normalized)
        self.assertIn("بیالیس ہزار", normalized)
        self.assertIn("چھ ہزار", normalized)
        self.assertIn("چھتیس ہزار", normalized)
        self.assertIn("این او سی", normalized)

    def test_sentence_chunking_filters_cues_and_comments(self):
        script = """# Legal Disclaimer
[ACT 1: HOOK]
فرض کیجیے، زندگی بھر کی جمع پونجی سے خریدی گئی فائل آپ کے پاس ہو۔
[CUE: Drone Shot]
مگر جب آپ موقع پر پہنچیں، تو وہاں سوائے بنجر زمین کے کچھ بھی نہ ہو۔"""
        chunks = chunk_narration_sentences(script)
        self.assertEqual(len(chunks), 2)
        for c in chunks:
            self.assertFalse(c.startswith("#"))
            self.assertFalse(c.startswith("["))

    def test_format_srt_timestamp(self):
        self.assertEqual(format_srt_timestamp(0.0), "00:00:00,000")
        self.assertEqual(format_srt_timestamp(65.5), "00:01:05,500")
        self.assertEqual(format_srt_timestamp(3600.125), "01:00:00,125")


if __name__ == "__main__":
    unittest.main()
