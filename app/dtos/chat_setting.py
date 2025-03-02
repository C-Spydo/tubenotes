from pydantic import BaseModel

class ChatSetting(BaseModel):
    username: str
    character_name: str
    character_description: str
    prompt: str