from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


SKILLS_ROOT = Path.home() / ".codex" / "skills"


def metadata(path: Path) -> dict:
    text = (path / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    parts = text.split("---", 2)
    front = parts[1] if len(parts) == 3 else ""

    def field(name: str) -> str:
        match = re.search(rf"^{re.escape(name)}:\s*(.+)$", front, re.MULTILINE)
        return match.group(1).strip().strip("\"'") if match else ""

    return {
        "name": field("name") or path.name,
        "description": field("description") or "No description provided.",
        "path": str(path),
    }


def discover() -> list[dict]:
    if not SKILLS_ROOT.is_dir():
        return []
    found = []
    for marker in SKILLS_ROOT.rglob("SKILL.md"):
        try:
            found.append(metadata(marker.parent))
        except OSError:
            continue
    return sorted(found, key=lambda item: item["name"].casefold())


def text_result(value) -> dict:
    return {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False, indent=2)}]}


def error(message: str) -> dict:
    return {"content": [{"type": "text", "text": message}], "isError": True}


def call_tool(name: str, arguments: dict) -> dict:
    skills = discover()
    if name == "list_skills":
        query = str(arguments.get("query", "")).strip().casefold()
        if query:
            skills = [item for item in skills if query in (item["name"] + " " + item["description"]).casefold()]
        return text_result({"count": len(skills), "skills": skills})
    if name == "get_skill":
        wanted = str(arguments.get("name", "")).strip().casefold()
        match = next((item for item in skills if item["name"].casefold() == wanted), None)
        if not match:
            return error(f"Skill not found: {arguments.get('name', '')}")
        try:
            instructions = (Path(match["path"]) / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return error(f"Could not read skill: {exc}")
        return text_result({**match, "instructions": instructions})
    if name == "build_skill_prompt":
        names = arguments.get("skill_names", [])
        if isinstance(names, str):
            names = [names]
        selected = [item for item in skills if item["name"] in names]
        missing = [name for name in names if name not in {item["name"] for item in selected}]
        task = str(arguments.get("task", "")).strip()
        if not selected:
            return error("Choose at least one installed skill.")
        if not task:
            return error("Describe the task before building a prompt.")
        prompt = f"请使用 {' 和 '.join('`' + item['name'] + '`' for item in selected)} 完成以下任务：\n\n{task}"
        return text_result({"prompt": prompt, "skills": selected, "missing": missing})
    return error(f"Unknown tool: {name}")


TOOLS = [
    {
        "name": "list_skills",
        "description": "List installed Codex skills, optionally filtered by name or description.",
        "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}},
    },
    {
        "name": "get_skill",
        "description": "Read the metadata and SKILL.md instructions for one installed skill.",
        "inputSchema": {"type": "object", "required": ["name"], "properties": {"name": {"type": "string"}}},
    },
    {
        "name": "build_skill_prompt",
        "description": "Build a prompt that invokes one or more installed skills for a concrete task.",
        "inputSchema": {
            "type": "object",
            "required": ["skill_names", "task"],
            "properties": {
                "skill_names": {"type": "array", "items": {"type": "string"}},
                "task": {"type": "string"},
            },
        },
    },
]


def reply(request: dict) -> dict | None:
    request_id = request.get("id")
    method = request.get("method")
    if method == "notifications/initialized" or method == "notifications/cancelled":
        return None
    if method == "initialize":
        result = {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "skill-picker", "version": "0.1.0"},
        }
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        params = request.get("params", {})
        result = call_tool(str(params.get("name", "")), params.get("arguments") or {})
    else:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def main() -> None:
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = reply(request)
            if response is not None:
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except Exception as exc:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(exc)}}, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
