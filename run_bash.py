import asyncio
SCHEMA = {
    "name": "run_bash",
    "description": "Execute a bash command in the background",
    "parameters": "Bash command string"
}
async def execute(arg: str, context: dict) -> str:
    agent = context.get("agent")
    if not agent: return "Error: Agent context missing."
    return await agent.execute_command(arg)
  
