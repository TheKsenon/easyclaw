import os
from pathlib import Path
SCHEMA = {
    "name": "save_macro",
    "description": "Save a custom Python tool to the macros directory",
    "parameters": "Valid Python code containing SCHEMA dict and async execute(arg, context) function"
}
async def execute(arg: str, context: dict) -> str:
    import re
    name_match = re.search(r'"name":\s*"([^"]+)"', arg)
    if not name_match: return "Error: Could not find tool name in SCHEMA."
    filename = f"{name_match.group(1)}.py"
    macros_dir = Path.home() / ".easyclaw" / "macros"
    macros_dir.mkdir(parents=True, exist_ok=True)
    filepath = macros_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(arg)
    context["agent"].tool_manager.reload_tools()
    return f"Macro {filename} saved and loaded successfully."
  
