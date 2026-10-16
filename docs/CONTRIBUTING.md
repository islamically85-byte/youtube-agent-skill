# Contributing to YouTube Agent Studio

Thank you for helping improve YouTube Agent Studio! We welcome community contributions, bug fixes, language packs, and new creator workflows.

---

## Contribution Principles
1. **Preserve MIT Licensing & Attribution**: All contributions must respect the MIT license and preserve upstream credit to Jake Schincariol.
2. **Standard Library First**: Core Python tools must remain dependency-free (no third-party pip packages required for baseline functionality).
3. **Cross-Platform Compatibility**: Code must work identically on macOS, Linux, and Windows with proper UTF-8 handling.
4. **Zero Hallucination / Ethical Integrity**: Workflows must never fabricate view counts, research papers, or clinical studies.

---

## Development Setup

```bash
# Clone the repository
git clone https://github.com/islamically85-byte/youtube-agent-skill.git
cd youtube-agent-skill

# Run the complete test suite
python3 -m unittest discover -s tests -t . -v

# Run the release build validator
python3 scripts/build-releases.py
```

---

## Adding a New Skill
1. Create `skills/yt-<new-skill>/SKILL.md` for the Claude edition.
2. Create `chatgpt/skills/yt-<new-skill>/SKILL.md` for the ChatGPT edition.
3. Ensure YAML frontmatter contains valid `name` and `description`.
4. Update `chatgpt/skills/yt-studio/SKILL.md` to declare the skill in the orchestration directory.
5. Add unit and behavioral tests in `tests/`.
6. Update `.claude-plugin/plugin.json`, `chatgpt/plugin.json`, and `scripts/build-releases.py`.

---

## Pull Request Guidelines
- Create a dedicated feature branch (e.g. `feature/my-enhancement`).
- Ensure all 56+ tests pass without warnings.
- Keep commits descriptive and atomic.
- Open a Pull Request against the `main` branch.
