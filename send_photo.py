SCHEMA = {
    "name": "send_photo",
    "description": "Send an image to the user",
    "parameters": "Absolute path to the image"
}
async def execute(arg: str, context: dict) -> dict:
    return {"type": "yield", "data": {"type": "send_photo", "path": arg.strip(), "caption": ""}}
  
