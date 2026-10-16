#!/usr/bin/env python3
"""Unit tests for credit_guard.py."""

import unittest

from shared.scripts.credit_guard import check_credit_authorization


class TestCreditGuard(unittest.TestCase):
    def test_zero_credit_operation_allowed_by_default(self):
        auth, msg, details = check_credit_authorization(tool="local_tools", cost=0, budget=0)
        self.assertTrue(auth)
        self.assertIn("0 credits", msg)

    def test_vidiq_call_blocked_without_consent(self):
        auth, msg, details = check_credit_authorization(tool="vidiq", action="competitor_research", budget=0, consent=False)
        self.assertFalse(auth)
        self.assertIn("BLOCKED", msg)
        self.assertIn("5 credits", msg)
        self.assertIn("free_alternative", details)

    def test_insufficient_balance_blocked_even_with_consent(self):
        # Connected vidIQ account with 2 remaining credits vs 5 cost
        auth, msg, details = check_credit_authorization(
            tool="vidiq", action="competitor_research",
            cost=5, budget=5, balance=2, consent=True
        )
        self.assertFalse(auth)
        self.assertIn("EXHAUSTED", msg)
        self.assertIn("only 2 credits", msg)

    def test_authorized_when_consent_and_balance_sufficient(self):
        auth, msg, details = check_credit_authorization(
            tool="vidiq", action="competitor_research",
            cost=5, budget=10, balance=15, consent=True
        )
        self.assertTrue(auth)
        self.assertIn("authorized", msg.lower())

    def test_cost_exceeding_budget_blocked(self):
        auth, msg, details = check_credit_authorization(
            tool="elevenlabs", action="default",
            cost=10, budget=5, balance=100, consent=True
        )
        self.assertFalse(auth)
        self.assertIn("OVER-BUDGET", msg)


if __name__ == "__main__":
    unittest.main()
