from pydantic import BaseModel
from typing import Optional

class QAPair(BaseModel):
    question: str
    answer: str

class QAPairUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None