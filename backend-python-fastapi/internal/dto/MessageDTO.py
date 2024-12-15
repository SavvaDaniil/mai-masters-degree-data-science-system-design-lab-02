from pydantic import BaseModel

class MessageNewDTO(BaseModel):
    content: str