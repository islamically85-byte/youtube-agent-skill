# Installing YouTube Agent Studio — ChatGPT Edition

The ChatGPT edition of YouTube Agent Studio is designed specifically for OpenAI ChatGPT environments, featuring natural conversational intent recognition and the master orchestrator **`yt-studio`**.

---

## Understanding ChatGPT Installation Modes

ChatGPT currently supports two different installation paradigms depending on your account plan and environment:

1. **Standalone ChatGPT Skill Package (ZIP)** — Uploadable archive containing workflows, references, and Python tools.
2. **ChatGPT Developer Plugin (Manifest & Local Host)** — Standard plugin manifest architecture (`plugin.json`).

---

## Method 1: Installing the Standalone ChatGPT Skill (ZIP)

This is the recommended distribution for ChatGPT Plus, Team, Enterprise, and Edu users with access to Custom GPTs and uploadable skill capabilities:

1. **Locate the Asset**:
   - Download `release/youtube-agent-chatgpt-skill.zip` from this repository's releases or run `python3 scripts/build-releases.py` locally.
2. **Create or Edit your Custom GPT**:
   - Navigate to [ChatGPT](https://chat.openai.com) -> **Explore GPTs** -> **Create**.
   - Under the **Configure** tab:
     - **Name**: `YouTube Agent Studio`
     - **Description**: `18 specialized workflows for YouTube creators: scripting, packaging, storyboarding, multi-scene video prompting, and audience retention.`
     - **Instructions**: Reference `chatgpt/skills/yt-studio/SKILL.md` as the core orchestrator prompt.
3. **Upload Files & References**:
   - In the **Knowledge** or **Code Interpreter / Capabilities** section, upload `youtube-agent-chatgpt-skill.zip` (or the unpacked `chatgpt/references/` and `chatgpt/scripts/` folders).
   - Enable **Code Interpreter** to allow ChatGPT to execute `hookscore.py`, `title.py`, `deadair.py`, `chapters.py`, `retention.py`, and `swipe.py` deterministically.
4. **Publish**:
   - Save your Custom GPT for **Only Me**, **Anyone with a link**, or the **GPT Store**.

---

## Method 2: Installing as a ChatGPT Developer Plugin

For developers working with local development environments or enterprise plugin hosting:

1. **Review Manifest**:
   - The plugin manifest is located at `chatgpt/plugin.json`.
   - An identical copy for Codex developer environments is at `chatgpt/.codex-plugin/plugin.json`.
2. **Host Manifest**:
   - Serve `plugin.json` at `/.well-known/ai-plugin.json` on your localhost server or staging domain.
3. **Connect in ChatGPT**:
   - Open ChatGPT -> Plugin Store -> **Develop your own plugin**.
   - Enter your host URL (e.g. `localhost:3000` or `https://your-domain.com`).
   - ChatGPT will verify the manifest and activate the plugin.

---

## Method 3: Conversational Prompt Injection (No Setup Required)

If you have a standard ChatGPT account without Custom GPT creation access:
1. Open `chatgpt/skills/yt-studio/SKILL.md`.
2. Copy the text into your first ChatGPT message.
3. Chat naturally! For example:
   > *"I need a YouTube video script and packaging about why 97% of creators burn out, with 4 scenes and an upload checklist."*
4. ChatGPT will invoke the studio logic and execute the project.

---

## Troubleshooting & Verification
- **Code Interpreter Check**: Ensure Python Code Interpreter is enabled if you want ChatGPT to run exact calculations with `hookscore.py` or parse `.srt` files with `deadair.py`.
- **Offline / Free Guarantee**: No external paid API keys or YouTube account credentials are ever required for core operations.
