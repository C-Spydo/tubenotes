from pydantic import BaseModel

class MessageRequest(BaseModel):
    chat_id: int
    prompt: str