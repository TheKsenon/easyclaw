SCHEMA = {
    "name": "send_file",
    "description": "Send a file to the user",
    "parameters": "Absolute path to the file"
}
async def execute(arg: str, context: dict) -> dict:
    return {"type": "yield", "data": {"type": "send_file", "path": arg.strip(), "caption": ""}}
  
