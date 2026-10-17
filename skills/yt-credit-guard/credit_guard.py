#!/usr/bin/env python3
"""credit_guard.py - Zero-credit quota guard and paid-service access controller.

Enforces the project's free-first rule:
- Default budget is 0 credits.
- Blocks unapproved calls to paid/metered tools (e.g. vidIQ, ElevenLabs, OpenAI DALL-E, paid APIs).
- Detects depleted third-party quotas (e.g. vidIQ 2/150 credits remaining vs 5 credits required).
- Requires explicit user consent before any metered charge can proceed.
- Provides fallback to offline, zero-credit alternatives.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional, Tuple

# Known metered tools and standard operation costs
DEFAULT_TOOL_COSTS: Dict[str, Dict[str, int]] = {
    "vidiq": {
        "competitor_research": 5,
        "keyword_expansion": 5,
        "daily_ideas": 5,
        "ai_thumbnail": 15,
        "ai_title_generator": 5,
        "default": 5
    },
    "elevenlabs": {
        "voice_synthesis_per_min": 10,
        "default": 10
    },
    "openai_dalle": {
        "generate_image": 10,
        "default": 10
    }
}

# Free-first alternatives mapping
FREE_ALTERNATIVES: Dict[str, str] = {
    "vidiq": "Use local offline yt-seo, yt-package, yt-audit, and manual YouTube search/autocomplete.",
    "elevenlabs": "Use human-recorded voiceover (preferred) or permissive offline open TTS benchmark.",
    "openai_dalle": "Use verified stock footage/stills from Pexels, Pixabay, Mixkit, or procedural motion graphics.",
    "paid_music": "Use YouTube Audio Library (Royalty-free, commercial use allowed) or Mixkit Free License."
}


def check_credit_authorization(
    tool: str,
    action: str = "default",
    cost: Optional[int] = None,
    budget: int = 0,
    balance: Optional[int] = None,
    consent: bool = False
) -> Tuple[bool, str, Dict[str, Any]]:
    """Determine whether a metered tool call is authorized under zero-credit rules.
    
    Returns (authorized, message, details).
    """
    tool_key = tool.lower().replace(" ", "_").replace("-", "_")
    tool_actions = DEFAULT_TOOL_COSTS.get(tool_key, {})
    
    if cost is None:
        cost = tool_actions.get(action, tool_actions.get("default", 0))

    details: Dict[str, Any] = {
        "tool": tool,
        "action": action,
        "requested_cost_credits": cost,
        "credit_budget": budget,
        "available_balance": balance,
        "consent_granted": consent,
        "free_alternative": FREE_ALTERNATIVES.get(tool_key, "Use local offline workflows.")
    }

    # If the operation costs 0 credits, it is completely free
    if cost <= 0:
        return True, "Operation requires 0 credits (free/offline-capable).", details

    # If the user has not explicitly consented to paid credits
    if not consent:
        msg = (
            f"🚫 [CREDIT-GUARD BLOCKED] Operation '{action}' on '{tool}' requires {cost} credits, "
            f"but current budget is {budget} credits and explicit user consent was not provided.\n"
            f"Free-first alternative: {details['free_alternative']}\n"
            f"To proceed with paid credits, the user must explicitly approve with --consent yes."
        )
        return False, msg, details

    # If user consented, check if balance is provided and sufficient
    if balance is not None and balance < cost:
        msg = (
            f"❌ [CREDIT-GUARD EXHAUSTED] Quota insufficient for '{tool}'. "
            f"Requested: {cost} credits, but current live balance is only {balance} credits. "
            f"Free-first alternative: {details['free_alternative']}"
        )
        return False, msg, details

    # If budget is lower than cost even after consent
    if budget < cost:
        msg = (
            f"⚠️ [CREDIT-GUARD OVER-BUDGET] Operation costs {cost} credits, which exceeds budget of {budget} credits. "
            f"Requires explicit budget adjustment."
        )
        return False, msg, details

    return True, f"✅ Operation authorized with explicit consent ({cost} credits deducted from budget).", details


def main() -> int:
    parser = argparse.ArgumentParser(description="Zero-Credit Quota Guard for YouTube Agent Studio.")
    parser.add_argument("--tool", "-t", required=True, help="Tool or service name (e.g. vidiq, elevenlabs, openai).")
    parser.add_argument("--action", "-a", default="default", help="Specific action or API endpoint.")
    parser.add_argument("--cost", "-c", type=int, default=None, help="Explicit credit cost (overrides tool defaults).")
    parser.add_argument("--budget", "-b", type=int, default=0, help="Allocated credit budget (default: 0).")
    parser.add_argument("--balance", type=int, default=None, help="Current known tool balance (e.g. 2).")
    parser.add_argument("--consent", choices=["yes", "no"], default="no", help="Explicit user consent to use credits.")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")
    args = parser.parse_args()

    has_consent = (args.consent.lower() == "yes")
    authorized, message, details = check_credit_authorization(
        tool=args.tool,
        action=args.action,
        cost=args.cost,
        budget=args.budget,
        balance=args.balance,
        consent=has_consent
    )

    out_payload = {
        "authorized": authorized,
        "message": message,
        "details": details
    }

    if args.json:
        print(json.dumps(out_payload, indent=2))
    else:
        if authorized:
            print(message)
        else:
            print(message, file=sys.stderr)

    return 0 if authorized else 1


if __name__ == "__main__":
    sys.exit(main())
