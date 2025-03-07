from pydantic import BaseModel

class ChatSetting(BaseModel):
    username: str
    prompt: str
    stock: str