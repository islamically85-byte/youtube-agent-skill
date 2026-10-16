# Installing YouTube Agent Studio — Claude Edition

The Claude edition of YouTube Agent Studio is compatible with **Claude Code (CLI)**, **Claude Desktop (mcp/skills)**, and conversational Claude sessions.

---

## Method 1: Claude Code Plugin Marketplace (Fastest)

To install directly as a named plugin inside Claude Code:

```bash
# Add marketplace source
/plugin marketplace add islamically85-byte/youtube-agent-skill

# Install the studio
/plugin install youtube-agent
```

Once installed, confirm all commands are available by running:
```bash
/yt-script
```

---

## Method 2: Global Skill Directory Installation

To install all 17 skills into your global Claude skills configuration:

```bash
git clone https://github.com/islamically85-byte/youtube-agent-skill.git
cd youtube-agent-skill

# Copy all skills to your user skills folder
mkdir -p ~/.claude/skills
cp -r skills/yt-* ~/.claude/skills/
```

Every skill is **100% self-contained** and includes its own zero-dependency Python tools and formula references.

---

## Method 3: Project-Local Installation

To use YouTube Agent Studio only inside a specific video project or code repository:

```bash
# From within your project root
mkdir -p .claude/skills
cp -r /path/to/youtube-agent-skill/skills/yt-* .claude/skills/
```

---

## Method 4: Offline / Single Skill File (Conversational Claude)

If you are using Claude in a browser or mobile app without Claude Code:
1. Open any specific `skills/yt-*/SKILL.md` file (e.g. `skills/yt-script/SKILL.md`).
2. Copy the entire markdown content.
3. Paste it at the top of your chat with your video idea.
4. Claude will adopt that specific skill mode for the duration of the conversation.

---

## Step 5: Creator Voice Personalization (Recommended)

To ground the skills in your authentic spoken tone, vocabulary, and audience:
```bash
mkdir -p ~/.claude/youtube
cp templates/channel-profile-template.yaml ~/.claude/youtube/channel-profile.yaml
cp templates/voice.md ~/.claude/youtube/voice.md
```
Open `~/.claude/youtube/voice.md` and customize:
- Who you are speaking to
- Phrases you actually say
- Words you never use (buzzwords)
- What you refuse to claim or promise

All 17 skills read this file automatically.
