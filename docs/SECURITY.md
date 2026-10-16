# Security, Privacy & Integrity Policy

## 1. Offline-First & Zero Credential Requirement
YouTube Agent Studio does not require, store, or transmit YouTube account passwords, OAuth access tokens, refresh tokens, client secrets, or private API keys.

- All core utilities run locally via Python Standard Library.
- No telemetry, analytics pings, or user surveillance trackers are embedded.
- Creator transcripts, video drafts, and audience retention CSVs are processed locally on your machine.

---

## 2. Passive Transcript & Text Processing (Untrusted Input)
Transcripts and comments downloaded from third-party sources or submitted by unknown viewers must be treated as **untrusted input**.

- The Python parsing engine (`transcript.py`, `deadair.py`) processes input purely as string data.
- **Never executes shell commands** from parsed subtitle text.
- Protected against regex exponential backoff (ReDoS) and directory traversal via sanitized path handling.
- Immune to prompt injection payloads embedded in subtitle cues (tested in `tests/evals/test_behavioral_evals.py`).

---

## 3. Publication Transparency & Disclaimers
YouTube Agent Studio will never attempt to publish, upload, or alter videos on a YouTube channel autonomously without an explicit, authenticated tool connected by the creator and verified with human confirmation.

- No automated deletion of comments or videos.
- No automated publishing of unreviewed drafts.
- Every workflow concludes with a creator checkpoint: **"Ship it, or change it?"**

---

## 4. Reporting Security Vulnerabilities
If you discover a security vulnerability or unexpected behavior:
1. Please open an issue on the repository or contact `errorcodelagfix@gmail.com`.
2. Do not publicly disclose sensitive security exploits until a remediation patch is deployed.
