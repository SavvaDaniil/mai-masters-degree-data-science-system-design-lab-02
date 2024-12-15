from pydantic import BaseModel
from dataclasses import dataclass

class MessageQueueViewModel(BaseModel):
    content: str
    creation_date: str