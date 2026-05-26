from pydantic import BaseModel

class Message(BaseModel):
    text: str
    priority: int = 1
