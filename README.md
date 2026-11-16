# Skill Picker

A Codex plugin that discovers installed skills, shows their instructions, and builds prompts that invoke selected skills for a task.

## Features

- `list_skills`: list installed skills, optionally filtered by a search phrase.
- `get_skill`: inspect a skill's metadata and `SKILL.md` instructions.
- `build_skill_prompt`: create a prompt for one or more skills and a concrete task.

The plugin reads skills from `%USERPROFILE%/.codex/skills` on Windows or `~/.codex/skills` on macOS and Linux. It discovers skills on each tool call, so newly installed skills appear without rebuilding the plugin. Python 3 must be available as `python` on `PATH` for the bundled stdio MCP server.

## Install from Codex

Add this repository as a plugin marketplace:

```text
/plugins
```

In the plugin marketplace UI, choose **Add marketplace**, then enter:

```text
https://github.com/zhuze580/skill-picker
```

Find **Skill Picker** in the marketplace and install it. Restart Codex if the plugin does not appear immediately.

If your Codex version supports the CLI marketplace commands, you can also run:

```bash
codex plugin marketplace add zhuze580/skill-picker
codex plugin install skill-picker@skill-picker-marketplace
```

## Local development

The plugin package is in `plugins/skill-picker/`. The repository marketplace manifest is `.agents/plugins/marketplace.json`.

The root-level `skills/skill-picker/SKILL.md` copy is included for Agent Skills indexes such as SkillsMP. The plugin package contains the same skill at `plugins/skill-picker/skills/skill-picker/SKILL.md`.

## SkillsMP

This public repository is formatted for SkillsMP indexing. Search for `skill-picker` on [SkillsMP](https://skillsmp.com/) after its next index update. Indexing is controlled by SkillsMP, so a new repository may take time to appear.

To test the MCP server directly, run it with Python and send newline-delimited MCP JSON-RPC requests on standard input:

```bash
python plugins/skill-picker/server/skill_picker_mcp.py
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
