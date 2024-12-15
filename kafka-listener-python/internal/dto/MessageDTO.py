from pydantic import BaseModel


class MessageFromQueueDTO(BaseModel):
    content: str
    creation_date: str