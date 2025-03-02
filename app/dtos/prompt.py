from pydantic import BaseModel

class Prompt(BaseModel):
    chat_id: int
    prompt: str