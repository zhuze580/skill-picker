---
name: skill-picker
description: Discover installed Codex skills and compose a prompt that invokes one or more of them for a requested task.
---

# Skill Picker

Use the bundled MCP tools when the user wants to see available skills, choose a skill, inspect its purpose, or combine multiple skills in a new task.

- Call `list_skills` to discover current skills. The list is read from the user's Codex skills directory at request time.
- Call `get_skill` when the user asks what a specific skill does.
- Call `build_skill_prompt` after the user has chosen one or more skill names and described the task. Return the generated prompt for the user to send in a new Codex conversation.
- Do not claim that this plugin directly starts a new Codex conversation. It prepares the invocation text and exposes the installed skill metadata.
