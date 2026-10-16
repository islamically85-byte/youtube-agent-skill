# Platform Compatibility & Architectural Comparison

YouTube Agent Studio v2.0 is engineered with dual native support for both **Anthropic Claude** and **OpenAI ChatGPT**, while preserving complete offline capability and zero-dependency portability.

---

## Feature & Platform Comparison Matrix

| Capability / Dimension | Claude Edition | ChatGPT Edition | Notes |
|---|---|---|---|
| **Primary Interaction Mode** | Slash Commands (`/yt-script`, `/yt-package`, etc.) | Conversational Intent & Master Orchestrator (`yt-studio`) | Both editions recognize intent; Claude preserves slash command aliases. |
| **Number of Workflows** | 17 Dedicated Skills | 18 Workflows (17 Specialized + `yt-studio` Orchestrator) | 100% functional parity across all creator workflows. |
| **Python Execution** | Local Shell / Terminal via Bash | Code Interpreter (Python sandbox) or Local Scripts | Standard Library only; zero external pip dependencies required. |
| **Pakistani Urdu Support** | Yes (Native Urdu Script `اردو`) | Yes (Native Urdu Script `اردو`) | Cultural idioms, ~130 WPM pacing, no Roman Urdu unless asked. |
| **Manifest Format** | `.claude-plugin/plugin.json`, `marketplace.json` | `chatgpt/plugin.json`, `.codex-plugin/plugin.json` | Follows official platform packaging specifications. |
| **Packaging Deliverable** | `youtube-agent-claude.zip` | `youtube-agent-chatgpt-skill.zip`, `youtube-agent-chatgpt-plugin.zip` | Independently distributable and verified. |
| **Offline Capability** | 100% Free & Offline-First | 100% Free & Offline-First | No paid API keys or external subscriptions required for core features. |

---

## Python Helper Portability

All six core tools (`transcript.py`, `hookscore.py`, `title.py`, `deadair.py`, `chapters.py`, `retention.py`, `swipe.py`) are strictly implemented using the **Python Standard Library**:
- **Python Version**: Tested on Python 3.10, 3.11, 3.12, and 3.13.
- **Operating Systems**: macOS (Darwin), Linux (Ubuntu/Debian/Fedora), and Windows (10/11 with UTF-8 consoles).
- **Encoding Safety**: Input files and terminal output are handled with explicit `utf-8` and `utf-8-sig` encodings, ensuring non-Latin scripts (e.g. Urdu, Arabic, Hindi, Japanese) do not trigger encoding errors.

---

## Tool Degradation & External Integrations

YouTube Agent Studio follows a strict **Graceful Degradation Policy**:
- **Image Generation**: If DALL-E, Midjourney, or an MCP image tool is connected, it is used only when explicitly requested. Otherwise, the tool outputs high-fidelity visual prompts and negative constraints.
- **Video Rendering**: If a local rendering tool or video generation API is absent, the system delivers structured scene-by-scene prompts with character consistency sheets.
- **YouTube Publication**: The toolkit formats upload-ready description blocks, verified chapters, and tags, but never fabricates autonomous video uploads.
