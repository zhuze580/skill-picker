# Skill Picker plugin

This local Codex plugin exposes the installed skills under `%USERPROFILE%/.codex/skills` through a small stdio MCP server.

Tools:

- `list_skills`: list all skills, optionally filtered by a search phrase.
- `get_skill`: read the metadata and instructions for one installed skill.
- `build_skill_prompt`: create a prompt that invokes one or more skills for a concrete task.

The server discovers skills on every tool call, so skills installed after the plugin are included without rebuilding it.
